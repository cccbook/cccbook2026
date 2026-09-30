# B.7 實戰：用 OpenCode 完成一個小專案

## 目標

本章透過一個完整的實戰練習，帶領你從零開始使用 OpenCode Desktop 建立一個小型的 Python 專案。你將體驗「與 AI Agent 協作」的完整流程：從專案初始化、需求分析、程式實作到測試驗證。

我們要建立的是一個 **CLI 版的待辦事項管理工具**（todo-cli），功能包括：
- 新增待辦事項
- 列出所有待辦事項
- 標記完成
- 刪除待辦事項
- 資料持久化（儲存到 JSON 檔案）

## 第一步：建立專案與初始化

### 建立專案目錄

```bash
mkdir todo-cli
cd todo-cli
git init
```

### 啟動 OpenCode Desktop

開啟 OpenCode Desktop，選擇 `todo-cli` 資料夾作為工作目錄。

### 初始化 AGENTS.md

在對話框中輸入：

```
/init
```

OpenCode 會掃覽專案（此時是空專案），產生一份基礎的 `AGENTS.md`。你可以在產生後手動補充專案資訊。

### 手動完善 AGENTS.md

在 OpenCode 中請它幫你編輯 `AGENTS.md`：

```
請幫我更新 AGENTS.md，加入以下內容：
- 這是一個 Python CLI 專案
- 使用 Python 3.10+
- 不使用任何外部套件，只用標準庫
- 資料儲存在 todo.json
- 需要提供單元測試
- 程式碼風格遵循 PEP 8
```

## 第二步：規劃（Plan Mode）

切換到 Plan 模式（按 Tab 鍵切換），讓 Agent 只規劃不實作：

```
我需要一個命令列的待辦事項管理工具。功能如下：
1. 新增待辦事項：python todo.py add "買牛奶"
2. 列出所有事項：python todo.py list
3. 標記完成：python todo.py done 1
4. 刪除事項：python todo.py remove 1
5. 資料存在 todo.json 中

請先提出實作方案，不要修改任何檔案。
```

Agent 會回應一份實作計畫，包括：
- 檔案結構（可能只有一個 `todo.py`）
- 資料結構設計（JSON 格式）
- 各功能的實作方式
- 測試策略

檢視計畫後，如果滿意就切回 Build 模式（再按一次 Tab）：

```
計畫看起來很好。請開始實作。
```

## 第三步：實作（Build Mode）

Agent 會開始建立檔案。你可以觀察它的工作過程：
- 建立 `todo.py`，實作 argparse 命令列介面
- 實作 JSON 檔案的讀寫邏輯
- 建立 `test_todo.py`，編寫單元測試

如果 Agent 的實作有需要調整的地方，直接告訴它：

```
請在 remove 指令中加入確認提示，避免誤刪。
```

### 實作過程中的常用指令

| 指令 | 用途 |
|---|---|
| `/undo` | 還原上一步的檔案變更 |
| `/redo` | 重做被還原的變更 |
| `@todo.py` | 在 prompt 中引用特定檔案 |
| Tab 鍵 | 切換 Build / Plan 模式 |

## 第四步：測試與驗證

請 Agent 執行測試：

```
請執行測試，確保所有功能正常運作。
```

Agent 會執行類似以下的命令：

```bash
python -m pytest test_todo.py -v
```

如果測試失敗，Agent 會分析失敗原因並嘗試修復。這正是 AI Agent 的價值——它不僅寫程式，還能自行驗證與迭代修正。

你也可以手動測試 CLI 功能：

```bash
python todo.py add "完成期末報告"
python todo.py add "閱讀第 8 章"
python todo.py list
python todo.py done 1
python todo.py list
python todo.py remove 2
python todo.py list
```

## 第五步：完善與版本控制

確認功能正常後，請 Agent 幫你補充文件：

```
請建立一份 README.md，說明安裝方式、使用方法與專案結構。
```

最後提交到 Git：

```
請幫我把所有檔案 commit 到 Git，提交訊息用 "feat: initial todo-cli implementation"。
```

## 完整協作流程圖

```mermaid
graph TD
    A[建立專案目錄] --> B[啟動 OpenCode Desktop]
    B --> C[/init 初始化 AGENTS.md]
    C --> D[切換 Plan Mode<br/>規劃實作方案]
    D --> E{方案是否滿意?}
    E -->|否| F[提供回饋<br/>修改方案]
    F --> D
    E -->|是| G[切換 Build Mode<br/>開始實作]
    G --> H[執行測試]
    H --> I{測試通過?}
    I -->|否| J[Agent 自動修復]
    J --> H
    I -->|是| K[補充文件]
    K --> L[Git Commit]
```

## 協作心法

**1. 先規劃後實作**

善用 Plan Mode，讓 AI 先提出方案。你可以在不觸動程式碼的情況下審視與討論，確認方向正確後再切換到 Build Mode 執行。

**2. 給足上下文**

好的 Prompt 應該包含：你要什麼功能、限制條件（如只用標準庫）、預期的輸入輸出格式。越具體的描述，AI 的實作越準確。

**3. 保持掌控**

AI 是協助者而非決策者。每個步驟都先看 AI 的提案，確認合理再批准執行。遇到不符合預期的輸出，用 `/undo` 還原後重新描述需求。

**4. 善用 @ 引用**

用 `@` 符號引用特定檔案，能幫助 Agent 精確理解你要修改的目標：

```
請在 @todo.py 的 done 函式中加入日期時間戳記
```

**5. 小步迭代**

不要一次提出十個功能。先完成核心功能並驗證，再逐步新增。這與敏捷開發的「增量交付」原則一致。

## 想一想

1. 在這個實戰練習中，哪些步驟是你做決策的、哪些是 AI 做決策的？你認為理想的分工應該是什麼？
2. 如果 AI 產生的程式碼有 bug，你會怎麼處理？直接請 AI 修、還是自己先分析？
3. 這個工作流程與你在過去作業中「自己從頭寫」的方式，有什麼本質上的差異？

## 本章小結

本章透過建立一個 Python CLI 待辦事項工具，完整演示了使用 OpenCode Desktop 進行 AI 輔助開發的流程：初始化專案、撰寫 AGENTS.md、在 Plan Mode 規劃方案、在 Build Mode 實作程式碼、測試驗證、以及版本控制。核心心法是「先規劃後實作、給足上下文、保持掌控、小步迭代」。AI Agent 是強大的協作夥伴，但最終的決策權與品質把關仍在於開發者自己。
