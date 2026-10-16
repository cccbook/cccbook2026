# 1936–1956 - Kleene 定理與正則語言

## 案件摘要
1943 年 McCulloch–Pitts 提出神經網路邏輯模型，1951 年 Kleene 在 RAND 報告中證明「正則事件」恰為有限狀態機可辨識的語言——即**Kleene 定理**。本案追查正則表示式、有限自動機與 Chomsky 文法階層如何在此匯流。

## 前因 -- 為什麼會有這個案子
- 1943 年 McCulloch–Pitts 用「神經元 = 邏輯閘」建模腦部活動，其中「事件」由有限個神經元的激發歷史描述。
- 1951 年 Kleene 受 RAND 委託研究該模型，發現可描述的事件類具有優美的代數結構：正則表示式。
- 1956 年 Chomsky 提出文法階層，發現「正則語言」正是最受限的 Type 3——Kleene 定理於是成為形式語言理論的第一塊基石。

## 線索與推理 -- 數學式、程式、理論

### 1. 有限狀態機（FSM/DFA）的定義
決定性有限自動機（DFA）是五元組：
$$
M = (Q,\ \Sigma,\ \delta,\ q_0,\ F)
$$
- $Q$：有限狀態集；$\Sigma$：輸入字母表；$\delta: Q \times \Sigma \to Q$：轉移函數
- $q_0 \in Q$：起始狀態；$F \subseteq Q$：接受狀態集

接受語言：$L(M) = \{ w \in \Sigma^* \mid \hat\delta(q_0, w) \in F \}$，其中 $\hat\delta$ 是 $\delta$ 的擴充（$\hat\delta(q, \epsilon) = q$，$\hat\delta(q, wa) = \delta(\hat\delta(q,w), a)$）。

**非決定性自動機（NFA）**：$\delta: Q \times \Sigma_\epsilon \to 2^Q$，一個輸入可有多個（含 $\epsilon$）後繼，只要**存在**一條接受路徑即接受。

### 2. DFA vs NFA 等價性：子集構造
對 NFA $N = (Q, \Sigma, \delta, q_0, F)$，構造 DFA $D$：
$$
D = (2^Q,\ \Sigma,\ \delta',\ \{q_0\},\ F')
$$
- $\delta'(S, a) = \bigcup_{q \in S} \delta(q, a)$（狀態集整體推移）
- $F' = \{ S \subseteq Q \mid S \cap F \neq \emptyset \}$

**定理**：$L(D) = L(N)$。子集數最壞 $2^n$ 個（指數爆炸），但實務上常遠小於此；不可達子集可再剪除。

### 3. Kleene 定理：正則語言 = FSM 可辨識
正則表示式文法：
$$
R ::= \emptyset \mid \epsilon \mid a \;(a \in \Sigma) \mid R_1 R_2 \mid R_1 \mid R_2 \mid R^*
$$

**Kleene 定理（1951/1956）**：
$$
L \text{ 是正則表示式定義的語言} \iff L \text{ 被某個有限自動機辨識}
$$

兩個方向：
- **(⇒) 表示式 → 自動機**：對 $\emptyset, \epsilon, a$ 給基本自動機；串接用串聯（$R_1$ 的接受態 →$R_2$ 起始態）、聯集用並聯、星號用迴路（Thompson 構造，1968）。
- **(⇐) 自動機 → 表示式**：狀態消去法（state elimination）或動態規劃：
$$
R_{ij}^{(k)} = R_{ij}^{(k-1)} \;\big|\; R_{ik}^{(k-1)} \left( R_{kk}^{(k-1)} \right)^* R_{kj}^{(k-1)}
$$
（$R_{ij}^{(k)}$：從 $i$ 到 $j$ 只經過中間狀態 $\le k$ 的路徑表示式。）

### 4. 封閉性與泵引理
正則語言在聯集、串接、星號、補、交集下封閉：
$$
L, M \text{ 正則} \Rightarrow L \cup M,\ LM,\ L^*,\ \bar{L},\ L \cap M \text{ 皆正則}
$$
（補靠 DFA 完備性直接翻轉 $F$；交集由 De Morgan：$L \cap M = \overline{\bar L \cup \bar M}$。）

**泵引理（pumping lemma）**：若 $L$ 正則，則存在 $p \ge 1$，使任意 $w \in L$、$|w| \ge p$ 可寫成 $w = xyz$，滿足：
$$
|xy| \le p,\quad |y| \ge 1,\quad \forall i \ge 0:\ xy^i z \in L
$$
（DFA 走過 $p$ 步必重複狀態，迴圈 $y$ 可任意泵。）用以證明 $\{a^n b^n\}$、$\{a^{2^n}\}$ 等語言**非正則**。

### 5. Python：DFA 模擬器與 NFA→DFA 子集構造

```python
# ---- DFA 模擬器 ----
def run_dfa(dfa, w):
    """dfa = {state: {symbol: next}}, start, accepts"""
    states, start, accepts = dfa
    q = start
    for ch in w:
        q = states[q].get(ch)
        if q is None:
            return False
    return q in accepts

# DFA：辨識 (a|b)* 中含 'ab' 的字串
dfa_states = {0: {'a': 1, 'b': 0}, 1: {'a': 1, 'b': 2}, 2: {'a': 2, 'b': 2}}
print(run_dfa((dfa_states, 0, {2}), 'aabba'))   # True
print(run_dfa((dfa_states, 0, {2}), 'baa'))     # False

# ---- NFA（含 ε）與子集構造 ----
def epsilon_closure(nfa_states, S):
    stack, out = list(S), set(S)
    while stack:
        q = stack.pop()
        for p in nfa_states[q].get('', ()):   # '' = ε 轉移
            if p not in out:
                out.add(p); stack.append(p)
    return frozenset(out)

def nfa_to_dfa(nfa_states, start, accepts, alphabet):
    init = epsilon_closure(nfa_states, {start})
    dfa, todo = {}, [init]
    seen = {init}
    while todo:
        S = todo.pop()
        dfa[S] = {}
        for a in alphabet:
            T = epsilon_closure(nfa_states,
                    {t for q in S for t in nfa_states[q].get(a, ())})
            dfa[S][a] = T
            if T and T not in seen:
                seen.add(T); todo.append(T)
    dfa_accepts = {S for S in dfa if S & set(accepts)}
    return (dfa, init, dfa_accepts)

# NFA：辨識以 'ab' 結尾的字串（ε 鏈 + 不確定跳躍）
nfa = {0: {'a': {0, 1}, 'b': {0}},        # 迴圈讀任意
       1: {'b': {2}},                     # 讀到 a 後期待 b
       2: {}}                             # 接受
d = nfa_to_dfa(nfa, 0, {2}, 'ab')
print(len(d[0]), "個 DFA 狀態（含起始）")  # 子集構造結果
print(run_dfa(d, 'aabab'))               # True（以 ab 結尾）
print(run_dfa(d, 'aabba'))               # False
```

## 結案 -- 後果與影響
- Kleene 定理連通了三個世界：神經網路邏輯（McCulloch–Pitts）、文法（Chomsky Type 3）、正則表示式——後兩者成為電腦科學的核心工具。
- 正則表示式經 Thompson (1968)、Kleene 的 Unix 工具（grep, 1973）落地，成為編譯器詞法分析、文字搜尋的日常技術。
- DFA ⊆ NFA = 正則 ⊂ CFG ⊂ 無限制文法的階層圖譜，是計算複雜度與形式驗證（模型檢驗用自動機）的起點。

## 關鍵人物與文獻
- **Stephen Kleene**（1909–1994）：RAND 報告與正則事件理論。
- **Warren McCulloch & Walter Pitts** (1943)：神經邏輯模型。
- **Noam Chomsky** (1956, 1959)：文法階層，確立正則語言地位。
- Kleene, S. C. (1951). *Representation of Events in Nerve Nets and Finite Automata.* RAND Memorandum RM-704；修訂版刊於 *Automata Studies* (1956).
- Thompson, K. (1968). "Regular expression search algorithm." *CACM* 11(6):419–422.
