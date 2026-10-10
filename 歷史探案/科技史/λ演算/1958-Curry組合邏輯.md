# 1958 - Curry 出版《Combinatory Logic》

## 案件摘要

1958 年，Haskell Curry 與 Robert Feys 出版《Combinatory Logic, Vol. I》，
把「無變數的函數邏輯」系統化為嚴謹理論。這是一場「消除變數」的
偵查行動：只用 S、K 兩個組合子，就能表達一切 λ 項——
變數是煙霧彈，函數本質上是「組合」。

## 前因 -- 為什麼會有這個案子

- 1920 年代，Moses Schönfinkel 提出組合邏輯的雛形：能否不用變數
  就寫出所有函數？他發現 **S 與 K 兩個組合子即已足夠**。
- 1928 年起，Haskell Curry 獨立 rediscover 並終身發展此理論，
  試圖以此為數學邏輯提供「更基礎」的基礎。
- λ 演算依賴變數與α-改名、捕獲衝突、替換的細節繁瑣；
  組合邏輯中「替換」消失，只有「組合」。
- 1958 年 Curry 與 Feys 出版專著第一卷，1968 年出版第二卷（與
  Feys、Craig），成為組合邏輯的權威文獻。

## 線索與推理 -- 數學式、程式、理論

### 基本組合子

組合邏輯中，項的文法：

```
C ::= S | K | I | (C C)
```

三大基本組合子的定義（λ 演算語法）：

$$
S = \lambda f.\lambda g.\lambda x.\, f\ x\ (g\ x)
$$

$$
K = \lambda a.\lambda b.\, a
$$

$$
I = \lambda x.\, x = S\ K\ K
$$

組合子邏輯的約簡規則：

$$
S\ f\ g\ x \to f\ x\ (g\ x), \qquad K\ a\ b \to a, \qquad I\ x \to x
$$

例：

$$
S\ K\ K\ x \to K\ x\ (K\ x) \to x
$$

所以 $I \equiv S\ K\ K$——恆等函數竟可由 S、K 組合而成。

Python 模擬：

```python
S = lambda f: lambda g: lambda x: f(x)(g(x))
K = lambda a: lambda b: a
I = S(K)(K)          # I x = x

assert I(42) == 42
assert K(1)(2) == 1  # K a b = a
```

### 變數消除原理（Bracket Abstraction）

**Bracket abstraction** 是把 λ 項轉為組合子的演算法。對 $\lambda x.\, M$：

$$
[x] M =
\begin{cases}
K\ M & x \notin \mathrm{FV}(M) \\
I & M = x \\
S\ ([x]\,M_1)\ ([x]\,M_2) & M = M_1\ M_2
\end{cases}
$$

例：把 $\lambda x.\ f\ x$ 轉為組合子：

$$
[x]\,(f\ x) = S\ ([x]\,f)\ ([x]\,x) = S\ (K\ f)\ I
$$

驗證：$S\ (K\ f)\ I\ x \to K\ f\ x\ (I\ x) \to f\ x$ ✓

完整轉換（Python）：

```python
def bracket_abstraction(var, m):
    # m: ('v', x) | ('lam', x, body) | ('app', a, b) | ('c', name)
    if isinstance(m, tuple) and m[0] == 'v':
        return ('c', 'I') if m[1] == var else ('app', ('c', 'K'), m)
    if isinstance(m, tuple) and m[0] == 'lam':
        inner = bracket_abstraction(m[1], m[2])
        return bracket_abstraction(var, inner)   # 逐層剝離
    if isinstance(m, tuple) and m[0] == 'app':
        return ('c', 'S') if m == (('v', var), ('v', var)) else \
               ('app', ('app', ('c', 'S'),
                        bracket_abstraction(var, m[1])),
                        bracket_abstraction(var, m[2]))
    return ('app', ('c', 'K'), m)   # 常數

# λx. f x  →  S (K f) I
f = ('v', 'f')
print(bracket_abstraction('x', ('app', f, ('v', 'x'))))
# ('app', ('app', ('c','S'), ('app', ('c','K'), ('v','f'))), ('c','I'))
```

### Curry 化（Currying）

Curry 的另一貢獻：把多參數函數轉為單參數函數鏈（Schönfinkeling）。

$$
f : A \times B \to C \quad \Longleftrightarrow \quad \mathrm{curry}(f) : A \to (B \to C)
$$

$$
\mathrm{curry}(f)(a)(b) = f(a, b), \qquad \mathrm{uncurry}(g)(a, b) = g(a)(b)
$$

Python 範例：

```python
def curry(f):
    def curried(a):
        return lambda b: f(a, b)
    return curried

def uncurry(g):
    return lambda a, b: g(a)(b)

add = lambda a, b: a + b
assert uncurry(curry(add))(3, 4) == 7
assert curry(add)(3)(4) == 7      # add 3 4，組合子邏輯的呼叫方式

# λ 演算天然就是 curry 化的：
# λa. λb. a + b  ≡  curry(add)
```

這解釋了為何函數型 $\sigma \to \tau \to \gamma$ 右結合、
應用 $f\ x\ y$ 左結合——兩者都是 curry 化的語法體現。

### Curry–Howard 對應中 Curry 的角色

- 1934 年，Curry 觀察到：組合邏輯的型別與公理模式
  $P \to P$、$P \to (Q \to P)$、$(P \to (Q \to R)) \to ((P \to Q) \to (P \to R))$
  一一對應。
- 1958 年《Combinatory Logic》中此觀察被系統化：**組合子 = 公理、
  應用 = modus ponens（肯定前件）**。
- 1969 年 William Howard 將其推廣到直覺主義邏輯全貌：

| 組合邏輯 / λ 演算 | 直覺主義邏輯 |
|---|---|
| 組合子 K（λa.λb.a） | 公理 $P \to (Q \to P)$ |
| 組合子 S（λf.λg.λx.f x (g x)） | 公理 $(P \to (Q \to R)) \to ((P \to Q) \to (P \to R))$ |
| λ 抽象（→-I 引入） | 蘊含引入 |
| 函數應用（→-E 消除） | modus ponens |
| 項 $M$ | 證明（proof） |
| 型別 $\tau$ | 命題（proposition） |

**命題即型別、證明即程式**——這是現代定理證明器（Coq、Agda、Lean）
的理論基石。

### 與 λ 演算的等價性

> **定理**：組合邏輯與 λ 演算在表達力上等價。
> 由 bracket abstraction，每個 λ 項 $M$ 可轉為組合子項 $[M]$；
> 反之每個組合子項都是 λ 項。

$$
M \to_\beta N \implies [M] \to_w [N], \qquad [M] \to_w P \implies \exists N.\ M \twoheadrightarrow_\beta N \text{ 且 } P \twoheadrightarrow_w [N]
$$

其中 $\to_w$ 是「弱約簡」（weak reduction：不在 $\lambda$ 下方約簡）。
此等價性由 Curry 與 Feys 嚴格證明（abstraction theorem）。

## 結案 -- 後果與影響

- **組合邏輯成為函數式語言編譯的實用技術**：GHC（Haskell 編譯器）
  使用 SK 组合（Spineless Tagless G-machine）作為中間表示。
- **Curry 化**進入所有函數式語言：Haskell 預設所有函數皆 curry 化。
- **Curry–Howard 對應**成為類型論與邏輯的橋樑，催生證明助理
  （Coq、Agda、Lean）與依值型別（dependent types）。
- Curry 的名字進入兩個領域：程式語言 **Haskell** 以 Haskell Curry 命名。
- 「無變數程式設計」（point-free style）成為函數式程式碼的風格典範。

## 關鍵人物與文獻

- **Haskell Curry**（1900–1982）：組合邏輯系統化者，Curry 化得名者。
- **Moses Schönfinkel**（1889–1942）：組合邏輯原始提出者（S、K）。
- **Robert Feys**：Curry 的合作者。
- Curry, H., Feys, R. (1958). *Combinatory Logic, Vol. I*.
  North-Holland Publishing Company.
- Curry, H., Hindley, J.R., Seldin, J.P. (1972). *Combinatory Logic, Vol. II*.
