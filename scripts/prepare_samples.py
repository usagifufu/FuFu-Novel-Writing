#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""整理下载的小说样本（txt/epub）为文风学习语料。

用法:
    python prepare_samples.py <输入文件或目录>... [-o 输出目录] [--no-ads] [--split N]

流程衔接:
    番茄小说下载器下载（Tomato-Novel-Downloader，见 references/novel-download.md）
    -> 本脚本整理为干净语料样本
    -> scripts/style_analyze.py 统计
    -> 提炼风格卡（references/style-learning.md）

说明:
    - 仅使用 Python 标准库，无第三方依赖。
    - txt 自动探测编码（utf-8 / utf-8-sig / gb18030）。
    - epub 按 spine 顺序抽取正文并剥离 HTML 标签。
    - 默认过滤明显的平台广告行，可用 --no-ads 关闭。
"""

import argparse
import html
import posixpath
import re
import sys
import urllib.parse
import zipfile
from pathlib import Path


CHAPTER_RE = re.compile(
    r"^(第[0-9零一二三四五六七八九十百千万]+[章节回卷部集]|序章|楔子|番外|尾声)"
)
AD_RE = re.compile(
    r"https?://|www\.|番茄小说.{0,8}(app|APP|下载|免费|阅读|客户端)"
    r"|(请|欢迎).{0,8}(下载|安装).{0,12}(番茄|app|APP)"
    r"|手机用户请访问|天才一秒记住"
)
ITEM_RE = re.compile(r"<item\b[^>]*>")
SPINE_RE = re.compile(r"<itemref[^>]*idref=\"([^\"]+)\"")


def read_txt(path: Path) -> str:
    raw = path.read_bytes()
    for enc in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="ignore")


def read_epub(path: Path) -> str:
    with zipfile.ZipFile(path) as zf:
        container = None
        try:
            container = zf.read("META-INF/container.xml").decode("utf-8", errors="ignore")
        except KeyError:
            pass
        opf_path = None
        if container:
            m = re.search(r"full-path=\"([^\"]+)\"", container)
            if m:
                opf_path = m.group(1)
        if not opf_path:
            candidates = [n for n in zf.namelist() if n.lower().endswith(".opf")]
            if not candidates:
                raise ValueError(f"EPUB 中没有 OPF 文件: {path}")
            opf_path = candidates[0]
        opf = zf.read(opf_path).decode("utf-8", errors="ignore")
        base_dir = opf_path.rsplit("/", 1)[0] if "/" in opf_path else ""
        id2href = {}
        for tag in ITEM_RE.findall(opf):
            idm = re.search(r"\bid=\"([^\"]+)\"", tag)
            hrefm = re.search(r"\bhref=\"([^\"]+)\"", tag)
            if idm and hrefm:
                id2href[idm.group(1)] = hrefm.group(1)
        parts = []
        for idref in SPINE_RE.findall(opf):
            href = id2href.get(idref)
            if not href:
                continue
            href = urllib.parse.unquote(href)
            full = posixpath.normpath(href if not base_dir else base_dir + "/" + href)
            try:
                raw = zf.read(full).decode("utf-8", errors="ignore")
            except KeyError:
                continue
            raw = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", raw)
            raw = re.sub(r"(?s)<[^>]+>", "\n", raw)
            parts.append(html.unescape(raw))
        return "\n".join(parts)


def is_ad_line(line: str) -> bool:
    return bool(AD_RE.search(line)) and len(line) <= 80


def clean_text(text: str, filter_ads: bool) -> list[str]:
    lines = []
    for ln in text.splitlines():
        s = ln.strip()
        if not s:
            continue
        if filter_ads and is_ad_line(s):
            continue
        lines.append(s)
    return lines


def count_chapters(lines: list[str]) -> int:
    return sum(1 for ln in lines if CHAPTER_RE.match(ln))


def split_chunks(lines: list[str], per: int) -> list[list[str]]:
    if per <= 0:
        return [lines]
    chunks: list[list[str]] = []
    current: list[str] = []
    count = 0
    for ln in lines:
        current.append(ln)
        if CHAPTER_RE.match(ln):
            count += 1
            if count % per == 0:
                chunks.append(current)
                current = []
    if current:
        chunks.append(current)
    return chunks or [lines]


def safe_name(name: str) -> str:
    name = re.sub(r"[\\/:*?\"<>|]", "_", name).strip()
    return name or "未命名样本"


def collect_inputs(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for p in paths:
        path = Path(p)
        if path.is_file():
            if path.suffix.lower() in (".txt", ".epub"):
                files.append(path)
        elif path.is_dir():
            for f in sorted(path.rglob("*")):
                if f.is_file() and f.suffix.lower() in (".txt", ".epub"):
                    files.append(f)
        else:
            print(f"[跳过] 不存在: {p}")
    return files


def main() -> int:
    parser = argparse.ArgumentParser(
        description="整理下载的小说（txt/epub）为文风学习语料",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("inputs", nargs="+", help="小说文件或目录（txt/epub）")
    parser.add_argument("-o", "--output", default="风格资料/sources", help="样本输出目录")
    parser.add_argument("--no-ads", action="store_true", help="不过滤广告行")
    parser.add_argument("--split", type=int, default=0, help="每 N 章拆一个样本文件（0 = 不拆）")
    args = parser.parse_args()

    files = collect_inputs(args.inputs)
    if not files:
        print("[错误] 没有找到 txt/epub 文件")
        return 1

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    records = []
    used_names: set[str] = set()

    for path in files:
        try:
            text = read_epub(path) if path.suffix.lower() == ".epub" else read_txt(path)
        except Exception as e:
            print(f"[失败] {path}: {e}")
            continue
        lines = clean_text(text, filter_ads=not args.no_ads)
        if not lines:
            print(f"[失败] {path}: 没有提取到正文")
            continue
        chunks = split_chunks(lines, args.split)
        base = safe_name(path.stem)
        total_chars = 0
        total_chapters = 0
        written = []
        for i, chunk in enumerate(chunks, 1):
            suffix = f"-part{i:02d}" if len(chunks) > 1 else ""
            name = base + suffix
            if name in used_names:
                j = 2
                while f"{name}-{j}" in used_names:
                    j += 1
                name = f"{name}-{j}"
            used_names.add(name)
            dest = out_dir / (name + ".md")
            nchars = sum(len(ln) for ln in chunk)
            nchapters = count_chapters(chunk)
            total_chars += nchars
            total_chapters += nchapters
            # 不写头部注释：注释文本会被 style_analyze.py 计入统计，元信息统一放样本清单。
            dest.write_text("# " + name + "\n\n" + "\n\n".join(chunk) + "\n", encoding="utf-8")
            written.append(str(dest))
            print(f"[OK] {dest} （{nchars} 字 / {nchapters} 章）")
        records.append((path, base, total_chars, total_chapters, written))

    manifest = out_dir / "样本清单.md"
    rows = ["| 原始文件 | 样本 | 字数 | 章节数 |", "| --- | --- | --- | --- |"]
    for src, base, chars, chapters, written in records:
        rows.append(f"| {src.name} | {', '.join(Path(w).name for w in written)} | {chars} | {chapters} |")
    manifest.write_text("# 文风学习样本清单\n\n" + "\n".join(rows) + "\n", encoding="utf-8")
    print(f"\n[清单] {manifest}")
    print("下一步：运行 python scripts/style_analyze.py <样本文件>... 做量化统计，再按 references/style-learning.md 提炼风格卡。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
