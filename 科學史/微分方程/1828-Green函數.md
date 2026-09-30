# 1828 Green 函數

## 案發現場

1828 年，英國諾丁漢的一位磨坊工 George Green（1793–1841）自費出版了一本小冊子：《論數學分析在電磁理論的應用》（An Essay on the Application of Mathematical Analysis to the Theories of Electricity and Magnetism）。印刷量極少，買的人寥寥無幾，幾乎注定埋沒。

但這本冊子裡藏著一個劃時代的思想武器：**如何求偏微分方程的邊值問題之解？**

當時的懸案是位勢理論的核心問題。給定一個帶電導體或電荷分布，空間中的靜電位勢 $V(x)$ 滿足 Laplace 方程

$$
\nabla^2 V = \frac{\partial^2 V}{\partial x^2} + \frac{\partial^2 V}{\partial y^2} + \frac{\partial^2 V}{\partial z^2} = 0,
$$

或帶電荷源時滿足 Poisson 方程 $\nabla^2 V = -4\pi\rho$。已知的是邊界上的位勢（邊界條件）。問題：**區域內部的位勢是多少？** 對一般形狀的區域（不是球、不是無限平面），當時完全無解。

更傳奇的是：Green 是**完全自學**的磨坊工，四十歲前沒受過正規大學教育，靠著圖書館與自費購書自修數學。1828 年這本冊子提出的三個工具——Green 函數、Green 恆等式、Green 定理——把邊值問題整個改寫了。

## 偵查過程

### 第一步：Green 恆等式——偵查的第一把鑰匙

Green 的出發點是一個樸素的分部積分推廣。設 $u, v$ 是區域 $\Omega$ 上的光滑函數。從散度定理出發：

$$
\int_\Omega \nabla\cdot(u\,\nabla v)\,d\tau = \oint_{\partial\Omega} u\,\frac{\partial v}{\partial n}\,ds,
$$

其中 $\partial/\partial n$ 是邊界上的外法向導數。把左邊展開 $\nabla\cdot(u\nabla v) = \nabla u\cdot\nabla v + u\nabla^2 v$，得到 **Green 第一恆等式**：

$$
\int_\Omega \nabla u\cdot\nabla v\,d\tau + \int_\Omega u\,\nabla^2 v\,d\tau = \oint_{\partial\Omega} u\,\frac{\partial v}{\partial n}\,ds.
$$

交換 $u, v$ 再相減，消去 $\nabla u\cdot\nabla v$ 項，得 **Green 第二恆等式**：

$$
\int_\Omega \big(u\,\nabla^2 v - v\,\nabla^2 u\big)\,d\tau = \oint_{\partial\Omega}\left(u\,\frac{\partial v}{\partial n} - v\,\frac{\partial u}{\partial n}\right)ds.
$$

這個恆等式把「體積內的資訊」與「邊界上的資訊」連了起來——這正是解邊值問題需要的橋樑。

### 第二步：點源之謎——Green 函數的誕生

Green 的天才靈感：**考慮一個「點電荷」的位勢**。在物理上，把單位點電荷放在點 $\xi$，它在空間中產生的位勢是

$$
\Phi(x) = \frac{1}{|x - \xi|}.
$$

數學上，這個函數在 $x \ne \xi$ 處滿足 Laplace 方程 $\nabla^2 \Phi = 0$，而在 $x = \xi$ 處是奇點（廣義函數的語言：$\nabla^2\frac{1}{|x-\xi|} = -4\pi\,\delta(x-\xi)$）。

Green 接著做了關鍵的一步：**把點源與邊界條件結合**。定義**Green 函數** $G(x, \xi)$ 為滿足以下條件的函數：

1. $G(x,\xi) = \dfrac{1}{|x-\xi|} + H(x,\xi)$，其中 $H$ 在 $\Omega$ 內調和（$\nabla^2 H = 0$）；
2. $G(x,\xi) = 0$ 當 $x$ 在邊界 $\partial\Omega$ 上。

也就是說：$G$ 是「點電荷的位勢」加上一個「抵消邊界值」的調和修正項。對給定區域求 $H$ 本身也是邊值問題，但 $H$ 的邊界值是已知的負的 $\frac{1}{|x-\xi|}$，比原問題容易。

### 第三步：偵查的高潮——把解寫成積分

現在把 Green 第二恆等式用在 $u = V$（要求的位勢）、$v = G(\,\cdot\,,\xi)$ 上。因為 $V$ 調和（$\nabla^2 V = 0$），而 $\nabla^2 G = -4\pi\delta(x - \xi)$（在 $\xi$ 處的點源），第二恆等式右邊的體積積分只剩點源的貢獻：

$$
\int_\Omega \big(V\,\nabla^2 G - G\,\underbrace{\nabla^2 V}_{=0}\big)d\tau = -4\pi V(\xi).
$$

再算邊界積分：因為 $G$ 在邊界上為 $0$，邊界積分中 $u\frac{\partial v}{\partial n}$ 項消失，只剩

$$
\oint_{\partial\Omega} -V\,\frac{\partial G}{\partial n}\,ds.
$$

合起來：

$$
-4\pi V(\xi) = -\oint_{\partial\Omega} V\,\frac{\partial G}{\partial n}\,ds,
$$

解出內部任一點 $\xi$ 的位勢：

$$
V(\xi) = \frac{1}{4\pi}\oint_{\partial\Omega} V(x)\,\frac{\partial G(x,\xi)}{\partial n}\,ds.
$$

**這是本案的破案時刻**：區域內部的位勢，完全由邊界上的位勢值乘上 Green 函數的法向導數積分決定。只要知道 Green 函數，任何邊值問題迎刃而解。

若有電荷源（Poisson 方程 $\nabla^2 V = -4\pi\rho$），同法可得

$$
V(\xi) = \int_\Omega G(x,\xi)\,\rho(x)\,d\tau + \frac{1}{4\pi}\oint_{\partial\Omega} V\,\frac{\partial G}{\partial n}\,ds.
$$

### 第四步：驗證——球的情形

Green 用球域驗證。半徑為 $a$、球心在原點的球，用「鏡像法」求 Green 函數：點 $\xi$ 在球內的鏡像點為 $\xi^* = \dfrac{a^2}{|\xi|^2}\xi$，則

$$
G(x, \xi) = \frac{1}{|x-\xi|} - \frac{a/|\xi|}{|x - \xi^*|}.
$$

驗證：當 $|x| = a$ 時 $|x - \xi| = \dfrac{a}{|\xi|}|x - \xi^*|$（可由餘弦定理直接核對），故 $G = 0$。✓ 把這個 $G$ 代入積分公式，就得到著名的 **Poisson 積分公式**：

$$
V(\xi) = \frac{a(a^2 - |\xi|^2)}{4\pi}\int_{|x|=a}\frac{V(x)}{|x - \xi|^3}\,ds.
$$

一維的情形更清楚：區間 $[0,1]$ 上 $-y'' = f$、邊界 $y(0)=y(1)=0$ 的 Green 函數是

$$
G(x,\xi) = \begin{cases} x(1-\xi), & x \le \xi, \\ \xi(1-x), & x > \xi, \end{cases}
$$

而解為 $y(x) = \displaystyle\int_0^1 G(x,\xi)f(\xi)\,d\xi$。

## 結案報告

Green 解開了位勢理論的邊值問題之謎：**解 = Green 函數加權的邊界（與源）積分**。他還證明了區域內部邊值問題的解若存在則唯一（用 Green 第一恆等式：兩個解之差 $u$ 滿足 $\nabla^2 u = 0$ 且邊界值為 $0$，則 $\int_\Omega |\nabla u|^2 = 0$，故 $u$ 為常數，邊界為 $0$ 故恆為 $0$）。

遺產：

1. **現代電磁學**：Maxwell 在《電磁通論》中大量引用 Green 的方法；今天電磁散射、天線設計的積分方程法全是 Green 函數的後代。
2. **量子力學**：Schödinger 方程的傳播子（propagator）就是量子力學版的 Green 函數；費曼的路徑積分本質上是 Green 函數的疊加。量子力學的譜理論基礎則可追溯到 Sturm-Liouville 理論（參見 [1858-SturmLiouville理論.md](1858-SturmLiouville理論.md)）。
3. **偏微分方程一般理論**：Green 函數法成為橢圓型、拋物型、雙曲型方程的統一武器；Riemann 把 Green 函數帶進複變函數論，導出 Riemann 映射定理。
4. **調和分析與譜理論**：Green 函數的「特徵展開」思想（$G(x,\xi) = \sum \frac{\phi_n(x)\phi_n(\xi)}{\lambda_n}$）是本徵函數展開理論的先聲，連結了 Fourier 的級數革命（參見 [1822-Fourier熱傳導與級數之謎.md](1822-Fourier熱傳導與級數之謎.md)）。

## 證據與工具

```python
# Green 函數數值驗證：一維邊值問題 -y'' = f, y(0)=y(1)=0
import numpy as np
from scipy.integrate import solve_ivp

N = 200
x = np.linspace(0, 1, N)

def green_1d(x, xi):
    """一維 Green 函數：x<=xi 時 x(1-xi)，否則 xi(1-x)"""
    return np.where(x <= xi, x*(1 - xi), xi*(1 - x))

def solve_by_green(f):
    """用 Green 函數積分公式求 y(x) = ∫ G(x,xi) f(xi) dxi"""
    xi = np.linspace(0, 1, N)
    return np.array([np.trapz(green_1d(xx, xi)*f(xi), xi) for xx in x])

# 測試：f(x) = sin(pi x)，精確解 y = sin(pi x)/pi^2
f = lambda t: np.sin(np.pi*t)
y_green = solve_by_green(f)
y_exact = np.sin(np.pi*x)/np.pi**2
print("Green 積分解 vs 精確解 最大誤差:", np.max(np.abs(y_green - y_exact)))

# 直接用 ODE 求解器驗證
sol = solve_ivp(lambda t, Y: [Y[1], -np.sin(np.pi*t)], [0, 1], [0, np.pi/np.pi**2])
print("ODE 數值解終點 y(1) ≈ 0 ?", abs(sol.y[0][-1]))

# 二維驗證：自由空間 Green 函數 1/|x-xi| 是 Laplace 算子的基本解
def green_free(X, Y, xi, eta):
    return 1.0/np.sqrt((X - xi)**2 + (Y - eta)**2)

gx = np.linspace(0.1, 1, 30)
X, Y = np.meshgrid(gx, gx)
xi, eta = 0.5, 0.5
G = green_free(X, Y, xi, eta)
# 數值驗證：在遠離奇點處 Laplace(G) ≈ 0
lap = np.zeros_like(G)
h = gx[1] - gx[0]
lap[1:-1,1:-1] = (G[2:,1:-1] + G[:-2,1:-1] + G[1:-1,2:] + G[1:-1,:-2] - 4*G[1:-1,1:-1])/h**2
mask = np.sqrt((X - xi)**2 + (Y - eta)**2) > 0.2   # 避開奇點
print("遠離奇點處 max|Laplace G| =", np.abs(lap[mask]).max(), "（應接近 0）")

# 一維 Green 函數圖示
import matplotlib.pyplot as plt
plt.figure(figsize=(6,4))
for xi_ in [0.25, 0.5, 0.75]:
    plt.plot(x, green_1d(x, xi_), label=f"xi={xi_}")
plt.legend(); plt.title("一維 Green 函數 G(x, xi)")
plt.savefig("green_1d.png", dpi=100)
print("已存圖 green_1d.png")
```
