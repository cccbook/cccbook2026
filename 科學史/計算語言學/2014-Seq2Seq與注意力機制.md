# 2014-Seq2Seq與注意力機制

## 案件摘要

2014 年，翻譯品質這樁懸案迎來兩份關鍵證詞。Google 的 Ilya Sutskever、Oriol Vinyals 與 Quoc Le 在 NeurIPS 2014 發表《Sequence to Sequence Learning with Neural Networks》，用兩個 LSTM 把整句英文壓成一個向量再解碼成法文，證明端到端神經翻譯可行。然而長句子的資訊在壓縮中不斷流失——這是「固定長度向量瓶頸」的疑點。同年稍晚，Dzmitry Bahdanau、Kyunghyun Cho 與 Yoshua Bengio 在 arXiv（後 ICLR 2015）發表《Neural Machine Translation by Jointly Learning to Align and Translate》，以「注意力」讓解碼器每一步回頭查看整句，破解了瓶頸懸案。破案時刻是：翻譯不需要把句子壓成一個點，只需要學會「看哪裡」。

## 前因 -- 為什麼會有這個案子

- Word2Vec（2013）解决了詞級表示，把每個詞變成語義向量，但句子級翻譯仍缺一套處理變長序列的架構。
- LSTM（Hochreiter 與 Schmidhuber，1997）以遺忘門緩解梯度消失，使長序列訓練成為可能，但標準用法是輸出一個固定向量。
- 統計機器翻譯（SMT）的 IBM Model 系列（1990-1993）統治多年，但需大量特徵工程、詞對齊表與語言模型拼裝，系統複雜脆弱。
- Google 翻譯部門想要一套端到端、可微、能隨資料成長的系統，取代手工拼裝的 SMT。

## 線索與推理 -- 數學式、程式、理論

### 線索一：Seq2Seq 的編碼-解碼框架

編碼器 LSTM 逐詞讀入源句 $x_1, \dots, x_T$，把整句壓縮成最終隱狀態（上下文向量）$c$：

$$
h_t = \text{LSTM}(x_t, h_{t-1}), \qquad c = h_T
$$

解碼器是另一個 LSTM，條件式地逐詞生成目標句：

$$
P(y_1, \dots, y_{T'} \mid x) = \prod_{t=1}^{T'} P(y_t \mid y_{<t}, c)
$$

### 線索二：固定長度瓶頸的數學

不論源句是 5 個詞還是 50 個詞，所有資訊都必須塞進同一個 $d$ 維向量 $c$。若源句的資訊量以 $I(x)$ 度量，向量容量固定為 $d \cdot b$ 位元（$b$ 為每維精度），則長句必然發生資訊損失：

$$
\text{Loss} = I(x) - \min(I(x),\, d \cdot b) \xrightarrow{T \to \infty} \infty
$$

Sutskever 等人的實驗線索也吻合：他們發現把源句逆序輸入（使句首對句首相近）能大幅改善 BLEU，說明梯度與資訊在長距離傳遞時確實衰減——瓶頸不只存在於向量，也存在於 RNN 的記憶。

### 線索三：注意力機制——軟對齊破解瓶頸

Bahdanau 等人的推理：既然壓成一個向量會遺失資訊，那就不要壓。保留編碼器所有隱狀態 $\{h_1, \dots, h_T\}$，解碼器在每個時間步 $t$ 自行決定要看哪些狀態：

$$
e_{t,i} = a(s_{t-1}, h_i), \qquad \alpha_{t,i} = \frac{\exp(e_{t,i})}{\sum_{j=1}^{T} \exp(e_{t,j})}, \qquad c_t = \sum_{i=1}^{T} \alpha_{t,i}\, h_i
$$

其中 $s_{t-1}$ 是解碼器前一個隱狀態，$a$ 是一個小型前饋網路的對齊打分函數。上下文向量從「一個固定的 $c$」變成「隨時間變化的 $c_t$」，瓶頸消失。

### 線索四：軟對齊取代 IBM 硬對齊

IBM Model 1/2 的對齊是硬性的：一個源詞要麼對到某目標詞、要麼不對。注意力的 $\alpha_{t,i} \in [0,1]$ 是機率分布，形成「軟對齊」——每一步都是全體源詞的加權，且矩陣 $[\alpha_{t,i}]$ 本身就是可視化的對齊證據。這把 SMT 中需單獨訓練的對齊模型，變成翻譯目標函數自動學出的副產品。

### 程式碼：numpy 手刻 attention 並印出對齊矩陣

```python
import numpy as np

np.random.seed(42)
T, Tp, d = 5, 4, 8          # 源句 5 詞、目標句 4 詞、隱狀態維度
H = np.random.randn(T, d)   # 編碼器各時間步隱狀態 h_1..h_T
S = np.random.randn(Tp, d)  # 解碼器各時間步隱狀態 s_1..s_t

# 加性對齊打分：e[t,i] = v^T tanh(W_s s_t + W_h h_i)
W_s = np.random.randn(d, d) / np.sqrt(d)
W_h = np.random.randn(d, d) / np.sqrt(d)
v   = np.random.randn(d)    / np.sqrt(d)

M = np.tanh(S[:, None, :] @ W_s + H[None, :, :] @ W_h)  # 形狀 (Tp, T, d)
E = M @ v                                     # e[t,i]，形狀 (Tp, T)
A = np.exp(E - E.max(axis=1, keepdims=True))  # softmax（數值穩定）
A = A / A.sum(axis=1, keepdims=True)

C = A @ H                                     # 加權上下文 c_t = sum_i alpha_t,i h_i
print("注意力（對齊）矩陣 alpha[t,i]：")
np.set_printoptions(precision=2, suppress=True)
print(A)
print("各步上下文向量範數：", np.linalg.norm(C, axis=1).round(2))
# 觀察：每列加總為 1；某列權重集中即該步「看著」特定源詞——軟對齊
```

每一步解碼都有專屬的 $c_t$；對齊矩陣 $A$ 的亮點位置即譯詞與源詞的對應，這正是 Bahdanau 論文圖 3 所呈現的證據。

### 線索五：beam search 解碼

逐詞貪心取 $\arg\max P(y_t \mid \cdot)$ 會累積錯誤。Seq2Seq 實務上用束搜尋：每步保留 $k$ 個累積對數機率最高的部分序列，最後整句取優：

$$
\hat{y} = \arg\max_{y \in \text{beam}} \sum_{t=1}^{T'} \log P(y_t \mid y_{<t}, c)
$$

## 結案 -- 後果與影響

- 神經機器翻譯（NMT）誕生，數年內 Google 翻譯從短語式 SMT 全面轉向 GNMT（2016），SMT 退場。
- 注意力機制成為深度學習的萬用零件，從翻譯擴散到語音、摘要、問答、影像。
- Bahdanau 的軟對齊讓翻譯可解釋：注意力矩陣本身即對齊證據。
- 注意力只需「查表加權」、不需沿時間反覆遞迴，啟發了 self-attention（Cheng 2016、Parikh 2016），直接通往 Transformer（2017）。
- Sutskever 後續主持 OpenAI 研究多年；Cho、Bengio 持續推動序列建模理論。

## 關鍵人物與文獻

- Ilya Sutskever, Oriol Vinyals, Quoc V. Le (2014). Sequence to Sequence Learning with Neural Networks. *NeurIPS 2014*. arXiv:1409.3215.
- Dzmitry Bahdanau, Kyunghyun Cho, Yoshua Bengio (2015). Neural Machine Translation by Jointly Learning to Align and Translate. *ICLR 2015*. arXiv:1409.0473.
- Sepp Hochreiter, Jürgen Schmidhuber (1997). Long Short-Term Memory. *Neural Computation*, 9(8), 1735-1780.
- Peter F. Brown et al. (1993). The Mathematics of Statistical Machine Translation: Parameter Estimation. *Computational Linguistics*, 19(2), 263-311.
- Yonghui Wu et al. (2016). Google's Neural Machine Translation System: Bridging the Gap between Human and Machine Translation. arXiv:1609.08144.
