# 1971：Thompson Shell——第一個 UNIX Shell

## 事件
1971 年，UNIX 第一版（First Edition）隨附 **Thompson Shell**，由 **Ken Thompson** 撰寫，以外部程式 `sh` 執行。它是 UNIX 第一個命令直譯器，也是 shell script 語言的起點。

## 語法與特性及其理論、實用原因

### 1. 外部 `sh` 直譯器
- **理論原因**：繼承 Multics 的「外殼與核心分離」——shell 只是一支普通程式，不進核心。
- **實用原因**：使用者可以替換自己的 shell，`sh` 只是選項之一。

### 2. `<` `>` 重導向
- **理論原因**：「一切皆檔案」的直接體現——輸入輸出都是檔案，重導向只是換檔案。
- **實用原因**：`prog > file` 一個符號就把結果存檔，不需要專屬參數。
- **彌補缺陷**：每支程式都要自己實作「存檔」選項的重複浪費。

### 3. 簡單參數取代
- **實用原因**：命令列參數可以簡單地傳給腳本，腳本可以有一定彈性。
- **缺陷伏筆**：Thompson Shell **沒有變數**、沒有控制流程（if/for/while）、沒有函數——它只能「依序執行命令」。

### 4. `read` 指令的腳本用法（1973 強化）
- **實用原因**：腳本內可讀取輸入再重導向，勉強做出簡單分支的替代。

## 當時的語法範圍
`<`、`>`、`>>`、簡單參數取代、`sh file` 執行腳本。**沒有**變數、條件、迴圈、函數。

## 程式範例：Thompson Shell 的語法範圍

```sh
# 重導向：輸入輸出都是檔案
prog > result.txt        # 輸出存檔
prog < input.txt         # 從檔案讀輸入
prog >> log.txt          # 附加到檔案
```

```sh
# 腳本：命令序列存檔後用 sh 執行
# backup.sh 內容：
cc prog.c
cp a.out /backup/a.out
# 執行：
sh backup.sh
```

```sh
# 缺陷示範：Thompson Shell 沒有變數與條件
# 想做「檔案存在才備份」——做不到！只能靠外部程式或人工判斷
# 同樣的路徑必須重複寫死：
cp /usr/src/prog.c /backup/prog.c    # 路徑寫死兩次
```

## 彌補了什麼缺陷
彌補了「命令序列不可儲存重用」的缺陷（RUNCOM 概念在 UNIX 的實現），但它自身暴露了更大的缺陷：無法做邏輯判斷與迴圈，催生了 Mashey Shell 與後來的 Bourne Shell。

## 相關條目
- [1969-UNIX問世](1969-UNIX問世.md)
- [1973-管線pipe問世](1973-管線pipe問世.md)
- [1977-BourneShell-sh問世](1977-BourneShell-sh問世.md)
