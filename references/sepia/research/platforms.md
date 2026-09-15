# 四平台 plugin 格式研究（2026-08）

核心結論：四平台已收斂到 Agent Skills 開放標準（agentskills.io）。同一份 SKILL.md 可直接共用；只需打包層 adapter。

## 共通規格（canonical 要守住的）
- `skill-name/SKILL.md`；name ≤64 字元、小寫+hyphen、＝資料夾名
- description 1–1024 字元（what + when，關鍵字前置）
- frontmatter 只用 spec 六欄位：name, description, license, compatibility, metadata, allowed-tools（claude.ai 上傳會對其他欄位報錯）
- SKILL.md 本體 <500 行 / <5000 tokens；細節放 references/（相對路徑、一層深）
- progressive disclosure：啟動只載 name+description（~100 tokens）
- 驗證：`skills-ref validate ./my-skill`

## 各平台接入
| 平台 | 位置 | 觸發 | 轉換 |
|---|---|---|---|
| Claude Code | `~/.claude/skills/` / `.claude/skills/` / plugin `skills/`；plugin.json 在 `.claude-plugin/`；marketplace.json | 自動 + `/name` | 不用 |
| Codex | `.agents/skills/`（cwd→repo root→`~`）；`.codex-plugin/plugin.json`；custom prompts 已 deprecated | 自動 + `$name` | 不用 |
| Grok Build | 自動吃 Claude Code 的 skills/plugins/marketplaces；也有 `.grok/skills/` | 自動 + `/name` | 不用（零設定相容 Claude Code） |
| Antigravity | plugin `skills/`、`.agents/skills/`（與 Codex 同目錄）或 `~/.gemini/config/skills/` | 自動 + `/name` | 不用；workflows 已 deprecated |

## 建議 repo 佈局
```
repo/
├── skills/<name>/SKILL.md + references/   # canonical 唯一真相
├── .claude-plugin/plugin.json + marketplace.json
├── .codex-plugin/plugin.json              # "skills": "./skills/"
├── .agents/workflows/<name>.md            # legacy Antigravity 相容；新入口直接用 skills
└── README.md                              # native host installers + manual Antigravity copy
```
- Claude Code plugin 的 skills 預設路徑就是 `./skills/` → 零設定
- Grok 免安裝（自動發現 Claude 的安裝結果）
- Codex 與 Antigravity 共用 `.agents/skills/` checkout
- Antigravity CLI 1.1.22 的 `agy plugin validate .` 會處理 plugin `skills/` 下的五個 skill；內建 migration 文件把 workflows 標為 deprecated，skill 名稱本身就是 slash command

官方文件：
- https://agentskills.io/specification
- https://code.claude.com/docs/en/skills / plugins-reference / plugin-marketplaces
- https://developers.openai.com/codex/skills / plugins/build/plugins
- https://docs.x.ai/build/features/skills-plugins-marketplaces
- https://antigravity.google/docs/skills / rules-workflows
