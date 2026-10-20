# B.3 AGENTS.md：為 AI 寫一份崗位說明書

## 為什麼需要 AGENTS.md

AI Agent 就像一位新加入團隊的成員。它具備能力，但不了解你的專案——不知道用什麼框架、怎麼跑測試、有哪些慣例要遵守。`AGENTS.md` 就是你遞給這位新成員的「崗位說明書」，告訴它：這個專案是什麼、該怎麼工作、有哪些規則要遵守。

在 OpenCode 中，`AGENTS.md` 的內容會被加入 LLM 的上下文（context），直接影響 Agent 的行為。寫得好的 `AGENTS.md` 能讓 AI 更準確地協助你，減少來回修正的次數。

## AGENTS.md 的位置與優先順序

OpenCode 會從多個位置讀取規則檔：

| 位置 | 用途 | 是否納入 Git |
|---|---|---|
| 專案根目錄 `AGENTS.md` | 專案專屬規則，與團隊共享 | 建議納入 |
| `~/.config/opencode/AGENTS.md` | 個人全域規則 | 否 |
| `CLAUDE.md`（備援） | 相容 Claude Code 格式 | 視情況 |

如果專案同時存在 `AGENTS.md` 與 `CLAUDE.md`，OpenCode 只會讀取 `AGENTS.md`。

## 如何建立 AGENTS.md

### 方法一：自動產生

在 OpenCode 中執行 `/init` 指令。它會掃描專案中的重要檔案，自動產生一份包含以下資訊的 `AGENTS.md`：

- 建構、lint、測試指令
- 專案架構與目錄結構
- 程式碼慣例與特殊注意事項
- 對既有規則檔（如 Cursor Rules）的參考

### 方法二：手動撰寫

以下是某個 TypeScript 專案的 `AGENTS.md` 範例：

```markdown
# SST v3 Monorepo Project
This is an SST v3 monorepo with TypeScript. The project uses bun
workspaces for package management.

## Project Structure
- `packages/` - Contains all workspace packages (functions, core, web, etc.)
- `infra/` - Infrastructure definitions split by service (storage.ts, api.ts, web.ts)
- `sst.config.ts` - Main SST configuration with dynamic imports

## Build & Test Commands
- Install dependencies: `bun install`
- Run dev server: `bun dev`
- Run tests: `bun test`
- Lint: `bun lint`

## Code Standards
- Use TypeScript with strict mode enabled
- Shared code goes in `packages/core/` with proper exports configuration
- Functions go in `packages/functions/`
- Infrastructure should be split into logical files in `infra/`

## Conventions
- Import shared modules using workspace names: `@my-app/core/example`
- All API endpoints must include input validation
- Write unit tests for business logic; integration tests for API endpoints
```

## 撰寫原則

### 1. 具體明確，避免模糊

差的寫法：「遵循良好的程式碼風格」
好的寫法：「使用 2 空格縮排、單引號字串、分號結尾」

### 2. 包含可執行的指令

Agent 需要知道怎麼建構、測試你的專案。明確寫出：

```markdown
## Commands
- Install: `npm install`
- Dev: `npm run dev`
- Test: `npm test`
- Lint: `npm run lint`
- Build: `npm run build`
```

### 3. 描述架構而非實作細節

Agent 可以自己讀懂程式碼，但需要你解釋的是「為什麼」——為什麼分成這些模組、資料流是什麼、有哪些隱含的約束。

### 4. 指出特殊注意事項

```markdown
## Gotchas
- `config/database.ts` uses a custom connection pool; do not modify the pool size
- The `legacy/` directory uses CommonJS; do not convert to ESM
- Environment variables must be prefixed with `APP_`
```

## 引用外部文件

如果規則內容很長，可以拆分成多個檔案，再透過 `opencode.json` 的 `instructions` 欄位引用：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": [
    "CONTRIBUTING.md",
    "docs/coding-standards.md",
    "docs/testing-guide.md"
  ]
}
```

這些檔案會與 `AGENTS.md` 合併，一起加入 Agent 的上下文。

## 實務建議

**對團隊而言**：將 `AGENTS.md` 納入 Git，作為專案文件的一部分。每次專案結構或慣例有重大變更時，同步更新。

**對個人而言**：在 `~/.config/opencode/AGENTS.md` 放置個人偏好設定，例如偏好的程式碼風格、語言（例如要求 AI 用繁體中文回應）等。

**對課程而言**：教師可以為每個作業專案維護一份 `AGENTS.md`，統一學生使用 AI 輔助時的行為規範。

## 想一想

1. 如果你要為本課程的期末專案撰寫 `AGENTS.md`，你會包含哪些內容？
2. `AGENTS.md` 與一般軟體專案中的 `README.md` 有什麼不同？它們的讀者分別是誰？
3. 為什麼自動產生的 `/init` 不能完全取代手動撰寫？

## 本章小結

`AGENTS.md` 是你與 AI Agent 之間的溝通橋樑。它定義了專案的背景資訊、建構方式、程式碼慣例與特殊注意事項。透過 `/init` 可以快速自動產生，但手動撰寫能更精準地控制 Agent 的行為。撰寫時應具體明確、包含可執行指令、描述架構意圖，並指出特殊注意事項。建議將其納入版本控制，作為團隊知識管理的一環。
