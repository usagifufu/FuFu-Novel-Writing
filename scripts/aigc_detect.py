#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AI 文本检测助手（融合 aigc-detector 能力 + 中文增强规则）。

来源项目: https://github.com/hoyo0210/aigc-detector
- 本地规则引擎：免 API，逐行标记 AI 痕迹（修复了原项目按空格分词的
  中文失效问题，改用 n-gram 滑窗；并补充排比三连、"连…都"、"不是A是B"、
  句首代词密度、比喻密度、高频词重复等中文 AI 指纹）。
- Qwen 深度检测：可选，调用 DashScope 大模型做文本来源判别
  （需设置环境变量 DASHSCOPE_API_KEY；无 key 时自动降级为纯规则引擎）。

用法:
    python aigc_detect.py <文件> [--html 报告.html] [--qwen] [--json]
    python aigc_detect.py --stdin < 稿件.txt [--qwen]

输出:
    行级命中列表（行号/类型/原文/理由）+ 指纹分类统计；
    --html 生成带高亮标记的交互式报告；
    --json 输出机器可读 JSON。
"""

import argparse
import json
import os
import re
import sys
import uuid

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ---------------------------------------------------------------- 规则引擎

# 正式表达 / 机械连接（原项目 formal_patterns + 网文常见 AI 连接词）
FORMAL_PATTERNS = [
    (r"因此[，,]", "formal_connector", "正式连接词（因此）"),
    (r"此外[，,]", "formal_connector", "正式连接词（此外）"),
    (r"综上所述[，,]", "formal_conclusion", "正式总结（综上所述）"),
    (r"总而言之[，,]", "formal_conclusion", "正式总结（总而言之）"),
    (r"值得注意的是[，,]", "formal_attention", "正式提示（值得注意的是）"),
    (r"需要强调的是[，,]", "formal_emphasis", "正式强调（需要强调的是）"),
    (r"根据以上[，,]", "formal_reference", "正式引用（根据以上）"),
    (r"不得不说[，,]", "formal_connector", "机械转折（不得不说）"),
    (r"换句话说[，,]", "formal_connector", "机械转折（换句话说）"),
    (r"首先[，,].{0,30}其次[，,]", "sequential_connector", "序列连接（首先…其次…）"),
]

# 复杂句式 / 平衡句（原项目 complex_patterns + 中文 AI 指纹）
COMPLEX_PATTERNS = [
    (r"[^，,。！？\n]{0,12}的[^，,。！？\n]{0,12}的[^，,。！？\n]{0,12}的", "complex_modifiers", "多重'的'字修饰结构"),
    (r"通过[^，,。！？\n]{0,15}从而", "causal_chain", "因果链（通过…从而…）"),
    (r"以及[^，,。！？\n]{0,10}以及", "parallel_structure", "多重'以及'并列"),
    (r"不仅[^，,。！？\n]{0,12}[，,][^，,。！？\n]{0,12}而且", "parallel_structure", "递进并列（不仅…而且…）"),
    (r"不是[^，,。！？\n]{1,14}，[^，,。！？\n]{0,8}而是", "balance_sentence", "平衡句（不是A，而是B）"),
    (r"连[^，,。！？\n]{1,14}都", "even_structure", "'连…都'强调句式"),
    (r"既[^，,。！？\n]{1,12}又[^，,。！？\n]{1,12}", "balance_sentence", "并列句（既…又…）"),
    (r"与其[^，,。！？\n]{1,12}不如[^，,。！？\n]{1,12}", "balance_sentence", "选择句（与其…不如…）"),
]

# 空泛总结 / 万金油
FLUFF_PATTERNS = [
    (r"这一刻[，,]?仿佛", "fluff", "空泛总结（这一刻仿佛）"),
    (r"仿佛一切", "fluff", "空泛总结（仿佛一切）"),
    (r"一切都(结束了|开始|变了)", "fluff", "空泛总结（一切都…）"),
    (r"岁月静好", "fluff", "模板化（岁月静好）"),
    (r"望向远方|看向远方", "fluff", "万金油动作（望向远方）"),
    (r"深吸一口气|长舒一口气", "fluff", "万金油动作（深吸/长舒一口气）"),
    (r"嘴角勾起[^，,。！？\n]{0,6}笑|露出一抹[^，,。！？\n]{0,6}笑", "fluff", "万金油神态（嘴角勾起…笑）"),
]

# 比喻词（统计用，>阈值告警）
METAPHOR_WORDS = re.compile(r"像.{0,4}(一样|一般|似的)|仿佛|如同|宛如|犹如|好似|好像是|就像")

# 句首代词（统计用，>阈值告警）
PRONOUN_STARTS = ("他", "她", "我", "你", "它")

# 常见停用词（高频词重复统计时排除）
STOPWORDS = set(
    "的一了是我不在有人这他上个来们到说地也要与你会子那得去看".strip()
)


def _gen_id():
    return str(uuid.uuid4())


def _ngrams(text, n):
    """中文 2/3-gram 滑窗，用于行内重复检测。"""
    out = []
    for i in range(len(text) - n + 1):
        out.append(text[i:i + n])
    return out


def mark_ai_traces(text: str) -> dict:
    """逐行标记 AI 痕迹。返回与 aigc-detector 相同的结构。"""
    original_text = text.rstrip()
    lines = original_text.split("\n")
    all_traces = []
    marked_lines = []

    # 全文级统计
    metaphor_count = len(METAPHOR_WORDS.findall(original_text))
    total_chars = len(original_text.replace("\n", ""))
    word_freq = {}
    phrase_freq = {}
    for i in range(len(original_text) - 1):
        w = original_text[i:i + 2]
        if all("\u4e00" <= c <= "\u9fff" for c in w) and w not in STOPWORDS:
            word_freq[w] = word_freq.get(w, 0) + 1
    # 全文 4-gram 短语频率（全汉字才算，过滤标点空格碎片）
    for i in range(len(original_text) - 3):
        g = original_text[i:i + 4]
        if all("\u4e00" <= c <= "\u9fff" for c in g):
            phrase_freq[g] = phrase_freq.get(g, 0) + 1

    # 句首代词连续行统计
    pronoun_runs = []
    run = 0
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(PRONOUN_STARTS):
            run += 1
        else:
            if run >= 3:
                pronoun_runs.append(run)
            run = 0
    if run >= 3:
        pronoun_runs.append(run)

    for line_idx, line in enumerate(lines):
        line_traces = []
        line_start = sum(len(lines[i]) + 1 for i in range(line_idx))
        stripped = line.strip()
        line_no = line_idx + 1

        if not stripped:
            marked_lines.append(line)
            continue

        # 1) 行内重复短语（4-gram 全汉字，同一行出现≥2次才算）
        grams = _ngrams(stripped, 4)
        seen_pos = {}
        for gi, g in enumerate(grams):
            if not all("\u4e00" <= c <= "\u9fff" for c in g):
                continue
            if g in seen_pos:
                rel = stripped.find(g, seen_pos[g][-1] + 4)
                if rel != -1:
                    line_traces.append({
                        "id": _gen_id(),
                        "start": line_start + rel,
                        "end": line_start + rel + 4,
                        "type": "word_repetition",
                        "reason": f"短语'{g}'在行内重复，AI 生成特征",
                    })
                    break
            else:
                seen_pos[g] = []
            seen_pos[g].append(gi)

        # 2) 行过长
        if len(stripped) > 80:
            line_traces.append({
                "id": _gen_id(),
                "start": line_start,
                "end": line_start + len(line),
                "type": "long_line",
                "reason": f"行过长（{len(stripped)} 字），缺人类自然停顿",
            })

        # 3) 正式表达
        for pattern, ttype, reason in FORMAL_PATTERNS:
            for m in re.finditer(pattern, stripped):
                line_traces.append({
                    "id": _gen_id(),
                    "start": line_start + m.start(),
                    "end": line_start + m.end(),
                    "type": ttype,
                    "reason": reason,
                })

        # 4) 复杂句式 / 平衡句
        for pattern, ttype, reason in COMPLEX_PATTERNS:
            for m in re.finditer(pattern, stripped):
                line_traces.append({
                    "id": _gen_id(),
                    "start": line_start + m.start(),
                    "end": line_start + m.end(),
                    "type": ttype,
                    "reason": f"{reason}：{m.group()[:24]}…",
                })

        # 5) 空泛总结 / 万金油
        for pattern, ttype, reason in FLUFF_PATTERNS:
            for m in re.finditer(pattern, stripped):
                line_traces.append({
                    "id": _gen_id(),
                    "start": line_start + m.start(),
                    "end": line_start + m.end(),
                    "type": ttype,
                    "reason": reason,
                })

        # 6) 行内比喻密度（单行 ≥2 个比喻词）
        line_metaphors = METAPHOR_WORDS.findall(stripped)
        if len(line_metaphors) >= 2:
            line_traces.append({
                "id": _gen_id(),
                "start": line_start,
                "end": line_start + len(line),
                "type": "metaphor_dense",
                "reason": f"单行 {len(line_metaphors)} 处比喻，疑似堆砌",
            })

        # 标记行（倒序插入避免偏移）
        marked = line
        for t in sorted(line_traces, key=lambda x: x["start"], reverse=True):
            rs = t["start"] - line_start
            re_ = t["end"] - line_start
            if 0 <= rs < len(marked) and 0 <= re_ <= len(marked):
                marked = (
                    f"{marked[:rs]}<mark class='ai-trace {t['type']}' "
                    f"data-trace-id='{t['id']}'>{marked[rs:re_]}</mark>{marked[re_:]}"
                )

        marked_lines.append(marked)
        for t in line_traces:
            t["line"] = line_no
        all_traces.extend(line_traces)

    # 全文级指纹（不是行级命中，单独汇报）
    global_flags = []
    if metaphor_count >= 3:
        global_flags.append({
            "type": "metaphor_high",
            "detail": f"全文比喻 {metaphor_count} 处（阈值 3），比喻堆砌是强 AI 指纹",
        })
    if pronoun_runs:
        global_flags.append({
            "type": "pronoun_run",
            "detail": f"连续 3+ 行以'他/她/我'开头的段落 {len(pronoun_runs)} 处，"
                      f"最长连续 {max(pronoun_runs)} 行，句首代词密度偏高",
        })
    top_words = sorted(
        ((w, c) for w, c in word_freq.items() if c >= 8),
        key=lambda x: -x[1],
    )[:10]
    if top_words:
        global_flags.append({
            "type": "word_freq",
            "detail": "高频二字词："
                      + "、".join(f"{w}×{c}" for w, c in top_words[:5]),
        })
    top_phrases = sorted(
        ((g, c) for g, c in phrase_freq.items() if c >= 4),
        key=lambda x: -x[1],
    )[:10]
    if top_phrases:
        global_flags.append({
            "type": "phrase_freq",
            "detail": "高频四字短语："
                      + "、".join(f"{g}×{c}" for g, c in top_phrases[:5])
                      + "（整段复读同一短语，AI 重复指纹）",
        })

    n = len(all_traces)
    explanation = (
        f"发现 {n} 个潜在 AI 痕迹，"
        f"全文比喻 {metaphor_count} 处。"
        f"{'（仅规则引擎，未配置 DASHSCOPE_API_KEY，Qwen 深度检测已跳过）' if not os.getenv('DASHSCOPE_API_KEY') else ''}"
    )

    return {
        "original_text": original_text,
        "marked_text": "\n".join(marked_lines),
        "traces": all_traces,
        "global_flags": global_flags,
        "explanation": explanation,
    }


# ---------------------------------------------------------------- Qwen 深度检测

def detect_with_qwen(text: str) -> dict:
    """调用 DashScope Qwen 做深度检测，返回 7 字段结果。
    无 API key 时抛 RuntimeError。"""
    key = os.getenv("DASHSCOPE_API_KEY", "")
    if not key:
        raise RuntimeError("DASHSCOPE_API_KEY 未配置")

    try:
        import dashscope
        from dashscope import Generation
    except ImportError:
        raise RuntimeError("缺少依赖 dashscope，请先执行: pip install dashscope")

    model = os.getenv("QWEN_MODEL", "qwen-plus")
    prompt = (
        "分析这段文本是否由AI生成，返回JSON格式：\n\n"
        f"{text.strip()[:7000]}\n\n"
        "JSON格式要求（严格遵守）：\n"
        '{ "label": "ai 或 human 或 uncertain", "score": 0到1之间的数字, '
        '"confidence": "high 或 medium 或 low", "rationale": "简短判断理由", '
        '"detailed_analysis": "详细分析文字", '
        '"key_indicators": ["指标1", "指标2"], "methodology": "分析方法说明" }\n\n'
        "重要：只返回JSON，不要添加任何其他文字或解释！"
    )
    dashscope.api_key = key
    resp = Generation.call(
        model=model,
        messages=[
            {"role": "system", "content": "你是一个AI文本检测分析器，只能输出JSON格式的结果。严格按照指定格式返回，不要添加任何其他内容。"},
            {"role": "user", "content": prompt},
        ],
        temperature=float(os.getenv("DETECT_TEMPERATURE", "0.2")),
        result_format="message",
        timeout=float(os.getenv("QWEN_TIMEOUT", "15")),
    )
    raw = resp.get("output", {}).get("choices", [{}])[0].get("message", {}).get("content", "")
    raw = raw.strip()
    if raw.startswith("```json"):
        raw = raw[7:]
    if raw.startswith("```"):
        raw = raw[3:]
    if raw.endswith("```"):
        raw = raw[:-3]
    raw = raw.strip()
    start = raw.find("{")
    end = raw.rfind("}")
    if start != -1 and end != -1:
        raw = raw[start:end + 1]
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {"label": "uncertain", "score": 0.5, "confidence": "low",
                "rationale": f"Qwen 返回解析失败", "detailed_analysis": raw[:200],
                "key_indicators": [], "methodology": "Qwen 深度检测"}
    label = str(data.get("label", "uncertain"))
    if label not in ("ai", "human", "uncertain"):
        label = "uncertain"
    score = max(0.0, min(1.0, float(data.get("score", 0.5))))
    conf = str(data.get("confidence", "medium"))
    if conf not in ("high", "medium", "low"):
        conf = "medium"
    return {
        "label": label,
        "score": score,
        "confidence": conf,
        "rationale": str(data.get("rationale", "")),
        "detailed_analysis": str(data.get("detailed_analysis", "")),
        "key_indicators": [str(x) for x in data.get("key_indicators", []) if str(x).strip()],
        "methodology": str(data.get("methodology", "Qwen 深度检测")),
    }


# ---------------------------------------------------------------- 输出

def render_html(result: dict, qwen_result: dict | None, source: str) -> str:
    traces = result["traces"]
    counts = {}
    for t in traces:
        counts[t["type"]] = counts.get(t["type"], 0) + 1
    type_names = {
        "word_repetition": "词语重复", "long_line": "行过长", "formal_connector": "正式连接词",
        "formal_conclusion": "正式总结", "formal_attention": "正式提示", "formal_emphasis": "正式强调",
        "formal_reference": "正式引用", "sequential_connector": "序列连接",
        "complex_modifiers": "多重'的'修饰", "causal_chain": "因果链",
        "parallel_structure": "并列结构", "balance_sentence": "平衡句",
        "even_structure": "'连…都'句式", "fluff": "空泛总结", "metaphor_dense": "比喻堆砌",
    }
    qwen_html = ""
    if qwen_result:
        label_map = {"ai": "🤖 AI 生成", "human": "🧑 人类写作", "uncertain": "❓ 不确定"}
        qwen_html = f"""
        <div class="qwen">
          <h2>Qwen 深度检测</h2>
          <div class="qwen-label">{label_map.get(qwen_result['label'], qwen_result['label'])}
            <span class="score">分数 {qwen_result['score']:.2f} · 置信度 {qwen_result['confidence']}</span></div>
          <p><b>理由：</b>{qwen_result['rationale']}</p>
          <p><b>分析：</b>{qwen_result['detailed_analysis']}</p>
          <p><b>关键指标：</b>{'、'.join(qwen_result['key_indicators']) if qwen_result['key_indicators'] else '无'}</p>
        </div>"""
    flags_html = ""
    if result.get("global_flags"):
        items = "".join(
            f"<li><b>{f['type']}</b>：{f['detail']}</li>" for f in result["global_flags"]
        )
        flags_html = f"<div class='flags'><h2>全文级指纹</h2><ul>{items}</ul></div>"
    stats = "".join(
        f"<span class='stat'><b>{type_names.get(k, k)}</b> {v}</span>"
        for k, v in sorted(counts.items(), key=lambda x: -x[1])
    ) or "<p>未发现行级命中。</p>"
    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>AI 检测报告</title>
<style>
  body {{ font-family: "Microsoft YaHei", sans-serif; max-width: 900px; margin: 24px auto; padding: 0 16px; background: #fff; color: #222; }}
  h1 {{ font-size: 20px; border-bottom: 2px solid #f0f0f0; padding-bottom: 8px; }}
  .stats {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 12px 0; }}
  .stat {{ background: #f6f6f6; padding: 6px 12px; border-radius: 6px; font-size: 13px; }}
  .qwen, .flags {{ background: #fafafa; border: 1px solid #eee; border-radius: 8px; padding: 12px 16px; margin: 12px 0; }}
  .qwen-label {{ font-size: 18px; font-weight: bold; }}
  .score {{ font-size: 13px; color: #666; margin-left: 8px; }}
  .text {{ white-space: pre-wrap; line-height: 1.9; font-size: 15px; background: #fffdf5; border: 1px solid #eee; border-radius: 8px; padding: 16px; }}
  mark {{ background: #ffe08a; border-radius: 3px; padding: 0 2px; cursor: help; }}
  mark.word_repetition {{ background: #ffb3b3; }}
  mark.long_line {{ background: #ffd1dc; }}
  mark.balance_sentence, mark.even_structure {{ background: #b3e5fc; }}
  mark.complex_modifiers, mark.causal_chain, mark.parallel_structure {{ background: #c8e6c9; }}
  mark.formal_connector, mark.formal_conclusion, mark.formal_attention, mark.formal_emphasis, mark.formal_reference, mark.sequential_connector {{ background: #fff59d; }}
  mark.fluff {{ background: #d1c4e9; }}
  mark.metaphor_dense {{ background: #ffcc80; }}
  .legend {{ font-size: 12px; color: #666; margin: 8px 0; }}
</style></head><body>
<h1>🔍 AI 文本检测报告</h1>
<p>来源：{source} · 命中 {len(traces)} 处 · {result['explanation']}</p>
{qwen_html}
{flags_html}
<div class="stats">{stats}</div>
<div class="legend">颜色：<mark>词语重复</mark> <mark>行过长</mark> <mark>平衡句/'连…都'</mark> <mark>复杂句式</mark> <mark>正式表达</mark> <mark>空泛总结</mark> <mark>比喻堆砌</mark></div>
<div class="text">{result['marked_text']}</div>
</body></html>"""


def main():
    ap = argparse.ArgumentParser(description="AI 文本检测助手（aigc-detector 融合版）")
    ap.add_argument("file", nargs="?", help="要检测的文本文件（缺省用 --stdin）")
    ap.add_argument("--stdin", action="store_true", help="从标准输入读取文本")
    ap.add_argument("--html", metavar="OUT", help="输出带高亮标记的 HTML 报告")
    ap.add_argument("--qwen", action="store_true", help="追加 Qwen 深度检测（需 DASHSCOPE_API_KEY）")
    ap.add_argument("--json", action="store_true", help="输出机器可读 JSON")
    args = ap.parse_args()

    if args.stdin:
        text = sys.stdin.read()
        source = "<stdin>"
    elif args.file:
        with open(args.file, encoding="utf-8", errors="replace") as f:
            text = f.read()
        source = args.file
    else:
        ap.error("需要提供文件路径或 --stdin")

    result = mark_ai_traces(text)

    qwen_result = None
    if args.qwen:
        try:
            qwen_result = detect_with_qwen(text)
        except RuntimeError as e:
            print(f"[降级] Qwen 深度检测跳过：{e}", file=sys.stderr)

    if args.json:
        out = {"source": source, "rules": result, "qwen": qwen_result}
        json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
        return

    # 终端输出
    print(f"=== AI 检测报告: {source} ===")
    print(result["explanation"])
    if qwen_result:
        print(f"[Qwen] label={qwen_result['label']} score={qwen_result['score']:.2f} "
              f"confidence={qwen_result['confidence']}")
        print(f"       理由: {qwen_result['rationale']}")
        print(f"       指标: {'、'.join(qwen_result['key_indicators'])}")
    if result.get("global_flags"):
        print("\n--- 全文级指纹 ---")
        for f in result["global_flags"]:
            print(f"  [{f['type']}] {f['detail']}")
    if result["traces"]:
        print("\n--- 行级命中 ---")
        for t in result["traces"]:
            print(f"  L{t['line']:>3d} {t['type']:24s} {t['reason']}")
    else:
        print("\n未发现行级命中。")

    if args.html:
        with open(args.html, "w", encoding="utf-8") as f:
            f.write(render_html(result, qwen_result, source))
        print(f"\nHTML 报告已写出: {args.html}")


if __name__ == "__main__":
    main()
