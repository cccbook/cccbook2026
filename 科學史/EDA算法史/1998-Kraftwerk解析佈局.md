# 1998-Kraftwerk解析佈局

## 案件摘要
退火佈局（Timberwolf, 1985）品質好但慢——百萬單元的設計要跑一天；min-cut 佈局快但品質受限。1998 年 DAC，慕尼黑工大的 H. Eisenmann 與 F. M. Johannes 發表 **Kraftwerk**（德語「發電廠」）：把 net 建模成虎克定律的彈簧，佈局化為最小化彈簧能量——一個可微分的**二次規劃**，用共軛梯度法解；擁塞/重疊用「密度場的反作用力」處理。解析佈局（analytical placement）自此誕生：連續優化取代離散搜尋，速度比退火快幾十倍。Kraftwerk 是 FastPlace（2004）、RePlAce（2019）等現代佈局器的直系祖先，其「彈簧 + 反作用力」框架至今仍是佈局主引擎。

## 前因 -- 為什麼會有這個案子
- **退火的時間牆**：百萬單元的退火佈局要 CPU 天級——VLSI 規模繼續增長，迭代次數必須從「指數探索」降為「梯度下降」。
- **二次佈局的先例**：Kirkpatrick-Hill（1987）、Hall（1970）的二次佈局已證明「彈簧模型 + 線性系統」可行，但單純彈簧模型會把所有單元**擠成一點**（塌縮）——缺少「攤開」的機制。
- **虎克定律就緒**：彈簧能量 $E = \frac{1}{2} k x^2$ 的物理與最速下降/共軛梯度的數值方法成熟。
- **Poisson 方程的伏筆**：密度場的「反作用力」需要解偏微分方程——FFT 與多重網格的數值工具已就緒。

## 線索與推理 -- 數學式、程式、理論

### 核心：彈簧網 = 二次規劃
每條 net 建成彈簧（虎克定律），單元 $i, j$ 連接權 $w_{ij}$，目標最小化彈簧勢能：

$$\min_x\ E(x) = \frac{1}{2} \sum_{(i,j)} w_{ij} \big((x_i - x_j)^2 + (y_i - y_j)^2\big)$$

I/O pad（固定位置）提供參考系，防塌縮。梯度令其為零得線性系統：

$$\nabla E = L\, x = 0, \quad L_{ii} = \sum_j w_{ij},\ L_{ij} = -w_{ij}$$

$L$ 是**圖拉普拉斯矩陣**（graph Laplacian）——譜圖論的對象進入佈局！用共軛梯度法（CG）解，收斂快且記憶體省。

### 為什麼會塌縮：無約束的最優
無 pad、無密度約束時，$x = 0$（全疊一點）就是最優——彈簧能量沒有「攤開」項。Kraftwerk 的解法：**密度場反作用力**——把佈局區離散成格子，計算每格密度，過密處產生「斥力」推單元散開：

$$F_{\text{density}}(x) \propto -\nabla \rho(x), \quad \rho = \text{密度場}$$

每輪迭代：解彈簧系統 → 更新密度場 → 加反作用力 → 再解——「彈簧吸、密度斥」的動力平衡，最終單元攤開且線長短。

### 為什麼快：連續 vs 離散
| | 退火（離散搜尋） | Kraftwerk（連續優化） |
|---|---|---|
| 移動 | 隨機搬移 + 接受機率 | 梯度方向確定前進 |
| 每步成本 | $O(\deg)$ | $O(n \log n)$（CG/FFT 解場）|
| 總迭代 | $10^6\text{-}10^8$ | $10^1\text{-}10^2$ 輪 |
| 複雜度 | 時小時-天級 | 時分級 |

連續優化的「每步都有確定下降方向」，使其迭代數比隨機搜尋少幾個數量級——這是解析法勝出的結構性原因。

### 後繼者的接力
- **FastPlace（2004, Viswanathan-Chu）**：斥力模型化簡，速度再快；
- **mPL6（2006, Kahng-Reda）**：多重網格解密度場；
- **RePlAce（2019, Cheng-Kahng）**：全域佈局與繞線性驗證整合，OpenROAD 採用；
- **ePlace（2015）**：反作用力升級為靜電場（見 2015 卷宗）。

## 結案 -- 後果與影響
- **解析佈局成為主流**：Kraftwerk 確立「二次優化 + 密度斥力」框架，今日所有現代佈局器（RePlAce、TritonPlacer）都是其直系或變體。
- **譜圖論的入口**：圖拉普拉斯矩陣、譜方法自此進入 EDA——後續的圖分割（譜分割）、聚類（譜聚類）同源。
- **退火時代的落幕**：解析法以速度取勝，退火佈局逐漸退場（僅存於特定巨集排布）——兩代演算法的接力完成。
- **物理的第三次回歸**：虎克定律（力學）→ 密度場（統計）→ 靜電場（電磁學, ePlace）——佈局的物理類比一路升級，支撐到 GPU 時代（DREAMPlace）。

## 關鍵人物與文獻
- **H. Eisenmann, F. M. Johannes**：慕尼黑工大（TUM），Kraftwerk 系統作者。
- 文獻：
  - H. Eisenmann, F. M. Johannes, "Generic Global Placement and Floorplanning," *DAC* 1998, 269–274.
  - K. M. Hall, "An r-Dimensional Quadratic Placement Algorithm," *Management Science* 17, 219 (1970)（二次佈局先例）。
  - N. Viswanathan, C. Chu, "FastPlace: An Efficient Analytical Placement Algorithm," *ISPD* 2004（後繼）。
