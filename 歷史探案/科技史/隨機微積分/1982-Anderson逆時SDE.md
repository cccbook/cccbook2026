# 1982 年 Anderson 逆時 SDE：把擴散倒著播的人

| 項目 | 內容 |
|------|------|
| 案發時間 | 1982 年 |
| 案發地點 | 期刊 Stochastics，逆時擴散的冷案卷宗 |
| 主角 | Brian D. O. Anderson、Haussmann–Pardoux（同期逆時工匠） |
| 案件性質 | 擴散過程倒著看還是擴散嗎？漂移該如何修正 |
| 關鍵證物 | 逆時 SDE， $dx = [f - g^2\nabla\log p_t]dt + g d\bar W$ |
| 關聯案件 | 1931 年 Kolmogorov 前向後向、2021 年擴散生成模型、1990 年 BSDE |

## 案發現場

1982 年，一篇名為《Reverse-time diffusion equation models》的論文登上 Stochastics 期刊。作者 Anderson 問了一個孩子氣的問題：把擴散的電影倒著播，會看到什麼？

正向擴散人人會寫。設狀態 $x_t$ 服從：

$$
dx_t = f(x_t,t) dt + g(t) dW_t
$$

其中 $f$ 為漂移， $g$ 為擴散係數， $W_t$ 為布朗運動。邊際密度 $p_t$ 服從 Fokker–Planck 方程向前流動。但若固定終點分佈，從 $T$ 往 $0$ 倒著走，路徑還滿足某條 SDE 嗎？漂移要加什麼修正？

這個問題在 1982 年毫無應用場景。濾波要向前，控制要向前，定價要向後但用的是 BSDE 而非逆時 SDE。論文發表後幾乎無人引用，沉入故紙堆，一睡四十年。

直到 2021 年，Song 等人把分數生成模型寫成 SDE，世人才驚覺：DALL·E 與 Stable Diffusion 的引擎蓋底下，躺的正是 Anderson 的公式。冷案重啟，兇器竟是生成式 AI 的心臟。

## 偵查過程

Anderson 的偵查從 Fokker–Planck 出發。正向密度流為：

$$
\partial_t p_t = -\nabla\cdot(f p_t) + \frac{1}{2}g^2 \Delta p_t
$$

倒放時間 $\tau = T - t$ ，要求逆時過程的密度流與正向一致。經分部積分與 Kolmogorov 後向方程比對，逆時漂移必須多出一項分數修正。結論是逆時 SDE：

$$
dx_t = [f(x_t,t) - g(t)^2 \nabla_x \log p_t(x_t)] dt + g(t) d\bar W_t
$$

其中 $\bar W_t$ 為逆時布朗運動， $\nabla_x \log p_t$ 稱為分數（score）。直覺是：倒著走時，原本把粒子推散的噪聲，必須靠分數項把粒子拉回高密度區，否則密度流對不上。

偵查筆錄如下表：

| 角色 | 符號 | 推理意義 |
|------|------|----------|
| 正向漂移 | $f$ | 原電影的劇情推力 |
| 分數修正 | $-g^2\nabla\log p_t$ | 倒播時拉回高密度區的手 |
| 逆時噪聲 | $d\bar W_t$ | 倒著走仍是布朗增量 |
| 邊際守恆 | $p_t$ 不變 | 正逆同享同一條密度流 |
| 機率流 ODE | 去掉噪聲即得 | 與連續正則化流的親緣 |

同期 Haussmann–Pardoux（1986 前後）以弱解與時間反轉的嚴格機率論重證此式，Föllmer 更以熵與時間反轉連結。但 1980 年代的最大障礙是：分數 $\nabla\log p_t$ 無法計算。沒有數據、沒有神經網路，公式再美也只是標本。

2021 年的反轉在於：分數不必解析求，用去噪分數匹配從數據學出來。Song 等人的 Score SDE 框架把 Anderson 公式直接變成採樣器：先加噪（正向），再學分數，最後跑逆時 SDE 生成。沉睡的標本睜開眼睛，變成能畫圖的引擎。

一個常見誤解必須澄清：逆時 SDE 的噪聲係數 $g$ 與正向相同，只有漂移被修正。這正是本案最反直覺的證詞：時間反轉不改變抖動強度，只改變抖動的偏好方向。

## 結案報告

結案：擴散倒著看仍是擴散，代價是漂移減去 $g^2\nabla\log p_t$ 。Anderson 1982 年以 Fokker–Planck 與時間反轉封緘此案，Haussmann–Pardoux 補上嚴格機率封印。

本案的離奇在於量刑延遲四十年。1982–2020 年間引用寥寥，淪為時間反轉習題；2021 年擴散模型引爆後，一夜之間成為引用熱點。Denoising Diffusion、Score SDE、Flow Matching，全是逆時公式的子孫。

遺產第一層是生成式 AI：從文字到圖像到音訊，逆時採樣是當代引擎。第二層是理論：分數即對數密度的梯度，連結了 Langevin 採樣、Schrödinger 橋、熵正則最優傳輸。第三層是史觀：最冷僻的隨機分析也可能在四十年後成為显學。寫下公式的人，等不到掌聲，但掌聲終會沿著時間逆流而上。

Anderson 若地下有知，看到自己的方程在 GPU 上每秒倒播百萬次，不知會說什麼。大概只會淡淡一句：我早就告訴過你們，電影可以倒著播。

## 證據與工具

核心證物一：正向 SDE， $f$ 為漂移， $g$ 為擴散係數：

$$
dx_t = f(x_t,t) dt + g(t) dW_t
$$

核心證物二：逆時 SDE， $\bar W_t$ 為逆時布朗運動：

$$
dx_t = [f - g^2 \nabla\log p_t] dt + g d\bar W_t
$$

核心證物三：分數定義， $p_t$ 為邊際密度：

$$
s(x,t) = \nabla_x \log p_t(x)
$$

辦案工具箱：

| 工具 | 用途 | 備註 |
|------|------|------|
| Fokker–Planck 方程 | 推導漂移修正 | 正逆共享密度流 |
| 去噪分數匹配 | 從數據學 $s(x,t)$ | 2021 年的復活鑰匙 |
| OU 逆時實驗 | 解析分數驗證公式 | 對應 `_code/1982-reverse_ou.py` |
| 機率流 ODE | 去噪聲的確定性孿生 | 採樣更快，似然可算 |

接案提示：取 OU 過程為白老鼠，其高斯分數有解析式，直接跑逆時 SDE，可見終點分佈精確重建初始分佈。

## 補充：程式實作

### 對應程式

本節對應程式為 [1982-reverse_ou.py](_code/1982-reverse_ou.py) 。

### 理論呼應

本文核心為逆時公式 $dx_t = [f - g^2 \nabla \log p_t] dt + g d\bar W_t$ ，其中 $\bar W_t$ 為逆時布朗運動。
分數定義為 $s(x, t) = \nabla_x \log p_t(x)$ ，它把正向推散的噪聲拉回高密度區。
程式以 OU 過程 $dx_t = f(x_t, t) dt + g(t) dW_t$ 為例，其高斯分數有解析式，可直接驗證正逆共享同一條密度流。
時間反轉不改變抖動強度 $g$ ，只修正漂移方向，此反直覺結論在倒播重建均值與變異數時得到數值印證。

### 執行方式

在本文所在目錄執行 `python3 _code/1982-reverse_ou.py` 。

### 實測輸出

本次實測前向終點均值為 0.27324，目標為 0.27067，變異數為 0.50831，目標為 0.50916。
逆時重建均值為 1.99265，目標為 2.0000，相對誤差為 0.3674%。
重建變異數為 0.99825，目標為 1.0000，相對誤差為 0.1752%，兩者皆小於 8%，通過驗證門檻。

### 讀者實驗

可將步長 $dt$ 由 0.01 改為 0.02，再觀察重建均值與變異數的相對誤差變化。

完整程式如下：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""1982 OU 逆時倒播（對應 wiki：Anderson 逆時 SDE / score-based 生成模型溯源）。
前向 OU：dX = -a*X dt + sig*dW，X0 ~ N(mu0=2, v0=1)，跑至 T=2（近似平穩）。
邊際解析：m(t)=mu0*e^{-at}，v(t)=e^{-2at}*v0 + sig^2/(2a)*(1-e^{-2at})，
score = -(x-m(t))/v(t)。
逆時（Anderson）：dY = [-f + g^2*score] dtau + g*dWbar
               = [a*Y - sig^2*(Y-m(t))/v(t)] dtau + sig*dWbar，t=T-tau。
以 X_T 樣本為 Y_0 倒播回 tau=T，驗證重建均值/變異數 ≈ (mu0, v0)，誤差 < 8%。
只用 numpy，固定種子，不畫圖。
"""
import numpy as np
import time

t0 = time.time()
SEED = 1982
np.random.seed(SEED)

a, sig = 1.0, 1.0
mu0, v0 = 2.0, 1.0
T = 2.0
dt = 0.01
nsteps = int(round(T / dt))
M = 100_000


def m_v(t):
    e1 = np.exp(-a * t)
    return mu0 * e1, np.exp(-2 * a * t) * v0 + sig ** 2 / (2 * a) * (1 - np.exp(-2 * a * t))


# 前向（精確轉移）
X = mu0 + np.sqrt(v0) * np.random.randn(M)
efd = np.exp(-a * dt)
sfd = sig * np.sqrt((1 - np.exp(-2 * a * dt)) / (2 * a))
for _ in range(nsteps):
    X = X * efd + sfd * np.random.randn(M)

mT, vT = m_v(T)
print(f"[revOU] fwd: mean={np.mean(X):.5f} (target {mT:.5f}), "
      f"var={np.var(X):.5f} (target {vT:.5f})")

# 逆時倒播
Y = X.copy()
sq = np.sqrt(dt)
for k in range(nsteps):
    t = T - k * dt
    m, v = m_v(t)
    drift = a * Y - sig ** 2 * (Y - m) / v
    Y = Y + drift * dt + sig * sq * np.random.randn(M)

mean_r, var_r = float(np.mean(Y)), float(np.var(Y))
rel_mean = abs(mean_r - mu0) / abs(mu0)
rel_var = abs(var_r - v0) / v0

print(f"[revOU] seed={SEED} M={M} dt={dt} steps={nsteps} a={a} sig={sig} T={T}")
print(f"[revOU] recon: mean={mean_r:.5f} (target {mu0:.4f}, relerr {rel_mean:.4%})")
print(f"[revOU] recon: var ={var_r:.5f} (target {v0:.4f}, relerr {rel_var:.4%})")
print(f"[revOU] elapsed {time.time()-t0:.2f}s")

assert rel_mean < 0.08, f"mean relerr {rel_mean} exceeds 8%"
assert rel_var < 0.08, f"var relerr {rel_var} exceeds 8%"
print(f"VERIFY: reverse_ou mean_relerr={rel_mean:.4%}, var_relerr={rel_var:.4%} <8% PASS")
```
