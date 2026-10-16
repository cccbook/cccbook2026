# 1883 — Gram–Schmidt 正交化

## 案件摘要
1883 年，丹麥數學家 Jørgen Pedersen Gram 在論文〈Om Ækvationer mellem Coefficienter i Lineære Differentialligninger〉（關於線性微分方程中係數的方程）中，發表了一套把線性無關向量組轉成正交向量組的方法——原初目的是處理最小平方法與級數展開。1907 年 Erhard Schmidt 在研究積分方程與希爾伯特空間理論時，把同樣的程序以內積語言系統化、命名並寫進幾何框架，於是世人稱之為 **Gram–Schmidt 正交化**。一樁橫跨 24 年的「共同偵破」案件：Gram 提出技術，Schmidt 給出理論與名字。

## 前因 -- 為什麼會有這個案子
- **Legendre 多項式與正交函數**：18–19 世紀，Legendre、Laplace、Fourier 在處理位勢論與熱傳導時，發現多項式族 $\{1, x, x^2, \dots\}$ 經過適當「處理」後具有互相正交的性質——$\int_{-1}^{1} P_m(x) P_n(x)\,dx = 0\ (m \neq n)$。正交函數是好東西，但**怎麼系統地造出來**，缺乏一般方法。
- **Fourier 級數的係數之謎**：Fourier 1807/1822 年展開 $f(x) = \sum a_n \cos nx + b_n \sin nx$，係數公式 $a_n = \frac{1}{\pi}\int f(x)\cos nx\, dx$ 隱含正交性，但為什麼係數「一個一個獨立決定」、互不干擾，需要幾何解釋。
- **最小平方法的計算負擔**：Legendre 1805 年、Gauss 1809 年提出最小平方法，法方程（normal equations）$A^T A c = A^T b$ 在基底不良時病態嚴重。Gram 的工作正是為了**更穩地**做最小平方擬合與級數逼近。
- Schmidt 的舞台：Hilbert 的積分方程理論（1904–1906）把函數空間視為無限維內積空間；Schmidt 1907 年的論文正是要把「基底」「正交」「投影」這些幾何概念在該空間裡落實——正交化程序是必備工具。

## 線索與推理 -- 數學式、程式、理論

### 線索一：正交化公式
設 $v_1, v_2, \dots, v_n$ 線性無關。Gram–Schmidt 程序逐個構造正交向量：

$$\hat{e}_1 = v_1$$
$$\hat{e}_k = v_k - \sum_{i<k} \frac{\langle v_k, \hat{e}_i \rangle}{\langle \hat{e}_i, \hat{e}_i \rangle}\, \hat{e}_i, \qquad k = 2, \dots, n$$

再單位化 $e_k = \hat{e}_k / \|\hat{e}_k\|$，得到正交歸一基底 $\{e_1, \dots, e_n\}$。核心思想：新向量 = 原向量 − 它在已有方向上的**投影**，把「平行成分」全部扣除，剩下的自然垂直。

### 線索二：為什麼扣除投影就垂直
用內積的雙線性直接驗證：對 $j < k$，

$$\langle \hat{e}_k, \hat{e}_j \rangle = \langle v_k, \hat{e}_j \rangle - \sum_{i<k} \frac{\langle v_k, \hat{e}_i \rangle}{\langle \hat{e}_i, \hat{e}_i \rangle}\langle \hat{e}_i, \hat{e}_j \rangle = \langle v_k, \hat{e}_j \rangle - \langle v_k, \hat{e}_j \rangle = 0$$

因為 $\{\hat{e}_i\}_{i<k}$ 已互相正交，求和項中只有 $i = j$ 那一項倖存，恰好抵消。歸納法收案：每一步新造的向量與之前全部正交。

### 線索三：幾何解釋——投影與逼近
$\hat{e}_k$ 是 $v_k$ 在 $\mathrm{span}\{\hat{e}_1,\dots,\hat{e}_{k-1}\}$ 的**正交補**上的分量，而

$$\sum_{i<k} \langle v_k, e_i \rangle e_i = \mathrm{proj}_{\mathrm{span}\{e_1,\dots,e_{k-1}\}}(v_k)$$

正是投影定理：正交投影是子空間中**最佳逼近**。這一步解釋了 Fourier 係數的獨立性——在正交基底上，逼近係數 $\langle f, e_i \rangle$ 一個一個獨立決定，互相不干擾；Fourier 級數不過是無限維內積空間裡的「座標分解」。

### 線索四：QR 分解的矩陣化身
Gram–Schmidt 等價於 QR 分解：把 $A = [v_1, \dots, v_n]$ 寫成

$$A = QR, \qquad Q = [e_1, \dots, e_n]\ \text{正交},\quad R\ \text{上三角}$$

其中 $R_{ik} = \langle v_k, e_i \rangle\ (i \le k)$，對角元素 $\|\hat{e}_k\|$ 就是投影後的殘餘長度。經典 Gram–Schmidt 數值上不穩（捨入誤差會累積出非正交鬼影），**修正型 Gram–Schmidt（MGS）**改變計算順序後大幅改善；Householder 反射（1958）則是完全穩定的替代兇器。

### 程式碼範例：Gram–Schmidt 正交化並驗證 Q 為正交矩陣
```python
import numpy as np

np.set_printoptions(precision=6, suppress=True)

def gram_schmidt(V):                 # V 的行向量為待正交化的向量
    n = V.shape[1]
    Q = np.zeros_like(V)
    R = np.zeros((n, n))
    for k in range(n):
        w = V[:, k].copy()
        for i in range(k):           # 扣除在已有方向上的投影
            R[i, k] = Q[:, i] @ V[:, k]
            w -= R[i, k] * Q[:, i]
        R[k, k] = np.linalg.norm(w)  # 殘餘長度
        Q[:, k] = w / R[k, k]
    return Q, R

A = np.array([[1.0, 1.0, 1.0],
              [1.0, 2.0, 0.0],
              [0.0, 1.0, 3.0]])
Q, R = gram_schmidt(A)

print("Q（正交基底，行）:\n", Q)
print("R（上三角）:\n", R)
print("驗證 A = QR      :", np.allclose(A, Q @ R))
print("驗證 Q^T Q = I   :", np.allclose(Q.T @ Q, np.eye(3)))
print("驗證兩兩正交     :", np.allclose(Q[:, 0] @ Q[:, 1], 0),
                           np.allclose(Q[:, 0] @ Q[:, 2], 0),
                           np.allclose(Q[:, 1] @ Q[:, 2], 0))
```

輸出中 $Q^TQ = I$（各行單位長且兩兩正交）、$A = QR$ 恆成立——正交化程序的代數鐵證；$R$ 的上三角結構正是「每次只扣除之前投影」的痕跡。

## 結案 -- 後果與影響
- **正交基底成為內積空間的標準配備**：從 $\mathbb{R}^n$ 到希爾伯特空間，凡是要求解、投影、展開的場合，先造正交基底。
- **希爾伯特空間理論**：Schmidt 1907 年的工作（與 Riesz 1907 的 $L^2$ 理論）催生了 von Neumann 1929 年的希爾伯特空間公理化——量子力學的數學家園。
- **QR 分解**：Gram–Schmidt 的矩陣化身，成為最小平方問題的**穩定解法**（避開病態的法方程）、特徵值 QR 演算法的基礎步驟。
- **最小平方的正交解**：$\hat{c} = R^{-1}Q^Tb$ 直接給出最佳逼近係數，法方程的條件數災難被繞過。
- **函數空間的正交多項式**：Legendre、Hermite、Laguerre、Chebyshev 多項式全部可由對冪基 $\{1, x, x^2, \dots\}$ 做 Gram–Schmidt 造出——古典正交多項式是同一程序的產物。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Jørgen Pedersen Gram | 1883 年提出正交化技術（最小平方動機） |
| Erhard Schmidt | 1907 年系統化並命名，幾何框架 |
| Adrien-Marie Legendre | 最小平方法、正交多項式（前案） |
| David Hilbert | 積分方程與函數空間理論（舞台） |

- J. P. Gram, *Om Ækvationer mellem Coefficienter i Lineære Differentialligninger*, 位勢論與級數逼近論文 (1883)；德文擴充版 *Über die Entwicklung reeller Functionen in Reihen mittelst der Methode der kleinsten Quadrate*, J. Reine Angew. Math. **94**, 41–73 (1883)。
- E. Schmidt, *Zur Theorie der linearen und nichtlinearen Integralgleichungen*, Math. Ann. **63**, 433–476 (1907)。
- A.-M. Legendre, *Nouvelles méthodes pour la détermination des orbites des comètes* (1805)。
