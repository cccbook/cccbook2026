# 1964-Hironaka 奇點解消

## 案件摘要
1964 年，廣中平祐（Heisuke Hironaka）證明特徵 0 域上任意代數簇皆可透過一連串 blow-up「解消奇點」，使簇變得光滑。這個百年懸案以「不變量遞降」的壯觀論證落幕，也為 Grothendieck 綱領補上最後一塊基石。

## 前因 -- 為什麼會有這個案子
- 代數簇 $X \subset \mathbb{A}^n$ 是多項式方程的公共零點集，但零點集可能有**奇點**（如尖點、自交點），使微積分工具（切空間、維數論證）失效。
- Zariski（1926–40s）解決了曲線與曲面的奇點解消（特徵 0）；**三維以上**無人能解。
- Jung（1908）、Abhyankar（1956）有部分結果；蘇聯學派（Bogomolov 之後的工具）亦未突破。
- 疑問成形：**是否存在一個「正則」程序，把任意維數、特徵 0 的代數簇化為光滑的雙有理等價簇？**

## 線索與推理 -- 數學式、程式、理論

### 線索一：代數簇的奇點
奇點的判別：在點 $P$ 處，局部環 $\mathcal{O}_{X,P}$ 不是正則局部環，即

$$\dim \mathfrak{m}_P / \mathfrak{m}_P^2 \neq \dim \mathcal{O}_{X,P}$$

（切空間維數大於簇維數）。經典例子：尖點曲線 $y^2 = x^3$ 在原點處有一個尖點（cusp）——原點處切空間是整個平面（維數 2），但曲線維數只有 1。

### 線索二：雙有理變換與 blow-up
**Blow-up（爆脹）**：把一點 $P \in X$ 「放大」成整個射影空間 $\mathbb{P}^{n-1}$（該點所有切方向的集合）：

$$Bl_P X = \overline{\{(Q, \ell) : Q \in X \setminus P,\ \ell \text{ 為過 } Q \text{ 且過 } P \text{ 的直線}\}} \subset X \times \mathbb{P}^{n-1}$$

映射 $\pi: Bl_P X \to X$ 是雙有理的（同構於 $X \setminus P$，且 $X$ 與 $Bl_P X$ 的函數域相同）。爆脹在原點拉出一條**例外除子** $E = \mathbb{P}^{n-1}$，把奇點「攤開」到除子上；反覆爆脹 + 嚴格變換（strict transform），可望消除奇點。

### 線索三：奇點解消定理（1964）
**Hironaka 定理**：設 $k$ 為特徵 0 域，$X$ 為 $k$ 上任意代數簇。則存在 $X'$ 光滑，且存在一列閉嵌入

$$X' = X_n \xhookrightarrow{\pi_n} X_{n-1} \xhookrightarrow{} \cdots \xhookrightarrow{\pi_1} X_0 = X$$

每個 $\pi_i$ 是沿光滑中心（不在光滑軌跡上）的 blow-up，且 $\pi: X' \to X$ 是真（proper）雙有理映射，$\pi^{-1}(X_{\text{sing}})$ 是簡單法交交叉除子。

**核心發明——不變量 $\nu$ 與遞降策略**：對奇點 $P$ 定義**階數（order）** $\nu_P(f) = $ 局部方程 $f$ 在 $P$ 的 Taylor 展開首非零項次數。Hironaka 的策略：
1. 構造上半連續函數 $P \mapsto \nu_P(f)$，在奇點處極大；
2. 每次沿「最大階點集」的 blow-up 後，證明 $\nu$ **嚴格不增**，且不會永久停在 $>0$；
3. 歸納地 $\max \nu \to 0$ ⇒ 簇變光滑。

這個「測量—吹脹—監控不變量」的架構，被後人稱為 **Hironaka 遊戲**，其證明長達 200+ 頁（*Annals of Math.* 1964），數十年間被 Bierstone–Milman、Encinas–Villamayar 等大幅簡化，如今有構造性演算法（可程式化！）。特徵 $p > 0$ 的情形至今仍是懸案（僅 $n \le 3$，由 Abhyankar 解決）。

### 程式碼：Python sympy 畫出奇點曲線 $y^2 = x^3$（尖點）並演示 blow-up 概念

```python
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# 1) 尖點曲線 y^2 = x^3：奇點分析
x, y, t = sp.symbols('x y t')
f = y**2 - x**3

# 參數化：x = t^2, y = t^3（尖點在 t=0 處）
x_t, y_t = t**2, t**3
print("參數化代入 f =", sp.expand(f.subs({x: x_t, y: y_t})))  # 0

# 奇點判別：梯度在原點為零
fx, fy = sp.diff(f, x), sp.diff(f, y)
print("grad f 在原點:", fx.subs({x: 0, y: 0}), fy.subs({x: 0, y: 0}))  # (0,0) => 奇點

# 2) blow-up 概念演示：把 (x,y) 換成 x = u, y = u*v
#    （在原點拉出例外除子 u = 0，v 是切方向的座標）
u, v = sp.symbols('u v')
f_blown = sp.expand(f.subs({x: u, y: u * v}))
print("blow-up 後：", f_blown)                     # u^2 * (v^2 - u)
print("嚴格變換（除掉 u^2）：", sp.factor(f_blown / u**2))  # v^2 - u

# 嚴格變換 v^2 = u 在 u=0 處：grad = (1, 0) 非零 => 光滑！
# 一次 blow-up 就解消了這個尖點——尖點被「攤開」成例外除子上的兩個方向

# 3) 畫圖：原曲線與 blow-up 後的嚴格變換
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
tt = np.linspace(-1.5, 1.5, 400)
ax1.plot(tt**2, tt**3, 'b-')
ax1.set_title(r"cusp: $y^2 = x^3$ (奇點在原點)")
ax1.axhline(0, color='gray', lw=0.5); ax1.axvline(0, color='gray', lw=0.5)
ax1.scatter([0], [0], color='red', zorder=5, label="奇點")
ax1.legend(); ax1.set_aspect('equal')

uu = np.linspace(0, 1.5, 200)
ax2.plot(uu, np.sqrt(uu), 'g-', label=r"$v = +\sqrt{u}$")
ax2.plot(uu, -np.sqrt(uu), 'g-')
ax2.axhline(0, color='gray', lw=0.5); ax2.axvline(0, color='gray', lw=0.5)
ax2.scatter([0], [0], color='orange', zorder=5, label="例外除子 $E$")
ax2.set_title(r"blow-up 後: $v^2 = u$ (光滑)")
ax2.legend(); ax2.set_aspect('equal')
plt.tight_layout(); plt.savefig("hironaka_blowup.png", dpi=120)
print("已儲存圖 hironaka_blowup.png")
```

### 線索四：廣中平祐（1931–2022，2010 菲爾茲獎？）
廣中平祐生於 1931 年（山口縣），哈佛大學博士（師從 Zariski），1964 年證明特徵 0 奇點解消。**訂正**：廣中於 **1970 年**獲**菲爾茲獎**，是**首位日本菲爾茲得主**（2010 年他獲頒的是日本文化勳章與多項榮譽）。他晚年致力於沖繩科學技術大學院大學（OIST）的創建，2022 年逝世。

## 結案 -- 後果與影響
- 特徵 0 的代數幾何從此**原則上可局部化到光滑情形**：一切維數論證（維數、切空間、微分形式）皆可先用解消再套微積分。
- 補全 **Grothendieck 綱領**：Hironaka 的 proper 雙有理映射是導出範疇、相對對偶化、消沒理論（Kawamata–Viehwag）的技術基礎；奇點解消也是極小模型綱領（MMP，Mori 1990 菲爾茲獎）的前置工具。
- 啟發**構造性代數**：Bierstone–Milman（1997）的演算法化證明，使解消可寫成程式。
- 特徵 $p > 0$：$n \ge 4$ 至今未解——Hironaka 遊戲仍是活躍研究前沿（相關工具：$F$-奇異性、de Jong 的交變（2000））。

## 關鍵人物與文獻
- **Oscar Zariski**：曲線/曲面解消（1926–1940s）；廣中的博士導師。
- **Heisuke Hironaka（廣中平祐）**：*On the resolution of singularities of algebraic varieties over fields of characteristic zero*（Annals of Math. 79, 1964）；1970 年菲爾茲獎（首位日本得主）。
- **Shreeram Abhyankar**：特徵 $p$、$n \le 3$ 的解消（1956–66）。
- **Edward Bierstone & Pierre Milman**：構造性解消演算法（1997）。
- **Aise Johan de Jong**：交變（alteration）方法，特徵 $p$ 的替代路線（1996）。
