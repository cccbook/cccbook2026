# 1979 - Garey & Johnson 的「聖經」

## 案件摘要
1979 年，Michael Garey 與 David Johnson 出版《Computers and Intractability: A Guide to the Theory of NP-Completeness》，把 NP-完備理論從論文森林整理成一本手冊，附上 300 多個問題的歸約清單。這本紅皮書被譽為「NP-完備的聖經」，四十年後仍是理論與實務的橋樑。

## 前因 -- 為什麼會有這個案子
- Cook（1971）與 Karp（1972）之後，NP-完備性證明如雨後春筍：1970 年代每年數十篇論文散落在運籌學、圖論、排程、VLSI 等期刊。
- 實務工程師面對新問題時，無從得知「這問題已被證明很難」——知識嚴重碎片化。
- Garey 與 Johnson 都在 Bell 實驗室工作，長期研究排程與圖著色的複雜度，深知實務需求。
- 案件動機：**寫一本「地圖集」，把所有已知困難問題標記在地圖上。**

## 線索與推理 -- 數學式、程式、理論
### 內容架構
全書分兩大半：
1. **理論部分**（前 4 章）：定義 $\text{P}$、$\text{NP}$、多項式歸約 $\leq_p$、NP-完備性；證明 Cook–Levin 定理；示範標準歸約技術（限制法、局部替換法、組合設計法）。
2. **問題清單**（附錄 A）：**300+ 個問題**，每個條目格式嚴格：

> **[問題名稱]**
> 實例：輸入的正式描述
> 詢問：是/否問題
> 註解：歸約來源、參考文獻、複雜度分類（如 [AN6]、[GT19]）

清單按領域編號：GT（圖論）、ND（網路設計）、SP（集合與分割）、SR（排序與排程）、AL（代數）、AN（數值與規劃）、MS（程式與最佳化）等。

### 歸約技術（書中歸納的三大法門）
```python
# 例：從 SAT 歸約到「團問題」的局部替換法
def sat_to_clique(clauses, k_vars):
    # 每個 clause 的每個文字變成圖上一個頂點
    vertices = []
    for i, clause in enumerate(clauses):
        for lit in clause:
            vertices.append((i, lit))
    # 邊：不同 clause 且文字不互斥（非 x 與非 -x）
    edges = []
    for (i, l1) in vertices:
        for (j, l2) in vertices:
            if i != j and l1 != negate(l2):
                edges.append(((i, l1), (j, l2)))
    # 有大小為 m = len(clauses) 的團 ⟺ 原式可滿足
    return vertices, edges, len(clauses)
```
這條歸約在書中清單裡登記為團問題的標準出處。

### 近似演算法與近似比
書中專章討論：對最佳化問題，與其求精確解（可能永遠跑不完），不如求「有保證的近似解」。定義：
$$\rho\text{-近似演算法：}\quad \forall x,\quad \text{ALG}(x) \le \rho \cdot \text{OPT}(x) \quad (\text{最小化問題})$$
書中收錄的例子：
- **頂點覆蓋**：2-近似（極大匹配法）
- **裝箱問題（bin packing）**：First-Fit-Decreasing 滿足 $\text{FFD}(I) \le \frac{11}{9}\text{OPT}(I) + C$
- **旅行商（一般圖）**：無常數近似比（除非 P = NP）；但**度量 TSP** 有 2-近似（MST 法），Christofides 1976 達到 $3/2$-近似
- 同時指出有些問題（如一般圖最大團）**連近似都難**——這個伏線要到 PCP 定理（1990s）才被嚴格證明。

### 實務觀點：面對 NP-hard 的三種策略
1. **近似演算法**：多項式時間 + 可證明的品質保證 $\rho$。
2. **啟發式方法（heuristics）**：實務上快，但無理論保證（模擬退火、貪婪法、局部搜索）。
3. **參數化/特殊結構**：當輸入有特殊結構（平面圖、樹狀結構、小參數 $k$）時，問題可以變簡單——書中大量記錄「此問題在限制條件 $X$ 下多項式可解」的註解。

## 結案 -- 後果與影響
- **演算法課程的革命**：1979 年後，「NP-完備性」成為大學演算法課程的標準單元，本書是二十年間的指定教材（後由 CLRS 等接棒，但清單仍被引用）。
- **業界的影響**：運籌學、晶片設計（VLSI 佈局）、排程系統的工程師從此有一本「困難詞典」——遇到新問題，先查清單，確認 NP-hard 後直接採用近似或啟發式策略，不再盲目追求精確解。
- **研究議程的建立**：清單中未解的條目（如圖同構、質因數分解「未分類」）成為後續數十年的研究目標。
- 書中「有些問題難以近似」的直覺，在 PCP 定理問世後被證明為真，使本書成為近似演算法理論的先聲。
- 2020 年代，書中 300+ 清單仍是判定「新問題難度」的第一站；Garey 於 2022 年逝世，Johnson 於 2016 年逝世，兩人留下的地圖仍在被使用。

## 關鍵人物與文獻
- **Michael R. Garey、David S. Johnson**：*Computers and Intractability: A Guide to the Theory of NP-Completeness*, W.H. Freeman, 1979。
- **Stephen Cook**（1971）、**Richard Karp**（1972）：清單的理論源頭。
- **Christos Papadimitriou、Kenneth Steiglitz**（1982）：*Combinatorial Optimization*，接續本書的最佳化視角。
- **Vijay Vazirani**（2001）：*Approximation Algorithms*，把書中近似章節發展成完整理論。
- 書中著名的開場：Garey 與 Johnson 獻給「所有在多項式時間內找不到答案的人」。
