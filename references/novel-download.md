# 网文素材下载（番茄小说下载器接入）

用途：文风学习时，用番茄小说下载器（Tomato-Novel-Downloader）获取目标平台作品作为样本，再走 [style-learning.md](style-learning.md) 的标准分析流程。作者：zhongbai2333（基于 Dimily 项目重构，Rust 重写，版本参考 v2.4.13）。

## 获取与启动

1. 从 [GitHub Releases](https://github.com/zhongbai2333/Tomato-Novel-Downloader/releases) 下载对应平台可执行文件：
   - Windows：`TomatoNovelDownloader-Win64-<版本号>.exe`（双击运行）
   - Linux / macOS：下载对应二进制，终端运行
   - Docker：`zhongbai233/tomato-novel-downloader-webui:latest --server --data-dir /data`
   - 安卓 Termux：Release 中的 Android arm64 产物
2. 首次下载新书用 **Web UI 或 TUI**（CLI 只允许更新本地已有书籍，防滥用）：
   - Web UI：`Tomato-Novel-Downloader.exe --server`，浏览器打开 `http://127.0.0.1:18423/`，搜索书名 → 创建下载任务。
   - 局域网访问：`TOMATO_WEB_ADDR=0.0.0.0:18423`；加密码：`--password <密码>`。
   - TUI：直接运行程序，在界面里搜索与下载。
3. 命令行更新已有书籍：`Tomato-Novel-Downloader.exe --update <book_id>`（仅限默认保存目录内已有下载记录的书籍）。

## 输出与配置

- 默认输出 txt / epub；下载目录与格式在配置菜单或 `config.yml` 中设置。
- 数据目录（Web UI / Docker）：`--data-dir <目录>`，`config.yml` 与日志放在其中。
- 章节文件按 `0001-第一章名` 命名；下载封面会生成 `cover.jpg`。
- 可选 Edge TTS 有声书：配置中开启后输出 `{书名}_audio/` 目录。

## 与文风学习流程的衔接

```text
1. 下载目标作品（Web UI / TUI 搜索书名 → 下载 txt/epub）
2. python scripts/prepare_samples.py <下载目录或文件> -o 风格资料/sources
   （自动剥离 HTML、过滤广告行、统计字数与章节数，输出样本文件 + 样本清单）
3. python scripts/style_analyze.py 风格资料/sources/*.md   （量化统计）
4. 通读样本按六维提炼 → 生成 lorebook/风格卡.md          （见 style-learning.md）
5. 试写校准 → 定稿入档
```

- 样本不足 2000 字时提示用户换书或追加章节；整本书太大时用 `--split N` 按章拆分样本。
- 多个作者/多本作品可分别下载，走**三层风格链**多源合成。

## 边界与合规（必读）

- **用途限制**：下载内容仅供个人学习与研究（文风特征提炼），不得转载、传播或商用；学特征不抄句子，输出不含样本原文长片段。
- **法律风险**：项目本身声明仅供学习用途；使用前确认符合当地法律与目标平台政策，看完及时删除文件。
- **使用注意**：不要开 VPN/代理；章节数不建议超过 1500 章；API 可能失效，失败时稍后再试或检查 Issues。
- **隐私**：Web UI 暴露到公网必须加密码锁并放在反向代理/HTTPS 后。
