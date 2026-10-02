# 1900 -- Louis Bachelier《投機理論》：隨機性進入金融

## 案件描述

1900 年 3 月 29 日，一位名不見經傳的法國博士生 Louis Bachelier 在索邦大學答辯了他的博士論文《投機理論》（Théorie de la Spéculation）。這篇論文做了一件前無古人的事：**用數學為巴黎證券交易所的價格波動建模**。

在 1900 年，「金融」根本不是一門科學。股市被視為賭場，價格波動被視為貪婪與恐懼的產物。Bachelier 卻提出一個激進的主張：

> **價格的未來變化是純隨機的，其行為可以用機率論精確描述。**

## 前因：數學工具已經就位

- 19 世紀機率論的成熟：Laplace、Gauss 建立了常態分配與誤差理論。
- 物理學中的布朗運動還未被解釋（Einstein 要到 1905 年才發表他的解釋）。
- 期貨與選擇權在 19 世紀的巴黎交易所已經交易，但沒有人知道它們「應該」值多少錢。

**線索**：Bachelier 在交易所當過職員，親眼觀察過價格的跳動。他注意到：如果價格的未來變動是可預測的，投機者早就把利潤吃光了——市場會自我抵銷一切可預測性。

## 推理過程

### 線索一：公平賭局

Bachelier 假設市場是「公平的」（fair game）：在任何時刻，價格上漲與下跌的期望值為零：

$$E[S_{t+\Delta t} - S_t] = 0$$

這正是後來「有效市場假說」與「無套利原理」的胚胎。

### 線索二：隨機漫步方程式

他寫下股價的隨機過程（以現代記號重寫）：

$$dS_t = \sigma \, dW_t$$

其中 $W_t$ 是標準布朗運動（他稱之為「機率輻射」radiation de probabilité），$\sigma$ 是波動率。

**關鍵推導**：他推導出價格轉移機率密度滿足**擴散方程式（熱傳導方程）**：

$$\frac{\partial p}{\partial t} = \frac{\sigma^2}{2} \frac{\partial^2 p}{\partial x^2}$$

其解為高斯核：

$$p(x, t) = \frac{1}{\sigma\sqrt{2\pi t}} \exp\left(-\frac{x^2}{2\sigma^2 t}\right)$$

這意味著：時間越長，價格的不確定性以 $\sqrt{t}$ 的速度擴散——這是所有金融風險計算的根基。

### 線索三：第一個選擇權定價公式

Bachelier 甚至推出了歐式選擇權的定價公式（在零利率、算術布朗運動假設下）：

$$C(K) = (S_0 - K)\,\Phi\!\left(\frac{S_0 - K}{\sigma\sqrt{T}}\right) + \sigma\sqrt{T}\,\phi\!\left(\frac{S_0 - K}{\sigma\sqrt{T}}\right)$$

其中 $\Phi$ 是常態 CDF，$\phi$ 是常態 PDF。這比 Black–Scholes 公式早了 **73 年**。

## 現代程式驗證：用 Python 模擬 Bachelier 的隨機漫步

```python
import numpy as np
import matplotlib.pyplot as plt

sigma, T, n = 2.0, 1.0, 1000
dt = T / n
t = np.linspace(0, T, n + 1)

# Bachelier: dS = sigma * dW  （算術隨機漫步）
dW = np.random.normal(0, np.sqrt(dt), n)
S = sigma * np.cumsum(dW)
plt.plot(t, np.concatenate([[0], S]))
plt.title("Bachelier (1900): Arithmetic Random Walk")
plt.xlabel("t"); plt.ylabel("S(t)")
plt.show()

# 驗證 sqrt(t) 擴散律：多條路徑的標準差應與 sqrt(t) 成正比
paths = np.cumsum(np.random.normal(0, np.sqrt(dt), (2000, n)), axis=1)
std_t = paths.std(axis=0)
# 檢驗 std_t / sqrt(t) 是否近似常數 sigma
print(np.mean(std_t / np.sqrt(t[1:])))   # 應接近 2.0
```

## 後果：一個被遺忘的天才

- Bachelier 的論文當時幾乎無人問津。答辯委員（包括數學大師 Poincaré）給了中庸的評語，他一生鬱鬱不得志，只在小學院任教。
- **1931 年**，Kolmogorov 在建立現代機率論時引用了 Bachelier，這是他唯一一次被主流數學界注意。
- **1950 年代**，Samuelson 偶然透過學生發現這篇論文，驚為天人，並推薦給整個經濟學界——隨機漫步理論由此復活。
- **1960 年代之後**：Markowitz、Sharpe、Fama、Black–Scholes 全部站在 Bachelier 的肩膀上。
- Einstein 1905 年的布朗運動論文在物理學界享有盛名，而 Bachelier 同樣的數學在金融學晚到了半世紀才被發現——**科學史上最著名的「同名異命」案例之一**。

## 偵探筆記

- 動機：市場公平性 → 隨機性（後來的有效市場假說）
- 工具：機率論 + 熱傳導方程
- 遺產：$\sqrt{t}$ 擴散律、第一個選擇權公式
- 盲點：算術布朗運動允許價格為負——這個漏洞要等 Samuelson（1965）與 Black–Scholes（1973）來修補。

## 參考資料

- Bachelier, L. (1900). *Théorie de la Spéculation*. Annales Scientifiques de l'École Normale Supérieure.
- Courtault et al. (2000). "Louis Bachelier on the Centenary of Théorie de la Spéculation". *Mathematical Finance*.
- MacKenzie, D. (2006). *An Engine, Not a Camera*.
