# 1900 年巴黎賭局：Bachelier 投機理論奇案

> 巴黎證券交易所喧囂震天，一名數學博士生把股價當成花粉，把賭徒當成分子。他比 Einstein 早五年寫下布朗運動，卻被埋沒了六十年。這是科學史上最安靜的一次搶劫。

| 欄位 | 內容 |
|------|------|
| 發生時間 | 1900 年 3 月 29 日，博士論文答辯日，指導教授為 Henri Poincaré |
| 地點 | 巴黎大學科學院，Théorie de la spéculation 答辯廳；取材自巴黎證券交易所債券價格 |
| 報案人 | Louis Bachelier（1870–1946），自費博士生，出身波爾多，後任教於第戎與貝桑松 |
| 偵探 | Bachelier 本人；導師 Poincaré 寫下正面評語卻未追認其遠見；後世由 Samuelson 與 Fama 翻案 |
| 兇器 | 算術布朗運動，股價增量服從常態分佈，模型為 $dS = \\sigma dW$ ，反射原理先聲奪人 |
| 結論 | 投機價格的數學即熱傳導方程，選擇權定價已有雛形，論文被冷落六十年後成為數量金融鼻祖 |

## 案發現場

1900 年的巴黎，是數學與金錢的交界口。

巴黎證券交易所裡交易的是法國公債 rente，價格每分每秒跳動。經紀人憑直覺喊價，投機者憑運氣下注，沒有人覺得這裡面有數學。

Bachelier 偏偏覺得有。他在論文開頭寫下一句判詞：投機的數學期望為零。市場的每一輪漲跌，在資訊公開的條件下互相抵消，價格沒有可被預見的漂移。

案發現場有三個反常細節。

第一，價格圖長得像花粉之路。Bachelier 收集的債券報價序列起伏不定，增量時正時負，毫無記憶。這與 Brown 的花粉之舞是同一種抖動，只是舞台從載玻片換成了交易所。

第二，投機者口中的「均值回歸」站不住腳。當時的商人相信大漲之後必有大跌，大跌之後必有大漲。Bachelier 用數據打臉：條件期望仍然是現價，過去的漲跌不提供方向情報。

第三，選擇權已經在交易。當時的巴黎已有類似買賣權的投機合約，稱為 prime。商人憑經驗報價，Bachelier 想給出公式。這比 Black 與 Scholes 早了七十三年。

Poincaré 作為口試委員，看懂了數學的嚴謹，給了高度評價，卻把論文歸檔於「金融應用」，而非「物理發現」。檔案室的標籤一貼錯，六十年無人翻閱。

## 偵查過程

Bachelier 的偵查工具是機率論，而當年機率論還是一門半吊子的學問。他幾乎是徒手蓋樓。

### 第一步：增量的常態假設

他假設在微小時間 $dt$ 內，價格增量 $dS$ 服從零均值常態分佈，變異數正比於 $dt$ 。用今日符號寫，即

$$
dS = \\sigma dW
$$

其中 $W$ 為標準布朗運動， $\\sigma$ 為波動參數。這就是算術布朗運動，比 Einstein 的擴散方程早五年，比 Wiener 的嚴格構造早二十三年。

由此可得 $t$ 時刻價格 $S_t$ 的分佈。若初值為 $S_0$ ，則密度為

$$
p(x,t) = (2 \\pi \\sigma^2 t)^{-1/2} \\exp(-(x - S_0)^2 / 2 \\sigma^2 t)
$$

這正是熱方程的基本解。Bachelier 明確指出，價格機率滿足 Fourier 熱傳導方程。他在金融裡重新發現了物理。

### 第二步：反射原理的先驅

Bachelier 要為 prime 定價，必須計算價格觸及某個障礙的機率。這逼他證明了反射原理，比 Lévy 早了數十年。

設 $M_t$ 為至 $t$ 為止的最大值，障礙為 $H$ 高於初值 $S_0$ 。他論證

$$
P(M_t \\ge H, S_t \\le x) = P(S_t \\ge 2H - x)
$$

直觀說法是：一旦路徑碰到 $H$ ，之後的走勢關於 $H$ 對稱反射，碰障後的分佈等於從鏡像點出發的分佈。憑此可得最大值分佈與障礙選擇權價格。

他進一步給出買權公式的雛形。若履約價為 $K$ ，到期為 $T$ ，則價值正比於超越機率的積分，即今日所謂 Bachelier 公式

$$
C = (S_0 - K) \\Phi(d) + \\sigma \\sqrt{T} \\phi(d)
$$

其中 $d = (S_0 - K) / \\sigma \\sqrt{T}$ ， $\\Phi$ 與 $\\phi$ 分別為標準常態的分佈與密度函數。這是 Black–Scholes 的算術版祖先。

### 第三步：數據對質

Bachelier 不是空想家。他拿巴黎交易所的 rente 報價驗證，整理了價格差分的經驗分佈。

| 檢驗項目 | Bachelier 的做法 | 結果 |
|----------|------------------|------|
| 增量均值 | 計算不同區間的平均漲跌 | 接近於零，印證鞅性 |
| 增量變異數 | 比較一日、十日、月度波動 | 近似正比於時間 $t$ |
| 分佈形狀 | 繪製差分直方圖 | 中部近似鐘形，尾部略厚 |
| 選擇權報價 | 以公式反推 prime 合理價格 | 與市場經驗報價量級相符 |

尾部略厚的發現極有先見之明。百年後的經驗金融學證實，短期報酬確實肥尾。但在 1900 年，這個細節被當成誤差放過了。

## 結案報告

Bachelier 的論文答辯通過了，分數不錯，但學術市場給了他一張冷板凳。

原因有三。第一，題材被輕視。數學系認為股市是賭場，不是科學。第二，算術布朗允許負價格，經濟學家覺得荒謬，儘管對 rente 短期建模無傷大雅。第三，機率論當時地位低下，Poincaré 本人也未把隨機性視為主流。

於是這篇論文在圖書館裡睡了六十年。直到 1950 年代，統計學家 Savage 翻出它，寄給 Samuelson，Samuelson 才驚呼這是天才之作。Fama 的效率市場假說、Black–Scholes 的避險思想，都要叫它一聲祖師爺。

歷史的判決是：Bachelier 破了兩案。他破了投機定價案，也無意中破了布朗運動的數學案。只是第二份功勞被記在了 Einstein 名下，因為物理學家不讀金融論文。

探案的教訓是：兇手會換舞台。今天在水裡跳舞，明天在股市裡跳舞，數學只認舞步，不認舞台。

## 證據與工具

本案物證為 Bachelier 論文 Théorie de la spéculation（1900）與 Annales 科學院紀要版本，以及巴黎交易所 rente 報價手抄表。

| 工具 | 數學形式 | 用途 |
|------|----------|------|
| 算術布朗運動 | $dS = \\sigma dW$ | 股價動態的起點，零漂移常態增量 |
| 熱方程對應 | $\\partial_t p = \\sigma^2 \\partial_{xx} p / 2$ | 機率密度的演化，與 Einstein 擴散同構 |
| 反射原理 | $P(M_t \\ge H) = 2 P(S_t \\ge H)$ | 障礙機率與計算法，選擇權定價關鍵 |
| Bachelier 買權公式 | $C = (S_0 - K) \\Phi(d) + \\sigma \\sqrt{T} \\phi(d)$ | 算術模型的封閉解， $d$ 如上定義 |
| 零期望鞅性 | $E[S_t \\mid S_0] = S_0$ | 效率市場的數學雛形 |

辦案備註：讀者可用蒙地卡羅模擬算術布朗路徑，統計 $S_T$ 的均值與變異數，驗證均值為 $S_0$ 、變異數為 $\\sigma^2 T$ 。對應程式見 _code 目錄中 1900 年 Bachelier 選擇權程式，比較模擬價格與上表封閉公式，誤差應小於百分之一。

## 補充：程式實作

### 對應程式

[1900-bachelier_option.py](_code/1900-bachelier_option.py)

### 理論呼應

本文以算術布朗運動 $dS = \sigma dW$ 為起點，增量零均值且變異數正比於時間。
零漂移蘊含鞅性 $E[S_t \mid S_0] = S_0$ ，到期變異數滿足 $Var(S_T) = \sigma^2 T$ 。
買權封閉解為 $C = (S_0 - K) \Phi(d) + \sigma \sqrt{T} \phi(d)$ ，其中 $d = (S_0 - K) / \sigma \sqrt{T}$ 。
程式以蒙地卡羅模擬驗證封閉解，誤差小於百分之一即為理論成立的數量證據。

### 執行方式

`python3 _code/1900-bachelier_option.py`

### 實測輸出

```text
S0=100.0 sigma=15.0 T=1.0 K=100.0 M=200000
d=0.000000 phi(d)=0.398942 Phi(d)=0.500000
closed(Bachelier)=5.984134 std_form=5.984134
mc_price=6.017451 se=0.019627
rel_err=0.005568 (tol 0.01)
VERIFY 1900-bachelier_option PASS mc=6.0175 closed=5.9841 rel_err=0.5568%
```

### 讀者實驗

試將 $K$ 由 $100.0$ 改為 $110.0$ ，觀察買權價格是否明顯下跌。

完整程式如下：

```python
# 對應 wiki：1900 年 Bachelier 算術布朗與選擇權定價（Bachelier 模型）
# 說明：S_T = S0 + sigma*sqrt(T)*Z；看漲 payoff = max(S_T-K,0)；
# 封閉解 C = sigma*sqrt(T)*(phi(d) - d*Phi(-d))，d=(S0-K)/(sigma*sqrt(T))，
# 其中 phi 標準常態 pdf，Phi 為 cdf（僅用 numpy 以 A&S 近似實作 cdf，不用 scipy/matplotlib/math）。
import numpy as np

SEED = 1900
S0 = 100.0
SIGMA = 15.0
T = 1.0
K = 100.0
M = 200_000


def phi(x):
    x = np.asarray(x, dtype=np.float64)
    return np.exp(-0.5 * x * x) / np.sqrt(2.0 * np.pi)


def Phi(x):
    # Abramowitz & Stegun 7.1.26，僅用 numpy（exp/sqrt），精度 ~1e-7
    x = float(x)
    a1 = 0.254829592
    a2 = -0.284496736
    a3 = 1.421413741
    a4 = -1.453152027
    a5 = 1.061405429
    p = 0.3275911
    z = x / float(np.sqrt(2.0))
    sgn = 1.0 if z >= 0.0 else -1.0
    az = abs(z)
    t = 1.0 / (1.0 + p * az)
    tau = (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * float(np.exp(-az * az))
    erfz = sgn * (1.0 - tau)
    return 0.5 * (1.0 + erfz)


rng = np.random.default_rng(SEED)
Z = rng.standard_normal(M)
ST = S0 + SIGMA * float(np.sqrt(T)) * Z
payoff = np.maximum(ST - K, 0.0)
price_mc = float(payoff.mean())
se = float(payoff.std(ddof=1) / np.sqrt(M))

d = (S0 - K) / (SIGMA * float(np.sqrt(T)))
price_closed = float(SIGMA * float(np.sqrt(T)) * (float(phi(d)) - d * Phi(-d)))
# 標準形式交叉核對：C = (S0-K)*Phi(d) + sigma*sqrt(T)*phi(d)
price_std = float((S0 - K) * Phi(d) + SIGMA * float(np.sqrt(T)) * float(phi(d)))

rel_err = abs(price_mc - price_closed) / price_closed

print(f"S0={S0} sigma={SIGMA} T={T} K={K} M={M}")
print(f"d={d:.6f} phi(d)={float(phi(d)):.6f} Phi(d)={Phi(d):.6f}")
print(f"closed(Bachelier)={price_closed:.6f} std_form={price_std:.6f}")
print(f"mc_price={price_mc:.6f} se={se:.6f}")
print(f"rel_err={rel_err:.6f} (tol 0.01)")

assert rel_err < 0.01, f"Bachelier rel_err {rel_err} >= 1%"
print(f"VERIFY 1900-bachelier_option PASS mc={price_mc:.4f} closed={price_closed:.4f} rel_err={rel_err:.4%}")
```
