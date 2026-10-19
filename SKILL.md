---
name: fufu-novel-assistant
display_name: FuFu小说助手
agent_created: true
description: FuFu（芙芙）小说助手 —— 基于 NeuroBook、Webnovel Writer、MuMu-AINovel、Openwrite 方法论的长篇小说创作全流程技能：把软件工程实践（事件溯源、提交链、技术债追踪、ADR、lint、体检）与创意写作理论（设定圣经、契诃夫之枪、桑德森承诺三法则、希区柯克悬念、MICE、追读力）结合，融合 Openwrite 的创作罗盘、双 Agent、单一真源、canonical packet、四级大纲、伏笔 DAG、三层风格链、确认门、旧稿导入/整书导出，覆盖从灵感、拆书与题材研究、文风学习、世界观与人设搭建、剧情规划、伏笔管理、章节写作、六维审查、去 AI 味审校到长期记忆的完整闭环。Use when the user asks to write, plan, continue, or revise a novel or long-form fiction; create or expand worldbuilding, characters, power/level systems; design plot, outline, chapters, scenes, arcs, or read-retention pacing; track foreshadowing/promises and payoffs; deconstruct existing novels or research genres; learn a writing style from sample files or mimic a provided author's style; record creative decisions; fix continuity errors or "吃书"; check or remove AI-flavored writing; draft chapter prose via brief; scaffold a novel project workspace; import an existing draft; run consistency/health checks. 触发场景：写小说、开新书、写长篇、大纲/剧情/伏笔/人设/世界观/战力体系/章节写作、拆书、题材研究、追读力/爽点、润色修稿、设定矛盾、项目体检、AI味检查、文风学习、风格提取、学文风、模仿文风、范文下载、网文下载、批量推进、推进N章、写第5-15章、继续往下写、黄金三章、扫榜、拆解。
---

# 📖 FuFu小说助手

长篇小说写不完、吃书、烂尾，通常是工程问题，不是才华问题。本技能把写作拆成可维护、可审计的流程：写前查设定，写后入账，每章过闸，手法沉淀。作者管创意，AI 管执行与记录。

## 核心原则

1. **文件即记忆。** 设定、剧情、正文、状态、提交链都是项目里看得见的文件，不放对话记忆。续写前先读文件，不凭印象。不会随剧情变的进 `lorebook/`，会变的进 `world-state/`；每章写完追加一条提交，章节之间靠提交链衔接。
2. **伏笔是承诺。** 埋下、推进、兑现全程记账，逾期必须提示。感情线发糖、爽点间隔同样算承诺。
3. **单一真源。** 每个已批准的事实只有一个确认版；每条规则也只有一个真源。改设定先出 diff 预览，用户确认才落盘，不静默改写已批准内容。
4. **人主导，AI 执行。** 大决策作者拍板并留理由。规划与写作分家：规划只定方向排节奏，写作只按批准方案动笔，不边写边改大纲。
5. **罗盘压跑偏。** 每个项目维护 `plot/罗盘.md`（长期承诺 / 近期焦点 / 必须保留 / 必须避免），开写前对齐。与罗盘冲突的新灵感先记待办，不擅自改主线。
6. **先定情绪，再定故事。** 每个场景服务于明确的情绪目标。从验证过的模式组装，不重新发明。
7. **写完必须过闸。** 审查是找问题，不是验证正确性：红线 P0 阻断、P1 建议、P2 优化。去 AI 味的目标不是零命中，而是减掉没有功能的模板负担。

## 写作主链

**灵感探索 → 拆书/题材研究（可选）→ 文风学习（可选）→ 项目与世界书初始化 → 创作罗盘 → 世界状态建档 → 剧情规划 → 章节写作 → 评审与回补**

每章都走「剧情设计 → 拍板落库 → 正文/审查/提交」这个小循环。

## 意图路由

| 用户意图 | 关键词 | 走哪一步 |
|---|---|---|
| 开新书 / 写长篇 | 开书、写大纲、连载、日更 | 步骤 1 → 4 |
| 批量推进 | 推进N章、写第5-15章、继续往下写 | 步骤 9 |
| 续写 / 改稿 | 续写、修改第X章、重写 | 读提交链 → 对齐罗盘 → 步骤 7 |
| 拆书 / 拆文 | 拆文、分析这本书、黄金三章 | 步骤 2 |
| 扫榜 / 选题 | 什么火、排行、选题方向 | 步骤 2 |
| 学文风 | 学文风、模仿文风、风格提取 | 步骤 3 |
| 去 AI 味 | 去AI味、太AI了 | 步骤 7 第 5 关 |
| 审查 / 体检 | 审查一下、项目体检 | 步骤 8 |
| 查设定 / 查进度 | 查角色、查伏笔、写到哪了 | 直接读项目文件 |
| 导入旧稿 | 导入、把我的书导进来 | `openwrite-core.md` |
| 整书导出 | 导出、发布 | `openwrite-core.md` |

**不知道读哪份参考文件时，先查 [`references/README.md`](references/README.md)。** 那里按任务分了十类，每份一句话说明加使用时机。单次任务通常只需要 1-3 份，超过 5 份说明该拆任务了。

## 三种模式

- **讨论模式**：只出主意、查资料、给建议，不碰文件。
- **计划模式**：先出完整方案，用户批准后才执行。
- **执行模式**：按已批准方案动手写文件。

用户没说「直接写」，默认先给方案。每章写完展示评审结果，不静默改写。

## 分步工作流

### 1. 三层递进问答（开新书）

每层确认后再进入下一层，不要一口气问完：

- **核心定位**（必答）：题材创意、主角设定、核心冲突。
- **深度定制**：世界观、视角基调、主题、读者定位、篇幅。
- **拍板**：候选标题、确认配置。

已有明确需求可直接跳过。详见 [`writer-brief.md`](references/writer-brief.md)。

### 2. 拆书与题材研究（可选）

选同题材代表作，拆结构、伏笔、爽点节奏、人设，提炼手法写进 `经验库.md`。题材模板、复合题材规则、题材雷达、拆书流程见 [`genre-research.md`](references/genre-research.md)；题材库见 [`genre-catalog.md`](references/genre-catalog.md)，公式与机制见 [`genre-writing-formulas.md`](references/genre-writing-formulas.md)、[`genre-core-mechanics.md`](references/genre-core-mechanics.md)。

### 3. 文风学习（可选）

跑 `scripts/style_analyze.py` 做量化统计，通读样本按词汇/句式/描写/对话/节奏/叙述六维提炼，生成 `lorebook/风格卡.md`，试写校准后供每章引用。多份样本走**三层风格链**（source pack → manifest → composed），最终只引用 composed 层。没有样本可先用番茄下载器取范文（[`novel-download.md`](references/novel-download.md)），再用 `scripts/prepare_samples.py` 整理语料。

两条硬规矩：

- **风格卡跑参数，文风总纲跑规则**，两份文件分工写死、不互相抄。样本 3 份以上时另编译 `lorebook/文风模仿要求.md`。
- **建卡前先做参数交叉校验**：对话率与段均互斥，短句率+段均+句长+高对话率四者不能同时成立。详见 [`style-learning.md`](references/style-learning.md)「建卡时的参数交叉校验」。

学特征不抄句子，输出不含样本原文。

### 4. 项目搭建

`scripts/init_novel.py <目录> --title <书名>` 初始化。目录规范与**按读写权限分层**（哪些区走确认门、哪些区只追加、哪些区只增不改）见 [`project-structure.md`](references/project-structure.md)。

五步：① 一句话核心（主角+目标+障碍+代价）② 世界书框架进 `lorebook/` ③ 角色五件套（动机/缺陷/欲望/秘密/弧光）④ 写 `plot/罗盘.md` ⑤ 定历法与开局状态。方法与体系刻度见 [`world-engine.md`](references/world-engine.md)、[`character-design-methods.md`](references/character-design-methods.md)。

### 5. 世界状态与提交链

`world-state/` 是动态真相源，存「按时间排列的变更记录」，不存当前状态。每章完成后在 `commits.md` 追加：章号、新事实、审查状态、备份位置。

只记会影响后续一致性的变更；带时间戳、主体、来源章节；历史只追加不回改。写正文时只查不改，新事实写完后回补。规则见 [`world-engine.md`](references/world-engine.md)。

### 6. 剧情规划

在 `plot/` 维护五份：

| 文件 | 装什么 |
|---|---|
| `罗盘.md` | 长期承诺 / 近期焦点 / 必须保留 / 必须避免 |
| `structure.md` | 四级大纲（总纲→卷→幕→节→章）、承载树与因果树、章间逻辑链 |
| `promises.md` | 承诺账本、伏笔时间线、伏笔 DAG（依赖不满足的标阻塞） |
| `decisions.md` | ADR 式决策记录，推翻留痕 |
| `specs/` `briefs/` | 章节规格与任务书，命名 `第XXX章.yaml` / `第XXX章-brief.md` |

每章规划还要确认**信息控制**：读者知道什么、主角知道什么、必须隐瞒什么、只能暗示什么。四级大纲、两棵树、MICE、伏笔 DAG 与钩子布局见 [`plot-workbench.md`](references/plot-workbench.md)、[`hooks-chapter.md`](references/hooks-chapter.md)。

### 7. 章节写作（六道关卡）

动笔前编译 **Writer Brief**（[`writer-brief.md`](references/writer-brief.md)），上下文按 canonical packet 只装本章需要的最小集合。

1. **预检**：目录、时间线、承诺账本、上一条提交是否齐全；本章依赖的事实是否已入账；对齐罗盘。
2. **任务书**：写 Brief（目标、视角、锚点、信息控制、应兑现承诺、风格卡、字数）；需 spec 驱动则先写 `plot/specs/第XXX章.yaml`（[`chapter-spec.md`](references/chapter-spec.md)）。
3. **起草**：只用已批准事实，守视角纪律，新伏笔先登记再写。禁写事项自动叠加 [`写作约束.md`](references/写作约束.md)。
4. **审查（可阻断）**：六维——爽点、一致性、节奏、OOC、连贯性、追读力；P0/P1/P2 分级。事实矛盾、OOC、漏兑现必须修。见 [`review-rubrics.md`](references/review-rubrics.md)。
5. **润色与去 AI 味**：按下表跑，表层修完仍不过再往架构层走。

   | 层 | 工具 | 说明 |
   |---|---|---|
   | 硬禁令 | `check_prose.py` | 「需修改」必须清零，人工判断项结合语境复核 |
   | 静态痕迹 | `novel_lint.py`、`aigc_detect.py` | 行级命中 + 全文指纹；`--qwen` 可加模型佐证 |
   | 质量兜底 | `check_quality.py`、三个 Node 脚本 | 词汇、病句、标点规范化 |
   | 架构层 | Sepia 三遍 | 表层修完仍不过时用，见 [`sepia-guide.md`](references/sepia-guide.md) |

   规则与改法统一查 [`anti-ai-prompts.md`](references/anti-ai-prompts.md)，**它是本类唯一的入口**，其余检测文档只讲分工不重复列词表。
6. **提交与备份**：新事实进 `timeline.md`，承诺同步，写 `commits.md`，正文备份。

中途失败可断点续跑，已可信完成的步骤不重做。

### 8. 评审与回补

每章结束给四态报告：**已完成 / 部分完成 / 需要你处理 / 未完成**，固定三段（产物与完成情况、问题与耗时、下一步建议）。定期做项目体检：时间线、承诺账本、提交链、经验库是否一致，到期伏笔是否积压。

把本章摘要（2-5 句，含新事实与新伏笔）写回提交链与正文头部，这就是**有界章节记忆**：续写只加载上一章正文与摘要。旧稿导入与整书导出见 [`openwrite-core.md`](references/openwrite-core.md)。

### 9. 批量自动推进

「推进 N 章」走章节 spec + 批量循环（规划→生成→评审→修订），配置与报告模板见 [`chapter-spec.md`](references/chapter-spec.md)，骨架脚本 `scripts/auto_write.py`。

## 资源

### references/

**先读 [`references/README.md`](references/README.md)**，那里有完整分类索引与「按任务找文件」表。本处只列四个最常用的入口：

| 文件 | 什么时候读 |
|---|---|
| [`README.md`](references/README.md) | 不知道该读哪份时 |
| [`writer-brief.md`](references/writer-brief.md) | 每章动笔前 |
| [`anti-ai-prompts.md`](references/anti-ai-prompts.md) | 去 AI 味、判断某句像不像 AI |
| [`project-structure.md`](references/project-structure.md) | 建项目、改目录、理权限分区 |

### scripts/

| 脚本 | 用途 |
|---|---|
| `init_novel.py` | 初始化项目工作区 |
| `style_analyze.py` | 统计样本文风特征 |
| `prepare_samples.py` | 把下载的 txt/epub 整理成干净语料 |
| `auto_write.py` | 批量推进骨架（需 pyyaml，缺失降级 JSON） |
| `novel_lint.py` | 静态扫描 AI 写作痕迹 |
| `aigc_detect.py` | AIGC 痕迹检测，`--html` 出报告，`--qwen` 加深度检测 |
| `check_prose.py` | 活人感硬禁令检查，分「需修改」与「需人工判断」 |
| `check_quality.py` | 质量检测（词汇、错别字、病句、套路表达） |
| `audit_rules.py` | **技能自身的结构体检**：规则冲突、词表副本、入口体积、导航覆盖 |

`check-ai-patterns.js`、`check-degeneration.js`、`normalize-punctuation.js` 为 Node 辅助脚本。

## 维护约定

改这个技能时守住两条，改完跑 `python scripts/audit_rules.py` 验收：

- **规则只改真源。** 禁用词与禁句的唯一真源是 `anti-ai-prompts.md` 2.3 / 2.3.1；标点政策在第〇部分。其余文件（`写作约束.md`、`style-craft.md`、`llmlint.md`）一律引用不复述。
- **验收口径：规则冲突 0、词表副本 1。** 「词表副本 1」指只有 `anti-ai-prompts.md` 在整表罗列禁用词，其他文件出现同样的词只允许是零散举例。

新增参考文件时，同步更新 `references/README.md` 的分类表，否则审计会报孤儿文件。
