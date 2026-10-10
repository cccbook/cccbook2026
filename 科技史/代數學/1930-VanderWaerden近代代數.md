# 1930 - van der Waerden《Moderne Algebra》出版

## 案件摘要
1930 年，荷蘭數學家 Bartel Leendert van der Waerden 出版《Moderne Algebra》（近代代數）第一卷，1931 年出版第二卷——史上第一本以抽象公理化方法系統撰寫的代數教科書。偵探的結論：這樁案子把 Noether 與 Artin 的課堂筆記，鑄造成席捲全世界的「結構主義教科書」。

## 前因 -- 為什麼會有這個案子
- **代數教材的舊世界**：20 世紀初的代數教科書（如 Weber《Lehrbuch der Algebra》、Dickson 的著作）仍以方程式論、行列式與具體計算為主軸，抽象結構散落各處而無統一框架。
- **Göttingen 的寶藏**：Emmy Noether 在 Göttingen 的講授（環、理想、模）與 Emmy Noether/Emil Artin 在 Hamburg 的課程（群論、超複數），蘊含全新的抽象觀點，但只存在於課堂與講義中。
- **van der Waerden 的線索**：van der Waerden 1924–25 年先後到 Göttingen 聽 Noether 的課、到 Hamburg 聽 Artin 的課，驚覺：「這些課程的內容如果能系統寫下來，就是一本全新的代數書。」

## 線索與推理 -- 數學式、程式、理論

### 線索一：受 Noether 與 Artin 課程啟發
van der Waerden 在序言中直言：
> 「本書的目標是引入代數的概念……其內容大部分取自 Noether 與 Artin 的課程。」
（《Moderne Algebra》第一版前言）

他的方法：不按「研究對象的歷史」組織，而按**公理結構**組織——先給定義，再證定理，最後給例子。這正是偵探辦案的「先立規則、再查線索」。

### 線索二：第一本抽象代數教科書——兩冊架構
**第一卷（1930）**：
- 集合與映射的基礎語言；
- **群論**：公理、子群、陪集、正規子群、商群、同態定理 $G/\ker\varphi \cong \operatorname{im}\varphi$；
- **環與理想**：環公理、理想、商環、多項式環、Noether 環與唯一分解；
- **域論**：域擴張、Galois 理論（以 Artin 的觀點重述）。

**第二卷（1931）**：
- **線性代數**：向量空間公理、線性變換、矩陣、雙線性型；
- **模論**：交換環上的模、張量積的早期形式；
- **超複數系**（結合代數）：Wedderburn 結構定理。

**推理**：這個「群 → 環/域 → 線性代數」的骨架，就是今天全世界大學代數課程與教科書的標準架構。以域論為例，書中採用的核心工具是同構擴張引理與分裂域：
- 對域 $F$ 與其上的不可約多項式 $f(x)$，存在擴張域 $E \supseteq F$ 使 $f$ 在 $E$ 上分裂；
- Galois 對應：$E/F$ 的中間域與 Galois 群 $G = \operatorname{Gal}(E/F)$ 的子群之間有反序雙射
  $$\{ \text{中間域 } K : F \subseteq K \subseteq E \} \;\longleftrightarrow\; \{ \text{子群 } H \leq G \}$$
  這個對應徹底解決了「五次方程無根式解」的古典問題（Abel–Ruffini，$S_5$ 不可解）。

### 線索三：結構主義數學的典範
《Moderne Algebra》的哲學：數學研究的不是「數」，而是**結構**。書中首次大規模使用「同構的兩個結構視為同一」的觀點，並以定義—定理—證明的嚴格公理化格式呈現。這種風格直接啟發了 1930 年代末期的 **Bourbaki 學派**（法國），其《Éléments de mathématique》正是結構主義的極致版本。偵探的推理：一本教科書之所以能成為典範，是因為它改變了「什麼才算一段數學」的敘述格式。

### 線索四：影響全世界代數教育
- 英譯本 *Modern Algebra*（1937–1949，二卷）成為英美標準參考；
- 二戰後的經典教科書——Birkhoff & MacLane《A Survey of Modern Algebra》(1941)、Herstein、Lang、Artin《Algebra》——全部沿用 van der Waerden 的架構與術語；
- 「環」「域」「模」「理想」等術語的標準化歸功於此書的流通；
- 「modern algebra（近代代數）」一詞本身就成為這門學科的名字。

### Python 示範：Galois 對應的小例子
以 $E = \mathbb{F}_4$（$\mathbb{F}_2$ 的二次擴張）為例，驗證 Galois 對應：
```python
from itertools import product

p = 2
# 用 F2[x]/(x^2+x+1) 建構 F4，元素以多項式係數 tuple 表示
irr = (1, 1, 1)  # x^2 + x + 1
def fadd(a, b): return tuple((x + y) % p for x, y in zip(a, b))
def fmul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i + j] ^= x & y
    for k in range(len(r) - 1, 1, -1):       # 模 x^2+x+1
        if r[k]:
            r[k - 2] ^= 1; r[k - 1] ^= 1
    return tuple(r[:2])

F4 = [(0, 0), (1, 0), (0, 1), (1, 1)]
# Frobenius 自同構 σ(u) = u^2，生成 Gal(E/F2) ≅ Z/2
sigma = lambda u: fmul(u, u)
print("σ 保持加法:", all(fadd(sigma(a), sigma(b)) == sigma(fadd(a, b)) for a, b in product(F4, repeat=2)))
print("σ 修正 F2 子域:", all(sigma(u) == u for u in F4[:2]))  # 不動點 = 子域 F2
# Galois 對應：子群 {id, σ} ↔ 子域 F2；子群 {id} ↔ E 本身
```
程式驗證了書中 Galois 理論的最小實例：$\operatorname{Gal}(\mathbb{F}_4/\mathbb{F}_2) \cong \mathbb{Z}/2\mathbb{Z}$，其子群與中間域一一對應。

## 結案 -- 後果與影響
- **代數教育的全球統一**：此書的章節架構沿用至今，所有「近世代數」「抽象代數」課程都是它的後裔。
- **Bourbaki 與結構主義**：《Moderne Algebra》是結構主義數學的第一個成功範本，Bourbaki 的公理化工程直接繼承其方法。
- **同調代數與範疇論的前奏**：書中對「結構與同態」的重視，為 Eilenberg–MacLane 的範疇論（1945）提供了思想土壤。
- **結案陳詞**：van der Waerden 沒有發明新數學，卻偵破了一樁「傳播案」——他從 Noether 與 Artin 的課堂取得線索，把抽象代數寫成全世界都能閱讀的偵探手冊。

## 關鍵人物與文獻
- **Bartel Leendert van der Waerden (1903–1996)**：荷蘭數學家，Göttingen/Hamburg 受訓，後任教於 Groningen、Leipzig、Zürich；也是 Ramsey 理論先驅（1926 年 van der Waerden 定理）。
- van der Waerden, B.L. (1930, 1931). *Moderne Algebra*, Bd. I & II. Springer, Berlin.
- Noether, E. (1921). *Idealtheorie in Ringbereichen*.（第一卷環論章節的來源）
- Artin, E. (1927). 超複數系與 Wedderburn 定理的講授（第二卷來源）。
- 交叉參照：`1858-Cayley矩陣.md`、`1893-抽象群公理化.md`、`1921-Noether環論.md`、`1945-範疇論.md`。
