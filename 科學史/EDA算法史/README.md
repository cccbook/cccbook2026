# EDA算法史 -- AI 偵探風格

以「推理探案」的方式，追查電子設計自動化（EDA, Electronic Design Automation）演算法從 1937 年 Shannon 開關理論，到 AlphaChip 強化學習與 LLM 設計代理的每一步：
前因是什麼？線索在哪裡？推理如何展開？後果又如何改變了整個矽文明？

（涵蓋：邏輯合成、電路模擬、分區、佈局、繞線、時序分析、形式驗證、物理驗證、AI 輔助設計——以演算法本身為主角）

## 案件卷宗（歷史年表）

### 史前與奠基：布林代數進入機器（1937–1960）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1937 | Shannon 碩士論文——布林代數與開關電路同構，數位設計的數學地基 | [1937-Shannon開關理論.md](1937-Shannon開關理論.md) |
| 1952 | Quine-McCluskey 表格法——第一個可程式化的邏輯化簡演算法 | [1952-QuineMcCluskey最小化.md](1952-QuineMcCluskey最小化.md) |
| 1957 | IBM「設計自動化」——主機時代的自動接線表與佈線 | [1957-IBM設計自動化.md](1957-IBM設計自動化.md) |

### 迷宮時代：實體設計演算法誕生（1961–1971）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1961 | C. Y. Lee 迷宮繞線——BFS 波前搜尋保證最短路徑 | [1961-Lee迷宮繞線.md](1961-Lee迷宮繞線.md) |
| 1964 | 第一屆 DAC——學界與業界的設計自動化交叉點 | [1964-DAC設計自動化會議.md](1964-DAC設計自動化會議.md) |
| 1966 | Hanan 網格定理——直角 Steiner 樹的結構性突破 | [1966-Hanan網格Steiner樹.md](1966-Hanan網格Steiner樹.md) |
| 1966 | Roth 的 D 演算法——ATPG 測試向量的系統化生成 | [1966-RothD演算法.md](1966-RothD演算法.md) |
| 1969 | Hightower 線搜尋繞線——從格子爆炸跳到連續平面線段 | [1969-Hightower線搜尋繞線.md](1969-Hightower線搜尋繞線.md) |
| 1971 | Hashimoto-Stevens 左緣演算法——通道繞線的區間著色最優解 | [1971-左緣演算法通道繞線.md](1971-左緣演算法通道繞線.md) |

### 分治與模擬（1970–1979）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1970 | Kernighan-Lin 圖分區——貪心交換 + 最佳前綴回溯 | [1970-KernighanLin分區.md](1970-KernighanLin分區.md) |
| 1973 | SPICE——改進節點分析、稀疏 LU、牛頓法與隱式積分合流 | [1973-SPICE電路模擬.md](1973-SPICE電路模擬.md) |
| 1976 | 掃描線 DRC——幾何規則檢查從 O(n²) 降到 O(n log n) | [1976-掃描線DRC.md](1976-掃描線DRC.md) |
| 1977 | Hadlock 最小繞送——A* 家族的格子圖理論基礎 | [1977-Hadlock最小繞送.md](1977-Hadlock最小繞送.md) |

### VLSI 革命（1980–1989）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1980 | Mead-Conway《Introduction to VLSI Systems》——λ 設計規則與結構化設計 | [1980-MeadConway結構化設計.md](1980-MeadConway結構化設計.md) |
| 1982 | Fiduccia-Mattheyses 線性時間分區——桶串增益更新取代成對交換 | [1982-FiducciaMattheyses分區.md](1982-FiducciaMattheyses分區.md) |
| 1982 | Hitchcock 增量式靜態時序分析——不靠向量、遍歷全晶片的時序偵測 | [1982-增量式靜態時序分析.md](1982-增量式靜態時序分析.md) |
| 1983 | 模擬退火（Kirkpatrick 等，Science）——冶金退火的組合最佳化移植 | [1983-模擬退火.md](1983-模擬退火.md) |
| 1983 | Ousterhout 的 Magic——角針織資料結構與增量式 DRC | [1983-Magic版圖編輯器.md](1983-Magic版圖編輯器.md) |
| 1984 | Espresso 邏輯最小化器——兩級布林化簡的業界標準 | [1984-Espresso邏輯最小化.md](1984-Espresso邏輯最小化.md) |
| 1985 | Timberwolf——模擬退火佈局擊敗 min-cut，退火進入實戰 | [1985-Timberwolf退火佈局.md](1985-Timberwolf退火佈局.md) |
| 1986 | Bryant 的 BDD——布林函數的典範表示，驗證的數學地基 | [1986-BDD二元決策圖.md](1986-BDD二元決策圖.md) |
| 1986 | MIS/SIS 多層邏輯合成與 Synopsys 創立——RTL 到閘級自動化革命 | [1986-SIS邏輯合成框架.md](1986-SIS邏輯合成框架.md) |
| 1987 | Keutzer 的 DAGON——DAG 模式比對的技術映射 | [1987-DAGON技術映射.md](1987-DAGON技術映射.md) |

### 形式化與規模化（1990–2005）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1990 | 符號模型檢查——CTL + BDD 讓工業級狀態機可驗證 | [1990-符號模型檢查.md](1990-符號模型檢查.md) |
| 1994 | Elmore 延遲與時序驅動 Steiner 繞線——互連從幾何變成物理 | [1994-Elmore延遲時序驅動繞線.md](1994-Elmore延遲時序驅動繞線.md) |
| 1997 | 多層超圖分區（hMetis/MLPart）——粗化-反粗化典範 | [1997-多層分區.md](1997-多層分區.md) |
| 1998 | Kraftwerk 力導向佈局——虎克定律彈簧網與共軛梯度 | [1998-Kraftwerk解析佈局.md](1998-Kraftwerk解析佈局.md) |
| 1998 | PRIMA 模型降階——Krylov 子空間讓百萬元件互連模擬可行 | [1998-PRIMA模型降階.md](1998-PRIMA模型降階.md) |
| 2001 | Chaff SAT 求解器——CDCL 革命讓 SAT 成為 EDA 萬用引擎 | [2001-Chaff與SAT革命.md](2001-Chaff與SAT革命.md) |
| 2005 | ABC 合成系統——AIG 與 SAT sweeping 的極簡主義 | [2005-ABC合成系統.md](2005-ABC合成系統.md) |

### 平行化與 AI 時代（2015–2024）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 2015 | ePlace——靜電位場類比 + Nesterov 加速梯度 | [2015-ePlace靜電佈局.md](2015-ePlace靜電佈局.md) |
| 2019 | DREAMPlace——深度學習框架把佈局搬到 GPU | [2019-DREAMPlace.md](2019-DREAMPlace.md) |
| 2021 | AlphaChip——圖神經網路 + 強化學習的晶片巨集佈局 | [2021-AlphaChip.md](2021-AlphaChip.md) |
| 2023 | LLM 輔助 EDA——ChipNeMo、ChatEDA 與生成式設計代理 | [2023-LLM輔助EDA.md](2023-LLM輔助EDA.md) |

## 破案主線一覽

1. **表示法之戰**（1937–2005）：Shannon 布林代數 → QM 真值表 → BDD 典範圖 → AIG——每個時代的勝者，都是「更好表示布林函數的資料結構」。
2. **搜尋空間的馴服**（1961–2015）：Lee 迷宮 → 線搜尋 → A*；KL → FM → 多層分區；min-cut → 退火 → 解析佈局——三條主線都在對抗 NP-hard 的組合爆炸。
3. **物理的回歸**（1973–2019）：SPICE 牛頓法 → Elmore/RC 樹 → PRIMA 降階 → ePlace 靜電場——EDA 每到瓶頸就回頭借用物理定律。
4. **邏輯自動化的完成**（1952–2005）：QM → Espresso → SIS → DAGON → ABC——從真值表到 RTL 到閘級的完整映射鏈。
5. **驗證的形式化**（1966–2001）：D 演算法 → BDD → 符號模型檢查 → SAT/CDCL——「證明正確」從夢想變成流程必備。
6. **算力升維**（1983–2024）：退火（IBM 主機）→ GPU（DREAMPlace）→ 深度強化學習（AlphaChip）→ LLM 代理——每次計算平台躍遷，都重寫一次 EDA 工具鏈。
