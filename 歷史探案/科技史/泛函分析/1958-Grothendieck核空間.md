# 1958-Grothendieck核空間

| 案件檔案 | |
|------|------|
| 案發年份 | 1955（法國，南錫；thèse 發表） |
| 主嫌 | 核空間與拓樸張量積 $\otimes_\pi,\ \otimes_\varepsilon$ |
| 受害者 | Banach 空間理論的邊界：對偶與張量的幾何仍是謎 |
| 關鍵證人 | Alexander Grothendieck（1955 thèse《張量積與核空間》） |
| 結案結果 | 拓樸向量空間的哥白尼轉向，逼近性質問題提出，Fields 1966 伏筆 |

## 案發現場

1950 年代，Banach 空間理論的黃金年代剛剛落幕（Banach 1932 教科書、Hahn–Banach、開映射、一致有界三柱石都已定稿），但一樁大案在邊界地帶浮現：

1. **無窮維張量積沒有統一理論**：兩個無窮維向量空間的「張量積」有好多種自然的拓樸（投影拓樸 $\otimes_\pi$ 與內射拓樸 $\otimes_\varepsilon$ ），彼此何時一致？
2. **核空間的身分不明**：Schwartz 的分布空間 $\mathcal D$ 、 $\mathcal S$ 有著異常好的性質（可數綱、稠密對偶、容易取極限），但它們的抽象特徵是什麼？
3. **Schwartz 學派的懸案**：核空間上的算子是否都有「幾乎有限秩」的表示？

謎題的核心：**能否建立拓樸張量積的系統理論，並用它解剖核空間？** 這是年僅 27 歲的 Alexander Grothendieck 在南錫要接的案子。

## 偵查過程

Grothendieck 的偵查策略是：**把張量積變成「對偶的顯微鏡」——用兩種自然拓樸的差距來量測空間的幾何**。

### 第一步：兩種拓樸張量積

設 $E,\ F$ 為局部凸空間。代數張量積 $E\otimes F$ 上有兩種自然拓樸：

1. **投影拓樸** $\otimes_\pi$ ：由所有 $E^*\otimes F^*$ 中的範數 $p\otimes q$ 誘導，範數為

$$\pi(u)=\inf\Big\{\sum_i\|x_i\|\,\|y_i\|:\ u=\sum_i x_i\otimes y_i\Big\} ;$$

2. **內射拓樸** $\otimes_\varepsilon$ ：由嵌入 $E\otimes F\hookrightarrow \mathcal B(E'_\sigma,F)$ 誘導，範數為

$$\varepsilon(u)=\sup\Big\{\Big|\sum_i x^*(x_i)\,y^*(y_i)\Big|:\ x^*\in B_{E^*},\ y^*\in B_{F^*}\Big\} .$$

恆有 $\varepsilon(u)\le\pi(u)$ ；完成的空間記作 $E\widehat\otimes_\pi F$ 與 $E\widehat\otimes_\varepsilon F$ 。

### 第二步：對偶的顯微鏡

兩種拓樸的對偶空間都是 $\mathcal B(E,F^*)$ （連續雙線性形式），但完備化不同。Grothendieck 的高招：**用 $\pi$ 與 $\varepsilon$ 的差距當作幾何不變量**：

| 對象 | $\pi=\varepsilon$ 的意義 | 典型例子 |
|------|--------------------------|----------|
| 核算子 | $\mathcal B(E,F^*)$ 中的元可表示為 $\sum x_n^*\otimes y_n$ 且 $\sum\|x_n^*\|\,\|y_n\|<\infty$ | 積分算子的抽象化 |
| 核空間 $E$ | 對所有 Banach 空間 $F$ ， $E\widehat\otimes_\pi F=E\widehat\otimes_\varepsilon F$ | $\mathcal D,\ \mathcal S,\ s$ （快速衰變序列） |
| 迹類算子 | $\ell^1\widehat\otimes_\pi \ell^2=(\ell^2)^*$ | Hilbert–Schmidt 理論 |

### 第三步：核空間的解剖

Grothendieck 證明核空間的等價刻畫：

1. **表示刻畫**： $E$ 上每一連續線性映射到 Banach 空間的都是核算子（幾乎有限秩）。
2. **對偶刻畫**： $E'$ 的等距鄰域基存在「快速收斂」的子列結構。
3. **張量刻畫**：對所有 $F$ ， $\otimes_\pi=\otimes_\varepsilon$ 。

核空間性質偵查表：

| 性質 | Banach 空間（無窮維） | 核空間 |
|------|----------------------|--------|
| 張量積唯一性 | 一般不成立 | 成立 |
| 算子結構 | 多樣（含非核算子） | 全是核算子 |
| 極限操作 | 需謹慎 | 容易（ $\mathcal D$ 的 LF 拓樸） |
| 範例 | $\ell^p,\ L^p,\ C[0,1]$ | $\mathcal D,\ \mathcal S,\ s,\ C^\infty$ |

### 第四步：逼近性質問題的提出

Grothendieck 在 thèse 中提出一樁深案：**逼近性質（AP）**。空間 $E$ 有 AP 若對每個緊集 $K\subset E$ 與 $\varepsilon>0$ ，存在有限秩算子 $T$ 使

$$\|Tx-x\|\le\varepsilon,\qquad \forall x\in K .$$

等價地（Grothendieck 的張量語言）： $E\widehat\otimes_\pi F\to E\widehat\otimes_\varepsilon F$ 的典範映射對所有 $F$ 都是單射。

Grothendieck 證明：自反空間與核空間都有 AP；並提出**逼近性質問題**：是否所有 Banach 空間都有 AP？他在 thèse 中留下六個等價形式的問題，成為泛函分析未來二十年的懸案。

### 第五步：Schwartz 學派的接手

Grothendieck 的 thèse 由 Dieudonné 與 Schwartz 學派推廣：

1. **核空間在 $\mathcal D'$ 中的角色**：核空間理論為分布理論（1945）提供抽象基礎—— $\mathcal D$ 的可數綱、 $\mathcal S$ 的快速衰變，都是核性的表現。
2. **譜論的應用**：核空間上的核算子有完備的譜論（迹公式、Fredholm 行列式推廣）。
3. **代數幾何的遠親**：Grothendieck 1957 年轉向代數幾何（Tohoku 論文把同調代數公理化），張量積的思維方式（用對偶解剖空間）貫穿他後半生的綱領。

## 結案報告

1955 年 Grothendieck thèse 完成，宣布結案：拓樸張量積有了系統理論，核空間有了三重等價刻畫，逼近性質問題正式立案。案件遺產如下：

- **拓樸向量空間的哥白尼轉向**：把「空間的幾何」由內部結構轉到對偶與張量的視角，這一思維方式影響了 Grothendieck 後半生的代數幾何綱領。
- **逼近性質問題**：成為泛函分析的頭號懸案，直到 1971 年 Enflo 構造性反例才落幕（見 1971-Enflo反例）。
- **核空間的工具化**：分布理論、譜論、馬爾可夫過程（Minlos 定理：核空間上的正定泛函給出測度）都以核空間為舞台。
- **Fields 1966 伏筆**：Grothendieck 因代數幾何（而非泛函分析）獲 1966 年菲爾茲獎，但 his thèse 的張量積思維是他統一視野的第一站。
- **算子理想理論**：Pietsch 的算子理想理論（ $p$ -核算子、積核算子）是核空間理論的直接後裔。

## 證據與工具

**關鍵公式一覽表：**

| 工具 | 公式／陳述 | 用途 |
|------|-----------|------|
| 投影範數 | $\pi(u)=\inf\{\sum\|x_i\|\,\|y_i\|\}$ | $\otimes_\pi$ 的度量 |
| 內射範數 | $\varepsilon(u)=\sup\{|\sum x^*(x_i)y^*(y_i)|\}$ | $\otimes_\varepsilon$ 的度量 |
| 核空間刻畫 | $\forall F:\ E\widehat\otimes_\pi F=E\widehat\otimes_\varepsilon F$ | 核性的定義 |
| 核算子 | $T=\sum x_n^*\otimes y_n$ ， $\sum\|x_n^*\|\,\|y_n\|<\infty$ | 迹類推廣 |
| 逼近性質 | $\inf_T\sup_{x\in K}\|Tx-x\|\le\varepsilon$ | AP 的定義 |
| Minlos 定理 | 核空間上的連續正定泛函 $\Leftrightarrow$ 測度 | 隨機過程應用 |

**證明骨架（ $\pi\ge\varepsilon$ ）：**

1. 設 $u=\sum x_i\otimes y_i$ 是任一表示。
2. 對任意 $x^*\in B_{E^*},\ y^*\in B_{F^*}$ ：
$$\Big|\sum x^*(x_i)y^*(y_i)\Big|\le\sum\|x_i\|\,\|y_i\| .$$
3. 對右端取下確界即得 $\varepsilon(u)\le\pi(u)$ 。 $\blacksquare$

**典型例子：** Hilbert 空間 $H$ 上的核算子： $T=\sum\lambda_n\langle\cdot,e_n\rangle f_n$ ， $\sum|\lambda_n|<\infty$ 。迹公式 $\mathrm{tr}(T)=\sum\lambda_n$ 良定義且與基底無關——這是有限維線性代數「迹」在無窮維的核空間推廣，Grothendieck 的 $\otimes_\pi$ 正是它的抽象舞台。
