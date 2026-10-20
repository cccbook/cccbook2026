# 附錄 C：數學符號與範疇論對照指南

## C.1 基本符號

| 符號 | 意義 | 首次出現 |
|---|---|---|
| $\mathbb{N}, \mathbb{Z}, \mathbb{Q}, \mathbb{R}, \mathbb{C}$ | 自然數、整數、有理數、實數、複數 | 全書 |
| $\mathbb{F}_q$ | $q$ 元有限體 | 2.4 |
| $\in, \subseteq, \cup, \cap$ | 屬於、包含、并、交 | 2.2 |
| $\cong$ | 同構 | 1.3 |
| $\simeq$ | 同倫等價 | 7.1 |
| $\hookrightarrow$ | 嵌入（單射態射） | 5.1 |
| $\twoheadrightarrow$ | 滿射態射 | 1.2 |
| $\oplus, \otimes$ | 直和、張量積 | 1.2 |
| $H_n, H^n$ | 同調、上同調群 | 7.2 |
| $\pi_n(X)$ | $n$ 階同倫群 | 7.1 |
| $\Omega^k(M)$ | $k$ 階微分形式 | 2.3 |
| $d, \partial, \bar\partial$ | 外微分、邊界、Dolbeault 算子 | 7.3, 7.2, 12.2 |
| $\Delta, \mathrm{Ric}, R$ | Laplacian、Ricci、純量曲率 | 11.1, 12.1 |
| $\mathrm{GL}_n, \mathrm{SO}(n), \mathrm{SU}(n), \mathrm{SL}_2\mathbb{R}$ | 典型李群 | 8.3 |
| $\mathfrak{g}, [X,Y]$ | 李代數與換位子 | 8.3 |
| $\mathrm{Gal}(L/K)$ | Galois 群 | 1.1, 10.1 |
| $\mathrm{Spec}\, R$ | 素譜 | 6.3 |
| $L(s, \rho), L(s, \pi)$ | L-函數 | 10.1 |
| $\zeta(s)$ | Riemann ζ 函數 | 3.2 |
| $D_{KL}(p\|q)$ | KL 散度 | 4.3 |
| $\mathbb{E}[X], P(\cdot)$ | 期望、機率 | 4.1 |

## C.2 範疇論符號

| 符號/術語 | 意義 | 對應直觀 |
|---|---|---|
| $\mathcal{C}, \mathcal{D}$ | 範疇 | 一類物件 + 全部態射 |
| $\mathrm{Hom}(A,B)$ | 態射集合 | 從 $A$ 到 $B$ 的結構保持映射 |
| $F: \mathcal{C} \to \mathcal{D}$ | （共變）函子 | 結構的「翻譯機」 |
| $F: \mathcal{C}^{op} \to \mathcal{D}$ | 反變函子 | 翻譯時方向反轉（Gelfand 對偶） |
| $\eta: F \Rightarrow G$ | 自然變換 | 函子之間的一致變換 |
| $A \times B$ / $A \sqcup B$ | 積 / 餘積 | 同時擁有 / 最通用合併 |
| $\ker f$ / $\mathrm{coker}\, f$ | 核 / 餘核 | 被打為零者 / 打零後的商 |
| $F \dashv G$ | 伴隨對 | 建構 ↔ 觀察的對偶 |
| $\varprojlim, \varinjlim$ | 極限 / 餘極限 | 普遍錐 / 普遍上錐 |
| $\mathcal{C}^{op}$ | 反範疇 | 所有箭頭反向 |
| Set, Grp, Top, Sch | 集合/群/拓撲/概形範疇 | — |
| Abelian 範疇 | 核/餘核行為良好的範疇 | 同調代數的舞台（7.2） |
| Topos | 「像集合宇宙」的範疇 | 幾何化的邏輯世界（6.3, 9.3） |

## C.3 Curry–Howard 對應（邏輯 ↔ 程式）

| 邏輯 | 類型論/程式 |
|---|---|
| 命題 | 類型 |
| 證明 | 項（程式） |
| $A \to B$ | 函數類型 |
| $A \wedge B$ | 積類型 |
| $A \vee B$ | 和類型 |
| 構造性證明 | 可執行程式 |

## C.4 常用恆等式速查

- Cauchy–Schwarz： $|\langle x,y\rangle|^2 \le \|x\|^2\|y\|^2$ （5.3）
- Stokes： $\int_M d\omega = \int_{\partial M}\omega$ （7.3）
- $d^2 = 0 = \partial^2$ （2.3, 7.2）
- Weyl 律： $N(\Lambda) \sim \frac{\mathrm{vol}}{(4\pi)^{n/2}\Gamma(n/2+1)}\Lambda^{n/2}$ （11.1）
- 指標公式： $\mathrm{ind}(D) = \int_M \hat A \mathrm{ch}(E)$ （11.2）
- 交比不變性（8.2）；Dirac 量子化 $\int F \in 2\pi\mathbb{Z}$ （8.4）
