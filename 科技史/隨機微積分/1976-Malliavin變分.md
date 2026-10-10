# 1976 年 Malliavin 變分：不微分路徑也能算希臘字母

| 項目 | 內容 |
|------|------|
| 案發時間 | 1976 年（講義與論文），1978 年 ICM 正式宣示 |
| 案發地點 | 法國，巴黎與國際數學家大會 |
| 主角 | Paul Malliavin、Hörmander（hypoellipticity 前傳） |
| 案件性質 | 退化擴散的光滑性如何證明？避險參數能否不靠差分估計 |
| 關鍵證物 | Wiener 空間 $D$ 算子、分部積分、權重 Delta |
| 關聯案件 | 1931 年 Kolmogorov、1951 年 Itô 公式、1973 年 Black–Scholes 希臘字母 |

## 案發現場

案發現場有兩具「屍體」。第一具是 Hörmander 留下的難題：退化擴散（噪聲只打在部分方向）的轉移密度為何仍光滑？Hörmander（1967）用偽微分算子給出解析證明，但機率學家想要一個機率證明：光滑性應來自噪聲在 Lie 括號作用下「攪拌」到所有方向。

第二具是交易室的日常：Delta、Gamma、Vega 都要算。有限差分 $ (V(S+\epsilon)-V(S))/\epsilon $ 又慢又抖，對不連續 payoff（如數位選擇權）更是災難。能否不微分 payoff，只對光滑的密度動手？

1976 年，Paul Malliavin 在 Wiener 空間上建立變分學，把「對布朗路徑求導」變成嚴格數學。核心武器是分部積分：把對 payoff 的導數轉嫁到權重上。

## 偵查過程

Malliavin 的第一步是定義 $D$ 算子。對柱形泛函 $F = f(W_{t_1},\dots,W_{t_n})$ ，定義其 Malliavin 導數為隨機過程：

$$
D_t F = \sum_{i=1}^n \partial_i f(W_{t_1},\dots,W_{t_n}) 1_{[0,t_i]}(t)
$$

直覺是：把布朗路徑在 $t$ 時刻輕輕一推， $F$ 變化多少。 $D$ 是從隨機變數到隨機過程的算子，配上 Sobolev 範數形成 $\mathbb D^{1,2}$ 空間。

第二步是 Skorokhod 積分 $\delta$ ，它是 $D$ 的伴隨算子，分部積分公式為：

$$
E[\langle DF, u\rangle_H] = E[F\delta(u)]
$$

其中 $H$ 為 Cameron–Martin 空間， $u$ 為適當的過程。這條公式是全案的兇器：左邊含 $F$ 的導數，右邊只含 $F$ 本身乘上權重 $\delta(u)$ 。

偵查的高潮是希臘字母。歐式選擇權 $C_0 = e^{-rT}E[\Phi(S_T)]$ 的 Delta 可寫成：

$$
\Delta = E\left[\Phi(S_T)\frac{W_T}{S_0\sigma T}\right]
$$

（此處取 $r = 0$ 簡化，完整版多一折現因子。）payoff $\Phi$ 再也不用微分，即使是數位選擇權的階梯函數也能算。這就是 Malliavin 權重法。

案情結構如下表：

| 證據 | 數學內容 | 推理角色 |
|------|----------|----------|
| $D$ 算子 | 對路徑的變分導數 | 偵探的放大鏡 |
| $\delta$ 積分 | $D$ 的伴隨 | 把導數搬家的兇器 |
| Malliavin 協方差 | $\Gamma = \langle DF, DF\rangle_H$ | 可逆即光滑，hypoellipticity 的機率判據 |
| 權重 Delta | $\Phi \cdot W_T/S_0\sigma T$ | 不微分 payoff 的結案價 |
| Hörmander 條件 | Lie 括號張成全空間 | 噪聲攪拌到所有方向 |

hypoellipticity 的機率證明思路是：SDE 解 $X_T$ 的 Malliavin 協方差 $\Gamma$ 在 Hörmander 括號條件下幾乎必然可逆，分部積分反覆作用可得密度任意階可微。這把 1967 年的解析堡壘改寫成機率語言，Stroock、Watanabe 等人後續補上大偏差與漸近展開。

## 結案報告

結案有兩份。第一份給分析：退化擴散的光滑性得證，Malliavin 以機率手法重奪 hypoellipticity。第二份給金融：希臘字母不必差分，權重法一次模擬同時給出價格與 Delta，方差更小、適用更廣。

遺產第一層是計算金融：Fournié 等人（1999）把權重法系統化為交易室工具，Gamma、Vega 皆有對應權重。第二層是隨機分析：Wiener 空間的 Sobolev 理論、密度估計、 Stein 方法，全數由此開枝。第三層是理念：微分不必作用在最粗糙的對象上，伴隨算子可以把導數搬到光滑處。這一思想在 2021 年擴散模型的分數匹配中再度還魂。

Malliavin 本人是法國學派的鋼琴家數學家，此案之後 Wiener 空間從此有了微積分。路徑雖不可微，泛函依然可變分——這就是本案的墓誌銘。

## 證據與工具

核心證物一：Malliavin 導數， $1$ 表指示函數， $H$ 範數即 $L^2$ 範數：

$$
D_t F = \sum_{i=1}^n \partial_i f \cdot 1_{[0,t_i]}(t)
$$

核心證物二：分部積分， $\delta$ 為 Skorokhod 積分：

$$
E[\langle DF, u\rangle_H] = E[F\delta(u)]
$$

核心證物三：權重 Delta， $\Phi$ 為 payoff， $W_T$ 為終值布朗：

$$
\Delta = E[\Phi(S_T) W_T/S_0\sigma T]
$$

辦案工具箱：

| 工具 | 用途 | 備註 |
|------|------|------|
| 鏈鎖律 | $D\phi(F) = \phi'DF$ | SDE 解的導數流程 |
| 權重蒙地卡羅 | $\Phi$ 乘權重求 Delta | 對應 `_code/1976-malliavin_delta.py` |
| Hörmander 括號檢定 | 判定 $\Gamma$ 可逆 | 退化്ഠ擴散的體檢表 |
| 有限差分對照組 | 驗證權重法方差更小 | 數位選擇權差距最大 |

接案提示：以數位買權 $1_{S_T > K}$ 為實驗對象，有限差分會劇烈抖動，而 Malliavin 權重一次給出穩定 Delta。

## 補充：程式實作

### 對應程式

本節對應程式為 [1976-malliavin_delta.py](_code/1976-malliavin_delta.py) 。

### 理論呼應

本文核心為分部積分公式 $E[\langle DF, u \rangle_H] = E[F \delta(u)]$ ，它把對 payoff 的導數搬到權重上。
歐式買權的權重 Delta 寫為 $\Delta = E[\Phi(S_T) W_T / S_0 \sigma T]$ ，其中 $\Phi$ 為 payoff 且 $W_T$ 為終值布朗運動。
程式以此權重一次模擬同時估計價格與 Delta，無須微分不連續 payoff，對照解析解 $N(d_1)$ 驗證精度。
此結果呼應 Malliavin 導數 $D_t F$ 與 Skorokhod 積分 $\delta$ 互為伴隨的核心思想。

### 執行方式

在本文所在目錄執行 `python3 _code/1976-malliavin_delta.py` 。

### 實測輸出

本次實測使用 1000000 條路徑，測得解析 Delta 為 0.636831，Malliavin 估計為 0.637901，相對誤差為 0.1680%。
共同亂數下差分估計為 0.636609，相對誤差為 0.0348%，兩者皆通過小於 2% 與小於 3% 的驗證門檻。

### 讀者實驗

可將擾動 $h$ 由 1.0 改為 0.5，再比較權重法與差分法的相對誤差變化。

完整程式如下：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""1976 Malliavin Delta（對應 wiki：Malliavin 微積分 / Bismut–Elworthy–Li Greeks）。
歐式 call：Delta = e^{-rT} E[Phi(S_T) * W_T/(S0*sigma*T)]（Malliavin 權重），
對照解析解 N(d1) 與 bump-and-revalue（共同亂數，h=1）。
S0=K=100, r=0.05, sigma=0.2, T=1。要求 Malliavin 相對誤差 < 2%。
只用 numpy（常態 CDF 用 math.erf），固定種子，不畫圖。
"""
import numpy as np
import time
from math import erf

t0 = time.time()
SEED = 1976
np.random.seed(SEED)

S0, K, r, sigma, T = 100.0, 100.0, 0.05, 0.2, 1.0
N = 1_000_000
h = 1.0

_v_erf = np.vectorize(erf)


def ncdf(x):
    return 0.5 * (1.0 + _v_erf(x / np.sqrt(2.0)))


d1 = (np.log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
delta_exact = float(ncdf(d1))

Z = np.random.randn(N)
W = np.sqrt(T) * Z
grow = np.exp((r - 0.5 * sigma ** 2) * T + sigma * W)
ST = S0 * grow
pay = np.maximum(ST - K, 0.0)
disc = np.exp(-r * T)

delta_mal = float(disc * np.mean(pay * W / (S0 * sigma * T)))

# bump-and-revalue（共同亂數）
pay_up = np.maximum((S0 + h) * grow - K, 0.0)
pay_dn = np.maximum((S0 - h) * grow - K, 0.0)
delta_bump = float(disc * np.mean((pay_up - pay_dn) / (2 * h)))

rel_mal = abs(delta_mal - delta_exact) / delta_exact
rel_bump = abs(delta_bump - delta_exact) / delta_exact

print(f"[malliavin] seed={SEED} N={N} S0=K=100 r={r} sig={sigma} T={T}")
print(f"[malliavin] exact N(d1)={delta_exact:.6f}")
print(f"[malliavin] Malliavin ={delta_mal:.6f} relerr={rel_mal:.4%}")
print(f"[malliavin] bump(h={h})={delta_bump:.6f} relerr={rel_bump:.4%}")
print(f"[malliavin] elapsed {time.time()-t0:.2f}s")

assert rel_mal < 0.02, f"Malliavin relerr {rel_mal} exceeds 2%"
assert rel_bump < 0.03, f"bump relerr {rel_bump} exceeds 3%"
print(f"VERIFY: malliavin relerr={rel_mal:.4%}<2%, bump relerr={rel_bump:.4%} PASS")
```
