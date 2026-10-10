# 1969 — Strassen 矩陣乘法

## 案件摘要
1969 年，德國數學家 Volker Strassen 發表論文〈Gaussian elimination is not optimal〉，扔下一枚震撼彈：$n \times n$ 矩陣相乘**不需要** $n^3$ 次乘法。他用一個分塊技巧，把 8 次子塊乘法壓縮到 7 次，將複雜度降到 $O(n^{\log_2 7}) \approx O(n^{2.807})$——這是人類史上**第一次**打破矩陣乘法的立方壁壘。兇手不是更快的手指，而是一個更聰明的代數恆等式。

## 前因 -- 為什麼會有這個案子
- 矩陣乘法定義：$C_{ij} = \sum_{k=1}^n A_{ik}B_{kj}$。直接計算每個元素要 $n$ 次乘法，$n^2$ 個元素共 $n^3$ 次乘法——這是「定義」，但沒有人證明它是「下界」。
- 1950–60 年代，科學計算的核心工作負載就是矩陣乘法：結構力學、流體模擬、線性規劃。所有人都假設 $n^3$ 是天經地義。
- Strassen 的疑點來自一個更早的案件：他證明了**高斯消去法不是最佳解法**。既然消去法都能被質疑，那矩陣乘法這個更基本的操作，憑什麼被豁免？
- 計算複雜度理論正在成型：1965 年 Cobham、Edmonds 定義了多項式時間概念。數學家們開始追問「下界在哪裡」——但矩陣乘法的下界卻沒有人能證明超過 $\Omega(n^2)$（因為有 $n^2$ 個輸出）。
- 巨大的鴻溝：上界 $O(n^3)$、下界 $\Omega(n^2)$，中間一片黑暗。1969 年，Strassen 用一個「顯然不可能」的技巧，點亮了第一盞燈。

## 線索與推理 -- 數學式、程式、理論

### 線索一：分塊乘法與「8 次乘法」的宿命
把 $n \times n$ 矩陣切成四塊 $2\times 2$：

$$\begin{pmatrix} C_{11} & C_{12} \\ C_{21} & C_{22} \end{pmatrix} = \begin{pmatrix} A_{11} & A_{12} \\ A_{21} & A_{22} \end{pmatrix} \begin{pmatrix} B_{11} & B_{12} \\ B_{21} & B_{22} \end{pmatrix}$$

按定義展開，$C_{11} = A_{11}B_{11} + A_{12}B_{21}$，$C_{12} = A_{11}B_{12} + A_{12}B_{22}$，……共需 **8 次子塊乘法**（再加 4 次加法）。遞迴下去：$T(n) = 8T(n/2) + O(n^2)$，由主定理得 $T(n) = O(n^{\log_2 8}) = O(n^3)$。分塊沒有幫助——宿命似乎是鎖死的。

### 線索二：Strassen 的 7 次乘法恆等式
Strassen 的天才之舉：他發現 7 個精心設計的中間量，只需要 **7 次**子塊乘法：

$$\begin{aligned}
M_1 &= (A_{11}+A_{22})(B_{11}+B_{22}) \\
M_2 &= (A_{21}+A_{22})B_{11} \\
M_3 &= A_{11}(B_{12}-B_{22}) \\
M_4 &= A_{22}(B_{21}-B_{11}) \\
M_5 &= (A_{11}+A_{12})B_{22} \\
M_6 &= (A_{21}-A_{11})(B_{11}+B_{12}) \\
M_7 &= (A_{12}-A_{22})(B_{21}+B_{22})
\end{aligned}$$

然後組合出四塊結果：

$$\begin{aligned}
C_{11} &= M_1 + M_4 - M_5 + M_7 \\
C_{12} &= M_3 + M_5 \\
C_{21} &= M_2 + M_4 \\
C_{22} &= M_1 - M_2 + M_3 + M_6
\end{aligned}$$

驗證 $C_{12} = M_3 + M_5 = A_{11}B_{12} - A_{11}B_{22} + A_{11}B_{22} + A_{12}B_{22} = A_{11}B_{12} + A_{12}B_{22}$。展開後中間項**互相抵消**，結果正確。這就是代數的魔術：用加法交換「乘法次數」——乘法是貴的（7 次），加法是便宜的（18 次）。

遞迴複雜度：$T(n) = 7T(n/2) + O(n^2)$，由主定理：

$$T(n) = O(n^{\log_2 7}) = O(n^{2.807\ldots})$$

$n$ 越大，省得越多：$n = 1024$ 時，$\log_2 7 \approx 2.807$，$7^{10} = 282{,}475{,}249$ 次 vs $8^{10} = 1{,}073{,}741{,}824$ 次——**省了 3.8 倍**。

### 線索三：證明「正確性」與「遞迴結構」
Strassen 恆等式可以抽象地看：$2\times 2$ 矩陣乘法的張量秩（tensor rank）是 7 而非 8。這是「張量分解」概念的開端——後來 Bini、Capovani、Lotti（1979）用近似張量秩把指數降到 2.78，Schönhage 證明 $O(n^{2.522})$ 的理論上界……一路延續到 Coppersmith–Winograd（1990）的 $O(n^{2.376})$、Le Gall（2014）的 $O(n^{2.373})$、Alman–Vassilevska Williams（2021）的 $O(n^{2.37286})$。理論下界至今只有 $\Omega(n^2)$——鴻溝仍在，但已經被撕開一道大口子。

Strassen 演算法的實務限制：
1. **數值穩定性較差**：中間量的加減會累積誤差，誤差界比古典演算法差一個 $n$ 的多項式因子。高精度需求（如科學模擬）通常仍用古典法。
2. **遞迴深度與快取**：實務上遞迴到某個 cutoff（如 $n = 64$ 或 128）就切回古典法，因為小矩陣時加法開銷超過省下的乘法。
3. **記憶體存取**：分塊遞迴天然有利於快取局部性，這也是它在現代 GPU 上重新受到關注的原因之一。

### 線索四：從 1969 到深度學習
Strassen 的案件開啟了「計算複雜度 ≠ 直覺」的偵探時代：連乘法這種「顯然 $O(n^3)$」的操作都能被打破。這個精神在 2017 年 Transformer 的注意力機制、2020 年代的 LLM 訓練中持續發酵——矩陣乘法從「計算瓶頸」變成「效能指標」，硬體（GPU/TPU）專門為它設計張量核心（Tensor Core）。Strassen 的 7 次乘法在 GPU 上因為加法頻寬問題很少直接使用，但**分塊遞迴的快取策略**已經成為 cuBLAS、oneDNN 的標準配備。

### 程式碼範例：Strassen 分塊乘法 7 次乘法驗證
```python
import numpy as np

def strassen(A, B):
    n = A.shape[0]
    if n <= 64:                      # cutoff：小矩陣用古典法
        return A @ B
    m = n // 2
    A11, A12, A21, A22 = A[:m,:m], A[:m,m:], A[m:,:m], A[m:,m:]
    B11, B12, B21, B22 = B[:m,:m], B[:m,m:], B[m:,:m], B[m:,m:]

    # 7 次乘法（Strassen 恆等式）
    M1 = strassen(A11 + A22, B11 + B22)
    M2 = strassen(A21 + A22, B11)
    M3 = strassen(A11, B12 - B22)
    M4 = strassen(A22, B21 - B11)
    M5 = strassen(A11 + A12, B22)
    M6 = strassen(A21 - A11, B11 + B12)
    M7 = strassen(A12 - A22, B21 + B22)

    # 組合
    C11 = M1 + M4 - M5 + M7
    C12 = M3 + M5
    C21 = M2 + M4
    C22 = M1 - M2 + M3 + M6
    return np.vstack([np.hstack([C11, C12]), np.hstack([C21, C22])])

# 驗證 1：正確性
rng = np.random.default_rng(42)
A = rng.random((256, 256)); B = rng.random((256, 256))
C_s = strassen(A, B); C_n = A @ B
print("‖C_strassen - C_numpy‖ =", np.linalg.norm(C_s - C_n))   # ≈ 1e-13
print("相對誤差 =", np.linalg.norm(C_s - C_n) / np.linalg.norm(C_n))

# 驗證 2：遞迴乘法次數 7^k vs 8^k
for k in range(4, 11):
    n = 2**k
    print(f"n={n:5d}: 7^{k}={7**k:>12,d}  8^{k}={8**k:>13,d}  省倍率={8**k/7**k:.2f}")
```

輸出顯示 $\|C_{strassen} - C_{numpy}\| \approx 10^{-13}$（浮點誤差累積但可控），且 $n = 1024$ 時 Strassen 只需 $7^{10} \approx 2.8 \times 10^8$ 次乘法，相較古典分塊的 $8^{10} \approx 1.07 \times 10^9$ 次**省 3.8 倍**——$O(n^{2.807})$ 打破 $O(n^3)$ 的效應隨 $n$ 增大而放大。

## 結案 -- 後果與影響
- **計算複雜度理論誕生的催化劑**：Strassen 證明「下界不能靠直覺」，催生了代數複雜度（algebraic complexity）、張量秩理論、快速演算法研究。矩陣乘法指數 $\omega$ 成為理論電腦科學最重要的未解常數之一。
- **$\omega$ 的追逐戰**：1969 年 2.807 → 1978 年 Schönhage 2.522 → 1990 年 Coppersmith–Winograd 2.376 → 2014 年 Le Gall 2.373 → 2021 年 Alman–Vassilevska Williams 2.37286。理論與實務的鴻溝（實務仍用 $O(n^3)$ 的快取最佳化版本）本身就是一個懸案。
- **實務影響**：分塊遞迴與快取局部性成為 BLAS 程式庫（BLIS、cuBLAS、oneDNN）的標準策略；大型科學模擬與深度學習訓練間接受益。
- **理論電腦科學的連鎖效應**：Strassen 的技巧啟發了快速傅立葉變換之外的一系列「分治演算法」，包括快速矩陣求逆、快速多項式乘法（Schönhage–Strassen）。
- **機器學習時代**：矩陣乘法佔 LLM 訓練 90% 以上的 FLOPs，如何突破 $O(n^3)$ 成為理論與工程共同追問的問題——Strassen 1969 年的那盞燈，至今仍照亮著這條路。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Volker Strassen | 1969 年提出 7 次乘法分塊演算法 |
| Arnold Schönhage | 1978 年推進到 $O(n^{2.522})$ |
| Don Coppersmith & Shmuel Winograd | 1990 年 $O(n^{2.376})$ |
| François Le Gall | 2014 年 $O(n^{2.373})$ |
| Virginia Vassilevska Williams | 2012/2021 年多度刷新 $\omega$ 上界 |

- V. Strassen, *Gaussian elimination is not optimal*, Numer. Math. **13**, 354–356 (1969)。
- A. Schönhage & V. Strassen, *Schnelle Multiplikation großer Zahlen*, Computing **7**, 281–292 (1971)。
- D. Coppersmith & S. Winograd, *Matrix multiplication via arithmetic progressions*, J. Symb. Comput. **9**, 251–280 (1990)。
- F. Le Gall, *Powers of tensors and fast matrix multiplication*, ISSAC (2014)。
