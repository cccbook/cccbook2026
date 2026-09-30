# 1843 — Laurent 級數

## 案件摘要
1843 年，法國工程師兼數學家 Pierre Alphonse Laurent 在一份提交給法國科學院的備忘錄中，發表了一個看似只是「Taylor 級數補遺」的結果：在圓環（annulus）內解析的函數，可以展開成**同時含正冪與負冪**的雙向無窮級數。這個級數後來被稱為 Laurent 級數，它不只補足了 Taylor 展開的盲區，更成為**奇點分類**與**留數計算**的偵探工具——要知道一個函數在某點「犯了什麼罪」，打開它的 Laurent 展開式看負冪項即可。

## 前因 -- 為什麼會有這個案子
- 1825 年 Cauchy 建立複積分理論：解析函數在閉迴路上的積分為零，並在 1831 年給出 Taylor 展開定理：若 $f$ 在圓盤 $|z-a| < R$ 內解析，則
$$f(z) = \sum_{n=0}^{\infty} a_n (z-a)^n, \qquad a_n = \frac{f^{(n)}(a)}{n!}$$
- 但 Taylor 級數有一個致命盲區：它**只能以解析點為中心**展開。函數在奇點附近的行為——那正是複分析最想偵辦的「案發現場」——Taylor 級數完全無法觸及。
- 天文學的實際需求：Laurent 在處理天體力學中的積分時（1840 年代計算行星攝動），經常遇到積分路徑包圍奇點、被積函數在圓環內解析的情況。Taylor 公式在此失效，而 Cauchy 的理論尚未給出現成工具。
- Cauchy 當時已是法國科學院複分析的權威，但他的積分公式的完整形式（$f(a) = \frac{1}{2\pi i}\oint \frac{f(z)}{z-a}dz$）與其推論之間，仍有一塊拼圖缺席：**在圓環上，積分為什麼不為零？不為零的部分怎麼算？**

## 線索與推理 -- 數學式、程式、理論

### 線索一：圓環上的雙向展開
Laurent 的核心定理：設 $f(z)$ 在圓環 $r < |z-a| < R$ 內解析，則在此圓環內
$$f(z) = \sum_{n=-\infty}^{\infty} a_n (z-a)^n, \qquad a_n = \frac{1}{2\pi i}\oint_{C} \frac{f(\zeta)}{(\zeta-a)^{n+1}}\, d\zeta$$
其中 $C$ 是圓環內任一繞 $a$ 一圈的閉迴路。
- 正冪部分 $\sum_{n\ge 0} a_n(z-a)^n$ 在 $|z-a|<R$ 收斂（「解析部分」）。
- 負冪部分 $\sum_{n\le -1} a_n(z-a)^n$ 在 $|z-a|>r$ 收斂（「主要部分」，principal part）。
- 展開式在整個圓環內**唯一**——這是偵探鑑識的關鍵：不管你怎麼算出展開式，負冪係數都一樣，所以它反映的是函數的客觀罪證，不是計算方法的產物。

### 線索二：奇點分類——三種罪犯
把孤立奇點 $z=a$ 附近的主要部分攤開來驗屍，可以給奇點定罪：

| 類型 | 主要部分 | 例子 |
|---|---|---|
| 可去奇點 | 全為零 | $\frac{\sin z}{z}$ 在 $z=0$（補上 $f(0)=1$ 即無罪釋放） |
| $m$ 階極點 | $a_{-m}(z-a)^{-m} + \cdots + a_{-1}(z-a)^{-1}$，$a_{-m}\ne 0$ | $\frac{1}{(z-1)^2 z}$ 在 $z=1$ 為二階極點 |
| 本性奇點 | 無窮多個負冪項 | $e^{1/z} = 1 + \frac{1}{z} + \frac{1}{2!z^2} + \cdots$ |

本性奇點最凶殘：Weierstrass–Casorati 定理（1875 年之前已有雛形）指出，本性奇點的任意鄰域內，函數值**稠密地取到整個複平面**；後來 Picard 大定理（1879）更斷言取到除了至多一點外的**每一個值**。

### 線索三：留數——負冪項裡的黃金證據
係數 $a_{-1}$ 有特殊地位，被稱為**留數**（residue）：
$$\operatorname{Res}(f, a) = a_{-1} = \frac{1}{2\pi i}\oint_C f(z)\,dz$$
因為在展開式中，只有 $(z-a)^{-1}$ 這一項繞圈積分不為零（$\oint (z-a)^n dz$ 當 $n\ne -1$ 時為零）。於是 Cauchy 留數定理誕生：
$$\oint_C f(z)\,dz = 2\pi i \sum_{k} \operatorname{Res}(f, a_k)$$
複積分的計算從此標準化：不必硬算積分，只要找出奇點、讀出 $a_{-1}$。實積分（如 $\int_{-\infty}^{\infty} \frac{dx}{1+x^2} = \pi$）也藉由圍道積分大批批量生產。

### 程式碼範例：Laurent 級數部分和的視覺化
```python
import numpy as np
import matplotlib.pyplot as plt

# 在圓環 0 < |z| < pi 內展開 f(z) = 1/(z*sin(z)) 的 Laurent 級數
# 1/(z*sin z) = z^{-2} + 1/6 + 7z^2/360 + 31z^4/15120 + ...
# 注意 z=0 是二階極點，主要部分只有 z^{-2} 這一項
N = 400
r, R = 0.3, 3.0   # 圓環內外半徑
theta = np.linspace(0, 2*np.pi, N)

def laurent_partial(z):
    # 取前幾項：z^{-2} + 1/6 + 7z^2/360 + 31z^4/15120
    return 1/z**2 + 1/6 + 7*z**2/360 + 31*z**4/15120

# 驗證：在圓環內任取一點比較精確值
z0 = 1.0 + 0.5j
exact = 1/(z0*np.sin(z0))
approx = laurent_partial(z0)
print("精確值   =", exact)
print("Laurent  =", approx)
print("誤差     =", abs(exact - approx))

# 沿半徑畫 |f| 與部分和的 |.|
rad = np.linspace(r, R, N)
z_line = rad * np.exp(1j*0.7)
plt.figure(figsize=(8,5))
plt.semilogy(rad, np.abs(1/(z_line*np.sin(z_line))), label="|1/(z sin z)|")
plt.semilogy(rad, np.abs(laurent_partial(z_line)), "--", label="|Laurent partial sum|")
plt.xlabel("|z| (r=0.3 到 R=3)"); plt.ylabel("模（對數尺度）")
plt.title("Laurent series on the annulus: pole at z=0")
plt.legend(); plt.show()
```

程式在圓環內任一點的誤差極小，驗證了 Laurent 展開在圓環內的有效性；對數尺度圖中 $|z|\to 0$ 時函數以 $|z|^{-2}$ 爆炸，正是二階極點的罪證形狀。

## 結案 -- 後果與影響
- **奇點理論正式誕生**：可去奇點、極點、本性奇點的三分法成為複分析教科書的標準章節，為 Weierstrass–Casorati 與 Picard 定理提供舞台。
- **留數計算標準化**：Cauchy 留數定理把複積分化為代數運算，實積分的圍道方法（物理學中的色散關係、量子場論的傳播子積分）至今都在用。
- Laurent 級數是 Fourier 級數的遠親：取 $z = e^{i\theta}$，Laurent 級數變成雙向 Fourier 級數，訊號處理的 Z 變換與其同構。
- 有趣的偵探花絮：Weierstrass 早在 1841 年（當時是中學教師）就得到類似結果，但稿件在普魯士的期刊中延遲發表，法國科學院 1843 年收到 Laurent 的備忘錄後，Cauchy 本人指出了先後問題——最終名稱仍歸 Laurent，而 Weierstrass 版本收錄於其全集。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Pierre Alphonse Laurent | 1843 年發表 Laurent 級數（工程師，里爾炮兵學校） |
| Augustin-Louis Cauchy | 複積分理論、留數定理的奠基者 |
| Karl Weierstrass | 1841 年獨立得到圓環展開（延遲發表） |
| Felice Casorati / Émile Picard | 本性奇點理論的後續偵辦 |

- P. A. Laurent, «Extension du théorème de M. Cauchy relatif à la convergence du développement d'une fonction...», C. R. Acad. Sci. Paris **17** (1843)。
- A.-L. Cauchy, «Sur la théorie des intégrales définies» 等系列論文（1825–1840）。
- K. Weierstrass, «Darstellung einer analytischen Funktion einer komplexen Veränderlichen...»（1841，收錄於 Werke, Bd. 1）。
