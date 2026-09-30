# 1739 Clairaut 隱式解與奇解：包絡線的發現

## 案發現場

1739 年，巴黎。年僅二十六歲的 Alexis Claude Clairaut 已是法國科學院最年輕的院士——他十八歲就靠幾何研究入選，被視為神童。此時微積分經過 Euler 的系統化（見 [1727-Euler常微分方程.md](1727-Euler常微分方程.md)），一階方程的解法地圖已初具規模，但一個根本性的概念問題仍然懸而未決：

> 微分方程的「解」一定是什麼樣子？一定要寫成 $y = f(x)$ 的**顯式**形式嗎？如果一條曲線只能用**隱式**方程 $F(x, y) = 0$ 描述，甚至根本不是單一函數的圖像，它還算不算解？

更深一層的謎題是：Euler 與 Bernoulli 們解方程時，總是先給定初值、再求滿足初值的解——解的個數似乎由初值唯一決定。但 Clairaut 在研究某些方程時發現了一種**怪異的現象**：某些微分方程除了「正常」的解族之外，還藏著一條**多出來的解**——它不屬於通解族，卻處處滿足微分方程，而且在幾何上是整個解族的**包絡線**（envelope，即與解族中每一條曲線都相切的曲線）。

這個現象為何重要？因為它動搖了「初值唯一決定解」的直覺——在包絡線上，兩條無限接近的解曲線在此相切匯合，初值資訊失效。這是**微分方程解的奇異性（singularity）**的首次現身，也是日後奇點理論、分歧理論（bifurcation theory）的遠祖。

## 偵查過程

### 第一步：Clairaut 方程的結構

Clairaut 於 1734-1739 年間研究的一類方程，今日稱為 **Clairaut 方程**：

$$y = x\, y' + f(y')$$

它的特點是：$x$ 與 $y$ 只以 $y'$ 為媒介出現——$y$ 等於「$x$ 乘以斜率」加上「斜率的某個函數」。這種結構在幾何上有個自然的解讀：若記 $p = y'$，方程變成

$$y = px + f(p)$$

這正是**直線族**的方程！以 $p$ 為參數，每一個 $p$ 值給出一條斜率為 $p$、截距為 $f(p)$ 的直線。

### 第二步：求通解——直線族

Clairaut 的第一步推理是：既然直線族 $y = px + f(p)$ 中的每一條直線斜率恆為 $p$，把它代入原方程驗證：

$$y' = p, \qquad y = x\,p + f(p) \quad\Rightarrow\quad y = x\,y' + f(y') \checkmark$$

所以**直線族就是通解**：對每個常數 $C$，$y = Cx + f(C)$ 都是解。這半個謎題平淡無奇。

### 第三步：關鍵靈感——對方程求導，讓「多出來的解」現形

真正的奇案在第二步。Clairaut 的關鍵靈感是：**對方程兩邊求導**，看會冒出什麼。設 $p = y'$，對 $y = xp + f(p)$ 求導（記住 $p$ 是 $x$ 的函數，用乘積法則與鏈鎖法則）：

$$y' = p + x\, p' + f'(p)\, p'$$

左邊 $y'$ 就是 $p$，代回並整理：

$$p = p + \left(x + f'(p)\right) p' \quad\Rightarrow\quad \left(x + f'(p)\right) p' = 0$$

**兩個因子的乘積為零**，於是有兩種可能：

**情況一**：$p' = 0$，即 $p = C$ 為常數——這就是剛才的直線族（通解）。

**情況二**：$x + f'(p) = 0$，即

$$x = -f'(p)$$

這第二種情況就是那個**多出來的解**！把 $x = -f'(p)$ 代回原方程 $y = px + f(p)$：

$$y = -p\, f'(p) + f(p)$$

聯立起來，得到一條以 $p$ 為參數的曲線：

$$\boxed{\;x = -f'(p), \qquad y = f(p) - p\, f'(p)\;}$$

它**不是直線**（除非 $f$ 特殊），卻處處滿足微分方程——一條不屬於通解族的「奇解」（singular solution）。

### 第四步：奇解的幾何身分——包絡線

Clairaut 再進一步揭示了奇解的幾何意義：這條奇解是**直線族的包絡線**。驗證如下：直線族 $\Phi(x, y, p) = px + f(p) - y = 0$，包絡線的標準條件是：

$$\Phi = 0 \quad\text{且}\quad \frac{\partial \Phi}{\partial p} = 0$$

計算偏導：$\dfrac{\partial \Phi}{\partial p} = x + f'(p) = 0$——**這正是情況二的條件**！

更進一步，可以驗證奇解與每條直線**相切**：在 $x = -f'(p_0)$ 處，奇解的斜率為

$$\frac{dy}{dx} = \frac{dy/dp}{dx/dp} = \frac{f'(p) - f'(p) - p f''(p)}{-f''(p)} = \frac{-p f''(p)}{-f''(p)} = p$$

奇解在切點的斜率恰為 $p$，與該直線的斜率相同——兩者相切！包絡線與解族中每一條曲線相切、位於解族的邊界上。

### 第五步：全微分與隱函數解的探索

Clairaut 的工作還延伸到更廣的領域：**全微分方程**（total differential equations）與**隱函數定理**。他在研究多變數微分關係時，系統地探索了

$$dz = M\, dx + N\, dy$$

何時可積分（恰當條件 $\partial M/\partial y = \partial N/\partial x$），以及何時積分結果是隱式關係 $F(x, y, z) = 0$ 而非顯式解。這些探索與他同時代的 Euler、d'Alembert 相互呼應，為日後的隱函數定理（Euler-Lagrange 時代之後由 Lagrange、Cauchy 嚴格化）鋪路。Clairaut 的洞見是：**解不必是顯式的**——隱式關係 $F(x,y)=0$ 同樣是合法的解，而奇解正是隱式關係中的奇點（$\partial F/\partial y = 0$ 之處，隱函數定理失效）。

## 結案報告

謎題就此告破：Clairaut 方程 $y = xy' + f(y')$ 的解有兩族——**通解**為直線族 $y = Cx + f(C)$，**奇解**為包絡線 $x = -f'(p),\ y = f(p) - pf'(p)$。

此案的遺產：

1. **奇解概念的誕生**。Clairaut 是第一位明確區分「通解」與「奇解」的數學家。奇解不包含於通解之中（無論 $C$ 取何值），卻處處滿足方程——這個現象挑戰了直覺，也開啟了微分方程奇異性研究的大門。
2. **包絡線理論**。Clairaut 揭示了「微分方程的奇解 = 解族的包絡線」這一深刻的幾何-分析聯繫。此後 Lagrange 在《Mécanique analytique》中發展了系統的包絡線理論（Lagrange 乘子法與此一脈相承），今日從優化理論、微分幾何到熱力學相變（相變點正是自由能面族的包絡），包絡無所不在。
3. **解的存在唯一性的遠祖**。包絡線上「兩條解曲線相切匯合、初值失效」的現象，是對解的唯一性定理的最早挑戰。半世紀後 Cauchy 與 Lipschitz 給出的存在唯一性定理，正是以排除這類奇異現象為目標。
4. **隱式解與全微分**。Clairaut 對隱式關係與全微分的探索（承繼 [1727-Euler常微分方程.md](1727-Euler常微分方程.md) 中的恰當方程），成為隱函數定理與多變數微積分嚴格化的先聲。
5. **奇點理論之源**。二十世紀的奇點理論（Whitney、Thom 的突變論/catastrophe theory）研究「光滑族產生奇異邊界」的普適模式——包絡線正是最簡單的範例，Thom 的突變論中摺疊突變（fold catastrophe）的幾何核心就是一族曲面的包絡。

Clairaut 本人的科學生涯同樣輝煌：他於 1743 年發表《Théorie de la figure de la Terre》研究地球形狀（Clairaut 定理至今是地球物理學的基石），1758 年正確預測了哈雷彗星於 1759 年回歸的時間（誤差僅一個月）——用微分方程計算天體軌道，正是他一生致力的方向。他在微分方程中發現的「多出來的解」，如同他預測的彗星：藏在方程的深處，卻在正確的時刻現身。

## 證據與工具

以下 Python 程式繪出 Clairaut 方程的直線族與其包絡線（奇解）：

```python
import numpy as np
import matplotlib
matplotlib.use("Agg")            # 無顯示環境下也能執行
import matplotlib.pyplot as plt

# 案例方程：y = x·y' + (y')²   即 f(p) = p²
# 通解（直線族）：y = Cx + C²
# 奇解（包絡線）：x = -2p, y = p² - 2p² = -p²  →  y = -x²/4
f  = lambda p: p**2
fp = lambda p: 2*p

fig, ax = plt.subplots(figsize=(8, 6))

# 畫直線族（通解）：每個 C 一條直線
xs = np.linspace(-6, 6, 200)
for C in np.linspace(-2, 2, 9):
    ax.plot(xs, C*xs + C**2, color="gray", alpha=0.6,
            label=f"y = {C:.1f}x + {C:.1f}²" if C in [-2, 2] else None)

# 畫奇解（包絡線）：x = -f'(p) = -2p, y = f(p) - p·f'(p) = -p²
ps = np.linspace(-2, 2, 200)
ax.plot(-fp(ps), f(ps) - ps*fp(ps), "r-", lw=3, label="奇解（包絡線）y = -x²/4")

# 標註相切點：直線 y = Cx + C² 與包絡線切於 x = -2C
for C in [-1.5, -0.5, 0.5, 1.5]:
    tx, ty = -2*C, C**2 - 2*C**2
    ax.plot(tx, ty, "ko", ms=5)
ax.annotate("包絡線與每條直線相切", xy=(1.0, -0.25), xytext=(2.0, -2.0),
            arrowprops=dict(arrowstyle="->"))

ax.set_xlim(-6, 6); ax.set_ylim(-4, 4)
ax.axhline(0, color="k", lw=0.5); ax.axvline(0, color="k", lw=0.5)
ax.legend(loc="upper left"); ax.set_title("Clairaut 方程 y = xy' + (y')²：直線族與包絡線（奇解）")
plt.savefig("clairaut_envelope.png", dpi=100, bbox_inches="tight")
print("圖已存為 clairaut_envelope.png")

# 數值驗證：奇解 y = -x²/4 處處滿足 y = x·y' + (y')²
check = lambda x: -x**2/4 - (x*(-x/2) + (-x/2)**2)
print(f"驗證奇解 y=-x²/4 滿足方程（殘差應為 0）: max |殘差| = {max(abs(check(x)) for x in xs):.2e}")

# 驗證通解 y = Cx + C² 滿足方程
C = 1.3
res = lambda x: (C*x + C**2) - (x*C + C**2)
print(f"驗證通解 y = {C}x + {C}² 滿足方程（殘差應為 0）: max |殘差| = {max(abs(res(x)) for x in xs):.2e}")

# 觀察：奇解 y = -x²/4 不屬於直線族（無論 C 取何值都不是拋物線），
# 卻處處滿足方程且與每條直線相切 → Clairaut 的「多出來的解」真實存在
```

執行後可見：灰色的直線族（通解）被紅色的拋物線（奇解/包絡線）從下方托住，兩者處處相切——Clairaut 於 1739 年揭露的「多出來的解」，就這樣浮現在圖像上。
