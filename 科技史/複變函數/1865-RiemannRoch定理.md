# 1865 — Riemann–Roch 定理

## 案件摘要
1857 年，Riemann 在〈Theorie der Abelschen Funktionen〉中證明了他的**Riemann 不等式**：曲面上由除子（divisor）決定的獨立有理函數個數有下界。1865 年，他早逝的學生 Gustav Roch（Riemann 已於 1866 年病逝，此工作完成於 Riemann 生前指導期）在 Göttingen 發表論文，把不等式**補全為等式**——這就是 **Riemann–Roch 定理**：
$$\ell(D) - \ell(K - D) = \deg D + 1 - g$$
一條把「代數曲線上有理函數空間的維數」與「曲面的拓撲（虧格 $g$）」鎖死的公式。它是代數幾何的心臟：此後 150 年的代數幾何，幾乎都是這條公式的推廣史。

## 前因 -- 為什麼會有這個案子
- **Riemann 曲面（1857）**：Riemann 已確立曲面上有理函數的理論，並提出不等式——但他的方法（Dirichlet 原理 + 拓撲）給不出精確的維數。
- **Abel/Jacobi 的橢圓函數**：橢圓函數（$g=1$）有雙週期、亞純函數的零點與極點數目相等。Jacobi 知道 $g=1$ 時的種種特殊恆等式，但一般 $g$ 的情形是一片空白。
- **Roch 的處境**：Gustav Roch（1839–1866）是 Riemann 的博士學生，年輕、體弱、死於肺結核（比導師 Riemann 還早幾個月）。他在短暫的一生中完成了這條公式——偵探史上最令人唏噓的結案。
- 懸案的本質：在一條 Riemann 曲面（緊緻代數曲線）$X$ 上，給定「容許的極點」，最多能有多少個**線性獨立的**有理函數？這是存在性與維數的雙重問題。

## 線索與推理 -- 數學式、程式、理論

### 線索一：除子與 $\ell(D)$
把曲線上的「極點配額」形式化：**除子**是形式和
$$D = \sum_{P \in X} n_P\, P, \qquad n_P \in \mathbb{Z},\ \text{僅有限多個非零}$$
$\deg D = \sum n_P$。定義
$$L(D) = \{ f \text{ 有理函數} : (f) + D \ge 0 \}, \qquad \ell(D) = \dim_{\mathbb{C}} L(D)$$
其中 $(f)$ 是 $f$ 的零點極點除子。條件 $(f) + D \ge 0$ 意思是：$f$ 在 $n_P > 0$ 的點允許至多 $n_P$ 階極點、在 $n_P < 0$ 的點必須有至少 $-n_P$ 階零點。$\ell(D)$ 就是「在配額 $D$ 之下能寫出的獨立有理函數個數」。

### 線索二：典範除子 $K$ 與公式本身
曲面上亞純微分 $\omega$ 的零點極點除子 $(\omega)$ 稱為**典範除子** $K$（任取兩個 $\omega$，$(\omega_1)-(\omega_2)$ 是主除子，所以 $\deg K$ 有定義）。Riemann–Roch 定理斷言：
$$\ell(D) - \ell(K - D) = \deg D + 1 - g$$
其中 $g$ 是曲面的虧格，而 $\deg K = 2g - 2$（微分 $\omega$ 是全純的若且唯若 $K \ge 0$）。
**偵辦邏輯**：等式左邊是「想要的 $\ell(D)$」減去「障礙項 $\ell(K-D)$」。當 $\deg D$ 大到 $\deg D > 2g - 2 = \deg K$ 時，$\ell(K - D) = 0$（$K-D$ 次數為負），障礙消失，得到 Riemann 的原始不等式變成等式：
$$\ell(D) = \deg D + 1 - g \qquad (\deg D > 2g-2)$$
即「配額夠大時，每加一個極點階數就多一個獨立函數」。

### 線索三：三個判例——球面、環面、虧格 2
- **$g = 0$（Riemann 球面 $\hat{\mathbb{C}}$）**：$\deg K = -2$。取 $D = n \cdot \infty$：允許 $\infty$ 處 $n$ 階極點的多項式空間，維數 $n+1$。公式給 $\ell(D) = n + 1 - \ell(-2-n) = n+1$ ✓。球面上有理函數就是有理函數，一切吻合。
- **$g = 1$（環面，橢圓曲線）**：$\deg K = 0$，$K$ 是主除子。取 $D = 0$：$\ell(0) - \ell(K) = 1 - 1 = 0$，而 $\ell(0) = \ell(K) = 1$（唯一的非常數條件下只有常函數與常微分）✓。取 $D = 3 \cdot O$：$\ell(D) = 3 + 1 - 1 = 3$——橢圓曲線的 Weierstrass 方程 $y^2 = x^3 + ax + b$ 的 $\{1, x, y\}$ 恰好三個生成元！公式「算出」了橢圓曲線的方程形狀。
- **$g \ge 2$**：$\ell(K) = g$，即全純微分的空間維數等於虧格——Riemann 的原始發現。Riemann–Roch 保證曲線上函數與微分的一切維數計算。

### 程式碼範例：橢圓曲線上的 $\ell(D)$ 數值驗證
```python
import numpy as np
import matplotlib.pyplot as plt

# g=1（橢圓曲線）上用線性代數驗證 Riemann-Roch：
# D = n*O 時，L(D) 的基底是 {1, x, y, x^2, xy, ...} 中滿足 pole order <= n 的函數
# pole order: ord(1)=0, ord(x)=2, ord(y)=3（橢圓曲線的標準權重）
def basis_pole_orders(n):
    # 回傳 pole order <= n 的單項式清單（divisor D = n*O 的情形）
    funcs = []
    for i in range(0, n // 2 + 1):        # x^i: order 2i
        funcs.append((f"x^{i}" if i else "1", 2*i))
    for j in range(0, (n - 3) // 2 + 1):  # y·x^j: order 2j+3（j=0 即 y），需 2j+3 <= n
        funcs.append((f"y·x^{j}" if j else "y", 2*j + 3))
    return funcs

print("g=1, deg K = 0, Riemann-Roch: l(D) - l(K-D) = deg D")
for n in [1, 2, 3, 4, 5, 6]:
    l_D = len(basis_pole_orders(n))
    l_KD = 0 if n > 0 else 1        # deg(K - nO) = -n < 0 對 n>=1
    rr = l_D - l_KD
    print(f"n={n}: l(D)={l_D}, l(K-D)={l_KD},  l(D)-l(K-D)={rr} (應為 deg D = {n})")

# 幾何驗證：D = 3O 時基底 {1, x, y} 給出 Weierstrass 方程 y^2 = x^3 - x
# 在曲線 y^2 = x^3 - x 上抽樣檢查 y^2 - (x^3 - x) = 0
x = np.linspace(-0.9, 1.4, 300)
resid = np.sqrt(np.maximum(x**3 - x, 0))**2 - (x**3 - x)
print("y² = x³ - x 的最大殘差 =", np.max(np.abs(resid)), "（應為 0）")

plt.figure(figsize=(7, 5))
x = np.linspace(-1.1, 1.5, 500)
y2 = x**3 - x
m = y2 >= 0
plt.plot(x[m], np.sqrt(y2[m]), 'b', label="y = +√(x³-x)")
plt.plot(x[m], -np.sqrt(y2[m]), 'r', label="y = -√(x³-x)")
plt.title(r"l(3O)=3 on elliptic curve: basis {1, x, y}")
plt.legend(); plt.grid(alpha=0.3); plt.axis('equal')
plt.show()
```

程式輸出中每個 $n$ 都有 $\ell(D) - \ell(K-D) = n$，直接驗證了 $g=1$ 的 Riemann–Roch；而 $\ell(3\cdot O) = 3$ 與基底 $\{1, x, y\}$ 說明：**Weierstrass 方程 $y^2 = x^3 - x$ 的形狀不是假設，是 Riemann–Roch 公式的必然結論**。

## 結案 -- 後果與影響
- **代數幾何的心臟**：Riemann–Roch 成為曲線論的計算引擎；1890 年代意大利學派把它推廣到曲面（Castelnuovo、Enriques）。
- **Hirzebruch–Riemann–Roch（1954）**：用示性類（Chern classes）把定理推廣到高維代數簇。
- **Grothendieck–Riemann–Roch（1957）**：Grothendieck 把它變成函子性的相交理論公式，成為現代代數幾何的支柱。
- **Atiyah–Singer 指標定理（1963）**：Riemann–Roch 是它的特例——分析（微分算子的指標）與拓撲的偉大會師，可追溯至 1857/1865 的這條公式。
- 影響至今：橢圓曲線密碼學中點群結構、模形式空間的維數計算（$g=1$ 的 Riemann–Roch 直接算出權 $k$ 模形式的維數）、弦論的真空計數。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Bernhard Riemann | 1857 證明 Riemann 不等式 |
| Gustav Roch | 1865 補全為等式，27 歲病逝 |
| Friedrich Hirzebruch | 1954 示性類推廣（HRR） |
| Alexander Grothendieck | 1957 函子性推廣（GRR） |
| Michael Atiyah / Isadore Singer | 1963 指標定理 |

- G. Roch, «Über die Anzahl der willkürlichen Constanten in algebraischen Funktionen», J. reine angew. Math. **64** (1865)。
- B. Riemann, «Theorie der Abelschen Funktionen», J. reine angew. Math. **54** (1857)。收錄於 *Gesammelte Mathematische Werke*。
- F. Hirzebruch, *Neue topologische Methoden in der algebraischen Geometrie* (1956)。
- A. Grothendieck, «La théorie des classes de Chern», Bull. Soc. Math. France **86** (1957)。
