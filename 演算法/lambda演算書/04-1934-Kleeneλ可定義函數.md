# 1934 - Kleene 證明 λ 可定義函數涵蓋原始遞迴函數

## 案件摘要
1934 年，Church 的學生 Stephen Kleene 證明了一個關鍵事實：
所有 Gödel 原始遞迴函數都可以在 λ 演算中「定義」出來。
這意味著純粹的「函數與一條歸約規則」，居然能算出整個原始遞迴的世界 —— 可計算性的輪廓第一次浮出水面。

## 前因 -- 為什麼會有這個案子
- 1931 年 Gödel 提出**原始遞迴函數**（primitive recursive functions）作為「可機械計算」的候選數學模型，並用它編碼算術化（Gödel numbering）。
- Church 想主張更強的命題：「可有效計算 = λ 可定義」（後稱 Church 命題）。要讓這個主張有說服力，至少得先證明：Gödel 的原始遞迴函數全部都是 λ 可定義的。
- Kleene 最初對 λ 演算相當懷疑，甚至認為這套「純符號遊戲」算不出什麼東西；他決定親自檢驗 —— 結果被自己的證明說服了。

## 線索與推理 -- 數學式、程式、理論

### 1. 原始遞迴函數的定義
原始遞迴函數由以下三條規則生成：

1. **零函數**：$Z(x) = 0$
2. **後繼函數**：$S(x) = x + 1$
3. **投影函數**：$P_i^n(x_1, \dots, x_n) = x_i$
4. **複合**（composition）：若 $g_1,\dots,g_m, h$ 是原始遞迴的，則
   $$
   f(x_1,\dots,x_n) = h(g_1(\vec{x}), \dots, g_m(\vec{x}))
   $$
   也是。
5. **原始遞迴**（primitive recursion）：若 $g, h$ 是原始遞迴的，則
   $$
   f(0, \vec{x}) = g(\vec{x}), \qquad f(n+1, \vec{x}) = h(n,\ f(n,\vec{x}),\ \vec{x})
   $$

加法、乘法、階乘都是原始遞迴的：
$$
\begin{aligned}
add(0, y) &= y, & add(n+1, y) &= S(add(n, y)) \\
mult(0, y) &= 0, & mult(n+1, y) &= add(mult(n, y),\ y)
\end{aligned}
$$

### 2. Church 數字（Church numerals）：把數字變成函數
Kleene 面對的第一個難題：λ 演算裡沒有數字，怎麼算術？
答案是**編碼**：自然數 $n$ 編碼為「把函數 $f$ 應用 $n$ 次到 $x$」：

$$
\bar{n} = \lambda f.\, \lambda x.\, f^n\ x
$$

即：
$$
\bar{0} = \lambda f.\lambda x.\, x, \quad
\bar{1} = \lambda f.\lambda x.\, f\ x, \quad
\bar{2} = \lambda f.\lambda x.\, f\ (f\ x), \quad \dots
$$

**Church 數字的妙處**：$\bar{n}$ 自帶「迭代 $n$ 次」的語義 —— 數字本身就是迭代器。

### 3. 後繳函數的 λ 定義
後繼函數 $S(n) = n+1$，在 λ 演算中：

$$
SUCC = \lambda n.\, \lambda f.\, \lambda x.\, f\ (n\ f\ x)
$$

**推理過程**：$n\ f\ x$ 是「把 $f$ 應用 $n$ 次到 $x$」的結果；再外面套一層 $f$，就是應用 $n+1$ 次。

驗證：$SUCC\ \bar{1}$
$$
\begin{aligned}
SUCC\ \bar{1}
&= (\lambda n.\lambda f.\lambda x.\, f\ (n\ f\ x))\ (\lambda f.\lambda x.\, f\ x) \\
&\to_\beta \lambda f.\lambda x.\, f\ ((\lambda f.\lambda x.\, f\ x)\ f\ x) \\
&\to_\beta \lambda f.\lambda x.\, f\ (f\ x) = \bar{2} \quad\checkmark
\end{aligned}
$$

### 4. 加法的 λ 定義
有兩種等價寫法：

**法一（迭代 SUCC）**：$add(m, n)$ 就是「對 $\bar{n}$ 迭代 $m$ 次 $SUCC$」：
$$
ADD = \lambda m.\, \lambda n.\, m\ SUCC\ n
$$

**法二（直接重疊應用）**：
$$
ADD = \lambda m.\, \lambda n.\, \lambda f.\, \lambda x.\, m\ f\ (n\ f\ x)
$$

驗證：$ADD\ \bar{2}\ \bar{3}$
$$
ADD\ \bar{2}\ \bar{3}
= \lambda f.\lambda x.\ \bar{2}\ f\ (\bar{3}\ f\ x)
= \lambda f.\lambda x.\ f\ (f\ (f\ (f\ (f\ x)))) = \bar{5} \quad\checkmark
$$

### 5. 乘法與原始遞迴的一般套路
乘法：「把 $m$ 次應用『迭代 $n$ 次』這件事再做 $m$ 次」：
$$
MULT = \lambda m.\, \lambda n.\, \lambda f.\, m\ (n\ f)
$$

原始遞迴的一般模板：$f(n+1) = h(f(n))$ 在 λ 演算中就是把 $h$ 迭代 $n$ 次後從基底出發 —— 這正需要（受限的）迭代能力，而 Church 數字天生提供。

### 6. Python 驗證
```python
def church(n):                      # n ↦ λf.λx. f^n x
    return lambda f: lambda x: f(*([x] * 0)) if n == 0 else (
        (lambda g, k: g)  # placeholder, see below
    )

# 直接以遞迴建構：
def N(n):
    if n == 0:
        return lambda f: lambda x: x
    prev = N(n - 1)
    return lambda f, _prev=prev: lambda x: f(_prev(f)(x))

SUCC = lambda n: lambda f: lambda x: f(n(f)(x))
ADD  = lambda m: lambda n: m(SUCC)(n)
MULT = lambda m: lambda n: lambda f: m(n(f))

def to_int(c):                      # 解碼：套用 (λy. y+1) n 次
    return c(lambda y: y + 1)(0)

assert to_int(SUCC(N(1))) == 2
assert to_int(ADD(N(2))(N(3))) == 5
assert to_int(MULT(N(2))(N(3))) == 6
assert to_int(N(10)) == 10
print("所有原始遞迴測試通過：SUCC / ADD / MULT / N ✓")
```

## 結案 -- 後果與影響
- 1934 年 Kleene 在 Princeton 的討論班上報告此結果：**原始遞迴函數 ⊆ λ 可定義函數**，Church 命題獲得第一塊堅實證據。
- Kleene 接著證明 λ 可定義函數**恰好**等於一般遞迴函數（1936），使「可計算」有了精確刻畫 —— 直接鋪路給 1936 年 Church 的判定問題不可判定性證明。
- Church 數字成為程式語言理論的經典教材：它展示了「資料可以是函數」，影響了 Lisp、Haskell 的型別設計與函式式思維。
- 有趣的歷史插曲：Kleene 起初嫌 λ 演算「毫無用處」，最後卻成為它最忠實的推廣者之一。

## 關鍵人物與文獻
- **Stephen C. Kleene**（1909–1994）：Church 的博士生，遞迴函數論的奠基者之一。
- **Kurt Gödel**：原始遞迴函數與不完備定理的提出者。
- S. C. Kleene, *λ-definability and recursiveness*, Duke Mathematical Journal 2 (1936)。
- A. Church, *An unsolvable problem of elementary number theory*, American Journal of Mathematics 58 (1936)。
- S. C. Kleene, *Introduction to Metamathematics* (1952)：遞迴函數論的標準教科書。
