# 1970-WoodsATN

## 案件摘要

1970 年，William Woods（BBN 公司）在《Communications of the ACM》發表〈Transition Network Grammars for Natural Language Analysis〉，提出增強轉移網路（Augmented Transition Network, ATN）：在有限狀態機上加裝暫存器（registers）與遞迴呼叫子網路（push/pop）的能力。這個設計巧妙地繞過了 Chomsky 對有限狀態語言的否定——純 FSM 不夠，但加上遞迴的 FSM 就等價於 CFG。Woods 隨後把 ATN 用於 LUNAR 系統（1973），讓地質學家用英語查詢月球岩石資料庫。ATN 成為 1970-1980 年代 NLP 的主流剖析框架，但它「規則全靠手工編寫」的維護噩夢，也間接促成 1990 年代統計法的抬頭。

## 前因 -- 為什麼會有這個案子

- Chomsky（1956, 1957）證明英語不是有限狀態語言（finite state language）：巢狀與交叉依存結構（如 center-embedding）超出 FSM 的表達能力，FSM 因此被 NLP 界棄用。
- 但轉換生成語法（transformational grammar）雖理論優雅，其轉換規則（transformational rules）極難直接實作成高效的剖析程式。
- 有限狀態機的工程優點又很難放棄：實作簡單、控制流清楚、容易除錯——Woods 想在 FSM 上「加料」，使其具備 CFG 能力。
- BNS 的 LUNAR 專案（NASA 資助）需要讓不懂程式的地質學家直接用英語查詢月球樣本資料庫，這是一個具體的應用壓力。
- 當時的遞迴下降剖析器有左遞迴與回溯（backtracking）效率問題，Woods 想要一個控制更精細的方案。

## 線索與推理 -- 數學式、程式、理論

### 核心證據：ATN 的三種弧

ATN 的形式化：一個網路是 $(Q, \Sigma, \text{arcs}, q_0, F)$，其中弧（arc）有三類，語義各不相同：

- **Cat arc（詞類弧）**：從狀態 $q$ 到 $q'$，條件是下一個詞屬於詞類 $\text{Cat}$（如 NP、V）。掃描一個詞，推進輸入指標。
- **Push arc（推入弧）**：從 $q$ 到 $q'$，遞迴呼叫子網路 $\text{Net}$（如呼叫 NP 網路）；子網路成功返回後才推進。這是突破 FSM 限制的關鍵。
- **Pop arc（彈出弧）**：宣告子網路成功結束，把建構好的結構（存在暫存器裡）回傳給呼叫者。
- **Jump arc（跳躍弧）**：不消耗輸入、直接轉移狀態，用於可選成分（如省略冠詞）。

### 遞迴使 ATN 等價於 CFG

Push/Pop 的遞迴能力是破案的關鍵時刻：對任意 CFG $G$，可以構造一個 ATN $M_G$，使得

$$L(M_G) = L(G)$$

每個非終端符號 $A$ 對應一個子網路，每條產生規則 $A \rightarrow X_1 X_2 \cdots X_k$ 對應子網路中一條經過 $k$ 個 Cat/Push 弧的路徑。反之，任何 ATN 也可被 CFG 模擬（ATN 的辨識能力恰好落在 CFG 層級）。這個等價性證明，讓「被 Chomsky 否定的 FSM」以增強的形式重返戰場。

### 暫存器：從辨識到結構

純辨識只回答「是否合法」；ATN 的暫存器（registers）讓剖析過程順便建構語法樹與語義表示。每個 Push arc 成功後，把子網路 Pop 回傳的結構存入暫存器（如 `SUBJ`、`OBJ`），最後 Pop 時組裝成完整結構：

$$\text{POP}(\text{net}, \; \text{regs}[\text{SUBJ} \leftarrow s, \text{OBJ} \leftarrow o])$$

這也是 LUNAR 語義翻譯的基礎：暫存器裡填的不是語法樹節點，而是直接可查詢資料庫的邏輯式。

### LUNAR 系統：ATN 的實戰

LUNAR 的問答流程分三步：

1. **語法剖析**：ATN 把英語問題（如 "What is the average concentration of aluminum in high alkali rocks?"）解析成結構。
2. **語義翻譯**：將結構翻譯成資料庫查詢語言（一階邏輯式）。
3. **資料庫查詢**：對月球樣本資料庫執行查詢，回傳答案。

這是 1973 年最完整的「語言 → 語義 → 資料」管線，展示了 ATN 不只是剖析器，而是語義介面的骨架。

### 可執行程式：mini ATN

```python
# mini ATN: 狀態機 + 暫存器 + 遞迴子網路，解析 NP / VP
POS = {"Det": {"the"}, "N": {"dog", "cat", "food"}, "V": {"saw", "ate"}}

NETS = {  # 每個非終端一個子網路：弧 = (type, arg, from, to)
    "NP": [(("cat", "Det"), "q0", "q1"), (("cat", "N"), "q1", "q2"),
           (("pop", None),  "q2", "q2")],
    "VP": [(("cat", "V"), "q0", "q1"), (("push", "NP"), "q1", "q2"),
           (("pop", None),  "q2", "q2")],
    "S":  [(("push", "NP"), "q0", "q1"), (("push", "VP"), "q1", "q2"),
           (("pop", None),  "q2", "q2")],
}

def run_net(net_name, words, i):
    """遞迴執行子網路；回傳 (終態位置, 結構) 或 None"""
    arcs = NETS[net_name]
    def step(state, i, regs):
        if state == "q2" and net_name in ("NP", "VP", "S") and not arcs[-1][0][1]:
            pass
        for (targ, src, dst) in arcs:
            typ, arg = targ          # targ = (弧型, 詞類/子網路名)
            if src != state: continue
            if typ == "cat" and i < len(words) and words[i] in POS[arg]:
                r = step(dst, i + 1, regs + (words[i],))
                if r: return r
            elif typ == "push":                      # 遞迴呼叫子網路
                sub = run_net(arg, words, i)
                if sub:
                    j, substruct = sub
                    r = step(dst, j, regs + (substruct,))
                    if r: return r
            elif typ == "pop":                       # 彈出：組裝結構
                if net_name == "NP":  return (i, ("NP",) + regs)
                if net_name == "VP":  return (i, ("VP",) + regs)
                if net_name == "S":   return (i, ("S",) + regs)
        return None
    return step("q0", i, ())

print(run_net("S", "the dog saw the cat".split(), 0))
# (5, ('S', ('NP', 'the', 'dog'), ('VP', 'saw', ('NP', 'the', 'cat'))))
```

程式展示三種弧的語義：cat 掃詞、push 遞迴呼叫子網路、pop 回傳暫存器中組裝好的結構——正是 Woods 1970 年的設計核心。

## 結案 -- 後果與影響

- ATN 成為 1970-1980 年代 NLP 的主流剖析框架：LIFER（1977, BBN）、語義文法系統（semantic grammar systems）皆以 ATN 或其變體為基礎。
- LUNAR 證明「自然語言資料庫介面」可行，啟發了整個 1980 年代的介面研究傳統。
- 遞迴狀態機的思想影響後來的 chart parsing 與有限狀態轉移器（FST）在形態學的應用——FSM 家族在 NLP 的多個層次復活。
- ATN 的缺陷同樣是判決書：規則全靠手工編寫、規則之間互相干擾、每擴充一個領域都是維護噩夢——「知識獲取瓶頸」的直接證據，促成 1990 年代統計剖析法（PCFG、HMM）抬頭。
- Woods 的等價性證明留下持久的理論遺產：表達能力與工程可控性可以兼得，只要在正確的層級上加料。

## 關鍵人物與文獻（條例）

- William A. Woods (1970). "Transition Network Grammars for Natural Language Analysis." *Communications of the ACM*, 13(10), 591-606.
- William A. Woods (1973). "Progress in Natural Language Understanding: An Application to Lunar Geology." AFIPS Conference Proceedings, 42, 441-450.（LUNAR 系統）
- Noam Chomsky (1956). "Three Models for the Description of Language." *IRE Transactions on Information Theory*, 2(3), 113-124.（證明有限狀態語言不足以描述英語）
- Gary G. Hendrix et al. (1978). "Developing a Natural Language Interface to Complex Data." *ACM Transactions on Database Systems*, 3(2), 105-147.（LIFER 與語義文法的後繼）
- Ronald Kaplan (1970s). ATN 實作與擴展的重要貢獻者，後來發展詞彙功能文法（LFG）。
