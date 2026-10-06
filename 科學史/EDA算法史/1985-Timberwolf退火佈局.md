# 1985-Timberwolf退火佈局

## 案件摘要
模擬退火（1983, Science）是漂亮理論，但工業界都在問：真的能打贏線性時間的 min-cut 佈局嗎？1984-85 年，UC Berkeley 的 Carl Sechen 與 Alberto Sangiovanni-Vincentelli 用 **Timberwolf** 給出答案：把退火完整工程化——成本函數 = 線長（半周長）+ 重疊懲罰 + 擁塞懲罰，搬移距離隨溫度縮放，加 dogleg 段式的互動細節——在 IBM 與學界基準上，線長比當時最強的商用 min-cut 工具（如 IBM 的工具）省 15-35%。這是「理論演算法首次在實戰基準擊敗工程啟發式」的標誌性案件，退火自此從學術好奇變成 EDA 佈局的主流路線。

## 前因 -- 為什麼會有這個案子
- **min-cut 的天花板**：遞迴二分佈局（recursive bisection placement，Dunlop-Kernighan 1985）速度快，但每刀只看局部——全局線長品質有結構性上限。
- **退火需要工程化**：Kirkpatrick 的 Science 論文只有概念與小例；成本函數、排程、鄰居結構全是空白——「能不能打」待驗證。
- **佈局是退火的理想土壤**：成本（線長）可增量計算、鄰居結構自然（搬移/交換）——土壤就緒，缺一個完整的工程作品。
- **Berkeley 的戰場**：Sechen 博士論文正是「退火佈局」，Sangiovanni-Vincentelli 同時掌有 SPICE/Espresso 的工業人脈——學界與業界的橋。

## 線索與推理 -- 數學式、程式、理論

### 成本函數：三項懲罰的合流
$$E = \underbrace{\sum_{\text{nets}} \text{HPWL}}_{\text{線長}} + \lambda_1 \underbrace{\sum_{\text{重疊對}} \text{area}}_{\text{重疊懲罰}} + \lambda_2 \underbrace{\sum_{\text{通道}} \text{擁塞}}_{\text{擁塞懲罰}}$$

- **HPWL（半周長線長）**：net 的包圍矩形半周長，是 Steiner 樹長度的下界且 $O(1)$ 計算——工程取捨的教科書案例；
- **重疊懲罰**：高溫時允許重疊（自由探索），低溫時懲罰權重 $\lambda_1$ 漸增——「軟約束漸硬化」的退火哲學；
- **擁塞懲罰**：預估通道密度超限處加罰——提前考慮繞線資源。

### 排程與鄰居結構
- **搬移距離隨溫度縮放**：高溫大跳（全域重排），低溫小挪（局部精修）——$T$ 同時控制接受機率與步長；
- **降溫**：$T_{k+1} = \alpha T_k$，$\alpha \approx 0.8\text{-}0.95$；每溫度的移動數隨溫度降低而增加；
- **巨集單元**：Timberwolf 支援可變尺寸單元與 row-based 標準單元——覆蓋當時兩大設計風格。

### 為什麼能贏：全局視野的數學
min-cut 的錯誤是「每刀局部最優的組合不等於全局最優」；退火的高溫階段允許**跨區大搬移**，探索 min-cut 結構上到不了的配置。理論上（Geman-Geman 1984），無限慢的降溫機率收斂全局最優——Timberwolf 用有限但足夠慢的排程，實務逼近之。

### 戰績
Sechen 在 1985 JSSC/DAC 論文中報告：對 IBM 內部基準與學界電路，Timberwolf 線長比當時最優商業 min-cut 工具平均省 15-35%，且繞線後面積更小。這組數字讓退火一夜之間成為 EDA 研究的主流題目。

## 結案 -- 後果與影響
- **退火進入實戰**：Timberwolf 之後，退火成為 1980-90 年代佈局研究的主流；商用工具（如 Cadence 的早期佈局器）大量吸收其工程技巧（軟約束漸硬化、排程設計）。
- **基準文化的推手**：Timberwolf 的公開比較促成了「同基準打擂台」的研究文化，為 1990s 的 MCNC/GSRC benchmark 與 ISPD 競賽鋪路。
- **與解析法的分道**：退火品質高但 CPU 時小時級；Kraftwerk（1998）解析佈局以速度反超——兩路在 DREAMPlace（2019）合流（退火的品質 + 解析的速度）。
- **Sechen 的續航**：Sechen 後創辦 Duet Technologies 等公司，退火佈局直接商品化。

## 關鍵人物與文獻
- **Carl Sechen**：Berkeley 博士（Sangiovanni-Vincentelli 指導），Timberwolf 作者，退火佈局的實戰派。
- **Alberto Sangiovanni-Vincentelli**：Berkeley 教授，SPICE/Espresso/Timberwolf 的共同推手，Cadence 共同創辦人。
- 文獻：
  - C. Sechen, A. Sangiovanni-Vincentelli, "The TimberWolf Placement and Routing Package," *IEEE J. Solid-State Circuits* SC-20, 510 (1985).
  - C. Sechen, K. W. Lee, "An Improved Simulated Annealing Algorithm for Row-Based Placement," *DAC* 1987（TimberwolfSc 改良版）。
  - S. Geman, D. Geman, "Stochastic Relaxation, Gibbs Distributions, and the Bayesian Restoration of Images," *IEEE TPAMI* 6, 721 (1984)（收斂性理論）。
