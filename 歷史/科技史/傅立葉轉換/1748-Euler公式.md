# 1748 - Euler 公式（複指數：萬用基底的前奏）

## 案件摘要
1748 年，Euler 在《無窮分析引論》(Introductio in analysin infinitorum) 中寫下數學史上最美的公式之一：
$$e^{i\theta} = \cos\theta + i\sin\theta.$$
表面上是複數與三角函數的聯姻，實際上卻埋下了 250 年後整個訊號處理的基石：
**複指數 $e^{i\omega t}$ 是線性系統的本徵函數**。傅立葉轉換偵探案的「兇器」在此提前出土。

## 前因 -- 為什麼會有這個案子
- **級數的黃金時代**：Newton 與 Leibniz 之後，數學家熱衷把函數展開為冪級數 $\sin\theta = \theta - \theta^3/3! + \cdots$。
- **複數的地位曖昧**：複數被視為「想像的」計算工具，缺乏幾何與分析的正當性。
- **Euler 的偵探直覺**：他在求冪級數時大膽對比兩個級數：
  $$e^{ix} = 1 + ix - \frac{x^2}{2!} - i\frac{x^3}{3!} + \cdots,\qquad \cos x + i\sin x = \left(1-\frac{x^2}{2!}+\cdots\right) + i\left(x - \frac{x^3}{3!}+\cdots\right)$$
  兩式逐項相同——兇手現形：$e^{ix} = \cos x + i\sin x$。

## 線索與推理 -- 數學式、程式、理論

### 幾何偵查：單位圓
令 $\theta$ 為實角，$e^{i\theta}$ 的實部是 $\cos\theta$、虛部是 $\sin\theta$——它是單位圓上以角速度 $\theta$ 旋轉的點。
令 $\theta = \pi$：
$$e^{i\pi} = -1 \quad\Longrightarrow\quad e^{i\pi} + 1 = 0,$$
五個最重要的常數在一行式中會合。

### 為什麼 $e^{i\omega t}$ 是「完美嫌疑人」
對線性時不變 (LTI) 系統，輸入 $e^{i\omega t}$ 的輸出必為同頻率訊號：
$$h * e^{i\omega t} = H(i\omega)\, e^{i\omega t}.$$
證明（捲積展開）：
$$(h * e^{i\omega t})(t) = \int h(\tau) e^{i\omega(t-\tau)}\,d\tau = e^{i\omega t}\int h(\tau)e^{-i\omega\tau}\,d\tau = H(i\omega)\, e^{i\omega t}.$$
換句話說：**微分方程中的求導在複指數上只是乘法**——
$$\frac{d^n}{dt^n} e^{st} = (s)^n e^{st}.$$
這使得把訊號分解成複指數之和後，任何 LTI 微分方程都變成代數方程。這是傅立葉與拉普拉斯轉換全部力量的根源。

### Python 驗證：逐項級數比對與單位圓

```python
import numpy as np

x = 0.7
n = np.arange(0, 30)
# 直接用複指數級數逐項加總
e_series = np.sum((1j*x)**n / np.array([np.math.factorial(k) for k in n], dtype=float))
print(e_series, np.cos(x) + 1j*np.sin(x))   # 兩者一致
```

輸出：
```
(0.7648421872844885+0.644217687237691j) (0.7648421872844885+0.644217687237691j)
```

## 結案 -- 後果與影響
- 複數取得分析上的正當性，日後成為電路學（相量 $V = V_0 e^{i\omega t}$）、量子力學（$\psi = e^{-iEt/\hbar}$）的通用語言。
- Euler 公式使三角級數可以改寫成複指數級數：
  $$f(t) = \sum_{n=-\infty}^{\infty} c_n e^{in\omega_0 t},\qquad c_n = \frac{1}{T}\int_0^T f(t)e^{-in\omega_0 t}\,dt.$$
  這正是現代形式的傅立葉級數——1753 年 Bernoulli 的疊加主張（見「1753-Bernoulli疊加原理」）將獲得最強的數學武器。
- 1807 年 Fourier 的熱傳導論文（見「1807-Fourier熱傳導論文」），正是在這條線索上破案。

## 關鍵人物與文獻
- **Leonhard Euler**：Introductio in analysin infinitorum (1748)。
- 相關案件：`1753-Bernoulli疊加原理.md`、`1807-Fourier熱傳導論文.md`。
