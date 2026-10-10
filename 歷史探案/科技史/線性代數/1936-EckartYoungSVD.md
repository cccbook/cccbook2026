# 1936 — Eckart–Young 與 SVD 奇異值分解

## 案件摘要
1936 年，普林斯頓的 Carl Eckart 与 Gale Young 發表〈The approximation of one matrix by another of lower rank〉，證明了一條驚人的定理：在所有秩不超過 $k$ 的矩陣中，用**截斷奇異值分解**逼近原矩陣是 Frobenius 範數意義下的**最佳**選擇。兇器 SVD 其實早在此前六十年（Beltrami 1873、Jordan 1874）就被發明，但直到 Eckart–Young 指認它「不僅存在，而且最佳」，奇異值分解才成為數值線性代數的心臟。

## 前因 -- 為什麼會有這個案子
- **1873/1874 年 SVD 首創**：意大利的 Eugenio Beltrami（1873）與法國的 Camille Jordan（1874）獨立證明：任何（實）矩陣都可用正交變換對角化——$A = U \Sigma V^T$。但當時無人看出它的實用價值，Jordan 甚至為其優先權與 Beltrami 筆戰，此後 SVD 沉寂數十年。
- **特徵值理論成熟**：19 世紀的譜理論（Cayley、Hermite、Sylvester）只對方陣的特徵分解有效；SVD 的價值在於它對**任意矩形矩陣**都成立。
- **主成分問題**：統計學中 Pearson（1901）與 Hotelling（1933）提出主成分分析（PCA），本質上是在問「最佳低秩逼近」——但缺少一條證明最佳性的定理。
- **數值計算的需求**：1930 年代科學計算興起，如何在最小平方意義下用低階矩陣近似資料矩陣，成為急迫的實務問題——這就是案發現場。

## 線索與推理 -- 數學式、程式、理論

### 線索一：SVD 奇異值分解（Beltrami–Jordan, 1873/74）
對任意 $m \times n$ 實矩陣 $A$，存在正交矩陣 $U \in \mathbb{R}^{m \times m}$、$V \in \mathbb{R}^{n \times n}$ 與非負對角矩陣 $\Sigma$，使

$$A = U \Sigma V^T, \qquad \Sigma = \operatorname{diag}(\sigma_1 \geq \sigma_2 \geq \dots \geq \sigma_r > 0)$$

其中 $\sigma_i$ 稱為**奇異值**，$r = \operatorname{rank}(A)$。偵探筆記：奇異值就是 $A^T A$ 特徵值的平方根——

$$A^T A = V \Sigma^2 V^T, \qquad \sigma_i^2 = \lambda_i(A^T A)$$

這把「任意矩陣」的問題化約為「對稱方陣」的特徵值問題——譜理論的觸角由此伸向所有矩陣。奇異值也給出矩陣的幾何尺度：$\|A\|_2 = \sigma_1$（譜範數）、$\|A\|_F = \sqrt{\sigma_1^2 + \dots + \sigma_r^2}$（Frobenius 範數）。

### 線索二：Eckart–Young 定理（1936）
在所有秩 $\leq k$ 的矩陣中，截斷 SVD 是最佳逼近：

$$\min_{\operatorname{rank}(B) \leq k} \|A - B\|_F = \sqrt{\sigma_{k+1}^2 + \sigma_{k+2}^2 + \dots + \sigma_r^2}$$

且取 $B = U_k \Sigma_k V_k^T$（只保留前 $k$ 個奇異值）即達到該最小值；譜範數版本同樣成立：$\min_{\operatorname{rank}(B)\le k}\|A-B\|_2 = \sigma_{k+1}$。

**偵探推理**：丟棄的奇異值平方和，就是逼近誤差的「殘留痕跡」——資訊量集中在大的奇異值，小的奇異值幾乎只是雜訊。PCA 的「主成分解釋變異量」$\sigma_i^2 / \sum_j \sigma_j^2$，正是這條定理的統計化身。

### 線索三：Eckart–Young 的證明思路
Eckart 與 Young 的關鍵一步：任何秩 $\leq k$ 的逼近 $B$，其誤差矩陣 $E = A - B$ 必然「壓縮」了至少一個 $n-k$ 維子空間的資訊。利用 Courant–Fischer 極小極大特徵值定理，可以證明

$$\|A - B\|_F^2 \geq \sum_{i>k} \sigma_i^2$$

等號在 $B$ 取截斷 SVD 時成立。證明的骨架是**正交不變性**：Frobenius 範數在正交變換下不變，因此可在 $A = U \Sigma V^T$ 的對角化坐標系中辦案——對角線上的 $\sigma_i$ 無所遁形。

### 線索四：從 Eckart–Young 到 Schmidt
同時期，數學家 Erhard Schmidt（Eckart 的老師輩，Hilbert 空間理論家）1907 年即對積分算子給出類似的逼近定理（Mirsky 1960 年將 Eckart–Young 推廣到所有單調矩陣範數）。偵探檔案顯示：從積分方程到矩陣逼近，這條線索貫穿了泛函分析與數值分析兩個世界。

### 程式碼範例：SVD 與 Eckart–Young 最佳低秩逼近
```python
import numpy as np

rng = np.random.default_rng(1)
# 造一個內在秩為 3、再混入雜訊的 100x40 資料矩陣
U0 = rng.normal(size=(100, 3))
V0 = rng.normal(size=(40, 3))
A = U0 @ V0.T + 0.1 * rng.normal(size=(100, 40))

# SVD 分解
U, s, Vt = np.linalg.svd(A, full_matrices=False)
print("奇異值前 6 個：", np.round(s[:6], 3))

# Eckart–Young：k=3 截斷逼近
k = 3
A_k = (U[:, :k] * s[:k]) @ Vt[:k, :]
err = np.linalg.norm(A - A_k, 'fro')

# 定理預測的誤差下界：丟棄奇異值的平方和開根號
pred = np.sqrt(np.sum(s[k:]**2))
print(f"實際誤差 ||A - A_k||_F = {err:.6f}")
print(f"定理預測 √(Σσ², i>k)  = {pred:.6f}")
print("Eckart–Young 成立：", np.allclose(err, pred))

# 反證：隨機秩 3 矩陣的逼近誤差必然更大
B_rand = rng.normal(size=(100, 3)) @ rng.normal(size=(3, 40))
print(f"隨機低秩逼近誤差 = {np.linalg.norm(A - B_rand, 'fro'):.6f}  （> pred，非最佳）")

# 壓縮率：只存 U_k、s、Vt^T 的儲存成本
full = A.size
comp = U[:, :k].size + k + Vt[:k, :].size
print(f"壓縮率：{comp}/{full} = {comp/full:.1%}")
```

輸出顯示：實際誤差與定理預測完全一致（`np.allclose` 為真），而任何其他秩 3 矩陣的誤差都更差——截斷 SVD 被當場指認為最佳低秩逼近。同時只儲存少數奇異值與向量，即以極小的儲存成本保留矩陣的主要資訊。

## 結案 -- 後果與影響
- **數值線性代數的心臟**：最小平方問題、偽逆（Moore–Penrose）$A^+ = V \Sigma^+ U^T$、條件數 $\kappa = \sigma_1 / \sigma_r$、矩陣秩的判定，全部透過 SVD 計算。Golub（1965）的穩定 SVD 演算法使其成為標準工具。
- **PCA 主成分分析**：資料矩陣的 SVD 即 PCA，解釋變異量由奇異值的平方給出——Eckart–Young 保證主成分是「最佳」的。
- **影像壓縮**：丟棄小奇異值，用少量秩保留圖像主體——Eckart–Young 定理是壓縮誤差的理論保證。
- **推薦系統**：Latent Semantic Analysis（1990）與協同過濾的矩陣補全，用低秩逼近挖掘「潛在因子」。
- **泛函分析**：Schmidt 的緊緻算子逼近理論、Mirsky 1960 年的推廣，使 SVD 從矩陣延伸到無窮維算子。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Carl Eckart / Gale Young | 1936 年證明最佳低秩逼近定理 |
| Eugenio Beltrami | 1873 年首創 SVD |
| Camille Jordan | 1874 年獨立發現 SVD |
| Erhard Schmidt | 1907 年積分算子的逼近定理 |
| Karl Pearson / Harold Hotelling | 主成分分析（1901/1933） |
| Gene Golub | 1965 年穩定 SVD 數值演算法 |

- C. Eckart, G. Young, *The approximation of one matrix by another of lower rank*, Psychometrika **1**, 211–218 (1936)。
- E. Beltrami, *Sulle funzioni bilineari*, Giorn. Mat. Battaglini **11**, 98–97 (1873)。
- C. Jordan, *Mémoire sur les formes bilinéaires*, J. Math. Pures Appl. **19**, 35–54 (1874)。
