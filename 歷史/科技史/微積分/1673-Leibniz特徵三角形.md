# 1673 — Leibniz 特徵三角形

## 案件摘要
1673 年至 1676 年間，年輕的德國外交官兼哲學家 Leibniz 在巴黎展開了一場改變數學史的秘密偵查：他試圖找出「切線問題」與「求積問題」背後的共同原理。在他的手稿中，一個由 $dx$、$dy$ 與斜邊構成的微小直角三角形——「特徵三角形」（characteristic triangle）——逐漸浮出水面。四年后，他掌握了 $\int y\,dy = y^2/2$ 這類「求和即求積」的對偶規律，並發明了沿用至今的記號 $dx$、$dy$、$\int$。這樁無人知曉的巴黎懸案，正是微積分誕生的案發現場。

## 前因 -- 為什麼會有這個案子
- 1635 年 Cavalieri 出版《幾何學的不可分量》：把面積看成無窮多條「不可分量的線」疊加，能算出許多面積，但方法粗糙、邏輯飽受批評（卡瓦列里原理：若兩圖形在每個高度上的截面長度相等，則面積相等）。
- 1663–1669 年 Isaac Barrow 在劍橋的《幾何講座》（Lectiones Geometricae）中以幾何方式處理切線與面積，甚至隱含了「切線與面積互逆」的線索——他正是牛頓的老師，但他始終沒有把這些線索拼成一套通用演算法。
- 1672 年 Leibniz 以梅因茲選帝侯使節身份抵達巴黎，初遇荷蘭物理學家 Huygens。Huygens 要他先解決一個「總和數列」問題：計算 $\sum \frac{1}{n(n+1)}$ 之類的三角和。Leibniz 解出後，Huygens 收他為入門弟子，指導他研讀自己的《鐘擺論》與 Descartes 的著作。
- 動機非常實際：Leibniz 夢想一套「普遍語言」（characteristica universalis），讓所有推理都能化為符號運算。切線與面積問題，正好是他選中的試金石。

## 線索與推理 -- 數學式、程式、理論

### 線索一：特徵三角形
1673 年 8 月，Leibniz 在巴黎研究 Pascal 關於圓的論文時靈光一閃：把曲線上一段無窮小的弧，看成以 $dx$、$dy$ 為兩股、$ds$ 為斜邊的小直角三角形，且這個小三角形與曲線的法線、次法線構成的大三角形**相似**。由相似性立即得到切線的幾何關係：

$$\frac{dy}{dx} = \frac{T}{y} \quad \text{（$T$ 為次切距，即切線在 $x$ 軸上的投影長）}$$

這個小三角形之所以「特徵」，是因為它把曲線的局部幾何（切線斜率、法線長、次切距）全部編碼進 $dx : dy = y : T$ 的比例關係中。Leibniz 在 1673 年手稿中寫道：這個方法「對所有曲線都成立」，比 Descartes 的代數圓法與 Fermat 的切線法更通用。

### 線索二：求和與求積的對偶——$\int y\, dy = y^2/2$
1675 年 10 月 29 日前後的手稿是全案最關鍵的物證。Leibniz 思考：把縱坐標 $y$ 的無窮多個微小增量 $dy$ 全部加起來，會得到什麼？

$$\int y\, dy = \frac{y^2}{2}$$

他的推理是：$\sum y\,\Delta y$ 正是直角三角形（或拋物線下區域）的面積；而 $\frac{1}{2}(y + dy)^2 - \frac{1}{2}y^2 = y\,dy + \frac{(dy)^2}{2}$，略去無窮小的高階項後恰好等於 $y\,dy$。換句話說，**求和（面積）與差分（切線）互為逆運算**——這正是微積分基本定理的雛形。1675 年 11 月 11 日的手稿中，他首次用 $\int$（拉丁文 summa 的首字母拉長）代表求和，用 $dx$、$dy$ 代表微分。

### 線索三：超越 Cavalieri 與 Barrow
- Cavalieri 只能對個別曲線逐一求積，Leibniz 的記號卻把「面積」變成可以**按代數法則運算**的對象：$\int f\,dx$ 滿足線性律、分部律，甚至有換元律。
- Barrow 的《幾何講座》講座十已幾何化地證明：若面積 $A(x)$ 由縱坐標 $y$ 累積而成，則 $A$ 的增量與 $y\,dx$ 成比例——但 Barrow 用純幾何語言表述，沒有演算法，也沒有記號。Leibniz 讀過 Barrow（很可能在 1673 年訪倫敦時經 Oldenburg 接觸），他的突破是把幾何真理**符號化、機械化**。
- 1676 年 Leibniz 已能用 $\int x^n dx = \frac{x^{n+1}}{n+1}$、乘積微分律、以及 transmutation（變換法）處理圓與 $\pi/4$ 的級數展開（Arctan 級數）。

### 程式碼範例：sympy 驗證 Leibniz 的求和即求積，以及特徵三角形
```python
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

x, y = sp.symbols('x y', real=True)

# 1) Leibniz 1675 的核心發現：int y dy = y^2/2
expr = sp.integrate(y, y)
print("∫ y dy =", expr)                       # y**2/2

# 2) 驗證「求和與差分互逆」：(1/2)(y+dy)^2 - (1/2)y^2 ≈ y dy
dy = sp.symbols('dy', positive=True)
diff_ = (y + dy)**2 / 2 - y**2 / 2
print("差分展開 =", sp.expand(diff_))          # y*dy + dy**2/2 → 略去高階項即 y*dy

# 3) 驗證冪函數律 ∫ x^n dx = x^(n+1)/(n+1)，與 d/dx 互逆
for n in [2, 3, 5, 10]:
    F = sp.integrate(x**n, x)
    print(f"n={n}: ∫x^n dx = {F},  d/dx 回來 = {sp.simplify(sp.diff(F, x))}")

# 4) 特徵三角形：拋物線 y = x^2 上某點的 dx, dy, ds
f = sp.Lambda(x, x**2)
x0 = 1.0
xs = np.linspace(0, 1.4, 100)
ys = xs**2
dx, dyv = 0.4, f(1.4) - f(1.0)          # 放大版的 Δx, Δy
fig, ax = plt.subplots(figsize=(6, 6))
ax.plot(xs, ys, lw=2, label='y = x²')
ax.plot([1, 1 + dx], [f(1.0), f(1.0)], 'r-', lw=2, label='dx')
ax.plot([1 + dx, 1 + dx], [f(1.0), f(1.4)], 'g-', lw=2, label='dy')
ax.plot([1, 1 + dx], [f(1.0), f(1.4)], 'k--', lw=2, label='ds（斜邊）')
ax.set_aspect('equal'); ax.legend()
ax.set_title("Leibniz 特徵三角形（放大示意）")
plt.show()

# 5) 數值驗證微積分基本定理：∫₀¹ x² dx 應等於 F(1)-F(0) = 1/3
area = np.trapz(xs[xs <= 1]**2, xs[xs <= 1])
print("數值面積 =", area, " 理論 = 1/3 =", 1/3)
```

程式輸出顯示：`∫ y dy = y²/2`、差分展開為 $y\,dy + \frac{(dy)^2}{2}$（略去二階無窮小即 Leibniz 的推理）、冪函數律對任意 $n$ 成立且求導後完美還原——1675 年巴黎手稿裡的每一條線索，都被現代符號計算一一證實。

## 結案 -- 後果與影響
- 1684 年，Leibniz 在《Acta Eruditorum》發表〈Nova Methodus pro Maximis et Minimis〉，微積分首次公開問世——但那已是另一個案件。
- 萊布尼茲記號 $dx$、$dy$、$\int$ 因其結構清晰，成為今日全世界微積分課本的標準語言；相比 Newton 的流數記號 $\dot{x}$，$\frac{dy}{dx}$ 與 $\int f\,dx$ 更能直接表達「比」與「和」的本質。
- 特徵三角形的思想後來發展為微分幾何的接觸元素與弧長元素 $ds = \sqrt{dx^2 + dy^2}$。
- 「求和即求積」的對偶性，在 150 年後被 Riemann 積分理論嚴格化，成為微積分基本定理的現代形式。
- 遺留疑點：Leibniz 1673 年訪倫敦是否看過牛頓或 Barrow 的未發表手稿，成為日後優先權之爭的導火線。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Gottfried W. Leibniz | 1673–1676 巴黎研究，發明記號與演算法 |
| Christiaan Huygens | 巴黎的指導者，引入 Leibniz 走入數學 |
| Bonaventura Cavalieri | 不可分量法先驅（1635） |
| Isaac Barrow | 《幾何講座》，切線與面積的幾何先聲 |

- G. W. Leibniz, 《巴黎手稿》（1673–1676），Hanover 手稿庫，"Historia et origo calculi differentialis" 相關文件。
- I. Barrow, *Lectiones Geometricae* (1670)。
- B. Cavalieri, *Geometria indivisibilibus* (1635)。
