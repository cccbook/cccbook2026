# 1763 - Bayes 定理

## 案件摘要

1763 年，牧師 Thomas Bayes 遺稿《An Essay towards Solving a Problem in the Doctrine of Chances》由友人 Richard Price 交給皇家學會並出版。這份遺稿解決了一個困擾機率學界多年的「逆向機率問題」——從觀察到的結果反推原因的機率，開啟了貝葉斯統計學派兩百多年的發展。

## 前因 -- 為什麼會有這個案子

18 世紀的機率論由 Pascal、Fermat、Huygens、Bernoulli、de Moivre 等人奠定，主要處理「正向問題」：已知機率模型，預測結果。例如已知骰子公平，求擲出 6 的機率。

但自然地會浮出反向的疑問：

> 擲球員 Bill 在桌上彈球，彈了幾次都落在某區間內，我們能反推他每次彈球的「落點機率」嗎？

這就是「從結果反推原因」的問題。de Moivre 在《The Doctrine of Chances》（1718）中未解決此問題；Bernoulli 的大數法則（1713）只告訴我們頻率會收斂到真實機率，卻沒告訴我們「已知頻率，真實機率的可信度如何」。Bayes 這位精算背景的長老會牧師在私下鑽研此題，1761 年去世後，遺稿落到 Price 手中——Price 出於宗教與哲學動機（反駁 Hume 對奇蹟的懷疑論）將其整理出版。

## 線索與推理 -- 數學式、程式、理論

### 核心定理

設 $H$ 為假設（原因），$D$ 為資料（結果），則：

$$P(H|D) = \frac{P(D|H)\,P(H)}{P(D)} = \frac{P(D|H)\,P(H)}{\sum_{H'} P(D|H')\,P(H')}$$

三個組成部分的偵探式解讀：

| 術語 | 符號 | 偵探角色 |
|------|------|----------|
| 先驗機率 | $P(H)$ | 開案前的「嫌疑程度」 |
| 概似度 | $P(D\|H)$ | 若嫌疑為真，看到這些「線索」的可能性 |
| 後驗機率 | $P(H\|D)$ | 看完線索後更新的嫌疑程度 |
| 證據 | $P(D)$ | 線索本身的整體出現機率（歸一化常數） |

### Bayes 的原始推理

Bayes 用一張「桌子」與連續丟球的幾何論證：球 $W$ 均勻落在長度 1 的桌面上，之後再丟 $n$ 顆球，設落在 $[0, x]$ 區間的有 $p$ 顆。他推得（現代記號）：

$$P\left(\frac{p}{n} \le x \;\middle|\; \text{觀察}\right) = \frac{(n+1)!}{p!\,(n-p-p)!}\int_0^x z^p (1-z)^{n-p}\, dz$$

這正是 Beta 分佈的累積機率——現代「Beta-Binomial 共軛」的先聲：

$$P(\theta \mid k) \propto \theta^{k}(1-\theta)^{n-k} \cdot \underbrace{\theta^{a-1}(1-\theta)^{b-1}}_{\text{先驗 Beta}(a,b)}$$

即先驗 $\text{Beta}(a,b)$ + 觀察 $(k, n-k)$ $\Rightarrow$ 後驗 $\text{Beta}(a+k,\; b+n-k)$。

### Laplace 的推廣

Laplace 獨立重新發現並大幅推廣了此定理（1774 年起）：

1. **逆向機率的通用解法**：對任意離散假設 $H_1, \dots, H_n$，
$$P(H_i \mid D) = \frac{P(D \mid H_i) P(H_i)}{\sum_j P(D \mid H_j) P(H_j)}$$
2. **「機率的因果論」（Principle of Insufficient Reason）**：無資訊時給各原因相同先驗（均勻先驗），用後驗比較原因。
3. 實際應用：估計法國男嬰出生比例（1781）、分析巴黎天文台的觀測誤差、推導最小平方法的機率基礎（1810）。

### 醫療檢測偽陽性問題（經典演示）

某疾病盛行率 1%，檢測靈敏度 99%（有病者陽性機率），偽陽性率 5%。檢測陽性，真的有病的機率是多少？

$$P(\text{病}\mid +) = \frac{0.99 \times 0.01}{0.99 \times 0.01 + 0.05 \times 0.99} = \frac{0.0099}{0.0594} \approx 0.1667$$

直覺答案 99% 大錯特錯——只有約 16.7%！因為健康人遠多於病人，偽陽性總數壓過真陽性。

### Python 演示：貝葉斯更新

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# ---- 1. 醫療檢測偽陽性 ----
P_disease, sens, fpr = 0.01, 0.99, 0.05
post = sens * P_disease / (sens * P_disease + fpr * (1 - P_disease))
print(f"P(有病 | 陽性) = {post:.4f}")   # 0.1667

# ---- 2. Beta-Binomial 連續更新：估計硬幣不公平程度 ----
a, b = 1.0, 1.0            # 均勻先驗 Beta(1,1)
data = [1,1,1,0,1,1,0,1,1,1]  # 10 次擲幹，8 次正面
theta = np.linspace(0, 1, 500)
plt.figure(figsize=(8, 4))
plt.plot(theta, stats.beta.pdf(theta, a, b), label="先驗 Beta(1,1)")
for n, k in [(2, 2), (5, 4), (10, 8)]:
    a2, b2 = a + k, b + (len(data) - k)
    plt.plot(theta, stats.beta.pdf(theta, a2, b2), label=f"後驗 Beta({a2:g},{b2:g})")
plt.legend(); plt.xlabel("正面機率 θ"); plt.ylabel("機率密度")
plt.title("貝葉斯更新：資料越多，後驗越集中"); plt.tight_layout()
plt.show()

# ---- 3. 蒙地卡羅驗證後驗均值 ----
a2, b2 = a + sum(data), b + (len(data) - sum(data))
print(f"後驗均值 = {a2/(a2+b2):.3f}")   # 0.75，接近樣本比例
```

## 結案 -- 後果與影響

1. **貝葉斯學派誕生**：Laplace、Gauss（部分）、Boole 等人用它解決估計問題；Laplace 更以「機率的因果論」讓貝葉斯方法成為 19 世紀科學估計的主流工具。
2. **百年之爭**：19 世紀末至 20 世紀中葉，頻率學派（Fisher、Neyman、Pearson）批判先驗機率的「主觀性」，認為機率只應是長期頻率；貝葉斯學派（Jeffreys、de Finetti、Savage）則主張機率是「信念的程度」。這場論戰主導了統計學的發展。
3. **現代復興**：MCMC（Markov Chain Monte Carlo，1990s）計算工具出現後，貝葉斯方法在機器學習、貝葉斯網路、貝葉斯深度學習、A/B 測試、司法鑑識、流行病學中大放異彩。
4. **哲學遺產**：Bayes 定理證明「學習」在數學上就是條件化——知識隨證據更新，成為認識論與 AI 的形式基礎。

## 關鍵人物與文獻

- **Thomas Bayes**（1701–1761）：長老會牧師、業餘數學家，皇家學會會員。
- **Richard Price**（1723–1791）：哲學家與統計學家，整理出版遺稿。
  - Bayes, T. (1763). *An Essay towards Solving a Problem in the Doctrine of Chances*. Phil. Trans. R. Soc. 53.
- **Pierre-Simon Laplace**（1749–1827）：獨立重現並推廣，寫入《Théorie analytique des probabilités》(1812)。
- 延伸閱讀：de Moivre《The Doctrine of Chances》(1718)、Jeffreys《Theory of Probability》(1939)、Jaynes《Probability Theory: The Logic of Science》(2003)。
