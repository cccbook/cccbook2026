# B.4 權限控制：讓 AI 能做什麼、不能做什麼

## 為什麼需要權限控制

AI Agent 擁有強大的能力——它可以讀寫檔案、執行 Shell 命令、搜尋網路、甚至刪除資料。如果不加限制，一個錯誤的指令就可能造成不可逆的損害。權限控制（Permissions）是確保 AI 在安全範圍內工作的機制。

OpenCode 的權限系統設計原則是「預設寬鬆，按需收緊」。你可以針對每種操作設定不同的權限等級，也可以針對特定命令或檔案路徑做更精細的控制。

## 三種權限動作

每個權限規則會解析為以下三種動作之一：

| 動作 | 說明 |
|---|---|
| `"allow"` | 自動執行，無需確認 |
| `"ask"` | 執行前要求使用者確認 |
| `"deny"` | 直接封鎖，禁止執行 |

## 全域權限設定

在 `opencode.json` 中設定全域權限：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "*": "ask",
    "bash": "allow",
    "edit": "deny"
  }
}
```

上例的含義是：
- 所有操作預設需要確認（`"*": "ask"`）
- Shell 命令自動執行（`"bash": "allow"`）
- 檔案修改直接封鎖（`"edit": "deny"`）

你也可以用簡寫一次設定所有權限：

```json
{
  "permission": "allow"
}
```

這等同於所有操作都自動執行。在教學環境中不建議使用此設定。

## 可用的權限鍵

OpenCode 提供以下權限鍵，對應不同的工具類別：

| 權限鍵 | 控制的工具 |
|---|---|
| `read` | 讀取檔案 |
| `edit` | 寫入、編輯、套用補丁 |
| `bash` | 執行 Shell 命令 |
| `glob` | 檔案搜尋 |
| `grep` | 內容搜尋 |
| `task` | 啟動子 Agent |
| `webfetch` | 抓取網頁 |
| `websearch` | 網路搜尋 |
| `skill` | 載入技能 |
| `external_directory` | 存取專案目錄外的路徑 |
| `doom_loop` | 偵測重複執行的工具（預設 ask） |

## 精細化規則（Object 語法）

對於 `bash`、`edit` 等支援精細控制的權限，你可以使用物件語法，針對特定命令或路徑設定不同的動作：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "bash": {
      "*": "ask",
      "git status": "allow",
      "git diff": "allow",
      "git log *": "allow",
      "grep *": "allow",
      "rm *": "deny",
      "sudo *": "deny"
    },
    "edit": {
      "*": "ask",
      "docs/*.md": "allow"
    }
  }
}
```

規則的匹配邏輯是「最後匹配的規則勝出」（last match wins）。因此建議把通用的 `*` 規則放在前面，具體的規則放在後面。

萬用字元的規則如下：
- `*` 匹配零個或多個任意字元
- `?` 恰好匹配一個字元
- 其餘字元照字面匹配

## 環境目錄控制

`external_directory` 用於控制對專案工作目錄以外路徑的存取。例如允許讀取特定外部目錄但禁止修改：

```json
{
  "permission": {
    "external_directory": {
      "~/projects/personal/**": "allow"
    },
    "edit": {
      "~/projects/personal/**": "deny"
    }
  }
}
```

## Agent 層級的權限覆寫

你可以在個別 Agent 上設定不同的權限，覆寫全域設定：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "bash": { "*": "ask" }
  },
  "agent": {
    "build": {
      "permission": {
        "bash": {
          "*": "ask",
          "git status *": "allow",
          "npm run *": "allow"
        }
      }
    },
    "plan": {
      "permission": {
        "bash": "deny",
        "edit": "deny"
      }
    }
  }
}
```

在 Markdown 格式的 Agent 定義中，也可以直接在 frontmatter 設定：

```markdown
---
description: 只讀的程式碼審查 Agent
mode: subagent
permission:
  edit: deny
  bash:
    "*": deny
    "git diff": allow
    "git log*": allow
  webfetch: deny
---

你是一位程式碼審查員。只分析程式碼並提出建議，不做任何修改。
```

## 權限確認的互動方式

當操作設定為 `"ask"` 時，OpenCode 會在執行前提示你確認。你有三個選擇：

- **once** —— 只允許本次操作
- **always** —— 允許未來符合相同模式的所有操作（僅限當次 OpenCode 會話）
- **reject** —— 拒絕本次操作

## Auto 模式

啟動 OpenCode 時加上 `--auto` 參數，可以自動批准所有未被明確封鎖的權限請求：

```bash
opencode --auto
```

注意：明確設為 `"deny"` 的規則仍然生效，`--auto` 只影響原本應為 `"ask"` 的請求。在教學環境中，建議學生使用預設設定而非 auto 模式，以養成確認的習慣。

## 教學建議

在課堂中使用 OpenCode 時，建議以下設定：

```json
{
  "permission": {
    "bash": {
      "*": "ask",
      "git status": "allow",
      "git diff": "allow",
      "npm test": "allow"
    },
    "edit": "ask",
    "websearch": "allow"
  }
}
```

這個設定讓學生的 AI 可以自由搜尋網路與查看 Git 狀態，但修改檔案與執行較具風險的命令時需要確認。這能培養學生「先審視 AI 的提案，再決定是否執行」的良好習慣。

## 想一想

1. 如果你將所有權限設為 `"allow"`，可能帶來什麼風險？在什麼場景下這樣做是合理的？
2. `"ask"` 模式下出現的 `always` 與 `once` 有什麼差異？什麼時候該選 `always`？
3. 為什麼 `external_directory` 預設為 `"ask"` 而非 `"allow"`？

## 本章小結

權限控制是使用 AI Agent 時不可或缺的安全機制。OpenCode 提供 `"allow"`、`"ask"`、`"deny"` 三種動作，支援全域設定、精細化的命令/路徑匹配、以及 Agent 層級的覆寫。善用權限控制，能在享受 AI 效率的同時，保持對系統變更的掌控力。在教學環境中，建議使用 `"ask"` 為預設，培養學生審視 AI 輸出的習慣。
