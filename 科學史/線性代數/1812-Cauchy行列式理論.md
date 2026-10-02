# 1812 — Cauchy 行列式理論

## 案件摘要
1812 年，28 歲的 Augustin-Louis Cauchy 在巴黎發表兩篇重磅論文（一篇法文〈Mémoire sur les fonctions qui ne peuvent obtenir que deux valeurs égales et de signes contraires...〉，一篇拉丁文〈DeBinis...〉系列），首次把「行列式」當成一個獨立的數學物件系統研究：確立了雙重下標記法 $a_{ij}$、證明乘法規則 $\det(AB)=\det(A)\det(B)$、系統研究行列式的對稱性質。混亂的「符號偵探學」從此變成有法可依的偵探科學。

## 前因 -- 為什麼會有這個案子
- 1683 年 Leibniz 在寫給 l'Hôpital 的信中已經使用類似行列式的陣列來解線性方程組，但符號笨重、無人跟進——第一樁懸案石沉大海。
- 1750 年 Cramer 在《曲線解析引論》中提出 **Cramer 法則**：$n$ 個未知數、$n$ 個方程的解可以用係數陣列的比值表示。但他沒有給這個「陣列」正式的名字與理論，符號的合法性來自直覺。
- 1772 年 Vandermonde 在巴黎科學院宣讀論文，研究如何用「帶符號的乘積和」計算行列式，並對特殊結構（如循環規則）給出聰明算法。Bézout 也在同期研究消去法中的結式。但這些都是「個案偵辦」，沒有統一的理論框架。
- 1800 年前後，Gauss 在《算術研究》處理二次型時用「行列式」一詞（determinans，指二次型的判別式性質），但含義與今日不同。
- 案件的核心疑問：這些散落各處的符號技巧，究竟是不是同一個數學物件？它有沒有自己的運算律？

## 線索與推理 -- 數學式、程式、理論

### 線索一：雙重下標記法與定義
Cauchy 的第一大功績是記法。他把 $n$ 階行列式寫成方陣 $(a_{ij})$，其中第一個下標 $i$ 標示行、第二個下標 $j$ 標示列，並定義：

$$\det(A) = \sum_{\sigma \in S_n} \operatorname{sgn}(\sigma)\, a_{1\sigma(1)} a_{2\sigma(2)} \cdots a_{n\sigma(n)}$$

其中 $\sigma$ 跑遍所有 $n!$ 個置換，$\operatorname{sgn}(\sigma)$ 是置換的符號（偶置換 $+1$、奇置換 $-1$）。Cauchy 是第一個清楚地把「符號」與「置換的奇偶性」綁在一起的人——他甚至發展了置換理論（後來成為群論的養分）來當偵查工具。

### 線索二：乘法規則 $\det(AB) = \det(A)\det(B)$
1812 年論文的高潮是證明：兩個行列式的乘積等於「乘積行列式」。用今日記法：

$$\det(AB) = \det(A)\,\det(B)$$

Cauchy 用雙重和與置換符號的乘法性質 $\operatorname{sgn}(\sigma\tau) = \operatorname{sgn}(\sigma)\operatorname{sgn}(\tau)$ 證明此式。他還給出一個漂亮的組合表述：乘積 $\det(A)\det(B)$ 等於把 $A$ 的第 $i$ 行與 $B$ 的第 $i$ 列「配對」後形成的所有「合成項」之和——這就是所謂 **Cauchy–Binet 公式**的雛形（完整版 1815 年由 Cauchy 本人給出，處理非方陣情形）：

$$\det(AB) = \sum_{S} \det(A_{[n],S})\det(B_{S,[n]})$$

其中 $S$ 跑遍所有 $n$ 元子集。這條公式像指紋比對：把兩個嫌疑人的特徵逐一組合，得到第三人的完整特徵。

### 線索三：拉丁方與對稱性
Cauchy 觀察到行列式展開式中各項的正負號排列，可以用「拉丁方」（每行每列符號恰出現一次的方陣）來記憶。3 階與 4 階的符號方陣呈現完美對稱：沿主對角線翻轉不變、符號成對出現。他系統列出一系列恆等式：

- 轉置不變：$\det(A^T) = \det(A)$（Cauchy 證明，解釋了行與列的地位對等）
- 兩行（列）交換則變號：$\det(\cdots \text{swap} \cdots) = -\det(A)$
- 一行乘 $c$ 加到另一行：行列式不變
- 兩行相同則行列式為零：$\det(A) = 0$

這些「偵查守則」至今就是每一本線性代數教科書第一章的內容。Cauchy 還研究**對稱函數與交錯函數**：行列式是變數的交錯函數，這正是他 1812 年法文論文的標題主題。

### 程式碼範例：Laplace 展開驗證 Cauchy 恆等式
```python
import numpy as np
from itertools import permutations, combinations

def det_bruteforce(A):
    n = len(A)
    total = 0.0
    for p in permutations(range(n)):
        sgn = 1
        pl = list(p)
        for i in range(n):              # 計算置換符號（氣泡排序法）
            for j in range(i+1, n):
                if pl[j] < pl[i]:
                    sgn = -sgn
        prod = 1.0
        for i in range(n):
            prod *= A[i][p[i]]
        total += sgn * prod
    return total

def det_laplace(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    total = 0.0
    for j in range(n):                  # 沿第一行 Laplace 展開
        minor = [row[:j] + row[j+1:] for row in A[1:]]
        total += ((-1)**j) * A[0][j] * det_laplace(minor)
    return total

A = [[2, 1, 3], [0, -1, 4], [5, 2, 1]]
B = [[1, 0, 2], [3, 1, 1], [0, 2, -1]]
AB = [[sum(A[i][k]*B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]

print("brute force det(A)      =", det_bruteforce(A))
print("Laplace    det(A)      =", det_laplace(A))
print("det(AB)                =", det_bruteforce(AB))
print("det(A)*det(B)          =", det_bruteforce(A)*det_bruteforce(B))
print("det(A^T)               =", det_bruteforce(list(map(list, zip(*A)))))

# Cauchy–Binet：對 2x3 乘 3x2 的驗證
A2 = [[1, 2, 0], [3, 1, 4]]
B2 = [[2, 1], [0, 3], [1, 1]]
cb = sum(det_laplace([[A2[i][s] for s in S] for i in range(2)]) *
         det_laplace([[B2[s][j] for j in range(2)] for s in S])
         for S in combinations(range(3), 2))
AB2 = [[sum(A2[i][k]*B2[k][j] for k in range(3)) for j in range(2)] for i in range(2)]
print("Cauchy–Binet sum       =", cb, " det(AB) =", det_laplace(AB2))
```

輸出顯示三條線索全部吻合：暴力展開與 Laplace 展開相等、$\det(AB)=\det(A)\det(B)$、$\det(A^T)=\det(A)$、Cauchy–Binet 和恰等於 $\det(AB)$。

## 結案 -- 後果與影響
- 行列式從「解方程的符號技巧」升格為**獨立的代數物件**，擁有自己的定義、記法與運算律。
- Cauchy 的置換符號理論直接餵養了 1840–1880 年代 Galois、Jordan 的群論。
- 1841 年 Jacobi 站在 Cauchy 肩膀上，把行列式推廣到**函數行列式（Jacobian）**，打開多元微積分的大門。
- 1850 年 Sylvester 創造 "matrix" 一詞、1858 年 Cayley 建立矩陣代數——兇器（陣列）終於有了正式身分證。
- 「determinant」一詞由 Gauss 使用的 determinans 經 Cauchy 確立為今日術語。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Augustin-Louis Cauchy | 系統化行列式理論、證明乘法規則 |
| Alexandre-Théophile Vandermonde | 早期行列式算法（1772） |
| Gabriel Cramer | Cramer 法則（1750） |
| Carl Friedrich Gauss | determinans 一詞的先行者 |
| Pierre-Simon Laplace | Laplace 展開（1772） |

- A.-L. Cauchy, *Mémoire sur les fonctions qui ne peuvent obtenir que deux valeurs égales et de signes contraires par suite des transpositions opérées entre les variables qu'elles renferment*, J. Éc. Polytech. **10**, 29–112 (1812)。
- A.-L. Cauchy, *Mémoire sur le nombre des valeurs qu'une fonction de plusieurs variables peut acquérir...*, J. Éc. Polytech. **10**, 1–28 (1815)。
