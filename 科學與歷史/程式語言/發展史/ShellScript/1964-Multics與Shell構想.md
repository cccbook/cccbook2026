# 1964：Multics 與 Shell 構想

## 事件
1964 年，麻省理工學院（MIT）、貝爾實驗室與奇異公司（GE）啟動 **Multics**（Multiplexed Information and Computing Service）計畫，目標是建造一台「像水電一樣」的共用計算機系統。計畫中，**Louis Pouzin** 等人設計了稱為 **shell** 的命令直譯器——這是「shell」一詞的起源。

## 概念的理論與實用原因

### 1. 核心與外殼分離
- **理論原因**：分層設計（layered design）——作業系統的核心（kernel）負責資源管理，外殼（shell）負責人機介面，兩者可以各自獨立演化。
- **實用原因**：使用者不需要重編譯整個作業系統就能改變命令介面。
- **彌補缺陷**：當時的批次作業系統（如 IBM OS/360 的 JCL）把「使用者介面」硬編碼在系統裡，改介面等於改系統。

### 2. RUNCOM：腳本的前身
- **實用原因**：Pouzin 設計的 RUNCOM 允許把一連串命令存成檔案後重複執行——這就是「script」（腳本）一詞的由來。
- **彌補缺陷**：人工重複輸入相同命令序列，既慢又容易出錯。

## 程式範例：RUNCOM 概念——腳本的雛形

```
# RUNCOM 的概念（偽代碼）：把命令序列存成檔案重複執行
# cleanup.com 檔案內容：
delete *.tmp
sort data.txt
print report.txt

# 執行：一行命令跑完三件事
runcom cleanup
```

```sh
# 這個概念在 UNIX 的實現（1971 年起）：
sh cleanup.sh    # 「script」＝命令的劇本
```

## 彌補了什麼缺陷
彌補了「命令介面不可替換、命令序列不可儲存重用」的缺陷，確立了「shell 是作業系統之外殼，腳本是命令的劇本」兩大概念。

## 相關條目
- [1969-UNIX問世](../C++/1969-UNIX問世.md)
- [1971-ThompsonShell問世](1971-ThompsonShell問世.md)
