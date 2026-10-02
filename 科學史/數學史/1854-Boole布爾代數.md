# 1854 - Boole 布爾代數

## 案件摘要
1854 年，英國數學家 George Boole 出版《思維規律的研究》（An Investigation of the Laws of Thought）：把**邏輯代數化**——「真/假」變成 1/0，「且/或/非」變成乘法/加法/補集——**邏輯第一次成為可運算的代數**。萊布尼茨的夢想（推理 = 計算，1703，見 `1703-Leibniz二進制.md`）第一次有了數學實現。**80 年後 Shannon 的電路**（1937，見 `../密碼學/1703-Leibniz二進制.md`）讓布爾代數成為**電腦的邏輯基礎**——每一次 AND、OR、XOR 運算都是 Boole 的遺產。

## 前因 -- 為什麼會有這個案子
**邏輯的兩千年**：亞里士多德的三段論（前 350）——「所有人皆會死；蘇格拉底是人；故蘇格拉底會死」——**用自然語言推理**，無法運算。

**萊布尼茨的夢想**（1703，見 `1703-Leibniz二進制.md`）：把推理化為計算——「讓我們計算吧」——但沒有實現（符號系統太粗糙）。

**19 世紀的機會**：
- **代數的成熟**：抽象的運算律（交換、結合、分配）——**運算律可以「脫離數字」**（與 Hamilton 四元數 1843 的非交換解放同源，見 `1843-Hamilton四元數.md`）
- **De Morgan 的先聲**（1847）：《形式邏輯》——**德摩根律**：$\neg(A \land B) = \neg A \lor \neg B$——邏輯的「代數味」

**Boole 的問題**：能否把邏輯推理**完全代數化**——用運算律取代三段論？

## 線索與推理 -- 數學式、程式、理論

### 布爾代數
**基本元素**：$\{0, 1\}$（假/真）——**兩個值的世界**。

**運算**：

| 邏輯 | 布爾代數 | 運算律 |
|------|----------|--------|
| 且（AND, $\land$） | 乘法 $x \cdot y$ | 交換、結合、分配 |
| 或（OR, $\lor$） | 加法 $x + y$ | 交換、結合 |
| 非（NOT, $\neg$） | 補集 $1 - x$ | $\neg\neg x = x$ |

**德摩根律**：

$$\neg(x \land y) = \neg x \lor \neg y \implies 1 - xy = (1-x) + (1-y) - (1-x)(1-y)$$

**分配律的驚喜**（邏輯有、數沒有）：

$$x \land (y \lor z) = (x \land y) \lor (x \land z) \implies x(y + z) = xy + xz$$

**在布爾代數中成立**——但在**數**（$x, y, z \in \mathbb{R}$）中，$x(y+z) = xy + xz$ 也成立（分配律）——但 $x + x = x$（**冪等律**，邏輯的「真且真 = 真」）在數中**不成立**（$1 + 1 = 2$）——**邏輯與數的運算律不同**——**布爾代數是新的代數結構**（與 Galois 的群論、Hamilton 的四元數同源的「結構」傳統）。

### 推理 = 計算
**三段論的代數化**：「所有人皆會死（$M \subseteq D$）；蘇格拉底是人（$s \in M$）」——**推理變成集合/代數的運算**：

$$s \in M \subseteq D \implies s \in D$$

**邏輯推理 = 代數運算**——萊布尼茨的夢想實現。

**深遠的意義**：
1. **邏輯的形式化**：Frege（1879，見 `1879-Frege概念文字.md`）的概念文字、羅素的白頭稿——**數理邏輯的譜系**
2. **電路的誕生**（Shannon 1937）：**布爾代數 = 開關電路**——AND 門 = 串聯、OR 門 = 並聯——**電腦的邏輯基礎**
3. **程式語言**：條件判斷（if-else）的布爾邏輯——**每一次 if 都是 Boole**

### 程式碼：布爾代數

```python
def boolean_algebra():
    """布爾代數：邏輯 = 代數"""
    # 冪等律（邏輯的「真且真 = 真」）——數中不成立！
    print(f"x·x = x（邏輯）：{all(x & x == x for x in [0, 1])}")
    print(f"數中 1+1 = 2 ≠ 1——邏輯與數的運算律不同")

    # 德摩根律
    dm = []
    for x in [0, 1]:
        for y in [0, 1]:
            lhs = 1 - (x & y)                    # ¬(x ∧ y)
            rhs = (1-x) | (1-y)                  # ¬x ∨ ¬y
            dm.append(lhs == rhs)
    print(f"德摩根律 ¬(x∧y) = ¬x∨¬y：{all(dm)} ✓")

    # 分配律（邏輯有）
    dist = []
    for x in [0, 1]:
        for y in [0, 1]:
            for z in [0, 1]:
                dist.append(x & (y | z) == (x & y) | (x & z))
    print(f"分配律 x(y∨z) = xy∨xz：{all(dist)} ✓")

boolean_algebra()

# 邏輯 = 計算（萊布尼茨的夢想）
def syllogism(m_subset_d, s_in_m):
    """三段論的代數化：推理 = 運算"""
    return m_subset_d and s_in_m

print(f"\n三段論：M⊆D 且 s∈M → s∈D：{syllogism(True, True)}")
print("推理 = 計算——Boole 1854 實現萊布尼茨的夢想")
print("Shannon 1937：布爾代數 = 開關電路——電腦的邏輯基礎")
```

## 結案 -- 後果與影響
- **邏輯的代數化**：邏輯成為可運算的結構——萊布尼茨夢想的實現。
- **電腦的邏輯基礎**：Shannon 1937 的電路——**每一次 AND、OR、XOR 都是 Boole**。
- **新代數結構的傳統**：冪等律（$x+x=x$）——**邏輯與數的運算律不同**（格論 lattice 的誕生：Dedekind 1897、Birkhoff 1930s）。
- **數理邏輯的譜系**：Boole → Frege → Russell → Hilbert → Gödel——**邏輯的世紀**。
- **程式語言**：if-else 的布爾邏輯、SQL 的 WHERE——**每一次條件判斷都是 Boole**。
- **Boole 的人生**：鞋匠之子、自學成才（與 Ramanujan 同源）、死於肺炎（妻子用冷水淋身的「療法」——悲劇）。

## 關鍵人物與文獻
- **George Boole**（1815–1864）：The Mathematical Analysis of Logic (1847)、An Investigation of the Laws of Thought (1854)
- **Augustus De Morgan**（1806–1871）：德摩根律 (1847)——Boole 的同路人
- **Claude Shannon**（1916–2001）：1937 電路——布爾代數的工程化
- **Gottlob Frege**（1848–1925）：概念文字 (1879)——見 `1879-Frege概念文字.md`
- **Garrett Birkhoff**（1911–1996）：格論（lattice theory）——布爾代數的推廣
- 交叉參照：`1703-Leibniz二進制.md`、`1879-Frege概念文字.md`、`1843-Hamilton四元數.md`、`1832-Galois群論.md`
