# 1877 - Routh 穩定性判據

## 案件摘要

1877 年，Edward John Routh（羅斯）出版《動力系統穩定性論著》(A Treatise on the Stability of a Given State of Motion)，
提出**Routh 判據**：不用解特徵方程，只用係數排成的表格（Routh 表）就能判斷
「特徵根是否都在左半平面」。Maxwell 的線索（穩定性 = 根的實部符號，見 [1868-Maxwell論調速器.md](1868-Maxwell論調速器.md)）
被系統化成**機械化的計算程序**——工程師第一次有了「紙上判穩」的標準工具。

## 前因

- **Maxwell 的線索（1868）**：穩定性 = 特徵根實部皆負；但他只給了低階情形的條件。
- **高階系統的困境**：蒸汽機 + 調速器的模型常是 3–5 階，五階以上多項式**沒有根式解**
  （Abel–Ruffini 定理，1824）——「先解根再判穩」這條路數學上不通！
- **Abel 與 Galois 的警告**：五階以上方程不可用根式解——逼出「不求解的判據」這個全新思路。

## 線索與推理

### 第 1 步：問題的精確形式

給定特徵多項式

$$
a_n \lambda^n + a_{n-1}\lambda^{n-1} + \cdots + a_1 \lambda + a_0 = 0, \qquad a_n > 0
$$

**問題**：所有根是否都在左半平面（$\mathrm{Re}(\lambda_i) < 0$）？——不解方程回答。

### 第 2 步：Routh 表的構造

把係數排成兩列，再逐列計算：

$$
\begin{array}{c|cccc}
\lambda^n & a_n & a_{n-2} & a_{n-4} & \cdots \\
\lambda^{n-1} & a_{n-1} & a_{n-3} & a_{n-5} & \cdots \\
\lambda^{n-2} & b_1 & b_2 & b_3 & \cdots \\
\lambda^{n-3} & c_1 & c_2 & c_3 & \cdots \\
\vdots & \vdots & & & \\
\end{array}
$$

其中

$$
b_1 = \frac{a_{n-1}a_{n-2} - a_n a_{n-3}}{a_{n-1}}, \qquad
b_2 = \frac{a_{n-1}a_{n-4} - a_n a_{n-5}}{a_{n-1}}, \quad \dots
$$

$$
c_1 = \frac{b_1 a_{n-3} - a_{n-1} b_2}{b_1}, \quad \dots
$$

### 第 3 步：判據

**Routh 判據**：特徵根在右半平面的個數 = Routh 表**第一列的變號次數**。

所以：

$$
\text{穩定} \;\Longleftrightarrow\; \text{第一列全為正（無變號）}
$$

### 第 4 步：必要條件的速查版

在排 Routh 表之前，有兩個必要條件可以秒殺：

1. **係數全為正**：任何係數 $\le 0$ ⇒ 必不穩定（不用再算）。
2. **缺項**：任何次數的係數缺失 ⇒ 必不穩定。

### 範例：三階系統判穩

$$
\lambda^3 + 6\lambda^2 + 11\lambda + 6 = 0
$$

Routh 表：

$$
\begin{array}{c|cc}
\lambda^3 & 1 & 11 \\
\lambda^2 & 6 & 6 \\
\lambda^1 & \frac{6 \times 11 - 1 \times 6}{6} = 10 & \\
\lambda^0 & 6 & \\
\end{array}
$$

第一列 $1, 6, 10, 6$ 全正、無變號 ⇒ **穩定**（實際上根是 $-1, -2, -3$，全在左半平面）。

**反例**：

$$
\lambda^3 + 2\lambda^2 + \lambda + 5 = 0
$$

$$
\begin{array}{c|cc}
\lambda^3 & 1 & 1 \\
\lambda^2 & 2 & 5 \\
\lambda^1 & \frac{2 \times 1 - 1 \times 5}{2} = -1.5 & \\
\lambda^0 & 5 & \\
\end{array}
$$

第一列 $1, 2, -1.5, 5$：變號兩次（$2 \to -1.5$、$-1.5 \to 5$）⇒ **兩個根在右半平面，不穩定**。

### 為什麼這是偵探式的突破？

Maxwell 給了線索（根的實部符號），但「解根」這條路被 Abel 堵死了。
Routh 的手法是**繞過根、直接從係數提取符號資訊**——
這是「不回答原問題、回答等價問題」的偵探技巧：
不看兇手的臉（根），只看指紋（係數）。

## 後果

- Routh 判據成為經典控制的標準工具，至今仍在教科書中。
- Hurwitz（1893）獨立導出等價的矩陣形式（Hurwitz 矩陣），更適合代數證明——見 [1893-Hurwitz判據.md](1893-Hurwitz判據.md)。
- 「不求解的判據」思想延續：Nyquist 判據（1932，頻域版，見 [1932-Nyquist判據.md](1932-Nyquist判據.md)）。
- 限制：Routh 判據只適用**線性定常系統**；非線性系統要等 Lyapunov（見 [1892-Lyapunov穩定性.md](1892-Lyapunov穩定性.md)）。

## 結案陳詞

Routh 判據把「判穩」從求解方程的苦工，變成機械化的表格計算。
它證明了 Abelle 的不可能定理反而催生了新方法：**解不開的方程，可以繞開它**。
這是控制理論第一次擁有「標準化的設計工具」。
