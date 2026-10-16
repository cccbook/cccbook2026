# 1858 — Cayley 矩陣代數

## 案件摘要
1858 年，英國律師兼數學家 Arthur Cayley 發表〈A Memoir on the Theory of Matrices〉，首次把「矩形數陣」本身當作獨立的數學物件，系統地定義了矩陣的加法、乘法、轉置、逆矩陣與恒等元素，並提出 Cayley-Hamilton 定理的雛形。從此，矩陣不再是附屬於方程組的計算工具，而成為一門新數學——矩陣代數——的主角。這是線性代數誕生史的頭號案件。

## 前因 -- 為什麼會有這個案子
- 古老的聯立線性方程組（可上溯至中國《九章算術》的方程術與高斯消去法）早就把係數排成表，但那張表只被視為「速記」，不是物件。
- 1850 年 James Joseph Sylvester 在論文中首創「matrix」一詞——意指「能從中孵化出行列式的子宮」——但他關心的仍只是行列式。
- 線性變換 $\mathbf{x} \mapsto A\mathbf{x}$ 的複合 $\mathbf{z} = B(A\mathbf{x})$ 自然對應一張「係數的係數」表；Gauss、Eisenstein 都碰過這類計算，Eisenstein 甚至在 1852 年用過矩陣乘法，卻沒有人把這套規則抽象化、公理化。
- Cayley 是勤奮的劍橋數學家（後來執業律師十四年仍發表數百篇論文），與 Sylvester 是摯友；他問了一個前人沒問的問題：**如果「數陣」本身就是一種新的「數」，它的運算律是什麼？**

## 線索與推理 -- 數學式、程式、理論

### 線索一：矩陣作為新物件與其運算
Cayley 定義 $m \times n$ 矩陣

$$A = \begin{pmatrix} a_{11} & a_{12} & \cdots \\ a_{21} & a_{22} & \cdots \\ \vdots & \vdots & \ddots \end{pmatrix}$$

並規定：加法逐元素相加 $A + B = (a_{ij} + b_{ij})$、數乘 $kA = (ka_{ij})$、轉置 $A^T = (a_{ji})$、以及滿足 $AI = IA = A$ 的單位矩陣 $I$。這些運算構成今天的矩陣環與模組結構的起點。

### 線索二：乘法規則與 $AB \neq BA$
Cayley 洞察到：矩陣乘法正是**線性變換的複合**。若先做 $A$ 再做 $B$，合成變換的係數為

$$(BA)_{ij} = \sum_{k} b_{ik} a_{kj}$$

注意順序：$BA$ 表示「先 $A$ 後 $B$」（以行向量作用於左側的慣例下）。這條規則立即可推出矩陣乘法結合律 $(AB)C = A(BC)$ 與分配律，但**交換律一般不成立**——這是人類第一次正視「不交換的乘法」（比 Hamilton 1843 年的四元數更有系統地進入了代數核心）。逆矩陣則由 $AA^{-1} = A^{-1}A = I$ 定義，且 $\det(AA^{-1}) = 1$ 暗示 $A$ 必須可逆（行列式非零）。

### 線索三：Cayley-Hamilton 定理雛形
Cayley 在論文結尾以 $2 \times 2$ 與 $3 \times 3$ 的例子驗證了一個驚人的猜想：若

$$p_A(\lambda) = \det(\lambda I - A) = \lambda^n + c_{n-1}\lambda^{n-1} + \cdots + c_0$$

是 $A$ 的特徵多項式，則**把矩陣 $A$ 自己代入多項式**，會得到零矩陣：

$$p_A(A) = A^n + c_{n-1}A^{n-1} + \cdots + c_0 I = 0$$

Cayley 說他「已對 $3\times 3$ 完成驗證，一般情形未給證明」。這個看似怪異的式子（純量 $\lambda$ 變成矩陣 $A$）背後的深意——多項式環對「矩陣的最小多項式」取商——要等到 Frobenius（1878）才徹底釐清。

### 程式碼範例：用 Python 驗證 Cayley 的矩陣代數與 Cayley-Hamilton 定理
```python
import numpy as np

A = np.array([[2.0, 1.0],
              [1.0, 3.0]])
B = np.array([[1.0, 0.0],
              [0.0, 4.0]])
I = np.eye(2)

# Cayley 乘法規則：手算 BA 逐元素
BA_manual = np.array([[sum(B[i, k] * A[k, j] for k in range(2))
                       for j in range(2)] for i in range(2)])
print("BA 手算 =", BA_manual.tolist(), "，與 numpy 一致：",
      np.allclose(BA_manual, B @ A))

# 交換律失敗的實例
print("AB - BA =\n", A @ B - B @ A)   # 非零矩陣！
print("AB == BA ?", np.allclose(A @ B, B @ A))

# Cayley-Hamilton：p_A(λ) = λ² - 5λ + 5，代入 A
tr, det = np.trace(A), np.linalg.det(A)
pA_of_A = A @ A - tr * A + det * I
print("p_A(A) =\n", pA_of_A)          # 幾乎為 0
print("Cayley-Hamilton 成立 ?", np.allclose(pA_of_A, 0))
```

輸出顯示：手算乘法與 numpy 一致；$AB - BA \neq 0$（交換律確實不成立）；而 $p_A(A) = A^2 - 5A + 5I = 0$ 精確到浮點誤差——Cayley 1858 年的猜想被程式「重審」確認。

## 結案 -- 後果與影響
- 矩陣理論正式誕生：加法、乘法、逆、轉置、單位元一次到位，矩陣成為線性代數的**標準語言**。
- Cayley-Hamilton 定理成為矩陣論的基石：可用於求逆（$A^{-1} = -\frac{1}{c_0}(A^{n-1} + \cdots + c_1 I)$）、化簡矩陣冪、定義最小多項式。
- 「不交換代數」自此進入數學主流，預示了群表示論（Frobenius 1896）與量子力學矩陣力學（1925）。
- 1880 年代起，Sylvester、Frobenius、Jordan 等人接力，把 Cayley 的骨架填上秩、特徵值、標準形等血肉。
- 今日電腦繪圖、深度學習（GPU 矩陣乘法）、量子計算，全部建基於這份 1858 年的備忘錄。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Arthur Cayley | 撰寫《A Memoir on the Theory of Matrices》，矩陣代數之父 |
| James Joseph Sylvester | 1850 年命名「matrix」，Cayley 的合作者 |
| Ferdinand Eisenstein | 1852 年曾使用矩陣乘法但未系統化 |
| Carl Friedrich Gauss | 線性變換與消去法的先驅 |

- A. Cayley, *A Memoir on the Theory of Matrices*, Phil. Trans. R. Soc. Lond. **148**, 17–37 (1858)。
- J. J. Sylvester, *Additions to the articles...*, Phil. Mag. **37**, 363–370 (1850)：matrix 一詞首見。
