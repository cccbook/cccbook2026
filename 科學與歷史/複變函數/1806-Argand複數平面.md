# 1806 — Argand 複數平面

## 案件摘要
1797 年，挪威測量員 Caspar Wessel 在丹麥科學院宣讀了一篇論文，把複數 $a+bi$ 畫成平面上的點與向量，乘法變成「旋轉加伸縮」——卻被埋沒近一世紀。1806 年，巴黎的業餘數學家 Jean-Robert Argand 自費出版小冊子《Essai sur une manière de représenter les quantités imaginaires dans les constructions géométriques》，獨立提出同樣的幾何詮釋。虛數這樁纏鬥兩百多年的「無理之案」，終於在平面上找到了屍體與兇器：虛數不是幽靈，而是平面上看得見的旋轉。

## 前因 -- 為什麼會有這個案子
- 1545 年 Cardano 在解三次方程時被迫使用 $\sqrt{-121}$，自稱操作它「精神上的折磨」（mental tortures）。
- 1637 年 Descartes 創造「imaginary（虛構的）」一詞——這個名字本身就是偏見的判決書。
- 1702 年 Leibniz 形容 $\sqrt{-1}$ 是「介於存在與不存在之間的兩棲動物」（amphibium inter Ens et Non-ens）。
- Euler（1748）與 d'Alembert 大量使用複數運算， Euler 的 $e^{i\theta} = \cos\theta + i\sin\theta$ 已暗示幾何結構，卻沒人把它「畫出來」。
- Gauss 在 1799 年的博士論文中已私下擁有複數平面的想法（他聲稱虛數在平面上有直觀位置），但直到 1831 年才公開發表——這是一條被藏起來的關鍵證據。
- Wessel 1797 年的論文〈Om Directionens analytiske Betegning〉以丹麥文發表於科學院院報，當時無人注意，直到 1895 年才被 Juel 重新發現。

案發現場的核心問題是：**$\sqrt{-1}$ 到底是什麼？** 它不是數線上的任何一點，不是任何測量結果，兩百年來只被當作「運算的中間工具」。要結案，需要一張地圖——把數從一維的線解放到二維的平面。

## 線索與推理 -- 數學式、程式、理論

### 線索一：數的方向——Wessel 的向量想法
Wessel 是測量員，每天和「長度 + 方向」打交道。他問：如果一個數可以攜帶方向，那 $\sqrt{-1}$ 就是那個「轉了 90 度」的方向。Wessel 定義：單位長度、方向為 $\theta$ 的量就是 $\cos\theta + \varepsilon\sin\theta$（他的 $\varepsilon$ 就是我們的 $i$）。兩個這種量相乘：

$$(\cos\alpha + \varepsilon\sin\alpha)(\cos\beta + \varepsilon\sin\beta) = \cos(\alpha+\beta) + \varepsilon\sin(\alpha+\beta)$$

這正是複數乘法的**輻角相加律**。用現代記號：複數 $z = a+bi$ 對應平面向量 $(a,b)$，模長 $\rho = |z| = \sqrt{a^2+b^2}$，輻角 $\theta = \arg z$，極形式：

$$z = \rho(\cos\theta + i\sin\theta) = \rho e^{i\theta}$$

### 線索二：Argand 的旋轉詮釋
Argand 換了一個更直觀的角度：乘以 $-1$ 是把數線上的點**旋轉 180 度**。但兩次半轉才能等於一次整轉——那「一次半轉的一半」，即**旋轉 90 度**，是什麼？Argand 說：它就是 $\sqrt{-1}$。因為：

$$i \cdot i = e^{i\pi/2} \cdot e^{i\pi/2} = e^{i\pi} = -1$$

換言之，$i$ 不需要是「虛構的數」——它是平面上的一個旋轉算符。乘法 $z_1 z_2$ 的幾何意義：**模長相乘、輻角相加**（旋轉 + 伸縮）：

$$|z_1 z_2| = |z_1||z_2|, \qquad \arg(z_1 z_2) = \arg z_1 + \arg z_2$$

三次方程之所以會冒出虛數，也在此現形：Casus irreducibilis 中，三個實根必須經過複數中間步驟才能用根式表達——因為三次根式的公式本質上是「三分旋轉」，而實數軸裝不下旋轉。

### 線索三：De Moivre 定理與單位圓
1707 年 De Moivre 已給出公式（以三角形式）：

$$(\cos\theta + i\sin\theta)^n = \cos(n\theta) + i\sin(n\theta)$$

在 Argand 平面上，這只是「單位圓上旋轉 $n$ 次」的顯而易見事實。複數的 $n$ 次方根——原本文書上的代數噩夢——變成：單位圓均勻分成 $n$ 份的 $n$ 個點：

$$z^{n}=1 \;\Rightarrow\; z_k = e^{2\pi i k/n}, \quad k=0,\dots,n-1$$

這些點構成正 $n$ 邊形——$n$ 次單位根的幾何，後來成為 Gauss 1831 年理論與分圓理論的基礎。

### 線索四：Gauss 的公開判決（1831）
Gauss 在 1831 年的論文（及 1832 年分圓論文）中系統性地陳述複數平面：複數是平面上「位移」的完整代數，虛數單位 $i$ 表示縱向單位。他寫道：如果 $+1$、$-1$、$i$ 被賦予「直、反向、橫向」的幾何意義，一切神秘消失。他還首次使用記號選擇的影響——今日稱此平面為 **Argand 平面**或 **Gauss 平面**（complex plane）。Gauss 名氣太大，他的版本成為主流；Argand 的功勞被 Cauchy 等人於 1813–1815 年在《Annales de Mathématiques》上代為平反。

### 程式碼範例：Argand 圖——乘法就是旋轉加伸縮
```python
import numpy as np
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 3, figsize=(13, 4.2))

def draw(ax, z, z0, title):
    ax.quiver(0, 0, z0.real, z0.imag, angles='xy', scale_units='xy',
              scale=1, color='gray', label=f"$z_0$={z0:.2f}")
    ax.quiver(0, 0, z.real, z.imag, angles='xy', scale_units='xy',
              scale=1, color='red', label=f"結果={z:.2f}")
    # 畫單位圓與旋轉弧
    t = np.linspace(0, 2*np.pi, 200)
    ax.plot(np.cos(t), np.sin(t), 'b--', lw=0.5)
    ax.set_title(title); ax.legend(loc='upper left', fontsize=8)
    ax.set_aspect('equal'); ax.axhline(0, c='k', lw=0.3); ax.axvline(0, c='k', lw=0.3)

# 案件一：乘以 i = 旋轉 90 度
z0 = 1 + 0.5j
draw(axes[0], 1j*z0, z0, "$i \\cdot z_0$: 旋轉 $\\pi/2$")

# 案件二：乘以 -1 = 旋轉 180 度
draw(axes[1], -1*z0, z0, "$-z_0$: 旋轉 $\\pi$")

# 案件三：一般乘法 = 旋轉 + 伸縮
w = 1.5 * np.exp(1j * np.pi/3)
draw(axes[2], w*z0, z0, "$w z_0$: $\\rho\\times 1.5$, $\\arg+\\pi/3$")

# 數值驗證：模長相乘、輻角相加
print("|z0||w| =", abs(z0)*abs(w), " |wz0| =", abs(w*z0))
print("arg(z0)+arg(w) =", np.angle(z0)+np.angle(w), " arg(wz0) =", np.angle(w*z0))

# 額外驗證：1 的 6 次方根構成正六邊形
roots = np.array([np.exp(2j*np.pi*k/6) for k in range(6)])
print("六次單位根:", np.round(roots, 3))
```

數值輸出顯示 $|z_0||w| = |wz_0|$ 且 $\arg z_0 + \arg w = \arg(wz_0)$（模長相乘、輻角相加），以及六次單位根確實是正六邊形的六個頂點——Argand 平面的兩條鐵證。

## 結案 -- 後果與影響
- 虛數「看得見」了：複數從代數幽靈變成平面向量，哲學阻力一夕崩塌。數系從 $\mathbb{R}$ 擴充到 $\mathbb{C}$ 有了幾何保證。
- **複分析的地圖**：複變函數 $w = f(z)$ 從此是「平面到平面的映射」，解析函數的保角性質（conformality）成為可研究的幾何對象，直接鋪路給 1814 年 Cauchy 的積分定理。
- Wessel 1895 年被追認，Argand 平面之名留世；Gauss 1831 年公開版本定調，並以複數平面證明代數基本定理的幾何觀點（每個根是平面上一點）。
- 後續鏈條：Hamilton 1837 年試圖把複數推廣到三維失敗，1843 年被迫發明四元數——複數平面的成功與失敗共同塑造了現代代數。
- 影響至今：電路交流電分析（相量法）、訊號處理（$z$ 變換）、量子力學（波函數取值於複平面）、碎形（Mandelbrot 集合）皆以 Argand 平面為舞台。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Caspar Wessel | 1797 年首創複數平面向量詮釋，被埋沒一世紀 |
| Jean-Robert Argand | 1806 年獨立提出並公開發表，「Argand 平面」得名者 |
| Carl Friedrich Gauss | 1799 暗中擁有、1831 公開系統化，定調複數平面 |
| Leonhard Euler | $e^{i\theta}$ 公式暗藏幾何結構的先行者 |
| Adrien-Marie Legendre 等 | 1813–1815 為 Argand 平反的數學界人士 |

- C. Wessel, 〈Om Directionens analytiske Betegning〉, Danske Vidensk. Selsk. Skr. (1799 刊出，1797 宣讀)；1895 年被重新發現。
- J.-R. Argand, *Essai sur une manière de représenter les quantités imaginaires dans les constructions géométriques*, Paris (1806)。
- C. F. Gauss, *Theoria residuorum biquadraticorum, Commentatio secunda*, Göttingen (1831)：複數平面的公開系統化。
