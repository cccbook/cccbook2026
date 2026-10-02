# 1750 — Cramer 法則

## 案件摘要
1750 年，瑞士日內瓦數學家 Gabriel Cramer 出版《線性代數分析引論》（*Introduction à l'analyse des lignes courbes algébriques*），其中附錄首次以出版品形式給出：$n$ 個未知數、$n$ 個聯立一次方程組的解可用兩個行列式之比表出——
$$x_i = \frac{\det(A_i)}{\det(A)}$$
這就是後世所稱的 **Cramer 法則**。本案追查：這個公式為何誕生於一本「曲線分析」的書附錄裡？以及為什麼它效率不高、卻依然成為線性代數的經典？

## 前因 -- 為什麼會有這個案子
- **Leibniz 的未發明線索**：Leibniz 1693 年已在信中寫下二階行列式與 resultant 的想法，但手稿未發表、被遺忘。Cramer 並不知道這些信。
- **Maclaurin 的未發表工作**：蘇格蘭數學人 Colin Maclaurin 在 1748 年去世後出版的《代數論》（*Treatise of Algebra*，附錄）中，已對二元、三元、四元聯立方程給出用係數表達的解——但用的是文字冗長的消元描述，且未曾推廣到一般 $n$。Cramer 在書中還引用並致謝了 Maclaurin。史料考據（Muir）指出：二階、三元的規則 Maclaurin 更早，但 **$n$ 個未知數的一般處理與標準記號屬於 Cramer**。
- **Cramer 的實際動機**：他寫這本書是為了研究代數曲線——決定一條曲線需要多少個點？確定圓錐曲線需要五個點，對應一組五元聯立方程。曲線問題源源不絕地生出高階聯立方程組，逼出一個一般解法。
- **記號困境**：之前的數學家用「第一個未知數、第二個未知數」這樣的文字敘述，$n$ 一大就寫不下去。Cramer 採用了他朋友 Johann Bernoulli 的雙下標記號 $a_{ij}$，使一般公式的書寫成為可能。

## 線索與推理 -- 數學式、程式、理論

### 線索一：Cramer 法則的推導
對 $n$ 個方程 $A\mathbf{x} = \mathbf{b}$，$\det A \neq 0$。以二元情形為樣本：
$$\begin{cases}a_1x + b_1y = c_1\\a_2x + b_2y = c_2\end{cases}$$
消去 $y$ 得 $x = \dfrac{c_1b_2 - c_2b_1}{a_1b_2 - a_2b_1}$。分母正是 $\det A$；分子是把常數列 $c$ 換掉 $A$ 的第一行後的行列式——
$$x = \frac{\begin{vmatrix}c_1 & b_1\\ c_2 & b_2\end{vmatrix}}{\begin{vmatrix}a_1 & b_1\\ a_2 & b_2\end{vmatrix}}, \qquad y = \frac{\begin{vmatrix}a_1 & c_1\\ a_2 & c_2\end{vmatrix}}{\begin{vmatrix}a_1 & b_1\\ a_2 & b_2\end{vmatrix}}$$
一般 $n$：把 $\mathbf{b}$ 替換 $A$ 的第 $i$ 行得到 $A_i$，則 $x_i = \det(A_i)/\det(A)$。Cramer 的證明是對 $n$ 做歸納：逐次消去一個未知數，展示公式如何保持形狀。

### 線索二：為什麼公式會成立？—— Laplace 展開的視角
用現代語言可給出優雅的一行證明：對 $\det(A_i)$ 沿第 $i$ 行（即 $\mathbf{b}$ 所在的那行）展開，得
$$\det(A_i) = \sum_{k=1}^n b_k\, C_{ki}$$
其中 $C_{ki}$ 是 $A$ 的 $(k,i)$ 餘因子（cofactor）。代回 Cramer 法則：
$$\sum_{i=1}^n a_{ji}\frac{\det(A_i)}{\det A} = \frac{1}{\det A}\sum_{k=1}^n b_k \underbrace{\sum_{i=1}^n a_{ji}C_{ki}}_{=\ \det A\,\delta_{jk}} = b_j$$
（餘因子的正交性：$\sum_i a_{ji}C_{ki} = \det A\,\delta_{jk}$。）公式成立的全部秘密藏在**餘因子的正交性**裡。

### 線索三：效率的伏筆——法則很美，但很慢
Cramer 法則需要計算 $n+1$ 個 $n$ 階行列式，而每個行列式按定義有 $n!$ 項。直接展開的計算量是
$$O\big((n+1)\cdot n!\big)$$
——當 $n = 20$ 時已是天文數字（$20! \approx 2.4\times10^{18}$ 項）。相比之下，Gaussian elimination 只要 $O(n^3)$。十九世紀的數值分析學家（後來的 Bunch–Hopcroft 複雜度分析）正式定案：**Cramer 法則是理論上的優雅、計算上的災難**。這個效率問題的伏筆，要到 Gauss 消去法成熟後才被清算。

### 線索四：與九章算術的對照
《九章算術》的「損益」消去法（比 Cramer 早近兩千年）回答的是「如何逐步算出解」；Cramer 法則回答的是「解的封閉公式是什麼」。兩者是同一個問題的兩種答案：一條是演算法路線（逐步消元），一條是公式路線（行列式之比）。Cramer 的雙下標記號 $a_{ij}$ 也與 Leibniz 的「指數對」記號異曲同工——記號的成熟，是一般理論誕生的前提。

### 程式碼範例：Cramer 法則求解對照
```python
import numpy as np
import time

def cramer(A, b):
    A = np.array(A, float); b = np.array(b, float)
    d = np.linalg.det(A)                       # det(A)
    xs = []
    for i in range(len(b)):
        Ai = A.copy(); Ai[:, i] = b            # 換掉第 i 行
        xs.append(np.linalg.det(Ai) / d)       # det(A_i)/det(A)
    return np.array(xs)

# 九章算術第一題（向 Cramer 的方法致意）
A = [[3, 2, 1], [2, 3, 1], [1, 2, 3]]
b = [39, 34, 26]
x = cramer(A, b)
print("Cramer 法則解：", x)                     # [9.25, 4.25, 2.75] = 37/4, 17/4, 11/4
print("numpy 對照   ：", np.linalg.solve(np.array(A, float), b))

# 效率對照：n 增大時 Cramer（用 numpy det）與消去法的時間
for n in [100, 300, 600]:
    M = np.random.rand(n, n); v = np.random.rand(n)
    t0 = time.time(); cramer(M, v); t1 = time.time()
    np.linalg.solve(M, v); t2 = time.time()
    print(f"n={n}: Cramer 式 {t1-t0:.3f}s vs 消去法 {t2-t1:.4f}s")
```

輸出顯示：Cramer 法則與消去法給出相同解（$37/4, 17/4, 11/4$），但 $n$ 增大時 Cramer 式明顯變慢——$O(n^3)$ 對 $O(n!)$ 的差距在數值上現形。

## 結案 -- 後果與影響
- Cramer 法則是**第一個以出版品形式給出的 $n$ 元聯立方程一般解公式**，使行列式正式成為線性代數的核心工具。
- 雙下標記號 $a_{ij}$（借自 Johann Bernoulli）經 Cramer 的使用而廣泛傳播，成為今日矩陣記號的直接源頭之一。
- 「解的可解性由 $\det A$ 判定」的思想確立：$\det A \neq 0$ 有唯一解——這是後來「非奇異矩陣」理論的前身。
- **效率問題的伏筆**就此埋下：法則優雅但計算量 $O(n!)$，促成了對「更快解法」的長期追尋，最終由 Gauss 消去法（$O(n^3)$）在數值計算上勝出。
- 附帶影響：代數曲線研究中「確定曲線所需點數 ↔ 聯立方程階數」的對應，成為射影幾何中「五點定圓錐曲線」等結果的代數基礎。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Gabriel Cramer | 1750 年發表 Cramer 法則與一般記號 |
| Colin Maclaurin | 1748 年去世後出版《代數論》，小規模規則更早 |
| Gottfried Wilhelm Leibniz | 1693 年未發表的先行者 |
| Johann Bernoulli | 雙下標記號的來源（Cramer 引用） |

- G. Cramer, *Introduction à l'analyse des lignes courbes algébriques*, Genève (1750)，附錄。
- C. Maclaurin, *A Treatise of Algebra* (1748)。
- T. Muir, *The Theory of Determinants in the Historical Order of Development*（1906）：關於 Cramer 與 Maclaurin 優先權的考據。
