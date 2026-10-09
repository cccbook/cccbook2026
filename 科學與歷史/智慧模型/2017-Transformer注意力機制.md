# 2017 - Transformer 注意力機制

## 案件摘要

2017 年 6 月，Google 的 Vaswani 等人發表 **《Attention Is All You Need》**：完全拋棄循環與卷積，只用**自注意力（self-attention）**處理序列。核心公式一行寫盡：

$$\mathrm{Attention}(Q, K, V) = \mathrm{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V$$

查詢 $Q$ 對所有鍵 $K$ 做相似度比對，加權聚合值 $V$——任意兩個位置**直連一步**，長程依賴不再是 $O(T)$ 步的馬拉松，而是一矩陣乘法。LSTM 被謀殺——兇手不是更強的記憶，而是**直連任意距離 + 完美並行**。這是本書大模型時代的總開關：BERT、GPT、ViT、CLIP 全是這一行公式的子孫。

## 前因 -- 為什麼會有這個案子

- **2014-Seq2Seq與注意力.md** 已埋下引線：Bahdanau、Luong 的注意力是 RNN 編碼器—解碼器之上的「補丁」——翻譯時讓解碼器回頭看編碼器的所有隱狀態。但注意力只是配角，主角仍是 LSTM。
- LSTM 的兩大死穴（見 **1997-LSTM長短期記憶.md**）：
  1. **序列性**：時間步 $t$ 必須等 $t-1$ 算完，GPU 的萬級核心閒置——訓練無法並行。
  2. **長程路徑**：資訊要穿越 $O(T)$ 個閘門，距離越遠越稀釋。
- **2016-WaveNet語音合成.md** 證明了「捨棄 RNN、用卷積並行生成」可行，但卷積感受野仍要逐層擴張。
- Transformer 論文原文的引用列表中，PixelRNN、WaveNet、ByteNet、ConvS2S 全部在列——自注意力是所有前驅線索的合流點。
- 動機：Google 翻譯團隊要「訓練快三倍、翻譯好一截」；英國團隊（Szegedy 系）則主張卷積——最後 Vaswani、Shazeer、Parmar 的「全注意力」極端方案勝出。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：Q、K、V——把記憶檢索變成矩陣運算

自注意力把每個 token 向量 $x_i$ 線性投影成三個角色：

$$Q = XW_Q, \qquad K = XW_K, \qquad V = XW_V$$

然後整個序列的「每對位置之間的注意力」一次算完：

$$\mathrm{Attention}(Q, K, V) = \mathrm{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V$$

| 物件 | 角色 | 類比 |
|---|---|---|
| $Q$ | 我想找什麼 | 查詢關鍵字 |
| $K$ | 我能被搜到什麼 | 索引標籤 |
| $V$ | 找到後取出的內容 | 資料本體 |

$\sqrt{d_k}$ 縮放因子是穩定性細節：$d_k$ 大時 $QK^\top$ 方差過大，softmax 會飽和、梯度消失——除以 $\sqrt{d_k}$ 恰好把方差歸一。

### 第二條線索：多頭注意力——八雙眼睛同時看

單頭注意力只有一種「看的方式」。Transformer 把 $d_{\text{model}}=512$ 切成 $h=8$ 個 64 維子空間，各自做注意力再拼接：

$$\mathrm{MultiHead}(Q,K,V) = \mathrm{Concat}(\mathrm{head}_1, \dots, \mathrm{head}_8)\,W^O, \qquad \mathrm{head}_i = \mathrm{Attention}(QW_i^Q, KW_i^K, VW_i^V)$$

各頭自動分工：有的頭盯語法依賴（主謂一致），有的頭做共指消解（代詞→先行詞），有的頭只看相鄰位置。這是**分佈式表徵**（見 **1985-Boltzmann機器.md**）在注意力機制上的重演：一種關係由多頭共同編碼，一個頭參與多種關係。

### 第三條線索：位置編碼——沒有循環，序從何來？

自注意力對輸入是**置換等變**的：打亂 token 順序，輸出只是相應打亂。序列資訊必須從外面注入。Transformer 用正弦位置編碼：

$$PE_{(pos, 2i)} = \sin(pos / 10000^{2i/d}), \qquad PE_{(pos, 2i+1)} = \cos(pos / 10000^{2i/d})$$

每個維度是一個不同波長的振盪器——像二進位計數器的連續版本，相對位置 $PE_{pos+k}$ 可以表示為 $PE_{pos}$ 的線性變換。這是模型「天生知道序」的唯一線索；後續案件（BERT 用學習式位置、RoPE 旋轉編碼）都在這條線索上換工具。

### 第四條線索：$O(T^2)$ 的代價——案件值與代價

| 模型 | 每層計算量 | 序列操作 | 長程路徑 |
|---|---|---|---|
| RNN / LSTM | $O(T \cdot d^2)$ | $O(T)$ 步 | $O(T)$ |
| 卷積（ByteNet） | $O(k \cdot T \cdot d^2)$ | $O(1)$ | $O(T/k)$ |
| **Self-Attention** | $O(T^2 \cdot d)$ | $O(1)$ | $O(1)$ |

自注意力用 $O(T^2)$ 換來 $O(1)$ 長程路徑與完美並行。$T$ 小時血賺；$T$ 大時 $T^2$ 是未來所有「長文本」案件的案值——FlashAttention、稀疏注意力、線性注意力都是後續回聲。

### 第五條線索：案發現場的成績——WMT14 的宣判

WMT14 機器翻譯的 BLEU 成績（越高越好）：

| 系統 | 英→德 BLEU | 英→法 BLEU | 訓練成本 |
|---|---|---|---|
| GNMT（Google，LSTM） | 24.6 | 39.9 | 96 顆 GPU × 6 天 |
| ConvS2S（Facebook，卷積） | 25.2 | 40.5 | 512 顆 GPU × 1 天 |
| **Transformer（base / big）** | **27.3 / 28.4** | **41.0 / 41.8** | 8 顆 GPU × 3.5 天 |

Transformer big 以**十分之一的算力**超越兩大陣營——BLEU 提升 3.8 分在機器翻譯史上是斷崖級跳升。消融實驗進一步宣判：拿掉多頭（改單頭）掉 0.9 BLEU、拿掉 $\sqrt{d_k}$ 縮放導致訓練不穩、拿掉位置編碼 BLEU 崩至 8.3（模型完全不知道序）。線索至此全部合攏：**QKV 注意力 + 多頭 + 位置編碼，缺一不可**——2017 年 6 月的法庭判決書就此簽署。

## 結案 -- 後果與影響

- WMT14 英德翻譯 BLEU 28.4、英法 41.8，大幅超越所有 RNN/卷積系統，且訓練只需 3.5 天（8 顆 GPU）。
- 架構一分為二：
  - **只留編碼器** → **2018-BERT與GPT預訓練典範.md** 的 BERT（雙向理解）。
  - **只留解碼器** → GPT 系列的骨架（自回歸生成），見 **2019-GPT-2危險模型.md**、**2020-GPT-3規模湧現.md**。
- 注意力機制從翻譯補丁升格為通用計算原語：影像（**2021-ViT視覺Transformer.md**）、圖文對齊（**2021-CLIP多模態對齊.md**）、蛋白質（**2021-AlphaFold2.md** 的 Evoformer）全部注意力化。
- 序列建模的權杖正式從 LSTM 轉交 Transformer——神經網路通史的分水嶺（見「科學與歷史/神經網路/2017-瓦茲瓦尼Transformer.md」）。
- $O(T^2)$ 伏筆：上下文長度之戰（長上下文、檢索增強、FlashAttention）成為此後十年的持續案件。
- 規模化伏筆：架構已備、並行已通，只差資料與參數——「規模即智慧」的下一案即將開庭。

## 關鍵人物與文獻

- **Ashish Vaswani**：第一作者，主導「全注意力」架構。
- **Noam Shazeer**：多頭注意力與架構調校的關鍵人物，後續多個 Transformer 變體之父。
- **Jakob Uszkoreit**：提出捨棄 RNN 的核心主張。
- Vaswani et al., *Attention Is All You Need*, NIPS 2017, arXiv:1706.03762。
- Bahdanau et al., *Neural Machine Translation by Jointly Learning to Align and Translate*, 2014（前驅注意力）。
- Sutskever et al., *Sequence to Sequence Learning with Neural Networks*, 2014。
- He et al., *Deep Residual Learning*, 2015（殘差連接的借用）。
- 相關案件：**2014-Seq2Seq與注意力.md**、**2016-WaveNet語音合成.md**、**2018-BERT與GPT預訓練典範.md**、**2021-ViT視覺Transformer.md**、**2021-AlphaFold2.md**
