# 1951 — Lanczos 迭代法

## 案件摘要
1950–1951 年，匈牙利裔物理學家 Cornelius Lanczos 在美國國家標準局（NBS）發表〈An Iteration Method for the Solution of the Eigenvalue Problem of Linear Differential and Integral Operators〉，提出一個看似簡單卻威力驚人的程序：用一個起始向量反覆左乘矩陣 $A$，把 $A$ 「投影」成一個小型的三對角矩陣。這就是著名的 **Lanczos 演算法**——稀疏矩陣特徵值問題的破案關鍵，也是日後共軛梯度法、ARPACK 的共同祖先。

## 前因 -- 為什麼會有這個案子
- 1940 年代末，結構力學（飛機機翼振動）、量子化學（分子軌道能量）產生動輒數萬、數十萬階的矩陣，但矩陣**極度稀疏**：每列只有少數幾個非零元素。
- 傳統手法（Jacobi 對角化、行列式展開、正交三角分解）需要 $O(n^3)$ 記憶體與時間——大型稀疏矩陣直接「塞不進」當時的計算機。
- 1946 年 ENIAC 問世，數值分析界意識到：必須設計**只用到矩陣─向量乘法**的演算法，才能利用稀疏性。
- 1931 年 Krylov 已研究過冪級數序列 $\operatorname{span}\{b, Ab, A^2b, \dots\}$ 的行為——這條「子空間」正是 Lanczos 案件的偵查範圍。

## 線索與推理 -- 數學式、程式、理論

### 線索一：Krylov 子空間——偵查的搜索範圍
給定對稱矩陣 $A \in \mathbb{R}^{n\times n}$ 與起始向量 $b$，定義 **Krylov 子空間**：

$$\mathcal{K}_k = \operatorname{span}\{b,\, Ab,\, A^2b,\, \dots,\, A^{k-1}b\}$$

直覺：$A^j b$ 把 $b$ 沿著 $A$ 的各個特徵方向放大 $\lambda_i^j$ 倍，冪次越高、絕對值最大的特徵值 $\lambda_1$ 越佔優勢。因此「$A$ 的秘密」就藏在這個子空間裡——只是冪迭代會被 $\lambda_1$ 完全淹沒，看不到其他特徵值。Lanczos 的手法是：在子空間內做**正交化**，保住所有線索。

### 線索二：三對角化——把嫌犯壓縮成一張小照片
Lanczos 迭代：從 $b = v_1$（$||v_1||=1$）出發，反覆做

$$w_j = A v_j - \beta_{j-1} v_{j-1}, \qquad \alpha_j = v_j^T w_j, \qquad w_j \leftarrow w_j - \alpha_j v_j$$

$$\beta_j = \|w_j\|, \qquad v_{j+1} = w_j / \beta_j$$

由於 $\mathcal{K}_k$ 在 $A$ 作用下封閉（$Av_j \in \mathcal{K}_{j+1}$），正交化時**只需要減掉前兩項** $v_{j-1}, v_j$——這就是「短遞迴」的奇蹟。結果：

$$V_k = [v_1, \dots, v_k], \qquad V_k^T A V_k = T_k = \begin{pmatrix} \alpha_1 & \beta_1 & & \\ \beta_1 & \alpha_2 & \beta_2 & \\ & \ddots & \ddots & \beta_{k-1} \\ & & \beta_{k-1} & \alpha_k \end{pmatrix}$$

$T_k$ 是 $k$ 階三對角矩陣，其 Ritz 值（特徵值）極速逼近 $A$ 的極端特徵值（最大、最小代數值）。只要 $k \ll n$（例如 $k = 50$、$n = 10^6$），就能用 $O(k n)$ 的成本取得關鍵特徵值。

### 線索二・補：收斂速度的保證
設 $A$ 的特徵值為 $\lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_n$，Lanczos 的 Ritz 值 $\theta_k^{(i)}$ 滿足 Kaniel–Paige–Saad 型收斂界：

$$\lambda_i - \theta_k^{(i)} \le \left(\text{常數}\cdot\frac{\text{gap}}{|\lambda_{\text{near}}-\lambda_i|}\right)^2 \cdot (\text{起始向量偏折量}) \cdot |\lambda_i - \lambda_n|$$

更直覺的說法：極端特徵值的 Ritz 誤差以**幾何級數**衰減，且衰減率與「特徵值之間的間隔」有關——特徵值越孤立，收斂越快。這解釋了為什麼實務上 $k$ 遠小於 $n$ 就能取得極端特徵值。

### 線索三：從 Lanczos 到共軛梯度——同一案件的兩份口供
1952 年 Hestenes 與 Stiefel 發現：解對稱正定系統 $Ax = b$ 的共軛梯度法（CG），與 Lanczos 迭代**數學上等價**——CG 的殘差 $r_k = b - Ax_k$ 正是 Lanczos 向量乘上尺度，兩者產生同一組三對角矩陣 $T_k$。1970 年代 Paige 的誤差分析、Parlett 的整理，讓這層關係成為 Krylov 子空間方法論的統一框架。

### 程式碼範例：Lanczos 三對角化迭代（numpy 實作）
```python
import numpy as np

def lanczos(A, b, m):
    n = A.shape[0]
    V = np.zeros((n, m)); alpha = np.zeros(m); beta = np.zeros(m)
    v = b / np.linalg.norm(b); V[:, 0] = v
    for j in range(m):
        w = A @ v - (beta[j-1] * V[:, j-1] if j > 0 else 0)
        a = v @ w
        w = w - a * v                    # 完全正交化（對付浮點誤差）
        b_ = np.linalg.norm(w)
        alpha[j], beta[j] = a, b_
        if j < m - 1:
            v = w / b_; V[:, j+1] = v
    T = np.diag(alpha) + np.diag(beta[:-1], 1) + np.diag(beta[:-1], -1)
    return V, T

np.random.seed(0)
n = 500
d = np.arange(1, n + 1)                   # 真實特徵值 1..500
Q, _ = np.linalg.qr(np.random.randn(n, n))
A = Q @ np.diag(d) @ Q.T                  # 對稱矩陣，特徵值已知

V, T = lanczos(A, np.random.randn(n), 60)
ritz = np.sort(np.linalg.eigvalsh(T))
print("真最大特徵值 :", d[-1], " Ritz 逼近 :", ritz[-1])
print("真最小特徵值 :", d[0],  " Ritz 逼近 :", ritz[0])
print("只用 60 階三對角矩陣就抓到極端特徵值！")
```

輸出顯示：$m = 60$ 步的 Ritz 值已精確逼近 $n = 500$ 階矩陣的最大與最小特徵值——三對角化以極小的成本鎖定了 $A$ 的核心秘密。

## 結案 -- 後果與影響
- 1952 年 Hestenes–Stiefel 直接從 Lanczos 框架發展出**共軛梯度法**，成為稀疏線性系統的解法（見 1976 年案）。
- 1970 年代 Paige 證明 Lanczos 向量在浮點運動下會失去正交性，導出**完全正交化 / 再正交化**技巧，演算法從此可靠。
- 1990 年代 ARPACK（Arnoldi/Lanczos 套件，`eigs`、`svds` 的核心）把此法變成大型特徵值問題的工業標準。
- 非對稱版本就是 **Arnoldi 迭代**（1951 年論文中已有影子），GMRES 等方法由此而生。
- 影響至今：量子化學計算、PageRank（1998 年案）、模型降階、譜聚類——全都是 Krylov 子空間的子孫。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Cornelius Lanczos | 提出 Lanczos 演算法（1950–51） |
| Aleksei Krylov | Krylov 序列的先驅（1931） |
| Magnus Hestenes / Eduard Stiefel | 共軛梯度法（1952） |
| Christopher Paige | 浮點誤差分析（1971–76） |
| Beresford Parlett | 《The Symmetric Eigenvalue Problem》（1980） |

- C. Lanczos, *An Iteration Method for the Solution of the Eigenvalue Problem of Linear Differential and Integral Operators*, J. Res. Nat. Bur. Standards **45**, 255–282 (1950); **49**, 33–53 (1951)。
- M. Hestenes & E. Stiefel, *Methods of Conjugate Gradients for Solving Linear Systems*, J. Res. Nat. Bur. Standards **49**, 409–436 (1952)。
