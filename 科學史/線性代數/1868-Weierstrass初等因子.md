# 1868 — Weierstrass 初等因子

## 案件摘要
1868 年，Karl Weierstrass 發表〈Zur Theorie der bilinearen und quadratischen Formen〉，提出**初等因子理論**（elementary divisors），給出雙線性型在任意基底變換下的完整分類。這份判决書嚴格地回答了：「兩個矩陣何時本質上是同一個（相似）？」Jordan 1870 年隨即將其推廣到線性變換，得到今天的 Jordan 標準形。矩陣分類這樁懸案，真正的破案者是 Weierstrass。

## 前因 -- 為什麼會有這個案子
- **Sylvester 1851–1852**：Sylvester 提出「不變式」（invariant）一詞，並證明實對稱矩陣的**慣性定律**（Sylvester's law of inertia）：二次型化簡為平方和後，正負係數個數是變換不變量。對稱二次型的分類看似完成。
- **Cayley 1858**：Cayley 發明矩陣代數，證明 Cayley–Hamilton 定理：$A$ 滿足自己的特徵多項式 $p_A(\lambda) = 0$。但他用的是非交換代數的計算技巧，對「矩陣何時相似」沒有完整答案。
- **對稱型的盲點**：Sylvester–Cayley 的方法依賴對稱性與特徵值相異的假設。一旦特徵值**重根**，或矩陣**不對稱**，整個理論失靈——重根時矩陣可能可對角化、也可能不可，差別在哪裡？無人能答。
- **Cauchy 1829** 的特徵值理論只處理對稱情形。 nineteenth 世紀中葉，天文學與力學（攝動理論、剛體運動）不斷產生需要分類的實矩陣。
- Weierstrass——分析學的嚴格化大師——被請來當偵探。他的武器不是幾何直觀，而是**多項式的因式分解**。

## 線索與推理 -- 數學式、程式、理論

### 線索一：雙線性型與合成多項式
考慮雙線性型 $A(x, y) = x^T A y$。在變換 $x = P x'$、$y = P y'$ 下，矩陣變為 $P^T A P$（**相合**，congruent）。Weierstrass 的關鍵一步：同時考慮型 $A$ 與線性型 $\lambda B$ 的「合成」$A + \lambda B$，即行列式

$$\det(A + \lambda B)$$

當 $B = I$ 時這就是特徵多項式。Weierstrass 問：$\det(A + \lambda B)$ 的因式在相合變換下哪些是不變的？

### 線索二：初等因子——破案的關鍵證物
Weierstrass 證明：對固定的特徵值 $\lambda_0$，不僅要看它出現幾次（代數重數），還要追蹤一串多項式

$$(\lambda - \lambda_0)^{k_1}, \ (\lambda - \lambda_0)^{k_2}, \ \dots, \ k_1 \ge k_2 \ge \cdots$$

這些 $(\lambda - \lambda_0)^{k_i}$ 稱為**初等因子**（elementary divisors）。**初等因子（連同各 $\lambda_0$）構成相似與相合的完全不變量**：兩個矩陣相似 $\iff$ 特徵多項式的初等因子完全相同。

例如 $p(\lambda) = (\lambda - 2)^3$ 的矩陣有三種可能：
- 初等因子 $(\lambda-2), (\lambda-2), (\lambda-2)$ → 可對角化（三個 $1\times 1$ 塊）
- $(\lambda-2)^2, (\lambda-2)$ → 一個 $2\times 2$ 塊加一個 $1\times 1$ 塊
- $(\lambda-2)^3$ → 一個 $3\times 3$ 塊

**特徵多項式相同，命運卻不同**——區分它們的，正是初等因子的分配方式。這解開了重根之謎：不可對角化的元凶是「重根被合併成大塊」。

### 線索三：Jordan 標準形——判决書的執行
每個初等因子 $(\lambda - \lambda_0)^k$ 對應一個 **Jordan 塊**：

$$J_k(\lambda_0) = \begin{pmatrix} \lambda_0 & 1 & & \\ & \lambda_0 & \ddots & \\ & & \ddots & 1 \\ & & & \lambda_0 \end{pmatrix}$$

1870 年 Camille Jordan 把 Weierstrass 的理論（原本針對雙線性型的相合）翻譯成線性變換的語言（相似），證明：**任何複矩陣都相似於 Jordan 塊的直和**。Weierstrass 1868 是嚴格的前奏，Jordan 1870 是執行判决。幾何意義：每個 Jordan 塊對應一條「廣義特徵向量鏈」$v, (A-\lambda_0)v, (A-\lambda_0)^2 v, \dots$——不變子空間的分解。

### 程式碼範例：初等因子與 Jordan 塊的數值構造
```python
import numpy as np

def jordan_block(k, lam):
    J = lam * np.eye(k)
    J[np.arange(k-1), np.arange(1, k)] = 1.0
    return J

def direct_sum(blocks):
    """Jordan 塊的直和（此例特徵值全同 λ=2）"""
    n = sum(s for s, _ in blocks)
    J = np.zeros((n, n))
    pos = 0
    for s, lam in blocks:
        J[pos:pos+s, pos:pos+s] = jordan_block(s, lam)
        pos += s
    return J

def elementary_divisors(blocks):
    """由 Jordan 塊 (尺寸, λ) 清單生成初等因子 (λ-λ0)^k"""
    return [f"(λ-{lam})^{s}" for s, lam in sorted(blocks, reverse=True)]

# 同一個特徵多項式 (λ-2)^3，三種不同的矩陣
cases = {
    "可對角化":      [(1, 2.0), (1, 2.0), (1, 2.0)],
    "一塊2+一塊1":    [(2, 2.0), (1, 2.0)],
    "單一3x3塊":     [(3, 2.0)],
}

for name, blocks in cases.items():
    J = direct_sum(blocks)
    divisors = elementary_divisors(blocks)
    print(f"{name}: 初等因子 = {divisors}, 可對角化 = {np.allclose(J, 2*np.eye(3))}")

# 數值驗證：用 Jordan 塊的冪檢驗冪零部分的成長
N = jordan_block(3, 0.0)   # 冪零塊
for m in range(1, 4):
    print(f"N^{m} = 0? {np.allclose(np.linalg.matrix_power(N, m), 0)}")
# N^3 = 0 但 N, N^2 ≠ 0：塊大小 = 3 正是冪零指數
```

輸出顯示：三個矩陣特徵多項式同為 $(\lambda-2)^3$，但初等因子各異、可對角化性不同；冪零塊 $N^3 = 0$ 直接驗證 Jordan 塊尺寸與冪零指數的關係。

## 結案 -- 後果與影響
- **矩陣分類完成**：複數域上矩陣的相似分類由初等因子完全給定。Frobenius 1878 年以後把理論整合進矩陣論，寫成今日教科書的形式。
- **函數演算的基礎**：$f(A)$ 的定義（如 $e^{At}$、矩陣函數）依賴 Jordan 分解——微分方程組 $\dot{x} = Ax$ 的解法由此奠定。
- **Frobenius 標準形**：Frobenius 1879 引入有理標準形（不變因子），把分類推廣到任意體。
- **模論的先聲**：Jordan 標準形在現代觀點下是 $\mathbb{C}[t]$-模的結構定理——初等因子理論是有限生成模分類的最早實例。
- **現代應用**：線性系統控制理論（可達性、極點配置）、PageRank 的收斂分析、數值線性代數中對 Schur 形式的偏好（Jordan 形數值不穩定），都源於這樁案件的判決書。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Karl Weierstrass | 破案者：初等因子理論（1868） |
| Camille Jordan | 執行判决：Jordan 標準形（1870） |
| Arthur Cayley | 矩陣代數與 Cayley–Hamilton（1858） |
| James Joseph Sylvester | 慣性定律與不變式（1851–52） |
| Ferdinand Georg Frobenius | 整合為矩陣論（1878–79） |

- K. Weierstrass, *Zur Theorie der bilinearen und quadratischen Formen*, Monatsber. Königl. Preuss. Akad. Wiss. Berlin (1868)。
- C. Jordan, *Traité des substitutions et des équations algébriques* (1870)。
- T. Hawkins, *Weierstrass and the theory of matrices*, Hist. Math. (1977)：本案最權威的史學考證。
