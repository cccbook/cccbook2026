# 1970-Earley剖析器

## 案件摘要

1970 年，Jay Earley 在《Communications of the ACM》發表〈An Efficient Context-Free Parsing Algorithm〉，為「如何高效剖析上下文自由文法（CFG）」這樁懸案提出了一個優雅的解法。他的策略是動態規劃：把剖析過程中所有「半成品」記錄在一張圖表（chart）上，避免重複工作，也避免遞迴下降的無窮循環。Earley 剖析器不需要把文法轉成 CNF 形式、能處理任意 CFG、還能自然地表示歧義句的多重剖析。它成為 chart parsing 家族的經典起點，至今仍是 NLP 教科書的標準內容。

## 前因 -- 為什麼會有這個案子

- Chomsky 1956-1957 年確立 CFG 為描述自然語言句法的基本框架，但「給定文法與句子，如何求出剖析樹」的演算法問題遲遲沒有令人滿意的答案。
- 遞迴下降（top-down）剖析器遇到左遞迴規則（如 NP → NP and NP）會無窮遞迴，而自然語言文法充滿這類規則。
- CYK 演算法（1960-1962）雖然是 O(n³) 的動態規劃，但要求文法必須先轉成 Chomsky Normal Form（只允許 A → B C 與 A → a），轉換後的文法失去可讀性，剖析樹也需再還原。
- NLP 的實際需求：句子普遍存在結構歧義（ambiguity），例如「I saw the man with the telescope」有兩種剖析；剖析器必須能同時表示所有可能，而非只回傳一個。
- 1960 年代末，Earley 在 CMU 進行博士研究，想找一個「直接用原始文法、能處理歧義、複雜度可控」的通用剖析演算法。

## 線索與推理 -- 數學式、程式、理論

### 核心證據：Earley item 與 chart

Earley 的關鍵發明是「帶點的狀態項」（dotted rule / Earley item）：

$$[A \rightarrow \alpha \bullet \beta, \; i]$$

dot 的語義：規則右側 $\alpha$ 的部分已經「被掃描或推導完成」，對應輸入從位置 $i$ 開始的部分；$\beta$ 是尚未處理的部分。整個剖析過程維護一組狀態集 $S_0, S_1, \dots, S_n$（n 為句子長度），$S_j$ 記錄「讀完第 j 個詞之後，所有可能的半成品」。若最終 $S_n$ 中出現 $[S' \rightarrow S \bullet, 0]$，句子即被辨識（recognize）。

### 三個操作：推理的三步棋

chart 上每個狀態集反覆執行三個操作，直到不動點：

- **Predictor（預測）**：對 $[A \rightarrow \alpha \bullet B, i]$，為每條規則 $B \rightarrow \gamma$ 加入 $[B \rightarrow \bullet \gamma, j]$——「接下來應該出現 B，先預測它的所有展開方式」。
- **Scanner（掃描）**：對 $[A \rightarrow \alpha \bullet a, i]$ 且第 j 個詞是 $a$，加入 $[A \rightarrow \alpha a \bullet, i]$ 到 $S_{j+1}$——「詞與預期相符，dot 前進」。
- **Completer（完成）**：對 $[A \rightarrow \gamma \bullet, i]$（A 完成），回頭修改所有 $S_i$ 中形如 $[B \rightarrow \alpha \bullet A, k]$ 的項，將其升級為 $[B \rightarrow \alpha A \bullet, k]$——「一個半成品等到了它的組成部分」。

### 複雜度分析：破案的量尺

設句子長度為 n，Earley 剖析器的複雜度取決於 Completer 的代價：

- 一般 CFG：$O(n^3)$——與 CYK 相同，但不需 CNF 轉換。
- 無歧義文法：$O(n^2)$——每個 item 只被完成一次。
- 近似正則（regular）文法：$O(n)$——chart 上活躍的 item 數為常數。

這個「複雜度隨文法性質滑動」的特性，是 Earley 演算法優於固定 $O(n^3)$ 的 CYK 之處。

### recognize-then-parse 的兩階段

Earley 演算法天然分兩階段：第一階段（recognizer）只判斷句子是否合法；第二階段（parser）在 chart 上回溯，從 $S_n$ 的完成項往回取出完整剖析樹。歧義句會取出多棵樹——這正是 NLP 需要的能力。

### 可執行程式：mini Earley 剖析器

```python
# mini Earley parser: Predictor / Scanner / Completer
grammar = {
    "S":  [["NP", "VP"]],
    "NP": [["Det", "N"], ["NP", "PP"]],
    "PP": [["P", "NP"]],
    "VP": [["V", "NP"], ["VP", "PP"]],
}
POS = {"Det": {"the"}, "N": {"man", "telescope", "hill"}, "V": {"saw"},
       "P": {"with", "on"}}

def earley(words):
    n = len(words)
    chart = [[] for _ in range(n + 1)]
    def add(j, item):
        if item not in chart[j]:
            chart[j].append(item); return True
        return False
    add(0, (("S", "S"), (), 0))       # 虛擬起始規則 S -> . S
    for j in range(n + 1):
        i = 0
        while i < len(chart[j]):
            rule, before, origin = chart[j][i]
            rhs = rule[1:]                # 右側符號序列
            todo = rhs[len(before):]      # 尚未處理的部分
            if todo:                  # dot 未到底
                nxt = todo[0]
                if nxt in POS:        # Scanner
                    if j < n and words[j] in POS[nxt]:
                        add(j + 1, (rule, before + (nxt,), origin))
                elif nxt in grammar:  # Predictor
                    for r in grammar[nxt]:
                        add(j, ((nxt,) + tuple(r), (), j))
            else:                     # Completer
                for (r2, b2, o2) in list(chart[origin]):
                    t2 = r2[1:][len(b2):]
                    if t2 and t2[0] == rule[0]:
                        add(j, (r2, b2 + (rule[0],), o2))
            i += 1
    return (("S", "S"), ("S",), 0) in chart[n]

print(earley("the man saw the hill with the telescope".split()))  # True
```

執行結果為 `True`，且 chart 中會同時保有「介系詞片語修飾 VP」與「修飾 NP」兩種半成品——歧義被完整記錄。

## 結案 -- 後果與影響

- Earley 演算法成為 chart parsing 的經典範式，啟發了 1984 年 Tomita 的 GLR 演算法（用圖表修復 LR 剖析器的歧義處理）。
- CYK 的變體與 Earley 一起構成「圖表剖析」（chart parsing）傳統，成為 NLP 剖析器的標準架構。
- Python NLTK 內建 `nltk.parse.chart` 與 Earley 剖析器實作，至今仍是教學標準工具。
- garden path 句（如「The horse raced past the barn fell」）的解析研究，建立在 chart 能同時追蹤多個假設的基礎上。
- Earley 本人的原創動機其實是語義解析（semantic interpretation），但影響最深遠的是句法剖析部分——這是偵探沒有預料到的案外案。

## 關鍵人物與文獻（條例）

- Jay Earley (1970). "An Efficient Context-Free Parsing Algorithm." *Communications of the ACM*, 13(2), 94-102.
- Jay Earley (1969). *An Efficient Context-Free Parsing Algorithm.* PhD dissertation, Carnegie-Mellon University.
- Tadao Kasami (1965); Daniel Younger (1967). CYK 演算法的獨立提出者，O(n³) 剖析的先驅。
- M. Tomita (1984). *Efficient Parsing for Natural Language.* Kluwer. GLR 演算法，chart parsing 的後繼者。
- Noam Chomsky (1957). *Syntactic Structures.* Mouton. CFG 與自然語言句法的理論起點。
