# 1918 - Noether 定理——對稱性與守恆量的深層結構

## 案件摘要
1918 年，Emmy Noether 在 Göttingen 發表《不變變分問題》(Invariante Variationsprobleme)，
證明了一條統攝全部哈密頓/拉格朗日力學的定理：
**每一個連續對稱性，對應一個守恆量；反之亦然。**
$$\text{對稱性} \;\Longleftrightarrow\; \text{守恆量}$$
時間平移對稱 ⇒ 能量守恆；空間平移對稱 ⇒ 動量守恆；旋轉對稱 ⇒ 角動量守恆。
Lagrange 循環座標的樣本（見 [1788-分析力學.md](1788-分析力學.md)）、Euler 的能量積分（見 [1736-Euler力學.md](1736-Euler力學.md)），
都只是這條定理的特例。守恆律不再是「巧合」，而是**對稱性的影子**。

## 前因
- **廣義相對論的危機**：Einstein 的廣義相對論（1915）中能量守恆看似「破產」——重力場的能量無法局部定義。
  Klein 與 Hilbert 在 Göttingen 為此苦惱，邀 Noether 協助。
- **Lagrange 循環座標**：$L$ 不含 $q_j$ ⇒ $p_j$ 守恆，是「對稱 ⇒ 守恆」的具體樣本，但缺一般性證明。
- **Felix Klein 的 Erlangen 綱領（1872）**：「幾何 = 研究不變量下的變換群」——把「群」推上數學中心的思想氛圍。
- **Sophie Germail 之前的變分學女性先驅**：Noether 是變分法與抽象代數的雙料大師，手上有最強的工具。

## 線索與推理

### 定理的正向敘述（Noether 第一定理）
設作用量 $S = \int L(q, \dot q, t)\,dt$ 在連續變換
$$t \to t + \epsilon\,\tau(q, t), \qquad q_i \to q_i + \epsilon\,\xi_i(q, t)$$
下不變（$\delta L + L\,d\tau/dt = \dfrac{d(\cdots)}{dt}$ 全微分形式），則
$$\boxed{\ \sum_i \frac{\partial L}{\partial \dot q_i}(\xi_i - \dot q_i\,\tau) + L\,\tau = \text{常數}\ }$$
在運動方程的解上守恆。

### 三大守恆律的推導
| 對稱性 | 變換 | Noether 量 | 守恆律 |
|---|---|---|---|
| 時間平移 | $\tau = 1,\ \xi = 0$ | $-L + \sum\dot q_i\,\partial L/\partial \dot q_i = H$ | 能量守恆 |
| 空間平移 | $\tau = 0,\ \xi_i = 1$ | $p_i = \partial L/\partial \dot q_i$ | 動量守恆 |
| 旋轉 | $\xi_i = \epsilon_{ijk}\omega_j q_k$ | $\sum \vec r \times \vec p$ | 角動量守恆 |

**能量守恆 = 時間平移對稱**——這個等價是哈密頓力學最深刻的單一洞見。
宇宙若無時間平移對稱（如膨脹宇宙），能量守恆確實會「破產」——這正是 Einstein 廣義相對論中能量問題的解答。

### 反向敘述：守恆量 ⇔ 對稱性
若 $F(q, \dot q, t)$ 沿所有軌跡守恆（$\dot F = 0$），則存在以 $F$ 為生成函數的正則變換族（單參數辛群），使 $H$ 不變。
**守恆量生成對稱性**——例如動量 $p$ 生成平移、角動量 $\ell$ 生成旋轉。
正向與反向合起來：對稱性與守恆量是**同一件事的兩面**，溝通的橋樑正是 Poisson 括號。

### 場論版本（第二定理）
對無限維系統（場論），Noether 第二定理給出規範對稱性 ⇒ 恆等式（Noether 恆等式）。
電磁學的規範對稱、電荷守恆（$\partial_\mu j^\mu = 0$）、廣義座標不變性（廣義協變），全部由此統攝。
**現代物理場論的每一條守恆律，都要先問：「對稱性是什麼？」**

### Python 驗證：數值檢驗能量 = 時間平移守恆量
```python
import numpy as np
from scipy.integrate import solve_ivp

def pendulum(t, z):        # 單擺：L = ½ml²θ̇² − mgl(1−cosθ)，時間平移對稱
    th, w = z
    return [w, -9.81*np.sin(th)]

sol = solve_ivp(pendulum, [0, 50], [1.0, 0.0], t_eval=np.linspace(0, 50, 500), rtol=1e-10)
E = 0.5*sol.y[1]**2 + 9.81*(1-np.cos(sol.y[0]))     # H = T + V
print(E.std())   # ≈ 1e-10：能量在數值上守恆 ⟹ 對稱性的影子
```

## 結案
- 守恆律的「為什麼」有了終極答案：對稱性。物理學的研究方法被重定向：**先找對稱性，再談守恆律**。
- 現代物理的標準流程（標準模型的規範群 $SU(3)\times SU(2)\times U(1)$）完全建立在此方法論上。
- Noether 在 Göttingen 因性別被拒授教席多年，Hilbert 以「大學不是澡堂」反擊反對者——定理與人格同樣彪炳。
- 遺憾的鏡像：時間平移對稱破壞 ⇒ 能量不守恆（宇宙膨脹、暗能量），是 1998 年觀測的理論背景。
