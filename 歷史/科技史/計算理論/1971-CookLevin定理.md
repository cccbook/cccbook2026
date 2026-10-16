# 1971 - Cook–Levin 定理：SAT 是 NP-complete

## 案件摘要
1971 年，Stephen Cook 在 STOC 發表〈The Complexity of Theorem-Proving Procedures〉，證明 SAT 是 NP-complete；幾乎同時，蘇聯的 Leonid Levin 獨立證明了等價結果。證明的核心是把圖靈機的計算歷程編碼成一個 CNF 公式（tableau 構造）。從此，解決 SAT 一個問題，就等於解決全部 NP 問題。

## 前因 -- 為什麼會有這個案子
到 1971 年，證據鏈已齊備：

- **Cobham–Edmonds (1965)**：多項式時間 = good algorithm，$\text{P}$ 是易處理類；
- **Hartmanis–Stearns (1965)**：複雜度類有真包含，歸約與完備性概念存在；
- **Cook (1967 報告)**：SAT 的驗證只需多項式，NP 類與 NP-complete 概念已成型；
- 命題邏輯 SAT 的「窮舉需 $2^n$、驗證只需 $O(n)$」的不對稱始終無法解釋。

核心案件問題：

> **是否存在一個 NP 問題，是所有 NP 問題的「共同瓶頸」？** Cook 的答案是：SAT。而且證明方法是偵探式的——把「計算」本身翻譯成「邏輯」。

## 線索與推理 -- 數學式、程式、理論

### 線索一：Cook–Levin 定理的陳述
**定理（Cook 1971；Levin 1973）**：

$$\text{SAT is NP-complete}$$

即：(1) $\text{SAT} \in \text{NP}$；(2) 對任意 $L \in \text{NP}$，有 $L \leq_p \text{SAT}$。

### 線索二：證明核心——tableau 構造
設 $L \in \text{NP}$，由驗證者觀點存在 NTM $M$ 在 $p(n)$ 步內判定 $L$。對輸入 $x$，構造 CNF 公式 $\varphi_x$，其可滿足 $\iff M$ 接受 $x$。

**Tableau 構造**：做一張 $(p(n)+1) \times p(n)$ 的表格，第 $t$ 列記錄 $M$ 在第 $t$ 步的**完整格局**（帶內容、狀態、讀寫頭位置）：

$$\begin{array}{|c|c|c|c|c|}
\hline
q_0 & x_1 & x_2 & \cdots & x_n \\
\hline
x_1 & q_1 & x_2 & \cdots & x_n \\
\hline
\multicolumn{5}{|c|}{\vdots} \\
\hline
\multicolumn{5}{|c|}{\text{接受格局（含 } q_{\text{acc}}\text{）}} \\
\hline
\end{array}$$

引入布爾變元 $C_{i,j,s} = $「第 $t=i$ 步、帶格 $j$ 的符號/狀態是 $s$」。用四組子句編碼：

1. **初始條件**：$\bigwedge_j C_{1,j,x_j} \wedge C_{1,1,q_0}$（第一列就是輸入 $x$ 加初始狀態）；
2. **接受條件**：$\bigvee_{i,j} C_{i,j,q_{\text{acc}}}$（某處出現接受狀態）；
3. **合法性（每格恰一符號）**：$\bigwedge_{i,j} \Big(\bigvee_s C_{i,j,s} \wedge \bigwedge_{s \neq s'} \neg(C_{i,j,s} \wedge C_{i,j,s'})\Big)$；
4. **轉移合法性（每個 $2\times3$ 窗口合法）**：對每個窗口，若它不能是合法格局演化的局部影像，就禁止它：

$$\bigwedge_{i,j} \neg\!\left(\text{不合法的窗口 }(i,j)\right)$$

局部性是關鍵：圖靈機每步只改變讀寫頭附近一格，所以「第 $t+1$ 列是否合法」只取決於第 $t$ 列的 $2\times3$ 局部窗口——**這使編碼規模只有多項式**。

**結論**：$\varphi_x$ 有 $O(p(n)^2)$ 個變元與子句，可在多項式時間內從 $x$ 構造；且 $M$ 接受 $x \iff \varphi_x$ 可滿足。$\blacksquare$

### 線索三：歸約 $L \leq_p \text{SAT}$
上述構造本身就是歸約函數 $f$：

$$f(x) = \varphi_x, \qquad x \in L \iff f(x) \in \text{SAT}$$

$f$ 的可計算性：構造 $\varphi_x$ 只是循環生成子句，時間 $O(p(n)^2)$ 是多項式。因此任何 $L \in \text{NP}$ 都歸約到 SAT，SAT 是 NP-hard；又 SAT 自己可被 NTM 快速判定（猜賦值再驗證），故 SAT $\in$ NP。合起來即 NP-complete。

### 線索四：Python 構造小型 tableau 範例
構造一個迷你 NTM 的 tableau 子句（概念示範，時間軸 2 步、帶長 3 格）：

```python
def tableau_clauses(symbols, states, init, T=2, n=3):
    """生成 tableau 的 CNF 子句（省略全部窗口檢查，示範結構）"""
    clauses = []
    C = lambda i, j, s: (i, j, s)   # 變元「第 i 步格 j 為 s」

    # 1. 初始條件：第 0 步 = 輸入 + 初始狀態
    for j, s in enumerate(init):
        clauses.append([C(0, j, s)])

    # 3. 每格恰一符號（簡化：至少一符號）
    for i in range(T):
        for j in range(n):
            clauses.append([C(i, j, s) for s in symbols])

    # 4. 窗口禁止：相鄰兩步的變化必須是某個轉移的影像
    for i in range(T - 1):
        for j in range(n):
            for a in states:          # (舊狀態, 新狀態) 不在轉移表 → 禁止
                for b in states:
                    if (a, b) not in transitions:
                        clauses.append([-C(i, j, a), -C(i+1, j, b)])
    return clauses

symbols = ['0', '1', '#']
states  = ['q0', 'qacc']
transitions = {('q0', 'qacc'), ('qacc', 'qacc')}   # 迷你轉移表
init = ['q0', '1', '#']
clauses = tableau_clauses(symbols, states, init)
print(len(clauses), "clauses")   # 多項式個子句
# 若存在使全部子句為真的賦值 = 機器沿 tableau 走到接受
```

真實證明需完整窗口條件（保證整列由上一列合法演化而來），原理相同。

### 線索五：NP-complete 的意義——一個問題解決全部解決
若 SAT 有多項式演算法 $A$，則對任意 $L \in \text{NP}$：

$$x \xrightarrow{\ f\ \text{(poly)}\ } \varphi_x \xrightarrow{\ A\ \text{(poly)}\ } \text{答案}$$

總時間 $O(p(n)^2) + O(q(n))$ 仍為多項式，故 $\text{NP} = \text{P}$。反之若 $\text{P} \neq \text{NP}$，則 SAT 無多項式演算法。**SAT 成為整個 NP 類的單點故障。**

## 結案 -- 後果與影響
1. **第一個 NP-complete 問題誕生**，從此證明 NP-complete 只需「$\text{SAT} \leq_p X$」一步（Karp 1971 立即示範了 21 個）。
2. $\text{P}$ vs $\text{NP}$ 問題被精確聚焦：成為千禧年七大數學難題之一（Clay 獎百萬美元）。
3. Levin 的獨立發現（universal sequential search problem）顯示概念是時代必然；兩人合稱 Cook–Levin 定理。
4. **tableau 構造**成為歸約技術的範本：之後所有 NP-complete 證明都是它的變奏（局部檢查 + 多項式編碼）。
5. 衍生領域：SAT 求解器（DPLL、CDCL）成為工業工具，驗證晶片與軟體；PCP 定理把 tableau 思想推到極致。
6. Cook 獲 1982 年圖靈獎。

## 關鍵人物與文獻
- **Stephen Cook**：〈The Complexity of Theorem-Proving Procedures〉, *Proc. 3rd STOC*, 1971, pp. 151–158.
- **Leonid Levin**：〈Universal sequential search problems〉, *Problems of Information Transmission* 9(3), 1973（蘇聯獨立發現，1975 年英譯）。
- 前驅：Cook (1967 報告)、Edmonds (1965)、Hartmanis–Stearns (1965)。
- 後續：Karp (1971) 21 問題；Sipser 教科書 §7.4 的 tableau 證明；CDCL SAT 求解器（Marques-Silva & Sakallah 1996）。
