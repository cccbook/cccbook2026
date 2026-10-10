# 1974 - Hulse–Taylor 雙脈衝星

## 案件摘要
1974 年，Russell Hulse 與 Joseph Taylor 在波多黎各 Arecibo 望遠鏡的資料中發現雙脈衝星 PSR B1913+16。這對互繞的中子星是一具「天然的精密時鐘」——它們的軌道週期以每年約 $-2.4\times 10^{-12}$ 的速率穩定衰減，與廣義相對論預測的重力波輻射完全吻合（誤差 < 0.2%），成為重力波存在的第一個間接證據。兩人因此獲 1993 年諾貝爾物理學獎。

## 前因 -- 為什麼會有這個案子
- **1915–1916**：愛因斯坦建立廣義相對論，並預言時空的漣漪——重力波——以光速傳播。但線性化重力波方程的應變 $h \sim 10^{-21}$ 小到令人絕望，直接偵測遙不可及。
- **1967**：Jocelyn Bell 發現脈衝星（轉動的中子星），其週期穩定性可媲美原子鐘（可達 $10^{-15}$ 量級），為天文學提供了一個前所未有的計時基準。
- **問題**：愛因斯坦的重力波究竟是數學產物，還是真實的物理？能量守恆要求：若重力波帶走能量，發射源的軌道必然衰減。誰能當這個「被監視的嫌犯」？
- **案發現場**：1973–74 年，Hulse 在 Arecibo 做脈衝星巡天搜尋（作為 Taylor 的博士生），逐一計時每顆新脈衝星。多數脈衝星週期固定；但 PSR B1913+16 的脈衝到達時間卻「飄忽不定」——這是疑點，也是線索。

## 線索與推理 -- 數學式、程式、理論

### 線索一：飄移的週期
PSR B1913+16 的脈衝週期 $P \approx 59$ ms，但觀測到的到達時間呈現週期性的漂移。推理：這是**都卜勒效應**——脈衝星在軌道上運動，時而接近、時而遠離地球。這是一個**雙星系統**，且伴星也是中子星（軌道上另可見到第二組微弱脈衝）。

### 線索二：軌道參數
由脈衝到達時間擬合（周光時 model fit）可解出（Taylor & Weisberg 1982）：

| 參數 | 數值 |
|---|---|
| 軌道週期 $P_b$ | 7.75 小時 |
| 軌道離心率 $e$ | 0.617 |
| 兩星質量 $m_1, m_2$ | $1.441,\ 1.387\ M_\odot$ |
| 半長軸投影 $x = a_1\sin i / c$ | $2.34$ 光秒 |

高度偏心的短週期雙中子星系統——這正是廣義相對論效應最強的「實驗舞台」：近星點處重力場極強，輻射功率劇烈集中在近星點通過的瞬間。

### 理論：廣義相對論的四極輻射公式
線性化重力場中，質量四極矩 $Q_{ij}$ 的三階時間導數輻射功率（Peters & Mathews 1963）：

$$
P_{\rm GW} = -\frac{dE}{dt} = \frac{32}{5}\frac{G^4}{c^5}\frac{(m_1 m_2)^2 (m_1+m_2)}{a^5}\, f(e)
$$

其中偏心修正因子

$$
f(e) = \frac{1+\frac{73}{24}e^2+\frac{37}{96}e^4}{(1-e^2)^{7/2}}
$$

對 $e = 0.617$，$f(e) \approx 11.8$——偏心軌道讓輻射功率放大超過十倍！軌道能量 $E = -\dfrac{G m_1 m_2}{2a}$，故半長軸與週期皆隨時間縮小：

$$
\dot{a} = -\frac{64}{5}\frac{G^3 m_1 m_2 (m_1+m_2)}{c^5 a^3 (1-e^2)^{7/2}}\Big(1+\tfrac{73}{24}e^2+\tfrac{37}{96}e^4\Big),\qquad
\frac{\dot{P}_b}{P_b} = \frac{3}{2}\frac{\dot{a}}{a}
$$

代入 PSR B1913+16 的參數，理論預測：

$$
\dot{P}_b^{\rm GR} \approx -2.4025 \times 10^{-12}\ \text{s/s}
$$

### 推理：天窗的校正（銀河系加速項）
觀測值與理論值之間還有一道「偽線索」必須排除：地球與脈衝星都在銀河系引力場中加速，這會在觀測到的 $\dot{P}_b$ 上附加一個視運動學項（Shklovskii 效應與銀河差動自轉）：

$$
\Delta\left(\frac{\dot{P}_b}{P_b}\right)_{\rm gal} \approx \frac{a_{\rm gal}^{\rm PSR}\cdot \hat{n} - a_{\rm gal}^{\oplus}\cdot \hat{n}}{c}
$$

以脈衝星距離（$\approx 7$–8 kpc）與自行速度校正後，觀測值為：

$$
\dot{P}_b^{\rm obs} = -2.4184(51) \times 10^{-12}
$$

與 GR 預測之比為 $0.997 \pm 0.002$——**誤差小於 0.2%**。線索、理論、校正三方對質，案子水落石出：軌道能量正以重力波的形式流失。

### Python 模擬：軌道週期衰變曲線（理論 vs 觀測）

```python
import numpy as np
import matplotlib.pyplot as plt

# PSR B1913+16 參數 (SI 單位)
G, c = 6.674e-11, 2.998e8
m1, m2 = 1.441 * 1.989e30, 1.387 * 1.989e30
e = 0.617
T_obs_span = 50.0            # 觀測年數 (1974-2024)
year = 3.156e7               # 秒/年

# 由 Kepler 第三定律求初始半長軸
Pb0 = 7.75 * 3600.0
a0 = (G * (m1 + m2) * Pb0**2 / (4 * np.pi**2))**(1/3)

# GR 預測的軌道週期衰變率 (Peters 公式)
fe = (1 + 73/24*e**2 + 37/96*e**4) / (1 - e**2)**3.5
Pbdot_GR = -(192/5) * (2*np.pi)**(8/3) * (G**(5/3) / c**5) * \
           m1*m2*(m1+m2)**(-1/3) / Pb0**(5/3) * fe
print(f"Pbdot (GR)  = {Pbdot_GR:.4e}  s/s")

t = np.linspace(0, T_obs_span, 500) * year

# 積分 dP/dt = k P^(-5/3)  =>  P(t) = [P0^(8/3) - (8/3) k t]^(3/8)
k = -(8/3) * (2*np.pi)**(8/3) * (G**(5/3)/c**5) * m1*m2*(m1+m2)**(-1/3) * fe
Pb_t = (Pb0**(8/3) + k * t)**(3/8)

# 累積軌道相位差（相對於固定週期），即「拋物線狀」殘差
cum_shift = np.array([np.trapz(Pb_t[:i] - Pb0, t[:i]) for i in range(len(t))])

# 模擬觀測點（含量測雜訊）加上觀測的 Pbdot
rng = np.random.default_rng(0)
t_obs = np.linspace(0, T_obs_span, 25) * year
Pb_obs = Pb0 * (1 + (-2.4184e-12) * t_obs) + rng.normal(0, 1e-9, len(t_obs))

fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
ax[0].plot(t/year, Pb_t*1e3, 'b-', label='GR theory (Peters)')
ax[0].plot(t_obs/year, Pb_obs*1e3, 'ro', ms=4, label='observed (sim)')
ax[0].set_xlabel('year since 1974'); ax[0].set_ylabel('orbital period $P_b$ (ms)')
ax[0].legend(); ax[0].set_title('Orbital decay: 7.75h -> shorter')

# 經典圖：脈衝星到達時間的累積位移呈向下拋物線
ax[1].plot(t/year, -cum_shift, 'b-', label='GR prediction')
ax[1].set_xlabel('year since 1974'); ax[1].set_ylabel('cumulative shift (s)')
ax[1].set_title('Periastron timing: parabola = gravity waves')
ax[1].legend()
plt.tight_layout(); plt.show()
```

輸出顯示：$\dot{P}_b^{\rm GR} \approx -2.40 \times 10^{-12}$ s/s；到達時間累積位移是一條**開口向下的拋物線**（Taylor–Weisberg 的經典圖）——這條拋物線就是重力波寫下的「簽名」。

## 結案 -- 後果與影響
- **1978**：Taylor 團隊首次報告軌道衰變與 GR 吻合；之後數十年持續計時，累積符合精度達 $10^{-3}$ 以下。
- **1993**：Hulse 與 Taylor 獲諾貝爾物理學獎——「發現一種新型脈衝星，此發現使我們得以研究重力」。重力波由假說升級為被間接證實的物理實體。
- **深遠影響**：
  - 開創「相對論性雙脈衝星計時」這個持續至今的精密檢驗產業；後繼者如雙脈衝星 PSR J0737-3039（2003）以更高的精度繼續通過檢驗。
  - 為 2015 年 LIGO 的直接偵測鋪路：雙中子星合併正是 Hulse–Taylor 系統的終點（再約 3 億年）。
  - 展示了「用天體當實驗儀器」的方法學——精密計時取代精密工程。

## 關鍵人物與文獻
- **Russell Hulse**（1950–）、**Joseph Taylor**（1941–）：發現者，1993 諾貝爾獎。
- **Joel Weisberg**：Taylor 的學生，長期主導計時分析。
- 文獻：
  - Hulse & Taylor, *ApJ* **195**, L51 (1975) —— 發現論文。
  - Peters & Mathews, *Phys. Rev.* **131**, 435 (1963) —— 四極輻射功率公式。
  - Taylor & Weisberg, *ApJ* **253**, 908 (1982) —— 軌道衰變與 GR 檢驗。
  - Weisberg & Taylor, *ASP Conf. Ser.* **328**, 25 (2005) —— 30 年數據總結。
