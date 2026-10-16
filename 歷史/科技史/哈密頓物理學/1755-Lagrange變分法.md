# 1755 - Lagrange 變分法——19 歲少年的一般方法

## 案件摘要
1755 年 8 月，都靈的 19 歲炮兵學校講師 Lagrange 寫信給 Euler，
宣布他發明了「變分法的一般方法」：把求極值曲線的問題，化為一個**微分方程**。
$$\frac{\partial L}{\partial q} - \frac{d}{dt}\frac{\partial L}{\partial \dot q} = 0$$
Euler 回信讚嘆並立即採用，還刻意延後自己同主題論文的發表，讓少年先發。
這條今日稱為 **Euler–Lagrange 方程**的式子，是拉格朗日力學（乃至現代物理場論）的發動機。

## 前因
- **Euler 的變分法（1736/1744）**：用「有限差分逼近 + 極限」的幾何式手法，繁瑣且難以推廣。
- **最速降線與等時曲線**：一連串極值問題暴露了「逐案處理」的痛苦。
- **Maupertuis 最小作用量（1744）**：宣告自然路徑使作用量穩定，但缺少一般性數學工具。
- **Lagrange 的直覺**：與其「抖動整條曲線」，不如把曲線寫成座標的函數，直接對**座標本身**做微積分。

## 線索與推理

### Lagrange 的核心手法：「變分」的代數化
考慮積分
$$J[y] = \int_a^b L(y, y', x)\,dx$$
Lagrange 引入「變分」記號 $\delta$：讓 $y \to y + \epsilon\,\eta$（端點固定 $\eta(a)=\eta(b)=0$），要求 $\delta J = 0$：
$$\delta J = \epsilon \int_a^b \left( \frac{\partial L}{\partial y}\eta + \frac{\partial L}{\partial y'}\eta' \right) dx = 0$$
對第二項**分部積分**（這是神來一筆）：
$$\int \frac{\partial L}{\partial y'}\eta'\,dx = \underbrace{\left[\frac{\partial L}{\partial y'}\eta\right]_a^b}_{=0\ \text{(端點固定)}} - \int \frac{d}{dx}\frac{\partial L}{\partial y'}\,\eta\,dx$$
合併：
$$\int_a^b \left( \frac{\partial L}{\partial y} - \frac{d}{dx}\frac{\partial L}{\partial y'} \right)\eta\,dx = 0$$
因 $\eta$ 任意 ⇒ 被積函數必為零：
$$\boxed{\ \frac{\partial L}{\partial y} - \frac{d}{dx}\frac{\partial L}{\partial y'} = 0\ }$$

### 驗證：最速降線
代入 $L = \sqrt{\dfrac{1+y'^2}{2gy}}$（注意 $L$ 不含 $x$，有首次積分 $\;y'^2 = \dfrac{1}{2gy\,c} - 1$ 的 Bézout 形式），
解得擺線（cycloid）——與 1696 年諸大家的答案一致。一般方法一次成功。

### 從變分法到力學：作用量原理
把 $x$ 換成時間 $t$、$y$ 換成廣義座標 $q$，取 $L = T - V$：
$$\delta \int_{t_1}^{t_2} (T - V)\,dt = 0 \;\Longleftrightarrow\; \frac{\partial L}{\partial q} - \frac{d}{dt}\frac{\partial L}{\partial \dot q} = 0, \quad i = 1,\dots,n$$
**Newton 的 $n$ 個二階方程 ⇔ 一個純量函數 $L$ 的變分原理。**
約束力完全消失——牛頓形式的痛點被治癒。

### Python 驗證：諧振子的 Euler–Lagrange 方程
```python
import sympy as sp

t = sp.symbols('t')
q = sp.Function('q')(t)
k, m = sp.symbols('k m', positive=True)

L = sp.Rational(1,2)*m*sp.diff(q, t)**2 - sp.Rational(1,2)*k*q**2
eom = sp.diff(L, q) - sp.diff(sp.diff(L, sp.diff(q, t)), t)   # Euler–Lagrange
print(sp.simplify(eom))    # -k*q(t) - m*d²q/dt² = 0  ⟹  q'' = -(k/m) q，與 Newton 一致
```

## 結案
- 變分法成為標準數學分支；Euler 主動讓先，1755 年信件成為科學史美談。
- Lagrange 隨即建立「都靈學派」期刊，並花 33 年寫成《分析力學》（見 [1788-分析力學.md](1788-分析力學.md)）。
- 深遠影響：今日一切場論（電磁、廣義相對論、標準模型）都以「作用量 + 變分」為語言——全源自這封信。
