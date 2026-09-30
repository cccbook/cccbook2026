# 2018 - BERT 與 GPT 預訓練典範（先學語言，再學任務）

## 案件摘要
2018 年，兩篇論文確立 NLP 的新典範——**預訓練 + 微調**：
- **GPT** (OpenAI, Radford 等)：Transformer 解碼器 + 自回歸訓練——預測下一個詞。
- **BERT** (Google, Devlin 等)：Transformer 編碼器 + 掩碼訓練——完形填空。
$$\text{GPT: } P(x_t | x_{<t}) \qquad \text{BERT: } P(x_{\text{mask}} | x_{\text{其餘}}).$$
在無標註文本上先學語言的「通識」，再用少量標註微調特定任務——NLP 的 ImageNet 時刻（見「2012-AlexNetImageNet革命.md」）。

## 前因 -- 為什麼會有這個案子
- **NLP 的困境**：每個任務（分詞、NER、問答、翻譯）都要單獨的標註資料與模型——**標註昂貴、無法通用**。
- **詞向量的先驅線索**：
  - **Word2Vec（2013）**：用「上下文相似」學出詞向量，詞義可算——$v_{king} - v_{man} + v_{woman} \approx v_{queen}$。
  - **ELMo（2018）**：雙向 LSTM 的上下文相關向量——但仍是 LSTM（無法並行）。
- **Transformer 的到來（2017）**：架構就位（見「2017-Transformer注意力機制.md」）——只缺「怎麼用無標註資料訓練」。
- **兩個陣營的分岔**：OpenAI 押注**自回歸**（預測下一詞，天然適合生成）；Google 押注**掩碼**（雙向理解，適合分類與理解）——兩條路線都成功，但日後 GPT 路線（生成）統治了世界。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：GPT 的自回歸訓練
Transformer 解碼器（帶因果遮罩），最大化下一詞的似然：
$$L = -\sum_t \log P(x_t \mid x_{<t}; \theta).$$
因果遮罩 (causal mask) 使位置 $t$ 只能看 $< t$——訓練與生成完全一致：
$$x_{<t} \xrightarrow{\text{Transformer}} \text{softmax} \xrightarrow{\text{取樣}} x_t.$$
**「預測下一個詞」看似簡單，但要預測得好，必須學會語法、語義、事實、甚至推理**——這是大語言模型哲學的核心。

### 第二條線索：BERT 的掩碼訓練
隨機遮住 15% 的詞，用雙向上下文預測：
$$L = -\sum_{t \in M} \log P(x_t \mid x_{\setminus M}; \theta).$$
雙向注意力看見前後文——理解任務（問答、NER）表現極強，但**無法直接生成**。

### 第三條線索：微調與湧現
預訓練（海量無標註）→ 微調（少量標註）：
$$\theta_{\text{通用}} \xrightarrow{\text{任務資料}} \theta_{\text{特定}}.$$
模型規模放大後，**湧現能力** (emergent ability) 出現：不經微調、僅靠提示 (prompt) 就能完成新任務——**零樣本/少樣本學習**，通往 ChatGPT 的橋樑。

### Python：自回歸訓練與掩碼訓練的縮影

```python
import torch, torch.nn as nn

vocab = {"<pad>":0, "我":1, "愛":2, "NLP":3}
d = 16
emb = nn.Embedding(len(vocab), d)
head = nn.Linear(d, len(vocab))

# GPT 式：預測下一詞（因果）
tokens = torch.tensor([[1, 2, 3]])
x = emb(tokens)
mask = torch.triu(torch.ones(3,3), 1).bool()        # 上三角遮罩
h = x + torch.where(mask.unsqueeze(-1), torch.tensor(0.), x*0)   # 簡化示範
logits = head(x)
loss_gpt = nn.functional.cross_entropy(logits[0,:-1], tokens[0,1:])
print("GPT 下一詞損失:", round(loss_gpt.item(), 3), "→ 學習預測 x_t | x_{<t}")

# BERT 式：完形填空（雙向）
tokens_m = torch.tensor([[1, 0, 3]])                # 遮住「愛」
logits_m = head(emb(tokens_m))
loss_bert = nn.functional.cross_entropy(logits_m[0,1], torch.tensor([2]))
print("BERT 掩碼損失:", round(loss_bert.item(), 3), "→ 學習預測 x_mask | 其餘")
```
輸出：
```
GPT 下一詞損失: 1.812 → 學習預測 x_t | x_{<t}
BERT 掩碼損失: 1.773 → 學習預測 x_mask | 其餘
```

## 結案 -- 後果與影響
- **NLP 範式革命**：2018 年後，預訓練 + 微調成為標準；任務專用模型被謀殺。
- **GPT 路線的勝利**：GPT-2（2019, 1.5B）展示零樣本能力；GPT-3（2020, 175B）確立規模法則；GPT-3.5 + RLHF = ChatGPT（見「2022-ChatGPT與RLHF.md」）——**生成路線統治世界**。
- **規模法則 (Scaling Laws)**：Kaplan 等（2020）證明損失隨參數/資料/算力的冪律下降：
  $$L \propto N^{-\alpha}, \quad L \propto D^{-\beta}.$$
  「加大規模就能更好」成為工程信仰，引發算力軍備競賽。
- **詞向量的遺產**：Word2Vec 的「詞義可算」思想在 Transformer 中升級為「上下文相關表示」。
- 歷史定位：BERT 與 GPT 是 Transformer（2017）的第一代後裔——**同一個祖先，兩條路線，最後生成路線勝出**。

## 關鍵人物與文獻
- **A. Radford 等**：〈Improving Language Understanding by Generative Pre-Training〉(GPT, 2018)；GPT-2 (2019)。
- **J. Devlin 等**：〈BERT: Pre-training of Deep Bidirectional Transformers...〉, NAACL (2019)。
- **T. Mikolov 等**：Word2Vec, NeurIPS (2013)；**Kaplan 等**：Scaling Laws (2020)。
- 相關案件：`2017-Transformer注意力機制.md`、`2022-ChatGPT與RLHF.md`。
