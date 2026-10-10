# 1956-Chomsky語言層級

## 案件摘要

1956 年，Chomsky 在《IRE Transactions on Information Theory》發表〈Three Models for the Description of Language〉，為語言找回了缺失的數學骨架。他比較了三種語言描述模型——有限狀態馬可夫過程、短語結構文法、轉換文法——並建立了著名的語言層級：Type-3 ⊂ Type-2 ⊂ Type-1 ⊂ Type-0。這篇短文證明了英語的某些結構（如中心嵌入）無法用有限狀態機描述，把語言學與計算理論正式接軌，也埋下「自然語言究竟在哪個層級」這場至今未歇的爭論。

## 前因 -- 為什麼會有這個案子

- Shannon 1948 年的《A Mathematical Theory of Communication》用馬可夫鏈近似英語字母與詞序列，語言第一次被當成隨機過程描述。
- 但馬可夫模型只能捕捉局部統計依賴，無法表達語言的遞迴結構——缺乏語言的「生成能力」理論。
- 美國結構主義語言學（Bloomfield、Harris）的分布主義（distributionalism）只做語料分類，沒有數學化的生成機制。
- Chomsky 師承 Harris，但走向相反方向：他要的不是分類，而是形式系統。
- 資訊理論與自動機理論在 1950 年代快速發展，提供了比較語言模型所需的數學工具。

## 線索與推理 -- 數學式、程式、理論

### Chomsky 層級：四個世界的嵌套

Chomsky 依生成規則的形式限制，把文法分為四層，生成能力嚴格遞增：

$$\text{Type-3} \subset \text{Type-2} \subset \text{Type-1} \subset \text{Type-0}$$

- Type-3（正規文法，regular）：規則形如 $A \to aB$ 或 $A \to a$，對應有限狀態自動機。
- Type-2（上下文無關文法，context-free）：規則形如 $A \to \alpha$，對應下推自動機。
- Type-1（上下文有關文法，context-sensitive）：規則形如 $\alpha A \beta \to \alpha\gamma\beta$。
- Type-0（無限制文法）：任意改寫規則，等價於圖靈機。

各層級的判定（recognition）複雜度差異巨大：

$$\text{regular: } O(n), \quad \text{CFL: } O(n^3), \quad \text{CSL: PSPACE}, \quad \text{RE: undecidable}$$

這個「生成能力 vs 判定代價」的取捨，是計算語言學最核心的數學張力。

### 「英語不是 regular」的證明

Chomsky 的偵探式論證：若英語是正規語言，則所有英語句子構成的集合可被有限狀態機接受。但他給出兩類反例。

1. **長距離依賴**：條件句 "if $S_1$, then $S_2$" 中，if 與 then 的配對距離可以任意長——有限狀態機沒有記憶，無法追蹤。
2. **中心嵌入（center embedding）**：

$$\text{The rat the cat the dog chased killed ate the malt.}$$

結構是 $a^n b^n$ 型的嵌套：名詞短語逐層嵌入，開頭的 the...the...the 必須與結尾的動詞鏈反向配對。形式化：語言 $\{a^n b^n \mid n \geq 0\}$ 不是正規的，可用 pumping lemma 證明——正規語言的足夠長句子必可切分為 $uvwxy$，其中 $vx$ 可任意重複而不離開語言；但 $a^n b^n$ 重複中間片段後 $a$ 與 $b$ 數量失衡，離開語言。

### 馬可夫過程 vs 轉換文法

- 馬可夫模型：$P(w_i \mid w_{i-1})$ 只看前一狀態，無法表達任意深的嵌套。
- 短語結構文法（CFG）：可以用遞迴規則生成中心嵌入，但無法處理被動式等轉換現象。
- 轉換文法：CFG 加上轉換規則，是 Chomsky 認為描述英語所需的第三層模型。
- 這個三層比較直接預告了次年《Syntactic Structures》的完整理論。

### 程式碼示範：pumping lemma 驗證與 CFG 解析

```python
# pumping lemma 驗證：a^n b^n 不是 regular
# 正規語言性質：存在 p，任何長度 >= p 的字串 s 都可切成 u v w x y，
# 使 |v x| >= 1、|v w x| <= p，且對所有 i >= 0，u v^i w x^i y 仍在語言中。
# 反證：取 s = a^p b^p，v x 只能落在 a 段或 b 段（|vx|<=p 跨不過中點），
# 重複後 a、b 數量失衡 -> 離開語言 -> 非 regular。

def is_an_bn(s):
    i = s.count("a")
    return i == s.count("b") and i > 0

p = 3
s = "a" * p + "b" * p
print(f"s = {s}, 在語言中: {is_an_bn(s)}")

# 窮舉所有合法切分位置（v x 完全在 a 段），驗證 pumping 必然失敗
failures = 0
for v_len in range(1, p + 1):
    for x_len in range(0, p + 1 - v_len):
        pumped = "a" * (p + v_len) + "b" * (p + x_len)  # v x 皆在 a 段
        if is_an_bn(pumped):
            failures += 1
print(f"泵入後仍在語言中的切分數: {failures}（0 表示 pumping lemma 成立，非 regular）")

# 簡易 CFG 解析器：檢查 a^n b^n 型的中心嵌入（等價於下推自動機）
def parse_center_embedding(tokens):
    # 嵌套語法: S -> NP VP；NP -> NP S | the N；以括號深度模擬堆疊
    depth = 0
    for t in tokens:
        if t == "the":
            depth += 1      # 開啟一層嵌入
        elif t in ("killed", "ate", "chased"):
            depth -= 1      # 動詞關閉一層
        if depth < 0:
            return False
    return depth == 0

sent = "the rat the cat the dog chased killed ate the malt".split()
print(f"中心嵌入句解析成功: {parse_center_embedding(sent)}")
# 正規自動機（只有有限狀態、無堆疊）做不到這件事——這就是層級的分界
```

## 結案 -- 後果與影響

- 計算語言學獲得數學骨架：形式語言理論成為描述語言結構的標準語言。
- 編譯器理論的直接基礎：程式語言語法被形式化為 CFG，ALGOL 58/60 的語法設計、日後的 LR/LL 剖析演算法皆源於此。
- NLP 剖析器的理論目標確立：1950-60 年代的自然語言解析系統以 CFG 為核心。
- 「自然語言在哪個層級」的爭論至今：英語中心嵌入的處理能力、統計語言模型是否「真的是語法」、LLM 的隱式文法，都是這場爭論的現代化身。
- 生成能力與判定複雜度的取捨成為工程指南：選哪一層文法，就是在選「表達力 vs 可計算性」。

## 關鍵人物與文獻

- Noam Chomsky (1956). "Three Models for the Description of Language." *IRE Transactions on Information Theory* 2(3): 113–124.
- Claude Shannon (1948). "A Mathematical Theory of Communication." *Bell System Technical Journal* 27: 379–423, 623–423.
- Noam Chomsky (1957). *Syntactic Structures.* The Hague: Mouton.
- Noam Chomsky (1959). "On Certain Formal Properties of Grammars." *Information and Control* 2(2): 137–167.（層級的嚴格數學化與 pumping lemma）
- Zellig Harris (1951). *Methods in Structural Linguistics.* University of Chicago Press.（分布主義的方法論出發點）
