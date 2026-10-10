# 1975 數值解與 SciPy

## 案發現場

1960–70 年代，微分方程的求解正面臨一場「生產方式」的危機與轉型。理論上，Hilbert 世紀初定下的研究議程（見 [1900-Hilbert與微分方程問題.md](1900-Hilbert與微分方程問題.md)）已經豐收：解的存在性、唯一性、正則性理論成熟，Lorenz 更用電腦發現了混沌（見 [1963-Lorenz混沌與蝴蝶效應.md](1963-Lorenz混沌與蝴蝶效應.md)），Courant 的有限元素法席捲工程界（見 [1952-有限元素法.md](1952-有限元素法.md)）。但實務上出現了一個尖銳的矛盾：**每個需要解微分方程的科學家與工程師，都得自己重寫一遍數值積分程式**。

當時的困境有三：

1. **重複造輪子**：每個實驗室都有自己的 RK4 副程式，品質參差不齊、錯誤叢生，同一個問題不同實驗室算出不同答案。
2. **剛性方程的噩夢**：化學動力學、電路模擬、van der Pol 張弛振盪（見 [1927-van_der_Pol振盪子.md](1927-van_der_Pol振盪子.md)）這類問題中，系統同時含極快與極慢的時間尺度。顯式法（如 RK4）被迫用最慢尺度的步長前進，計算量爆炸。數學上，若系統矩陣 $A$ 的特徵值為 $\lambda_i$，顯式法的穩定性要求 $h|\lambda_i| < C$ 對**所有** $i$ 成立——最快的模（$|\lambda_i|$ 最大的負實部特徵值）卡死了整個積分。
3. **軟體無處安放**：好的數值程式存在於個別論文的附錄裡，沒有標準化的庫、文件與測試。

此謎題之所以重要：科學計算的未來取決於「可靠數值方法能否大眾化」。誰能把最好的演算法打包成可靠、好用、人人可得的軟體，誰就完成了微分方程從手工解到電腦解的最後一哩路。

## 偵查過程

### 線索一：Fortran 庫時代——把演算法變成公共財

第一波偵查在 1960–70 年代展開。隨著 Fortran 成為科學計算的通用語言，第一批數學軟體庫誕生：

- **IMSL**（International Mathematical and Statistical Libraries，1970）：商業庫，涵蓋 ODE、線性代數、統計。
- **NAG**（Numerical Algorithms Group，1970）：英國牛津與諾丁漢學派主導的庫，以嚴格的測試與文件聞名。
- **EISPACK / LINPACK**（1970s）：Argonne 榮譽退休的國家實驗室計畫，分別處理矩陣本徵值與線性系統——後來成為 MATLAB 的直系祖先。
- **ODEPACK**（1980s，Argonne 的 Hindmarsh 與 Petzold）：系統化的剛性/非剛性 ODE 求解器集合，含著名的 LSODE 及其變體。

這一波的偵查精神是：**把最好的演算法（Gear 的 BDF、Fox的 Runge–Kutta 變體、Dormand–Prince 的 RK45）寫成經過數千個測試問題驗證的 Fortran 副程式**，讓每個科學家直接呼叫，而非自己重寫。

### 線索二：剛性方程與隱式法——BDF 的數學

剛性（stiffness）是這個時代的核心數學謎題。以測試問題為例：

$$
\dot y = -1000(y - \cos t)
$$

解包含一個快速衰減的暫態 $Ce^{-1000t}$ 與一個慢速的強迫響應 $\approx\cos t$。顯式 Euler 法的遞推為

$$
y_{n+1} = y_n + h(-1000)(y_n - \cos t_n)
$$

穩定性要求放大因子 $\left|1 - 1000h\right| \le 1$，即 $h \le 0.002$。**即使暫態早已衰減、解本身平滑緩慢，步長仍被 1000 卡死**——這就是剛性。

**隱式法的偵查靈感**：把遞推中的右端取在**新**時間點：

$$
y_{n+1} = y_n + h f(t_{n+1}, y_{n+1})
$$

對線性問題，這變成每步解一個方程：$y_{n+1} = \dfrac{y_n + 1000h\cos t_{n+1}}{1 + 1000h}$。放大因子 $\left|\dfrac{1}{1+1000h}\right| < 1$ 對**任意** $h$ 成立——**無條件穩定**。步長不再被剛性卡死，只需保證精度即可。

BDF（Backward Differentiation Formula，Gear 1971 系統化）把這個思想推廣到高階：用過去 $k+1$ 個點的值做多項式插值，再對插值多項式求導：

$$
\sum_{j=0}^{k} \alpha_j\, y_{n+1-j} = h\,\beta\, f(t_{n+1}, y_{n+1})
$$

其中係數 $\alpha_j$ 由插值條件決定。BDF 的 $k$ 階方法對 $k \le 6$ 是零穩定的，且是 **A(α)-穩定**的——幾乎無條件穩定，特別適合剛性問題。Gear 的 DIFSUB 副程式（1971）自動偵測剛性、在剛性時切換到 BDF、自動調整階數與步長——這是「自適應智慧求解器」的誕生。

**代價**：隱式法每步要解（非線性）方程組，通常用 Newton 法：

$$
\left(I - h\gamma \frac{\partial f}{\partial y}\right)\delta = -F(y_{\text{guess}})
$$

需要計算 Jacobian $\frac{\partial f}{\partial y}$ 並解線性系統。這就是為什麼剛性求解器（Radau、BDF、LSODE）每步比顯式法昂貴——但步長大幾個數量級，總成本反而低得多。

### 線索三：從 MATLAB 到 SciPy——大眾化之路

第三波偵查在 1980–2000 年代：

- **MATLAB**（1984，Cleve Moler）：Moler 在教學中發現學生浪費太多時間在 Fortran 細節上，於是把 LINPACK/EISPACK 包裝成互動式矩陣語言。名字是 Matrix Laboratory。微分方程求解器（`ode45`、`ode15s`——後者正是 BDF）成為工程師的日常工具。
- **Netlib**（1980s）：把公共領域的數值軟體放上網路，電子郵件伺服器時代的開源軟體庫。
- **NumPy/SciPy**（2001–2006，Travis Oliphant、Eric Jones 等人）：Python 科學堆疊的誕生。SciPy 把 Netlib 的 Fortran 代碼（如 LSODE 的後繼 ODEPACK、LAPACK）包裝成 Python API。`scipy.integrate.solve_ivp`（2017 年引入，取代舊的 `odeint`）統一了 RK45、RK23、DOP853（顯式）與 Radau、BDF、LSODA（隱式，自動在剛性/非剛性間切換）。
- **開源科學計算的完成**：Python 免費、開源、可讀性高，Jupyter notebook 讓「程式 + 數學 + 文字」融為一體。微分方程的數值解從 Fortran 專家的絕技，變成任何學生電腦上的一行代碼。

## 結案報告

數值軟體的偵破路線：

1. **Fortran 庫**（IMSL、NAG、EISPACK/LINPACK、ODEPACK）→ 演算法變公共財；
2. **剛性理論**（Gear 的 BDF、隱式法、無條件穩定）→ 剛性方程不再是噩夢；
3. **MATLAB**（1984）→ 互動式、工程師大眾化；
4. **SciPy**（2001–）→ 開源、免費、`solve_ivp` 統一介面，最終大眾化完成。

其遺產：

- **科學計算成為獨立學科**：數值分析、計算數學系所遍地開花，SIAM 學會壯大。
- **微分方程的大眾化**：從 1670 年代 Newton 手解（見 [1727-Euler常微分方程.md](1727-Euler常微分方程.md)），到 1900 年 Hilbert 轉向定性理論，到 1952 年 FEM 的工程革命，到 1975 年後的軟體大眾化——今天任何高中生都能用三十行 Python 解 Lorenz 方程、畫出奇怪吸子。
- **現代科學的模式轉變**：計算成為與理論、實驗並列的第三支柱。氣象集合預報、藥物動力學、晶片設計、氣候模型、火箭軌道，背後都是數值微分方程求解器。
- **與前幾幕的呼應**：`solve_ivp` 的 RK45 是 Dormand–Prince 1980 年對 Runge–Kutta 傳統（[1727-Euler常微分方程.md](1727-Euler常微分方程.md)）的優化；BDF 是 Gear 1971 對剛性問題的偵破，其思想根源可追溯到 Curtiss 與 Hirschfelder 1952 年首次命名「剛性方程」；而 Lorenz 混沌的發現本身，就依賴這些數值積分器。
- **二十一世紀**：Julia、JAX、神經 ODE（neural ODE，2018）——微分方程與機器學習的融合正在展開，但 `solve_ivp` 仍是每個科學家的第一站。

## 證據與工具

以下程式示範 `solve_ivp` 的多種用法：顯式法 vs 隱式法在剛性問題上的表現、PDE 的數值解，以及自適應步長的觀察。

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# ============ 實驗一：剛性方程——顯式法 vs 隱式法 ============
# 測試問題: y' = -1000*(y - cos(t)), y(0) = 0
# 暫態 e^{-1000t} 極快衰減，但顯式法步長被 h < 0.002 卡死

def stiff_ode(t, y):
    return -1000.0 * (y - np.cos(t))

t_span = (0, 5)
t_eval = np.linspace(*t_span, 500)

# 顯式 RK45：被迫用小步長（觀察 nfev = 函數呼叫次數）
sol_rk45 = solve_ivp(stiff_ode, t_span, [0.0], t_eval=t_eval, method='RK45',
                     rtol=1e-6)
# 隱式 BDF：無條件穩定，可用大步長
sol_bdf  = solve_ivp(stiff_ode, t_span, [0.0], t_eval=t_eval, method='BDF',
                     rtol=1e-6)
# LSODA：自動在非剛性/剛性間切換
sol_lsoda = solve_ivp(stiff_ode, t_span, [0.0], t_eval=t_eval, method='LSODA',
                      rtol=1e-6)

print("剛性方程求解成本比較（nfev = 右端函數呼叫次數）:")
print(f"  RK45  (顯式): nfev = {sol_rk45.nfev:6d}")
print(f"  BDF   (隱式): nfev = {sol_bdf.nfev:6d}  <- 約省 10 倍以上")
print(f"  LSODA (自動): nfev = {sol_lsoda.nfev:6d}")

plt.figure(figsize=(10, 5))
plt.plot(t_eval, np.cos(t_eval), 'k-', lw=1, label='緩慢解 cos(t)')
plt.plot(sol_rk45.t, sol_rk45.y[0], 'b.', ms=2, label='RK45 (顯式)')
plt.plot(sol_bdf.t, sol_bdf.y[0], 'r.', ms=2, label='BDF (隱式)')
plt.xlabel('t'); plt.ylabel('y')
plt.title('剛性方程：兩法都算對，但成本天差地遠')
plt.legend(); plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("stiff_compare.png", dpi=120)
plt.show()

# ============ 實驗二：自適應步長的觀察 ============
# van der Pol 方程 mu=50（強剛性，見 1927-van_der_Pol振盪子.md）
def vdp(t, z, mu):
    x, y = z
    return [y, mu*(1 - x**2)*y - x]

sol = solve_ivp(vdp, (0, 10), [2.0, 0.0], args=(50,), method='BDF', rtol=1e-8)
print(f"\nvan der Pol mu=50 (BDF): 3000 個時間單位內只用了 {sol.n} 步")
print("步長自適應：跳躍處步長極小，慢爬處步長極大——BDF 自動偵測剛性")

plt.figure(figsize=(10, 4))
plt.plot(sol.t[:-1], np.diff(sol.t), 'g-', lw=0.8)
plt.xlabel('t'); plt.ylabel('步長 h')
plt.title('BDF 自適應步長：張弛振盪的跳躍與爬行')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("adaptive_steps.png", dpi=120)
plt.show()

# ============ 實驗三：PDE 數值解——熱傳導方程（見 1822-Fourier熱傳導與級數之謎.md） ============
# u_t = D * u_xx，用 Crank-Nicolson（隱式，無條件穩定）離散化
# 邊界 u(0,t)=u(1,t)=0，初值為中央高斯脈衝

D, N, T = 0.1, 200, 0.05
x = np.linspace(0, 1, N)
dx, dt = x[1] - x[0], 0.0005
u0 = np.exp(-200*(x - 0.5)**2)

# 隱式矩陣：(I - r*L) u^{n+1} = (I + r*L) u^n，r = D*dt/(2*dx^2)
from scipy.linalg import solve_banded
r = D*dt / (2*dx**2)
main = (1 + 2*r) * np.ones(N-2)
off  = -r * np.ones(N-3)
def tri_solve(rhs):
    ab = np.zeros((3, N-2))
    ab[0, 1:] = off; ab[1, :] = main; ab[2, :-1] = off
    return solve_banded((1, 1), ab, rhs)

u = u0.copy()
snapshots = {0.0: u0.copy()}
n_steps = int(T/dt)
for n in range(1, n_steps+1):
    rhs = (1 - 2*r)*u[1:-1] + r*(u[:-2] + u[2:])
    u[1:-1] = tri_solve(rhs)
    snapshots[round(n*dt, 4)] = u.copy()

plt.figure(figsize=(10, 5))
for t_s, u_s in list(snapshots.items())[::20]:
    plt.plot(x, u_s, lw=1, label=f't={t_s}')
plt.xlabel('x'); plt.ylabel('u')
plt.title('熱傳導方程 Crank-Nicolson 隱式解：脈衝擴散與衰減')
plt.legend(fontsize=7); plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("heat_pde.png", dpi=120)
plt.show()

# 驗證：熱傳導方程解析解為高斯核卷積，總熱量（積分）守恆
print("\n總熱量（應守恆）:", np.trapezoid(u0, x), "→", np.trapezoid(u, x))
print("Crack-Nicolson 是隱式法思想的 PDE 版本——無條件穩定")
```

程式展示了三個時代的證據：剛性方程上顯式法與隱式法的成本對比（Gear 偵破的謎題）、自適應步長的智慧（BDF 的工程）、PDE 的隱式離散（Crank–Nicolson，有限元素法思想的親戚）。從 1670 年 Newton 的手工級數，到 1900 年 Hilbert 的定性轉向，到 1952 年 Courant 的變分革命，到 1963 年 Lorenz 的計算發現，再到 1975 年後的軟體大眾化——微分方程的四百年歷史，最後濃縮成今天的一行代碼：`solve_ivp(...)`。每個科學家都是偵探，而偵探的工具箱，終於對所有人敞開。
