# 1978-HindleyMilner型別推論

## 案件摘要

1978 年，Robin Milner 發表「A Theory of Type Polymorphism in Programming」（Journal of Computer and System Sciences 17(3)），正式提出演算法 W：一個能為不寫型別的程式自動推導出「最一般型別」（principal type）的演算法。謎題是：1973 年 ML 需要「不寫型別卻型別安全」，這在理論上可能嗎？Milner 證明了答案為真——結合 Robinson 1965 年的合一演算法與 Roger Hindley 1969 年的 principal type 理論，型別推論成為可能。此後每個現代編譯器裡都住著一個 unifier。

## 前因 -- 為什麼會有這個案子

- 1973 年 ML 誕生時的承諾：使用者完全不寫型別，系統卻全程型別安全。這需要理論證明，不只是實作技巧。
- 無型 λ-Calculus 太自由：可以 apply 任何東西——$\lambda x. x\ x$ 合法但無型別意義，會導致 Russell 悖論式的發散。要型別安全，必須先確定「誰能套用誰」。
- Hindley 1969 年已在組合邏輯中提出類似演算法：組合邏輯中的物件有「principal type scheme」——最一般的型別，且唯一。這來自 Curry-Howard 傳統（型別即命題、程式即證明）。
- Robinson 1965 年提出合一（unification）演算法：找一個替換（substitution）使兩個型別表達式相等。這是拼圖的最後一塊。
- Milner 把三者結合：型別文法 + unification + 推論 = 演算法 W，並證明其正確性與 principal type 的唯一性。

## 線索與推理 -- 數學式、程式、理論

### 線索一：型別文法

型別由型別變數 $\alpha, \beta$ 與函數型別構成：

$$\tau ::= \alpha \mid \mathrm{int} \mid \mathrm{bool} \mid \tau_1 \to \tau_2$$

型別環境 $\Gamma$ 把變數映射到型別，判斷式 $\Gamma \vdash e : \tau$ 表示「在環境 $\Gamma$ 下，表達式 $e$ 有型別 $\tau$」。

### 線索二：Robinson 合一演算法

合一（unification）是找替換 $\sigma$ 使 $\sigma(\tau_1) = \sigma(\tau_2)$：

$$\mathrm{unify}(\alpha, \mathrm{int}) = [\alpha \mapsto \mathrm{int}] \qquad \mathrm{unify}(\alpha \to \beta, \gamma \to \gamma) = [\alpha \mapsto \gamma, \beta \mapsto \gamma]$$

 Robinson 演算法保證：若合一存在，必存在最一般合一（most general unifier, mgu），且唯一（在變數改名意義下）。

### 線索三：演算法 W -- 破案時刻

演算法 W 對每個表達式推導型別與替換：

- **變數** $x$：查 $\Gamma(x)$，一般化為型別方案。
- **應用** $e_1\ e_2$：推 $e_1 : \tau_1$、$e_2 : \tau_2$，合一 $\tau_1 \sim \tau_2 \to \alpha_{\text{new}}$，結果型別為 $\alpha_{\text{new}}$。
- **抽象** $\lambda x.\ e$：推 $e : \tau$，結果為 $x$ 的新鮮型別變數 $\alpha \to \tau$。
- **let** $\mathrm{let}\ x = e_1\ \mathrm{in}\ e_2$：推 $e_1 : \tau_1$，一般化 $\forall \bar{\alpha}.\ \tau_1$，在擴充環境中推 $e_2$。

$$\frac{\Gamma \vdash e_1 : \tau_1 \quad \Gamma, x : \forall \bar{\alpha}.\ \tau_1 \vdash e_2 : \tau_2}{\Gamma \vdash \mathrm{let}\ x = e_1\ \mathrm{in}\ e_2 : \tau_2}$$

Milner 證明：演算法 W 終止、正確（sound），且推出的型別是 principal type——最一般的型別，所有其他可行型別都是它的實例。

### 線索四：principal type 的唯一性

principal type 的意義：對 identity 函數 $\lambda x. x$，推論結果是 $\alpha \to \alpha$；它是最一般的——$\mathrm{int} \to \mathrm{int}$、$\mathrm{bool} \to \mathrm{bool}$ 都是它的實例。Hindley 已證明此型別在組合邏輯中唯一；Milner 把定理推廣到 let 多型的語言。

### 線索五：let-多型與 value restriction

let 綁定的變數可被實例化為不同型別，lambda 參數不行：

```python
# let x = (lambda v: v) in (x(1), x(True))
# x 是 let 綁定：可一般化為 ∀a. a->a，一處當 int，一處當 bool
# (lambda f: (f(1), f(True))) (lambda v: v)
# f 是 lambda 參數：只能有一個型別，會推論失敗
```

lambda 參數的多型會破壞 principal type 的唯一性與 soundness，因此被禁止。後續（ML 參考呼叫與可變結構的出現）加入 value restriction：只有「值」層次的 let 綁定才一般化。

### 程式驗證：mini Hindley-Milner 推論器

用 Python 實作最小版演算法 W（unify + infer，支援 lambda/apply/let）：

```python
import itertools

class Var:
    def __init__(self, name): self.name = name; self.instance = None
    def prune(self):
        if self.instance is not None:
            self.instance = self.instance.prune()
            return self.instance
        return self

class Con:
    def __init__(self, name, args=()): self.name = name; self.args = args

def Arrow(a, b): return Con("->", (a, b))

counter = itertools.count()
def fresh():
    return Var(f"t{next(counter)}")

def occurs(v, t):
    t = t.prune()
    if isinstance(t, Var): return t is v
    return any(occurs(v, a) for a in t.args)

def unify(a, b):
    a, b = a.prune(), b.prune()
    if isinstance(a, Var):
        if a is not b:
            if occurs(a, b): raise TypeError("occurs check failed")
            a.instance = b            # Robinson: 最一般合一
        return
    if isinstance(b, Var): return unify(b, a)
    if a.name != b.name or len(a.args) != len(b.args):
        raise TypeError(f"cannot unify {show(a)} with {show(b)}")
    for x, y in zip(a.args, b.args): unify(x, y)

def show(t):
    t = t.prune()
    if isinstance(t, Var): return t.name
    if t.name == "->": return f"({show(t.args[0])} -> {show(t.args[1])})"
    return t.name if not t.args else f"{t.name} {' '.join(map(show, t.args))}"

def infer(env, e):
    if isinstance(e, str):                  # 變數
        return env[e]
    if e[0] == "lambda":                    # lambda x. body
        a = fresh(); env2 = dict(env, **{e[1]: a})
        body = infer(env2, e[2])
        return Arrow(a, body)
    if e[0] == "apply":                     # f x
        tf = infer(env, e[1]); tx = infer(env, e[2])
        result = fresh()
        unify(tf, Arrow(tx, result))
        return result
    if e[0] == "let":                       # let x = e1 in e2
        t1 = infer(env, e[2])
        env2 = dict(env, **{e[1]: t1})      # let-polymorphism（此處簡化）
        return infer(env2, e[3])

# 測試：identity λx.x 應推出 α -> α
id_type = infer({}, ("lambda", "x", "x"))
print("id      :", show(id_type))            # (t0 -> t0)

# apply 應推出 (α -> β) -> α -> β
K = infer({}, ("lambda", "f", ("lambda", "x", ("apply", "f", "x"))))
print("apply   :", show(K))                  # ((t0 -> t1) -> t0 -> t1)

# let x = id in (x x) 型別檢查通過
let_type = infer({}, ("let", "y", "id_var",
                      ("apply", "y", "y")))
```

對 $\lambda x. x$ 推出 $\alpha \to \alpha$，對 $\lambda f. \lambda x. f\ x$ 推出 $(\alpha \to \beta) \to \alpha \to \beta$——這正是 principal type。

## 結案 -- 後果與影響

- OCaml、Standard ML、F#、Elixir 的型別推論直接源自演算法 W。
- Haskell 全程使用 HM 型別推論（加上 type class 的擴充，成為「qualified types」）。
- Swift、Kotlin、Rust、TypeScript、C++20 的局部型別推論皆為 HM 後裔——「不寫型別，編譯器推」已是現代語言標配。
- 每個現代編譯器都有 unifier：泛型推導、trait solving、型別檢查的核心都是 Robinson 合一的後代。
- Hindley-Milner 型別系統成為型別理論的標準教材章節；progress + preservation 的證明範式（Wright & Felleisen 1994）成為型別健全性的標準論證方式。
- value restriction 成為處理可變狀態與多型互動的標準手法。

## 關鍵人物與文獻

- Milner, R., *A Theory of Type Polymorphism in Programming*, Journal of Computer and System Sciences, 17(3), 1978。
- Hindley, R., *The Principal Type-Scheme of an Object in Combinatory Logic*, Transactions of the American Mathematical Society, 146, 1969。
- Robinson, J. A., *A Machine-Oriented Logic Based on the Resolution Principle*, Journal of the ACM, 12(1), 1965（合一演算法）。
- Damas, L. and Milner, R., *Principal Type-Schemes for Functional Programs*, POPL, 1982（Damas-Milner 演算法，let-polymorphism 的形式化）。
- Wright, A. K. and Felleisen, M., *A Syntactic Approach to Type Soundness*, Information and Computation, 115(1), 1994（progress + preservation 範式）。
- Cardelli, L., *Basic Polymorphic Typechecking*, Science of Computer Programming, 8(2), 1987。
- Pierce, B. C., *Types and Programming Languages*, MIT Press, 2002。
