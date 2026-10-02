# 2012 - Peter Scholze 發明 Perfectoid Space

## 案件摘要
2012 年，24 歲的德國博士生 Peter Scholze 發明 **perfectoid space**，為 p 進幾何建立了「兩個幾何世界的字典」。這項工作震撼代數數論界，直接推進朗蘭茲綱領，並使他於 2018 年（27 歲）獲頒菲爾茲獎。

## 前因 -- 為什麼會有這個案子

**p 進數**：與實數不同，p 進絕對值以「$p$ 的整除性」衡量距離：

$$\left|\frac{a}{b} p^n\right|_p = p^{-n}, \quad \left|p\right|_p = p^{-1}, \quad \mathbb{Q}_p = \text{完成化}(\mathbb{Q}, |\cdot|_p)$$

兩數「接近」意指其差被 $p$ 的高次冪整除。這產生了詭異的幾何：三角形內角和為零、每個三角形內含無窮多個更小的同心三角形。

**數論的核心困難**：整數與有理數的許多問題（局部-整體原理、伽羅瓦表示、朗蘭茲對應），需要在 $p$ 進世界做幾何。但 $\mathbb{Q}_p$ 的幾何「坑坑疤疤」、缺乏光滑性——特別是特徵 $p$ 的世界存在 **Frobenius** $x \mapsto x^p$，這個強大的對稱性在特徵 0 的 $p$ 進世界裡缺席。

**案子本身**：能否構造一類空間，讓特徵 0 的 $p$ 進幾何「借用」特徵 $p$ 幾何的 Frobenius 對稱性？Scholze 的答案就是 perfectoid space。

## 線索與推理 -- 數學式、程式、理論

### 線索一：perfectoid 空間的定義

**定義（perfectoid 域）**：完備非阿基米德域 $K$（特徵 0）若其絕對值非離散、且 Frobenius 在 $K^{\circ}/p$ 上是同構（$K^{\circ}$ 為冪整元素環），則稱為 perfectoid。典型例子：

$$\mathbb{Q}_p(p^{1/p^\infty}) = \mathbb{Q}_p(p^{1/p}, p^{1/p^2}, p^{1/p^3}, \ldots)$$

**定義（perfectoid 空間）**：由 perfectoid 仿射空間 $\mathrm{Spa}(A, A^+)$ 粘合而成的 adic 空間，其仿射開集 $A$ 滿足：存在一組冪零指數逼近的生成元 $T_i$，使 $A$ 的結構「無窮靠近」特徵 $p$ 的完美環。

### 線索二：Tilting 等價——幾何 ↔ 幾何的字典

**tilting 操作**：將特徵 0 的 perfectoid 空間 $X$ 轉為特徵 $p$ 的空間 $X^{\flat}$：

$$K^{\flat} = \lim_{\leftarrow \, x \mapsto x^p} K^{\circ}/p$$

元素取 $p$ 次方根的極限，世界從特徵 0「翻轉」到特徵 $p$。

**主定理（Scholze 2012，Tilting Correspondence）**：

$$X \;\text{perfectoid（特徵 0）} \;\longleftrightarrow\; X^{\flat} \;\text{perfectoid（特徵 } p\text{）}$$

兩邊的拓撲空間範疇等價，且**幾乎所有函數層性質（étale 上同調等）可以互相轉譯**。這是一本「幾何 ↔ 幾何」的字典：

| 特徵 0 世界 | 特徵 $p$ 世界 |
|---|---|
| $\mathbb{Q}_p(p^{1/p^\infty})$ | $\mathbb{F}_p((t))$（Laurent 級數） |
| $p$ 進 adic 空間 | 完美空間，有 Frobenius $x \mapsto x^p$ |
| 伽羅瓦表示 | 局部系（local systems） |

**威力示範**：Scholze 用它證明了特徵 0 情況的 **Deligne 加權單值猜想**（monodromy-weight conjecture），將困難問題翻轉到特徵 $p$、用 Frobenius 的剛性解決。

### 線索三：幾乎純數學的年輕天才

- Scholze 2009 年（22 歲）以三個月讀完並簡化 Harris–Taylor 的朗蘭茲證明；2010 年波恩大學博士，博士論文即為 perfectoid 空間的雛形。
- 2012 年論文 *Perfectoid Spaces* 發表於 Publ. Math. IHÉS，立即被視為革命。
- 2018 年（27 歲）獲菲爾茲獎，表彰其「將 p 進幾何學革命化，並使之與李群表示論連結」。

### 線索四：對朗蘭茲綱領與代數數論的影響

- **局部朗蘭茲**：2014 年與 Caraiani 等合作，用 perfectoid 技術證明局部-整體相容性的關鍵情形（$l \neq p$ 情形的 Hodge–Tate 性質）。
- **Shimura 簇的高維擴張**：perfectoid 化使高維 Shimura 簇可以「取極限」成 perfectoid 簇，從而證明：
  - Carayiani–Scholze：Shimura 簇的 Étale 上同調具有意想不到的「消沒」性質；
  - 2015–2020 年間一系列朗蘭茲相容性結果。
- **Prismatic 上同調**（2019 年後）：Scholze 與 Bhargav Bhatt 將「Frobenius 借用」的思想發展成 prismatic cohomology，統一了晶形上同調與 de Rham 上同調。
- **稠密性革命**：2018 年 Scholze 提出「液體向量空間」（liquid vector spaces）與解析幾何（analytic geometry）計畫，重建實數與 p 進的分析基礎。

## 結案 -- 後果與影響

- perfectoid 空間已成為 p 進幾何的**標準語言**，如同層論之於代數幾何。
- 朗蘭茲綱領的多個關鍵進展（局部-整體、上同調消沒、prismatic 方法）皆由其驅動。
- 證明了 Deligne 加權單值猜想，並為 Sato–Tate、R=T 等問題提供新工具。
- 開啟的問題仍在發酵：prismatic 上同調與 $p$ 進 Hodge 理論的完全統一、以及 Scholze 的「分析幾何」綱領（liquid spaces、實數版的 perfectoid——如與 Clausen 合作的 real blown-up 構造）。
- 教育影響：Scholze 的論文與 IOU（«I owe you»）風格的線上講義，帶動數學界開放協作的新文化。

## 關鍵人物與文獻

| 人物 | 貢獻 |
|---|---|
| Kurt Hensel | 1897 發明 p 進數 |
| Jean-Marc Fontaine | 建構 $p$ 進 Hodge 理論與 period rings（perfectoid 的前身） |
| Peter Scholze | 2012 發明 perfectoid space，2018 菲爾茲獎（27 歲） |
| Bhargav Bhatt | 與 Scholze 共建 prismatic cohomology（2019） |

**文獻**：
- Scholze, P. (2012). "Perfectoid spaces". *Publ. Math. IHÉS* 116, 1–74.
- Scholze, P., Weinstein, J. (2019). *Berkeley Lectures on p-adic Geometry*. Annals of Math. Studies.
- Bhatt, B., Scholze, P. (2019). "Prisms and prismatic cohomology". arXiv:1905.08229.
