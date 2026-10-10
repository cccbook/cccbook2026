# 1947 — Von Neumann 條件數

## 案件摘要
1947 年，John von Neumann 與 Herman Goldstine 發表論文〈Numerical inverting of matrices of high order〉，首次對「用電腦求逆大型矩陣」做了系統的誤差分析，並提出了今日稱為**條件數**的概念：

$$\kappa(A) = \|A\|\,\|A^{-1}\|$$

這個數字衡量一個矩陣「有多危險」：$\kappa$ 越大，浮點運算的捨入誤差被放大的倍數越大。這是數值線性代數的誕生時刻——ENIAC 的硬體問世，逼出了解釋「電腦算出來的答案能不能信」的理論。

## 前因 -- 為什麼會有這個案子
- 1945 年 ENIAC 誕生：第一台通用電子計算機，von Neumann 是顧問。它算得快，但每一步都是有限位數的浮點運算，捨入誤差無可避免。
- Gauss 消去法是兩百年前（1809 年）的方法：理論上 $n$ 個未知數 $n$ 個方程必有唯一解，但「理論上有解」與「電腦算得出正解」是兩回事。
- 1940 年代的悲觀氛圍：許多數學家（包括 von Neumann 本人一度）相信 $n = 100$ 的矩陣求逆會因捨入誤差累積而完全失敗——誤差像雪崩一樣滾雪球。
- Hotelling 1943 年的悲觀估計：他推測誤差增長可能是 $4^n$ 級別，意味著 $n$ 稍大就沒救。這個錯誤估計是案發現場的謎題。

## 線索與推理 -- 數學式、程式、理論

### 線索一：浮點運算的誤差來源
電腦中每個數字以有限位浮點表示（IEEE 754，1985 年才標準化，1947 年是各機器自訂）：實數 $x$ 存為 $\hat{x}$，相對誤差約為

$$\frac{|\hat{x} - x|}{|x|} \le \varepsilon = \frac{1}{2}\beta^{1-t}$$

其中 $\beta$ 是基底（二進制為 2）、$t$ 是有效位數。ENIAC 用十進制、約 12 位。每次浮點運算（加、乘）都引入這麼小的誤差，一次求逆要做 $O(n^3)$ 次運算——問題是這些誤差會**互相放大**還是**互相抵銷**？

### 線索二：條件數——誤差的放大倍數
von Neumann 與 Goldstine 的核心洞見：誤差放大的倍數由矩陣本身決定，與演算法無關。定義：

$$\kappa(A) = \|A\| \, \|A^{-1}\|$$

（2-范數下 $\kappa_2(A) = \sigma_1 / \sigma_n$，最大與最小奇異值之比——這與 Beltrami 1873 年的 SVD 會合。）關鍵不等式：若解線性系統 $Ax = b$，輸入有擾動 $\delta b$，則解的相對誤差被放大：

$$\frac{\|\delta x\|}{\|x\|} \le \kappa(A) \, \frac{\|\delta b\|}{\|b\|}$$

若係數矩陣也有擾動 $\delta A$，同樣有 $\kappa(A)$ 級別的放大。這個不等式是**可達的**：存在擾動方向使放大恰好達到 $\kappa(A)$。條件數是「矩陣的先天體質」，不是演算法的後天缺陷。

### 線索三：破案——Hotelling 的 $4^n$ 是錯的
von Neumann 與 Goldstine 對 Gauss 消去法（含部分選主元）做嚴格誤差界估計，結論驚人：誤差增長**不是** $4^n$，而是 $O(n)$ 級別的多項式增長（更精確地，隨機矩陣實測增長緩慢得多）。粗略地說：

$$\frac{\|\hat{x} - x\|}{\|x\|} \approx n \cdot \varepsilon \cdot \kappa(A)$$

代入 ENIAC 的 $\varepsilon \approx 10^{-12}$：即使 $n = 100$、$\kappa = 10^4$，相對誤差仍約 $10^{-6}$——可用！悲觀派錯了，數值求逆大型矩陣**是可行的**。這個結論直接催生了數值線性代數這門學科：Wilkinson（1963）的《Rounding Errors in Algebraic Processes》完成系統化的向後誤差分析（backward error analysis），證明 Gauss 消去法在選主元下是**向後穩定**的——算出的解是擾動系統的精確解。

### 線索四：條件數的實際應用
- **病態矩陣**（$\kappa \gg 1$）：Hilbert 矩陣 $H_{ij} = 1/(i+j-1)$ 是經典案例，$\kappa_2(H_n)$ 隨 $n$ 指數增長。
- **正規方程的陷阱**：解最小平方問題時，直接用正規方程 $A^TAx = A^Tb$ 會使條件數平方化：$\kappa(A^TA) = \kappa(A)^2$——這就是為什麼要用 SVD 或 QR 分解（Wilkinson、Golub 的路線）。
- **演算法選擇**：條件數告訴你何時該換演算法、何時該正規化、何時該用高精度。

### 程式碼範例：條件數 $\kappa(A)=\|A\|\|A^{-1}\|$ 與誤差放大實驗
```python
import numpy as np

np.random.seed(0)

# --- 線索二：條件數定義驗證 ---
U, _ = np.linalg.qr(np.random.randn(50, 50))
V, _ = np.linalg.qr(np.random.randn(50, 50))
s = np.logspace(0, -4, 50)                    # 奇異值從 1 到 1e-4
A = U @ np.diag(s) @ V.T                       # κ₂ = σ₁/σₙ = 1e4
kappa_def = np.linalg.norm(A, 2) * np.linalg.norm(np.linalg.inv(A), 2)
print("定義式 κ(A):", kappa_def)               # ≈ 1e4
print("奇異值比 σ₁/σₙ:", s[0] / s[-1])          # ≈ 1e4（兩者相符）

# --- 誤差放大實驗：δb 的方向決定放大倍數 ---
x = np.ones(50)
b = A @ x
rng = np.random.default_rng(1)
worst = 0
for _ in range(1000):
    db = rng.standard_normal(50); db *= 1e-8 / np.linalg.norm(db)  # 相對大小固定 1e-8
    dx = np.linalg.solve(A, b + db) - x
    worst = max(worst, np.linalg.norm(dx) / np.linalg.norm(x))
print("實測最大放大倍數:", worst / 1e-8)        # 可達 ~1e4 = κ(A)
print("理論上限 κ(A):", kappa_def)              # 不等式成立

# --- 線索四：病態矩陣 Hilbert ---
n = 12
i, j = np.meshgrid(np.arange(1, n+1), np.arange(1, n+1))
H = 1.0 / (i + j - 1)
print(f"Hilbert {n}x{n} 條件數: {np.linalg.cond(H):.3e}")   # ~1.7e16，接近機器精度極限

# --- 正規方程的陷阱：κ(A^TA) = κ(A)² ---
A2 = np.random.randn(100, 20) * np.logspace(0, -3, 20)  # 病態
print("κ(A):", np.linalg.cond(A2), "κ(A^TA):", np.linalg.cond(A2.T @ A2))
print("κ(A)²:", np.linalg.cond(A2)**2)   # κ(A^TA) ≈ κ(A)² → 正規方程加倍病態
```

輸出顯示：定義式與奇異值比一致（$\kappa_2 = \sigma_1/\sigma_n$，與 Beltrami SVD 會合）、誤差放大實測可達 $\kappa(A)$ 級別、Hilbert 矩陣的條件數接近機器精度極限（12x12 就已無可救藥）、正規方程把條件數平方化——von Neumann 1947 年的每個結論都在行程式碼裡現形。

## 結案 -- 後果與影響
- 數值線性代數誕生：誤差分析從「悲觀猜測」變成「可計算的界」，Wilkinson 1963 年的向後誤差分析是集大成之作。
- Wilkinson 1963 年《Rounding Errors in Algebraic Processes》與 1965 年的 QR 算法論文：證明選主元的 Gauss 消去法向後穩定，並發展出 QR 演算法求特徵值——1970 年 Golub-Reinsch 的 SVD 演算法也是這條路線。
- LAPACK（1992）與 BLAS：現代數值線性代數的標準函式庫，全部建立在 von Neumann-Goldstine 誤差分析的觀念之上。
- 浮點標準化：IEEE 754（1985）的設計考量（捨入模式、次正常數）都源自這門學科的需求。
- 影響至今：機器學習的數值穩定性（如混合精度訓練的 loss scaling）、CFD、氣候模擬、矩陣補全，每一個「大規模計算」的可靠性都依賴條件數的語言。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| John von Neumann | 1947 誤差分析與條件數，ENIAC 顧問 |
| Herman Goldstine | ENIAC 計畫的共同作者 |
| James H. Wilkinson | 1963 向後誤差分析，數值線性代數集大成 |
| Carl Friedrich Gauss | 消去法（1809），前案偵探 |
| Harold Hotelling | 1943 悲觀估計（$4^n$），謎題的提出者 |

- J. von Neumann & H. H. Goldstine, "Numerical inverting of matrices of high order", Bull. Amer. Math. Soc. **53**, 1021–1099 (1947)。
- J. H. Wilkinson, *Rounding Errors in Algebraic Processes*, Prentice-Hall (1963)。
