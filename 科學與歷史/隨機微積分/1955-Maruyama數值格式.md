# 1955 年丸山格式：第一個敢把布朗運動放進計算機的男人

| 項目 | 內容 |
|------|------|
| 案發時間 | 1955 年 |
| 案發地點 | 日本北海道大學 |
| 主角 | 丸山儀四郎（Gisiro Maruyama） |
| 案件性質 | SDE 沒有解析解，計算機卻已誕生，數值解從何而來 |
| 關鍵證物 | Euler–Maruyama 格式，強 1/2 階、弱 1 階 |
| 關聯案件 | 1951 年 Itô 公式、1975 年 Milstein 格式、1992 年 Kloeden–Platen 聖經 |

## 案發現場

時間回到 1955 年。Itô 積分（1942）和 Itô 公式（1951）剛剛落成，隨機微分方程正式成為一門學問。方程可以寫下來了：

$$
dX_t = b(X_t) dt + \sigma(X_t) dW_t
$$

但問題立刻浮現：除了幾何布朗運動、Ornstein–Uhlenbeck 等少數特例外，幾乎沒有 SDE 有解析解。

與此同時，另一條時間線正在逼近。電子計算機剛問世不久，確定性微分方程的 Euler 法早已是工程師的日常工具。一個自然的疑問懸在空中：能不能把 Euler 法搬到隨機世界？

案發現場有三道障礙。第一，布朗增量 $dW_t$ 不是 $dt$ ，它抖得太厲害，路徑處處不可微。第二，Itô 積分是「向前看」的，非預料項的處理稍有不慎就會掉進 Stratonovich 或其他積分的陷阱。第三，當時連「數值格式收斂」該如何定義都不清楚：是路徑對路徑逼近，還是分佈逼近？

在北海道大學的書桌前，丸山儀四郎接下了這樁懸案。

## 偵查過程

丸山的偵查策略出奇地直率：既然確定性 Euler 法是把微分換成差分，那麼隨機版本就把增量換成布朗增量。

設時間切分為 $0 = t_0 < t_1 < \cdots < t_N = T$ ，步長為 $h$ ，記 $X_n \approx X_{t_n}$ ，布朗增量為 $\Delta W_n$ 。丸山寫下：

$$
X_{n+1} = X_n + b(X_n) h + \sigma(X_n) \Delta W_n
$$

其中 $\Delta W_n$ 是獨立同分佈的常態增量，滿足 $\Delta W_n \sim N(0,h)$ 。這就是後世所稱的 Euler–Maruyama 格式。

偵探的第一個問題是： $\Delta W_n$ 的量級是多少？由常態分佈的性質可知，其典型大小為 $\sqrt{h}$ 。也就是說，噪聲項比漂移項 $b h$ 大得多。當 $h = 0.0001$ 時，漂移推進 $0.0001$ ，噪聲卻推進約 $0.01$ 。整個格式的精度註定被噪聲主宰。

丸山進一步追問收斂的意義，並留下後世沿用至今的雙軌制。強收斂看的是路徑誤差的均值，弱收斂看的是期望泛函的誤差：

$$
E[|X_T - X_N|] \le C h^{\gamma}
$$

$$
|E[f(X_T)] - E[f(X_N)]| \le C_f h^{\beta}
$$

其中 $\gamma$ 為強階， $\beta$ 為弱階。

關鍵的偵查筆錄整理如下表：

| 概念 | 定義 | Euler–Maruyama 的階 |
|------|------|---------------------|
| 強收斂 | 路徑層級的 $L^1$ 誤差 | $\gamma = 1/2$ |
| 弱收斂 | 期望 $E[f(X_T)]$ 層級 | $\beta = 1$ |
| 噪聲主導項 | $\sigma \Delta W_n$ 量級 $\sqrt{h}$ | 誤差瓶頸 |
| Itô–Taylor 截斷 | 只保留到 $h$ 與 $\Delta W$ 一次項 | 高階項被丟棄 |

為什麼強階只有 $1/2$ ？偵探在 Itô–Taylor 展開中找到兇器。真解的展開式中藏著雙重隨機積分 $\int \int dW dW$ ，其量級為 $h$ ，但 Euler–Maruyama 直接丟棄了它的漲落細節，只在弱意義下用 $h$ 彌補了均值。這就是強弱分家的原因。

另一個細節是：格式必須是 Itô 解釋下的顯式格式。 $\sigma(X_n)$ 只能用左端點取值，若誤用中點，就會滑向 Stratonovich 世界，漂移項會多出一項修正。這一點丸山在論文中以測度論的嚴謹語言固定下來。

丸山 1955 年的論文發表於北海道大學的數學期刊，標題直白地談論 SDE 解的連續近似。當時引用者寥寥，但證據鏈完整：存在性、近似構造、收斂性，一應俱全。

## 結案報告

本案的結論是：SDE 從此有了第一個可計算的數值解。Euler–Maruyama 格式以強 $1/2$ 階、弱 $1$ 階的精度，將 Itô 的抽象世界接上了計算機的地氣。

此案的遺產有三層。第一，它確立了 SDE 數值分析的雙軌語言：強收斂與弱收斂。第二，它開啟了 Itô–Taylor 展開的高階追兇，二十年後 Milstein（1975）正是在此基礎上加了一項修正，把強階推上 $1$ 。第三，它成為 Kloeden–Platen（1992）數值聖經的起點，所有高階格式都是這條血脈的後裔。

從應用的角度看，沒有丸山格式，就沒有後來的蒙地卡羅定價、粒子濾波模擬、神經 SDE 訓練。每一次用程式跑出 $X_n$ 的軌跡，都是在重演 1955 年的那場推理。

兇手找到了嗎？找到了。限制精度的兇手正是被丟棄的雙重隨機積分。而丸山留下的格式，就是第一張通緝令。

## 證據與工具

核心證物一：Euler–Maruyama 迭代式， $X_n$ 為數值解， $h$ 為步長， $\Delta W_n$ 為布朗增量：

$$
X_{n+1} = X_n + b(X_n) h + \sigma(X_n) \Delta W_n
$$

核心證物二：增量抽樣規則， $Z_n$ 為標準常態變數：

$$
\Delta W_n = \sqrt{h} Z_n
$$

核心證物三：收斂階數判據， $C$ 為與 $h$ 無關的常數：

$$
E[|X_T - X_N|] \le C h^{1/2}
$$

辦案工具箱：

| 工具 | 用途 | 備註 |
|------|------|------|
| Itô–Taylor 展開 | 分析局部截斷誤差 | 強弱階的法醫鑑定書 |
| 蒙地卡羅模擬 | 以大量路徑驗證收斂階 | 對應 `_code/1955-euler_maruyama_order.py` |
| Lipschitz 條件 | 保證解存在唯一與格式穩定 | $b$ 與 $\sigma$ 須滿足 |
| 弱收斂檢定 | 檢驗 $E[f(X_T)]$ 的誤差 | 定價應用只看此項 |

 接案提示：若讀者想親手驗證強 $1/2$ 階，可固定同一批布朗路徑，將 $h$ 逐次減半，觀察路徑誤差的對數斜率是否趨近 $1/2$ 。

## 補充：程式實作

### 對應程式

本節對應 [1955-euler_maruyama_order.py](_code/1955-euler_maruyama_order.py) ，以共用布朗路徑驗證強收斂階。

### 理論呼應

本文核心迭代為 $X_{n+1} = X_n + b(X_n)h + \sigma(X_n)\Delta W_n$ ，其中 $\Delta W_n = \sqrt{h}Z_n$ 量級主導誤差。
強誤差判據為 $E[|X_T-X_N|] \le Ch^{1/2}$ ，弱誤差則為 $1$ 階，程式選乘性噪聲幾何布朗運動以避開加性噪聲退化。
以同一批布朗增量比較 $h = 0.04,0.02,0.01$ 的終值均方誤差，對數斜率還原 $0.5$ 理論值。
實測斜率 $0.5181$ 落在容許區間，證實被丟棄的雙重隨機積分正是精度瓶頸。

### 執行方式

`python3 _code/1955-euler_maruyama_order.py`

### 實測輸出

`h=0.040 N=25 strong_err=0.403264` ， `h=0.020 N=50 strong_err=0.286254` ， `h=0.010 N=100 strong_err=0.196632` ， `log-log slope=0.5181 (theory 0.5)` ， `VERIFY ... PASS` 。

### 讀者實驗

將 $h$ 數列改為 $0.08,0.04,0.02,0.01$ 四點再重跑，觀察對數斜率是否仍穩定趨近 $0.5$ 。

完整程式如下：

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
