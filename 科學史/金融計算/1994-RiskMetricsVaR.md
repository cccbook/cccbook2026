# 1994 -- J.P. Morgan 的 RiskMetrics：Value at Risk 成為風險管理的通用語言

## 案件描述

1994 年 10 月，J.P. Morgan 免費向全球發布 **RiskMetrics**——一套完整的市場風險度量技術文件與資料集。它的核心是一個簡單到可以印在 CEO 名片背面的數字：

> **Value at Risk（VaR）：在 95% 信賴水準下，明天這個組合最多會虧多少錢？**

例如「一日 95% VaR = 1,000 萬美元」的意思：有 5% 的機率明天虧損超過 1,000 萬。

VaR 從此成為全球銀行業的通用風險語言，並被巴塞爾委員會寫進資本規定。

## 前因：Dennis Weatherstone 的「15:15 報告」

- 1980 年代末，J.P. Morgan 的董事長 Dennis Weatherstone 要求他的風控長每天下午 4:15 交一頁紙報告：**明天全行最多可能虧多少錢**。
- 當時的風險管理是「名目本金」（notional amount）：「我們有 10 億美元的利率曝險」——但 10 億的曝險在不同波動環境下風險完全不同。
- 1987 黑色星期一（見 [1987-黑色星期一與投資組合保險.md](1987-黑色星期一與投資組合保險.md)）讓全行業痛感：**需要一個把所有曝險折算成同一種「潛在虧損貨幣」的方法。**
- **線索**：J.P. Morgan 內部已經有 GARCH 型的波動率預測技術（1980 年代末）與完整的共變異數矩陣資料。

## 推理過程

### 線索一：VaR 的統計定義

對組合報酬 $R$、信賴水準 $\alpha$（如 95%）、期間 $\Delta t$（如 1 日）：

$$P(R_{\Delta t} < -\mathrm{VaR}_\alpha) = 1 - \alpha$$

若 $R$ 近似常態（均值可忽略）：

$$\mathrm{VaR}_\alpha = z_\alpha \, \sigma_p \, V$$

其中 $z_{0.95} = 1.645$、$V$ 是組合價值、$\sigma_p$ 是組合波動率。**風險從「名目曝險」變成「機率加權的潛在虧損」**。

### 線索二：共變異數法（Variance-Covariance Method）

RiskMetrics 的標準演算法：

1. 把組合拆成**現金流映射**（cash flow mapping）到風險因子（各期限利率、匯率、股價）。
2. 預測各風險因子的波動率與相關性——用**指數加權移動平均（EWMA）**：

$$\sigma_t^2 = \lambda \sigma_{t-1}^2 + (1-\lambda) r_{t-1}^2, \quad \lambda = 0.94 \text{（日資料）}$$

（這是 $\alpha + \beta = 1$ 的 GARCH 特例——RiskMetrics 用實證把 $\lambda$ 定為 0.94，見 [1986-BollerslevGARCH模型.md](1986-BollerslevGARCH模型.md)。）

3. 組合波動率：$\sigma_p = \sqrt{\mathbf{w}^T \Sigma \mathbf{w}}$（Markowitz 的數學，見 [1952-Markowitz投資組合理論.md](1952-Markowitz投資組合理論.md)）。
4. VaR $= 1.645 \, \sigma_p \, V$。

**巧妙之處**：VaR 把 Markowitz 的組合數學、GARCH 的波動率預測、Black–Scholes 的敏感度（greeks）全部整合成「一個數字」。

### 線索三：其他計算路線

- **歷史模擬法（historical simulation）**：直接用過去 N 天的實際報酬重估組合——不假設常態。
- **蒙地卡羅法**：模擬成千上萬條路徑取分位數（見 [1977-Boyle蒙地卡羅選擇權定價.md](1977-Boyle蒙地卡羅選擇權定價.md)）。
- 三種路線的取捨：速度（共變異數）vs 準確性（蒙地卡羅）vs 簡單性（歷史模擬）。

## 現代程式重現：三種 VaR 計算

```python
import numpy as np

def var_covar_var(returns, weights, V=1e7, alpha=0.95):
    """共變異數法 VaR"""
    z = {0.95: 1.645, 0.99: 2.326}[alpha]
    sigma_p = np.sqrt(weights @ np.cov(returns.T) @ weights)
    return z * sigma_p * V

def historical_var(returns, weights, V=1e7, alpha=0.95):
    """歷史模擬法 VaR"""
    port_returns = returns @ weights
    return -np.percentile(port_returns, (1-alpha)*100) * V

def ewma_sigma(returns, lam=0.94):
    """RiskMetrics 的 EWMA 波動率"""
    s2 = returns.var()
    for r in returns:
        s2 = lam * s2 + (1 - lam) * r**2
    return np.sqrt(s2)

# 巴塞爾規定：VaR 需乘以 3 的乘數 + 回溯測試（backtesting）
```

## 後果

- **巴塞爾協定（1996 市場風險修正案）**：銀行的市場風險資本 = 3 × VaR（+ 附加項），VaR 成為法規語言。全球銀行的風控部門都圍繞 VaR 組織。
- **回溯測試（backtesting）**：Kupiec（1995）等檢驗 VaR 是否「說謊」——觀測到的違約次數是否與 5% 一致。
- **尾端風險的遺漏**：VaR 不說「超過 VaR 之後虧多少」——這催生了**期望短缺（Expected Shortfall, CVaR）**：

$$\mathrm{ES}_\alpha = -E[R \mid R < -\mathrm{VaR}_\alpha]$$

巴塞爾協定 IV（2019）已把法規從 VaR 轉向 ES。
- **模型同質性的危機**：所有人都用同一套 VaR，壓力下的去槓桿行為同質化——2008 年金融海嘯中 VaR 全面失靈（見 [2008-金融海嘯與CDO.md](2008-金融海嘯與CDO.md)）。
- RiskMetrics 團隊後來獨立成 RiskMetrics Group 公司（1998），2008 年被 MSCI 收購。

## 偵探筆記

- 動機：Weatherstone 的「一頁紙報告」需求 + 1987 年的教訓
- 工具：分位數統計、EWMA/GARCH 波動率、Markowitz 共變異數矩陣
- 遺產：法規標準、風控部門的組織原則、ES 的誕生
- 盲點：尾端風險、常態假設、模型同質性的系統性風險

## 參考資料

- J.P. Morgan (1994). *RiskMetrics Technical Document*.
- Jorion, P. (2006). *Value at Risk: The New Benchmark for Managing Financial Risk*. McGraw-Hill.
