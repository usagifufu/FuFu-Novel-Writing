#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""初始化小说项目工作区（目录 + 模板文件）。

用法:
    python init_novel.py <项目目录> [--title 书名] [--calendar gregorian|simple|custom]
"""

import argparse
import os
import sys


TEMPLATES = {
    "lorebook/world.md": """# 世界观（稳定设定）

## 一句话世界观
<!-- 这个世界最核心的一条规则或气质 -->

## 力量体系 / 规则
<!-- 魔法/武学/科技等体系：来源、代价、上限 -->

## 历史大事
<!-- 只写不会随剧情改变的历史背景 -->

## 势力
<!-- 名称、立场、关系（静态部分） -->
""",
    "lorebook/characters/index.md": """# 角色卡

<!-- 每个核心角色一节。只写稳定设定；会变的（伤势、位置、关系现状）进 world-state/。 -->

## 主角
- 身份与背景：
- 目标（想要什么）：
- 障碍（什么挡着）：
- 代价（得到要付出什么）：
- 缺陷与弱点：
- 秘密（谁知道/谁不知道）：
- 弧光（故事结束时变成什么样）：
- 说话语气与习惯：
""",
    "lorebook/风格卡.md": """# 风格卡

<!-- 手写，或走文风学习流程从样本文件统计提炼（scripts/style_analyze.py + references/style-learning.md）。每章 Brief 引用。 -->

- 来源样本：
- 基调：
- 句长（平均/短句率）：
- 段落（平均长度/短段占比）：
- 描写密度（动作/氛围/心理；感官偏好）：
- 对话（密度/标签用法/人物语气差异）：
- 用词（高频特色词/口头禅/避免的词）：
- 句式习惯（设问/排比/反问强度）：
- 节奏（快慢；收尾方式）：
- 叙述（视角/人称/距离）：
- 禁学特征：
""",
    "lorebook/locations.md": """# 地点与势力（静态部分）

## 主场景
- 名称：
- 地理/氛围：
- 重要设定：
""",
    "manuscript/000-大纲.md": """# 全书大纲

## 一句话故事
<!-- 主角 + 目标 + 障碍 + 代价 -->

## 卷结构（承载树）
<!--
- 卷一：...
  - 幕一：...
    - 第 1 章：...
-->

## 剧情线（因果树）
<!-- 每条线：起点、推进节点、终点（如何算关掉） -->
""",
    "world-state/calendar.md": """# 历法

策略：{calendar}
<!--
gregorian：现实公历，支持公元前
simple：简化纪年，如 "第 372 年 春"
custom：自定义月份、周期、闰法
-->

时间表达示例：
""",
    "world-state/subjects.md": """# 主体登记（有状态的事物）

<!-- 只列会影响后续一致性的属性。会变的（伤势、位置、物品、关系）写在这里并在 timeline.md 中记录每次变更。 -->

## 主角
- 类型：人物
- 关键属性：
""",
    "world-state/timeline.md": """# 切面时间线（只追加，不回改）

<!-- 不存当前状态，只存按时间排列的变更。任意时刻状态 = 该时刻之前所有切面推算。 -->

| 时间 | 主体 | 变更 | 来源 |
| --- | --- | --- | --- |
| 开局 | 主角 | 初始状态登记 | 开局设定 |
""",
    "world-state/commits.md": """# 章节提交链

<!-- 每章完成 = 一条提交：新事实进 timeline、章节摘要写回（有界章节记忆）、审查状态、正文备份。续写先看最后一条提交。 -->

| 提交 | 章节 | 新事实 | 本章摘要 | 审查状态 | 备份位置 |
| --- | --- | --- | --- | --- | --- |
| C-001 |  |  |  |  |  |
""",
    "经验库.md": """# 项目长期记忆（经验库）

<!-- 两类内容：1) 拆书所得的手法（钩子类型、爽点密度、伏笔间隔）；2) 本书实证有效的写法与踩过的坑。来源标注章号/书名。 -->

## 拆书所得

## 本书实证
""",
    "plot/罗盘.md": """# 创作罗盘

<!-- 每次规划与动笔前对齐。长期承诺与必须保留是硬约束；近期焦点当前有效；必须避免是红线。改动记入 plot/decisions.md。 -->

## 长期承诺（本书不可动摇的核心）
- 主题/核心冲突：
- 主角弧光终点：
- 核心关系与最终悬念：

## 近期焦点（当前卷/近十章目标）
- 本卷目标：
- 近十章推进的线：

## 必须保留（读者已记住、不能撤回的元素）
- 已兑现承诺/关键物件：
- 已成事实：

## 必须避免（红线）
- OOC 行为：
- 设定冲突：
- 无回报拖戏：
""",
    "plot/structure.md": """# 剧情结构

## 四级大纲（总纲 → 篇/卷 → 幕 → 节 → 章）
- 总纲：
- 卷一：
  - 幕一：
    - 节：第 1 章 -

## 承载树（故事在哪里讲：卷 → 幕 → 节 → 章 → 正文）

## 因果树（故事为什么发生：阶段 → 剧情线 → 场景）

<!-- 场景字段：场景结果（达成/未达成/无冲突/被动承受）、节奏角色、剧情线类型（MICE：环境/谜题/角色/事件） -->

## 章节关系图谱（思维链）

<!-- 每章三行：回应（开头回应了哪章的钩子）、埋设（结尾把钩子留给哪章）、关系类型（因果/呼应/并行/转折） -->
""",
    "plot/promises.md": """# 承诺账本（伏笔 = 对读者的欠债）

| 编号 | 承诺 | 依赖 | 埋下章 | 推进节拍 | 兑现章 | 状态 | 类型 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P-001 |  |  |  |  |  | 埋下 | 铺垫兑现/预言/母题/镜像对照 |

<!-- 依赖：P-B 依赖 P-A 兑现才能揭晓时，在依赖列写 P-A；依赖未满足的兑现自动标为阻塞。 -->
""",
    "plot/decisions.md": """# 创作决策记录（ADR）

<!-- 拍板当场存档：决定、动机、风险必填；放弃写明原因；推翻留痕。罗盘改动也在此记录。 -->

## D-001：初始设定拍板
- 决定：
- 动机：
- 风险：
- 状态：已拍板 / 未决
""",
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="初始化小说项目工作区",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("dir", help="项目目录路径")
    parser.add_argument("--title", default="未命名小说", help="书名（写入大纲标题）")
    parser.add_argument(
        "--calendar",
        choices=["gregorian", "simple", "custom"],
        default="gregorian",
        help="历法策略",
    )
    args = parser.parse_args()

    root = os.path.abspath(args.dir)
    if os.path.exists(root) and os.listdir(root):
        print(f"[错误] 目录已存在且非空，拒绝覆盖: {root}")
        return 1

    # 空目录：审查报告、备份、章节规格与任务书
    # specs 与 briefs 目录同样预先建好：chapter-spec.md 要求把规格写到
    # plot/specs/第XXX章.yaml，auto_write.py 也按这个路径拼文件名读规格。
    for rel in ("审查报告", "备份", "plot/specs", "plot/briefs"):
        os.makedirs(os.path.join(root, rel), exist_ok=True)

    for rel in TEMPLATES:
        path = os.path.join(root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        content = TEMPLATES[rel].format(calendar=args.calendar)
        if rel == "manuscript/000-大纲.md":
            content = f"# {args.title} 大纲\n" + content
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        print(f"[OK] {rel}")
    for rel in ("审查报告", "备份", "plot/specs", "plot/briefs"):
        print(f"[OK] {rel}/")

    print(f"\n项目已初始化: {root}")
    print("下一步：填 lorebook/（稳定设定）→ plot/罗盘.md（创作罗盘）→ world-state/（开局状态与提交链）→ plot/（剧情结构）。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
