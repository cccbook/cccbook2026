# 1992・Kloeden–Platen 數值聖經：SDE 數值解的大一統

> 「解析解是神的語言，數值格式是凡人的梯子。」
> 本案時間：1992 年（1999 年再版加冕），地點：澳洲與德國，報案人：所有算不出解析解的工程師。

| 案件檔案 | 內容 |
|----------|------|
| 案號 | NP-1992-KP |
| 年份 | 1992 年初版，1999 年修訂再版 |
| 主角 | Peter Kloeden、Eckhard Platen |
| 關鍵文獻 | Numerical Solution of Stochastic Differential Equations（1992） |
| 涉案對象 | Euler–Maruyama 格式、Milstein 格式、強收斂、弱收斂 |
| 核心證物 | 強／弱 Taylor 展開、Platen–Wagner 展開、階數障壁定理 |
| 關聯舊案 | 1955 年 Maruyama 格式、1975 年 Milstein 格式、1960 年 Kalman 濾波 |
| 遺產 | 計算金融、粒子濾波實作、神經 SDE 訓練的格式地基 |

## 案發現場

1990 年代初，SDE 數值圈是一座沒有地圖的叢林。

每個實驗室都有自己的格式：Euler–Maruyama 簡單但慢，Milstein 加了修正項卻只在特定噪聲下漂亮，高階 Runge–Kutta 眾說紛紜。有人用步長  $h$  吹噓精度，有人用樣本數  $N$  掩飾偏差。更亂的是，強收斂與弱收斂被混為一談：追蹤一條軌跡的誤差，和估計一個期望值的誤差，根本是兩樁不同的案子。

當時的受害者是計算金融與工程。選擇權定價要的是期望，誤差量的是弱收斂；濾波與控制要的是路徑，誤差量的是強收斂。沒有統一理論，審稿人只能各憑信仰判案。

Kloeden 與 Platen 決定編一本法典。他們的野心毫不掩飾：把 Itô–Taylor 展開、Stratonovich–Taylor 展開、多重隨機積分、階數條件，全部寫進同一套符號系統。這本書 1992 年初版逾六百頁，1999 年再版修訂，從此被稱為「數值聖經」。

## 偵查過程

偵探的第一步，是區分兩種正義：強收斂追路徑，弱收斂追分佈。

設步長為  $h$ ，數值解為  $\bar X$ ，真解為  $X$ 。強收斂量均方路徑誤差，弱收斂量光滑泛函期望誤差：

$$
\mathbb{E}\lvert X_T - \bar X_T\rvert \le C\,h^{\gamma}
$$

$$
\lvert \mathbb{E}[g(X_T)] - \mathbb{E}[g(\bar X_T)]\rvert \le C\,h^{\beta}
$$

其中  $\gamma$  為強階， $\beta$  為弱階。Euler–Maruyama 的強階只有  $1/2$ ，弱階卻有  $1$ 。一句話：算期望比跟軌跡容易一倍。

第二步是解剖 Itô–Taylor 展開。古典 Taylor 按  $h$  的整數次展開，隨機 Taylor 還要按多重隨機積分展開。記  $I_{\alpha}$  為指標  $\alpha$  對應的多重積分，則：

$$
X_t = X_0 + \sum_{\alpha} c_{\alpha}(X_0)\,I_{\alpha}(t)
$$

截斷這級數，就得到不同階數的格式。Euler–Maruyama 只留到  $I_{(0)}$  與  $I_{(1)}$ ；Milstein 多留一項  $I_{(1,1)}$ ，強階從  $1/2$  升到  $1$ 。

下表是格式的身分證，也是聖經最常被翻開的一頁：

| 格式 | 強階  $\gamma$  | 弱階  $\beta$  | 關鍵增項 | 代價 |
|------|----------------|----------------|----------|------|
| Euler–Maruyama |  $1/2$  |  $1$  | 無 | 最省，每步一次正態 |
| Milstein |  $1$  |  $1$  |  $\tfrac{1}{2}b b'((\Delta W)^2 - h)$  | 需導數或差商 |
| 強 Taylor 1.5 |  $3/2$  |  $2$  | 含  $I_{(1,0)}$  等雙重積分 | 需模擬 Lévy 面積 |
| 弱 Taylor 2.0 | — |  $2$  | 矩匹配的三點分佈可代正態 | 省隨機數，宜定價 |

第三步是本案的法醫高潮：階數障壁與 Platen–Wagner 展開。當噪聲為多維且非交換時，高階格式需要模擬 Lévy 面積  $A_{ij}$ ，其密度無初等閉式。Platen–Wagner 展開把層級結構講透：想跨過強階  $1$  的門檻，就必須面對面積；想繞開，就只能退守弱格式，用矩匹配的三點隨機數蒙混過關。

聖經還釐清了穩定性。均方穩定域、剛性 SDE 的隱式格式、外插加速，皆有專章。隱式 Euler 對付剛性漂移，恰如古典 ODE 世界的隱式格式翻版，只是穩定條件多了擴散項的貢獻。

1992 初版建立法典，1999 再版增補習題、勘誤與新格式。兩版相加，引用數以萬計，至今仍是審稿人手中的量刑基準。

## 結案報告

1992 年一案沒有發明單一格式，它發明的是度量衡。

從此以後，任何新格式都必須報上戶口：強階多少、弱階多少、在什麼噪聲結構下成立、每步成本多少。宣稱「高階」卻不提 Lévy 面積的，一律視為口供不實。

遺產遍地開花。計算金融的定價引擎、粒子濾波的傳播步驟、神經 SDE 的前向求解器，腳下踩的都是這本聖經。2017 年 Deep BSDE 與 2018 年 Neural SDE 看似新潮，其反向傳播穿過的，正是 Kloeden–Platen 整理過的離散格式。

在歷史年表裡，本案上承 1955 年 Maruyama 與 1975 年 Milstein，下接一切需要動手算的後續。理論家負責破案，數值家負責讓真相可以在電腦裡重演。

案件狀態：法典生效，凡動手模擬者皆為其子民。

## 證據與工具

證物一，Euler–Maruyama 與 Milstein 的並排虛擬碼。設步長  $h$ ，增量  $\Delta W \sim \mathcal{N}(0, h)$ ，漂移  $a$ ，擴散  $b$ ：

$$
\bar X_{n+1} = \bar X_n + a\,h + b\,\Delta W \quad \text{(Euler)}
$$

$$
\bar X_{n+1} = \bar X_n + a\,h + b\,\Delta W + \tfrac{1}{2}b b'((\Delta W)^2 - h) \quad \text{(Milstein)}
$$

證物二，收斂階速查與選型指南：

| 任務 | 推薦格式 | 理由 |
|------|----------|------|
| 畫軌跡、算強誤差 | Milstein 或強 1.5 | 強階優先，面積跑不掉就認了 |
| 算選擇權價格 | 弱 2.0 或外插 Euler | 弱階便宜，三點分佈更快 |
| 剛性漂移 | 隱式 Euler–Maruyama | 穩定壓倒精度 |
| 高維系統 | 簡化弱格式 | 成本隨維度線性化 |

證物三，動手實驗。對應程式  `_code/1955-euler_maruyama_order.py`  驗證強階  $1/2$ ， `_code/1975-milstein_order.py`  驗證強階  $1$ 。讀者可把步長折半四次，以 log–log 圖量斜率，親自為聖經驗明正身。

探員格言：先問強弱，再問階數，最後才問步長。不分強弱就調參者，如同不驗屍就結案。

## 補充：程式實作

### 對應程式

- [1955-euler_maruyama_order.py](_code/1955-euler_maruyama_order.py)：以幾何布朗運動驗證 Euler–Maruyama 強階 $1/2$ 。
- [1975-milstein_order.py](_code/1975-milstein_order.py)：以三次漂移乘性噪聲模型驗證 Milstein 強階 $1$ ，並同場附帶 Euler 對照組；兩支合起來即聖經核心對照表 EM 半階對 Milstein 一階。

### 理論呼應

聖經以強誤差 $E[\lvert X_T - \bar X_T\rvert] \le C\,h^{\gamma}$ 定義強階 $\gamma$ ，弱誤差以 $\lvert E[g(X_T)] - E[g(\bar X_T)]\rvert$ 另計。
Euler–Maruyama 只留到 $I_{(0)}$ 與 $I_{(1)}$ ，故在乘性噪聲下強階僅為 $\gamma = 1/2$ ，弱階卻有 $1$ 。
Milstein 多留一項 $I_{(1,1)}$ ，對應修正項 $\tfrac{1}{2}bb'((\Delta W)^2 - h)$ ，把強階拉到 $\gamma = 1$ 。
兩支程式皆以 log–log 斜率量測 $\gamma$ ，正是聖經要求新格式報戶口的標準動作。

### 執行方式

在 `隨機微積分` 目錄下分別執行 `python3 _code/1955-euler_maruyama_order.py` 與 `python3 _code/1975-milstein_order.py` 。

### 實測輸出

Euler–Maruyama（GBM， $h = 0.04, 0.02, 0.01$ ）：

```text
h=0.040 N=25 strong_err=0.403264
h=0.020 N=50 strong_err=0.286254
h=0.010 N=100 strong_err=0.196632
errors=['0.403264', '0.286254', '0.196632']
log-log slope=0.5181 (theory 0.5)
VERIFY 1955 Euler-Maruyama strong order: slope=0.5181 in [0.35,0.65] PASS
```

Milstein（ $dX = -X^3\,dt + X\,dW$ ， $dt = 0.04, 0.02, 0.01, 0.005$ ）：

```text
[milstein] seed=1975 M=8000 SDE dX=-X^3*dt+X*dW X0=0.5 T=1.0 N_fine=1600
[milstein] dt=0.0400 Euler_err=0.032773 Milstein_err=0.007186
[milstein] dt=0.0200 Euler_err=0.021756 Milstein_err=0.003307
[milstein] dt=0.0100 Euler_err=0.014506 Milstein_err=0.001572
[milstein] dt=0.0050 Euler_err=0.010119 Milstein_err=0.000745
[milstein] slope Euler=0.567 (expect ~0.5), Milstein=1.088 (expect ~1.0)
[milstein] elapsed 0.55s
VERIFY: milstein slope=1.088 in [0.8,1.2] PASS
```

### 讀者實驗

將 Euler 程式的步長表 `h_list` 加一格 0.005，或將 Milstein 程式的粒子數 `M` 由 8000 改為 16000，再看兩條斜率是否仍分守 $0.5$ 與 $1.0$ 附近。

完整程式如下：

[1955-euler_maruyama_order.py](_code/1955-euler_maruyama_order.py) 全文：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""1955 Euler-Maruyama 強收斂階對應 wiki 說明
對應 wiki：1955 年 Skorokhod / Euler-Maruyama 方法，強階 0.5（弱階 1.0）。
註：OU 為加性噪音，EM 強階實際是 1.0（與 Milstein 重合），無法展示 0.5；
本程式改用同樣有精確解的 GBM（乘性噪音 dS = mu*S dt + sigma*S dW），
以同布朗路徑比較 EM 終值強誤差 e(h) = (E|S_T - S^h_T|^2)^{1/2} ~ C*h^{0.5}。
h=[0.04,0.02,0.01] 共用布朗增量，精確解 S_T = S0*exp((mu-s^2/2)T + s*W_T)，
log-log 斜率約 0.5。
規範：只用 numpy，固定種子，不畫圖只印數字，結尾印 VERIFY 並用 assert 把關。
"""
import numpy as np

np.random.seed(11)

mu = 0.5
sigma = 1.0
S0 = 1.0
T = 1.0
h_list = [0.04, 0.02, 0.01]
h_ref = 0.001
M = 20000

N_ref = int(round(T / h_ref))
dW_fine = np.sqrt(h_ref) * np.random.randn(M, N_ref)
W_T = dW_fine.sum(axis=1)
S_exact = S0 * np.exp((mu - 0.5 * sigma ** 2) * T + sigma * W_T)

errors = []
for h in h_list:
    k = int(round(h / h_ref))
    N_c = int(round(T / h))
    dW_c = dW_fine.reshape(M, N_c, k).sum(axis=2)
    S = np.full(M, S0)
    for j in range(N_c):
        S = S + mu * S * h + sigma * S * dW_c[:, j]
    err = float(np.sqrt(np.mean((S - S_exact) ** 2)))
    errors.append(err)
    print(f"h={h:.3f} N={N_c} strong_err={err:.6f}")

logh = np.log(h_list)
loge = np.log(errors)
slope = float(np.polyfit(logh, loge, 1)[0])
print(f"errors={['%.6f' % e for e in errors]}")
print(f"log-log slope={slope:.4f} (theory 0.5)")

assert 0.35 <= slope <= 0.65, f"slope {slope} outside [0.35, 0.65]"
print(f"VERIFY 1955 Euler-Maruyama strong order: slope={slope:.4f} in [0.35,0.65] PASS")
```

[1975-milstein_order.py](_code/1975-milstein_order.py) 全文：

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
