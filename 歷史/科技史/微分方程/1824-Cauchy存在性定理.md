# 1824 Cauchy 存在性定理

## 案發現場

十八世紀以來，數學家解微分方程的方式是「先猜後驗」：猜一個級數、猜一個積分式，然後形式地驗證它滿足方程。但有一個根本問題從來沒人認真追問過：**你怎麼知道解真的存在？你怎麼知道解只有一個？**

這不是吹毛求疵。有些方程看似無害，解卻不存在或不唯一。例如

$$
y' = y^{2/3}, \qquad y(0) = 0.
$$

它可以驗出「解家族」：$y = \left(\dfrac{x - C}{3}\right)^3$ 對任意 $C \ge 0$（在 $x < C$ 時恆為 $0$）都滿足方程與初始條件。更糟的是 $y' = \mathrm{sgn}(x)$ 型的方程，連解都可能不存在。如果連「解存不存在」都不確定，那麼求出來的「解」到底是什麼？

接案的勇士是 Augustin-Louis Cauchy（1789–1857）。在 1820 年代推動「分析嚴格化」的浪潮中——他重新定義了極限、連續、積分——Cauchy 把手伸向了微分方程這塊最後的處女地。1824 年，他在巴黎綜合理工學院的講義中首次給出了 ODE 初值問題解的**存在性與唯一性的嚴格證明**。

## 偵查過程

### 第一步：把問題寫清楚

Cauchy 考慮的初值問題是：

$$
y' = f(x, y), \qquad y(x_0) = y_0.
$$

他假設 $f(x,y)$ 及其偏導數 $\partial f/\partial y$ 在矩形區域

$$
R = \{(x,y) : |x - x_0| \le a,\ |y - y_0| \le b\}
$$

上連續且有界。設 $M = \max_R |f|$。目標：證明在 $|x - x_0| \le \min(a, b/M)$ 的範圍內，存在唯一的解 $y(x)$。

### 第二步：化為積分方程

Cauchy 的第一個關鍵觀察：初值問題等價於積分方程。對 $y' = f(x,y)$ 兩邊從 $x_0$ 積到 $x$，並用 $y(x_0) = y_0$：

$$
y(x) = y_0 + \int_{x_0}^{x} f(t, y(t))\,dt.
$$

這一步的妙處：積分方程的右邊把 $y$ 「藏」在積分號裡面，而積分是「抹平」操作——它不放大誤差。這為估計創造了舞台。

### 第三步：優級數法（比較級數法）

Cauchy 的原創證明用的是**優級數法**（méthode des majorants）：構造一個「更大的級數」，證明原級數被它壓住，從而證明原級數收斂。

假設解可以展開為 Taylor 級數

$$
y(x) = \sum_{n=0}^{\infty} \frac{y^{(n)}(x_0)}{n!}(x - x_0)^n.
$$

各階導數可由方程逐次微分得到：$y^{(n+1)}(x_0) = \dfrac{d^n}{dx^n}f(x, y(x))\big|_{x=x_0}$。由 $f$ 與 $\partial f/\partial y$ 的有界性，Cauchy 用歸納法證明存在常數 $C, K$ 使得

$$
|y^{(n)}(x_0)| \le C\,K^{n-1}(n-1)!.
$$

於是解被「優函數」壓住：

$$
|y(x)| \le |y_0| + \sum_{n\ge 1} \frac{C K^{n-1}(n-1)!}{n!}|x-x_0|^n
= |y_0| + \frac{C}{K}\sum_{n\ge 1}\frac{(K|x-x_0|)^n}{n}.
$$

後面的級數在 $K|x - x_0| < 1$ 時絕對收斂（這正是 $\sum z^n/n$，即 $-\ln(1-z)$）。級數被壓住了，收斂性得證，因此解存在。

### 第四步：唯一性——壓縮的思想

唯一性的論證蘊含了日後「壓縮映射」的思想。設 $y_1, y_2$ 是兩個解，令 $e(x) = y_1(x) - y_2(x)$，則

$$
e(x) = \int_{x_0}^{x}\big[f(t, y_1(t)) - f(t, y_2(t))\big]dt.
$$

由微分中值定理與 $L = \max|\partial f/\partial y|$：

$$
|f(t, y_1) - f(t, y_2)| \le L\,|y_1(t) - y_2(t)| = L\,|e(t)|.
$$

代入積分方程，取絕對值：

$$
|e(x)| \le L\left|\int_{x_0}^{x}|e(t)|\,dt\right|.
$$

令 $\Phi(x) = \displaystyle\int_{x_0}^{x}|e(t)|dt$，則 $\Phi'(x) \le L\Phi(x)$ 且 $\Phi(x_0)=0$。乘上衰減因子 $e^{-L(x-x_0)}$：

$$
\frac{d}{dx}\big[\Phi(x)e^{-L(x-x_0)}\big] = e^{-L(x-x_0)}\big[\Phi'(x) - L\Phi(x)\big] \le 0,
$$

故 $\Phi(x)e^{-L(x-x_0)} \le 0$，但 $\Phi \ge 0$，所以 $\Phi \equiv 0$，即 $e \equiv 0$，$y_1 = y_2$。唯一性得證。

### 第五步：反例偵訊——為什麼要假設 Lipschitz

為什麼必須假設 $\partial f/\partial y$ 有界？看看嫌疑人 $y' = y^{2/3}$：

$$
y' = y^{2/3}, \quad y(0) = 0.
$$

$f$ 連續，但 $\dfrac{\partial f}{\partial y} = \dfrac{2}{3}y^{-1/3}$ 在 $y = 0$ 附近**無界**。檢查「解家族」：

$$
y(x) = \begin{cases} 0, & x \le C, \\[2pt] \left(\dfrac{x-C}{3}\right)^3, & x > C, \end{cases} \qquad C \ge 0
$$

對每個 $C$ 都驗證成立：當 $x \le C$ 時 $y = 0$，$y' = 0 = y^{2/3}$；當 $x > C$ 時 $y' = 3\cdot\frac{(x-C)^2}{27} = \left(\frac{x-C}{3}\right)^{2} = y^{2/3}$；在黏合點 $x = C$ 處左右導數皆為 $0$，光滑接合。**無窮多個解**——假設一破，唯一性即亡。這個反例告訴我們：Cauchy 定理的每個假設都不是裝飾品。

## 結案報告

Cauchy 證明了：在 $f$ 連續且 $\partial f/\partial y$ 有界（今稱 Lipschitz 條件）的區域內，初值問題存在唯一的局部解。「解是否存在」從哲學爭論變成了定理。

遺產：

1. **存在性理論成為一門學問**：Picard 在 1890 年代把 Cauchy 的思想改造成**逐次逼近法**（Picard iteration）：
   $$
   y_{n+1}(x) = y_0 + \int_{x_0}^{x} f(t, y_n(t))\,dt,
   $$
   證明 $y_n$ 一致收斂到解——這是壓縮映射原理與現代泛函分析不動點理論的直接前身。
2. **Peano 定理**：只需 $f$ 連續（不必 Lipschitz）就能保證解存在（但不唯一，正如 $y' = y^{2/3}$ 的反例所示）。
3. **嚴格化浪潮**：Cauchy 的極限、連續、積分定義加上這個定理，把分析學整個搬上了嚴格化的軌道，通往 Weierstrass 與二十世紀的實變函數論。
4. **數值分析的基礎**：解存在唯一，數值方法（如 Euler 法、Runge-Kutta 法）才有收斂的對象（參見 [1841-Liouville可積性之謎.md](1841-Liouville可積性之謎.md)）。

## 證據與工具

```python
# Picard 逐次逼近：數值驗證 Cauchy 存在性定理
import numpy as np
from scipy.integrate import solve_ivp

# 問題：y' = y, y(0) = 1，精確解 y = e^x
def picard_iteration(N=6, n_points=100):
    """y_{n+1}(x) = 1 + ∫_0^x y_n(t) dt，觀察收斂到 e^x"""
    x = np.linspace(0, 1, n_points)
    y = np.ones_like(x)          # y_0(x) = 1（初始猜測）
    for n in range(N):
        y_new = 1 + np.array([np.trapz(y[:i+1], x[:i+1]) if i > 0 else 0 for i in range(len(x))])
        err = np.max(np.abs(y_new - np.exp(x)))
        print(f"第 {n+1} 次逼近，最大誤差 = {err:.6f}")
        y = y_new
    return x, y

x, y = picard_iteration()
print("驗證：逼近值 vs e^x =", y[-1], np.exp(1))

# 反例偵訊：y' = y^{2/3}, y(0)=0 有無窮多解
def counter_example(C, x):
    """分段解：x<=C 恆為 0，之後 ((x-C)/3)^3"""
    return np.where(x <= C, 0.0, ((x - C)/3)**3)

x2 = np.linspace(-1, 2, 500)
for C in [0, 0.5, 1.0]:
    y2 = counter_example(C, x2)
    # 數值檢驗 y' == y^{2/3}（在解的定義域內）
    dy = np.gradient(y2, x2)
    ok = np.allclose(dy[10:], np.maximum(y2[10:], 0)**(2/3), atol=1e-2)
    print(f"C={C}: 解滿足方程？{ok}")

# 唯一性破壞視覺化：三條解曲線都過 (0,0)
import matplotlib.pyplot as plt
plt.figure(figsize=(6, 4))
for C in [0, 0.5, 1.0]:
    plt.plot(x2, counter_example(C, x2), label=f"C={C}")
plt.scatter([0], [0], color='red', zorder=5, label="同一初始點")
plt.legend(); plt.title("y' = y^{2/3}：無窮多解（Lipschitz 條件失效）")
plt.savefig("cauchy_counter.png", dpi=100)
print("已存圖 cauchy_counter.png")
```
