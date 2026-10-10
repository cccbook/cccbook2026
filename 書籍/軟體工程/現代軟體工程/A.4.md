# A.4 GitHub 協作：Pull Request、Code Review、Issue

## 從本地端到雲端：GitHub 是什麼

Git 是版本控制系統，而 **GitHub** 是建立在 Git 之上的雲端協作平台。它提供了遠端版本倉的託管服務，更重要的是，它圍繞著 Git 建立了一整套團隊協作的工作流程。GitHub 上的專案稱為 **repository（版倉）**，任何人都可以建立自己的版倉來存放程式碼。

要開始使用 GitHub，你需要：

1. 在 [github.com](https://github.com) 註冊帳號
2. 在本機設定 Git 使用者資訊（只需設定一次）：

```bash
git config --global user.name "你的名字"
git config --global user.email "你的電子郵件"
```

## 連結本地版倉與遠端版倉

假設你在 GitHub 上建立了一個空版倉 `my-project`，可以將它與本地的 Git 版倉連結：

```bash
# 方法一：先建立版倉再連結
git remote add origin https://github.com/你的帳號/my-project.git

# 方法二：從 GitHub 複製（clone）版倉
git clone https://github.com/你的帳號/my-project.git
```

`origin` 是遠端版倉的預設名稱。你可以用 `git remote -v` 確認連結：

```bash
git remote -v
```

## 推送與拉取：push、pull、fetch

將本地的提交推送到 GitHub：

```bash
git push origin main
```

從 GitHub 拉取最新的變更到本地：

```bash
git pull origin main
```

`git pull` 其實等同於 `git fetch`（只下載變更）加上 `git merge`（合併到本地分支）。如果你想要先看看遠端有哪些變更再決定是否合併，可以分兩步執行：

```bash
git fetch origin
git log origin/main --oneline  # 先檢視遠端的變更
git merge origin/main          # 確認後再合併
```

## 分叉與 Pull Request 的工作流程

在 GitHub 的協作中，你不直接將變更推送到別人的版倉，而是透過 **Fork（分叉）** 和 **Pull Request（拉取請求）** 的機制。完整流程如下：

1. **Fork**：在 GitHub 上點擊版倉頁面的「Fork」按鈕，將別人的版倉複製一份到你的帳號下。
2. **Clone**：將你 Fork 後的版倉 clone 到本地端。
3. **建立分支**：在本地建立功能分支。
4. **開發並提交**：在功能分支上工作，完成後推送。
5. **建立 Pull Request**：在 GitHub 上將你的功能分支提交合併請求到原始版倉。
6. **Code Review**：團隊成員審查你的程式碼。
7. **合併**：審查通過後，維護者將你的變更合併到主線。

操作範例：

```bash
# Fork 版倉後，clone 到本地
git clone https://github.com/你的帳號/original-project.git
cd original-project

# 建立功能分支
git checkout -b feature/add-login

# 開發並提交
echo "login functionality" > login.py
git add .
git commit -m "新增登入功能"

# 推送到你 Fork 的遠端版倉
git push origin feature/add-login
```

然後到 GitHub 上的版倉頁面，你會看到一個「Compare & pull request」的提示，點擊後填寫標題和說明，提交 Pull Request。

## Code Review 的意義

**Code Review（程式碼審查）** 是 Pull Request 流程中最關鍵的環節。它不只是找 Bug，更是一個知識分享和品質保證的過程。在 Code Review 中，審查者會關注：

- **正確性**：程式碼是否正確實現了預期功能？
- **可讀性**：程式碼是否容易理解？命名是否恰當？
- **安全性**：是否有資安漏洞（如 SQL injection、硬編碼密碼）？
- **效能**：是否有不必要的效能浪費？
- **一致性**：是否符合團隊的程式碼風格規範？

在 GitHub 上，審查者可以直接在 Pull Request 的特定行數上留下評論。你可以使用 **Suggested Changes** 功能直接建議修改，提交者只需點擊「Commit suggestion」就能接受建議。

### Code Review 的禮儀

- **對事不對人**：批評程式碼，不要批評人。
- **說明原因**：不只指出問題，也要解釋為什麼這是問題。
- **肯定優點**：好的程式碼值得讚賞，不要只挑毛病。
- **及時回覆**：收到審查意見後儘快回覆，避免阻礙團隊進度。

## Issue：專案的任務管理

GitHub 的 **Issue** 功能是輕量級的任務追蹤系統。每一個 Issue 是一個討論串，可以用來：

- 報告 Bug
- 提出新功能需求
- 討論技術方案
- 記錄待辦事項

Issue 支援 **Label（標籤）** 來分類，例如 `bug`、`enhancement`、`documentation`。也可以指派（assign）給特定成員，並設定里程碑（milestone）來追蹤進度。

一個好的 Issue 應該包含：

- **清楚的標題**：簡潔描述問題或需求
- **重現步驟**（如果是 Bug 報告）
- **預期行為 vs 實際行為**
- **環境資訊**（作業系統、瀏覽器版本、程式語言版本等）

### 連結 Issue 與 Pull Request

在提交訊息或 Pull Request 描述中寫入 `Fixes #123`，當這個 Pull Request 被合併後，Issue #123 會自動關閉。這能讓你的開發歷史與任務追蹤保持同步。

```bash
git commit -m "修正登入表單驗證邏輯，Fixes #42"
```

## 一個完整的協作場景

假設你和兩位同學要合作開發一個課程專案，以下是建議的工作流程：

1. 由一位組員建立 GitHub 版倉並設為組織（Organization）或使用 GitHub Classroom。
2. 所有組員 Fork 版倉到自己的帳號。
3. 每位組員在本地 clone 自己 Fork 後的版倉。
4. 從 `main` 建立功能分支，完成後向原始版倉提交 Pull Request。
5. 至少一位組員進行 Code Review 後才合併。
6. 每天下班前執行 `git pull` 同步最新的變更。

## 想一想

1. 為什麼 GitHub 不直接讓你推送到別人的版倉，而要透過 Fork + Pull Request 的機制？這樣做有什麼好處？
2. 如果你在 Code Review 中發現同事的程式碼有嚴重的安全問題，但對方堅持不改，你該怎麼處理？
3. Issue 和 Pull Request 可以互相連結，這對大型專案的維護有什麼幫助？

## 本章小結

本章介紹了 GitHub 協作的核心流程：從連結遠端版倉、推送與拉取變更，到 Fork + Pull Request 的工作模式。我們也探討了 Code Review 的意義與實踐方式，以及 Issue 作為任務管理工具的用法。這些協作技能將是你在團隊專案中不可或缺的能力。下一章我們將學習如何用 GitHub Actions 實現自動化的 CI/CD 管線。
