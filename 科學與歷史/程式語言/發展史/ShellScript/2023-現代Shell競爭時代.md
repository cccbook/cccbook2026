# 2023：現代 Shell 競爭時代

## 事件
2020 年代，新一代 shell 陸續問世：**Nushell**（2019 起）、**Elvish**（2016 起）、**Oil Shell**（2017 起）、以及 Rust 寫的快速 shell（如 **Nushell** 與 **Starship** 提示符）。它們的共同主張是：**管線應傳遞結構化資料，而非純文字**——挑戰 1973 年以來五十年不變的文字管線典範。

## 新典範的理論與實用原因

### 1. 結構化管線（structured data pipeline）
- **理論原因**：1973 年的文字管線沒有結構（欄位、型別），解析文字是五十年來的痛點；關聯式資料模型（Codd, 1970）證明結構化查詢的威力。
- **實用原因**：管線中的每個階段操作的是「表格/記錄」而非字串，不需要 awk/grep/cut 拼接。
- **彌補缺陷**：`ps aux | grep nginx | awk '{print $2}'` 這類「以文字解析模擬查詢」的脆弱鏈條。

### 2. 型別安全的腳本
- **理論原因**：Shellshock（2014）與引號陷阱證明「字串即命令」的資料/程式碼不分離是危險的。
- **實用原因**：結構化 shell 中資料就是資料，不會被意外當作命令執行。
- **彌補缺陷**：shell 的「字串即命令」傳統。

### 3. 以系統語言重寫（Rust/Go）
- **理論原因**：C 語言的記憶體安全問題（也催生了 Shellshock 類漏洞的土壤）。
- **實用原因**：Rust/Go 實作的 shell 啟動更快、更安全。
- **彌補缺陷**：傳統 shell（C 實作）的記憶體安全負擔。

## 程式範例：文字管線 vs 結構化管線

```bash
# 傳統 bash：純文字管線，解析靠 awk/grep 拼接
ps aux | grep nginx | grep -v grep | awk '{print $2}'
```

```nu
# Nushell（2023 年代的結構化典範）：管線傳遞表格
ps | where name =~ nginx | get pid

# 讀取 JSON/CSV 是一等公民
open data.csv | where age > 30 | sort-by name | first 5

# 錯誤即資料，型別即語言
ls | where size > 1mb | get name
```

```elvish
# Elvish：資料結構一等公民、管線可傳遞 list/map
use str
puts [ (os:ls | each [f]{ +$f'.bak' }) ]
```

```bash
# Oil Shell：修補而非取代——相容 bash 但消除引號陷阱
var f = "my file.txt"
ls $f        # 不需引號，變數就是值
```

```bash
# Starship（Rust 寫的提示符，跨 shell）：
# 只改體驗不改語言的代表
eval "$(starship init bash)"
```

## 歷史意義
2023 年代的 shell 競爭證明：shell 的演化主軸已從「語法相容性」（1977–2000）與「互動體驗」（2005–2015）轉移到「**結構化資料與型別安全**」。傳統 POSIX/bash 腳本仍是伺服器世界的霸主，但新典範正在定義下一個五十年。

## 彌補了什麼缺陷
彌補了五十年來文字管線「無結構、無型別、解析脆弱」的根本缺陷，以及「字串即命令」的安全缺陷。

## 相關條目
- [1973-管線pipe問世](1973-管線pipe問世.md)
- [2014-Shellshock漏洞事件](2014-Shellshock漏洞事件.md)
- [2025-ShellScript未來展望](2025-ShellScript未來展望.md)
