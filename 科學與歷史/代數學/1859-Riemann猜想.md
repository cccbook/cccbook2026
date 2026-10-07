# 1859-Riemann猜想

## 案件摘要
1859 年，黎曼（Bernhard Riemann）發表唯一的數論論文《論小於給定值的質數個數》，八頁改寫了整個數學。他給出質數計數的精確公式，並提出一個至今未解的猜想：zeta 函數所有非平凡零點都在臨界線上。這是千禧年七難之首。

## 前因 -- 為什麼會有這個案子
- 歐拉的 $\zeta(s) = \prod_p (1-p^{-s})^{-1}$（1737）把質數裝進了一個級數；Chebyshev（1850）證出 $\pi(x)$ 的粗略夾逼 $0.92\,x/\ln x < \pi(x) < 1.1\,x/\ln x$。
- 高斯憑手算猜想 $\pi(x) \approx \mathrm{Li}(x) = \int_2^x \frac{dt}{\ln t}$（對數積分）。
- 黎曼在哥廷根接任 Dirichlet 的教席，1859 年當選柏林科學院院士，以這篇論文作為就職回禮——他帶來了複分析的全力武器。

## 線索與推理 -- 數學式、程式、理論

### 線索一：π(x)、Li(x) 與 zeta
質數計數函數 $\pi(x) = \#\{p \le x : p \text{ 為質數}\}$。高斯猜想的近似：

$$\pi(x) \sim \mathrm{Li}(x) = \int_2^x \frac{dt}{\ln t} \qquad (\text{質數定理, 1896})$$

黎曼的 zeta 函數起初定義為 $\mathrm{Re}(s) > 1$ 的級數：

$$\zeta(s) = \sum_{n=1}^{\infty} \frac{1}{n^s} = \prod_{p}\left(1 - p^{-s}\right)^{-1}$$

### 線索二：解析延拓與函數方程
黎曼把 $\zeta(s)$ **解析延拓**到全複數平面（除 $s=1$ 單極點），並證明對稱的函數方程：

$$\zeta(s) = 2^s \pi^{s-1} \sin\left(\frac{\pi s}{2}\right) \Gamma(1-s)\, \zeta(1-s)$$

函數方程把 $s$ 與 $1-s$ 鏡像，臨界帶 $0 < \mathrm{Re}(s) < 1$ 對稱於 $\mathrm{Re}(s) = \frac{1}{2}$——這條線就是「臨界線」。

### 線索三：猜想本身
黎曼計算了若干零點後寫下（原文意譯）：「非平凡零點的實部**很可能**都是 $\frac{1}{2}$」——一個隨手的旁註，成了 166 年未解之謎：

> **Riemann 猜想**：$\zeta(s) = 0$ 且 $0 < \mathrm{Re}(s) < 1 \;\Rightarrow\; \mathrm{Re}(s) = \frac{1}{2}$，即所有非平凡零點都在臨界線上。

```python
import numpy as np
import matplotlib.pyplot as plt

def zeta_grid(re, im_range):
    """在垂直線 Re(s)=re 上取 |zeta(s)|"""
    from scipy.special import zeta
    s = re + 1j * np.array(im_range)
    return np.array([abs(zeta(x)) for x in s])

# 驗證：平凡零點 s = -2, -4, -6；s=1 是極點
from scipy.special import zeta
print(f"|zeta(-2)| = {abs(zeta(-2)):.2e}  (平凡零點)")
print(f"|zeta(0.5 + 14.134725j)| = {abs(zeta(0.5+14.134725j)):.2e}  (第一個非平凡零點!)")
```

### 線索四：臨界線上的數值驗證
至今已驗證超過 **$10^{13}$** 個零點全在 $\mathrm{Re}(s)=\frac{1}{2}$ 上。可用 mpmath 的 `zetazero` 取出第 $n$ 個零點：

```python
from mpmath import zetazero, mp
mp.dps = 30
N = 1000
ok = all(abs(mp.re(zetazero(n)) - 0.5) < 1e-25 for n in range(1, N+1))
print(f"臨界線驗證：前 {N} 個非平凡零點實部皆 = 1/2 ？ {ok}")
# 第 1 個零點：0.5 + 14.13472514173469379045i（虛部即 'Riemann–Siegel z 值' 的首例）
```

### 線索五：零點 ↔ 質數分佈的顯式公式
黎曼的**顯式公式**把 $\pi(x)$ 寫成對零點求和（Von Mangoldt 形式）：

$$\psi(x) = x - \sum_{\rho} \frac{x^{\rho}}{\rho} - \ln(2\pi) - \ln(1-x^{-2})$$

每個零點 $\rho = \frac{1}{2} + i\gamma$ 貢獻一個振盪項 $x^{1/2}e^{i\gamma\ln x}/\rho$：**零點是質數分佈的「頻譜」**。若 RH 成立，則 $\pi(x) = \mathrm{Li}(x) + O(\sqrt{x}\ln x)$——誤差達到理論極限。

```python
import numpy as np
import matplotlib.pyplot as plt
from sympy import primerange
from scipy.integrate import quad
import mpmath as mp

def Li(x):  # 對數積分
    return quad(lambda t: 1/np.log(t), 2, x)[0]

xs = np.arange(100, 20001, 100)
pix = [len(list(primerange(2, x))) for x in xs]
liy = [Li(x) for x in xs]

plt.figure(figsize=(9, 4))
plt.plot(xs, pix, label='π(x) 實際質數個數')
plt.plot(xs, liy, label='Li(x) 黎曼近似')
plt.legend(); plt.xlabel('x'); plt.ylabel('個數'); plt.grid(True)
plt.title('π(x) ∼ Li(x)：兩條曲線幾乎重合'); plt.savefig('prime_li.png', dpi=120)
```

## 結案 -- 後果與影響
- **未結案**：RH 至今懸而未決，是克雷研究所 2000 年設立的**千禧年七難**之一，懸賞一百萬美元。
- Hadamard–de la Vallée Poussin（1896）用黎曼的方法證明質數定理（去掉零點假設）；Hardy（1914）證明臨界線上有無窮多零點；Conrey（1989）證明至少 40% 的零點在臨界線上。
- RH 與大量定理等價（$\pi(x)$ 誤差界、RSA 相關的偽隨機性、Miller–Rabin 判定的确定性版本），其真偽直接影響現代密碼學的理論安全邊際。
- 黎曼的「頻譜」觀點啟發 Hilbert–Pólya 猜想（零點對應某自伴算子的特徵值）與隨機矩陣理論（Montgomery 配對猜想起 1972 年與 Dyson 的著名對話）。

## 關鍵人物與文獻
- **Riemann, B.**（1859）：《Über die Anzahl der Primzahlen unter einer gegebenen Größe》（8 頁）。
- **Edwards, H. M.**（1974）：《Riemann's Zeta Function》，逐行解讀原始論文。
- **Hadamard / de la Vallée Poussin**（1896）：質數定理。
- **Conrey, J. B.**（2003）：《The Riemann Hypothesis》綜述（Notices of the AMS）。
