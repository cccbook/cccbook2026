# 1870 — Jordan 標準形

## 案件摘要
1870 年，法國數學家 Camille Jordan 在《Traité des substitutions et des équations algébriques》附錄中提出：任何複數域上的方陣 $A$ 都相似於一個「幾乎對角」的標準形 $J$——Jordan 標準形。配上 Weierstrass 1868 年的初等因子理論，線性變換的分類問題宣告結案：**不論多麼「頑固」的矩陣（不可對角化），都逃不出 Jordan 塊的掌心。**

## 前因 -- 為什麼會有這個案子
- Cauchy（1826–1829）建立特徵值理論：對稱矩陣可正交對角化，特徵值皆為實數。但非對稱矩陣呢？
- Cayley（1858）定義了矩陣代數，卻沒有回答「兩個矩陣什麼時候本質上相同」——即相似分類問題。
- Hermite（1855）對複矩陣做過分類嘗試；Weierstrass（1868）以初等因子（elementary divisors）理論給出雙線性型的完全分類，但論述繁複。
- 問題的核心：特徵值 $\lambda$ 若有重根，矩陣可能**不可對角化**——例如 $A = \begin{pmatrix} \lambda & 1 \\ 0 & \lambda \end{pmatrix}$，特徵空間只有一維，找不到足夠的特徵向量張成全空間。兇手是誰？它把矩陣藏到什麼形狀裡？

## 線索與推理 -- 數學式、程式、理論

### 線索一：Jordan 塊與標準形
Jordan 發現：每個 $n \times n$ 複矩陣 $A$ 都存在可逆矩陣 $P$ 使得

$$A = P J P^{-1}, \qquad J = \begin{pmatrix} J_{k_1}(\lambda_1) & & \\ & \ddots & \\ & & J_{k_m}(\lambda_m) \end{pmatrix}$$

其中每個 **Jordan 塊** $J_k(\lambda) = \lambda I_k + N_k$ 是上雙對角矩陣：

$$J_k(\lambda) = \begin{pmatrix} \lambda & 1 & & \\ & \lambda & \ddots & \\ & & \ddots & 1 \\ & & & \lambda \end{pmatrix}$$

若所有塊都是 $1\times 1$（$N_k = 0$），矩陣可對角化；否則「1」出現在超對角線上，標記了**廣義特徵向量鏈**的長度。塊的尺寸集合（初等因子 $\{k_i\}$）在相似變換下不變——這就是分類的完整答案。

### 線索二：為什麼不可對角化？——幾何重數 < 代數重數
對 $J_2(\lambda)$，特徵多項式 $p(\mu) = (\mu - \lambda)^2$（代數重數 2），但

$$\mathrm{rank}(J_2(\lambda) - \lambda I) = \mathrm{rank}\begin{pmatrix} 0 & 1 \\ 0 & 0 \end{pmatrix} = 1 \;\Rightarrow\; \dim\ker = 1$$

（幾何重數 1）。缺口正好由廣義特徵向量補上：滿足 $(A - \lambda I)v_2 = v_1$ 的 $v_2$ 構成長度 2 的鏈。一般情形，塊的大小由冪零部分 $N$ 的零化指數決定：$N_k^k = 0$ 但 $N_k^{k-1} \neq 0$。

### 線索三：矩陣冪的爆炸性簡化——遠通量子力學
Jordan 形的最大實用價值：計算 $A^m$ 與 $e^{At}$ 變得輕而易舉。因為 $A^m = P J^m P^{-1}$，且

$$J_k(\lambda)^m = \sum_{j=0}^{\min(m,\,k-1)} \binom{m}{j} \lambda^{m-j} N_k^{\,j}$$

（二項式定理，因 $\lambda I$ 與 $N$ 可交換、$N^k = 0$ 截斷級數）。同樣地 $e^{At} = P e^{Jt} P^{-1}$ 直接給出線性 ODE 系統的解。這套「用標準形馴服矩陣函數」的思想，正是 1925 年 Heisenberg-Born 矩陣力學裡處理矩陣函數與本徵展開的數學遠因——量子力學中能量算符 $H$ 的對角化，本質上就是尋找讓 $H = PDP^{-1}$ 的表象變換。

### 程式碼範例：數值化 Jordan 形與矩陣冪驗證
```python
import numpy as np
from sympy import Matrix

# 一個不可對角化的矩陣（單一 3x3 Jordan 塊 + 一個 2x2 塊）
J, P = Matrix([[2,1,0,0,0],
               [0,2,0,0,0],
               [0,0,2,1,0],
               [0,0,0,2,0],
               [0,0,0,0,-1]]), Matrix.eye(5)
A = P * J * P.inv()

print("可對角化？", A.is_diagonalizable())          # False
print("特徵值（含重數）：", A.eigenvals())           # {2: 4, -1: 1}

# 對特徵值 2：幾何重數 vs 代數重數
E2 = (A - 2*Matrix.eye(5))
print("rank(A-2I) =", E2.rank(), "→ 幾何重數 =", 5 - E2.rank())  # 2 < 4

# Jordan 標準形
Jstd, Q = A.jordan_cells()
print("Jordan 形 =\n", Jstd)

# 驗證 A^m = P J^m P^{-1}：二項式截斷公式
m = 5
Jpow_manual = Matrix(5, 5, lambda i, j: 0)
lam = 2
# 塊 J2(2) 的 5 次冪：C(5,j) * 2^(5-j) * N^j, j=0,1
Jpow_manual[0, 0] = Jpow_manual[1, 1] = lam**m
Jpow_manual[0, 1] = 5 * lam**(m-1)      # C(5,1)*2^4
Jpow_manual[2, 2] = Jpow_manual[3, 3] = lam**m
Jpow_manual[2, 3] = 5 * lam**(m-1)
Jpow_manual[4, 4] = (-1)**m
print("手算 A^5 == numpy A**5 ?",
      np.allclose(np.array(Jpow_manual, dtype=float),
                  np.array(A**5, dtype=float)))
```

程式確認：`is_diagonalizable()` 為 False、特徵值 2 的幾何重數（2）小於代數重數（4）、Jordan 形正確還原，且用二項式截斷公式手算的 $A^5$ 與直接計算一致。

## 結案 -- 後果與影響
- 複數域上線性變換的相似分類**正式完成**：相似若且唯若初等因子（Jordan 塊尺寸）相同。
- Weierstrass-Jordan 理論合流：初等因子 + Jordan 塊 = 分類的兩面陳述。
- 線性 ODE 系統、矩陣函數、控制理論（狀態空間分解）獲得標準工具。
- 為量子力學埋下遠因：1925 年矩陣力學中「把算符對角化」的思想，以及 1926 年波動力學與矩陣力學的等價性證明（么正變換 $UQU^{-1}$），都是 Jordan 分類思想的直系後裔。
- 數值線性代數中，Jordan 形對誤差極端敏感（病態），實務上改用 Schur 分式形 $A = QTQ^*$——這是結案報告的「實務附註」。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Camille Jordan | 1870 年提出 Jordan 標準形與置換群理論 |
| Karl Weierstrass | 1868 年初等因子理論，雙線性型分類 |
| Augustin-Louis Cauchy | 1829 年特徵值與對稱矩陣理論 |
| Charles Hermite | 1855 年複矩陣分類先驅 |

- C. Jordan, *Traité des substitutions et des équations algébriques*, Paris: Gauthier-Villars (1870), Note on matrices。
- K. Weierstrass, *Zur Theorie der bilinearen und quadratischen Formen*, Berl. Monatsber. (1868)。
