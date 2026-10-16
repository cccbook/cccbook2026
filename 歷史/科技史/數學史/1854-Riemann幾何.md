# 1854 - 黎曼幾何

## 案件摘要
1854 年 6 月 10 日，27 歲的 Bernhard Riemann 在 Göttingen 發表就職演講《論作為幾何學基礎的假設》（Über die Hypothesen, welche der Geometrie zu Grunde liegen）：提出**黎曼幾何**——拋棄歐氏的「平坦空間」假設，定義**任意維度、任意曲率的空間**（用度量張量 $g_{ij}$）。**空間本身可以是彎的**——60 年後 Einstein 的廣義相對論（1915）正是用它描述引力。**幾何從「空間的科學」變成「任意流形的科學」**，Gauss（見 `1799-Gauss代數基本定理.md`）的學生完成了老師未發表的夢想。

## 前因 -- 為什麼會有這個案子
**兩千年的公設**：歐幾里得第五公設（平行公設，見 `-0300-Euclid幾何原本.md`）——「過直線外一點至多一條平行線」。**兩千年的攻擊**：

- **Gauss（1820s，未發表）**：發現**非歐幾何**（否定第五公設的自洽幾何）——但**不敢發表**（怕「愚昧的鼓噪」，Beati paenultima 的爭議）
- **Lobachevsky（1829）**：發表雙曲幾何（負曲率）——被視為異端
- **Bolyai（1832）**：發表「絕對幾何」——Gauss 回信「讚美你等同讚美我自己」（Bolyai 暴怒，此後不再發表）

**Gauss 的曲面論（1827）**：《曲面的一般研究》——**三維空間中的曲面**（二維流形）的曲率理論：高斯曲率 $K$、**Theorema Egregium**（絕妙定理：曲率是內在的，不依賴嵌入）。

**Riemann 的問題（Gauss 指定的題目三選一）**：**能否推廣到任意維度、任意曲率的空間？**——不只是二維曲面，是 $n$ 維流形。

## 線索與推理 -- 數學式、程式、理論

### 度量張量：空間的DNA
**Riemann 的核心想法**：空間的幾何完全由**度量張量**（metric tensor）決定——每點附近，兩個無窮小位移 $dx^i, dx^j$ 的距離：

$$ds^2 = \sum_{i,j} g_{ij}(x)\, dx^i dx^j$$

- **歐氏幾何**：$g_{ij} = \delta_{ij}$（單位矩陣）——平坦，畢氏定理
- **球面幾何**：$g_{ij}$ 隨位置變化——正曲率，三角形內角和 > 180°
- **雙曲幾何**：負曲率——三角形內角和 < 180°
- **任意流形**：$g_{ij}$ 是任意光滑函數——**空間的幾何是「場」，不是「背景」**

**革命性**：空間不再有「預設的形狀」——**幾何是度量張量的函數**，每個 $g_{ij}$ 定義一個不同的幾何世界。**維度也自由**：2、3、4、$n$ 維——純代數的推廣（與 Descartes 座標的算術化同源，見 `1637-Descartes解析幾何.md`）。

### 曲率：空間的彎曲
**曲率的定義（Riemann）**：由度量張量的二階導數構造：

$$R_{ijkl} = \frac{\partial^2 g_{ij}}{\partial x^k \partial x^l} + \dots \quad \text{（Riemann 曲率張量）}$$

- $R = 0$：平坦（歐氏）
- $R > 0$：正曲率（球面——三角形內角和超過 180°）
- $R < 0$：負曲率（雙曲——內角和不足）

**高斯曲率的推廣**：Gauss 的二維曲率 $K$ 推廣為 $n$ 維的 Riemann 張量——**Theorema Egregium 的 $n$ 維版**（曲率是內在性質，不依賴嵌入空間）。

### 程式碼：曲率與測地線

```python
import math

# 球面上的三角形內角和（正曲率）
def sphere_angle_sum(R, area):
    """球面三角形：內角和 = 180° + (面積/R²) 的弧度轉換"""
    return math.pi + area / R**2           # 弧度

R = 1.0
# 概念：半徑 1 的球面上，面積 0.1 的三角形
s = sphere_angle_sum(R, 0.1)
print(f"球面三角形內角和 = {math.degrees(s):.2f}° > 180°（正曲率）")

# 歐氏：180°
print(f"歐氏（R→∞）：{math.degrees(sphere_angle_sum(1e9, 0.1)):.4f}° ≈ 180° ✓")

# 測地線（geodesic）：曲面上「最直的路」
def geodesic_sphere(phi0, theta0, phi1, theta1, R=1.0):
    """球面兩點的最短路（大圓弧）——半正矢公式"""
    dphi, dtheta = phi1 - phi0, theta1 - theta0
    a = math.sin(dphi/2)**2 + math.cos(phi0)*math.cos(phi1)*math.sin(dtheta/2)**2
    return 2 * R * math.asin(math.sqrt(a))

# 台北到東京的距離（大圓弧——地球曲率的幾何）
d = geodesic_sphere(math.radians(25.0), math.radians(121.5),
                    math.radians(35.7), math.radians(139.7), R=6371)
print(f"台北–東京的大圓距離 ≈ {d:.0f} km（黎曼幾何的實際應用）")
```

### Einstein 的接棒（1915）
**60 年後**：Einstein 的廣義相對論——**引力 = 時空的曲率**：

$$G_{\mu\nu} = \frac{8\pi G}{c^4} T_{\mu\nu}$$

（Einstein 張量 = 能量動量張量——**物質決定時空如何彎曲，時空決定物質如何運動**，Wheeler 的名言。）

**推理鏈**：
- 黎曼（1854）：任意曲率的空間
- Ricci（1880s）：Ricci 張量（曲率的收縮）
- Einstein（1912–15）：用 Ricci 張量描述引力——**黎曼幾何是廣義相對論的數學語言**

Einstein 自己說：「如果沒有黎曼的幾何，我無法建立廣義相對論。」

### 黎曼假設的伏筆
**同一個人**：Riemann 1859 年的數論論文提出**黎曼假設**（ζ 函數的零點，見 `1734-Euler巴塞爾問題.md`）——**幾何與數論的雙棲天才**。黎曼 40 歲死於肺結核——與 Abel（26 歲）、Galois（20 歲）同列早夭天才。

## 結案 -- 後果與影響
- **廣義相對論**：黎曼幾何是引力的數學語言——黑洞、宇宙學、GPS 的相對論修正（見 `../相對論/README.md`）。
- **幾何的革命**：空間是「場」（度量張量），不是「背景」——流形、拓撲學（Poincaré 1895，見 `2003-Perelman龐加萊猜想.md`）。
- **非歐幾何的統一**：Gauss、Lobachevsky、Bolyai 的三個版本被黎曼的框架統一（曲率的符號決定幾何）。
- **內在幾何**：Theorema Egregium 的 $n$ 維版——曲率不依賴嵌入，**空間自己知道自己的形狀**。
- **數學與物理的融合**：黎曼幾何 → Einstein → 弦論（Calabi–Yau 流形）——**幾何是物理的語言**。

## 關鍵人物與文獻
- **Bernhard Riemann**（1826–1866）：Über die Hypothesen... (1854 就職演講，1868 出版)；黎曼假設 (1859)
- **Carl Friedrich Gauss**（1777–1855）：曲面論 (1827)、Theorema Egregium、非歐幾何（未發表）
- **Lobachevsky**（1792–1856）：雙曲幾何 (1829)
- **János Bolyai**（1802–1860）：絕對幾何 (1832)
- **Gregorio Ricci-Curbastro**（1853–1925）：Ricci 張量——Einstein 的工具
- **Albert Einstein**（1879–1955）：廣義相對論 (1915)
- 交叉參照：`-0300-Euclid幾何原本.md`、`1799-Gauss代數基本定理.md`、`1637-Descartes解析幾何.md`、`2003-Perelman龐加萊猜想.md`、`../相對論/README.md`
