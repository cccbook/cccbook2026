# 1969-Strassen矩陣乘法

## 案件摘要

1969 年，德國數學家 Volker Strassen 發表了一篇標題即宣言的論文：〈Gaussian elimination is not optimal〉。兩百年來，矩陣乘法 $O(n^3)$ 被視為顯然的最優——三個巢狀迴圈，一個不多。 Strassen 卻證明：只要把 $2 \times 2$ 矩陣乘法所需的 8 次標量乘法巧妙地降到 7 次，分治遞迴就會把整體複雜度降到 $O(n^{\log_2 7}) \approx O(n^{2.807})$。 這樁案子的破案時刻不只是一個更快的演算法，而是一個哲學宣言：「顯然最優」也可以被打破。

## 前因 -- 為什麼會有這個案子

- 矩陣乘法的 $O(n^3)$ 定義自高斯消去法（Gaussian elimination）的傳統：$n \times n$ 矩陣相乘需要 $n^3$ 次標量乘法，自 19 世紀以來無人質疑。
- Strassen 的動機恰恰是想證明「高斯消去法不是最優」——他在研究消除法（elimination）的複雜性下界時，意外發現上界反而可以更低。
- 分治法在 1960 年代已經成熟：von Neumann 的合併排序（1945）展示 $O(n \log n)$，Karatsuba 的整數乘法（1960）展示 $O(n^{1.585})$，都是先聲。
- Karatsuba 的案例尤其關鍵：它證明「乘法次數」這種看似最基本的運算量也可以削減，為 Strassen 提供了方法論模板。

## 線索與推理 -- 數學式、程式、理論

### 線索一：Karatsuba 的先聲

兩個 $n$ 位數相乘，樸素法需要 $n^2$ 次單位乘法。Karatsuba（1960）把每數切成兩半：

$$
x = x_1 \cdot 2^m + x_0, \qquad y = y_1 \cdot 2^m + y_0
$$

樸素法需要 4 次半長乘法（$x_1 y_1, x_1 y_0, x_0 y_1, x_0 y_0$），Karatsuba 只用 3 次：

$$
xy = x_1 y_1 \cdot 2^{2m} + \big[(x_1 + x_0)(y_1 + y_0) - x_1 y_1 - x_0 y_0\big] \cdot 2^m + x_0 y_0
$$

遞迴關係：

$$
T(n) = 3T(n/2) + O(n) \implies T(n) = O(n^{\log_2 3}) = O(n^{1.585})
$$

「少一次乘法、多幾次加法」在漸進意義下大賺——這正是 Strassen 的靈感來源。

### 線索二：Strassen 的 7 次乘法

$2 \times 2$ 矩陣乘法 $C = AB$，樸素分治需要 8 次子矩陣乘法。Strassen 把 $A$、$B$ 各分成四塊 $A = \begin{pmatrix} A_{11} & A_{12} \\ A_{21} & A_{22} \end{pmatrix}$，$B$ 同理，然後只做 7 次乘法：

$$
\begin{aligned}
M_1 &= (A_{11} + A_{22})(B_{11} + B_{22}) \\
M_2 &= (A_{21} + A_{22})B_{11} \\
M_3 &= A_{11}(B_{12} - B_{22}) \\
M_4 &= A_{22}(B_{21} - B_{11}) \\
M_5 &= (A_{11} + A_{12})B_{22} \\
M_6 &= (A_{21} - A_{11})(B_{11} + B_{12}) \\
M_7 &= (A_{12} - A_{22})(B_{21} + B_{22})
\end{aligned}
$$

結果由加減法組合（無需再乘）：

$$
\begin{aligned}
C_{11} &= M_1 + M_4 - M_5 + M_7 \\
C_{12} &= M_3 + M_5 \\
C_{21} &= M_2 + M_4 \\
C_{22} &= M_1 - M_2 + M_3 + M_6
\end{aligned}
$$

### 線索三：主定理的應用

遞迴關係：

$$
T(n) = 7T(n/2) + O(n^2)
$$

由主定理（master theorem）：$a = 7$，$b = 2$，$f(n) = O(n^2)$，且 $n^{\log_2 7} \approx n^{2.807}$ 支配 $n^2$，故

$$
T(n) = O(n^{\log_2 7}) = O(n^{2.8074})
$$

每省一次標量乘法，指數就下降一截：8 次 ⇒ $n^3$，7 次 ⇒ $n^{2.807}$。

### 線索四：後續戰場與理論極限

- Pan（1978）降到 $O(n^{2.795})$，Coppersmith–Winograd（1990）降到 $O(n^{2.376})$。
- 2010 年代的組合改進（Vassilevska Williams、Le Gall 等）將指數壓到 $O(n^{2.373})$ 左右。
- 理論下界是 $n^2$（輸出本身就有 $n^2$ 個元素），但至今無人達到。
- AlphaTensor（DeepMind，2022）用強化學習搜尋張量分解，為 $4 \times 4$ 矩陣找到 47 次乘法的方案，刷新了該尺寸的紀錄。

### 線索五：Python 實作與實測

以下程式實作 Strassen 矩陣乘法，並統計乘法次數對照樸素法：

```python
mul_count = {"naive": 0, "strassen": 0}

def mat_mul(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                mul_count["naive"] += 1
                C[i][j] += A[i][k] * B[k][j]
    return C

def add(A, B):
    return [[a + b for a, b in zip(ra, rb)] for ra, rb in zip(A, B)]

def sub(A, B):
    return [[a - b for a, b in zip(ra, rb)] for ra, rb in zip(A, B)]

def strassen(A, B):
    n = len(A)
    if n == 1:
        mul_count["strassen"] += 1
        return [[A[0][0] * B[0][0]]]
    m = n // 2
    half = lambda M, i, j: [row[j*m:(j+1)*m] for row in M[i*m:(i+1)*m]]
    A11, A12, A21, A22 = (half(A, i, j) for i in (0, 1) for j in (0, 1))
    B11, B12, B21, B22 = (half(B, i, j) for i in (0, 1) for j in (0, 1))
    M1 = strassen(add(A11, A22), add(B11, B22))
    M2 = strassen(add(A21, A22), B11)
    M3 = strassen(A11, sub(B12, B22))
    M4 = strassen(A22, sub(B21, B11))
    M5 = strassen(add(A11, A12), B22)
    M6 = strassen(sub(A21, A11), add(B11, B12))
    M7 = strassen(sub(A12, A22), add(B21, B22))
    C11 = add(sub(add(M1, M4), M5), M7)
    C12 = add(M3, M5)
    C21 = add(M2, M4)
    C22 = add(sub(add(M1, M2), M3), M6)
    return [r1 + r2 for r1, r2 in zip(C11, C12)] + \
           [r1 + r2 for r1, r2 in zip(C21, C22)]

n = 16
A = [[i * n + j + 1 for j in range(n)] for i in range(n)]
B = [[(i + j) % 7 + 1 for j in range(n)] for i in range(n)]

C1 = mat_mul(A, B)
C2 = strassen(A, B)
print("results equal:", C1 == C2)
print(f"naive multiplications:    {mul_count['naive']:>8}")
print(f"Strassen multiplications: {mul_count['strassen']:>8}")
```

理論預測：$n = 16$ 時樸素法做 $16^3 = 4096$ 次乘法，Strassen 做 $7^{\log_2 16} = 7^4 = 2401$ 次。執行程式驗證結果相等且次數吻合。

## 結案 -- 後果與影響

- 第一次證明「顯然最優」可以打破：$O(n^3)$ 不是矩陣乘法的宿命，也動搖了其他「顯然」下界的信心。
- 分治遞迴的教科書案例：$T(n) = 7T(n/2) + O(n^2)$ 成為主定理教學的標準例題。
- 矩陣乘法指數成為獨立的研究戰場：從 Strassen 的 2.807 到 Coppersmith–Winograd 的 2.376，再到 2024 年理論極限 $n^2$ 仍未達成。
- 實務影響有限但存在：Strassen 演算法在大矩陣（$n > 10^3$）上可勝過樸素法，BLAS 函式庫與某些高效能計算場景採用了它的變體。
- Strassen 之後轉向機率演算法：Solovay–Strassen 質數測試（1977）是 RSA 時代機率質數測試的先驅。

## 關鍵人物與文獻

- Volker Strassen：德國數學家（波昂大學、蘇黎世大學），矩陣乘法與機率質數測試的先驅。
- Anatoly Karatsuba：蘇聯數學家，1960 年發明分治整數乘法。
- Shmuel Winograd：IBM 研究員，Coppersmith–Winograd 演算法合作者。
- Don Coppersmith：IBM 研究員，1990 年將指數壓到 2.376。

主要文獻：

- Strassen, V. (1969). "Gaussian elimination is not optimal". *Numerische Mathematik*, 13(4), 354–356.
- Karatsuba, A., & Ofman, Y. (1962). "Multiplication of Many-Digital Numbers by Automatic Computers". *Doklady Akademii Nauk SSSR*, 145, 293–294.
- Coppersmith, D., & Winograd, S. (1990). "Matrix Multiplication via Arithmetic Progressions". *Journal of Symbolic Computation*, 9(3), 251–280.
- Fawzi, A., et al. (2022). "Discovering Faster Matrix Multiplication Algorithms with Reinforcement Learning". *Nature*, 610, 47–53.（AlphaTensor）
- Solovay, R., & Strassen, V. (1977). "A Fast Monte-Carlo Test for Primality". *SIAM Journal on Computing*, 6(1), 84–85.
