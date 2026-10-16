# 1961 — Francis QR 演算法

## 案件摘要
1961 年，英國計算機科學家 J. G. F. Francis（在 Ferranti 公司工作）發表〈The QR Transformation: A Unitary Analogue to the LR Transformation〉，提出以 QR 分解為核心的迭代法：反覆把矩陣分解 $A_k = Q_k R_k$，再令 $A_{k+1} = R_k Q_k$。配合隱式雙位移技巧，非對稱矩陣的特徵值從此可以**穩定而實用**地算出。這就是 Francis QR 演算法——六十年後仍是 LAPACK、MATLAB `eig` 背後的破案標準手法。

## 前因 -- 為什麼會有這個案子
- 1958 年瑞士的 Rutishauser 提出 **LR 演算法**：$A_k = L_k R_k$，$A_{k+1} = R_k L_k$。收斂快，但 $L$（下三角）元素的成長可能導致數值爆炸——用非正交變換辦案，嫌犯會「掙脫」。
- 1958 年前後 Householder 提出用鏡射矩陣做正交三角化，把矩陣化為**上 Hessenberg 形式**（次對角線以下皆零）——這是 QR 迭代的完美起點。
- 冪迭代法（20 世紀初）一次只能抓一個特徵值，且收斂比是 $|\lambda_2/\lambda_1|$，遇到相近特徵值就卡住。
- 產業需求：EISPACK 計畫（1970 年代初）需要一套能處理一般實矩陣、數值穩定的特徵值演算法——QR 演算法應徵成功。

## 線索與推理 -- 數學式、程式、理論

### 線索一：QR 迭代為什麼會收斂
對 $A_k$ 做 QR 分解 $A_k = Q_k R_k$（$Q_k$ 正交、$R_k$ 上三角），令

$$A_{k+1} = R_k Q_k = Q_k^{-1} A_k Q_k$$

每次迭代都是一個**正交相似變換**：特徵值不變。若 $A$ 的特徵值絕對值互異，且冪迭代收斂條件成立，則 $A_k$ 的極限是上三角矩陣——對角線上就是特徵值。關鍵恆等式：

$$A^k = Q_1 Q_2 \cdots Q_k \cdot R_k \cdots R_2 R_1$$

即 $A^k$ 的 QR 分解。$Q_1\cdots Q_k$ 的前幾行逼近冪迭代的方向——QR 迭代本質上是「**所有特徵向量同時做的冪迭代**」。

### 線索二：位移加速——把收斂比從 0.9 壓到近乎 0
裸 QR 收斂比是 $|\lambda_{j+1}/\lambda_j|$，太慢。加上位移 $\mu$：

$$A_k - \mu I = Q R, \qquad A_{k+1} = R Q + \mu I$$

若 $\mu$ 接近某個特徵值 $\lambda$，對應方向的收斂比變成 $|\lambda - \mu|/|\lambda_{\text{next}} - \mu| \to 0$——瞬間收斂。對對稱矩陣用 Wilkinson 位移（三對角矩陣尾端二階子陣的特徵值中較接近 $a_{nn}$ 者）；實務上通常 2–3 步就收斂到機器精度。

### 線索二・補：Wilkinson 位移的細節
對三對角矩陣尾端的 $2\times 2$ 子陣

$$\begin{pmatrix} a_{n-1,n-1} & a_{n-1,n} \\ a_{n-1,n} & a_{n,n} \end{pmatrix}$$

取其兩個特徵值中**較接近 $a_{nn}$** 的那個作為位移（Wilkinson 位移）。這個選擇的收斂性可以證明是**漸近三次方**的（cubic convergence）——實務上每個特徵值平均只需 2–3 次迭代就能 deflation。對非對稱的 Hessenberg 矩陣，尾端二階子陣的特徵值是共軛複數對，正好接上線索三的隱式雙位移。

### 線索三：隱式雙位移——非對稱案件的關鍵突破
實矩陣的特徵值可能是**共軛複數對** $a \pm bi$，單一實位移 $\mu$ 無法接近複數特徵值。Francis 的招數：取尾端二階子陣的兩個（複）特徵值 $\mu_1, \mu_2$ 為位移，做兩步位移 QR。雖然 $\mu_1, \mu_2$ 是複數，但兩步合併後的矩陣 $M = (A-\mu_2 I)(A-\mu_1 I)$ 是**實矩陣**，因此整個過程不需要複數運算——這就是**隱式雙位移 QR**。

演算法步驟：
1. Householder 化簡：$A \to H$（上 Hessenberg 形式）。
2. 取 $H$ 尾端 $2\times 2$ 子陣的特徵值 $\mu_1, \mu_2$。
3. 計算 $M = H^2 - s H + t I$（$s = \mu_1+\mu_2$、$t = \mu_1\mu_2$ 為實數），取第一列非零元 $x = (m_{21}, m_{22}, m_{23}, 0, \dots)$ 決定 Householder $P_0$。
4. 做「chase the bulge」（追逐凸塊）：$PHP_0$ 在次對角下方冒出凸塊，再用一連串 Householder 把凸塊沿對角線一路推到底，等效完成兩步位移 QR：$H \to H'$。
5. 當尾端 $1\times 1$ 或 $2\times 2$ 子陣收斂（deflation），縮小問題，回到第 2 步。

### 程式碼範例：Francis QR 的冪迭代本質與位移收斂（numpy 模擬）
```python
import numpy as np

np.random.seed(1)
n = 60
d = np.array([10, 9.9] + list(2 + 0.5 * np.arange(n - 2)))  # 前兩個特徵值極近
Q, _ = np.linalg.qr(np.random.randn(n, n))
A = Q @ np.diag(d) @ Q.T

# 線索一：QR 迭代 = 同時冪迭代；比較「裸 QR」與「位移 QR」收斂
off = lambda M: np.sqrt(np.sum(np.tril(M, -1)**2))  # 下三角能量
A0 = A.copy()
for k in range(100):                                  # 裸 QR（無位移）
    q, r = np.linalg.qr(A0); A0 = r @ q
    if k in (0, 9, 99): print(f"裸 QR   第{k:3d}步 off(H) = {off(A0):.3e}")

mu = 9.995                                            # 位移取在 10 與 9.9 之間
A1 = A.copy()
for k in range(100):                                  # 位移 QR
    q, r = np.linalg.qr(A1 - mu * np.eye(n)); A1 = r @ q + mu * np.eye(n)
    if k in (0, 9, 99): print(f"位移QR  第{k:3d}步 off(H) = {off(A1):.3e}")

eig = np.sort(np.diag(A1))[::-1]
print("收斂後前四個對角元 :", np.round(eig[:4], 4))
print("真實前四個特徵值   :", np.round(np.sort(d)[::-1][:4], 4))
```

輸出顯示：裸 QR 100 步仍收斂緩慢（特徵值 10 與 9.9 太近，收斂比 ≈ 0.999）；加上位移 $\mu = 9.995$ 後，對應方向收斂比 ≈ 0，下三角能量急速歸零——這正是 Francis 雙位移在實矩陣上的威力縮影。

## 結案 -- 後果與影響
- 1970 年代 EISPACK 把 Francis QR（HQR2 等）變成**非對稱實矩陣特徵值**的標準解法。
- LAPACK（1992 起）以分塊化的 QR 演算法為核心：`dhseqr` 至今仍是 `eig`、`schur` 的引擎。
- 對稱版本（Wilkinson 位移、三對角 QR）成為對稱特徵值問題的首選，配合 MRRR、分治法構成現代 LAPACK 全家福。
- 隱式雙位移思想催生了 **Arnoldi + 隱式重啟**（IRAM，ARPACK 的核心）。
- 影響至今：控制系統（Schur 形式）、結構振動、量子力學數值計算——凡是「求特徵值」的地方，幾乎都是 Francis QR 在幕後辦案。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| J. G. F. Francis | 提出 QR / 隱式雙位移演算法（1961–62） |
| Heinz Rutishauser | LR 演算法先驅（1958） |
| Alston Householder | 正交三角化 / Hessenberg 化簡 |
| James Wilkinson | 誤差分析、Wilkinson 位移 |
| Gene Golub | 分塊 QR、奇異值分解的現代化 |

- J. G. F. Francis, *The QR Transformation: A Unitary Analogue to the LR Transformation*, Computer J. **4**, 265–271, 332–271 (1961–62)。
- J. H. Wilkinson, *The Algebraic Eigenvalue Problem*, Oxford (1965)。
- H. Rutishauser, *Solution of eigenvalue problems by the LR-transformations*, Appl. Math. Ser. **49**, NBS (1958)。
