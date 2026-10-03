# 1957-SyntacticStructures

## 案件摘要

1957 年，Chomsky 出版《Syntactic Structures》，這本薄薄的小書徹底改變了語言學的研究對象：語法不再是語料分類的「清單」，而是一個會「生成」句子的裝置。書中用短語結構文法加轉換規則描述英語句法，並以「Colorless green ideas sleep furiously」這句語法合法但語義荒謬的例句，證明語法獨立於語義。這本書成為認知革命的號角，也為 NLP 確立了「剖析」（parsing）這個持續六十年的目標。

## 前因 -- 為什麼會有這個案子

- 美國結構主義語言學（Bloomfield 1933、Harris 1951）的方法論是分布主義：只靠語料中語音與詞的分佈做分類，避免觸碰「意義」與「心理」。
- 分布主義只能描述「看過的語料」，無法解釋說話者為何能理解從未聽過的新句子。
- Chomsky 想把語法變成「生成裝置」：一組有限的規則，生成無限的句子集合——這正好對應說話者的創造性。
- 1956 年的三模型論文已鋪好數學地基，1957 年的專書要給出英語的完整分析。
- 機器翻譯與軍方資金讓形式化語法有工程上的急迫性。

## 線索與推理 -- 數學式、程式、理論

### 短語結構文法的生成式定義

語法 $G = (N, \Sigma, P, S)$，其中 $N$ 是非終端符號（S、NP、VP…），$\Sigma$ 是詞彙，$P$ 是生成規則，$S$ 是起始符號。書中分析英語的核心規則包括：

$$S \to NP + VP, \quad VP \to V + NP, \quad NP \to T + N$$

語法「生成」的語言是所有可從 $S$ 推導出的句子集合：

$$L(G) = \{ w \in \Sigma^* \mid S \Rightarrow^* w \}$$

關鍵在於：有限條規則經遞迴引用，生成無限句子——這就是 Chomsky 所謂語言的「無限使用有限手段」。

### 轉換規則：被動式的數學

短語結構文法無法優雅處理主動/被動的關係（兩句要各寫一套規則）。Chomsky 引入轉換規則（transformational rules）：作用於整個句法結構上的映射。被動轉換 $T_{\text{passive}}$：

$$NP_1 + V + NP_2 \Rightarrow NP_2 + be + V + en + by + NP_1$$

例如：

- 主動：John admires sincerity.
- 被動：Sincerity is admired by John.

轉換是「核」（kernel）句結構到衍生句的變換，這是語法理論第一次把句法關係寫成明確的映射。

### 「Colorless green ideas sleep furiously」

Chomsky 的著名偵探式例證：

> Colorless green ideas sleep furiously.（無色的綠色觀念狂暴地睡著。）

這句語義荒謬，但任何母語者都判定它「語法完全合法」；而詞序重排後的「Furiously sleep ideas green colorless」語義同樣荒謬，卻變得語法不合法。

- 這證明語法合法性与語義合法性是**獨立**的兩個層面，且語法合法性對**詞序結構**敏感，不只是詞的集合。
- 這句在真實語料中頻率為零，但母語者仍能判定其合法性——分布主義無法解釋，語法理論可以。

### 三個論證：馬可夫不可、有限狀態不可、CFG 可

《Syntactic Structures》第三章的偵探式排除法：

1. **有限狀態馬可夫模型不可**：無法表達中心嵌入（The rat the cat the dog chased killed ate the malt）的任意深度配對。
2. **短語結構文法可以**生成中心嵌入：遞迴規則 $NP \to NP + S'$ 提供無限嵌套能力。
3. **但 CFG 不足以**描述英語全部現象（被動式、助動詞移位），需要轉換規則。
結論：英語的語法是「CFG + 轉換」的第三種模型——這就是書的破案時刻。

### 程式碼示範：mini CFG 生成器

```python
import random
# 迷你 CFG：短語結構文法，遞迴規則可生成無限句子
grammar = {
    "S":  [["NP", "VP"]],
    "VP": [["V", "NP"], ["V", "NP", "ADV"]],
    "NP": [["T", "N"], ["NP", "REL"]],          # 遞迴：中心嵌入能力
    "REL": [["that", "NP", "V"]],
}
lexicon = {
    "T": ["the"], "N": ["ideas", "cat", "dog", "man"],
    "V": ["sleep", "chase", "admire"], "ADV": ["furiously"],
}
def generate(symbol="S"):
    if symbol in lexicon:
        return [random.choice(lexicon[symbol])]
    expansion = random.choice(grammar[symbol])
    return [tok for s in expansion for tok in generate(s)]
random.seed(7)
for _ in range(3):
    print(" ".join(generate()))
# 可能輸出（含中心嵌入）: the ideas that the cat that the dog admire chase chase
# Colorless green ideas sleep furiously：語法合法但語義荒謬
sentence = ["Colorless", "green", "ideas", "sleep", "furiously"]
def check_syntax(words):
    # 簡化檢查：Adj Adj N + V(不及物) + ADV -> 合法
    return (words[1] in ["green"] and words[2] in lexicon["N"]
            and words[3] in lexicon["V"] and words[4] in lexicon["ADV"])
print(f"語法合法: {check_syntax(sentence)}, 語義荒謬: True  -> 兩者獨立")
shuffled = sentence[::-1]  # Furiously sleep ideas green colorless
print(f"重排後語法合法: {check_syntax(shuffled) if len(shuffled)==5 else False}  -> 語法敏感於詞序")
```

## 結案 -- 後果與影響

- 認知革命的號角：語言被理解為「心理裝置」而非行為習慣，語言學重回認知科學中心。
- NLP 的「剖析」目標確立：1958 年 ALGOL 語法、1960 年代各種剖析器都以 CFG/轉換文法為理論核心。
- 機器翻譯的轉換法（1960 年代）：以轉換規則為基礎的翻譯系統成為規則法 MT 的主流路線。
- 「語法 vs 語義」的分離影響六十年：語法可獨立於語義研究，塑造了 1960-80 年代的理論語言學。
- 統計 NLP 的長期論敵：Chomsky 對統計方法的不信任，成為規則法 vs 統計法之爭的源頭。

## 關鍵人物與文獻

- Noam Chomsky (1957). *Syntactic Structures.* The Hague: Mouton.
- Noam Chomsky (1956). "Three Models for the Description of Language." *IRE Transactions on Information Theory* 2(3): 113–124.
- Leonard Bloomfield (1933). *Language.* New York: Henry Holt.（美國結構主義的方法論背景）
- Zellig Harris (1951). *Methods in Structural Linguistics.* University of Chicago Press.
