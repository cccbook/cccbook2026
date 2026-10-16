# 1993・Heston 隨機波動：微笑曲線的隨機解

> 「Black–Scholes 以為波動是常數，市場卻笑出了一條曲線。」
> 本案時間：1993 年，地點：美國耶魯，報案人：外匯與股票選擇權交易員。

| 案件檔案 | 內容 |
|----------|------|
| 案號 | SV-1993-Heston |
| 年份 | 1993 年 |
| 主角 | Steven Heston |
| 關鍵文獻 | A Closed-Form Solution for Options with Stochastic Volatility（1993） |
| 涉案對象 | 價格  $S$ 、變異數  $v$ 、相關係數  $\rho$ 、波速  $\xi$ |
| 核心證物 | CIR 型變異數過程、半封閉特徵函數、Fourier 反演定價 |
| 關聯舊案 | 1973 年 Black–Scholes、1979 年鞅定價、1992 年數值聖經 |
| 遺產 | 外匯微笑標準模型、粗糙波動的前輩、校準工業的起點 |

## 案發現場

1987 年股災之後，選擇權市場留下了一道洗不掉的微笑。

Black–Scholes 公式假設波動率  $\sigma$  是常數，推出的隱含波動應該是一條水平線。但交易螢幕上，深價外賣權的隱含波動明顯上翹，偏度與峰度公然嘲笑常態假設。交易員被迫用一張波動曲面打補丁：每個履約價配一個波動，模型淪為插值器。

此前的嫌疑犯各有缺陷。Merton 的跳躍模型能造出厚尾，但跳躍難對沖；Hull–White 的隨機波動直覺正確，卻只能依賴蒙地卡羅或近似；Stein–Stein 模型把波動本身寫成 OU 過程，波動卻可能變負，物理上說不通。

Heston 接案時開出的條件很硬：波動必須恆正，模型必須能算，最好有接近封閉的定價公式，能直接校準到市場微笑。少一條，就不算破案。

## 偵查過程

偵探把價格與變異數寫成一對連動的 SDE。設價格為  $S$ ，瞬時變異數為  $v$ ，兩組布朗運動相關係數為  $\rho$ ：

$$
dS = \mu S\,dt + \sqrt{v}\,S\,dW^S
$$

$$
dv = \kappa(\bar v - v)\,dt + \xi\sqrt{v}\,dW^v
$$

$$
dW^S\,dW^v = \rho\,dt
$$

第二行是 CIR 型（平方根）過程： $\kappa$  是均值回歸速度， $\bar v$  是長期均值， $\xi$  是波動的波動。平方根  $\sqrt{v}$  是神來之筆——變異數貼近零時噪聲自動熄火，配合 Feller 條件就不會穿越零點。

Feller 條件是本案的第一道封條：

$$
2\kappa\bar v \ge \xi^2
$$

成立時，變異數過程恆正；違反時，原點可達，數值模擬會頻繁撞零。實務上市場參數常踩線，於是有了全套截斷與反射修補，那是 1992 年數值聖經也頭痛的硬骨頭。

第二步是定價。風險中性下寫出二維 PDE，傳統有限差分直接硬解，維度一高就喘。Heston 改走特徵函數路線：猜對數價格的條件特徵函數有指數仿射形式，偏微分方程坍縮成一組 Riccati 常微分方程，可半封閉求解。再經 Fourier 反演，選擇權價格化為兩個「尾機率」之差：

$$
C = S_0 P_1 - K e^{-rT} P_2
$$

其中  $P_1$  與  $P_2$  由特徵函數  $\phi$  的積分給出。這就是所謂半封閉解：Riccati 部分解析，反演積分留給數值求積。

下表是參數的側寫檔案，每個參數都是微笑曲線的一名整形醫生：

| 參數 | 符號 | 整形效果 |
|------|------|----------|
| 相關 |  $\rho$  | 控制偏度，負值造出權益市場的左偏微笑 |
| 波速 |  $\xi$  | 控制峰度，越大微笑兩端翹得越高 |
| 回歸速 |  $\kappa$  | 控制期限結構，越大短期微笑衰減越快 |
| 長期均值 |  $\bar v$  | 控制曲面高度，整體上下平移 |
| 初值 |  $v_0$  | 控制短期 at-the-money 水位 |

相關係數  $\rho$  的符號尤其關鍵。股票市場多為負相關：跌時波動飆升，左尾肥大，微笑左高右低。外匯市場  $\rho$  近零，微笑近乎對稱。一組參數同時解釋偏度、峰度與期限結構，這是 Heston 勝過局部波動模型的探案亮點。

## 結案報告

1993 年一案，用五個參數馴服了微笑。

Heston 模型成為外匯與權益衍生品的工業標準：校準快、能對沖、能報價。Duffie–Pan–Singleton 後來把它收編進仿射框架，Bates 再把跳躍接回來，家族開枝散葉。即使 2014 年粗糙波動指控「波動比布朗更粗糙」，Heston 仍是每個新模型的必考對手。

在歷史年表裡，本案是 1973 年 Black–Scholes 的嫡傳續集：從常數波動到隨機波動，從封閉公式到半封閉特徵函數。它也反哺了數值學：平方根擴散的離散格式，至今仍是 Kloeden–Platen 法典裡的經典難題。

未竟之業是校準的穩定性。五個參數辨識不易，Riccati 的複對數分支切割曾引發著名的「Heston 陷阱」，後由 Gatheral 與 Albrecher 等人修補。微笑被解釋了，但沒有被消滅——它只是換了一組參數繼續微笑。

案件狀態：主犯落網，微笑收押，餘黨（跳躍與粗糙）另案偵辦。

## 證據與工具

證物一，風險中性 Heston 的標準寫法（ $r$  為利率）：

$$
dS = rS\,dt + \sqrt{v}\,S\,dW^{S*}
$$

$$
dv = \kappa^*(\bar v^* - v)\,dt + \xi\sqrt{v}\,dW^{v*}
$$

星號標記風險中性測度。注意漂移可變，擴散結構不變，這正是 Girsanov 定理的承諾。

證物二，特徵函數結構速記。設  $x = \ln S_T$ ，則：

$$
\phi(u) = \mathbb{E}[e^{iu x}] = \exp(C(u, T) + D(u, T)\,v_0 + iu\ln S_0)
$$

函數  $C$  與  $D$  滿足 Riccati 系統，初值  $C = D = 0$ 。記住「仿射進、仿射出」，就不會在推導中迷路。

證物三，實務工具箱：

| 工具 | 用途 | 備註 |
|------|------|------|
| Fourier 反演求積 | 由  $\phi$  算  $P_1, P_2$  | 注意阻尼因子與分支切割 |
| Feller 檢查 |  $2\kappa\bar v \ge \xi^2$  | 違反時改用截斷 Euler 或 QE 格式 |
| 賣買權平價 | 模型無關驗算 | 對應程式  `_code/1993-heston_mc.py`  |

探員建議：先用平價驗程式，再校準微笑，最後才信任對沖比。順序錯了，微笑會反咬你一口。

## 補充：程式實作

### 對應程式

- [1993-heston_mc.py](_code/1993-heston_mc.py)：以全截斷 Euler 加 log-Euler 蒙地卡羅模擬 Heston 模型，並用賣買權平價驗收。

### 理論呼應

本文模型為 $dS = \mu S\,dt + \sqrt{v}S\,dW^S$ 配 CIR 型變異數 $dv = \kappa(\bar v - v)\,dt + \xi\sqrt{v}\,dW^v$ ，相關結構為 $dW^S\,dW^v = \rho\,dt$ 。
平方根擴散使變異數貼近零時噪聲自動熄火，Feller 條件 $2\kappa\bar v \ge \xi^2$ 則是恆正的封條，程式以 $v^+ = \max(v, 0)$ 做全截斷正是對應的數值修補。
定價半封閉解形如 $C = S_0P_1 - Ke^{-rT}P_2$ ，而任何相容定價都須先過模型無關的賣買權平價 $C - P = S_0 - Ke^{-rT}$ ，程式即以此式驗收。

### 執行方式

在 `隨機微積分` 目錄下執行 `python3 _code/1993-heston_mc.py` 。

### 實測輸出

```text
Call = 9.226585, Put = 6.304900
parity LHS(C-P) = 2.921685, RHS = 2.955447
abs_err = 0.033761, rel_err = 0.000338 (tol 0.01)
VERIFY rel_parity_err=0.000338 C=9.2266 P=6.3049
```

### 讀者實驗

將相關係數 `rho` 由 -0.7 改為 0.0 再重跑，觀察 Call 與 Put 價格及平價誤差是否仍過關並體會偏度消失的對稱微笑。

完整程式如下：

```python
"""1993 Heston 隨機波動率：全截斷 Euler 蒙地卡羅。
對應 wiki：Heston (1993) 閉式解 / 特徵函數定價；此處以蒙地卡羅驗證。
模型：dv = κ(θ-v)dt + ξ√v dWv, dS/S = r dt + √v dWs, Corr = ρ。
參數：S0=100, v0=0.04, κ=2, θ=0.04, ξ=0.3, ρ=-0.7；
定價參數：r=0.03, K=100, T=1.0（wiki 常見 ATM 基準）。
格式：變異數全截斷 v+ = max(v,0)；資產採 log-Euler
  S *= exp((r-0.5 v+)dt + √(v+ dt) Zs)，保證 S > 0。
驗證：同路徑 Call/Put 滿足 put-call parity
  C - P = S0 - K exp(-rT)，相對誤差(除以 S0) < 1%；
  且價格為正有限。
只用 numpy，固定種子，不畫圖。
"""
import numpy as np

rng = np.random.default_rng(1)
S0 = 100.0
v0 = 0.04
kappa = 2.0
theta = 0.04
xi = 0.3
rho = -0.7
r = 0.03
K = 100.0
T = 1.0
N = 100
dt = T / N
M = 100000

sqdt = np.sqrt(dt)
v = np.full(M, v0)
S = np.full(M, S0)
corr = np.sqrt(1.0 - rho ** 2)
for _ in range(N):
    z1 = rng.standard_normal(M)
    z2 = rng.standard_normal(M)
    zv = z1
    zs = rho * z1 + corr * z2
    vpos = np.maximum(v, 0.0)
    sqv = np.sqrt(vpos)
    v = v + kappa * (theta - vpos) * dt + xi * sqv * sqdt * zv
    S = S * np.exp((r - 0.5 * vpos) * dt + sqv * sqdt * zs)

disc = np.exp(-r * T)
C = float(np.mean(np.maximum(S - K, 0.0)) * disc)
P = float(np.mean(np.maximum(K - S, 0.0)) * disc)
lhs = C - P
rhs = S0 - K * np.exp(-r * T)
err = abs(lhs - rhs)
rel = err / S0

print(f"Call = {C:.6f}, Put = {P:.6f}")
print(f"parity LHS(C-P) = {lhs:.6f}, RHS = {rhs:.6f}")
print(f"abs_err = {err:.6f}, rel_err = {rel:.6f} (tol 0.01)")
print(f"VERIFY rel_parity_err={rel:.6f} C={C:.4f} P={P:.4f}")
assert np.isfinite(C) and np.isfinite(P), "價格非有限"
assert C > 0 and P > 0, "價格須為正"
assert rel < 0.01, f"put-call parity 誤差過大: {rel}"
```
