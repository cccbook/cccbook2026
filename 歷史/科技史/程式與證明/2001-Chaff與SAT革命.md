# 2001 Chaff 與 SAT 革命：百萬變元的閃電審判

> 案件編號：2001-CHAFF。報案人：EDA 與驗證工程師。案情：SAT 是 NP 完全，實例卻大到百萬變元。破案者：Moskewicz、Madigan、Zhang、Malik。

## 案發現場

SAT（命題可滿足性）是計算理論的頭號重犯：NP 完全，理論上難解。但 1990 年代末，晶片驗證、有界模型檢查（BMC）、規劃問題全都歸約到 SAT。實例規模從數百變元暴漲到數十萬，舊求解器紛紛窒息。

當時的 DPLL 求解器（如 GRASP、SATO）已有回溯搜尋、單元傳播、純文字消除，但有三個致命傷：學到的子句保留太少、回溯總是按時間順序、分支啟發式盲目。解一個工業實例要數小時甚至超時，BMC 產生的公式根本解不動。

2001 年，普林斯頓的 Moskewicz、Madigan、Zhang、Malik 推出 Chaff，一篇 DAC 論文震動 EDA 界：同樣的機器，Chaff 比前人快一到兩個數量級。SAT 從學術玩具變成工業引擎。

## 偵查過程（含數學式/表格/理論）

### 線索一：CDCL 的三件兇器

Chaff 的核心是 CDCL（Conflict-Driven Clause Learning，衝突驅動子句學習）。它把 DPLL 的「搜尋＋傳播」升級為「搜尋＋傳播＋學習＋聰明回溯」。

設部分賦值為 $\sigma$ ，子句集為 $F$ 。單元傳播記為 $UP(F, \sigma)$ 。當傳播遇到衝突，分析蘊含圖（implication graph），學到新子句 $C_{learn}$ ：

$$
F := F \cup \{ C_{learn} \}
$$

$$
\sigma := Backtrack(F, \sigma, level)
$$

三件兇器分解：

1. 衝突學習（clause learning）：從衝突切出 UIP（Unique Implication Point）子句，防止重蹈覆轍。
2. 非時序回溯（non-chronological backtrack）：直接跳回與衝突相關的決策層，而非一層層退。設衝突層為 $l_c$ ，回跳層為 $l_b$ ，常有 $l_b \ll l_c - 1$ 。
3. VSIDS（Variable State Independent Decaying Sum）：給每個變數計分，參與衝突就加分，定期衰減。分支選最高分者，聚焦「最近最吵」的變數。

表格：DPLL 與 CDCL 對比。

| 機制 | DPLL（1962） | CDCL/Chaff（2001） |
|---|---|---|
| 傳播 | 單元傳播 $UP$ | 高效兩文字監控 |
| 衝突處理 | 時序回溯 | 學習 $C_{learn}$ ＋跳躍回溯 |
| 分支啟發式 | 靜態/隨機 | VSIDS 動態評分 |
| 重啟 | 無 | 頻繁重啟保多樣性 |

### 線索二：工程即理論——兩文字監控

Chaff 的另一半功勞是工程。每個子句只監控兩個文字（two-literal watch），賦值時不必掃全部子句；回溯時不需還原監控指標。這讓單元傳播快上數倍，而傳播佔求解時間八成以上。

偵查筆記：CDCL 的完全性來自歸結（resolution）。學到的每個 $C_{learn}$ 都是原公式的歸結後承，故 $F \models C_{learn}$ 。求解器一邊搜尋，一邊構造歸結證明；答 UNSAT 時，學習軌跡即不可滿足證明。

規模對照：

| 年代 | 求解器 | 可解變元數 |
|---|---|---|
| 1992 | Davis–Putnam 系 | 約 $10^2$ |
| 1996 | GRASP | 約 $10^3$ |
| 2001 | Chaff | $10^5$ 以上 |
| 2003 | MiniSAT | 百萬級 BMC 實例 |

### 線索三：MiniSAT 2003 與 SAT Competition

Chaff 之後，Eén 與 Sörensson 在 2003 年推出 MiniSAT：僅數千行、開源、模組化，成為所有新點子的實驗床。SAT competition 更把競賽變成軍備賽：每年工業、手工、隨機三組，優勝啟發式迅速被全行吸收。

CDCL 從此成為標準答案，BMC、符號執行、SMT 求解器全部站在它肩上。SAT 由「難題」變成「引擎」。

## 結案報告

案件告破。Chaff 證明：NP 完全不代表實務無解。衝突學習記住教訓，非時序回溯跳過無辜決策，VSIDS 追蹤熱點，三者合力把百萬變元實例變成秒級任務。

遺產有三：

1. EDA 等價檢查、時序 BMC 全面 SAT 化，BDD 的部分江山被 SAT 奪走。
2. MiniSAT 開源生態催生 Glucose、CryptoMiniSat 等名器，影響延續至今。
3. 直接餵養 2008 Z3 與 SMT 革命：DPLL(T) 的 SAT 核心幾乎都是 CDCL 後代。

從因果鏈看，Chaff 上承 1960 Davis–Putnam、1962 DPLL、1963 歸結原理，下啟 SMT、軟體驗證與 AI 規劃求解。

## 證據與工具

證據 A：CDCL 主迴圈虛擬碼。

```
loop:
    conflict := UnitPropagate(F, sigma)
    if conflict != None:
        if level == 0: return UNSAT
        C_learn, blevel := Analyze(conflict)
        F := F ∪ {C_learn}
        Backtrack(blevel)
    else:
        if all assigned: return SAT(sigma)
        v := PickVSIDS()
        Decide(v)
```

證據 B：VSIDS 更新。變數 $v$ 初始分 $score(v) = 0$ ，每次參與衝突分析則 $score(v) := score(v) + inc$ ，每輪 $inc := inc / decay$ ， $decay$ 如 $0.95$ 。分支選 $argmax \, score$ 。

證據 C：UIP 學習示例。若衝突圖在決策層僅剩單一 UIP 節點 $u$ ，學到子句為否定該層至 $u$ 的前因切割，對應公式 $\neg l_1 \lor \neg l_2 \lor u$ 形式。

證據 D：延伸閱讀。Moskewicz 等 2001 年〈Chaff: Engineering an Efficient SAT Solver〉；Eén 與 Sörensson 2003 年 MiniSAT 報告；SAT competition歷年基準與 Biere 等《Handbook of Satisfiability》。
