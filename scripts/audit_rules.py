#!/usr/bin/env python3
"""审计技能自身的结构健康度：规则冲突、词表分散、入口体积、导航覆盖。

只检查技能文件，不检查正文。用来在重构前后取同一套数字做对比。

用法：
    python scripts/audit_rules.py [技能根目录]
缺省根目录为脚本所在目录的上一级。
"""

from __future__ import annotations

import os
import re
import sys

# 用来识别「这份文件是不是又在列一遍禁用词表」的种子词。
# 单独出现不算，一份文件里命中 >= 5 个才判定为「词表副本」。
SEED_TERMS = (
    "仿佛",
    "犹如",
    "宛若",
    "一丝",
    "一抹",
    "深吸一口气",
    "缓缓",
    "不禁",
    "眼中闪过",
    "嘴角勾起",
    "眉头微皱",
    "不容置疑",
    "不易察觉",
    "心中一动",
)

# 声明自己是镜像快照、不是真源的文件，不参与「词表副本」计数。
MIRROR_MARKERS = ("本文件不是本技能的真源",)

WORDLIST_THRESHOLD = 5
WORDLIST_WINDOW = 300
WORDLIST_STEP = 50

ALLOW_MARKERS = ("允许省略号", "省略号可用", "省略号允许")
DENY_MARKERS = ("禁用省略号", "禁止省略号", "不用省略号", "不使用省略号")

# 变更日志与导航索引不是规则来源，不参与政策判定。
EXCLUDE_FROM_POLICY = {"UPDATE-NOTES.md", "README.md"}

LONG_LINE_BYTES = 300


def read(path: str) -> str:
    with open(path, encoding="utf-8", errors="replace") as handle:
        return handle.read()


def md_files(root: str) -> list[str]:
    out = []
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in {".git", "__pycache__"}]
        for name in files:
            if name.endswith(".md"):
                out.append(os.path.join(base, name))
    return sorted(out)


def ellipsis_policy(paths: list[str]) -> tuple[list[str], list[str], list[str]]:
    """返回 (允许派文件, 禁用派文件, 冲突明细)。

    只统计正文陈述，跳过表格行——口径裁决表里常引述上游的不同说法，
    那是元讨论，不是本技能的政策主张。
    """
    allow, deny, detail = [], [], []
    for path in paths:
        if os.path.basename(path) in EXCLUDE_FROM_POLICY:
            continue
        text = read(path)
        rel = os.path.relpath(path)
        allows, denies = [], []
        for number, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            if stripped.startswith("|"):
                continue
            for marker in ALLOW_MARKERS:
                if marker in stripped:
                    allows.append(marker)
                    detail.append(f"{rel}:{number}  允许  {marker}")
            for marker in DENY_MARKERS:
                if marker in stripped:
                    denies.append(marker)
                    detail.append(f"{rel}:{number}  禁用  {marker}")
        if allows:
            allow.append(rel)
        if denies:
            deny.append(rel)
    return allow, deny, detail


def wordlist_copies(paths: list[str]) -> tuple[list[tuple[str, int]], list[int]]:
    """找出仍在整表罗列禁用词的文件。

    判据是「同一窗口内密集出现」，不是「全文出现过」——散落的举例说明不算副本。
    """
    hits = []
    for path in paths:
        text = read(path)
        if any(marker in text for marker in MIRROR_MARKERS):
            continue
        if len(text) <= WORDLIST_WINDOW:
            best = sum(1 for term in SEED_TERMS if term in text)
        else:
            best = 0
            for start in range(0, len(text) - WORDLIST_WINDOW + 1, WORDLIST_STEP):
                chunk = text[start:start + WORDLIST_WINDOW]
                count = sum(1 for term in SEED_TERMS if term in chunk)
                if count > best:
                    best = count
                    if best == len(SEED_TERMS):
                        break
        if best >= WORDLIST_THRESHOLD:
            hits.append((os.path.relpath(path), best))
    hits.sort(key=lambda item: -item[1])
    return hits, [count for _, count in hits]


def entry_metrics(root: str) -> dict[str, int]:
    path = os.path.join(root, "SKILL.md")
    if not os.path.exists(path):
        return {}
    raw = read(path)
    lengths = [len(line.encode("utf-8")) for line in raw.splitlines()]
    return {
        "bytes": len(raw.encode("utf-8")),
        "lines": raw.count("\n") + 1,
        "long_lines": sum(1 for value in lengths if value > LONG_LINE_BYTES),
        "max_line": max(lengths) if lengths else 0,
    }


def nav_coverage(root: str) -> tuple[int, list[str]]:
    """统计 references 下没被入口或索引点名的文件。"""
    ref_dir = os.path.join(root, "references")
    if not os.path.isdir(ref_dir):
        return 0, []
    targets = [os.path.join(ref_dir, name) for name in os.listdir(ref_dir)
               if name.endswith(".md")]
    entry_text = ""
    for name in ("SKILL.md", os.path.join("references", "README.md")):
        path = os.path.join(root, name)
        if os.path.exists(path):
            entry_text += read(path)
    orphans = []
    for path in targets:
        name = os.path.basename(path)
        if name == "README.md":
            continue
        if name not in entry_text:
            orphans.append(name)
    return len(targets), sorted(orphans)


def main() -> int:
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))
    paths = md_files(root)

    print(f"技能根目录 {root}")
    print(f"markdown 文件 {len(paths)} 个\n")

    allow, deny, detail = ellipsis_policy(paths)
    print("== 省略号政策 ==")
    print(f"允许派 {len(allow)} 个文件：{'、'.join(allow) if allow else '无'}")
    print(f"禁用派 {len(deny)} 个文件：{'、'.join(deny) if deny else '无'}")
    conflict = 1 if allow and deny else 0
    print(f"政策冲突 {'有' if conflict else '无'}")
    if detail:
        print("命中位置：")
        for row in detail[:12]:
            print(f"  {row}")
    print()

    hits, spreads = wordlist_copies(paths)
    print("== 禁用词表副本 ==")
    print(f"仍在整表罗列的文件 {len(hits)} 个（判定阈值：≥{WORDLIST_THRESHOLD} 个种子词）")
    for name, count in hits:
        print(f"  {count:2d} 词  {name}")
    avg = sum(spreads) / len(spreads) if spreads else 0
    print(f"平均种子词覆盖 {avg:.1f}")
    print()

    metrics = entry_metrics(root)
    print("== 入口体积 SKILL.md ==")
    if metrics:
        print(f"字节 {metrics['bytes']}  行 {metrics['lines']}  "
              f"超长行(>{LONG_LINE_BYTES}B) {metrics['long_lines']}  "
              f"最长行 {metrics['max_line']}B")
    else:
        print("未找到 SKILL.md")
    print()

    total, orphans = nav_coverage(root)
    print("== 导航覆盖 ==")
    print(f"references 顶层 md {total} 个，未被入口或索引点名 {len(orphans)} 个")
    for name in orphans[:15]:
        print(f"  {name}")
    if len(orphans) > 15:
        print(f"  ……另有 {len(orphans) - 15} 个")
    print()

    print("== 汇总 ==")
    print(f"规则冲突 {conflict} | 词表副本 {len(hits)} | "
          f"入口字节 {metrics.get('bytes', 0)} | 长行 {metrics.get('long_lines', 0)} | "
          f"孤儿文件 {len(orphans)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
