# 1718/1733 - De Moivre：常態曲線的誕生

## 案件摘要
1718 年 Abraham de Moivre 出版《The Doctrine of Chances》，系統化擲骰機率計算；1733 年他在一篇拉丁文論文中，為了逼近 $n$ 很大的二項分佈，導出了史上第一條常態曲線。$e^{-x^2/2}$ 從賭博問題的輔助工具，最終成為統計學之王。

## 前因 -- 為什麼會有這個案子
Bernoulli 1713 年證明了大數法則，但只說「頻率會收斂到機率」，沒有回答**收斂的速度與誤差的形狀**。賭徒與天文學家都迫切需要答案：

- 賭徒：$n$ 次賭局中淨贏多少的機率分佈長什麼樣？
- 天文學家：多次觀測星體位置的誤差該如何合成？（「誤差曲線」問題）

De Moivre 是流亡倫敦的法國胡格諾派新教徒，靠當家教與算命顧問維生（他晚年以「死亡日期預測」聞名——他自己算出的日子竟奇準）。他與 Newton、Halley 交好，Newton 曾說：「想問數學問題，去找 de Moivre，他比我懂。」1711 年他發表《De Mensura Sortis》，1718 年擴充為《The Doctrine of Chances》。

**核心難題**：二項分佈 $P(X=k) = \binom{n}{k}p^kq^{n-k}$ 當 $n$ 很大時無法直接計算——$\binom{n}{k}$ 與 $n!$ 都爆炸性地大。需要一個近似公式。

## 線索與推理 -- 數學式、程式、理論

### Stirling 公式的角色

De Moivre 在計算過程中卡在 $n!$ 的漸近行為。他求助於友人 Stirling（也與他獨立推導），得到**Stirling 公式**：

$$n! \approx \sqrt{2\pi n}\,\left(\frac{n}{e}\right)^n$$

有趣的是，公式中的常數 $\sqrt{2\pi}$ 正是 de Moivre 與 Stirling 一起確定的。這個 $\sqrt{2\pi}$ 後來成為常態分佈密度中的歸一化常數——**常態曲線的核心常數誕生於階乘的近似**。

### 二項分佈的常態近似

De Moivre 取 $p = 1/2$（公平硬幣），把 $\binom{n}{k}$ 用 Stirling 公式展開，得到：

$$P(X = k) \approx \frac{1}{\sqrt{2\pi \cdot n/4}} \exp\!\left(-\frac{(k - n/2)^2}{2 \cdot n/4}\right)$$

令 $z = \dfrac{k - n/2}{\sqrt{n}/2}$（標準化：減均值、除標準差），則：

$$P(X = k) \approx \frac{1}{\sqrt{n}/2}\,\phi(z), \qquad \phi(z) = \frac{1}{\sqrt{2\pi}}\,e^{-z^2/2}$$

$\phi(z)$ 正是**標準常態密度函數**。De Moivre 在 1733 年 11 月 12 日的拉丁文論文《Approximatio ad Summam Terminorum Binomii $(a+b)^n$ in Seriem Expansi》中發表此結果，並親手計算了 $\phi(z)$ 從 $z=0$ 到 $z=3$ 的積分值表——史上第一張常態曲線面積表。

用現代語言，這就是**de Moivre–Laplace 定理**（中心極限定理的特例）：

$$\frac{X - np}{\sqrt{npq}} \;\xrightarrow{\ d\ }\; N(0, 1)$$

### 一般二項（$p \ne 1/2$）與誤差曲線

De Moivre 主要處理 $p=1/2$；Laplace 在 1810 年將結果推廣到一般 $p$，並在 1812 年《機率的解析理論》中證明完整的**中心極限定理**：獨立同分佈變數之和（無論原分佈如何）標準化後趨近常態：

$$\frac{\bar{X}_n - \mu}{\sigma/\sqrt{n}} \;\xrightarrow{\ d\ }\; N(0,1)$$

天文學家 Gauss 在 1809 年以「誤差分佈應使均值成為最可能估計」為公理，獨立導出常態誤差曲線，並發展出**最小平方法**——「Gaussian 曲線」之名由此而來（De Moivre 的優先權一度被遺忘，Karl Pearson 在 1924 年為其正名）。

### Python 畫出二項 vs 常態近似曲線

```python
import math
import matplotlib.pyplot as plt
from collections import Counter
import random

n, p = 50, 0.5
q = 1 - p

# 精確二項機率
def binom(k):
    return math.comb(n, k) * p**k * q**(n-k)

ks = range(n + 1)
exact = [binom(k) for k in ks]

# De Moivre 常態近似
mu, sigma = n * p, math.sqrt(n * p * q)
approx = [math.exp(-((k - mu)**2) / (2 * sigma**2)) / (sigma * math.sqrt(2*math.pi))
          for k in ks]

plt.figure(figsize=(9, 5))
plt.bar(ks, exact, width=0.8, alpha=0.6, label="Binomial(n=50, p=0.5)")
plt.plot(ks, approx, "r-", lw=2, label="De Moivre normal approx")
plt.legend(); plt.xlabel("k"); plt.ylabel("P(X=k)")
plt.title("De Moivre's 1733 discovery: binomial -> normal")
plt.savefig("binom_normal.png", dpi=120)

# Monte Carlo 驗證：擲 50 次硬幣的重複實驗
random.seed(0)
counts = Counter(sum(random.random() < p for _ in range(n)) for _ in range(100_000))
sim = [counts[k] / 100_000 for k in ks]
mse = sum((s - e)**2 for s, e in zip(sim, exact)) / len(ks)
print("模擬 vs 精確二項的 MSE ≈", mse)    # 極小，驗證模擬正確
```

模擬的頻率分佈會緊貼二項機率，而二項機率又緊貼紅色的常態曲線——三層貼合正是 De Moivre 定理的可視化。

## 結案 -- 後果與影響
常態曲線從 De Moivre 的賭桌輔助計算出發，經 Gauss 的誤差理論（1809）成為天文測量的標準，經 Laplace 的中心極限定理（1810–1812）成為一切求和現象的通則，最終在 19 世紀經 Quetelet（「平均人」）與 Galton（迴歸與相關）滲透進社會科學與生物統計。20 世紀的統計推論——置信區間、t 檢定、卡方檢定——全部建立在小樣本常態理論之上。Karl Pearson 的評語最為傳神：「De Moivre 在 1733 年那篇論文，是統計學史上最重要的一天。」

## 關鍵人物與文獻
- **Abraham de Moivre**（1667–1754）：法裔英國數學家，de Moivre 定式 $(\cos\theta + i\sin\theta)^n$ 亦以其為名。
- **James Stirling**（1692–1770）：蘇格蘭數學家，Stirling 公式發表者（1730）。
- **Pierre-Simon Laplace**（1749–1827）：推廣至一般二項並證明中心極限定理。
- **Carl Friedrich Gauss**（1777–1855）：最小平方法與常態誤差理論。
- 文獻：A. de Moivre, *The Doctrine of Chances*（1718, 2nd ed. 1738, 3rd ed. 1756）；*Approximatio...*（1733, Latin pamphlet）。
