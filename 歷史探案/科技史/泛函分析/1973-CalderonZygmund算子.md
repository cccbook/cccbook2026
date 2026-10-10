# 1973-CalderonZygmund算子

| 案件檔案 | |
|------|------|
| 案發年份 | 1973 前後（調和革命；源頭 Calderón–Zygmund 1952、Hilbert 變換） |
| 主嫌 | 奇異積分算子 $Tf(x)=\mathrm{p.v.}\int K(x-y)f(y)\,dy$ |
| 受害者 | 經典調和分析：核的奇異性讓 $L^p$ 有界性成謎 |
| 關鍵證人 | Alberto Calderón、Antoni Zygmund（1952 綱領、1973 前的算子觀成形） |
| 結案結果 | 弱 $(1,1)$ 估計與 $T(1)$ 理論，調和分析的算子觀確立 |

## 案發現場

十九世紀以來，調和分析的頭號懸案是 **Hilbert 變換**：

$$Hf(x)=\frac{1}{\pi}\,\mathrm{p.v.}\int_{-\infty}^{\infty}\frac{f(y)}{x-y}\,dy .$$

核 $K(x)=\frac{1}{\pi x}$ 在 $x=0$ 處奇異（不可積），但物理與 Fourier 分析中它無處不在：

1. **Fourier 共軛**： $H$ 是「取 $-i\,\mathrm{sgn}(\xi)$ 乘子」的 Fourier 乘子算子，即解析信號的虛部。
2. **邊值問題**：共軛函數是單位圓盤解析函數的邊界虛部。
3. **Cauchy 積分**： $\int\frac{f(y)}{x-y}dy$ 是 Cauchy 型積分的極限。

謎題的兩難：

1. 核奇異 → 直接的 Schur 檢驗失效， $L^2$ 有界性可由 Fourier 乘子取得，但 $L^p$ （ $p\ne 2$ ）呢？
2. $L^1$ 的映像更糟： $Hf$ 甚至不一定在 $L^1$ 中。

謎題的核心：**奇異積分算子的 $L^p$ 有界性該如何證明？ $L^1$ 中的正確估計是什麼？** 這是 Calderón 與 Zygmund 要接的案子。

## 偵查過程

Calderón–Zygmund 的偵查策略是：**「實變方法」——用層級分解與弱型估計繞過奇異性**。

### 第一步：Calderón–Zygmund 分解

對 $f\in L^1(\mathbb{R}^n)$ 與高度 $\alpha>0$ ，存在分解

$$f=g+\sum_j b_j,\qquad \|g\|_{L^\infty}\le\alpha,\qquad \mathrm{supp}\,b_j\subset Q_j,\quad \int_{Q_j}b_j=0 ,$$

其中 $\{Q_j\}$ 是二進方體， $\sum|Q_j|\le\|f\|_{L^1}/\alpha$ 。

| 成分 | 大小 | 支撐 |
|------|------|------|
| $g$ （好部分） | $\|g\|_{L^\infty}\le\alpha$ | 全域 |
| $b_j$ （壞部分） | 零平均 | 二進方體 $Q_j$ |

### 第二步：弱 $(1,1)$ 估計

用分解估計水平集：

$$\big|\{x:\ |Tf(x)|>\alpha\}\big|\le\frac{C}{\alpha}\|f\|_{L^1} .$$

偵查的兩段式：

1. **好部分** $g$ ： $|Tg(x)|\le\int|K(x-y)||g(y)|dy$ 需要核的「標準條件」：

$$|K(x-y)-K(x-y')|\le\frac{C|y-y'|}{|x-y|^2},\qquad |x-y|>2|y-y'| ,$$

即 **Hörmander 條件**（核的光滑性），配合 $\|g\|_{L^\infty}\le\alpha$ 與 Chebyshev 估計。
2. **壞部分** $b_j$ ：零平均使奇異的主項相消，只剩 $\frac{|y-y'|}{|x-y|^2}$ 型的尾巴，由 $\sum|Q_j|\le\|f\|_{L^1}/\alpha$ 控制。

合併即得弱 $(1,1)$ 估計。

### 第三步：插值取得 $L^p$

弱 $(1,1)$ ＋ $L^2$ 有界性（由 Fourier 乘子： $\widehat{Hf}=-i\,\mathrm{sgn}(\xi)\,\hat f$ ， $|{-i\,\mathrm{sgn}}|=1$ ）經 Marcinkiewicz 插值定理：

$$\|Tf\|_{L^p}\le C_p\|f\|_{L^p},\qquad 1<p<\infty .$$

**線索一**： $L^p$ 有界性確立，Hilbert 變換的 $L^p$ （ $1<p<\infty$ ）理論完成。

### 第四步：算子觀的成形

Calderón–Zygmund 把個案升級為綱領：**奇異積分算子的系統理論**。核滿足標準條件的算子

$$Tf(x)=\mathrm{p.v.}\int K(x,y)\,f(y)\,dy,\qquad |K(x,y)|\le\frac{C}{|x-y|^n}$$

形成一個算子代數的觀點：

| 性質 | 條件 | 結論 |
|------|------|------|
| 弱 $(1,1)$ | Hörmander 條件＋標準大小 | $\mu\{x:\ |Tf|>\alpha\}\le\frac{C}{\alpha}\|f\|_{L^1}$ |
| $L^p$ 有界 | 弱 $(1,1)$ ＋ $L^2$ | $1<p<\infty$ |
| 對偶 | 核交換 $K(x,y)^*=K(y,x)$ | $L^p$ 有界 ⟺ $L^{p'}$ 有界 |
| 交換子 | $[b,T]=bT-Tb$ | BMO 空間的角色 |

### 第五步： $T(1)$ 理論與 BMO

1973 年前後，Cotlar–Stein 引理與 $T(1)$ 理論把框架推廣到非卷積核：

**Cotlar–Stein 引理：** 若 $\|T_jT_k^*\|\le\omega(j-k)$ 且 $\sum\omega(j)<\infty$ （近對角衰減），則 $\|\sum T_j\|\le\sum\omega(j)^{1/2}$ 的平方和版本。

** $T(1)$ 理論**（David–Journé 1984 為定稿）： $T$ 在 $L^2$ 有界當且僅當 $T(1)$ 、 $T^*(1)$ 在 **BMO** 空間中，且核滿足標準條件。BMO 空間（John–Nirenberg 1961）成為奇異積分的天然「對偶」—— $H^1$ 的對偶正是 BMO（Fefferman–Stein 1972）。

### 第六步：Hardy–Littlewood 極大函數的接手

整個偵查的底層工具是 **Hardy–Littlewood 極大函數**：

$$Mf(x)=\sup_{r>0}\frac{1}{|B_r(x)|}\int_{B_r(x)}|f(y)|\,dy ,$$

它滿足弱 $(1,1)$ 估計（Vitali 覆蓋引理）與 $L^p$ 有界（ $p>1$ ）。奇異積分與極大函數聯手，構成調和分析的「實變雙刀」。

## 結案報告

1973 年前後，Calderón–Zygmund 算子觀結案：奇異積分算子的 $L^p$ 有界性由「分解＋弱型估計＋插值」的實變方法統一取得。案件遺產如下：

- **調和分析的算子觀確立**：個案（Hilbert 變換）升級為系統理論（奇異積分算子代數）； $T(1)$ 理論、交換子理論、BMO 空間成為標準工具。
- **PDE 的應用**：橢圓方程的正則性（Calderón–Zygmund 分解的 $L^p$ 版）、邊值問題的 Cauchy 積分法（後來的 Cauchy 積分有界性，1982 Coifman–McIntosh–Meyer）。
- **小波的前史**：1986 年 Daubechies 緊支撐小波（見 1986-Daubechies小波）的多分辨分析，正是「近對角衰減＋Cotlar–Stein」的濾波器組版本；Meyer 小波（1986）的 $L^2$ 理論直接以 $T(1)$ 理論為工具。
- **後續浪潮**：Fefferman–Stein 的 $H^1$ –BMO 對偶、Coifman–Rochberg–Weiss 的交換子理論、直到多線性奇異積分（1980s）與 Carleson 的 a.e. 收斂定理（1966）共同構成現代調和分析。

## 證據與工具

**關鍵公式一覽表：**

| 工具 | 公式／陳述 | 用途 |
|------|-----------|------|
| Hilbert 變換 | $Hf(x)=\frac{1}{\pi}\mathrm{p.v.}\int\frac{f(y)}{x-y}dy$ | 個案原型 |
| 弱 $(1,1)$ | $\mu\{|Tf|>\alpha\}\le\frac{C}{\alpha}\|f\|_{L^1}$ | 核心估計 |
| CZ 分解 | $f=g+\sum b_j$ ， $b_j$ 零平均 | 層級拆解 |
| Hörmander 條件 | $|K(x-y)-K(x-y')|\le\frac{C|y-y'|}{|x-y|^2}$ | 核光滑性 |
| 乘子表示 | $\widehat{Hf}=-i\,\mathrm{sgn}(\xi)\hat f$ | $L^2$ 有界 |
| Cotlar–Stein | $\|\sum T_j\|\le(\sum\omega(j))^{1/2}$ 型 | 非卷積推廣 |
| 極大函數 | $Mf(x)=\sup_r\frac{1}{|B_r|}\int_{B_r}|f|$ | 底層雙刀 |

**證明骨架（弱 $(1,1)$ ）：**

1. CZ 分解： $f=g+\sum b_j$ ， $\|g\|_{L^\infty}\le\alpha$ ， $\sum|Q_j|\le\frac{\|f\|_{L^1}}{\alpha}$ 。
2. $g$ 部分：Hörmander 條件＋Chebyshev。
3. $b_j$ 部分：零平均相消＋尾巴控制。
4. 合併得 $\mu\{|Tf|>\alpha\}\le\frac{C}{\alpha}\|f\|_{L^1}$ 。 $\blacksquare$

**典型例子：** Hilbert 變換在 $L^1$ 中無界：取 $f=\chi_{[0,1]}$ ，則 $Hf(x)=\frac{1}{\pi}\log\Big|\frac{x}{x-1}\Big|$ ，它在 $0,1$ 附近如 $\log$ 型發散，故 $Hf\notin L^1$ 。但弱 $(1,1)$ 估計成立： $\mu\{|Hf|>\alpha\}\sim\frac{2}{\pi\alpha}\|f\|_{L^1}$ ——弱型是 $L^1$ 的正確語言，這正是奇異積分理論的起點。
