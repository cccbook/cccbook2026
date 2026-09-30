# 1713 - Bernoulli 出版《猜度術》與大數法則

## 案件摘要
1713 年，Jacob Bernoulli 逝世八年後，其遺作《Ars Conjectandi》（猜度術）出版。書中首次以數學證明「頻率趨近機率」——弱大數法則，讓機率從賭桌上的計算升格為可以描述大自然的定律，也埋下頻率學派與貝葉斯學派百年論戰的源頭。

## 前因 -- 為什麼會有這個案子
Huygens 1657 年的教科書回答了「賭局如何計算」，但只處理**已知機率的等可能事件**。真正的大問題是：大自然的機率——例如一個人死於某年齡的機率、一枚鑄造不均的硬幣出現正面的機率——**事先並不知道，只能靠觀察**。

那麼關鍵問題來了：

> 觀察到的頻率，憑什麼可以告訴我們那個未知的機率？

Graunt 1662 年憑經驗做了「從部分推全體」，但沒有證明。Jacob Bernoulli 從 1680 年代開始撰寫《Ars Conjectandi》，耗費近 20 年，臨終（1705）仍未完成。他在書中說道：「即使最愚笨的人，憑天生的本能也知道觀察越多，離真相越近。但**用數學證明這一點**，卻不是容易的事。」他稱之為「golden theorem」（黃金定理）。

## 線索與推理 -- 數學式、程式、理論

### Bernoulli 試驗與二項分佈

**Bernoulli 試驗**：單次試驗只有成功（機率 $p$）與失敗（機率 $q=1-p$）兩種結果。獨立重複 $n$ 次，成功次數 $X$ 服從**二項分佈**：

$$P(X = k) = \binom{n}{k} p^k q^{n-k}, \qquad \binom{n}{k} = \frac{n!}{k!\,(n-k)!}$$

樣本頻率 $\bar{X}_n = X/n$，期望值與變異數：

$$E[\bar{X}_n] = p, \qquad \mathrm{Var}(\bar{X}_n) = \frac{pq}{n}$$

變異數隨 $n$ 增大而縮小——這正是「頻率會穩定下來」的數學根源。

### 黃金定理：弱大數法則

Bernoulli 的證明策略：對任意 $\varepsilon > 0$，用二項分佈的尾部機率直接估計 $P(|\bar{X}_n - p| \ge \varepsilon)$，並證明它趨近 0。現代表述（弱大數法則）：

$$P\!\left(|\bar{X}_n - p| < \varepsilon\right) \longrightarrow 1 \quad \text{當 } n \to \infty$$

Bernoulli 證明所用的核心估計（以現代記號簡化）：

$$P\!\left(|\bar{X}_n - p| \ge \varepsilon\right) \le 2\exp\!\left(-\,2n\varepsilon^2\right)$$

（此為後世 Hoeffding 不等式的形式；Bernoulli 原版估計較弱但精神相同。）由變異數也可用 Chebyshev 不等式得到：

$$P\!\left(|\bar{X}_n - p| \ge \varepsilon\right) \le \frac{pq}{n\varepsilon^2} \le \frac{1}{4n\varepsilon^2} \to 0$$

### Bernoulli 的驚人數值結論

Bernoulli 用自己的定理算出一個發人深省的例子：要使「頻率落在真機率的 $\frac{1}{1000}$ 範圍內」的機率達到 $\frac{1000}{1001}$ 以上，需要觀察次數 $n$ **高達數萬次**。他嘆道，這解釋了為什麼日常經驗中「頻率趨近機率」看似理所當然，數學上卻需要如此龐大的樣本——**收斂是必然的，但速度可以很慢**。

### 頻率學派 vs 貝葉斯學派的源頭

Bernoulli 的黃金定理確立了**頻率學派**的根基：機率的定義就是長期頻率的極限（von Mises 1919 年正式化），統計推論依靠重複抽樣。

但書中還有一段關鍵討論：Bernoulli 主張「**先驗地**（a priori，由對稱性算出）」與「**後驗地**（a posteriori，由觀察頻率估出）」兩種取得機率的方式並存。他甚至提出：觀察到「$n$ 次中成功 $k$ 次」後，可以反推未知 $p$ 的可能範圍——這正是**逆機率**（inverse probability）問題，Thomas Bayes（1763）與 Laplace（1774）將其發展成貝葉斯定理：

$$P(p \mid k \text{ 次成功}) \propto P(k \text{ 次成功} \mid p)\, \pi(p)$$

一場持續三百年的學派之爭，源頭就在《Ars Conjectandi》的這兩頁。

### Python Monte Carlo 模擬擲硬幣驗證大數法則

```python
import random
import statistics

random.seed(42)
p_true = 0.5

# 樣本數從 1 到 100000，記錄每次的累積頻率
n_list, freq_list = [], []
count = 0
for n in range(1, 100_001):
    if random.random() < p_true:
        count += 1
    if n in (1, 10, 100, 1000, 10000, 100000):
        n_list.append(n)
        freq_list.append(count / n)

for n, f in zip(n_list, freq_list):
    print(f"n = {n:>6}, 頻率 = {f:.4f}, 誤差 = {abs(f - p_true):.4f}")

# 收斂誤差應隨 n 縮小，量級約 ~ 1/sqrt(n)（符合二項變異數 pq/n）
# 重複模擬多次可估計 P(|X̄_n - p| < ε) 是否趨近 1
eps = 0.01
trials = 500
hit = 0
for _ in range(trials):
    c = sum(random.random() < p_true for _ in range(10_000))
    hit += abs(c / 10_000 - p_true) < eps
print(f"P(|X̄_10000 - 0.5| < 0.01) ≈ {hit/trials:.3f}")   # ≈ 0.95
```

## 結案 -- 後果與影響
《Ars Conjectandi》全書四部分：重刊並註解 Huygens 的 14 命題、系統化排列組合與二項係數、證明黃金定理、以及把機率應用於政治、法律與道德的「社會數學」藍圖。大數法則成為保險業、抽樣調查與實驗科學的理論基石；弱大數法則後被 Khinchin、Kolmogorov 推廣到一般隨機變數；而「逆機率」的種子在 1763 年開花為貝葉斯定理。Bernoulli 家族三代（Jacob、Nicholas、Daniel）接力，讓機率論成為 18 世紀數學的主流。

## 關鍵人物與文獻
- **Jacob (Jakob) Bernoulli**（1655–1705）：巴塞爾大學數學教授，微積分先驅、變分法開創者。
- **Nicholas Bernoulli**（1687–1759）：Jacob 的姪子，整理出版遺作並完成部分未竟內容。
- **Thomas Bayes**（1701–1761）：逆機率與貝葉斯定理的發表者。
- 文獻：J. Bernoulli, *Ars Conjectandi*（1713, Basel）。
