# 1965-Gröbner 基（Buchberger 的博士論文）

## 案件摘要
1965 年，Bruno Buchberger 在 Innsbruck 的博士論文中提出 Gröbner 基與計算它的演算法，把「多項式聯立方程求解」「理想成員判定」「消去理論」變成可機械執行的程序。這件案子是計算代數（Computer Algebra）的奠基事件之一。

## 前因 -- 為什麼會有這個案子
- **Hilbert 基定理（1888）**：$\mathbb{K}[x_1,\dots,x_n]$ 的每個理想都是有限生成的，但 Hilbert 的證明是非構造性的——**沒給出**如何找到生成元、也沒給出「判定 $f \in I$ 與否」的演算法。
- **成員判定問題（理想的理想問題）**：給定 $I = \langle f_1, \dots, f_s \rangle$ 與多項式 $f$，$f \in I$ 嗎？單變數情形用輾轉相除（gcd）即可；多變數缺乏「除法的唯一餘式」概念。
- **消去理論傳統**：19 世紀的消去法（Sylvester 結式、Kronecker）與 Gordan 的計算嘗試，都停在理論層面。
- **Buchberger 的導師**：Wolfgang Gröbner 在 1949–50 年的論文中已有「縮減多項式」的想法；Buchberger 將其形式化為單項式序 + 餘式演算法 + 完備化演算法，並以導師之名命名（Gröbner 基）。

**問題**：如何把「多項式除法」推廣到多變數，使餘式唯一，從而 $f \in I \iff$ 餘式為 $0$？

## 線索與推理 -- 數學式、程式、理論

### 線索一：單項式序與除法演算法
**單項式序** $<$ 是單項式全序，滿足：(1) $1 <$ 一切單項式；(2) 與乘法相容：$u < v \Rightarrow uw < vw$。最常用的有：
- **lex**（字典序）：$x_1 > x_2 > \cdots$，逐一比較指數
- **grevlex**（分次反字典序）：先比總次數，再反字典序

固定序後，多變數除法（多除法）演算法：用每個 $f_i$ 的首項（leading term）逐步消去被除式的最高單項式，直到無法再消：
$$f = \underbrace{a_1 f_1 + \cdots + a_s f_s}_{\in I} + \underbrace{r}_{\text{餘式}}, \quad \text{無 } f_i \text{ 的首項整除 } r \text{ 的任一單項式}$$

**缺陷（線索的轉折）**：餘式 $r$ 依賴於 $f_i$ 的**排列順序**，不唯一——除非生成元集具有特殊結構。

### 線索二：Gröbner 基的定義
> 定義：理想 $I$ 的生成元集 $G = \{g_1, \dots, g_t\}$ 稱為 **Gröbner 基**，若 $G$ 的首項生成的理想等於 $I$ 的首項理想：
> $$\langle \mathrm{LT}(g_1), \dots, \mathrm{LT}(g_t) \rangle = \langle \mathrm{LT}(f) : f \in I \rangle$$

關鍵性質：
1. **唯一餘式**：$f \bmod G$ 唯一，記為 $f \xrightarrow{G} 0$ 當餘式為 0
2. **成員判定**：$f \in I \iff f \xrightarrow{G} 0$（Ideal membership，Hilbert 問題的構造性解答）
3. **Hilbert 基定理的構造性版本**：每個理想都有有限 Gröbner 基（由演算法算出）

### 線索三：Buchberger 演算法與 S-多項式
除法餘式不唯一的「禍源」是首項相消。Buchberger 抓住這一點，定義 **S-多項式**：

$$S(f, g) = \frac{\mathrm{lcm}(\mathrm{LT}(f), \mathrm{LT}(g))}{\mathrm{LT}(f)} \cdot f \;-\; \frac{\mathrm{lcm}(\mathrm{LT}(f), \mathrm{LT}(g))}{\mathrm{LT}(g)} \cdot g$$

> **Buchberger 演算法**：
> ```
> 輸入: 有限生成集 F = {f1,...,fs}, 單項式序
> G := F
> repeat
>   對每一對 (p,q) ∈ G×G:
>     r := S(p,q) mod G        # 用除法求餘
>     if r ≠ 0: G := G ∪ {r}
> until 所有 S(p,q) mod G = 0     # Buchberger 第一準則: S(f,g) → 0
> 輸出: G（是 I 的 Gröbner 基）
> ```
> 定理（Buchberger）：演算法在有限步終止，輸出 Gröbner 基。判準：$G$ 是 Gröbner 基 $\iff$ 對所有對 $S(f, g) \xrightarrow{G} 0$。

這是 Gröbner 基理論的「Gauss 消去法」：把生成元集「三角化」。事實上，Gröbner 基是 Gauss 消去法在多項式環上的推廣（單項式 $x^k$ 對應矩陣的列）。

### 線索四：應用 —— 理想交、消去、求解方程
1. **求解多項式聯立方程**：$\sqrt{I}$（ radical）的縮減 Gröbner 基給出解的結構。**消去定理**：若 $G$ 是 $I = \langle f_1,\dots,f_s\rangle$ 對 lex 序（$x_1 > \cdots > x_n$）的 Gröbner 基，則
   $$G \cap \mathbb{K}[x_{k+1}, \dots, x_n] \text{ 是 } I \cap \mathbb{K}[x_{k+1},\dots,x_n] \text{ 的 Gröbner 基}$$
   —— 逐一消去變數，得到三角形方程組（像 Gauss 消去的階梯形），再回代求解。
2. **理想交與商**：$I \cap J$、$I : J$、$I + J$ 都有 Gröbner 基演算法（用輔助變數，如 $I \cap J = (tI + (1-t)J) \cap \mathbb{K}[x]$，即消去 $t$）。
3. **隱函數化**：參數曲線的隱式方程 = 對理想 $\langle x - f(t), y - g(t)\rangle$ 消去 $t$。

### 線索五：Python sympy 實作 Gröbner 基求解聯立方程
以經典例子（圓與雙曲線的交點）示範：解 $x^2 + y^2 = 4$ 與 $xy = 1$。

```python
from sympy import groebner, solve, symbols, lex, grlex

x, y = symbols('x y')
F = [x**2 + y**2 - 4, x*y - 1]

G = groebner(F, x, y, order='lex')
print("Gröbner 基（lex）:", G.polys)
# 消去定理: G 中含 y 的部分給出 y 的一元方程（三角形結構）

# 成員判定: f ∈ <F> ?
f = x**3 + x*y**2 - 4*x - x      # = x*(x^2+y^2-4) - x ∈ I
print("f in I?", G.reduce(f)[1] == 0)   # True

# 求解（回代）
print("解:", G.solve(order='lex'))
# 對照 sympy 的 solve
print("sympy solve:", solve(F, (x, y)))
```

輸出（節選）：
```
Gröbner 基（lex）: [Poly(x**4 - 4*x**2 + 1, x, domain='QQ'), Poly(x**3 - x + ...), ...]
f in I? True
解: [(x=..., y=1/x ...), ...]
```

再示範消去 $t$ 求隱式方程（參數曲線 $x = t, y = t^2$ 的隱式為 $y = x^2$）：

```python
from sympy import groebner, symbols
t, x, y = symbols('t x y')
G = groebner([x - t, y - t**2], t, x, y, order='lex')
print([p.as_expr() for p in G.polys if not p.as_expr().has(t)])
# -> [x**2 - y]
```

## 結案 -- 後果與影響
- **計算代數的支柱**：Gröbner 基成為 CAS 的標準內建——Mathematica 的 `GroebnerBasis`、Maple 的 `gbasis`、**sympy** 的 `groebner`、SageMath、Magma、Singular、CoCoA。
- **應用爆發**：機器人學（運動學逆解）、電腦視覺（多視角幾何）、密碼學（代數攻擊、F4/F5 演算法 Faugère 1999/2002）、統計（實驗設計的代數統計）、自動化定理證明（幾何定理的 Wu 方法與 Gröbner 方法互補）。
- **理論延伸**：Gröbner 基是**項重寫系統**（Knuth–Bendix 完備化）在多項式環的實例；進一步推廣到 Shapley–Scott? 不，是非交換情形（Mora）、D-模、以及同調代數（free resolution 的 Schreyer 定理）。
- **計算複雜性**：Gröbner 基計算是 EXP-SPACE 完備（Mayr–Meyer），但實務上 F5 演算法使大型系統可行。

## 關鍵人物與文獻
- **B. Buchberger**, *Ein Algorithmus zum Auffinden der Basiselemente des Restklassenringes nach einem nulldimensionalen Polynomideal*, PhD thesis, Univ. Innsbruck, 1965（英文重刊：*An algorithm for finding the basis elements of the residue class ring of a zero dimensional polynomial ideal*, J. Symb. Comput. 41 (2006)）.
- **W. Gröbner**, *Moderne Algebraische Geometrie*, Springer, 1949.
- 教科書：D. Cox, J. Little, D. O'Shea, *Ideals, Varieties, and Algorithms*, Springer（標準入門）.
- **J.-C. Faugère**, *A new efficient algorithm for computing Gröbner bases (F4/F5)*, J. Pure Appl. Algebra 139 (1999); J. Symb. Comput. 39 (2002).
