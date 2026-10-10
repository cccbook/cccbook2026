# 1744 — Euler 變分法

## 案件摘要
1744 年，Euler 在柏林出版《Methodus Inveniendi Lineas Curvas Maximi Minimive Proprietate Gaudentes》（尋求具有極大極小性質的曲線的方法），史上第一次把「在所有曲線中找極值」這類問題系統化。他導出的極值條件——今日稱為 Euler 方程（Euler–Lagrange 方程）：

$$\frac{\partial F}{\partial y} - \frac{d}{dx}\frac{\partial F}{\partial y'} = 0$$

把無窮維的幾何極值問題化為一條常微分方程。這是變分法的誕生證書，也是此後兩百年理論力學變分原理的數學引擎。

## 前因 -- 為什麼會有這個案子
- **最速降線問題（1696）**： Johann Bernoulli 向全歐洲挑戰：求從 $A$ 滑到 $B$ 最快的曲線。Newton、Leibniz、L'Hôpital、兩位 Bernoulli 兄弟都交出答案——擺線（cycloid）。但大家的解法都是針對單一問題的「個案偵查」，沒有一般方法。
- **等周問題**：古希臘以來的老問題——固定周長中什麼曲線圍出最大面積（答案：圓）。17 世紀末 James Gregory、Jacob Bernoulli 用幾何方法處理，但方法繁瑣且不一般。
- **Newton 的阻力最小問題（1685）**：Newton 在《Principia》中求旋轉體在流體中受阻力最小的形狀——這其實是第一個變分法問題，但 Newton 用了保密的幾何技巧。
- **極值問題的共同結構**：普通微積分處理「函數在某一點的極值」（有限維），但這些問題是「函數在整條曲線上的極值」（無窮維）——傳統導數 $\frac{dy}{dx}=0$ 完全派不上用場。年輕的 Euler（1707–1783）意識到：需要一套新的微積分。

## 線索與推理 -- 數學式、程式、理論

### 線索一：Euler 的原始方法——折線逼近
1744 年書中的推理是一場「無窮維的圍捕」。Euler 的策略：用逐段線性的折線代替曲線。考慮積分泛函

$$J[y] = \int_a^b F(x, y, y')\,dx$$

把 $[a,b]$ 分成 $n$ 段，折線的節點值 $y_1, y_2, \dots, y_{n-1}$ 是有限個自由變數（端點固定 $y(a)=A, y(b)=B$）。於是 $J$ 變成普通的多元函數，對每個 $y_i$ 求偏導並令其為零：

$$\frac{\partial J}{\partial y_i} = \frac{\partial F}{\partial y}(x_i, y_i, y'_i)\,h - \left[\frac{\partial F}{\partial y'}(x_{i+1}, y_{i+1}, y'_{i+1}) - \frac{\partial F}{\partial y'}(x_i, y_i, y'_i)\right] = 0$$

令 $n \to \infty$，方括號除以 $h$ 收斂到導數，得到：

$$\frac{\partial F}{\partial y} - \frac{d}{dx}\frac{\partial F}{\partial y'} = 0$$

**極值曲線必須滿足這條二階常微分方程**。Euler 用這個方法重解了最速降線、等周問題等已知案例，全部命中——方法通過了驗證。

### 線索二：重審最速降線
最速降線問題的泛函（能量守恆 $v = \sqrt{2gy}$，時間是路徑積分）：

$$T[y] = \int_0^B \sqrt{\frac{1 + y'^2}{2gy}}\,dx$$

代入 Euler 方程。被積函數 $F$ 不顯含 $x$，存在首次積分（Beltrami 恆等式的特例）：

$$F - y'\frac{\partial F}{\partial y'} = \frac{1}{\sqrt{2gy(1+y'^2)}} = \text{常數}$$

解出 $y(1 + y'^2) = C$，這正是**擺線**的微分方程——與 1696 年挑戰賽的答案完全一致。個案變成了定理。

### 線索三：Lagrange 的改進——從幾何到解析
1755 年，年僅 19 歲的 Lagrange 寫信給 Euler，提出用純解析的方法（不用折線）處理變分：對曲線做虛擾動 $y(x) + \epsilon\,\eta(x)$（端點 $\eta(a)=\eta(b)=0$），計算泛函的一階變化：

$$\delta J = \int_a^b \left(\frac{\partial F}{\partial y}\eta + \frac{\partial F}{\partial y'}\eta'\right) dx = \int_a^b \left(\frac{\partial F}{\partial y} - \frac{d}{dx}\frac{\partial F}{\partial y'}\right)\eta\, dx + \left[\frac{\partial F}{\partial y'}\eta\right]_a^b$$

第二步用分部積分。由於 $\eta$ 任意且端點擾動為零，得極值條件：

$$\frac{\partial F}{\partial y} - \frac{d}{dx}\frac{\partial F}{\partial y'} = 0$$

與 Euler 方程一致，但推理乾淨得多。Euler 大為讚賞，將新方法命名為「變分法」（calculus of variations），並在 1764 年後的著作中改用 Lagrange 的方式。記號 $\delta$ 也是 Lagrange 引入的。

### 線索四：通往力學的變分原理
變分法立即被應用到力學。Hamilton（1834）的最小作用量原理：

$$S[q] = \int_{t_1}^{t_2} L(q, \dot{q}, t)\, dt, \qquad \delta S = 0 \;\Rightarrow\; \frac{\partial L}{\partial q} - \frac{d}{dt}\frac{\partial L}{\partial \dot{q}} = 0$$

其中 $L = T - V$ 為 Lagrangian。牛頓力學的 $F = ma$ 與「作用量極值」等價——整個力學被重寫為一條變分原理。Euler 1744 年的那條方程，成為從經典力學到量子場論（費曼路徑積分、規範場論）的共同起點。

### 程式碼範例：Euler–Lagrange 方程的數值求解（最速降線）
```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# 最速降線的首次積分: y(1 + y'^2) = C，參數解（擺線）
# x = r(t - sin t), y = r(1 - cos t)
def cycloid(r, t):
    return r * (t - np.sin(t)), r * (1 - np.cos(t))

# 端點: A=(0,0) 到 B=(1, 0.5)。求 r 使擺線過 B：
from scipy.optimize import brentq
def f(r):
    x, y = cycloid(r, np.pi)          # 擺線在 t=pi 處最低
    # 用數值積分找 t 使 (x,y) = (1, 0.5) —— 改用參數式求解
    return None
# 直接求 r: y_B = r(1-cos t), x_B = r(t - sin t)，聯立解 t, r
def eqs(t):
    # 由 x_B=1 反推 r，再檢查 y_B
    r = 1.0 / (t - np.sin(t))
    return r * (1 - np.cos(t)) - 0.5
t_end = brentq(eqs, 0.5, 2 * np.pi)
r = 1.0 / (t_end - np.sin(t_end))

t = np.linspace(0, t_end, 100)
x, y = cycloid(r, t)

# 數值驗證：用有限差分檢查歐拉方程 F - y' F_{y'} = const
yp = np.gradient(y, x)
val = 1.0 / np.sqrt(2 * 9.8 * y * (1 + yp**2))
print("首次積分值（應為常數）:", val[5], "vs", val[-5])

fig, ax = plt.subplots(figsize=(7, 5))
ax.plot(x, y, lw=2, label="最速降線（擺線）")
ax.plot([0, 1], [0, 0.5], "ro")
ax.plot(x, x * 0.5, "g--", lw=1, label="直線（比較）")
ax.set_aspect("equal"); ax.legend(); ax.invert_yaxis()
plt.show()
```

數值輸出顯示首次積分 $F - y'\frac{\partial F}{\partial y'} = \dfrac{1}{\sqrt{2gy(1+y'^2)}}$ 沿擺線為常數——直接驗證了 Euler 方程。而比較曲線顯示：擺線確實比直線「下降得更快」。

## 結案 -- 後果與影響
- **變分法正式誕生**：極值問題從「個案偵查」變成「一般方法」，1755 年 Lagrange 的解析改進使其定型。
- **力學的重寫**：Lagrange《Mécanique analytique》（1788）以變分法重建整個力學——牛頓的幾何推理被代數取代。Hamilton 1834 年的最小作用量原理是巔峰。
- **幾何的擴張**：測地線、極小曲面（Plateau 問題）、等周問題全部納入變分法框架。
- **通往現代物理**：量子力學的路徑積分（Feynman, 1948）、廣義相對論的場方程、粒子物理的標準模型，全部以「作用量極值」為語言——Euler 1744 年的方程是共同祖先。
- 影響至今：最佳控制理論、機器學習的泛函優化、影像處理的變分方法，都是這個案件的直接後代。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Leonhard Euler | 1744 年系統化變分法，導出 Euler 方程 |
| Johann Bernoulli | 1696 年最速降線挑戰的發起者 |
| Jacob Bernoulli | 等周問題的先驅 |
| Joseph-Louis Lagrange | 1755 年解析改進，命名「變分法」，1788 年《Mécanique analytique》 |
| William Rowan Hamilton | 1834 年最小作用量原理 |

- L. Euler, *Methodus Inveniendi Lineas Curvas Maximi Minimive Proprietate Gaudentes*, Berlin (1744)。
- J.-L. Lagrange, *Mécanique analytique*, Paris (1788)。
- C. B. Boyer, *The History of the Calculus and its Conceptual Development*, Dover (1949)。
