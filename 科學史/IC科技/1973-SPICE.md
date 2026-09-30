# 1973-SPICE

## 案件摘要
1973 年，Berkeley 的 Laurence Nagel 與 Donald Pederson 發表 SPICE（Simulation Program with Integrated Circuit Emphasis），把電路設計從「麵包板試誤」變成「電腦數值實驗」。此後五十餘年，幾乎每一顆晶片在流片前都先在 SPICE 的後代裡跑過一遍。

## 前因 -- 為什麼會有這個案子
- 1960 年代末 IC 複雜度暴增（摩爾定律發動），靠麵包板驗證電路已不可能：晶片上的電路無法插在麵包板上。
- IBM 有內部程式 ECAP，Berkeley 有 CANCER（Computer Analysis of Nonlinear Circuits, Excluding Radiation）——後來改名 SPICE 以去除敏感字眼並公開釋出。
- 需求：通用、免費、能在學校與公司的小型機上跑、支援 MOS 元件模型的電路模擬器。
- 線索：電路方程本質上是**非線性微分代數方程組**，可由數值方法系統化求解。

## 線索與推理 -- 數學式、程式、理論

### SPICE 架構
三層管線：**網表解析 → 方程組建立 → 數值求解**。

**1. 修正節點分析（Modified Nodal Analysis, MNA）**：對每個節點寫 KCL（$\sum I = 0$），用元件的伴隨模型（companion model）把非線性/動態元件線性化後塞進矩陣：
$$G \cdot x = b$$
其中 $G$ 是稀疏導納矩陣，$x$ 是節點電壓（與部分支路電流）向量。

**2. Newton-Raphson 非線性求解**：含二極體/MOSFET 的電路方程 $f(x)=0$ 非線性，迭代求解：
$$x_{k+1} = x_k - \left[J_f(x_k)\right]^{-1} f(x_k)$$
其中雅可比矩陣 $J_f = \partial f/\partial x$。MOSFET 飽和電流模型：
$$I_D = \frac{1}{2}\beta (V_{GS}-V_{th})^2, \quad \beta = \mu_n C_{ox}\frac{W}{L}$$
每次迭代把元件在其工作點線性化（等效為電導 + 電流源），直到 $|f(x_k)| < \varepsilon$ 收斂。

**3. LU 分解**：矩陣求解 $Gx=b$ 不直接求反矩陣，而做稀疏 LU 分解 $G = LU$，先解 $Ly=b$（前代）再 $Ux=y$（回代），複雜度 $O(n^3)$ 降為稀疏情形近似 $O(n)$。SPICE 的稀疏矩陣技術（Sparse matrix package）是它能處理數百節點電路的關鍵。

### 元件模型（BSIM）
- SPICE 2 用 Level 1–3 MOS 模型（平方律、經驗修正）。
- 短通道效應（速度飽和、亞閾值漏電、DIBL）使簡單模型失效，Berkeley 在 1980–90 年代發展 **BSIM**（Berkeley Short-channel IGFET Model）系列，今日 BSIM4/BSIM6 是晶圓廠交付 PDK 的標準模型。
- 模型參數透過**參數萃取**（從實測 I-V 曲線擬合）取得，例如用最小平方法最小化 $\sum_i (I_{meas,i} - I_{model,i}(p))^2$。

### 瞬態分析：$\frac{dx}{dt}$ 的數值積分
瞬態分析解微分方程 $\frac{dx}{dt} = f(x, t)$（如 $C\frac{dv}{dt} = i$）。SPICE 用隱式方法保證穩定：

**後向歐拉（Backward Euler）**：
$$x_{n+1} = x_n + h\, f(x_{n+1}, t_{n+1})$$
一階精度，但無條件穩定，適合剛性（stiff）電路。

**梯形法（Trapezoidal）**（SPICE 預設）：
$$x_{n+1} = x_n + \frac{h}{2}\left[f(x_n,t_n) + f(x_{n+1},t_{n+1})\right]$$
二階精度；SPICE 再搭配 LTE（局部截斷誤差）控制自動調步長，以及 Gear 法處理梯形法的振鈴問題。

### Python：簡單 nodal analysis 解 RC 電路
用後向歐拉 + MNA 解「電流源對並聯 RC」：$\;C\frac{dv}{dt} + \frac{v}{R} = I$。
```python
import numpy as np
import matplotlib.pyplot as plt

R, C, I = 1e3, 1e-9, 1e-3   # 1kΩ, 1nF, 1mA
dt, steps = 1e-8, 300
G = np.array([[1/R + C/dt]])  # 後向歐拉的 MNA 伴隨矩陣

v = np.zeros(steps + 1)
for n in range(steps):
    b = np.array([I + C/dt * v[n]])  # 電容電荷歷史項
    v[n+1] = np.linalg.solve(G, b)[0]

t = np.arange(steps + 1) * dt
plt.plot(t*1e9, v, label='backward Euler')
plt.plot(t*1e9, I*R*(1-np.exp(-t/(R*C))), '--', label='analytic')
plt.xlabel('Time (ns)'); plt.ylabel('V (V)')
plt.title('Nodal Analysis: RC circuit'); plt.legend(); plt.show()
```
理論穩態 $V_\infty = IR = 1\,\text{V}$，時間常數 $\tau = RC = 1\,\text{ns}$——數值解與解析解重合，驗證了 MNA + 後向歐拉的正確性。這 20 行程式就是 SPICE 的最小核心。

### SPICE 衍生家族
- **SPICE 2**（1975, Nagel）：C 語言重寫前身，成為業界事實標準。
- **SPICE 3**（1985）：C 語言、X 視窗、BSD 授權釋出。
- **HSPICE**（Synopsys）：商業強化版，簽核（sign-off）標準。
- **LTspice**（ADI）：免費商業版，以高速求解器聞名。
- **ngspice**：開源後繼者，SPICE 3f5 的延續。

## 結案 -- 後果與影響
- Pederson 堅持**免費公開釋出** SPICE，使它成為 EDA 產業的種子：Cadence、Synopsys、Mentor 皆由此發芽。
- 「先模擬、後流片」成為 IC 設計鐵律；模擬正確性直接決定數百萬美元的流片成敗。
- BSIM 模型 + SPICE 求解器 + PDK，構成今日晶片設計的基礎設施三件套。
- 教育影響：全世界電機系學生都用 SPICE 學電路，Pederson 獲 1997/1998 年 IEEE 榮譽獎章級肯定。

## 關鍵人物與文獻
- **Donald Pederson**（1925–2004）：Berkeley 教授，SPICE 計畫推手，堅持開放釋出。
- **Laurence Nagel**：SPICE 主要作者，博士論文 "SPICE2: A Computer Program to Simulate Semiconductor Circuits," UC Berkeley, 1975.
- L.W. Nagel & D.O. Pederson, "Simulation Program with Integrated Circuit Emphasis," Midwest Symposium on Circuit Theory, 1973.
- BSIM Group, UC Berkeley, https://bsim.berkeley.edu
