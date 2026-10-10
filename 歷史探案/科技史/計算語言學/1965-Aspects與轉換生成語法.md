# 1965-Aspects與轉換生成語法

## 案件摘要

1965 年，Chomsky 出版《Aspects of the Theory of Syntax》，把 1957 年的「CFG + 轉換」升級為更精確的「標準理論」（standard theory）。書中正式引進深層結構與表層結構之分、能力/表現（competence vs performance）之分，以及普遍語法假說，試圖讓語義有系統地進入語法理論。這本書是規則法的理論高峰，而「competence/performance」這條分界線，更成為規則法 vs 統計法之爭、乃至 2020 年代「LLM 是否有語言能力」辯論的核心。

## 前因 -- 為什麼會有這個案子

- 《Syntactic Structures》的 CFG + 轉換規則不夠精確：轉換規則可以任意改變語義，理論缺乏約束。
- 語義如何進入語法理論的爭論：Katz-Postal 假說（1964）主張所有語義解釋都應由深層結構決定，轉換規則不影響語義。
- 描述性語法（只描述語料）vs 解釋性語法（解釋說話者為何能產生與理解句子）的方法論分歧。
- 1950 年代末的語料中，歧義句（如 "Flying planes can be dangerous"）顯示表層形式相同、深層結構不同的現象，需要新概念。
- 認知革命氛圍興起，語言學被期待成為「心理學的一部分」。

## 線索與推理 -- 數學式、程式、理論

### 深層結構與表層結構

《Aspects》的核心發明：每個句子有兩層句法表徵。

- **深層結構（deep structure）**：由基礎規則（base rules）生成的句法結構，承載語義解釋。
- **表層結構（surface structure）**：經轉換規則變換後的實際句序，決定語音形式。

標準理論的規則層次是一條流水線：

$$\text{base rules} \to \text{deep structure} \to \text{transformational rules} \to \text{surface structure} \to \text{semantic interpretation}$$

形式化：句子 $s$ 的語義由深層結構 $d$ 決定，表層結構 $t = T(d)$ 只決定語音。歧義句的破案工具：

- "Flying planes can be dangerous" 有一個深層結構（planes fly → 飛機危險）與另一個（[someone] flies planes → 開飛機危險）——表層相同、深層不同，所以歧義。
- 反之，主動與被動句表層不同、深層相同，所以語義相同。

### 能力/表現之分

《Aspects》最影響深遠的方法論分界：

- **能力（competence）**：ideal speaker-listener 在完全無干擾下所具備的內在語法知識——語法理論描述的對象。
- **表現（performance）**：實際的語言行為，受記憶、注意、口誤、猶豫、中心嵌入的加工極限所扭曲——不是語法理論的對象。

形式上，實際語料是能力的「雜訊觀測」：

$$\text{observed data} = \text{performance} = f(\text{competence}) + \text{noise}$$

因此「語料中的頻率」不反映語法知識——這是 Chomsky 反對統計方法的哲學根據。而統計 NLP 陣營則認為：既然只能觀測 performance，就該直接為 performance 建模。這條戰場延燒到 2020 年代：LLM 從語料（performance）中學習，它是否因此獲得「能力」，正是 competence/performance 之分的現代化身。

### 普遍語法與選擇限制

- **普遍語法（universal grammar）**：人類語言共有的、天生的語法原則集合，具體語言是它的參數化實例。這是語言習得悖論（刺激貧乏）的解答草案。
- **選擇限制（selectional restrictions）**：詞項帶語義特徵（如 [±human]、[±abstract]），句法規則要求動詞與論元的特徵相容。例如 "admire" 要求受事為 [+human]——這使 "sincerity admires John" 在深層結構階段即被標記為異常。
- Katz-Postal 假說被吸收：語義解釋規則只看深層結構。

### 程式碼示範：深層/表層轉換（主動轉被動）

```python
# 標準理論的轉換規則示範：主動轉被動
# T_passive: NP1 + V + NP2  =>  NP2 + be + V-en + by + NP1
# 詞項語義特徵（選擇限制）——這是《Aspects》的新發明
features = {
    "John":       {"human": True},
    "sincerity":  {"human": False, "abstract": True},
    "the boy":    {"human": True},
    "the book":   {"human": False},
    "admire":     {"requires_object_human": True},
    "read":       {},
}
V_past_participle = {"admire": "admired", "read": "read", "love": "loved"}

def t_passive(np1, v, np2):
    # 深層結構階段：檢查選擇限制
    if features[v].get("requires_object_human") and not features[np2]["human"]:
        return f"[深層結構異常: {v} 的受事必須為人類，但 {np2} 不是]"
    # 轉換規則套用：產生表層結構
    return f"{np2} is {V_past_participle[v]} by {np1}"

# 深層相同、表層不同 -> 語義相同；選擇限制在深層階段排除異常句
print(t_passive("John", "admire", "sincerity"))
# -> [深層結構異常: admire 的受事必須為人類，但 sincerity 不是]
print(t_passive("the boy", "read", "the book"))
# -> the book is read by the boy

# 歧義句的深層/表層分析：Flying planes can be dangerous
print("表層結構: Flying planes can be dangerous （只有一個）")
for d in ["planes + fly              (深層1: 飛機自己飛 -> 飛機危險)",
          "[someone] + fly + planes   (深層2: 駕駛飛機 -> 開飛機這件事危險)"]:
    print(f"  對應深層結構: {d}")
print("=> 表層一對多 -> 歧義；深層是語義解釋的鑰匙（標準理論的破案時刻）")

# competence vs performance 的數學對照
def competent(n): return True           # 能力層面：語法皆允許
def performance_limit(n): return n <= 3  # 表現層面：實際無法處理深嵌套
print("n=5 的中心嵌入句：語法合法 =", competent(5), ", 實際可處理 =", performance_limit(5))
print("=> competence ≠ performance，語料頻率不反映語法知識")
```

## 結案 -- 後果與影響

- 規則法的理論高峰：標準理論成為 1960s–1980s 語言學主流，語法研究全面心理化。
- 理論演化的起點：標準理論的不足催生 GB 理論（1981《Lectures on Government and Binding》）與最簡方案（1995《The Minimalist Program》）。
- NLP 的規則法系統皆受影響：LFG（1978，Bresnan）、HPSG（1984，Pollard & Sag）在功能與詞彙層面回應標準理論的問題。
- competence/performance 之分成為規則法 vs 統計法的哲學戰場：統計 NLP（1980s-90s）直接挑戰「頻率不反映語法知識」的立場。
- 這條分界線延續到 2020 年代：LLM 是否從語料中獲得「語言能力」，是 competence/performance 之分的當代辯論核心——六十年的懸案仍在進行。

## 關鍵人物與文獻

- Noam Chomsky (1965). *Aspects of the Theory of Syntax.* Cambridge, MA: MIT Press.
- Jerrold Katz, Paul Postal (1964). *An Integrated Theory of Linguistic Descriptions.* Cambridge, MA: MIT Press.（Katz-Postal 假說）
- Noam Chomsky (1981). *Lectures on Government and Binding.* Dordrecht: Foris.
- Noam Chomsky (1995). *The Minimalist Program.* Cambridge, MA: MIT Press.
- Joan Bresnan (1978). "A Realistic Transformational Grammar." 收錄於 Halle, Bresnan & Miller 編 *Linguistic Theory and Psychological Reality*, MIT Press.（LFG 的起點）
- Carl Pollard, Ivan Sag (1994). *Head-Driven Phrase Structure Grammar.* University of Chicago Press.
