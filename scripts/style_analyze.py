#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""统计中文文本的文风特征，生成文风分析报告（纯标准库）。

用法:
    python style_analyze.py <文件或glob>... [--name 档案名] [--json]
    python style_analyze.py 样本/*.md > 文风报告.md

只做确定性统计：句长、段落、标点、对话密度、高频双字、语气词、设问/排比等。
语境判断与风格提炼由 Codex 结合 references/style-learning.md 完成。
"""

import argparse
import glob
import json
import re
import sys
from collections import Counter

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


# 高频虚字（统计特色双字时排除）
STOP_CHARS = set(
    "的了是在我有他不这和那着也一个就以吧吗呢啊哦嗯呀哟哈啦嘛哎咯喂诶"
    "这那又还都只便因为与及或而所被把向从对到让说想看去听来出上中里下外"
    "么什之其于等得很"
)

SENT_SPLIT = re.compile(r"(?<=[。！？…])")
LE_END_RX = re.compile(r"了[。！？…]?$")
QUOTE_CHARS = "「」“”\"\""
CN_PAIR_RX = re.compile(r"[\u4e00-\u9fff]")
DIALOG_RX = re.compile(r"「[^」]*」|“[^”]*”|\"[^\"]*\"")
RHET_RULES = {
    "设问（难道…吗）": re.compile(r"难道[^。！？\n]{0,14}吗"),
    "反问（难道/岂/何曾）": re.compile(r"难道|岂非|岂能|何曾|怎能|岂不"),
    "排比（不是…不是…而是）": re.compile(r"不是[^，。]{1,14}，不是[^，。]{1,14}，而是"),
    "排比（无论×3）": re.compile(r"无论[^，。]{1,12}[，,]，无论[^，。]{1,12}[，,]，无论"),
}
MOOD_WORDS = ["吧", "吗", "呢", "啊", "哦", "嗯", "呀", "哈", "啦", "嘛", "哟", "诶", "哎", "咯"]
REDUP_RX = re.compile(r"([\u4e00-\u9fff])\1")


def clean_text(raw: str) -> str:
    # 去掉 Markdown 语法噪音，保留正文
    raw = re.sub(r"^#{1,6}\s.*$", "", raw, flags=re.M)
    raw = re.sub(r"^\s*[-*+]\s", "", raw, flags=re.M)
    raw = re.sub(r"`[^`]*`", "", raw)
    raw = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", raw)
    raw = re.sub(r"\[[^\]]*\]\([^)]*\)", "", raw)
    return raw


def analyze_file(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        text = clean_text(fh.read())
    total_chars = len(text)
    no_space = len(re.sub(r"\s", "", text))

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    par_lens = [len(re.sub(r"\s", "", p)) for p in paragraphs]

    # 句子切分
    raw_sents = [s.strip() for s in SENT_SPLIT.split(text) if s.strip()]
    sents = [re.sub(r"\s", "", s) for s in raw_sents if len(re.sub(r"\s", "", s)) > 0]
    sent_lens = [len(s) for s in sents]
    avg_sent = sum(sent_lens) / len(sent_lens) if sent_lens else 0
    short_rate = sum(1 for n in sent_lens if n <= 10) / len(sent_lens) if sent_lens else 0
    mid_rate = sum(1 for n in sent_lens if 11 <= n <= 20) / len(sent_lens) if sent_lens else 0
    long_rate = sum(1 for n in sent_lens if 21 <= n <= 40) / len(sent_lens) if sent_lens else 0
    xlong_rate = sum(1 for n in sent_lens if n > 40) / len(sent_lens) if sent_lens else 0
    le_rate = sum(1 for s in sents if LE_END_RX.search(s)) / len(sents) if sents else 0

    # 标点
    punc_counts = Counter()
    for ch in text:
        if ch in "，。！？；：、——…“”‘’「」（）《》":
            punc_counts[ch] += 1
    question_rate = punc_counts.get("？", 0) + punc_counts.get("?", 0)
    exclaim_rate = punc_counts.get("！", 0) + punc_counts.get("!", 0)
    per_k = 1000.0 / no_space if no_space else 0

    # 对话密度
    dialog_chars = sum(len(m) for m in DIALOG_RX.findall(text))
    dialog_rate = dialog_chars / no_space if no_space else 0
    dialog_par_rate = (
        sum(1 for p in paragraphs if DIALOG_RX.search(p)) / len(paragraphs) if paragraphs else 0
    )

    # 高频双字（只取中文相邻对）
    pairs = Counter()
    cjk = "".join(CN_PAIR_RX.findall(text))
    for i in range(len(cjk) - 1):
        a, b = cjk[i], cjk[i + 1]
        if a in STOP_CHARS or b in STOP_CHARS:
            continue
        pairs[a + b] += 1
    top_pairs = pairs.most_common(20)

    # 语气词与叠词
    mood_counts = {w: text.count(w) for w in MOOD_WORDS}
    redup_count = len(REDUP_RX.findall(text))

    # 句式
    rhetoric = {}
    for name, rx in RHET_RULES.items():
        rhetoric[name] = len(rx.findall(text))

    stats = {
        "file": path,
        "total_chars": total_chars,
        "non_space_chars": no_space,
        "paragraphs": len(paragraphs),
        "avg_paragraph_len": round(sum(par_lens) / len(par_lens), 1) if par_lens else 0,
        "short_paragraph_rate": round(sum(1 for n in par_lens if n <= 30) / len(par_lens), 3) if par_lens else 0,
        "long_paragraph_rate": round(sum(1 for n in par_lens if n > 150) / len(par_lens), 3) if par_lens else 0,
        "sentences": len(sents),
        "avg_sentence_len": round(avg_sent, 1),
        "short_sentence_rate": round(short_rate, 3),
        "mid_sentence_rate": round(mid_rate, 3),
        "long_sentence_rate": round(long_rate, 3),
        "xlong_sentence_rate": round(xlong_rate, 3),
        "ending_le_rate": round(le_rate, 3),
        "punc_per_1000": {ch: round(n * per_k, 1) for ch, n in sorted(punc_counts.items())},
        "question_per_1000": round(question_rate * per_k, 1),
        "exclaim_per_1000": round(exclaim_rate * per_k, 1),
        "dialogue_rate": round(dialog_rate, 3),
        "dialogue_paragraph_rate": round(dialog_par_rate, 3),
        "top_bigrams": [{"w": w, "n": n} for w, n in top_pairs],
        "mood_words": mood_counts,
        "reduplication_count": redup_count,
        "rhetoric": rhetoric,
    }
    return stats


def render_markdown(stats: list, name: str) -> str:
    lines = [f"# 文风分析报告：{name}", ""]
    for s in stats:
        top_bigrams = "、".join(f"{item['w']}×{item['n']}" for item in s["top_bigrams"][:10])
        lines += [
            f"## {s['file']}",
            "",
            f"- 规模：非空白字符 {s['non_space_chars']} | 段落 {s['paragraphs']} | 句子 {s['sentences']}",
            f"- 句长：平均 {s['avg_sentence_len']} 字 | 短句(≤10) {s['short_sentence_rate']:.0%} | 中句(11-20) {s['mid_sentence_rate']:.0%} | 长句(21-40) {s['long_sentence_rate']:.0%} | 超长(>40) {s['xlong_sentence_rate']:.0%} | 句末'了' {s['ending_le_rate']:.0%}",
            f"- 段落：平均 {s['avg_paragraph_len']} 字 | 短段(≤30) {s['short_paragraph_rate']:.0%} | 长段(>150) {s['long_paragraph_rate']:.0%}",
            f"- 标点（每千字）：逗号 {s['punc_per_1000'].get('，', 0)} | 句号 {s['punc_per_1000'].get('。', 0)} | 问号 {s['question_per_1000']} | 感叹号 {s['exclaim_per_1000']} | 省略号 {s['punc_per_1000'].get('…', 0)} | 破折号 {s['punc_per_1000'].get('——', 0)}",
            f"- 对话：引号内文字占比 {s['dialogue_rate']:.0%} | 含对话段落占比 {s['dialogue_paragraph_rate']:.0%}",
            f"- 高频特色双字：{top_bigrams}",
            f"- 语气词：{'、'.join(f'{k}×{v}' for k, v in s['mood_words'].items() if v) or '无'}",
            f"- 叠词数量：{s['reduplication_count']}",
            f"- 句式：{' | '.join(f'{k}×{v}' for k, v in s['rhetoric'].items() if v) or '无明显设问/排比'}",
            "",
        ]
    lines.append("> 统计只是证据。结合 references/style-learning.md 做语境提炼，生成风格卡。")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="统计中文文本的文风特征")
    parser.add_argument("paths", nargs="+", help="文件或 glob")
    parser.add_argument("--name", default="未命名", help="档案名")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()

    files = []
    for p in args.paths:
        files.extend(glob.glob(p, recursive=True))
    files = sorted(set(f for f in files if f.lower().endswith((".md", ".txt"))))
    if not files:
        print("[错误] 没有找到可分析的 .md / .txt 文件")
        return 1

    results = [analyze_file(f) for f in files]
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return 0
    print(render_markdown(results, args.name))
    return 0


if __name__ == "__main__":
    sys.exit(main())
