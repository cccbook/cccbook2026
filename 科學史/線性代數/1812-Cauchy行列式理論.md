# 1812 — Cauchy 行列式理論

## 案件摘要
1812 年，29 歲的 Augustin-Louis Cauchy 向法國科學院提交長篇論文〈Mémoire sur les fonctions qui ne peuvent obtenir que deux valeurs égales et de signes contraires par suite des transpositions opérées entre les variables qu'elles renferment〉。他在這篇論文中第一次把行列式當作**獨立的研究對象**系統處理：證明行列式乘法規則 $\det(AB)=\det(A)\det(B)$、用拉丁方與置換的對稱性統一各種行列式恆等式，並把 "déterminant" 這個術語正式固定下來。線性代數的第一樁大案，就此立案。

## 前因 -- 為什麼會有這個案子
- 1683 年 Leibniz 在寫給 l'Hôpital 的信中，用類似行列式的數組消去聯立方程的未知數——這是現場最早的指紋，但手稿塵封到 19 世紀才出土。
- 1750 年 Cramer 在《代數曲線分析引論》中發表**Cramer 法則**：$n$ 元聯立方程的解可用係數行列式表為
  $$x_i = \frac{\det(A_i)}{\det(A)}$$
  但 Cramer 並沒有把這個數組當成獨立物件命名，只當成消去的「中間產物」。
- 1772 年 Vandermonde 在〈Mémoire sur l'élimination〉中首次認真研究「這個數組本身的性質」，甚至有交錯置換變號的初步觀察，可惜他不久轉向其他領域，線索中斷。
- 18 世紀末，Lagrange 已經在三元情形用過 $\det(AB)=\det(A)\det(B)$ 的特例（與乘積行列式有關的恆等式），但沒有一般證明。
- 案件動機：當時聯立方程、二次型、座標變換各處都在重複出現「同一個神祕數組」，卻沒有人對它建立完整法典。Cauchy 決定當這位立法者。

## 線索與推理 -- 數學式、程式、理論

### 線索一：行列式的置換定義
Cauchy 採用（今日稱為 Leibniz 公式，但 Cauchy 將其系統化）的定義：

$$\det(A) = \sum_{\sigma \in S_n} \mathrm{sgn}(\sigma)\, a_{1\sigma(1)} a_{2\sigma(2)} \cdots a_{n\sigma(n)}$$

其中 $\mathrm{sgn}(\sigma)$ 是置換的符號：偶置換為 $+1$、奇置換為 $-1$。Cauchy 在這篇論文中首次把「置換」當成獨立的代數物件來研究——換句話說，**群論的胚胎就藏在行列式的案子裡**。兩行（列）交換則變號、兩行相同則行列式為零、行線性性，這些今日稱為「行列式公理」的性質，都是從這個定義推演出來的偵訊筆錄。

### 線索二：拉丁方與乘法規則
Cauchy 用「拉丁方」的符號計法整理雙重和：把兩個指標分別記在行與列，若 $a_{\sigma(1)\tau(1)}\cdots a_{\sigma(n)\tau(n)}$ 這樣的項在雙重置換下，$\sigma\tau^{-1}$ 決定符號，則雙重求和可以合併。由此得到**行列式乘法定理**：

$$\det(AB) = \det(A)\,\det(B)$$

證明骨架：$\det(AB) = \sum_{\sigma}\mathrm{sgn}(\sigma)\prod_i \left(\sum_k a_{ik}b_{k\sigma(i)}\right)$，展開成雙重和後按 $\sigma\tau^{-1}$ 重新分組，拉丁方的對稱性保證每一組符號正確合併，收斂到 $\det(A)\det(B)$。

這條法則的幾何意義要到很久之後才看清：$\det$ 是線性映射下體積的縮放因子，複合映射的縮放因子當然是相乘的。但 Cauchy 純粹用代數手法就抓到了這條規律——不靠幾何直覺，靠的是置換的對稱性。

### 線索三：術語 "déterminant" 的確立
"determinant" 一詞其實是 Gauss 在 1801 年《Disquisitiones Arithmeticae》中用來指「二次型的判別式」（今日的 discriminant）。Cauchy 在 1812 年論文中把這個詞借來稱呼「這個神祕數組本身」，並在之後的講義與論文（尤其是 1815 年〈Mémoire sur le nombre des valeurs...〉）中持續使用，術語就此固定。此外 Cauchy 還引入了：
- 雙下標記法 $a_{ij}$（今日矩陣記法的遠祖）；
- 「交替函數」（fonctions alternées）的概念：變數置換會變號的函數，行列式正是最典型的交替函數。

### 線索四：異號成對的價值——為什麼是 ± 兩個值
論文標題說明了一切：這類函數在變數置換下「只能取兩個等值異號的值」。$n!$ 個項分兩大陣營（偶/奇置換），非黑即白。這種二值結構正是行列式有用的根源：$\det \neq 0$ 等價於線性獨立、可逆、唯一解。Cauchy 把這個二值性講清楚，等於把「方程組何時有唯一解」這個偵探問題給出了化學檢測法。

### 程式碼範例：Laplace 展開 vs. 置換定義 vs. 乘法規則驗證
```python
import numpy as np
from itertools import permutations

def det_by_permutation(A):
    """Leibniz/Cauchy 置換定義：sum sgn(sigma) prod a[i][sigma(i)]"""
    n = len(A)
    total = 0.0
    for sigma in permutations(range(n)):
        # 計算置換符號：數逆序數
        inv = sum(1 for i in range(n) for j in range(i+1, n) if sigma[i] > sigma[j])
        term = 1.0
        for i in range(n):
            term *= A[i][sigma[i]]
        total += (-1)**inv * term
    return total

def laplace_expansion(A):
    """Laplace 沿第一行展開（遞迴）"""
    n = len(A)
    if n == 1:
        return A[0][0]
    total = 0.0
    for j in range(n):
        minor = [row[:j] + row[j+1:] for row in A[1:]]
        total += (-1)**j * A[0][j] * laplace_expansion(minor)
    return total

rng = np.random.default_rng(42)
A = rng.normal(size=(4, 4))
B = rng.normal(size=(4, 4))

d1 = det_by_permutation(A)
d2 = laplace_expansion(A)
d3 = np.linalg.det(A)
print(f"置換定義   det(A) = {d1:.10f}")
print(f"Laplace    det(A) = {d2:.10f}")
print(f"numpy      det(A) = {d3:.10f}")

# 乘法規則 det(AB) = det(A) det(B)
lhs = np.linalg.det(A @ B)
rhs = np.linalg.det(A) * np.linalg.det(B)
print(f"det(AB)          = {lhs:.10f}")
print(f"det(A)·det(B)    = {rhs:.10f}")
print("相對誤差 =", abs(lhs - rhs) / abs(lhs))
```

三種方法算出的行列式完全一致（相對誤差在浮點精度內），$\det(AB)=\det(A)\det(B)$ 也數值成立——Cauchy 1812 年的紙筆推理，今日一行 numpy 即可重審。

## 結案 -- 後果與影響
- 行列式從「消去法的副產品」升格為**獨立的代數物件**，理論自此系統化。
- Cauchy 對置換的研究直接啟發了群論：Galois 1830 年代用置換群解五次方程之謎，語言正是 Cauchy 建立的。
- 乘法定理 $\det(AB)=\det(A)\det(B)$ 日後成為理解「可逆矩陣、相似變換、體積縮放」的基石。
- 1841 年 Jacobi 把行列式推廣到函數行列式（Jacobian），線索繼續延伸。
- 1850 年 Sylvester 為「生出行列式的數組」命名 matrix，1888 年 Peano 的公理化向量空間收網——整條線性代數的案情鏈，起點在 1812 年這篇論文。
- 影響至今：每本線性代數教科書第一章的行列式，敘事順序仍是 Cauchy 的偵訊筆錄。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Augustin-Louis Cauchy | 行列式理論的立法者 |
| Alexandre-Théophile Vandermonde | 最早的獨立研究者，線索開端 |
| Gabriel Cramer | Cramer 法則（1750） |
| Carl Friedrich Gauss | "determinant" 一詞的最初使用者（指判別式） |
| Joseph-Louis Lagrange | 三元乘積恆等式的先驅 |

- A.-L. Cauchy, *Mémoire sur les fonctions qui ne peuvent obtenir que deux valeurs égales et de signes contraires...*, J. Éc. Polytech. **10**, 29–112 (1812)。
- A.-L. Cauchy, *Mémoire sur le nombre des valeurs qu'une fonction peut acquérir...*, J. Éc. Polytech. **10**, 1–28 (1815)。
- A.-T. Vandermonde, *Mémoire sur l'élimination*, Hist. Acad. R. Sci. Paris (1772)。
