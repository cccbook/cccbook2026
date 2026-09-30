# 1927 van der Pol 振盪子

## 案發現場

1920 年代，荷蘭飛利浦（Philips）實驗室。無線電技術剛剛起飛，工程師們面對一個實際又惱人的現象：真空管振盪電路有時會穩定地發出純音，有時卻發出嘶啞的「張弛」聲——波形像鋸齒一樣慢爬快跳，甚至出現奇怪的「整數倍頻率鎖定」。用線性電路理論完全無法解釋：線性系統的振盪要嘛指數衰減（阻尼），要嘛指數發散（能量無限增長），**不可能有穩定的有限振幅振盪**。

Balthasar van der Pol（1889–1959），荷蘭物理學家與無線電工程師，在飛利浦實驗室研究真空管三極管電路。1920 年他發表了描述該電路的方程，1926 年與 van der Mark 合作研究其張弛振盪與「頻率分割」（frequency demultiplication）現象，1927 年發表了著名的論文，徹底改變了非線性振動的研究典範。

此謎題之所以重要：工程上，振盪器的穩定振幅是無線電發射的基礎；科學上，這是第一個被系統研究的**自激振盪**（self-sustained oscillation）系統——它不需要週期外力，卻能自己產生穩定的週期行為。這在線性理論的框架內是邏輯上不可能的，必須引入非線性。

## 偵查過程

### 線索一：真空管電路的物理

van der Pol 的三極管電路含一個 LC 共振迴路與一個提供能量的真空管。關鍵在於真空管的非線性特性：其板極電流對柵極電壓的響應是 S 形曲線——在小電壓時增益為正（提供能量），在大電壓時飽和（停止供能）。van der Pol 將此非線性特性近似為三次曲線，得到方程

$$
\ddot x - \mu(1 - x^2)\dot x + x = 0
$$

其中 $x$ 是電容電壓（無量綱化後），$\mu > 0$ 是非線性阻尼參數。

**破案的關鍵線索藏在阻尼項的符號裡**：當 $|x| < 1$ 時，$1 - x^2 > 0$，項 $-\mu(1-x^2)\dot x$ 是**負阻尼**——它給系統注入能量，振盪增長；當 $|x| > 1$ 時，$1 - x^2 < 0$，變成**正阻尼**——它消耗能量，振盪衰減。兩種機制同時存在，系統被夾在中間：**振幅穩定在 $|x| \approx 1$ 附近持續振盪**。

### 線索二：與 Poincaré 極限環的連結

van der Pol 本人可能不知道，他的方程正是 Poincaré 定性理論（見 [1886-Poincare三體問題.md](1886-Poincare三體問題.md)）所預言的結構的具體實例。改寫成一階系統：

$$
\dot x = y, \qquad \dot y = \mu(1 - x^2)y - x
$$

**第一步：奇點分析。** 唯一奇點是原點 $(0,0)$。在原點附近線性化，$1-x^2 \approx 1$，得

$$
\dot x = y, \qquad \dot y = \mu y - x
$$

特徵方程 $\lambda^2 - \mu\lambda + 1 = 0$，特徵根

$$
\lambda_{\pm} = \frac{\mu \pm \sqrt{\mu^2 - 4}}{2}
$$

當 $\mu > 0$，$\mathrm{Re}\,\lambda_{\pm} > 0$——原點是**不穩定焦點**（$\mu < 2$）或不穩定結點（$\mu > 2$）。軌線從原點向外逃逸。

**第二步：無窮遠分析。** 當 $|x|$ 很大，$\dot y \approx \mu(-x^2)y$，強正阻尼把軌線拉回。Poincaré–Bendixson 定理（1901）說：平面有界區域內若不含不動點以外的閉軌候選……更精確地，一個「外緣向內、內緣向外」的環域若不含奇點，必含極限環。van der Pol 方程正是這種結構：**原點排斥 + 無窮遠吸引 = 必有極限環**。

**第三步：本徵函數展開（平均法）。** van der Pol 用了緩慢變化振幅的近似。設 $x = r(t)\cos(t + \phi(t))$，$r, \phi$ 隨時間緩慢變化，對一個週期平均後得

$$
\dot r = \frac{\mu}{2} r\left(1 - \frac{r^2}{4}\right), \qquad \dot\phi = 0
$$

這個一階方程有穩定平衡點 $r = 2$：**極限環的振幅為 2**（在此尺度下），與 $\mu$ 無關。這解釋了工程上的核心謎題：振盪器的振幅由非線性飽和決定，與初始條件無關——這就是「自激振盪」的本質。

### 線索三：張弛振盪與頻率分割

當 $\mu \gg 1$（強非線性），方程的行為劇變。振盪變成「張弛」型：軌線沿 $x = \pm 2$ 附近的「慢分支」緩慢爬行，到達分支末端後快速跳躍到另一分支。慢運動的時間尺度由 $\dot x \approx \mu x^2 \dot x$ 主導，可推出爬行時間 $\sim \mu$，而跳躍時間 $\sim 1$。**兩個相差 $\mu$ 倍的時間尺度**正是奇異攝動理論（singular perturbation）的典型場景。

更奇特的是 van der Pol 與 van der Mark 在 1927 年用張弛電路發現的「頻率分割」：當電容充電時間被外部週期信號調制，電路會鎖定在外力的整數分之一頻率——這是**鎖頻現象**（frequency locking）的最早記錄之一，半個世紀後成為混沌學中 Arnold 舌頭與準週期道路的核心（見 [1963-Lorenz混沌與蝴蝶效應.md](1963-Lorenz混沌與蝴蝶效應.md)）。他們當時甚至聽到了「不穩定的雜訊」——事後看來，那可能就是混沌的前兆。

## 結案報告

van der Pol 的偵破路線：

1. **物理觀察**：真空管的非線性 S 形特性 → 三次非線性阻尼項；
2. **符號分析**：負阻尼（小振幅）+ 正阻尼（大振幅）→ 必有穩定有限振幅；
3. **定性理論**：Poincaré–Bendixson 定理保證極限環存在；
4. **平均法**：緩慢振幅近似給出振幅 $r = 2$ 與 $\mu$ 無關；
5. **奇異攝動**：$\mu \gg 1$ 時兩個時間尺度分離 → 張弛振盪。

其遺產：

- **非線性振動典範**：van der Pol 方程成為非線性動力系統的「果蠅」（模式生物），幾乎每一本非線性動力學教科書都從它講起。
- **工程**：振盪器設計、鎖相迴路（PLL）、雷射動力學、心臟起搏器模型，全部有 van der Pol 的影子。
- **生物**：心臟節律、神經元放電（FitzHugh–Nagumo 模型正是 van der Pol 的變體）。
- **奇異攝動理論**：張弛振盪的分析催生了 matched asymptotic expansions。
- **混沌的前夜**：受迫 van der Pol 方程在參數空間中展現鎖頻、倍週期與混沌——這是從極限環（[1900-Hilbert與微分方程問題.md](1900-Hilbert與微分方程問題.md) 第 16 問）通往混沌的重要橋樑。
- **數值方法**：van der Pol 方程因其在 $\mu$ 大時的剛性（stiffness），成為剛性 ODE 求解器的標準測試題（見 [1975-數值解與SciPy.md](1975-數值解與SciPy.md)）。

## 證據與工具

以下程式數值求解 van der Pol 方程，展示極限環、張弛振盪與剛性現象：

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# van der Pol 方程: x'' - mu*(1-x^2)*x' + x = 0
# 改寫成一階系統: x' = y,  y' = mu*(1-x^2)*y - x

def vdp(t, z, mu):
    x, y = z
    return [y, mu*(1 - x**2)*y - x]

t_span = (0, 60)

# 實驗一：不同 mu 值下的波形——小 mu 近似正弦，大 mu 變張弛振盪
mus = [0.3, 1.0, 5.0]
fig, axes = plt.subplots(len(mus), 1, figsize=(10, 8), sharex=True)
for ax, mu in zip(axes, mus):
    # mu 大時系統是剛性的，必須用剛性求解器（見 1975-數值解與SciPy.md）
    method = 'Radau' if mu >= 5 else 'RK45'
    sol = solve_ivp(vdp, t_span, [0.5, 0.0], args=(mu,), t_eval=np.linspace(*t_span, 6000),
                    method=method, rtol=1e-8)
    ax.plot(sol.t, sol.y[0], lw=0.8)
    ax.set_title(f"mu = {mu}  ({'張弛振盪' if mu >= 5 else '近正弦振盪'})")
    ax.grid(alpha=0.3)
axes[-1].set_xlabel('t')
plt.tight_layout()
plt.savefig("vdp_waveforms.png", dpi=120)
plt.show()

# 實驗二：相平面——極限環的可視化（mu = 1）
mu = 1.0
sols = [solve_ivp(vdp, t_span, ic, args=(mu,), t_eval=np.linspace(*t_span, 6000),
                  rtol=1e-8) for ic in ([0.1, 0.0], [3.0, 3.0], [0.5, -2.0])]

fig, ax = plt.subplots(figsize=(7, 6))
for sol in sols:
    ax.plot(sol.y[0], sol.y[1], lw=0.8)
ax.plot(0, 0, 'rx', ms=12, label='不穩定焦點（原點）')
# 極限環理論振幅：平均法給出 r = 2（即 x^2+y^2 ≈ 4 的圓附近）
theta = np.linspace(0, 2*np.pi, 100)
ax.plot(2*np.cos(theta), 2*np.sin(theta), 'k--', lw=1, label='平均法預測 r=2')
ax.set_xlabel('x'); ax.set_ylabel("x'")
ax.set_title(f'van der Pol 極限環 (mu={mu})：無論初值，軌線都收斂到同一閉軌')
ax.legend(); ax.grid(alpha=0.3); ax.set_aspect('equal')
plt.tight_layout()
plt.savefig("vdp_limit_cycle.png", dpi=120)
plt.show()

# 實驗三：驗證振幅與 mu 無關（平均法的預測）
print("穩態振幅隨 mu 的變化（平均法預測恆為 2）:")
for mu in [0.3, 1.0, 3.0]:
    sol = solve_ivp(vdp, (0, 200), [0.5, 0.0], args=(mu,),
                    t_eval=np.linspace(100, 200, 2000), rtol=1e-8)
    amp = sol.y[0].max() - sol.y[0].min()
    print(f"  mu={mu}: 峰對谷振幅 = {amp:.3f} (半幅 ≈ {amp/2:.3f})")
```

程式展示了偵查的三個證據：極限環的吸引性（相平面）、波形從正弦到張弛的質變（$\mu$ 掃描）、振幅與 $\mu$ 無關（平均法驗證）。當 $\mu = 5$ 時，注意我們不得不改用隱式求解器 `Radau`——這個小小的工程細節，正是剛性方程故事的入口（見 [1975-數值解與SciPy.md](1975-數值解與SciPy.md)）。而受迫 van der Pol 方程中隱藏的不規則行為，將在 1963 年被 Lorenz 以更徹底的方式揭示。
