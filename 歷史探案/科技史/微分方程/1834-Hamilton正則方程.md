# 1834 Hamilton 正則方程

## 案發現場

1834 年，愛爾蘭天文學家、數學家 William Rowan Hamilton（1805–1865）發表論文《論力學中的一般方法》（On a General Method in Dynamics）。這篇論文的表面目的是研究行星軌道，實際上卻完成了一件驚天動地的統一：**把光學與力學寫進同一套數學框架**。

懸案始於 Lagrange 力學的一個「不完美」。Lagrange 已經把牛頓力學改寫成

$$
\frac{d}{dt}\frac{\partial L}{\partial \dot q_i} - \frac{\partial L}{\partial q_i} = 0,
$$

其中 $L = T - V$ 是 Lagrangian（動能減位能），$q_i$ 是廣義座標。這套方程很美，但有兩個「瑕疵」：

1. 它是 $n$ 個**二階** ODE——二階方程不如一階方程好處理、好理解；
2. 方程同時混雜了 $q$ 與 $\dot q$，兩者地位不對稱，幾何圖像模糊。

當時還有一個更深層的謎：**光線的傳播與行星的運動，為什麼看起來這麼像？** 光有 Fermat 原理（光走時間最短的路徑），力學有 Maupertuis 原理（粒子走「作用量」最小的路徑）。兩者都是「極值原理」，形式上驚人地相似。這是巧合，還是有更深的統一？

Hamilton 從年輕時就迷上了這個謎。他 1827 年以 22 歲之齡提出「特徵函數」理論統一光學，1834–1835 年再把同一套思想搬進力學。

## 偵查過程

### 第一步：從 Lagrangian 出發——Legendre 變換

Hamilton 的第一個靈感：**換變數**。Lagrange 方程裡 $q$ 與 $\dot q$ 的地位不對稱，原因在於 Lagrangian 是 $\dot q$ 的函數而非動量的函數。Hamilton 提議把速度 $\dot q$ 換成**動量** $p$：

$$
p_i = \frac{\partial L}{\partial \dot q_i}.
$$

這個變數替換就是 **Legendre 變換**。幾何上，它把函數 $L(\dot q)$ 換成其「對偶函數」：定義

$$
H(q, p) = \sum_i p_i \dot q_i - L(q, \dot q),
$$

其中 $\dot q$ 要用 $p$ 反解出來（由 $p = \partial L/\partial \dot q$）。這個新函數 $H$ 就是**Hamiltonian**。對最常見的情形，動能是速度的二次型，此時 $H = T + V$——**動能加位能，即總能量**。

驗證一下最簡單的例子：一維自由粒子，$L = \frac{1}{2}m\dot q^2$。動量 $p = m\dot q$，反解 $\dot q = p/m$，於是

$$
H = p\cdot\frac{p}{m} - \frac{1}{2}m\left(\frac{p}{m}\right)^2 = \frac{p^2}{m} - \frac{p^2}{2m} = \frac{p^2}{2m}.
$$

正是 $\frac{1}{2}mv^2$（以 $p$ 表示），即動能。✓

### 第二步：推導正則方程

現在把 Lagrange 方程翻譯到新變數 $(q, p)$。設 $H(q, p)$ 由 Legendre 變換而來，對 $p_i$ 求偏導：

$$
\frac{\partial H}{\partial p_i} = \dot q_i + \sum_j p_j\frac{\partial \dot q_j}{\partial p_i} - \sum_j \frac{\partial L}{\partial \dot q_j}\frac{\partial \dot q_j}{\partial p_i}.
$$

最後一項由 $p_j = \partial L/\partial\dot q_j$ 恰好與前一項相消（Chain rule 的配合），剩下

$$
\frac{\partial H}{\partial p_i} = \dot q_i. \qquad \text{（第一條正則方程）}
$$

再對 $q_i$ 求偏導（固定 $p$，即 $\dot q$ 隨 $q$ 變化的部分也相消）：

$$
\frac{\partial H}{\partial q_i} = -\frac{\partial L}{\partial q_i}.
$$

而 Lagrange 方程說 $\dfrac{d}{dt}\dfrac{\partial L}{\partial \dot q_i} = \dfrac{\partial L}{\partial q_i}$，即 $\dot p_i = \dfrac{\partial L}{\partial q_i}$。代入得

$$
\frac{\partial H}{\partial q_i} = -\dot p_i. \qquad \text{（第二條正則方程）}
$$

合起來就是**Hamilton 正則方程**：

$$
\dot q_i = \frac{\partial H}{\partial p_i}, \qquad \dot p_i = -\frac{\partial H}{\partial q_i}.
$$

$n$ 個二階方程搖身一變，成了 $2n$ 個**一階**方程——而且形式完美對稱：$q$ 往 $H$ 對 $p$ 的方向走，$p$ 往 $H$ 對 $q$ 的反方向走。

### 第三步：驗證——諧振子

一維諧振子：$H = \dfrac{p^2}{2m} + \dfrac{1}{2}kq^2$。正則方程：

$$
\dot q = \frac{p}{m}, \qquad \dot p = -kq.
$$

兩式組合：$\ddot q = \dot p / m = -\dfrac{k}{m}q$，回到熟悉的 $\ddot q + \omega^2 q = 0$（$\omega^2 = k/m$），解為 $q = A\cos(\omega t) + B\sin(\omega t)$。✓ 與 Lagrange、牛頓力學完全一致。

### 第四步：相空間與守恆量

正則方程的幾何革命：$(q, p)$ 組成的 $2n$ 維空間稱為**相空間**（phase space）。系統的演化是相空間中的一條曲線（相軌道）。而能量守恆在此變得顯而易見：沿解計算 $H$ 對時間的全導數，

$$
\frac{dH}{dt} = \sum_i\left(\frac{\partial H}{\partial q_i}\dot q_i + \frac{\partial H}{\partial p_i}\dot p_i\right)
= \sum_i\left(\frac{\partial H}{\partial q_i}\frac{\partial H}{\partial p_i} - \frac{\partial H}{\partial p_i}\frac{\partial H}{\partial q_i}\right) = 0.
$$

兩項恰好相消——**$H$ 沿軌道恆定**。若 $H = T + V$，這正是能量守恆。守恆律不再是物理觀察，而是方程結構的直接推論。

### 第五步：光學與力學的統一

Hamilton 更深層的偵查成果：他在光學中定義的「特徵函數」$S$（光程），在力學中也有對應物。Fermat 原理說光走 $\delta\int n\,ds = 0$ 的路徑；Maupertuis 原理說粒子走 $\delta\int p\,ds = 0$ 的路徑。兩者的數學結構完全相同——只是把折射率 $n$ 換成動量 $p$。這個統一最終導出 Hamilton-Jacobi 方程（參見 [1838-Jacobi與Hamilton-Jacobi方程.md](1838-Jacobi與Hamilton-Jacobi方程.md)），而在一百年後，它更成為量子力學（Schrödinger 方程與 WKB 近似）的先聲。

## 結案報告

Hamilton 解開了光學與力學的統一之謎：兩者都是「變分原理 + 特徵函數」的結構。他把力學改寫為 $2n$ 個一階正則方程，並發明了相空間。

遺產：

1. **相空間與統計力學**：Boltzmann 與 Gibbs 的統計力學完全建立在相空間之上；Liouville 的「相體積不變定理」（參見 [1841-Liouville可積性之謎.md](1841-Liouville可積性之謎.md)）是正則方程的直接推論。
2. **Hamilton-Jacobi 理論**：Jacobi 完善的 HJ 方程是可積系統與量子力學的橋樑。
3. **混沌理論**：Poincaré 研究三體問題時用的正是正則方程與相空間幾何（參見 [1886-Poincare三體問題.md](1886-Poincare三體問題.md)）；Hamilton 系統的保守性導致了 KAM 定理與混沌的研究。
4. **辛幾何**：正則方程背後的幾何結構（辛形式）在二十世紀發展成辛幾何，成為現代數學的重要分支。
5. **量子力學**：正則量子化就是「把 $q, p$ 換成算符並保持對易關係 $[q,p] = i\hbar$」，直接繼承了 Hamilton 的框架。

## 證據與工具

```python
# Hamilton 正則方程數值驗證：諧振子與能量守恆
import numpy as np
from scipy.integrate import solve_ivp

def harmonic_hamiltonian(t, z):
    """諧振子 H = p^2/2m + k q^2/2，正則方程 q' = p/m, p' = -k q"""
    q, p = z
    m, k = 1.0, 4.0
    return [p/m, -k*q]

def energy(z):
    """計算 H（總能量）"""
    q, p = z
    m, k = 1.0, 4.0
    return p**2/(2*m) + k*q**2/2

# 數值求解正則方程
sol = solve_ivp(harmonic_hamiltonian, [0, 10], [1.0, 0.0], max_step=0.01)
q, p = sol.y
E = [energy([qq, pp]) for qq, pp in zip(q, p)]
print("能量守恆檢驗：H 起始 =", E[0], " 終點 =", E[-1], " 波動 =", max(E)-min(E))

# 驗證解析解 q = cos(2t)（omega = sqrt(k/m) = 2）
q_exact = np.cos(2*sol.t)
print("數值解 vs 解析解最大誤差:", np.max(np.abs(q - q_exact)))

# Legendre 變換驗證：L = 0.5*m*v^2 -> H = p^2/(2m)
m, v = 2.0, 3.0
L = 0.5*m*v**2
p_ = m*v                      # p = dL/dv
H = p_*v - L                  # H = pv - L
print("Legendre 變換：H =", H, " 應等於 p^2/(2m) =", p_**2/(2*m))

# 相空間圖：諧振子的橢圓軌道（能量守恆的幾何呈現）
import matplotlib.pyplot as plt
plt.figure(figsize=(5,5))
plt.plot(q, p, lw=1)
plt.xlabel("q"); plt.ylabel("p")
plt.title("諧振子相軌道：H = 常數的橢圓")
plt.savefig("hamilton_phase.png", dpi=100)
print("已存圖 hamilton_phase.png")

# 雙擺的混沌前身：用正則方程看非線性系統的敏感依賴
def double_well(t, z):
    """雙阱位勢 V = q^4/4 - q^2/2 的正則方程"""
    q, p = z
    return [p, -(q**3 - q)]

s1 = solve_ivp(double_well, [0, 20], [0.01, 0.0], max_step=0.01)
s2 = solve_ivp(double_well, [0, 20], [0.01001, 0.0], max_step=0.01)  # 初值差 1e-5
d = np.abs(s1.y[0] - s2.y[0])
print(f"雙阱系統：初值差 1e-5，20 秒後軌道差 = {d[-1]:.4f}（非線性系統敏感依賴）")
```
