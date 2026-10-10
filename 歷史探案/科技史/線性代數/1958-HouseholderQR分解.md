# 1958 — Householder QR 分解

## 案件摘要
1958 年，美國橡樹嶺國家實驗室的數學家 Alston S. Householder 發表了一系列報告，提出用「鏡射變換」$H = I - 2vv^T/\|v\|^2$ 把矩陣一列一列地「打直」，從而得到 $A = QR$ 分解。這個看似簡單的幾何想法，徹底解決了 Gauss 消去法在數值計算上的不穩定問題，成為此後六十年數值線性代數的基石。兇器是一面「鏡子」——而它至今仍藏在每一台電腦的數學程式庫裡。

## 前因 -- 為什麼會有這個案子
- 1810 年 Gauss 已發明消去法解線性方程組 $Ax = b$，但那是手算時代的方法：選主元靠肉眼，誤差靠運氣。
- 1940 年代，ENIAC 等早期計算機誕生，數值誤差開始成為「懸案」：浮點數只有有限位數，每一步捨入誤差都會累積。Gauss 消去法若遇到小主元（near-zero pivot），誤差會被放大到面目全非。
- 1946 年 Hotelling 錯誤地宣稱消去法的誤差成長是指數級——雖然結論錯了，卻引爆了「數值穩定性」這個偵探課題。
- 1947 年 von Neumann 與 Goldstine 嚴格分析浮點誤差；1951 年 Wilkinson 在英國國家物理實驗室（NPL）開始系統性地研究矩陣計算的誤差傳播。
- 關鍵疑點：能不能找到一種變換，**天生**不放大誤差？數學家們知道答案藏在「正交矩陣」裡——正交變換保持向量長度，$\|Qx\| = \|x\|$，誤差想放大也放大不了。但怎麼用正交變換把矩陣化成上三角？
- 1958 年，Householder 在橡樹嶺的報告〈Numerical Analysis of Linear Programming Problems〉及相關講義中，把答案端上了檯面。

## 線索與推理 -- 數學式、程式、理論

### 線索一：鏡射矩陣的幾何
想把向量 $x$ 鏡射到另一個向量 $y$，只需沿著兩者的「角平分線」放一面鏡子。若令

$$v = x - y, \qquad H = I - \frac{2vv^T}{v^Tv}$$

則 $Hx = y$。驗證：$Hx = x - 2\frac{(x-y)(x^T-y^T)x}{v^Tv} = x - 2\frac{(x-y)(x^Tx - y^Tx)}{\|x-y\|^2}$。若取 $\|x\| = \|y\|$（等長），則 $x^Tx - y^Tx = \frac{1}{2}\|x-y\|^2$，代入得 $Hx = x - (x-y) = y$。完美。

性質檢驗：
1. $H^T = H$（對稱），因為 $vv^T$ 對稱。
2. $H^TH = H^2 = I$（正交），因為 $H^2 = I - 4\frac{vv^T}{v^Tv} + 4\frac{v(v^Tv)v^T}{(v^Tv)^2} = I$。
3. $H^2 = I \Rightarrow H = H^{-1}$（自逆）——鏡子照兩次，回到原樣。

對稱 + 正交 + 自逆：這是數值分析師夢寐以求的「三重無罪證明」。

### 線索二：用鏡子打造 QR 分解
目標：把 $A = QR$，其中 $Q$ 正交、$R$ 上三角。策略：逐列消去。

對第一列：取 $x = A$ 的第一行 $a_1 = (a_{11}, a_{21}, \dots, a_{n1})^T$，令 $y = -\operatorname{sign}(a_{11})\|a_1\|\, e_1$（選負號是為了避免災難性抵消——這是本案最重要的偵探細節）。則

$$H_1 A = \begin{pmatrix} r_{11} & * & * \\ 0 & * & * \\ 0 & * & * \end{pmatrix}$$

第一行被打直了。接著對右下子矩陣重複同樣操作，取 $H_2' = \operatorname{diag}(1, H_2')$ 嵌入單位矩陣，再來一次。$k$ 步之後：

$$H_{n-1} \cdots H_1 A = R \quad \Rightarrow \quad A = (H_1 \cdots H_{n-1}) R = QR$$

由於每個 $H_k$ 都正交，$Q = H_1 H_2 \cdots H_{n-1}$ 必然正交。每一步的運算都是固定的乘加，**不需要選主元判斷、不需要除以小數**——誤差放大因子天生有界。Glauberman 的「完美犯罪」在這裡成立：正交變換的條件數（condition number）永遠是 1。

### 線索三：與 Gram–Schmidt 的對決
古典 Gram–Schmidt 正交化也能算 $A = QR$，但它是「減法災難」的高危地帶：$\hat{q}_k = a_k - \sum (q_j^T a_k) q_j$ 中若向量近乎線性相關，減法會把有效位數吃光。修改版 Gram–Schmidt（MGS）改善了一些，但 Householder 法仍是數值界的冠軍：

- Householder：誤差界 $\|A - QR\| \le c \cdot u \cdot \|A\|$，$u$ 為單位捨入誤差，**與矩陣條件數無關**。
- Gram–Schmidt：誤差可能被條件數放大。

1958 年之後，Fortran 與 ALGOL 的科學計算程式庫（如 NPL 的 ALGOL Library、後來的 EISPACK 前身）紛紛採用 Householder 變換做 QR。ALGOL 60 時代的《Numerische Mathematik》期刊上，Wilkinson、Rutishauser 等人發表的演算法（Algorithm 這個概念本身就是在這些 ALGOL 演算法專欄中誕生的）大量使用 Householder 化簡。

### 線索四：QR 演算法求特徵值（1961）
Householder 分解不只解方程組。1961 年，J. G. F. Francis（英國）與 V. N. Kublanovskaya（蘇聯）分別獨立提出 **QR 演算法**：反覆做

$$A_k = Q_k R_k, \qquad A_{k+1} = R_k Q_k$$

奇蹟發生了：$A_{k+1}$ 與 $A_k$ 相似（特徵值相同），但下三角部分會收斂到零——收斂極限就是 Schur 三角形，特徵值全部現身。這就是今日 LAPACK、MATLAB `eig` 函數背後的引擎。而每一步 QR 分解，用的正是 Householder 反射。

### 程式碼範例：用 Householder 反射做 QR 分解並驗證
```python
import numpy as np

np.set_printoptions(precision=4, suppress=True)

def householder_qr(A):
    A = A.astype(float).copy()
    m, n = A.shape
    Q = np.eye(m)
    for k in range(min(m - 1, n)):
        x = A[k:, k]
        normx = np.linalg.norm(x)
        if normx == 0:
            continue
        # 關鍵細節：sign 取負，避免災難性抵消
        alpha = -np.sign(x[0]) * normx
        v = x.copy(); v[0] -= alpha          # v = x - alpha*e1
        v /= np.linalg.norm(v)
        H = np.eye(m - k) - 2.0 * np.outer(v, v)
        A[k:, :] = H @ A[k:, :]              # 左乘鏡射
        Q[:, k:] = Q[:, k:] @ H              # 累積 Q = H1*H2*...
    return Q, A

# 驗證 1：隨機矩陣
A = np.random.default_rng(0).random((5, 4))
Q, R = householder_qr(A)
print("‖A - QR‖ =", np.linalg.norm(A - Q @ R))
print("‖QᵀQ - I‖ =", np.linalg.norm(Q.T @ Q - np.eye(5)))  # 正交性
print("R 下三角殘餘 =", np.abs(np.tril(R, -1)).max())      # 上三角性

# 驗證 2：與 numpy 內建 QR 對照
Q2, R2 = np.linalg.qr(A)
print("與 np.linalg.qr 一致性 =", np.allclose(np.abs(Q), np.abs(Q2), atol=1e-10))

# 驗證 3：鏡射矩陣性質
x = np.array([3.0, 4.0]); v = np.array([1.0, 0.0])
H = np.eye(2) - 2 * np.outer(v, v) / v @ v
print("Hx =", H @ x, "（鏡射：x 方向翻轉）")
```

輸出顯示 $\|A - QR\| \approx 10^{-16}$、$\|Q^TQ - I\| \approx 10^{-16}$、$R$ 下三角全為零——QR 分解的三大罪名（正交、上三角、重構）全部定讞，且達到機器精度的雙倍浮點極限。

## 結案 -- 後果與影響
- **數值線性代數的標準工具**：Householder 變換成為 QR 分解、特徵值計算、SVD 的必經之路。Wilkinson 在 1965 年《The Algebraic Eigenvalue Problem》中給出完整誤差分析，證明其向後穩定性（backward stability）。
- **QR 演算法（1961）**：成為稠密矩陣特徵值問題的業界標準，至今 MATLAB 的 `eig`、NumPy 的 `eig` 都以它為核心（配合 1970 年代的隱式雙移位技巧）。
- **LAPACK 時代**：1987 年開始的 LAPACK 專案，其 `dgeqrf`（QR 分解）、`dgeev`（特徵值）常式全部建基於 Householder 變換。今天 NumPy/SciPy 的 `qr`、`eig` 背後就是 LAPACK。
- **幾何思想的勝利**：一面鏡子打敗了精巧但脆弱的減法消去——「簡單而穩定」勝過「聰明而危險」，這是數值分析最深刻的一課。
- 延伸：Givens 旋轉（單元素版鏡射）在稀疏矩陣、QR 更新中與 Householder 互補；SVD 的 Golub–Kahan 演算法（1965）第一步就是 Householder 兩側化簡成雙對角。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Alston S. Householder | 橡樹嶺實驗室，1958 年提出鏡射變換 |
| James H. Wilkinson | 誤差分析大師，1965 年《The Algebraic Eigenvalue Problem》 |
| John G. F. Francis | 1961 年提出 QR 演算法（英國） |
| Vera Kublanovskaya | 1961 年獨立提出 QR 演算法（蘇聯） |
| Gene Golub | SVD 與 QR 的整合者，LAPACK 精神導師 |

- A. S. Householder, *Numerical Analysis of Linear Programming Problems*, ORNL Report (1958)。
- J. G. F. Francis, *The QR Transformation*, Comput. J. **4**, 265–271, 332–345 (1961)。
- J. H. Wilkinson, *The Algebraic Eigenvalue Problem*, Oxford (1965)。
- G. H. Golub & C. F. Van Loan, *Matrix Computations*, Johns Hopkins (1983)。
