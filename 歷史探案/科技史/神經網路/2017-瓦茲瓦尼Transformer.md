# 2017 - Vaswani Transformer（注意力就是一切）

## 案件摘要
2017 年，**Ashish Vaswani** 等人（Google Brain/Research，八人團隊）在 NIPS 發表
*Attention Is All You Need*，提出 **Transformer**：
$$\boxed{\text{捨棄遞迴與卷積——只用注意力（self-attention）}}$$
**核心公式**是縮放點積注意力（scaled dot-product attention）：
$$\text{Attention}(Q, K, V) = \text{softmax}\!\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$
- $Q$（query，查詢）、$K$（key，鍵）、$V$（value，值）——全部從**同一個序列**來（self-attention）；
- 除以 $\sqrt{d_k}$：防止點積過大、softmax 飽和、梯度消失；
- **多頭注意力**：$h$ 組平行的注意力，各自看不同的「子空間」：
  $$\text{MultiHead}(Q,K,V) = \text{Concat}(\text{head}_1, \dots, \text{head}_h)W^O.$$
- **位置編碼**：因為捨棄遞迴，序列的「順序」必須額外注入：
  $$PE_{(pos, 2i)} = \sin(pos/10000^{2i/d_{model}}), \quad PE_{(pos, 2i+1)} = \cos(pos/10000^{2i/d_{model}}).$$
**訓練快 10 倍**（平行化，無序列依賴）——**這是 NLP 的「創世紀」**，
七年後變成了 GPT 與 ChatGPT（見 `2020-布朗GPT-3.md`、`2022-ChatGPT大型語言模型.md`）。

## 前因 -- 為什麼會有這個案子
- **LSTM 的瓶頸（1997–2016）**：
  **1997 年 LSTM**（見 `1997-長短期記憶LSTM.md`）用**門控記憶**處理長序列，
  是 2016 年之前機器翻譯、語音辨識的主流。
  但 LSTM 是**遞迴**的：$h_t = f(h_{t-1}, x_t)$——
  **第 $t$ 步必須等第 $t-1$ 步**，無法平行計算：
  $$\text{LSTM：序列依賴} \xrightarrow{\text{GPU 時代的痛}} \text{訓練慢、長依賴仍會遺忘}.$$
  而且任意兩個遠距離 token 的資訊必須**一步步傳遞**（路徑長度 $O(n)$）。
- **詞向量的地基（2013）**：
  **2013 年 word2vec**（見 `2013-米科洛夫詞向量.md`）把詞變成向量
  （$king - man + woman \approx queen$），讓 NLP 有了**可計算的語義空間**——
  但 word2vec 是**靜態**的：一個詞只有一個向量，無視上下文
  （「蘋果」在「吃蘋果」與「蘋果手機」中意義不同）。
  $$\text{word2vec：靜態詞向量} \xrightarrow{\text{Transformer：動態上下文}} \text{語義的革命}.$$
- **Bahdanau attention 的先聲（2015）**：
  **Bahdanau 等（2015）** 在 seq2seq 翻譯中加入**注意力**：
  解碼器每一步「回頭看」編碼器的全部隱狀態，**加權對齊**源語言與目標語言——
  翻譯品質大增。
  $$\text{attention（2015）：附屬零件} \xrightarrow{\text{Transformer（2017）：唯一主角}} \text{地位的逆轉}.$$
  **Vaswani 等的洞察**：既然注意力這麼好用——
  $$\boxed{\text{「Attention is all you need」——把遞迴整個丟掉！}}$$
- **論文標題的豪氣**：
  這是深度學習史上最「挑釁」的標題之一——
  審稿人一度認為太激進；七年後，這篇論文被引用**超過 10 萬次**，
  **八位作者全部離開 Google 創業**（AI 新創的黃金班底）。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：self-attention 的縮放點積
**單頭注意力**：給定序列的 $Q, K, V \in \mathbb{R}^{n \times d_k}$：
$$\text{Attention}(Q, K, V) = \text{softmax}\!\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$
**逐步拆解**：
1. **相容度**：$e_{ij} = q_i \cdot k_j / \sqrt{d_k}$——token $i$ 對 token $j$ 的「關注程度」；
2. **歸一化**：$\alpha_{ij} = \text{softmax}(e_{i\cdot})_j = \frac{e^{e_{ij}}}{\sum_j e^{e_{ij}}}$——注意力權重（每列和為 1）；
3. **加權求和**：$\text{output}_i = \sum_j \alpha_{ij} v_j$——token $i$ 的新表示。
$$\boxed{\text{每個 token 的新表示 = 全序列的加權平均（權重由內容決定）}}$$
**為什麼除以 $\sqrt{d_k}$**：若 $q, k$ 的分量是均值 0、變異數 1 的隨機變數，
則 $q \cdot k$ 的變異數是 $d_k$——$d_k$ 大時 softmax 飽和、梯度消失。
$$\text{Var}(q \cdot k) = d_k \quad\Longrightarrow\quad \text{除以 } \sqrt{d_k} \text{ 使變異數回到 } 1.$$

### 第二條線索：多頭注意力與位置編碼
**多頭**：$h$ 組獨立的 $W_i^Q, W_i^K, W_i^V$（投影到較低維 $d_k = d_{model}/h$）：
$$\text{head}_i = \text{Attention}(QW_i^Q, KW_i^K, VW_i^V), \quad \text{MultiHead} = \text{Concat}(\text{head}_1, \dots, \text{head}_h)W^O.$$
- **每頭看不同的關係**：有的頭看語法（主詞-動詞）、有的看語義（指代）——
  **注意力的「分工合作」**。
**位置編碼**：捨棄遞迴後，attention 對順序**完全無感**（排列不變）——
必須把位置資訊**加進輸入**：
$$PE_{(pos, 2i)} = \sin(pos/10000^{2i/d_{model}}), \quad PE_{(pos, 2i+1)} = \cos(pos/10000^{2i/d_{model}})$$
- **不同頻率的 sin/cos**：像「時鐘的指針」——低頻記大位置、高頻記小位置；
- $PE_{pos+k}$ 是 $PE_{pos}$ 的**線性變換**（旋轉）——模型容易學「相對位置」。

### 第三條線索：手算級的 attention 例子
3 個 token、維度 4，手算級的 scaled dot-product attention——
**觀察重點**：注意力權重每列和為 1，輸出是 $V$ 的加權平均。

### Python：純 Python 實作 scaled dot-product attention

```python
# 純 Python 實作：3 token、維度 4 的 scaled dot-product attention
import math

def matmul(A, B):
    """矩陣乘法"""
    return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))]
            for i in range(len(A))]

def transpose(A):
    return [[A[i][j] for i in range(len(A))] for j in range(len(A[0]))]

def softmax_row(v):
    m = max(v)
    e = [math.exp(x-m) for x in v]
    s = sum(e)
    return [x/s for x in e]

def attention(Q, K, V):
    """Attention(Q,K,V) = softmax(QK^T/sqrt(d_k)) V"""
    d_k = len(K[0])
    scores = matmul(Q, transpose(K))
    scaled = [[x/math.sqrt(d_k) for x in row] for row in scores]
    weights = [softmax_row(row) for row in scaled]
    out = matmul(weights, V)
    return weights, out

# 3 個 token（「我」、「愛」、「AI」）、維度 4
# 手算級的 Q, K, V（簡化數字，便於驗證）
Q = [[2, 0, 1, 0],
     [0, 2, 2, 1],
     [1, 1, 0, 2]]
K = [[1, 1, 0, 1],
     [2, 0, 1, 0],
     [0, 1, 2, 0]]
V = [[1, 0, 0, 1],
     [0, 2, 1, 0],
     [1, 1, 0, 2]]

weights, out = attention(Q, K, V)

print("scaled dot-product attention（3 tokens，d_k = 4）")
print("token 順序：[我, 愛, AI]\n")
print("注意力權重（每列和 = 1）：")
for i, wrow in enumerate(weights):
    toks = ["我", "愛", "AI"]
    parts = [f"{t}:{w:.4f}" for t, w in zip(toks, wrow)]
    print(f"  {toks[i]} → [ {'  '.join(parts)} ]  (sum={sum(wrow):.4f})")

print("\n輸出（V 的加權平均）：")
for i, row in enumerate(out):
    toks = ["我", "愛", "AI"]
    print(f"  {toks[i]} → {['%.4f' % x for x in row]}")

print("\n驗證：softmax(QK^T/sqrt(d_k)) 的縮放效果")
raw = matmul(Q, transpose(K))
for i in range(3):
    print(f"  token {i}: 原始分數 {[x for x in raw[i]]} → 縮放後 {[round(x/math.sqrt(4),4) for x in raw[i]]}")
```
輸出：
```
scaled dot-product attention（3 tokens，d_k = 4）
token 順序：[我, 愛, AI]

注意力權重（每列和 = 1）：
  我 → [ 我:0.1543  愛:0.6914  AI:0.1543 ]  (sum=1.0000)
  愛 → [ 我:0.1643  愛:0.0996  AI:0.7361 ]  (sum=1.0000)
  AI → [ 我:0.6285  愛:0.2312  AI:0.1402 ]  (sum=1.0000)

輸出（V 的加權平均）：
  我 → ['0.3086', '1.5372', '0.6914', '0.4628']
  愛 → ['0.9004', '0.9354', '0.0996', '1.6365']
  AI → ['0.7688', '0.6027', '0.2312', '0.9090']

驗證：softmax(QK^T/sqrt(d_k)) 的縮放效果
  token 0: 原始分數 [2, 5, 2] → 縮放後 [1.0, 2.5, 1.0]
  token 1: 原始分數 [3, 2, 6] → 縮放後 [1.5, 1.0, 3.0]
  token 2: 原始分數 [4, 2, 1] → 縮放後 [2.0, 1.0, 0.5]
```

## 結案 -- 後果與影響
- **NLP 的統一（2017）**：
  $$\boxed{\text{Transformer 統一了 NLP——遞迴退場，注意力稱王}}$$
  機器翻譯、問答、摘要——全部換成 Transformer 架構；
  LSTM 在工業界**幾乎絕跡**（只剩長序列的小眾場景）。
- **GPT 與 BERT 的誕生（2018）**：
  - **GPT-1（2018，OpenAI）**：Transformer 的**解碼器** + 自迴歸語言模型——
    「**預測下一個詞**」（見 `2020-布朗GPT-3.md`）；
  - **BERT（2018，Google）**：Transformer 的**編碼器** + 遮罩語言模型——
    「**完形填空**」；
  $$\text{Transformer（2017）} \xrightarrow{\text{拆兩半}} \text{GPT（解碼器）} + \text{BERT（編碼器）}.$$
- **GPT-3 與規模法則（2020）**：
  **GPT-3（2020）** 用 1750 億參數的 Transformer 解碼器，
  展示 **in-context learning**（見 `2020-布朗GPT-3.md`）——
  **規模（scale）就是能力**。
- **ChatGPT 與大型語言模型時代（2022）**：
  Transformer + RLHF = **ChatGPT**（見 `2022-ChatGPT大型語言模型.md`）——
  $$\text{Transformer（2017）} \xrightarrow{} \text{GPT-3（2020）} \xrightarrow{} \text{ChatGPT（2022）}.$$
  **兩個月破億使用者**——史上最快的消費級應用。
- **工程遺產**：
  - **2018 圖靈獎**頒給 Hinton、LeCun、Bengio（深度學習）——
    Transformer 是這場革命的**極盛期**；
  - **2024 諾貝爾物理獎**（Hinton、Hopfield）與**化學獎**（Hassabis、Jumper，AlphaFold）
    ——AI 全面滲透科學；
  - Transformer 也征服了**影像（ViT，2020）**、**語音（Whisper，2022）**、**蛋白質（AlphaFold2，2021）**。
- 歷史定位：**Vaswani 等八人改寫了 NLP 的歷史**——
  他們把 2015 年的附屬零件（attention）變成唯一主角；
  $$\text{LSTM（1997）} \xrightarrow{} \text{attention（2015）} \xrightarrow{} \text{Transformer（2017）} \xrightarrow{} \text{LLM（2020–）}.$$
  **八行公式，統一了語言**。

## 關鍵人物與文獻
- **A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, Ł. Kaiser, I. Polosukhin**：*Attention Is All You Need*（NIPS 2017）。
- **M. Bahdanau**：神經機器翻譯的注意力（2015）——Transformer 的先聲。
- **S. Hochreiter 與 J. Schmidhuber**：LSTM（1997）——被取代的前王朝（見 `1997-長短期記憶LSTM.md`）。
- **T. Mikolov**：word2vec（2013）——詞向量的地基（見 `2013-米科洛夫詞向量.md`）。
- **J. Devlin**：BERT（2018）——Transformer 編碼器的應用。
- **A. Radford**：GPT-1（2018）、GPT-2（2019）、GPT-3（2020）——Transformer 解碼器的王朝。
- 相關案件：`1997-長短期記憶LSTM.md`、`2013-米科洛夫詞向量.md`、`2020-布朗GPT-3.md`、`2022-ChatGPT大型語言模型.md`、`../資訊科學/1936-圖靈機.md`。
