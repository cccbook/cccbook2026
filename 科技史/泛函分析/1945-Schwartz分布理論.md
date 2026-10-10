# 1945-Schwartz分布理論

| 案件檔案 | |
|------|------|
| 案發年份 | 1945（法國，格勒諾布爾） |
| 主嫌 | 分布空間 $\mathcal D'$ |
| 受害者 | Dirac 的 $\delta$ 函數：物理用了二十年卻「不是函數」 |
| 關鍵證人 | Laurent Schwartz（1945 論文、1950–51《分布論》） |
| 結案結果 | $\delta$ 函數扶正為線性泛函，Schwartz 獲 1950 Fields 獎 |

## 案發現場

物理學家 Dirac 在 1930 年代量子力學中使用了一個幽靈般的對象： $\delta(x)$ ，宣稱它「除了在 $0$ 之外處處為零，積分卻等於 $1$ 」。任何學過 Lebesgue 積分的學生都知道：這樣的函數不存在——一個 a.e. 為零的可測函數積分必為零。

更糟的是，物理學家還對 $\delta$ 做「導數」：

$$\delta'(x)=\lim_{h\to 0}\frac{\delta(x+h)-\delta(x)}{h} ,$$

甚至把 $\delta(x)$ 當成收斂函數列 $\frac{1}{\pi}\frac{\varepsilon}{x^2+\varepsilon^2}$ 的「極限」——但這個極限在 $L^1$ 與逐點意義下都不存在。

謎題的兩難是：

1. 物理需要 $\delta$ ：點電荷、衝擊、瞬時源的數學代言。
2. 數學不容 $\delta$ ：它不是函數，沒有嚴格的操作規則。

誰能替這個幽靈補辦身分證，同時讓「導 $\delta$ 的導數」合法化？這是 Laurent Schwartz 在 1945 年要接的案子。

## 偵查過程

Schwartz 的偵查策略是：**反轉視角——不把 $\delta$ 當成函數，而把它當成「對函數做作用的機器」**。

### 第一步：測試函數空間 $\mathcal D$

定義 $\mathcal D=C_c^\infty(\mathbb{R}^n)$ ：無窮可微且緊支撐的函數全體。賦予局部凸拓樸：對每個緊集 $K$ ，取半範數族

$$p_{K,m}(\phi)=\sup_{x\in K,\ |\alpha|\le m}|\partial^\alpha\phi(x)| ,$$

以歸納極限的方式拼出 $\mathcal D$ 的 LF 拓樸。這個拓樸的關鍵性質： $\phi_j\to\phi$ 意味著支撐集落在一個共同緊集內，且各階導數一致收斂。

### 第二步：分布的定義

定義 $\mathcal D'$ 為 $\mathcal D$ 上所有**連續**線性泛函的空間：

$$T\in\mathcal D'\ \Longleftrightarrow\ T:\mathcal D\to\mathbb{C}\ \text{線性且連續} ,$$

記 $T(\phi)=\langle T,\phi\rangle$ 。局部可積函數 $f$ 以正則方式入籍：

$$\langle T_f,\phi\rangle=\int f(x)\,\phi(x)\,dx .$$

而 $\delta$ 的真面目終於現形：

$$\langle \delta,\phi\rangle=\phi(0) .$$

它是一台「在原點取值的機器」，完全合法、完全連續——幽靈扶正為泛函。

### 第三步：導數的推廣

既然 $\delta$ 是泛函，導數也定義在泛函上：利用分部積分的對偶轉移，定義

$$\langle \partial^\alpha T,\phi\rangle=(-1)^{|\alpha|}\langle T,\partial^\alpha\phi\rangle .$$

於是 $\delta'=\partial\delta$ 由 $\langle \delta',\phi\rangle=-\phi'(0)$ 定義。任意分布有任意階導數，且 $\partial^\alpha:\mathcal D'\to\mathcal D'$ 是連續線性映射。物理學家偷偷導了二十年的 $\delta'(x)$ ，正式拿到戶口。

### 第四步：收斂的扶正

那些「物理極限」也扶正了：定義 $\mathcal D'$ 中的弱*收斂：

$$T_j\to T\ \Longleftrightarrow\ \langle T_j,\phi\rangle\to\langle T,\phi\rangle,\quad \forall\phi\in\mathcal D .$$

例如 $\frac{1}{\pi}\frac{\varepsilon}{x^2+\varepsilon^2}\to\delta$ （ $\varepsilon\to 0^+$ ），因為

$$\int \frac{1}{\pi}\frac{\varepsilon}{x^2+\varepsilon^2}\,\phi(x)\,dx \to \phi(0) ,$$

（Poisson 核的逼近恆等性質）。由 Banach–Steinhaus 型論證，逐點收斂的分布列自動為連續收斂， $\mathcal D'$ 在弱*拓樸下是序列完備的。

### 第五步：偵查筆記本——各種操作的合法性

| 操作 | 經典函數 | 分布 |
|------|----------|------|
| 積分作用 | $\int f\phi\,dx$ | $\langle T,\phi\rangle$ |
| 導數 | 需逐點可微 | $\langle\partial T,\phi\rangle=-\langle T,\partial\phi\rangle$ ，任意階 |
| 極限 | 需一致或 $L^p$ 收斂 | 弱*逐點收斂即可 |
| 乘以 $C^\infty$ | 自然 | $\langle aT,\phi\rangle=\langle T,a\phi\rangle$ |
| Fourier 變換 | 需 $L^1$ 或 Schwartz 類 | 在 $\mathcal S'$ 上延拓， $\widehat{\delta}=1$ |

### 第六步：Schwartz 空間 $\mathcal S$ 與 $\mathcal S'$

Schwartz 同時引進緩增函數空間 $\mathcal S$ （快速衰變的 $C^\infty$ 函數）與其對偶 $\mathcal S'$ （緩增分布），使 Fourier 變換成為 $\mathcal S'$ 上的自同構：

$$\mathcal F:\mathcal S'\to\mathcal S',\qquad \mathcal F\mathcal F=4\pi^2 R\ \text{（適當規範下）} .$$

這條線索為調和分析（Calderón–Zygmund 算子）與 PDE 基本解理論開了路。

## 結案報告

1945 年 Schwartz 宣布結案： $\delta$ 函數不是函數，而是 $\mathcal D$ 上的連續線性泛函；「導它、取極限、Fourier 變換它」全部合法化。案件遺產如下：

- **1950 年 Fields 獎**：Schwartz 因分布理論獲首屆菲爾茲獎之一；1950–51 年兩卷《分布論》（Théorie des distributions）成為經典。
- **PDE 基本解理論**：Malgrange–Ehrenpreis 定理（任意常係數線性 PDO 有基本解）在分布語言下成立； $L(E-\lambda)u=\delta$ 的解是研究算子譜的鑰匙。
- **Dirac 的勝利**：量子力學的數學基礎（von Neumann 1932 之後）補上了分布這一塊， $\delta$ 正規化為投影測度的密度。
- **Sobolev 空間接軌**：1935 年 Sobolev 的弱導數成為分布導數的特例；Sobolev 嵌入成為分布論的正則性工具。
- **後續浪潮**：1956 年 Gårding 不等式、1973 年 Calderón–Zygmund 奇異積分的算子觀，都以 $\mathcal D'$ 為舞台。

## 證據與工具

**關鍵公式一覽表：**

| 工具 | 公式／陳述 | 用途 |
|------|-----------|------|
| $\delta$ 的作用 | $\langle \delta,\phi\rangle=\phi(0)$ | 幽靈扶正 |
| 分布導數 | $\langle\partial^\alpha T,\phi\rangle=(-1)^{|\alpha|}\langle T,\partial^\alpha\phi\rangle$ | 任意階導數 |
| 弱*收斂 | $\langle T_j,\phi\rangle\to\langle T,\phi\rangle\ \forall\phi$ | 物理極限合法化 |
| 正則分布 | $\langle T_f,\phi\rangle=\int f\phi\,dx$ | 函數入籍 |
| Poisson 核 | $\frac{1}{\pi}\frac{\varepsilon}{x^2+\varepsilon^2}\to\delta$ | $\delta$ 的逼近恆等 |
| $\mathcal F(\delta)$ | $\widehat{\delta}=1$ | Fourier 變換在 $\mathcal S'$ 上延拓 |

**證明骨架（ $\delta$ 的連續性）：**

1. 設 $\phi_j\to 0$ 在 $\mathcal D$ 中：支撐在共同緊集 $K$ 內，各階導數一致趨於零。
2. $|\langle\delta,\phi_j\rangle|=|\phi_j(0)|\le\sup_{x\in K}|\phi_j(x)|\to 0$ 。
3. 故 $\delta$ 連續， $\delta\in\mathcal D'$ 。 $\blacksquare$

**典型例子：** 計算 $x\,\delta=\phi\mapsto\langle x\delta,\phi\rangle=\langle\delta,x\phi\rangle=x\phi(0)\big|_{x=0}=0$ ，故 $x\,\delta=0$ 。同樣可算 $\partial(x\delta)=\delta+x\delta'=\delta$ ——分布的乘法與導數服從 Leibniz 法則，但 $x\delta=0$ 這類恆等式在函數世界不可能出現，這正是分布語言的威力。
