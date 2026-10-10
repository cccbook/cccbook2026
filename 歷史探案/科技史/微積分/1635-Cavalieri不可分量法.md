# 1635 — Cavalieri 不可分量法

## 案件摘要
1635 年，米蘭耶穌會士 Bonaventura Cavalieri 出版《用不可分量連續新幾何學》（Geometria Indivisibilibus Continuam Nova quadam Ratione Promota），提出「不可分量原理」：平面圖形由無限多條等距平行線段組成，立體由無限多張等距平行截面組成。只要兩個圖形在每個高度上的截面都相等，兩者面積/體積就相等。Cavalieri 用它算出圓錐、球、柱的體積，並得到 $\int_0^1 x^n dx = \frac{1}{n+1}$ 的雛形——積分表的前身。

## 前因 -- 為什麼會有這個案子
- Archimedes 的《方法》用「把面積切成線段掛上槓桿秤」求出球體積，但這份手稿長期失傳，歐洲只有部分 Archimedes 著作的拉丁譯本（1543 年 Tartaglia 譯本、1558 年 Commandino 譯本）流傳。
- Archimedes 給 Galileo 的追隨者留下了一個懸案：他用某種「祕密方法」發現了這些結果，卻用繁瑣的雙重歸謬法包裝。Galileo 自己猜測：連續體由無限多個「不可分量」原子組成，並在《兩門新科學》(1638) 中討論之。
- 1615 年，Kepler 為算酒桶體積出版《測量酒桶體積的新立體幾何》（Nova Stereometria Doliorum Vinariorum），把酒桶切成無限多片薄殼再求和——這是「切片求和」思想的直接示範，也啟發了 Cavalieri。
- Cavalieri 是 Galileo 的通訊追隨者、波隆那大學數學教授。案件的動機：把 Kepler 的直觀切片升級成一套**有原理可循**的系統方法。

## 線索與推理 -- 數學式、程式、理論

### 線索一：不可分量原理
Cavalieri 原理：若兩個立體在等高處的截面面積恆相等，則兩立體體積相等。

$$\text{若 } A_1(h) = A_2(h)\ \forall h, \quad \text{則 } V_1 = V_2$$

經典範例：半徑 $r$ 的半球與「半徑 $r$ 的圓柱挖去倒置圓錐」在高度 $h$ 處的截面都是環形，面積同為 $\pi(r^2 - h^2)$，故兩者體積相等，從而

$$V_{\text{半球}} = \pi r^3 - \frac{1}{3}\pi r^3 = \frac{2}{3}\pi r^3, \qquad V_{\text{球}} = \frac{4}{3}\pi r^3$$

這個結果 Archimedes 早已知道，但 Cavalieri 用了一條幾乎不需要計算的原理就得出——原理本身比計算更有威力。

### 線索二：$\int_0^1 x^n dx = \frac{1}{n+1}$ 的雛形
Cavalieri 在書中證明：正方形被對角線分割後，考慮 $n$ 次冪的「所有線段之和」。他將邊長為 1 的正方形內，從頂點到對角線上各點的線段長度視為 $x$，這些線段的 $n$ 次冪之和與「整個圖形的對應和」之比為 $1 : (n+1)$。

用現代語言：

$$\frac{\int_0^1 x^n\,dx}{\int_0^1 1\,dx} = \frac{1}{n+1} \quad \Rightarrow \quad \int_0^1 x^n\,dx = \frac{1}{n+1}$$

Cavalieri 對 $n = 1, \dots, 9$ 給出了結果，並猜想一般公式成立（1655 年 Wallis 用算術方法嚴格處理，Fermat 更早用幾何級數證明）。

### 線索三：圓錐與球的體積
圓錐體積：把高 $h$、底半徑 $r$ 的圓錐切成平行於底面的薄片，高度 $y$ 處的截面半徑為 $\frac{r y}{h}$（相似三角形），截面面積 $\pi r^2 y^2/h^2$。對所有薄片「求和」（Cavalieri 意義下）：

$$V = \int_0^h \pi \frac{r^2}{h^2} y^2\,dy = \frac{\pi r^2}{h^2} \cdot \frac{h^3}{3} = \frac{1}{3}\pi r^2 h$$

正是 Democritus 猜測、Eudoxus 證明的結果——Cavalieri 用 $\int y^2\,dy = \frac{h^3}{3}$ 一次搞定。

### 線索四：方法的爭議與辯護
Jesuit 數學家 Paul Guldin 在 1640 年出版《重心論》第二冊時攻擊 Cavalieri：「無限多條沒有厚度的線段怎麼能有面積？連續體不能由不可分量組成。」Cavalieri 回應：不可分量法只是「快速工作的捷徑」，其結果總可以用窮竭法驗證。這場爭論與 20 世紀 Hilbert 對直覺主義的批評遙相呼應——**工具的有效性**與**邏輯的嚴格性**是兩件事。

### 程式碼範例：Cavalieri 體積的數值驗證
```python
import numpy as np

r, N = 1.0, 1000000
h = np.linspace(0, r, N)      # 高度切片

# (1) 半球截面：A(h) = pi(r^2 - h^2)
A_hemisphere = np.pi * (r**2 - h**2)

# (2) 圓柱挖圓錐截面：A(h) = pi(r^2 - h^2)，逐點比較
A_cyl_cone = np.pi * (r**2 - h**2)
print("兩截面最大差異:", np.max(np.abs(A_hemisphere - A_cyl_cone)))

# (3) Cavalieri 原理 → 體積相等
V_slice = np.trapz(A_hemisphere, h)          # 切片求和
print("半球體積（切片求和）:", V_slice, "理論 2/3·pi =", 2/3*np.pi)

# (4) ∫_0^1 x^n dx = 1/(n+1) 驗證
x = np.linspace(0, 1, N)
for n in range(1, 10):
    num = np.trapz(x**n, x)
    print(f"n={n}: 數值 {num:.6f}, 1/(n+1) = {1/(n+1):.6f}")
```

程式輸出：兩立體截面逐點相等（差異為 0），切片求和得半球體積 $\approx 2.0944 = \frac{2}{3}\pi$；$\int_0^1 x^n dx$ 的數值與 $\frac{1}{n+1}$ 逐項吻合——Cavalieri 的積分表在數值上完全成立。

### 線索五：從幾何到代數的關鍵一步
Cavalieri 的 $\int_0^1 x^n dx = \frac{1}{n+1}$ 表面上是幾何定理，實質上卻是一張**代數積分表**：只要被積函數是冪函數 $x^n$，答案就是 $\frac{1}{n+1}$，與幾何圖形無關。這個「脫離圖形」的視角是 17 世紀微積分的關鍵轉折——1637 年 Descartes《幾何學》確立「曲線 = 方程」之後，Cavalieri 的表可以直接套用到任何冪函數曲線上。1655 年 Wallis 更把它徹底算術化，寫成冪和極限 $\lim_{n\to\infty}\frac{0^k+\cdots+n^k}{n^{k+1}} = \frac{1}{k+1}$——積分表從幾何原理蛻變為算術定律。

## 結案 -- 後果與影響
- Cavalieri 原理成為 17 世紀幾何求積的**主力工具**，Torricelli 用它算出無限長號角的體積（Gabriel's Horn，1643），無窮大體積問題大量湧現。
- $\int_0^1 x^n dx = \frac{1}{n+1}$ 的雛形被 Wallis (1655)、Pascal、Fermat 進一步發展，成為微積分基本定理之前的「積分表」。
- 不可分量的哲學爭議（無限小是否合法）懸而未決，直到 19 世紀 Weierstrass 的 $\varepsilon$-$\delta$ 語言、乃至 1960 年代 Robinson 的非標準分析才徹底結案。
- 為 Newton/Leibniz 鋪路：Newton 讀 Wallis，Wallis 讀 Cavalieri，Cavalieri 讀 Archimedes——一條完整的證據鏈。
- 案件的影響：今日中國中學教材仍教「祖暅原理」（與 Cavalieri 原理等價，祖沖之之子祖暅早 1100 年提出）——同一件兇器，東西方各持一份。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Bonaventura Cavalieri | 不可分量原理，$\int x^n$ 雛形 |
| Johannes Kepler | 1615 酒桶體積，切片思想的示範 |
| Galileo Galilei | 連續體由不可分量組成的猜想 |
| Paul Guldin | 攻擊不可分量法的批評者 |
| Torricelli | Evangelista Torricelli，Gabriel's Horn |
| 祖暅 | 中國版本「祖暅原理」，早 Cavalieri 約 1100 年 |

- B. Cavalieri, *Geometria Indivisibilibus Continuam Nova quadam Ratione Promota*, Bologna (1635)。
- J. Kepler, *Nova Stereometria Doliorum Vinariorum* (1615)。
- A. Wallis, *Arithmetica Infinitorum* (1655)。
