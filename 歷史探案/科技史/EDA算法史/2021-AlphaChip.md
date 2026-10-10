# 2021-AlphaChip

## 案件摘要
佈局的最後堡壘：**巨集佈局（macro placement）**——數十至數百個巨型塊（memory、ALU、互連）的排布，組合空間爆炸且評估一次（要跑繞線 + 時序）極慢，傳統退火與解析法都要人類專家數週調參。2021 年，Google 的 Azalia Mirhoseini、Anna Goldie 等人在《Nature》發表**強化學習（RL）晶片佈局**：把巨集佈局視為圍棋式的馬可夫決策過程——狀態用**圖神經網路（GNN）**編碼 netlist，動作是「放下下一個巨集」，獎勵是線長/密度/擁塞的加權負值——RL 智慧體在 6 小時內產出與人類工程師數週成果相當的 TPU 佈局。2024 年 Google 把方法命名為 **AlphaChip**。這是 AlphaGo 的技術路線首次落地晶片設計——AI 從「輔助工具」變成「設計主體」的分水嶺（儘管業界對其泛化性仍有爭議）。

## 前因 -- 為什麼會有這個案子
- **巨集佈局的獨特性**：與標準單元佈局不同，巨集少而大、離散排布、評估一次貴——解析法（ePlace）擅長連續，對這種「少而貴」的離散問題不對症。
- **評估的延遲回報**：佈局好壞要到繞線 + 時序分析才知——延遲回報 + 巨大狀態空間，正是 RL/圍棋的場景。
- **AlphaGo 的技術就緒**（2016-2017）：GNN + RL + 快速模擬的組合已在圍棋驗證——技術模板現成，缺一個晶片應用。
- **Google 的自給自足**：TPU 世代設計，Google 擁有自己的設計團隊與算力——內部需求 + 算力 + 人才合流。

## 線索與推理 -- 數學式、程式、理論

### 核心：佈局 = MDP
- **狀態 $s$**：當前版圖（已放置巨集的座標 + netlist 特徵，以 **GNN 編碼**——圖神經網路在電路圖上做消息傳遞，學出節點嵌入）：

$$h_i^{(k+1)} = \sigma\Big(W_1 h_i^{(k)} + \sum_{j \in \mathcal{N}(i)} W_2 h_j^{(k)}\Big)$$

- **動作 $a$**：把下一個巨集放到某候選座標（按巨集大小排序逐一放置）；
- **獎勵**：線長、擁塞、密度的加權負值（前期）+ 繞線後評估（後期）；

**Q-learning 更新**（深度 Q 網路 DQN）：

$$Q(s,a) \leftarrow Q(s,a) + \alpha\big[r + \gamma \max_{a'} Q(s',a') - Q(s,a)\big]$$

最佳策略 $\pi^*(s) = \arg\max_a Q^*(s,a)$。訓練用 Policy Gradient（REINFORCE/PPO 變體）+ 模仿人類專家起手。

### 為什麼 RL 對症：三個同構
| 圍棋（AlphaGo）| 巨集佈局（AlphaChip）|
|----------------|---------------------|
| 棋盤狀態 | 版圖狀態 |
| 落子 | 放巨集 |
| 勝負（終局才知）| 線長/擁塞（繞線後才知）|
| 策略網路 + 估值網路 | GNN + Q 函數 |

巨大狀態空間（$k^n$，$n$ = 巨集數）、延遲回報、離散動作——RL 的理想土壤。

### 為什麼快：一次訓練、反覆使用
- RL 智慧體在**相似設計**（TPU 各代、相同巨集庫）上遷移——一次訓練，後續設計數小時出解；
- 對比：人類專家每次都要數週——「學習曲線」取代「人工曲線」，這是 RL 方案的核心經濟學。

### 爭議：泛化性的辯論
2023 年，Igor Markov（前 Meta）在《CACM/Nature》發表質疑：對比基準不公平、部分結果難重現。Google 回應（Nature addendum, 2024）。這場辯論本身是 EDA 演算法科學的「同行偵辦」——AI 佈局的真實實力仍在被驗證中。工程界目前共識：RL 佈局在「相似設計族」上有效，對全新設計仍需專家介入。

## 結案 -- 後果與影響
- **AI 佈局時代的開啟**：Synopsys DSO.ai（2020）、Cadence Cerebrus（2021）等商業 AI 工具同期推出——RL/搜尋 + AI 成為 EDA 的新戰場。
- **EDA 的算力升維完成**：CPU（退火）→ GPU（DREAMPlace）→ RL 叢集（AlphaChip）——計算平台的每一級都重寫一次佈局演算法。
- **設計主體的轉移辯論**：AI 從「輔助」變「主體」——EDA 演算法的設計者從人類工程師擴展到學習系統，方法學（可解釋性、可重現性）成為新課題。
- **GNN 的入口**：圖神經網路自此成為 EDA 標配（預測時序、擁塞、DRC 違規），「學習式 EDA」成為獨立研究領域。

## 關鍵人物與文獻
- **Azalia Mirhoseini, Anna Goldie**：Google Brain/DeepMind，RL 佈局團隊核心。
- **Jeff Dean**：Google，AI for Systems 的推手。
- 文獻：
  - A. Mirhoseini et al., "A Graph Placement Methodology for Fast Chip Design Using a Deep RL Algorithm," *Nature* 594, 207 (2021).
  - I. Markov, "Limitations of the Nature Paper on Chip Placement," *CACM* 66 (2023)；Google 回應：Nature addendum, 2024（AlphaChip 命名）。
  - D. Silver et al., "Mastering the Game of Go with Deep Neural Networks and Tree Search," *Nature* 529, 484 (2016)（AlphaGo 技術模板）。
