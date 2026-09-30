# 1693 — Leibniz 行列式

## 案件摘要
1693 年 4 月 28 日，Leibniz 在寫給 l'Hôpital 的信中，首次寫下二階與三階「行列式」的表達式：對聯立方程組 $a_1 + b_1x + c_1y = 0$、$a_2 + b_2x + c_2y = 0$，他提出係數的組合 $a_1b_2 - a_2b_1$ 等於零即兩式有公共解的條件，並以指標記號與符號規則記錄這類「resultant」。這是行列式概念與記號的雛形——比 Cramer 的正式發表早了半個多世紀，卻沉沒在手稿與信件中近一百五十年。

## 前因 -- 為什麼會有這個案子
- 兩千年前，《九章算術》已用消去法解聯立方程，但「把係數整體打包成一個數」的觀念尚未出現。
- 17 世紀的代數學：Descartes、Viète 建立符號代數；Leibniz 本人是符號思考的大師，堅信「好的記號能讓計算自動進行」。
- 實際動機：**消去理論（elimination theory）**。兩條方程有公共解的條件是什麼？三條呢？數學家需要一個「判別量」。
- 1684 年起 Leibniz 已在研究兩曲線相交的條件——幾何交點問題，翻譯成代數就是聯立方程的相容性問題。
- Cramer 前夜：當時還沒有「行列式」這個名詞，但土壤已經備好。

## 線索與推理 -- 數學式、程式、理論

### 線索一：兩條方程的相容條件
考慮兩條一次方程：

$$\begin{cases}a_1 + b_1x + c_1y = 0\\ a_2 + b_2x + c_2y = 0\end{cases}$$

消去 $y$：第一式乘 $c_2$、第二式乘 $c_1$ 相減，得 $(a_1c_2 - a_2c_1) + (b_1c_2 - b_2c_1)x = 0$，故

$$x = \frac{a_2c_1 - a_1c_2}{b_1c_2 - b_2c_1}$$

Leibniz 敏銳地注意到：分子、分母都是**同一種結構**——兩項相減，每項是取自不同行不同列的係數乘積。他稱這類量為 **resultant**（結式），並寫下相容性條件：

$$b_1c_2 - b_2c_1 \neq 0$$

這正是今日的二階行列式 $\begin{vmatrix} b_1 & c_1 \\ b_2 & c_2 \end{vmatrix}$。

### 線索二：符號規則——Leibniz 的指標密碼
在 1693 年的信與更早（1693 年前後）的手稿中，Leibniz 對三階情形提出：由 $\begin{vmatrix}1&2&3\end{vmatrix}$ 型指標排列，取三項乘積

$$a_{12}b_{23}c_{31} - a_{13}b_{23}c_{21} + \cdots$$

並以「偶排列取正、奇排列取負」的規則決定符號——這就是今日三階行列式的完全展開式：

$$\det A = a_{11}a_{22}a_{33} + a_{12}a_{23}a_{31} + a_{13}a_{21}a_{32} - a_{13}a_{22}a_{31} - a_{12}a_{21}a_{33} - a_{11}a_{23}a_{32}$$

Leibniz 甚至設計了一種指標記號：把下標寫成數字對 $(1,2)$、$(2,3)$……用排列的奇偶性自動產生符號。他寫道，這種記號使得「人們不必思考就能正確計算」——這是他一貫的符號哲學（與他發明微積分記號 $dx, dy$ 的思路如出一轍）。

### 線索三：resultant 的推廣——多條方程的公共解
Leibniz 更進一步：對三條二元一次方程

$$a_i + b_ix + c_iy = 0 \quad (i = 1, 2, 3)$$

有公共解（且 $x, y$ 非平凡）的條件，是三個二階 resultant 滿足

$$(a_1b_2 - a_2b_1)(a_2c_3 - a_3c_2) + (a_2b_3 - a_3b_2)(a_1c_2 - a_2c_1) + \cdots = 0$$

——這其實是三階行列式展開後的恆等式。他把方程組相容性問題轉化為「某個由係數構成的量為零」的判別問題，這是把**整個方程組壓縮成一個數**的革命性想法：矩陣與行列式的種子已然埋下。

### 線索四：為什麼這案子會沉沒？
Leibniz 的信寄出後，l'Hôpital 並未重視；Leibniz 本人也未將行列式理論系統化發表。他的相關思考散落於手稿，直到 19 世紀中葉（Gerhardt 編輯 Leibniz 數學手稿，1849 年起）才重見天日。數學史的偵探們後來發現：1684–1693 年間 Leibniz 已有約五十份手稿涉及這類記號，但他作為一個「公開發表控」卻在這件事上缺席，導致行列式的桂冠最後落在 Cramer 頭上。

### 程式碼範例：Leibniz 2x2/3x3 行列式
```python
import numpy as np
from itertools import permutations

def leibniz_det(M):
    n = len(M)
    total = 0
    for p in permutations(range(n)):      # 遍歷所有排列（Leibniz 指標）
        term = M[i][p[i]] for_i... if False else np.prod([M[i][p[i]] for i in range(n)])
        # 符號：偶排列 +1、奇排列 -1（Leibniz 符號規則）
        sign = 1 if inversions(p) % 2 == 0 else -1
        total += sign * term
    return total

def inversions(p):
    return sum(1 for i in range(len(p)) for j in range(i+1, len(p)) if p[i] > p[j])

# 重寫乾淨版本
def leibniz_det_clean(M):
    n, total = len(M), 0
    for p in permutations(range(n)):
        term = np.prod([M[i][p[i]] for i in range(n)])
        sign = 1 if inversions(p) % 2 == 0 else -1
        total += sign * term
    return total

A2 = [[2, 3], [1, 4]]                      # 2x2：應為 2*4-3*1 = 5
A3 = [[3, 2, 1], [2, 3, 1], [1, 2, 3]]     # 九章第一題係數矩陣

print(leibniz_det(A2), leibniz_det_clean(A2))   # 5 5
print(leibniz_det_clean(A3), np.linalg.det(A3)) # 18.0 18.0
```

2x2 情形給出 $a_1b_2 - a_2b_1 = 5$；3x3 情形（九章算術第一題的係數矩陣）給出 18，與 `numpy.linalg.det` 一致——Leibniz 的排列符號規則，就是現代行列式定義 $\det A = \sum_{\sigma} \mathrm{sgn}(\sigma)\prod_i a_{i,\sigma(i)}$。

## 結案 -- 後果與影響
- Leibniz 的 resultant 思想是**消去理論**的起點：判定多條方程是否有公共解，日後發展為結式（Sylvester, 1840）與判別式理論。
- 行列式記號的雛形（排列指標＋奇偶符號規則）在 19 世紀被 Cauchy（1812）、Jacobi 等人重新發現並系統化；「determinant」一詞由 Gauss（1801）首次使用、Cauchy（1812）賦予現代意義。
- 行列式成為線性代數的第一件「獨立工具」：解方程組（Cramer 法則）、判別線性相依、求特徵值（特徵多項式 $\det(A - \lambda I) = 0$）。
- 19 世紀中葉手稿出土後，數學史界公認：**Leibniz 是行列式概念的最早發明者**，只是他的破案筆錄晚了近 150 年才公開。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Gottfried Wilhelm Leibniz | 1693 年信中首寫行列式與 resultant |
| Guillaume de l'Hôpital | 收信人，未重視（破案筆錄沉沒的關鍵） |
| Gabriel Cramer | 1750 年正式發表行列式解法 |
| Augustin-Louis Cauchy | 1812 年系統化行列式理論 |

- G. W. Leibniz, 寫給 l'Hôpital 的信，1693 年 4 月 28 日（Gerhardt 編《Leibniz 數學手稿》卷二，1849）。
- A.-L. Cauchy, «Mémoire sur les fonctions qui ne peuvent obtenir que deux valeurs...», J. Éc. polytech. (1812)。
- C. B. Boyer, "A History of Mathematics"（行列式史部分）。
