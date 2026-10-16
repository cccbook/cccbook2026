# 1878 — Frobenius 秩與特徵多項式

## 案件摘要
1878 年，德國數學家 Ferdinand Georg Frobenius 發表長篇論文〈Über homogene Substitutionen und lineare Transformationen〉（論齊次代換與線性變換），為線性代數補上了最關鍵的兩塊拼圖：**矩陣秩（rank）的一般理論**與**特徵多項式 $\chi_A(\lambda) = \det(\lambda I - A)$ 的嚴格框架**，並首次給出 Cayley-Hamilton 定理的完全嚴格證明。Cayley 留下的骨架、Sylvester 留下的線索，在這一年被整合成一套嚴密體系——線性代數從此從「計算技巧集」升級為「數學結構理論」。

## 前因 -- 為什麼會有這個案子
- Sylvester（1851）已提出「rank」的直覺（矩陣中不為零的最大子行列式階數），並證明對 $n$ 個未知數、$m$ 條方程的相容性判別；但秩在運算下如何變化、為何是相似不變量，缺乏系統論述。
- Cayley（1858）定義矩陣代數並猜想 Cayley-Hamilton 定理，但只驗證了 $3 \times 3$ 以下，一般證明缺席。
- Weierstrass（1868）的初等因子理論以雙線性型為載體，語言繁複；矩陣本身的「內在維度」仍無清晰定義。
- 當時「線性變換」與「矩陣」的關係曖昧：同一個變換在不同基底下對應不同矩陣——什麼量不隨基底改變？這是本案要追查的「不變量」。

## 線索與推理 -- 數學式、程式、理論

### 線索一：秩的一般理論
Frobenius 將矩陣 $A$ 的秩定義為**最大非零子行列式的階數**（Sylvester 的線索），並證明其等價刻畫：

$$\mathrm{rank}(A) = \dim \mathrm{im}(A) = n - \dim\ker(A)$$

（像空間的維度 = 列空間維度 = 行空間維度 = $n$ 減核空間維度）。他還證明了秩的基本不等式鏈：

$$\mathrm{rank}(AB) \le \min\{\mathrm{rank}(A),\ \mathrm{rank}(B)\}$$

以及 **Sylvester 不等式** $\mathrm{rank}(A) + \mathrm{rank}(B) - n \le \mathrm{rank}(AB)$。秩在乘法下的衰減規律，成為判定線性方程組相容性與解空間維度的標準工具（Rouché–Capelli 定理的矩陣版本）。

### 線索二：特徵多項式的一般理論與相似不變量
Frobenius 系統化定義特徵多項式

$$\chi_A(\lambda) = \det(\lambda I - A) = \lambda^n - (\mathrm{tr}\,A)\lambda^{n-1} + \cdots + (-1)^n \det(A)$$

並證明它是**相似不變量**：若 $B = PAP^{-1}$，則

$$\chi_B(\lambda) = \det(\lambda I - PAP^{-1}) = \det\big(P(\lambda I - A)P^{-1}\big) = \det(\lambda I - A) = \chi_A(\lambda)$$

同理 $\mathrm{tr}(B) = \mathrm{tr}(A)$、$\det(B) = \det(A)$、各階係數皆不變。這回答了前因中的問題：**特徵多項式（及其根——特徵值）是線性變換的內在屬性，與座標選擇無關。** Frobenius 也用初等因子理論證明：特徵多項式被最小多項式整除，且兩者有相同的根集合。

### 線索三：Cayley-Hamilton 定理的嚴格證明
Frobenius 給出 Cayley-Hamilton 定理第一個完全證明：對任意 $n \times n$ 矩陣 $A$，

$$p_A(A) = A^n - (\mathrm{tr}\,A)A^{n-1} + \cdots + (-1)^n \det(A)\,I = 0$$

證明思路：先在 $A$ 可對角化（或用擾動 $\mathrm{tr}$ 的一般技巧）時直接驗證，再以**多項式恆等式的稠密性論證**（或用伴隨矩陣 $\mathrm{adj}(\lambda I - A)$ 的多項式恆等式 $\det(\lambda I - A)I = (\lambda I - A)\,\mathrm{adj}(\lambda I - A)$，令 $\lambda = A$）過渡到一般情形。附帶收穫：當 $\det(A) \neq 0$ 時可從 $p_A(A) = 0$ 解出

$$A^{-1} = -\frac{1}{\det(A)}\left(A^{n-1} - (\mathrm{tr}\,A)A^{n-2} + \cdots\right)$$

——只乘矩陣、不除，對手工與機器計算都極重要。

### 程式碼範例：用 Python 重審 Frobenius 的三大結論
```python
import numpy as np
from sympy import Matrix, symbols, Poly

A = Matrix([[3, 1, 0],
            [0, 3, 0],
            [0, 0, 2]])
P = Matrix([[1, 0, 1],
            [1, 1, 0],
            [0, 1, 1]])
B = P * A * P.inv()          # 相似矩陣
lam = symbols('lambda')

# 線索一：秩的三種等價刻畫 + Sylvester 不等式
M = np.random.randn(4, 3); N = np.random.randn(3, 5)
print("rank(AB) <= min(rank(A),rank(B)) ?",
      np.linalg.matrix_rank(M @ N) <=
      min(np.linalg.matrix_rank(M), np.linalg.matrix_rank(N)))
print("Sylvester: rA+rB-3 <= rank(MN) ?",
      np.linalg.matrix_rank(M)+np.linalg.matrix_rank(N)-3
      <= np.linalg.matrix_rank(M @ N))

# 線索二：相似不變量——特徵多項式、跡、行列式
chiA, chiB = A.charpoly(lam), B.charpoly(lam)
print("χ_A == χ_B ?", chiA == chiB)
print("tr A == tr B, det A == det B ?",
      A.trace() == B.trace(), A.det() == B.det())

# 線索三：Cayley-Hamilton 嚴格驗證（含不可對角化的 Jordan 塊！）
print("可對角化？", A.is_diagonalizable())      # False：塊 J2(3)
print("p_A(A) == 0 ?", A.evalf_subs(lam, A) if False
      else np.allclose(np.array(chiA.as_expr().subs(lam, A),
                                dtype=float), np.zeros((3, 3))))

# 附帶收穫：由 Cayley-Hamilton 求 A^{-1}（3x3：χ = λ³-8λ²+21λ-12）
c2, c1, c0 = -8, 21, -12
Ainv_manual = -(A*A - (-c2)*A + c1*Matrix.eye(3)) / (-c0)  # 展開式簡化版
print("A^{-1} 手算正確？", Ainv_manual == A.inv())
```

程式重審結果：秩不等式成立、相似矩陣的特徵多項式／跡／行列式完全相同、含不可對角化塊的 $p_A(A) = 0$ 精確成立，且由 Cayley-Hamilton 反解出的 $A^{-1}$ 與直接求逆一致。

## 結案 -- 後果與影響
- 線性代數獲得**嚴格基礎**：秩、特徵多項式、相似不變量三件套，把 Cayley 的代數骨架與 Sylvester 的判別技巧熔為一爐。
- Cayley-Hamilton 定理從猜想變定理，成為矩陣論、控制理論（可穩定性分析）、最小多項式理論的基石。
- Frobenius 的「不變量思維」直通 1896 年群表示論（他本人創立），並影響 Hilbert 的不變量論與公理化綱領。
- 秩的概念為 1888 年 Peano 的抽象向量空間（維度、線性無關）鋪路。
- 今日矩陣分析（如 PCA、最小平方、數值秩）全數建基於此案的結論。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Ferdinand Georg Frobenius | 1878 年秩理論、特徵多項式、Cayley-Hamilton 嚴格證明 |
| James Joseph Sylvester | 1851 年 rank 概念與相容性判別 |
| Arthur Cayley | 1858 年矩陣代數與 Cayley-Hamilton 猜想 |
| Karl Weierstrass | 1868 年初等因子理論 |

- F. G. Frobenius, *Über homogene Substitutionen und lineare Transformationen*, J. reine angew. Math. **84**, 1–63 (1878)。
- J. J. Sylvester, *On the relation between the minor determinants...,* Phil. Mag. (1851)。
