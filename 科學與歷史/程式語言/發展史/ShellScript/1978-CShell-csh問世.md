# 1978：C Shell（csh）問世

## 事件
1978 年，加州大學柏克萊分校的 **Bill Joy**（2.8BSD 開發者、後來 vi 與 Sun Microsystems 的創辦人）發表 **C Shell**（`csh`），隨 2.8BSD / 3BSD 問世。csh 是第一個以「互動使用者體驗」為設計核心的 shell。

## 新語法與特性及其理論、實用原因

### 1. 歷史命令（history、`!!`、`!$`）
- **理論原因**：重複輸入是最常見的使用者行為，歷史機制把「重複」交給機器。
- **實用原因**：`!!` 重跑上一條命令、`!$` 取上一條的最後參數，打字量大幅下降。
- **彌補缺陷**：Bourne Shell 是純腳本導向，互動時每次都要重打整行命令。

### 2. 別名（`alias`）
- **理論原因**：巨集展開（macro expansion）在命令列的應用。
- **實用原因**：`alias ll='ls -l'` 一行定義個人化命令。
- **彌補缺陷**：個人化命令必須寫成腳本放到 PATH 裡。

### 3. 工作控制（job control：`&`、`jobs`、`fg`、`bg`、`Ctrl-Z`）
- **理論原因**：BSD 核心加入了信號與行程群組的支援，shell 提供對應介面。
- **實用原因**：在終端機上暫停、背景執行、切換行程—— multitasking 首次觸手可及。
- **彌補缺陷**：Bourne Shell 只能 `cmd &` 背景執行，無法中途暫停或切回前景。

### 4. C 風格語法（`if (expr) then ... endif`、`foreach`、`@` 算術）
- **理論原因**：Bill Joy 的目標使用者是「已經會 C 的程式設計師」，語法長得像 C 可零成本上手。
- **實用原因**：`@ count = count + 1` 提供內建算術（Bourne Shell 當時只能靠外部 `expr` 指令，fork 開銷大）。
- **彌補缺陷**：Bourne 語法刻意不像 C（`fi`、`esac`），C 程式設計師嫌它古怪。

### 5. 運算式與 `$?`、`$#argv` 等特殊變數
- **實用原因**：腳本可讀取參數個數、上個命令的狀態。

## 致命的腳本缺陷
csh 的交互功能大獲成功，但它的**腳本能力有著名惡名昭彰的缺陷**：
- 無法定義函數
- 檔案重導向無法分開 stdout/stderr（`2>` 不存在）
- 運算式解析有大量陷阱（Tom Christiansen 的名文 *"csh Programming Considered Harmful"*）
- 錯誤處理能力薄弱

這導致「**交互用 csh、腳本用 sh**」的分裂文化，也直接啟發了 ksh（融合兩者）與後來 zsh（集大成）。

## 程式範例：C Shell 的語法

```csh
# 1. 歷史命令：重複交給機器
!!          # 重跑上一條命令
!$          # 取上一條命令的最後參數
!gcc        # 重跑最近一條以 gcc 開頭的命令
history     # 查看歷史
```

```csh
# 2. 別名：個人化命令
alias ll 'ls -l'
alias backup 'cp \!* /backup'    # !* = 所有參數
```

```csh
# 3. 工作控制：multitasking 首次觸手可及
make &        # 背景執行
jobs          # 查看工作
Ctrl-Z        # 暫停前景工作
bg            # 送入背景
fg %1         # 切回前景
```

```csh
# 4. C 風格語法與內建算術
@ count = 0
foreach f (*.c)
  @ count = count + 1     # 內建算術，不用 fork expr
end
echo "共 $count 個檔案"

if ($?PATH) then           # $? 變數存在測試
  echo "PATH 已設定"
endif
```

```csh
# 致命腳本缺陷示範：csh 無函數、重導向陷阱
# 想把 stdout 和 stderr 分開——做不到！csh 沒有 2>
cc prog.c >& log    # stdout+stderr 只能合併，無法分流
# 運算式陷阱：
if (1 == 2) echo "never"      # 運算式解析有許多隱藏規則
```

## 彌補了什麼缺陷
彌補了 Bourne Shell「互動體驗貧乏」的缺陷（歷史、別名、工作控制），但自身腳本能力不足，反而強化了 shell 世界「交互與腳本分裂」的結構。

## 相關條目
- [1977-BourneShell-sh問世](1977-BourneShell-sh問世.md)
- [1983-KornShell-ksh問世](1983-KornShell-ksh問世.md)
- [1987-TCSH問世](1987-TCSH問世.md)
