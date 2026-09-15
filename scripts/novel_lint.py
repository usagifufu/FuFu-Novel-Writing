#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""静态扫描中文小说文本中的 AI 写作痕迹（候选位置，不是判决）。

用法:
    python novel_lint.py <文件或glob>...
    python novel_lint.py manuscript/*.md --json

输出行级命中与分类统计。需要语境判断的问题由 Codex 结合
references/llmlint.md 人工复核，命中不等于要改。
"""

import argparse
import glob
import json
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


# 类别 -> [(名称, 正则)]
RULES = {
    "填充词与冗余修饰": [
        ("弱化词", re.compile(r"不禁|仿佛|似乎|好像|宛如|犹如|顿时|瞬间|缓缓|轻轻|微微|深深|默默|喃喃|蓦然")),
        ("表情包式写法", re.compile(r"心中一动|心头一紧|眼底(?!深处)[^，。]{0,4}|眸光|目光[^，。]{0,6}(一凝|一沉|闪烁|复杂|坚定|深邃|幽深|平静)")),
    ],
    "机械过渡与套路衔接": [
        ("转折词堆叠", re.compile(r"然而[，,]|不过[，,]|就在这时|忽然|只见|没想到|令人惊讶的是|原来如此|可想而知|不知不觉|不得不说|实际上[，,]|毕竟[，,]|毫无疑问|显而易见")),
    ],
    "公式化设问": [
        ("自问自答", re.compile(r"难道[^。！？\n]{0,14}吗|是不是[^。！？\n]{0,10}[？?]|难道说|莫非[^。！？\n]{0,10}[？?]")),
    ],
    "公式化排比与二元对比": [
        ("三段排比", re.compile(r"不是[^，。]{1,14}，不是[^，。]{1,14}，而是|无论[^，。]{1,12}[，,]，无论[^，。]{1,12}[，,]，无论|既不是[^，。]{1,12}，也不是[^，。]{1,12}，而是")),
        ("二元对比", re.compile(r"[^。！？\n]{1,16}不是[^，。]{1,14}，[^。！？\n]{0,8}而是[^，。]{1,16}")),
    ],
    "空泛总结与万金油": [
        ("空泛总结", re.compile(r"总而言之|总的来说|这一刻|仿佛一切|一切仿佛|岁月静好|一切都结束了|新的开始|一切都会好起来")),
        ("万金油收尾", re.compile(r"望向远方|看向远方|深吸一口气|长舒一口气|嘴角勾起[^，。]{0,6}笑|露出一抹[^，。]{0,6}笑")),
    ],
    "句式雷同": [],
}


def scan_text(text: str, path: str):
    """逐行扫描，返回命中列表。句式雷同类做行级状态判定。"""
    hits = []
    lines = text.splitlines()

    prev_ended_le = 0          # 连续以"了。"结尾的行数
    prev_started_he = 0        # 连续以他/她开头的行数
    prev_short = 0             # 连续超短句行数

    for idx, raw in enumerate(lines, start=1):
        line = raw.strip()
        if not line:
            prev_ended_le = prev_started_he = prev_short = 0
            continue

        # 行内正则命中
        for cat, rule_list in RULES.items():
            for name, rx in rule_list:
                for m in rx.finditer(line):
                    start = m.start()
                    snippet = m.group(0)[:24]
                    hits.append(
                        {
                            "file": path,
                            "line": idx,
                            "col": start + 1,
                            "category": cat,
                            "rule": name,
                            "match": snippet,
                        }
                    )

        # 句式雷同：连续状态判定
        ends_le = 1 if line.endswith("了。") or line.endswith("了！") else 0
        prev_ended_le = prev_ended_le + 1 if ends_le else 0
        if prev_ended_le >= 3:
            hits.append(
                {
                    "file": path,
                    "line": idx,
                    "col": 1,
                    "category": "句式雷同",
                    "rule": "连续「了」结尾（3 行以上）",
                    "match": line[:24],
                }
            )

        starts_he = 1 if re.match(r"^[他她]", line) else 0
        prev_started_he = prev_started_he + 1 if starts_he else 0
        if prev_started_he >= 4:
            hits.append(
                {
                    "file": path,
                    "line": idx,
                    "col": 1,
                    "category": "句式雷同",
                    "rule": "连续以他/她开头（4 行以上）",
                    "match": line[:24],
                }
            )

        short = 1 if re.match(r"^[^，。！？]{1,7}[。！？]$", line) else 0
        prev_short = prev_short + 1 if short else 0
        if prev_short >= 5:
            hits.append(
                {
                    "file": path,
                    "line": idx,
                    "col": 1,
                    "category": "句式雷同",
                    "rule": "连续超短句（5 行以上）",
                    "match": line[:24],
                }
            )
    return hits


def main() -> int:
    parser = argparse.ArgumentParser(description="扫描中文文本的 AI 写作痕迹")
    parser.add_argument("paths", nargs="+", help="文件或 glob")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()

    files = []
    for p in args.paths:
        files.extend(glob.glob(p, recursive=True))
    files = sorted(set(f for f in files if f.lower().endswith((".md", ".txt"))))
    if not files:
        print("[错误] 没有找到可扫描的 .md / .txt 文件")
        return 1

    all_hits = []
    for f in files:
        with open(f, encoding="utf-8") as fh:
            all_hits.extend(scan_text(fh.read(), f))

    if args.json:
        print(json.dumps(all_hits, ensure_ascii=False, indent=2))
        return 0

    from collections import Counter

    counts = Counter()
    for h in all_hits:
        counts[h["category"]] += 1
        print(
            f"{h['file']}:{h['line']}:{h['col']}  [{h['category']}|{h['rule']}] {h['match']}"
        )

    print("\n=== 汇总 ===")
    for cat, n in counts.most_common():
        print(f"{cat}: {n}")
    print(f"总计: {len(all_hits)} 处候选命中")
    print("提示: 命中只是证据。逐条结合语境复核（见 references/llmlint.md），不要机械清零。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
