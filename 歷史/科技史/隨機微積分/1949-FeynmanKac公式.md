# 1949 年 Feynman–Kac 公式：拋硬幣解熱方程奇案

> 探案代號 ： 量子信使
>
> 一句話案情 ： 物理學家的路徑積分遇上數學家的布朗運動 ， 拋硬幣竟能解偏微分方程 。

**案件檔案**

| 項目 | 內容 |
|------|------|
| 案發時間 | 1947 年偶遇 ， 1949 年 Kac 發表 |
| 案發地點 | Cornell 大學 ， Feynman 與 Kac 的走廊對話 |
| 主角 | Richard Feynman 與 Mark Kac ， 物理直覺遇上機率嚴謹 |
| 核心證物 | 拋硬幣解熱方程 ， 路徑積分即期望值 |
| 涉案人物 | Wiener ， Kolmogorov ， Schrödinger ， Einstein |
| 案件狀態 | 已破案 ， PDE 與機率的橋樑 |
| 關聯案件 | 1931 年 Kolmogorov 後向方程 ， 1942 年 Itô 積分 ， 1990 年 BSDE |

## 案發現場

1947 年的 Cornell 走廊 ， 上演了科學史最傳奇的偶遇 。

Feynman 剛提出路徑積分 ， 主張量子粒子走過所有路徑 ， 每條路徑貢獻一個相位 。

數學家聽了直搖頭 ， 所有路徑求和聽起來像天方夜譚 ， 測度何在 。

Kac 卻眼睛一亮 ， 他正在苦思熱方程的機率解 ， 聽見 Feynman 的演講 ， 立刻嗅到血跡 。

熱方程描述溫度擴散 ， 布朗運動描述粒子亂走 ， 兩者長得太像 ， 不可能是巧合 。

現場留下一道謎題 ： 能否用隨機軌道的平均值 ， 直接寫出偏微分方程的解 。

若真能如此 ， 解 PDE 就不必動用分離變數 ， 拋硬幣模擬即可 。

Kac 把自己關進辦公室 ， 手邊只有 Wiener 測度與 Kolmogorov 後向方程 。

他說 ， Feynman 的瘋狂路徑 ， 在虛時間下就是布朗運動 ， 這樁跨界奇案有解 。

## 偵查過程

偵探先從最單純的熱方程下手 ， 不加位勢 ， 不加漂移 。

設布朗運動為  $W_t$  ， 初值為  $x$  ， 終端酬勞為  $f$  。

定義候選解為期望值  $u(t,x) = E_x[f(W_T)]$  ， 其中下標  $x$  表初值 。

利用布朗增量的高斯性 ， 可驗證  $u$  滿足熱方程 。

$$ \partial_t u + \frac{1}{2}\Delta u = 0 $$

其中終端條件為  $u(T,x) = f(x)$  ， 時間倒著走 。

這正是 1931 年 Kolmogorov 後向方程的特例 ， 漂移為零 ， 擴散為單位矩陣 。

接著加入位勢函數  $V(x)$  ， 案情升級為 Schrödinger 型方程 。

考慮帶殺戮或折現的期望 ， 權重為指數積分 。

$$ u(t,x) = E[ f(X_T) e^{- \int_t^T V(X_s) ds} \mid X_t = x ] $$

其中  $X$  為擴散過程 ， $V$  為位勢 ， 指數項為 Feynman 權重 。

Kac 證明上式滿足下列拋物方程 。

$$ \partial_t u + Lu - Vu = 0 $$

其中  $L$  為生成元 ， $V$  為位勢 ， 終端條件仍為  $u(T,x) = f(x)$  。

若再加入漂移  $b$  與一般擴散  $\sigma$  ， 生成元展開為完整形式 。

$$ L = b \cdot \nabla + \frac{1}{2} \mathrm{tr}( a \nabla^2 ) $$

其中  $a = \sigma\sigma^T$  ， 與 1931 年前向方程互為伴隨 。

偵探用下表整理三種層次的對應 。

| 方程類型 | PDE 形式 | 機率表示  $u$  |
|----------|----------|----------------|
| 純熱方程 |  $\partial_t u + \frac{1}{2}\Delta u = 0$  |  $E_x[f(W_T)]$  |
| 含位勢 |  $\partial_t u + \frac{1}{2}\Delta u - Vu = 0$  |  $E_x[f(W_T)e^{- \int V}]$  |
| 一般擴散 |  $\partial_t u + Lu - Vu = 0$  |  $E_x[f(X_T)e^{- \int V} \mid X_t = x]$  |

證明關鍵有三步 ， 偵探在白板上推演 。

| 步驟 | 動作 | 數學 |
|------|------|------|
| Markov 性 | 切斷過去 ， 只看現在  $X_t$  |  $E[ \cdot \mid F_t] = v(t,X_t)$  |
| Itô 公式 | 對  $v$  作二階展開 |  $dv = (\partial_t v + Lv)dt + \nabla v \cdot dW$  |
| 取期望 | 鞅項消失 ， 剩餘漂移為零 | 得到 PDE ， 反之亦然 |

直覺是 ， PDE 的解沿著隨機軌道走 ， 加上折現後形成鞅 ， 期望守恆 。

Feynman 的所有路徑求和 ， 在數學家手中變成了 Wiener 測度下的積分 。

$$ \int_{\text{路徑}} e^{-S} \mathcal{D} \text{路徑} \longleftrightarrow E[ \cdot ] $$

其中左端為物理啟發 ， 右端為嚴格期望 ， Kac 補上了測度地基 。

## 結案報告

真兇現身 ： 偏微分方程的解 ， 就是隨機軌道的加權平均 。

拋硬幣不再是賭博 ， 而是解方程的蒙地卡羅算法 ， 維度再高也不怕網格爆炸 。

本案遺產有四件 。

第一 ， PDE 與機率從此互通 ， 分析學家可用模擬猜解 ， 機率學家可用 PDE 算期望 。

第二 ， 金融定價直接受惠 ， Black–Scholes 公式本質上就是 Feynman–Kac 公式的變體 。

第三 ， Schrödinger 方程的虛時間版本得到機率詮釋 ， 量子與擴散正式結盟 。

第四 ， 1990 年 BSDE 與 2017 年 Deep BSDE 皆以此為起點 ， 從線性走向非線性 。

當然 ， 經典公式只處理線性方程 ， 非線性 PDE 需要倒向隨機微分方程接棒 。

Feynman 本人對嚴格化興趣缺缺 ， 他要的是直覺 ， Kac 給的是證明 ， 兩全其美 。

1947 年走廊上的三分鐘對話 ， 換來了橫跨物理與數學的百年橋樑 。

## 證據與工具

證物一號 ： 熱方程的機率解 ， 最純粹的 Feynman–Kac 公式 。

$$ u(t,x) = E_x[ f(W_T) ] $$

其中  $W$  為布朗運動 ， $f$  為終端函數 ， $u$  解熱方程 。

證物二號 ： 含位勢的完整版 ， 折現因子現形 。

$$ u(t,x) = E[ f(X_T) e^{- \int_t^T V(X_s) ds} \mid X_t = x ] $$

其中  $V$  為位勢 ， 指數項可理解為殺戮率或利率 。

證物三號 ： 生成元形式 ， 連回 Kolmogorov 後向方程 。

$$ \partial_t u + b \cdot \nabla u + \frac{1}{2} \mathrm{tr}( a \nabla^2 u ) - Vu = 0 $$

偵探工具 ： Markov 性 ， Itô 公式 ， 可選停時定理 ， Wiener 測度 。

數值呼應可參考程式 `_code/1949-feynman_kac_heat.py` ， 以蒙地卡羅解熱方程誤差小於百分之一 。

參數速查表如下 。

| 符號 | 意義 | 備註 |
|------|------|------|
|  $u$  | PDE 的解 | 同時是期望值 |
|  $X$  | 擴散過程 | 由  $b$  與  $\sigma$  驅動 |
|  $V$  | 位勢 | 物理為位能 ， 金融為利率 |
|  $f$  | 終端條件 | 到期酬勞或初溫分佈 |
|  $E_x$  | 初值為  $x$  的期望 | 條件於  $X_t = x$  |

## 補充：程式實作

### 對應程式

本節對應 [1949-feynman_kac_heat.py](_code/1949-feynman_kac_heat.py) ，以蒙地卡羅驗證熱方程的 Feynman–Kac 表示。

### 理論呼應

本文核心是熱方程 $\partial_t u + \frac{1}{2}\Delta u = 0$ 的機率表示 $u(t,x) = E_x[f(W_T)]$ 。
取初值 $f(x) = \cos(x)$ 時，解析解為 $u(T,x) = \cos(x)e^{-T/2}$ ，恰為布朗增量特徵函數的實部。
程式固定 $x = 1.0$ 與 $T = 0.5$ ，以六十萬條 $W_T$ 模擬驗證 $E[\cos(x+W_T)]$ 趨近解析解。
實測相對誤差小於百分之一，呼應期望守恆與鞅論證的結論。

### 執行方式

`python3 _code/1949-feynman_kac_heat.py`

### 實測輸出

`exact u=0.420788 (=cos(1)*exp(-0.25))` ， `MC u=0.420375 rel_err=0.0982%` ， `VERIFY ... err=0.0982%<1% PASS` 。

### 讀者實驗

將 $T$ 改為 $1.0$ 並把 $N$ 提高為一百萬，再觀察相對誤差是否維持在百分之一以內。

完整程式如下：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""1949 Feynman-Kac 熱方程對應 wiki 說明
對應 wiki：1949 年 Feynman-Kac 公式，拋物 PDE 以布朗期望表示。
熱方程 u_t = (1/2) u_xx，初值 u(0,x)=cos(x)，解 u(T,x)=E[cos(x+W_T)]=cos(x)*exp(-T/2)。
本程式 x=1.0、T=0.5，MC 驗證約 e^{-0.25}cos(1)，相對誤差<1%。
規範：只用 numpy，固定種子，不畫圖只印數字，結尾印 VERIFY 並用 assert 把關。
"""
import numpy as np

np.random.seed(3)

x = 1.0
T = 0.5
N = 600000

WT = np.sqrt(T) * np.random.randn(N)
payoff = np.cos(x + WT)
u_mc = float(np.mean(payoff))
u_exact = float(np.cos(x) * np.exp(-T / 2.0))
rel_err = abs(u_mc - u_exact) / abs(u_exact)

print(f"Heat Feynman-Kac x={x} T={T} N={N}")
print(f"exact u={u_exact:.6f} (=cos(1)*exp(-0.25))")
print(f"MC    u={u_mc:.6f} rel_err={rel_err:.4%}")

assert rel_err < 0.01, f"rel err {rel_err} >= 1%"
print(f"VERIFY 1949 Feynman-Kac heat: u_mc={u_mc:.6f} exact={u_exact:.6f} err={rel_err:.4%}<1% PASS")
```
