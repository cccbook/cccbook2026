# A.2 Git 基礎操作：init、add、commit、branch、merge

## 建立版本倉：git init

要開始使用 Git，第一步是在專案目錄中建立一個版本倉。使用 `git init` 指令即可：

```bash
mkdir my-project
cd my-project
git init
```

執行後，Git 會在當前目錄下建立一個隱藏的 `.git` 資料夾，裡面包含了版本倉的所有中繼資料和物件資料庫。從此刻起，這個目錄就受到 Git 的管理。

你可以用以下指令確認版本倉的狀態：

```bash
git status
```

輸出中會顯示 `No commits yet`，代表這是一個全新的空版倉。

## 追蹤檔案：git add

假設你在版本倉中建立了一個檔案 `hello.txt`：

```bash
echo "Hello, Git!" > hello.txt
git status
```

此時 Git 會告訴你有一個 `Untracked file`。要讓 Git 開始追蹤這個檔案，需要將它加入暫存區：

```bash
git add hello.txt
```

如果要一次加入所有變更的檔案，可以使用：

```bash
git add .
```

`.` 代表當前目錄下所有的新增和修改。這是日常開發中最常用的用法。

## 提交變更：git commit

暫存區中的檔案已經準備好被記錄。使用 `git commit` 將暫存區的內容正式提交到版本倉：

```bash
git commit -m "第一次提交：新增 hello.txt"
```

`-m` 後面的字串是**提交訊息（commit message）**，用來說明這次提交做了什麼。好的提交訊息應該簡潔但有意義。避免使用「update」或「fix」這種模糊的描述，而是說明「做了什麼」以及「為什麼」。

每次提交都會產生一個唯一的**雜湊值**（如 `a1b2c3d`），代表那個版本的快照。這就是為什麼 Git 也叫做「快照式」版本控制系統。

## 查看歷史：git log

想看所有的提交紀錄，可以使用：

```bash
git log
```

這會顯示從最新到最舊的每次提交，包含作者、日期和提交訊息。更常用的簡潔格式：

```bash
git log --oneline
```

輸出範例：

```
a1b2c3d (HEAD -> main) 第一次提交：新增 hello.txt
```

## 建立與切換分支：git branch

**分支（branch）** 是 Git 最強大的功能之一。它讓你可以在不影響主線的情況下進行開發實驗。建立一個新分支：

```bash
git branch feature
```

這會建立一個名為 `feature` 的分支，但它不會自動切換過去。要切換到新分支：

```bash
git checkout feature
```

或者使用更新的語法（Git 2.23+）：

```bash
git switch feature
```

也可以用一行指令完成建立並切換：

```bash
git checkout -b feature
# 或
git switch -c feature
```

使用 `git branch` 不加任何參數可以查看所有分支，目前所在的分支前面會有 `*` 號：

```bash
git branch
```

```
* feature
  main
```

## 合併分支：git merge

假設你在 `feature` 分支上完成了一些工作並提交了：

```bash
echo "New feature code" > feature.txt
git add feature.txt
git commit -m "新增 feature.txt"
```

現在要把 `feature` 分支的成果合併回 `main`：

```bash
git checkout main
git merge feature
```

這會將 `feature` 分支的變更整合到 `main` 分支。Git 會自動產生一個合併提交（merge commit）。

合併完成後，如果 `feature` 分支不再需要，可以將其刪除：

```bash
git branch -d feature
```

## 常見的合併衝突

當兩個分支同時修改了同一個檔案的同一行，Git 無法自動判斷該保留哪個版本，就會產生**合併衝突（merge conflict）**。Git 會在衝突的檔案中標記出衝突區域：

```
<<<<<<< HEAD
Hello, Git!
=======
Hello, Git! Updated.
>>>>>>> feature
```

你需要手動編輯檔案，決定保留哪個版本（或兩者都保留），然後刪除衝突標記，再重新提交：

```bash
# 手動編輯檔案後
git add .
git commit -m "解決合併衝突"
```

衝突是 Git 使用過程中必然會遇到的情況，不用害怕，理解它背後的邏輯後其實很直覺。

## 完整流程範例

以下是一個從零開始的完整操作流程：

```bash
# 建立專案並初始化 Git
mkdir demo && cd demo
git init

# 建立第一個檔案並提交
echo "# Demo Project" > README.md
git add .
git commit -m "初始化專案：建立 README.md"

# 建立功能分支
git switch -c add-hello

# 在功能分支上工作
echo "print('Hello!')" > main.py
git add .
git commit -m "新增 main.py"

# 切回主線並合併
git switch main
git merge add-hello

# 清理分支
git branch -d add-hello
```

## 想一想

1. `git add .` 和 `git add -A` 有什麼差異？在什麼情況下你會選擇其中一個？
2. 如果你在 `feature` 分支上改了檔案但忘了提交，切換回 `main` 分支時會發生什麼事？
3. 合併衝突發生時，為什麼 Git 不能自己選擇保留哪一個版本？

## 本章小結

本章帶你走過了 Git 最基礎的操作流程：從 `git init` 建立版本倉，`git add` 加入暫存區，`git commit` 提交變更，到 `git branch` 建立分支以及 `git merge` 合併分支。這些是指令是日常 Git 使用的核心，熟練這些操作後，你已經有能力用 Git 管理個人專案的版本。下一章我們將探討更進階的分支策略。
