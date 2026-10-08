# 1978 - Version 7 與 2.8BSD（「第一個可移植 Unix」）

## 案件摘要
1979 年 1 月發布的 **Version 7 Unix**（研發於 1978–79）被 Ritchie 稱為「第一個真正的可移植 Unix」——
它包含 Bourne shell、完整的 C 編譯器、awk、sed、make，約 10,000 行核心，
是此後**所有 Unix 變種（System V、Xenix、BSD）的共同祖先**。
$$\text{V7} = \text{今日所有 Unix 的最近共同祖先 (MRCA)}.$$

## 前因 -- 為什麼會有這個案子
- **機器多元化的壓力**：1970 年代末 Unix 已跑在 PDP-11、Interdata 8/32、VAX 上——每次移植都要改系統。**彌補的缺陷：機器相關碼散落各處**。V7 把「機器相關」隔離到少數檔案，其餘全用 C。
- **Bourne shell 的需求**：Thompson shell 太簡陋，無法寫複雜腳本——**Steve Bourne** 用 Algol 風格語法寫出 `sh`：變數、控制流、函式、可寫成真正程式語言。
- **工具鏈的成熟**：awk (1977)、sed (1974)、make (1977)——Unix 的「小工具家族」在 V7 時代成型。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：可移植性的結構化
$$\text{Unix} = \text{機器無關層（99\%，C 語言）} + \text{機器相關層（1\%，組語）}.$$
- **彌補的缺陷**：V6 移植到 Interdata 8/32 花了兩年、改了數千行——V7 的結構把移植成本降到「重寫編譯器後端 + 少數驅動」。

### 第二條線索：Bourne shell——腳本即程式
```sh
# Bourne shell (1978)：第一次可以寫「真正的程式」
for f in *.txt; do
    if [ -s "$f" ]; then
        wc -l "$f"
    fi
done
```
- **彌補的缺陷**：Thompson shell 無迴圈、無條件判斷、無函式——只能當指令啟動器。Bourne shell 把 shell 變成**程式語言**，開啟 shell 腳本自動化的 50 年傳統。

### 第三條線索：awk——模式掃描語言
**Aho、Weinberger、Kernighan**（三人的姓氏縮寫）於 1977 年寫出 `awk`：
$$\text{awk} = \text{模式} \;\{\; \text{動作} \;\} \quad \text{——正規表示式 + 陣列 + 浮點運算的一行式資料處理}.$$
- **彌補的缺陷**：處理欄位式資料時，sed 太弱、C 太重——awk 填補「中間層」。

### Shell 範例：awk 的一行式威力

```bash
# 1978 年就能做到：統計 /etc/passwd 各 shell 的使用人數
$ awk -F: '{print $7}' /etc/passwd | sort | uniq -c
  10 /bin/sh
   5 /bin/csh
```

### C 範例：V7 的可移植層結構

```c
/* V7 風格：機器相關碼被隔離在少數檔案 */
#ifdef PDP11
    /* PDP-11 專用：setjmp 的堆疊細節 */
#endif
#ifdef VAX
    /* VAX 專用：虛擬記憶體管理 */
#endif
/* 其餘 99% 的程式碼完全相同 */
```

## 結案 -- 後果與影響
- **V7 = 共同祖先**：System V（AT&T 商業線）、Xenix（Microsoft）、BSD（Berkeley 線）全部源於 V7——**今天 Linux 的系統呼叫介面仍保留 V7 的影子**。
- **Bourne shell** → POSIX sh → bash（1989）——今日所有 Linux 發行版的預設腳本語言。
- **awk** → Perl（1987）、今天的文字處理工具鏈。
- **V7 原始碼**（Caldera 2002 年開源）至今仍是教學經典。
- 歷史教訓：**可移植性不是口號，而是「把機器相關碼隔離到 1%」的工程紀律**。

## 關鍵人物與文獻
- **S. R. Bourne**：〈The UNIX Shell〉(1978)。
- **A. Aho, P. Weinberger, B. Kernighan**：awk (1977)。
- **S. Feldman**：make (1977)。
- 相關案件：`1973-Unix以C重寫與管道.md`、`1975-Version6與BSD起源.md`。
