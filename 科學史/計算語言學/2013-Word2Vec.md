# 2013-Word2Vec

## 案件摘要

2013 年，Google 的 Tomas Mikolov 等人發表《Efficient Estimation of Word Representations in Vector Space》，提出兩種極其高效的詞向量訓練架構：CBOW 與 skip-gram。這篇論文解開了一樁懸案：如何在不犧牲語義品質的前提下，把詞向量的訓練成本從「數週」壓到「數小時甚至數小時內」。「king - man + woman ≈ queen」的向量算術示例，更讓整個領域相信語義就是向量空間裡的幾何。本案是「分佈假說」從語言學理論走進工業實務的破案時刻。

## 前因 -- 為什麼會有這個案子

- Bengio 等人 2003 年的神經語言模型（NNLM）已經證明「詞的連續向量表示」有用，但 softmax 必須對整個詞彙表 $V$（數十萬詞）計算機率，成為致命 bottleneck，訓練一個模型要數週。
- 語言學家 Zellig Harris 1954 年早已提出分佈假說（distributional hypothesis）：出現在相似語境的詞，語義相似。傳統的 PMI 矩陣 + SVD 分解是這個假說的線性代數實現，但同樣難以擴展到超大語料。
- 深度學習浪潮興起（2012 年 AlexNet 之後），大家相信「大資料 + 快硬體 + 簡單模型」可以打敗精緻的傳統方法。
- Mikolov 先前以 RNN 語言模型成名，但他心中真正想要的，是一個「快而好」、能被工業界大量使用的詞向量工具——目標不是語言模型本身，而是詞向量這個副產品。

## 線索與推理 -- 數學式、程式、理論

### CBOW 與 skip-gram 的架構

Word2Vec 的第一個推理線索：把「用整句預測下一詞」的語言模型目標，換成更直接的「用語境預測詞」或「用詞預測語境」。

- CBOW（Continuous Bag of Words）：用中心詞周圍的語境詞預測中心詞，語境詞的向量直接平均（bag = 不考慮順序）。
- Skip-gram：反過來，用中心詞預測周圍的每個語境詞。對小語料、罕見詞，skip-gram 品質更好。

skip-gram 的目標函數（給定中心詞 $w_c$，最大化其語境詞 $w_o$ 的條件機率）：

$$
\max_\theta \; \frac{1}{T} \sum_{t=1}^{T} \sum_{-m \le j \le m, \, j \ne 0} \log P(w_{t+j} \mid w_t ; \theta)
$$

### 負採樣：取代全 softmax 的關鍵一步

第二個線索：softmax 的 bottleneck 在於分母要對整個詞彙表求和：

$$
P(w_o \mid w_c) = \frac{\exp(v_{w_o}^\top v_{w_c})}{\sum_{w \in V} \exp(v_w^\top v_{w_c})}
$$

Mikolov 的破案手法：不改變模型，改變目標。負採樣（negative sampling）把多類別分類拆成一組二元分類：真實語境詞的內積要大，隨機抽出的「負例」詞的內積要小：

$$
\log \sigma(v_c \cdot v_w) + \sum_{i=1}^{k} \mathbb{E}_{w_i \sim P_n} \log \sigma(-v_c \cdot v_{w_i})
$$

其中 $\sigma(x) = 1/(1+e^{-x})$ 是 sigmoid 函數，$P_n$ 是噪音分佈（實務上取一元詞頻的 3/4 次方）。每次更新的成本從 $O(V)$ 降到 $O(k)$，$k$ 通常只是 5-20。對照組層次 softmax（hierarchical softmax）則用 Huffman 編碼樹把 $O(V)$ 降到 $O(\log V)$，但負採樣更簡單，成為實務首選。

### 向量算術的幾何解釋

第三個線索是那個著名的示例：$v_{king} - v_{man} + v_{woman} \approx v_{queen}$。

幾何解釋：如果「性別」是一個方向向量，那麼所有詞在這個方向上的位移是近似線性的。skip-gram 的目標函數只用到內積（線性運算），語義關係因此在訓練後收斂成向量空間中的平行方向。詞類比任務（a - b + c ≈ d）成了評估詞向量品質的標準測試。

### 與 PMI/SVD 的數學等價性

第四個線索由 Levy 與 Goldberg（2014）指出：skip-gram + 負採樣其實是在隱式地分解移位後的 PMI 矩陣。若把內積拆成 $w_c^\top w_o + b_c + b_o$，其最優解滿足：

$$
w_c^\top w_o + b_c + b_o = \log \frac{P(w_o, w_c)}{P(w_o) P(w_c) \cdot k} = \text{PMI}(w_o, w_c) - \log k
$$

換句話說，Word2Vec 不是革命，而是「分佈假說 + 矩陣分解」這條老線索的高效重新偵辦——只是它用隨機梯度下降在線上串流資料中完成分解，因此能吃下整個 Google News 語料。

### 程式示範：mini skip-gram + negative sampling

以下 Python（numpy）在一個小語料上訓練 skip-gram，並展示詞向量相似度：

```python
import numpy as np

corpus = ("the king rules the kingdom . the queen loves the king . "
          "the man works in the field . the woman loves the man . "
          "the king and the queen talk .").split()
words = sorted(set(corpus))
w2i = {w: i for i, w in enumerate(words)}
V, d = len(words), 16
rng = np.random.default_rng(0)
W_in = rng.normal(0, 0.1, (V, d))   # 中心詞向量
W_out = rng.normal(0, 0.1, (V, d))  # 語境詞向量
idx = [w2i[w] for w in corpus]

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

freq = np.bincount(idx, minlength=V).astype(float)
p_noise = (freq ** 0.75) / (freq ** 0.75).sum()  # 噪音分佈：詞頻的 3/4 次方

lr, window, k_neg = 0.05, 2, 5
for epoch in range(200):
    loss = 0.0
    for t, c in enumerate(idx):
        ctx = [idx[j] for j in range(max(0, t - window), min(len(idx), t + window))
               if j != t]
        for o in ctx:
            v_c, v_o = W_in[c], W_out[o]
            negs = rng.choice(V, size=k_neg, p=p_noise)
            negs = negs[negs != o][:k_neg]
            # 正例：sigma(v_c . v_o) 應趨近 1；負例：應趨近 0
            score_pos = sigmoid(v_c @ v_o)
            score_neg = sigmoid(W_out[negs] @ v_c)
            loss += -np.log(score_pos + 1e-9) - np.log(1 - score_neg + 1e-9).sum()
            grad = (score_pos - 1) * v_c
            W_out[o] -= lr * grad
            W_out[negs] += lr * np.outer(score_neg, v_c)
            W_in[c] -= lr * ((score_pos - 1) * v_o
                             + (score_neg @ W_out[negs] if len(negs) else 0))

def cos(a, b):
    va, vb = W_in[w2i[a]], W_in[w2i[b]]
    return float(va @ vb / (np.linalg.norm(va) * np.linalg.norm(vb)))

for a, b in [("king", "queen"), ("man", "woman"), ("king", "field")]:
    print(f"cos({a}, {b}) = {cos(a, b):.3f}")
# 觀察：king-queen 與 man-woman 的相似度應高於 king-field
```

## 結案 -- 後果與影響

- 詞向量成為 2013-2018 年間 NLP 的標配：所有任務（分詞、NER、句法分析、翻譯）的輸入層幾乎都換成 word2vec 或同類詞向量。
- GloVe（Pennington 等，2014）以「全域共現統計 + 最小平方式分解」正面對照 skip-gram，證明兩條路殊途同歸。
- fastText（Bojanowski 等，2016）把詞拆成字元 n-gram，讓罕見詞與形態豐富語言（如捷克語、土耳其語）也有好向量。
- 「語義 = 向量空間幾何」的信念全面勝利，詞類比、相似度、向量檢索成為標準評估與應用。
- 缺陷同時現形：上下文無關詞向量讓多義詞（bank 的河邊與銀行）共用同一個向量，這個懸案由 ELMo（2018）與 BERT（2018）的「上下文相關表示」接手偵辦。

## 關鍵人物與文獻（條列，含真實文獻書目）

- Tomas Mikolov、Kai Chen、Greg Corrado、Jeffrey Dean：Efficient Estimation of Word Representations in Vector Space. arXiv:1301.3781, 2013（ICLR 2013 Workshop）。
- Tomas Mikolov、Ilya Sutskever、Kai Chen、Greg Corrado、Jeffrey Dean：Distributed Representations of Words and Phrases and their Compositionality. NeurIPS 2013（負採樣與向量算術的完整版）。
- Yoshua Bengio、Réjean Ducharme、Pascal Vincent、Christian Jauvin：A Neural Probabilistic Language Model. JMLR 3:1137-1155, 2003。
- Zellig Harris：Distributional Structure. Word 10(2-3):146-162, 1954。
- Omer Levy、Yoav Goldberg：Neural Word Embedding as Implicit Matrix Factorization. NeurIPS 2014。
- Jeffrey Pennington、Richard Socher、Christopher Manning：GloVe: Global Vectors for Word Representation. EMNLP 2014。
