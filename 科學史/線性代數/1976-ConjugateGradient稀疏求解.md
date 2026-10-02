# 1976 — Conjugate Gradient 稀疏求解

## 案件摘要
共軛梯度法（Conjugate Gradient, CG）由 Hestenes 與 Stiefel 於 1952 年提出，但問世後沉寂了二十多年——被視為「理論漂亮、實務難用」的直接法。1970 年代，Paige 的誤差分析、Concus–Golub–O'Leary 等人的再發掘，加上有限元素法產生的巨型稀疏矩陣，讓 CG 以**迭代法**的身分重新歸案，成為科學計算的破案主力。今天所有大型模擬（結構、流體、電磁）背後，幾乎都有 CG 的影子。

## 前因 -- 為什麼會有這個案子
- 1952 年 Hestenes–Stiefel 發表 CG：理論上 $n$ 步精確解出 $n$ 階對稱正定系統，被當成「另一種直接法」。
- 但浮點運算下誤差累積，$n$ 步不精確；1950–60 年代的大型稠密矩陣用直接法（Cholesky）反而更快——CG 被打入冷宮。
- 1960 年代末，有限元素法（FEM）在土木、航空、核工爆發，產生數十萬階的**稀疏對稱正定**矩陣：直接法 $O(n^3)$ 記憶體塞不下。
- 1971 年 Paige 證明 CG 與 Lanczos 迭代等價、並完成浮點誤差分析；1976 年 Concus、Golub、O'Leary 在 Standford 的論文與課程，正式把 CG 定位為「預條件 + 迭代」的稀疏求解器——案件重新開庭。

## 線索與推理 -- 數學式、程式、理論

### 線索一：二次函數的下降路線
解對稱正定系統 $Ax = b$ 等價於最小化二次函數

$$\phi(x) = \frac{1}{2}x^T A x - b^T x, \qquad \nabla \phi(x) = Ax - b = -r$$

最速下降法沿殘差 $-r_k$ 前進，但相鄰搜尋方向互相垂直、在病態條件數下呈「鋸齒狀」龜速前進。CG 的改良：讓每個搜尋方向與之前的方向 **A-共軛**：

$$p_k^T A p_j = 0 \quad (j < k)$$

在共軛方向上二次函數可**逐維獨立最小化**——$n$ 個方向各走一步就到達最小值。

### 線索二：CG 迭代公式與 Krylov 子空間
從 $x_0 = 0$、$p_0 = r_0 = b$ 出發，每步：

$$\alpha_k = \frac{r_k^T r_k}{p_k^T A p_k}, \qquad x_{k+1} = x_k + \alpha_k p_k$$

$$r_{k+1} = r_k - \alpha_k A p_k, \qquad \beta_k = \frac{r_{k+1}^T r_{k+1}}{r_k^T r_k}, \qquad p_{k+1} = r_{k+1} + \beta_k p_k$$

三個關鍵性質：
- **最優性**：$x_k$ 是 Krylov 子空間 $\mathcal{K}_k = \operatorname{span}\{b, Ab, \dots, A^{k-1}b\}$ 中讓 $A$-範數 $||x-x_k||_A$ 最小的點。
- **有限終止**：精確運算下 $n$ 步收斂（$\mathcal{K}_n = \mathbb{R}^n$）。
- **收斂速度**：誤差界

$$\|x - x_k\|_A \le 2\left(\frac{\sqrt{\kappa} - 1}{\sqrt{\kappa} + 1}\right)^k \|x - x_0\|_A, \qquad \kappa = \frac{\lambda_{\max}}{\lambda_{\min}}$$

條件數 $\kappa = 10^6$ 時收斂比 ≈ $1 - 2\times 10^{-6}$——太慢。因此 1970 年代的關鍵字是**預條件**（preconditioning）：先用不完全 Cholesky、對角縮放等手法把 $\kappa$ 壓小，再跑 CG。

### 線索三：CG 與 Lanczos——同一份口供
CG 的殘差 $r_k$ 正比於 Lanczos 向量 $v_{k+1}$，兩者產生同一組三對角矩陣 $T_k$；CG 的 $\alpha_k, \beta_k$ 就是 Lanczos 係數。這層等價性（Paige 1971–76）解釋了 CG 的收斂行為，也開啟了 Krylov 方法論的統一框架：對稱不定系統用 MINRES/SYMMLQ，非對稱系統用 GMRES/BiCGSTAB——全都是這份口供的分支。

### 程式碼範例：共軛梯度法解 $Ax=b$ 的收斂曲線
```python
import numpy as np
import matplotlib.pyplot as plt

def cg(A, b, tol=1e-10, maxit=None):
    n = len(b); x = np.zeros(n)
    r = b.copy(); p = r.copy(); rs = r @ r
    hist = [np.sqrt(rs)]
    for k in range(maxit or n):
        Ap = A @ p
        alpha = rs / (p @ Ap)
        x += alpha * p
        r -= alpha * Ap
        rs_new = r @ r
        hist.append(np.sqrt(rs_new))
        if np.sqrt(rs_new) < tol: break
        p = r + (rs_new / rs) * p
        rs = rs_new
    return x, np.array(hist)

np.random.seed(2)
n = 300
Q, _ = np.linalg.qr(np.random.randn(n, n))
lam = np.concatenate([np.full(n//3, 1.0),          # 條件數 10^4 的譜
                      np.full(n//3, 100.0),
                      np.full(n - 2*(n//3), 10**4)])
A = Q @ np.diag(lam) @ Q.T
b = np.random.randn(n)
x, h = cg(A, b, maxit=300)

kappa = lam.max() / lam.min()
theory = 2 * ((np.sqrt(kappa)-1)/(np.sqrt(kappa)+1))**np.arange(len(h))
print("收斂步數 :", len(h)-1, " 條件數 :", kappa)
print("殘差最終值 :", h[-1])

plt.semilogy(h, label="CG residual")
plt.semilogy(theory * h[0], "--", label=r"bound $\propto ((\sqrt{\kappa}-1)/(\sqrt{\kappa}+1))^k$")
plt.xlabel("iteration k"); plt.ylabel(r"$\|r_k\|$"); plt.legend(); plt.show()
```

半對數圖顯示：CG 殘差隨迭代指數下降，且不劣於理論界 $2\left(\frac{\sqrt{\kappa}-1}{\sqrt{\kappa}+1}\right)^k$——「A-共軛方向」確實避開了最速下降的鋸齒陷阱。

## 結案 -- 後果與影響
- 1970 年代起 CG 成為**稀疏對稱正定系統**的標準解法：有限元素、結構分析、油藏模擬、影像重建。
- **預條件 CG**（ICCG、多重網格預條件）成為 HPC 的主力組合，寫進所有大型套件（PETSc、Trilinos、 hypre）。
- 思想外溢：非對稱系統的 GMRES（Saad–Schultz 1986）、BiCGSTAB（1992）皆源自 Krylov 子空間框架。
- 1989 年 O'Leary 等人的回顧、Golub–Van Loan 教科書的推廣，讓 CG 成為每一代科學家的必修課。
- 影響至今：從手機影像處理到氣候模擬，凡是「解大型線性系統」的地方，CG 仍在幕後辦案。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Magnus Hestenes / Eduard Stiefel | 提出 CG（1952） |
| Cornelius Lanczos | Krylov 子空間框架（1950–51） |
| Christopher Paige | CG–Lanczos 等價性與誤差分析（1971–76） |
| Gene Golub / Paul Concus / Dianne O'Leary | 1970 年代 CG 的再發掘與推廣 |

- M. Hestenes & E. Stiefel, *Methods of Conjugate Gradients for Solving Linear Systems*, J. Res. Nat. Bur. Standards **49**, 409–436 (1952)。
- C. Paige, *The Computation of Eigenvalues and Eigenvectors of Very Large Sparse Matrices*, PhD thesis, Univ. of London (1971)。
- P. Concus, G. Golub & D. O'Leary, *A Generalized Conjugate Gradient Method for the Numerical Solution of Elliptic PDEs*, in Bunch & Rose (eds.), Sparse Matrix Computations, Academic Press (1976)。
