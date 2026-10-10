# 1837 - Poisson 分佈

## 案件摘要

1837 年，Siméon Denis Poisson 在《Recherches sur la probabilité des jugements en matière criminelle et en matière civile》中發表了以他命名的分佈——描述「單位時間內稀有事件發生次數」的機率律。這個從司法判決機率研究意外誕生的分佈，成為現代排隊論、通訊工程與核物理的基石。

## 前因 -- 為什麼會有這個案子

Poisson 是 Laplace 的學生與繼承者，任教於巴黎綜合理工學院。1830 年代他的研究動機來自一個法國司法界的實際問題：

> 法國的刑事與民事陪審團判決有錯誤（冤枉無辜、放過有罪），如何用機率評估司法判決的可靠性，並建議陪審團人數與多數決門檻？

Laplace 在 1812 年《Théorie analytique》中已處理過此問題，用二項分佈分析陪審員「正確判決」的機率。Poisson 深入研究時發現：當陪審員人數多、個別錯判機率小時，二項分佈的計算有一個優美的極限——稀有事件的機率律。

同時期的線索：

1. **de Moivre–Laplace**：二項分佈的常態近似（$n$ 大、$p$ 不太小）。
2. 缺口：當 $n$ 大而 $p$ **很小**、$np$ 適中時（稀有事件），常態近似失效，需要新的極限分佈。
3. 大數法則（Bernoulli 1713）只處理頻率收斂，Poisson 將其推廣到更一般的情形。

## 線索與推理 -- 數學式、程式、理論

### Poisson 分佈的定義

$$\boxed{P(X = k) = \frac{\lambda^k e^{-\lambda}}{k!}, \qquad k = 0, 1, 2, \dots}$$

其中 $\lambda = np$ 為單位時間（或單位面積）內事件的平均發生次數。

$$E[X] = \lambda, \qquad \operatorname{Var}(X) = \lambda \quad (\text{期望 = 變異數，是 Poisson 的指紋})$$

### 二項分佈的極限（推導）

設二項分佈 $X \sim B(n, p)$，取 $n \to \infty$、$p \to 0$、$np \to \lambda$：

$$P(X = k) = \binom{n}{k} p^k (1-p)^{n-k} = \frac{n(n-1)\cdots(n-k+1)}{k!} \left(\frac{\lambda}{n}\right)^k \left(1 - \frac{\lambda}{n}\right)^{n} \left(1-\frac{\lambda}{n}\right)^{-k}$$

逐項取極限：

- $\frac{n(n-1)\cdots(n-k+1)}{n^k} \to 1$
- $\left(\frac{\lambda}{n}\right)^k$ 中 $n^k$ 消去 $\to \frac{\lambda^k}{1}$（配對後）
- $\left(1 - \frac{\lambda}{n}\right)^n \to e^{-\lambda}$（自然指數的定義）
- $\left(1 - \frac{\lambda}{n}\right)^{-k} \to 1$

$$\Rightarrow \quad \binom{n}{k}p^k(1-p)^{n-k} \;\longrightarrow\; \frac{\lambda^k e^{-\lambda}}{k!}$$

直覺：稀有事件（$p$ 小）在大量機會（$n$ 大）中發生的次數，只依賴平均值 $\lambda = np$，不依賴 $n, p$ 個別大小。

### Poisson 過程（現代形式）

Poisson 分佈的隨機過程版本——單位時間到達次數 $N(t)$：

1. **獨立增量**：不相交時段的到達數互相獨立。
2. **平穩增量**：$P(N(t+h) - N(t) = k) = \frac{(\lambda h)^k e^{-\lambda h}}{k!}$。
3. **無瞬時多重到達**：短時間內最多一個事件。

等價刻畫：事件間隔 $T_1, T_2, \dots$ 獨立同分佈，且

$$T_i \sim \text{Exponential}(\lambda), \qquad f(t) = \lambda e^{-\lambda t}$$

### Poisson 大數法則

Poisson 在 1837 年書中推廣了 Bernoulli 的大數法則：即使每次試驗的機率 $p_i$ **不必相同**（非常數機率），只要獨立，樣本平均仍收斂於機率平均：

$$\bar{X}_n = \frac{1}{n}\sum_{i=1}^{n} X_i \;\xrightarrow{P}\; \frac{1}{n}\sum_{i=1}^{n} p_i = \bar{p}_n$$

Bernoulli 版：$\bar{X}_n \to p$（同一個 $p$）；Poisson 版：$\bar{X}_n \to \bar{p}_n$（平均機率）。他稱之為「萬有的大數法則」（law of large numbers for universal phenomena）——司法、人口、自然現象皆適用。

### 司法判決的應用動機

Poisson 的原始模型：設陪審員正確判決的機率為 $p$，$n$ 人陪審團以多數決判決，錯判機率為

$$P(\text{錯判}) = \sum_{k > n/2} \binom{n}{k} p^k (1-p)^{n-k}$$

他用此公式比較不同陪審團規模與多數門檻（如 8:4 與 7:5）的錯判率，結論是降低門檻會增加冤案風險。這是機率論首次系統地介入司法制度設計。

### Python 模擬 Poisson 過程

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

lam, n = 3.0, 10000

# ---- 1. 二項分佈 → Poisson 極限 的驗證 ----
ks = np.arange(0, 12)
p_bin = stats.binom.pmf(ks, 1000, lam / 1000)     # B(1000, 0.003)
p_poi = stats.poisson.pmf(ks, lam)                # Poisson(3)
for k, a, b in zip(ks, p_bin, p_poi):
    print(f"k={k:2d}  binom={a:.6f}  poisson={b:.6f}  diff={abs(a-b):.1e}")

plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.bar(ks - 0.2, stats.binom.pmf(ks, 20, 0.15), width=0.4, label="B(20, 0.15)")
plt.bar(ks + 0.2, stats.poisson.pmf(ks, 3), width=0.4, label="Poisson(3)")
plt.legend(); plt.title("二項 → Poisson（λ=np=3）")

# ---- 2. 模擬 Poisson 過程：事件到達 ----
T = 10.0
arrival_times = []
t = 0
while True:
    t += rng.exponential(1 / lam)   # 指數間隔
    if t > T: break
    arrival_times.append(t)

plt.subplot(1, 2, 2)
plt.eventplot(arrival_times, lineoffsets=0.5, colors='b')
plt.title(f"10 小時內到達 {len(arrival_times)} 件（λ=3/時，期望 30 件）")
plt.xlabel("時間"); plt.tight_layout(); plt.show()

# ---- 3. 驗證期望 = 變異數 ----
counts = rng.poisson(lam, n)
print(f"樣本均值 = {counts.mean():.3f}（λ={lam}）")
print(f"樣本變異數 = {counts.var():.3f}（也應 ≈ {lam}）")
```

## 結案 -- 後果與影響

1. **司法機率**：Poisson 的工作延續了 Laplace 的司法統計傳統（孔多塞陪審團定理），雖然 19 世紀末此類「社會機率」因主觀假設受批評而衰落，但它是現代法律統計學與鑑識機率的遠祖。
2. **稀有事件定律的帝國擴張**：
   - **Bortkiewicz**（1898）《小數法則》：用 Poisson 分佈分析普魯士軍隊中被馬踢死的士兵人數——經典案例。
   - **Erlang**（1909）：丹麥電話工程師用 Poisson 過程建立排隊論（queueing theory）。
   - **核物理**：放射性衰變計數、Geiger 計數器服從 Poisson 分佈。
   - **現代**：網路封包到達、保險理賠、交通事故、突變計數、單分子螢光——一切「單位時間隨機到達」的模型。
3. **統計推論**：Poisson 迴歸（GLM）、卡方檢定的 Poisson 近似、點過程理論（空間統計、隨機幾何）。
4. **大數法則譜系**：Bernoulli → Poisson → Chebyshev/Khinchin 的現代弱/強大數法則，Poisson 佔承先啟後的一環。

## 關鍵人物與文獻

- **Siméon Denis Poisson**（1781–1840）：法國數學物理學家，Laplace 學派繼承者。
  - Poisson, S.-D. (1837). *Recherches sur la probabilité des jugements en matière criminelle et en matière civile, précédées des règles générales du calcul des probabilités*. Paris.
- **Pierre-Simon Laplace**（1812）：司法判決機率與二項分析的先行者。
- **Ladislaus Bortkiewicz**（1898）：《小數法則》，普魯士軍隊馬踢死案例。
- **Agner Krarup Erlang**（1909）：Poisson 過程與排隊論的創立者。
- 延伸閱讀：Kingman《Poisson Processes》(1993)、Ross《Introduction to Probability Models》。
