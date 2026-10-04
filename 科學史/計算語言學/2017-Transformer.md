# 2017-Transformer

## 案件摘要

2017 年 6 月，Google Brain 與 Google Research 的八位作者——Ashish Vaswani、Noam Shazeer、Niki Parmar、Jakob Uszkoreit、Llion Jones、Aidan Gomez、Łukasz Kaiser、Illia Polosukhin——在 arXiv 投下一份大膽的起訴書：《Attention Is All You Need》（NeurIPS 2017）。被告是統治序列建模二十年的循環網路：RNN 的順序計算讓 GPU 無法平行運轉，是效率之罪。他們的破案宣言是：序列建模不需要循環、也不需要卷積，注意力就夠了。證據是 Transformer 在 WMT14 英德翻譯上以 BLEU 28.4 打破紀錄，且訓練僅需 12 小時——用不到前紀錄系統幾分之一的算力。

## 前因 -- 為什麼會有這個案子

- RNN/LSTM 的隱狀態 $h_t$ 依賴 $h_{t-1}$，計算本質上順序執行，GPU 大量時間在等待，無法用資料平行換取規模。
- ConvS2S（Gehring 等，2017）用卷積實現可平行訓練，但長距離依賴需要堆疊多層才能讓兩個遠距詞「相見」，路徑長度 O(log n)。
- Self-Attention 已嶄露頭角：Cheng 等（2016）與 Parikh 等（2016）證明注意力本身可承擔表示任務、不需 RNN。
- Jakob Uszkoreit 提出用自注意力取代整個遞迴的想法，團隊目標是證明「注意力就夠了」。

## 線索與推理 -- 數學式、程式、理論

### 線索一：Scaled Dot-Product Attention

查詢 $Q$、鍵 $K$、值 $V$ 皆為矩陣。注意力是「用 $Q$ 去比對 $K$、再按相似度加權 $V$」：

$$
\text{Attention}(Q, K, V) = \text{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V
$$

### 線索二：為什麼要除以 sqrt(d_k)

設 $q, k \in \mathbb{R}^{d_k}$ 各分量獨立、均值 0、方差 1，則點積方差隨維度線性增長：

$$
q \cdot k = \sum_{i=1}^{d_k} q_i k_i, \qquad \operatorname{Var}(q \cdot k) = d_k
$$

未縮放的大點積會把 softmax 推入飽和區、梯度趨近於零；除以 $\sqrt{d_k}$ 使方差回到 1，維持 softmax 梯度健康。

### 線索三：Multi-Head Attention

單頭注意力平均化了所有資訊。多頭把 $d_{\text{model}}$ 切成 $h$ 個子空間，各頭獨立做注意力再拼接：

$$
\text{MultiHead}(Q,K,V) = \text{Concat}(\text{head}_1, \dots, \text{head}_h) W^O, \quad \text{head}_i = \text{Attention}(QW_i^Q, KW_i^K, VW_i^V)
$$

Transformer 用 $h=8$、$d_k = d_v = d_{\text{model}}/h = 64$：每個頭在不同子空間學不同的語義關係（語法依賴、指代、鄰近性），是子空間的平行語義。

### 線索四：Sinusoidal 位置編碼

注意力本身對順序無感（置換等變），必須注入位置資訊：

$$
PE_{(pos,\,2i)} = \sin\!\left(\frac{pos}{10000^{2i/d}}\right), \qquad PE_{(pos,\,2i+1)} = \cos\!\left(\frac{pos}{10000^{2i/d}}\right)
$$

每個位置是不同頻率正弦波的組合，且 $PE_{pos+k}$ 可表示為 $PE_{pos}$ 的線性函數，讓模型容易學到相對位移。

### 線索五：殘差連接與 LayerNorm

每個子層（注意力或前饋網路）外包裹殘差連接（He 等，2016）與層正規化（Ba 等，2016）：

$$
x \mapsto \text{LayerNorm}(x + \text{Sublayer}(x))
$$

殘差讓梯度直通頂層，深層堆疊（base/big 皆 6 層）才得以穩定訓練。

### 線索六：複雜度對比——可平行性即證據

| 模型 | 每層複雜度 | 順序操作 | 兩點間路徑長度 |
|---|---|---|---|
| RNN | $O(nd^2)$ | $O(n)$ | $O(n)$ |
| ConvS2S | $O(knd + nd^2)$ | $O(1)$ | $O(\log_k n)$ |
| Self-Attention | $O(n^2 d)$ | $O(1)$ | $O(1)$ |

Self-Attention 每層計量 $O(n^2 d)$ 較 RNN 貴，但順序操作為 $O(1)$——所有位置同時計算，GPU 全程滿載。任何兩個詞一層即相見，長距離依賴直接破解。「可平行性 = 可擴展性」成為工程哲學。

### 程式碼：numpy 手刻 mini self-attention（含多頭拼接）

```python
import numpy as np
np.random.seed(0)
n, d_model, h = 6, 32, 4    # 序列長 6、模型維度 32、4 個頭
d_k = d_v = d_model // h    # 每頭 8 維
X = np.random.randn(n, d_model)               # 輸入表示（已含位置編碼）

def attn(Q, K, V):
    E = Q @ K.T / np.sqrt(Q.shape[-1])        # scaled dot-product
    E = E - E.max(axis=-1, keepdims=True)     # 數值穩定
    A = np.exp(E); A /= A.sum(axis=-1, keepdims=True)
    return A, A @ V

heads, mats = [], []
for i in range(h):                            # 每頭獨立的 Q/K/V 投影
    Wq = np.random.randn(d_model, d_k) / np.sqrt(d_model)
    Wk = np.random.randn(d_model, d_k) / np.sqrt(d_model)
    Wv = np.random.randn(d_model, d_v) / np.sqrt(d_model)
    A, O = attn(X @ Wq, X @ Wk, X @ Wv)       # self-attention：Q=K=V 來自 X
    heads.append(O); mats.append(A)
W_O = np.random.randn(h * d_v, d_model) / np.sqrt(h * d_v)
out = np.concatenate(heads, axis=-1) @ W_O    # 多頭拼接後投影
print("輸出形狀:", out.shape)                  # (6, 32)，與輸入同形，可再堆一層
print("頭 0 注意力矩陣（第 i 行是位置 i 對全句的分佈）：")
np.set_printoptions(precision=2, suppress=True)
print(mats[0])
```

輸出與輸入同形，代表可以無限堆疊殘差層；每個頭的注意力矩陣各自捕捉不同的詞-詞關係，這正是 multi-head 的意義。Big 模型（6 層、$d_{\text{model}}=512$、8 頭）在 WMT14 英德達 BLEU 28.4，超過所有先前最佳系統（含集成模型），且訓練 3.5 天中最後 12 小時的算力即超過前紀錄系統的全部訓練量；英法 41.8 亦為單模型新紀錄。

## 結案 -- 後果與影響

- Transformer 成為語言模型的統一架構：BERT（2018）、GPT 系列（2018-）、GPT-3、GPT-4、Claude、Gemini、LLaMA 全是 Transformer 或其變體。
- Vision Transformer（Dosovitskiy 等，2020）把同一架構搬到影像，證明「注意力就夠了」跨域成立。
- 「可平行性 = 可擴展性」成為深度學習的工程哲學：先讓訓練可平行，再讓規模說話。
- 八位作者後續：Aidan Gomez 創立 Cohere；Llion Jones 的論文圖 1 視覺化成為被引用最多的架構圖之一；Jakob Uszkoreit 被視為想法發起者；Shazeer 持續改良（含 GShard/MoE）。

## 關鍵人物與文獻

- Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin (2017). Attention Is All You Need. *NeurIPS 2017*. arXiv:1706.03762.
- Jonas Gehring et al. (2017). Convolutional Sequence to Sequence Learning. *ICML 2017*. arXiv:1705.03122.
- Jianpeng Cheng, Li Dong, Mirella Lapata (2016). Long Short-Term Memory-Networks for Machine Reading. *EMNLP 2016*. arXiv:1601.06733.
- Ankur P. Parikh, Oscar Täckström, Dipanjan Das, Jakob Uszkoreit (2016). A Decomposable Attention Model for Natural Language Inference. *EMNLP 2016*. arXiv:1606.01933.
- Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun (2016). Deep Residual Learning for Image Recognition. *CVPR 2016*.
- Jimmy Lei Ba, Jamie Ryan Kiros, Geoffrey E. Hinton (2016). Layer Normalization. arXiv:1607.06450.
