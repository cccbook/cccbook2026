# 1772 — Vandermonde 行列式

## 案件摘要
1772 年，法國數學家 Alexandre-Théophile Vandermonde 向巴黎科學院提交論文〈Mémoire sur l'élimination〉（關於消去法），首次把行列式當成**獨立的研究對象**——不再是解聯立方程的副產品，而是一個有自身規則、自身結構的代數物件。論文中最著名的成果，是以兩兩之差的乘積表出的**Vandermonde 行列式**：
$$\prod_{1 \le i < j \le n}(x_j - x_i)$$
本案追查：為什麼這篇論文被視為行列式理論「獨立化」的起點？以及插值問題如何逼出這個美麗的公式？

## 前因 -- 為什麼會有這個案子
- **Cramer 的遺產**：1750 年 Cramer 法則讓行列式成為解方程的工具，但行列式始終是「方程組的附屬品」——每次出現都是為了解 $A\mathbf{x} = \mathbf{b}$，沒人問「行列式本身有什麼性質」。
- **插值問題的召喚**：天文觀測與航海表的計算需要「過已知點畫一條多項式曲線」——給定 $n$ 個點 $(x_1, y_1), \dots, (x_n, y_n)$，求 $n-1$ 次多項式 $p(x)$。設 $p(x) = a_0 + a_1x + \cdots + a_{n-1}x^{n-1}$，代入 $n$ 個點得到一組以係數 $a_k$ 為未知數的聯立方程，係數矩陣正是 Vandermonde 矩陣。插值問題是本案的案發現場。
- **對稱性思考的萌芽**：Vandermonde 注意到行列式在「交換未知數」時有固定的行為（變號或不變），並意識到「每一項都取自不同行不同列」是行列式的本質結構——這種把對稱性當研究對象的思考，預示了後來的置換群與 Galois 理論。
- 有趣的是，現代所稱「Vandermonde 行列式」的完整公式，Vandermonde 本人只處理了特殊情形；一般形式由後人（如 A. N. Kronecker 時代之前的文獻）補全——這是「以人名命名但非其人完成」的另一個經典案例。

## 線索與推理 -- 數學式、程式、理論

### 線索一：Vandermonde 矩陣從插值問題中現形
過 $n$ 個點求多項式：代入 $p(x_i) = y_i$，得到
$$\begin{pmatrix} 1 & x_1 & x_1^2 & \cdots & x_1^{n-1}\\ 1 & x_2 & x_2^2 & \cdots & x_2^{n-1}\\ \vdots & & & & \vdots \\ 1 & x_n & x_n^2 & \cdots & x_n^{n-1} \end{pmatrix} \begin{pmatrix} a_0 \\ a_1 \\ \vdots \\ a_{n-1} \end{pmatrix} = \begin{pmatrix} y_1 \\ y_2 \\ \vdots \\ y_n \end{pmatrix}$$
係數矩陣的第 $(i, k)$ 元是 $x_i^{k-1}$——每行是同一個數的各次冪。這就是 **Vandermonde 矩陣** $V$。

### 線索二：行列式公式——兩兩之差的乘積
$V$ 的行列式有封閉公式：
$$\det V = \prod_{1 \le i < j \le n}(x_j - x_i) = (x_2 - x_1)(x_3 - x_1)\cdots(x_n - x_{n-1})$$
三元驗證：
$$\begin{vmatrix}1 & x_1 & x_1^2\\ 1 & x_2 & x_2^2\\ 1 & x_3 & x_3^2\end{vmatrix} = (x_2-x_1)(x_3-x_1)(x_3-x_2)$$
證明的關鍵技巧（Vandermonde 的思路的現代版本）：從最後一行起，用「第 $k$ 行減去第 $k-1$ 行的 $x_1$ 倍」逐行相減，把第一行變成 $(1, 0, 0, \dots, 0)$；按第一行展開後，再對剩下的矩陣重複同樣操作——遞迴地提取因子 $(x_j - x_i)$。歸納到底，得到 $n(n-1)/2$ 個兩兩之差的乘積。

### 線索三：這個公式立刻回答了插值問題
$\det V = \prod_{i<j}(x_j - x_i) \neq 0$ 若且唯若所有 $x_i$ 互不相同。於是：
- 給定 $n$ 個**橫坐標互異**的點，過它們的 $n-1$ 次插值多項式**存在且唯一**——這正是多項式插值唯一性定理的代數證明；
- 若有兩個 $x_i$ 相同，$\det V = 0$，插值問題退化。

一個公式，把「過 $n$ 點的多項式何時唯一」這個幾何直覺變成了代數必然。

### 線索四：行列式的獨立化與對稱性
Vandermonde 的論文與前人的根本差異：他研究的不是「用行列式解方程」，而是**行列式本身的運算規則**——
- 交換兩行（或兩列），行列式變號；
- 某行乘常數，行列式乘同一常數；
- 每項取自不同行不同列的結構性描述。

他把「未知數互換時行列式的行為」系統化，這正是**置換的奇偶性**首次作為數學對象登場——交錯群 $A_n$ 的思想在此萌芽。行列式從此不再是方程組的影子，而是有自己姓名的研究對象。

### 線索五：與現代理論的深層對照
Vandermonde 行列式在現代數學中有四個關鍵出場點：
- **DF 可逆性**：取 $x_i = \omega^{i-1}$（$n$ 次單位根）時，$\det V = \prod_{i<j}(\omega^{j-1} - \omega^{i-1}) \neq 0$，保證離散 Fourier 變換矩陣可逆——FFT 的數學基礎；
- **特徵值理論**：對可對角化矩陣，特徵向量矩陣正是一個 Vandermonde 型矩陣；$\prod_{i<j}(\lambda_j - \lambda_i)$ 作為特徵值的判別式出現在矩陣函數與隨機矩陣理論中；
- **隨機矩陣**：GUE（Gaussian Unitary Ensemble）特徵值的聯合密度正比於 $\prod_{i<j}|\lambda_j - \lambda_i|^2 e^{-\sum\lambda_i^2}$——「兩兩互斥」的統計行為直接來自這個公式；
- **插值災害**：等距節點上高次插值因 $\det V$ 的性質而病態（Runge 現象），促使 Chebyshev 節點的選擇。

一篇 1772 年的論文，在計算機時代的 FFT、數值分析、隨機矩陣三個領域都留下了指紋。

### 程式碼範例：Vandermonde 行列式數值驗證
```python
import numpy as np
from itertools import combinations

def vandermonde_det(x):
    x = np.array(x, float)
    V = np.vander(x, increasing=True)          # 第 (i,k) 元 = x_i^k
    return V, np.linalg.det(V)

def product_formula(x):
    x = np.array(x, float)
    return np.prod([x[j] - x[i] for i, j in combinations(range(len(x)), 2)])

for xs in ([1, 2, 3], [2, 5, 7, 11], [1.5, -2, 4, 0.3, 6]):
    V, d = vandermonde_det(xs)
    print(f"x={xs}: det(V)={d:.4f}  兩兩差乘積={product_formula(xs):.4f}")

# 插值唯一性：橫坐標互異 → 可逆；重複 → 奇異
V3, d3 = vandermonde_det([1, 2, 3])
print("互異點 det =", d3, "→ 插值多項式唯一")
_, d_dup = vandermonde_det([1, 2, 2])
print("重複點 det =", d_dup, "→ 插值退化")
```

數值輸出顯示 $\det V$ 與兩兩之差乘積 $\prod_{i<j}(x_j - x_i)$ 在各種樣本上完全一致；重複橫坐標使行列式歸零，直接驗證插值唯一性定理。

## 結案 -- 後果與影響
- 行列式理論**獨立化**：Vandermonde 1772 年論文首次把行列式當成獨立研究對象，系統整理其運算規則，是行列式作為數學分支的起點。
- **Vandermonde 行列式**成為線性代數的經典公式：插值唯一性、離散 Fourier 變換的可逆性（$x_i$ 取單位根時的特例）、有限元與譜方法中的基變換，都以它為核心。
- 置換奇偶性的首次登場，為置換群、交錯群、乃至 Galois 理論鋪路——對稱性從此成為代數的核心語言。
- 插值問題的代數基礎確立：Lagrange（1778 年前後）與 Newton 的插值公式，其唯一性的最終裁判正是 $\det V \neq 0$。
- 平行案件：Laplace 同期（1772 年）也發表了行列式展開（Laplace 展開），兩人共同把行列式理論推向獨立。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Alexandre-Théophile Vandermonde | 1772 年論文，行列式獨立化、對稱性思考 |
| Gabriel Cramer | 1750 年法則，行列式工具化的前驅 |
| Pierre-Simon Laplace | 1772 年展開定理（平行案件） |
| Joseph-Louis Lagrange | 插值公式，其唯一性由 Vandermonde 行列式保證 |

- A.-T. Vandermonde, *Mémoire sur l'élimination*, Hist. Acad. Roy. Sci. Paris (1772)。
- T. Muir, *The Theory of Determinants in the Historical Order of Development*（1906）：考據指出 Vandermonde 僅完成特殊情形。
- C. D. Olds, *Continued Fractions* 及多項式插值文獻中對 Vandermonde 行列式的標準處理。
