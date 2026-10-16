# 1966-RothD演算法

## 案件摘要
電路越來越大，出錯的機率越來越高，但「怎樣自動找出能抓到故障的測試向量」長期靠運氣。1966 年，IBM 的 J. Paul Roth 發表 D 演算法（D-Algorithm）：用一個符號「D」同時編碼「正常電路是 1、故障電路是 0」，把測試生成從枚舉所有輸入向量，變成在電路網路上做系統的符號傳播。這是 ATPG（自動測試圖樣產生）的第一個完整演算法，也是此後五十年測試演算法族（PODEM、FAN、SAT-based ATPG）的開山卷宗。

## 前因 -- 為什麼會有這個案子
- **故障是常態**：製程缺陷讓電晶體卡在 0（stuck-at-0）或卡在 1；一顆晶片數千閘，不可能人工想測試。
- **暴力枚舉不可行**：$n$ 輸入電路有 $2^n$ 個向量，$n=30$ 就超過十億——必須有目標導向的搜尋。
- **IBM 的量產壓力**：System/360 時代，IBM 需要對出廠的每一顆模組做測試，測試成本直逼製造成本。
- **理論工具就緒**：McCluskey 的開關理論（1956-62）已定義故障模型與可測性概念，缺一個可執行的演算法。

## 線索與推理 -- 數學式、程式、理論

### 線索一：D 立方的符號代數
Roth 的洞察：擴充布林值的字母表為 $\{0, 1, D, \bar{D}\}$，其中：

$$D = (1 \text{ in good circuit},\ 0 \text{ in faulty circuit}), \quad \bar{D} = (0,\ 1)$$

一個測試向量必須完成兩件事，D 演算法把它們變成兩個機械步驟：

1. **故障致活（fault activation）**：在故障點輸入使其顯現 D（如 stuck-at-0 的線要輸入 1）；
2. **D 驅動（D-drive）與一致性（consistency）**：把 D 沿某條路徑傳播到輸出（使故障「可觀察」），同時反向指定內部節點值使電路自洽。

D 立方（D-cube）是每個閘的「傳播規則表」，例如 AND 閘的 D 傳播：

| 輸入 A | 輸入 B | 輸出 |
|--------|--------|------|
| D | 1 | D |
| D | 0 | 0（被阻塞）|
| 1 | D | D |

### 線索二：搜尋即回溯
D 演算法 = 在「故障點選擇 × 傳播路徑 × 內部賦值」的決策樹上做深度優先回溯。形式上，測試存在 $\iff$ 存在賦值使故障點為 D 且某輸出為 D/$\bar{D}$：

$$\exists v \in \{0,1\}^n:\ f_{\text{good}}(v) \ne f_{\text{faulty}}(v)$$

這其實是一個**可滿足性問題**——半世紀後（1992, Larrabee；2000s, SAT-based ATPG）人們發現它就是 SAT，繞了一圈回到 Roth 的原點。

### 後繼者的改良譜系
| 演算法 | 年份 | 改良 |
|--------|------|------|
| D 演算法 | 1966 | 首個系統化 ATPG，符號傳播 |
| PODEM | 1981 (Goel) | 只在**原始輸入**上回溯，內部值用蘊含推出，搜尋空間縮小 |
| FAN | 1983 (Fujiwara-Shimono) | 回溯停止在「頭線」（head lines），學習衝突 |
| SOCRI/FAST | 1980s | 並行模擬加速 |
| SAT-based | 1992– (Larrabee) | ATPG = CNF-SAT，用 CDCL 求解 |

## 結案 -- 後果與影響
- **測試從藝術變工程**：D 演算法證明測試生成可全自動化，IBM 內部工具（如 ELSTP）量產化，撐起 System/360 世代的品質。
- **可測性設計的源頭**：演算法難以傳播 D 的電路「天生難測」，促成 scan chain（把時序電路變組合電路）等 DFT 設計規範——演算法反過來塑造了電路設計。
- **故障模型的標準化**：stuck-at 模型 + D 演算法成為教科書標準，延伸出橋接故障、延遲故障、path delay ATPG。
- **SAT 的宿命伏線**：D 演算法本質是 SAT 的符號解法；五十年後 SAT-based ATPG 與 scan、BIST 一起成為 DFT 流程心臟。

## 關鍵人物與文獻
- **J. Paul Roth**（1926–2020）：IBM Watson，D 演算法與代數拓撲研究。
- 文獻：
  - J. P. Roth, "Diagnosis of Automata Failures: A Calculus and a Method," *IBM J. Res. Dev.* 10, 278 (1966).
  - P. Goel, "An Implicit Enumeration Algorithm to Generate Tests for Combinational Logic Circuits," *IEEE TC* C-30, 215 (1981)（PODEM）。
  - H. Fujiwara, T. Shimono, "On the Acceleration of Test Generation Algorithms," *IEEE TC* C-32, 1137 (1983)（FAN）。
