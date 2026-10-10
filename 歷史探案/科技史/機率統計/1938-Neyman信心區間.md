# 1938 - Neyman 信心區間

## 案件摘要
1937 年 Neyman 在皇家統計學會演講（1938 年正式發表）提出信心區間（confidence interval）理論，以「重複抽樣的覆蓋率」給出區間估計的頻率式保證，成為現代統計區間估計的標準框架。

## 前因 -- 為什麼會有這個案子
- 點估計（如最大概似估計 $\hat\theta$）不告訴你「估得多準」，需要區間式的誤差範圍。
- Fisher 的 fiducial inference（信仰推斷，1930）試圖給區間機率詮釋，但邏輯含糊且在多參數時失效。
- Neyman 延續其假設檢定思想：把「區間是否蓋住真值」當成一個長期行為的錯誤率問題。

## 線索與推理 -- 數學式、程式、理論
### 覆蓋性質
信心區間由兩個統計量 $L(X_1,\dots,X_n) \leq U(X_1,\dots,X_n)$ 構成，若對所有 $\theta$ 滿足
$$
P_\theta\big(\theta \in [L(X),\, U(X)]\big) = 1-\alpha
$$
則稱 $[L, U]$ 為信心水準 $1-\alpha$ 的信心區間。

**關鍵：機率是對隨機區間 $[L,U]$ 而言，不是對固定的 $\theta$。** 頻率詮釋：重複抽樣多次，每次建一個區間，長期而言約 $100(1-\alpha)\%$ 的區間會蓋住真值 $\theta$。一旦算出特定區間如 $[2.1, 3.7]$，它要嘛蓋住要嘛沒蓋住，不能說「$\theta$ 落在此區間的機率是 95%」——這是最常見的誤讀。

### 經典例子：常態均值的 $t$ 區間
$X_1,\dots,X_n \sim N(\mu, \sigma^2)$，$\sigma$ 未知時：
$$
\bar{X} \pm t_{\alpha/2,\, n-1} \frac{S}{\sqrt{n}}, \quad S^2 = \frac{1}{n-1}\sum_i (X_i - \bar{X})^2
$$
因為 $\frac{\bar{X}-\mu}{S/\sqrt{n}} \sim t_{n-1}$（與 $\mu, \sigma$ 無關的樞紐量 pivot），覆蓋率對所有 $\mu, \sigma$ 精確成立。

### 與貝葉斯可信區間的對照
| | 信心區間（Neyman） | 可信區間（Bayesian） |
|---|---|---|
| 隨機的是什麼 | 區間 $[L,U]$ | 參數 $\theta$（有後驗分佈） |
| 機率詮釋 | 重複抽樣覆蓋率 | 給定資料後 $\theta$ 落入區間的機率 |
| 保證對象 | 所有 $\theta$（長期行為） | 特定這一次的推論 |
| 所需前提 | 樞紐量或漸近理論 | 事前分佈 prior |

貝葉斯的敘述「$P(\theta \in [L,U] \mid x) = 0.95$」直觀得多，但依賴 prior 選擇；Neyman 的保證不依賴 prior，但詮釋間接。兩者在大樣本、均勻 prior 下常近似重合。

### p 值與信心區間的關係
**對偶性**：信心水準 $1-\alpha$ 的信心區間，恰是所有「不會被水準 $\alpha$ 檢定拒絕」的參數值：
$$
[L, U] = \{\theta_0 : p(\theta_0) > \alpha\}
$$
因此「$95\%$ 信心區間不含 $\theta_0$」$\iff$「水準 $0.05$ 的雙尾檢定拒絕 $H_0: \theta=\theta_0$」$\iff p < 0.05$。

```python
# 模擬信心區間覆蓋率：驗證頻率詮釋
import numpy as np
from scipy import stats

rng = np.random.default_rng(7)
mu, sigma, n, alpha, reps = 5.0, 2.0, 25, 0.05, 20000
t_crit = stats.t.ppf(1 - alpha/2, n-1)

covered = 0
for _ in range(reps):
    x = rng.normal(mu, sigma, n)
    L, U = x.mean() - t_crit * x.std(ddof=1)/np.sqrt(n), \
           x.mean() + t_crit * x.std(ddof=1)/np.sqrt(n)
    covered += (L <= mu <= U)

print(f"實測覆蓋率 = {covered/reps:.4f}（目標 1-alpha = {1-alpha}）")
```

## 結案 -- 後果與影響
- 信心區間成為現代統計報告的標準格式（論文中「均值 ± CI」無所不在）。
- 覆蓋率思想延伸出信賴帶（simultaneous confidence band）、bootstrap 區間等。
- Fisher 對此理論強烈反對，fiducial inference 之爭延續多年，但 fiducial 學派最終式微。
- 與檢定的對偶性使 p 值、區間估計、假設檢定整合成一套一致框架。

## 關鍵人物與文獻
- **Jerzy Neyman**（1894–1981）：本案件主謀，1937 年讀文中提出理論。
- **J. Neyman (1937), "Outline of a Theory of Statistical Estimation Based on the Classical Theory of Probability", Phil. Trans. R. Soc. A 236.**（1938 年刊出）
- **J. Neyman (1934/1938)**：信心區間在工業抽樣中的應用推廣。
- R. A. Fisher：fiducial inference 創始者與論戰對手。
