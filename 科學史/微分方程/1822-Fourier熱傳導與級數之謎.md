# 1822 Fourier 熱傳導與級數之謎

## 案發現場

十九世紀初，法國數學家 Jean-Baptiste Joseph Fourier（1768–1830）在擔任格勒諾布爾的伊澤爾省行政長官時，研究的卻是一個「物理學懸案」：**熱如何在固體中傳播？**

這不是茶餘飯後的閒談。熱傳導關係到炮管冷卻、金屬冶煉、建築保溫，是拿破崙時代工業與軍事的實際問題。更重要的是，它是一道當時無人能解的**偏微分方程**：

$$
\frac{\partial u}{\partial t} = \alpha \frac{\partial^2 u}{\partial x^2},
$$

其中 $u(x,t)$ 是位置 $x$、時間 $t$ 的溫度分布。已知的是初始溫度分布 $u(x,0) = f(x)$ 與邊界條件。

當時數學界的主流看法（以 Lagrange 為代表）是：只有「光滑、解析」的函數才能展開成級數，而且級數展開只是形式技巧。若初始溫度分布是「突然加熱半根棒子」那種帶跳躍的片段函數呢？「那種東西根本不是函數！」——這是當時的共識。懸案就此埋下：**任意形狀的初始溫度分布，究竟能不能展開成三角級數？**

1822 年，Fourier 出版《熱的解析理論》（Théorie analytique de la chaleur），宣告了一個驚天動地的答案。

## 偵查過程

### 第一步：分離變數

Fourier 的第一個靈感是「分離變數」：假設解可以寫成只含空間的函數乘上只含時間的函數：

$$
u(x,t) = X(x)\,T(t).
$$

代入熱傳導方程 $u_t = \alpha u_{xx}$：

$$
X(x)\,T'(t) = \alpha\,X''(x)\,T(t).
$$

兩邊除以 $\alpha X T$，把變數分到兩邊：

$$
\frac{T'(t)}{\alpha T(t)} = \frac{X''(x)}{X(x)}.
$$

左邊只含 $t$，右邊只含 $x$，兩者卻要對所有 $x, t$ 相等——唯一的可能是**兩邊都等於同一個常數**。設這個分離常數為 $-\lambda$：

$$
T' = -\alpha\lambda\,T, \qquad X'' = -\lambda\,X.
$$

### 第二步：解出時間與空間因子

時間方程是再熟悉不過的一階 ODE：

$$
T(t) = C\,e^{-\alpha\lambda t}.
$$

空間方程 $X'' + \lambda X = 0$ 依 $\lambda$ 的符號有三種解：

- $\lambda < 0$：$X$ 指數增長或衰減；
- $\lambda = 0$：$X$ 為線性函數；
- $\lambda > 0$：$X = A\cos(\sqrt{\lambda}\,x) + B\sin(\sqrt{\lambda}\,x)$。

考慮長度為 $L$、兩端恆為 $0^\circ$ 的棒子（邊界條件 $X(0) = X(L) = 0$）：$X(0)=0$ 迫使 $A=0$；$X(L)=0$ 迫使 $\sin(\sqrt{\lambda}L)=0$，即

$$
\sqrt{\lambda}\,L = n\pi \quad\Longrightarrow\quad \lambda_n = \left(\frac{n\pi}{L}\right)^2, \qquad n = 1, 2, 3, \ldots
$$

離散的 $\lambda_n$ 就此現身——這是**本徵值問題**的雛形（參見 [1858-SturmLiouville理論.md](1858-SturmLiouville理論.md)）。於是每個分離解為

$$
u_n(x,t) = \sin\!\left(\frac{n\pi x}{L}\right) e^{-\alpha (n\pi/L)^2 t}.
$$

### 第三步：疊加與係數公式

熱傳導方程是線性的，解的線性組合也是解：

$$
u(x,t) = \sum_{n=1}^{\infty} b_n \sin\!\left(\frac{n\pi x}{L}\right) e^{-\alpha (n\pi/L)^2 t}.
$$

剩下的關鍵：$b_n$ 要如何選，才能滿足任意初始條件 $u(x,0) = f(x)$？也就是說：

$$
f(x) = \sum_{n=1}^{\infty} b_n \sin\!\left(\frac{n\pi x}{L}\right) \quad ?
$$

Fourier 的第二個天才靈感來自「逐項積分」的技巧。兩邊同乘 $\sin\!\left(\dfrac{m\pi x}{L}\right)$ 後從 $0$ 積到 $L$，並利用關鍵的正交性質（可由積化和差直接驗證）：

$$
\int_0^L \sin\!\left(\frac{n\pi x}{L}\right)\sin\!\left(\frac{m\pi x}{L}\right)dx
= \begin{cases} 0, & n \ne m, \\ \dfrac{L}{2}, & n = m. \end{cases}
$$

於是級數右邊只剩 $n = m$ 那一項活著：

$$
\int_0^L f(x)\sin\!\left(\frac{m\pi x}{L}\right)dx = b_m \cdot \frac{L}{2},
$$

解出係數：

$$
b_m = \frac{2}{L}\int_0^L f(x)\,\sin\!\left(\frac{m\pi x}{L}\right)dx.
$$

一般情形（不含邊界條件限制），任意 $f(x)$ 的三角級數展開即**Fourier 級數**：

$$
f(x) = \frac{a_0}{2} + \sum_{n=1}^{\infty}\left[a_n\cos\frac{n\pi x}{L} + b_n \sin\frac{n\pi x}{L}\right],
$$

其中

$$
a_n = \frac{1}{L}\int_{-L}^{L} f(x)\cos\frac{n\pi x}{L}\,dx, \qquad
b_n = \frac{1}{L}\int_{-L}^{L} f(x)\sin\frac{n\pi x}{L}\,dx.
$$

### 第四步：函數概念的革命

Fourier 用這套公式算了一個爆炸性的例子：他取

$$
f(x) = \begin{cases} 1, & |x| < \dfrac{\pi}{2} \\[2pt] 0, & \dfrac{\pi}{2} < |x| < \pi \end{cases}
$$

這個**帶跳躍、不連續**的片段常數函數，算出 Fourier 級數：

$$
f(x) = \frac{1}{2} + \frac{2}{\pi}\left(\cos x - \frac{\cos 3x}{3} + \frac{\cos 5x}{5} - \cdots\right),
$$

並發現：在跳躍點處，級數收斂到左右極限的**平均值** $\frac{1}{2}$；在跳躍點附近，部分和還會出現「過衝」（日後稱為 Gibbs 現象）。一個「不光滑的東西」竟然也能展開成收斂級數——這直接挑戰了當時「函數必須是解析式」的定義，迫使數學家把「函數」重新定義為「任意的對應關係」。

## 結案報告

Fourier 解開了熱傳導之謎：任意初始溫度分布都能展開成三角級數，而級數中高頻成分隨時間指數衰減（$e^{-\alpha (n\pi/L)^2 t}$），這完美解釋了「為什麼熱會自動變得平滑」。

遺產極為豐厚：

1. **函數概念革命**：「函數」從解析式解放為任意對應，催生了 Dirichlet 的函數定義與分析嚴格化浪潮（參見 [1824-Cauchy存在性定理.md](1824-Cauchy存在性定理.md)）。
2. **三角級數大辯論**：Lagrange、Poisson、Dirichlet、Riemann 相繼參戰——「Fourier 級數何時收斂到 $f$？」這個問題直接導致 Riemann 積分與 Lebesgue 積分的誕生。
3. **譜理論**：本徵值、本徵函數、正交展開的三件套，經 Sturm-Liouville 發揚光大（參見 [1858-SturmLiouville理論.md](1858-SturmLiouville理論.md)），最終成為量子力學的數學基礎。
4. **現代科技**：從 JPEG 影像壓縮、MP3 音訊、FFT 快速演算法到通訊系統，全都是 Fourier 級數的後代。

## 證據與工具

```python
# 驗證 Fourier 級數：帶跳躍的方波之展開
import numpy as np
import matplotlib.pyplot as plt

L = np.pi
def square_wave(x):
    """方波：|x| < pi/2 時為 1，其餘為 0"""
    return np.where(np.abs(x) < L/2, 1.0, 0.0)

def fourier_square(x, N):
    """方波的 Fourier 級數部分和：f = 1/2 + (2/pi)(cos x - cos 3x/3 + ...)"""
    s = np.full_like(x, 0.5)
    for n in range(1, N+1, 2):          # 只有奇數項
        s += (2/np.pi) * (-1)**((n-1)//2) * np.cos(n*x) / n
    return s

x = np.linspace(-L, L, 1000)
# 檢驗：逐項積分算出的係數應為 a_n = 2/(pi*n) * sin(n*pi/2)
for n in [1, 2, 3, 5]:
    a_n = (1/L) * np.trapz(square_wave(x)*np.cos(n*x), x)
    formula = (2/(L)) * np.sin(n*L/2) / n * L / L  # sin(n*pi/2)/(n) * 2/L
    print(f"a_{n} 數值積分 = {a_n:.4f}, 公式 = {np.sin(n*np.pi/2)*2/L/n:.4f}")

# Gibbs 現象：部分和越多項，過衝不消失只變窄
for N in [5, 11, 51, 201]:
    s = fourier_square(x, N)
    print(f"N={N:4d}  過衝峰值 = {s.max():.4f}（理論極限約 1.0895）")

# 熱傳導方程數值解：初始方波，看高頻如何被指數衰減抹平
alpha = 0.1
ts = [0.0, 0.5, 2.0, 10.0]
plt.figure(figsize=(8, 5))
for t in ts:
    u = np.zeros_like(x)
    for n in range(1, 101, 2):
        b_n = np.sin(n*np.pi/2)*2/L  # 係數
        u += b_n * np.sin(n*x/L*np.pi/L*x/L) if False else b_n*np.sin(n*x)*np.exp(-alpha*n**2*t)
    plt.plot(x, u, label=f"t={t}")
plt.plot(x, square_wave(x), 'k--', label="初始方波")
plt.legend(); plt.title("u_t = alpha u_xx 的級數解")
plt.savefig("fourier_heat.png", dpi=100)
print("已存圖 fourier_heat.png")
```
