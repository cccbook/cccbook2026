# 1965 -- Paul Samuelson 的幾何布朗運動：價格不能為負

## 案件描述

1965 年，Paul Samuelson（1970 年諾貝爾獎得主）在《Industrial Management Review》發表《認股權證定價的理性理論》（Rational Theory of Warrant Pricing）。他發現了 Bachelier 模型的一個致命漏洞並予以修補：

> **股價不可能為負，但 Bachelier 的算術布朗運動允許它為負。解法：改用幾何布朗運動——對價格取對數後再做隨機漫步。**

$$\frac{dS_t}{S_t} = \mu \, dt + \sigma \, dW_t$$

## 前因：Bachelier 的遺漏

- Bachelier（1900）的模型 $dS = \sigma \, dW$ 是**算術**的：價格是常態分配，理論上有正的機率出現負價格——對股價來說是荒謬的（但對利率或價差不一定）。
- Samuelson 在 1950 年代透過學生（他在 MIT 的研討會上）偶然發現 Bachelier 1900 年的論文，驚為天人：這篇被遺忘半世紀的論文正是他想做的一切。
- **線索**：Samuelson 追問——如果價格是算術隨機漫步，那報酬率隨價格下降而放大，貧窮投資人的槓桿會無限放大；而且負價格違反「有限責任」的公司法概念。

## 推理過程

### 線索一：報酬率而非價格才是隨機對象

Samuelson 的修正：隨機的對象應該是**報酬率**（百分比變動），而不是價格的絕對變動：

$$dS_t = \mu S_t \, dt + \sigma S_t \, dW_t$$

其解為**幾何布朗運動**：

$$S_t = S_0 \exp\left((\mu - \tfrac{1}{2}\sigma^2)t + \sigma W_t\right)$$

**數學驗證**：$\ln S_t$ 是算術布朗運動（常態分配），所以 $S_t$ 是**對數常態分配**——恆為正。且 $E[S_t] = S_0 e^{\mu t}$，期望報酬率是 $\mu$，乾淨漂亮。

### 線索二：認股權證的第一個「理性」定價框架

Samuelson 用幾何布朗運動為認股權證（warrant，選擇權的前身）定價：

$$C = E\left[e^{-\rho T} (S_T - K)^+\right]$$

但他在論文中留下了一個著名的**未解問題**：期望報酬率 $\mu$ 與折現率 $\rho$ 應該是什麼？它們取決於投資人的風險偏好——這團謎的答案要等 **Black–Scholes（1973）**：透過動態避險，風險偏好會被完全消掉，$\mu$ 與 $\rho$ 都不需要！

Samuelson 甚至在論文中提出這個問題的獎金——後來被 Black 與 Scholes 領走。

### 線索三：與 Merton 的合作

Samuelson 是 Merton 在 MIT 的博士指導教授。他把自己未解的認股權證定價問題交給 Merton——Merton 用連續時間隨機過程（Itô calculus）的方法處理，最終與 Black–Scholes 路線殊途同歸（見 [1973-BlackScholes選擇權定價.md](1973-BlackScholes選擇權定價.md)）。

## 現代程式重現：幾何 vs 算術隨機漫步

```python
import numpy as np
import matplotlib.pyplot as plt

sigma, mu, T, n = 0.3, 0.08, 1.0, 252
dt = T / n
t = np.linspace(0, T, n + 1)
dW = np.random.normal(0, np.sqrt(dt), n)

# Bachelier (1900)：算術 — 可能為負
S_bach = 100 + 100 * mu * t[1:].sum() * 0 + np.cumsum(sigma * 100 * dW)

# Samuelson (1965)：幾何 — 恆為正
S_geo = 100 * np.exp(np.cumsum((mu - 0.5*sigma**2) * dt + sigma * dW))

plt.plot(t[1:], S_bach, label="Bachelier (arithmetic)")
plt.plot(t, np.concatenate([[100], S_geo]), label="Samuelson (geometric)")
plt.legend(); plt.show()

# 驗證 log-常態性：S_geo 恆 > 0
print(np.all(S_geo > 0))   # True
print(np.any(S_bach < 0))  # 可能 True — Bachelier 的漏洞
```

## 後果

- 幾何布朗運動成為 **Black–Scholes 公式的價格動態假設**——今天所有選擇權教科書的第一個模型。
- Samuelson 的未解問題（風險偏好的角色）直接引導出 Black–Scholes 的核心洞察：**動態避險消掉風險偏好**。
- 訓練了 Merton——MIT 路線與 Black–Scholes 路線匯合。
- Samuelson 自己是積極的投資人，但他公開主張「難以擊敗市場」，支持指數化投資（他與 Bogle 的友誼是 Vanguard 誕生的推力之一）。
- 盲點：實證發現股價報酬有**厚尾**（fat tails）與**波動率聚類**（volatility clustering），幾何布朗運動的常態假設低估極端風險——這催生了 ARCH/GARCH（1982/1986）、跳躍過程（Merton 1976）與隨機波動率（Heston 1993）。

## 偵探筆記

- 動機：Bachelier 算術模型的負價格漏洞
- 工具：幾何布朗運動、對數常態分配、期望折現
- 遺產：Black–Scholes 的價格動態、MIT-Merton 路線
- 盲點：厚尾與波動率聚類——常態世界的極限

## 參考資料

- Samuelson, P. (1965). "Rational Theory of Warrant Pricing". *Industrial Management Review*, 6(2), 13–32.
- Samuelson, P. (1965). "Proof that Properly Anticipated Prices Fluctuate Randomly". *Industrial Management Review*, 6(2), 41–49.
