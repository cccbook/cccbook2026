# 2001 -- Longstaff–Schwartz 最小平方法蒙地卡羅：美式選擇權的高維解法

## 案件描述

2001 年，Francis Longstaff 與 Eduardo Schwartz（UCLA）在《Review of Financial Studies》發表《Valuing American Options by Simulation: A Simple Least-Squares Approach》。他們解決了一個困擾金融計算界 20 多年的難題：

> **蒙地卡羅模擬（1977, Boyle）可以為任何歐式商品定價，但「可以提前執行」的美式商品——蒙地卡羅只能向前模擬，怎麼知道「現在該不該執行」？**

答案驚人的簡單：**用迴歸（最小平方法）估計「繼續持有的價值」**。這個被稱為 LSM 的演算法，讓蒙地卡羅終於能處理美式選擇權、可轉債、可贖回債券、不動產選擇權等一切「最適停時」問題。

## 前因：美式商品的高維難題

- 二項樹（1979, CRR，見 [1979-CRR二項樹模型.md](1979-CRR二項樹模型.md)）可以處理美式選擇權，但**維度災難**：多標的（籃子選擇權）或多狀態變數（隨機波動率 + 隨機利率）的樹會組合爆炸。
- 蒙地卡羅可以處理高維度，但**倒推歸納做不了**：定價美式選擇權需要動態規劃（從末端倒推），而蒙地卡羅的路徑是「平行前進」的——兩種方法在美式問題上互斥。
- 1990 年代的嘗試：Tilley（1993）、Broadie–Glasserman（1997）等，都複雜且難以收斂。
- **線索**：Longstaff 與 Schwartz 意識到：蒙地卡羅雖然不能倒推，但可以**在每個執行時點，用已模擬的路徑資料做迴歸**——估計「繼續持有的條件期望」。

## 推理過程

### 線索一：把動態規劃變成迴歸

美式選擇權的定價是最適停時問題：

$$V_0 = \sup_{\tau} E\left[e^{-r\tau} f(S_\tau)\right]$$

動態規劃的貝爾曼方程：在每個時點比較「執行價值」與「繼續價值」：

$$V_t = \max\left(f(S_t),\; e^{-r\Delta t} E[V_{t+\Delta t} \mid S_t]\right)$$

**難點**：條件期望 $E[V_{t+\Delta t} \mid S_t]$ 沒有解析解。

**LSM 的洞察**：用已模擬的 $M$ 條路徑，在每個時點跑**最小平方法迴歸**：

$$Y_m = \sum_k \beta_k \, \phi_k(S_t^{(m)}) + \eta_m$$

其中 $Y_m$ 是第 $m$ 條路徑「未來支付的折現值」、$\phi_k$ 是基底函數（多項式、Laguerre 多項式等）。迴歸擬合值就是「繼續價值」的估計。

### 線索二：演算法的三步驟

1. **前進模擬**：模擬 $M$ 條標的路徑（在風險中立測度下）。
2. **倒推迴歸**：從到期日往前，在每個（價內的）執行時點：
   - 對「未來支付的折現值」對狀態變數做最小平方法迴歸
   - 比較執行價值與迴歸擬合的繼續價值 → 決定該路徑的執行時點
3. **平均折現**：對所有路徑的執行支付折現取平均 → 選擇權價格。

### 線索三：為什麼迴歸是無偏的（近似）

**數學基礎**：迴歸是在 $L^2$ 空間做**條件期望的投影**——最小平方法的擬合值正是 $E[Y \mid S_t]$ 對基底函數張成的子空間的正交投影。基底函數夠多時，投影收斂到真實條件期望（Clément–Lamberton–Protter 2002 證明了收斂性）。

**下偏性質**：LSM 的估計是「下偏」的（偏低的），因為用估計的繼續價值做決策，不會優於用真實繼續價值——Broadie–Glasserman 的雙邊界法可以夾出誤差範圍。

## 現代程式重現：LSM 美式賣權

```python
import numpy as np

def lsm_american_put(S, K, r, sigma, T, M=100_000, n=50, degree=3, seed=0):
    rng = np.random.default_rng(seed)
    dt = T / n; disc = np.exp(-r*dt)
    # 1. 前進模擬
    dW = rng.standard_normal((M, n)) * np.sqrt(dt)
    logS = np.log(S) + np.cumsum((r - 0.5*sigma**2)*dt + sigma*dW, axis=1)
    S_paths = np.exp(logS)

    # 2. 倒推迴歸
    cashflow = np.maximum(K - S_paths[:, -1], 0)  # 到期支付
    exercise_t = np.full(M, n)
    for step in range(n-1, 0, -1):
        St = S_paths[:, step]
        itm = St < K                              # 只在價內做迴歸
        if itm.sum() == 0: continue
        y = cashflow * np.exp(-r*dt*(exercise_t - step))  # 折現未來支付
        # 3. 最小平方法：條件期望的投影
        X = np.vander(St[itm], degree+1, increasing=True)
        beta = np.linalg.lstsq(X, y[itm], rcond=None)[0]
        continuation = X @ beta
        exercise_now = K - St[itm] > continuation  # 執行價值 > 繼續價值
        idx = np.where(itm)[0][exercise_now]
        cashflow[idx] = K - St[idx]
        exercise_t[idx] = step

    # 支付折現平均 → 價格
    return np.mean(cashflow * np.exp(-r*dt*exercise_t))

print(lsm_american_put(100, 100, 0.05, 0.2, 1))
# 美式賣權解析基準 ≈ 6.09（蒙地卡羅 ± 0.02）— 驗證 LSM 準確
```

## 後果

- LSM 成為**高維美式商品的工業標準**：可轉債定價、可贖回債券、不動產選擇權、實質選擇權、能源商品（swing options）——全部用 LSM。
- **最適停時 + 蒙地卡羅的統一**：Longstaff–Schwartz 把「動態規劃」與「蒙地卡羅」兩大方法焊接在一起——這是金融計算方法論的里程碑。
- **機器學習的前聲**：LSM 的「用迴歸估計條件期望」思想，正是後來深度學習定價（用神經網路代替多項式基底）的邏輯原型——見 [2017-深度避險.md](2017-深度避險.md)。
- **收斂理論**：Clément–Lamberton–Protter（2002）證明 LSM 收斂；Longstaff–Schwartz 的原論文成為 RFS 史上被引用最多的論文之一。
- 盲點：迴歸基底選擇（多項式階數）影響精度；路徑數不足時下偏明顯；對高頻決策（每日執行、百期）的計算量仍然大。

## 偵探筆記

- 動機：蒙地卡羅不能倒推、樹模型維度災難——美式商品的高維難題
- 工具：最適停時、貝爾曼方程、最小平方法迴歸（條件期望投影）
- 遺產：高維美式定價工業標準、機器學習定價的思想原型
- 盲點：基底選擇、下偏性、計算量

## 參考資料

- Longstaff, F., Schwartz, E. (2001). "Valuing American Options by Simulation: A Simple Least-Squares Approach". *Review of Financial Studies*, 14(1), 113–147.
- Clément, E., Lamberton, D., Protter, P. (2002). "An Analysis of a Least Squares Regression Method for American Option Pricing". *Finance and Stochastics*.
