# A.6 Git 進階：rebase、cherry-pick、bisect

## 前言

前面的章節已經涵蓋了 Git 日常使用所需的基本操作。本章要介紹三個更進階的指令：`rebase` 用來整理提交歷史，`cherry-pick` 用來精確提取特定提交，`bisect` 用來二分搜尋找出引入 Bug 的提交。這些工具在處理複雜的開發場景時非常有用。

## rebase：重新整理提交歷史

### merge 的問題

假設你在 `feature` 分支上工作，同時 `main` 分支也有了新的提交。你將 `feature` 合併回 `main` 時，會產生一個合併提交。如果這種情況反覆發生，提交歷史就會充滿大量的合併提交，變得難以閱讀：

```
* merge commit C
|\
| * feature commit 3
* | main commit B
|/
* merge commit A
|\
| * feature commit 2
* | main commit A
|/
* feature commit 1
```

### rebase 的做法

`git rebase` 的作用是**將你的變更重新應用在目標分支的最新提交之後**，產生一條線性的歷史：

```bash
# 在 feature 分支上
git checkout feature
git rebase main
```

執行後，Git 會：

1. 暫存 `feature` 分支上相對於 `main` 的所有提交。
2. 將 `feature` 分支的起點移到 `main` 的最新提交。
3. 逐個重新套用暫存的提交。

結果歷史變成一條直線：

```
* feature commit 3
* feature commit 2
* main commit B
* main commit A
* feature commit 1
```

### rebase 後合併

通常 rebase 後你會使用 **fast-forward merge** 來合併，因為兩個分支已經在同一条線上：

```bash
git checkout main
git merge feature  # 這會是 fast-forward
```

### rebase 的黃金法則

**永遠不要對已經推送到遠端（被其他人使用的）分支執行 rebase。**

因為 rebase 會改寫提交歷史（產生新的雜湊值），如果其他人已經基於舊的歷史進行開發，強行 rebase 會導致他們的歷史與你衝突，造成極大的混亂。

這個原則可以簡化為：**只 rebase 你自己的本地分支。**

### rebase 的衝突處理

rebase 遇到衝突時，和 merge 一樣需要手動解決，但方式略有不同：

```bash
git rebase main
# 遇到衝突時...
# 手動編輯衝突檔案
git add <已解決的檔案>
git rebase --continue    # 繼續下一個提交的 rebase
# 如果想放棄整個 rebase
git rebase --abort
```

## cherry-pick：精確提取特定提交

有時候你需要的不是整條分支的合併，而是某個**特定的提交**。`git cherry-pick` 就是用來做這件事：將某個指定的提交「摘」過來，應用在目前的分支上。

```bash
# 找出你想要的提交的雜湊值
git log --oneline
# 假設輸出：
# a1b2c3d 修正 SQL injection 漏洞
# e4f5g6h 新增搜尋功能

# 將特定提交摘過來
git cherry-pick a1b2c3d
```

### 常見使用場景

**場景一：hotfix 的精確移植**

你在 `main` 分支上發現並修了一個 Bug（提交 `a1b2c3d`），但 `develop` 分支也需要這個修正。你不想合併整個 `main`，只想拿那個修正：

```bash
git checkout develop
git cherry-pick a1b2c3d
```

**場景二：撤銷錯誤提交**

如果你發現某個提交有問題但不想用 `git revert`，可以先找到該提交的前一個提交，然後反向 cherry-pick：

```bash
# 找到要撤銷的提交
git log --oneline
# b7c8d9e 這個提交有問題

# 反向 cherry-pick（撤銷該提交的變更）
git cherry-pick -n b7c8d9e --no-commit
```

**場景三：從多個分支挑選提交**

你可以一次 cherry-pick 多個提交：

```bash
git cherry-pick a1b2c3d e4f5g6h
```

### cherry-pick 的注意事項

cherry-pick 會產生一個新的提交，即使程式碼內容相同，新提交的雜湊值也不同。這意味著同一個變更在不同分支上會有不同的提交歷史。在大多數情況下，直接合併分支比 cherry-pick 更好，但在需要精確控制時，cherry-pick 是不可或缺的工具。

## bisect：用二分搜尋找出 Bug

當你發現程式碼中有 Bug，但不知道是哪次提交引入的，手動逐一檢查是非常痛苦的。如果你有 100 個提交，線性搜尋需要檢查 100 次。`git bisect` 利用**二分搜尋**的原理，將複雜度降為 O(log n)。100 個提交大約只需要檢查 7 次。

### 基本用法

```bash
# 啟動 bisect 模式
git bisect start

# 標記目前的版本是有 Bug 的（bad）
git bisect bad

# 標記一個已知沒有 Bug 的過去版本（good）
git bisect good a1b2c3d   # 替換為你確定沒問題的提交雜湊值
```

Git 會自動 checkout 到中間的提交，讓你測試。測試後告訴 Git 結果：

```bash
# 如果這個版本有 Bug
git bisect bad

# 如果這個版本沒問題
git bisect good
```

Git 會根據你的回答繼續二分搜尋，直到找出第一個引入 Bug 的提交：

```
e4f5g6h is the first bad commit
Author: 某同學 <student@school.edu>
Date:   Mon Sep 1 10:30:00 2026

    重構資料庫查詢邏輯
```

找到後，結束 bisect 模式：

```bash
git bisect reset
```

### 自動化 bisect

如果你有自動化測試腳本，可以讓 Git 自動執行 bisect，完全不需要手動介入：

```bash
git bisect start
git bisect bad HEAD
git bisect good a1b2c3d
git bisect run pytest tests/test_login.py
```

`git bisect run` 會自動執行你指定的指令。如果指令的退出碼為 0，Git 標記為 `good`；非 0 則標記為 `bad`。幾分鐘後你就能精確知道是哪次提交出了問題。

### 完整範例

假設你在開發一個計算機程式，最近一次提交後發現加法運算出錯。你確定五個提交前的版本是正常的：

```bash
git bisect start
git bisect bad HEAD                    # 目前版本有問題
git bisect good HEAD~5                 # 五個提交前是正常的

# Git 切換到中間的提交，執行測試
python calc.py 2 + 3
# 結果正確
git bisect good

# Git 切換到下一個中間點
python calc.py 2 + 3
# 結果錯誤
git bisect bad

# 繼續...
# 最終輸出：
# abc1234 is the first bad commit
git bisect reset
```

## 三個指令的使用時機總整理

| 指令 | 核心功能 | 典型場景 |
|------|----------|----------|
| `rebase` | 重寫提交歷史，使其線性化 | 清理功能分支的提交歷史後合併 |
| `cherry-pick` | 將特定提交應用到另一個分支 | 只需要某次 hotfix，不需要整個分支 |
| `bisect` | 用二分搜尋定位引入 Bug 的提交 | 知道某個 Bug 是最近才出現的，但不知何時引入 |

## 想一想

1. 如果你在 `feature` 分支上 rebase 了 `main`，然後推送到 GitHub，你的隊友會遇到什麼問題？該如何補救？
2. 在什麼情況下你會選擇 `cherry-pick` 而不是 `merge`？反過來呢？
3. `git bisect` 依賴一個前提：你能快速判斷某個版本「有沒有 Bug」。如果一個 Bug 需要花 30 分鐘的測試才能確認，bisect 還有用嗎？

## 本章小結

本章介紹了三個 Git 進階指令：`rebase` 透過重新套用提交來整理歷史，讓分支歷史保持線性；`cherry-pick` 允許你精確地提取特定提交到其他分支；`bisect` 則利用二分搜尋的原理快速定位引入 Bug 的提交。掌握這些工具後，你將能更從容地應對複雜的開發場景。至此，附錄的 Git 相關章節全部完成，你已經具備了在真實專案中使用 Git 進行版本控制和團隊協作的基礎能力。
