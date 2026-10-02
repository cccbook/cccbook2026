# 1901 — Pearson 相關與 PCA

## 案件摘要
1901 年，Karl Pearson 在 Philosophical Magazine 上發表〈On Lines and Planes of Closest Fit to Systems of Points in Space〉：給定一群散布在空間中的點，如何找出「最佳擬合」的直線與平面？Pearson 用矩陣語言給出答案——最佳擬合的方向就是協方差（相關）矩陣最大特徵值對應的特徵向量。這正是**主成分分析（PCA）**的數學起源，比 Hotelling 1933 年正式命名「principal components」早了 32 年。Pearson 解的其實是同一個幾何問題的兩面：最小平方擬合（距離最小）與變異數最大（投影最散）。

## 前因 -- 為什麼會有這個案子
- **Gauss–Legendre 最小平方法**：1805/1809 年確立的最小平方法是資料擬合的黄金法則，但傳統用法是「固定一個自變數、擬合一條線」；若資料點在**多個方向**都散布、且無所謂「自變數」，怎麼找最佳直線？這是案發的空白地帶。
- **Bravais 與 Galton 的相關概念**：1846 年 Bravais 研究二維誤差分佈的相關；1885 年起 Galton 用「回歸」（regression）描述親子身高資料，1888 年 Pearson 本人定義了**相關係數** $r$。相關是「多變數共同變動」的量，但把相關推廣到**多個變數、多個方向**的幾何，尚待完成。
- **Pearson 的生物統計戰場**：Pearson 創辦 Biometrika（1901），研究演化與遺傳資料；高維資料的「主要變動方向」對分類與描述至關重要。
- 有趣的細節：Pearson 1901 年論文是回應 Macdonell 的頭顱測量資料而寫——四個測量維度的資料需要降維可視化，這是史上第一個「高維資料降維」的實戰案件。

## 線索與推理 -- 數學式、程式、理論

### 線索一：最佳擬合直線 = 最大特徵向量
給定中心化後的資料點 $\{x_i\}_{i=1}^n \subset \mathbb{R}^p$（$\sum_i x_i = 0$），定義協方差矩陣（實對稱半正定）：

$$S = \frac{1}{n-1}\sum_{i=1}^n x_i x_i^T$$

要找單位方向向量 $u$ 使資料投影 $\{u^T x_i\}$ 的變異數最大：

$$\max_{\|u\|=1} \frac{1}{n-1}\sum_i (u^T x_i)^2 = \max_{\|u\|=1} u^T S u$$

用 Lagrange 乘子：$\mathcal{L} = u^TSu - \lambda(u^Tu - 1)$，令梯度為零得

$$Su = \lambda u$$

答案出人意料地乾淨：**最佳方向就是 $S$ 的最大特徵值對應的特徵向量**，且該最大變異數恰好等於 $\lambda_1$。第二、第三主成分同理：取次大特徵值，並與之前的方向正交（對稱矩陣不同特徵值的特徵向量自動正交）。

### 線索二：兩面同一案——距離最小 = 變異數最大
Pearson 的原始問法是「點到直線的**垂直距離平方和**最小」：

$$\min_{\|u\|=1} \sum_i \|x_i - (u^T x_i)u\|^2 = \min_{\|u\|=1} \left(\sum_i \|x_i\|^2 - \sum_i (u^Tx_i)^2\right)$$

因為 $\sum_i \|x_i\|^2$ 為常數，最小化距離等價於**最大化**投影變異數。最小平方擬合與最大變異數投影是同一個特徵值問題的兩面——幾何與統計在這裡會合，這是本案最漂亮的推理。

### 線索三：SVD 的統計語言
設中心化資料矩陣 $X \in \mathbb{R}^{n \times p}$，其奇異值分解：

$$X = U\Sigma V^T$$

則協方差矩陣 $S = \frac{1}{n-1}X^TX = \frac{1}{n-1}V\Sigma^2V^T$。因此：
- $V$ 的行向量 = 主成分方向（= $S$ 的特徵向量）；
- $\sigma_k^2/(n-1)$ = 第 $k$ 主成分的變異數（= 特徵值 $\lambda_k$）；
- 得分矩陣 $T = XV = U\Sigma$ = 資料在新座標上的投影。

前三個奇異值往往佔總變異數的絕大部分——降維就是把 $X$ 用 $U_k\Sigma_kV_k^T$（秩 $k$）近似。1901 年 Pearson 做的正是這件事，只是當時還沒有 SVD 的語言。

### 線索四：相關係數矩陣的角色
Pearson 1888 年的相關係數 $r = \frac{\mathrm{cov}(x,y)}{\sigma_x\sigma_y}$ 推廣成**相關矩陣** $R$：先將各變數標準化（減均值除標準差）再算協方差。$R$ 也是實對稱半正定、對角線全為 1；對標準化資料做 PCA 即對 $R$ 做特徵分解。相關矩陣的特徵值全為非負，且滿足 $\sum\lambda_k = p$（跡不變）——這是檢驗數值計算的便捷指紋。

### 程式碼範例：Pearson 相關係數矩陣與 PCA 對照
```python
import numpy as np

np.set_printoptions(precision=4, suppress=True)
rng = np.random.default_rng(7)

# 造一組三維資料：真正的主要變動方向只有兩個（二維潛在因素映射到三維）
n = 500
L = rng.standard_normal((n, 2)) @ np.diag([3.0, 1.5])
X = L @ np.array([[1.0, 0.2, 0.1], [0.3, 1.0, 0.2]]) + rng.standard_normal((n, 3)) * 0.1

Xc = X - X.mean(axis=0)                       # 中心化
S = Xc.T @ Xc / (n - 1)                       # 協方差矩陣
R = np.corrcoef(X, rowvar=False)              # Pearson 相關係數矩陣
print("相關係數矩陣 R:\n", R)

lam, V = np.linalg.eigh(S)                    # 特徵分解（由小到大）
idx = np.argsort(lam)[::-1]
lam, V = lam[idx], V[:, idx]
print("\n特徵值（變異數）:", lam)
print("解釋變異比例  :", lam / lam.sum())
print("跡 = 總變異數 :", lam.sum(), " vs ", np.trace(S))

# 用 SVD 交叉驗證：X = U Σ V^T
U, sig, Vt = np.linalg.svd(Xc, full_matrices=False)
print("\nSVD 奇異值平方/(n-1):", sig**2 / (n - 1), " ← 與特徵值一致")
print("V 與 SVD 的 V^T 對應 :", np.allclose(np.abs(V), np.abs(Vt.T)))

# 降到二維：秩 2 近似
k = 2
Xk = Xc @ V[:, :k]
X_approx = Xk @ V[:, :k].T
err = np.linalg.norm(Xc - X_approx, 'fro') / np.linalg.norm(Xc, 'fro')
print(f"\n降到 {k} 維後的相對誤差: {err:.4f}")
```

輸出顯示特徵值與 SVD 奇異值平方完全一致、前兩個主成分解釋了絕大部分變異數、降維後相對誤差極小——Pearson 的「最佳擬合平面」在資料上現身。

## 結案 -- 後果與影響
- **1933 年 Hotelling 的 PCA**：Harold Hotelling 在 J. Psych. 上正式提出「Analysis of a complex of statistical variables into principal components」，把 Pearson 的幾何發展成完整的統計方法——心理測量、因子分析的數學核心。
- **資料科學的心臟**：今日 PCA 是降維、可視化、雜訊過濾、特徵工程的標準第一步；特徵臉（eigenfaces）、譜聚類、推薦系統（矩陣分解）都是它的後裔。
- **Eckart–Young 定理（1936）**：Eckart 與 Young 證明秩 $k$ 的最佳近似就是截斷 SVD $U_k\Sigma_kV_k^T$——Pearson 降維做法的最優性有了嚴格保證。
- **Karhunen–Loève 展開**：隨機過程的 PCA 版本，成為訊號處理與模式識別的理論基礎。
- 相關矩陣的特徵值理論（Marchenko–Pastur 分佈、隨機矩陣理論）成為現代高維統計的顯學。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Karl Pearson | 1901 年「最佳擬合」論文、1888 相關係數 |
| Harold Hotelling | 1933 年正式提出 PCA |
| Carl Friedrich Gauss | 最小平方法（前案） |
| Auguste Bravais / Francis Galton | 相關與回歸的先驅 |
| Carl Eckart & Gale Young | 1936 年截斷 SVD 最優性 |

- K. Pearson, *On Lines and Planes of Closest Fit to Systems of Points in Space*, Phil. Mag. **2**, 559–572 (1901)。
- H. Hotelling, *Analysis of a complex of statistical variables into principal components*, J. Educ. Psych. **24**, 417–441, 498–520 (1933)。
- C. Eckart, G. Young, *The approximation of one matrix by another of lower rank*, Psychometrika **1**, 211–208 (1936)。
