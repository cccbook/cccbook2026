# 1843 - Jacobi 正則變換與最後乘子——相空間幾何的基礎

## 案件摘要
1843 年前後，Jacobi 在動力學講義中系統化**正則變換**（canonical transformation）理論：
哪些變換 $(q, p) \to (Q, P)$ 能保持正則方程的形式不變？
答案是：保持「正則 2-形式」$dq \wedge dp$ 不變的變換——
$$\sum_i dq_i \wedge dp_i = \sum_i dQ_i \wedge dP_i$$
這是**辛幾何**（symplectic geometry）的誕生時刻：相空間不是普通歐氏空間，而是帶辛結構的空間。
Jacobi 還發明「最後乘子」(last multiplier) 方法，處理非正則變換的修正因子。
相空間的幾何學基礎就此打下，劉維爾定理、辛流、乃至混沌理論都站在這個地基上。

## 前因
- **Hamilton 正則方程（1834）**：形式優美，但只有在「正則座標」下才成立——換座標後形式會破壞嗎？（見 [1834-Hamilton正則方程.md](1834-Hamilton正則方程.md)）
- **Hamilton–Jacobi 理論（1837）**：Jacobi 已用 $S$ 作為生成函數做變換（見 [1837-HamiltonJacobi方程.md](1837-HamiltonJacobi方程.md)），需要一般化理論。
- **生成函數的樣本**：$F_1(q, Q)$ 型生成函數已出現，$p = \partial F_1/\partial q$、$P = -\partial F_1/\partial Q$。
- **Jacobi 的問題意識**：變換的自由度有多大？哪些量在變換下不變？

## 線索與推理

### 正則變換的判據
變換 $(q,p) \to (Q,P)$ 是正則的 ⇔ 對任意封閉曲線 $C$：
$$\oint_C \sum_i p_i\,dq_i = \oint_C \sum_i P_i\,dQ_i \quad\Longleftrightarrow\quad \sum dq_i \wedge dp_i = \sum dQ_i \wedge dP_i$$
以矩陣語言：$M = \dfrac{\partial(Q,P)}{\partial(q,p)}$ 是正則的 ⇔
$$M^T J M = J, \qquad J = \begin{pmatrix} 0 & I \\ -I & 0 \end{pmatrix}$$
滿足此條件的矩陣構成群——**辛群** $Sp(2n, \mathbb{R})$。

### 不變量清單
| 不變量 | 表述 | 意義 |
|---|---|---|
| 辛 2-形式 | $\sum dq_i \wedge dp_i$ | 相空間的「面積」結構 |
| 相空間體積 | $d^{2n}z$ 不變（劉維爾）| 統計力學的基礎 |
| Poisson 括號 | $\{Q_i, P_j\} = \delta_{ij}$ | 量子對易關係的經典版 |
| Hamiltonian 的形式 | $\dot Z = J\nabla H'$ | 動力學結構不變 |

### 生成函數的四種型
| 型 | 變數 | 關係 |
|---|---|---|
| $F_1(q, Q)$ | 舊位置、新位置 | $p = \partial F_1/\partial q,\ P = -\partial F_1/\partial Q$ |
| $F_2(q, P)$ | 舊位置、新動量 | $p = \partial F_2/\partial q,\ Q = \partial F_2/\partial P$ |
| $F_3(p, Q)$ | 舊動量、新位置 | $q = -\partial F_3/\partial p,\ P = -\partial F_3/\partial Q$ |
| $F_4(p, P)$ | 舊動量、新動量 | $q = -\partial F_4/\partial p,\ Q = \partial F_4/\partial P$ |

Hamilton–Jacobi 方程的 $S(q, \alpha, t)$ 正是 $F_2$ 型：新動量 $P = \alpha$、新 Hamiltonian $H' = H + \partial S/\partial t = 0$。

### 最後乘子（last multiplier）
若變換 $q \to Q$ 不是正則的，新方程 $\dot Q = M \dot q$ 中會出現修正因子 $\mu$：
$$\mu = \frac{\partial(Q)}{\partial(q)}\ \text{的倒數相關量}$$
Jacobi 證明 $\mu$ 可由一條一階線性 PDE 求出。這是「非正則變換的補救手術」——
日後成為劉維爾方程與測度論觀點的先聲。

### 劉維爾定理（1838）的直接後果
正則變換保體積 ⇒ 相空間中的「流」不可壓縮：
$$\frac{d\rho}{dt} = \{\rho, H\} + \frac{\partial \rho}{\partial t} = 0$$
一團相點像不可壓縮流體一樣流動。統計力學（Boltzmann、Gibbs）的整個基礎就在這裡。

## 結案
- 辛幾何正式誕生：相空間 = 辛流形，動力學 = 辛同胚。
- 1890 年 Poincaré 在這個幾何舞台上發現混沌（見 [1890-Poincare三體問題.md](1890-Poincare三體問題.md)）。
- 1983 年辛積分器把「保辛結構」變成數值演算法的設計原則（見 [1983-辛積分器.md](1983-辛積分器.md)）。
