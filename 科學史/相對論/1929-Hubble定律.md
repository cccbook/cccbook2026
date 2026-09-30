# 1929-Hubble 定律

## 案件摘要
1929 年，Edwin Hubble 用造父變星測量星系距離，結合 Slipher 的紅移數據，發現星系遠離速度與距離成正比：$v = H_0 d$。
宇宙在膨脹——靜態宇宙的千年信仰就此崩塌，大爆炸宇宙學正式誕生。

## 前因 -- 為什麼會有這個案子
- 1912–1917 年，Vesto Slipher 測得大多數「星雲」都有**紅移**（光譜向長波偏移），但它們是什麼、多遠，無人知曉。
- 1920 年「宇宙大辯論（Shapley–Curtis Debate）」：星雲是銀河系內的雲氣，還是獨立的島宇宙？
- 1923 年 Hubble 在 M31（仙女座星系）中找到造父變星，證明 M31 在銀河系之外——島宇宙勝訴。
- 1922/1927 年 Friedmann 與 Lemaître 已從理論推得膨脹宇宙，但缺觀測證據。
- **線索疑點**：既然這些星系在退行，退行速度與距離之間有沒有規律？這是本案的核心謎題。

## 線索與推理 -- 數學式、程式、理論

### 1. 造父變星測距：標準燭光
Henrietta Leavitt (1908) 發現造父變星的**週光關係**：光變週期 $P$ 越長，絕對星等 $M$ 越亮：

$$M = a \log_{10} P + b$$

測得 $P$ → 得 $M$ → 比較視星等 $m$，用距離模數求距離：

$$m - M = 5\log_{10}\frac{d}{10\,\text{pc}} \quad\Rightarrow\quad d = 10^{(m-M+5)/5}\,\text{pc}$$

這是天文學的「量天尺」，Hubble 用它一步步量出星系的距離。

### 2. 星系紅移：都卜勒與宇宙學紅移
紅移定義：

$$z = \frac{\lambda_{obs} - \lambda_0}{\lambda_0} = \frac{\Delta\lambda}{\lambda_0}$$

- 小 $z$ 時用都卜勒公式：$v \approx cz$。
- 大 $z$ 需用宇宙學紅移：$1 + z = \frac{a(t_{obs})}{a(t_{emit})} = \frac{1}{a(t_{emit})}$（取 $a(t_{obs})=1$）。
  光被「膨脹的空間本身」拉長——這不是星系在空間中飛，而是空間自己在脹。

### 3. Hubble 定律
Hubble 疊加 Slipher 的速度數據與自己的距離數據（24 個星系，最遠僅約 2 Mpc），發現線性關係：

$$v = H_0 d$$

- 1929 年原始論文得 $H_0 \approx 500\,\text{km/s/Mpc}$——因造父變星校準錯誤（把 HII 區誤當亮星），大了約 7 倍。
- 現代值（Planck 2018）：$H_0 \approx 67.4\,\text{km/s/Mpc}$；局域測量（SH0ES）：$H_0 \approx 73\,\text{km/s/Mpc}$。通常記為 $H_0 \approx 70\,\text{km/s/Mpc}$。

### 4. Hubble 張力爭議（現代懸案）
- 早期宇宙推斷（Planck, CMB, $\Lambda$CDM）：$H_0 \approx 67.4$
- 晚期局域測量（SH0ES, 造父變星＋超新星）：$H_0 \approx 73.0$
- 兩者差約 8%，遠超誤差範圍（約 5σ）——是系統誤差還是新物理？至今未解，稱為「Hubble 張力」。

### 5. 宇宙年齡估計
對平坦塵埃宇宙 $a \propto t^{2/3}$，$\frac{\dot{a}}{a} = \frac{2}{3t} = H$，故：

$$t_0 \approx \frac{2}{3H_0} \approx \frac{1}{H_0}$$

取 $H_0 = 70\,\text{km/s/Mpc}$ 換算：

$$H_0 = \frac{70}{3.086\times 10^{19}}\,\text{s}^{-1} \approx 2.27\times 10^{-18}\,\text{s}^{-1}$$
$$t_0 \approx \frac{1}{H_0} \approx 4.4\times 10^{17}\,\text{s} \approx 140\ \text{億年}$$

（精確的 $\Lambda$CDM 模型給 $t_0 \approx 138$ 億年。）

### 6. Python 線性擬合紅移-距離數據

```python
import numpy as np
import matplotlib.pyplot as plt

# 模擬 Hubble 1929 風格的觀測數據 (H0 = 70 km/s/Mpc, 帶噪聲)
rng = np.random.default_rng(42)
H0_true = 70.0
d = np.linspace(0.5, 300, 30)                 # 距離 (Mpc)
z = H0_true * d / 299792.458                  # 小 z: z ≈ H0 d / c
z += rng.normal(0, 0.003, z.size)             # 觀測噪聲
v = z * 299792.458                            # 速度 (km/s)

# 線性最小平方擬合: v = H0 * d
A = np.vstack([d, np.zeros_like(d)]).T
H0_fit, _ = np.linalg.lstsq(np.vstack([d]).T, v, rcond=None)[0][[0]], None
# 簡潔寫法：
H0_fit = np.polyfit(d, v, 1)[0]

print(f"擬合 H0 = {H0_fit:.1f} km/s/Mpc (真值 {H0_true})")

plt.figure(figsize=(8,5))
plt.scatter(d, v, s=20, label='觀測數據 (模擬)')
dd = np.linspace(0, 320, 10)
plt.plot(dd, H0_fit*dd, 'r-', label=f'擬合: v = {H0_fit:.1f} d')
plt.xlabel('距離 d (Mpc)'); plt.ylabel('退行速度 v (km/s)')
plt.title('Hubble 定律: v = H0 d')
plt.legend(); plt.grid(alpha=0.3); plt.show()
```

擬合結果應接近 $70\ \text{km/s/Mpc}$——Hubble 的那條直線，就是宇宙膨脹的第一份「偵查報告」。

## 結案 -- 後果與影響
- **結案**：宇宙在膨脹。$v = H_0 d$ 之後，Friedmann/Lemaître 的數學解從「遊戲」升級為「描述真實宇宙的理論」。
- Einstein 1931 年訪問 Wilson 山天文台後，放棄靜態宇宙與 $\Lambda$（「最大錯誤」）。
- Lemaître 1931 年提出原始原子假說；Gamow 1948 年發展為熱大爆炸並預言 CMB。
- 宇宙年齡之謎：$H_0 \approx 500$ 曾給出「宇宙比地球還年輕」的荒謬結果（約 20 億年），校準修正後才化解——這是本案的一個插曲判决。
- 1998 年 Ia 型超新星觀測發現膨脹在加速，Hubble 定律只是「章節一」；$H_0$ 隨時間變化，記作 $H(t)$。

## 關鍵人物與文獻
| 人物 | 貢獻 |
|------|------|
| Henrietta Leavitt (1868–1921) | 1908 造父變星週光關係 |
| Vesto Slipher (1875–1969) | 1912–17 星系紅移 |
| Edwin Hubble (1889–1953) | 1923 島宇宙、1929 Hubble 定律 |
| Milton Humason (1891–1972) | 1930s 大紅移星系速度測量 |
| Georges Lemaître (1894–1966) | 1927 理論預言膨脹 |

**文獻**
- E. Hubble, "A relation between distance and radial velocity among extra-galactic nebulae" (1929), PNAS 15, 168.
- G. Lemaître (1927)——1998 年被重新翻譯後，學界承認其優先權。
- Planck Collaboration (2018), A&A 641, A6（現代 $H_0$ 值）。
- Riess et al., "Large Magellanic Cloud Cepheid Standards..." (2019)——SH0ES 與 Hubble 張力。
