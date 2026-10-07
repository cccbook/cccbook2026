# 1984-Espresso邏輯最小化

## 案件摘要
QM 演算法（1952-56）能化簡布林函數，但質蘊涵項枚舉在變數一多就爆炸（Sperner 定理給的 $O(2^n/\sqrt{n})$ 下界）。1984 年，UC Berkeley 的 Robert Brayton、Richard Rudell、Alberto Sangiovanni-Vincentelli 發表 **Espresso**：反轉策略——**根本不枚舉全部質蘊涵項**，改用「膨脹（expand）→ 不可約（irredundant）→ 縮減（reduce）」的迭代迴圈，每次只處理局部，得到一個接近最優的 cover。這是「啟發式為王」路線的經典勝利：Espresso 成為 PLA 與兩級邏輯化簡的業界標準，是 SIS（1986）與現代邏輯合成工具直系的祖先。

## 前因 -- 為什麼會有這個案子
- **QM 的組合爆炸**：枚舉質蘊涵項需 $O(2^n/\sqrt{n})$ 級；$n = 25$ 就崩——而實際電路動輒上百輸入。
- **PLA 的量產需求**：可程式邏輯陣列（PLA）的兩級 AND-OR 結構，面積正比於積項數——每省一個積項就是省一片矽。
- **最優不必、夠好即可**：涵蓋問題是 NP-hard（Karp 1971），精確解無望；工程需要的是「接近最優 + 可規模化」。
- **MINI 的先例**（IBM, 1974）：已有「迭代改進」式的化簡器，但實作粗略、速度慢——Berkeley 要把它做對。

## 線索與推理 -- 數學式、程式、理論

### 核心：cover 與三步迴圈
布林函數以**積項之和**（cover $C$）表示，每個積項是 cube（如 $x\bar{y}$）。Espresso 主迴圈：

1. **Expand（膨脹）**：把每個 cube 儘量膨脹成質蘊涵項（照顧到最大），並**吞掉**被它涵蓋的其他 cube（cover 變小）；
2. **Irredundant（去冗）**：刪掉刪了不影響函數的 cube（保留最小必要集）；
3. **Reduce（縮減）**：把 cube 縮小（騰出空間），讓下一輪 Expand 能換個方向膨脹——**逃出局部最優的關鍵**；
4. 若 cover 不再變小，停；否則回 1。

$$C \xrightarrow{\text{expand}} C' \xrightarrow{\text{irredundant}} C'' \xrightarrow{\text{reduce}} C''' \xrightarrow{\text{expand}} \cdots$$

### 為什麼有效：三步的互補推理
- **Expand 用了單立方距離（single-cube distance）**：兩 cube 只差一位即可合併（QM 的合併律，但局部使用）；
- **Reduce 是「繞路逃脫」**：Expand 收斂到的 cover 依賴處理順序；Reduce 縮小某些 cube 打破順序依賴，讓後續 Expand 換路徑——這是啟發式版的「退火式逃逸」，但用確定性方向而非隨機。

### 表示法：BDD 之前的王牌——cube 列表 + 位元運算
Espresso 用「字元三值編碼」$\{0, 1, -\}$（$-$ 表示該位被消去）表示 cube，合併、比較、包含檢查全是**位元運算**：

| cube A | cube B | 距離 | 可合併？ |
|--------|--------|------|---------|
| $10-$ | $11-$ | 1（第 2 位）| 是 → $1--$ |
| $10-$ | $01-$ | 2 | 否 |

**複雜度**：主迴圈 $O(\text{迭代數} \times |C| \times n)$——對輸入數 $n$ 與 cover 大小都是近線性，對比 QM 的指數枚舉。這是「捨棄全局枚舉、換取規模化」的典型交易。

### 效果
Espresso-II 對標準測例通常達到最優解的 1-5% 以內，速度比精確法（如 McBoole/ESPRESSO-EXACT）快幾個數量級——「夠好且夠快」正是工業的選擇。

## 結案 -- 後果與影響
- **業界標準二十年**：Espresso 成為 PLA/ROM 化簡的事實標準，被所有 EDA 廠商吸收；至今仍以 Espresso 引擎形式存在於開源工具。
- **多層合成的起跳板**：Espresso 處理「兩級」；Brayton 團隊隨即把思想推廣到多級（MIS 1986、SIS 1992），成為現代邏輯合成的母體。
- **「啟發式為王」的典範確立**：Espresso 證明在 NP-hard 世界裡，「接近最優 + 可規模化」擊敗「精確但指數」——這一推理成為整個 EDA 演算法設計的指導哲學。
- **Rudell 與 Synopsys**：Richard Rudell 後參與 Synopsys Design Compiler（1987-88），Espresso 的技術直接商品化，掀起 RTL 合成革命。

## 關鍵人物與文獻
- **Robert K. Brayton**：Berkeley 教授，邏輯合成理論宗師。
- **Alberto Sangiovanni-Vincentelli**：Berkeley 教授，SPICE、Espresso、Timberwolf 共同推手，EDA 產業顧問。
- **Richard L. Rudell**：Espresso 實作與 Exact 版，後為 Synopsys 核心工程師。
- 文獻：
  - R. K. Brayton, G. D. Hachtel, C. T. McMullen, A. L. Sangiovanni-Vincentelli, *Logic Minimization Algorithms for VLSI Synthesis* (Espresso-II), Kluwer, 1984.
  - R. L. Rudell, A. Sangiovanni-Vincentelli, "Multiple-Valued Minimization for PLA Optimization," *IEEE TCAD* 6, 727 (1987).
  - S. J. Hong, D. L. Ostapko, "MINI: A Heuristic Approach for Logic Minimization," *IBM J. Res. Dev.* 18, 443 (1974)（前身）。
