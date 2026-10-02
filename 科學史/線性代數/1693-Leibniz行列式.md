# 1693 — Leibniz 行列式

## 案件摘要
1693 年 4 月 28 日，Gottfried Wilhelm Leibniz 在寫給法國數學家 l'Hôpital 的信中，首次寫下了形如 $a_1b_2 - a_2b_1$ 的數字排列計算——也就是今日所謂的二階行列式，並用一種「指數對」的巧妙記號推廣到 $n$ 個未知數的聯立方程組。這是行列式觀念在西方的第一次現身，比 Cramer 的一般法則早了半個多世紀。本案追查：這位微積分的共同發明人，為何會在解方程組時創造出這個後來席捲線性代數的物件？

## 前因 -- 為什麼會有這個案子
- **解聯立方程的困境**：十七世紀的代數學家處理兩個、三個未知數的方程組時，靠的是逐一消元。消元本身不難，難的是：能不能直接從係數「讀出」方程組何時有解？解是什麼？
- **Seki Takakazu 的平行案件**：幾乎同一時期（1683 年左右），日本數學家關孝和在《解伏題之法》中也獨立發展出行列式的概念，用來處理消元後的方程組——東西方在同一十年、互不知情的情況下撞出了同一個觀念。
- **九章算術的遠古線索**：消去法早在中國漢代已經成熟；Leibniz 要解決的不是「如何消元」，而是「消元之後，解的公式長什麼樣」——他要的是一個封閉的顯式公式。
- **與 l'Hôpital 的通信**：Leibniz 與這位法國年輕貴族通信多年，講授微積分。1693 年的這封信，是他向對方報告一個「新發明」——結果這個發明被歷史遺忘了近一百五十年，直到 1850 年前後 Leibniz 的手稿被整理出版，世人才知道他早就到過案發現場。

## 線索與推理 -- 數學式、程式、理論

### 線索一：二階行列式的誕生
考慮二元一次方程組：
$$\begin{cases}a_1x + b_1y = c_1\\a_2x + b_2y = c_2\end{cases}$$
消去 $y$：第一式乘 $b_2$、第二式乘 $b_1$、相減，得
$$(a_1b_2 - a_2b_1)x = c_1b_2 - c_2b_1 \quad\Rightarrow\quad x = \frac{c_1b_2 - c_2b_1}{a_1b_2 - a_2b_1}$$
Leibniz 注意到：分子分母都是「交叉相乘再相減」的固定花樣。他給這個花樣起了名字——**resultant**（結式）：當 $a_1b_2 - a_2b_1 = 0$ 時方程組退化（無解或無限多解），係數的這個組合「決定了方程組的命運」。

### 線索二：指數對記號——行列式記號的雛形
為了推廣到 $n$ 個未知數，Leibniz 發明了一個極具前瞻性的記號：他把係數寫成 $10$、$21$、$32$ 這樣的「指數對」，第一個數字標記方程的編號（直行的位置），第二個數字標記未知數的編號（橫列的位置）。這正是**雙下標矩陣記號 $a_{ij}$** 的前身——比正式的矩陣記號早了兩百年。用這套記號，他寫下三元情形：
$$\begin{vmatrix} a_{10} & a_{11} & a_{12} \\ a_{20} & a_{21} & a_{22} \\ a_{30} & a_{31} & a_{32} \end{vmatrix} = a_{10}a_{21}a_{32} + a_{11}a_{22}a_{30} + a_{12}a_{20}a_{31} - a_{12}a_{21}a_{30} - a_{10}a_{22}a_{31} - a_{11}a_{20}a_{32}$$
六項，正好是 $3! = 6$ 個排列；正負號由排列的奇偶性決定。Leibniz 已經掌握了行列式的一般定義：**所有「每行每列各取一個」的乘積項之帶符號總和**。

### 線索三：為什麼是這個花樣？——從消元的視角看
$n$ 階行列式可以看成消元公式的封裝。用現代記號，對 $2\times2$ 矩陣 $A = \begin{pmatrix}a & b\\ c & d\end{pmatrix}$：
$$\det A = ad - bc$$
它的幾何意義（Leibniz 未察覺、後由 Gauss 時代補足）是列向量張成的平行四邊形面積；$\det A = 0$ 表示兩列共線、向量「塌陷」，方程組退化。行列式是「可解性」的偵測器：
- $\det A \neq 0$：唯一解；
- $\det A = 0$：無解或無限多解。

此外，Leibniz 在同期手稿中還嘗試把這套方法應用到**多項式的公共根**（兩個多項式何時有共同解）——resultant 一詞在今日代數學中正是「結式」：$\mathrm{Res}(f, g) = 0$ 若且唯若 $f$、$g$ 有公共根。從二元方程組的係數偵測，到多項式公共根的偵測，Leibniz 看到的是同一個結構：**「退化」總會在某個由係數組成的多項式歸零時現形**。這個思想在十九世紀由 Sylvester、Bézout 的結式理論正式完成，成為計算機代數系統中消去理論的核心。

### 線索四：與 Cramer 法則的前夜
Leibniz 的信中已經隱含了「用兩個 resultants 之比表出未知數」的想法——正是五十七年後 Cramer 法則 $x_i = \det(A_i)/\det(A)$ 的雛形。但他只處理了小規模情形，也沒有系統性地展開 $n$ 個未知數的一般公式。歷史把「掛名」留給了 Cramer——這是科學史上著名的「發明者被遺忘」案件之一。

### 程式碼範例：Leibniz 2x2 行列式與 resultant 驗證
```python
import numpy as np

def leibniz_det2(A):
    (a, b), (c, d) = A
    return a * d - b * c          # 交叉相乘相減

def leibniz_det3(A):
    # 按 Leibniz 的一般定義：3! = 6 個帶符號項
    from itertools import permutations
    s = 0
    for p in permutations(range(3)):
        term, sign = 1, 1
        for row, col in enumerate(p):
            term *= A[row][col]
        sign = (-1) ** sum(1 for i in range(3) for j in range(i+1, 3) if p[i] > p[j])
        s += sign * term
    return s

A = np.array([[3., 1.], [2., 3.]])
print("Leibniz det2 =", leibniz_det2(A))            # 7
print("numpy 驗證   =", np.linalg.det(A))           # 7.0

B = [[2, -1, 1], [1, 3, -2], [3, 1, 0]]
print("Leibniz det3 =", leibniz_det3(B))            # 逐項 6 項展開
print("numpy 驗證   =", np.linalg.det(np.array(B, float)))

# resultant = 0 的退化偵測：兩列共線
D = np.array([[1., 2.], [2., 4.]])
print("退化方程組 resultant =", leibniz_det2(D))     # 0 → 無唯一解
```

`leibniz_det3` 逐項驗證了六項帶符號展開與 `numpy.linalg.det` 完全一致；退化矩陣 $D$ 的 resultant 為零，正對應「兩列共線、方程組退化」的偵測結果。

## 結案 -- 後果與影響
- 1693 年的信是**行列式理論在西方的開端**：Leibniz 首次把「係數的帶符號組合」當成一個有名字、有用途的數學物件（resultant）。
- 他的**雙下標「指數對」記號**預示了兩百年後的矩陣記號 $a_{ij}$。
- 遺憾的是這封信長期未發表，影響力遲到：Cramer（1750）、Vandermonde（1772）、Laplace 等人是獨立重新發展的；直到 1850 年前後 Leibniz 手稿出版，偵探界才補記了這筆功勞。
- 行列式從此走上獨立發展之路：Cramer 法則、Laplace 展開、Cayley 的矩陣理論，乃至特徵值 $\det(A - \lambda I) = 0$，全都源自這個 1693 年寫下的交叉相減花樣。
- 東亞平行案件：關孝和 1683 年《解伏題之法》獨立發現行列式，是數學史上「多重獨立發現」的經典案例。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Gottfried Wilhelm Leibniz | 首次寫下行列式，發明指數對記號 |
| Guillaume de l'Hôpital | 收信人，微積分的早期傳播者 |
| Seki Takakazu（關孝和） | 1683 年獨立發現行列式（平行案件） |
| Étienne Bézout / Alexandre-Théophile Vandermonde | 後續重新發展行列式理論 |

- G. W. Leibniz, 致 l'Hôpital 的信（1693 年 4 月 28 日），收入 *Leibnizens mathematische Schriften*（1850 年代出版）。
- 關孝和《解伏題之法》（1683）。
- T. Muir, *The Theory of Determinants in the Historical Order of Development*（1906）：行列式史的標準考據。
