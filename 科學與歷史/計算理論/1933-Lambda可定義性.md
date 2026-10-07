# 1933 - λ 可定義性與有效可計算性

## 案件摘要
1933 年前後，Church 與 Kleene 在普林斯頓系統化 λ 可定義函數，證明它們恰好涵蓋原始遞迴函數（再加上 μ 運算則涵蓋一般遞迴函數）。「有效可計算性」這個模糊概念第一次有了精確的數學定義——為 1936 年的 Church–Turing 命題鋪路。

## 前因 -- 為什麼會有這個案子
Hilbert 的判定問題（見 `1900-Hilbert23問題.md`）要求「機械程序」，但「程序」一詞沒有嚴格定義，無法證明「不存在這樣的程序」。Gödel (1931) 已用「遞迴函數」與「原始遞迴函數」刻劃了一類可計算的函數，但他本人不認為這涵蓋了所有「有效可計算」的函數。Church 在 1920 年代末發展 λ 演算（一個以函數抽象為唯一原語的形式系統），Kleene 則負責檢驗：λ 演算到底能算出哪些函數？

## 線索與推理 -- 數學式、程式、理論

### λ 演算的三條語法規則
項（term）的語法：

$$M ::= x \mid \lambda x.\, M \mid M\, N$$

三種構造：變數 $x$、函數抽象 $\lambda x. M$、函數應用 $M\, N$。歸約規則（β 歸約）：

$$(\lambda x.\, M)\, N \to_\beta M[x := N]$$

（把 $M$ 中的自由 $x$ 代換為 $N$。）另有 α 變換（重新命名約束變數）與 η 歸約。

### Church 數字
Church 用純 λ 項編碼自然數 $n$ 為「$n$ 次應用」：

$$\ulcorner n \urcorner \equiv \lambda f.\, \lambda x.\, f^n(x)$$

例如：
- $\ulcorner 0 \urcorner = \lambda f.\, \lambda x.\, x$
- $\ulcorner 1 \urcorner = \lambda f.\, \lambda x.\, f(x)$
- $\ulcorner 2 \urcorner = \lambda f.\, \lambda x.\, f(f(x))$
- $\ulcorner 3 \urcorner = \lambda f.\, \lambda x.\, f(f(f(x)))$

### 算術運算的 λ 定義
加法：$m + n$ 就是「把 $m$ 疊在 $n$ 上」：

$$\mathrm{ADD} \equiv \lambda m.\, \lambda n.\, \lambda f.\, \lambda x.\, m\, f\, (n\, f\, x)$$

乘法：

$$\mathrm{MUL} \equiv \lambda m.\, \lambda n.\, \lambda f.\, m\, (n\, f)$$

前驅函數（predecessor，最精巧的部分）與減法：

$$\mathrm{PRED} \equiv \lambda n.\, \lambda f.\, \lambda x.\, n\, (\lambda g.\, \lambda h.\, h\, (g\, f))\, (\lambda u.\, x)\, (\lambda u.\, u)$$

布爾值與條件：
- $\mathrm{TRUE} \equiv \lambda a.\, \lambda b.\, a$，$\mathrm{FALSE} \equiv \lambda a.\, \lambda b.\, b$
- $\mathrm{IF} \equiv \lambda c.\, \lambda t.\, \lambda e.\, c\, t\, e$

布爾值本質上是「選擇器」，條件分支就是直接應用——**資料與程式碼的界線在 λ 演算中消失了**。

### Kleene 的覆蓋證明
Kleene (1936) 證明：每個**原始遞迴函數**都是 λ 可定義的。

**原始遞迴函數**的定義：
1. **基底**：零函數 $Z(x)=0$、後繼 $S(x)=x+1$、投影 $P_i^n(x_1,\dots,x_n)=x_i$
2. **合成**：$f(\vec{x}) = g(h_1(\vec{x}), \dots, h_m(\vec{x}))$
3. **原始遞迴**：
$$f(0, \vec{x}) = g(\vec{x}), \quad f(n+1, \vec{x}) = h(n, f(n, \vec{x}), \vec{x})$$

Kleene 對每條規則構造出對應的 λ 項。再加上**最小化運算**（μ 運算）：

$$\mu y.\, [f(y, \vec{x}) = 0] = \text{最小的 } y \text{ 使得 } f(y, \vec{x}) = 0$$

即可涵蓋**一般遞迴函數**（部分函數；μ 運算可能不終止，這正是「部分」的來源）。

### 程式碼：Church 數字的 Python 模擬
```python
# Church 數字：n = lambda f: lambda x: f^n(x)
def church_zero():
    return lambda f: lambda x: x

def succ(n):
    return lambda f: lambda x: f(n(f)(x))

def add(m, n):
    return lambda f: lambda x: m(f)(n(f)(x))

def mul(m, n):
    return lambda f: m(n(f))

# 布爾值：TRUE/FALSE 是選擇器
TRUE  = lambda a: lambda b: a
FALSE = lambda a: lambda b: b

def to_int(c):          # 把 Church 數字轉回 Python 整數
    return c(lambda v: v + 1)(0)

one, two, three = succ(church_zero()), succ(succ(church_zero())), succ(two := succ(succ(church_zero())))
print(to_int(add(two, three)))   # 5
print(to_int(mul(two, three)))   # 6
print(TRUE("yes")("no"))          # 'yes' —— 條件分支就是函數應用
```

### 有效可計算性的候選定義
1935–36 年間，幾個定義浮出水面並被證明**等價**：

| 定義 | 提出者 | 年份 |
|---|---|---|
| λ 可定義函數 | Church, Kleene | 1933–36 |
| 一般遞迴函數 | Gödel, Herbrand, Kleene | 1934–36 |
| Turing 機可計算函數 | Turing | 1936 |
| Post 系統 | Post | 1936 |

**偵探筆記**：這種「獨立發現卻完全吻合」的現象，正是它們捕捉到同一個客觀概念——「有效可計算」——的最強證據。這就是 **Church–Turing 命題**：

> 所有「有效可計算」的函數，恰好就是圖靈機可計算（= 遞迴 = λ 可定義）的函數。

它不是定理（無法證明，因為「有效可計算」不是形式概念），而是被經驗與數學證據支持的**命題**——相當於計算領域的牛頓定律。

## 結案 -- 後果與影響
- 1936 年 Church 用 λ 演算證明**判定問題不可判定**（Church 定理）——第一個正面使用「精確化可計算性」來證明否定性結果。
- λ 演算成為**程式語言理論**的基石：Lisp (McCarthy 1958/1960)、ML、Haskell、所有函數式語言的理論源頭；現代類型系統、閉包（closure）、匿名函數皆源自 λ。
- 「資料即程式碼」的思想直接塑造了 Lisp 與 REPL 文化。
- Church–Turing 命題成為計算理論的公理級假設，物理版本（Church–Turing–Deutsch 命題）延伸到量子計算。
- 交叉參照：λ 演算書（本書姊妹卷，含完整歸約理論與 Y 組合子）；`1936-Turing機與停機問題.md`

## 關鍵人物與文獻
- **Alonzo Church**（1903–1995）：A Set of Postulates for the Foundation of Logic (1932/33)；An Unsolvable Problem of Elementary Number Theory (1936)
- **Stephen Kleene**（1909–1994）：λ-definability and recursiveness (1936)；General recursive variables of natural numbers (1936)
- **J. Barkley Rosser**：Church–Rosser 定理（合流性，1935）
- **Alan Turing**：On Computable Numbers (1936)——證明 λ 可定義 = 圖靈可計算
- 交叉參照：`1931-Godel不完備定理.md`、`1936-Turing機與停機問題.md`
