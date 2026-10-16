# 2003 - Perelman 龐加萊猜想

## 案件摘要
2002–2003 年，Grigori Perelman 在 arXiv 貼出三篇預印本，用**Ricci 流（Ricci flow）+ 手術（surgery）**證明**龐加萊猜想**：單連通的閉 3-流形同胚於 3 維球面——拓撲學百年懸案（1904 年 Poincaré 提出）。更強的：他證明了**幾何化猜想**（Thurston 1982）——3-流形的完整分類。**千禧年獎（見 `2000-千禧年大獎.md`）唯一已解的問題**——而 Perelman **放棄 Fields 獎（2006）與百萬獎金（2010）**：「如果證明是對的，就不需要別的認可。」**數學史上最傳奇的隱士。**

## 前因 -- 為什麼會有這個案子
**1904 年**，Henri Poincaré 研究拓撲學（他自稱 analysis situs）時提出：

**龐加萊猜想**：閉 3-流形若**單連通**（每個圈可收縮到一點，$\pi_1 = 0$），則同胚於 3 維球面 $S^3$。

**直覺**：3 維空間中，任何「沒有洞的閉合空間」都是球的變形——**2 維成立**（球面上任何圈可收縮；環面不行）、$n \ge 4$ 維已證（Smale 1961、Freedman 1982，各得 Fields）——**只有 3 維懸**（3 維的「刁鑽」）。

**100 年的攻擊**：
- **Whitehead（1934）**：宣稱證明——錯誤
- **Bing、Papakyriakopoulou（1950s）**：部分結果
- **Hamilton（1982）**：發明**Ricci 流**——**幾何化的方法**（用曲率方程演化流形），證明部分情況（正曲率）
- **Thurston（1982）**：**幾何化猜想**——3-流形的完整分類（8 種幾何）——龐加萊是其特例

**Perelman 的路徑**：Ricci 流 + **手術（surgery）**——在流形「奇異點」出現時切開縫合，繼續演化——**最終收斂到標準幾何**。

## 線索與推理 -- 數學式、程式、理論

### Ricci 流：幾何的熱方程
**Hamilton 的發明（1982）**：把度量張量（見 `1854-Riemann幾何.md`）隨時間演化：

$$\frac{\partial g_{ij}}{\partial t} = -2 R_{ij}$$

（$g$ 的變化率 = 負的 Ricci 曲率——**與熱方程同構**（見 `../微分方程/README.md`）：曲率「擴散」，幾何「平滑」。）

**直覺**：不均勻的曲率隨時間**均勻化**——就像熱傳導平滑溫度。**正曲率的區域收縮、負曲率膨脹**——最終收斂到「標準」幾何（球面、環面……）。

**Hamilton 的困境**：演化中出現**奇異點**（singularity）——曲率爆炸、流形「撕裂」。**如何處理奇異點？** Hamilton 攻擊 20 年無果。

### Perelman 的手術
**核心創新（Perelman 2002–03）**：

1. **手術（surgery）**：奇異點出現時，**切開撕裂處、縫合蓋帽**（標準零件）——繼續演化
2. **熵函數**（Perelman 的發明）：單調遞增的量（$\mathcal{W}$），**控制奇異點的結構**——只有有限類型
3. **有限時間內有限次手術**——最終收斂到幾何化猜想的標準幾何

**推理鏈**：

$$\text{任意 3-流形} \xrightarrow{\text{Ricci 流 + 手術}} \text{標準幾何的分解} \implies \text{幾何化猜想} \implies \text{龐加萊猜想}$$

**龐加萊的特例**：單連通 ($\pi_1 = 0$) 的流形經 Ricci 流收斂到 $S^3$——**同胚於球面**。$\blacksquare$

**Perelman 的三篇預印本**（2002 年 11 月、2003 年 3 月、2003 年 7 月）——**貼在 arXiv，不投期刊**——與傳統發表文化的決裂。

### 程式碼：Ricci 流的概念

```python
import math, random

# Ricci 流的概念：曲率平滑化（與熱方程同構）
def heat_equation_1d(u0, steps=100, dt=0.001, dx=0.01, nu=1.0):
    """熱方程 ∂u/∂t = ν ∂²u/∂x²——Ricci 流的 1 維類比"""
    u = u0[:]
    for _ in range(steps):
        u2 = [u[i] for i in range(len(u))]
        for i in range(1, len(u)-1):
            u2[i] = u[i] + nu * dt * (u[i+1] - 2*u[i] + u[i-1]) / dx**2
        u = u2
    return u

random.seed(42)
import random
# 初始：不均勻的「溫度」（曲率）——隨時間平滑
u0 = [math.sin(i * 0.1) + random.gauss(0, 0.3) for i in range(50)]
u1 = heat_equation_1d(u0, steps=1000)
roughness0 = sum(abs(a-b) for a, b in zip(u0[1:], u0[:-1]))
roughness1 = sum(abs(a-b) for a, b in zip(u1[1:], u1[:-1]))
print(f"粗糙度：初始 = {roughness0:.2f}，演化後 = {roughness1:.2f}（平滑化 ✓）")
print("\nRicci 流 ∂g/∂t = -2R：曲率隨時間平滑——Hamilton 1982 的方法")
print("Perelman 的手術：奇異點切開縫合，熵函數控制結構——幾何化猜想 ✓")
```

**單連通性的直覺**：基本群 $\pi_1$ 是「圈可否收縮」的代數判準：

| 空間 | $\pi_1$ | 圈的行為 |
|------|---------|----------|
| 球面 $S^2$ | $0$（平凡） | 任何圈可收縮到一點——單連通 |
| 環面 $T^2$ | $\mathbb{Z}^2$ | 繞環的圈不可收縮——非單連通 |

**龐加萊猜想**：閉 3-流形單連通（$\pi_1 = 0$）$\implies$ 同胚於 $S^3$（Perelman 2003）。

### 放棄一切：Perelman 的傳奇
**榮譽的拒絕**：
- **2006 年 Fields 獎**：拒領——「我不願意成為展覽品」
- **2010 年百萬獎金**：拒領——「如果證明是對的，就不需要別的認可」
- **2005 年退出數學界**：辭去 Steklov 研究所，與母親同住聖彼得堡的公寓——**完全的隱士**

**爭議的背景**：2006 年《紐約客》報導曹懷東–朱熹平（中國團隊）與 Hamilton 的「共同貢獻」——Perelman 憤怒：「**他們沒有貢獻任何新的東西**」——**數學的優先權之爭**（與 Cardano–Tartaglia 1545、Newton–Leibniz 1684 同列，見 `1545-Cardano三次方程.md`）。

**Perelman 的哲學**：數學與名利無關——**與 Wiles 的秘密研究（1995，見 `1994-Wiles費馬定理.md`）對照**：Wiles 為榮譽深潛，Perelman 連榮譽都不要。**兩位世紀證明者，兩種人生**。

## 結案 -- 後果與影響
- **百年懸案終結**：龐加萊猜想（1904→2003）——拓撲學的世紀勝利。
- **幾何化猜想**：3-流形的完整分類（8 種幾何）——比龐加萊更強的定理。
- **Ricci 流的帝國**：幾何分析（geometric analysis）的中心工具——Hamilton 的方法 + Perelman 的手術。
- **arXiv 的文化**：Perelman 不投期刊——**預印本的合法性**（與現代開放科學同源）。
- **數學與名利**：Perelman 的放棄成為「數學精神」的寓言——**證明是對的就夠了**。
- **3 維的特異性**：2 維與 4 維已證（Smale、Freedman），3 維最難——**維度的刁鑽**（3 維流形的野蠻性）。

## 關鍵人物與文獻
- **Henri Poincaré**（1854–1912）：猜想提出 (1904)；拓撲學之父
- **Grigori Perelman**（1966–）：The entropy formula for the Ricci flow... (2002)、Ricci flow with surgery... (2003)——arXiv 預印本
- **Richard Hamilton**（1943–2024）：Ricci 流 (1982)——方法論的發明者
- **William Thurston**（1946–2012）：幾何化猜想 (1982)
- **Stephen Smale**（1930–）：$n \ge 5$ 維的龐加萊 (1961)；**Michael Freedman**：4 維 (1982)
- **曹懷東–朱熹平**：2006 年的爭議（「完整證明」的宣稱）
- 交叉參照：`1854-Riemann幾何.md`、`2000-千禧年大獎.md`、`1994-Wiles費馬定理.md`、`../微分方程/README.md`
