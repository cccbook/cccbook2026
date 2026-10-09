# 1837 - Hamilton–Jacobi 方程——完全積分的魔法

## 案件摘要
1837 年前後，Jacobi 在 Königsberg 的講義（後成《力學講義》 Vorlesungen über Dynamik, 1866 出版）
把 Hamilton 的特徵函數理論推向極致：
**找一個正則變換，把 $H$ 變成零（或常數）——則新變數全部是常數，運動方程被「完全積出」。**
$$H\left(q, \frac{\partial S}{\partial q}\right) + \frac{\partial S}{\partial t} = 0$$
這條 **Hamilton–Jacobi 方程**是求解可積系統的終極武器：
不逐點積分 $2n$ 條一階方程，而是解**一條偏微分方程**——用一個函數 $S$ 概括整個系統的全部運動。

## 前因
- **Hamilton 特徵函數（1835）**：$\partial S/\partial q = p$、$\partial S/\partial t = -H$（見 [1835-Hamilton特徵函數.md](1835-Hamilton特徵函數.md)），但 Hamilton 未完成變換理論。
- **Hamilton 正則方程（1834）**：$\dot z = J\nabla H$（見 [1834-Hamilton正則方程.md](1834-Hamilton正則方程.md)）。
- **Jacobi 的偵探直覺**：正則變換不改變方程的形式 ⇒ 若能變換到 $H' = 0$，則 $\dot Q = \dot P = 0$，一切是常數。
  「解 ODE」被重述為「找變換」——這是嘉當（Cartan）「等價問題」思想的先聲。

## 線索與推理

### 核心定理（Jacobi 定理）
若找到函數 $S(q, \alpha, t)$（$n$ 個參數 $\alpha_1,\dots,\alpha_n$）滿足
$$H\left(q_1,\dots,q_n;\ \frac{\partial S}{\partial q_1},\dots,\frac{\partial S}{\partial q_n}\right) + \frac{\partial S}{\partial t} = 0$$
且 $\det\left(\dfrac{\partial^2 S}{\partial q_i\, \partial \alpha_j}\right) \neq 0$，則
$$\beta_i = \frac{\partial S}{\partial \alpha_i}\ (\text{常數}), \qquad p_i = \frac{\partial S}{\partial q_i}, \qquad \text{由 }\beta\text{ 反解 } q(t)$$
**一條 PDE 概括全部運動。**「完全積分」的魔法。

### 範例 1：自由粒子
$H = p^2/2m$。設 $S = W(x) - Et$，則 $W' = \sqrt{2mE}$：
$$S = \sqrt{2mE}\,x - Et \;\Rightarrow\; p = \partial S/\partial x = \sqrt{2mE}, \quad \beta = \partial S/\partial E = \frac{mx}{\sqrt{2mE}} - t = \text{const}$$
反解：$x(t) = \dfrac{\sqrt{2mE}}{m}(t + \beta)$——勻速運動，一次成功。

### 範例 2：諧振子（分離變數法）
$H = \dfrac{p^2}{2m} + \dfrac{kq^2}{2}$。設 $S = W(q) - Et$：
$$\frac{1}{2m}\left(\frac{dW}{dq}\right)^2 + \frac{kq^2}{2} = E \;\Rightarrow\; W = \int \sqrt{2mE - mkq^2}\;dq$$
積分後得（$\omega = \sqrt{k/m}$）：
$$S = -Et + \frac{E}{\omega}\arcsin\!\left(\sqrt{\frac{k}{2E}}\,q\right) + \frac{q}{2}\sqrt{2mE - mkq^2}$$
$\beta = \partial S/\partial E = \text{const}$ 可反解出 $q(t) = A\sin(\omega t + \phi)$。
**分離變數 = 找出可積性**——凡是能分離變數的系統都是可積的。

### 深層結構：$S$ 是一個「生成函數」
$S(q, \alpha, t)$ 生成了正則變換 $(q, p) \to (\beta, -\alpha)$：
$$p_i\,dq_i - H\,dt = \alpha_i\,d\beta_i - dS + (\text{全微分項})$$
「作用量 1-形式」$p\,dq - H\,dt$ 是整個理論的幾何對象——
日後成為辛幾何的 Liouville 1-形式、乃至費曼路徑積分的相位（見 [1948-Feynman路徑積分.md](1948-Feynman路徑積分.md)）。

### 極限的伏筆：WKB 近似
量子力學中，設 $\psi = A\,e^{iS/\hbar}$，代入 Schrödinger 方程取 $\hbar \to 0$：
$$\frac{1}{2m}\left(\nabla S\right)^2 + V = E \quad\text{(Hamilton–Jacobi 方程重現！)}$$
經典力學 = 量子力學的 $\hbar \to 0$ 極限，數學上由這條方程保證。

## 結案
- 可積系統的求解法正式定型：解 HJ 方程 → 分離變數 → 反解。開普勒問題、諧振子等盡數拿下。
- 但**並非所有系統都可分離變數**——Poincaré（1890）將證明：三體問題一般不可積（見 [1890-Poincare三體問題.md](1890-Poincare三體問題.md)）。
- 量子伏筆：HJ 方程在 1926 年成為 Schrödinger 推導波動力學的跳板（見 [1926-波動力學誕生.md](1926-波動力學誕生.md)）。
