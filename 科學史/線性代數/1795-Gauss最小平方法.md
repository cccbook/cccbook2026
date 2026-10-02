# 1795 — Gauss 最小平方法

## 案件摘要
1795 年前後，年僅十八歲的 Carl Friedrich Gauss 已經私下發明了**最小平方法**：當觀測數據多於未知數（超定方程組）時，選取使「誤差平方和最小」的參數估計。1801 年，Gauss 用它從零散的觀測數據中算出新發現的小行星 Ceres 的軌道，使其在失蹤一年後被重新找到，一舉成名。1809 年，他在《天體運動論》（*Theoria motus corporum coelestium*）中正式發表此法，並同時給出誤差的常態分布（「Gauss 分布」）——統計學與數值線性代數的雙重基石就此奠定。本案追查：一條天文觀測誤差之謎，如何逼出 $A^TA\hat{x} = A^Tb$ 這條著名的正規方程？

## 前因 -- 為什麼會有這個案子
- **天文觀測的宿命**：每次天文觀測都有誤差；多次觀測同一量，數值卻各不相同。十八世紀的天文學家（包括 Legendre、Mayer、Lambert）長期追問：**如何從一堆互相矛盾的觀測中，提取出「最可信」的值？**
- **超定方程組的現形**：要確定 Ceres 的橢圓軌道需要 6 個參數，但 Piazzi 只觀測到 24 個數據點（40 天內）就因病中斷。24 條方程、6 個未知數——方程多於未知數，一般沒有精確解。這是本案的案發現場。
- **Legendre 的同期發表**：1805 年，Legendre 先出版《計算彗星軌道的新方法》，首次公開「最小平方法」這個名字。Gauss 宣稱自己早在此前十年（1795）就已使用；兩人為優先權爭執多年。史實考據（Gauss 1809 年信件與手稿）支持 Gauss 更早使用、但 **Legendre 率先發表**。
- **哲學難題**：誤差服從什麼分布？取平均值為何「合理」？Gauss 的天才之處，是把「最小平方和」與「誤差常態分布下的最大概似」兩件事證明是同一件事。

## 線索與推理 -- 數學式、程式、理論

### 線索一：超定方程組與殘差
設模型為線性：$A\mathbf{x} \approx \mathbf{b}$，$A$ 是 $m \times n$ 矩陣（$m > n$），$\mathbf{b}$ 是觀測向量。因方程多於未知數，精確解一般不存在；定義**殘差**（誤差）向量：
$$\mathbf{r} = \mathbf{b} - A\mathbf{x}, \qquad S(\mathbf{x}) = \|\mathbf{r}\|^2 = \sum_{i=1}^m (b_i - \textstyle\sum_j a_{ij}x_j)^2$$
最小平方法的目標：找 $\hat{x}$ 使 $S(\hat{x})$ 最小——「平方和最小」而非「誤差總和最小」，因為平方消除正負抵消、且處處可微。

### 線索二：正規方程的推導
對 $S(\mathbf{x})$ 求極小：展開
$$S(\mathbf{x}) = \mathbf{b}^T\mathbf{b} - 2\mathbf{x}^TA^T\mathbf{b} + \mathbf{x}^TA^TA\mathbf{x}$$
令梯度為零：
$$\nabla S = -2A^T\mathbf{b} + 2A^TA\mathbf{x} = 0 \quad\Rightarrow\quad \boxed{A^TA\,\hat{x} = A^T\mathbf{b}}$$
這就是**正規方程**（normal equations）：$n$ 條方程、$n$ 個未知數。當 $A$ 各列線性獨立（$\mathrm{rank}\,A = n$）時，$A^TA$ 可逆，解唯一：
$$\hat{x} = (A^TA)^{-1}A^T\mathbf{b}$$
幾何解釋：$A\hat{x}$ 是 $\mathbf{b}$ 在 $A$ 的列空間上的**正交投影**；殘差 $\mathbf{b} - A\hat{x}$ 與列空間垂直（$A^T\mathbf{r} = 0$ 正是垂直條件）。

### 線索三：誤差的常態分布——最大概似的統一
Gauss 1809 年的關鍵推理：假設誤差獨立同分布、密度為 $\varphi(\varepsilon)$，且「算術平均是最可能的值」對任意樣本成立，則可推出 $\varphi$ 必須是
$$\varphi(\varepsilon) = \frac{1}{\sigma\sqrt{2\pi}}\,e^{-\varepsilon^2/2\sigma^2}$$
——**常態分布**。反過來：在常態誤差假設下，最小平方法恰是**最大概似估計**（maximize $\prod_i \varphi(b_i - (A\mathbf{x})_i)$，取對數後正是最小化 $\|\mathbf{r}\|^2$）。幾何最小平方與統計最大概似，在常態假設下合而為一。

### 線索四：Ceres 案件的偵破
1801 年 1 月 1 日，Piazzi 發現 Ceres，觀測 24 次後失蹤。多數天文學家無法從這麼短的弧段算出可靠軌道；Gauss 用自己的最小平方法處理這組超定數據，預測 Ceres 於 1801 年 12 月 7 日（Zach 觀測到）重新出現在天球上的預測位置附近。這是科學史上最著名的「數據破案」——最小平方法一戰成名，Gauss 聲譽鵲起。

### 程式碼範例：最小平方方法的正規方程 $A^TA\hat{x}=A^Tb$ 驗證
```python
import numpy as np

# 樣本：以二次多項式擬合含雜訊的觀測（超定：15 條方程、3 個未知數）
rng = np.random.default_rng(0)
t = np.linspace(-1, 1, 15)
b = 0.5 + 2*t - 1.5*t**2 + rng.normal(0, 0.15, len(t))   # 觀測（含誤差）

A = np.column_stack([np.ones_like(t), t, t**2])          # 模型矩陣

# 路徑一：正規方程 A^T A x = A^T b
x_normal = np.linalg.solve(A.T @ A, A.T @ b)
# 路徑二：正交投影（QR 分解，數值上更穩定）
x_qr, *_ = np.linalg.lstsq(A, b, rcond=None)

print("正規方程解   :", x_normal.round(4))   # 應接近 [0.5, 2, -1.5]
print("QR/投影解    :", x_qr.round(4))
print("兩路徑一致   :", np.allclose(x_normal, x_qr))

# 驗證正交條件：A^T r = 0（殘差垂直於列空間）
r = b - A @ x_normal
print("A^T r =", (A.T @ r).round(12))       # ≈ [0, 0, 0]

# 殘差平方和 vs 其他候選
for dx in [np.zeros(3), np.array([0.1, -0.1, 0.1])]:
    print("S =", np.sum((b - A @ (x_normal + dx))**2).round(4), "(偏移)", dx)
```

輸出顯示：正規方程解與 `lstsq` 的投影解完全一致，$A^T\mathbf{r} \approx \mathbf{0}$ 驗證殘差正交於列空間，且任何偏移都使平方和變大——$\hat{x}$ 確實是極小點。

## 結案 -- 後果與影響
- **統計學的基石**：最小平方法 + 誤差常態分布，成為迴歸分析的起點；「Gauss–Markov 定理」（1821，Gauss 證明最小平方估計在線性無偏估計中方差最小）奠定其理論地位。常態分布因此被稱為「Gauss 分布」。
- **數值線性代數的基石**：正規方程 $A^TA\hat{x} = A^T\mathbf{b}$ 是最古老的超定方程解法；後續的 QR 分解、SVD 方法在數值穩定性上勝過正規方程（條件數平方放大的問題），但正規方程的思想仍是教材的起點。
- **天文學的勝利**：Ceres 的重新發現證明了數學方法處理觀測誤差的力量，開啟了「天體力學 + 數據分析」的傳統。
- **優先權懸案**：Legendre 1805 率先發表，Gauss 宣稱 1795 年已使用並於 1809 年發表理論基礎——兩人的爭執是科學史上著名的優先權糾紛之一，最終史學界給出「Legendre 先發表、Gauss 更早使用且理論更深」的判決。
- 影響至今：從 GPS 定位、機器學習的線性迴歸，到航天軌道確定，全是這條 1809 年數學式的後代。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Carl Friedrich Gauss | 1795 年前後發明，1801 破 Ceres 案，1809 發表理論 |
| Adrien-Marie Legendre | 1805 年率先發表最小平方法 |
| Giuseppe Piazzi | 1801 年發現 Ceres 並留下 24 筆觀測數據 |
| Franz Xaver von Zach | 1801 年依 Gauss 預測重新找到 Ceres |

- C. F. Gauss, *Theoria motus corporum coelestium in sectionibus conicis solem ambientium* (1809)。
- A.-M. Legendre, *Nouvelles méthodes pour la détermination des orbites des comètes* (1805)，附錄首載最小平方法。
- C. F. Gauss, *Theoria combinationis observationum erroribus minimis obnoxiae* (1821)：Gauss–Markov 定理前身。
- S. M. Stigler, *The History of Statistics* (1986)：優先權爭議的標準考據。
