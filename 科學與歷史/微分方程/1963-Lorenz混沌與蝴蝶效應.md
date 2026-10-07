# 1963 Lorenz 混沌與蝴蝶效應

## 案發現場

1960 年代初，美國麻省理工學院（MIT）。氣象學家 Edward Lorenz（1917–2008）面對一個古老的難題：**天氣能不能長期預報？** 當時的主流信念來自氣象學界與數值計算的先驅——von Neumann 在 1950 年代曾樂觀地預言，隨著電腦速度增長，數值天氣預報終將征服天氣，甚至可以人工改造氣候。數值預報的數學基礎也看似穩固：給定大氣的初值與控制方程，解是存在且唯一的（古典決定論），那麼理論上預報可以無限精準——只要有夠快的電腦與夠密的觀測。

Lorenz 用一台 Royal McBee LGP-30 真空管電腦——每秒只能做約 60 次乘法——模擬大氣對流。他把 Rayleigh–Bénard 對流（加熱的流體層中熱流體上升、冷流體下降的現象）的偏微分方程用 Fourier 級數截斷，只保留前三個模，得到一個三維常微分方程組。此謎題之所以重要：天氣預報是當時應用科學的旗艦問題；而 Lorenz 即將發現的現象，將徹底推翻「決定論 = 可預測」這個自 Newton 以來的科學信念。

## 偵查過程

### 線索一：從對流 PDE 到三維 ODE

Rayleigh–Bénard 對流的控制方程是 Boussinesq 近似下的 Navier–Stokes 方程（偏微分方程）。Lorenz 用 Saltzman 的截斷法，把流場與溫度場展開成 Fourier 模，只保留最不穩定的三個模：流函數的振幅 $x$（對流強度）、溫度場的水平與垂直模 $y, z$。得到的方程組：

$$
\dot x = \sigma(y - x), \qquad \dot y = x(\rho - z) - y, \qquad \dot z = xy - \beta z
$$

參數的物理意義：$\sigma$ 是 Prandtl 數（動量擴散與熱擴散之比），$\rho$ 是 Rayleigh 數（驅動對流的浮力強度，正比於上下溫差），$\beta = 8/3$ 是幾何參數。Lorenz 選用的標準值是 $\sigma = 10$、$\rho = 28$、$\beta = 8/3$。

**第一步：奇點與穩定性分析。** 系統有三個奇點：原點 $O=(0,0,0)$ 與一對對稱點

$$
C_{\pm} = \left(\pm\sqrt{\beta(\rho-1)},\ \pm\sqrt{\beta(\rho-1)},\ \rho - 1\right)
$$

原點對應「無對流」的靜止狀態；$C_\pm$ 對應兩個方向相反的定常對流卷。在 $C_\pm$ 處線性化，特徵多項式為

$$
\lambda^3 + (\sigma + \beta + 1)\lambda^2 + (\rho + \sigma)\beta\lambda + 2\sigma\beta(\rho - 1) = 0
$$

**第二步：失穩的臨界值。** 用 Routh–Hurwitz 判據（三階多項式的根都有負實部的條件）：

$$
(\sigma + \beta + 1)(\rho + \sigma)\beta > 2\sigma\beta(\rho - 1)
$$

化簡得

$$
\rho < \frac{\sigma(\sigma + \beta + 3)}{\sigma - \beta - 1}
$$

代入 $\sigma = 10, \beta = 8/3$，得臨界值 $\rho_c \approx 24.74$。**當 $\rho > 24.74$，$C_\pm$ 失穩**——定常對流卷不再穩定，軌線被拋入未知的領域。Lorenz 選的 $\rho = 28$ 正好在失穩區內。

### 線索二：歷史性的偶然——初值敏感性

1961 年冬，Lorenz 想重現之前一次模擬的後半段。他沒有從頭跑，而是從中途的狀態開始：為省紙，他把之前列印出來的數值 0.506127 取整成 0.506 輸入——**只差 0.000127**。結果新軌線迅速偏離舊軌線，幾個「模擬月」後完全不同。

Lorenz 的靈感時刻是：這不是電腦誤差累積的問題，而是**方程本身的结构**。對這個系統，初值的微小誤差會被**指數放大**。數學上，若 $\delta_0$ 是初值誤差，則誤差增長近似為

$$
\delta(t) \approx \delta_0\, e^{\lambda_{\max} t}
$$

其中 $\lambda_{\max}$ 是最大 Lyapunov 指數——軌線間距離的平均指數增長率。對 Lorenz 標準參數，$\lambda_{\max} \approx 0.906$，意味著誤差約每 $\ln 2 / 0.906 \approx 0.77$ 個時間單位翻倍。Lorenz 估計，就算初值精確到小數點後十位（誤差 $10^{-10}$），預報在幾十個時間單位後也完全失效。**長期天氣預報在原理上不可能**——這是決定論的死刑判決。

1972 年，Lorenz 在一次演講中用了詩意的標題：「巴西的蝴蝶拍翅膀，會在德克薩斯引起龍捲風嗎？」——「蝴蝶效應」從此成為初值敏感性的通俗名字。

### 線索三：奇怪吸子

初值敏感性帶來一個悖論：既然軌線指數發散，它們逃到哪裡去了？答案是**有界但不重複**。Lorenz 發現，無論初值為何，軌線最終都被吸到一個有限的區域內，但永遠不會重複自己的路徑，也永遠不會收斂到週期軌道。這個集合被他稱為「確定性非週期流」的載體，後來被 David Ruelle 與 Floris Takens 在 1971 年命名為「**奇怪吸子**」（strange attractor）——「奇怪」是因為它既非點（平衡）、也非閉曲線（極限環）、也非環面（準週期），而是一個**分形**。

奇怪吸子的幾何性質：Lorenz 吸子的 Hausdorff 維數約為 2.06——介於二維曲面與三維體之間。軌線在兩個「翅膀」之間無規則地來回跳躍：在每一側繞行若干圈後跳到另一側，繞行圈數看似隨機，實則完全由決定論方程決定。**決定論與隨機性的並存**正是混沌的本質：短期可預測（方程唯一決定軌線），長期不可預測（誤差指數放大），統計上有規律（吸子的機率測度、維數、Lyapunov 譜都是確定的幾何量）。

## 結案報告

Lorenz 的偵破路線：

1. **模型截斷**：對流 PDE → 三維 ODE（保留三個 Fourier 模）；
2. **穩定性分析**：Routh–Hurwitz 判據 → $\rho_c \approx 24.74$，定常對流失穩；
3. **歷史偶然**：0.506127 → 0.506 → 軌線徹底分離 → 初值敏感性；
4. **指數放大**：最大 Lyapunov 指數 $\lambda_{\max} \approx 0.906$ → 長期預報不可能；
5. **奇怪吸子**：有界、非週期、分形維數 2.06 → 決定論混沌的幾何載體。

其遺產：

- **混沌學誕生**：Ruelle–Takens 的湍流混沌道路、Feigenbaum 的倍週期普適性（1975–1978）、May 的邏輯映射——非線性科學在 1970–80 年代爆發，Lorenz 1963 是起點。
- **科學哲學的轉折**：「決定論 = 可預測」的 Newton–Laplace 信念被推翻。Poincaré 在 1890 年三體問題中已見端倪（見 [1886-Poincare三體問題.md](1886-Poincare三體問題.md)），Lorenz 把它變成了可計算的現實。
- **氣象與預報科學**：集合預報（ensemble forecasting）、可預報性極限（約兩週）成為現代數值天氣預報的理論基礎。
- **其他領域的混沌**：心臟節律、生態族群、經濟波動、化學反應——混沌無所不在。
- **計算科學**：Lorenz 的發現本身就是電腦時代的第一個重大科學發現之一——沒有數值積分就沒有混沌。這條線索延續到 [1975-數值解與SciPy.md](1975-數值解與SciPy.md) 的數值大眾化，也與 [1927-van_der_Pol振盪子.md](1927-van_der_Pol振盪子.md) 的鎖頻現象一起，構成通往混沌的三條經典道路。

## 證據與工具

以下程式用 RK45 數值積分 Lorenz 方程，重現初值敏感性與奇怪吸子：

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Lorenz 方程組 (1963)
#   x' = sigma*(y - x)
#   y' = x*(rho - z) - y
#   z' = x*y - beta*z
sigma, rho, beta = 10.0, 28.0, 8.0/3.0

def lorenz(t, s):
    x, y, z = s
    return [sigma*(y - x), x*(rho - z) - y, x*y - beta*z]

# 實驗一：初值敏感性——兩條軌線初值只差 1e-6
t_span = (0, 40)
t_eval = np.linspace(*t_span, 8000)
s0 = [1.0, 1.0, 1.0]
eps = 1e-6
sol1 = solve_ivp(lorenz, t_span, s0, t_eval=t_eval, rtol=1e-10)
sol2 = solve_ivp(lorenz, t_span, [v+eps for v in s0], t_eval=t_eval, rtol=1e-10)

# 計算兩條軌線的距離隨時間的變化
dist = np.sqrt(np.sum((sol1.y - sol2.y)**2, axis=0))
fig = plt.figure(figsize=(12, 5))
ax1 = fig.add_subplot(1, 2, 1)
ax1.semilogy(t_eval, dist + 1e-16, lw=0.8)
ax1.set_xlabel('t'); ax1.set_ylabel('軌線距離 (對數尺度)')
ax1.set_title(f'初值敏感性：初始誤差 {eps} 指數放大\n(斜率 ≈ 最大 Lyapunov 指數)')
ax1.grid(alpha=0.3, which='both')

# 估計最大 Lyapunov 指數：對增長段做線性擬合
grow = (t_eval > 2) & (t_eval < 15) & (dist > 1e-12) & (dist < 5)
slope = np.polyfit(t_eval[grow], np.log(dist[grow]), 1)[0]
ax1.semilogy(t_eval[grow], np.exp(slope*t_eval[grow]), 'r--', lw=1,
             label=f'擬合斜率 λ ≈ {slope:.3f}')
ax1.legend()

# 實驗二：奇怪吸子的三維圖
ax2 = fig.add_subplot(1, 2, 2, projection='3d')
ax2.plot(sol1.y[0], sol1.y[1], sol1.y[2], lw=0.3)
ax2.set_title('Lorenz 奇怪吸子：有界、非週期、分形')
ax2.set_xlabel('x'); ax2.set_ylabel('y'); ax2.set_zlabel('z')
plt.tight_layout()
plt.savefig("lorenz_attractor.png", dpi=120)
plt.show()

print(f"最大 Lyapunov 指數（擬合）: {slope:.3f}  (理論值 ≈ 0.906)")
print(f"誤差翻倍時間: {np.log(2)/abs(slope):.2f} 個時間單位")

# 實驗三：z(t) 的「翅膀跳躍」——決定論的偽隨機性
plt.figure(figsize=(11, 4))
plt.plot(t_eval[:4000], sol1.y[2][:4000], lw=0.5)
plt.xlabel('t'); plt.ylabel('z')
plt.title("z(t)：在兩個對流卷之間無規則跳躍——看似隨機，實則完全決定")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("lorenz_z.png", dpi=120)
plt.show()

# 延伸：把 rho 改為 20（< 24.74），系統會收斂到定常對流卷 C± 而非混沌
# 可自行修改參數重跑，觀察混沌到非混沌的轉變
```

程式展示了偵查的全部證據：誤差在對數尺度上沿直線增長（指數放大，斜率即 Lyapunov 指數）、奇怪吸子的雙翅膀幾何、$z(t)$ 的偽隨機跳躍。1961 年 Lorenz 用一台每秒六十次乘法的電腦發現這一切；今天你用三十行 Python 就能重現。而這種「用計算發現理論」的新科學模式，正是計算時代（[1975-數值解與SciPy.md](1975-數值解與SciPy.md)）的開端。
