# 1975 年 Milstein 格式：多出來的那半項修正

| 項目 | 內容 |
|------|------|
| 案發時間 | 1975 年 |
| 案發地點 | 蘇聯，數值機率學派 |
| 主角 | Grigori Milstein（G. N. Milstein） |
| 案件性質 | Euler–Maruyama 強階卡在 1/2，能否只加一項就衝上 1 階 |
| 關鍵證物 | 修正項 $\frac12\sigma\sigma'((\Delta W)^2-h)$ ，強 1 階 |
| 關聯案件 | 1955 年 Maruyama、1992 年 Kloeden–Platen、交換噪聲與 Lévy 面積 |

## 案發現場

Euler–Maruyama 格式（1955）雖然開山，但強收斂只有 $1/2$ 階。對只關心期望定價的人，弱 $1$ 階夠用；但對要追蹤路徑的濾波、控制、強逼近模擬， $1/2$ 階意味著步長砍四倍精度才升一倍，貴得令人心痛。

案發現場的屍檢報告早已寫明死因：Itô–Taylor 展開中被丟棄的雙重隨機積分。真解走一步的展開為：

$$
X_{t+h} \approx X_t + b h + \sigma\Delta W + \sigma\sigma'\int_t^{t+h}\int_t^s dW_u dW_s
$$

其中 $\sigma'$ 表 $\sigma$ 對 $x$ 的導數。Euler 法直接砍掉最後一項，而這一項的量級恰為 $h$ ，正是強誤差的瓶頸。

1975 年，Milstein 出手。他問：雙重積分能否顯式算出來？在一維情形，答案漂亮得像魔術。由 Itô 公式可得：

$$
\int_t^{t+h}\int_t^s dW_u dW_s = \frac{1}{2}((\Delta W)^2 - h)
$$

於是只需加一項修正，強階即可翻倍。這就是 Milstein 格式。

## 偵查過程

Milstein 的完整格式為：

$$
X_{n+1} = X_n + b h + \sigma\Delta W + \frac{1}{2}\sigma\sigma'((\Delta W)^2 - h)
$$

其中 $\sigma$ 與 $\sigma'$ 皆在 $X_n$ 取值， $\Delta W \sim N(0,h)$ 。新增的修正項均值為零（因為 $E[(\Delta W)^2] = h$ ），所以不影響弱階的一階性；但它補上了雙重積分的漲落，把強階從 $1/2$ 推上 $1$ 。

偵探用 Itô–Taylor 驗屍表確認：

| 展開項 | 量級 | Euler 法 | Milstein 法 |
|--------|------|----------|-------------|
| $b h$ | $h$ | 保留 | 保留 |
| $\sigma\Delta W$ | $\sqrt{h}$ | 保留 | 保留 |
| $\sigma\sigma'\int\int dW dW$ | $h$ | 丟棄 | 以修正項保留 |
| 高階餘項 | $h^{3/2}$ | 丟棄 | 丟棄 |
| 強收斂階 | — | $1/2$ | $1$ |

一維破案後，真正的連環殺手現身：多維多噪聲。設第 $j$ 個噪聲的擴散為 $\sigma^{(j)}$ ，雙重積分變成 $I_{jk} = \int\int dW^j dW^k$ 。當 $j \ne k$ 時， $I_{jk} + I_{kj} = \Delta W^j \Delta W^k$ ，但各自拆不開，差值正是 Lévy 面積：

$$
A_{jk} = \frac{1}{2}(I_{jk} - I_{kj})
$$

若擴散向量場滿足交換性（commutativity），即 Lie 括號為零，則交叉項可合併，Milstein 仍顯式；否則必須模擬 Lévy 面積，沒有便宜的閉式。這條伏筆將在 Kloeden–Platen（1992）聖經中大書特書，並一路連到 Lyons 粗糙路徑（1998）。

加性噪聲是另一個趣案：若 $\sigma$ 為常數，則 $\sigma' = 0$ ，修正項自動消失，Euler 與 Milstein 重合。這解釋了為何 OU 過程用 Euler 法已有一階強收斂：兇手根本不在場。

## 結案報告

結案：只加一項 $\frac12\sigma\sigma'((\Delta W)^2-h)$ ，強收斂即從 $1/2$ 升至 $1$ 。代價是需要 $\sigma$ 可微並計算 $\sigma'$ ，弱階維持 $1$ 不變。

遺產第一層是實務：路徑追蹤、強逼近、巢式模擬從此有便宜的一階格式。第二層是理論：Milstein 證明高階格式的關鍵是高階重隨機積分，開啟了高階 Taylor、Runge–Kutta、 extrapolation 的軍備賽。第三層是警示：多維非交換噪聲的 Lévy 面積無法迴避，粗糙路徑理論正是為此而生。

從 Maruyama（1955）到 Milstein（1975），二十年只加一項。這一項，是隨機數值分析從開山到登堂入室的距離。

## 證據與工具

核心證物一：Milstein 迭代， $h$ 為步長， $\Delta W$ 為布朗增量：

$$
X_{n+1} = X_n + b h + \sigma\Delta W + \frac{1}{2}\sigma\sigma'((\Delta W)^2 - h)
$$

核心證物二：雙重 Itô 積分的閉式， $E[(\Delta W)^2] = h$ ：

$$
\int_t^{t+h}\int_t^s dW_u dW_s = \frac{1}{2}((\Delta W)^2 - h)
$$

核心證物三：強一階判據， $C$ 為與 $h$ 無關的常數：

$$
E[|X_T - X_N|] \le C h
$$

辦案工具箱：

| 工具 | 用途 | 備註 |
|------|------|------|
| Itô–Taylor 展開 | 定位截斷誤差階數 | 強弱階的鑑識手冊 |
| 強收斂斜率實驗 | 固定布朗路徑減半 $h$ | 對應 `_code/1975-milstein_order.py` |
| 自動微分 | 計算 $\sigma'$ | 高維時省去手推 |
| Lévy 面積模擬 | 非交換多維噪聲必備 | 通往粗糙路徑的門 |

接案提示：取幾何布朗運動為試金石， $\sigma(x) = \sigma x$ 使 $\sigma' = \sigma$ ，對比 Euler 與 Milstein 的強誤差斜率，可見 $1/2$ 與 $1$ 的分岔。

## 補充：程式實作

### 對應程式

本節對應程式為 [1975-milstein_order.py](_code/1975-milstein_order.py) 。

### 理論呼應

本文核心迭代為 $X_{n+1} = X_n + b h + \sigma \Delta W + \frac{1}{2} \sigma \sigma^{\prime} ((\Delta W)^2 - h)$ ，其中 $h$ 為步長且 $\Delta W$ 服從常態分佈。
新增修正項補上雙重隨機積分 $I = \frac{1}{2} ((\Delta W)^2 - h)$ ，其期望滿足 $E[(\Delta W)^2] = h$ 故均值為零。
程式以同一組布朗路徑比較 Euler 法與 Milstein 法的強誤差 $E[|X_T - X_N|]$ ，驗證斜率由 $1/2$ 提升至 $1$ 。
加性噪聲下因 $\sigma^{\prime} = 0$ 使修正項消失，兩格式重合，此邊界情形亦可由本程式的擴散設定加以理解。

### 執行方式

在本文所在目錄執行 `python3 _code/1975-milstein_order.py` 。

### 實測輸出

本次實測以細網格 Milstein 解為參考解，測得 Euler 誤差在步長 0.04 至 0.005 依序為 0.032773、0.021756、0.014506、0.010119。
對應 Milstein 誤差依序為 0.007186、0.003307、0.001572、0.000745。
對數對數迴歸斜率 Euler 為 0.567，Milstein 為 1.088，通過 Milstein 斜率介於 0.8 至 1.2 的驗證門檻。

### 讀者實驗

可將路徑數 $M$ 由 8000 改為 2000，再觀察 Euler 與 Milstein 的斜率是否依然分岔。

完整程式如下：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""1975 Milstein 強收斂階（對應 wiki：Milstein 方法 / Euler–Maruyama 強誤差階）。
SDE：dX = -X^3 dt + X dW（漂移 a=-x^3，擴散 b=x，b'=1，
Milstein 修正項 0.5*b*b'*(dW^2-dt) = 0.5*X*((dW)^2-dt) 明顯非零）。
無解析解，故以細網格 Milstein 解為參考解 X_ref，
同一組布朗路徑下比較 dt=[0.04,0.02,0.01,0.005] 的強誤差
  E|X_T^{scheme} - X_ref|，log-log 斜率 Milstein 應 ≈1.0。
只用 numpy，固定種子，不畫圖。
"""
import numpy as np
import time

t0 = time.time()
SEED = 1975
np.random.seed(SEED)

X0, T = 0.5, 1.0
M = 8000
N_fine = 1600
dt_fine = T / N_fine
dts = np.array([0.04, 0.02, 0.01, 0.005])


def step_euler(x, dw, dt):
    return x - x ** 3 * dt + x * dw


def step_milstein(x, dw, dt):
    return x - x ** 3 * dt + x * dw + 0.5 * x * (dw ** 2 - dt)


# 同一路徑：先產生細網格增量
dW_fine = np.sqrt(dt_fine) * np.random.randn(M, N_fine)

# 參考解：細網格 Milstein
X_ref = np.full(M, X0)
for j in range(N_fine):
    X_ref = step_milstein(X_ref, dW_fine[:, j], dt_fine)

err_e, err_m = [], []
for dt in dts:
    Nc = int(round(T / dt))
    block = N_fine // Nc
    dW = dW_fine.reshape(M, Nc, block).sum(axis=2)  # 同路徑粗化
    Xe = np.full(M, X0)
    Xm = np.full(M, X0)
    for j in range(Nc):
        dw = dW[:, j]
        Xe = step_euler(Xe, dw, dt)
        Xm = step_milstein(Xm, dw, dt)
    err_e.append(float(np.mean(np.abs(Xe - X_ref))))
    err_m.append(float(np.mean(np.abs(Xm - X_ref))))

err_e = np.array(err_e)
err_m = np.array(err_m)
slope_e = float(np.polyfit(np.log(dts), np.log(err_e), 1)[0])
slope_m = float(np.polyfit(np.log(dts), np.log(err_m), 1)[0])

print(f"[milstein] seed={SEED} M={M} SDE dX=-X^3*dt+X*dW X0={X0} T={T} N_fine={N_fine}")
for dt, ee, em in zip(dts, err_e, err_m):
    print(f"[milstein] dt={dt:.4f} Euler_err={ee:.6f} Milstein_err={em:.6f}")
print(f"[milstein] slope Euler={slope_e:.3f} (expect ~0.5), Milstein={slope_m:.3f} (expect ~1.0)")
print(f"[milstein] elapsed {time.time()-t0:.2f}s")

assert 0.8 <= slope_m <= 1.2, f"Milstein slope {slope_m} not in [0.8,1.2]"
print(f"VERIFY: milstein slope={slope_m:.3f} in [0.8,1.2] PASS")
```
