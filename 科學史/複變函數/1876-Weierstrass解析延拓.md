# 1876 — Weierstrass 解析延拓

## 案件摘要
1876 年，61 歲的 Karl Weierstrass 把他散落各處（有些寫於 1840 年代、當時他還是中學教師）的複分析工作整理發表，包括〈Zur Theorie der eindeutigen analytischen Funktionen〉與〈Zur Theorie der aus $n$ Haupteinheiten gebildeten complexen Größen〉。這些工作代表與 Cauchy、Riemann 完全不同的偵辦路線：**不靠幾何直覺、不靠積分**，而是從一個最純粹的起點——**冪級數**（函數元）——出發，用**解析延拓鏈**逐步擴張函數的疆域，並用**整函數的因子分解**（Weierstrass 因子定理）重建整個函數。這是複分析的第二座大山，也是現代嚴格分析（$\varepsilon$–$\delta$）的發源地。

## 前因 -- 為什麼會有這個案子
- **嫌棄 Cauchy 的積分直覺**：Cauchy 的理論依賴積分與路徑的幾何圖像，證明常有漏洞（如交換極限與積分）。Weierstrass 主張分析必須「算術化」——一切從級數的**嚴格收斂**出發，不要畫圖。
- **Abel 函數論的召喚**：Weierstrass 年輕時（1840 年代在 Westphalia 的中學教書）自學 Abel 的橢圓函數論，立志用冪級數重建 Abelian 函數的整個理論。他 1841–1843 年的工作（圓環展開、函數元）因期刊延遲而埋沒，1876 年才正式問世。
- **Riemann 的對手戲**：1851/1857 年 Riemann 用幾何方法（Riemann 曲面、Dirichlet 原理）攻下了多值函數與 Abelian 積分。Weierstrass 1870 年批評 Dirichlet 原理不嚴格，並用自己的冪級數路線給出「代數的」替代證明——兩座大山的路線之爭。
- 懸案的本質：一個冪級數只在它的收斂圓盤內定義函數。圓盤邊界之外呢？能不能用「接力」的方式把函數延拓出去？延拓後的多值性怎麼用純代數方法處理？

## 線索與推理 -- 數學式、程式、理論

### 線索一：函數元與解析延拓鏈
Weierstrass 的起點是一個**函數元**（function element）：一對
$$(P(z, a), R) = \left(\sum_{n=0}^{\infty} c_n (z-a)^n,\; \text{收斂半徑 } R\right)$$
延拓的方法是**接力**：在圓盤內取一點 $b$，把級數**重展開**為以 $b$ 為中心的新冪級數
$$P(z, b) = \sum_{n=0}^{\infty} d_n (z-b)^n, \qquad d_n = \frac{P^{(n)}(b)}{n!}$$
（這純粹是項與項的運算，不需要積分！）新級數的收斂半徑可能更大，於是函數的定義域擴張。一串接力
$$(P(z, a_0), R_0) \to (P(z, a_1), R_1) \to (P(z, a_2), R_2) \to \cdots$$
稱為**解析延拓鏈**。所有經由任何鏈可達的函數元的總體，稱為一個**完整解析函數**（complete analytic function）。

### 線索二：單值性問題與自然邊界
延拓有兩種結局：
- **單值性問題**：沿不同路徑延拓到同一點，可能得到**不同的值**（如 $\log z$）——這正是 Riemann 曲面處理的現象。Weierstrass 用「函數元的等價類」純代數地處理：兩個函數元等價若它們在某重疊區一致。函數元的集合配上延拓關係，就是 Riemann 曲面的代數版本（今日的層論、解析空間概念的先聲）。
- **自然邊界**（natural boundary）：有些級數的收斂圓**無法跨過**。例如
$$f(z) = \sum_{n=0}^{\infty} z^{2^n} = z + z^2 + z^4 + z^8 + \cdots$$
在 $|z| < 1$ 收斂，而圓周上的每個二進根 $e^{2\pi i k/2^m}$ 都是奇點——單位圓是「自然邊界」，函數被終身監禁在圓盤內。Weierstrass 最早系統研究這種現象。

### 線索三：整函數的因子分解（Weierstrass 因子定理）
延拓的終點站之一是**整函數**（entire function，全平面解析）。Weierstrass 證明：給定任意離散的複數序列 $\{a_n\}$（無重複或按重數計），存在整函數恰好以這些點為零點：
$$f(z) = z^m\, e^{g(z)} \prod_{n=1}^{\infty} E_p\!\left(\frac{z}{a_n}\right)$$
其中**初等因子**（elementary factors）
$$E_0(w) = 1 - w, \qquad E_p(w) = (1-w)\exp\!\left(w + \frac{w^2}{2} + \cdots + \frac{w^p}{p}\right), \quad p \ge 1$$
$g(z)$ 是整函數。偵辦邏輯：直接寫 $\prod (1 - z/a_n)$ 可能不收斂；每個因子補上指數修正項 $E_p$，使它「接近 1」得夠快，讓乘積**整體收斂**。特例：
- $\sin \pi z = \pi z \prod_{n=1}^{\infty}\left(1 - \frac{z^2}{n^2}\right)$——Euler 的猜想在 Weierstrass 手中成為定理。
- $\Gamma$ 函數的 Weierstrass 乘積：$\dfrac{1}{\Gamma(z)} = z e^{\gamma z} \prod_{n=1}^{\infty}\left(1+\dfrac{z}{n}\right)e^{-z/n}$。

### 程式碼範例：解析延拓的冪級數收斂半徑示意
```python
import numpy as np
import matplotlib.pyplot as plt
from math import factorial

# 例一：自然邊界 f(z) = sum z^(2^n)，單位圓是牢籠
def f_nat(z, terms=12):
    s = np.zeros_like(z, dtype=complex)
    for n in range(terms):
        s += z**(2**n)
    return s

# 沿實軸掃向單位圓，看 |f| 如何爆炸
x = np.linspace(0, 0.99, 300)
plt.figure(figsize=(8, 4.5))
plt.semilogy(x, np.abs(f_nat(x)), label=r"$|f(z)|$, f(z)=Σz^{2^n}")
plt.axvline(1.0, color='r', ls='--', label="natural boundary |z|=1")
plt.xlabel("Re z along real axis"); plt.ylabel("|f| (log scale)")
plt.title("Power series trapped by natural boundary")
plt.legend(); plt.show()

# 例二：解析延拓接力——重展開 √(1+z) 超越初始收斂半徑
# 初始函數元：以 a0=0 為中心，(1+z)^{1/2} 的級數，半徑 R=1（奇點 z=-1）
def binom_sqrt_coeffs(a0, N=30):
    # 對 (1+z)^{1/2} 在 z=a0 處重展開：係數 = binom(1/2,n) (1+a0)^{1/2-n}
    z0 = 1 + a0
    coeffs = []
    for n in range(N):
        c = np.prod([0.5 - k for k in range(n)]) / factorial(n) * z0**(0.5 - n)
        coeffs.append(c)
    return np.array(coeffs)

def eval_series(coeffs, a0, z):
    return sum(c * (z - a0)**n for n, c in enumerate(coeffs))

# 第一棒：以 0 為中心，展開到 |z|<1 內一點 b=0.5
b = 0.5
c1 = binom_sqrt_coeffs(0)
val = eval_series(c1, 0, b)
print("第一棒：√(1+0.5) ≈", val, "精確 =", np.sqrt(1.5))

# 第二棒：以 b=0.5 為中心重展開，新半徑 = |b - (-1)| = 1.5，可達 z = 1.4
c2 = binom_sqrt_coeffs(b)
z_far = 1.4                       # 超出初始半徑 R=1！
print("第二棒：√(1+1.4) ≈", eval_series(c2, b, z_far), "精確 =", np.sqrt(2.4))
print("z=1.4 已超出初始收斂半徑 |z|<1 —— 解析延拓成功越獄")
```

例一中 $|z|\to 1^-$ 時級數以對數速度爆炸，單位圓是自然邊界；例二中第二棒的重展開把定義域從 $|z|<1$ 擴張到以 $0.5$ 為心、半徑 $1.5$ 的圓盤——$z=1.4$ 這個初始牢籠外的點被成功偵辦，這就是 Weierstrass 解析延拓的接力本質。

## 結案 -- 後果與影響
- **複分析的第二座大山**：Weierstrass 的冪級數路線與 Cauchy 的積分路線、Riemann 的幾何路線三足鼎立；他的 $\varepsilon$–$\delta$ 嚴格化（極限、連續、一致收斂）成為現代分析的語言。
- **整函數理論誕生**：Weierstrass 因子定理 → Hadamard 1893 的整函數階與乘積公式 → 現代複分析的核心章節。
- **現代代數函數論**：函數元與延拓的代數處理，經 Dedekind–Weber 1882 的理想論版本，成為現代代數幾何中層（sheaf）、概型概念的遠祖。
- **橢圓函數的完全重建**：Weierstrass 用冪級數建立了 $\wp$ 函數理論（$\wp'^2 = 4\wp^3 - g_2\wp - g_3$），不依賴任何幾何，是 Abelian 函數論的嚴格版本。
- 影響至今：橢圓函數密碼學、Γ 函數的數值計算、冪級數求和的電腦代數系統，都在用 Weierstrass 的語言。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Karl Weierstrass | 冪級數路線、解析延拓、因子定理（1876） |
| Niels Henrik Abel | 橢圓函數論的召喚 |
| Augustin-Louis Cauchy | 積分路線（被 Weierstrass 嫌棄的對手） |
| Bernhard Riemann | 幾何路線（另一座大山） |
| Richard Dedekind / Heinrich Weber | 1882 代數函數論的理想論版本 |
| Jacques Hadamard | 1893 整函數的階理論 |

- K. Weierstrass, «Zur Theorie der eindeutigen analytischen Funktionen», Abh. Königl. Akad. Wiss. Berlin (1876)；«Zur Theorie der aus $n$ Haupteinheiten gebildeten complexen Größen» (1876)。收錄於 *Mathematische Werke*, Bd. 2。
- K. Weierstrass, «Darstellung einer analytischen Funktion einer komplexen Veränderlichen...»（1841，延遲發表）。
- R. Dedekind & H. Weber, «Theorie der algebraischen Funktionen einer Veränderlichen», J. reine angew. Math. **92** (1882)。
