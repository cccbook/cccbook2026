# 1850 — Sylvester 矩陣命名

## 案件摘要
1850 年，James Joseph Sylvester 在《Philosophical Magazine》論文〈Additions to the Articles, "On a New Class of Theorems"...〉中，首次創造 "matrix"（矩陣）一詞。他把矩陣定義為「由許多排成方形陣列的項所組成的數學物件，從中可以生出各種行列式」——用他自己的話說，矩陣是「生出 determinants 的子宮」（womb）。在此之前，陣列只是行列式的臨時道具；從此，它有了自己的名字，並在八年後由 Cayley 發展成完整的矩陣代數。

## 前因 -- 為什麼會有這個案子
- 1812–1841 年 Cauchy、Jacobi 把行列式理論系統化：定義、乘法規則、函數行列式——但行列式始終是「一個數」，排它的方陣只是書寫工具，沒有人研究方陣本身的運算。
- 1840 年代 Sylvester 與 Cayley 在倫敦展開長期合作（Cayley 是劍橋畢業的律師兼數學家，Sylvester 比他年長 14 歲）。兩人共同發展不變量理論（invariant theory），研究多項式在座標變換下的不變性質。
- 不變量理論的核心工具是**消去法**：兩個多項式何時有公根？Sylvester 1840 年提出 **Sylvester 消去法（dialytic method）**，用一個特殊陣列的行列式判斷公根存在性——這個陣列的行列式就是**結式（resultant）**。
- 案件核心疑問：這些不斷出現的「方形陣列」究竟是什麼？它們只是行列式的包裝紙，還是值得獨立偵辦的嫌疑人？

## 線索與推理 -- 數學式、程式、理論

### 線索一：matrix 的誕生
1850 年論文中，Sylvester 寫道（意譯）：「我們必須定義一個由若干項排成的矩形陣列……我把這樣的矩形陣列稱為 **matrix**，因為從這個母體中可以生出各種不同的行列式系統，就像是從共同子宮生出的一批子女。」

具體地，一個 $(m+1)\times(n+1)$ 的矩陣可以刪去某些行與列，生出許多不同階的子行列式（ minors）。Sylvester 的視角是：矩陣是**生成行列式的母體**，行列式才是主角。他沒有想到——這個「配角」在八年後會反客為主。

### 線索二：Sylvester 消去法與結式
1840 年的消去法：給定兩多項式

$$f(x) = a_0 x^m + a_1 x^{m-1} + \cdots + a_m, \qquad g(x) = b_0 x^n + b_1 x^{n-1} + \cdots + b_n$$

把它們分別乘上 $1, x, \dots, x^{n-1}$ 與 $1, x, \dots, x^{m-1}$，得到 $m+n$ 個方程，其係數排成 $(m+n)\times(m+n)$ 的 **Sylvester 矩陣**。定義**結式**：

$$\operatorname{Res}(f, g) = \det(\operatorname{Syl}(f, g))$$

核心定理：$\operatorname{Res}(f,g) = 0 \Leftrightarrow f$ 與 $g$ 有公根（在 $\mathbb{C}$ 上）。消去法像指紋比對：把兩個嫌疑人的所有線索排成陣列，若行列式為零，表示指紋重疊——公根存在。結式選一個更簡單的例子：$\operatorname{Res}(x^2-2, x-1) = (1)^2-2 = -1 \neq 0$，無公根；$\operatorname{Res}(x^2-1, x-1) = 0$，公根 $x=1$。

### 線索三：判別式（discriminant）與不變量
Sylvester 進一步定義**判別式**：多項式與其導數的結式（帶符號正規化）：

$$\Delta = (-1)^{\frac{m(m-1)}{2}} \frac{1}{a_0}\operatorname{Res}(f, f')$$

判別式為零 $\Leftrightarrow$ $f$ 有重根。例如二次式 $ax^2+bx+c$ 的判別式 $b^2-4ac$ 正是這個定義的特例。判別式是**座標變換下的不變量**（在適當的權重意義下），這正是不變量理論的起點：Sylvester 創造 "invariant" 一詞（1851），Cayley 發展不變量的形式理論。1851 年 Sylvester 還創造 "discriminant" 一詞。矩陣、結式、判別式、不變量——這批「同門子女」全部出自 1840–1851 年的倫敦偵探社。

### 程式碼範例：Sylvester 結式與判別式計算
```python
import numpy as np
from itertools import product

def sylvester_matrix(f, g):
    """f 次數 m、g 次數 n 的 Sylvester 矩陣（(m+n)x(m+n)）"""
    m, n = len(f)-1, len(g)-1
    S = np.zeros((m+n, m+n))
    for k in range(n):                      # f 乘 1, x, ..., x^{n-1}
        for i, a in enumerate(f):
            S[k, k + (m-i)] = a
    for k in range(m):                      # g 乘 1, x, ..., x^{m-1}
        for i, b in enumerate(g):
            S[n+k, k + (n-i)] = b
    return S

def resultant(f, g):
    return np.linalg.det(sylvester_matrix(f, g))

def discriminant(f):
    m = len(f)-1                            # f = a0 x^m + ... + am（降冪）
    a0 = f[0]
    fp = [f[i]*(m-i) for i in range(m)]     # 導數（降冪）
    if len(fp) == 0 or all(c == 0 for c in fp):
        return 0.0
    return (-1)**(m*(m-1)//2) / a0 * resultant(f, fp)

# 線索一：二次判別式 b²-4ac 特例驗證
f1 = [1, 0, -2]        # x² - 2，判別式 = 0² - 4·1·(-2) = 8
f2 = [1, -2, 1]        # x² - 2x + 1 = (x-1)²，判別式 = 0
f3 = [1, -1, -6]       # x² - x - 6 = (x-3)(x+2)，判別式 = 25
for name, f in [("x²-2", f1), ("(x-1)²", f2), ("(x-3)(x+2)", f3)]:
    print(f"disc({name}) = {discriminant(f):.4f}")

# 線索二：結式與公根
g = [1, -1]            # x - 1
h = [1, 0, -1]         # x² - 1（有公根 x=1）
print("Res(x-1, x²-1)  =", np.round(resultant(g, h), 6), " <- 0，公根存在")
print("Res(x-1, x²-2)  =", np.round(resultant(g, f1), 6), " <- 非 0，無公根")

# 線索三：數值掃描驗證 Res 隨參數連續變化、過零點即重根
f3p = [1, -1, -6 + 2.25]   # (x-1.5)²+... 檢查重根附近
print("disc((x-1.5)²之系數) =", np.round(discriminant([1, -3, 2.25]), 6))

# 用數值求根交叉驗證
roots = np.roots(f3)
print("x²-x-6 的根 =", roots, " 判別式 > 0 ↔ 兩相異實根 ✓")
```

輸出確認：$\operatorname{disc}(x^2-2)=8$、$\operatorname{disc}((x-1)^2)=0$、$\operatorname{Res}(x-1,x^2-1)=0$（有公根）、$\operatorname{Res}(x-1,x^2-2)=-1$（無公根）——Sylvester 的偵查儀完全可靠。

## 結案 -- 後果與影響
- 1858 年 Cayley 發表〈A Memoir on the Theory of Matrices〉，首次把矩陣當成獨立代數物件：定義矩陣加法、純量乘法、乘法 $AB$（注意一般不可交換）、零矩陣與單位矩陣。矩陣從「生出行列式的子宮」反客為主，成為主角。
- Cayley 觀察到 Cayley–Hamilton 定理的跡象（一般證明由 Frobenius 1878 補全）：矩陣滿足自己的特徵多項式。
- 不變量理論在 1860–1890 年代成為數學主戰場（Cayley、Sylvester、Gordan、Hilbert；Hilbert 1893 年用基底定理終結經典不變量理論）。
- 結式與判別式至今是計算代數幾何、符號計算（Gröbner 基底的先聲）的標準工具。
- 影響至今：量子力學的 Heisenberg 矩陣（1925）用的正是 Cayley 1858 年的矩陣乘法——Sylvester 為兇器命的名，成就了物理學最深的革命之一。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| James Joseph Sylvester | 創造 matrix、invariant、discriminant 等術語 |
| Arthur Cayley | 1858 矩陣代數、Sylvester 的長期合作者 |
| Augustin-Louis Cauchy / Carl Jacobi | 行列式理論的奠基者 |
| David Hilbert | 1893 終結經典不變量理論 |

- J. J. Sylvester, *Additions to the Articles, "On a New Class of Theorems", and on Pascal's Theorem*, Phil. Mag. **37**, 363–370 (1850)：matrix 一詞首次出現。
- J. J. Sylvester, *On a remarkable modification of Cauchy's theorem...*, Phil. Mag. (1851)：discriminant 與 invariant 術語。
- A. Cayley, *A Memoir on the Theory of Matrices*, Phil. Trans. R. Soc. **148**, 17–37 (1858)。
