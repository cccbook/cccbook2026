# 1966-Hanan網格Steiner樹

## 案件摘要
Lee 演算法解決「兩點連一線」，但一條 net 常有幾十個 pin，要連成一棵**樹**；且 EDA 裡走線只能水平垂直（直角距離），這是經典 Steiner 樹問題的直角變體——連續版本已在 19 世紀困住幾何學家。1966 年，貝爾實驗室的 Maurice Hanan 證明一個漂亮的結構定理：**最優直角 Steiner 樹一定落在 Hanan 網格上**（過每個 pin 畫水平垂直線，取其交點即可）。無限連續的搜尋空間瞬間縮成 $O(k^2)$ 個候選點——Steiner 繞線從此從幾何懸案變成離散可偵辦的案件。

## 前因 -- 為什麼會有這個案子
- **多 pin net 是常態**：一條時脈或匯流排連接數十個負載，兩兩兩兩連接（MST，最小生成樹）不見得最短——必須允許新增「分岔點」。
- **Steiner 問題的老懸案**：平面上加點使總長最短（幾何 Steiner 樹）自 Fermat/Steiner 起是經典難題；直角度量（Manhattan）版本在 EDA 場景更迫切。
- **無法直接套用 Lee**：Lee 演算法對任意格子都能走，理論上可在完整格線上找最優，但連續空間的候選點無窮多，窮舉不可行。
- **手工佈線靠經驗**：工程師用「丁字尺加直覺」畫分岔，品質參差——需要一個可證明的有限候選集。

## 線索與推理 -- 數學式、程式、理論

### 定理：最優解落在 Hanan 網格
給定 pin 集 $P = \{p_1, \dots, p_k\}$，定義 **Hanan 網格**：

$$H(P) = \{(x_i, y_j) : x_i \in \text{pins 的 } x \text{ 座標集},\ y_j \in \text{pins 的 } y \text{ 座標集}\}$$

**Hanan 定理（1966）**：存在一棵最優直角 Steiner 樹 $T^*$，其所有 Steiner 點都落在 $H(P)$ 的頂點上。

**推理骨架**（可換論證 exchange argument）：若 $T^*$ 的某條邊通過非 Hanan 頂點的交點，總可把該段的轉折「推」到最近的 Hanan 交點而不增加總長——因為樹的分支可以重排，成本不變或更小。於是：

$$|\text{候選 Steiner 點}| = O(k^2), \quad \text{連續無窮} \to \text{有限離散}$$

### 最優性與近似
- Hanan 網格上的 Steiner 樹仍是 NP-困難（Hwang 1976 證明直角版 NP-完全；Dreyfus-Wagner 1971 給出 $O(3^k k + k^2)$ 的精確指數演算法）。
- 但有了有限候選集，好的近似唾手可得：**MST 在 Hanan 網格上不超過最優 Steiner 樹的 $3/2$ 倍**（Hwang, 1976）：

$$\text{len}(MST) \le \frac{3}{2} \cdot \text{len}(SMT)$$

MST 可用 Kruskal/Prim 在 $O(k^2 \log k)$ 內求出，成為實務上的主力近似。

### 範例：三點的 Steiner 樹
三個 pin：A(0,4)、B(2,0)、C(6,1)。Hanan 網格交點含 (2,4)、(6,4)、(0,0)、(6,0) 等。最優解在 (2,1) 附近立分岔：總長 $6+1$ 級別，明顯短於 MST 的兩兩連接（$2\sqrt{20}/$… 直角化後更長）。在 Hanan 網格上搜尋，候選分岔點只有有限個——這就是從「無窮」到「九個交點」的縮減。

## 結案 -- 後果與影響
- **Steiner 繞線成為 EDA 標配**：所有現代繞線器的時序關鍵 net 都用 Steiner 樹而非 MST；RSMT 求解器（如 FLUTE, 2005）是每台佈局繞線器的內建零件。
- **理論的接力偵辦**：Hwang 的 3/2 近似、Gilbert-Pollak Steiner ratio 猜想（1968）、Zelikovsky 的 11/6 改良（1993），整條近似演算法鏈都從 Hanan 網格出發。
- **時序驅動的入口**：有了有限候選集，才能把延遲模型（Elmore, 1994 案）嫁接到樹的建構上，催生時序驅動繞線。
- **證明技術的範本**：交換論證（exchange argument）證結構定理的做法，成為 EDA 理論文獻的標準武器。

## 關鍵人物與文獻
- **Maurice Hanan**（1926–2014）：貝爾實驗室，繞線理論先驅。
- 文獻：
  - M. Hanan, "On Steiner's Problem with Rectilinear Distance," *SIAM J. Appl. Math.* 14, 255 (1966).
  - F. K. Hwang, "On Steiner Minimal Trees with Rectilinear Distance," *SIAM J. Appl. Math.* 30, 104 (1976)（NP-完全與 3/2 界）。
  - S. E. Dreyfus, R. A. Wagner, "The Steiner Problem in Graphs," *Networks* 1, 195 (1971).
  - C. Alpert, T.-C. Hu et al., 之 FLUTE：C. Chu, Y.-C. Wong, "FLUTE: Fast Lookup Table Based Wirelength Estimation Technique," *ICCAD* 2008.
