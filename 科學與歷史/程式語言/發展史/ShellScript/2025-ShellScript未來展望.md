# 2025：Shell Script 未來展望

## 事件
2025 年的今天，shell script 生態呈現「一個標準、兩大霸主、多重新典範」的格局：POSIX 語法仍是腳本可移植性的公分母，bash 統治 Linux 伺服器，zsh 統治開發者桌面與 macOS，而 nushell 等結構化 shell 正定義下一個時代。

## 當前格局

| 陣營 | 代表 | 定位 |
|------|------|------|
| POSIX 標準 | dash、busybox ash | 最小可移植腳本（`/bin/sh`） |
| Bourne 血統霸主 | bash | Linux 伺服器、CI/CD、Dockerfile |
| 體驗霸主 | zsh + Oh My Zsh | macOS 預設、開發者桌面 |
| 體驗前衛 | fish | 自動建議、語法高亮 |
| 結構化新典範 | nushell、elvish、oil | 結構化管線、型別安全 |
| 跨 shell 工具 | starship、fzf、atuin | 提示符、搜尋、歷史——改體驗不改語言 |

## 演化的不變定律

回顧 1964 年至今，shell 的每次躍升都遵循同一模式：

1. **新環境出現**（分時系統→網路→Web→容器→AI）
2. **舊語法成為缺陷**（無變數→無交互→無結構→無型別安全）
3. **新語法彌補**（Bourne 變數→csh 工作控制→ksh/bash 融合→nushell 結構化）
4. **相容性與創新的張力**——勝者總是「相容為骨、創新為血」（ksh、bash、zsh），純創新者（scsh）或純相容者（dash）都只能守住一角。

## 未來方向

### 1. AI 時代的 shell
- **理論原因**：自然語言到命令的轉譯，正是 shell「命令直譯器」概念的延伸。
- **實用原因**：AI 輔助的 shell（自然語言產生腳本、自動修錯）把「重複」的交給機器的哲學推到極致。
- **彌補缺陷**：人類記不住語法細節的缺陷——AI 成為新的「補全」。

### 2. 結構化管線的普及
- **彌補缺陷**：文字管線五十年來的解析脆弱性。
- **觀察**：JSON 已是 Web 世界的通用語言（2001 年發明），shell 管線的結構化是遲到的必然。

### 3. 安全的最小化
- **彌補缺陷**：Shellshock（2014）暴露的攻擊面。
- **觀察**：容器與 distroless 影像正在移除 shell——「沒有 shell 的部署」成為最佳實務。

## 程式範例：三個時代的同一件事

「找出佔用最多記憶體的前三個行程」——見證五十年的演化：

```sh
# 1977 年（Bourne Shell）：文字管線 + awk 解析
ps aux | sort -rn -k4 | head -4 | awk '{print $11}'
```

```bash
# 2009 年（Bash 4.0）：陣列與進階展開，但本質仍是文字解析
mapfile -t procs < <(ps aux --sort=-%mem | tail -n +2 | head -3)
for p in "${procs[@]}"; do
  echo "${p##* }"
done
```

```nu
# 2025 年（Nushell）：結構化管線，資料就是表格
ps | sort-by mem | reverse | first 3 | get name
```

## 彌補了什麼缺陷
未來的 shell 將繼續彌補「人類記不住語法」「文字管線無結構」「字串即命令不安全」三大缺陷——這也是 1964 年 Multics 以來，shell 概念不變而實作不斷重生的證明。

## 相關條目
- [1964-Multics與Shell構想](1964-Multics與Shell構想.md)
- [1977-BourneShell-sh問世](1977-BourneShell-sh問世.md)
- [2023-現代Shell競爭時代](2023-現代Shell競爭時代.md)
