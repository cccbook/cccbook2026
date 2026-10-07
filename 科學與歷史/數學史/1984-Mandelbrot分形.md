# 1984 - Mandelbrot 分形

## 案件摘要
1975 年，Benoît Mandelbrot 在 IBM 發明「**分形**」（fractal）一詞；1980 年他發現 **Mandelbrot 集合**：

$$z_{n+1} = z_n^2 + c, \quad z_0 = 0 \quad \text{（收斂的 } c \text{ 集合）}$$

——**史上最美麗的數學圖形**（一個簡單的迭代，無限的複雜）。1982 年《大自然的分形幾何》（The Fractal Geometry of Nature）出版：**雲不是球、山不是錐、海岸線不是圓**——自然界是分形（自相似、無限細節、非整數維度）。**歐幾里得以來的「平滑幾何」被補充**——Weierstrass 函數（1872，見 `1872-Weierstrass分析嚴格化.md`）的「怪物」成為自然界的常態。**IBM 的電腦圖學讓分形「被看見」**——數學與視覺的革命。

## 前因 -- 為什麼會有這個案子
**兩千年的平滑幾何**：歐幾里得（見 `-0300-Euclid幾何原本.md`）以來，幾何研究**平滑的形狀**（直線、圓、多項式曲線）——**自然界卻不平滑**：

- **海岸線問題**（Richardson 1961）：英國海岸線的長度**隨測量尺度變化**——比例尺越小，長度越長（無限長！）——**「長度」這個概念失效**
- **Weierstrass 函數**（1872，見 `1872-Weierstrass分析嚴格化.md`）：處處連續處處不可微——**被視為「怪物」**
- **布朗運動**（1905，見 `../隨機算法/1905-布朗運動.md`）：路徑處處不可微——**物理的「怪物」**
- **Julia 集**（Julia 1918、Fatou 1919）：複迭代的集——**數學家知道，無人「看見」**（沒有電腦圖學）

**Mandelbrot 的環境**：波蘭出生、法國長大（叔父 Szolem 是數學家）、1958 年加入 **IBM**（Watson 研究中心）——**IBM 的自由研究 + 電腦圖學**——分形的溫床。

## 線索與推理 -- 數學式、程式、理論

### 分形維度
**海岸線的啟示**：Richardson（1961）的數據——海岸線長度 $L(\epsilon)$ 隨尺度 $\epsilon$：

$$L(\epsilon) \propto \epsilon^{1-D} \quad \text{（} D \text{ 是分形維度，} D > 1\text{）}$$

**英國海岸線**：$D \approx 1.25$——**非整數維度**！**「長度」無限，「維度」是分數**。

**分形維度的定義**（Hausdorff 1918）：

$$D = \frac{\ln N}{\ln (1/\epsilon)} \quad \text{（覆蓋數與尺度的對數比）}$$

- 直線：$D = 1$（尺度減半，覆蓋數 ×2）
- 正方形：$D = 2$（×4）
- **海岸線**：$D = 1.25$（×2.38）——**介於線與面之間**！

### Mandelbrot 集合
**1980 年的發現**：迭代

$$z_{n+1} = z_n^2 + c, \quad z_0 = 0$$

**Mandelbrot 集合** $M$ = 使迭代**有界**的 $c$ 集合——電腦圖學畫出後：

**無限的複雜**：邊界**無限精細**（放大任何部分都有新結構）、**自相似**（部分像整體但不完全相同）、**被稱為「史上最美麗的數學圖形」**。

**Julia 集的表兄弟**：每個 $c$ 對應一個 Julia 集 $J_c$（迭代的「爆炸邊界」）——$c \in M$ ⟺ $J_c$ 連通——**Mandelbrot 集是 Julia 集的「地圖」**。

### 程式碼：Mandelbrot 集合與分形維度

```python
def mandelbrot(c, max_iter=100):
    """判斷 c 是否在 Mandelbrot 集合中（迭代 z² + c）"""
    z = 0
    for i in range(max_iter):
        z = z*z + c
        if abs(z) > 2:
            return i                      # 逃逸時間
    return max_iter                       # 有界 → 在集合中

# 邊界的逃逸時間圖（ASCII 畫出「被看見」的分形）
for im in [i * 0.1 - 1.0 for i in range(21)]:
    row = ""
    for re in [i * 0.05 - 2.0 for i in range(70)]:
        it = mandelbrot(complex(re, im), max_iter=30)
        row += " " if it == 30 else (".:-=+*#%@"[min(it // 4, 7)])
    print(row)
# 史上最美麗的數學圖形——IBM 電腦圖學的功勞

# 分形維度：海岸線與 Koch 曲線
def koch_snowflake_length(iterations, side=1.0):
    """Koch 雪花：每迭代邊長 ×4/3——無限長！"""
    return 3 * side * (4/3)**iterations

print(f"\nKoch 雪花：{[f'{koch_snowflake_length(n):.2f}' for n in [0, 2, 4, 10]]}")
# 邊長趨於無窮——「長度」失效，分形維度 D = ln4/ln3 ≈ 1.26

print(f"Koch 維度 = {math.log(4)/math.log(3):.4f}（介於線與面之間）")
print(f"英國海岸線維度 ≈ 1.25（Richardson 1961 的數據）")
```

### 自然的分形幾何
**Mandelbrot 的帝國**：
- **金融**：棉花價格的波動（Mandelbrot 1963 的早期工作）——**市場是分形的**（厚尾分佈）
- **物理**：湍流、臨界現象（自相似性）——**重整化群**（Wilson 1971，見 `../量子力學/README.md`）的分形
- **生物**：肺的支氣管、血管的分支、樹的形狀——**生長是分形**（最佳填充與運輸）
- **電腦圖學**：地形生成、雲、火焰——**遊戲與電影的分形演算法**

**偵探筆記**：Mandelbrot 的推理是「**被看見**」——Julia 集與 Weierstrass 函數（1872 的「怪物」）早已存在，**IBM 的電腦圖學讓它們被看見**——**視覺化催生理解**。與 Galois 遺稿（1846 出版）、Koch 的曲線（1904）同源：**數學的「怪物」常在科技進步後成為主角**——怪物與科技的對話。

## 結案 -- 後果與影響
- **分形幾何的誕生**：自相似、非整數維度——**歐幾里得以來幾何的補充**（怪物成為常態）。
- **Mandelbrot 集合**：史上最美麗的數學圖形——**數學與藝術的交匯**（郵票、展覽、流行文化）。
- **混沌理論的連結**：Mandelbrot 集的邊界 = 混沌的邊界（Feigenbaum 1975 的倍增週期）——**非線性科學的黃金年代**（Lorenz 的吸引子 1963、 logistic 映射）。
- **金融的分形**：市場波動的厚尾——**風險管理的革命**（Black–Scholes 的修正）。
- **電腦圖學的功勞**：IBM 的自由研究——**企業實驗室的黃金年代**（Bell Labs、PARC 的傳統）。
- **海岸線問題**：Richardson 的數據 → 分形維度——**「長度」概念的極限**（測量的尺度依賴）。

## 關鍵人物與文獻
- **Benoît Mandelbrot**（1924–2010）：分形 (1975)、Mandelbrot 集合 (1980)、The Fractal Geometry of Nature (1982)；IBM Watson 研究中心、Yale
- **Karl Weierstrass**（1815–1897）：處處不可微的函數（1872）——分形的祖先（見 `1872-Weierstrass分析嚴格化.md`）
- **Gaston Julia**（1893–1978）：Julia 集 (1918)——Mandelbrot 集的表兄弟
- **Lewis Fry Richardson**（1881–1953）：海岸線數據 (1961)——分形維度的啟示
- **Mitchell Feigenbaum**（1944–2019）：倍增週期 (1975)——混沌的普適常數
- **Edward Lorenz**（1917–2008）：蝴蝶效應 (1963)——混沌理論的起點
- 交叉參照：`1872-Weierstrass分析嚴格化.md`、`1874-Cantor集合論.md`、`../隨機算法/1905-布朗運動.md`、`../量子力學/README.md`、`../密碼學/2022-LLM時代密碼學.md`
