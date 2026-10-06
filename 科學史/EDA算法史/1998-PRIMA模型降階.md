# 1998-PRIMA模型降階

## 案件摘要
SPICE（1973）精確但慢：百萬節點的互連網路，一次瞬態分析要數小時。1990 年代，深次微米製程讓互連 RC 網路動輒百萬節點——模擬成為設計週期的瓶頸。1998 年 ICCAD，CMU 的 A. Odabasioglu、M. Celik、L. Pileggi 發表 **PRIMA**：以 Krylov 子空間投影把百萬階的 MNA 系統降為百階的宏觀模型（macromodel），且**保證無源性（passivity）**——前代 PVL（1995）會產生虛假的振盪。PRIMA 讓互連模擬快 2-3 個數量級，是 fast-SPICE 時代的數學引擎，也是線性代數（Krylov 子空間、Arnoldi 迭代）直接服務晶片設計的經典案例。

## 前因 -- 為什麼會有這個案子
- **互連的規模爆炸**：深次微米製程（1995-）使每個閘的互連 RC 網路龐大，全晶片 SPICE 級模擬不可行——模擬佔設計週期 70%。
- **AWE 的先例**（1990, Pillage-Rohrer）：漸近波形估計（Asymptotic Waveform Evaluation）用矩陣的矩（moments）匹配降階——概念可行，但矩匹配在階數高時**數值不穩**。
- **PVL 的缺陷**（1995, Feldmann-Freund）：Lanczos 型降階穩定，但**不保證無源性**——降階模型可能輸出能量（違反物理），在時域模擬中虛假振盪。
- **物理律是底線**：無源系統不產生能量；違反無源性的模型在下游模擬中會炸——必須保證。

## 線索與推理 -- 數學式、程式、理論

### 核心：Krylov 子空間投影
MNA 的頻域方程：

$$(sC + G)\, x(s) = b(s), \quad H(s) = l^T (sC + G)^{-1} b$$

傳遞函數 $H(s)$ 的降階 = 找子空間 $V \in \mathbb{R}^{n \times q}$（$q \ll n$），投影：

$$H_q(s) = l^T V (s V^T C V + V^T G V)^{-1} V^T b$$

子空間 $V$ 取 **Krylov 子空間**（Arnoldi 迭代生成）：

$$\mathcal{K}_q(G^{-1}C, G^{-1}b) = \text{span}\{G^{-1}b,\ (G^{-1}C)G^{-1}b,\ \dots,\ (G^{-1}C)^{q-1}G^{-1}b\}$$

**矩匹配定理**：投影模型的 Taylor 展開前 $q$ 項矩與原模型一致（$H_q$ 與 $H$ 匹配前 $q$ 個矩）——這是 AWE 矩匹配的嚴格化，但用正交投影（Arnoldi）避免高階矩的數值爆炸。

### 無源性的保證：PRIMA 的關鍵貢獻
系統無源 ⟺ 傳遞函數**正實**（positive real）：

$$\text{Re}\{H(s)\} \ge 0 \quad \forall\ \text{Re}\{s\} > 0$$

PVL 的 Lanczos 雙正交投影不保證此性質。PRIMA 的推理：用 **Arnoldi 正交投影**且保持 $C, G$ 的對稱結構——可證明投影模型繼承無源性：

$$C, G \succeq 0\ (\text{半正定}) \implies V^T C V,\ V^T G V \succeq 0 \implies H_q \text{ 無源}$$

半正定性在正交投影下保持——這是線性代數的標準結果，PRIMA 把它變成工程保證。

### 複雜度的推理
$|V| = q \approx 10\text{-}100$，遠小於 $n \approx 10^6$。一次時域分析：$O(n)$ 的 Arnoldi 預處理 + $O(q^3)$ 的降階模擬——總成本比直接 SPICE（$O(n^{1.5})$ × 時間點數）快 2-3 個數量級。

## 結案 -- 後果與影響
- **fast-SPICE 時代的引擎**：PRIMA 成為互連降階的標準（Synopsys HSIM、Cadence UltraSim 的互連處理），百萬節點互連的模擬從天級降到分級。
- **線性代數的工業聖殿**：Krylov 子空間、Arnoldi/Lanczos 迭代（數值線性代數 1950s 的理論）在此案服務晶片設計——EDA 與數值分析的深度合流。
- **無源性的工程標準**：PRIMA 確立「降階必須保被動」的鐵律，後續所有降階演算法（如 Sprim, 2005 的結構保持）都以此為底線。
- **Pileggi 的續航**：Larry Pileggi 成為 CMU 佈局合成與降階理論的宗師，PRIMA 系列延伸到非線性降階與電源網分析。

## 關鍵人物與文獻
- **Altan Odabasioglu, Mauro Celik, Lawrence Pileggi**：CMU，PRIMA 三人組。
- 文獻：
  - A. Odabasioglu, M. Celik, L. T. Pileggi, "PRIMA: Passive Reduced-Order Interconnect Macromodeling Algorithm," *ICCAD* 1998.
  - L. T. Pillage, R. A. Rohrer, "Asymptotic Waveform Evaluation for Timing Analysis," *IEEE Trans. CAD* 9, 352 (1990)（AWE 先例）。
  - P. Feldmann, R. W. Freund, "Efficient Linear Circuit Analysis by Pade Approximation via the Lanczos Process," *IEEE Trans. CAD* 14, 639 (1995)（PVL 先例）。
