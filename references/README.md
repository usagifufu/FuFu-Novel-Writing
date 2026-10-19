# 参考文件索引

`references/` 下有 56 份文档、约 75 万字节。**不要顺着读，按任务找。**

## 怎么用这份索引

1. 先看下面的「按任务找文件」表，定位到类别。
2. 只读该类别里标着**必读**的那一份，需要细节再往下读同类的。
3. 读完就动笔，不要为了「读全」把 56 份都过一遍——那会把上下文烧光，反而写不好。

> **上下文纪律**：单次任务通常只需要 1-3 份参考文件。超过 5 份，说明任务该拆了。

## 按任务找文件

| 你要做的事 | 先读这一份 | 需要细节再读 |
|---|---|---|
| 第一次用这个技能 | [教程.md](教程.md) | `openwrite-core.md` |
| 开新项目、定目录 | [project-structure.md](project-structure.md) | — |
| 排剧情、做大纲 | [plot-workbench.md](plot-workbench.md) | `outline-*.md` |
| 想钩子、排爽点 | [hooks-chapter.md](hooks-chapter.md) | `hooks-paragraph.md`、`hooks-suspense.md` |
| 写章节正文 | [writer-brief.md](writer-brief.md) | `chapter-spec.md`、`写作约束.md` |
| 批量推进 N 章 | [chapter-spec.md](chapter-spec.md) | `auto_write.py` |
| 去 AI 味 | [anti-ai-prompts.md](anti-ai-prompts.md) | `llmlint.md`、`human-writing-guide.md` |
| 学别人的文风 | [style-learning.md](style-learning.md) | `style-jiangnan.md` |
| 拆书、选题 | [genre-research.md](genre-research.md) | `genre-catalog.md` |
| 审查一章 | [review-rubrics.md](review-rubrics.md) | `quality-checklist.md` |
| 建人设 | [character-design-methods.md](character-design-methods.md) | `character-basics.md`、`character-relations.md` |
| 定世界观与力量体系 | [world-engine.md](world-engine.md) | — |

---

## 一、入口必读

- **[教程.md](教程.md)**：技能完整操作流程与使用教程。新手从这里读起，读一遍就能跑通全流程。
- **[openwrite-core.md](openwrite-core.md)**：方法论总纲。规划写作分家、创作罗盘、单一真源与确认门、canonical packet、有界章节记忆、四级大纲、伏笔 DAG、旧稿导入与整书导出。**遇到「这套流程为什么这么设计」的问题，答案在这里。**

## 二、项目与流程

- **[project-structure.md](project-structure.md)**：项目目录规范，含**按读写权限分层**（src / 运行态 / 产出物 / 例外层）、每章产物流水线、命名硬约束、旧稿导入与整书导出。建项目前必读。
- **[workflow-daily.md](workflow-daily.md)**：日更工作流。每天怎么排、写多少、什么时候审。
- **[workflow-revision.md](workflow-revision.md)**：修订工作流。改稿的次序与边界，避免越改越乱。
- **[state-tracking.md](state-tracking.md)**：状态追踪。世界状态与提交链怎么记、记到什么粒度。
- **[artifact-protocols.md](artifact-protocols.md)**：产物协议。每类文件长什么样、谁写谁读。
- **[cross-book-recall.md](cross-book-recall.md)**：跨书记忆。多本书并行时怎么不串味。

## 三、剧情与大纲

- **[plot-workbench.md](plot-workbench.md)**：情节总工作台。四级大纲、两棵树（承载树 / 因果树）、章节关系图谱、承诺账本、伏笔 DAG、追读力系统、信息控制、MICE。**排剧情的首选。**
- **[plot-core-methods.md](plot-core-methods.md)**：情节核心方法。冲突怎么长出来、场景怎么串。
- **[plot-frameworks.md](plot-frameworks.md)**：情节框架库。三幕、英雄之旅等成型结构的网文改法。
- **[plot-special-topics.md](plot-special-topics.md)**：情节专题。复仇、追妻、悬疑、宫斗等专门套路。
- **[plot-emotion-system.md](plot-emotion-system.md)**：情绪系统。情绪如何在章与卷的尺度上起伏。
- **[outline-methods.md](outline-methods.md)**：大纲方法。从一句话到四级大纲怎么推。
- **[outline-structure-theory.md](outline-structure-theory.md)**：结构理论。为什么这样分段、这样卡点。
- **[outline-rhythm.md](outline-rhythm.md)**：节奏规划。快慢交替、松紧分配。
- **[outline-conflict.md](outline-conflict.md)**：冲突设计。冲突的层数与升级路径。

## 四、钩子与情绪

- **[hooks-chapter.md](hooks-chapter.md)**：章末钩子。类型、密度、什么章该给什么钩子。
- **[hooks-paragraph.md](hooks-paragraph.md)**：段内钩子。让读者不跳段的小钩子。
- **[hooks-suspense.md](hooks-suspense.md)**：悬念设计。信息差怎么控制。
- **[opening-design.md](opening-design.md)**：开篇设计。黄金三章与前三段。
- **[reversal-toolkit.md](reversal-toolkit.md)**：反转工具箱。反转的类型、铺垫条件、常见翻车点。
- **[emotional-arc-design.md](emotional-arc-design.md)**：情绪弧线。一个人物的情绪怎么走完一条线。
- **[emotional-methods.md](emotional-methods.md)**：情绪手法。怎么写哭、写燃、写憋屈而不靠形容词。

## 五、章节生产

- **[writer-brief.md](writer-brief.md)**：章节写作指令模板。canonical packet 怎么组装、风格卡怎么引用、六维审查清单、提交与备份。**每章动笔前必读。**
- **[chapter-spec.md](chapter-spec.md)**：章节规格 YAML 模板、连贯性检查、批量自动推进流程与报告模板。

## 六、人物与世界

- **[world-engine.md](world-engine.md)**：世界状态引擎。主体 / 切面 / 操作 / 历法、等级体系刻度、检索方法。
- **[character-design-methods.md](character-design-methods.md)**：人物塑造方法。从功能位推到立体人。
- **[character-basics.md](character-basics.md)**：人物基础。动机、缺陷、欲望、秘密、弧光五件套。
- **[character-relations.md](character-relations.md)**：人物关系。关系网怎么搭、怎么变。
- **[dialogue-mastery.md](dialogue-mastery.md)**：对话掌控。语气区分、信息密度、潜台词。
- **[female-audience-writing.md](female-audience-writing.md)**：女频向写作。读者预期与雷区。

## 七、题材与商业

- **[genre-research.md](genre-research.md)**：题材研究与拆书流程。题材模板、复合题材规则、题材雷达。**拆书与选题的首选。**
- **[genre-catalog.md](genre-catalog.md)**：37 类网文题材总目录。
- **[genre-writing-formulas.md](genre-writing-formulas.md)**：各题材的写作公式。
- **[genre-core-mechanics.md](genre-core-mechanics.md)**：各题材的核心机制（爽点从哪来）。
- **[genre-readers.md](genre-readers.md)**：各题材的读者画像与预期。
- **[commercial-core-methods.md](commercial-core-methods.md)**：商业核心方法。付费点、追读率、留存。

## 八、文风与文字

- **[style-learning.md](style-learning.md)**：文风学习流程。样本收集、统计分析、六维提炼、三层风格链、两层风格文档、**建卡时的参数交叉校验**。**学文风的首选。**
- **[style-jiangnan.md](style-jiangnan.md)**：江南式文风档案。**独立模块，默认不生效**，项目要在风格卡里显式声明采用模块与强度才会加载，且附带冲突表。
- **[style-craft.md](style-craft.md)**：文风手艺。视角、距离、节奏的手上功夫。
- **[style-combat-face.md](style-combat-face.md)**：对仗与打脸风格。
- **[style-genre-modules.md](style-genre-modules.md)**：风格题材模块。某类题材惯用的语言质感。
- **[writing-craft.md](writing-craft.md)**：文字技艺总纲。句子、段落、意象的基本功。
- **[format-and-structure.md](format-and-structure.md)**：格式与结构。章节切分、排版、标点。
- **[写作约束.md](写作约束.md)**：全书默认写作硬约束。客观化中立化叙述、少用虚词、只写言行本身。**每章 Brief 的禁写事项自动叠加这一份。**

## 九、去 AI 味与检测

- **[anti-ai-prompts.md](anti-ai-prompts.md)**：**反 AI 提示词大全（融合版），本类别唯一入口。** 口径裁决、活人感规范、2.3 禁用词表、**2.3.1 用词替换表（全局最高优先级）**、最毒句式、八种 AI 模式、指纹、段尾环境描写专章、七 Gate 门禁、三遍法、范例库、6 个可直接粘贴的提示词模板。
- **[anti-ai-writing.md](anti-ai-writing.md)**：去 AI 味的实操篇。八种 AI 写作模式的识别与改法、三遍法、按场景分的改写范例库。**想知道「这句话怎么改」翻这份。**
- **[llmlint.md](llmlint.md)**：AI 味反模式清单与审校执行顺序。偏清单与判定边界，**词表不在此处**。
- **[quality-checklist.md](quality-checklist.md)**：写完逐项扫的质量清单。长篇、短篇分册。
- **[banned-words.md](banned-words.md)**：**镜像快照，非真源。** 来自 story-setup 体系，保留仅为与外部 6 个 skill 对齐。冲突一律以 `anti-ai-prompts.md` 为准。
- **[aigc-detector-guide.md](aigc-detector-guide.md)**：AIGC 检测器接入。本地规则引擎、Qwen 深度检测配置、Web UI 部署、与 novel_lint 的分工。
- **[human-writing-guide.md](human-writing-guide.md)**：活人感写作接入。七遍改稿法、与 `aigc_detect.py` / `novel_lint.py` 的分工。
- **[sepia-guide.md](sepia-guide.md)**：Sepia 去 AI 化接入。三层检测栈定位、三遍处理协议、30 特征评分、每模型指纹。**表层手段用尽仍不过检时读这份。**

## 十、审查与质量

- **[review-rubrics.md](review-rubrics.md)**：五角色加权评审、P0/P1/P2 红线分级、四视角对抗式审查、审查报告格式。**审一章之前必读。**

## 十一、外部接入

- **[novel-download.md](novel-download.md)**：番茄小说下载器接入。获取方式、Web UI / TUI / CLI 用法、与文风学习衔接、版权边界。

---

## 子目录

| 目录 | 是什么 |
|---|---|
| `aigc-detector/` | aigc-detector 开源项目本体（FastAPI 后端 + React 前端，可 Docker 独立部署） |
| `human-writing/` | human-writing 开源项目本体（SKILL.md + 五份方法论 + check_prose.py + 蒸馏版，MIT） |
| `sepia/` | Sepia 开源项目本体（v0.4.0，MIT，含 narrative / discourse / style 三遍与 rubric） |

三个子目录都是**第三方项目原样收录**，不是本技能写的，改动要跟上上游。

## 单一真源声明

这几件事各自只有一个真源，其余文件一律引用不复述。改规则时**只改真源**：

| 规则 | 真源 | 哪里只是引用 |
|---|---|---|
| 禁用词、禁句、禁喻 | `anti-ai-prompts.md` 2.3 / 2.3.1 | `写作约束.md`、`style-craft.md`、`llmlint.md`、`banned-words.md`（镜像） |
| 标点政策（省略号 / 破折号） | `anti-ai-prompts.md` 第〇部分 | `banned-words.md`、`anti-ai-writing.md` |
| 项目目录与权限分层 | `project-structure.md` | `文件布局.md`（项目级只记偏差） |
| 风格卡与文风总纲的分工 | `style-learning.md` | `writer-brief.md` |
| 质量阈值 | `scripts/check_prose.py` 等脚本 | 各文档的描述 |

改动后跑一遍 `python scripts/audit_rules.py`，确认「规则冲突 0、词表副本 1」。
