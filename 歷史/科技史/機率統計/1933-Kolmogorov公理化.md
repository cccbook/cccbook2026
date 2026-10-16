# 1933 - Kolmogorov 公理化

## 案件摘要
1933 年，年僅 30 歲的蘇聯數學家 Kolmogorov 出版《機率論基礎》（Grundbegriffe der Wahrscheinlichkeitsrechnung），以測度論為工具，用三條公理為機率論奠定嚴格基礎，使機率論正式成為數學的一個分支。

## 前因 -- 為什麼會有這個案子
- 十九世紀以來，機率論被 Bertrand 悖論等「無限多種等可能定義」的問題困擾，基礎含糊不清。
- Hilbert 於 1900 年提出第六問題：應將物理學（尤其機率論）公理化。
- Borel 與 Lebesgue 建立了測度論與 Lebesgue 積分，提供了現成的數學工具。
- Bernstein（1917）、Frechet 等人已嘗試公理化，但都不夠完備；機率論被數學主流視為「半吊子」學問。

## 線索與推理 -- 數學式、程式、理論
Kolmogorov 的關鍵洞察：**機率只是一種特殊的測度**，隨機試驗就是一個測度空間。

### 公理體系
1. **樣本空間與 σ-代數**：給定樣本空間 $\Omega$ 與其上的 σ-代數 $\mathcal{F}$（對補集與可數聯集封閉的事件集合），$(\Omega, \mathcal{F})$ 描述「有哪些事件」。
2. **三條機率公理**：機率 $P: \mathcal{F} \to [0,1]$ 滿足
   $$
   \text{(K1) 非負性：} \quad P(A) \geq 0, \quad \forall A \in \mathcal{F}
   $$
   $$
   \text{(K2) 規範性：} \quad P(\Omega) = 1
   $$
   $$
   \text{(K3) 可數可加性：} \quad A_i A_j = \emptyset \ (i \neq j) \Rightarrow P\left(\bigcup_{i=1}^{\infty} A_i\right) = \sum_{i=1}^{\infty} P(A_i)
   $$

由這三條公理即可推出熟悉的所有機率性質，例如：
$$
P(A^c) = 1 - P(A), \quad P(\emptyset) = 0, \quad P(A \cup B) = P(A) + P(B) - P(A \cap B)
$$

### 隨機變數與分佈函數
隨機變數是可測函數 $X: \Omega \to \mathbb{R}$，其機率行為完全由**分佈函數**刻劃：
$$
F(x) = P(X \leq x)
$$
期望值則定義為 Lebesgue 積分 $E[X] = \int_{\Omega} X \, dP$。這使「機率論 = 測度論 + 額外公理 $P(\Omega)=1$」。

### 嚴格證明大數法則與重對數法則
在此架構下，Kolmogorov 證明了**強大數法則（SLLN）**：若 $X_i$ 獨立且 $\sum_i \frac{\mathrm{Var}(X_i)}{i^2} < \infty$，則
$$
\frac{S_n - E[S_n]}{n} \xrightarrow{a.s.} 0, \quad S_n = \sum_{i=1}^n X_i
$$
以及**重對數法則（LIL）**：對 iid、零均值、變異數 $\sigma^2$ 的 $X_i$，
$$
\limsup_{n \to \infty} \frac{S_n}{\sigma \sqrt{2 n \log\log n}} = 1 \ \text{a.s.}
$$
這精確刻劃了隨機波動的「極限包絡線」，超越了大數法則與中央極限定理。

### 對隨機過程的影響
公理化使「無限維」的隨機現象可以嚴格處理：
- **Markov 過程**：轉移機率 $P(X_{n+1}=j \mid X_n=i) = p_{ij}$ 成為嚴格定義的條件機率。
- **Brownian 運動**：Kolmogorov 與 Wiener 之後確立了布朗運動的存在性（連續樣本路徑），定義為滿足
  $$
  W(0)=0, \quad W(t)-W(s) \sim N(0, t-s), \quad \text{獨立增量}
  $$
  的隨機過程，成為隨機分析的起點。

```python
# 以模擬「驗證」大數法則與重對數法則的包絡線
import numpy as np
rng = np.random.default_rng(0)
n = 100000
X = rng.standard_normal(n)
S = np.cumsum(X)
t = np.arange(1, n+1)
env = np.sqrt(2 * t * np.log(np.log(t)))   # LIL 上包絡線（sigma=1）
ratio = S / env
print(f"limsup 逼近值: {np.nanmax(ratio[np.isfinite(ratio)]):.4f}")  # 應接近 1
print(f"S_n/n = {S[-1]/n:.6f}")  # 應接近 0（SLLN）
```

## 結案 -- 後果與影響
- 機率論正式成為數學分支，所有機率命題都可由公理嚴格推導，Bertrand 悖論消解。
- 開啟了隨機過程、隨機分析（Itô 積分）、遍歷理論等新領域。
- 現代金融數學（Black–Scholes 建立在布朗運動上）與統計力學的數學基礎皆源於此。
- Kolmogorov 公理至今仍是教科書的標準起點。

## 關鍵人物與文獻
- **Andrey Kolmogorov**（1903–1987）：蘇聯數學家，本案件主謀。
- **Emile Borel / Henri Lebesgue**：提供測度論兇器。
- **A. N. Kolmogorov (1933), *Grundbegriffe der Wahrscheinlichkeitsrechnung*, Springer.**（英譯：*Foundations of the Theory of Probability*）
- Kolmogorov (1929)：Über das Gesetz des iterierten Logarithmus（重對數法則證明）。
