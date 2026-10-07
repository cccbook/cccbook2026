# 1984 - Gibbs 抽樣（MCMC 革命）

## 案件摘要
1984 年 Geman 兄弟在影像處理研究中提出 Gibbs 抽樣，配合 1990 年 Gelfand–Smith 將其推廣到統計界，掀起貝葉斯計算的革命。從此，任何複雜的後驗分布只要能寫出條件分布，就能用「一步步抽樣」逼近——貝葉斯推論從數學美化變成實際可算。

## 前因 -- 為什麼會有這個案子
- 貝葉斯推論的核心公式是**貝葉斯定理**：

$$
p(\theta \mid x) = \frac{p(x \mid \theta)\, p(\theta)}{p(x)}
= \frac{p(x \mid \theta)\, p(\theta)}{\int p(x \mid \theta')\, p(\theta') \, d\theta'}
$$

- 分母 $p(x)$ 是對 $\theta$ 的**高維積分**，當 $\theta$ 維度很高或模型複雜時，這個積分**沒有解析解**，也難以數值逼近（維度詛咒）。
- 1953 年 Metropolis 等人在核物理中提出 Metropolis 演算法；1970 年 Hastings 推廣為 **Metropolis–Hastings（MH）**，但統計界長期未重視。
- 1984 年 Geman & Geman 在研究影像的 Gibbs 分布（MRF）時提出 Gibbs 抽樣；1990 年 Gelfand & Smith 證明它在一般貝葉斯模型中的威力，引爆應用浪潮。

## 線索與推理 -- 數學式、程式、理論

### MCMC 原理：馬可夫鏈 + 平穩分布
**馬可夫鏈**：下一狀態只依賴目前狀態：

$$
P(\theta^{(t+1)} \mid \theta^{(t)}, \theta^{(t-1)}, \dots) = P(\theta^{(t+1)} \mid \theta^{(t)})
$$

**平穩分布（stationary distribution）**：若存在分配 $\pi$ 使得

$$
\pi(\theta') = \int \pi(\theta) \, K(\theta' \mid \theta) \, d\theta
$$

（$K$ 為轉移核），則鏈收斂到 $\pi$。MCMC 的核心技巧：**設計一個轉移核 $K$，使它的平穩分布恰好是我們想抽的後驗 $p(\theta|x)$**。

**詳細平衡（detailed balance）**是充分條件：

$$
\pi(\theta) \, K(\theta' \mid \theta) = \pi(\theta') \, K(\theta \mid \theta')
$$

### Metropolis–Hastings 演算法
1. 由提議分布 $q(\theta' \mid \theta^{(t)})$ 產生候選 $\theta'$。
2. 以機率 $\alpha$ 接受：

$$
\alpha = \min\left(1, \; \frac{p(\theta' \mid x) \, q(\theta^{(t)} \mid \theta')}{p(\theta^{(t)} \mid x) \, q(\theta' \mid \theta^{(t)})}\right)
$$

（注意：$\pi$ 的比例形式即可，分母 $p(x)$ 會消去——這正是繞過高維積分的關鍵！）
3. 接受則 $\theta^{(t+1)} = \theta'$，否則 $\theta^{(t+1)} = \theta^{(t)}$。

### Gibbs 抽樣：逐條件抽樣
Gibbs 是 MH 的特例（提議分布即條件分布、接受率恆為 1）。設 $\theta = (\theta_1, \dots, \theta_d)$，每一輪依序從**滿條件分布（full conditional）**抽樣：

$$
\theta_i^{(t+1)} \sim p(\theta_i \mid \theta_{-i}^{(t)}, x),
\quad \text{其中 } \theta_{-i} = (\theta_1, \dots, \theta_{i-1}, \theta_{i+1}, \dots, \theta_d)
$$

在貝葉斯模型中，$p(\theta_i \mid \theta_{-i}, x) \propto p(x \mid \theta)\, p(\theta_i \mid \theta_{-i})$，常是**標準分布**（如常態、Gamma）——這是 Gibbs 的魔法：把高維積分分解成一連串一維抽樣。

### burn-in 與收斂診斷
- **Burn-in**：丟棄前 $m$ 次迭代（鏈尚未收斂到平穩分布的階段）。
- **Thinning**：每隔 $k$ 次取一個樣本，減少自相關。
- **收斂診斷**：
  - 多鏈不同初值，比較 $\hat R$（Gelman-Rubin statistic），$\hat R \approx 1$ 表示收斂。
  - 追蹤圖（trace plot）應像「毛毛蟲」而非漂移的波浪。
  - 有效樣本數 ESS 應足夠大（自相關會讓名義樣本數虛高）。

### Python 實作：Metropolis–Hastings 與 Gibbs 抽樣（二維常態）

```python
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

# 目標：二維常態，mu=[0,0]，相關係數 rho=0.8
rho = 0.8
Sigma = np.array([[1, rho], [rho, 1]])
Sigma_inv = np.linalg.inv(Sigma)

def log_p(x):
    return -0.5 * x @ Sigma_inv @ x

# ---- Metropolis–Hastings ----
n_iter, burn = 20_000, 5_000
samples_mh = np.empty((n_iter, 2))
x = np.array([2.0, 2.0])

for t in range(n_iter):
    prop = x + np.random.normal(0, 0.5, 2)          # 對稱提議
    alpha = min(1, np.exp(log_p(prop) - log_p(x)))
    if np.random.rand() < alpha:
        x = prop
    samples_mh[t] = x

# ---- Gibbs 抽樣（滿條件分布可解析：皆為常態） ----
samples_gibbs = np.empty((n_iter, 2))
g = np.array([2.0, 2.0])

for t in range(n_iter):
    # p(x1 | x2) = Normal(rho * x2, 1 - rho^2)
    g[0] = np.random.normal(rho * g[1], np.sqrt(1 - rho**2))
    # p(x2 | x1) = Normal(rho * x1, 1 - rho^2)
    g[1] = np.random.normal(rho * g[0], np.sqrt(1 - rho**2))
    samples_gibbs[t] = g

# ---- 比較（丟棄 burn-in） ----
mh_b = samples_mh[burn:]
gb_b = samples_gibbs[burn:]
print("      平均            變異數")
print(f"MH    {mh_b.mean(axis=0)}   {mh_b.var(axis=0)}")
print(f"Gibbs {gb_b.mean(axis=0)}   {gb_b.var(axis=0)}")

fig, axes = plt.subplots(1, 3, figsize=(13, 4))
axes[0].scatter(*mh_b[::20].T, s=3, alpha=.5);  axes[0].set_title("MH samples")
axes[1].scatter(*gb_b[::20].T, s=3, alpha=.5);  axes[1].set_title("Gibbs samples")
axes[2].plot(samples_mh[:2000, 0]);             axes[2].set_title("MH trace (x1)")
plt.tight_layout(); plt.show()
```

執行後：兩種方法的樣本均值接近 $[0,0]$、變異數接近 1；散點圖呈現 $\rho=0.8$ 的橢圓相關結構；trace plot 顯示鏈已穩定混合。

## 結案 -- 後果與影響
- **貝葉斯計算的革命**：BUGS（1990s）與 Stan（2012，採用 HMC/NUTS）讓複雜貝葉斯模型只需描述模型即可自動推論。
- 應用爆炸：階層模型、貝葉斯迴歸、空間統計、流行病學、金融、生態學。
- 理論發展：HMC（Hamiltonian Monte Carlo）、Slice sampling、Particle filter（SMC）、變分推論（VI）作為 MCMC 的快速替代。
- Geman & Geman 原論文同時催生了**模擬退火（simulated annealing）**，成為組合優化的經典演算法。
- Gibbs 抽樣也串起了與 EM 的血緣：在貝葉斯 GMM 中，隱變數 $z_i$ 的滿條件分布正是 Gibbs 抽樣的對象。

## 關鍵人物與文獻
- **Stuart Geman & Donald Geman**（布朗大學）：Gibbs 抽樣與模擬退火的提出者。
- **Alan Gelfand & Adrian Smith**（1990）：將 Gibbs 抽樣帶入統計主流。
- **Nicholas Metropolis, W. K. Hastings**：MCMC 的奠基者。
- Geman, S., & Geman, D. (1984). *Stochastic relaxation, Gibbs distributions, and the Bayesian restoration of images*. IEEE TPAMI 6(6), 721–741.
- Gelfand, A. E., & Smith, A. F. M. (1990). *Sampling-based approaches to calculating marginal densities*. JASA 85(410), 398–409.
- Gelman, A., et al. (2013). *Bayesian Data Analysis*, 3rd ed. CRC Press.
