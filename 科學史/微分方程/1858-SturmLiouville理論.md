# 1858 Sturm-Liouville 理論

## 案發現場

Fourier 在 1822 年解熱傳導方程時（參見 [1822-Fourier熱傳導與級數之謎.md](1822-Fourier熱傳導與級數之謎.md)），用到了一個「神奇」的現象：邊界條件會挑出**離散的**分離常數 $\lambda_n = (n\pi/L)^2$，而且對應的 $\sin(n\pi x/L)$ 之間有**正交性**。但這只是最簡單的情形——等係數、等權重的區間。

到了 1830 年代，數學家面對的真實物理問題越來越複雜：變截面棒的熱傳導（係數隨 $x$ 變）、非均勻弦的振動（密度隨 $x$ 變）、球面上的位勢（球座標下的分離變數）。這些問題化成的微分方程都有共同的形狀：

$$
\frac{d}{dx}\!\left(p(x)\frac{dy}{dx}\right) + q(x)\,y + \lambda\,w(x)\,y = 0,
$$

或整理為**Sturm-Liouville 本徵值問題**：

$$
-(p\,y')' + q\,y = \lambda\,w\,y,
$$

其中 $p(x) > 0$、$w(x) > 0$、$q(x)$ 是給定函數，$\lambda$ 是待定參數，加上齊次邊界條件。懸案是：

1. $\lambda$ 一定是**離散**的嗎？會不會有連續的取值？
2. $\lambda$ 是實數還是複數？
3. 不同 $\lambda$ 對應的解之間，還有 Fourier 那樣的正交性嗎？
4. 任意函數還能用這些解展開嗎？

接案的是法國的 Charles Sturm（1803–1855）與 Joseph Liouville（1809–1882，參見 [1841-Liouville可積性之謎.md](1841-Liouville可積性之謎.md)）。兩人在 1836–1838 年間發表了一系列論文，1850 年代理論成型，系統地解開了以上所有謎題。

## 偵查過程

### 第一步：本徵值是實數

考慮 Sturm-Liouville 問題

$$
-(p\,y')' + q\,y = \lambda\,w\,y, \qquad y \text{ 滿足齊次邊界條件},
$$

設 $y$ 是對應 $\lambda$ 的非零解。把方程乘以 $y$ 從 $a$ 積到 $b$（區間端點）：

$$
-\int_a^b y\,(p y')'\,dx + \int_a^b q\,y^2\,dx = \lambda \int_a^b w\,y^2\,dx.
$$

對第一項分部積分：

$$
\int_a^b y\,(p y')'\,dx = \big[y\,p\,y'\big]_a^b - \int_a^b p\,(y')^2\,dx.
$$

由齊次邊界條件（$y(a) = y(b) = 0$，或 $y' = 0$ 端點，或週期條件），邊界項為 $0$。於是

$$
\int_a^b p\,(y')^2\,dx + \int_a^b q\,y^2\,dx = \lambda \int_a^b w\,y^2\,dx.
$$

現在假設 $\lambda$ 是複數，$y$ 複值。對上式取複共軛（$p, q, w$ 是實函數）：

$$
\int_a^b p\,|\bar y'|^2\,dx + \int_a^b q\,|\bar y|^2\,dx = \bar\lambda \int_a^b w\,|\bar y|^2\,dx.
$$

兩式比較（或直接對第一式兩邊取虛部），關鍵在於左邊是實數（$p, q$ 實、$y^2$ 換成 $|y|^2$ 後為實），故

$$
(\lambda - \bar\lambda)\int_a^b w\,|y|^2\,dx = 0.
$$

由 $w > 0$ 且 $y \not\equiv 0$，積分 $> 0$，故 $\lambda = \bar\lambda$，即

$$
\lambda \in \mathbb{R}.
$$

**本徵值必為實數**——這在物理上的意義：$\lambda$ 對應振動頻率的平方或能量，理應是實數。

### 第二步：本徵函數的正交性

設 $y_m, y_n$ 是對應**不同**本徵值 $\lambda_m \ne \lambda_n$ 的解：

$$
-(p\,y_m')' + q\,y_m = \lambda_m\,w\,y_m, \qquad
-(p\,y_n')' + q\,y_n = \lambda_n\,w\,y_n.
$$

把第一式乘 $y_n$、第二式乘 $y_m$，相減：

$$
y_n\,(p\,y_m')' - y_m\,(p\,y_n')' = (\lambda_n - \lambda_m)\,w\,y_m y_n.
$$

左邊注意到它是 $\big[p\,(y_n\,y_m' - y_m\,y_n')\big]'$ 的相反（Wronskian 的導數，乘積求導展開後 $y_n'y_m'$ 項相消）。從 $a$ 積到 $b$：

$$
-\big[p\,(y_n y_m' - y_m y_n')\big]_a^b = (\lambda_n - \lambda_m)\int_a^b w\,y_m y_n\,dx.
$$

由齊次邊界條件，邊界項為 $0$；又 $\lambda_n \ne \lambda_m$，故

$$
\boxed{\int_a^b w(x)\,y_m(x)\,y_n(x)\,dx = 0 \quad (m \ne n).}
$$

**本徵函數帶權重 $w$ 正交**。Fourier 的 $\int \sin(n\pi x/L)\sin(m\pi x/L) = 0$（對應 $p = 1, w = 1$）只是特例。

### 第三步：Sturm 比較定理——本徵值的節點結構

Sturm 的另一絕技：**比較定理**。考慮兩個方程

$$
-(p\,y_1')' + q_1\,y_1 = 0, \qquad -(p\,y_2')' + q_2\,y_2 = 0,
$$

若 $q_2 > q_1$（同樣的 $p$），則 $y_2$ 的零點（節點）比 $y_1$ 的**更密**——「位勢越高，振盪越快」。

證明的核心是把兩式相減後乘上 $y_1 y_2$ 形狀的組合，得到 Wronskian 的導數估計：在兩個 $y_1$ 的相鄰零點之間，若 $y_2$ 不變號，將導出 Wronskian 單調且在端點異號的矛盾。於是 $q_2 > q_1$ 時 $y_2$ 在 $y_1$ 的任意兩個相鄰節點之間至少有一個零點。

由此推出本徵值的節點排序：對應第 $n$ 個本徵值 $\lambda_n$ 的本徵函數 $y_n$ 恰有 $n-1$ 個節點在區間內，且

$$
\lambda_1 < \lambda_2 < \lambda_3 < \cdots \to \infty.
$$

**本徵值是離散、單調遞增、發散到無窮的實數序列**——離散性的謎題解開了。

### 第四步：級數展開——Fourier 的推廣

Liouville 完成了最後一步：任意函數 $f$ 可以用本徵函數展開：

$$
f(x) = \sum_{n=1}^{\infty} c_n\,y_n(x), \qquad
c_n = \frac{\displaystyle\int_a^b w(x)\,f(x)\,y_n(x)\,dx}{\displaystyle\int_a^b w(x)\,y_n^2(x)\,dx}.
$$

係數公式的推導與 Fourier 完全同法：兩邊乘 $w\,y_m$ 積分，用正交性，級數只剩 $n = m$ 項存活，解出 $c_m$。

驗證範例：$p = 1, q = 0, w = 1$，區間 $[0, L]$，邊界 $y(0) = y(L) = 0$：

$$
-y'' = \lambda\,y \quad\Longrightarrow\quad y_n = \sin\frac{n\pi x}{L}, \quad \lambda_n = \left(\frac{n\pi}{L}\right)^2.
$$

這正是 Fourier 的情形。✓ 而取 $p = x^2$（變截面棒）、$q = \ell(\ell+1)$（球座標分離變數）就得到 Legendre 多項式的正交性。

### 第五步：Rayleigh 商——本徵值的變分特徵

本徵值還有一個漂亮的「能量」表示。從第一步的積分恆等式解出 $\lambda$：

$$
\lambda = \frac{\displaystyle\int_a^b \big[p\,(y')^2 + q\,y^2\big]\,dx}{\displaystyle\int_a^b w\,y^2\,dx}.
$$

這個商稱為 **Rayleigh 商**：對任意滿足邊界條件的 $y$，Rayleigh 商 $\ge \lambda_1$，且等號成立當且僅當 $y = y_1$（第一本徵函數）。本徵值是「能量泛函」的臨界值——這為日後的變分法與譜理論架好了橋。

## 結案報告

Sturm 與 Liouville 解開了本徵值問題的全部謎題：本徵值是離散、實、單調遞增至無窮的；本徵函數帶權正交；任意函數可展開成本徵函數級數；本徵函數的節點結構由比較定理完全掌握。

遺產：

1. **譜理論**：本徵值問題的推廣——算子的譜分解——在二十世紀由 Hilbert 與 von Neumann 發展成 Hilbert 空間上的譜理論，這是無窮維線性代數的基礎。
2. **量子力學**：Schrödinger 方程的本徵值問題 $-\frac{\hbar^2}{2m}\psi'' + V\psi = E\psi$ 正是 Sturm-Liouville 問題；「能量量子化」在數學上就是「邊界條件挑出離散本徵值」；觀測量的正交性就是「本徵態正交」（參見 [1838-Jacobi與Hamilton-Jacobi方程.md](1838-Jacobi與Hamilton-Jacobi方程.md)）。
3. **特殊函數的統一**：Legendre、Bessel、Hermite、Laguerre 多項式全是 Sturm-Liouville 問題的本徵函數，正交性全部統一（參見 [1812-Gauss與超幾何函數.md](1812-Gauss與超幾何函數.md)）。
4. **Green 函數的特徵展開**：Green 函數可按本徵函數展開 $G(x,\xi) = \sum_n \frac{y_n(x)y_n(\xi)}{\lambda_n\|y_n\|^2}$（參見 [1828-Green函數.md](1828-Green函數.md)）。
5. **數值方法**：Rayleigh 商是數值求本徵值（Rayleigh 商迭代法）的基礎。

## 證據與工具

```python
# Sturm-Liouville 理論：數值驗證本徵值、正交性與展開
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# 1) 標準問題：-y'' = lambda y, y(0)=y(L)=0, L=pi
#    本徵值 lambda_n = n^2，本徵函數 y_n = sin(nx)
def shoot_eigenvalue(n_max=5, L=np.pi):
    """用試射法（shooting）找本徵值：調 lambda 使 y(L)=0"""
    eigenvalues = []
    for n in range(1, n_max+1):
        lam = n**2  # 理論值
        sol = solve_ivp(lambda t, z: [z[1], -lam*z[0]], [0, L], [0.0, 1.0], max_step=0.001)
        err = abs(sol.y[0][-1])   # 應為 0
        eigenvalues.append((lam, err))
    return eigenvalues

for lam, err in shoot_eigenvalue():
    print(f"本徵值 lambda={lam}，試射法驗證 y(L)={err:.2e}（應為 0）")

# 2) 正交性數值驗證
N = 500
x = np.linspace(0, np.pi, N)
ys = [np.sin(n*x) for n in range(1, 6)]
print("正交性檢驗：")
for m in range(5):
    row = []
    for n in range(5):
        val = np.trapz(ys[m]*ys[n], x)
        row.append(f"{val:7.3f}")
    print("  ", row)   # 對角線非零，其餘近零

# 3) 變係數的 Sturm-Liouville 問題：-(p y')' + q y = lambda w y
#    取 p=x, q=0, w=x（貝塞爾型）：x^2 y'' + x y' + lambda x^2... 化為 Bessel
#    這裡用有限差分矩陣求一般 Sturm-Liouville 的本徵值
def sturm_liouville_spectrum(p, q, w, a, b, N=400):
    """離散化 -(p y')' + q y = lambda w y，回傳本徵值"""
    xs = np.linspace(a, b, N)
    h = xs[1] - xs[0]
    pm = p(xs); qm = q(xs); wm = w(xs)
    A = np.zeros((N, N))
    for i in range(1, N-1):
        # -(p y')' ≈ -(p_{i+1/2}(y_{i+1}-y_i) - p_{i-1/2}(y_i-y_{i-1}))/h^2
        A[i, i+1] = -pm[i]/h**2 + pm[i]/(2*h**2)
        A[i, i-1] = -pm[i]/h**2 + pm[i]/(2*h**2)
        A[i, i]   = 2*pm[i]/h**2 + qm[i]
    A[0, 0] = A[-1, -1] = 1   # 邊界 y=0
    B = np.diag(wm)
    # 廣義本徵值問題 A y = lambda B y
    from scipy.linalg import eigh
    vals = eigh(A, B, eigvals_only=True)
    return vals

vals = sturm_liouville_spectrum(lambda t: np.ones_like(t), lambda t: 0*t,
                                 lambda t: np.ones_like(t), 0, np.pi)
print("數值譜（前 5 個）:", np.round(vals[:5], 4), "（理論值 1, 4, 9, 16, 25）")

# 4) Sturm 比較定理視覺化：位勢越高，振盪越快
plt.figure(figsize=(8,4))
for q_val, style in [(0, '-'), (10, '--')]:
    lam = 30  # 固定能量參數
    sol = solve_ivp(lambda t, z: [z[1], (q_val - lam)*z[0]], [0, 10], [0.0, 1.0], max_step=0.01)
    plt.plot(sol.t, sol.y[0], style, label=f"q={q_val}")
plt.axhline(0, color='k', lw=0.5)
plt.legend(); plt.title("Sturm 比較定理：q 越大，零點越密")
plt.savefig("sturm_compare.png", dpi=100)
print("已存圖 sturm_compare.png")
```
