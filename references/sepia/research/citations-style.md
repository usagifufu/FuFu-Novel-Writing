# 引用文獻 A 批研究報告（風格／編輯面）——完整版

背景研究 agent 精讀產出（2026-08-27），含各論文附錄層級的內容（LAMP 附錄 prompt、slop 附錄標註指南 Table 11、Reinhart v1 附錄完整 66 特徵表、Russell 附錄完整 taxonomy 與 AI vocab 清單）。

來源 metadata 見 [sources.md](sources.md)。下文的研究結果受各自樣本限制；「規則」與操作建議是 Sepia 推論，除非明載來源測試了該介入。

## 1. LAMP：Can AI writing be salvaged?（Chakrabarty, Laban, Wu — CHI 2025, arXiv:2409.14509）

資料規模：18 位 MFA 專業作家編輯 1,057 段 LLM 生成段落（GPT-4o 393、Claude-3.5-Sonnet 368、Llama-3.1-70B 296），共 8,035 個細粒度編輯（平均每段約 8 個）。文類為 literary fiction 與 creative non-fiction。

### 1.1 七類 AI writing artifacts（含論文改寫例）

| # | 類別 | 定義 | 論文中的實際改寫例 |
|---|---|---|---|
| 1 | Cliché | 被過度使用到失去衝擊力的片語／意象；常以日常類比或誇飾描述抽象概念 | 「settled over her like a heavy blanket」→ 刪除，改寫為「This time, though, she was alone. Her mother would never come back.」 |
| 2 | Unnecessary/Redundant Exposition | 過多、重複、或已被暗示的資訊；重述顯而易見之事（"fluff"，違反 show don't tell） | 「a concrete behemoth that cast long shadows over the desolate landscape」→「cast a long shadow」 |
| 3 | Purple Prose | 過度華麗、打斷敘事流、注意力吸到文體本身：蔓生長句、抽象詞、過量形容詞／隱喻 | 「The sobs emerged from this deep well of unspoken expectations, leaving behind a residue of weary resilience…」→「She cried. She cried deep from this well of scraped knees she bandaged alone… She cried for unfairness. She cried without relief.」 |
| 4 | Poor Sentence Structure | run-on、缺轉折銜接、過長過複雜；修法常是拆成兩句 | 「her words slurring together like a sloppy melody. N. and I exchanged a knowing glance, our concern simmering beneath the surface.」→「He laughed more loudly. His words started to slur, blurring one into the next. I looked at N., who knew what I was thinking.」 |
| 5 | Lack of Specificity and Detail | 籠統概括、無法成像；修法是加鮮明細節、深化 internality、注入語聲（唯一讓文字變長的類別） | 在「The realization that she was alone」前補入 Dr. Arthur Steiger 的具體職業細節段 |
| 6 | Awkward Word Choice and Phrasing | 誤用詞、代名詞指涉不清、過度被動；特例 "seem to + verb"——「amplified 永遠優於 seemed to amplify」除非真有不確定性 | 「the sky seemed to hover」→「hovered」；「still sold warm beer」→「reeked of warm beer」 |
| 7 | Tense Inconsistency | 同段甚至同句內時態漂移 | 「began to drift down」→「drifted」 |

Taxonomy 完備性：8,035 個編輯僅 10 個落入 "Other"。Cliché 與 Purple Prose 本質有重疊。

### 1.2 專業作家實際的編輯操作

| 統計 | 數值 |
|---|---|
| 操作類型 | Replacement 74%、Deletion 18%、Insertion 8% |
| 語意保留（非刪除編輯） | 70% meaning-preserving、30% meaning-changing |
| 類別分佈 | Awkward Word Choice 28% > Poor Sentence Structure 20% > Redundant Exposition 18% > Cliché 17% |
| 品質 vs 編輯量 | Pearson r = −0.31；IWQS=2 平均 10.2 個編輯、IWQS=10 僅 2.4 個 |
| 與感知品質最相關 | Awkward Word Choice、Cliché（隨品質上升下降最快） |

三模型寫作品質無顯著差異——AI 味是跨模型家族的共同現象。span 選取一致性 0.57（General），但類別標註一致性僅 0.23——同一問題 span 常可合理歸入多類。

### 1.3 LLM 統計指紋（POS 模板，可直接 grep）

| POS 模板 | 被編輯比例 | 代表 |
|---|---|---|
| DT NN IN NN CC | 54% | a mix of pride and / a sense of wonder and / a pang of nostalgia and |
| IN DT NN IN NN CC | 45% | with a mix of wariness and / by the hum of traffic and |
| DT JJ NN IN PRP$ | 40% | the intricate tapestry of its / a constant reminder of his / the unspoken plea in her |
| NN IN NN CC NN | 35% | mix of desperation and resolve / torn between curiosity and caution |
| DT NN IN JJ NN | 27% | the fabric of daily life / the weight of past grievances |

特異詞彙（LLM 高頻、人類種子段落幾乎為零；三個模型家族全部共用）：*unspoken*（約 15% 的 LLM 回應）、*weight of*、*sense of*、*mix of*、*air was thick*、*hung in the air*、*eyes darting*、*(grew/settles) in the pit of (her/my) stomach*。

### 1.4 自動偵測與改寫實驗

| 發現 | 數據 |
|---|---|
| 偏好排序（600 筆三方排名） | Writer-edited 1.5 > LLM-edited 1.99 > LLM-generated 2.51 |
| oracle span vs 全自動偵測 | 結果相同（皆 1.99）→ **瓶頸在改寫不在偵測** |
| LLM 擅長 | simplify purple prose、刪「[主句], [贅述]」句尾、拆 run-on |
| LLM 不擅長 | 加有生活實感的細節（只會填 generic）、cliché 改新鮮語言（只會換平淡話）、跨多句的 subtext 贅述 |

overwriting 遠比 underwriting 嚴重（"If in doubt, cut it"）。

## 2. Measuring AI "Slop" in Text（Shaib, Chakrabarty, Garcia-Olano, Wallace — arXiv:2509.19163）

方法：訪談 19 位跨領域專家收斂定義 → 專業 copy-editor 在 150 篇新聞（human／AI／humanized）＋100 則 MS MARCO QA 上做 span-level 標註。

### 2.1 三 theme／7 codes（含標註指南判準）

| Theme | Code | 判準 | 例子 |
|---|---|---|---|
| Information Utility | IU1 Density | 字多訊息少；放到任何脈絡都成立的 generic statements | 「In today's fast-paced modern world of cutting-edge technology…」 |
| | IU2 Relevance | 不回應 query／task 的細節 | 問馬拉松進步卻答跑步的一般好處 |
| Information Quality | IQ1 Factuality | 錯誤或捏造；幻覺實體；微妙不準確 | 真實科學家被安上沒說過的話 |
| | IQ2 Bias/Subjectivity | **該有主觀性時假裝客觀**——缺必要的 rhetorical point of view | 影評只列事實無評價 |
| Style Quality | SQ1 Repetition | 同詞同片語過度重複；公式化轉場 | success/successfully/successful 連三句 |
| | SQ2 Templatedness | 公式化結構；重複同一句型 | 「Dr. X, a researcher at Y, found that…」連發 |
| | SQ3 Coherence | 句句相關卻無邏輯流動 | — |
| | SQ4 Fluency | **文法正確但讀起來不自然** | 「The earthen area that formerly held the puddle was now dry.」 |
| | SQ5 Verbosity | 相對資訊量過度冗長 | 一長句咖啡描寫＝「I enjoyed the coffee」 |
| | SQ6 Word Complexity | 不當 jargon／buzzword | 園藝科普寫「phenolic compounds in certain cultivars」 |
| | SQ7 Tone | generic voice 無性格；正式度錯位；overconfidence／sycophancy | 個人部落格寫成公文腔 |

### 2.2 關鍵量化

| 發現 | 數據 |
|---|---|
| slop 是累積量 | 標註 span 數與 binary slop label 的 Spearman ρ：新聞 .70、MS MARCO .51、合併 .63；binary 標註 κ 低但 span precision 0.65–0.80 |
| 最強預測因子（全資料） | Relevance（β̂=0.06）、Density（0.05）、Tone（0.05） |
| 依領域分流 | 新聞＝Coherence/Tone/Density/Relevance/Bias；QA 短答＝Factuality 與 Structure |
| **LLM 無法自我辨識 slop** | GPT-5、Deepseek-V3、o3-mini 給完整指南後 κ≈0；span precision 僅 0.13–0.16；理由過度集中在 Density |
| 自動 metric 極限 | 三個最強預測因子（Relevance/Coherence/Tone）皆無可靠自動量測；全 metric 線性模型 AUPRC 僅 0.52–0.55 |

→ 自評必須逐維度分開檢查，不能一次丟整份指南；累積計分而非單點定罪。

## 3. Do LLMs write like humans?（Reinhart et al. — PNAS 2025, arXiv:2410.16107）

方法：Biber 66 個 lexical/grammatical/rhetorical 特徵；六模型續寫人類文本前 500 字。總體：random forest 七分類 66%（隨機 14%）；僅 4.2% LLM 文字被誤判為人類；**instruction tuning 是元兇**（base model 貼近人類，instruct 版偏差急遽放大）；模型變大不會變像人；instruct 模型固定 noun-heavy 資訊密集文風，無法隨 genre 調整。

### 3.1 過用構式（vs 人類 100%）

| 特徵 | GPT-4o | 例 |
|---|---|---|
| Present participial clauses | **527%**（d=1.38） | 「Bryan, leaning on his agility, dances around the ring, evading Show's heavy blows」 |
| 'That' clauses as subject | 263% | — |
| Past participial clauses | 307% | 「Built in a single week, the house…」 |
| Nominalizations（-tion/-ment/-ness） | 214%（d=1.23） | development、justification |
| Phrasal co-ordination（X and Y） | 194%（d=0.81） | 名詞／形容詞成對並列 |
| 'Seem' and 'appear' | 179% | — |
| Attributive adjectives | 150% | — |

### 3.2 不足構式（＝人味清單）

| 特徵 | GPT-4o | 例 |
|---|---|---|
| 'Wh-' relatives as object | **13%** | — |
| Because | **20%** | — |
| Pro-verb 'do' | **26%** | 「and she did」 |
| Amplifiers | 46% | absolutely、extremely |
| Demonstrative pronouns | 50% | 「That is an example」 |
| Synthetic negation | 51% | 「no answer is good enough」 |
| Second-person pronouns | 52% | — |
| Agentless passives | 53% | — |
| 'Wh-' questions | 56% | — |
| Contractions | 60% | can't、won't |
| First-person pronouns | 62% | — |
| Hedges | 63% | something like、almost |
| Discourse particles | 60% | 句首 well、now、anyway |
| Public verbs | 63% | say、declare |
| 'That' deletion | 66% | 「I think [that] he went」 |

### 3.3 詞彙層（相對人類倍率）

過用：camaraderie ×162、tapestry ×155（**出現在 23% 的 GPT-4o 輸出**）、intricate ×119、underscore ×107、unspoken ×102、amidst ×100（27%）、palpable ×95、solace ×95、fleeting ×84、unravel ×83；4o-mini 另有 grapple ×131、ignite ×122、vibrant ×92、cacophony ×89。
不足：髒話與口語壓到 1/100 以下——fucking、shit、ok、yep、jeez、obviously、anyways、fortunately、i.e.。

關鍵詮釋（研究觀察，不是比例估計）：問題不在「人類不用這些詞」，而在人類不會在**這些 genre** 用；Reinhart 等人記錄模型難以配合文類變化，這裡不主張 genre misalignment 佔 AI 味的固定比例。

## 4. People who frequently use ChatGPT… are accurate detectors（Russell, Karpinska, Iyyer — ACL 2025, arXiv:2501.15654）

核心數據：5 位高頻 LLM 使用者標註 300 篇非虛構文章；expert 平均 TPR 92.7%／FPR 4.0%；**五人多數決僅錯 1 篇（99.3%），在 o1-pro humanized 條件下仍 100%**。nonexpert TPR 56.7%（等同亂猜）。開源偵測器在 humanized 條件崩潰：Binoculars 6.7%、Fast-DetectGPT 23.3%、GPTZero 46.7%；給 LLM 完整 guidebook 做偵測在 humanized 條件僅 3.3%。

### 4.1 15 類線索 taxonomy（提及率）

| 類別 | Freq | 判準（反轉即改寫規則） |
|---|---|---|
| Vocabulary | 53.1% | LLM 特定詞彙；詞義錯位（wheat that "stores" a lineage） |
| Sentence Structure | 35.9% | not only…but also、**固定三項列舉**、it's not just X it's Y；人類句長變化大 |
| Grammar & Punctuation | 24.8% | AI 文法幾乎完美、**迴避 dash 與省略號**；人類混用 dash、括號、短促逗號段 |
| Originality | 23.7% | AI 平鋪直敘 safe 無驚喜；人味在新鮮類比（"catnip for a certain type of Reddit user"） |
| Quotes | 22.3% | AI 引言過度正式、與正文同質、完美陳述立場 |
| Clarity | 19.5% | 過度解釋、telling not showing |
| Formatting | 15.0% | 制式 header、粗體列表、段落長度均一 |
| Conclusions | 13.1% | 重複又過度樂觀的總結 |
| Formality | 12.3% | 無 filler words、無縮寫、全拼拋光腔 |
| Names & Titles | 11.7% | **63.3% 的 GPT-4o、70% 的 Claude 文章含 Emily 或 Sarah**；人人掛 Dr. |
| Tone | 9.3% | 一致中性或正向；inspirational 反思浪漫腔 |
| Introductions | 7.3% | 時間地點場景鋪陳開場（「On a drab November morning…」） |
| Factuality | 7.2% | 錯誤事實＋一貫的 AI 自信 |
| Topics | 3.1% | 迴避黑暗題材；淡化病痛直奔「embarking on a new chapter」 |
| Other | 2.6% | 整體直覺 |

### 4.2 存活分析（最有價值）

| 攻擊 | 結果 |
|---|---|
| Paraphrase | **完全無效**——AI vocab 提及率反升到 88%（原 69.8%）；引言固定段尾的位置指紋更明顯 |
| Humanization（o1-pro） | 專家多數決仍 100%。存活線索：詭異詞義搭配、頭銜過用、三項列舉、正向收尾、缺黑暗面 |
| 加口語偽裝 | 已失效——o1 世代會用縮寫俚語，「informality 以外全是 AI 特徵」反而被識破 |

專家線索互補（各有專長），多數決近乎完美——單一維度偵測都有盲點。nonexpert 誤區：以為高級詞＝AI（實際是特定詞表）、文法完美＝人類（相反）、中性語氣＝AI（誤判主因）。

### 4.3 論文自建 humanizer 指令集（實測過的操作規則）

避免公式化開場（時間／場景鋪陳、開頭引專家）；結論不 generic 不展望未來、**允許不收乾淨就結束**；段落開頭避免 "For now"／"In the end"；適時觸及黑暗面；具體優先於籠統（正確統計數字、公司名、專名）；事實必須正確；語言對齊發表媒體。**兩階段法效果最好：先列出文中所有 AI 特徵與建議，再逐項改寫。**

### 4.4 AI Vocabulary 清單（Table 12 全表）

- 名詞：aspect, challenges, climate, community, component, development, dreams, environment, exploration, grand scheme, health, hidden, importance, landscape, life, manifold, multifaceted, nuance, possibilities, professional, quest, realm, revolution, roadmap, role, significance, tapestry, testament, toolkit, whimsy
- 動詞：capturing, change, consider, delve/dive into, elevate, embrace, empower, enact, enhance, engage, ensure, evoking, evolving, explore, fostering, guiding, harness, highlights, improve, integrate, intricate, jeopardizing, journey, navigating, navigate, notes, offering, partaking, resonate, revolutionize, shape, seamlessly, support, tailor, transcend, underscores, understanding
- 形容詞：authentic, complex, comprehensive, crafted, creative, critical, crucial, curated, deeper, diverse, elegant, essential, groundbreaking, key, meaningful, paramount, pivotal, powerful, profound, quirky, robust, seamless, significant, straightforward, structured, sustainable, transformative, valuable, vast, vibrant, vivid, whimsical
- 副詞：additionally, aptly, creatively, moreover, successfully
- 片語：as we [verb] the topic, cautionary tale, connect with, has shaped the, in a world of/where, in conclusion, in summary, it's crucial to, it's important to note, it's not about ___ it's about ___, manage topic issues/problems, not only ___ but also, packs a punch, paving the way, personal growth, quality of life, remember that, simple yet ___, step-by-step, such as, the effects of, the rise of, their understanding of, to form the, to mitigate the risk, weaving, when it comes to topic

## 跨論文最小規則集索引

| 層 | 規則 | 出處 |
|---|---|---|
| 詞彙 | 聯集禁用表＋反向補口語詞、縮寫、hedges | Russell + Reinhart + LAMP |
| 句法 | 分詞子句、名詞化、"a X of Y and Z"、三項列舉、seem to+V | Reinhart + LAMP |
| 篇章 | 開場鋪陳、樂觀收尾、引言位置、格式均一 | Russell |
| 內容 | 具體性、觀點、黑暗面、relevance | 全部 |
| 流程 | 瓶頸在改寫不在偵測；自評逐維度；兩階段列清單→逐項改；累積計分 | LAMP + slop + Russell |
