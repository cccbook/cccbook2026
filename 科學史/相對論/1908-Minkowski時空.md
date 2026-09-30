# 1908 - Minkowski 時空（空間與時間融為一體）

## 案件摘要
1908 年 9 月，Einstein 的數學老師 Minkowski 在科隆演講開場即宣判：
「從今以後，孤立的空間與孤立的時間註定消逝為影子，只有兩者的結合才能保存獨立的實在性。」
他將 Lorentz 變換幾何化為四維時空的「旋轉」，相對論從一組方程變成一座幾何——廣義相對論的數學地基就此澆灌。

## 前因 -- 為什麼會有這個案子
- **1905 論文的「代數外觀」**：Einstein 原始論文以聯立方程呈現 Lorentz 變換，物理意義清楚，但缺乏幾何統一性——「為何 $t$ 與 $x$ 這樣混合？」仍是懸案。
- **非歐幾何的成熟**：Gauss、Riemann 的 $n$ 維度量幾何已備，卻無人想到套用在「時間」上。
- **Poincaré 的半步**：1906 年 Poincaré 已把 $(t, x, y, z)$ 當四維座標並引入類虛數時間 $ict$，但視為數學技巧。
- **Minkowski 的偵探直覺**：他是 Einstein 在蘇黎世聯邦理工的數學老師，曾說 Einstein 是「懶惰的狗」——如今學生的物理要靠老師的幾何加冕。

## 線索與推理 -- 數學式、程式、理論

### 四維時空座標
$$x^\mu = (x^0, x^1, x^2, x^3) = (ct,\; x,\; y,\; z), \qquad \mu = 0, 1, 2, 3$$
時間被乘上 $c$ 換算為長度，與空間座標平起平坐——「時空」（spacetime）一詞由此誕生。

### 時空間隔與其不變性
兩事件間的時空間隔：
$$ds^2 = -c^2 dt^2 + dx^2 + dy^2 + dz^2$$
**關鍵定理**：$ds^2$ 對所有慣性觀察者相同——$ds^2 = ds'^2$。
驗證：在 $S'$（速度 $v$ 沿 $x$）中代入 Lorentz 變換，
$$-c^2dt'^2 + dx'^2 = -\gamma^2(c\,dt - \beta\,dx)^2 + \gamma^2(dx - \beta\,c\,dt)^2 = -c^2dt^2 + dx^2 \quad(\beta = v/c)$$
交叉項恰好相消。這就是為何 Lorentz 變換「那樣混合」$t$ 與 $x$——它是保持 $ds^2$ 不變的變換。

### Minkowski 度規
$$\eta_{\mu\nu} = \mathrm{diag}(-1, +1, +1, +1), \qquad ds^2 = \eta_{\mu\nu}\, dx^\mu dx^\nu \quad(\text{Einstein 求和約定})$$
逆度規 $\eta^{\mu\nu} = \eta_{\mu\nu}$，用於升降指標：$x_\mu = \eta_{\mu\nu}x^\nu = (-ct, x, y, z)$。
（符號約定有兩派：$(-,+,+,+)$ 粒子物理常用，$(+,-,-,-)$ 相對論教科書常用，$ds^2$ 差一個整體符號。）

### 光錐與因果結構
以事件 $P$ 為原點，$ds^2$ 的符號將事件分為三類：
| 分類 | 條件 | 意義 |
|------|------|------|
| 類時 (timelike) | $ds^2 < 0$ | 可用低於光速的訊號連接，因果可相關；$|dx| < c\,dt$ |
| 類光 (lightlike/null) | $ds^2 = 0$ | 恰好以光速連接，光的世界線 |
| 類空 (spacelike) | $ds^2 > 0$ | 任何訊號皆不可達，因果無關；存在系統中兩事件「同時」 |

幾何圖像：每個事件都攜帶一個**光錐**——未來光錐（$t > 0$）是該事件能影響的區域，過去光錐是能影響它的區域。類空區域的事件「既非因亦非果」。光錐就是因果結構的幾何化身：**因果律 = 光錐不翻轉**。

### 固有時間：時空的「弧長」
類時世界線的固有时间：
$$\tau = \int \sqrt{-ds^2}/c = \int \sqrt{1 - v^2/c^2}\; dt$$
慣性（直線）世界線使 $\tau$ 極大——雙生子悖論在此幾何化結案。

### 四維向量與張量的誕生
- **四維速度**：$U^\mu = dx^\mu/d\tau = \gamma(c, \mathbf{v})$
- **四維動量**：$P^\mu = m U^\mu = (E/c,\; \mathbf{p})$——能量與動量統一為一個四維向量，$P^\mu P_\mu = -m^2c^2$ 即 $E^2 = (pc)^2 + (mc^2)^2$。
- **四維電流**：$J^\mu = (c\rho, \mathbf{J})$；Maxwell 方程組可寫成協變形式 $\partial_\mu F^{\mu\nu} = \mu_0 J^\nu$。
- Lorentz 變換 = 保持 $\eta_{\mu\nu}$ 不變的線性變換：$\Lambda^\mu{}_\rho \Lambda^\nu{}_\sigma \eta_{\mu\nu} = \eta_{\rho\sigma}$——即時空的**雙曲旋轉**（快度參數化：$x^0' = x^0\cosh\varphi - x^1\sinh\varphi$，$\tanh\varphi = \beta$）。
- 度規、張量、協變性——廣義相對論的全部數學語言在此備齊。

### Python 模擬：光錐圖與因果分類

```python
import numpy as np
import matplotlib.pyplot as plt

c = 1.0
fig, axes = plt.subplots(1, 2, figsize=(11, 5))

# 左圖: 光錐
ax = axes[0]
t = np.linspace(-5, 5, 100)
for s in (1, -1):
    ax.plot(s * c * t, t, "r--", lw=1)
tt, xx = np.meshgrid(np.linspace(-5, 5, 400), np.linspace(-5, 5, 400))
ds2 = xx**2 - c**2 * tt**2
ax.contourf(xx, tt, np.sign(ds2), levels=[-2, 0, 2],
            colors=["lightyellow", "lightblue"], alpha=0.6)
ax.set_title("Light cone: blue=spacelike, yellow=timelike, red=null")
ax.set_xlabel("x"); ax.set_ylabel("ct")

# 右圖: Lorentz 變換 = 雙曲旋轉 (beta = 0.6)
ax = axes[1]
beta = 0.6
gamma = 1 / np.sqrt(1 - beta**2)
ax.plot(t, t, "r--", lw=1)
for ang in np.linspace(0, np.arctanh(beta), 6):
    x0 = np.linspace(-4, 5, 50)
    x1 = x0 * np.tan(ang) if abs(np.tan(ang)) < 1e6 else x0 / beta
    ax.plot(np.cosh(ang) * x1 - np.sinh(ang) * x0 * c * 0 + 0*x0, 0*x0, alpha=0)  # placeholder
    # 雙曲旋轉後的世界線 x' = 常數 (運動物體)
    xp = 0
    tp = np.linspace(-4, 4, 50)
    xxp = gamma * (xp + beta * c * tp)
    ax.plot(xxp, tp, "b-", lw=0.8, alpha=0.6)
ax.plot(0, 0, "ko", label="event P")
ax.set_title("Hyperbolic rotation: worldlines tilted by beta=0.6")
ax.set_xlabel("x"); ax.set_ylabel("ct"); ax.legend()

plt.tight_layout()
plt.savefig("lightcone.png", dpi=100)
print("已輸出 lightcone.png")

# 因果分類數值檢驗
events = [(1, 0), (0, 3), (3, 1), (2, 4)]  # (x, ct)
for x, ct in events:
    d = x**2 - ct**2
    kind = "lightlike" if abs(d) < 1e-12 else ("timelike" if d < 0 else "spacelike")
    print(f"事件 (x={x}, ct={ct}): ds^2 = {d:+.1f} -> {kind}")
```

輸出節選：
```
事件 (x=1, ct=0): ds^2 = +1.0 -> spacelike
事件 (x=0, ct=3): ds^2 = -9.0 -> timelike
事件 (x=3, ct=1): ds^2 = +8.0 -> spacelike
事件 (x=2, ct=4): ds^2 = -12.0 -> timelike
```

## 結案 -- 後果與影響
- 相對論獲得幾何形式：Lorentz 變換 = 時空雙曲旋轉，物理量以四維張量協變表述。
- 直接鋪路廣義相對論：Einstein 與 Grossmann (1912–1915) 將 Minkowski 度規推廣為彎曲時空的 $g_{\mu\nu}$ 與 Riemann 幾何，1915 年場方程 $G_{\mu\nu} = 8\pi G T_{\mu\nu}/c^4$ 誕生。
- 「空間與時間融為一體」成為現代物理的世界觀：粒子物理的 Feynman 圖、黑洞的視界（光錐翻轉處）、重力波偵測，皆以時空幾何為語言。
- 諷刺的尾聲：Minkowski 於 1909 年 1 月因病去世（年僅 44 歲），未能親見 1915 年學生用他的幾何改寫宇宙。

## 關鍵人物與文獻
- **Hermann Minkowski**：〈空間與時間〉(Raum und Zeit), 科隆演講 1908；收錄於 Phys. Z. 10, 104 (1909)。
- **Henri Poincaré** (1906)：四維座標的先驅工作。
- **Albert Einstein**：1905 狹義相對論（本案的物理基礎）。
- **Hermann Minkowski 曾任教於**：蘇黎世聯邦理工學院（Einstein 的數學老師）。
- 相關案件：`1905-狹義相對論.md`、`1907-等效原理.md`。
