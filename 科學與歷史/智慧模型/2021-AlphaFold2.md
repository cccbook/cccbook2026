# 2021 - AlphaFold2 蛋白質結構預測

## 案件摘要

2021 年 7 月，DeepMind 的 Jumper 等人在 **CASP14**（第 14 屆蛋白質結構預測競賽）發表 **AlphaFold2**：以**端對端注意力網路（Evoformer）**直接從胺基酸序列預測三維結構。中位 GDT_TS 達 **92.4**（GDT 100 = 完美重合）——而傳統實驗方法（冷凍電鏡、X 射線繞射）一個蛋白質要數年與百萬美元。這是**五十年大問題的結案**：1972 年 Anfinsen 提出的「序列決定結構」假說，被一個注意力網路在數分鐘內實現。核心公式是幾何約束的學習：

$$\text{序列} \xrightarrow{\text{Evoformer}} \text{殘基對表示} \xrightarrow{\text{結構模組}} \text{三維座標} \; \{\mathbf{r}_1, \dots, \mathbf{r}_L\}$$

這是科學智能的巔峰案件：2024 年，Hassabis 與 Jumper 獲**諾貝爾化學獎**（與 Baker 共享）。

## 前因 -- 為什麼會有這個案子

- **五十年大問題**：蛋白質折疊——1972 年 Anfinsen 諾獎演說提出假說：**蛋白質的天然三維結構完全由其胺基酸序列決定**。序列已知，但從序列算出結構的「折疊密碼」五十年未破。
- 搜尋空間的殘酷：$L$ 個殘基的構象空間天文數字（Levinthal 悖論：若隨機搜尋，宇宙年齡都不夠）——但蛋白質在數毫秒內自己折好，說明存在**物理原理**或**動力學路徑**可循。
- CASP 競賽的歷史：兩年一屆的結構預測奧林匹克，2018 年 CASP13 的 **2021-AlphaFold蛋白質摺疊.md**（AlphaFold1）已奪冠（GDT ~60），但仍是「協同進化特徵 + 梯度下降優化」的兩段式方法，且距離實驗精度遙遠。
- 前驅線索：**共進化訊號**——MSA（多序列比對）中，兩個在空間上相鄰的殘基會協同突變；DCA（direct coupling analysis, 2011）用統計物理從 MSA 推出殘基接觸圖。但 MSA 深度不足時訊號崩塌。
- **2017-Transformer注意力機制.md** 的注意力恰好是「殘基對之間的關係學習器」——注意力矩陣天然對應殘基接觸。
- 動機：DeepMind 在 **2016-AlphaGo擊敗李世乭.md** 之後要證明「AI 能解決科學大問題」——Hasabis 的科學願景直指蛋白質折疊。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：Evoformer——兩種表示的互相對質

AlphaFold2 的核心是 **Evoformer**（48 層）：同時維護兩種表示，並讓它們**互相交換資訊**：

| 表示 | 形狀 | 角色 |
|---|---|---|
| MSA 表示 | $M \times L \times c$ | $M$ 條同源序列 × $L$ 個殘基的演化史 |
| Pair 表示 | $L \times L \times c'$ | 每對殘基之間的關係（接觸圖、距離、方向） |

- **軸向注意力（axial attention）**：MSA 表示沿序列軸與沿序列間軸分別做注意力——把 $O(M^2 L^2)$ 的全注意力壓成 $O(ML^2 + M^2 L)$，48 層深網才訓得動。
- **三角更新（triangle update）**：pair 表示中，若 $i$-$j$ 相鄰且 $j$-$k$ 相鄰，則 $i$-$k$ 的關係受幾何一致性約束——三角不等式被寫進網路：

$$d(i,k) \;\lesssim\; d(i,j) + d(j,k)$$

這是「物理幾何先驗」被內化為架構的罕見設計：不是靠損失函數軟約束，而是**架構本身強制幾何一致性**。

### 第二條線索：端對端結構模組——從關係到座標

Evoformer 之後，結構模組用**不變點注意力（invariant point attention, IPA）**把 pair 表示直接解碼成三維座標：

$$\{\mathbf{r}_1, \dots, \mathbf{r}_L\} = \mathrm{StructureModule}(\text{MSA repr}, \text{pair repr})$$

IPA 的巧妙之處：注意力在 **SE(3) 等變**的框架下計算——整體旋轉、平移不影響內部表示。訓練時以「反覆修正」（recycling）：把上一輪的預測結構餵回輸入再修正，共 3 輪——像雕塑家反覆修整。損失函數的組合：

$$\mathcal{L} = \mathcal{L}_{\text{FAPE}} + \lambda_1 \mathcal{L}_{\text{dist}} + \lambda_2 \mathcal{L}_{\text{angle}} + \lambda_3 \mathcal{L}_{\text{masked MSA}} + \cdots$$

$\mathcal{L}_{\text{FAPE}}$（frame-aligned point error）在局部座標系中量測預測與真實殘基的偏差——對整體位姿不變。

### 第三條線索：從兩段式到端對端——AlphaFold1 的謀殺

| | **AlphaFold1 (2018)** | **AlphaFold2 (2021)** |
|---|---|---|
| 方法 | 協同進化特徵 + 梯度下降幾何優化（兩段式） | **端對端注意力**（Evoformer + 結構模組） |
| CASP 成績 | GDT ~60 | **GDT 92.4** |
| 預測時間 | 數小時 | **數分鐘** |
| MSA 依賴 | 重度（深 MSA 才有訊號） | 中度（淺 MSA 也能預測） |

AlphaFold1 的兩段式被謀殺——兇手是**端對端**：特徵提取與幾何優化之間的斷層被注意力抹平。與 **2017-Transformer注意力機制.md** 在翻譯上、**2021-ViT視覺Transformer.md** 在影像上的判決同構：**端對端 + 注意力 + 資料，打敗一切手工特徵工程**。

### 第四條線索：置信度與科學誠信——pLDDT 的發明

AlphaFold2 為每個殘基輸出**置信度分數 pLDDT（0–100）**：高置信區域與實驗結構重合，低置信區域（固有序列區、無序區）自動標出。這是科學工具的關鍵設計：**模型不只給答案，還告訴你哪裡的答案不可信**。CASP14 評委的判詞：AlphaFold2 在多數目標上達到與實驗方法相當的精度——五十年大問題，**在實務上宣告解決**。

### 第五條線索：CASP14 現場——成績單的宣判

CASP14 各方法在自由建模（FM）與 TBM 類目標上的中位 GDT_TS：

| 方法 | 中位 GDT_TS（全目標） |
|---|---|
| CASP13 最佳（AlphaFold1 系） | ~60 |
| CASP14 其他參賽組 | ~70（RoseTTAFold） |
| **AlphaFold2** | **92.4** |

評委的比喻：「一瞬間從可見地平線躍升至與實驗結構難以區分」。且 AlphaFold2 的骨幹在**無 MSA** 的極端條件下仍能給出可用結構（靠端對端學習的序列先驗）——共進化訊號從「必需品」降格為「增益項」。對照實驗的成本帳：一個蛋白質的 X 射線繞射結構需 1–3 年與百萬美元，AlphaFold2 預測只需**數分鐘與一枚 GPU**。線索至此全部合攏，五十年大問題正式宣判。

## 結案 -- 後果與影響

- 2021 年 7 月 DeepMind 開源 AlphaFold2 程式碼，並釋出 **AlphaFold Protein Structure Database**：至 2022 年已預測 **2 億+ 個蛋白質結構**（涵蓋幾乎所有已知蛋白質）——實驗界數十年的工作量被一次償清。
- **2024 年諾貝爾化學獎**：Hassabis 與 Jumper 因蛋白質結構預測獲獎（與 Baker 的蛋白質設計共享）——AI 科學家的最高加冕。
- 科學智能的典範確立：Evoformer 的設計（兩種表示互質、幾何先驗內化、IPA）外溢到 RNA 結構、蛋白質複合體、材料科學——「表示 + 幾何 + 注意力」成為科學 ML 的模板。
- 蛋白質設計的閉環：**2021-AlphaFold2（預測）→ RFdiffusion（設計，2023）→ 新藥與酶的從頭設計**——預測反轉即設計，擴散模型（呼應 **2020-DDPM擴散模型.md**）在結構空間中生成新蛋白質。
- 藥物研發加速：靶點結構即時可得，結構導向藥物設計（SBDD）的成本驟降（見「科學與歷史/化學史/」「科學與歷史/生理醫學史/」的對應討論）。
- 演化生物學的意外紅利：MSA 表示中發現了「演化尺度上的語義」——蛋白質語言模型（ESM 系列）隨後證明**不做 MSA、只讀序列**也能預測結構，與 **2018-BERT與GPT預訓練典範.md** 的預訓練典範匯流。
- 主線伏筆：AlphaFold2 是「AI for Science」的旗艦——從蛋白質到材料、天氣（GraphCast）、核融合控制，科學的每一格都開始被智能模型佔領。本書的主題「智慧模型」在此案達到巔峰：一個模型承載的不是語言、不是影像，而是**物質世界的結構知識**。

## 關鍵人物與文獻

- **John Jumper**：AlphaFold2 第一作者，2024 諾貝爾化學獎得主。
- **Demis Hassabis**：DeepMind 創辦人，2024 諾貝爾化學獎得主（見 **2016-AlphaGo擊敗李世乭.md**）。
- **John Moult**：CASP 競賽創辦人。
- **David Baker**：蛋白質設計（RoseTTAFold、RFdiffusion），2024 諾獎共享者。
- Jumper et al., *Highly accurate protein structure prediction with AlphaFold*, Nature, 2021。
- Senior et al., *Improved protein structure prediction using potentials from deep learning*（AlphaFold1）, Nature, 2020（見 **2021-AlphaFold蛋白質摺疊.md**）。
- Anfinsen, *Principles that govern the folding of protein chains*, Science, 1973（五十年前假說）。
- Baek et al., *Accurate prediction of protein structures using a three-track neural network*（RoseTTAFold）, Science, 2021。
- Watson et al., *De novo design of protein structure with a diffusion model*（RFdiffusion）, Nature, 2023。
- 相關案件：**2021-AlphaFold蛋白質摺疊.md**、**2020-DDPM擴散模型.md**、**2017-Transformer注意力機制.md**、**2016-AlphaGo擊敗李世乭.md**（見「科學與歷史/人工智慧/」）
