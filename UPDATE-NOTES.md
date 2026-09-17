# FuFu小说助手 技能更新说明（Openwrite 方法论融合）

依据：抖音号 34769724778（主打 Openwrite AI 写作助手与网文写作技巧）主推产品 Openwrite 的 GitHub 仓库（LiPu-jpg/Openwrite）方法论。抖音页面本身有反爬验证码，无法直接抓取视频内容，故以其开源仓库为学习来源。

## 本次变更

1. **SKILL.md**
   - frontmatter 描述加入 Openwrite 及新触发词（旧稿导入、整书导出）。
   - 核心原则新增 3 条：规划写作分家（双 Agent 模式）、创作罗盘压跑偏、单一真源 + 确认门。
   - 主链新增"创作罗盘建立"环节；项目搭建改为五阶段（新增创作罗盘）。
   - 剧情规划改为五类文件：新增 `plot/罗盘.md`；structure.md 采用四级大纲（总纲→篇/卷→幕→节→章）；promises.md 增加伏笔 DAG。
   - 章节写作引入 canonical packet 上下文组装与有界章节记忆。
   - 评审回补支持旧稿导入与整书导出。
2. **references/openwrite-core.md（新增）**：Openwrite 方法论落地细则——双 Agent、创作罗盘、单一真源、确认门、canonical packet、有界章节记忆、四级大纲、伏笔 DAG、三层风格链、旧稿导入/整书导出、事务安全网。
3. **references/writer-brief.md**：新增 canonical packet 组装清单；任务书加"罗盘对齐"栏；提交前检查加章节摘要回写。
4. **references/style-learning.md**：新增三层风格链（sources → manifest → composed）与多源合成规则。
5. **references/genre-research.md**：新增题材雷达（热度/供给/爆款共性/读者预期/差异化）。
6. **references/plot-workbench.md**：新增四级大纲、伏笔 DAG 两节；决策记录与罗盘联动。
7. **references/project-structure.md**：目录加 `plot/罗盘.md`；新增单一真源与运行态、旧稿导入、整书导出；提交链加"本章摘要"列。
8. **scripts/init_novel.py**：模板新增 `plot/罗盘.md`；commits.md 加章节摘要列；大纲模板体现四级层级。

## 第二次更新（番茄小说下载器融合，用于文风学习素材）

依据：zhongbai2333/Tomato-Novel-Downloader（番茄小说下载器不精简版，Rust 重写，v2.4.13）。

1. **references/novel-download.md（新增）**：下载器接入说明——获取方式（Releases/Docker/Termux）、Web UI（--server）/TUI/CLI（--update）用法、输出与配置（txt/epub、--data-dir）、与文风学习流程衔接、版权与合规边界。
2. **scripts/prepare_samples.py（新增）**：纯标准库脚本，把下载的 txt/epub 整理成语料——自动探测编码、epub 按 spine 抽取正文、剥 HTML、过滤广告行、统计字数/章节数、按章拆分（--split），输出样本文件与样本清单，直接衔接 style_analyze.py。
3. **references/style-learning.md**：收集样本步骤加入"无现成样本时用下载器获取平台范文"路径。
4. **SKILL.md**：文风学习步骤加入下载器衔接；description 增加"范文下载、网文下载"触发词；资源索引新增 prepare_samples.py 与 novel-download.md。

## 安装

运行 `install_skill.ps1`（自动备份现有技能到 `work/fufu-novel-assistant-skill-backup/<时间戳>/` 后覆盖），或由 Codex 在获得写权限后直接应用更新包到技能目录。

## 第三次更新（Openwrite 仓库细节二轮落盘）

依据同一来源：Openwrite 仓库 `SKILL.md v5.8.0` 与 `skills/goethe-agent/SKILL.md` 的一手细节。

1. **references/openwrite-core.md**
   - 双 Agent 节新增**显式交接（handoff）**：规划成熟后把 `author_intent.md` 与 `current_focus.md` 落盘，随每章 canonical packet 进入写作上下文。
   - 双 Agent 节新增**风格三模式**：`generic` / `extracted` / `hybrid`，写入风格卡头部并在每章 Brief 注明。
   - 单一真源节新增**世界关系图谱**：人物/实体关系共用单一真源，diff 预览 + `base_revision` 确认防覆盖。
   - 单一真源节新增**单源文档规范**：核心文档用 TOML front matter（id/summary/tags/detail_refs/related）+ Markdown 正文。
   - 确认门节新增**增量修改协议**：`old_text -> new_text` 精确补丁、先预览后落盘、revision 防冲突、安全重编号。
   - 事务感节强化为**运行态锁与回滚**：write/multi-write/review 共用取锁、备份、回滚规则。
2. **SKILL.md**：核心原则 9 补充显式交接与风格三模式；章节记忆处补充会话历史 JSONL 归档与滚动摘要压缩（恢复默认最近 24 轮）；资源索引描述同步。
3. **更新包完整性**：补齐 `agents/openai.yaml`、`references/llmlint.md`、`references/world-engine.md`、`scripts/novel_lint.py`、`scripts/style_analyze.py`；`install_skill.ps1` 文件清单同步扩充。

## 第四次更新（使用教程入档）

新增 `references/教程.md`：完整操作流程与使用教程（触发方式、三种工作模式、八阶段流程、命令速查、纪律红线、最快上手路径），并在 SKILL.md 资源索引置顶引用；`install_skill.ps1` 文件清单加入该文件。

## 第五次更新（写作硬约束入档）

新增 `references/写作约束.md`：全书默认生效的写作硬约束——禁止句式与禁喻词清单（火山/湖面/涟漪/眼神闪烁等）、禁止程式化情绪暗示、禁止惰性状态词、禁止动物比喻与平衡句式、客观化中立化叙述要求、豁免规则。SKILL.md 文风学习步骤与资源索引、writer-brief.md（Brief 禁写事项默认叠加 + 提交前检查）、教程.md（纪律第 9 条）同步接入；`install_skill.ps1` 文件清单加入该文件。

## 第六次更新（反 AI 提示词大全升级为融合版）

`references/anti-ai-prompts.md` 由 6914 字升级为 17577 字融合版，标题改为「反 AI 提示词大全（融合版）」，把 fufu 体系版与 story-setup 体系版两份上游文档合并为单文档全集。

1. **新增第〇部分「口径说明与冲突裁决」**：两份上游文档存在口径差异（省略号允许/禁用、删除比例上限），本节给出合并后的执行口径，并附**决策路由表**（按"你在做什么"直接跳对应模块）。
2. **并入 story-setup 体系内容**：禁用词表（一级/二级）、最毒禁用句式（★级排序）、八种 AI 写作模式（含最隐蔽的解释腔/上帝感）、AI 味打分客观指标、七 Gate 门禁执行序、系统性三遍法、Show Don't Tell 对照、改写范例库（情绪/场景/打斗/结尾/冲突对话/震惊分层）、质量检查清单。
3. **新增 3.3 段尾环境描写专章**：机制说明（AI 拿环境句当情绪封口）、三条准入条件（只能出现在段中或段首，禁止段尾）、四组反例对照、可直接粘贴的约束段与逐段自查清单。
4. **新增 3.4 叠加式描写**（同一动作掰开写三遍）与 4.5 文体骨架化操作表、4.6 Sepia 三遍处理协议。
5. **提示词模板由 4 个增至 6 个**：新增**模板 E 常驻约束**（精简 11 条，写入系统提示词或风格卡全程生效）、**模板 F 单段急救**（局部 AI 味重时的六步法）。
6. **附录**：三层检测栈速查、快速自检口诀、两条铁律。
7. **SKILL.md**：步骤 5「润色与 Anti-AI 终检」末尾把该文档标为去 AI 味的**汇总入口**；资源索引描述同步更新（模板数 4→6，补段尾环境描写专章等）。**README.md**：去 AI 味检测栈章节补汇总入口说明。

## 第七次更新（反 AI 提示词包纳入仓库）

把此前只存在于本地工作区的「反AI提示词包」正式纳入仓库，成为可单独取用的独立分发包。

1. **新增 `反AI提示词包/`（6 文件）**：`反AI提示词大全-融合版.md`（与 `references/anti-ai-prompts.md` 逐字节一致）、`分册/fufu体系版-指纹与骨架化.md`、`分册/story-setup体系版-禁令与范例.md`、`检测脚本/aigc_detect.py`、`检测脚本/check_prose.py`、包内 `README.md`。两个检测脚本仅依赖标准库，复制出去可独立运行。
2. **行尾口径统一**：包内 `check_prose.py` 由此前遗漏的 CRLF 归一为 LF（22237 → 21598 字节），与技能本体 `scripts/check_prose.py` 逐字节一致；全包 6 文件均为 LF，无 CRLF 残留。
3. **README.md**：目录结构补 `反AI提示词包/` 子树；去 AI 味检测栈章节新增「独立分发包」小节与文件用途表。

## 安装

运行 `install_skill.ps1`（自动备份现有技能到 `work/fufu-novel-assistant-skill-backup/<时间戳>/` 后覆盖），或由 Codex 在获得写权限后直接应用更新包到技能目录。
