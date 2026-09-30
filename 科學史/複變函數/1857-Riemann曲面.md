# 1857 — Riemann 曲面

## 案件摘要
1857 年，Riemann 在兩篇論文〈Beiträge zur Theorie der durch die Gauss'sche Reihe...〉（Abel 函數論）與〈Theorie der Abelschen Funktionen〉中，發表了他一生最具原創性的偵破：**Riemann 曲面**。面對多值函數（如 $\sqrt{z}$、$\log z$、橢圓積分的反函數）這樁讓分析學家頭痛百年的懸案，Riemann 的解法大膽得近乎科幻——與其讓函數「多值」，不如把**定義域擴建**：把複平面疊成多層葉片（sheets），在割縫（branch cut）處黏合，讓函數在新的曲面上**單值**。曲面上洞的個數——**虧格（genus）**——成為拓撲不變量，分析與拓撲從此結為一體。

## 前因 -- 為什麼會有這個案子
- **多值函數的百年懸案**：$\sqrt{z}$ 在複平面上取兩個值、$\log z$ 取無窮多個值。Euler、Cauchy 都遇過，但都靠「規定主枝」這種行政手段處理——函數一旦繞奇點一圈，值就跳到另一枝，像兇手逃逸換了假身分。
- **Abel 的橢圓積分**（1826）：積分 $\int \frac{dx}{\sqrt{P(x)}}$（$P$ 為三次或四次多項式）的反函數是多值的，Abel 與 Jacobi 用「兩個週期的函數」勉強處理，但理論支離破碎。
- **1851 博士論文的遺產**：Riemann 已確立「解析函數 = 保形映射」的幾何世界觀，並掌握了 Dirichlet 原理。他自然想到：多值性的根源不在函數，而在**定義域的拓撲**。
- 實際需求：Riemann 在研究超幾何函數（Gauss 級數 $F(a,b;c;z)$）時，發現它的解析延拓在 $z = 0, 1, \infty$ 三點有複雜的分支行為——這正是案發現場。

## 線索與推理 -- 數學式、程式、理論

### 線索一：$\sqrt{z}$ 的兩葉曲面
考慮 $w = \sqrt{z}$。在複平面上，繞 $z=0$ 一圈（$\theta \to \theta + 2\pi$）後 $w = \sqrt{r}e^{i\theta/2} \to -\sqrt{r}e^{i\theta/2}$，函數值跳到另一枝。
Riemann 的解法：取**兩片葉**（兩份複平面），沿正實軸割縫剪開，把第一葉割縫的上岸黏到第二葉割縫的下岸，反之亦然。函數在這個兩葉曲面上是**單值**的：走完一圈會自動「下樓」到另一葉，再走一圈回來——函數值連續，兇手無法換身。
推廣：$w = z^{1/n}$ 需要 $n$ 葉；$w = \log z$ 需要**無窮多葉**（每繞一圈上一層樓，永不回來——$\log$ 的週期是無限的）。

### 線索二：支點、割縫與虧格
**支點**（branch point）：多值函數的「案發地點」。$n$ 值函數在支點處，$n$ 葉黏合在一起（$z=0$ 是 $\sqrt{z}$ 的支點，$\infty$ 也是）。
Riemann 更深的一步：擴建後的曲面是一個**閉曲面**（無邊界、緊緻），它可以分類。曲面上「環柄」的個數稱為**虧格** $g$：
- $g = 0$：球面（$\hat{\mathbb{C}}$，無洞）。
- $g = 1$：環面（甜甜圈形，一個洞）——橢圓函數的家。
- $g \ge 2$：多洞曲面——一般代數函數的家。

關鍵判例：由代數方程 $P(z, w) = 0$ 定義的函數，其 Riemann 曲面的虧格可由 $P$ 的次數與奇點算出。例如 $w^2 = P(x)$，$P$ 為 $m$ 次無重根多項式，則
$$g = \left\lfloor \frac{m-1}{2} \right\rfloor$$
$m = 3, 4$ 時 $g = 1$（橢圓曲線是環面！），$m = 5, 6$ 時 $g = 2$。橢圓函數有兩個週期，正是因為環面上有兩個獨立的閉迴路——代數、分析、拓撲在這裡會師。

### 線索三：拓撲與分析的結合
Riemann 在曲面上做分析：曲面上有**閉迴路的基本群**（雖然 Poincaré 1895 才正式命名），$\sqrt{z}$ 的多值性等價於「沿迴路的單值性表示」——這是 1851 論文中「解析延拓」思想的深化。Riemann 還證明了著名的**Riemann 不等式**（後由 Roch 補全為等式，見 1865 案）：曲面上獨立的有理函數個數受虧格控制。分析的命題由拓撲量（$g$）約束——這在數學史上是第一次。

### 程式碼範例：橢圓曲線 $y^2 = x^3 - x$ 的繪圖
```python
import numpy as np
import matplotlib.pyplot as plt

# 橢圓曲線 y^2 = x^3 - x：實射影圖（左）與環面拓撲示意（右）
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# 左：實平面上的曲線（x^3 - x >= 0 的部分，y = ±sqrt(...)）
x = np.linspace(-1, 1, 500)
y2 = x**3 - x          # 在 [-1,0] 等區間為正
mask = y2 >= 0
ax1.plot(x[mask],  np.sqrt(y2[mask]), 'b', label=r"$y=+\sqrt{x^3-x}$")
ax1.plot(x[mask], -np.sqrt(y2[mask]), 'r', label=r"$y=-\sqrt{x^3-x}$")
for xp in (-1, 0, 1):   # 三個支點
    ax1.plot(xp, 0, 'ko')
    ax1.annotate(f"branch x={xp}", (xp, 0), textcoords="offset points",
                 xytext=(0, 12), ha='center', fontsize=9)
ax1.set_title(r"Elliptic curve $y^2=x^3-x$ (g=1)")
ax1.legend(); ax1.grid(alpha=0.3); ax1.set_aspect('equal')

# 右：環面（橢圓函數的 Riemann 曲面拓撲）
u = np.linspace(0, 2*np.pi, 60)
v = np.linspace(0, 2*np.pi, 30)
U, V = np.meshgrid(u, v)
R, r0 = 2.0, 0.8
X = (R + r0*np.cos(V)) * np.cos(U)
Y = (R + r0*np.cos(V)) * np.sin(U)
Z = r0 * np.sin(V)
ax2.remove()
ax2 = fig.add_subplot(122, projection='3d')
ax2.plot_surface(X, Y, Z, alpha=0.6, cmap='viridis')
# 畫環面上兩條獨立的閉迴路 = 橢圓函數的兩個週期
ax2.plot((R+r0)*np.cos(u), (R+r0)*np.sin(u), 0, 'r', lw=2)          # 經向迴路 a
t2 = np.linspace(0, 2*np.pi, 100)
ax2.plot((R + r0*np.cos(t2))*np.cos(0*t2), (R + r0*np.cos(t2))*np.sin(0*t2),
         r0*np.sin(t2), 'k', lw=2)                                   # 緯向迴路 b
ax2.set_title("Torus: two independent loops = two periods")
ax2.set_xlabel("X"); ax2.set_ylabel("Y"); ax2.set_zlabel("Z")
plt.show()

# 驗證虧格公式：w^2 = P(x)，P 次數 m=3 -> g = floor((m-1)/2) = 1
m = 3
print("m =", m, "-> genus g =", (m - 1) // 2, "（橢圓曲線是環面）")
```

紅與藍兩枝在支點 $x=-1,0,1$ 交會，正是 $\sqrt{P(x)}$ 的分支行為；右圖環面上的兩條獨立閉迴路，對應橢圓函數的兩個週期 $\omega_1, \omega_2$——拓撲（環面、兩個洞迴路）決定了分析（雙週期函數）。

## 結案 -- 後果與影響
- **多值函數懸案結案**：單值化思想成為標準——多值函數在其 Riemann 曲面上單值；今日複分析、代數幾何教科書的必經之路。
- **拓撲與分析結合**：虧格成為第一個被廣泛使用的拓撲不變量，Poincaré 的代數拓撲（1895 起）在此基礎上發展。
- **代數幾何的胚胎**：Riemann 曲面理論是曲線論的起點，Abel 簇、Jacobi 簇（Riemann 1857 同篇建立）成為代數幾何核心工具。
- **1907 單值化定理**：Poincaré 與 Koebe 證明任何單連通 Riemann 曲面等價於 $\hat{\mathbb{C}}$、$\mathbb{C}$ 或 $\mathbb{D}$ 三者之一——Riemann 曲面理論的大一統，也是 Uniformization 的完全體。
- 影響至今：弦論中世界面的虧格展開、模形式理論、橢圓曲線密碼學（ECC），都在用 Riemann 曲面的語言。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Bernhard Riemann | 1857 提出 Riemann 曲面、虧格、單值化思想 |
| Niels Henrik Abel | 橢圓積分多值性的源頭（1826） |
| Carl Gustav Jacobi | 橢圓函數雙週期理論 |
| Henri Poincaré / Paul Koebe | 1907 單值化定理 |

- B. Riemann, «Theorie der Abelschen Funktionen», J. reine angew. Math. **54** (1857)；«Beiträge zur Theorie der durch die Gauss'sche Reihe $F(\alpha, \beta, \gamma, x)$ darstellbaren Funktionen» (1857)。收錄於 *Gesammelte Mathematische Werke*。
- N. H. Abel, «Recherches sur les fonctions elliptiques», J. reine angew. Math. **2–3** (1827–28)。
- C. G. J. Jacobi, *Fundamenta nova theoriae functionum ellipticarum* (1829)。
