# 1809 - Gauss 常態誤差理論

## 案件摘要

1809 年，Carl Friedrich Gauss 出版天體力學巨著《Theoria motus corporum coelestium in sectionibus conicis solem ambientium》，在處理小行星 Ceres 軌道估計時，首次系統地提出「觀測誤差服從常態分佈」的理論，並以最大概似原則推出最小平方法。從此，「鐘形曲線」獲得了嚴謹的數學與機率基礎。

## 前因 -- 為什麼會有這個案子

1801 年元旦，天文學家 Piazzi 發現小行星 Ceres，觀測 40 天後因太陽遮擋而失去蹤影。僅憑短弧段的含誤差觀測預測其再現位置，是當時公認不可能的難題。

24 歲的 Gauss 用新的軌道計算方法成功預測 Ceres 位置（1801 年底被觀測證實），一舉成名。但這引出更深層的偵探疑問：

> 觀測有誤差，憑什麼「最小平方法」是最好的估計法？誤差的「自然律」究竟是什麼？

前人的線索：

1. **de Moivre**（1733）：在二項分佈 $n \to \infty$ 的極限中已導出鐘形曲線 $\exp(-x^2/2)$ 作為近似。
2. **Laplace**（1780s）：研究誤差理論，但偏好的誤差分佈不夠優美。
3. **Legendre**（1805）：已發表最小平方法，但只有「平方和最小」的計算原則，沒有機率辯護。
4. Simpson（1755）等人嘗試過各種誤差分佈（三角形、二次曲線形），但都缺乏原理性根據。

Gauss 的破案策略反其道而行：**先假設一個誤差分佈，再由估計的最優性反推分佈的形狀**。

## 線索與推理 -- 數學式、程式、理論

### Gauss 的反推推理

Gauss 設誤差密度為 $\phi(x)$，採用「最大概似」原則：給定觀測 $x_1, \dots, x_n$，選擇位置參數使

$$L(\theta) = \prod_{i=1}^{n} \phi(x_i - \theta) \quad \text{最大}$$

Gauss 要求此原則對**任何樣本**都給出算術平均 $\bar{x}$ 作為估計（他認為平均是「自然」的估計量）。在這個約束下，唯一滿足條件的密度函數是：

$$\boxed{f(x) = \frac{1}{\sigma\sqrt{2\pi}}\; e^{-\frac{(x-\mu)^2}{2\sigma^2}}}$$

證明梗概：令 $g = \ln \phi$，最大概似條件為 $\sum g'(x_i - \theta) = 0$；取 $\theta = \bar{x}$ 時恆成立，意味 $g'(x)/x$ 必為常數 $c$，故 $g(x) = \frac{c}{2}x^2 + b$，即 $\phi$ 為指數二次型。再由 $\int \phi = 1$ 與 $\sigma^2 = \int x^2\phi(x)dx$ 定出常數，得 $c = -1/\sigma^2$。

### 誤差理論

Gauss 的完整體系：

1. **誤差分佈**：觀測誤差 $\varepsilon \sim N(0, \sigma^2)$，$\sigma$ 稱為「平均誤差」的尺度參數。
2. **最小平方 = 最大概似**：常態誤差下，
$$\max_\beta \prod_i \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{(y_i - X_i\beta)^2}{2\sigma^2}} \iff \min_\beta \sum_i (y_i - X_i\beta)^2$$
   Legendre 的計算原則獲得了機率基礎。
3. **精確度**：Gauss 用 $\sigma/\sqrt{n}$ 估計平均的不確定度——標準誤的先聲。

### 高斯–馬可夫定理的先聲

Gauss 在 1821–23 年《Theoria combinationis》中進一步證明：**不需要常態假設**，只要誤差期望為 0 且同變異數，最小平方估計式就在線性無偏估計中變異數最小（BLUE）。Markov 1912 年重新發現，合稱高斯–馬可夫定理：

$$\operatorname{Var}(\hat{\beta}_{OLS}) = \sigma^2 (X^TX)^{-1} \le \operatorname{Var}(\tilde{\beta}) \quad \text{對一切線性無偏 } \tilde{\beta}$$

### 命名的由來

- 「**Gauss 分佈**」：德、法、俄等歐陸傳統的稱呼，紀念 Gauss 1809 年的誤差理論。
- 「**常態分佈**（Normal distribution）」：由 Peirce（1872）、Galton（1889）推廣，Pearson 定型——因為它在「誤差的世界」中無所不在，是「常態」。
- 「**誤差定律**（error law）」：19 世紀的通用稱呼，直接反映其出身。
- 「**鐘形曲線**」：幾何形容。de Moivre 1733 年的曲線最終以 Gauss 之名流傳，也曾被稱為 Laplace–Gauss 分佈。

### Python：常態分佈與誤差模擬

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# ---- 1. 畫出常態分佈 ----
x = np.linspace(-4, 4, 400)
plt.figure(figsize=(12, 4))
for s in [0.5, 1.0, 2.0]:
    plt.plot(x, stats.norm.pdf(x, 0, s), label=f"N(0, {s}²)")
plt.legend(); plt.title("常態分佈：σ 越大越分散"); plt.xlabel("誤差 ε")
plt.ylabel("機率密度"); plt.show()

# ---- 2. 誤差模擬：重複測量一個定值 ----
rng = np.random.default_rng(0)
truth, sigma = 10.0, 2.0
meas = rng.normal(truth, sigma, 10000)      # 10000 次含誤差測量

plt.hist(meas, bins=60, density=True, alpha=0.6, label="測量誤差直方圖")
plt.plot(x * sigma + truth, stats.norm.pdf(x, truth, sigma), 'r-',
         lw=2, label=f"理論 N({truth}, {sigma}²)")
plt.legend(); plt.show()

# ---- 3. 標準誤：平均比單次測量精確 √n 倍 ----
n = 100
means = meas.reshape(-1, n).mean(axis=1)
print(f"單次測量標準差 = {meas.std():.3f}")
print(f"100 次平均的標準差 = {means.std():.3f} ≈ σ/√n = {sigma/np.sqrt(n):.3f}")

# ---- 4. 驗證「常態誤差下 OLS = MLE」----
t = np.linspace(0, 5, 50)
y = 1 + 2 * t + rng.normal(0, 1, 50)
X = np.column_stack([np.ones_like(t), t])
print(f"OLS 估計: {np.linalg.solve(X.T @ X, X.T @ y)}")  # 與 MLE 相同
```

## 結案 -- 後果與影響

1. **統計學的機率化**：誤差理論讓「資料 + 機率模型 + 估計」的現代統計框架成形，最大概似法（Fisher 1912 正式化）的雛形就在此。
2. **最小平方法的普遍化**：常態誤差假設使最小平方法成為 19 世紀觀測科學（天文、測地、物理）的標準工具。
3. **常態分佈的帝國擴張**：Quetelet（1835）把誤差定律應用到人的身高與犯罪率，開啟社會統計；Galton（1889）用於遺傳迴歸；1900 年 Pearson 的卡方檢定——常態分佈從「誤差定律」變成「自然界的常態」。
4. **Ceres 案的後續**：Gauss 的軌道方法與誤差理論都寫入 1809 年著作，奠定了數理天文學與統計估計的雙重基礎。

## 關鍵人物與文獻

- **Carl Friedrich Gauss**（1777–1855）：「數學王子」，哥廷根天文台台長。
  - Gauss, C. F. (1809). *Theoria motus corporum coelestium in sectionibus conicis solem ambientium*. Hamburg.
  - Gauss, C. F. (1821–23). *Theoria combinationis observationum erroribus minimis obnoxiae*.
- **Abraham de Moivre**（1667–1754）：1733 年首導鐘形曲線（二項極限）。
- **Pierre-Simon Laplace**（1749–1827）：1810 年以中央極限定理證明誤差常態性。
- **Adrien-Marie Legendre**（1752–1833）：1805 年最小平方法的公開發表者，與 Gauss 有優先權之爭。
- **Adrien Quetelet**（1796–1874）：將誤差定律推廣至社會現象。
