# StoryScope 研究摘要（skill 設計的 evidence base）

> 來源：Jenna Russell、Rishanth Rajendhran、Chau Minh Pham、Mohit Iyyer、John Wieting (2026)。*StoryScope: Investigating idiosyncrasies in AI fiction*。arXiv:2604.03136v6（2026-08-10 修訂）。UMD + Google DeepMind。完整來源 metadata 見 [sources.md](sources.md)。
> Code/data: https://github.com/jenna-russell/storyscope （taxonomy.json = 304 features 完整定義）

## 一句話結論

AI 小說即使把表面風格（em-dash、"delve"、詞彙）洗掉，**敘事結構層的選擇**仍可被偵測（narrative features alone: 93.2% macro-F1；在所研究的 LAMP 編輯條件與樣本中，風格改寫後仍 93.9%）。這支持 Sepia 將敘事架構置前的設計推論；StoryScope 沒有測試「先改敘事架構、再改表面風格」的介入順序。

## 方法（可信度依據）

- 10,272 個 writing prompts（從 Books3 人類短篇逆向工程），人類 + 5 個 LLM（Claude Sonnet 4.6、GPT-5.4、Gemini 3 Flash、DeepSeek V3.2、Kimi K2.5）各寫一篇 → 61,608 篇，平均 ~4,753 字。
- Pipeline：故事 → NarraBench 結構模板（JSON）→ 跨來源比較 → feature discovery → 304 個可解釋敘事特徵（10 維度）→ XGBoost + SHAP。
- 特徵標註 reliability：Krippendorff's α=0.90；human–model Cohen's κ=0.84（高於 human–human 0.74）。
- 長度、主題、記憶污染都做過 ablation，結論不變。
- 二元偵測 93.2%（narrative only）/ 96.0%（+style）；6-way 歸屬 68.4% / 77.3%。
- Core Only：以 30 個 core features 訓練的 XGBoost held-out classifier，84.8% macro-F1、AUPRC .828；這是分類器成績，不是人工 rubric 的效能。
- 人類故事在敘事特徵空間更「稀有」且更分散：rarity percentile 0.71 vs 0.49（Cohen's d=0.83）；human–AI centroid 距離是 AI–AI 的 1.6 倍；24.7% 人類故事落在最稀有的 10%。

## 30 個 core features（Table 16，含數值）

### AI 偏高（要壓低）——主題過度決定 Thematic over-determination
| Feature | Human | AI | 說明 |
|---|---|---|---|
| Thematic Explicitness & Moralizing (1-5) | 3.28 | 3.94 | 敘事者/角色把主題講白 |
| Moral / Philosophical Weighting (1-5) | 3.26 | 3.68 | 道德/哲學命題壓過娛樂性 |
| Thematic Unity (1-5) | 4.41 | 4.74 | 每個場景都服務同一主題核心 |
| Narratorial Thematic Commentary → yes | 52% | 77% | 敘事者跳出來評論主題 |
| Dialogue Function → philosophical debate | 34% | 59% | 對話變哲學辯論 |
| Reference Explicitness → implicit echoes | 50% | 72% | 只敢模糊致意、不敢點名 |

### AI 偏高——感官與身體化的表演 Sensory & embodied performativity
| Feature | Human | AI | 說明 |
|---|---|---|---|
| Emotional Expression → embodied | 38% | 81% | 情緒全用身體感覺/隱喻寫（喉嚨緊、胸口重）|
| Setting as Psychological Mirror (1-5) | 3.58 | 4.07 | 環境永遠映照內心 |
| Environmental & Ecological Emphasis (1-5) | 2.83 | 3.21 | 自然環境戲份過重 |
| Sensory Modalities → olfactory | 57% | 82% | 嗅覺意象氾濫 |
| Sensory Density (1-5) | 3.66 | 3.93 | 感官描寫密度偏高 |
| Depth of Interior Access (1-5) | 3.67 | 3.93 | 內心透視太深太常 |

### AI 偏高——結構流線化 Structural streamlining
| Feature | Human | AI | 說明 |
|---|---|---|---|
| Causal Chain Continuity (1-5) | 3.92 | 4.20 | 單一因果鏈從頭鎖到尾 |
| Spatial Granularity (ord) | 2.27 | 2.53 | 空間描寫過度精細 |
| Agency in Resolution → protagonist choice | 46% | 69% | 結局全靠主角自己的抉擇 |
| Character Introduction → external description | 30% | 52% | 用外貌/背景摘要介紹主角 |
| Subplot Integration → no subplots | 57% | 79% | 沒有支線 |
| Resolution Mode → internal understanding | 27% | 47% | 用「內心接受/釋懷」收尾 |
| Opening Spatial Grounding (ord) | 2.12 | 2.33 | 開場交代地點交代得太乖 |
| Pre-Threat Character Investment (1-5) | 2.76 | 2.99 | 危機前鋪墊做好做滿 |

### 人類偏高（要拉高）——互文豐富度 Intertextual richness
| Feature | Human | AI | 說明 |
|---|---|---|---|
| Intertextual Strategy → explicit named reference | 47% | 24% | 直接點名真實作品/作者/品牌/地名 |
| Reference Explicitness → balanced mix | 37% | 16% | 明引與暗引並用 |

### 人類偏高——讀者互動 Reader engagement
| Feature | Human | AI | 說明 |
|---|---|---|---|
| Fourth-Wall Permeability (ord) | 0.67 | 0.39 | 打破第四面牆（67% vs 39%）|
| Direct Reader Address (ord) | 0.28 | 0.07 | 直接對讀者說話（28% vs 7%）|

### 人類偏高——時間複雜度 Temporal complexity
| Feature | Human | AI | 說明 |
|---|---|---|---|
| Depth of Recontextualization After Surprise (1-5) | 3.28 | 2.95 | 揭露迫使重讀前文 |
| Chronological Discontinuity (1-5) | 2.40 | 2.12 | 時間跳躍 |
| Nonlinear Framing for Delayed Disclosure (1-5) | 1.96 | 1.68 | 用非線性結構延後揭露 |
| Anachrony Intensity (1-5) | 2.58 | 2.31 | flashback / flash-forward |

### 人類偏高——敘事多樣性 Narrative diversity
| Feature | Human | AI | 說明 |
|---|---|---|---|
| Location Variety Scope (ord) | 1.34 | 1.08 | 場景地點更多 |
| Dialogue-to-Narration Proportion (1-5) | 2.95 | 2.70 | 對話比例更高 |
| Subplot Integration → thematically parallel | 42% | 21% | 有支線且與主題平行呼應 |
| Moral Polarity → ambivalent/mixed | 59% | 38% | 主角道德曖昧 |
| Emotional Expression → explicit labels | 29% | 8% | 人類敢直接寫「she was afraid」 |

## §4.1 質性發現（直接可轉成規則的敘述）

1. **AI over-explains its themes**：敘事者明講主題 77% vs 52%；「a grieving character's arc will typically end with the narrator stating the lesson learned」。過度決定（over-determination）：把意義塞給讀者，不信任讀者自行推論。
2. **Human authors subvert linearity**：AI 單線、少支線、少 loose ends；「a human mystery might open at the funeral and spiral backward through decades, while AI tells the same story from first clue to the grand reveal」。人類的結局更常曖昧未決；AI 偏好 internal understanding/acceptance 收尾（47% vs 27%）。
3. **AI over-writes the body and senses**：「Where a human author might write that a character "felt afraid," AI renders fear as a tightening chest, cold sweat, and dimming lamplight.」——「show don't tell」被 AI 執行成教條。人類 29% 直接用情緒標籤，AI 只有 8%。
4. **Human authors engage the outside world**：人類點名真實文本/作者的比率近 2 倍（47% vs 24%）；AI 迴避真實品牌、地名、作品；人類承認讀者存在（aside to "you, dear reader"），「AI writes as though no one is watching」。
5. **AI writing has less diverse narrative features**：人類用更多地點、更多對話、支線與主題交織（42% vs 21%）、道德立場曖昧的主角（59% vs 38%）。

## 各模型指紋（Table 17 + §5，供 model-specific 校正）

- **Claude**（最容易辨識，26 個指紋）：事件強度攀升最平（flat escalation）、事件類型多樣性特徵強、敘事聲音最均勻；奉行「reverent/continuist」文學傳統（62% vs 39–56%）；愛 epilogue/flash-forward 結尾；避免夢境；setting mood 傾向 uncanny/haunted；偏好安靜結局而非 avalanche endings。
- **GPT**：gossip/rumor 作為情節機制（64% vs 44–55%）；愛用「多年/數十年後回望」的遠距回顧敘事者；比其他 AI 更愛顛覆期待（41%）；和解結局曖昧；ensemble 社會網絡達到人類水準。
- **Gemini**：結局收得最乾淨＋extended denouements；88% 場景 bleak/oppressive；愛 frequent flashbacks；主角社會軌跡擴張；siege/ordeal schema；夢境過多（abstract 提及）。
- **DeepSeek**：把關鍵 context 前置（front-loads）；narrator presence 明顯；情緒用 behavioral cues；backstory 均勻穿插。
- **Kimi**：指紋最少（3 個），位於 AI 分布的「generic center」；in-action / in medias res 開場；不做 explicit trait labeling。
- **Human 的指紋**（供模仿）：角色用「對話中」登場（in-dialogue, uniq 21.4）、單一 focal 聚焦、無直接稱呼的敘事者、**back-loaded revelation pacing**、crossover genre 的文學企圖。

## 其他要點

- Style 特徵的界線（App. B）：sentence/phrase-level texture = style；events, causality, closure, character roles, relationship topology, setting, temporal arrangement = narrative。跳過 style 仍偵測得到，反之 style-only 只有 85.8%。
- LAMP（Chakrabarty 2025）的 7 類 artifact 改寫在所研究的編輯樣本中，narrative classifier 仍維持高辨識表現；相較基準僅降 1.6 個百分點。
- Chakrabarty et al. 2026：在該研究的文學模仿實驗中，微調後 detector classification rate 從 97% 降到 3%；該 Readers study 測量風格與品質偏好，沒有測試敘事結構介入。
- 人類故事比 AI 長（median 4,973 vs 3,355 字），但偵測結果與長度無關（length-matched 後不變）。

## 對 skill 的結構性啟示（Sepia 設計推論）

以下是 Sepia 根據上述研究觀察提出的設計推論，不是 StoryScope 已測試的介入；除非另有明載，recipe 與 ordering 都不能解讀為效果證據。

1. Sepia 將兩層架構排成 **Pass 1 敘事架構**（30 core features 的觀察）→ **Pass 2 表面風格**（LAMP/slop 類規則）；這個順序未在 StoryScope 中作為介入比較。
2. Sepia 將 30 core features 的 `detection_method` 用作生成前設計與生成後人工檢查的素材；這不等於已驗證的自我評分 detector。
3. Sepia 把人類均值視為校準參考而非反轉目標：Thematic Explicitness 人類 3.28 非 1.0，Chronological Discontinuity 2.40 非 5.0；任何目標區間都是 editorial heuristic。
4. Sepia 以選擇性取用手法回應人類作品的多樣性：每篇只挑部分手法，避免形成新的 humanizer 指紋；此做法未由研究直接測試。
5. Sepia 將 model-specific 表格作為可能的校正提示，例如 Claude 的事件強度曲線與結尾習慣；這是 inference，不是介入效果。
6. Sepia 將人類偏高的特徵當作可選 recipe：in-dialogue 登場、back-loaded revelation、跨文類、真實世界專名、對讀者說話；研究數據本身不保證採用 recipe 會改善文字。
