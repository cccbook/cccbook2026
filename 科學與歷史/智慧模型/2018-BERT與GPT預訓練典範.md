# 2018 - BERT 與 GPT 預訓練典範

## 案件摘要

2018 年是 NLP 的「ImageNet 元年」：兩篇論文在半年內各自宣判——6 月 OpenAI 的 **GPT-1**、10 月 Google 的 **BERT**。兩者共享同一骨架（2017 年 Transformer）與同一信條（**預訓練 + 微調**），卻選了兩條互相排斥的訓練目標：

$$\text{GPT（自回歸）:} \quad \mathcal{L} = \sum_{i} \log p(x_i \mid x_{<i}) \qquad\qquad \text{BERT（掩碼）:} \quad \mathcal{L} = \sum_{i \in M} \log p(x_i \mid x_{\setminus M})$$

GPT 是 Transformer 解碼器的語言化：從左到右逐字預測。BERT 是 Transformer 編碼器的語言化：遮住 15% 的字，用**雙向上下文**猜出被遮的字。這是「雙向理解 vs 自回歸生成」的百年之爭的開庭日。

## 前因 -- 為什麼會有這個案子

- **2013-米科洛夫詞向量.md**（word2vec）已證明「無監督預訓練詞向量 + 微調」有效，但詞向量是**靜態**的：一詞一向量，無法處理多義（bank 是銀行還是河岸？）。
- **2017-Transformer注意力機制.md** 交出了完美並行 + 直連長程的骨架——只差「拿來做什麼任務」。
- NLP 的長年困境：標註資料稀缺，每個任務（分詞、NER、問答）都要單獨從頭訓練——與影像界的 ImageNet 預訓練形成殘酷對比。
- 前驅線索：Dai & Le（2015）用 LSTM 做語言模型預訓練；ULMFiT（Howard & Ruder, 2018 年 1 月）確立「預訓練—微調」三步流程——但骨架還是 LSTM。
- ELMo（Peters et al., 2018 年 2 月）做出**上下文相關**詞向量（雙向 LSTM 拼接），但只是特徵拼接，不是端對端微調。
- 動機：OpenAI 想證明「生成式語言模型 + 規模」是通向 AGI 的路；Google 想證明「雙向理解」才是語言的本質——兩條路線的意識形態之爭正式開打。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：GPT——Transformer 解碼器的語言化

GPT-1 是 12 層 Transformer 解碼器（掩碼自注意力），在 BooksCorpus（約 7,000 本書）上做**從左到右的語言模型**：

$$p(x) = \prod_{i=1}^{T} p(x_i \mid x_1, \dots, x_{i-1}; \Theta), \qquad \mathcal{L}_{\text{LM}} = -\sum_i \log p(x_i \mid x_{<i})$$

訓練完後，微調時在最後加一個線性層做下游任務，損失混合：

$$\mathcal{L} = \mathcal{L}_{\text{task}} + \lambda \, \mathcal{L}_{\text{LM}}$$

GPT-1 在 12 項任務中 9 項刷新 SOTA。關鍵主張：**語言模型本身就在學「理解」**——預測下一個字需要語法、語義、常識的全部知識。

### 第二條線索：BERT——掩碼語言模型與雙向性

GPT 的自回歸只能看左邊；BERT 主張理解需要**雙向**。但雙向 + 自回歸 = 自己看見答案（洩題）。BERT 的解法是**掩碼語言模型（MLM）**：

- 隨機遮住 15% 的 token（80% 換 `[MASK]`、10% 換隨機詞、10% 保留）
- 用整個（雙向）上下文預測被遮的 token

$$\mathcal{L}_{\text{MLM}} = -\sum_{i \in M} \log p(x_i \mid x_{\setminus M}; \Theta)$$

加上**下一句預測（NSP）**：判斷句子 B 是否真的跟在 A 後面——給模型句際關係的線索。

### 第三條線索：兩條路線的對照表

| | **GPT-1** | **BERT** |
|---|---|---|
| 骨架 | Transformer 解碼器（12 層） | Transformer 編碼器（12/24 層） |
| 目標 | 自回歸 $\log p(x_i \mid x_{<i})$ | 掩碼 $\log p(x_i \mid x_{\setminus M})$ |
| 上下文 | 單向（左→右） | 雙向 |
| 擅長 | 生成、續寫 | 理解、分類、問答 |
| 資料 | BooksCorpus ~5GB | BooksCorpus + Wikipedia ~16GB |
| 參數 | 117M | 340M (LARGE) |

線索至此合攏：**兩者都是「無監督預訓練 + 微調」典範的 Transformer 實現**——差別只是掩碼的形狀。而這個差別決定了此後的意識形態分岔：BERT 稱霸理解榜，GPT 走向生成與規模。

### 第四條線索：[CLS] 與句子嵌入——理解任務的統一介面

BERT 在輸入前加一個特殊 token `[CLS]`，其最終隱狀態 $\mathbf{h}_{[\text{CLS}]}$ 被用作整句的表示，餵入分類器。加上 `[SEP]` 分隔句對，BERT 用**同一個模型**統一了分類、問答、NLI、命名實體識別——11 項 NLP 任務全部 SOTA，GLUE 榜單直接碾壓（+7.7 分）。這是「一個模型、所有任務」的預訓練典範正式加冕。

### 第五條線索：成績單——兩條路線的第一次交鋒

GLUE 榜與代表性任務的成績（2018 年底）：

| 任務 | ELMo（特徵拼接） | GPT-1 | **BERT-LARGE** |
|---|---|---|---|
| MNLI（推論） | 80.7 | 82.1 | **86.7** |
| SQuAD v1.1（問答 F1） | 85.8 | 88.1 | **93.2** |
| CoLA（語法接受度） | 35.0 | 45.4 | **52.1** |
| GLUE 總分 | 79.3 | 82.3 | **80.5 → 微調後 82.1+** |

線索至此全部合攏：ELMo 是特徵拼接（半吊子），GPT-1 是單向自回歸（理解受限），BERT 以**雙向 + 掩碼**雙殺——2018 年的意識形態法庭，第一次判決是 BERT 勝訴。但判決書中藏著一枚未爆彈：GPT-1 的自回歸路線只是「參數與資料都不夠」——這枚彈在 2019、2020 年兩案中相繼引爆。

## 結案 -- 後果與影響

- NLP 的 ImageNet 時刻：2018 年底起，「先預訓練、再微調」成為 NLP 的標準流程，工程師再也不從頭訓練模型。
- BERT 系後續：RoBERTa（2019，去掉 NSP、加倍資料）、ALBERT、DistilBERT——理解榜的軍備競賽；中文界有 BERT-wwm、MacBERT。
- GPT 系後續：GPT-1 的自回歸路線被 OpenAI 堅持到底——**2019-GPT-2危險模型.md** 的零樣本能力、**2020-GPT-3規模湧現.md** 的 in-context learning，最後通往 **2022-ChatGPT與RLHF.md**。
- 意識形態之爭的判詞：BERT 贏了理解榜，但輸了未來——生成式路線才能「無限續寫、任務自由」，掩碼式被鎖死在固定任務上。
- 預訓練典範外溢到全領域：語音（wav2vec 2.0）、影像（**2021-ViT視覺Transformer.md** 的 MAE 掩碼預訓練）、蛋白質（**2021-AlphaFold2.md** 與 ESM 語言模型）全部「先預訓練」。
- 伏筆：GPT-1 只有 117M 參數、只做微調——當參數再大一個數量級，「微調」本身將被淘汰，取而代之的是**零樣本**與**提示**。

## 關鍵人物與文獻

- **Alec Radford**（OpenAI）：GPT-1 的第一作者，GPT 系列的開山者。
- **Jacob Devlin**（Google）：BERT 的第一作者。
- Radford et al., *Improving Language Understanding by Generative Pre-Training*, OpenAI, 2018。
- Devlin et al., *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*, NAACL 2019, arXiv:1810.04805。
- Peters et al., *Deep Contextualized Word Representations*（ELMo）, 2018。
- Howard & Ruder, *Universal Language Model Fine-tuning*（ULMFiT）, ACL 2018。
- Mikolov et al., *Efficient Estimation of Word Representations*（word2vec）, 2013。
- 相關案件：**2017-Transformer注意力機制.md**、**2019-GPT-2危險模型.md**、**2021-ViT視覺Transformer.md**、**2022-ChatGPT與RLHF.md**（見「科學與歷史/人工智慧/」）
