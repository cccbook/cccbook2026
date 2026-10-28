# 2010：Oh My Zsh 問世

## 事件
2010 年，**Robby Russell** 發佈 **Oh My Zsh**——一個以 zsh 為基礎的社群設定框架，包含數百個外掛與主題。它讓 zsh 從「行家之選」變成「開發者大眾的預設選擇」。

## 理論與實用原因

### 1. 設定即外掛（plugin ecosystem）
- **理論原因**：軟體生態（ecosystem）理論——平台只提供機制，社群提供內容。zsh 的可編程補全（1990）正是「機制」，Oh My Zsh 把它變成「內容」。
- **實用原因**：`git` 補全、`kubectl` 補全、主題化提示符，一行 `plugins=(git kubectl)` 啟用。
- **彌補缺陷**：zsh 功能強大但設定檔（`.zshrc`）繁瑣，每個工具的補全都要手動配置——Oh My Zsh 把這些封裝成開箱即用的外掛。

### 2. 主題化提示符（robbyrussell、powerline 系）
- **實用原因**：提示符顯示 git 分支、狀態、環境（virtualenv、nvm）——開發者工作流的即時儀表板。
- **彌補缺陷**：預設提示符只有路徑與 `$`，資訊量貧乏。

### 3. 社群治理的網路效應
- **實用原因**：GitHub 開源模式——貢獻者越多、外掛越多、使用者越多（網路效應正循環）。
- **彌補缺陷**：個人 `.zshrc` 是孤島，社群框架讓設定可共享。

## 程式範例：Oh My Zsh 的設定

```zsh
# ~/.zshrc：一行啟用外掛生態
ZSH_THEME="robbyrussell"              # 主題化提示符
plugins=(git kubectl docker)          # 一行啟用數百個社群補全
source $ZSH/oh-my-zsh.sh
```

```zsh
# 啟用後的效果：
git che<Tab>       # 補出 checkout、cherry-pick 等子命令
kubectl get p<Tab> # 補出 pods、pv 等
d ps<Tab>          # docker ps 補全
```

```zsh
# 主題化提示符：git 分支、狀態即時顯示
# robbyrussell 主題：➜ myproject git:(main) ✗
# powerline 系主題：顯示 virtualenv、nvm、時間等儀表板
```

```zsh
# 對比：沒有 Oh My Zsh 時，git 補全要手動配置
# 以前：自己 clone git-completion.bash、寫進 .zshrc、維護路徑……
# 現在：plugins=(git) 一行
```

## 歷史意義
Oh My Zsh 是「社群化 shell 設定」的濫觴，之後出現 zprezto、antigen、zplug、以及 2020 年代的 starship（跨 shell 提示符）與 zinit。其模式也證明了：**shell 的競爭已從「語言能力」轉移到「生態與體驗」**。zsh 語言本身（1990 年誕生）在 2010 年代因 Oh My Zsh 而登上 macOS（2019）預設 shell。

## 彌補了什麼缺陷
彌補了 zsh「功能強大但設定門檻高、設定不可共享」的生態缺陷，把 shell 的價值從語言能力轉移到社群生態。

## 相關條目
- [1990-Zsh誕生](1990-Zsh誕生.md)
- [2005-Fish問世](2005-Fish問世.md)
- [2019-macOS改用Zsh](2019-macOS改用Zsh.md)
