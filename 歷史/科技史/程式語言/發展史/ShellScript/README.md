# ShellScript 程式語言發展史年表

> Shell Script 是 UNIX 世界最古老的「膠水語言」：它沒有獨立的編譯器，
> 而是以解譯器（shell）的形式存在，負責把使用者的指令翻譯給作業系統。
> 從 1971 年 Thompson Shell 的雛形，到 1977 年 Bourne Shell（sh）奠定現代語法，
> 再到 bash、zsh、fish 等後裔，Shell Script 見證了 UNIX、POSIX、Linux 與開源運動的整部歷史。

## 前史：理論根源

| 年份 | 事件 | 意義 |
|------|------|------|
| 1964 | Multics 計畫啟動 | 「shell」一詞的起源：作業系統的外殼應與核心分離 |
| 1965 | Louis Pouzin 提出 shell 設計 | 首次把「命令直譯器」稱為 shell，設計了 RUNCOM |
| 1969 | UNIX 問世 | Thompson 與 Ritchie 在貝爾實驗室創造 UNIX |
| 1971 | Thompson Shell | UNIX 第一個 shell，以外部程式 `sh` 執行腳本 |
| 1973 | 管線（pipe）問世 | McIlroy 提出「小事處理」哲學，`|` 成為組合程式的基礎 |
| 1975 | Mashey Shell | 加入 `if`、`goto` 等控制流程，暴露高階語法需求的不足 |
| 1976 | C 語言成熟 | Bourne 以「不使用 C 語法」的方式重寫 shell 的時代背景 |

## 正式年表

| 年份 | 標題 | 關鍵語法/特性 |
|------|------|---------------|
| 1971 | [Thompson Shell：第一個 UNIX Shell](1971-ThompsonShell問世.md) | 外部 `sh` 直譯器、`<` `>` 重導向、簡單參數取代 |
| 1973 | [管線誕生](1973-管線pipe問世.md) | `\|` 管線運算子、「小事處理」組合哲學 |
| 1977 | [Bourne Shell（sh）問世](1977-BourneShell-sh問世.md) | 變數、`if/then/elif/else`、`for`、`while`、`case`、函數、**here-doc（`<<`，1977 發明）**、`$()` 環境 |
| 1978 | [C Shell（csh）問世](1978-CShell-csh問世.md) | 交互式歷史命令、別名（alias）、工作控制（job control）、C 風格語法 |
| 1983 | [Korn Shell（ksh）問世](1983-KornShell-ksh問世.md) | 相容 sh 又吸收 csh 交互功能、陣列、算術展開 `$(( ))`、命令列編輯 |
| 1987 | [TCSH 問世](1987-TCSH問世.md) | csh 的現代化：可編程補全、命令列編輯、拼字修正 |
| 1988 | [Bash 誕生（GNU 專案）](1988-Bash誕生.md) | 自由軟體基金會的 POSIX 相容 shell，Bourne Again Shell |
| 1989 | [Bash 1.x 與交互式強化](1989-Bash交互式強化.md) | 歷史命令、別名、`!!` 事件指定符、命令列編輯（readline） |
| 1990 | [Zsh 誕生](1990-Zsh誕生.md) | 集大成者：可編程補全、主題化提示符、極致可客製化 |
| 1991 | [Linux 問世與 GNU 工具鏈](1991-Linux問世.md) | bash 成為 Linux 世界的預設 shell，開源生態確立 |
| 1992 | [POSIX.2 Shell 標準化](1992-POSIXShell標準化.md) | IEEE 1003.2：以 Bourne Shell 為基礎的統一 shell 語言規範 |
| 1995 | [Fish 的前夜與腳本語言分化](1995-PerlPython衝擊.md) | Perl/Python 崛起，shell 退守「系統管理」本業 |
| 2000 | [Bash 2.0：重寫與陣列](2000-Bash2-0重寫.md) | `array` 變數、`$( )` 嵌套改進、國際化、新的解析器架構 |
| 2005 | [Fish 問世](2005-Fish問世.md) | 「友善的互動式 shell」：自動建議、語法高亮、不以 POSIX 為念 |
| 2009 | [Bash 4.0：關聯陣列與萬用字元強化](2009-Bash4-0關聯陣列.md) | `declare -A` 關聯陣列、`**` 遞迴萬用字元、`&>>`、coproc |
| 2010 | [Oh My Zsh 問世](2010-OhMyZsh問世.md) | zsh 設定框架，社群化外掛生態，zsh 大眾化 |
| 2014 | [Shellshock 漏洞事件](2014-Shellshock漏洞事件.md) | bash 25 年歷史漏洞曝光，shell 安全性的全球警鐘 |
| 2019 | [macOS 改用 Zsh](2019-macOS改用Zsh.md) | macOS Catalina 以 zsh 取代 bash（GPLv3 授權因素） |
| 2023 | [現代 Shell 競爭時代](2023-現代Shell競爭時代.md) | nushell、elvish、oil shell：結構化資料管線的新典範 |
| 2025 | [未來展望](2025-ShellScript未來展望.md) | Shell Script 在 AI 時代的角色：從膠水語言到自動化的共通介面 |

## 發展主軸

1. **1964–1977：從命令直譯器到程式語言** —— Thompson Shell 只會重導向，Bourne Shell 加入變數與控制流程，shell 正式成為「語言」。
2. **1978–1989：交互性革命** —— csh 開創歷史命令與工作控制，ksh/bash 融合交互性與腳本性。
3. **1990–2000：標準化與開源** —— POSIX 統一語法，Linux 讓 bash 成為世界預設。
4. **2005–至今：體驗與結構化** —— fish、oh-my-zsh 改造使用者體驗，nushell 等新典範挑戰純文字管線。

## 相關書目

- [C++ 程式語言發展史](../C++/README.md) —— UNIX 與 C 是 shell 的母體
- [JavaScript 程式語言發展史](../JavaScript/README.md)
- [Rust 程式語言發展史](../Rust/README.md)
