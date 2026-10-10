# 1960 年 Girsanov 定理：漂移消失的那一夜

| 項目 | 內容 |
|------|------|
| 案發時間 | 1960 年 |
| 案發地點 | 莫斯科，Steklov 數學研究所前後 |
| 主角 | Igor Girsanov、Cameron–Martin 先行者、Novikov（條件） |
| 案件性質 | 能否換一個機率測度，讓帶漂移的布朗運動變回純布朗運動 |
| 關鍵證物 | 指數鞅 $dQ/dP = \mathcal E(-\int\theta dW)$ ，Novikov 條件 |
| 關聯案件 | 1973 年 Black–Scholes、1979 年鞅定價、風險中性測度 |

## 案發現場

案發現場是一條看似無辜的 SDE。一個帶漂移的布朗運動走過：

$$
dX_t = \theta_t dt + dW_t
$$

其中 $W_t$ 是機率 $P$ 下的布朗運動， $\theta_t$ 是漂移。目擊者說，這條路徑抖動的樣子與純布朗運動一模一樣，只是整體歪向一邊。

問題來了：抖動的「形狀」相同，漂移能否只是視角的假象？換句話說，是否存在另一個機率測度 $Q$ ，在 $Q$ 的眼中 $X_t$ 就是標準布朗運動？

這不是哲學遊戲。若答案為是，那麼 SDE 的漂移項就可以被「搬家」：解題時先換到好算的測度，算完再搬回來。Cameron–Martin 在 1940 年代已對確定性平移給出肯定答案，但對隨機的 $\theta_t$ ，證據鏈仍是斷的。

1960 年，Girsanov 發表了關鍵論文，把斷掉的鏈條接上。幾乎同時，金融世界的未來也在暗處等待：十多年後，Black–Scholes 與鞅定價理論將完全建立在「換測度消滅漂移」這招之上。

## 偵查過程

Girsanov 的偵查手法是構造一個似然比鞅。定義指數鞅：

$$
Z_T = \exp\left(-\int_0^T \theta_s dW_s - \frac{1}{2}\int_0^T \theta_s^2 ds\right)
$$

並以此為 Radon–Nikodym 導數定義新測度 $dQ/dP = Z_T$ 。在 $Q$ 之下，原本的 $X_t$ 褪去漂移，成為標準布朗運動。

更一般的陳述是：若 $W_t$ 為 $P$ 布朗運動，定義 $W_t^Q = W_t + \int_0^t \theta_s ds$ ，則 $W_t^Q$ 在 $Q$ 下為布朗運動。漂移被整包搬進了測度變換裡。

但偵探很快發現一具「屍體」： $Z_t$ 不一定是真正的鞅，它可能只是局部鞅。若 $E[Z_T] < 1$ ，則 $Q$ 的總質量小於一，根本不是機率測度。於是 Novikov 條件登場：

$$
E\left[\exp\left(\frac{1}{2}\int_0^T \theta_s^2 ds\right)\right] < \infty
$$

滿足此條件，則 $Z_t$ 為一致可積鞅，換測度合法。Kazamaki 與 Beneš 條件則是後續的放寬版本。

案情整理如下表：

| 證據 | 數學內容 | 偵查意義 |
|------|----------|----------|
| 指數鞅 $Z_t$ | $\mathcal E(-\int\theta dW)$ | 換測度的兇器 |
| Novikov 條件 | 指數可積性 | 保證 $Z_t$ 是真鞅 |
| $W_t^Q$ | $W_t + \int\theta_s ds$ | 新測度下的布朗運動 |
| Cameron–Martin | 確定性 $\theta$ 的先行特例 | 本案的前傳 |

偵查過程的高潮是一場思想實驗。假設 $\theta$ 為常數，則 $Z_T$ 是對數常態變數，直接計算可驗 $E[Z_T] = 1$ 。此時換測度相當於把每條路徑按終點位置加權：偏向漂移方向的路徑被降權，反方向的被加權，加權之後整體看起來無漂移。這正是重要性抽樣的機率本質。

另一個關鍵轉折是逆向使用：給定 SDE 的弱解存在性問題，可先構造無漂移的布朗運動，再用 Girsanov 把漂移「貼回去」。弱解的存在性於是化約為指數鞅的鞅性。這招在 Stroock–Varadhan 鞅問題理論中發揚光大。

## 結案報告

結案陳詞：漂移不是路徑的本質，而是測度的選擇。Girsanov 定理證明，只要 $Z_t$ 是真鞅，就可以自由地在 $P$ 與 $Q$ 之間搬運漂移。

本案的直接遺產是數理金融。1973 年 Black–Scholes 公式中的風險中性測度，正是把股票漂移 $\mu$ 換成無風險利率 $r$ 的 Girsanov 操作。1979 年 Harrison–Kreps–Pliska 的鞅定價理論，更把「無套利等價於存在等價鞅測度」寫成第一基本定理，而 Girsanov 就是構造那個測度的工具。

更深的遺產在統計與濾波：Kallianpur–Striebel 公式用同樣的換測度技巧，把帶訊號的觀測變成純噪聲，從而導出 Zakai 方程。2000 年代的重要性抽樣、粒子濾波權重，骨子裡都是 $Z_T$ 。

Girsanov 本人 1967 年英年早逝，年僅 32 歲。這起案件的偵探沒能看到金融大廈的落成，但他留下的指數鞅，至今仍是每個量化分析師口袋裡的萬能鑰匙。

## 證據與工具

核心證物一：測度變換的 Radon–Nikodym 導數， $\mathcal E$ 表隨機指數：

$$
\frac{dQ}{dP} = \mathcal E\left(-\int_0^T \theta_s dW_s\right)
$$

核心證物二：隨機指數的顯式， $Z_t$ 滿足 $dZ_t = -\theta_t Z_t dW_t$ ：

$$
Z_T = \exp\left(-\int_0^T \theta_s dW_s - \frac{1}{2}\int_0^T \theta_s^2 ds\right)
$$

核心證物三：Novikov 可積條件， $E$ 表 $P$ 下期望：

$$
E\left[\exp\left(\frac{1}{2}\int_0^T \theta_s^2 ds\right)\right] < \infty
$$

辦案工具箱：

| 工具 | 用途 | 備註 |
|------|------|------|
| Itô 公式 | 驗證 $Z_t$ 的 SDE | 漂移項恰好相消 |
| Novikov / Kazamaki 條件 | 判定真鞅 | 新手最常忽略的陷阱 |
| 蒙地卡羅加權 | 以 $Z_T$ 為權重還原漂移 | 對應 `_code/1960-girsanov_drift.py` |
| 風險中性定價 | $C_0 = e^{-rT}E_Q[\Phi]$ | 下一案的預告 |

 接案提示：取常數 $\theta = 0.5$ ，模擬 $P$ 下的帶漂移路徑，再以 $Z_T$ 加權計算終點均值，可親眼見證加權後的均值歸零。

## 補充：程式實作

### 對應程式

本節對應 [1960-girsanov_drift.py](_code/1960-girsanov_drift.py) ，以加權蒙地卡羅驗證換測度消滅漂移。

### 理論呼應

本文核心是指數鞅 $Z_T = \exp(-\int_0^T\theta_sdW_s-\frac{1}{2}\int_0^T\theta_s^2ds)$ 作為 $dQ/dP$ 。
程式取常數 $\theta = 0.7$ 與 $T = 1.0$ ，以一百萬條 $W_T$ 驗證 $E_P[L] \approx 1$ 與 $E_P[D] \approx 1$ 的真鞅性。
再以 $D$ 加權計算 $E_Q[W_T] = E_P[D\cdot W_T]$ ，理論值為 $\theta T = 0.7$ ，呼應漂移搬家的思想實驗。
實測加權均值 $0.699554$ 幾乎命中漂移，證實路徑加權後無漂移假象完整現形。

### 執行方式

`python3 _code/1960-girsanov_drift.py`

### 實測輸出

`E_P[L]=0.999906` ， `E_P[D]=1.000109` ， `E_Q[W_T]=0.699554 (target theta*T=0.7000, relerr 0.0637%)` ， `VERIFY ... PASS` 。

### 讀者實驗

將 $\theta$ 改為 $0.5$ 再重跑一次，觀察加權均值是否同樣趨近新的 $\theta T$ 目標。

完整程式如下：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""1960 Girsanov 漂移變換（對應 wiki：Girsanov 定理 / 測度變換與漂移）。
P 下 W_T ~ N(0, T)。取 theta=0.7，題目指定的似然比
    L = exp(-theta*W_T - theta^2*T/2)      （= dP_-/dP，-theta 漂移的 RN 導數）
+theta 漂移測度 Q 的 RN 導數為 D = exp(+theta*W_T - theta^2*T/2)
= exp(-theta^2*T)/L。驗證：
  (1) E_P[L] ≈ 1 且 E_P[D] ≈ 1（指數鞅性），
  (2) E_Q[W_T] = E_P[D*W_T] ≈ theta*T。
只用 numpy，固定種子，不畫圖。
"""
import numpy as np
import time

t0 = time.time()
SEED = 1960
np.random.seed(SEED)

theta = 0.7
T = 1.0
N = 1_000_000

W = np.sqrt(T) * np.random.randn(N)
L = np.exp(-theta * W - 0.5 * theta ** 2 * T)   # 題目指定的 L
D = np.exp(theta * W - 0.5 * theta ** 2 * T)    # dQ/dP（+theta 漂移）
EL = float(np.mean(L))
ED = float(np.mean(D))
EQ_W = float(np.mean(D * W))                    # E_Q[W_T]
target = theta * T
err_EL = abs(EL - 1.0)
err_ED = abs(ED - 1.0)
rel_err = abs(EQ_W - target) / target

print(f"[girsanov] seed={SEED} N={N} theta={theta} T={T}")
print(f"[girsanov] E_P[L]      = {EL:.6f}  (target 1, abserr {err_EL:.2e})")
print(f"[girsanov] E_P[D]      = {ED:.6f}  (target 1, abserr {err_ED:.2e})")
print(f"[girsanov] E_Q[W_T]    = {EQ_W:.6f}  (target theta*T={target:.4f}, relerr {rel_err:.4%})")
print(f"[girsanov] elapsed {time.time()-t0:.2f}s")

assert err_EL < 0.01, f"E[L]={EL} deviates from 1"
assert err_ED < 0.02, f"E[D]={ED} deviates from 1"
assert rel_err < 0.05, f"E_Q[W_T]={EQ_W} vs {target} exceeds 5%"
print(f"VERIFY: girsanov E[L]={EL:.5f}≈1, E_Q[W_T]={EQ_W:.5f}≈theta*T={target:.4f} PASS")
```
