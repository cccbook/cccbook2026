# 1838 Jacobi 與 Hamilton-Jacobi 方程

## 案發現場

Hamilton 在 1834 年的正則方程（參見 [1834-Hamilton正則方程.md](1834-Hamilton正則方程.md)）把力學變成了 $2n$ 個一階 ODE，但他留下一個未竟之業：他的「特徵函數」理論中有一個關鍵方程，形式還很笨拙，處理「帶時間的演化」時尤其彆扭。而且 Hamilton 的理論雖然統一了光學與力學，卻沒有真正回答：**怎樣的力學系統是「可解」的？怎樣用「一個函數」就把整個系統的軌道全部求出來？**

接案的，是德國數學家 Carl Gustav Jacob Jacobi（1804–1851）。Jacobi 是當時最會「算」的數學家之一——橢圓函數論、行列式（Jacobian）、變分法都是他的戰場。1837 年 Jacobi 讀到 Hamilton 的論文後驚為天人，隨即在 1838 年前後發表一系列論文，把 Hamilton 的理論改造成今天所稱的 **Hamilton-Jacobi 方程**，並發展出「完整積分」的求解方法。

## 偵查過程

### 第一步：從正則方程到主函數

Jacobi 的核心思想：**找一個「主函數」$S(q, t)$，它同時編碼了系統的全部運動資訊**。考慮一個機械系統，其 Hamiltonian 為 $H(q, p)$。Jacobi 主張：若能找到一個函數 $S$ 滿足

$$
\frac{\partial S}{\partial t} + H\!\left(q, \frac{\partial S}{\partial q}\right) = 0,
$$

這就是 **Hamilton-Jacobi 方程**——一個關於 $S$ 的**一階偏微分方程**，其中動量 $p$ 被 $\partial S/\partial q$ 取代。

它從哪裡來？從正則變換的思想：Hamilton 力學允許「正則變換」——保持正則方程形式的變數替換。若做一個由「生成函數」$S(q, P, t)$ 生成的正則變換（$P$ 是新動量），並要求新 Hamiltonian 恆為 $0$（新座標「靜止不動」——這是最極端的簡化），生成函數必須滿足：

$$
H\!\left(q, \frac{\partial S}{\partial q}, t\right) + \frac{\partial S}{\partial t} = 0.
$$

新 Hamiltonian 為零意味著：在新變數下，正則方程是 $\dot Q = 0, \dot P = 0$——**座標全部變成常數**。於是「解力學系統」化約為「解一個 PDE」。

### 第二步：分離變數——完整積分

怎麼解 HJ 方程？Jacobi 的方法：找「**完整積分**」——一個包含 $n$ 個（比變數少一）任意常數的解族

$$
S = S(q_1, \ldots, q_n, \alpha_1, \ldots, \alpha_n, t) + \beta,
$$

其中 $\alpha_i$ 是任意常數。一旦有了完整積分，軌道由隱式方程給出：

$$
\frac{\partial S}{\partial \alpha_i} = \beta_i \quad (\text{求出 } q_i(t)), \qquad
\frac{\partial S}{\partial q_i} = p_i(t).
$$

**驗證範例：一維自由粒子**。$H = \dfrac{p^2}{2m}$，HJ 方程：

$$
\frac{\partial S}{\partial t} + \frac{1}{2m}\left(\frac{\partial S}{\partial q}\right)^2 = 0.
$$

用分離變數：令 $S = W(q) - Et$（$E$ 是分離常數），代入：

$$
-E + \frac{1}{2m}\left(\frac{dW}{dq}\right)^2 = 0
\quad\Longrightarrow\quad
\frac{dW}{dq} = \pm\sqrt{2mE}
\quad\Longrightarrow\quad
W = \pm\sqrt{2mE}\,q.
$$

完整積分為 $S = \pm\sqrt{2mE}\,q - Et$。由 $\partial S/\partial E = \beta$：

$$
\pm\frac{m q}{\sqrt{2mE}} - t = \beta
\quad\Longrightarrow\quad
q(t) = \pm\sqrt{\frac{2E}{m}}\,(t + \beta).
$$

這正是勻速直線運動。✓ 一個 PDE 的解，給出了全部軌道。

### 第三步：驗證——諧振子與可積系統

一維諧振子：$H = \dfrac{p^2}{2m} + \dfrac{1}{2}m\omega^2 q^2$。同樣令 $S = W(q) - Et$：

$$
\frac{1}{2m}\left(\frac{dW}{dq}\right)^2 + \frac{1}{2}m\omega^2 q^2 = E
\quad\Longrightarrow\quad
\frac{dW}{dq} = \sqrt{2mE - m^2\omega^2 q^2}.
$$

積分得

$$
W(q) = \int \sqrt{2mE - m^2\omega^2 q^2}\,dq,
$$

這是橢圓型積分，可積出（代換 $q = \sqrt{2E/(m\omega^2)}\sin\theta$）：

$$
W(q) = \frac{E}{\omega}\arcsin\!\left(\sqrt{\frac{m\omega^2}{2E}}\,q\right) + \frac{q}{2}\sqrt{2mE - m^2\omega^2 q^2}.
$$

由 $\partial S/\partial E = \beta$ 隱式解出 $q(t)$，化簡後正是

$$
q(t) = A\cos(\omega t + \varphi).
$$

✓ 與正則方程、Lagrange 力學的解完全一致。

一般 $n$ 維系統若 HJ 方程**可完全分離變數**，系統就是**可積系統**：$n$ 個分離常數 $\alpha_i$ 就是 $n$ 個獨立的守恆量（運動積分）。這給出了「可積性」的判據——而這個判據正是 Liouville 可積性理論（參見 [1841-Liouville可積性之謎.md](1841-Liouville可積性之謎.md)）與 Poincaré 三體問題分析（參見 [1886-Poincare三體問題.md](1886-Poincare三體問題.md)）的關鍵。

### 第四步：光學與力學統一的完成

Jacobi 指出 HJ 方程與光學的深層聯繫：若把時間 $t$ 固定，$S(q, t)$ 的等值面 $S = \text{const}$ 就像「波前」，而 $\nabla S = p$ 是垂直波前的「光線方向」。粒子軌道與波前正交——**粒子的軌跡正如光線垂直於波前傳播**。這個幾何圖像在一百年後被 Schrödinger 拿來類比：經典力學之於波動力學，正如幾何光學之於波動光學。

### 第五步：通往 WKB——半經典的橋樑

HJ 方程還是量子力學 WKB 近似的起點。Schrödinger 方程

$$
-\frac{\hbar^2}{2m}\psi'' + V(q)\psi = E\psi
$$

若令 $\psi = e^{iS/\hbar}$ 並在 $\hbar \to 0$ 時做展開，最低階（比較 $1/\hbar^2$ 項）正是：

$$
\frac{1}{2m}\left(\frac{dS}{dq}\right)^2 + V(q) = E,
$$

——**這就是 HJ 方程**。經典力學是量子力學的「波長趨零」極限，橋樑正是 Jacobi 的方程。

## 結案報告

Jacobi 解開了「一個函數統治整個系統」之謎：HJ 方程的完整積分給出全部軌道；可分離變數 = 可積系統 = 有 $n$ 個守恆量。

遺產：

1. **可積系統理論**：Liouville 的可積性定理、Kolmogorov-Arnold-Moser（KAM）定理都以 HJ 理論為基礎。
2. **量子力學**：Schrödinger 方程在 $\hbar \to 0$ 時退化為 HJ 方程；WKB 近似、半經典量子化全是 HJ 理論的後代。
3. **光波統一**：Hamilton-Jacobi 的「波前—光線」圖像預示了 de Broglie 物質波與波動力學的誕生。
4. **PDE 理論**：HJ 方程是一階非線性偏微分方程的典範，其特徵線法（method of characteristics）成為解這類 PDE 的標準工具。
5. **混沌的反面教材**：正因為 HJ 分離變數極少成功（三體問題就是著名的失敗案例），人們才意識到「大多數力學系統不可積」——通往混沌的大門。

## 證據與工具

```python
# Hamilton-Jacobi 方程數值驗證：自由粒子與諧振子
import numpy as np
from scipy.integrate import solve_ivp

# 1) 一維自由粒子：完整積分 S = sqrt(2mE) q - Et 給出 q(t) = sqrt(2E/m)(t+beta)
m, E, beta = 1.0, 2.0, 0.5
def S_free(q, t):
    """HJ 方程的完整積分（自由粒子）"""
    return np.sqrt(2*m*E)*q - E*t

# 由 ∂S/∂E = beta 隱式解出 q(t)：mq/sqrt(2mE) - t = beta
def q_from_S(t):
    return np.sqrt(2*E/m)*(t + beta)

t = np.linspace(0, 2, 100)
# 檢驗 HJ 方程本身：S_t + (S_q)^2/(2m) = 0
h = 1e-5
S_t = (S_free(q_from_S(t), t+h) - S_free(q_from_S(t), t-h))/(2*h)
S_q = (S_free(q_from_S(t)+h, t) - S_free(q_from_S(t)-h, t))/(2*h)
print("HJ 方程檢驗：S_t + S_q^2/(2m) =", (S_t + S_q**2/(2*m)).max(), "（應接近 0）")

# 用正則方程獨立求解，與 HJ 結果對照
sol = solve_ivp(lambda t, z: [z[1], 0.0], [0, 2], [q_from_S(0), np.sqrt(2*E/m)], max_step=0.01)
print("HJ 求出的 q(2) =", q_from_S(2), " 正則方程數值解 =", sol.y[0][-1])

# 2) 諧振子：HJ 完整積分 vs 正則方程
w = 2.0
def harmonic_hj(t, z):
    q, p = z
    return [p/m, -m*w**2*q]

sol2 = solve_ivp(harmonic_hj, [0, 5], [1.0, 0.0], max_step=0.01)
q_exact = np.cos(w*sol2.t)
print("諧振子正則方程 vs 解析解誤差:", np.max(np.abs(sol2.y[0] - q_exact)))

# 3) WKB 近似：HJ 方程是量子力學的經典極限
from scipy.special import airy
# Airy 方程 psi'' = x psi 對應 V(q) = m w^2 q 的 WKB；這裡示範 WKB 波函數
k_of_q = lambda q: np.sqrt(2*m*(E - 0.5*m*w**2*q**2))/1.0  # 局部波數 = dS/dq
hbar = 0.05
q_wkb = np.linspace(-0.9, 0.9, 500)
# 數值積分 S(q) = ∫ k dq
S_wkb = np.array([np.trapz(k_of_q(q_wkb[:i+1]), q_wkb[:i+1]) if i>0 else 0 for i in range(len(q_wkb))])
psi_wkb = 1/np.sqrt(np.maximum(k_of_q(q_wkb), 1e-12)) * np.cos(S_wkb/hbar)
print(f"WKB 近似（hbar={hbar}）振幅 ~ 1/sqrt(k(q))，波數最大值 = {k_of_q(0):.3f}")
print("（波長越短，經典極限越好——HJ 方程在其中扮演最低階項）")
```
