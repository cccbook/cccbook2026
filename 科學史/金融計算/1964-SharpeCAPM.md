# 1964 -- William Sharpe 的 CAPM：beta 的誕生

## 案件描述

1964 年 1 月，William Sharpe 在《Journal of Finance》發表《資本資產價格：風險條件下的市場均衡理論》（Capital Asset Prices）。這篇論文提出了一個簡潔到令人屏息的公式：

> **任何資產的期望報酬，只由一個數字——beta——決定。**

$$E[R_i] = r_f + \beta_i (E[R_M] - r_f)$$

這就是資本資產定價模型（Capital Asset Pricing Model, CAPM）。它把 Markowitz 的 $n \times n$ 共變異數矩陣，壓縮成一個單因子模型。

## 前因：Markowitz 的計算難題

- Markowitz（1952）要求投資人計算 $n$ 檔資產的完整共變異數矩陣：50 檔股票需要 1,275 個共變異數項，實務上不可行。
- Markowitz 主管 Sharpe 在蘭德公司（RAND Corporation）工作時，向 Markowitz 請教博士論文題目。Markowitz 建議他把「簡化投資組合的計算」當作方向。
- **線索**：Sharpe 最初的論文（1963，SIM 單指數模型）是純粹的計算簡化。但他隨後追問一個更深的問題：**如果所有人都用 Markowitz 的方法投資，市場均衡時價格會長什麼樣？**——這是從「個體最佳化」到「一般均衡」的跳躍。

## 推理過程

### 線索一：市場組合與分離定理

在均衡中，如果所有投資人都在同一條效率前緣上做選擇，則（Tobin 分離定理）：

1. 所有人都持有**同一個風險資產組合**——即**市場組合 $M$**（加權後就是市場本身）。
2. 個人只透過無風險資產 $r_f$ 與 $M$ 的組合比例，調整自己的風險偏好。

這條「資本配置線」是：

$$E[R_p] = r_f + \frac{\sigma_p}{\sigma_M}(E[R_M] - r_f)$$

### 線索二：beta 的推導

對任意資產 $i$，在均衡中它的超額報酬只對市場超額報酬敏感：

$$\beta_i = \frac{\mathrm{Cov}(R_i, R_M)}{\mathrm{Var}(R_M)}$$

**關鍵推理**：在 CAPM 均衡中，**只有系統性風險（beta）有報酬，非系統性風險沒有**——因為非系統性風險可以透過分散免費消除，沒有人會為可以免費消除的風險付錢。

$$E[R_i] - r_f = \beta_i (E[R_M] - r_f)$$

$\beta = 0$ 的資產只能賺無風險利率；$\beta > 1$ 的資產報酬高於市場（也跌得更兇）。

### 線索三：證券市場線（SML）

把 CAPM 畫成圖：橫軸 $\beta$、縱軸 $E[R_i]$，所有資產必須落在一條直線上——**證券市場線**。任何偏離 SML 的資產，就是被錯定價的套利機會。

## 現代程式重現：估計 beta

```python
import numpy as np

def beta_regression(asset_returns, market_returns, rf=0.0):
    """用 OLS 估計 beta:  R_i - rf = alpha + beta * (R_M - rf)"""
    y = asset_returns - rf
    x = market_returns - rf
    beta = np.cov(y, x)[0, 1] / np.var(x)
    alpha = y.mean() - beta * x.mean()
    return alpha, beta

# Jensen's alpha: 若 alpha 顯著異於 0，表示該資產擊敗 CAPM 預測
# 這正是 1968 年 Jensen 檢驗基金經理人績效的方法
```

## 後果

- **基金績效評估革命**：Jensen（1968）用 CAPM 的 alpha 檢驗基金經理人，發現絕大多數 alpha 為負——「你的基金經理人有沒有技術」從此有了科學標準（延續 Cowles 1933 的問題）。
- **指數化投資的理論基礎**：CAPM 說「持有市場組合」，Bogle（1976）的 Vanguard 指數基金把它變成產品。
- **企業財務的實務標準**：WACC 計算中的股權成本至今仍普遍用 CAPM 估計。
- Sharpe 獲 **1990 年**諾貝爾獎。
- 盲點與後續：實證發現報酬不只由 beta 決定——Fama–French 三因子模型（1993）加入規模（SMB）與價值（HML）因子；Roll 批評（1977）指出市場組合根本無法觀測。CAPM 雖然「錯了」，但作為基準模型至今無人取代。

## 偵探筆記

- 動機：Markowitz 共變異數矩陣的計算不可行性
- 工具：一般均衡、分離定理、單因子線性定價
- 遺產：beta、alpha、SML、指數化投資
- 盲點：市場組合不可觀測（Roll 批評）、單因子假設的實證失敗

## 參考資料

- Sharpe, W. (1964). "Capital Asset Prices: A Theory of Market Equilibrium under Conditions of Risk". *Journal of Finance*, 19(3), 425–442.
- Sharpe, W. (1963). "A Simplified Model for Portfolio Analysis". *Management Science*.
- Jensen, M. (1968). "The Performance of Mutual Funds in the Period 1945–1964". *Journal of Finance*.
