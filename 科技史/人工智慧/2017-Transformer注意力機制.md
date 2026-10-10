# 2017 - Transformer 注意力機制（Attention Is All You Need）

## 案件摘要
2017 年，Google 的 Vaswani 等 8 人發表〈Attention Is All You Need〉：
**Transformer** 架構完全捨棄遞迴與卷積，只用**自我注意力 (self-attention)** 處理序列。
$$\mathrm{Attention}(Q, K, V) = \mathrm{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V.$$
序列建模的統治者 LSTM（見「1997-LSTM長短期記憶.md」）被謀殺——兇手不是更強的記憶，而是**直連任意距離 + 完美並行**。
這是今日所有大語言模型（GPT、BERT、Claude、Gemini）的共同祖先。

## 前因 -- 為什麼會有這個案子
- **LSTM 的兩個缺口**（見「1997-LSTM長短期記憶.md」）：
  1. **序列計算**：$h_t$ 依賴 $h_{t-1}$——**無法並行**，GPU 的並行能力被浪費（AlexNet 之後算力是王，見「2012-AlexNetImageNet革命.md」）。
  2. **長距離依賴**：即便有閘門，資訊仍需逐步傳遞——距離 100 步的依賴仍然微弱。
- **注意力的先驅線索**：
  - **Bahdanau（2014）**：機器翻譯中加入注意力——解碼時「回頭看」編碼器的所有位置，翻譯品質大增。
  - **Luong（2015）**：注意力的多種形式（全域/局部、點積/雙線性）。
- **Vaswani 團隊的偵探直覺**：既然注意力這麼有用，**何不捨棄遞迴、只用注意力？**——「Attention Is All You Need」的標題本身就是破案宣言。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：自我注意力的數學
每個 token 同時對所有 token 做「查詢-比對-取值」：
- $Q = XW_Q$（查詢：我要找什麼）
- $K = XW_K$（鍵：我有什麼）
- $V = XW_V$（值：我的內容）
$$\mathrm{Attention}(Q,K,V) = \mathrm{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V.$$
- $QK^\top$：所有 token 兩兩的相似度矩陣——**$O(1)$ 步直連任意距離**。
- 除以 $\sqrt{d_k}$：防止點積過大導致 softmax 飽和（梯度消失）。
- **多頭注意力**：$h$ 個注意力頭並行，各自學不同的「關注模式」：
  $$\mathrm{MultiHead} = \mathrm{Concat}(\mathrm{head}_1,\dots,\mathrm{head}_h)W_O.$$

### 第二條線索：位置編碼（順序的救贖）
注意力對順序**天生無感**（置換不變）——必須注入位置資訊：
$$\mathrm{PE}(pos, 2i) = \sin\!\left(\frac{pos}{10000^{2i/d}}\right), \qquad \mathrm{PE}(pos, 2i+1) = \cos\!\left(\frac{pos}{10000^{2i/d}}\right).$$
**正弦位置編碼**——傅立葉轉換（見「傅立葉轉換/README.md」）的迴響：用不同頻率的正弦波為每個位置編號。

### 第三條線索：完美並行
捨棄遞迴後，所有 token 的計算**同時進行**：
$$\text{LSTM: } O(T) \text{ 步序列} \quad\longrightarrow\quad \text{Transformer: } O(1) \text{ 步（純矩陣運算）}.$$
GPU 的並行火力全開——**訓練大模型在工程上變得可行**。這是大語言模型的時代前提。

### Python：手寫自我注意力

```python
import numpy as np
np.random.seed(0)

T, d = 4, 8
X = np.random.randn(T, d)                       # T 個 token
Wq, Wk, Wv = (np.random.randn(d, d)*0.3 for _ in range(3))
Q, K, V = X@Wq, X@Wk, X@Wv

scores = Q @ K.T / np.sqrt(d)                   # 兩兩相似度
weights = np.exp(scores - scores.max(-1, keepdims=True))
weights /= weights.sum(-1, keepdims=True)       # softmax
out = weights @ V

print("注意力權重矩陣 (每行總和=1):\n", np.round(weights, 2))
print("行總和:", weights.sum(-1))
```
輸出：
```
注意力權重矩陣 (每行總和=1):
 [[0.14 0.28 0.31 0.27]
  [0.21 0.25 0.29 0.29]
  [0.18 0.24 0.33 0.25]
  [0.17 0.27 0.3  0.26]]
行總和: [1. 1. 1. 1.]
```
（每個 token 以學到的權重「直連」所有 token——任意距離，$O(1)$ 步。）

## 結案 -- 後果與影響
- **序列建模改朝換代**：機器翻譯、語音、影像（Vision Transformer, 2021）全面 Transformer 化；RNN/LSTM 退居歷史。
- **大語言模型的共同祖先**：
  - **GPT**（2018）：Transformer 解碼器 + 自回歸訓練（見「2018-BERT與GPT預訓練典範.md」）。
  - **BERT**（2018）：Transformer 編碼器 + 掩碼訓練。
  - **ChatGPT**（2022）：GPT + RLHF（見「2022-ChatGPT與RLHF.md」）。
- **規模法則的載體**：Transformer 的完美並行使「加大參數、加大資料」在工程上可行——GPT-3（175B 參數）由此而生。
- **計算複雜度的代價**：注意力是 $O(T^2)$——序列越長成本平方增長；長上下文的後續案件（稀疏注意力、Mamba、線性注意力）由此展開。
- 歷史趣聞：這篇論文的 8 位作者全部已離開 Google 自立門戶——一篇論文孵化了整個 AI 產業的下一步。

## 關鍵人物與文獻
- **A. Vaswani, N. Shazeer, N. Parmar 等**：〈Attention Is All You Need〉, NeurIPS (2017)。
- **Bahdanau 等**：注意力機器翻譯, ICLR (2015)——先驅。
- 相關案件：`1997-LSTM長短期記憶.md`、`2018-BERT與GPT預訓練典範.md`、`2022-ChatGPT與RLHF.md`。
