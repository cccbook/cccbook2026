# 1851 — Riemann 複變函數基礎

## 案件摘要
1851 年 11 月，25 歲的 Georg Friedrich Bernhard Riemann 在 Göttingen 大學提交博士論文《Grundlagen für eine allgemeine Theorie der Funktionen einer veränderlichen complexen Größe》（單複變函數一般理論的基礎）。這篇薄薄的論文做了一件前人沒想過的事：不把解析函數當成「幂級數」或「積分的產物」，而是當成**幾何對象**——解析函數的本質是**保形映射**。同一篇論文中，Riemann 球面 $\hat{\mathbb{C}}$ 首次登場，Riemann 映射定理的構想被埋下伏筆。Gauss 審閱後評價：這是一篇「重大而困難的任務」的傑作——而這只是 Riemann 偵探生涯的第一案。

## 前因 -- 為什麼會有這個案子
- 1825 年起，Cauchy 用積分與導數定義複解析函數：$f'(z_0)$ 存在且連續、Cauchy–Riemann 方程成立。這是「分析的」路線。
- Gauss 是 Riemann 的指導教授，他早已私下持有複平面（用 $a+bi$ 表示複數的幾何圖像）的想法，但幾乎不發表。Riemann 從 Gauss 那裡繼承了「複數必須用幾何看待」的眼光。
- Dirichlet 是 Riemann 的另一位重要導師：Riemann 1847 年到柏林聽 Dirichlet 的課，學到了**Dirichlet 原理**（調和函數由邊值唯一決定，可用極小化能量泛函求解）——這成為 1851 論文的關鍵工具。
- 當時的懸案：解析函數到底是什麼？為什麼複可微這麼強（複可微一次就無窮次可微）？實函數論完全沒有這種現象。Riemann 認為答案藏在**幾何**裡：複可微 = 保形，這是一個幾何條件。

## 線索與推理 -- 數學式、程式、理論

### 線索一：解析函數 = 保形映射
Riemann 的出發點：設 $w = f(z)$ 是複平面到複平面的映射，把 $w$ 的實部與虛部寫成 $u(x,y), v(x,y)$。若 $f$ 複可微，則 Cauchy–Riemann 方程成立：
$$\frac{\partial u}{\partial x} = \frac{\partial v}{\partial y}, \qquad \frac{\partial u}{\partial y} = -\frac{\partial v}{\partial x}$$
Riemann 指出這正是**位勢理論的條件**：$u$ 與 $v$ 都是調和函數（$\nabla^2 u = \nabla^2 v = 0$），而且互為**共軛調和**。幾何上，$f'$ 在每點的作用是一個「旋轉＋均勻縮放」的複數乘法：
$$f'(z_0)\,dz = |f'(z_0)| e^{i\arg f'(z_0)}\, dz$$
這意味著映射在每一點把所有方向的切向量**旋轉同一角度、放大同一倍率**——角度與取向被保住，這就是**保形（conformal）**。Riemann 於是宣判：**解析函數就是保形映射**，複可微性的強大力量來自這個幾何本質。

### 線索二：Riemann 球面——把無窮遠點納入版圖
1851 論文中首次出現（更早 Gauss 也有想法）的圖像：把複平面 $\mathbb{C}$ 經**球極投影**（stereographic projection）貼到一顆去掉北極的球面上。北極 $N$ 對應「無窮遠點 $\infty$」，加上它之後得到 **Riemann 球面**：
$$\hat{\mathbb{C}} = \mathbb{C} \cup \{\infty\}$$
球極投影公式（球面參數 $(\theta, \phi)$，北極投影到平面）：對單位球上一點 $(X, Y, Z)$（$Z \ne 1$），
$$(x, y) = \left(\frac{X}{1-Z}, \frac{Y}{1-Z}\right), \qquad \text{逆：}\; (X,Y,Z) = \left(\frac{2x}{x^2+y^2+1}, \frac{2y}{x^2+y^2+1}, \frac{x^2+y^2-1}{x^2+y^2+1}\right)$$
球極投影的偵探級重要性：它是**保形的**、把球面上的圓映成平面上的圓或直線。有了 $\hat{\mathbb{C}}$，Möbius 變換
$$f(z) = \frac{az+b}{cz+d}, \qquad ad-bc \ne 0$$
就成了 Riemann 球面到自身的旋轉式映射，$\infty$ 不再是「例外」而是正常成員。

### 線索三：Dirichlet 原理與 Riemann 映射定理的構想
Riemann 用 Dirichlet 原理證明：單連通區域上的調和函數由邊界值唯一決定。以此為工具，他在論文末尾提出後世稱為 **Riemann 映射定理**的構想：
> 任何兩個單連通、邊界至少含兩點的區域之間，存在保形雙射。

特別地，任何這樣的區域都保形等價於單位圓盤 $\mathbb{D}$。這在當時**沒有完整嚴格證明**（Dirichlet 原理本身有漏洞，Weierstrass 1870 年指出的），直到 1900 年 Hilbert 修補原理、Koebe 與 Poincaré 1907–1912 年給出完整證明，才真正結案。但構想的提出本身就是偵破——幾何函數論的大門被 Riemann 推開了。

### 程式碼範例：Riemann 球面的 numpy 視覺化
```python
import numpy as np
import matplotlib.pyplot as plt

# 把複平面的格線經球極投影貼到 Riemann 球面上
n = 40
x = np.linspace(-2, 2, n)
y = np.linspace(-2, 2, n)
X, Y = np.meshgrid(x, y)
R2 = X**2 + Y**2

# 逆球極投影：平面 (x,y) -> 單位球 (Xs, Ys, Zs)
denom = R2 + 1
Xs, Ys, Zs = 2*X/denom, 2*Y/denom, (R2 - 1)/denom

fig = plt.figure(figsize=(12, 5))
ax = fig.add_subplot(121, projection='3d')
# 畫水平線與垂直線的像（格線）
step = 4
for i in range(0, n, step):
    ax.plot(Xs[i,:], Ys[i,:], Zs[i,:], 'b', lw=0.6)
    ax.plot(Xs[:,i], Ys[:,i], Zs[:,i], 'r', lw=0.6)
ax.set_title("Riemann sphere: images of grid lines")
ax.set_xlabel("X"); ax.set_ylabel("Y"); ax.set_zlabel("Z")

# 檢查球極投影是保形的：在平面上取兩條正交的短線段，投影後夾角仍應為 90 度
z0 = np.array([0.5, 0.3]); eps = 1e-4
d1 = np.array([eps, 0]); d2 = np.array([0, eps])   # 正交切向量
def to_sphere(p, d):
    # 投影的微分（數值）：p + d 投影減 p 投影
    def proj(p):
        r2 = p[0]**2 + p[1]**2
        return np.array([2*p[0], 2*p[1], r2 - 1])/(r2 + 1)
    return (proj(p + d) - proj(p - d)) / (2*np.linalg.norm(d))
v1, v2 = to_sphere(z0, d1), to_sphere(z0, d2)
cosang = v1 @ v2 / (np.linalg.norm(v1)*np.linalg.norm(v2))
print("投影後夾角 cos =", cosang, "（應接近 0，即 90 度保形）")

ax2 = fig.add_subplot(122)
th = np.linspace(0, 2*np.pi, 200)
ax2.plot(np.cos(th), np.sin(th), 'k')   # 單位圓 = 球面赤道的投影
ax2.set_aspect('equal'); ax2.set_title("Unit disk: canonical conformal domain")
plt.show()
```

數值輸出中投影後兩個正交切向量的夾角餘弦接近 0，直接驗證了球極投影的保形性——Riemann 球面不只是圖像，它是保形幾何的舞台。

## 結案 -- 後果與影響
- **幾何函數論誕生**：解析函數 = 保形映射的世界觀，與 Weierstrass 的冪級數路線、Cauchy 的積分路線三足鼎立，成為複分析三大路線之一。
- **Riemann 球面成為標準語言**：$\hat{\mathbb{C}}$ 上處理有理函數、$\infty$ 處的行為（Laurent 展開在 $\infty$ 的版本）從此無障礙。
- **Riemann 映射定理**：1907 年由 Koebe、Poincaré 完整證明，成為幾何函數論的基石；保形映射在流體力學（機翼繞流，Joukowski 變換）、電磁學中大量應用。
- **Dirichlet 原理的爭議**：Weierstrass 1870 年的批評反而刺激了變分法的嚴格化，Hilbert 1900 年的修補是 20 世紀分析的先聲。
- 這篇論文為 Riemann 1857 年的曲面理論與 1859 年的 ζ 函數論文鋪路——同一顆偵探腦袋連破三案。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Bernhard Riemann | 1851 博士論文作者，幾何函數論開創者 |
| Carl Friedrich Gauss | 指導教授、論文審閱人 |
| Peter Gustav Dirichlet | 柏林導師，Dirichlet 原理提供工具 |
| Karl Weierstrass | 批評 Dirichlet 原理，推動嚴格化 |
| Paul Koebe / Henri Poincaré | 1907–1912 完成映射定理證明 |

- B. Riemann, *Grundlagen für eine allgemeine Theorie der Funktionen einer veränderlichen complexen Größe*, Göttingen 博士論文 (1851)；收錄於 *Gesammelte Mathematische Werke*。
- P. G. L. Dirichlet, *Vorlesungen über die im umgekehrten Verhältniss...* 等講義（1846–，Riemann 聽課筆記）。
- D. Hilbert, «Über das Dirichletsche Prinzip», Math. Ann. (1900/1905)。
