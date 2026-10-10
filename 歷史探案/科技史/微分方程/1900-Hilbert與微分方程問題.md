# 1900 Hilbert 與微分方程問題

## 案發現場

1900 年 8 月 8 日，巴黎，第二屆國際數學家大會。三十八歲的德國數學家 David Hilbert（1862–1943）走上講台，發表了一場將支配整個二十世紀數學研究議程的演說。他提出了二十三個數學問題，其中好幾個直接指向微分方程的核心謎題。這不是偶然：十九世紀末，Poincaré 的定性理論剛剛起步（見 [1886-Poincare三體問題.md](1886-Poincare三體問題.md)），Lyapunov 的穩定性理論也才問世，但非線性微分方程的整體圖像仍然模糊不清。

當時的未解之謎主要有四條線索：

1. **物理學能否公理化？** Boltzmann 的統計力學、Maxwell 的電磁學雖然成功，但基礎邏輯鬆散，機率與極限概念的數學地位曖昧不明。
2. **非線性方程的解的結構？** Poincaré 已發現極限環（limit cycle），但一個平面多項式向量場能有幾個極限環？無人能答。
3. **變分問題的解是否光滑？** Weierstrass 舉出反例顯示極小化序列可能不收斂到光滑函數，那麼變分法還可靠嗎？
4. **線性微分方程的單值性？** Fuchs 型方程的解沿奇點繞行後會如何變換？Riemann 的遺志尚待完成。

這些謎題之所以重要，是因為它們決定了二十世紀微分方程的研究方向：從「求顯式解」徹底轉向「證明解的存在性、唯一性、正則性與定性結構」。

## 偵查過程

### 線索一：第 6 問——物理學的公理化

Hilbert 的第 6 問要求：「對物理學的基礎，尤其是力學，進行幾何學式的公理化處理。」他在 1900 年前後正專注於積分方程與位勢理論，建立了

$$
\int_a^b K(x,y)\,u(y)\,dy = f(x)
$$

這類積分方程的譜理論，並預見它將成為量子力學的數學骨架（後來確實如此，von Neumann 的 Hilbert 空間理論正是第 6 問精神的延續）。

Hilbert 的推理方式是：幾何學之所以穩固，是因為 Euclid 以降的公理化方法把直覺轉成邏輯。力學的核心是微分方程 $\ddot x = F(x,t)$，若能把「質量、力、時間」的直覺也公理化，則物理定律的推導將如同幾何定理的證明一般嚴格。這條線索後來促成了 Courant–Hilbert《數學物理方法》與 Kolmogorov 機率論公理化（1933）。

### 線索二：第 16 問——極限環個數

第 16 問的後半部是數學史上最著名的懸案之一：考慮平面多項式向量場

$$
\dot x = P(x,y), \qquad \dot y = Q(x,y)
$$

其中 $P, Q$ 為 $n$ 次多項式。Hilbert 問：閉軌線（極限環）的個數 $H(n)$ 的上界為何？

Poincaré 在 1880 年代已用定性方法證明：極限環是孤立閉軌，且必須包含奇點在其內部。Hilbert 的推理是：既然解的顯式表示（如級數）對非線性方程無能為力，那就問「解的拓撲結構」這種可以回答的問題。他猜測 $H(n)$ 有限。

Dulac 在 1923 年聲稱證明了有限性，但 1981 年 Ilyashenko 與 Écalle 各自發現其證明有漏洞，並在 1991–1992 年才真正補全。而對 $n=2$ 的 $H(2)$ 上界，至今（2026）仍未確定——最好的結果界於 4 與 37 之間。這是二十一世紀仍然活著的十九世紀之謎。

### 線索三：第 19 問——變分法的正則性

第 19 問問道：變分積分

$$
J[u] = \int_a^b F\left(x, u(x), u'(x)\right)\,dx
$$

的極小化解 $u$ 是否必然是解析的（甚至二次可微）？

Hilbert 自己在 1900 年用「直接法」給了部分答案。傳統變分法（Euler–Lagrange 路線）先假設極小解存在再推導方程：

$$
\frac{d}{dx}\frac{\partial F}{\partial u'} - \frac{\partial F}{\partial u} = 0
$$

但 Weierstrass 的反例顯示極小化序列可能沒有極小解。Hilbert 的靈感是：**不假設解存在，而是取極小化序列 $u_1, u_2, \dots$，證明其收斂極限就是解**。他用 Dirichlet 原理示範了這個方法：對 Dirichlet 積分

$$
D[u] = \int_\Omega |\nabla u|^2\,dx
$$

取極小化序列，利用等度連續性論證收斂。這個「直接法」孕育了 Sobolev 空間與弱解概念——20 世紀 PDE 理論的基石。而完整的正則性問題，由 De Giorgi（1957）與 Nash（1958）在非線性橢圓方程上解決，部分動機正是第 19 問。

### 線索四：第 21 問——Fuchs 型方程的單值化

第 21 問（Riemann–Hilbert 問題）：給定 Riemann 球面上的奇點 $\{a_1, \dots, a_n\}$ 與每個奇點指定的單值矩陣（monodromy matrix）$M_k$，是否存在 Fuchs 型線性微分方程

$$
\frac{d^2 w}{dz^2} + p(z)\frac{dw}{dz} + q(z)w = 0
$$

其解的單值表示恰好給定這些矩陣？

這個問題源於 Riemann 對超幾何方程的研究：解沿奇點 $a_k$ 繞行一圈後，$w \mapsto M_k w$。Hilbert 問的是「反問題」：先給單值矩陣，反求方程。此問題的線性版本在 1908 年前後由 Hilbert 的學生 Plemelj 大致解決（但 1986 年 Kohn 發現其證明對一個退化情形有誤）。而非線性版本則催生了 Riemann–Hilbert 方法，成為現代可積系統、孤立子理論（見 [1812-Gauss與超幾何函數.md](1812-Gauss與超幾何函數.md)）與隨機矩陣理論的核心工具。

## 結案報告

Hilbert 的二十三問題像一份偵探的案情清單，把二十世紀微分方程的偵查方向定了調：

- **第 6 問** → von Neumann 的 Hilbert 空間、Kolmogorov 機率公理化、量子力學的數學基礎。
- **第 16 問** → 定性理論與動力系統的黃金時代，Smale、Arnold 的工作，至今未解。
- **第 19 問** → 直接法、Sobolev 空間、弱解、De Giorgi–Nash 正則性理論，最終通向 [1952-有限元素法.md](1952-有限元素法.md) 的數值革命。
- **第 21 問** → Riemann–Hilbert 方法、可積系統、逆散射理論。

最深遠的遺產是**方法論的轉向**：從「找公式」到「證結構」。Hilbert 教會數學家：當顯式解不存在時（大多數非線性方程正是如此），存在性、唯一性、正則性、穩定性與拓撲結構才是可以回答、也值得回答的問題。這條思路直接鋪墊了 van der Pol 的非線性振盪（[1927-van_der_Pol振盪子.md](1927-van_der_Pol振盪子.md)）與 Lorenz 的混沌（[1963-Lorenz混沌與蝴蝶效應.md](1963-Lorenz混沌與蝴蝶效應.md)）。

## 證據與工具

以下程式示範第 16 問的核心現象：一個簡單的平面多項式系統如何產生極限環，以及解對參數的定性變化。

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# 第 16 問示範：平面多項式向量場的極限環
# 考慮系統  x' = y + x*(1 - x^2 - y^2),  y' = -x + y*(1 - x^2 - y^2)
# 這是極坐標下的 x' = r*(1-r^2) 的等價形式，有唯一極限環 r = 1

def field(t, z):
    x, y = z
    return [y + x*(1 - x**2 - y**2), -x + y*(1 - x**2 - y**2)]

# 從不同初值出發（圓內 r=0.2 與圓外 r=2.0），都會趨近極限環 r=1
t_span = (0, 20)
t_eval = np.linspace(*t_span, 2000)

sol_in  = solve_ivp(field, t_span, [0.2, 0.0], t_eval=t_eval, rtol=1e-9)
sol_out = solve_ivp(field, t_span, [2.0, 0.0], t_eval=t_eval, rtol=1e-9)

fig, axes = plt.subplots(1, 2, figsize=(11, 5))
for ax, sol, title in [(axes[0], sol_in, "初值在圓內 (r=0.2)"),
                       (axes[1], sol_out, "初值在圓外 (r=2.0)")]:
    theta = np.linspace(0, 2*np.pi, 100)
    ax.plot(np.cos(theta), np.sin(theta), 'k--', lw=1, label='極限環 r=1')
    ax.plot(sol.y[0], sol.y[1], 'b-', lw=1.2, label='軌線')
    ax.plot(sol.y[0, 0], sol.y[1, 0], 'go', label='初值')
    ax.set_title(title); ax.legend(); ax.set_aspect('equal'); ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig("hilbert16_limit_cycle.png", dpi=120)
plt.show()

# 驗證：半徑隨時間趨近 1（無論從內或從外）
r_in  = np.hypot(sol_in.y[0],  sol_in.y[1])
r_out = np.hypot(sol_out.y[0], sol_out.y[1])
print("圓內初值最終半徑:", r_in[-1])   # ≈ 1.0
print("圓外初值最終半徑:", r_out[-1])  # ≈ 1.0

# 延伸：改變參數觀察定性變化——這正是 Hilbert 問「個數上界」的動機
# 例如 Lienard 型系統 mu 參數化（見 1927-van_der_Pol振盪子.md）
```

這個簡單的程式展示了定性理論的精神：不求出解析解，而是直接觀察解的**幾何行為**——閉軌、吸引性、對初值的依賴。Hilbert 在 1900 年提出的問題，正是要數學家把這種幾何直覺變成嚴格定理。而當這類系統維度升到三維，行為將徹底失控——那就是 Lorenz 在 1963 年發現的混沌。
