# 1973 年 Black–Scholes 公式：華爾街的封神與詛咒

| 項目 | 內容 |
|------|------|
| 案發時間 | 1973 年（論文刊登），芝加哥選擇權交易所同年開業 |
| 案發地點 | 芝加哥大學、MIT，交織華爾街交易大廳 |
| 主角 | Fischer Black、Myron Scholes、Robert Merton |
| 案件性質 | 選擇權該賣多少錢？投機定價能否像物理定律一樣寫成 PDE |
| 關鍵證物 | 幾何布朗運動、對沖 PDE、 $N(d_1)-Ke^{-rT}N(d_2)$ |
| 關聯案件 | 1900 年 Bachelier、1960 年 Girsanov、1979 年鞅定價、1997 年 Nobel 獎 |

## 案發現場

1973 年，芝加哥選擇權交易所開張，選擇權第一次像股票一樣集中交易。但沒人知道一張買權到底值多少。報價靠喊，靠膽量，靠 Bachelier 留下的古老算術布朗公式勉強撐場。

案發現場的數學假設由三人寫下。股價服從幾何布朗運動：

$$
dS_t = \mu S_t dt + \sigma S_t dW_t
$$

其中 $\mu$ 為漂移， $\sigma$ 為波動率， $W_t$ 為布朗運動。無風險利率為 $r$ ，選擇權價格記為 $V(S,t)$ ，到期 payoff 為 $\Phi(S_T)$ 。

謎面是：漂移 $\mu$ 人人看法不同，定價豈不人言人殊？若價格依賴主觀的 $\mu$ ，交易所的公允價從何而來？

Black 是應用數學家轉行的顧問，Scholes 是計量經濟學家，Merton 是連續時間金融的數學大腦。三人幾乎同時意識到：選擇權可以用股票與債券「複製」，複製的成本就是公允價，而複製過程中 $\mu$ 會神秘消失。

## 偵查過程

偵查的第一步是構造對沖組合。持有 $\Delta$ 單位股票、空頭一單位選擇權，組合價值為 $\Pi = \Delta S - V$ 。由 Itô 公式：

$$
dV = \left(V_t + \mu S V_S + \frac{1}{2}\sigma^2 S^2 V_{SS}\right) dt + \sigma S V_S dW_t
$$

取 $\Delta = V_S$ ，則組合中的 $dW_t$ 項恰好相消， $\Pi$ 在瞬間變成無風險組合。無套利要求它賺取無風險利率，於是得到 Black–Scholes PDE：

$$
V_t + r S V_S + \frac{1}{2}\sigma^2 S^2 V_{SS} - rV = 0
$$

注意漂移 $\mu$ 已人間蒸發，取而代之的是 $r$ 。這正是 Girsanov 定理的金融化身：定價測度下漂移被搬成 $r$ 。

第二步是解 PDE。經對數變換 $x = \ln S$ ，方程化為常係數熱方程，可用熱核顯式求解。歐式買權的結案價為：

$$
C = S_0 N(d_1) - K e^{-rT} N(d_2)
$$

其中 $N$ 為標準常態分佈函數，且 $d_1$ 與 $d_2$ 定義為：

$$
d_1 = \frac{\ln(S_0/K) + (r + \sigma^2/2)T}{\sigma\sqrt{T}}
$$

$$
d_2 = d_1 - \sigma\sqrt{T}
$$

偵查筆錄如下表：

| 線索 | 數學角色 | 推理意義 |
|------|----------|----------|
| $\Delta = V_S$ | Delta 對沖 | 殺死隨機項的兇器 |
| PDE 中 $\mu \to r$ | 風險中性化 | 主觀漂移被逐出定價 |
| $N(d_1)$ | 風險中性下履約機率的加權 | 避險比率即 Delta |
| $Ke^{-rT}N(d_2)$ | 履約價現值的期望 | 折現後的或有支付 |
| 熱方程變換 | $x = \ln S$ | 非線性 PDE 化為熱核 |

Merton 同期補上了嚴謹的連續交易數學，並處理美式選擇權與配息。Merton 的版本讓論文從經濟直覺升級為數學定理，也埋下日後鞅定價的引線。

## 結案報告

結案：選擇權的公允價不依賴任何人的主觀預期，只依賴波動率 $\sigma$ 與利率 $r$ 。只要能連續對沖，價格就被鎖死在公式裡。

此案的榮耀在 1997 年抵達：Scholes 與 Merton 獲 Nobel 經濟學獎。但 Black 已於 1995 年因癌症逝世，享年 57 歲。Nobel 不頒給已故者，獎項致辭中特別留下 Black 的名字。這是三人命運的分岔：兩人封神，一人缺席。

遺產的第一層是實務：交易所報價、隱含波動率微笑、Delta 對沖手冊，全數由此衍生。第二層是理論：公式的風險中性內核直接催生 1979 年鞅定價理論， $C_0 = e^{-rT}E_Q[\Phi]$ 成為現代定價的通用語。第三層是警示：1987 年股災與 1998 年 LTCM 崩盤都暴露了常數波動、連續交易假設的脆弱，Heston 隨機波動（1993）與粗糙波動（2014）都是後續的補救。

封神之作也是詛咒之源。公式越好用，市場越忘記它的假設。這正是本案留給後世的最後一句證詞。

## 證據與工具

核心證物一：風險中性下的股價動態， $W_t^Q$ 為 $Q$ 下布朗運動：

$$
dS_t = r S_t dt + \sigma S_t dW_t^Q
$$

核心證物二：Black–Scholes PDE， $V_t$ 表時間導數， $V_S$ 表 Delta：

$$
V_t + r S V_S + \frac{1}{2}\sigma^2 S^2 V_{SS} - rV = 0
$$

核心證物三：歐式買權公式， $N$ 表標準常態累積函數：

$$
C = S_0 N(d_1) - K e^{-rT} N(d_2)
$$

辦案工具箱：

| 工具 | 用途 | 備註 |
|------|------|------|
| Delta 對沖模擬 | 驗證複製組合追蹤 payoff | 離散對沖留有誤差 |
| 蒙地卡羅定價 | 以 $Q$ 期望驗證公式 | 對應 `_code/1973-black_scholes_mc.py` |
| 隱含波動率反解 | 由市價倒求 $\sigma$ | 實務報價語言 |
| CRR 二項樹 | 離散逼近連續公式 | 1979 年案件的伏筆 |

接案提示：固定 $S_0 = 100$ 、 $K = 100$ 、 $r = 0.05$ 、 $\sigma = 0.2$ 、 $T = 1$ ，以十萬條路徑做風險中性蒙地卡羅，誤差可壓至 $1\%$ 以內。

## 補充：程式實作

### 對應程式

本節對應程式為 [1973-black_scholes_mc.py](_code/1973-black_scholes_mc.py) 。

### 理論呼應

本文核心公式為歐式買權定價式 $C = S_0 N(d_1) - K e^{-rT} N(d_2)$ ，其中 $d_1$ 與 $d_2$ 由利率 $r$ 與波動率 $\sigma$ 決定。
程式在風險中性動態 $dS_t = r S_t dt + \sigma S_t dW_t^Q$ 下模擬終值 $S_T$ ，再以折現期望 $C_0 = e^{-rT} E_Q[\Phi(S_T)]$ 估計價格。
此流程正是 Black–Scholes 偏微分方程 $V_t + r S V_S + \frac{1}{2} \sigma^2 S^2 V_{SS} - rV = 0$ 的機率對偶驗證。
當路徑數趨於無窮時，蒙地卡羅估計收斂至封閉解，體現主觀漂移 $\mu$ 被 $r$ 取代的風險中性精神。

### 執行方式

在本文所在目錄執行 `python3 _code/1973-black_scholes_mc.py` 。

### 實測輸出

本次實測使用 300000 條路徑，種子為 1973，測得買權蒙地卡羅價格為 10.46858，封閉解為 10.45058，相對誤差為 0.1722%。
賣權蒙地卡羅價格為 5.56347，封閉解為 5.57353，相對誤差為 0.1805%。
買賣權平價差為 4.90511，理論值為 4.87706，絕對誤差為 0.02805，通過小於 1% 與小於 0.15 的驗證門檻。

### 讀者實驗

可將波動率 $\sigma$ 由 0.2 改為 0.4，再比較蒙地卡羅價格與封閉解是否依然吻合。

完整程式如下：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""1973 Black-Scholes 蒙地卡羅（對應 wiki：Black-Scholes 模型 / 1973 年 BS 論文）。
S0=100, K=100, r=0.05, sigma=0.2, T=1。風險中性下
  S_T = S0*exp((r-s^2/2)T + s*sqrt(T)*Z)。
用 30 萬條路徑估 call/put，驗證：
  (1) MC call 與 BS 封閉解相對誤差 < 1%；
  (2) put-call parity：C_mc - P_mc ≈ S0 - K*exp(-rT)。
只用 numpy（常態 CDF 用 math.erf），固定種子，不畫圖。
"""
import numpy as np
import time
from math import erf

t0 = time.time()
SEED = 1973
np.random.seed(SEED)

S0, K, r, sigma, T = 100.0, 100.0, 0.05, 0.2, 1.0
M = 300_000

_v_erf = np.vectorize(erf)


def ncdf(x):
    return 0.5 * (1.0 + _v_erf(x / np.sqrt(2.0)))


d1 = (np.log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)
C_bs = float(S0 * ncdf(d1) - K * np.exp(-r * T) * ncdf(d2))
P_bs = float(C_bs - (S0 - K * np.exp(-r * T)))  # parity 反解

Z = np.random.randn(M)
ST = S0 * np.exp((r - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * Z)
disc = np.exp(-r * T)
C_mc = float(disc * np.mean(np.maximum(ST - K, 0.0)))
P_mc = float(disc * np.mean(np.maximum(K - ST, 0.0)))

parity_theory = S0 - K * np.exp(-r * T)
parity_mc = C_mc - P_mc
rel_call = abs(C_mc - C_bs) / C_bs
parity_err = abs(parity_mc - parity_theory)

print(f"[bsmc] seed={SEED} M={M} S0={S0} K={K} r={r} sig={sigma} T={T}")
print(f"[bsmc] call: MC={C_mc:.5f} BS={C_bs:.5f} relerr={rel_call:.4%}")
print(f"[bsmc] put : MC={P_mc:.5f} BS={P_bs:.5f} relerr={abs(P_mc-P_bs)/P_bs:.4%}")
print(f"[bsmc] parity: MC_diff={parity_mc:.5f} theory={parity_theory:.5f} abserr={parity_err:.5f}")
print(f"[bsmc] elapsed {time.time()-t0:.2f}s")

assert rel_call < 0.01, f"call relerr {rel_call} exceeds 1%"
assert parity_err < 0.15, f"parity abserr {parity_err} too large"
print(f"VERIFY: bsmc call_relerr={rel_call:.4%}<1%, parity_err={parity_err:.4f} PASS")
```
