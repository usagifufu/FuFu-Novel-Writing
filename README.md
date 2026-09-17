# FuFu 小说创作助手

面向中文长篇网络小说创作的 AI 技能包，覆盖从选题、拆书、世界观搭建，到章节写作、伏笔管理、去 AI 味终检的完整流程。

适用于 WorkBuddy / Codex / Claude Code 等支持 `SKILL.md` 规范的技能运行环境。

## 工作流

| 阶段 | 做什么 | 主要文档 |
|---|---|---|
| 1 选题与题材研究 | 榜单扫描、题材可行性、读者画像 | `genre-research.md`、`genre-catalog.md`、`genre-readers.md` |
| 2 拆书与文风学习 | 拆解爆款黄金三章、量化文风、生成风格卡 | `style-learning.md`、`scripts/style_analyze.py` |
| 3 世界观与人设 | 世界状态引擎、角色卡、关系网 | `world-engine.md`、`character-basics.md`、`character-design-methods.md` |
| 4 剧情规划 | 四级大纲、伏笔 DAG、情绪曲线 | `outline-*.md`、`plot-*.md`、`emotional-*.md` |
| 5 章节写作 | 章节规格、钩子设计、日常写作流程 | `chapter-spec.md`、`hooks-*.md`、`workflow-daily.md` |
| 6 审查与定稿 | 六维审查、去 AI 味三层检测 | `review-rubrics.md`、`quality-checklist.md`、`anti-ai-prompts.md` |

## 目录结构

```
FuFu-Novel-Writing/
├── SKILL.md                  # 技能主文件（frontmatter + 工作流 + 资源索引）
├── README.md
├── UPDATE-NOTES.md           # 更新日志
├── install_skill.ps1         # Windows 一键安装脚本
├── agents/
│   └── openai.yaml
├── references/               # 55 份方法论文档 + 3 个开源项目本体
│   ├── 题材与商业/           genre-*.md、commercial-core-methods.md
│   ├── 拆书与文风/           style-*.md、novel-download.md
│   ├── 世界观与人设/         world-engine.md、character-*.md
│   ├── 剧情与大纲/           outline-*.md、plot-*.md、emotional-*.md
│   ├── 章节与钩子/           chapter-spec.md、hooks-*.md、workflow-*.md
│   ├── 审查与去 AI 味/       anti-ai-*.md、banned-words.md、quality-checklist.md
│   ├── aigc-detector/        # MIT，AIGC 检测器完整项目
│   ├── human-writing/        # MIT，活人感写作方法论
│   └── sepia/                # MIT，叙事架构去 AI 化（三遍协议）
└── scripts/                  # 11 个工具脚本
```

## 内置脚本

| 脚本 | 用途 |
|---|---|
| `init_novel.py` | 初始化小说项目目录结构 |
| `auto_write.py` | 写作流程驱动 |
| `style_analyze.py` | 文风量化分析（句长分布、对话密度、语气词频率） |
| `prepare_samples.py` | 样本预处理，供文风学习使用 |
| `novel_lint.py` | 常规质量扫描（错别字、病句、套路化表达） |
| `aigc_detect.py` | AIGC 痕迹检测，中文增强指纹，支持 `--html` / `--json` / `--qwen` |
| `check_prose.py` | 活人感硬禁令检查（翻案腔、排比、名词化、冒号滥用等） |
| `check_quality.py` | 质量检测（AI 词汇、套路化表达） |
| `check-ai-patterns.js` | AI 句式模式检查（Node） |
| `check-degeneration.js` | 退化重复检查（Node） |
| `normalize-punctuation.js` | 标点规范化（Node） |

Python 脚本仅依赖标准库，无需额外安装。

## 安装

### Windows 一键安装

```powershell
powershell -ExecutionPolicy Bypass -File install_skill.ps1
```

脚本会自动定位技能目录（优先 `~/.workbuddy/skills`，其次 `~/.codex/skills`、`~/.claude/skills`），备份旧版本后同步全部文件。

指定目录：

```powershell
powershell -ExecutionPolicy Bypass -File install_skill.ps1 -SkillsRoot "D:\my\skills"
```

### 手工安装

把整个包复制到技能目录下，文件夹名保持 `fufu-novel-assistant`（与 `SKILL.md` 内的 `name` 字段一致）：

- WorkBuddy：`%USERPROFILE%\.workbuddy\skills\fufu-novel-assistant`
- Codex：`%USERPROFILE%\.codex\skills\fufu-novel-assistant`

安装后在新会话中描述写作需求（写小说 / 开新书 / 继续写第 N 章 / 学文风 / 项目体检）即可触发。

## 去 AI 味检测栈

三层递进，从表层指纹到叙事架构：

```
novel_lint.py（常规扫描）
      ↓
aigc_detect.py（AI 指纹：短语复读、平衡句、"连…都"、比喻密度、句首代词密度）
      ↓
check_prose.py（硬禁令：翻案腔、排比、名词化、冒号滥用、破折号、黑话）
      ↓
Sepia 三遍协议（叙事架构层，references/sepia/）
```

使用示例：

```bash
python scripts/aigc_detect.py 章节.md                  # 终端报告
python scripts/aigc_detect.py 章节.md --html 报告.html  # 高亮报告
python scripts/check_prose.py 章节.md                  # 硬禁令检查
```

`aigc_detect.py` 可选接入 DashScope 做来源判别，配置 `DASHSCOPE_API_KEY` 后加 `--qwen` 即可；未配置时自动降级为本地规则引擎。

规则与提示词的汇总入口是 [`references/anti-ai-prompts.md`](references/anti-ai-prompts.md)（反 AI 提示词大全·融合版），单文档覆盖口径裁决与决策路由、活人感规范、禁用词表、最毒句式、八种 AI 模式、行级与全文级指纹、段尾环境描写专章、七 Gate 门禁、三遍法、文体骨架化、Sepia 三遍协议与质量清单，并附 6 个可直接粘贴的提示词模板（章节写作 / 润色 / 终检 / 检测不过重写 / 常驻约束 / 单段急救）。

## 第三方项目与许可

本包内含以下开源项目的完整拷贝，用于支撑去 AI 味与文风学习能力。各项目的 LICENSE 保留在对应目录中。

| 项目 | 作者 | 许可证 | 位置 |
|---|---|---|---|
| [aigc-detector](https://github.com/hoyo0210/aigc-detector) | [hoyo0210](https://github.com/hoyo0210) | MIT | `references/aigc-detector/` |
| [human-writing](https://github.com/KKKKhazix/human-writing) | [KKKKhazix](https://github.com/KKKKhazix) | MIT | `references/human-writing/` |
| [sepia](https://github.com/Nanako0129/sepia) | [Nanako0129](https://github.com/Nanako0129) | MIT | `references/sepia/` |

## 许可

本仓库自有内容（`SKILL.md`、`agents/`、`install_skill.ps1`、`scripts/` 中的自有脚本，以及 `references/` 下除第三方子目录外的方法论文档）著作权归作者所有，转载或二次分发请注明出处。

第三方子目录遵循各自许可证。
