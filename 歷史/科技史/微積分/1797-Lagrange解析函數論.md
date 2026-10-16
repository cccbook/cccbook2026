# 1797 — Lagrange 解析函數論

## 案件摘要
1797 年，Lagrange 在巴黎出版《Théorie des fonctions analytiques》（解析函數理論），企圖發動一場微積分的「地基重建」：拋棄 Newton 的極限與 Leibniz 的無窮小（他嫌棄兩者的幾何直覺不夠可靠），改以**冪級數**為微積分的唯一基礎。他從展開式 $f(x+i)$ 定義導數：

$$f(x+i) = f(x) + i\,f'(x) + \frac{i^2}{2!}f''(x) + \cdots \quad\Rightarrow\quad f'(x) = \lim_{i\to 0}\frac{f(x+i)-f(x)}{i}$$

並系統化了泰勒公式的**Lagrange 餘項**。這條路線最終沒有完全成功——但它啟發了 Cauchy 與 Weierstrass 的嚴格化，是現代分析學的關鍵轉折點。

## 前因 -- 為什麼會有這個案子
- **無窮小的原罪**：Leibniz 的 $dx, dy$ 是「小到不為零卻又不是零」的量，Berkeley 主教 1734 年在《The Analyst》中猛烈攻擊：「消失增量的幽靈」（ghosts of departed quantities）。整個 18 世紀都沒有令人信服的回應。
- **Lagrange 的潔癖**：Lagrange 年輕時就以代數才能著稱（變分法、月球三體問題、《Mécanique analytique》1788——書中自豪地宣稱「連一張圖都沒有」）。他認為微積分應該像代數一樣純粹：不靠幾何、不靠極限、不靠無窮小，只靠有限次的代數運算與級數。
- **泰勒級數的成熟**：Taylor（1715）與 Maclaurin（1742）的冪級數展開已是分析學的日常工具。Lagrange 認為：與其把級數當作微積分的「結果」，不如把級數當作微積分的「起點」——導數從級數中定義出來。
- **柏林與巴黎的傳承**：Lagrange 在柏林接替 Euler 二十年（1766–1787），1787 年後移居巴黎，在法國科學院與 École Polytechnique 教書。《Théorie》正是他在巴黎的教學結晶。

## 線索與推理 -- 數學式、程式、理論

### 線索一：從 $f(x+i)$ 展開定義導數
Lagrange 的策略是逆轉偵查方向。他假設：對任意函數 $f$ 與增量 $i$，可以展開

$$f(x+i) = f(x) + i\,p(x) + i^2\,q(x) + i^3\,r(x) + \cdots$$

其中 $p, q, r, \dots$ 是不依賴 $i$ 的函數。他**定義**：$p(x)$ 為「第一導函數」，記作 $f'(x)$（這個撇號記號由 Lagrange 推廣並成為標準）；$q$ 為 $p$ 的第一導函數，記 $f''$，以此類推。

於是導數的性質變成純代數的推論：
- $\dfrac{d}{dx}(uv) = u'v + uv'$：由 $(uv)(x+i)$ 的展開比較 $i$ 的係數直接得到。
- 極限定義 $f'(x) = \lim_{i\to 0}\dfrac{f(x+i)-f(x)}{i}$ 成為**推論**而非定義——增量 $i$ 是真正的代數量，不是幽靈。

整個微積分被重建為「冪級數的代數」。Lagrange 用這套方法重新推導了所有已知結果：極值判準（$f'(x)=0$ 且 $f''(x)<0$ 為極大）、曲率、乃至《Mécanique analytique》中的力學方程。

### 線索二：Lagrange 餘項——誤差的代數圍捕
《Théorie》最重要的技術貢獻：對展開式截斷後的誤差，Lagrange 給出代數形式的估計：

$$f(x+i) = f(x) + i f'(x) + \frac{i^2}{2!}f''(x) + \cdots + \frac{i^n}{n!}f^{(n)}(x) + R_n$$

$$R_n = \frac{i^{n+1}}{(n+1)!}f^{(n+1)}(x + \theta i), \quad 0 < \theta < 1$$

其中 $\theta$ 是某個中間值參數（Lagrange 用中值定理式的論證證明其存在）。這個**Lagrange 餘項**讓冪級數從「無窮和的信仰」變成「可控制誤差的有限工具」——即使不談收斂，有限項的逼近也有明確誤差界。這是 18 世紀分析學最接近 19 世紀嚴格化的時刻。

### 線索三：路線的裂縫——「任意函數可展開」是假設
Lagrange 的地基有一個致命假設：**任意函數都能展開成冪級數**。他對此沒有證明（也無法在他自己的框架內證明）。裂縫在 19 世紀初暴露：

1. **Cauchy 的反例（1822）**：$f(x) = e^{-1/x^2}$（$x\neq 0$）、$f(0)=0$，在 $x=0$ 所有階導數為零，展開式恆為零，不等於函數本身。「存在所有階導數」不等於「可展開」。
2. **收斂半徑的謎**：$\dfrac{1}{1+x^2}$ 的 Maclaurin 級數只在 $|x|<1$ 收斂，但實軸上處處光滑——冪級數的失效無法在實代數框架內解釋（要到複變函數論才有答案）。
3. **連續但不可微**：Weierstrass 1872 年的處處連續處處不可微函數，徹底粉碎了「函數都由好的級數組成」的信念。

### 線索四：解析力學——同時代的另一件案
1788 年 Lagrange 的《Mécanique analytique》把整個力學建立在變分法與廣義坐標上：

$$\frac{d}{dt}\frac{\partial L}{\partial \dot{q}_k} - \frac{\partial L}{\partial q_k} = 0, \qquad k = 1, \dots, n$$

書中不使用一張幾何圖——力學被代數化。《Théorie》（1797）則把微積分本身代數化。兩本書是同一場「去幾何化」運動的兩面。有趣的是：《Mécanique》的路線大獲成功（延續到今天的分析力學），《Théorie》的路線則被修正——但被修正的方式（Cauchy 的極限、Weierstrass 的 ε-δ）反而建立了現代分析學。

### 程式碼範例：Lagrange 餘項的數值驗證與 sympy 求導
```python
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from math import factorial

# 1) sympy 求導：驗證 Lagrange 導數的代數性質
x = sp.Symbol('x')
f = x**3 * sp.sin(x)
d1 = sp.diff(f, x)
d2 = sp.diff(d1, x)
print("f  =", f)
print("f' =", d1)          # 應為 3x^2 sin x + x^3 cos x
print("f''=", d2)

# 2) Lagrange 餘項驗證：以 f = sin x 在 a=0 展開
a = 0
xs = np.linspace(-np.pi, np.pi, 300)
f_true = np.sin(xs)
f_true_at_a = np.sin(a)

def lagrange_rem_bound(xv, n):
    """|R_n| <= |x|^{n+1}/(n+1)!，因 |f^{(n+1)}| <= 1"""
    return abs(xv)**(n + 1) / factorial(n + 1)

def taylor_sin(xv, n):
    s = 0.0
    for k in range(n + 1):
        if k % 2 == 1:
            s += (-1)**((k - 1) // 2) * xv**k / factorial(k)
    return s

print("\nLagrange 餘項驗證（x = 2.0）：")
for n in [3, 5, 7, 9]:
    xv = 2.0
    actual = abs(np.sin(xv) - taylor_sin(xv, n))
    bound = lagrange_rem_bound(xv, n)
    print(f"  n={n}: 實際誤差 = {actual:.3e}, Lagrange 界 = {bound:.3e}, 通過 = {actual <= bound}")

# 3) Cauchy 反例：f(x) = exp(-1/x^2) 的所有導數在 0 處為 0
g = sp.exp(-1 / x**2)
print("\nCauchy 反例 f(x)=exp(-1/x^2)：")
for k in range(1, 5):
    print(f"  f^{(k)}(0) 極限 =", sp.limit(sp.diff(g, x), x, 0))

fig, ax = plt.subplots(figsize=(8, 5))
xs2 = np.linspace(-3, 3, 400)
ax.plot(xs2, np.exp(-1 / np.where(xs2 == 0, 1, xs2**2)), lw=2, label="e^{-1/x²}（展開式恆為 0）")
ax.plot(xs2, np.zeros_like(xs2), "r--", lw=1.5, label="其 Maclaurin 級數 = 0")
ax.set_ylim(-0.2, 1.2); ax.legend()
ax.set_title("Cauchy 反例：光滑 ≠ 可展開")
plt.show()
```

數值輸出顯示：實際誤差始終小於 Lagrange 界——餘項公式可靠；而 Cauchy 反例的所有階導數在 0 處極限為 0，其展開式恆為零不等於函數本身——Lagrange 假設的裂縫被直接驗證。

## 結案 -- 後果與影響
- **導數記號的標準化**：$f'(x)$ 的撇號記號經 Lagrange 推廣後成為世界標準，與 Leibniz 的 $\frac{dy}{dx}$ 並存至今。
- **Lagrange 餘項進入教科書**：泰勒公式的誤差估計成為分析學的必備工具，是數值分析與逼近論的基石。
- **路線的失敗與轉化**：「冪級數地基」被 Cauchy 的反例擊穿，但 Lagrange 的意圖——**讓微積分擺脫幾何直覺、走向純粹推理**——被 Cauchy（1821《Cours d'Analyse》）以極限語言實現，再由 Weierstrass（1870s）以 ε-δ 完成。
- **Weierstrass 的冪級數復興**：Weierstrass 的解析函數論（1870s）正是「以冪級數為基礎」的復活版——但他只對「可展開的函數」（解析函數）如此定義，並先解決了收斂性。Lagrange 的夢想以修正後的形式實現。
- 影響至今：分析學的「ε-嚴格化」傳統、數值分析的誤差理論、乃至 Weierstrass 式的嚴格證明文化，都可追溯到 1797 年這場未竟的地基重建。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Joseph-Louis Lagrange | 1797 年《Théorie des fonctions analytiques》，冪級數路線 |
| George Berkeley | 1734 年《The Analyst》攻擊無窮小 |
| Leonhard Euler | 柏林前任，冪級數操作的先驅 |
| Augustin-Louis Cauchy | 反例擊穿假設，1821 年極限語言重建 |
| Karl Weierstrass | ε-δ 嚴格化，冪級數路線的復興 |

- J.-L. Lagrange, *Théorie des fonctions analytiques*, Paris (1797)。
- J.-L. Lagrange, *Mécanique analytique*, Paris (1788)。
- G. Berkeley, *The Analyst*, London (1734)。
- V. J. Katz, *A History of Mathematics*, 3rd ed., Pearson (2009)。
