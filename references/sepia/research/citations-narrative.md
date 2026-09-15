# 引用文獻 B 批研究報告（敘事結構／創意面）

（由背景研究 agent 產出，2026-08-27）

來源 metadata 見 [sources.md](sources.md)。下文的研究結果受各自樣本限制；「規則」與操作建議是 Sepia 推論，除非明載來源測試了該介入。

## 1. NarraBench（Hamilton, Wilkens & Piper 2025, arXiv 2510.09869）

理論根基：Genette 敘事三角（story/discourse/narration）＋ Herman situatedness。
4 dimensions → 12 features → 50 aspects：
- Story: Agent(name,role,attributes,emotions,motivation) / Social Net(interaction,connections,relationship) / Event(event,schema,causality) / Plot(topic,plotline,moral,obstacle,conflict,archetype) / Structure(plot arc) / Setting(setting,location)
- Narration: Perspective(POV,focalization,dialogue) / Style(allusion,figurative,imageability,complexity,evaluative)
- Discourse: Time(duration,order) / Revelation(suspense,curiosity,surprise)
- Situatedness: Paratext(genre,author,date,medium,platform) / Motivation(intent)

僅 27% 敘事任務被既有 benchmark 覆蓋；events、style、perspective、revelation 幾乎完全缺席（＝模型最未被校準、最易露餡的軸）。
「perspectival（無正解）」面向是人味所在：moral、motivation、emotion 應保留分歧與曖昧。

## 2. Beguš 2024〈Experimental Narratives〉（arXiv 2310.12902）

250 篇人類 vs 80 篇 GPT-3.5/4，Pygmalion 主題。
AI 重複模式（禁用清單素材）：
- 開場公式：「Once upon a time」式抽離時空、先介紹角色再進情節；人類以衝突開場
- 泛用場景："a bustling metropolis teeming with innovation"、"the vibrant city of Elysia"
- 結尾說教定律："love knows no boundaries"、"love transcends artificiality"
- 重複命名：Ava（10 次）、Victor、Adam/Eve、Eliza、Amelia
- 無黑暗面：techno-positive；操縱、欺騙、背叛缺席
人類有而 AI 缺：孤獨、喪失替代、暴力、社會非難；隱性動機鋪陳；「允許故事壞掉」。
性別：表面配置進步、形容詞層仍刻板（女=beauty/grace/kindness；男=intelligence/perfection）。

## 3. Xu et al.〈Echoes in AI〉PNAS 2025（arXiv 2501.00273）

Sui Generis score：前綴截斷重採樣 K=20，看情節段是否必然重現。
- 人類 SG ~13–14；GPT-4 ~8–9；drop ratio（必然情節）人類 3.7% vs GPT-4 11.3%（高 7–9 倍）
- Kafka〈Give It Up〉續寫：5 次全是「警察熱心指路」；沒有一次到達原作冷峻反諷
- 跨模型互相 echo；人類情節幾乎不可重現
- LLM 中段 SG 驟降：節奏過快、懸念懸置不解釋
自檢規則：「同 prompt 重生成 20 次，這轉折會再出現嗎？會就砍。」中段需至少一個不可預測事件；鼓勵拒絕解決的反諷式結尾。

## 4. Tripto et al.〈Beyond Checkmate〉EMNLP 2025（arXiv 2501.19301）

- choke point 在中段（body）：人機分歧最大；開頭結尾 LLM 模仿最好
- 人類跨段落變異 > LLM：人會調變自己的語言指紋；AI 全文均勻一致
- burstiness（句構/用詞起伏）是關鍵訊號；「開頭太標準漂亮」本身就是 AI 訊號
規則：火力集中中段；段落間刻意改變句長節奏、密度、語域；允許局部失衡。

## 5. Namuduri et al.〈QUDsim〉COLM 2025（arXiv 2504.09373）

QUD＝每段所回答的隱含問題；LLM 的 QUD 序列模板化。
- LLM 彼此 discourse template 重用率 0.8–1.2 vs 對人類 0.3–0.4
- 重複四步：場景簡報 → 為欺瞞辯護 → 社會後果 → 責任的重負
- 過用：線性一問一答、consequence+procedural QUD（18.8%）；少用：comparative、verification（0.2–0.3%）、記憶回溯式非線性
規則：大綱層介入——列各段隱含 QUD，直線型即重排；注入比較／驗證（質疑前段敘述）／回溯 moves。

## 6. Chakrabarty, Ginsburg & Dhillon 2026（arXiv 2510.13939）

模仿 50 名家、MFA vs in-context LLM vs 微調 GPT-4o；Pangram classification rate 97%→3%。
- cliché 密度在該實驗的 mediation 分析中由 16.4% 降至 1.3%；這是實驗特定估計，1.3% 的信賴區間包含 0。
- 微調消除：purple prose、過度雕琢比喻、「polite, predictable, inoffensive, upbeat」聲音、多餘 exposition／說教、公式化結構
- MFA 讀者風格忠實度 odds ratio 0.16 → 8.16（翻轉）
- 一般讀者盲測的風格忠實度偏好不顯著（OR 1.06），品質偏好反而偏向 AI 版本（OR 1.82）；這是偏好結果，不是一般讀者 AI 偵測能力的測試，研究也未顯示他們會因文字可被偵測而懲罰它。
規則優先序：先殺 cliché → 過度比喻 → 說教；允許敘事者粗魯、偏頗、不討喜；驗收用「訓練有素讀者」視角。

## 7. Nonaka & Perry 2025（arXiv 2510.18932）

帶符號角色網絡，4 LLM vs Gutenberg 人類科幻：
| 指標 | LLM | 人類 |
|---|---|---|
| 網絡密度 | 0.338–0.470 | 0.182 |
| 平均邊權（情感） | +0.24~+0.66 全正 | −0.061 |
| 正向子網聚類 | 0.531–0.589 | 0.259 |
| 負向子網聚類 | 0.072–0.212 | 0.395 |
規則：(a) 網絡保持稀疏，部分角色僅間接相連 (b) 關係情感總和中性偏負 (c) 敵意要成結構（反派要有自己的關係網、同盟、內鬨）。「所有人都認識主角、都對主角友善」＝AI 指紋。

## 跨論文分層地圖

| 層 | 同質化模式 | 出處 |
|---|---|---|
| 情節元素 | echo 轉折（drop ratio 7–9 倍）、中段趕拍 | Xu |
| 篇章結構 | QUD 模板（簡報→辯護→後果→反思）、缺比較/驗證/回溯 | QUDsim |
| 段落位置 | 中段最露餡；全文風格均勻 | Tripto |
| 表層風格 | cliché、purple prose、說教、inoffensive upbeat | Chakrabarty |
| 主題情感 | techno-positive、無黑暗、道德收尾、重複命名 | Beguš |
| 社會結構 | 過密、全正向、無敵對網絡 | Nonaka & Perry |
| 檢查骨架 | 4×12×50；events/style/perspective/revelation 最無監督 | NarraBench |
