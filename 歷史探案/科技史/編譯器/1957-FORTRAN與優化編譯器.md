# 1957-FORTRAN與優化編譯器

## 案件摘要
1957 年 4 月，John Backus 領軍的 IBM 20 人小組交出了 FORTRAN 編譯器——當時最複雜的程式之一。Backus 下了一個賭注：「自動編碼的效率必須接近手工組碼，否則沒人用。」他們用暫存器分配、公共子表達式消除、迴圈不變碼外提等技術贏了這場賭局，徹底證明高階語言可行——程式設計從此脫離組合語言的奴役。

## 前因 -- 為什麼會有這個案子
- **IBM 704 上組語的成本**：1950 年代，在 IBM 704 上寫一個科學計算程式，需要熟練程式師數週到數月，且錯誤率極高——組合語言的每個指令都要人腦做暫存器調度與位址計算。
- **機器時間貴、人力貴**：704 每小時租金數百美元，但程式師的時間更貴。Backus 的算盤：若高階語言只損失 10-20% 的執行效率，卻省下 80% 的開發時間，這是划算的買賣。
- **之前的自動編碼都失敗**：Speedcoding、Autocode 等系統執行效率太差（常慢 10 倍以上），學界普遍認為「高階語言不可能兼顧效率」。
- **Backus 的賭注**：他向 IBM 提議一個「理論上不可能」的專案——設計一門語言與一個編譯器，使編譯出的碼效率**接近手工組碼**。IBM 同意了。

## 線索與推理 -- 數學式、程式、理論

### 案件的核心推理：編譯器可以比人更聰明
Backus 團隊的洞見是：人類程式師做優化時，其實是在做「局部模式匹配 + 代數化簡」——這正是機器最擅長的事。若把這些優化規則形式化，機器可以在所有地方套用它們，而人類只在少數地方想到。

優化的數學描述：若原始程式為 $P$，編譯後程式為 $C(P)$，優化的目標是：

$$\forall x: \; \llbracket P \rrbracket(x) = \llbracket C(P) \rrbracket(x), \qquad \text{cost}(C(P)) \le \text{cost}(P)$$

即**語意等價**（結果不變）且**成本下降**（更快或更小）。

### 優化一：公共子表達式消除（CSE）
若表達式中出現相同的子表達式，且其間變數未被修改，則只需計算一次：

```text
優化前：                優化後：
X = A*B + C            T = A*B
Y = A*B - D            X = T + C
                       Y = T - D
```

A*B 只需算一次乘法（704 上一次乘法要數十個週期）。

### 優化二：迴圈不變碼外提（LICM）
若迴圈內的計算不依賴迴圈變數，就把搬到迴圈外：

```python
# 迴圈不變碼外提（LICM）的模擬
# 原始程式（FORTRAN 風格）：
#   DO I = 1, N
#     A(I) = B(I) * (X**2 + Y**2)   -- (X**2+Y**2) 與 I 無關！
#   END DO

def naive(b, x, y, n):
    """優化前：每圈重算 X**2+Y**2"""
    a = [0.0] * n
    for i in range(n):
        a[i] = b[i] * (x**2 + y**2)      # 不變碼在圈內，重複計算
    return a

def optimized(b, x, y, n):
    """優化後：LICM 把不變碼提到圈外"""
    a = [0.0] * n
    t = x**2 + y**2                       # 只算一次
    for i in range(n):
        a[i] = b[i] * t
    return a

n = 1_000_000
assert naive(list(range(n)), 3.0, 4.0, n) == optimized(list(range(n)), 3.0, 4.0, n)
# 語意等價驗證：結果完全相同，但乘加次數從 3n 降為 2n+2
print("語意等價 ✓，圈內乘法次數從 3n 降為 2n+2")
```

其成本分析：原始每圈 3 個浮點運算（兩次平方一次乘），優化後每圈只剩 1 個乘法：

$$\text{cost}_{\text{before}} = 3n, \qquad \text{cost}_{\text{after}} = n + 2 \approx n$$

當 $n = 10^6$，這是近 3 倍的加速——Backus 的賭注贏在這些細節上。

### 優化三：暫存器分配（Register Allocation）
704 有 3 個索引暫存器，分配策略直接決定效率。這是 NP-hard 問題（圖著色），Backus 團隊用貪婪法與局部啟發式解決——後來 Chaitin（1981）把完整理論化為圖著色：

$$\text{衝突圖 } G = (V, E), \quad \chi(G) \le k \Rightarrow \text{可分配到 } k \text{ 個暫存器}$$

### 20 人小組的工程壯舉
1954 年先出語言規格（FORTRAN I），1957 年交出編譯器：共 25,000 行組合語言，含 6 個優化 pass——當時最複雜的單一程式。測試時鎖定 17 個大型程式（含 Boeing 的彈道程式），編譯出的碼平均只比手寫組碼慢 20%，部分甚至更快。

## 結案 -- 後果與影響
- **高階語言的勝利**：FORTRAN 的效率證明讓所有懷疑者閉嘴——到 1958 年，IBM 704 上一半以上的程式用 FORTRAN 寫。高階語言從此成為主流。
- **優化編譯器的誕生**：CSE、LICM、暫存器分配等技術成為現代編譯器的標準配備——今天 GCC/LLVM 的優化 pass 仍是 1957 年這些思想的直系後裔。
- **FORTRAN 的長壽**：FORTRAN II (1958)、IV (1962)、77、90 至今仍在科學計算中服役——史上最長壽的程式語言之一。
- **Backus 的反思**：他後來轉向 ALGOL（BNF 的發明者），1977 年獲圖靈獎時提出 FP 函數式程式設計——對「命令式語言的暴政」再發動一次革命。
- **軟體工業的起飛**：高階語言 + 優化編譯器使「軟體可以量產」——這是軟體工業的工業革命。

## 關鍵人物與文獻
- **John Backus**：FORTRAN 負責人，BNF 發明者，1977 年圖靈獎。
- 團隊成員含 **Irving Ziller、Harlan Herrick、Sheldon Best** 等 20 人。
- 文獻：
  - J. W. Backus et al., "The FORTRAN Automatic Coding System," *Proc. Western Joint Computer Conference* (1957).
  - J. W. Backus, "The History of FORTRAN I, II, and III," *IEEE Annals of the History of Computing* 20(4), 1998.
  - G. Chaitin, "Register Allocation & Spilling via Graph Coloring," *SIGPLAN* (1981).
