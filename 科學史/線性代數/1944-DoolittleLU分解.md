# 1944 — Doolittle LU 分解

## 案件摘要
1940 年代，工程師 Myrick H. Doolittle 在美國海軍的計算工作中，把一百年前 Gauss 消去法的「過程」重新包裝成一個可儲存、可重複使用的「矩陣因式」：$A = LU$。消去法不再是丟一次即棄的手工流程，而是被拆解成下三角矩陣 $L$（乘數）與上三角矩陣 $U$（剩餘），解線性方程組從此變成「前代 + 後代」兩趟三角求解。這是 Gauss 消去法在計算機誕生前夜的程式化結案報告。

## 前因 -- 為什麼會有這個案子
- 1809–1810 年 Gauss 在研究最小平方法時，實質上已使用消去法求解法方程；19 世紀手工計算時代，天文台與大地測量局常解幾十階的線性方程組。
- 1878 年 Lebesgue、1938 年波蘭數學家 Tadeusz Banachiewicz 把消去過程整理成 $A = LU$ 的因式形式，並發明「Krakowian」演算表格，讓計算員可以照表操作。
- 1941 年英國數學家 Alan Turing 與 Fox、Wilkinson 等人在英國國家物理實驗室（NPL）也獨立發展了 LU 框架與誤差分析。
- 1944 年 Doolittle 發表的版本以 $L$ 為單位下三角（對角線為 1），即今日所謂 Doolittle 分解——差別只在乘數歸誰保管。
- 案發動機：二次世界大戰中彈道計算、雷達、飛機結構計算量暴增，同一個係數矩陣要配多組右端項反覆求解——「每次都重做消去」已不可容忍，必須把工作成果「存檔」。

## 線索與推理 -- 數學式、程式、理論

### 線索一：Gauss 消去法的隱藏結構
對 $A$ 做第 $k$ 步消去，等於左乘一個初等下三角矩陣 $E_k^{-1}$（把 $i > k$ 行的第 $k$ 元素用乘數 $\ell_{ik} = a_{ik}/a_{kk}$ 消成零）。整個消去過程可寫成：

$$E_n \cdots E_2 E_1 A = U \quad\Longrightarrow\quad A = (E_1^{-1} E_2^{-1} \cdots E_n^{-1})\, U$$

關鍵觀察：這些初等矩陣的逆相乘「不會打架」，乘數直接填進下三角的位置：

$$L = \begin{pmatrix} 1 & & & \\ \ell_{21} & 1 & & \\ \vdots & & \ddots & \\ \ell_{n1} & \cdots & \ell_{n,n-1} & 1 \end{pmatrix}, \qquad A = LU$$

消去法的「中間紀錄」原來就是 $L$ 本身——這是本案最重要的指紋。

### 線索二：前代與後代 —— 解方程的兩趟旅程
有了 $A = LU$，解 $Ax = b$ 變成兩個三角系統：

$$Ly = b \quad(\text{前代 forward substitution})， \qquad Ux = y \quad(\text{後代 back substitution})$$

前代由上往下逐行算出 $y_i = (b_i - \sum_{j<i} \ell_{ij} y_j)$；後代由下往上算出 $x_i = (y_i - \sum_{j>i} u_{ij} x_j)/u_{ii}$。兩趟各需約 $n^2/2$ 次運算，而分解本身約需 $n^3/3$ 次——主嫌是分解，但只需做一次；之後換任何右端項 $b$，只要再花 $O(n^2)$。反對稱版本（$U$ 單位上三角、$L$ 存對角）即 Crout 分解，本質相同。

### 線索三：樞軸選取 —— 沒有選擇的分解會出人命
若某個主元 $a_{kk}$ 接近零（甚至等於零），消去法會崩潰或誤差爆炸。即使行列式不為零，如

$$\begin{pmatrix} 10^{-8} & 1 \\ 1 & 1 \end{pmatrix}$$

不做選取的消去也會產生巨大乘數 $\ell = 10^8$，把誤差放大 $10^8$ 倍。解法是部分樞軸選取（partial pivoting）：每步選該列絕對值最大的元素當主元，交換行。這等於對 $A$ 做行置換 $P$，分解變成：

$$PA = LU$$

對稱正定矩陣則可免樞軸，且可拆成 $A = LL^T$（Cholesky 分解，1930 年代），運算量再省一半——這是本案件的「特殊結案條款」。

### 線索四：一行儲存 —— 把 $L$ 塞回 $U$ 的空間
實務上還有一個漂亮的收尾：$L$ 嚴格下三角、$U$ 上三角，兩者恰好互補，可以共用一個 $n \times n$ 陣列——原矩陣 $A$ 的位置在消去後正好被 $L$（下三角）與 $U$（上三角）填滿，對角線歸 $U$。這就是「原地分解」（in-place factorization），1940–50 年代記憶體以 KB 計的時代，省一個矩陣的空間就是省一整間計算室。今日 LAPACK 的 `getrf` 依然沿用這個安排：分解完成後，輸入矩陣 $A$ 的位置上站著的正是 $L$ 與 $U$。

### 程式碼範例：手寫 LU 分解與前代後代，對照 numpy
```python
import numpy as np

def lu_decompose(A):
    A = A.astype(float).copy()
    n = A.shape[0]
    L = np.eye(n)
    for k in range(n - 1):
        mults = A[k+1:, k] / A[k, k]
        L[k+1:, k] = mults
        A[k+1:, k+1:] -= np.outer(mults, A[k, k+1:])
    return L, np.triu(A)

def forward_sub(L, b):
    y = np.zeros_like(b)
    for i in range(len(b)):
        y[i] = (b[i] - L[i, :i] @ y[:i]) / L[i, i]
    return y

def back_sub(U, y):
    x = np.zeros_like(y)
    for i in range(len(y) - 1, -1, -1):
        x[i] = (y[i] - U[i, i+1:] @ x[i+1:]) / U[i, i]
    return x

rng = np.random.default_rng(0)
A = rng.normal(size=(5, 5)) + 5 * np.eye(5)   # 對角加強，確保無樞軸也穩
b = rng.normal(size=5)

L, U = lu_decompose(A)
print("‖A - LU‖ =", np.linalg.norm(A - L @ U))          # 應接近 0
x1 = back_sub(U, forward_sub(L, b))
x2 = np.linalg.solve(A, b)
print("‖x手寫 - xnumpy‖ =", np.linalg.norm(x1 - x2))      # 應接近 0
print("運算量對比: 分解 n³/3 =", 5**3 / 3, "; 每次求解 2×(n²/2) =", 2 * 25 / 2)
```

輸出顯示 $\|A - LU\| \approx 0$ 且手寫解與 `np.linalg.solve` 一致——消去法被完整「存檔」為 $L$ 與 $U$，換任何 $b$ 都能只花 $O(n^2)$ 快速結案。

## 結案 -- 後果與影響
- LU 分解成為**稠密線性系統求解的標準格式**：1970 年代 Wilkinson 與 Forsythe 的演算法彙編、EISPACK/LINPACK 函式庫都以此為骨架。
- 1992 年 LAPACK 的 `getrf`（LU with partial pivoting）以分塊演算法實現，配合 BLAS-3 充分利用快取，至今仍是 `scipy.linalg.lu`、`numpy` 底層 `dgesv` 的核心。
- 誤差分析正式化：Wilkinson 證明部分樞軸下增長因子實務上很小，奠定了數值線性代數的「可靠性證據法」。
- 前代後代的雙趟結構延伸到 $A = LL^T$、$LDL^T$，成為有限元、最小平方、卡爾曼濾波的引擎。
- 影響至今：每一台筆電上跑的 `np.linalg.solve`，本質上就是 1944 年 Doolittle 那份存檔的現代重製版。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Carl Friedrich Gauss | 消去法原創（1809） |
| Tadeusz Banachiewicz | 1938 年 $A=LU$ 因式化與 Krakowian 演算 |
| Myrick H. Doolittle | 1944 年單位下三角版本（Doolittle 分解） |
| Prescott D. Crout | 1941 年 Crout 分解變體 |
| James H. Wilkinson | 誤差分析與樞軸選取理論 |

- T. Banachiewicz, *Principes d'une technique d'analyse*, Bull. Acad. Polon. Sci. (1938)。
- M. H. Doolittle, 見 Hormer V. Craig 與美國海岸大地測量局之記述（1944 年代文獻）。
- G. H. Golub & C. F. Van Loan, *Matrix Computations*, 4th ed., Johns Hopkins (2013)，Ch. 3。
