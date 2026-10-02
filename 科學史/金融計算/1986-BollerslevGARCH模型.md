# 1986 -- Tim Bollerslev 的 GARCH 模型：波動率預測的工業標準

## 案件描述

1986 年，Tim Bollerslev（Engle 的學生）在《Journal of Econometrics》發表《一般化自迴歸條件異質變異數》（Generalized Autoregressive Conditional Heteroskedasticity）。ARCH（1982）只用了過去的平方誤差；Bollerslev 加上了過去的**變異數本身**：

> **GARCH(p, q)：今天的條件變異數 = 常數 + 過去平方誤差的加權 + 過去變異數的加權。**

$$h_t = \omega + \sum_{i=1}^{q} \alpha_i \varepsilon_{t-i}^2 + \sum_{j=1}^{p} \beta_j h_{t-j}$$

最簡單的 GARCH(1,1) 成為金融計量經濟學史上被使用最多的模型——沒有之一。

## 前因：ARCH 的記憶太短

- ARCH(p) 需要**很大的 p** 才能捕捉金融資料的長記憶——Engle 自己估計英國通膨用了 ARCH(4)，股價資料常常需要 ARCH(8) 以上，參數過多、估計困難。
- **線索**：Bollerslev 意識到 ARMA 與 ARCH 的類比——ARMA 用 MA 項代替高階 AR；GARCH 用變異數的自迴歸項代替高階 ARCH，兩個參數就能表達長記憶。

## 推理過程

### 線索一：GARCH(1,1) 的優雅

$$h_t = \omega + \alpha \varepsilon_{t-1}^2 + \beta h_{t-1}$$

三個參數（$\omega, \alpha, \beta$）捕捉全部：

- $\alpha$：**衝擊的反應強度**（news 今天的影響）
- $\beta$：**記憶的持續性**（persistence）
- $\alpha + \beta < 1$：平穩條件；$\alpha + \beta$ 越接近 1，波動率的記憶越長（實證上股票通常 $\approx 0.95–0.99$）

### 線索二：波動率的預測公式

GARCH(1,1) 有封閉形式的多期波動率預測——這是它成為工業標準的實務理由：

$$E[h_{t+k}] = \sigma^2 + (\alpha+\beta)^{k-1}(h_{t+1} - \sigma^2)$$

其中 $\sigma^2 = \dfrac{\omega}{1-\alpha-\beta}$ 是長期（無條件）變異數。預測以幾何速度 $(\alpha+\beta)^k$ 回歸長期平均——**均值回歸的波動率**。

### 線索三：條件厚尾

即使標準化殘差 $z_t = \varepsilon_t/\sqrt{h_t}$ 是常態，$r_t$ 的**無條件分配**也是厚尾的（過度峰態）：

$$\text{kurtosis} = 3 + \frac{2\alpha^2}{1 - (\alpha+\beta)^2 - 2\alpha^2} \times \frac{1}{1} > 3$$

（在 $\alpha>0$ 時。）這解釋了為什麼金融報酬看起來「常態但厚尾」——**厚尾不一定是機制厚尾，可能是波動率隨機造成的**。

## 現代程式重現：GARCH(1,1) 估計與預測

```python
# pip install arch
import numpy as np
from arch import arch_model

def simulate_garch11(omega=0.05, alpha=0.1, beta=0.85, n=5000, seed=0):
    rng = np.random.default_rng(seed)
    eps = np.zeros(n); h = np.zeros(n)
    for t in range(1, n):
        h[t] = omega + alpha*eps[t-1]**2 + beta*h[t-1]
        eps[t] = np.sqrt(h[t]) * rng.standard_normal()
    return eps

eps = simulate_garch11()

# 用 arch 套件估計 GARCH(1,1)
am = arch_model(eps * 100, vol='GARCH', p=1, q=1)
res = am.fit(disp='off')
print(res.params)          # 應回收 omega≈0.05, alpha≈0.1, beta≈0.85

# 多期波動率預測（VaR 的核心輸入）
forecast = res.forecast(horizon=10)
print(forecast.variance.values[-1])
```

## 後果

- **RiskMetrics（1994）**：J.P. Morgan 的 VaR 系統的波動率引擎就是指數加權的 GARCH 特例（$\alpha+\beta=1$ 的 IGARCH，見 [1994-RiskMetricsVaR.md](1994-RiskMetricsVaR.md)）。
- **計量經濟的工業標準**：GARCH 家族超過數百個變體（EGARCH、GJR、TGARCH、GARCH-M...），用於匯率、利率、商品、加密貨幣。
- Engle 獲 2003 年諾貝爾獎——GARCH 是主要功臣之一。
- **選擇權定價**：Duan（1995）的 GARCH 選擇權定價模型，把條件變異數帶進衍生品定價。
- 盲點：GARCH 對「已實現波動率」（realized volatility，用高頻資料直接測量的波動率）的優勢在 2000 年代被挑戰；且 GARCH 描述的是「統計上的波動率」，不含跳躍與結構性斷裂。

## 偵探筆記

- 動機：ARCH 記憶太短、參數過多
- 工具：變異數自迴歸、封閉形式預測、極大概似
- 遺產：風險管理的工業標準、數百個變體的家族
- 盲點：統計波動率 vs 已實現波動率、跳躍與斷裂

## 參考資料

- Bollerslev, T. (1986). "Generalized Autoregressive Conditional Heteroskedasticity". *Journal of Econometrics*, 31(3), 307–327.
- Engle, R. (2001). "GARCH 101: The Use of ARCH/GARCH Models in Applied Econometrics". *Journal of Economic Perspectives*.
