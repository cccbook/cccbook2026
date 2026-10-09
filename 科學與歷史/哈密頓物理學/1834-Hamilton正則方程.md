# 1834 - Hamilton 正則方程——相空間的誕生

## 案件摘要
1834 年，都柏林的 Hamilton 發表《論力學中的一般方法，第一篇》(On a General Method in Dynamics)。
他做了一件看似小小的手術：把 Lagrange 的 $n$ 個二階方程，換成 $2n$ 個一階方程——
$$\boxed{\ \dot q_i = \frac{\partial H}{\partial p_i}, \qquad \dot p_i = -\frac{\partial H}{\partial q_i}\ }$$
其中 $H = \sum_i p_i\dot q_i - L$（今日稱 **Hamiltonian**，多數情況下 $H = T + V$ = 總能量）。
狀態從「配置空間中的點」變成「**相空間**中的點 $(q, p)$」，動力學變成流。
這是整部哈密頓物理學的核心案件：混沌、辛幾何、量子力學，都從這組方程生長。

## 前因
- **Lagrange 形式的限制**：二階方程、配置空間觀點；邊界條件要「位置 + 速度」兩組，不對稱。
- **Hamilton 的光學研究（1827–1833）**：他在光學中已發明「特徵函數」與 $p, q$ 式的變數
  （光線的方向餘弦 = 廣義動量！），並發現光學與力學的數學結構相同。
  這個「光學–力學類比」是他進攻力學的秘密武器。
- **Lagrange 的 Legendre 變換**：$\sum p\dot q - L$ 正是熱力學也使用的 **Legendre 變換**——
  把 $(\dot q)$ 變數換成 $(p)$ 變數，且不丟失資訊。

## 線索與推理

### 推導：Legendre 變換 + Euler–Lagrange
定義 $H(q, p, t) = \sum_i p_i \dot q_i - L(q, \dot q, t)$，其中 $p_i = \partial L/\partial \dot q_i$（反解出 $\dot q_i = \dot q_i(q,p,t)$）。

微分 $H$：
$$dH = \sum_i \dot q_i\, dp_i + \sum_i p_i\, d\dot q_i - \sum_i \frac{\partial L}{\partial q_i}dq_i - \sum_i \frac{\partial L}{\partial \dot q_i}d\dot q_i - \frac{\partial L}{\partial t}dt$$
中間兩項相消（$p_i = \partial L/\partial \dot q_i$）：
$$dH = \sum_i \dot q_i\,dp_i - \sum_i \dot p_i\,dq_i - \frac{\partial L}{\partial t}dt$$
與 $dH = \sum \dfrac{\partial H}{\partial p_i}dp_i + \sum \dfrac{\partial H}{\partial q_i}dq_i + \dfrac{\partial H}{\partial t}dt$ 逐項比較，得正則方程。
注意最後一項：$\dfrac{\partial H}{\partial t} = -\dfrac{\partial L}{\partial t}$——能量隨時間的變化由 $L$ 的顯式時間相依決定。

### $H = T + V$ 的檢驗
自然系統（約束與時間無關）時：
$$H = \sum p_i \dot q_i - L = \sum \frac{\partial T}{\partial \dot q_i}\dot q_i - (T - V) = 2T - (T - V) = T + V = E$$
由 Euler 的齊次函數定理（$T$ 是 $\dot q$ 的二次齊次函數）。**Hamiltonian = 總能量**——能量正式成為動力學的主角。

### 辛結構：正則方程的幾何面貌
把 $(q, p)$ 寫成向量 $z$，正則方程可寫成：
$$\dot z = J \nabla H, \qquad J = \begin{pmatrix} 0 & I \\ -I & 0 \end{pmatrix}$$
$J$ 滿足 $J^2 = -I$、$J^T = -J$——它就是「乘以 $i$」的實矩陣版。
相空間體積、劉維爾定理、Poisson 括號 $\{f, g\} = \sum(\partial_q f\,\partial_p g - \partial_p f\,\partial_q g)$，
都從 $J$ 的結構流出。量子力學的 $[\hat q, \hat p] = i\hbar$ 正是 Poisson 括號的「量子化」。

### Poisson 括號版正則方程
$$\dot q_i = \{q_i, H\}, \qquad \dot p_i = \{p_i, H\}$$
任何力學量 $f$ 的演化：$\dot f = \{f, H\} + \partial f/\partial t$。守恆 ⇔ $\{f, H\} = 0$。

### Python 驗證：諧振子的相空間圓
```python
import numpy as np
from scipy.integrate import solve_ivp

def hamilton_osc(t, z):
    q, p = z
    return [p, -q]          # H = (q² + p²)/2  ⟹  q̇ = ∂H/∂p = p, ṗ = -∂H/∂q = -q

sol = solve_ivp(hamilton_osc, [0, 20], [1.0, 0.0], t_eval=np.linspace(0, 20, 400))
# 相空間軌跡是圓 (q² + p² = 1)——能量守恆的幾何表現
print(max(sol.y[0]**2 + sol.y[1]**2) - min(sol.y[0]**2 + sol.y[1]**2))  # ≈ 0
```

## 結案
- 正則方程、相空間、Hamiltonian 成為標準語言；力學正式轉為「一階 + 相空間」觀點。
- 1835 年續篇把光學與力學徹底統一（見 [1835-Hamilton特徵函數.md](1835-Hamilton特徵函數.md)）。
- 深遠影響鏈：
  - Jacobi 用它「完全積出」運動方程（[1837-HamiltonJacobi方程.md](1837-HamiltonJacobi方程.md)）；
  - Poincaré 在相空間發現混沌（[1890-Poincare三體問題.md](1890-Poincare三體問題.md)）；
  - Schrödinger 從 $H$ 寫出波動方程（[1926-波動力學誕生.md](1926-波動力學誕生.md)）。
