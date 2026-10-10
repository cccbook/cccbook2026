# 1977 -- Phelim Boyle 把蒙地卡羅引進選擇權定價

## 案件描述

1977 年，加拿大滑鐵盧大學的 Phelim Boyle 在《Journal of Financial Economics》發表《選擇權定價：蒙地卡羅方法的結果》（Options: A Monte Carlo Approach）。他做了一件把兩大領域焊接在一起的事：

> **用 Ulam 在 Los Alamos 發明的蒙地卡羅方法（1946），為金融選擇權定價。**

從此，高維度衍生性商品有了通用計算武器。

## 前因：PDE 路線的極限

- Black–Scholes（1973）有解析解，但只適用於歐式、單一標的、常態波動。
- 有限差分法（Schwartz 1977 等）可以解 PDE，但**維度災難**：$d$ 個標的需要 $O(N^d)$ 記憶體——5 個標的的籃子選擇權就已經爆炸。
- **線索**：Boyle 意識到期望值本身就是積分：

$$C = e^{-rT} E^Q[(S_T - K)^+] = e^{-rT} \int (S_T - K)^+ \, dQ$$

而蒙地卡羅正是估計高維積分的通用方法（1946 年 Ulam 用它算中子擴散）。**積分的維度，蒙地卡羅不在乎。**

## 推理過程

### 線索一：把定價變成路徑模擬

Boyle 的演算法極其簡單：

1. 在風險中立測度 $Q$ 下模擬 $M$ 條標的價格路徑：

$$S_{t+\Delta t} = S_t \exp\left((r - \tfrac{1}{2}\sigma^2)\Delta t + \sigma\sqrt{\Delta t}\, Z\right), \quad Z \sim N(0,1)$$

2. 對每條路徑計算支付 $f(S_T^{(m)})$。
3. 估計值 $= e^{-rT} \frac{1}{M}\sum_m f(S_T^{(m)})$。

### 線索二：收斂速率的分析

蒙地卡羅的標準誤：

$$\mathrm{SE} = \frac{\sigma_f}{\sqrt{M}}$$

收斂速率是 $O(M^{-1/2})$——與維度無關。這是它在高維度的殺手級優勢：有限差分在 1 維很快、5 維爆炸；蒙地卡羅在 1 維不特別快、500 維照樣可行。

**誤差減半需要 4 倍模擬數**——這是它的代價，催生了後來的變異數縮減技術。

### 線索三：變異數縮減的軍備競賽

Boyle 及後續學者發展出整套加速技術：

- **對偶變數（antithetic variates）**：同時用 $Z$ 與 $-Z$ 模擬，正負相消。
- **控制變數（control variates）**：用已知解析解的類似商品（如幾何平均選擇權）校正。
- **重要性抽樣、條件期望**……

## 現代程式重現：蒙地卡羅歐式選擇權

```python
import numpy as np

def mc_call(S, K, r, sigma, T, M=1_000_000, seed=0):
    rng = np.random.default_rng(seed)
    Z = rng.standard_normal(M)
    ST = S * np.exp((r - 0.5*sigma**2)*T + sigma*np.sqrt(T)*Z)
    payoff = np.maximum(ST - K, 0)
    return np.exp(-r*T) * payoff.mean(), payoff.std()/np.sqrt(M)

price, se = mc_call(S=100, K=100, r=0.05, sigma=0.2, T=1)
print(f"MC 價格 = {price:.4f} ± {se:.4f}")
# 解析解為 10.4506（Black-Scholes），SE ≈ 0.02 → 95% 區間覆蓋

# 對偶變數加速：SE 約降低 30%
def mc_call_antithetic(S, K, r, sigma, T, M=500_000, seed=0):
    rng = np.random.default_rng(seed)
    Z = rng.standard_normal(M)
    ST1 = S*np.exp((r - 0.5*sigma**2)*T + sigma*np.sqrt(T)*Z)
    ST2 = S*np.exp((r - 0.5*sigma**2)*T - sigma*np.sqrt(T)*Z)
    payoff = (np.maximum(ST1-K,0) + np.maximum(ST2-K,0)) / 2
    return np.exp(-r*T) * payoff.mean()
```

## 後果

- 蒙地卡羅成為**高維衍生品（籃子選擇權、亞式選擇權、利率商品、CDO）的工業標準**。今日每一家的風控系統都在跑蒙地卡羅。
- **美式選擇權的難題**：蒙地卡羅只能前進模擬，無法直接處理「可以提前執行」的最適停時問題——這個懸案等到 Longstaff–Schwartz（2001）的最小平方法蒙地卡羅（見 [2001-LongstaffSchwartz蒙地卡羅.md](2001-LongstaffSchwartz蒙地卡羅.md)）。
- **準蒙地卡羅（QMC）**：低差異序列（Sobol、Faure）把收斂率從 $O(M^{-1/2})$ 提升到接近 $O(M^{-1})$（1990 年代）。
- **GPU 時代**：蒙地卡羅的完美平行性使它成為 GPU 計算的最早商業應用之一。
- 傳承：CDO 定價（2000 年代）正是靠蒙地卡羅 + 高斯 Copula——而這組合成為 2008 年金融海嘯的技術核心（見 [2008-金融海嘯與CDO.md](2008-金融海嘯與CDO.md)）。

## 偵探筆記

- 動機：PDE 路線的維度災難
- 工具：風險中立測度下的路徑模擬、大數法則、變異數縮減
- 遺產：高維定價的工業標準、QMC、GPU 金融計算
- 盲點：$O(M^{-1/2})$ 收斂慢、早期執行商品處理不了（直到 2001 年）

## 參考資料

- Boyle, P. (1977). "Options: A Monte Carlo Approach". *Journal of Financial Economics*, 4(3), 323–338.
- Glasserman, P. (2003). *Monte Carlo Methods in Financial Engineering*. Springer.
