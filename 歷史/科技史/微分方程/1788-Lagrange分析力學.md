# 1788 拉格朗日與分析力學

## 案發現場

牛頓的《原理》（1687）把力學變成數學，但牛頓的方法是**幾何的**：每道難題都要畫圖、構作輔助線、用幾何比例推理。到了十八世紀，力學累積了龐大的成果——擺的運動、複合擺、剛體、流體、行星攝動——但每一類問題都有一套自己的技巧，宛如各自為政的破案手法，**沒有統一的方法論**。

更深的困境是**約束問題**。單擺被繩子約束在圓弧上，剛體被約束保持形狀不變——牛頓方法必須把約束力（繩的張力、支點的反作用力）當作未知數先引進再消去，繁瑣且容易出錯。問題越多、約束越複雜，圖就越畫不下去。

拉格朗日（Joseph-Louis Lagrange）在都靈與柏林深耕力學近三十年，於 1788 年出版《分析力學》（Mécanique analytique）。這本書做了兩件驚天動地的事：

1. **全書無一圖**。拉格朗日在序言中宣稱：「本書中找不到任何圖形。我所闡述的方法，既不需要作圖，也不需要幾何或力學的論證，只需要代數運算——遵循一貫而規律的分析步驟。」力學徹底「分析化」了。
2. **統一的方法論**：無論是擺、剛體還是行星系，一律用**廣義座標**與一條**萬能方程**——拉格朗日方程——求解。這是力學的「大一統」。

## 偵查過程

**第一步：廣義座標——把約束「藏」進座標裡。**
拉格朗日的關鍵洞察：與其在直角座標 $(x, y, z)$ 中硬扛約束，不如**直接用描述系統形態的獨立參數**。單擺用擺角 $\theta$（一個數就夠了，繩長約束自動滿足）、平面雙擺用 $(\theta_1, \theta_2)$、$N$ 個自由度的系統用 $(q_1, \dots, q_N)$。直角座標是廣義座標的函數：

$$
\mathbf{r}_i = \mathbf{r}_i(q_1, \dots, q_N, t)
$$

約束力從方程中**徹底消失**——它們被座標的選擇吸收了。

**第二步：從虛功原理出發。**
拉格朗日力學的公理基礎是**達朗貝爾-拉格朗日原理**（虛功原理的動力學推廣）：對任意虛位移 $\delta \mathbf{r}_i$（滿足約束的瞬時假想位移），

$$
\sum_i (\mathbf{F}_i - m_i \mathbf{a}_i) \cdot \delta \mathbf{r}_i = 0
$$

理想約束下約束力的虛功為零，所以只剩主動力做功。這一步是達朗貝爾（1743）與拉格朗日的接力。

**第三步：鏈鎖法則的代數推理——導出拉格朗日方程。**
把虛位移用廣義座標表達：$\delta \mathbf{r}_i = \sum_j \dfrac{\partial \mathbf{r}_i}{\partial q_j}\delta q_j$，代入虛功原理。經過純代數的整理（這正是「無一圖」的精髓——每一步都是鏈鎖法則與指標運算），得到廣義力 $Q_j = \sum_i \mathbf{F}_i \cdot \frac{\partial \mathbf{r}_i}{\partial q_j}$ 滿足：

$$
\sum_i m_i \mathbf{a}_i \cdot \frac{\partial \mathbf{r}_i}{\partial q_j} = \frac{d}{dt}\left( \sum_i m_i \dot{\mathbf{r}}_i \cdot \frac{\partial \mathbf{r}_i}{\partial q_j} \right) - \sum_i m_i \dot{\mathbf{r}}_i \cdot \frac{d}{dt}\frac{\partial \mathbf{r}_i}{\partial q_j}
$$

而由 $\mathbf{r}_i(q, t)$ 的齊次性質，有兩個關鍵恆等式：

$$
\frac{\partial \mathbf{r}_i}{\partial q_j} = \frac{\partial \dot{\mathbf{r}}_i}{\partial \dot q_j}, \qquad
\frac{d}{dt}\frac{\partial \mathbf{r}_i}{\partial q_j} = \frac{\partial \dot{\mathbf{r}}_i}{\partial q_j}
$$

於是引入**動能** $T = \frac{1}{2}\sum_i m_i |\dot{\mathbf{r}}_i|^2$，定義**拉格朗日函數** $L = T - V$（$V$ 為位能），上式化為一條對每個廣義座標成立的方程：

$$
\boxed{\,\frac{d}{dt}\frac{\partial L}{\partial \dot q_i} - \frac{\partial L}{\partial q_i} = 0, \qquad i = 1, \dots, N\,}
$$

**第四步：實戰驗證——單擺。**
單擺：$q = \theta$，$x = l\sin\theta$，$y = -l\cos\theta$。動能與位能：

$$
T = \frac{1}{2} m l^2 \dot\theta^2, \qquad V = -mgl\cos\theta \quad\Longrightarrow\quad L = \frac{1}{2} m l^2 \dot\theta^2 + mgl\cos\theta
$$

代入拉格朗日方程：

$$
\frac{d}{dt}(m l^2 \dot\theta) - (-mgl\sin\theta) = 0 \quad\Longrightarrow\quad \ddot\theta + \frac{g}{l}\sin\theta = 0
$$

**一個廣義座標、三行代數**，牛頓方法需要畫圖分析張力與向心力的幾何關係，這裡完全不需要。

**第五步：守恆律的免費贈品。**
拉格朗日方程還隱含守恆律：若 $L$ 不顯含某座標 $q_k$（循環座標），則 $\partial L / \partial \dot q_k$ 守恆——**對稱性對應守恆量**的思想在此萌芽，通往 Noether 定理（1918）。

## 結案報告

《分析力學》解決了「力學缺乏統一方法論」的百年困境：從此任何力學系統，只要寫出 $L$，剩下的就是機械化的代數運算——「無一圖」不是傲慢，而是**方法論的成熟宣言**。其遺產：

1. **通往 Hamilton 力學（1834）**：哈密頓（William Rowan Hamilton）把 $q$ 與 $\dot q$ 換成 $(q, p)$（座標與動量），將拉格朗日方程改寫成對稱優美的**正則方程**：

$$
\dot q_i = \frac{\partial H}{\partial p_i}, \qquad \dot p_i = -\frac{\partial H}{\partial q_i}, \qquad H = T + V
$$

二階的 $N$ 個方程化為一階的 $2N$ 個方程，為相空間幾何與統計力學鋪路。
2. **變分法與最小作用量原理**：拉格朗日方程等價於「作用量 $\int L\, dt$ 取駐值」，這條原理成為現代物理的公理——量子力學的路徑積分（費曼，1948）、量子場論、粒子物理的標準模型，全用拉格朗日量與作用量書寫。
3. **Noether 定理（1918）**：「循環座標 → 守恆量」的思想被 Noether 嚴格化為「每一連續對稱性對應一守恆律」，成為理論物理的支柱。
4. **分析學的勝利**：拉格朗日的全分析風格確立了「以代數運算取代幾何直覺」的範式，與尤拉的場論觀點（[1755-Euler流體力學方程.md](1755-Euler流體力學方程.md)）共同把數學物理推向十九世紀的黃金時代；而他在太陽系穩定性上的工作（與拉普拉斯，[1782-Laplace位勢方程.md](1782-Laplace位勢方程.md)）則是天體力學的巔峰成就。

值得注意的是：拉格朗日本人對偏微分方程也有開創性貢獻（一階偏微分方程的特徵理論），而《分析力學》處理的振動問題，正是波動方程（[1747-dAlembert波動方程.md](1747-dAlembert波動方程.md)）與三角級數（[1763-三角級數大辯論.md](1763-三角級數大辯論.md)）的力學背景——第二幕的各條線索，在此交織成網。

## 證據與工具

以下程式用拉格朗日方程與數值積分重現單擺與雙擺的運動，展示「廣義座標 + 機械化代數」的威力。

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# ============ 第一部分：單擺（一個廣義座標 θ） ============
# 拉格朗日方程導出：θ'' + (g/l) sin θ = 0

def pendulum(t, y, g=9.8, l=1.0):
    theta, omega = y
    return [omega, -(g / l) * np.sin(theta)]   # 拉格朗日方程的右端

# 大角度釋放（牛頓的小角近似 sinθ ≈ θ 不再適用，拉格朗日方程卻直接可用）
sol = solve_ivp(pendulum, [0, 10], [np.pi / 2, 0], t_eval=np.linspace(0, 10, 500))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
ax1.plot(sol.t, sol.y[0])
ax1.set_title("Pendulum angle θ(t), released at π/2")
ax1.set_xlabel("t"); ax1.set_ylabel("θ (rad)"); ax1.grid(True, alpha=0.3)

# 相空間圖（通往 Hamilton 相空間幾何的先聲）
th = np.linspace(-np.pi, np.pi, 60)
om = np.linspace(-4, 4, 40)
TH, OM = np.meshgrid(th, om)
ax2.streamplot(TH, OM, OM, -9.8 * np.sin(TH), density=1.0, color="gray")
ax2.plot(sol.y[0], sol.y[1], "b", lw=1.5, label="trajectory")
ax2.set_title("Pendulum phase space (θ, ω)")
ax2.set_xlabel("θ"); ax2.set_ylabel("ω"); ax2.legend()
plt.tight_layout()
plt.savefig("lagrange_pendulum.png", dpi=120)
plt.show()

# 驗證能量守恆：E = T + V = (1/2) m l² ω² − m g l cosθ（L = T − V）
m = 1.0
E = 0.5 * m * 1.0**2 * sol.y[1]**2 - m * 9.8 * 1.0 * np.cos(sol.y[0])
print(f"單擺能量守恆：E 的變動範圍 = {E.max() - E.min():.2e} J（接近 0 → 拉格朗日方程正確）")

# ============ 第二部分：雙擺（兩個廣義座標 θ₁, θ₂） ============
# 拉格朗日方法的威力：兩個座標、同一條方程，無需畫圖分析四個約束力
m1 = m2 = 1.0
l1 = l2 = 1.0
g = 9.8

def double_pendulum(t, s):
    t1, w1, t2, w2 = s
    d = t1 - t2
    # 由拉格朗日方程（L = T − V）經代數整理得到的運動方程組
    den = 2 * m1 + m2 - m2 * np.cos(2 * d)
    a1 = (-g*(2*m1 + m2)*np.sin(t1) - m2*g*np.sin(t1 - 2*t2)
          - 2*np.sin(d)*m2*(w2**2*l2 + w1**2*l1*np.cos(d))) / (l1 * den)
    a2 = (2*np.sin(d)*(w1**2*l1*(m1 + m2) + g*(m1 + m2)*np.cos(t1)
          + w2**2*l2*m2*np.cos(d))) / (l2 * den)
    return [w1, a1, w2, a2]

# 混沌之舞：雙擺是低維混沌的經典範例
sol2 = solve_ivp(double_pendulum, [0, 20], [np.pi / 2, 0, np.pi / 2 + 0.01, 0],
                 t_eval=np.linspace(0, 20, 2000), rtol=1e-9)

t1, t2 = sol2.y[0], sol2.y[2]
x1, y1 = l1 * np.sin(t1), -l1 * np.cos(t1)
x2, y2 = x1 + l2 * np.sin(t2), y1 - l2 * np.cos(t2)

fig, ax = plt.subplots(figsize=(6, 6))
ax.plot(x2, y2, lw=0.4, color="steelblue", alpha=0.7)   # 擺錘 2 的軌跡
ax.plot(x2[-1], y2[-1], "ro")
ax.set_title("Double pendulum: Lagrange's (θ₁, θ₂) → chaos")
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_aspect("equal")
plt.tight_layout()
plt.savefig("lagrange_double_pendulum.png", dpi=120)
plt.show()

# 驗證混沌：初始條件僅差 0.01 rad，軌跡卻快速分離（對初值敏感）
sol3 = solve_ivp(double_pendulum, [0, 20], [np.pi / 2, 0, np.pi / 2 + 0.02, 0],
                 t_eval=np.linspace(0, 20, 2000), rtol=1e-9)
sep = np.sqrt((sol2.y[2] - sol3.y[2])**2 + (sol2.y[0] - sol3.y[0])**2)
print(f"雙擺混沌：初始差 0.01 rad，20 秒後 θ 分離量 = {sep[-1]:.2f} rad（敏感依賴 → 混沌）")
```

執行後可見：單擺的大角振盪與相空間閉軌（能量守恆驗證通過），以及雙擺看似優雅卻陷入混沌的軌跡——同一條拉格朗日方程，一個廣義座標給出可積的諧和，兩個廣義座標卻藏著混沌。這正是「無一圖」的全分析風格，通往 Hamilton 相空間與現代動力系統理論的驗屍報告。
