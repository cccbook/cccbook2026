# 1922 - Fisher 最大概似估計

## 案件摘要
1922 年，R. A. Fisher 發表《On the Mathematical Foundations of Theoretical Statistics》，釐清母體與樣本的觀念、提出最大概似估計（MLE），並證明其三大性質。統計學自此擁有「從樣本反推母體」的統一引擎。

## 前因 -- 為什麼會有這個案子
在 Fisher 之前，估計方法百花齊放卻缺乏統一標準：

- **動差法**（Pearson）：令樣本動差 $=$ 母體動差，解方程得估計。
- **最小平方法**（Gauss/Legendre）：只適用於線性模型，缺乏一般性。
- **逆機率法**（Bayes 學派）：需要先驗分佈，Fisher 認為這是「任意主觀」的。

**懸案**：有沒有一個方法，**不需要先驗、不限模型形狀、且在數學上最優**？

Fisher 同時發現當時的統計學者（包括 Pearson）**混淆了母體與樣本**：Pearson 用 "population" 和 "sample" 交替指涉，觀念混亂。這是本案的破案關鍵——**先釐清觀念，再建立方法**。

## 線索與推理 -- 數學式、程式、理論

### 線索一：母體 vs 樣本的觀念革命
Fisher 嚴格區分：
- **母體（population）**：一個無限大的假想集合，由參數 $\theta$ 的機率分佈 $f(x;\theta)$ 刻劃。
- **樣本（sample）**：從母體抽出、可觀測的有限數據 $x_1,\dots,x_n$。
- **統計量（statistic）**：樣本的函數 $T(x_1,\dots,x_n)$，不包含未知參數。

統計推論的方向是**單向**的：$f(x;\theta) \Rightarrow$ 樣本 $\Rightarrow$ 統計量 $\Rightarrow$ 推斷 $\theta$。這個框架至今仍是現代統計學的骨架。

### 線索二：最大概似估計（MLE）
定義**概似函數**（likelihood）：

$$L(\theta) = \prod_{i=1}^{n} f(x_i;\theta)$$

MLE 即選擇使概似最大的參數：

$$\hat{\theta} = \arg\max_\theta L(\theta) = \arg\max_\theta \prod_{i=1}^n f(x_i;\theta)$$

實務上取對數概似（log-likelihood）較方便：

$$\ell(\theta) = \log L(\theta) = \sum_{i=1}^{n} \log f(x_i;\theta), \qquad \hat{\theta} = \arg\max_\theta \ell(\theta)$$

求解條件：$\ell'(\hat{\theta}) = 0$（得分方程，score equation），其中 score 定義為

$$S(\theta) = \frac{\partial \ell}{\partial \theta}, \qquad I(\theta) = -E\!\left[\frac{\partial^2 \ell}{\partial \theta^2}\right] \;\;(\text{Fisher 資訊})$$

### 線索三：三大性質（Fisher 的證明）
Fisher 證明 MLE 具有：

1. **一致性（consistency）**：$\hat{\theta}_n \xrightarrow{p} \theta$，樣本越大估計越準。
2. **有效性（efficiency）**：漸近變異數達到 **Cramér–Rao 下界**：

   $$\text{Var}(\hat{\theta}) \ge \frac{1}{n I(\theta)}, \qquad \text{MLE 漸近達到} \;\; \text{Var}(\hat\theta_n) \approx \frac{1}{nI(\theta)}$$

3. **充分性（sufficiency）**：當存在充分統計量 $T$ 時（如常態的 $\bar{X}, s^2$），MLE 是 $T$ 的函數，不損失資訊。

漸近常態性：

$$\sqrt{n}(\hat{\theta}_n - \theta) \xrightarrow{d} N(0,\; 1/I(\theta))$$

### 推理重點
1. MLE 是「一致 + 有效 + 充分」的**同時達成者**，在 Fisher 的框架下沒有更好的通用方法。
2. Fisher 資訊 $I(\theta)$ 是 MLE 變異數的下界，也是日後 Fisher 資訊幾何的起點。
3. 貝葉斯學派後來證明：若使用正確先驗，貝葉斯估計也可達到同樣效率——兩派自此開始長達百年的競爭與融合。

### Python 實作：MLE 估計常態分佈參數
```python
import numpy as np
from scipy import stats, optimize
import matplotlib.pyplot as plt

rng = np.random.default_rng(7)
data = rng.normal(loc=3.0, scale=1.5, size=500)

# 常態分佈的對數概似
def neg_loglik(params, x):
    mu, sigma = params
    return -np.sum(stats.norm.logpdf(x, loc=mu, scale=sigma))

res = optimize.minimize(neg_loglik, x0=[0, 1], args=(data,), method='Nelder-Mead')
mu_hat, sigma_hat = res.x
print(f"MLE: mu = {mu_hat:.4f}, sigma = {sigma_hat:.4f}")

# 常態的解析解：MLE 恰為樣本均值與樣本標準差
print(f"解析: mu = {data.mean():.4f}, sigma = {np.sqrt(np.mean((data-data.mean())**2)):.4f}")

# 理論驗證：sqrt(n)*(hat-theta) -> N(0, 1/I(theta))，I(mu)=1/sigma^2
mus = [rng.normal(3.0, 1.5, n).mean() for n in [20, 100, 500]]
for n, m in zip([20, 100, 500], mus):
    se = 1.5 / np.sqrt(n)
    print(f"n={n}: mu_hat={m:.3f}, 理論 se={se:.3f}, 偏差/理論={abs(m-3)/se:.2f}")

# 目標函數地形圖
mu_grid = np.linspace(2.5, 3.5, 100)
sg_grid = np.linspace(1.0, 2.2, 100)
ll = np.array([[-neg_loglik([m, s], data) for m in mu_grid] for s in sg_grid])
plt.contourf(mu_grid, sg_grid, ll, 30, cmap='viridis')
plt.colorbar(label='log-likelihood')
plt.scatter([mu_hat], [sigma_hat], c='r', marker='x', s=100, label='MLE')
plt.xlabel('mu'); plt.ylabel('sigma'); plt.legend()
plt.title("Log-likelihood surface"); plt.savefig("mle.png", dpi=100)
```

## 結案 -- 後果與影響
- MLE 成為**統計推論的支柱**：從迴歸（ML 版本）、廣義線性模型、混合模型到機器學習中的最大概似訓練（如 softmax + cross-entropy 即 MLE），無所不在。
- Fisher 資訊 $I(\theta)$ 開啟了資訊幾何（information geometry）與漸近理論。
- 充分性概念促成指數族（exponential family）與充分統計量的完整理論。
- Fisher 與 Pearson 學派的觀念之爭（母體 vs 樣本、Bayes vs likelihood）塑造了 20 世紀統計學的版圖。
- 1925 年 Fisher 的《Statistical Methods for Research Workers》將 MLE 與檢定方法打包成「研究者工具箱」，是本案的直接續集。

## 關鍵人物與文獻
- **R. A. Fisher (1890–1962)**：MLE、Fisher 資訊、充分性、漸近理論的奠基者。
- **Karl Pearson (1857–1936)**：動差法與觀念混亂的「對照組」，也是 Fisher 的論敵。
- **Harald Cramér (1893–1985)**：1946 年完成 Cramér–Rao 下界的嚴格證明。
- Fisher, R. A. (1912). *On an absolute criterion for fitting frequency curves*. （MLE 的先驅短文）
- Fisher, R. A. (1922). *On the mathematical foundations of theoretical statistics*. Phil. Trans. R. Soc. A 222.
- Fisher, R. A. (1925). *Theory of statistical estimation*. Proc. Camb. Phil. Soc. 22.
