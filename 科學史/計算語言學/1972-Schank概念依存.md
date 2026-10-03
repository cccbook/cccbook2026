# 1972-Schank概念依存

## 案件摘要

1972 年，Roger Schank（時任 Stanford，後轉 Yale）在《Cognitive Psychology》發表〈Conceptual Dependency: A Theory of Natural Language Understanding〉，對「語言理解到底是什麼」這樁懸案提出激進答案：理解不是把句子解析成語法樹，而是把它轉譯成一種獨立於語言的「概念依存」（Conceptual Dependency, CD）表示。CD 用一小組原始動作（primitive acts，如 PTRANS、MTRANS、ATRANS）與固定的概念化結構表達意義，讓「John gave Mary a book」與「John handed a book over to Mary」在 CD 層完全相同。這套理論成為知識表示（KR）的先驅，並催生了 SAM、PAM、CYRUS 等故事理解系統，以及影響常識推理研究的腳本（script）理論。

## 前因 -- 為什麼會有這個案子

- Chomsky 的轉換生成語法只處理語法：它能判斷句子是否合語法，但對「意義」隻字未提——語義學在 1960 年代的 NLP 中幾乎是空白。
- 機器翻譯的歷史教訓（1966 ALPAC 報告後低潮）：逐詞對譯失敗，跨語言需要一種「表層之下」的中介表示（interlingua）。
- 表層結構不同的句子可以有相同意義（paraphrase），同一句子也可以有不同意義（ambiguity）——意義的表示必須把這兩件事分開。
- Schank 的心理學動機：他相信理解是人類認知的過程，AI 系統應該模擬人類「抓住概念、拋開字詞」的方式。
- 早期程序化語義（如 SHRDLU 1970）把意義寫成程序，但程序的表示無法做跨句推理與比較——Schank 想要一種可組合的靜態表示。
- Schank 想用「概念」而非「詞」作為意義的基本單位：詞是表層現象，概念才是深層結構。

## 線索與推理 -- 數學式、程式、理論

### 核心證據：原始動作與概念化結構

CD 的偵探手法是「化約」：把所有動作化約到一小組原始動作（primitive acts）：

- **PTRANS**：物理位置轉移（physical transfer）——「go」「move」「fly」的深層核心。
- **ATRANS**：抽象關係轉移（abstract transfer，如所有權）——「give」「take」「buy」的核心。
- **MTRANS**：心理資訊轉移（mental transfer）——「tell」「tell」「read」的核心。
- **MBUILD**：心智建構（thought creation）——「decide」「imagine」的核心。
- **ATE**、**DRINK**、**INGEST**：攝取類動作。
- **GRASP**、**MOVE**：操縱身體部位的動作。

概念化（conceptualization）是 CD 的基本結構，形式化為：

$$\text{Conceptualization} = [\text{Actor}, \; \text{Action}, \; \text{Object}, \; \text{Direction}, \; \text{Time}]$$

### 「John gave Mary a book」的 CD 表示

「give」的深層不是一個動作，而是兩個概念化的組合：

$$\text{ATRANS}(\text{book}, \; \text{John} \rightarrow \text{Mary})$$

即：一本書的抽象所有權（ATRANS）從 John 轉移到 Mary。這個表示的威力：

- 表層差異消失：「John gave Mary a book」「John handed a book over to Mary」「Mary received a book from John」在 CD 層完全相同（只是視角不同）。
- 歧義浮現：「John took the book」在 CD 層可以是 ATRANS（偷走所有權）或 PTRANS（物理拿走）——表層相同、深層不同，CD 把歧義表示出來。
- 推理變得直接：從 ATRANS 可以推出「Mary now has the book」「John no longer has the book」——CD 結構直接支援常識推理規則。

### 跨語言表示：interlingua 的目標

CD 的野心是成為跨語言的中介表示：中文「約翰給瑪麗一本書」、英文「John gave Mary a book」、日文的表層結構完全不同，但它們的 CD 表示相同。這正是 1960 年代機器翻譯夢寐以求的 interlingua——Schank 把它從翻譯工程搬到了認知理論。

### 腳本的先聲：餐廳腳本與 MOP

CD 表示單一句子的意義；要理解整段故事，需要「預期的知識」。Schank 與 Abelson（1977）提出腳本（script）：

$$\text{Script} = \text{Track}(\text{enter}, \; \text{order}, \; \text{eat}, \; \text{pay}, \; \text{leave})$$

「John went to a restaurant, ordered a hamburger, and left」——CD 層只有三個動作，但餐廳腳本補出了「付錢」「吃漢堡」「給小費」等未說出的概念。1980 年代 Schank 再發展 MOP（Memory Organization Packets），把腳本動態化，成為案例式推理（case-based reasoning）的先驅。

### 可執行程式：mini CD 表示器

```python
# mini CD 表示器：把簡單句子解析成 CD 結構
PRIMITIVES = {
    "gave":   "ATRANS", "took": "ATRANS", "bought": "ATRANS",
    "went":   "PTRANS", "moved": "PTRANS", "flew": "PTRANS",
    "told":   "MTRANS", "read": "MTRANS", "said": "MTRANS",
    "ate":    "INGEST", "drank": "INGEST",
    "decided": "MBUILD",
}

def to_cd(actor, verb, obj=None, direction=None):
    """產生 CD 概念化：[Actor, Primitive, Object, Direction]"""
    prim = PRIMITIVES.get(verb)
    if prim is None:
        raise ValueError(f"unknown verb: {verb}")
    return [actor, prim, obj, direction]

# 「John gave Mary a book」 -> ATRANS from John to Mary
cd1 = to_cd("John", "gave", obj="book", direction=("John", "Mary"))
print(cd1)   # ['John', 'ATRANS', 'book', ('John', 'Mary')]

# 表層不同、深層相同：paraphrase 檢查
cd2 = to_cd("Mary", "took", obj="book", direction=("John", "Mary"))
print(cd2[1] == cd1[1] and cd2[3] == cd1[3])   # True（同為 ATRANS John->Mary）

# 從 CD 推理：ATRANS 蘊含所有權轉移
def infer_ownership(cd):
    actor, prim, obj, (src, dst) = cd
    if prim == "ATRANS":
        return {f"{dst} now has {obj}", f"{src} no longer has {obj}"}
    return set()
print(infer_ownership(cd1))
# {'Mary now has book', 'John no longer has book'}
```

程式示範 CD 的三個核心：原始動作的化約、表層差異在 CD 層消失（paraphrase）、CD 結構直接支援常識推理。

## 結案 -- 後果與影響

- CD 成為知識表示（KR）研究的先驅：語義網路、框架（frames）、邏輯式表示法都在與 CD 的對話中成形。
- 催生一系列故事理解系統：SAM（Script Applier Mechanism, 1977）、PAM（Plan Applier Mechanism, 1978）、CYRUS（1980，記憶與政治人物傳記問答）——它們都用 CD 為底層表示。
- 腳本理論影響常識推理研究：餐廳腳本成為「預設知識如何補全理解」的教科書案例，案例式推理（CBR）的思想源頭。
- CD 的缺陷同樣重要：原始動作的完整性問題（約 10-15 個 primitives 真的夠嗎？「think」「love」「own」如何化約？）始終沒有滿意答案，化約的強制性造成資訊損失。
- 缺陷促成 1980 年代邏輯式知識表示（描述邏輯、非單調推理）與 1990 年代統計法的抬頭——「意義能否被窮舉為符號原語」這個問題被統計語義（word embeddings）以幾何方式重新回答。
- Schank 後來的語義路線（概念、腳本、MOP）與 2013 年 Word2Vec 的「語義 = 向量」路線形成兩個極端對照，是這樁案件最耐人尋味的餘波。

## 關鍵人物與文獻（條例）

- Roger C. Schank (1972). "Conceptual Dependency: A Theory of Natural Language Understanding." *Cognitive Psychology*, 3(4), 552-631.
- Roger C. Schank & Robert P. Abelson (1977). *Scripts, Plans, Goals, and Understanding: An Inquiry into Human Knowledge Structures.* Lawrence Erlbaum Associates.
- Roger C. Schank (1980). "Language and Memory." *Cognitive Science*, 4(3), 243-284.（MOP 的提出）
- Roger C. Schank & Christopher Riesbeck (1981). *Inside Computer Understanding: Five Programs Plus Miniatures.* Lawrence Erlbaum Associates.
- Roger Schank (1973). "Identification of Conceptualizations Underlying Natural Language." In Schank & Colby (eds.), *Computer Models of Thought and Language.* W. H. Freeman.
