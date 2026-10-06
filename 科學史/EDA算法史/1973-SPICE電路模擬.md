# 1973-SPICE電路模擬

## 案件摘要
晶片設好之前，怎麼知道它**真的會動**？1970 年代前，各家公司都有自家的電路模擬器，但演算法雜湊、數值不穩、不可移植。1973 年，UC Berkeley Donald Pederson 團隊釋出 SPICE（Simulation Program with Integrated Circuit Emphasis）：以改進節點分析法（MNA）列方程、稀疏 LU 分解解線性系統、牛頓-拉福森解非線性、梯形法隱式積分對付剛性電路——四大數值演算法在一份程式裡合流，而且**開放給大學免費使用**。SPICE 成為電路模擬的事實標準與「矽預言機」，此後五十年的類比設計與數位時序簽核，都靠它驗明正身。

## 前因 -- 為什麼會有這個案子
- **模擬是唯一預言機**：IC 一次流片昂貴，錯了就是幾個月與數萬美元；必須在投片前用數學預測電路行為。
- **前代模擬器的缺陷**：CANCER（Pederson 團隊前身）等工具用臨時演算法，非線性收斂不穩、矩陣處理不稀疏，規模一大就崩。
- **Berkeley 的開放傳統**：Pederson 堅持模擬器必須免費提供給學界——「讓所有工程師用同一把尺」，這是 SPICE 成為標準的社會學關鍵。
- **電晶體模型就緒**：Shichman-Hodges MOSFET 模型、Ebers-Moll/Gummel-Poon BJT 模型已發表，數學零件齊備。

## 線索與推理 -- 數學式、程式、理論

### 線索一：改進節點分析（MNA）
基爾霍夫定律（KCL：節點電流守恆）+ 支路方程，寫成矩陣方程：

$$\mathbf{G}\,\mathbf{v} = \mathbf{i}$$

MNA 的取捨：以**節點電壓**為主未知數，但把電流源、電感、電壓源的支路電流也列為未知數——避開純節點法無法處理電壓源的死角。矩陣 $\mathbf{G}$ 稀疏（每行非零元 = 該節點連接數），百萬節點的矩陣非零率僅萬分之一級。

### 線索二：三大數值法合流
| 問題 | 演算法 | 理論 |
|------|--------|------|
| 非線性元件 | Newton-Raphson | $x_{k+1} = x_k - J(x_k)^{-1} F(x_k)$，二次收斂，配 gmin/damping 防發散 |
| 稀疏線性系統 | Sparse LU with Markowitz pivoting | Markowitz（1957）準則：先消非零元最少的行列，最小化填入（fill-in） |
| 剛性微分方程 | Implicit trapezoidal / backward Euler | $x_{k+1} = x_k + \frac{h}{2}(f_{k+1} + f_k)$，A-穩定，大步長不炸 |

剛性（stiffness）是電路的本性：電晶體的時間常數橫跨皮秒到毫秒，顯式積分步長會被最快極限鎖死；隱式法無條件穩定，才讓瞬態分析可行。SPICE2（1975，Nagel 與 Rohrer）補齊稀疏矩陣與模型庫，成為工業版本。

### 線索三：收斂與精度的工程哲學
- **牛頓法初值**：用直流工作點（DC operating point）掃描、源分步（source stepping）協助收斂；
- **容差控制**：電壓電流相對容差 RELTOL 預設 $10^{-3}$——「夠準就停」的工程取捨；
- **複雜度**：一次瞬態分析 ≈ $T/h$ 個時間點 × 每點數次牛頓迭代 × 每次迭代一個稀疏 LU（$O(n^{1.5})$ 級）——這條乘法鏈是後世 fast-SPICE（2000s）要拆解的目標。

## 結案 -- 後果與影響
- **事實標準五十年**：SPICE2/3 釋出碼被所有 EDA 廠商吸收；今日 Synopsys HSPICE、Cadence Spectre 皆其嫡系，元件級模擬仍以 SPICE 語法為通用語言。
- **開放策略的勝利**：免費給大學 ⇒ 一代工程師都會 SPICE ⇒ 畢業進業界帶走語法與心智模型——Pederson 的「標準化」推理被證明與演算法同樣重要，2011 年獲 IEEE 榮譽獎章。
- **數值分析的工業聖殿**：MNA、稀疏 LU、隱式積分的合流，使 SPICE 成為應用數學教科書級的工程系統。
- **規模危機的伏筆**：百萬級電晶體（1990s）讓 SPICE 慢到不可用，逼出 AWE/PRIMA 模型降階（1990s）與 fast-SPICE 平行化——本案是「模擬加速軍備賽」的起點。

## 關鍵人物與文獻
- **Donald O. Pederson**（1925–2004）：Berkeley 教授，SPICE 之父，IEEE Medal of Honor（1998）。
- **Laurence Nagel**：SPICE 主要作者，1975 博士論文。
- 文獻：
  - L. W. Nagel, D. O. Pederson, "SPICE (Simulation Program with Integrated Circuit Emphasis)," *Memorandum ERL-M382*, UC Berkeley, 1973.
  - L. W. Nagel, "SPICE2: A Computer Program to Simulate Semiconductor Circuits," PhD thesis, UC Berkeley, 1975.
  - G. D. Hachtel, R. K. Brayton, F. G. Gustavson, "The Sparse Tableau Approach to Network Analysis," *IEEE TC* 1971（稀疏分析理論）。
