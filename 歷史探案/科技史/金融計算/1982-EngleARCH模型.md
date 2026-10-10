# 1982 -- Robert Engle 的 ARCH 模型：波動率不是常數

## 案件描述

1982 年，Robert Engle 在《Econometrica》發表《自迴歸條件異質變異數與英國通貨膨脹的估計》（Autoregressive Conditional Heteroscedasticity...）。論文的題目很學術，但主張震驚了金融界：

> **波動率不是常數——它可以被預測！**

Black–Scholes 假設 $\sigma$ 是常數，但看一眼任何股價圖就知道：平靜的日子聚集在一起，瘋狂的日子也聚集在一起（**波動率聚類**，volatility clustering）。Engle 的 ARCH 模型是第一個系統性地為「風險本身建模」的工具。Engle 獲 **2003 年**諾貝爾獎。

## 前因：常數波動的矛盾

- Black–Scholes（1973）與幾何布朗運動（1965）都假設波動率恆定。
- Mandelbrot（1963）早已觀察到大變動聚集——「大變動之後緊跟著大變動」，但沒有可操作的統計模型。
- 實證難題：用常態分配估計的風險**低估**極端事件——1987 年後這變成血淋淋的教訓。
- **線索**：Engle 在 LSE 與 UCSD 教計量經濟學，研究英國通膨的預測。他注意到殘差的**平方**有很強的自相關——「誤差的大小本身有記憶」。

## 推理過程

### 線索一：條件變異數是時間的函數

Engle 的核心思想：把變異數拆成「無條件（常數）」與「條件（隨時間變化）」：

$$r_t = \mu_t + \varepsilon_t, \qquad \varepsilon_t \mid \mathcal{I}_{t-1} \sim N(0, h_t)$$

其中 $h_t$ 是**條件變異數**——用過去資訊 $\mathcal{I}_{t-1}$ 可預測。

### 線索二：ARCH(p) 方程式

讓條件變異數取決於過去的**平方誤差**：

$$h_t = \omega + \sum_{i=1}^{p} \alpha_i \, \varepsilon_{t-i}^2$$

**數學解讀**：昨天的大誤差（$\varepsilon_{t-1}^2$ 大）→ 今天的變異數大。這正是波動率聚類的數學化身。

- 限制 $\alpha_i \geq 0$、$\sum \alpha_i < 1$ 保證平穩性。
- 無條件變異數 $= \dfrac{\omega}{1 - \sum \alpha_i}$（常數），但**條件**變異數隨時間劇烈波動。

### 線索三：為什麼這是革命？

在 ARCH 之前，「預測」只針對**均值**；ARCH 讓**變異數也可以預測**。這開啟了全新的問題清單：

- 波動率預測 → 風險管理（VaR）、選擇權定價（時變 $\sigma$）
- 波動率的可預測性**不違反**有效市場假說：報酬的均值仍不可預測，但風險可以——「預測風險」與「預測報酬」是兩回事。

## 現代程式重現：ARCH(1) 模擬與檢驗

```python
import numpy as np

def simulate_arch1(omega=0.1, alpha=0.7, n=2000, seed=0):
    rng = np.random.default_rng(seed)
    eps = np.zeros(n); h = np.zeros(n)
    for t in range(1, n):
        h[t] = omega + alpha * eps[t-1]**2
        eps[t] = np.sqrt(h[t]) * rng.standard_normal()
    return eps, h

eps, h = simulate_arch1()

# 檢驗 ARCH 效果：平方殘差的自相關應顯著
e1, e2 = eps[:-1]**2, eps[1:]**2
print("平方誤差自相關:", np.corrcoef(e1, e2)[0,1])   # 顯著 > 0
print("報酬自相關:", np.corrcoef(eps[:-1], eps[1:])[0,1])  # 接近 0
# → 均值不可預測，但波動率可以 — 這就是 ARCH 的訊息
```

## 後果

- **GARCH（1986, Bollerslev）**：加入變異數自身的自迴歸項，成為工業標準（見 [1986-BollerslevGARCH模型.md](1986-BollerslevGARCH模型.md)）。
- **風險管理**：VaR（1994）的波動率預測核心就是 GARCH（見 [1994-RiskMetricsVaR.md](1994-RiskMetricsVaR.md)）。
- **選擇權定價**：時變波動率的隨機波動率模型（Heston 1993）與 ARCH 路線殊途同歸。
- Engle 獲 2003 年諾貝爾獎（與 Granger 同年，表彰時間序列方法的貢獻）。
- 盲點：ARCH 對衝擊的反應較慢（只有平方誤差項），對「槓桿效果」（壞消息比好消息推升波動更多）處理不好——催生了 EGARCH（Nelson 1991）與 GJR 模型。

## 偵探筆記

- 動機：殘差平方的自相關——誤差的大小有記憶
- 工具：條件變異數、自迴歸結構、極大概似估計
- 遺產：波動率可預測性、GARCH 家族、風險管理的統計基礎
- 盲點：槓桿效果、厚尾的極端風險

## 參考資料

- Engle, R. (1982). "Autoregressive Conditional Heteroscedasticity with Estimates of the Variance of United Kingdom Inflation". *Econometrica*, 50(4), 987–1007.
- Mandelbrot, B. (1963). "The Variation of Certain Speculative Prices". *Journal of Business*.
