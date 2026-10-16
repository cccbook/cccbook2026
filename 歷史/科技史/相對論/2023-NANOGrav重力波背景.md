# 2023 - NANOGrav 重力波背景（奈赫茲宇宙合唱）

## 案件摘要
2023 年 6 月，NANOGrav 以 15 年的脈衝星計時數據首次偵測到奈赫茲（nHz, $10^{-9}$ Hz）頻段的重力波背景——最可能的來源是宇宙中無數超大型黑洞雙星（$10^8$–$10^{10}\,M_\odot$）互繞所發出的「宇宙合唱」。特徵應變譜呈 $h_c(f) \propto f^{-2/3}$，與理論預測吻合。中國 FAST、歐洲 EPTA、澳洲 PPTA 同期獨立公布相容結果。至此，重力波頻譜從 nHz 到 kHz 的完整覆蓋藍圖成形。

## 前因 -- 為什麼會有這個案子
- **1916**：愛因斯坦預言重力波；但重力波不只有「個別事件」——無數弱源疊加會形成**隨機重力波背景**（stochastic gravitational-wave background, SGWB），如同宇宙的「哼聲」。
- **1974–1993**：Hulse–Taylor 雙脈衝星間接證實重力波，同時確立了關鍵事實：**脈衝星是宇宙中最穩定的時鐘**。有人開始追問：重力波經過地球時，會不會讓所有脈衝星的「滴答」同步微微失準？
- **1983**：Sazhin、Detweiler 提出構想：重力波背景會在脈衝星到達時間中留下奈秒級的相關擾動。**脈衝星計時陣列**（Pulsar Timing Array, PTA）概念誕生——用整個銀河系的脈衝星組成一台「銀河系尺寸」的重力波偵測器。
- **方案**：NANOGrav（北美）、EPTA（歐洲）、PPTA（澳洲）各自長期計時數十顆毫秒脈衝星。難題：單顆脈衝星到達時間的雜訊（時鐘誤差、行星曆表誤差、星際介質色散）都在百奈秒量級，與訊號同量級——必須用多星**空間相關性**分辨訊號與雜訊。

## 線索與推理 -- 數學式、程式、理論

### 線索一：PTA 原理——重力波如何擾動計時
重力波（應變 $h$）經過地球與脈衝星之間時，會拉伸/壓縮此段的時空，改變光的傳播時間。到達時間殘差（timing residual）：

$$
\delta t(t) = \int_0^{L}\frac{1}{2}\hat{p}^i \hat{p}^j h_{ij}(t, \mathbf{x})\, dl
$$

其中 $\hat{p}$ 為脈衝星方向單位向量。對平面波，積分結果包含「地球項」（Earth term，所有脈衝星共有的擾動，源自波經過地球時）與「脈衝星項」（pulsar term，各星不同）：

$$
\delta t_a(t) = F_a^+ h_+(t - L_a(1-\hat{p}\cdot\hat{k})) + F_a^\times h_\times(\cdots)
$$

PTA 的關鍵：**地球項在所有脈衝星間是相關的**，而各種雜訊是不相關的。這就是空間相關性的「指紋」。

### 線索二：Hellings–Downs 相關曲線
1983 年 Hellings 與 Downs 計算出：各向同性、張量（廣義相對論）重力波背景下，兩顆脈衝星角距離 $\theta$ 的歸一化相關係數：

$$
\Gamma(\theta) = \frac{1}{2} + \frac{3}{2} x \ln\!\left(\frac{1-x}{2}\right) - \frac{x}{4} + \frac{1}{2}\delta_{ab},\qquad x = \frac{1-\cos\theta}{2}
$$

特徵：$\theta = 0$ 時相關為 1；隨角度增大而下降，在約 90° 時轉為負值；反向（$\theta = 180°$）時相關約 0.25。這條「駝峰曲線」就是 PTA 偵測的標的——2023 年 NANOGrav 觀測到的跨星相關性與此曲線在 $3$–$4\sigma$ 水平上吻合。

### 線索三：奈赫茲 vs 百赫茲——頻譜的另一端
| 偵測器 | 頻段 | 對應週期 | 主要來源 |
|---|---|---|---|
| LIGO | $10$–$10^3$ Hz | 毫秒–秒 | 恆星級黑洞/中子星合併 |
| LISA（2030s） | $10^{-4}$–$10^{-1}$ Hz | 秒–小時 | 白矮星雙星、中等質量黑洞 |
| **PTA（NANOGrav）** | $10^{-9}$–$10^{-7}$ Hz | **年–十年** | **超大型黑洞雙星** |

nHz 重力波對應波長以**光年**計——數年的觀測才能取樣一個週期。NANOGrav 的 15 年數據正是能解析 nHz 訊號的關鍵。

### 理論：超大型黑洞雙星的宇宙合唱
星系合併時，中央超大型黑洞（SMBH）也會合併成雙星。雙星在軌道上以 $f_{\rm GW} = 2 f_{\rm orb}$ 輻射重力波。宇宙中無數此類雙星疊加，形成各向同性背景。由 Phinney (2001) 的理論，能量密度參數：

$$
\Omega_{\rm GW}(f) = \frac{2\pi^2}{3H_0^2} f^2 h_c^2(f),\qquad h_c(f) = A\left(\frac{f}{f_{\rm ref}}\right)^{\alpha}
$$

對由引力波驅動的圓軌道 SMBH 雙星族群，譜指數 $\alpha = -2/3$：

$$
h_c(f) \propto f^{-2/3},\qquad \Omega_{\rm GW}(f) \propto f^{2/3}
$$

NANOGrav 15 年數據擬合結果：$A_{\rm GNB} = 6.4^{+4.2}_{-2.7}\times 10^{-15}$（參考頻率 $f_{\rm ref} = 1\ \text{yr}^{-1} \approx 32$ nHz）、$\alpha = -2/3$（在誤差內與理論一致）。換算能量密度 $\Omega_{\rm GW} \sim 10^{-8}$——宇宙能量密度中約億分之一由重力波背景貢獻。

### Python 模擬：Hellings–Downs 曲線與應變譜

```python
import numpy as np
import matplotlib.pyplot as plt

# (1) Hellings–Downs 相關曲線（理論 vs NANOGrav 觀測示意）
def hellings_downs(theta, ab=False):
    x = (1 - np.cos(theta)) / 2
    g = 0.5 + 1.5*x*np.log((1-x)/2) - x/4
    return g + (0.5 if ab else 0)     # 同一顆星時 +1/2

theta = np.linspace(1e-3, np.pi, 300)
rng = np.random.default_rng(2)
# 模擬 NANOGrav 15yr 的觀測相關點（15 顆脈衝星的星對）
t_obs = np.random.uniform(0.05, np.pi, 25)
y_obs = hellings_downs(t_obs) + rng.normal(0, 0.15, len(t_obs))

fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
ax[0].plot(np.degrees(theta), hellings_downs(theta), 'b-',
           label='Hellings–Downs (GR)')
ax[0].plot(np.degrees(t_obs), y_obs, 'ro', ms=4, label='NANOGrav 15yr (sim)')
ax[0].set_xlabel('angular separation [deg]')
ax[0].set_ylabel('correlation $\\Gamma(\\theta)$')
ax[0].axhline(0, color='gray', lw=0.5)
ax[0].legend(); ax[0].set_title('Spatial correlation fingerprint')

# (2) 特徵應變譜 h_c ∝ f^(-2/3)
f = np.logspace(-10, -7, 100)          # Hz (0.01 ~ 100 nHz)
A = 6.4e-15
f_ref = 1 / (3.156e7)                   # 1/yr ≈ 32 nHz
hc = A * (f / f_ref)**(-2/3)

ax[1].loglog(f, hc, 'b-', label='SMBHB theory: $h_c \\propto f^{-2/3}$')
# NANOGrav 15yr 觀測頻段與擬合值示意
f_nano = np.logspace(-9.3, -7.4, 8)
ax[1].loglog(f_nano, A*(f_nano/f_ref)**(-2/3) * (1 + rng.normal(0, 0.15, 8)),
             'ro', ms=5, label='NANOGrav 15yr (sim)')
ax[1].axvspan(1e-9, 1e-7, alpha=0.1, color='orange')
ax[1].set_xlabel('$f$ [Hz]'); ax[1].set_ylabel('$h_c(f)$')
ax[1].set_title('Gravitational-wave background spectrum')
ax[1].legend()
plt.tight_layout(); plt.show()
```

輸出顯示：左圖為 Hellings–Downs「駝峰曲線」與觀測點的吻合；右圖為 $h_c \propto f^{-2/3}$ 的特徵譜與 NANOGrav 15 年數據——這條冪律就是超大型黑洞雙星「合唱」的簽名。

## 結案 -- 後果與影響
- **2023 年 6 月 28 日**：NANOGrav（*ApJL* 951, L8）、EPTA+InPTA（*A&A*）、PPTA+DR3、中國 FAST（CPTA, *RAA*）在全球同步公布重力波背景證據。NANOGrav 達 $3$–$4\sigma$；FAST 以單望遠鏡在更短時間（3 年數據）看到同量級訊號。
- **2024–2025**：各合作組織持續累積數據，Hellings–Downs 空間相關的顯著性持續提升；開始嘗試分辨「連續波源」（單一超大型黑洞雙星）與背景。
- **深遠影響**：
  - 打開了「奈赫茲重力波天文學」——唯一能直接探測超大型黑洞雙星（$10^8$–$10^{10}\ M_\odot$）的頻段，直接檢驗星系演化與 SMBH 成長理論。
  - 也可能是其他來源：宇宙弦、原初重力波、相變等——譜指數 $\alpha$ 的精確測量將區分候選來源。
  - 重力波頻譜全覆蓋藍圖：LIGO（kHz）＋LISA（mHz, 2030s 發射）＋PTA（nHz）＋未來的 SKA（靈敏度更高）——多重頻段的 SGWB 測量將構成完整的「重力波宇宙學」。
  - 2023 年被譽為「重力波背景元年」——如同 2015 之於 GW150914。

## 關鍵人物與文獻
- **Ronald Hellings & George Downs**：1983 年計算空間相關曲線的先驅。
- **Bernard Schutz / Lee Samuel Finn**：PTA 概念的理論奠基者之一；**Don Backer**：毫秒脈衝星計時的推動者。
- **E. S. Phinney**：2001 年 $h_c \propto f^{-2/3}$ 譜的理論推導。
- 文獻：
  - Hellings & Downs, *ApJ* **265**, L39 (1983) —— 空間相關曲線。
  - Phinney, arXiv:astro-ph/0108028 (2001) —— SGWB 譜理論。
  - NANOGrav Collaboration, *ApJL* **951**, L8–L11 (2023) —— 15 年數據系列論文。
  - EPTA Collaboration, *A&A* **678**, A50 (2023)；Xu et al. (CPTA/FAST), *RAA* **23**, 075024 (2023)。
