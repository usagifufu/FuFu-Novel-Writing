# AIGC 检测器接入指南（aigc-detector 融合版）

来源项目：[hoyo0210/aigc-detector](https://github.com/hoyo0210/aigc-detector)（类似朱雀AI的检测助手）。
本技能将其能力融合进写作流水线的 **润色与 Anti-AI 终检** 环节，分两层：

| 层 | 能力 | 是否需要 API | 速度 |
|---|---|---|---|
| 本地规则引擎（`scripts/aigc_detect.py`） | 行级 AI 痕迹标记 + 全文级指纹统计 | ❌ 免 API | 秒级 |
| Qwen 深度检测（`--qwen`） | 大模型判别文本来源，输出 7 字段报告 | ✅ 需 DASHSCOPE_API_KEY | 数秒 |

## 快速开始（免 API，推荐日常用）

```bash
cd scripts
python aigc_detect.py 稿件.md                 # 终端报告
python aigc_detect.py 稿件.md --html 报告.html  # 生成带高亮标记的 HTML 报告
python aigc_detect.py 稿件.md --json          # 机器可读 JSON
cat 稿件.txt | python aigc_detect.py --stdin   # 管道输入
```

HTML 报告会按颜色区分痕迹类型：红色=词语重复、蓝色=平衡句/"连…都"、绿色=复杂句式、黄色=正式表达、紫色=空泛总结、橙色=比喻堆砌。鼠标悬停查看理由。

## Qwen 深度检测（可选）

需要阿里云 DashScope API Key：

```bash
export DASHSCOPE_API_KEY=sk-xxxx
python aigc_detect.py 稿件.md --qwen --html 报告.html
```

环境变量（可选）：

- `QWEN_MODEL`：默认 `qwen-plus`
- `DETECT_TEMPERATURE`：默认 `0.2`（低温度保证一致性）
- `QWEN_TIMEOUT`：默认 `15` 秒

未配置 key 时 `--qwen` 自动降级为纯规则引擎，不报错。

## 部署完整 Web UI（可选）

原项目自带 FastAPI 后端 + React 前端，可本地起服务用浏览器检测：

```bash
# 方案 A：Docker
cd references/aigc-detector
cp backend/.env.example backend/.env   # 填入 DASHSCOPE_API_KEY
docker-compose up -d
# 前端 http://localhost:5173  后端 http://localhost:8000

# 方案 B：裸跑后端（只需 API 接口）
cd references/aigc-detector/backend
pip install -r requirements.txt
export DASHSCOPE_API_KEY=sk-xxxx
uvicorn app.main:app --port 8000
# POST /api/detect        {"text": "..."}
# POST /api/mark-traces   {"text": "..."}
```

## 检测维度清单

### 行级命中（规则引擎）

| 类型 | 说明 |
|---|---|
| `word_repetition` | 同一行内 4 字短语重复（4-gram 全汉字滑窗，修复了原项目空格分词失效问题） |
| `long_line` | 单行超 80 字，缺人类停顿 |
| `formal_*` | 正式表达：因此/此外/综上所述/总而言之/值得注意的是/需要强调的是/根据以上/不得不说/换句话说 |
| `sequential_connector` | 序列连接：首先…其次… |
| `complex_modifiers` | 多重"的"字修饰 |
| `causal_chain` | 因果链：通过…从而… |
| `parallel_structure` | 并列结构：以及…以及…、不仅…而且… |
| `balance_sentence` | 平衡句：不是A而是B、既…又…、与其…不如… |
| `even_structure` | "连…都"强调句式 |
| `fluff` | 空泛总结/万金油：这一刻仿佛、望向远方、嘴角勾起… |
| `metaphor_dense` | 单行 ≥2 处比喻 |

### 全文级指纹（跨行统计）

| 类型 | 阈值 | 说明 |
|---|---|---|
| `metaphor_high` | 全文比喻 ≥3 处 | 比喻堆砌是强 AI 指纹 |
| `pronoun_run` | 连续 ≥3 行以他/她/我开头 | 句首代词密度 |
| `word_freq` | 二字词全文 ≥8 次 | 高频词复读 |
| `phrase_freq` | 四字短语全文 ≥4 次 | 整段复读同一短语 |

## 在流水线中的位置

在 **步骤 5「润色与 Anti-AI 终检」**，与 `novel_lint.py` 配合：

1. `novel_lint.py` 跑静态扫描（填充词、机械过渡、公式化设问等模板痕迹）。
2. `aigc_detect.py` 跑 AIGC 痕迹（重复、平衡句、比喻密度、代词密度等指纹）。
3. AI 结合 `llmlint.md` 人工复核命中项，判断是否真要改（命中 ≠ 要改，语境优先）。
4. 需要第三方佐证时，加 `--qwen` 让大模型判别来源，或上传朱雀AI交叉验证。

> 铁律：检测是找候选位置，不是判决。是否修改由作者拍板，AI 不静默改写。

## 实战经验：检测反复不过时的终极解法（文体骨架化）

三轮检测"人工创作特征较弱"后验证：**换毛刺（改词、删比喻、拆长句）只能小幅降分；真正有效的是换文体骨架**。当规则引擎命中不多、但外部检测仍判"AI 特征弱"时，问题不在句子而在文体——纯第三人称独白（长段叙述+内心流）本身就是检测高危文体，无论表面多干净。

按以下优先级改造（自上而下，先换骨架再修句子）：

| 优先级 | 手法 | 说明 | 示例 |
|---|---|---|---|
| P0 | 加对话回合 | 叙述段改写成你来我往的对话，一句一问一答 | "早点睡！""嗯。""明天降温，多穿件。""嗯。" |
| P0 | 外部切面 | 切出主角视角，用旁观者/巨物/环境反应侧写事件，制造距离感 | 地球观测站视角看异象，而非主角自述 |
| P1 | 压缩铺陈 | 砍环境描写（树草鸟兽），只留与情节强相关的物件 | 三行场景 → 一行+一个关键物件 |
| P1 | 信息炸弹章末 | 章尾抛新信息/反转钩子，替代总结升华 | "那缕丝飘进巨兽鼻孔，巨兽开口：'你身上……有她的味道。'" |
| P2 | 毛刺清扫 | 上述改完后跑规则引擎，清掉残余重复/平衡句/比喻堆砌 | 见检测维度清单 |

配套：重跑规则引擎对比前后命中数；仍不过时检查是否整章仍是"单人独角戏"（对话回合数 < 3、无外部切面）。

## 当前启用状态（2026-09-01 确认）

- ✅ 本地规则引擎：`scripts/aigc_detect.py`，免 API，秒级，日常主力
- ✅ HTML/JSON 报告：`--html` 高亮报告、`--json` 机器可读
- ⚠️ Qwen 深度检测（`--qwen`）：未启用（未配置 DASHSCOPE_API_KEY）
- ⚠️ Web UI：未部署（用户确认 CLI 够用；需要时按上文 Docker/裸跑方案启动）
