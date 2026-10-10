# 1993 -- Steven Heston 的隨機波動率模型：解開波動率微笑之謎

## 案件描述

1993 年，Steven Heston 在《Review of Financial Studies》發表《選擇權定價的隨機波動率閉式解》（A Closed-Form Solution for Options with Stochastic Volatility with Applications to Bond and Currency Options）。他面對的是 1987 年之後困擾市場的謎題：

> **為什麼 Black–Scholes 隱含波動率隨執行價呈「微笑」曲線？**

答案：**波動率本身也是隨機的**——而且 Heston 找到了一個有**閉式解**（特徵函數形式）的模型。

## 前因：1987 年留下的微笑

- 1987 年黑色星期一之前，美股選擇權的隱含波動率大致平坦（符合同一個 $\sigma$ 的假設）。
- 1987 年之後，市場出現持久的「微笑」（equity smirk）：深價外賣權（OTM put）的隱含波動率遠高於價平——**市場用價格投票：常態分配錯了，股價會崩、會跳**。
- 已有的修正路線：
  - 常數彈性變異數（CEV, Cox 1976）
  - 跳躍擴散（Merton 1976）
  - ARCH/GARCH 的統計路線（1982/1986）
- **線索**：Heston 意識到這些路線各有缺陷——他想要一個：波動率隨機、可擬合微笑、且**有閉式解**（能用特徵函數快速定價）的模型。

## 推理過程

### 線索一：雙變數隨機過程

Heston 模型：價格與方差（波動率的平方）都是隨機過程：

$$dS_t = \mu S_t \, dt + \sqrt{v_t}\, S_t \, dW_t^{(1)}$$

$$dv_t = \kappa(\theta - v_t) \, dt + \xi \sqrt{v_t} \, dW_t^{(2)}, \qquad dW^{(1)} dW^{(2)} = \rho \, dt$$

五個參數各司其職：

| 參數 | 意義 | 對應微笑的哪部分 |
|------|------|------|
| $\theta$ | 長期方差水準 | 整體高度 |
| $\kappa$ | 均值回歸速度 | 短端行為 |
| $\xi$ | 方差的波動率（vol of vol） | 笑的**深度** |
| $\rho$ | 價格與方差的相關 | 笑的**歪斜**（skew） |

**數學解讀**：$\rho < 0$（股價跌時波動升）產生負偏斜——正是美股 smirk；$\xi$ 越大，兩端翹得越高——正是微笑。

### 線索二：方差的 Feller 條件

方差過程 $dv = \kappa(\theta - v)dt + \xi\sqrt{v}\,dW$ 是 **CIR 過程**（Cox–Ingersoll–Ross 1985）——平方根項保證方差非負（可為零但撞到零時彈回），Feller 條件 $2\kappa\theta > \xi^2$ 保證不觸零。

### 線索三：特徵函數與閉式解

Heston 的殺手級技巧：歐式選擇權價格可寫成特徵函數的反傅立葉積分（用 Carr–Madan 的記號重述）：

$$C(K) = \frac{e^{-rT}}{2}\left[S_0 - \frac{\sqrt{S_0 K}}{\pi} \int_0^\infty \mathrm{Re}\left[e^{iu\ln(S_0/K)} \varphi(u - i/2)\right] \frac{du}{u}\right]$$

其中 $\varphi(u) = E^Q[e^{iu \ln S_T}]$ 是 $\ln S_T$ 的特徵函數——Heston 用仿射過程理論解出 $\varphi$ 的**閉式形式**（兩個 Riccati ODE 的解）。

**實務意義**：有了閉式特徵函數，定價只需一次數值積分——比蒙地卡羅（見 [1977-Boyle蒙地卡羅選擇權定價.md](1977-Boyle蒙地卡羅選擇權定價.md)）快上千倍，還能做隱含波動率校準（calibration）。

## 現代程式重現：Heston 定價與微笑

```python
import numpy as np
from scipy.integrate import quad

def heston_phi(u, S, v, kappa, theta, xi, rho, r, T):
    """Heston 特徵函數（仿射解）"""
    a = kappa*theta; b = kappa
    d = np.sqrt((rho*xi*u*1j - b)**2 + xi**2*(u**2 + u*1j))
    g = (b - rho*xi*u*1j - d) / (b - rho*xi*u*1j + d)
    C = (r*u*1j*T + a/(xi**2)*((b - rho*xi*u*1j - d)*T
         - 2*np.log((1 - g*np.exp(-d*T))/(1-g))))
    D = (b - rho*xi*u*1j - d)/(xi**2) * (1 - np.exp(-d*T)) / (1 - g*np.exp(-d*T))
    return np.exp(C + D*v + u*1j*np.log(S))

def heston_call(S, K, v, kappa, theta, xi, rho, r, T):
    """以特徵函數反積分定價"""
    f = lambda u: np.real(np.exp(-u*1j*np.log(K))
        * heston_phi(u, S, v, kappa, theta, xi, rho, r, T) / (1j*u))
    integral = 0.5 * quad(f, 0, 100)[0]
    return S - np.sqrt(S*K)/np.pi * integral + np.exp(-r*T)*K/2 * 2  # Lewis 形式簡化

# 校準：用市價隱含波動率反解 (kappa, theta, xi, rho) — 每個交易台的日常工作
```

## 後果

- Heston 成為**隨機波動率的工業標準**：每家衍生品交易台都有一個「Heston 校準器」，每天用市價微笑反解參數。
- **仿射跳擴散（Affine Jump-Diffusion）框架**：Duffie–Pan–Singleton（2000）把 Heston 推廣為「仿射過程」的統一理論——特徵函數法成為定價的通用引擎。
- **傅立葉定價法**：Carr–Madan（1999）的 FFT 定價讓 Heston 型模型快到可以即時報價。
- **SABR（2002）**：Hagan 等人的隨機波動率模型成為利率選擇權的微笑標準。
- 盲點：Heston 難以同時擬合短端與長端的微笑（需要局部波動率模型 Dupire 1994 補充）；且方差可以觸零（違反 Feller 條件時）在數值上造成麻煩。

## 偵探筆記

- 動機：1987 後的波動率微笑違反常數 $\sigma$
- 工具：雙變數 CIR 方差過程、仿射過程、特徵函數閉式解
- 遺產：隨機波動率工業標準、傅立葉定價法
- 盲點：短長端微笑難兼顧、Feller 條件的數值麻煩

## 參考資料

- Heston, S. (1993). "A Closed-Form Solution for Options with Stochastic Volatility with Applications to Bond and Currency Options". *Review of Financial Studies*, 6(2), 327–343.
- Carr, P., Madan, D. (1999). "Option Valuation Using the Fast Fourier Transform". *Journal of Computational Finance*.
- Gatheral, J. (2006). *The Volatility Surface*. Wiley.
