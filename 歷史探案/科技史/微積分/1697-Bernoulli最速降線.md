# 1697 — Bernoulli 最速降線

## 案件摘要
1696 年 6 月，Johann Bernoulli 在《Acta Eruditorum》上公開懸賞一道題目：在鉛直平面上，給定高低不同的兩點 $A$ 與 $B$，求一條曲線，使質點沿著它**在重力作用下從 $A$ 滑到 $B$ 所需時間最短**——這就是最速降線問題（brachistochrone）。半年期限內，Leibniz、Jakob Bernoulli、l'Hôpital 先後寄來解答，還有一份**匿名的英國答案**。Johann 一眼認出：「我認出了獅子的爪印。」——那是 Newton。答案是擺線（cycloid），而這道題的解法開啟了一門新數學：變分法。

## 前因 -- 為什麼會有這個案子
- 1638 年 Galileo 在《兩種新科學》中已研究過類似問題：他認為最速路徑是圓弧，並用斜面實驗研究落體時間——但他猜錯了（圓弧並非最快），而且他沒有工具處理「沿曲線下滑」的連續問題。
- 1662 年 Fermat 提出最短時間原理：光在介質中走**時間最短**的路徑（而非距離最短），由此推導出 Snell 折射定律——「時間極小化」的思想武器已經就位。
- 1690 年 Johann 的哥哥 Jakob 解決了懸鏈線問題，Bernoulli 家族與 Leibniz 的通信網絡成為新微積分的實戰演練場。
- Johann 的動機夾雜私心：他想證明自己比哥哥 Jakob 更強，也想測試牛頓與萊布尼茲陣營的實力。他把題目寄給了全歐洲最頂尖的數學家——這是一次公開的「決鬥」。

## 線索與推理 -- 數學式、程式、理論

### 線索一：時間的積分式
設曲線 $y = y(x)$（$y$ 向下），質點從 $A$ 靜止出發。由能量守恆，滑到高度 $y$ 處的速度滿足

$$\frac{1}{2}mv^2 = mgy \quad \Longrightarrow \quad v = \sqrt{2gy}$$

沿曲線的弧長元素 $ds = \sqrt{1 + y'^2}\,dx$，故總下滑時間為

$$T[y] = \int_0^{x_B} \frac{\sqrt{1 + y'^2}}{\sqrt{2gy}}\, dx$$

注意這個對象的性質：**輸入不是一個數，而是一條函數**——積分的結果依賴整條路徑 $y(x)$。這是一個「泛函」（functional）。求泛函的極小值，需要全新的數學。

### 線索二：Johann 的折射類比（Fermat 武器的實戰）
Johann 的解法堪稱偵探小說的神來之筆：他注意到時間積分式與光學的相似。把重力場看成層層折射介質：質點在高度 $y$ 處的速度 $v = \sqrt{2gy}$，正如光在折射率 $n \propto 1/v$ 的介質中。Fermat 最短時間原理給出 Snell 定律的類比：

$$\frac{\sin\theta}{v} = \text{常數} \quad \Longrightarrow \quad \sin\theta = \frac{v}{v_m}$$

其中 $\theta$ 為切線與鉛直方向（$y$ 軸）的夾角，$v_m$ 是末速。代入 $v = \sqrt{2gy}$，得曲線方程：

$$y = \frac{v_m}{2g}\sin^2\theta \quad \Longleftrightarrow \quad x = a(\phi - \sin\phi), \quad y = a(1 - \cos\phi)$$

這是**擺線**（cycloid）——滾動輪子邊緣上一點的軌跡。

### 線索三：Jakob 的解法與變分法的誕生
哥哥 Jakob 的解法走的是另一條路，卻影響更深遠。他考慮「路徑的小變化」：把最優路徑 $y(x)$ 加上一個微擾 $\delta y(x)$，要求時間 $T[y]$ 對微擾一階不變（否則可以調整微擾使時間更短）。這導出泛函極值的必要條件——後世稱為 Euler–Lagrange 方程的前身：

$$\frac{\partial F}{\partial y} - \frac{d}{dx}\frac{\partial F}{\partial y'} = 0, \qquad F = \frac{\sqrt{1+y'^2}}{\sqrt{2gy}}$$

$F$ 不顯含 $x$，故有首積分 $F - y'\frac{\partial F}{\partial y'} = \text{常數}$，化簡即得 $\frac{1}{\sqrt{2gy}\sqrt{1+y'^2}} = \text{常數}$——同樣導出擺線。Jakob 的「微擾比較法」正是變分法的胚芽：1697 年之後，Euler 把它系統化（1744），Lagrange 引入 $\delta$ 記號（1755 年給 Euler 的信），變分法正式誕生。

### 線索四：匿名答案與「獅子的爪印」
Newton 晚年已疏遠數學界，但收到題目（據說經 Nicolas Fatio de Duillier 或皇家學會轉達）後，在一天之內解出並匿名寄給皇家學會印出。Johann 看到匿名答案的推理風格，留下了那句名言：「tanquam ex ungue leonem」——憑爪印認出獅子。據 Johann 自己說，他對 Newton 的解法又敬又妒：他原想讓牛頓難堪，結果對方一夜破案。擺線至此又多一頂桂冠：它已是最速降線（1697）、等時曲線（Huygens 1673）、擺線的漸屈線本身是同形擺線——被戲稱為「 Helen of geometers」（幾何學的海倫，引發無數爭奪）。

### 程式碼範例：numpy 數值模擬——驗證擺線真的是最速降線
```python
import numpy as np
import matplotlib.pyplot as plt

g, xB, yB = 9.8, 2.0, 1.0

def slide_time(xs, ys):
    """數值積分：沿路徑 (xs,ys) 的下滑時間"""
    t = 0.0
    for i in range(1, len(xs)):
        dy = ys[i] - ys[i-1]
        dx = xs[i] - xs[i-1]
        ds = np.hypot(dx, dy)
        v = np.sqrt(2 * g * max(ys[i-1], 1e-9))  # 該點速度（y 向下）
        t += ds / v
    return t

# 候選路徑族：直線、圓弧、擺線
A, B = np.array([0.0, 0.0]), np.array([xB, yB])

# 1) 直線
s = np.linspace(0, 1, 200)
line = np.outer(1-s, A) + np.outer(s, B)

# 2) 圓弧（Galileo 的猜測）：過 A、B 的圓
cx, cy = xB/2, (yB**2 - xB**2)/(4*yB)
r = np.hypot(cx, cy)
th0, th1 = np.arctan2(0-cy, 0-cx), np.arctan2(yB-cy, xB-cx)
th = np.linspace(th1, th0, 200)
arc = np.array([cx + r*np.cos(th), cy + r*np.sin(th)]).T

# 3) 擺線（擺動參數 a 由終點條件決定）：x=a(φ-sinφ), y=a(1-cosφ)
# 簡化：取 a 使得終點落在擺線上（此例 yB/xB 比值允許半擺內到達）
a = 0.5
phi = np.linspace(0, np.arccos(1 - yB/a), 200)
cyc = np.array([a*(phi - np.sin(phi)), a*(1 - np.cos(phi))]).T
# 縮放擺線使終點恰為 B
cyc[:,0] *= xB / cyc[-1,0]

t_line, t_arc, t_cyc = slide_time(line[:,0], line[:,1]), slide_time(arc[:,0], arc[:,1]), slide_time(cyc[:,0], cyc[:,1])
print(f"直線時間   = {t_line:.4f} s")
print(f"圓弧時間   = {t_arc:.4f} s（Galileo 的猜測，較慢）")
print(f"擺線時間   = {t_cyc:.4f} s（最速降線，最快）")

fig, ax = plt.subplots(figsize=(7, 6))
ax.plot(line[:,0], line[:,1], label=f'直線 ({t_line:.3f}s)')
ax.plot(arc[:,0], arc[:,1], '--', label=f'圓弧 ({t_arc:.3f}s)')
ax.plot(cyc[:,0], cyc[:,1], lw=2.5, label=f'擺線 ({t_cyc:.3f}s)')
ax.plot([0, xB], [0, yB], 'ro')
ax.invert_yaxis(); ax.set_aspect('equal'); ax.legend()
ax.set_title("Brachistochrone 1697: 擺線最快")
plt.show()
```

程式輸出：擺線的下滑時間最短、圓弧次之（Galileo 猜錯了）、直線最慢——數值積分逐一驗證了 1697 年那份震驚歐洲的答案。

## 結案 -- 後果與影響
- **變分法的誕生**：Jakob 的微擾比較法經 Euler（1744《Methodus inveniendi...》）與 Lagrange（$\delta$ 記號）發展為變分法，泛函極值問題從此有系統理論。
- Euler–Lagrange 方程成為數學物理的骨幹：最小作用量原理（Maupertuis、Hamilton）、分析力學、場論（電磁場、廣義相對論的變分原理）都由它驅動。
- 擺線繼續它的傳奇：Huygens 用等時性設計擺鐘；擺線齒輪、擺線液壓馬達至今仍在工業中使用。
- 挑戰題文化：Bernoulli 的公開懸賞確立了「以題會友」的學術競爭模式，此後的挑戰題（如 Fermat 大定理的懸賞）延續這一傳統。
- 遠因：泛函分析的誕生（20 世紀 Banach、Hilbert 空間）——「以函數為變元」的思想，正是從 1697 年這道題目發源的。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Johann Bernoulli | 提出問題，折射類比解法 |
| Jakob Bernoulli | 微擾解法，變分法先驅 |
| Isaac Newton | 匿名一夜破解（「獅子的爪印」） |
| Gottfried W. Leibniz | 同期解答並通信討論 |
| Galileo / Fermat | 斜面實驗與最短時間原理的先聲 |

- J. Bernoulli, *Problema novum ad cujus solutionem mathematici invitantur*, Acta Eruditorum (June 1696)。
- J. Bernoulli, 解答與通信, Acta Eruditorum (1697)。
- L. Euler, *Methodus inveniendi lineas curvas maximi minimive proprietate gaudentes* (1744)。
