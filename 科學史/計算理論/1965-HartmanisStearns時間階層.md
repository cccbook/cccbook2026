# 1965 - Hartmanis 與 Stearns：時間階層定理與複雜度理論的誕生

## 案件摘要
1965 年，Hartmanis 與 Stearns 發表論文〈On the Computational Complexity of Algorithms〉，首次將「計算所需的時間」本身變成嚴格的數學研究對象。他們用對角線法證明了時間階層定理：給多一點時間，就一定能多解一些問題。這篇論文讓「複雜度」從工程直覺變成定理，兩人因此獲 1993 年圖靈獎。

## 前因 -- 為什麼會有這個案子
圖靈 (1936) 定義了「可計算」，但只回答 0/1 問題：算得出、或算不出。1960 年代面臨的謎題是：

- Rabin (1960)、Blum (1964) 已提出公理化複雜度測度，但那是「測度論式」的，抽象而難以計算具體結果；
- 工程上大家知道有些演算法快有些慢，但**沒有定理**說「快與慢之間真的存在不可跨越的鴻溝」。

核心案件問題：

> **計算時間 $f(n)$ 與 $g(n)$ 之間，是否真的存在「用 $g(n)$ 時間能解、用 $f(n)$ 時間永遠解不了」的問題？**

## 線索與推理 -- 數學式、程式、理論

### 線索一：時間複雜度類 $\text{TIME}(f(n))$ 的定義
Hartmanis–Stearns 採用**機器測度**而非公理測度：直接以多帶圖靈機的步數定義。

**定義**：語言 $L \in \text{TIME}(f(n))$，若存在多帶圖靈機 $M$ 使得對所有輸入 $x$，$M$ 在 $O(f(|x|))$ 步內停機，且 $x \in L \iff M(x) = 1$。

**定義（空間版本）**：$L \in \text{SPACE}(f(n))$，若 $M$ 在 $O(f(|x|))$ 格工作帶空間內判定 $L$。

他們首先證明**線性加速定理**：多帶圖靈機 $t(n)$ 步的計算，可被「更肥」的多帶圖靈機以 $t(n)/k$ 步模擬（把每格塞 $k$ 個符號）。推論：複雜度只對 $f(n) \mapsto f(n)/k$ 不變，因此對 $f(n) \mapsto f(n)\log f(n)$ 這種緩慢改變是可區分的——這正是階層定理的縫隙。

### 線索二：時間階層定理與對角線法
**定理（Hartmanis–Stearns, 1965）**：若 $f_2(n) \geq (1+\varepsilon) f_1(n)$ 且 $f_2$ 時間可構造（time-constructible）、$f_1$ 滿足溫和條件，則

$$\text{TIME}(f_1(n)) \subsetneq \text{TIME}\!\left(f_2(n)\right)$$

原論文的形式給出，例如：$\text{TIME}(n) \subsetneq \text{TIME}(n^{1+\varepsilon})$；現代教科書版本（需要模擬開銷）為：

$$\text{TIME}(f(n)) \subsetneq \text{TIME}\!\left(f(n)\log^2 f(n)\right)$$

**證明核心：對角線法（Cantor 1891 的靈魂轉世）。**

構造圖靈機 $D$：對輸入 $x$，$D$ 把 $x$ 視作第 $x$ 台機器的編碼，用 $f_2(n)$ 時間模擬 $M_x(x)$ 走 $f_1(n)$ 步，然後**輸出相反的答案**：

```
D(x):
    模擬 M_x(x) 執行 f_1(|x|) 步
    若 M_x 在此期間停機: 輸出 1 - M_x(x)   # 對角線反轉
    否則: 輸出 0
```

Python 概念示範（有限表上的對角線構造）：

```python
# 假設 M_0, M_1, ... 是所有 f1-時間機器在輸入 0,1,2,... 上的行為表
# rows = 機器, cols = 輸入, 值 = 0/1（None 表未在 f1 步內停機）
import itertools
rows = [
    [1, 0, 1, 1],
    [0, 1, 0, 0],
    [1, 1, 1, 0],
    [0, 0, 1, 1],
]
D = [1 - r[i] if r[i] is not None else 0
     for i, r in enumerate(rows)]   # 對角線反轉
# D 不等於任何一列：第 i 列上 D[i] != M_i(i)
print(D)   # 例: [0, 1, 0, 1]
```

- $D$ 最多用 $f_2(n)$ 時間（模擬 $f_1$ 步加常數開銷），故 $L(D) \in \text{TIME}(f_2)$；
- 但 $D$ 與每一台 $f_1$-時間機器在第 $x$ 個輸入上不同，故 $L(D) \notin \text{TIME}(f_1)$。$\blacksquare$

### 線索三：空間階層定理
同一手法對空間成立，且更乾淨（模擬開銷只是常數倍）：

**定理**：若 $f_2(n) \geq \omega(f_1(n))$（例如 $f_2 = f_1 \cdot \log f_1$）且 $f_2$ 空間可構造，則

$$\text{SPACE}(f_1(n)) \subsetneq \text{SPACE}(f_2(n))$$

由此立刻得到複雜度類的**真包含鏈**：

$$\text{TIME}(n) \subsetneq \text{TIME}(n^2) \subsetneq \text{TIME}(n^3) \subsetneq \cdots \subsetneq \text{EXPTIME}$$

$$\text{SPACE}(\log n) \subsetneq \text{SPACE}(n) \subsetneq \text{SPACE}(n^2) \subsetneq \cdots$$

還有重要推論：$\text{P} \subsetneq \text{EXPTIME}$（指數時間確實比多項式時間強——只是我們不知道 $\text{P}$ vs $\text{NP}$ 時縫隙在哪）。

### 線索四：把複雜度變成數學對象
Hartmanis–Stearns 的革命性在於**名詞的實體化**：

- 「這演算法複雜」→ 「$L \in \text{TIME}(n^3)$ 且 $L \notin \text{TIME}(n^2)$」；
- 他們並提出「複雜度類之間的歸約」思想，是日後多項式歸約的先聲；
- 他們還證明複雜度類有「完備問題」（在該類中最難者），是 completeness 概念的濫觴。

## 結案 -- 後果與影響
1. **複雜度理論正式誕生**：這篇論文被視為計算複雜度理論的開山之作。
2. **時間階層定理**成為所有「真包含」結果的模板：空間階層、確定性 vs 非確定性（Savitch 1970）、Interactive proofs（IP=PSPACE, 1992）皆承其手法。
3. 對角線法成為標準工具，同時也暴露其極限——Baker–Gill–Solovay (1975) 證明對角線法無法解決 $\text{P}$ vs $\text{NP}$。
4. **1993 年圖靈獎**授予 Hartmanis 與 Stearns，表揚「奠定計算複雜度理論基礎」。
5. 階層定理保證了複雜度研究「有無窮的問題可做」：階層無窮，地圖無邊。

## 關鍵人物與文獻
- **Jürgis Hartmanis**（Cornell，立陶宛裔）：與 Stearns 合著〈On the Computational Complexity of Algorithms〉, *Trans. AMS* 117, 1965.
- **Richard Stearns**（SUNY Albany）：同上。
- 前驅：Rabin (1960)〈Degree of difficulty of computing a function〉；Blum (1964) 公理複雜度測度。
- 後續：Savitch (1970)、Baker–Gill–Solovay (1975)、Hartmanis–Hopcroft–Ullman 教科書《Formal Languages and Their Relation to Automata》(1968)。
- 圖靈獎：1993 年（Hartmanis & Stearns）。
