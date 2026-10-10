# 1969-Scott域理論與指稱語義

## 案件摘要

1969 年，邏輯學家 Dana Scott 在牛津與程式語言理論家 Christopher Strachey 展開一段改寫歷史的合作：為程式語言建立真正的「數學語義」。案件的核心謎題是：遞迴程式 `rec f. f` 的語義到底是什麼？一個函數的定義裡含有它自己，這在數學上幾乎是悖論。Scott 用「域理論」（domain theory）與最小不動點定理破解了此案，催生了指稱語義（denotational semantics），成為此後所有程式語言形式語義學的基石。

## 前因 -- 為什麼會有這個案子

- Scott 在 1960 年代初曾「證明」單純型（untyped）λ-Calculus 的實在（set-theoretic）模型不存在：如果函數只是集合論的函數，則 $D \cong [D \to D]$ 不可能對非平凡集合成立，因為集合論中 $|[D\to D]| < |D^{[D]}|$ 的基數論證會爆炸。這個「模型不完備」結果讓他一度認為 λ-Calculus 沒有像樣的數學模型。
- Strachey 的立場不同：他是實務派，想給 ALGOL、ISWIM 這類真實程式語言一個數學語義。當時主流的操作性語義（operational semantics）只描述「機器怎麼跑」，不回答「程式到底是什麼」。
- 謎題浮現：遞迴定義 `rec f. fun x. if x = 0 then 1 else x * f(x-1)` 中，`f` 出現在自己的定義裡。若 $\llbracket f \rrbracket$ 是某個數學物件，它必須滿足一個自指方程。
- 兩人在 Oxford 遇上：Scott 的邏輯加上 Strachey 的實務，正好是破案的組合。

## 線索與推理 -- 數學式、程式、理論

### 線索一：域（Domain）與 ⊥

Scott 的第一個洞見：不要用「全函數集合」，改用帶偏序的完備集（CPO, complete partial order）。在域 $D$ 上定義偏序 $\sqsubseteq$，其中 $\bot$（bottom）代表「未定義值」，$\bot \sqsubseteq x$ 對所有 $x$ 成立。資訊越多的元素「越大」：

$$\bot \sqsubseteq 0 \sqsubseteq 1 \sqsubseteq 2 \sqsubseteq \cdots \sqsubseteq \top$$

### 線索二：單調與連續函數

域之間的函數必須是單調的（$x \sqsubseteq y \Rightarrow f(x) \sqsubseteq f(y)$），更好的是連續的（保序上確界）：

$$f\left(\bigsqcup_{n} x_n\right) = \bigsqcup_{n} f(x_n)$$

連續函數是「資訊增量」的合理運算：輸入多一點資訊，輸出就多一點，不會無中生有。

### 線索三：Kleene 不動點定理 -- 破案時刻

Kleene 不動點定理說：連續函數 $f: D \to D$ 在 CPO 上必有最小不動點，而且可以明確建構出來：

$$\mathrm{fix}(f) = \bigsqcup_{n=0}^{\infty} f^n(\bot)$$

從 $\bot$ 開始，反覆套用 $f$，逼近極限。這就是遞迴的語義：

$$\llbracket \mathrm{rec}\ f.\ e \rrbracket = \mathrm{fix}\left(\lambda d.\ \llbracket e \rrbracket[d/f]\right)$$

「rec 到底是什麼」的答案：遞迴程式的語義是其定義函數的最小不動點——最小的一個滿足方程的解，恰好捕捉「定義最少的合理行為」。

### 線索四：自指域 $D \cong [D \to D]$

剩下Scott 自己過去的「不可能證明」怎麼辦？他發現：若放棄集合論的全函數空間，改用**連續函數的域**，則基數悖論消失。Scott 用投影（retraction）與反演極限（inverse limit）建構出一個與自身函數空間同構的域 $D \cong [D \to D]$。函數可以是自己的輸入——λ-Calculus 終於有了數學模型。

### 程式驗證：最小不動點迭代

用 Python 在整數「平頂域」上模擬最小不動點的收斂：

```python
# 階乘的語義：f(n) = if n == 0 then 1 else n * f(n-1)
# 在「部分函數域」上：未定義 = None，定義 = 整數
BOT = None

def apply_factorial_step(f):
    """回傳 f 的一步逼近：fun g. fun n. if n==0 then 1 else n*g(n-1)"""
    def g(n):
        if n == 0:
            return 1
        prev = f(n - 1)
        if prev is BOT:      # f 未定義處，此步也未定義
            return BOT
        return n * prev
    return g

def fix_iterate(step, depth=12):
    """fix(f) = ⊔ f^n(⊥) 的有限逼近"""
    d = BOT
    for i in range(depth):
        d = step(d)
        print(f"第 {i} 次逼近: {d(3)}")
    return d

fact = fix_iterate(apply_factorial_step)
print("收斂結果 fact(3) =", fact(3))   # 6
print("收斂結果 fact(5) =", fact(5))   # 120
```

前幾次逼近 `f^n(⊥)(3)` 依次為 `None, None, None, 6, 6, ...`：逼近序列最終到達正確值。這正是「遞迴程式 = 最小不動點」的具體演示。

### 指稱語義：語義函數 ⟦e⟧

最後拼上 Strachey 的部分：語義函數 $\llbracket \cdot \rrbracket$ 把語法映射到域中的值：

$$\llbracket e_1 + e_2 \rrbracket \rho = \llbracket e_1 \rrbracket \rho + \llbracket e_2 \rrbracket \rho$$

其中 $\rho$ 是環境（environment，變數到域值的映射）。語法構造對應語義構造，這是「組合性」原則。

## 結案 -- 後果與影響

- 遞迴與循環的語義從此有了數學定義：最小不動點。這是本世紀程式語言理論最重要的單一概念之一。
- 指稱語義成為形式語義學的主流學派，牛津學派（Scott-Strachey）與後續的Plotkin 成為標準教材內容。
- Haskell 的 non-strict semantics（懶惰語義）直接建立在域理論上：`bottom`、strictness analysis、`seq` 的行為都以 ⊥ 與偏序來定義。
- ML、OCaml 的遞迴語義、模式匹配的完備性分析也依賴域論思維。
- 形式化驗證（如 Powerdomain、抽象解釋 Cousot 夫婦 1977）都是域理論的直系後裔。
- Scott 後續到 Carnegie-Mellon、Oxford，持續發展 domain theory；Strachey 的《Fundamental Concepts》講義（1967，死後出版）成為經典。

## 關鍵人物與文獻

- Dana Scott, *A Type-Theoretical Alternative to ISWIM, CUCH, OWHY*, 1969（手稿，2006 年正式發表於 Theoretical Computer Science 363(1)）。
- Dana Scott, *Outline of a Mathematical Theory of Computation*, Oxford Programming Research Group, Technical Monograph PRG-2, 1970。
- Scott, D. and Strachey, C., *Toward a Mathematical Semantics for Computer Languages*, Oxford PRG Technical Monograph PRG-6, 1971。
- Strachey, C., *Fundamental Concepts in Programming Languages*, Lecture notes, Oxford, 1967；重刊於 Higher-Order and Symbolic Computation 13(1-2), 2000。
- Joseph E. Stoy, *Denotational Semantics: The Scott-Strachey Approach to Programming Language Theory*, MIT Press, 1977。
- Abramsky, S. and Jung, A., *Domain Theory*, in Handbook of Logic in Computer Science, Vol. 3, Oxford University Press, 1994。
