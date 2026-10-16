# 1873 — Beltrami SVD 起源

## 案件摘要
1873 年，義大利數學家 Eugenio Beltrami 在波隆那發表論文〈Sulle funzioni bilineari〉（論雙線性函數），首次證明：任何實矩陣 $A$ 都可以透過兩組正交基分解為 $A = U\Sigma V^T$ 的形式——奇異值分解（Singular Value Decomposition, SVD）的雛形誕生。一年後（1874），法國數學家 Camille Jordan 獨立給出更完整的版本。這個分解是二次型主軸定理的自然推廣：把「一個二次型」的主軸化簡，推廣到「一個雙線性型」的雙重主軸化簡。它是今日 PCA、資料壓縮、矩陣低秩逼近的數學心臟。

## 前因 -- 為什麼會有這個案子
- 二次型主軸定理（Cauchy 1815、Sylvester 1852）已成熟：對稱矩陣可用正交變換對角化 $Q^TAQ = \Lambda$。但它只處理「$x$ 與 $y$ 是同一個向量」的特例。
- 雙線性型 $x^T A y$ 是更一般的對象：$x$ 與 $y$ 是兩個不同的向量、甚至不同維度的空間。對稱化 $x^TAx$ 的招數在這裡失效。
- 應用背景：微分幾何（Beltrami 的本行是曲面的微分幾何，研究曲率張量）、彈性力學、位勢理論中大量出現雙線性型。
- 案發現場：Beltrami 意識到，若對 $x$ 與 $y$ 各自允許**不同的**正交變換，$x^TAy$ 或許能化成最簡形式——兩組主軸，一次到位。

## 線索與推理 -- 數學式、程式、理論

### 線索一：從二次型到雙線性型
二次型 $q(x) = x^T A x$ 只有一組向量。雙線性型則是：

$$f(x, y) = x^T A y = \sum_{i,j} a_{ij} x_i y_j$$

它是兩個變數的函數，對每個變數各自線性。若 $A$ 對稱且 $x = y$，退化回二次型。Beltrami 的問題：能否找到 $x$ 空間的正交基 $\{v_i\}$ 與 $y$ 空間的正交基 $\{u_i\}$，使 $f$ 化成「純對角」形式？

### 線索二：Beltrami 的雙重主軸化簡
Beltrami 的推理（用現代語言重述）：考慮 $x^T A y$，固定 $y$，$f$ 對 $x$ 是線性函數。先對 $x$ 做主軸化簡——但 $A$ 不對稱怎麼辦？Beltrami 的洞見：看 $A$ 的兩個「衍生物」：

$$A A^T \quad\text{與}\quad A^T A$$

這兩個都是**對稱半正定**矩陣！由主軸定理，它們可以正交對角化，且特徵值非負：

$$A A^T u_i = \sigma_i^2 u_i, \qquad A^T A v_i = \sigma_i^2 v_i$$

$\sigma_i \geq 0$ 稱為**奇異值**，$u_i$、$v_i$ 分別是左、右奇異向量。關鍵恆等式：$A v_i = \sigma_i u_i$——右奇異向量被 $A$ 映射後，方向落在左奇異向量上、長度縮放 $\sigma_i$ 倍。於是：

$$A = U \Sigma V^T$$

其中 $U = [u_1, \dots, u_m]$、$V = [v_1, \dots, v_n]$ 是正交矩陣，$\Sigma$ 是對角矩陣（對角線為 $\sigma_i$，其餘為零）。在這組雙主軸座標下：

$$x^T A y = \sum_i \sigma_i \, \xi_i \, \eta_i$$

交叉項全部消失，只剩奇異值加權的乘積和——雙線性型的「標準形」正式結案。Beltrami 1873 年證明了 $m = n$ 的方陣情形；Jordan 1874 年獨立推廣到矩形矩陣，並證明更完整的性質。

### 線索三：奇異值的內在性
奇異值是矩陣的**不變量**：$A$ 在任何正交變換下（$A \mapsto P A Q$，$P, Q$ 正交），奇異值集合不變。它們與特徵值的關係：若 $A$ 對稱半正定，奇異值 = 特徵值；一般情形，奇異值是 $A$ 在歐氏幾何下的「真實伸縮量」。范數關係：

$$\|A\|_2 = \sigma_1, \qquad \|A\|_F = \sqrt{\sigma_1^2 + \cdots + \sigma_r^2}$$

奇異值按大小排列，$\sigma_1$ 是最大伸縮——這為 1936 年 Eckart-Young 定理（最佳低秩逼近）埋下伏筆。

### 線索四：從 Beltrami 到現代——SVD 的計算化
Beltrami 與 Jordan 給的是存在性證明，計算方法要等 20 世紀：Golub（1965）與 Golub-Reinsch（1970）的 QR 算法基 SVD 演算法讓 SVD 成為可計算的工具。1936 年 Eckart-Young 證明：截斷 SVD 是 Frobenius 範數下的最佳低秩逼近：

$$A_k = \sum_{i=1}^{k} \sigma_i u_i v_i^T, \qquad \min_{\operatorname{rank}(B) \le k}\|A - B\|_F = \sqrt{\sigma_{k+1}^2 + \cdots + \sigma_r^2}$$

這是 PCA（主成分分析，Pearson 1901、Hotelling 1933）的數學基礎：把資料矩陣做 SVD，取前 $k$ 個奇異值對應的成分，就是最佳壓縮。

### 程式碼範例：Beltrami 的 $A=U\Sigma V^T$ 手工驗證
```python
import numpy as np

A = np.array([[3.0, 0.0],
              [0.0, 2.0]])    # 簡單起點，先驗證恆等式

# Beltrami 的推理：看 A^T A
AtA = A.T @ A
vals, V = np.linalg.eigh(AtA)      # 右奇異向量
print("A^T A 特徵值 (=σ²):", vals)   # [4, 9] → σ = [2, 3]

sigma = np.sqrt(np.clip(vals, 0, None))
U = A @ V / np.where(sigma > 0, sigma, 1)   # Av_i = σ_i u_i
print("Av_i 與 σ·u_i 的最大差異:", np.max(np.abs(A @ V - U * sigma)))  # ~1e-16

# 重組 A = U Σ V^T
recon = U @ np.diag(sigma) @ V.T
print("重組誤差:", np.max(np.abs(A - recon)))   # ~1e-16

# --- Beltrami 的終局：雙線性型化成對角 ---
x = np.array([0.5, -0.3]); y = np.array([0.8, 0.6])
print("原始 x^T A y:", x @ A @ y)
xi, eta = U.T @ x, V.T @ y
print("主軸座標下 Σσ·ξη:", np.sum(sigma * xi * eta))   # 相同！

# --- Eckart-Young：截斷 SVD 是最佳低秩逼近 ---
B = np.array([[3.0, 1.0], [0.0, 2.0], [1.0, 1.0]])   # 3x2 矩形矩陣（Jordan 情形）
U2, s, Vt = np.linalg.svd(B)
print("奇異值:", s)
Bk = U2[:, :1] @ np.diag(s[:1]) @ Vt[:1]   # 秩 1 逼近
print("秩1逼近的 Frobenius 誤差:", np.linalg.norm(B - Bk))
print("理論值 √(σ₂²):", s[1])   # 相符 → Eckart-Young 成立
```

輸出顯示三件事：$Av_i = \sigma_i u_i$ 恆等式成立、$U\Sigma V^T$ 重組誤差為浮點零、截斷 SVD 的誤差恰好等於被丟棄的奇異值——Beltrami 1873 年的洞見與 Eckart-Young 1936 年的定理在同一行程式碼裡會合。

## 結案 -- 後果與影響
- SVD 成為線性代數四大分解之一：與特徵分解、LU、QR 並列，且是**唯一對任意矩陣（含矩形）都存在**的分解。
- 1936 年 Eckart-Young 定理：最佳低秩逼近，資料壓縮與去噪的數學基礎。
- PCA（主成分分析）：Hotelling 1933 年的統計工具，本質上就是對協方差矩陣做 SVD——現代資料科學的核心演算法。
- 影響至今：影像壓縮（SVD 截斷）、推薦系統（矩陣補全）、Latent Semantic Analysis（LSA）、Google PageRank 的前身、機器學習的 Whitening，全部是 Beltrami 1873 年那一晚的後裔。
- 計算化：Golub-Reinsch 1970 的 SVD 演算法成為 LAPACK 的標準例程，讓 SVD 從理論走進每一台電腦。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Eugenio Beltrami | 1873 首創 SVD（方陣情形） |
| Camille Jordan | 1874 獨立發現，推廣到矩形矩陣 |
| Carl Eckart & Gale Young | 1936 最佳低秩逼近定理 |
| Gene Golub | 1965/1970 SVD 演算法，計算化功臣 |

- E. Beltrami, "Sulle funzioni bilineari", Giornale di Matematiche **11**, 98–106 (1873)。
- C. Jordan, "Mémoire sur les formes bilinéaires", J. Math. Pures Appl. **19**, 35–54 (1874)。
- C. Eckart & G. Young, "The approximation of one matrix by another of lower rank", Psychometrika **1**, 211–218 (1936)。
