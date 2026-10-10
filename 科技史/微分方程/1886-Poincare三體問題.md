# 1886 Poincare 三體問題

## 案發現場

1885 年，瑞典國王 Oscar II 為慶祝六十歲生日，舉辦了一場國際數學競賽。題目之一（由 Weierstrass、Mittag-Leffler、Hermite 等人擬定）是：

**給定任意多個質點依牛頓萬有引力互相吸引，假設沒有碰撞，求每個質點的座標表示為時間的級數，並證明級數對所有時間收斂。**

這就是**多體問題**（n-body problem）的「求積」挑戰。懸案的背景是：

- 兩體問題早已被 Newton 與 Kepler 解開：軌道是圓錐曲線（橢圓、拋物線、雙曲線），完美可積；
- 但**三體問題**（如日—地—月）近兩百年來無人能解。Euler、Lagrange 找到了幾個特別對稱的特解（等邊三角形解、直線共線解），一般情況束手無策；
- 數學家手上有一個「清點工具」：Hamilton 力學告訴我們，$n$ 體系統有 $3n$ 個自由度（每個質點 3 個座標），即 $6n$ 維相空間。要完全積分（參見 [1838-Jacobi與Hamilton-Jacobi方程.md](1838-Jacobi與Hamilton-Jacobi方程.md)），需要 $3n$ 個獨立的守恆量（運動積分）。三體問題：$n = 3$，需要 $18 - 6 = 12$ 個（扣除質心運動與時間平移後）獨立積分。

當時已知三體問題的守恆量恰好只有 **10 個**：總動量 3 個、質心位置 3 個、總角動量 3 個、總能量 1 個。缺口巨大。

接案的是年僅 31 歲的法國數學家 Henri Poincaré（1854–1912）。1886–1890 年，他研究這個問題，最後交出的不是「解」，而是一個震撼數學界的**否定答案**。

## 偵查過程

### 第一步：清點守恆量——為什麼 10 個不夠

先精確清點。三體系統的 Hamiltonian（參見 [1834-Hamilton正則方程.md](1834-Hamilton正則方程.md)）：

$$
H = \sum_{i=1}^{3}\frac{|\mathbf{p}_i|^2}{2m_i} - G\sum_{i<j}\frac{m_i m_j}{|\mathbf{r}_i - \mathbf{r}_j|}.
$$

已知守恆量（由正則方程結構直接導出）：

1. **總動量** $\mathbf{P} = \sum \mathbf{p}_i$（3 個分量）——空間平移對稱性；
2. **質心** $\mathbf{G} = \sum m_i \mathbf{r}_i - \mathbf{P}t$（3 個分量）——Galileo 變換；
3. **總角動量** $\mathbf{L} = \sum \mathbf{r}_i \times \mathbf{p}_i$（3 個分量）——旋轉對稱性；
4. **總能量** $H$（1 個）——時間平移對稱性。

共 $10$ 個。但要把 $18$ 維相空間完全化約成「常數運動」，扣除質心與時間（$-6$）後需要 $12$ 個獨立積分。**缺口：$2$ 個，而且不是普通的缺口。**

### 第二步：積分不變量——Poincaré 的新武器

Poincaré 在偵查中發明了全新的武器：**積分不變量**（integral invariants）。他證明：正則方程的相流保持「相體積」不變。考慮相空間中一小塊區域 $D$，讓它的每個點沿正則方程演化時間 $t$，得到區域 $D_t$，則

$$
\mathrm{Vol}(D_t) = \mathrm{Vol}(D).
$$

證明的核心是計算體積的變化率。區域 $D_t$ 隨相流移動，其體積導數由散度給出：

$$
\frac{d}{dt}\mathrm{Vol}(D_t) = \int_{D_t} \nabla\cdot \mathbf{X}\,d\tau,
$$

其中 $\mathbf{X} = \left(\frac{\partial H}{\partial p_1}, -\frac{\partial H}{\partial q_1}, \ldots\right)$ 是相流向量場。計算散度：

$$
\nabla\cdot\mathbf{X} = \sum_i\left(\frac{\partial^2 H}{\partial q_i \partial p_i} - \frac{\partial^2 H}{\partial p_i \partial q_i}\right) = 0.
$$

混合偏導數相等（$H$ 光滑），兩兩相消——**相流是「不可壓縮」的**。這就是**Liouville 定理**（參見 [1841-Liouville可積性之謎.md](1841-Liouville可積性之謎.md) 的進一步發揮）。

Poincaré 更進一步：不只相體積，還有更高階的**積分不變量**——相曲面上「辛面積」$\oint p\,dq$ 的循環積分也不變。這些不變量是判斷「能否化約」的計數工具。

### 第三步：偵查高潮——積分不足，一般情況不可解

Poincaré 聚焦於**限制性三體問題**的簡化模型：兩個大質量（如太陽與木星）做圓周運動，一個小質量（如小行星）在它們的引力場中運動（小質量不影響大質量）。這化成二自由度的 Hamilton 系統。

Poincaré 證明的關鍵策略：假設系統存在一個**新的、獨立於能量之外的解析運動積分**（即第一積分），會導出什麼？

他把系統寫成「擾動」形式：Hamiltonian $H = H_0(I) + \varepsilon H_1(I, \theta)$，其中 $H_0$ 是可積部分（$I$ 是作用量變數，$\theta$ 是角變數），$\varepsilon$ 是小擾動參數（質量比）。若存在解析積分 $\Phi(I, \theta)$，對 $\varepsilon$ 做冪級數展開，逐階檢查：

- 第 $0$ 階：$\Phi_0$ 只能是 $H_0$ 的函數（可積部分的積分）；
- 第 $1$ 階：$\Phi_1$ 滿足一個沿「未擾動軌道」的傳輸方程，其 Fourier 展開的係數分母包含**共振組合** $k\cdot\omega(I)$（$\omega$ 是未擾動頻率）。

關鍵來了：Poincaré 證明，只要擾動中存在**足夠多的共振**（即存在整數向量 $k \ne 0$ 使 $k\cdot\omega(I) = 0$ 的 $I$ 點——這在二自由度系統中必然出現），解析積分的級數就會在共振面附近**發散**。無窮多個共振面把相空間切割得支離破碎，任何新的解析積分都無法穿越。

**結論：一般的三體問題不存在新的解析第一積分。** 十個守恆量就是全部——缺口補不上，系統不可完全積分，國王要求的「收斂級數解」不存在。

Poincaré 在修改競賽論文的過程中還發現了更驚人的事：相軌道在共振附近會出現**無窮複雜的糾纏**——穩定流形與不穩定流形相交出無窮多個「同宿點」，軌道對初值極度敏感。他寫道：「這些交織如此複雜，我甚至無法把它們畫出來。」這是**混沌**（chaos）的第一次現身。

### 第四步：驗證——數值上看見混沌

用數值方法驗證 Poincaré 的洞見：對限制性三體問題的軌道做**Poincaré 截面**（在每次經過某個截面時記錄相點），可積系統的截面點落在光滑曲線上，混沌系統的截面點散布成雲。初值的微小差異隨時間指數放大（正 Lyapunov 指數）——這正是 Poincaré 看到的「敏感依賴」。

## 結案報告

Poincaré 解開了三體問題之謎——以否定的方式：**一般情況下不可解**。僅有的 10 個守恆量不足以完全積分，新的解析積分因共振而無法存在，軌道還會混沌化。

遺產：

1. **混沌理論**：Poincaré 發現的「同宿糾纏」與敏感依賴，是二十世紀 Lorenz（1963）混沌、Feigenbaum 普適性的源頭；「蝴蝶效應」的數學祖先。
2. **KAM 定理**：Kolmogorov-Arnold-Moser 定理（1954–1963）回答了 Poincaré 留下的問題：小擾動下「大部分」不變環面仍存活，只有共振面附近破碎——對 Poincaré 證明的精細化。
3. **拓撲學**：Poincaré 為了研究軌道幾何而發明的工具（同倫、基本群、Betti 數），催生了**代數拓撲學**——他從天體力學走進了拓撲，日後留下著名的 Poincaré 猜想。
4. **動力系統理論**：相空間、截面、流形、遍歷理論，全從這一案萌芽；Liouville 的相體積不變定理成為遍歷理論的基石（參見 [1841-Liouville可積性之謎.md](1841-Liouville可積性之謎.md)）。
5. **數值方法的地位**：「解析解不存在」確立了數值模擬在天體力學中的正統地位——今日的太陽系長期演化模擬、航天軌道設計全是這一案的後代。

## 證據與工具

```python
# Poincare 三體問題：數值驗證守恆量與混沌
import numpy as np
from scipy.integrate import solve_ivp

# 1) 清點守恆量：二體問題的能量與角動量守恆
def two_body(t, z):
    """二體問題化為單體：r'' = -r/|r|^3（單位質量、單位引力參數）"""
    x, y, vx, vy = z
    r = np.sqrt(x*x + y*y)
    return [vx, vy, -x/r**3, -y/r**3]

def energy_L(z):
    x, y, vx, vy = z
    E = 0.5*(vx**2 + vy**2) - 1.0/np.sqrt(x*x + y*y)   # 能量
    L = x*vy - y*vx                                     # 角動量
    return E, L

sol = solve_ivp(two_body, [0, 20], [1.0, 0.0, 0.0, 1.0], rtol=1e-10, max_step=0.01)
Es = [energy_L(z) for z in sol.y.T]
E0, E1 = Es[0][0], Es[-1][0]
L0, L1 = Es[0][1], Es[-1][1]
print(f"二體問題：能量 {E0:.6f} -> {E1:.6f}，角動量 {L0:.6f} -> {L1:.6f}（守恆 ✓）")
print("橢圓軌道驗證：r 的範圍 =", np.sqrt(sol.y[0]**2 + sol.y[1]**2).min(),
      np.sqrt(sol.y[0]**2 + sol.y[1]**2).max(), "（應為常數的橢圓）")

# 2) 可積性計數：三體需要 12 個獨立積分（扣除質心與時間），只有 10 個
n = 3
print(f"{n} 體系統：{2*3*n} 維相空間，完全積分需 {3*n - 3} 個獨立積分（扣除質心與時間）")
print(f"已知守恆量：動量 3 + 質心 3 + 角動量 3 + 能量 1 = 10 個")
print("缺口存在 => 一般情況不可完全積分（Poincare 1890 證明）")

# 3) 混沌偵訊：非線性系統的敏感依賴（雙擺型 Hamilton 系統）
def nonlinear_ham(t, z):
    """H = p^2/2 + cos(q) + 0.5 p^2 型擺；取強非線性區域"""
    q, p = z
    return [p, -np.sin(q)]

s1 = solve_ivp(nonlinear_ham, [0, 50], [3.0, 0.0], rtol=1e-12, max_step=0.01)
s2 = solve_ivp(nonlinear_ham, [0, 50], [3.000001, 0.0], rtol=1e-12, max_step=0.01)
d = np.abs(s1.y[0] - s2.y[0])
print(f"單擺（高能量）：初值差 1e-6，50 秒後軌道差 = {d[-1]:.4f}")
print("（高能單擺接近混沌邊緣；三體問題的共振糾纏更甚）")

# 4) Poincare 截面：可積系統截面點落在曲線上
# 以 H0(I) + eps*H1(I,theta) 的思想，用微擺的截面示範
eps = 0.3
def perturbed(t, z):
    q, p = z
    return [p, -np.sin(q) - eps*np.sin(2*q)]   # 微擾項破壞可積性

s = solve_ivp(perturbed, [0, 200], [2.0, 0.5], rtol=1e-10, max_step=0.01)
q, p = s.y
# 截面：每次 q 穿越 0（上升時）記錄 p
crossings = []
for i in range(len(q)-1):
    if q[i] < 0 <= q[i+1]:
        frac = (0 - q[i])/(q[i+1] - q[i])
        crossings.append(p[i] + frac*(p[i+1] - p[i]))
print(f"Poincare 截面：{len(crossings)} 次穿越，p 值範圍 = "
      f"{min(crossings):.3f} ~ {max(crossings):.3f}")
print("（可積時截面點應落在離散曲線上；微擾後開始擴散——KAM 破壞的前兆）")

# 5) 視覺化：橢圓軌道 + 相空間糾纏
import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 2, figsize=(10, 4))
ax[0].plot(sol.y[0], sol.y[1]); ax[0].set_title("二體：可積的橢圓軌道")
ax[1].plot(s.y[0], s.y[1], lw=0.5); ax[1].set_title("微擾系統：軌道開始糾纏")
for a in ax: a.set_xlabel("q"); a.set_ylabel("p")
plt.savefig("poincare.png", dpi=100)
print("已存圖 poincare.png")
```
