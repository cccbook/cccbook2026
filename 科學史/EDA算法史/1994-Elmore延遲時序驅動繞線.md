# 1994-Elmore延遲時序驅動繞線

## 案件摘要
1970-80 年代的繞線只求「連起來且最短」——但元件縮小後，**線的電阻電容（RC）本身就是延遲**：一條繞長一倍的線，延遲可能翻倍，時序就爆。1990 年代，Elmore 延遲（1948）與 RC 樹分析（1983）成熟，讓「線長」升級成「延遲」：繞線器第一次知道每一條線的物理後果。時序驅動 Steiner 繞線、緩衝器插入、零偏斜時脈樹（DME 演算法）在此十年全面誕生——互連設計從幾何問題變成物理問題，這是先進製程時代「互連為王」的演算法序曲。

## 前因 -- 為什麼會有這個案子
- **製程縮小的物理後果**：線寬縮小 ⇒ 電阻 $R \propto 1/W$ 暴增；時脈 GHz 化 ⇒ 互連延遲從可忽略變成延遲主體（1990s 中葉，互連延遲超越閘延遲）。
- **線長 ≠ 延遲**：兩條等長線，分岔結構不同，RC 延遲可差數倍——必須建模拓撲。
- **Elmore 延遲就緒**（1948）：W. C. Elmore 給出 RC 網路的一階延遲估計——50 年前的物理公式，終於等到 EDA 場景。
- **SPICE 太慢**：全晶片互連都用 SPICE 瞬態分析不可行——需要閉式（closed-form）延遲估計。

## 線索與推理 -- 數學式、程式、理論

### 線索一：Elmore 延遲——衝擊響應的一階矩
RC 樹（無環、單源）的 Elmore 延遲 = 電容加權的共享電阻和：

$$t_{ed}(i) = \sum_{j \in \text{子樹}(i)} R_{\text{shared}}(i, j)\, C_j$$

其中 $R_{\text{shared}}(i,j)$ 是根到 $i$ 與根到 $j$ 路徑的**共享電阻**。物理意義：Elmore 延遲是衝擊響應 $h(t)$ 的一階矩（重心）：

$$t_{ed} = \int_0^\infty t\, h(t)\, dt$$

Rubinstein-Penfield-Horowitz（1983）證明：對 RC 樹，Elmore 延遲是 50% 延遲的良好上/下界，且 $O(k)$（$k$ = 樹節點數）線性可算——閉式延遲估計就此進入 EDA。

### 線索二：時序驅動 Steiner 樹
有了延遲模型，樹的建構從「最短」升級為「最快」：
- **Prim-Dijkstra 權衡**：Prim 式建樹偏短（delay 對源好）、Dijkstra 式偏淺（delay 對 sink 好）——混合權衡 $w = \alpha \cdot \text{edge} + (1-\alpha) \cdot \text{depth}$；
- **AHHK/BST/DME 零偏斜**：時脈樹要求所有 sink 同時到達（偏斜 skew = 0），DME（Deferred Merge Embedding, Edahiro 1991 / Boese-Kahng 1992）兩階段演算法在拓撲固定的條件下**精確嵌入零偏斜**：

$$\forall i, j:\ |t_{ed}(i) - t_{ed}(j)| \le \epsilon \quad (\text{skew 下界})$$

- **緩衝器插入**：RC 樹分段加 buffer，把 $O(L^2)$ 的延遲增長壓回線性——Alpert-Devgan 等人的理論（1990s 末）證明最優插入的多項式演算法。

### 線索三：繞線器的升級
global routing 的目標函數從 $\sum \text{wirelength}$ 升級為：

$$\min\ \max_{\text{paths}} \big(\text{delay}\big) \quad \text{s.t. 擁塞、密度}$$

時序驅動繞線（timing-driven routing）自 1990s 成為標準——STA（1982）給出 slack，繞線器按 slack 分配資源，「時序收斂」迴圈閉合。

## 結案 -- 後果與影響
- **互連為王時代的序曲**：1990s 末互連延遲超越閘延遲，Elmore/RC 樹成為每個繞線器、佈局器的內建模組——物理回歸主線的關鍵轉折。
- **時脈樹合成的誕生**：DME 零偏斜演算法成為 CTS（clock tree synthesis）的標準，支撐 GHz 時代。
- **與 STA 的合流**：Elmore 延遲讓繞線器自己算時序（不必每次呼叫 SPICE），時序驅動佈局繞線自此可行——「時序收斂」成為 EDA 的核心工程。
- **更精確模型的接力**：Elmore 一階矩 → AWE/PRIMA 高階矩（1990s）→ PRIMA 被動降階——延遲模型的精度階梯自此鋪好。

## 關鍵人物與文獻
- **W. C. Elmore**（1911–2006）：物理學家，1948 年 RC 延遲理論，50 年後成為 EDA 標準。
- **Jacob Rubinstein, Paul Penfield, Mark Horowitz**：RC 樹延遲界與波形估計。
- 文獻：
  - W. C. Elmore, "The Transient Response of Damped Linear Networks," *J. Appl. Phys.* 19, 55 (1948).
  - J. Rubinstein, P. Penfield, M. A. Horowitz, "Signal Delay in RC Tree Networks," *IEEE Trans. CAD* 2, 202 (1983).
  - M. Edahiro, "A Clustering-Based Optimization Algorithm in Zero-Skew Routings," *DAC* 1991（DME 相關）。
