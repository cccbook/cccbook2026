# 1972 年 Prolog：把邏輯變成程式語言的推理探案

> 報案人：Alain Colmerauer（馬賽）與 Robert Kowalski（愛丁堡）。
> 涉案物：一條 Horn 子句。兇器：SLD 歸結＋合一演算法。

## 案發現場

1960 年代末，自然語言問答是 AI 的聖杯。Colmerauer 在馬賽研究法語問答系統，
想讓機器回答「保羅是誰的祖先？」這類問題。傳統程式要手寫搜尋流程，
每加一條親屬規則就多一堆迴圈，混亂不堪。

與此同時，在愛丁堡的 Kowalski 正盯著 Robinson 1965 年的歸結原理發呆。
歸結原理很美：只要一條推理規則就能證明一切一階邏輯後果。但它太暴力，
對任意子句集做飽和推理，搜尋空間爆炸，根本跑不動。

現場留下兩個謎團：

1. 能否把「知識」與「如何搜尋知識」分開？只寫邏輯，搜尋交給機器？
2. 能否把歸結限制在一個又弱又快、卻夠用的片段上？

1972 年，Colmerauer 的學生 Philippe Roussel 寫出第一個 Prolog 解譯器。
同一年 Kowalski 證明：對 Horn 子句而言，線性歸結加選擇函數是完備的。
理論與實作在同一年交會，Prolog 就此誕生。

## 偵查過程

### 線索一：Horn 子句——馴服的邏輯

偵探把目光鎖定在一種形狀特別乖的子句。Horn 子句只允許至多一個正文字，
寫成邏輯程式的樣子就是一條規則：

$$
A \leftarrow B_1, \dots, B_n
$$

讀作「若 $B_1$ 到 $B_n$ 皆成立，則 $A$ 成立」。當 $n = 0$ 時就是事實。
例如家族知識庫：

| Prolog 寫法 | 邏輯讀法 |
|---|---|
| `parent(tom, bob).` | $Parent(Tom, Bob)$ 為真 |
| `parent(bob, ann).` | $Parent(Bob, Ann)$ 為真 |
| `ancestor(X, Y) :- parent(X, Y).` | $Parent(X,Y) \to Ancestor(X,Y)$ |
| `ancestor(X, Z) :- parent(X, Y), ancestor(Y, Z).` | $Parent(X,Y) \land Ancestor(Y,Z) \to Ancestor(X,Z)$ |

為什麼選它？因為 Horn 子句集的可滿足性是 P-完全的，
而一般子句集是 NP-完全的。偵探用「犧牲表達力」換來「可執行的效率」。

### 線索二：SLD 歸結——一條線索追到底

Kowalski 的關鍵推理：對 Horn 子句不需要滿天撒網，
只要從目標（goal）出發做線性歸結即可。這就是 SLD（Linear resolution
with Selection function for Definite clauses）。

查詢 `?- ancestor(tom, ann).` 的 SLD 反駁過程如下：

1. 目標為 $\leftarrow Ancestor(Tom, Ann)$ 。
2. 與第二條祖先規則合一，得替代 $\{X/Tom, Z/Ann\}$ ，新目標為 $\leftarrow Parent(Tom, Y), Ancestor(Y, Ann)$ 。
3. 選最左文字 $Parent(Tom, Y)$ ，與事實 $Parent(Tom, Bob)$ 合一，得 $\{Y/Bob\}$ 。
4. 剩餘目標 $\leftarrow Ancestor(Bob, Ann)$ ，與第一條規則合一，
   再與 $Parent(Bob, Ann)$ 合一，得到空子句 $\Box$ ，證畢。

一般形式的 SLD 步驟可寫為：

$$
\frac{\leftarrow A_1, \dots, A_i, \dots, A_k \quad A \leftarrow B_1, \dots, B_n}{(\leftarrow A_1, \dots, A_{i-1}, B_1, \dots, B_n, A_{i+1}, \dots, A_k)\theta}
$$

其中 $\theta$ 是 $A_i$ 與 $A$ 的最一般合一者（mgu）。
每次只解一個子目標，堆疊起來就是深度優先搜尋。

### 線索三：合一＋深度優先——引擎的兩顆心臟

合一演算法回答「 $P(X, Bob)$ 與 $P(Tom, Y)$ 能否變成一樣？」
答案是 $\theta = \{X/Tom, Y/Bob\}$ 。Robinson 的合一演算法保證
能找到最一般的替代，否則回報失敗。

Prolog 引擎的執行策略可歸納為下表：

| 機制 | 內容 | 代價 |
|---|---|---|
| 選取規則 | 永遠選最左子目標 | 簡單但不完備 |
| 搜尋規則 | 深度優先＋按程式順序試規則 | 省記憶體但可能無窮迴圈 |
| 回溯 | 失敗即退回上一個選擇點，試下一條規則 | 自動，不需程式設計師操心 |
| 切割 `!` | 砍掉回溯點，人為修剪搜尋樹 | 高效但破壞宣告語意 |

偵探發現：Prolog 其實是不完備的定理證明器。
子句順序一換，程式可能從「秒答」變成「無窮迴圈」。
但正是這種「不完美的實用主義」，讓它跑得動。

## 結案報告

Prolog 破了案：程式不必寫「怎麼做」，只要寫「是什麼」，
剩下的搜尋交給 SLD 引擎。這就是 Kowalski 名言「 $Algorithm = Logic + Control$ 」
的現場示範。

它的遺產有三：

1. **邏輯程式典範**：Datalog、約束邏輯程式、Answer Set Programming 皆源於此。
2. **自動證明實用化**：把 Robinson 歸結從紙上理論變成可執行的語言。
3. **AI 與語言處理**：1980 年代日本第五代電腦計畫豪賭 Prolog，
   雖未奪冠，卻把合一、回溯、非決定性深植後世語言（如 Erlang、Mercury）。

## 證據與工具

- 核心公式：Horn 規則 $A \leftarrow B_1, \dots, B_n$ ，查詢 $\leftarrow G_1, \dots, G_k$ ，終點 $\Box$ ， $\theta$ 為最一般合一者。
- 祖先範例完整程式：

```prolog
parent(tom, bob).
parent(bob, ann).
ancestor(X, Y) :- parent(X, Y).
ancestor(X, Z) :- parent(X, Y), ancestor(Y, Z).
?- ancestor(tom, Who).
% Who = bob ; Who = ann
```

- 手動模擬搜尋樹：節點為目標串列，邊為規則與合一替代， $\Box$ 即回報答案。
- 延伸閱讀：Kowalski 1974 年〈Predicate Logic as Programming Language〉，
  Colmerauer 與 Roussel 1996 年回顧 Prolog 誕生史。
