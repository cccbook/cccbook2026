# 1885 — Weierstrass 逼近定理

## 案件摘要
1885 年，Karl Weierstrass 年屆七十，在柏林科學院發表〈Über die analytische Darstellbarkeit sogenannter willkürlicher Funktionen reeller Veränderlicher〉：閉區間上的任何連續函數，都可以被多項式**一致逼近**——對任意 $\varepsilon > 0$，存在多項式 $p$ 使 $\|f - p\|_\infty < \varepsilon$。這句話終結了一場持續百年的爭論：冪級數能表示「所有」函數嗎？答案是不能（Cauchy 自己就錯過一次），但**多項式逼近**可以。分析學的一塊基石，在一位老偵探手中落下。

## 前因 -- 為什麼會有這個案子
- 18 世紀 Lagrange 樂觀主義：任何函數都可用冪級數表示——「函數」與「解析表達式」被混為一談。
- 1821 年 Cauchy 舉辦「審判」：他一度「證明」連續函數的級數和連續，隨即被自己與 Abel（1826）舉出反例：一致收斂才是關鍵。$f(x) = \sum \frac{\sin(n^2 x)}{n^2}$ 連續卻處處不解析的例子（Riemann 1861 論文中提及）更顯示冪級數路線的破產。
- 1872 年 Weierstrass 自己投下震撼彈：處處連續、處處不可微的函數
  $$W(x) = \sum_{n=0}^{\infty} a^n \cos(b^n \pi x), \quad 0 < a < 1,\ ab > 1 + \tfrac{3\pi}{2}$$
  「病態函數」時代降臨——連續函數的世界比想像中野蠻。
- 野蠻之中卻有秩序：這些病態函數**能不能**被溫馴的多項式一致逼近？Weierstrass 1885 年給出肯定的答案，且證明中他利用了複變函數的威力——用解析延拓把實函數「託管」到複平面。

## 線索與推理 -- 數學式、程式、理論

### 線索一：定理本身
> 若 $f \in C[a, b]$，則對任意 $\varepsilon > 0$，存在多項式 $p$ 使得
> $$\sup_{x \in [a,b]} |f(x) - p(x)| < \varepsilon$$

關鍵詞是**一致逼近**（$\|\cdot\|_\infty$ 全域控制），不是逐點收斂——前者保證最大誤差可控，是數值方法的合法性來源。注意定理只要求連續：不可微也無妨，病態函數照樣被馴服。

### 線索二：Weierstrass 的原始證明——熱核的秘密
Weierstrass 原始證明分兩步：(1) 用移位摺積 $\int f(t) K_n(x - t)\,dt$ 平滑化；(2) 對解析核用複變函數的冪級數展開。他的核函數後來被認出是**熱核**（Weierstrass 變換）：

$$W_t f(x) = \frac{1}{\sqrt{4\pi t}} \int_{-\infty}^{\infty} f(s)\, e^{-(x-s)^2 / 4t}\, ds$$

當 $t \to 0^+$，$W_t f \to f$ 一致收斂；且 $W_t f$ 是整函數，可被 Taylor 多項式一致逼近。熱核——1890 年前後才被 Picard、1900 年代被 Perron 與 Lebesgue 指認出來——其實是 Fourier 1822 年熱傳導方程的解核。案子背後藏著另一位偵探的舊檔案。

### 線索三：Bernstein 多項式——構造性證明（1912）
1912 年 Bernstein 給出完全構造性的證明：對 $f \in C[0, 1]$，定義

$$B_n(f)(x) = \sum_{k=0}^{n} f\!\left(\frac{k}{n}\right) \binom{n}{k} x^k (1-x)^{n-k}$$

則 $B_n(f) \to f$ 一致收斂。這是機率論的證明：$B_n(f)(x) = E[f(S_n/n)]$，$S_n$ 是二項隨機變數；大數法則 $S_n/n \to x$ 逼近了連續性。多項式逼近與機率收斂在此合流。

### 線索四：Stone–Weierstrass 推廣（1937）
1937 年 Marshall Stone 把定理抽象化：緊緻空間 $X$ 上，若子代數 $A \subset C(X)$ 分離點且含常函數（實版本還需自伴），則 $A$ 在 $C(X)$ 中稠密。三角多項式在圓上稠密（Weierstrass 1885 第二定理）、Lagrange 插值、小波框架——全是特例。這把逼近論從實直線升級為一般緊緻空間，成為泛函分析與調和分析的共同地基。

### 程式碼範例：Weierstrass 逼近多項式擬合
```python
import numpy as np
import matplotlib.pyplot as plt

# 病態目標：|x| 連續但在 0 不可微；再試 Weierstrass 病態函數的部分和
def weierstrass(x, a=0.5, b=11, n=30):
    return sum(a**k * np.cos(b**k * np.pi * x) for k in range(n))

x = np.linspace(-1, 1, 400)

# 用 Bernstein 多項式逼近 |x|（Weierstrass 定理的構造性證明）
def bernstein(f, n, x):
    k = np.arange(n + 1)
    # x 為陣列時的外積版本
    X = np.asarray(x)[:, None]
    K = k[None, :]
    coef = f(K / n) * np.array([np.math.comb(n, kk) for kk in k])
    return np.sum(coef * X**K * (1 - X)**(n - K), axis=1)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, np.abs(x), "k--", lw=2, label="f(x) = |x|")
for n in (5, 15, 40):
    ax.plot(x, bernstein(np.abs, n, x), label=f"Bernstein n={n}")
ax.legend(); ax.set_title("Uniform approximation by polynomials")
plt.show()

# 一致誤差檢驗：max 誤差隨 n 下降
for n in (5, 15, 40):
    err = np.max(np.abs(bernstein(np.abs, n, x) - np.abs(x)))
    print(f"n={n:2d}  ||f - B_n||_inf = {err:.4f}")
```

輸出顯示最大誤差隨 $n$ 增大穩定下降——即使目標 $|x|$ 在 $0$ 不可微，多項式仍一致逼近，定理的「馴服病態」能力直接可見。

## 結案 -- 後果與影響
- **分析學的基石**：$C[a,b]$ 的完備性 + 多項式稠密性 = 泛函分析的標準起點；譜理論、算子理論都在這個舞台上展開。
- **數值方法的合理性**：多項式插值、Chebyshev 逼近、最小平方擬合——「為什麼多項式可信」從此有數學保證；Runge 現象提醒我們一致收斂 ≠ 逐點插值收斂，逼近論成為獨立學科。
- Bernstein 多項式至今用於**電腦輔助幾何設計**（CAGD）：Bézier 曲線正是 Bernstein 基的幾何化身，動畫與字型皆受惠。
- Stone–Weierstrass（1937）成為**C*-代數**與量子力學數學結構的橋樑：Gelfand–Naimark 對偶的雛形。
- 熱核路線最終開花為**熱核證明**：Atiyah–Singer 指標定理（1963）、Hodge 理論的熱核證明，皆可追溯到 Weierstrass 1885 年的那個摺積。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Karl Weierstrass | 提出並證明定理（70 歲） |
| Joseph Fourier | 熱核的源頭（1822） |
| Sergei Bernstein | 1912 構造性證明 |
| Marshall Stone | 1937 推廣至緊緻空間 |
| Augustin-Louis Cauchy | 連續性誤案的當事人 |

- K. Weierstrass, *Über die analytische Darstellbarkeit sogenannter willkürlicher Funktionen reeller Veränderlicher*, Sitzungsber. Königl. Preuss. Akad. Wiss. (1885)。
- S. Bernstein, *Démonstration du théorème de Weierstrass fondée sur le calcul des probabilités*, Comm. Soc. Math. Kharkov (1912)。
- M. H. Stone, *Applications of the theory of Boolean rings to general topology*, Trans. AMS **41** (1937)。
