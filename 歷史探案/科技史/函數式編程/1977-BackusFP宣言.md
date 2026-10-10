# 1977-BackusFP宣言

## 案件摘要

1977 年，John Backus 站上 ACM 圖靈獎演說的講台，做了一件震撼全場的事：這位 Fortran 與 BNF 的發明人，公開宣判自己一手催生的命令式程式設計是「死路」。演說題目是「Can Programming Be Liberated from the von Neumann Style? A Functional Style and Its Algebra of Programs」，1978 年發表於 CACM 21(8)。Backus 提出 FP 系統：無變數、無賦值，只由 combining forms 組合的函數式程式，並主張程式應該像代數式一樣可以被推理與變換。這是函數式編程第一次登上主流舞台。

## 前因 -- 為什麼會有這個案子

- Backus 是 Fortran（1957）與 BNF（Backus-Naur Form, 1959）的發明人，貢獻無人能否認；但他自己承認 Fortran 是「一次性」的成功——靠大量的即興 hack 壓榨 von Neumann 機器，無法成為長遠的程式設計典範。
- von Neumann 架構的暴政：CPU 與記憶體之間「一個字一個字搬運」，傳統語言把這個瓶頸直接搬進語言設計——程式被迫以變數與賦值的方式一個一個更新狀態。
- 傳統語言無法用代數推理：一段含賦值的程式碼，你無法像對付 $f \circ g$ 那樣對付它——沒有等式、沒有變換律、沒有組合性。
- APL 的啟發：Iverson 的 APL 語言用陣列運算子取代迴圈，讓 Backus 看到「不用變數也能寫程式」的可能性。
- 於是 1977 年，他在圖靈獎演說上發表宣言：程式設計應該從 von Neumann 風格中解放，改用函數式風格。

## 線索與推理 -- 數學式、程式、理論

### 線索一：von Neumann bottleneck

Backus 指出問題的核心：CPU 與記憶體之間只有一條「搬 word 的通道」，程式設計被迫把問題切碎成一個個字的搬運：

```
word ← memory[addr]     ; 搬一個字
word ← word + 1         ; 改一個字
memory[addr] ← word     ; 搬回去
```

整個程式語言的語法（變數、賦值、迴圈）都是圍繞這個瓶頸設計的。語義被機器架構綁架。

### 線索二：FP 系統 -- 無變數無賦值

Backus 的解法：FP 系統中程式只由**combining forms**（組合形式）建構——如 $\circ$（組合）、$[f, g]$（tuple）、$\alpha f$（apply-to-all，即 map）、$/f$（insert，即 reduce）。沒有變數、沒有賦值：

$$\text{wordcount} = \text{length} \circ \text{tokens}$$

這是 dot-free 記法：程式就是函數的組合式，像代數式一樣。對照命令式版本：

```python
# 命令式：一個字一個字搬運
def wordcount_imperative(text):
    count = 0
    in_word = False
    for ch in text:
        if ch == ' ':
            in_word = False
        elif not in_word:
            count += 1
            in_word = True
    return count

# FP 風格：組合式
def wordcount_fp(text):
    return len(tokens(text))   # length ∘ tokens
```

### 線索三：程式的代數律

FP 的核心主張：程式滿足代數律，因此可以「程式變換」做優化。基本律如：

$$(f \circ g) \circ h = f \circ (g \circ h) \qquad \text{（結合律）}$$

$$\alpha f \circ \alpha g = \alpha (f \circ g) \qquad \text{（map 融合律）}$$

融合律說：先 map $g$ 再 map $f$，等於一次 map 完 $f \circ g$。這意味著中間結構可以被消滅——Deforest（stream fusion）的先聲。

### 線索四：融合優化實作 -- 破案時刻

用 Python 示範融合律如何消滅中間 list：

```python
def mymap(f, xs):
    return [f(x) for x in xs]

def mymap_fused(f, g, xs):
    return [f(g(x)) for x in xs]

xs = list(range(1_000_000))

# 未融合：建構中間 list（100 萬個元素的暫存結構）
step1 = mymap(lambda x: x * 2, xs)      # 中間 list 佔記憶體
step2 = mymap(lambda x: x + 1, step1)   # 再建一個

# 融合：map f ∘ map g = map (f∘g)，中間 list 消失
result = mymap_fused(lambda x: x + 1, lambda x: x * 2, xs)

assert step2 == result                  # 代數律保證相等
print(result[:5])                       # [1, 3, 5, 7, 9]
```

融合版本少建構一個百萬元素的 list：時間與記憶體都省一半。這就是「用代數律做優化」的具體證據——程式變換的威力。

### 線索五：代數推理的威力

融合律可以反覆套用、鏈式消滅：

$$\alpha f \circ \alpha g \circ \alpha h = \alpha(f \circ g) \circ \alpha h = \alpha(f \circ g \circ h)$$

一串 n 個 map 可以融合成 1 個。在串流（stream）場景下，這就是 deforestation：中間結構從未完整存在，逐元素流水線處理。

### 線索六：FP 的局限與後續

FP 系統本身太極簡（無型別、無使用者定義的多型），未能直接流行；但它的**哲學**——組合性、代數律、程式變換——存活下來，成為 Haskell 的核心精神。

## 結案 -- 後果與影響

- FP 第一次登上主流舞台：圖靈獎演說吸引大量研究者投入函數式編程，是 1987 年 Haskell 委員會成立的動機之一。
- map/reduce 的哲學先聲：2004 年 Google MapReduce、Spark RDD 的「map 與 reduce 為核心運算子」思想直接源自此傳統。
- Haskell 的 list fusion、GHC rewrite rules（使用者可自訂程式變換規則）是「代數律做優化」的直接實現。
- Deforestation（Wadler 1990）與 stream fusion（Coutts et al. 2007）都是融合律的工程化。
- 組合性原則成為函數式編程的核心美學：point-free style、函數組合库（如 Haskell 的 `(.)`、F# 的 `>>`）。
- Backus 的「程式即代數」主張影響了程式變換系統（如 Bird-Meertens formalism，BMF）的發展。

## 關鍵人物與文獻

- Backus, J., *Can Programming Be Liberated from the von Neumann Style? A Functional Style and Its Algebra of Programs*, Communications of the ACM, 21(8), 1978（1977 圖靈獎演說）。
- Backus, J., *The Syntax and Semantics of the Proposed International Algebraic Language of the Zurich ACM-GAMM Conference*, 1959（BNF 的起源）。
- Iverson, K., *A Programming Language*, Wiley, 1962（APL，Backus 的啟發來源）。
- Wadler, P., *Deforestation: Transforming Programs to Eliminate Trees*, Theoretical Computer Science, 73, 1990。
- Bird, R. and Meertens, L., *Two Exercises Found in a Book on Algorithmics*, 1987（Bird-Meertens formalism）。
- Coutts, D., Leshchinskiy, R., Stewart, D., *Stream Fusion: Practical Lists-of-Fusion for Program Computation*, ICFP, 2007。
- Dean, J. and Ghemawat, S., *MapReduce: Simplified Data Processing on Large Clusters*, OSDI, 2004。
