# Pi Agent 極簡書：極簡 Harness，無限可能

本書專為想要駕馭 [Pi](https://pi.dev/)（[@earendil-works/pi-coding-agent](https://www.npmjs.com/package/@earendil-works/pi-coding-agent)）的工程師設計。Pi 是一個極簡的 AI Agent 框架（Agent Harness），核心哲學是 **「讓 Agent 適應你的工作流程，而非讓你適應 Agent」**。它刻意不做 sub-agents、plan mode、permission popups，而是保留強大的擴充介面（Extensions）與上下文工程（Context Engineering）機制，讓你能打造專屬的 AI 助手。

> 前言：為什麼需要極簡 Agent Harness？
> Agent 框架的繁複困局——功能越多，自由越少。Pi 的答案是 **Primitives, Not Features**：別人內建的功能，你自己用幾十行 TypeScript 就能打造，或從 [Pi Packages](https://pi.dev/packages) 安裝。

## 第一章：快速上手（Quickstart）

- 一、快速上手
   - [1.1 安裝與環境準備](1.1.md)
   - [1.2 四大執行模式：Interactive / Print / RPC / SDK](1.2.md)
   - [1.3 模型設定與切換：15+ 提供商與自訂 Provider](1.3.md)

## 第二章：會話管理與樹狀歷史（Tree-Structured History）

- 二、會話管理與樹狀歷史
   - [2.1 樹狀會話：單一檔案，無限分支](2.1.md)
   - [2.2 /tree：在對話分支間自由穿梭與書籤](2.2.md)
   - [2.3 匯出與分享：/export 與 /share](2.3.md)

## 第三章：精準控制——上下文工程（Context Engineering）

- 三、上下文工程
   - [3.1 指令檔架構：AGENTS.md 與 SYSTEM.md](3.1.md)
   - [3.2 Skills 與 Prompt Templates：漸進式揭露](3.2.md)
   - [3.3 Compaction：上下文壓縮與自訂摘要](3.3.md)
   - [3.4 Steer 與 Follow-up：Agent 工作中途的人工干預](3.4.md)

## 第四章：極限擴充——Extensions 與 Packages

- 四、擴充與套件
   - [4.1 TypeScript Extensions：自訂命令、工具、快捷鍵與 TUI](4.1.md)
   - [4.2 工具整合：內建 MCP 與 Codemode 沙箱](4.2.md)
   - [4.3 Pi Packages 生態：打包與分享你的擴充](4.3.md)

## 第五章：實戰範例（Recipes & Use Cases）

- 五、實戰範例
   - [5.1 讓 Pi 為自己寫擴充：自我修改的 Agent](5.1.md)
   - [5.2 結合 tmux 實現多 Agent 協同](5.2.md)
   - [5.3 打造自動化 CI/CD 與代碼審查工作流](5.3.md)

## 第六章：常用速查表（Cheat Sheet）

- 六、速查表
   - [6.1 常用內建命令](6.1.md)
   - [6.2 快捷鍵指南](6.2.md)
   - [6.3 Pi vs OpenCode：差異與選擇](6.3.md)
