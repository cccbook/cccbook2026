# 2001-Chaff與SAT革命

## 案件摘要
SAT（布爾可滿足性）是 NP-完全的鼻祖（Cook, 1971），三十年來被認為「實務上無解」——直到 1996-2001 的 CDCL（衝突驅動子句學習）革命。1996 年 Marques-Silva 與 Sakallah 的 GRASP 引入衝突學習，2001 年普林斯頓的 Moskewicz 等人發表 **Chaff**：VSIDS 決策啟發 + 兩字面監看（two-watched literals），讓 SAT 求解器在工業級實例上快數個數量級。SAT 從理論噩夢變成 EDA 萬用引擎：等價檢查、ATPG、BMC、時序分析——昔日要專用演算法的案件，如今都化約成 SAT 交給 CDCL。這是「表示法 + 求解器」的典範轉移，也是 Chaff 之後 SAT/CSP 社群二十年軍備競賽的起跑線。

## 前因 -- 為什麼會有這個案子
- **SAT 的理論陰影**：NP-完全（Cook-Levin, 1971）——「最壞情形指數」的標籤讓工業界卻步三十年。
- **EDA 的重複投資**：等價檢查用 BDD、ATPG 用 D 演算法/PODEM、BMC 用 BDD——每個案件各造專用引擎，維護成本高。
- **DPLL 的舊引擎**（1962）：Davis-Putnam-Logemann-Loveland 的回溯搜尋已存在，但決策與學習策略原始——實務太慢。
- **GRASP 的突破**（1996）：Marques-Silva-Sakallah 引入衝突分析與學習（從失敗中學子句）——CDCL 的概念已誕生，缺工程化。

## 線索與推理 -- 數學式、程式、理論

### 核心：DPLL 骨架 + 三大改良
CNF-SAT：$\bigwedge_i \bigvee_j \ell_{ij}$（子句的合取）。DPLL 骨架：選變數 → 賦值 → 單位傳播（unit propagation：單字面子句強制賦值）→ 衝突則回溯。CDCL 的三大改良：

1. **衝突學習（conflict learning）**：衝突發生時，分析衝突的原因（蘊含圖的割），學出新子句加入公式——回溯不再盲目，直接跳到衝突根源：

$$\text{learn } C_{\text{new}} = \neg(\text{衝突的原因組合})$$

2. **非時序回溯（non-chronological backtracking）**：回溯到衝突根源的決策層，而非上一層；
3. **VSIDS（Variable State Independent Decaying Sum）**：衝突涉及的變數加權、定期衰減——決策偏好「常打架」的變數。

### 兩字面監看：單位傳播的工程革命
舊法：每次賦值掃描**所有**含該變數的子句（$O(\text{出現次數})$）。Chaff 的招式：每個子句只**監看兩個字面**；賦值時只檢查監看字面是否被賦假——只有兩個監看都被打掉（其中一個需重設）才動。效果：絕大多數賦值的傳播成本 $O(1)$ 級——單位傳播從主要瓶頸變成近乎免費。

```python
def unit_propagate_watch(assign, watched, clauses):
    """兩字面監看的單位傳播示意。"""
    queue = [v for v in assign if assign[v] is not None]
    while queue:
        v = queue.pop()
        for c in clauses_of(watched, v):      # 只查監看 v 的子句
            unassigned = [l for l in c if assign.get(abs(l)) is None]
            if len(unassigned) == 1:
                lit = unassigned[0]
                assign[abs(lit)] = (lit > 0)  # 強制賦值
                queue.append(abs(lit))
            elif not unassigned and not satisfied(c, assign):
                return "CONFLICT"             # 全假 → 衝突
    return assign
```

### 為什麼實務上快：重尾分布
工業級 SAT 實例的求解時間呈**重尾（heavy-tailed）分布**——隨機重啟（restarts）+ VSIDS 的組合，把長尾截斷。實務表現遠超最壞情形理論的預期，「NP-完全」的標籤在工程世界失效。

## 結案 -- 後果與影響
- **EDA 的萬用引擎**：等價檢查、ATPG、BMC、測試掃描、路由合法性——昔日專用演算法的案件大量化約成 SAT；EDA 演算法的「專用 vs 通用」天平傾向通用。
- **SAT 社群的軍備競賽**：MiniSat（2003，簡潔開源）、Glucose（2011）、CaDiCaL/Kissat（2020）——SAT 競賽（SAT Race/SAT Competition）讓求解器年年倍增，影響力擴散到密碼學、AI、運籌。
- **BMC 的燃料**：BMC（1999）+ Chaff（2001）的組合讓形式驗證在工業上全面可用——形式驗證的普及以此為起點。
- **ABC 的直接受益**：SAT sweeping（Mishchenko）用 CDCL 做等價合併——ABC（2005）的 AIG 與 SAT 合流，合成與驗證自此共引擎。

## 關鍵人物與文獻
- **Matthew Moskewicz, Conor Madigan, Ying Zhao, Lintao Zhang, Sharad Malik**：普林斯頓，Chaff 團隊。
- **João Marques-Silva, Karem Sakallah**：GRASP（1996），CDCL 概念先驅。
- 文獻：
  - M. W. Moskewicz, C. F. Madigan, Y. Zhao, L. Zhang, S. Malik, "Chaff: Engineering an Efficient SAT Solver," *DAC* 2001.
  - J. P. Marques-Silva, K. A. Sakallah, "GRASP: A Search Algorithm for Propositional Satisfiability," *IEEE Trans. Computers* 48, 506 (1999)（1996 會議版）。
  - M. Davis, G. Logemann, D. Loveland, "A Machine Program for Theorem-Proving," *Comm. ACM* 5, 394 (1962)（DPLL）。
