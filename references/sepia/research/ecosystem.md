# anti-AI／humanizer 生態系調查（2026-08-27）

## TL;DR
- 生態系擁擠但幾乎全在表面風格層。龍頭 blader/humanizer（38.3k★，Siqi Chen，源自 Wikipedia Signs of AI writing）。
- 唯一引用 StoryScope 的是 asavvin-pixel/unslop（58★），但用在論說文段落結構，非小說敘事。
- 敘事層（tidy plots、explicit themes、缺 nonlinearity、缺 intertextuality、embodied emotion overuse）＝空白市場。
- 詞彙 tells 會隨模型世代過期（Wikipedia Historical indicators、asavvin wordlist expiry 都承認）。

## 主要資源
1. blader/humanizer（38.3k★, MIT）：35 patterns（Content/Language/Style/Chatbot/Filler 五類）＋False Positives 白名單＋二次自問 pass「what still makes this obviously AI-generated?」＋voice matching。
2. Wikipedia: Signs of AI writing：上游源頭。Content/Language/Style/Communication/Markup 分類；Historical indicators 證明 tells 會過期；有「Signs of human writing」反向清單。
3. asavvin-pixel/unslop（58★）：三層（typography→vocabulary→structure/epistemics）；Level 3 引 StoryScope 數據（77/52、81/38、47/24、28/7、59/38）；「outline test」診斷法（段首句排大綱，太乾淨＝machine-shaped）；「slack」概念（允許 1-2 句平凡句）；voice calibration → style-profile.md。
4. sam-paech antislop 系：antislop-sampler（355★, backtracking + phrase 機率調整；ban "Elara" 等 AI 慣用名）、slop-forensics、EQ-Bench Slop Score（words 60% + not-x-but-y 25% + trigrams 15%；自承不測 narrative structure）、auto-antislop（FTPO 微調）。
5. mshumer/unslop（536★）：方法論可搬——對 domain 大量取樣→找模型 defaults→產 skill.md（可遷移到敘事層：同 premise 生成 N 篇比對 plot shape 收斂）。
6. Fiction/RP 社群（HawThorne Directives、Sukino banned tokens）：banned patterns（sensation-through-body-part、involuntary body verbs、filter words felt/seemed/noticed）、banned words（ozone、petrichor、shimmering、thrums）；anti-loop rule；Chekhov's Gun Rack。禁的是「這批字」不是「策略」。
7. 其他：Aboudjem/humanizer-skill（197★, 55 patterns + metrics CLI burstiness/MATTR）、haowjy/creative-writing-skills（429★, 24 skills）、pshort05/ClaudeHumanizer（10+3 pass）、ossa-ma tropes gist（listicle in a trench coat、fractal summaries、invented concept labels）、berenslab/llm-excess-vocab（~900 詞）、gutenberg-dpo。
8. anthropics/skills 官方無 humanizer 類。
9. 注意授權：walterwritesai/no-slop 是 CC BY-ND（禁衍生）勿參考內文。

## Gap（差異化空間）
1. 詞彙層紅海且會過期；修好只值 1.6pp。
2. Thematic over-explanation（fiction 的 telling-the-theme）：無人處理。
3. Tidy single-track plots：無人處理，主流 craft 工具（beat sheets）反而強化。
4. Embodied emotion overuse：只有詞彙殘影（禁字），無策略層規則。
5. Intertextuality：40+ 資源零覆蓋。
6. Nonlinear structure（flashback、frame narrative、in medias res）：fiction 語境零覆蓋。
7. 敘事層 AI-tell linter／評分：空白市場。
8. 可借方法：mshumer 取樣法、blader 二次自問 pass、asavvin outline test（升級成敘事版 beat outline test）。
9. 格式教訓：單檔 SKILL.md＋MIT＋多平台安裝＋false-positive 白名單＋voice calibration；「slack」防止規則變成新的 tell。
