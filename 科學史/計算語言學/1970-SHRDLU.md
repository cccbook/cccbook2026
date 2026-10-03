# 1970-SHRDLU

## 案件摘要

1968 至 1970 年，Terry Winograd 在 MIT 人工智慧實驗室完成 SHRDLU——一個能以自然語言對話、操縱虛擬「積木世界」的程式，並於 1971 年以博士論文《Procedures as a Representation for Data in a Computer Program for Understanding Natural Language》結案。SHRDLU 整合了語法（Halliday 系統語法）、語義（程序化語義）與推理（PLANNER 式目標導向搜尋）三層，能回答「the block on the table 是哪一塊」這類需要指稱消解的問題。它是規則式 NLP 的巔峰之作：在一個小得不能再小的世界裡，機器展現了真正的「理解」。但它的成功同時也是判決書——無法擴展到真實世界的規則法，註定在 1970 年代末迎來 AI 寒冬。

## 前因 -- 為什麼會有這個案子

- Chomsky 的轉換生成語法提供了語法理論基礎，但如何在程式裡「使用」語法來理解意義，仍是懸案。
- LISP 語言（McCarthy, 1958）的「程序即資料」（code as data，即 homoiconicity）特性，讓 Winograd 可以把語義直接寫成 LISP 程序。
- 1960 年代問答系統的局限：Baseball（1961）只靠關鍵字模式匹配、SIR（1964）只有粗糙的物性推理；ELIZA（1966）更只是無理解的心理諮商師模仿。
- Halliday 的系統語法（systemic grammar）強調語法選擇由功能與語境驅動，適合與語義、推理整合——Winograd 選它而非 Chomsky 學派。
- 「積木世界」（blocks world）策略：把領域縮到桌面上的幾塊積木，讓「完整理解」在封閉世界裡成為可能——這是當時 AI 的聰明妥協。
- PLANNER（Hewitt, 1969-1971）提供目標導向（goal-directed）的推理語言，成為 SHRDLU 的推理層。

## 線索與推理 -- 數學式、程式、理論

### 三層架構：語法、語義、推理的合流

SHRDLU 的偵探手法是「三層分工、即時對話」：

- **語法層**：Halliday 系統語法的剖析器，把句子解析成結構特徵。
- **語義層**：程序化語義（procedural semantics）——一個詞或句子的「意義」就是它所觸發的 LISP 程序。意義不是靜態的邏輯式，而是一段「如何在積木世界裡執行」的程式碼。
- **推理層**：PLANNER 式目標導向搜尋。要回答問題，就設定一個目標（goal），讓系統反覆嘗試可滿足目標的動作與查詢。

形式化地，理解句子 u 可以寫成三步合成：

$$\text{Semantics} = \llbracket \text{Syntax}(u) \rrbracket, \qquad \text{Answer} = \text{Inference}\big(\llbracket \text{Syntax}(u) \rrbracket, \; \text{WorldState}\big)$$

### 指稱消解與語境追蹤

SHRDLU 最精彩的線索是指稱消解（reference resolution）：當使用者說「Find a block which is taller than the one you are holding」，系統必須：

- 維護對話語境（discourse context）：追蹤「你正在拿的那一塊」是哪塊積木。
- 對候選積木逐一檢查性質，用目標導向搜尋找出滿足條件的物件。
- 若有歧義，反問使用者澄清——這是 1968 年就出現的澄清式對話。

典型對話：使用者問「How many blocks are not in the box?」，SHRDLU 查詢當前世界狀態（哪些積木不在箱子裡）並回答「Four of them」——語義程序直接查詢世界模型。

### 「程序即資料」的哲學

Winograd 的論文標題就是線索：資料的表示法是「程序」。積木的性質（紅色、在箱子上方）不是存在資料庫裡的布林值，而是可以呼叫的 LISP 函式。這呼應了 LISP 的 homoiconicity：

$$\text{program} \equiv \text{data}$$

知識與行動在語言層面上是同一種東西——這是 1970 年知識表示（KR）最有哲學野心的主張。

### 可執行程式：迷你積木世界 QA

```python
# mini blocks world: 簡單語法 + 世界狀態查詢 + 移動指令
world = {"A": {"color": "red",    "on": "table"},
         "B": {"color": "blue",   "on": "table"},
         "C": {"color": "red",    "on": "A"},
         "BOX": {"color": "green", "on": "table"}}

def blocks_on(x):   # 直接壓在 x 上的積木
    return [b for b, v in world.items() if v["on"] == x]

def find_block(pred):  # 目標導向搜尋：找第一個滿足條件的積木
    for b in world:
        if b != "BOX" and pred(b): return b
    return None

def move_block(src, dst):  # PTRANS 原語：移動
    if world[src]["on"] != "table" and src in blocks_on(world[src]["on"]):
        pass
    world[src]["on"] = dst
    return f"Moved {src} onto {dst}."

# 問答：「紅色的積木在哪裡？」
print(find_block(lambda b: world[b]["color"] == "red"))      # A
# 指令：「把藍色積木放到箱子上」
b = find_block(lambda b: world[b]["color"] == "blue")
print(move_block(b, "BOX"))                                   # Moved B onto BOX.
print({k: v["on"] for k, v in world.items()})                 # 世界狀態更新
```

程式示範了 SHRDLU 的三個核心：查詢即函式呼叫（程序化語義）、find_block 即目標導向搜尋（PLANNER 精神）、move_block 即對世界狀態的操作。

## 結案 -- 後果與影響

- SHRDLU 是規則式 NLP 的巔峰：完整的三層整合、真正的指稱消解、澄清式對話，在 1970 年無出其右。
- 同時是幻滅的開始：系統無法擴展到開放世界——每換一個領域就要重寫所有語法、語義程序與推理規則，「知識獲取瓶頸」浮上檯面。
- 1970 年代末 AI 寒冬（第一波）：過度承諾的規則法專案（含機器翻譯、語音識別）遭遇資金縮減，SHRDLU 常被引用為「受限領域的勝利與天花板」的雙面教材。
- 「受限領域」（microworld）策略本身有價值：證明了「理解 = 語法 + 語義 + 推理 + 世界模型」的架構在小規模上可行，成為後世對話系統的設計參照。
- 對話系統的先驅：ELIZA（1966）是無理解的模式匹配，SHRDLU 是有世界模型與推理的真理解——這條界線在 2020 年代 LLM 對話系統的哲學辯論中被反覆重新審視：LLM 像極了超大規模的 ELIZA，還是某種 SHRDLU？
- Winograd 後來轉向批評 AI（與 Flores 合著《Understanding Computers and Cognition》, 1986），成為這樁案件最耐人尋味的結局。

## 關鍵人物與文獻（條例）

- Terry Winograd (1971). *Procedures as a Representation for Data in a Computer Program for Understanding Natural Language.* PhD dissertation, MIT (AI Memo 235; 1972 年由 Birkhäuser 出版成書 *Understanding Natural Language*).
- Terry Winograd (1972). "Understanding Natural Language." *Cognitive Psychology*, 3(1), 1-191.
- Carl Hewitt (1969). "PLANNER: A Language for Manipulating theorems and Proving Theorems in a Robot." MIT AI Memo 168.
- M. A. K. Halliday (1967-1968). 系統語法理論，SHRDLU 語法層的基礎。
- Joseph Weizenbaum (1966). "ELIZA — A Computer Program for the Study of Natural Language Communication between Man and Machine." *Communications of the ACM*, 9(1), 36-45.
- Terry Winograd & Fernando Flores (1986). *Understanding Computers and Cognition.* Ablex.
