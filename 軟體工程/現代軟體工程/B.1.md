# B.1 OpenCode 是什麼：從 CLI 到 Desktop

## AI Coding Agent 的時代

過去幾年，AI 輔助程式設計工具百花齊放。從最早的語法自動補全，到如今能自主規劃、修改檔案、執行命令的「AI Agent」，這個領域正在經歷根本性的轉變。理解這些工具之間的差異，有助於我們選擇最適合自己工作流程的方案。

## 主流 AI 編碼工具比較

目前市面上幾個主要的 AI 編碼工具，各有不同的定位與特色：

**GitHub Copilot** 以 IDE 整合為核心，提供行內（inline）的程式碼補全與聊天功能。它深度嵌入 VS Code、JetBrains 等編輯器，擅長即時的語法建議與小範圍的程式碼生成。但本質上它仍然是一個「被動式」的輔助工具——需要開發者主動觸發，且修改範圍通常侷限於當前游標位置附近。

**Cursor** 是一個基於 VS Code 的分支（fork），將 AI 深度整合到編輯器之中。它支援跨檔案的智慧編輯、Composer 模式下的多檔案修改，以及較強的程式碼理解能力。Cursor 的優勢在於編輯器體驗流暢，但缺點是它綁定在自己的 IDE 中，使用者必須遷移到 Cursor 才能使用。

**Claude Code** 是 Anthropic 推出的 CLI 介面 AI Agent。它以終端機為操作介面，具備檔案讀寫、Shell 執行、Git 操作等能力。Claude Code 的特色是「Agentic」——它能自主規劃步驟、執行命令、觀察結果並迭代修正。但它僅提供 CLI 介面，對不熟悉終端機的使用者有一定門檻。

**OpenCode** 則是一個開源的 AI Coding Agent，由社群驅動（GitHub 上已超過 195,000 顆星）。它的核心理念是「Agent-as-a-Service」——AI 不只是補全程式碼，而是能像一位團隊成員一樣，理解專案架構、規劃實作方案、執行修改並驗證結果。最重要的是，OpenCode 提供了多種介面：

- **Desktop App**（桌面應用程式）—— 圖形化介面，操作直覺，推薦一般使用者與學生
- **TUI**（終端機使用者介面）—— 在終端機中運行的互動式介面，適合進階使用者
- **CLI**（命令列介面）—— 可嵌入腳本或 CI/CD 流程
- **IDE Extension** —— 整合到 VS Code 等編輯器中
- **Web** —— 透過瀏覽器使用

## OpenCode 的核心差異化

OpenCode 與上述工具有幾個關鍵差異：

**1. 開源且不綁定特定 IDE**

OpenCode 是開源專案，使用者可以自由檢視、修改、部署。不像 Cursor 綁定特定 IDE，OpenCode 可以在任何環境中運行。

**2. 多模型支援**

OpenCode 支援 75 種以上的 LLM Provider，包括 Anthropic Claude、OpenAI GPT、Google Gemini，甚至本地模型。你也可以直接使用 GitHub Copilot 或 ChatGPT Plus/Pro 的帳號。

**3. 真正的 Agent 能力**

OpenCode 內建多種 Agent 模式：
- **Build** —— 全功能開發模式，可讀寫檔案、執行命令
- **Plan** —— 規劃模式，只分析不修改，適合先審視方案再實作
- **Explore** —— 只讀探索，快速搜尋程式碼庫
- **General** —— 多步驟任務的通用 Agent
- **Scout** —— 外部文件與相依性研究

**4. 不只是編碼工具**

雖然 OpenCode 以「Coding Agent」為名，但它的能力不限於寫程式。你可以用它來：

- **技術寫作** —— 撰寫文件、報告、論文章節
- **資料分析** —— 讀取 CSV/JSON 檔案、撰寫分析腳本、生成視覺化圖表
- **研究工作** —— 搜尋網路、讀取論文、整理文獻回顧
- **系統管理** —— 撰寫 Shell 腳本、設定 CI/CD、管理伺服器配置

只要是你能在終端機或編輯器中完成的工作，OpenCode 都能協助。差別在於它擁有自主決策的能力——你不僅是下指令，而是與一個能理解脈絡的 Agent 協作。

## 選擇建議

| 需求場景 | 推薦工具 |
|---|---|
| 輕量級語法補全 | GitHub Copilot |
| 在 IDE 中深度 AI 整合 | Cursor |
| 開源、多模型、多介面 | OpenCode |
| 純終端機 Agent 工作流 | OpenCode CLI/TUI 或 Claude Code |
| 初學者、非程式背景 | OpenCode Desktop |

## 安裝方式預覽

OpenCode Desktop 可從官方網站（https://opencode.ai/download）直接下載，支援 macOS、Windows 與 Linux。CLI 版本則可透過一鍵腳本安裝：

```bash
curl -fsSL https://opencode.ai/install | bash
```

詳細安裝步驟將在下一章說明。

## 想一想

1. 你目前使用的 AI 編碼工具是什麼？它屬於「被動式輔助」還是「主動式 Agent」？
2. 如果 AI 能自主執行 Shell 命令並修改檔案，你認為哪些場景會受益最大？哪些場景需要格外小心？
3. OpenCode 是開源專案，這對你的學習與使用有什麼意義？

## 本章小結

本章介紹了 AI Coding Agent 的發展背景，比較了 GitHub Copilot、Cursor、Claude Code 與 OpenCode 的定位差異。OpenCode 是一個開源、多模型、多介面的 AI Agent，不僅能輔助編碼，也能用於寫作、研究與資料分析等多種場景。接下來的章節將帶領你完成安裝、設定與實戰練習。
