# 1956 - FORTRAN

## 案件摘要
1956 年，IBM 發表 FORTRAN（FORmula TRANslation）語言規格，1957 年 4 月第一個 FORTRAN 編譯器問世。它是史上第一個被廣泛使用的進階語言，也是第一個「優化編譯器」的傑作——John Backus 的團隊承諾：編出來的程式碼效能要接近手寫組合語言。

## 前因 -- 為什麼會有這個案子
- 1950 年代的程式幾乎全用組合語言（或機器碼）撰寫，IBM 704 每行組合語言都要人工管理暫存器、位址、浮點運算呼叫。
- 科學計算（彈道、流體力學、核物理）佔電腦使用的大宗，但程式開發成本極高：一個程式寫幾週，debug 又是幾週。
- John Backus 在 IBM 701 上寫過 Speedcoding 直譯器，深知直譯太慢；他向 IBM 提議做「能產生高效率機器碼」的編譯器。

開發成本的痛點：

$$T_{\text{開發}}^{\text{asm}} \gg T_{\text{開發}}^{\text{高階}}\ \text{（期望值），但}\ T_{\text{執行}}^{\text{直譯}} \gg T_{\text{執行}}^{\text{asm}}$$

破案關鍵：用「編譯 + 優化」同時壓低兩者——這在 1957 年是賭上職涯的豪賭。

## 線索與推理 -- 數學式、程式、理論

### 定義：編譯器與優化
> 編譯器是一個函數 $\text{compile}: \text{Source} \to \text{Target}$，將進階語言程式轉換為機器碼。優化編譯器進一步要求

$$\forall P:\quad T_{\text{執行}}(\text{compile}(P)) \lesssim k \cdot T_{\text{執行}}^{\text{asm}}(P), \quad k \approx 1$$

Backus 團隊的目標是讓 $k$ 接近 1（宣稱平均效率達手寫碼的一半以上，實測常常更好）。

### FORTRAN I 的核心語言特徵
- **算術式**：直接寫 `X = (A+B)*C`，編譯器自動配置暫存器與浮點指令（IBM 704 內建浮點硬體是關鍵助力）。
- **DO 迴圈**：最早的結構化迴圈，語義為（FORTRAN I 中 iteration 數至少一次，do-while 語義）

$$\text{for } i = m \text{ to } n \text{ step } s:\quad \text{body}(i)$$

- **IF 算術判斷**：`IF (X) 10, 20, 20` 依 $x < 0$、$x = 0$、$x > 0$ 三路跳轉。
- **格式化 I/O**：FORMAT 敘述，是科學報表的核心。

### 第一個優化編譯器
- 編譯器分 6 個 phase，共約 25,000 行組合語言，由 Backus 帶領約 10 人團隊（Irving Ziller、Sheldon Best、Harlan Herrick、Lois Haibt、David Sayre 等）耗時約 2.5 年完成。
- 關鍵優化：暫存器分配（graph coloring 的先聲）、公用子運算式消除、迴圈內程式碼移動。
- 1957 年 4 月發行後，因初期 bug 多被譏為 "FORMULA TRANSLATION" 失敗；修穩後大獲成功——程式開發時間從數週縮短到數小時。

### FORTRAN 範例：矩陣乘法
```fortran
      PROGRAM MATMUL
      REAL A(3,3), B(3,3), C(3,3)
      DATA A /1,2,3, 4,5,6, 7,8,9/
      DATA B /9,8,7, 6,5,4, 3,2,1/
C     C = A x B，三重 DO 迴圈
      DO 10 I = 1, 3
        DO 10 J = 1, 3
          C(I,J) = 0.0
          DO 10 K = 1, 3
   10       C(I,J) = C(I,J) + A(I,K)*B(K,J)
      PRINT 20, ((C(I,J), J=1,3), I=1,3)
   20 FORMAT(3F10.1)
      STOP
      END
```

數學定義：

$$C_{ij} = \sum_{k=1}^{n} A_{ik} B_{kj}, \qquad \Theta(n^3) \text{ 次乘加}$$

### Python 對照
```python
A = [[1,2,3],[4,5,6],[7,8,9]]
B = [[9,8,7],[6,5,4],[3,2,1]]
C = [[sum(A[i][k]*B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
for row in C:
    print(row)
# [30, 24, 18] / [84, 69, 54] / [138, 114, 90]
```

## 結案 -- 後果與影響
- FORTRAN 證明高階語言 + 優化編譯可以取代組合語言，直接催生了 ALGOL（1958）、COBOL（1959）、LISP（1958）等語言浪潮——程式語言的「寒武紀大爆發」。
- 編譯器理論成為獨立學科：語法分析、優化、暫存器分配的研究由此展開（Backus 的 BNF 是 ALGOL 60 的貢獻，但動機源自 FORTRAN 經驗）。
- **至今仍是超級電腦的主力語言**：HPC 領域（氣候模擬、計算流體力學、線性代數庫 BLAS/LAPACK）大量使用現代 FORTRAN（Fortran 90/2008/2018）。
- FORTRAN 標準化（1966 F66、1977 F77、1990 F90）是程式語言標準化的先驅，影響 ISO/IEEE 標準文化。

## 關鍵人物與文獻
- **John Backus**（1924–2007）：FORTRAN 計畫主持人，1977 年圖靈獎得主（也因 BNF 得獎）。
- **團隊成員**：Ziller、Best、Herrick、Haibt、Sayre、Nelson、Snyder、Hughes、Stern 等。
- 文獻：Backus, J. et al., "The FORTRAN Automatic Coding System", *Proceedings of the Western Joint Computer Conference*, 1957；Backus, "Can Programming Be Liberated from the von Neumann Style?", *CACM*, 1978（圖靈獎演講）。
