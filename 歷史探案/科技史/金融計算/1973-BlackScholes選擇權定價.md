# 1973 -- Black–Scholes–Merton 選擇權定價：衍生性商品時代的開啟

## 案件描述

1973 年 5–6 月，《Journal of Political Economy》刊出 Black 與 Scholes 的《選擇權與公司負債的定價》，《Bell Journal of Economics》刊出 Merton 的《理性選擇權定價理論》。兩篇論文共同解出了困擾金融界 73 年的謎題：

> **選擇權到底值多少錢？**

答案是一個優雅到近乎魔法般的公式：

$$C = S_0 \, \Phi(d_1) - K e^{-rT} \Phi(d_2), \qquad d_1 = \frac{\ln(S_0/K) + (r + \sigma^2/2)T}{\sigma\sqrt{T}}, \quad d_2 = d_1 - \sigma\sqrt{T}$$

其中 $\Phi$ 是標準常態 CDF。Scholes 與 Merton 獲 **1997 年**諾貝爾獎（Black 已於 1995 年去世）。

## 前因：73 年的懸案

- Bachelier（1900）給出第一個公式，但基於算術布朗運動且未處理風險溢價。
- Samuelson（1965）修正為幾何布朗運動，但留下未解問題：**期望報酬率 $\mu$ 與折現率 $\rho$ 取決於風險偏好，如何消掉它們？**
- Sprenkle、Boness、Samuelson 等人都給出過「接近但差一步」的公式——都還需要代入投資人的風險偏好參數。
- **線索一**：Black 與 Scholes 在 MIT 偶然相識。Black 是應用數學出身的顧問，Scholes 是財務學者。他們試圖用 CAPM 求解——用資產的 beta 決定折現率。
- **線索二**：Merton（MIT 博士生，師從 Samuelson）精通 Itô 隨機積分——當時金融學界幾乎沒人會的蘇聯數學。

## 推理過程

### 線索一：Black–Scholes 的 CAPM 路線（以及它為什麼失敗）

Black 與 Scholes 最初用 CAPM：選擇權的 beta 隨 $S/K$ 變化，用它決定折現率。他們推導出一個 PDE，但驗證時發現公式「差一項」卻又算不出錯在哪。他們卡了很多個月。

**關鍵突破**：他們注意到公式中的 $\mu$（股票期望報酬）**消失了**——這暗示正確的推理根本不需要風險偏好。

### 線索二：Merton 的動態避險路線（正解）

Merton 的推理是純粹的 MM 式套利論證（見 [1958-ModiglianiMiller定理.md](1958-ModiglianiMiller定理.md)）：

1. **賣出一個選擇權，動態持有 $\Delta = \Phi(d_1)$ 股股票**。
2. 由 Itô 引理，選擇權價值 $V(S,t)$ 滿足：

$$dV = \left(\frac{\partial V}{\partial t} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2}\right)dt + \frac{\partial V}{\partial S} dS$$

3. 選擇 $\Delta = \partial V/\partial S$ 時，$dS$ 項**完全抵銷**——組合瞬間無風險。
4. 無風險組合必須賺無風險利率 $r$（無套利）：

$$\frac{\partial V}{\partial t} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} + rS\frac{\partial V}{\partial S} - rV = 0$$

這就是 **Black–Scholes PDE**。終端條件 $V(S,T) = (S-K)^+$，解出即為公式。

**哲學核心**：風險偏好被「動態避險」機械地消掉了——**你不需要知道投資人怕不怕風險**。這是 Samuelson 未解問題的答案，也是 MM 套利論證在連續時間的完美重現。

### 線索三：風險中立評價（後見之明的詮釋）

Cox 與 Ross（1976）後來重新詮釋：定價等於在「風險中立測度」下取期望再折現：

$$C = e^{-rT} \, E^Q[(S_T - K)^+]$$

其中 $Q$ 測度下所有資產賺 $r$。Harrison–Kreps（1979）與 Harrison–Pliska（1981）將其公理化為**鞅定價理論**：無套利 ⟺ 存在等價鞅測度。

## 現代程式重現：Black–Scholes 定價與 delta 避險

```python
import numpy as np
from scipy.stats import norm

def bs_call(S, K, r, sigma, T):
    d1 = (np.log(S/K) + (r + sigma**2/2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    return S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)

def bs_delta(S, K, r, sigma, T):
    return norm.cdf((np.log(S/K) + (r + sigma**2/2)*T) / (sigma*np.sqrt(T)))

print(bs_call(S=100, K=100, r=0.05, sigma=0.2, T=1))  # ≈ 10.45

# 驗證動態避險：賣 call + 持有 delta 股 → 組合變異數 ≈ 0（瞬間）
dS = 1.0
dV = bs_delta(100,100,0.05,0.2,1) * dS   # 選擇權價值變動 ≈ delta * 股價變動
hedge = -bs_delta(100,100,0.05,0.2,1) * dS
print(dV + hedge)  # ≈ 0
```

## 後果

- **1973 年 4 月**，芝加哥選擇權交易所（CBOE）開幕，同時 Texas Instruments 把公式寫進計算機——理論與市場同一天誕生（金融史上絕無僅有）。
- 衍生性商品市場爆炸性成長：全球名目本金規模至今超過 600 兆美元。選擇權定價成為所有「或有請求權」（contingent claims）——包括公司債（Merton 1974）、不動產抵押貸款、實質選擇權——的定價基礎。
- 催生整個量化金融產業：避險基金、風控部門、衍生品交易台。
- 隱憂的種子：模型假設（常態波動、連續交易、無摩擦）在危機中失靈——1987 黑色星期一（見 [1987-黑色星期一與投資組合保險.md](1987-黑色星期一與投資組合保險.md)）與 LTCM（見 [1998-LTCM長期資本管理.md](1998-LTCM長期資本管理.md)）都是「模型太成功」的反噬。
- 盲點：實證的「波動率微笑」違反公式假設——催生 Heston（1993）隨機波動率。

## 偵探筆記

- 動機：Samuelson 未解問題——風險偏好如何消掉？
- 工具：Itô 引理、動態避險、無套利、熱傳導型 PDE
- 遺產：衍生性商品時代、鞅定價理論、量化金融產業
- 盲點：常態假設、連續避險不可能（避險本身會移動市場——1987 年的教訓）

## 參考資料

- Black, F., Scholes, M. (1973). "The Pricing of Options and Corporate Liabilities". *Journal of Political Economy*, 81(3), 637–654.
- Merton, R. (1973). "Theory of Rational Option Pricing". *Bell Journal of Economics*, 4(1), 141–183.
- MacKenzie, D. (2006). *An Engine, Not a Camera: How Financial Models Shape Markets*. MIT Press.
