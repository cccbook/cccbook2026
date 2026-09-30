# 1972 Prolog 誕生：Colmerauer 與 Kowalski 把邏輯變成程式

## 案發現場

1970 年代初，人工智慧研究陷入第一個低潮的邊緣。LISP 雖然能操作符號，但它本質上是「函數計算」——程式設計師必須描述**怎麼算**，而不是**算什麼**。同時，數理邏輯界已累積了近百年的成果：Horn 子句、合一（unification）、歸結（resolution）證明程序。但沒有人把這些理論變成能跑在電腦上的實用語言。

兩個不同地區的人同時遇到了同一個謎題：

- 在法國馬賽，Alain Colmerauer 正研究自然語言理解，需要一種能表達文法規則並自動推導句子結構的工具。
- 在英國愛丁堡，Robert Kowalski 從事定理證明研究，提出了「演算法 = 邏輯 + 控制」的著名公式：$A = L + C$。

未解之謎是：**如果程式設計師只寫邏輯（事實與規則），讓機器自己找出控制流程（搜尋與回溯），程式設計會變成什麼樣子？**

這個問題為何重要？宣告式程式設計的承諾——「你只管說你要什麼，機器負責怎麼做」——是程式語言史上最誘人但也最難實現的夢想。Prolog 是第一個真正把它做出來的通用語言。

## 偵查過程

Colmerauer 與 Philippe Roussel 在 1972 年實作出第一個 Prolog 直譯器，Kowalski 則提供了理論基石。核心技術推導如下。

**第一步：Horn 子句作為程式。** 邏輯程式由事實（fact）與規則（rule）構成，兩者都可統一表示為 Horn 子句：

$$H \leftarrow B_1, B_2, \ldots, B_n$$

讀作「若 $B_1$ 且 $B_2$ 且 $\ldots$ 且 $B_n$ 成立，則 $H$ 成立」。當 $n = 0$ 時就是事實。例如：

```prolog
parent(tom, bob).       % 事實：tom 是 bob 的父母
parent(bob, ann).
grandparent(X, Z) :- parent(X, Y), parent(Y, Z).   % 規則
```

**第二步：合一（unification）。** 要判斷查詢 `grandparent(tom, Z)` 是否成立，系統必須讓查詢項與子句頭匹配。合一演算法在兩個項之間尋找最一般的變數代入（most general unifier, MGU）。例如合一 $grandparent(tom, Z)$ 與 $grandparent(X, Z')$：

$$\sigma = \{X \mapsto tom,\ Z' \mapsto Z\}$$

合一的核心遞迴規則是：$\theta$ 是 $f(s_1,\ldots,s_n)$ 與 $f(t_1,\ldots,t_n)$ 的合一器，當且僅當 $\theta$ 同時是所有 $s_i$ 與 $t_i$ 的合一器。

**第三步：SLD 解析與回溯。** Prolog 採用 Selective Linear Definite clause resolution：從目標堆疊中依序選取最左目標，由上而下掃描子句尋找可合一者，代入後將子句體展開為新目標。若目標堆疊清空則成功；若無子句可匹配，則**回溯**（backtrack）到最近的選擇點，嘗試下一條子句。這就是深度優先搜尋：

```
目標: grandparent(tom, Z)
  → 合一規則, 得 parent(tom, Y), parent(Y, Z)
  → parent(tom, bob) ✓
  → parent(bob, Z) ✓ → 得 Z = ann，成功！
```

關鍵靈感在於：**控制的細節（搜尋順序、回溯）全部內建在直譯器裡，使用者完全不用寫。** 程式設計師只寫「什麼是真的」。

1980 年代日本推出「第五代電腦計畫」押注 Prolog，掀起全球 AI 熱潮，雖然計畫本身未達目標，卻讓邏輯程式設計成為顯學。

## 結案報告

Prolog 的遺產：

- **宣告式範式的確立**：與函數式並列的兩大宣告式傳統之一，直接影響 SQL、Datalog、約束求解（CLP）。
- **語言系譜**：Mercury、ECLiPSe、SWI-Prolog；Haskell（[1990-Haskell.md](1990-Haskell.md)）的型別類解析、Java（[1995-Java.md](1995-Java.md)）型別系統中的型別推導演算法，都有合一的影子。
- **實務應用**：IBM 的專家系統、自然語言處理（Definite Clause Grammar）、ESLint 的規則引擎、CodeQL 程式碼查詢語言，都是 Prolog 思想的後裔。
- **教育的啟示**：Prolog 教會世人「回溯搜尋」與「模式匹配」是可組合的語言機制，而非單純的演算法技巧。

Colmerauer 於 1986 年獲得首屆 Logic Programming 獎。Prolog 證明：**邏輯不只是數學的工具，它本身就是一種程式語言。**

## 證據與工具

Prolog 示範——家族關係查詢與列表處理：

```prolog
% 事實
parent(tom, bob).
parent(bob, ann).
parent(bob, pat).

% 規則
grandparent(X, Z) :- parent(X, Y), parent(Y, Z).

% 列表遞迴
member(X, [X|_]).
member(X, [_|T]) :- member(X, T).

% ?- grandparent(tom, Z).   → Z = ann ; Z = pat
% ?- member(X, [1,2,3]).   → X = 1 ; X = 2 ; X = 3
```

用 Python 模擬合一與回溯搜尋：

```python
def unify(t1, t2, subst=None):
    subst = subst or {}
    if t1 == t2:
        return subst
    if isinstance(t1, str) and t1.isupper():       # 變數
        subst[t1] = t2; return subst
    if isinstance(t2, str) and t2.isupper():
        subst[t2] = t1; return subst
    if isinstance(t1, tuple) and isinstance(t2, tuple) and t1[0] == t2[0]:
        for a, b in zip(t1[1:], t2[1:]):
            if unify(a, b, subst) is None: return None
        return subst
    return None

def walk(term, subst):
    while isinstance(term, str) and term in subst:
        term = subst[term]
    return term

facts = [("parent","tom","bob"), ("parent","bob","ann"), ("parent","bob","pat")]

def query(pred, *args, subst=None):
    subst = subst or {}
    for f in facts:
        s = unify((pred, *args), f, dict(subst))
        if s is not None:
            yield {k: walk(v, s) for k, v in s.items()}

for s in query("parent", "tom", "Z"):
    print(s)   # {'Z': 'bob'}
```
