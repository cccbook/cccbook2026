# 1787 — Lagrange 二次型化簡

## 案件摘要
1788 年，Joseph-Louis Lagrange 在《分析力學》（Mécanique analytique）中處理多質點系統在平衡位置附近的小振動時，被迫面對一個純代數問題：如何把二次型 $q(x) = x^T A x$ 化成平方和？他用配方法（現稱 Lagrange 方法）給出了系統性的答案，並在力學中區分出「動能恆正」與「位能不定」兩種情形。這是特徵值理論與主軸定理的前奏——Sylvester 的慣性定律要到 1852 年才補上最後一塊拼圖，Cauchy 則在 1815 年用特徵值完成主軸問題的嚴格證明。

## 前因 -- 為什麼會有這個案子
- 1760 年代，Euler 研究剛體旋轉時引進慣性矩張量，需把三次曲面化成標準形——已隱約觸及主軸問題。
- 力學中的振動問題：多自由度系統在平衡點附近，動能 $T = \frac{1}{2}\dot{q}^T M \dot{q}$ 與位能 $V = \frac{1}{2}q^T K q$ 都是二次型，運動方程 $M\ddot{q} + Kq = 0$ 的求解取決於這兩個二次型能否同時化簡。
- 17 世紀以來，Fermat、Euler 對「平方和表示數」的零星結果（如四平方和定理的早期嘗試）提供了線索。
- Lagrange 的野心：把力學「分析化」——不要圖、不要幾何，全部用方程說話。二次型化簡正是這個計畫的核心工具。

## 線索與推理 -- 數學式、程式、理論

### 線索一：配方法——Lagrange 的化簡術
對任意二次型 $q(x) = x^T A x = \sum_{i,j} a_{ij} x_i x_j$（$A$ 對稱），Lagrange 的配方方法是：

**第一步**：若 $a_{11} \neq 0$，把含 $x_1$ 的項全部抽出：
$$q = a_{11}\left(x_1 + \frac{1}{a_{11}}\sum_{j>1} a_{1j}x_j\right)^2 + q'(x_2, \dots, x_n)$$
其中 $q'$ 是只含 $n-1$ 個變數的新二次型。

**第二步**：對 $q'$ 重複同樣操作，直到所有變數用完。

**終局**：
$$q = \lambda_1 y_1^2 + \lambda_2 y_2^2 + \cdots + \lambda_n y_n^2$$
其中 $\lambda_i$ 是非零係數，$y_i$ 是 $x$ 的線性組合。若某步驟中所有對角項為零但交叉項 $a_{pq} \neq 0$，先做替換 $x_p = z_p + z_q$、$x_q = z_p - z_q$ 製造出對角項，再繼續配方。

### 線索二：慣性定律——Sylvester 1852 年的補刀
Lagrange 配方法的係數 $\lambda_i$ 取決於配方的路徑嗎？答案是否定的。Sylvester（1852）證明**慣性定律**（Law of Inertia）：正係數個數 $p$、負係數個數 $q$、零係數個數 $z$ 是二次型的不變量，與化簡路徑無關：

$$\text{signature} = (p, q, z), \qquad \text{rank} = p + q$$

這 $(p, q)$ 就是二次型的「指紋」。例如 $x^2 - y^2$ 與 $3x^2 - 2y^2$ 指紋相同 $(1,1)$，本質上是同一類。二次型的分類問題正式結案：實對稱二次型按 $(p, q, z)$ 分成有限幾大族。

### 線索三：主軸問題——Cauchy 1815 年的特徵值路線
Lagrange 的配方用的 $y = Bx$ 不一定是**正交變換**。Cauchy 在 1815 年的論文〈Recherches sur les surfaces...〉中走另一條路：找一組互相垂直的主軸，使二次型化為標準形。這等價於求解特徵值問題：

$$A v = \lambda v, \qquad v \neq 0$$

存在非零解 $v$ 的充要條件是特徵多項式為零：

$$\det(A - \lambda I) = 0$$

對實對稱矩陣，特徵值全為實數，且不同特徵值對應的特徵向量互相正交。取 $Q = [v_1, \dots, v_n]$ 為正交矩陣，則：

$$Q^T A Q = \operatorname{diag}(\lambda_1, \dots, \lambda_n), \qquad q = \lambda_1 y_1^2 + \cdots + \lambda_n y_n^2$$

這就是**主軸定理**（Spectral Theorem 的實對稱特例）：配方法（Lagrange 1788）與特徵值法（Cauchy 1815）給出相同的標準形，但正交變換版保留了幾何意義——主軸就是橢球面的對稱軸。慣性定律再次呼應：$\lambda_i$ 的符號個數 = 二次型指紋，與座標選擇無關。

### 線索四：力學中的應用——小振動的簡正模式
對 $M\ddot{q} + Kq = 0$，做廣義特徵值問題 $K v = \omega^2 M v$，找 $v_i$ 使動能與位能同時對角化。每個簡正模式 $q(t) = v_i \cos(\omega_i t)$ 是獨立的諧振子——多體振動的耦合之謎，化為 $n$ 個獨立振盪。這正是 Lagrange 在《分析力學》中的核心成就：他證明「小振動的頻率」是系統的內在不變量，不隨座標選擇改變。慣性定律的力學版本。

### 程式碼範例：配方 vs 特徵值——二次型 $\lambda$ 與特徵值對照
```python
import numpy as np

A = np.array([[2.0, 1.0],
              [1.0, 2.0]])   # 對稱矩陣，q(x) = 2x² + 2xy·(1) + 2y²

# --- 路線一：Lagrange 配方法 ---
# q = 2x² + 2xy + 2y² = 2(x + y/2)² + (3/2)y²
lam_lagrange = [2.0, 1.5]     # 兩個平方項的係數
B = np.array([[1.0, 0.5],
              [0.0, 1.0]])    # y1 = x + y/2, y2 = y

# --- 路線二：Cauchy 特徵值法 ---
vals, Q = np.linalg.eigh(A)   # eigh: 對稱矩陣專用，返回正交 Q
print("特徵值:", vals)                     # [1, 3]
print("特徵向量:\n", Q)                    # 互相正交

# --- 對照 ---
x = np.array([0.3, -0.7])
print("原始 q(x):", x @ A @ x)
y = B @ x
print("配方後 (λ·y² 之和):", lam_lagrange[0]*y[0]**2 + lam_lagrange[1]*y[1]**2)
z = Q.T @ x
print("特徵值法 (λ·z² 之和):", vals[0]*z[0]**2 + vals[1]*z[1]**2)
# 兩條路線給出相同數值 → 標準形唯一（慣性定律）

# --- 慣性驗證：正/負/零係數個數不變 ---
print("特徵值符號: 正", np.sum(vals > 0), "負", np.sum(vals < 0), "零", np.sum(vals == 0))
```

輸出顯示：配方法的係數 $(2, 1.5)$ 與特徵值 $(1, 3)$ 數值不同，但乘上各自變換後的平方和完全一致，且正係數個數都是 2——這就是慣性定律與主軸定理的同一結案。

## 結案 -- 後果與影響
- 特徵值理論誕生：Cauchy 1815 年的主軸定理是特徵值問題的嚴格起點，之後 Cayley（1858）的矩陣代數、Jordan（1870）的標準形都是後續案件。
- 二次型分類完成：Sylvester 1852 年慣性定律讓實二次型按指紋 $(p,q,z)$ 分類，為 19 世紀後期雙線性型理論（Beltrami SVD 1873）鋪路。
- 力學影響深遠：小振動簡正模式、剛體主軸、Hamilton-Jacobi 理論全部依賴二次型化簡。
- 現代迴響：量子力學的能階（Hermite 矩陣特徵值）、統計力學的二次型、機器學習的 Hessian 分析，都是 Lagrange 配方法的後裔。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Joseph-Louis Lagrange | 《分析力學》1788，二次型配方方法 |
| Augustin-Louis Cauchy | 1815 主軸定理，特徵值路線 |
| James Joseph Sylvester | 1852 慣性定律 |
| Leonhard Euler | 慣性矩張量，前案偵探 |

- J.-L. Lagrange, *Mécanique analytique*, Paris (1788)。
- A.-L. Cauchy, *Recherches sur les surfaces élastiques*, Paris (1815)。
- J. J. Sylvester, "A demonstration of the theorem that every homogeneous quadratic polynomial is reducible by real orthogonal substitutions...", Phil. Mag. (1852)。
