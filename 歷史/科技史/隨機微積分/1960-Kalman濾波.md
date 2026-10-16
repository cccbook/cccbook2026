# 1960 年 Kalman 濾波：登月艙裡的遞迴預言家

| 項目 | 內容 |
|------|------|
| 案發時間 | 1960 年 |
| 案發地點 | 美國巴爾的摩 ASME 年會論文、NASA 阿波羅計畫導航電腦 |
| 主角 | Rudolf Kalman、Richard Bucy、Stanley Schmidt（NASA 推手） |
| 案件性質 | 噪聲中的訊號如何即時還原，登月軌道分秒不能等 |
| 關鍵證物 | 預測–更新循環，增益 $K = PH^T(HPH^T+R)^{-1}$ |
| 關聯案件 | 1908 年 Langevin–OU 方程、1940 年代 Wiener 濾波、1993 年粒子濾波 |

## 案發現場

1960 年，美國正衝向月球。阿波羅太空船的導航電腦記憶體只有約 72KB，卻要在充滿噪聲的雷達與陀螺儀讀數中，即時算出太空船的位置與速度。地面大型電腦可以事後慢慢算，但太空船等不了。

當時的正統方法是 Wiener 濾波：用無窮歷史的卷積做最優估計，公式優美卻不遞迴。每來一筆新資料就要重算一次，對星載電腦是死刑判決。

案發現場的數學模型其實就是 Langevin 的後代。狀態按線性動力學演化，觀測被噪聲污染：

$$
x_k = F x_{k-1} + w_k
$$

$$
z_k = H x_k + v_k
$$

其中 $w_k$ 為過程噪聲，協方差為 $Q$ ， $v_k$ 為觀測噪聲，協方差為 $R$ 。已知帶噪觀測 $z_1,\dots,z_k$ ，求狀態 $x_k$ 的最優估計。這正是 OU–Langevin 血緣在離散時間的轉世。

Rudolf Kalman 在 1960 年拋出論文《A New Approach to Linear Filtering and Prediction Problems》，手法是狀態空間加遞迴。審稿人起初冷淡，說這不過是最小平方法的包裝。但 NASA 的 Stanley Schmidt 看懂了：這是唯一能上火箭的濾波器。

## 偵查過程

Kalman 的偵查分兩步：先預測，再更新。假設 $k-1$ 時刻已有估計 $\hat x_{k-1}$ 與誤差協方差 $P_{k-1}$ ，則預測步為：

$$
\hat x_{k|k-1} = F \hat x_{k-1}
$$

$$
P_{k|k-1} = F P_{k-1} F^T + Q
$$

新觀測 $z_k$ 到達後，計算殘差 $y_k = z_k - H\hat x_{k|k-1}$ ，再以 Kalman 增益 $K_k$ 修正：

$$
K_k = P_{k|k-1} H^T(H P_{k|k-1} H^T + R)^{-1}
$$

$$
\hat x_k = \hat x_{k|k-1} + K_k y_k
$$

$$
P_k = (I - K_k H) P_{k|k-1}
$$

增益 $K$ 的直覺是信噪比的天平： $R$ 很大（觀測不可信）則 $K$ 趨小，相信模型預測； $P$ 很大（預測不準）則 $K$ 趨大，相信觀測。這正是貝氏定理在高斯世界的閉式解。

偵查筆錄整理如下：

| 步驟 | 公式角色 | 統計意義 |
|------|----------|----------|
| 預測均值 | $\hat x_{k\|k-1} = F\hat x_{k-1}$ | 模型外推 |
| 預測協方差 | $FP_{k-1}F^T + Q$ | 不確定性膨脹 |
| Kalman 增益 | $PH^T(HPH^T+R)^{-1}$ | 觀測與預測的權重 |
| 更新均值 | $\hat x + Ky$ | 殘差修正 |
| 更新協方差 | $(I-KH)P$ | 不確定性收縮 |

連續時間版本由 Kalman–Bucy（1961）補上，狀態服從線性 SDE，協方差服從 Riccati 方程：

$$
d\hat x_t = A\hat x_t dt + K_t(dz_t - H\hat x_t dt)
$$

其中 $K_t = P_t H^T R^{-1}$ ，而 $P_t$ 滿足 $\dot P = AP + PA^T + Q - PH^T R^{-1}HP$ 。這條 Riccati 方程正是控制論 LQR 問題的鏡像，濾波與控制在此對偶。

破案關鍵在 Schmidt 的工程改造：原始協方差更新在數值上不穩定，Schmidt 改用平方根形式與序貫處理，讓 1969 年阿波羅 11 號的導航電腦得以實裝。理論與工程在此合流。

## 結案報告

結案：Kalman 濾波把最優估計變成兩行遞迴，計算量從 $O(k^3)$ 降為每步常數，阿波羅得以登月。1969 年 7 月 20 日，導航電腦裡跑的正是這組方程。

遺產第一層是血緣的證實：Kalman 濾波的連續極限正是 OU–Langevin 過程的條件分佈演化，線性 SDE、高斯性、Riccati 方程三者互鎖。第二層是方法論：預測–更新的貝氏遞迴成為此後所有濾波器的模板，包括 1993 年粒子濾波。第三層是對偶性：濾波的 Riccati 與最優控制的 Riccati 是同一枚硬幣的兩面，促成 LQG 理論。

此案也留下未解的伏筆：線性高斯之外，Riccati 閉式不再成立。擴展 Kalman 濾波用 Jacobian 硬上非線性，unscented 變換用 sigma 點逼近，直到粒子濾波徹底放棄高斯假設。這條支線將在 1993 年結案。

Kalman 本人因此獲 2009 年美國國家科學獎章。從登月到 GPS，從量化交易到自駕車，每個即時估計器裡都住著 1960 年的那位預言家。

## 證據與工具

核心證物一：離散預測步， $F$ 為狀態轉移， $Q$ 為過程噪聲協方差：

$$
P_{k|k-1} = F P_{k-1} F^T + Q
$$

核心證物二：Kalman 增益， $H$ 為觀測矩陣， $R$ 為觀測噪聲協方差：

$$
K_k = P_{k|k-1} H^T(H P_{k|k-1} H^T + R)^{-1}
$$

核心證物三：更新步， $y_k$ 為新息殘差， $I$ 為單位矩陣：

$$
\hat x_k = \hat x_{k|k-1} + K_k y_k
$$

辦案工具箱：

| 工具 | 用途 | 備註 |
|------|------|------|
| Riccati 方程 | 連續時間協方差演化 | 濾波–控制對偶的核心 |
| 新息序列 $y_k$ | 白化檢驗濾波器健康度 | 理想下應為白噪聲 |
| 一維常數模型 | 新手驗算增益收斂 | 對應 `_code/1960-kalman_1d.py` |
| OU 過程模擬 | 理解 $F$ 與 $Q$ 的來源 | $F \approx 1-\theta h$ |

 接案提示：用一維位置追蹤實驗比較原始觀測與濾波估計的 RMSE，可見濾波誤差通常低於觀測噪聲三成以上。

## 補充：程式實作

### 對應程式

本節對應 [1960-kalman_1d.py](_code/1960-kalman_1d.py) ，以一維隨機漫步驗證預測–更新循環。

### 理論呼應

本文核心是增益 $K_k = P_{k|k-1}H^T(HP_{k|k-1}H^T+R)^{-1}$ 在 $R$ 與 $P$ 之間取得信噪比平衡。
程式取 $Q = 1.0$ 與 $R = 4.0$ 跑五百步遞迴，預測步膨脹協方差 $P+Q$ ，更新步再以 $1-K$ 收縮。
數值增益收斂至穩態理論值 $K_{\infty} = 0.3903882032$ ，誤差為 $0.0$ ，呼應 $Riccati$ 方程的不動點。
濾波均方誤差比原始觀測低約三成六，證實遞迴估計在 $O(1)$ 單步計算下仍達最優。

### 執行方式

`python3 _code/1960-kalman_1d.py`

### 實測輸出

`RMSE_raw=2.04505 RMSE_kf=1.31193 ratio=0.6415 (need <0.7)` ， `K_last=0.3903882032 K_inf=0.3903882032 abserr=0.00e+00` ， `VERIFY ... PASS` 。

### 讀者實驗

將 $R$ 改為 $1.0$ 再重跑一次，觀察增益上升後濾波誤差比值如何跟著改變。

完整程式如下：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""1960 一維 Kalman 濾波（對應 wiki：Kalman 濾波 / 1960 年 Kalman 論文）。
狀態：x_{k+1} = x_k + w_k, w ~ N(0, Q)（隨機漫步）；
觀測：y_k = x_k + v_k, v ~ N(0, R)。
跑 500 步 Kalman 遞迴，驗證：
  (1) 濾波 RMSE 比 raw 觀測 RMSE 低三成以上（rmse_kf < 0.7*rmse_raw）；
  (2) 數值增益 K_500 吻合穩態理論增益 K_inf（誤差 < 1e-9）。
只用 numpy，固定種子，不畫圖。
"""
import numpy as np
import time

t0 = time.time()
SEED = 1960
np.random.seed(SEED)

Q = 1.0
R = 4.0
n = 500
x0 = 0.0
P0 = 1.0

w = np.sqrt(Q) * np.random.randn(n)
v = np.sqrt(R) * np.random.randn(n)
x_true = x0 + np.cumsum(w)          # x_k, k=1..n
y = x_true + v

# Kalman 遞迴
x_hat = 0.0
P = P0
K_last = 0.0
ests = np.empty(n)
for k in range(n):
    P_pred = P + Q
    K = P_pred / (P_pred + R)
    x_hat = x_hat + K * (y[k] - x_hat)
    P = (1.0 - K) * P_pred
    ests[k] = x_hat
    K_last = K

# 理論穩態：P = (-Q + sqrt(Q^2+4QR))/2，P_pred = P+Q，K_inf = P_pred/(P_pred+R)
P_inf = (-Q + np.sqrt(Q ** 2 + 4 * Q * R)) / 2.0
K_inf = (P_inf + Q) / (P_inf + Q + R)

rmse_raw = float(np.sqrt(np.mean((y - x_true) ** 2)))
rmse_kf = float(np.sqrt(np.mean((ests - x_true) ** 2)))
ratio = rmse_kf / rmse_raw
gain_err = abs(K_last - K_inf)

print(f"[kalman] seed={SEED} steps={n} Q={Q} R={R}")
print(f"[kalman] RMSE_raw={rmse_raw:.5f} RMSE_kf={rmse_kf:.5f} ratio={ratio:.4f} (need <0.7)")
print(f"[kalman] K_last={K_last:.10f} K_inf={K_inf:.10f} abserr={gain_err:.2e}")
print(f"[kalman] elapsed {time.time()-t0:.2f}s")

assert rmse_kf < 0.7 * rmse_raw, f"KF not 30% better: {rmse_kf} vs raw {rmse_raw}"
assert gain_err < 1e-9, f"steady gain mismatch: {K_last} vs {K_inf}"
print(f"VERIFY: kalman ratio={ratio:.4f}<0.7, gain_err={gain_err:.1e} PASS")
```
