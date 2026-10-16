# 1900 - Planck 量子假說

## 案件摘要
1900 年 12 月 14 日，Planck 在德國物理學會報告中提出能量量子化假說 $E = h\nu$，以一個「絕望之舉」破解了黑體輻射的紫外災難。這一天被視為量子力學的誕生日。

## 前因 -- 為什麼會有這個案子
19 世紀末，黑體輻射譜已有精確測量，但理論完全跟不上：

- **Kirchhoff（1859）** 提出黑體定義與「輻射譜只與溫度有關」的挑戰性問題。
- **Wien（1896）** 由熱力學給出半經驗公式，在高頻段吻合、低頻段失準。
- **Rayleigh–Jeans（1900/1905）** 由經典統計力學導出公式，低頻正確、高頻發散——即所謂**紫外災難（ultraviolet catastrophe）**。

經典物理在「低頻」與「高頻」各自對了一半，整體卻錯得離譜——這是本案最大的懸念。

## 線索與推理 -- 數學式、程式、理論

### 線索一：Rayleigh–Jeans 公式與紫外災難
把空腔電磁波視為駐波模式（每個模式自由度均分 $kT$ 能量），每單位體積單位頻率的能量密度為

$$
u_\nu^{RJ}(T) = \frac{8\pi \nu^2}{c^3}\, kT
$$

問題：$\nu \to \infty$ 時 $u_\nu \to \infty$。積分總能量 $\int_0^\infty u_\nu\, d\nu = \infty$——物理上荒謬：打開烤箱就會被無限紫外線照射。

### 線索二：Wien 公式
Wien 由熱力學 + 假設「輻射像理想氣體分子」得到

$$
u_\nu^{W}(T) = a\, \nu^3\, e^{-b\nu/T}
$$

高頻段與實驗吻合，但低頻段偏離：當 $\nu \to 0$ 時 $u_\nu^W \to 0$ 太快，實驗顯示應 $\propto \nu^2 T$。

### 推理一：Planck 的內插
Planck 的策略是「數學插值」：在 RJ 的 $\nu^2 T$ 行為與 Wien 的高頻行為之間取折衷。他猜測能量密度的另一種形式：

$$
u_\nu(T) = \frac{8\pi h \nu^3}{c^3}\, \frac{1}{e^{h\nu/kT} - 1}
$$

檢查極限：
- $\nu \to 0$（$h\nu \ll kT$）：$e^{h\nu/kT}-1 \approx h\nu/kT$，得 $u \approx \frac{8\pi \nu^2}{c^3} kT$，正是 Rayleigh–Jeans！
- $\nu \to \infty$（$h\nu \gg kT$）：$u \approx \frac{8\pi h\nu^3}{c^3} e^{-h\nu/kT}$，正是 Wien（$a = 8\pi h/c^3$，$b = h/k$）！

對應黑體光譜輻射亮度（單位面積單位立體角）：

$$
B_\nu(T) = \frac{2h\nu^3}{c^2}\, \frac{1}{e^{h\nu/kT} - 1}
$$

### 推理二：物理意義——能量量子化
為了「推導」而非「湊出」上式，Planck 假設腔壁振子（ oscillator）的能量只能取離散值：

$$
E_n = n h \nu, \quad n = 0, 1, 2, \dots
$$

並用 Boltzmann 統計計算平均能量（取代連續的 $kT$）：

$$
\bar{E} = \frac{\sum_n n h\nu\, e^{-n h\nu/kT}}{\sum_n e^{-n h\nu/kT}}
= \frac{h\nu}{e^{h\nu/kT} - 1}
$$

推導：令 $x = e^{-h\nu/kT}$，分子 $= h\nu \sum n x^n = h\nu \frac{x}{(1-x)^2}$，分母 $= \frac{1}{1-x}$，相除即得。這一步讓 $\nu$ 大的模式因 $h\nu \gg kT$ 而「凍結」，總能量積分收斂——紫外災難消失。

Planck 當時視量子化為數學手段，自己也說是「絕望之舉」（an act of desperation）——他不知道自己開啟了一場物理革命。

### 程式驗證：三條曲線比較

```python
import numpy as np
import matplotlib.pyplot as plt

h, c, k = 6.626e-34, 3.0e8, 1.381e-23
T = 5000  # K
nu = np.linspace(1e12, 2e15, 1000)

u_planck = (8*np.pi*h*nu**3/c**3) / (np.exp(h*nu/k/T) - 1)
u_rj     = 8*np.pi*nu**2/c**3 * k*T
u_wien   = (8*np.pi*h*nu**3/c**3) * np.exp(-h*nu/k/T)

plt.figure(figsize=(8,5))
plt.plot(nu*1e-14, u_planck, label='Planck (correct)', lw=2)
plt.plot(nu*1e-14, u_rj, '--', label='Rayleigh-Jeans (UV catastrophe)')
plt.plot(nu*1e-14, u_wien, ':', label='Wien (fails at low freq)')
plt.xlim(0, 200); plt.ylim(0, 6e-19)
plt.xlabel(r'$\nu$ ($10^{14}$ Hz)'); plt.ylabel(r'$u_\nu$ (J/m$^3$/Hz)')
plt.title('Blackbody radiation at T = 5000 K')
plt.legend(); plt.show()
```

執行結果：Rayleigh–Jeans 曲線在高頻暴衝（紫外災難），Wien 在低頻貼地，只有 Planck 曲線與實驗（例如 5000 K 約對應太陽表面）完全吻合。峰值由 Wien 位移定律 $\lambda_{max} T = 2.898\times 10^{-3}\,\text{m·K}$ 給出。

## 結案 -- 後果與影響
- 紫外災難結案，但引出新案：量子化的物理根源是什麼？
- 1905 年 Einstein 把 $h\nu$ 實體化為「光量子」（→ 光電效應案）。
- 1913 年 Bohr 用量子化解釋氫原子光譜（→ Bohr 模型案）。
- 1924 年 Bose 推導 Planck 定律開啟量子統計（Bose–Einstein 統計）。
- $h = 6.626\times 10^{-34}\,\text{J·s}$ 成為宇宙的基本常數，2019 年起 $h$ 被定為精確值、用於定義公斤。

## 關鍵人物與文獻
- **Max Planck**：Verhandlungen der Deutschen Physikalischen Gesellschaft 2, 237 (1900)；諾貝爾獎 1918。
- **Lord Rayleigh**：Phil. Mag. 49, 539 (1900)；**J. Jeans**：補正因子。
- **W. Wien**：Wied. Ann. 58, 662 (1896)；諾貝爾獎 1911。
