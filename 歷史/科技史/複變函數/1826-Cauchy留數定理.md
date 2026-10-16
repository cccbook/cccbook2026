# 1826 — Cauchy 留數定理

## 案件摘要
1826 年，Cauchy 在《Exercices de mathématiques》系列中發表留數（résidu）理論：函數在孤立奇點 $a$ 處的「留數」$\operatorname{Res}_{z=a} f = \frac{1}{2\pi i}\oint f\,dz$，把圍道積分化為奇點處留數的加總。配合 Cauchy 積分公式 $\oint_\gamma \frac{f(z)}{z-a}dz = 2\pi i\, f(a)$，複積分從此變成一台計算機器：繞一圈，只需讀出奇點的「案底」。這是十九世紀分析學最有生產力的發明之一——積分計算、級數展開、實積分求值，全都由它驅動。

## 前因 -- 為什麼會有這個案子
- 1814/1825 年 Cauchy 積分定理已結案：解析函數的閉曲線積分為零，但 $1/z$ 繞原點一圈得 $2\pi i$——積分值完全由「奇點」決定。
- 奇點是路徑積分的唯一嫌疑人：同樣的區域，函數沒有奇點則積分為零，有奇點則不為零。**那奇點到底留下了什麼痕跡？**
- Euler 早已用部分分式展開計算積分，Laurent 1843 年將發表奇點處的雙邊級數（實際上 Cauchy 1840 年代也獨立擁有），但 1826 年當時還沒有系統性的「奇點分類學」。
- 實積分的計算困境：$\int_{-\infty}^{\infty} \frac{dx}{1+x^2}$ 這類積分，用實變方法需要巧妙的代換（$x = \tan\theta$）；更複雜的 $\int_0^{2\pi}\frac{d\theta}{a+b\cos\theta}$ 則幾乎無計可施——這是案發現場。

核心疑問：**奇點對圍道積分的貢獻能否被「量化」？**

## 線索與推理 -- 數學式、程式、理論

### 線索一：Cauchy 積分公式——奇點的第一次筆錄
由積分定理直接推論：$f$ 在 $\gamma$ 內及其上解析，$a$ 為 $\gamma$ 內一點，則

$$f(a) = \frac{1}{2\pi i}\oint_\gamma \frac{f(z)}{z-a}\,dz, \qquad f^{(n)}(a) = \frac{n!}{2\pi i}\oint_\gamma \frac{f(z)}{(z-a)^{n+1}}\,dz$$

這條公式驚人的地方：**函數在內點的值，由邊界上的積分完全決定**。證明手法：在 $a$ 附近縮小圓周，$\frac{f(z)}{z-a}$ 在挖去 $a$ 的區域解析，積分定理說大圓與小圓積分相等；小圓上 $f(z)\approx f(a)$，剩下 $\oint \frac{dz}{z-a} = 2\pi i$。一個「解析性 + 奇點」的完美合謀。

### 線索二：留數的定義——奇點的量化案底
Cauchy 1826 年定義：$f$ 在孤立奇點 $a$ 附近（去心圓盤）解析，則積分

$$\operatorname{Res}_{z=a} f \;=\; \frac{1}{2\pi i}\oint_{|z-a|=\varepsilon} f(z)\,dz$$

是一個良定義的常數（不依賴 $\varepsilon$，因為積分定理）。它就是函數在奇點處 $1/z$ 型行為的係數——$f$ 在 $a$ 附近展開時 $\frac{c_{-1}}{z-a}$ 項的係數 $c_{-1}$。**留數定理**：若 $f$ 在 $\gamma$ 內除有限個奇點 $a_1,\dots,a_n$ 外解析，則

$$\oint_\gamma f(z)\,dz = 2\pi i \sum_{k=1}^{n} \operatorname{Res}_{z=a_k} f$$

證明：在每個奇點周圍畫小圓，用積分定理證明大圍道積分等於各小圓積分之和。積分定理說「無奇點則為零」，留數定理說「有奇點則讀案底」——兩者合璧，圍道積分完全結案。

### 線索三：單極點與高階極點的計算
實務上最常用的公式——單極點（simple pole）：

$$\operatorname{Res}_{z=a} f = \lim_{z\to a}(z-a)f(z)$$

例如 $f(z) = \frac{1}{z^2+1} = \frac{1}{(z-i)(z+i)}$ 在 $z=i$ 的留數：

$$\operatorname{Res}_{z=i} f = \lim_{z\to i}\frac{1}{z+i} = \frac{1}{2i}$$

$m$ 階極點：

$$\operatorname{Res}_{z=a} f = \frac{1}{(m-1)!}\lim_{z\to a}\frac{d^{m-1}}{dz^{m-1}}\left[(z-a)^m f(z)\right]$$

單極點的幾何意義也在此現形：$\frac{f(z)}{z-a}$ 恰好是 Cauchy 積分公式的被積式，所以 $\oint_\gamma \frac{f(z)}{z-a}dz = 2\pi i f(a)$——積分公式不過是留數定理的特例。

### 線索四：圍道積分算實積分——機器開動
用留數定理計算實積分 $\displaystyle\int_{-\infty}^{\infty}\frac{dx}{1+x^2}$：取上半平面大半圓圍道 $C_R$（半徑 $R$、沿實軸 $-R\to R$ 再沿半圓回到 $-R$）。被積函數在上半平面僅 $z=i$ 一個奇點，留數 $\frac{1}{2i}$。半圓弧上的積分隨 $R\to\infty$ 消失（Jordan 引理，被積式 $\sim 1/R^2$、弧長 $\sim R$）。於是：

$$\oint_{C_R}\frac{dz}{1+z^2} = \int_{-R}^{R}\frac{dx}{1+x^2} + \int_{\text{弧}} \;\xrightarrow{R\to\infty}\; \int_{-\infty}^{\infty}\frac{dx}{1+x^2} = 2\pi i\cdot\frac{1}{2i} = \pi$$

與已知結果 $\arctan(\infty) - \arctan(-\infty) = \pi$ 完全吻合。這台機器同樣能算 $\int_0^{2\pi}\frac{d\theta}{a+b\cos\theta}$（令 $z = e^{i\theta}$ 化為單位圓圍道）、三角級數和、甚至 $\sum_{n=1}^{\infty}\frac{1}{n^2}$（用 $\pi\cot\pi z$ 的留數）。

### 程式碼範例：Cauchy 積分公式與留數法的數值對照
```python
import numpy as np

def contour_integral(func, center, R, N=4000):
    """沿圓心 center、半徑 R 的圓數值計算圍道積分"""
    t = np.linspace(0, 2*np.pi, N, endpoint=False)
    z = center + R*np.exp(1j*t)
    dz = 1j*R*np.exp(1j*t) * (2*np.pi/N)
    return np.sum(func(z)*dz)

# 案件一：Cauchy 積分公式 ∮ f(z)/(z-a) dz = 2πi f(a)
f = lambda z: np.exp(z) + z**3
a = 0.3 + 0.4j
I = contour_integral(lambda z: f(z)/(z-a), 0, 2)
print("積分公式數值:", I/(2*np.pi*1j), " f(a) =", f(a))

# 案件二：留數定理 ∮ dz/(1+z^2)，圓心 0.5j、半徑 0.8 含奇點 i（避開極點 ±i）
I2 = contour_integral(lambda z: 1/(1+z**2), 0.5j, 0.8)
print("∮dz/(1+z^2):", I2, " 理論 2πi·(1/2i) =", np.pi)

# 案件三：留數法算實積分 ∫_{-∞}^{∞} dx/(1+x^2) = π（大半圓逼近）
for R in [10, 100, 1000]:
    t = np.linspace(0, np.pi, 20000)   # 上半平面半圓
    z = R*np.exp(1j*t)
    arc = np.sum((1j*R*np.exp(1j*t))/(1+z**2) * (np.pi/20000))
    real_part = np.trapz(1/(1+np.linspace(-R, R, 20000)**2),
                         np.linspace(-R, R, 20000))
    print(f"R={R}: 實軸+半圓 = {real_part + arc:.6f}  (π = {np.pi:.6f})")

# 案件四：單極點留數公式驗證  Res_{z=i} 1/(z^2+1) = 1/(2i)
print("極限公式:", (1/(2*1j)), " 積分定義:", contour_integral(
    lambda z: 1/(1+z**2), 1j, 0.5) / (2*np.pi*1j))
```

數值輸出顯示：積分公式還原 $f(a)$、單位圓積分為 $2\pi i\cdot\frac{1}{2i} = \pi i$、大半圓圍道逼近實積分收斂到 $\pi$——留數機器的每一個齒輪都被驗證。

## 結案 -- 後果與影響
- **計算積分的強大機器**：實變方法無能為力的積分（廣義積分、三角積分、級數和）從此有了系統性算法，物理學與工程學受用至今。
- Laurent 級數（Laurent 1843，Cauchy 1840 年代獨立擁有）：奇點處的雙邊冪級數 $f(z)=\sum_{n=-\infty}^{\infty}c_n(z-a)^n$，使奇點分類學（可去奇點、極點、本性奇點）正式誕生，留數即 $c_{-1}$。
- Cauchy 積分公式成為解析函數論的核心恆等式：邊界決定內部、解析函數无穷可微、Taylor 展開、最大模原理皆由它推出。
- 後續鏈條：Riemann 1851 年的幾何函數論、Weierstrass 的冪級數學派、1885 年 Runge 的多項式逼近、 twentieth 世紀的 Wiener–Hopf 方法與譜理論，皆以此案為基石。
- 影響至今：量子場論的 Feynman 積分、訊號處理的 Laplace/Z 變換反演、電磁散射的圍道方法，本質上都是「讀奇點案底」。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Augustin-Louis Cauchy | 1826 年提出留數與留數定理，1840 年代擁有 Laurent 展開 |
| Pierre Alphonse Laurent | 1843 年發表奇點處雙邊級數（Laurent 級數） |
| Bernhard Riemann | 1851 年幾何函數論，承接積分公式 |
| Karl Weierstrass | 冪級數學派，與 Cauchy 路線互補 |

- A.-L. Cauchy, *Exercices de mathématiques*, vol. 1–2, Paris (1826–1827)：留數理論的首次發表。
- A.-L. Cauchy, 〈Sur la théorie des résidus〉等系列論文 (1826–1829)。
- P. A. Laurent, 〈Extension du théorème de M. Cauchy...〉, C. R. Acad. Sci. Paris **17** (1843)。
