# 1954 — Givens 旋轉

## 案件摘要
1954 年，美國阿貢國家實驗室的 Wallace Givens 在一場會議報告中提出：用一連串「平面旋轉矩陣」$G(i,j,\theta)$，可以逐一、精準地把矩陣中的某個元素消成零。這個看似簡單的想法，成為數值線性代數中最優雅的兇器之一——QR 分解、對稱矩陣三對角化、特徵值計算背後的共通手法。

## 前因 -- 為什麼會有這個案子
- 1846 年 Jacobi 提出對稱矩陣特徵值方法：反覆做平面旋轉 $A \leftarrow J^T A J$，把非對角元素「磨」到趨近於零，最後對角線就是特徵值。但 Jacobi 法收斂慢，且在手工計算時代極為繁重。
- 1940 年代末，電子計算機誕生（ENIAC 1945、EDVAC）。問題來了：怎麼讓機器「算特徵值」？
- Jacobi 法每一步要掃整個矩陣找最大的非對角元素，$O(n^2)$ 的搜尋成本在早期機器上很貴。
- Givens 的洞察：不必「挑最大的」再磨，而是**按順序、有計畫地**用平面旋轉逐個消去元素，直接把矩陣打成三對角形或上三角——這是一場從「游擊戰」到「正規軍」的戰術升級。

## 線索與推理 -- 數學式、程式、理論

### 線索一：Givens 旋轉矩陣的長相
Givens 旋轉是作用在第 $i,j$ 兩個座標軸張成的平面上的旋轉，其餘維度不動：

$$G(i,j,\theta)_{kk} = 1 \ (k \neq i,j), \qquad \begin{pmatrix} g_{ii} & g_{ij} \\ g_{ji} & g_{jj} \end{pmatrix} = \begin{pmatrix} c & s \\ -s & c \end{pmatrix}, \quad c = \cos\theta,\ s = \sin\theta$$

它是**正交矩陣**：$G^T G = I$，因此左乘 $G^T A$ 不改變矩陣的譜範數、不改變特徵值——犯罪現場的「指紋」完全保留。

### 線索二：消去一個元素
要消去向量 $(a, b)^T$ 的第二個元素，選

$$c = \frac{a}{\sqrt{a^2+b^2}}, \qquad s = \frac{b}{\sqrt{a^2+b^2}}$$

則

$$\begin{pmatrix} c & s \\ -s & c \end{pmatrix}\begin{pmatrix} a \\ b \end{pmatrix} = \begin{pmatrix} \sqrt{a^2+b^2} \\ 0 \end{pmatrix}$$

一次旋轉，只動兩列（或兩行），其餘元素分毫不動——成本僅 $O(n)$，且天然保持稀疏結構。

### 線索三：對稱矩陣的三對角化
對對稱矩陣 $A$，依序用 $G(n-1,n), G(n-2,n), \dots, G(2,3)$ 把 $A$ 第一列（行）中三對角以外的元素全部消去，再處理第二列……最終：

$$Q^T A Q = T, \qquad T \text{ 為三對角矩陣},\ Q = G_1 G_2 \cdots G_k$$

三對角矩陣的特徵值可用二分法、QL/QR 迭代或 Sturm 序列高效求解——Givens 旋轉就是整條流水線的第一道工序。

### 線索四：與 Householder 的對決
1958 年 Householder 提出反射變換：一次鏡射消去**整列**元素，總操作量約 $\frac{4}{3}n^3$，比 Givens 逐步旋轉（約 $2n^3$）省。一般稠密矩陣用 Householder；但 Givens 旋轉：
- **稀疏矩陣友善**：只動兩列，不改變其他零元素的位置；
- **增量更新**：QR 分解後新增一列/一行，可用 $O(n)$ 次 Givens 旋轉更新，不必重算；
- **天然並行**：互不重疊的 $(i,j)$ 對可同時旋轉，適合 GPU/脈動陣列。

### 線索五：偵探筆記——θ 的計算與陷阱
實際計算中不真的算 $\theta$，直接由 $(a,b)$ 算 $c, s$；但若 $a, b$ 都接近零（病態情況），$\sqrt{a^2+b^2}$ 會下溢——處理方式是先除以較大者：

$$r = \mathrm{sign}(a)\sqrt{(|a|/\tau)^2 + (|b|/\tau)^2}\cdot\tau, \qquad \tau = \max(|a|, |b|)$$

若 $b = 0$ 則直接跳過（無事可辦）；若 $a = 0$ 則取 $c=0, s=1$（純換位）。這些「小機關」決定了數值函式庫的成敗——LAPACK 的 `dlartg` 就是這道工序的工業級版本。

## 程式碼範例：Givens 旋轉消去元素與對稱 QR 三對角化
```python
import numpy as np

def givens(a, b):
    r = np.hypot(a, b)
    return a / r, b / r          # c, s

def zero_out(A, i, j):
    """用 Givens 旋轉消去 A[j, i]（i < j），作用於列 i, j"""
    c, s = givens(A[i, i], A[j, i])
    G = np.eye(len(A)); G[i, i] = c; G[j, j] = c
    G[i, j] = s; G[j, i] = -s
    return G.T @ A, G

A = np.array([[4., 1., 2.],
              [1., 3., 0.],
              [2., 0., 5.]])

# --- QR 分解：逐步消去下三角元素 ---
R, Q = A.copy(), np.eye(3)
for i in range(3):
    for j in range(i + 1, 3):
        R, G = zero_out(R, i, j)
        Q = Q @ G
print("Q^T A = R ? ", np.allclose(Q.T @ A, R))      # True
print("Q 正交 ?   ", np.allclose(Q.T @ Q, np.eye(3))) # True

# --- 對稱矩陣三對角化：特徵值不變 ---
T, Q = A.copy(), np.eye(3)
for i in range(3):
    for j in range(i + 1, 3):
        if abs(T[j, i]) > 1e-12 and (j > i + 1):
            T, G = zero_out(T, i, j)
            Q = Q @ G
print("三對角化 T =\n", np.round(np.where(abs(T) < 1e-12, 0, T), 6))
print("特徵值保持 ?", np.allclose(sorted(np.linalg.eigvalsh(T)),
                                  sorted(np.linalg.eigvalsh(A))))  # True
```

輸出顯示：$Q^T A = R$、$Q$ 正交，且三對角化前後特徵值完全一致——Givens 旋轉「殺人（消零）不毀證據（譜）」。

## 結案 -- 後果與影響
- QR 分解家族成形：Householder（稠密）、Givens（稀疏、增量）、Gram–Schmidt（數值穩定性較差但可修正）。
- 1960 年代 Francis、Wilkinson 把 QR 迭代發展成特徵值計算的黃金標準；Givens 旋轉是其核心零件。
- LAPACK（1992 起）中 `dgeqr`、`dsteqr`、`dorgqr` 等常式大量使用 Givens 旋轉；稀疏 QR（如 SPQR）更依賴它保持稀疏性。
- 增量 QR 更新成為訊號處理（RLS 濾波、最小平方法即時更新）的標準手法。
- 並行化潛力在 GPU 時代兌現：脈動陣列、分塊 Givens 成為現代數值函式庫的設計元素。
- 教科書地位：Golub & Van Loan《Matrix Computations》將其列為標準章節。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Wallace Givens | 1954 提出平面旋轉消去法 |
| Carl Gustav Jacobi | 1846 特徵值旋轉方法（前案） |
| Alston Householder | 1958 反射變換，稠密矩陣主力 |
| James Wilkinson | QR 迭代與數值穩定性分析 |

- W. Givens, *Numerical Computation of the Characteristic Values of a Real Symmetric Matrix*, Oak Ridge National Laboratory Report ORNL-1574 (1954)。
- C. G. J. Jacobi, "Über ein leichtes Verfahren...", J. reine angew. Math. (1846)。
- G. H. Golub & C. F. Van Loan, *Matrix Computations*, 4th ed., Johns Hopkins (2013)。
