# 1956 - Dartmouth 會議（「人工智慧」的命名儀式）

## 案件摘要
1956 年夏天，John McCarthy 在達特茅斯學院組織了一場為期 8 週的研討會，並在提案書中首次創造術語：
**「人工智慧」(Artificial Intelligence)**。
與會者包括 Minsky、Shannon、Rochester、Newell、Simon、Samuel 等未來的巨匠。
會議本身的實質成果有限，但**這個命名把散落的線索集結成一門學科**——AI 偵探案在此正式開檔。

## 前因 -- 為什麼會有這個案子
- **散落的線索**：McCulloch–Pitts 神經元（1943，見「1943-McCullochPitts神經元.md」）、Turing 測試（1950，見「1950-Turing測試.md」）、Wiener 控制論 (1948)、Shannon 資訊論 (1948)、神經網路機（Rochester）、棋類程式（Shannon 1950、Samuel 1952）——人人都在研究「機器智能」，卻各自為政。
- **「控制論」的競爭**：Wiener 的 cybernetics 是當時的顯學，但 McCarthy 認為它聚焦回饋控制，偏離「智能」本題——**他需要一個新旗號**。
- **McCarthy 的偵探直覺**：與其各說各話，不如辦一場會議、立一個名目、發一份宣言，把「讓機器模擬智能」變成有編制的科學。
- **Rockefeller 基金會的資助**：McCarthy、Minsky、Shannon、Rochester 四人聯名提案，申請到 7,500 美元——學科的第一筆經費。

## 線索與推理 -- 數學式、程式、理論

### 提案書的宣言（案件開檔文書）
1955 年提案書寫道：
> 本研究的假設是：學習的每個面向，或智能的任何其他特徵，原則上都可以被**精確描述**，使得機器能夠模擬它。

這句話是整門學科的公設——**智能可以被形式化**。它繼承 Turing 的「行為測試」路線，並更進一步：不止測試，更要**建造**。

### 會議的實質成果：兩大範式的分岔
與會者實際帶來兩條路線，日後分岔為 AI 的兩大陣營：
1. **符號主義 (Symbolic AI)**：Newell 與 Simon 展示**邏輯理論家** (Logic Theorist, 1955)——第一個 AI 程式，用搜尋 + 邏輯證明《數學原理》的定理：
   $$\text{推理} = \text{狀態空間搜尋} + \text{形式邏輯}.$$
   它證明了 38 條定理，其中一條甚至比原書更優雅。
2. **聯結主義 (Connectionism)**：以神經元模型為本的路線（McCulloch–Pitts 為祖），1957 年 Rosenblatt 的感知器將發揚光大（見「1957-Perceptron感知器.md」）。

### 邏輯理論家的推理核心（啟發式搜尋）
證明定理 $P$ 的方法：從公理出發，反覆套用推理規則（代入、置換、演繹），在「證明狀態空間」中搜尋。
**啟發式** (heuristic) 是關鍵：不盲目窮舉，而是用「與目標的相似度」引導搜尋方向——
$$f(n) = g(n) + h(n),$$
這個框架日後成為 A\* 搜尋（1968）與整個符號 AI 的核心。

### Python：邏輯理論家式的簡易定理搜尋

```python
# 簡化示範：在狀態空間中搜尋「蘊涵傳遞」證明
axioms = [("p->q",), ("q->r",)]
def apply_rules(state):
    out = list(state)
    for i, (a,) in enumerate(state):
        for j, (b,) in enumerate(state):
            if a.endswith(b.split("->")[0] + "") and "->" in a and "->" in b:
                pre = a.split("->")[0]; mid = a.split("->")[1]
                if mid == b.split("->")[0]:
                    out.append((pre + "->" + b.split("->")[1],))
    return list(set(out))

state = list(axioms)
for step in range(5):
    new = apply_rules(state)
    if new == state: break
    state = new
print("推得:", state)
```
輸出：
```
推得: [('p->q',), ('p->r',), ('q->r',)]
```
（由 $p\to q$、$q\to r$ 推得 $p\to r$——邏輯理論家的推理縮影。）

## 結案 -- 後果與影響
- **學科正式誕生**：「人工智慧」成為正式術語；McCarthy 與 Minsky 分別在 Stanford 與 MIT 建立 AI 實驗室。
- **黃金年代（1956–1974）**：符號 AI 大放異彩——GPS 通用問題解決器 (1957)、LISP 語言 (1958)、Samuel 跳棋程式自我對弈學習 (1959)、ELIZA (1966)、A\* (1968)、Shakey 機器人 (1970)。
- **過度承諾的代價**：Newell 與 Simon 預言「20 年內機器能做任何人做的事」——承諾未兌現，1974–1980 與 1987–1993 兩度「AI 寒冬」降臨（資金與信心雙崩）。
- **聯結主義的寒冬**：1969 年 Minsky–Papert 的 XOR 批判（見「1969-MinskyPapert批判.md」）幾乎謀殺神經網路路線——諷刺的是，30 年後正是聯結主義復活並統治了整個學科。
- 歷史教訓：**命名創造了學科，但過度承諾幾乎毀滅了它**。

## 關鍵人物與文獻
- **J. McCarthy, M. L. Minsky, N. Rochester, C. E. Shannon**：達特茅斯提案書 (1955)。
- **A. Newell & H. Simon**：Logic Theorist (1955–56)；GPS (1957)。
- **J. McCarthy**：LISP 語言 (1958)。
- 相關案件：`1950-Turing測試.md`、`1957-Perceptron感知器.md`、`1969-MinskyPapert批判.md`。
