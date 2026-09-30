# 1805 - Legendre 最小平方法

## 案件摘要

1805 年，法國數學家 Adrien-Marie Legendre 在《Nouvelles méthodes pour la détermination des orbites des comètes》附錄中首次公開發表「最小平方法」（méthode des moindres quarrés）。這個為天文觀測誤差而生的方法，成為此後一切迴歸分析與資料擬合的數學基礎。

## 前因 -- 為什麼會有這個案子

18 世紀天文學面臨一個實際難題：觀測天體（如彗星、行星）位置時，每次測量都有誤差。由 $n$ 個觀測方程解 $k$ 個未知數（軌道參數）時：

- 若 $n = k$：解唯一，但完全被誤差污染。
- 若 $n > k$：方程過多，通常**無解**（互相矛盾）。

問題：如何在互相矛盾的觀測之間，找到「最合理」的一組參數？

前人的嘗試：

1. **Bernoulli 與 Euler**（clairaut 亦然）用誤差函數的變分法，但結果繁複且缺乏原則。
2. **Mayer 與 Boscovich**：分組平均法、以絕對誤差和 $\sum|e_i|$ 極小化為準則——但絕對值難以微分處理。
3. **Laplace**（1793 前後）研究過誤差分佈，但未提出系統化的擬合法。

Legendre 在處理 1802 年發現的彗星（Ceres 相關的軌道計算時代背景）觀測資料時，提出了一個優美得可疑的簡單原則：**取誤差平方和最小**。

## 線索與推理 -- 數學式、程式、理論

### 最小平方法原理

Legendre 的陳述（1805 附錄）：選擇參數使

$$\min_{\beta} \; S(\beta) = \sum_{i=1}^{n} (y_i - \hat{y}_i)^2 = \sum_{i=1}^{n} e_i^2$$

其中 $\hat{y}_i$ 為模型預測值，$e_i = y_i - \hat{y}_i$ 為殘差。

**為何是平方？** Legendre 給出的辯護：

1. 平方消除了正負誤差互相抵消的問題。
2. 平方函數可微，極值條件化為線性方程——計算可行。
3. 平方對大誤差懲罰重，符合「誤差應平均分散」的直覺。

（真正的機率辯護要到 Gauss 1809 年才出現：常態誤差下，最小平方 = 最大概似。）

### 正規方程（Normal Equations）

線性模型 $\hat{y}_i = \beta_0 + \beta_1 x_{i1} + \cdots + \beta_p x_{ip}$，矩陣形式 $X\beta$。對 $S(\beta)$ 求梯度並令為零：

$$\frac{\partial S}{\partial \beta} = -2X^T(y - X\beta) = 0 \quad\Longrightarrow\quad X^T X \hat{\beta} = X^T y$$

$$\boxed{\hat{\beta} = (X^T X)^{-1} X^T y}$$

單變數情形的正規方程（1821 年 Gauss 更簡潔的推導）：

$$\hat{\beta}_1 = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sum (x_i - \bar{x})^2} = \frac{\operatorname{Cov}(x,y)}{\operatorname{Var}(x)}, \qquad \hat{\beta}_0 = \bar{y} - \hat{\beta}_1 \bar{x}$$

### 幾何觀點（Gauss 後代的現代詮釋）

最小平方解是 $y$ 在 $X$ 的行空間（column space）上的**正交投影**：

$$\hat{y} = X\hat{\beta} = P_X y, \qquad P_X = X(X^TX)^{-1}X^T$$

殘差 $e = y - \hat{y}$ 與 $X$ 的每一行正交：$X^T e = 0$——這正是正規方程的幾何意義。

### Python：numpy 實作最小平方法

```python
import numpy as np
import matplotlib.pyplot as plt

# 模擬彗星位置觀測：真實軌道 y = 2 + 3t + 噪聲
rng = np.random.default_rng(42)
t = np.linspace(0, 10, 20)
y = 2 + 3 * t + rng.normal(0, 2, 20)   # 觀測誤差服從常態分佈

# ---- 最小平方法（正規方程）----
X = np.column_stack([np.ones_like(t), t])   # 設計矩陣
beta = np.linalg.inv(X.T @ X) @ X.T @ y     # (X^T X)^{-1} X^T y
print(f"估計參數: beta0={beta[0]:.3f}, beta1={beta[1]:.3f}")  # ≈ 2, 3

# 等價寫法：lstsq（數值上更穩定，用 SVD）
beta2, res, rank, sv = np.linalg.lstsq(X, y, rcond=None)

# ---- 殘差檢驗 ----
y_hat = X @ beta
e = y - y_hat
print(f"殘差和 = {e.sum():.4f}（應接近 0，因為 X^T e = 0）")
print(f"殘差與 t 的內積 = {np.dot(t, e):.4f}（正交性驗證）")

plt.scatter(t, y, label="觀測值")
plt.plot(t, y_hat, 'r-', label=f"擬合: y = {beta[0]:.2f} + {beta[1]:.2f}t")
plt.legend(); plt.xlabel("時間 t"); plt.ylabel("位置 y")
plt.title("最小平方法擬合彗星軌道"); plt.show()
```

## 結案 -- 後果與影響

1. **優先權之爭**：1809 年 Gauss 出版《Theoria motus》時聲稱自 1795 年起已使用最小平方法（雖未發表），Legendre 大為光火，公開抗議。這是統計史上最著名的優先權爭議之一。Gauss 的優勢在於他提供了機率論證（常態誤差 + 最大概似）；Legendre 的優勢在於**公開發表在先**。現代文獻一般寫「Gauss–Legendre 最小平方法」。
2. **迴歸分析的誕生**：1885 年 Galton 用「迴歸」一詞研究身高遺傳，1886 年 Pearson 給出相關係數的數學理論——都建構在最小平方的框架上。
3. **高斯–馬可夫定理**（1912, Markov；Gauss 1821 先聲）：在線性無偏估計類中，最小平方估計式具有最小變異數（BLUE），為最小平方法提供不依賴常態假設的最優性證明。
4. **現代應用**：線性迴歸、廣義線性模型、機器學習中的損失函數（MSE）、Kalman 濾波、GPS 定位、經濟計量——全部是最小平方法的後裔。「平方誤差」至今是資料科學的預設損失。

## 關鍵人物與文獻

- **Adrien-Marie Legendre**（1752–1833）：法國數學家，首次公開發表。
  - Legendre, A.-M. (1805). *Nouvelles méthodes pour la détermination des orbites des comètes*. Paris.
- **Carl Friedrich Gauss**（1777–1855）：聲稱更早使用，並給出機率基礎。
  - Gauss, C. F. (1809). *Theoria motus corporum coelestium*; (1821–23) *Theoria combinationis observationum erroribus minimis obnoxiae*.
- **Pierre-Simon Laplace**（1749–1827）：1810 年以中央極限定理證明誤差的常態性，補全最小平方法的機率論證。
- **Andrei Markov**（1856–1922）：1912 年證明高斯–馬可夫定理。
