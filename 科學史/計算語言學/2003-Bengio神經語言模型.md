# 2003-Bengio神經語言模型

## 案件摘要

n-gram 語言模型統治了語音辨識與機器翻譯二十多年，但它有一個致命弱點：維度詛咒。詞彙表一大，「詞序列」的組合空間爆炸，絕大多數 n-gram 在訓練語料中出現零次，模型只能靠粗糙的平滑手段硬撐。2003 年，Université de Montréal 的 Yoshua Bengio、Réjean Ducharme、Pascal Vincent 與 Christian Jauvin 發表《A Neural Probabilistic Language Model》（JMLR 3），提出破案手法：把每個詞表示成一個學到的實數向量，讓「相似詞有相似向量」，知識便能在詞與詞之間流動。這是神經語言模型的第一個完整實作，也是 GPT 這類大型語言模型的直接祖先。

## 前因 -- 為什麼會有這個案子

- n-gram 語言模型的維度詛咒：若詞彙表大小為 $V$，$n$-gram 的參數空間是 $V^n$，$V = 100{,}000$、$n = 5$ 時組合空間遠超任何語料的覆蓋能力，資料稀疏性無解。
- one-hot 表示的稀疏性：每個詞是 $V$ 維單位向量，任意兩詞的內積恆為零——模型眼中「貓」和「狗」與「貓」和「太空梭」一樣毫無關係，無法泛化。
- 傳統平滑（Good-Turing、Kneser-Ney）只能修補計數，無法表達「相似詞應共享證據」的語言學直覺。
- 1986 年 Rumelhart、Hinton、Williams 的反傳播（backpropagation）讓多層神經網路可訓練，1980 年代末至 90 年代神經網路方法在 NLP 有零星嘗試（如 NetTalk、神經機率標記器），但規模與理論都有限。
- Bengio 的動機：用「表示學習」對付維度詛咒——不硬數離散組合，而是讓模型自己學出一個連續、低維、有幾何結構的詞語義空間。

## 線索與推理 -- 數學式、程式、理論

### 線索一：詞嵌入矩陣 C 的學習

第一條線索是引入一個共享的嵌入矩陣 $C \in \mathbb{R}^{V \times m}$：詞彙中第 $i$ 個詞的向量是 $C$ 的第 $i$ 列 $C(i) \in \mathbb{R}^m$（論文中 $m$ 約為 30-100）。給定前 $n-1$ 個詞，先把它們的向量拼接成輸入：

$$
x = \big( C(w_{t-n+1}),\ C(w_{t-n+2}),\ \ldots,\ C(w_{t-1}) \big) \in \mathbb{R}^{m(n-1)}
$$

$C$ 不是手工特徵，而是與網路其他參數一起由梯度下降學出來的——這是「語義 = 學到的向量」哲學的第一次落實。

### 線索二：神經網路架構與 softmax

完整模型是一個三層前饋網路：嵌入層 + 隱層 + softmax 輸出。以論文的記號（$h = \tanh(d + Hx)$，再加一個從 $x$ 直通輸出的線性捷徑）：

$$
P(w_t = i \mid w_{t-n+1..t-1}) = \frac{\exp\big( b_i + U_{:,i} h + W_{:,i} x \big)}{\sum_{j=1}^{V} \exp\big( b_j + U_{:,j} h + W_{:,j} x \big)}
$$

其中 $U \in \mathbb{R}^{h_{dim} \times V}$、$W \in \mathbb{R}^{m(n-1) \times V}$（捷徑權重，可設零）。訓練目標是最大化整個語料的對數概似：

$$
L = \frac{1}{T} \sum_{t} \log P(w_t \mid w_{t-n+1..t-1}) + \lambda R(\theta)
$$

全部參數 $\theta = \{b, d, U, W, C\}$ 以隨機梯度下降 + 反傳播更新。

### 線索三：破案時刻——平滑效應的數學

破案的理論核心：因為輸出對嵌入向量是（近似）平滑函數，若詞 $i$ 與詞 $j$ 的向量接近，則 $P(i|\text{context}) \approx P(j|\text{context})$。所以「狗 ate the bone」的證據會自動提升「貓 ate the bone」的機率——每個訓練樣本不只更新自己，還更新鄰近的整片語義區域。這正是 n-gram 做不到的泛化：

- n-gram：$P(\text{cat} \mid \text{saw the})$ 只由「saw the cat」的計數決定，出現零次就完蛋。
- 神經 LM：由「saw the $w$」中所有 $w$ 與 cat 的相似度加權決定，零次也能泛化。

維度詛咒並未消失（softmax 仍要對 $V$ 個類別求和），但被有效馴服。論文同時討論了 hierarchical softmax：把詞彙組織成樹，把 $O(V)$ 的分母降為 $O(\log V)$，作為大詞彙的加速手段。實驗上，Bengio 等人在 Brown 與 AP News 語料上以較小的困惑度（perplexity）超越同階的 Kneser-Ney n-gram，且兩者混合後更好——證明神經模型學到了 n-gram 之外的訊息。

### 程式：numpy 實作 mini 神經語言模型

以下用 numpy 實作嵌入層 + 隱層 + softmax 的完整 mini 版，訓練小語料並展示學到的詞向量：

```python
import numpy as np
np.random.seed(0)

corpus = ("the cat sat on the mat . the dog sat on the floor . "
          "a cat ate the fish . a dog ate the bone .").split()
vocab = sorted(set(corpus))
V, m, hdim = len(vocab), 8, 16
w2i = {w: i for i, w in enumerate(vocab)}
N = 3  # 用前 2 個詞預測第 3 個詞

data = [( [w2i[w] for w in corpus[i:i+N-1]], w2i[corpus[i+N-1]] )
        for i in range(len(corpus) - N + 1)]

C  = np.random.randn(V, m) * 0.1          # 詞嵌入矩陣
H  = np.random.randn(hdim, m*(N-1)) * 0.1
d  = np.zeros(hdim)
U  = np.random.randn(V, hdim) * 0.1
b  = np.zeros(V)

def forward(ctx):
    x = C[ctx].reshape(-1)                # 拼接嵌入
    h = np.tanh(d + H @ x)
    logits = b + U @ h                    # (捷徑 W 設為零)
    logits -= logits.max()
    p = np.exp(logits); p /= p.sum()
    return x, h, p

for epoch in range(500):
    lr = 0.5 / (1 + epoch * 0.01)
    for ctx, target in data:
        x, h, p = forward(ctx)
        loss = -np.log(p[target])
        g_logits = p.copy(); g_logits[target] -= 1
        g_U = np.outer(g_logits, h)
        g_h = U.T @ g_logits * (1 - h**2)
        g_H = np.outer(g_h, x)
        g_d = g_h
        g_C = (H.T @ g_h).reshape(N-1, m)
        C[ctx] -= lr * g_C                # 嵌入共享更新
        H -= lr * g_H; d -= lr * g_d; U -= lr * g_U; b -= lr * g_logits

def predict(w1, w2):
    ctx = [w2i[w1], w2i[w2]]
    _, _, p = forward(ctx)
    top = p.argsort()[::-1][:3]
    return [(vocab[i], round(float(p[i]), 3)) for i in top]

print("P(next | 'the', 'cat'):", predict("the", "cat"))
print("P(next | 'the', 'dog'):", predict("the", "dog"))

# 相似詞有相似向量: 以餘弦相似度檢驗
emb = C
def cos(a, b):
    va, vb = emb[w2i[a]], emb[w2i[b]]
    return round(float(va @ vb / (np.linalg.norm(va)*np.linalg.norm(vb))), 3)
print("cos(cat, dog) =", cos("cat", "dog"))
print("cos(cat, fish) =", cos("cat", "fish"))
```

執行可見：「the cat」與「the dog」之後的高機率詞高度相似（sat/ate 互換仍合理），且語法角色相近的詞（cat、dog）餘弦相似度明顯高於語義無關的詞——「相似詞有相似向量」的平滑效應在迷你規模上重現。

## 結案 -- 後果與影響

- 詞向量思想的種子：Word2Vec（Mikolov et al., 2013）的直接先驅——其 skip-gram 可視為去掉隱層、簡化目標的 Bengio 模型變體。
- 神經語言模型成為 LLM 的直接祖先：RNN 語言模型（2010 Mikolov）→ LSTM → Transformer（2017）→ GPT，血緣一脈相承，GPT 本質上就是放大版的神經機率語言模型。
- Bengio 因表示學習與深度學習的貢獻，與 Hinton、LeCun 同獲 2018 年圖靈獎。
- 「表示學習」的哲學轉折確立：語義是學到的連續向量，不是手工離散特徵——這成為此後二十年 NLP 的主旋律。
- hierarchical softmax、詞嵌入共享、困惑度對照等技術細節，成為後續神經 NLP 的標準配備；與 n-gram 混合可再降困惑度的發現，預示了神經與統計方法的互補關係。

## 關鍵人物與文獻（條列）

- Yoshua Bengio, Réjean Ducharme, Pascal Vincent, Christian Jauvin. "A Neural Probabilistic Language Model." Journal of Machine Learning Research 3, 2003, pp. 1137-1155.
- David E. Rumelhart, Geoffrey E. Hinton, Ronald J. Williams. "Learning Representations by Back-propagating Errors." Nature 323, 1986, pp. 533-536.
- Yoshua Bengio, Holger Schwenk, Jean-Sébastien Senécal, Fréderic Morin, Jean-Luc Gauvain. "Neural Probabilistic Language Models." In Innovations in Machine Learning, Springer, 2006, pp. 137-186（hierarchical softmax 的後續）.
- Frédéric Morin, Yoshua Bengio. "Hierarchical Probabilistic Neural Network Language Model." AISTATS 2005.
- Tomas Mikolov, et al. "Efficient Estimation of Word Representations in Vector Space." ICLR Workshop 2013（Word2Vec）.
- Tomas Mikolov, et al. "Recurrent Neural Network Based Language Model." INTERSPEECH 2010.
- Stanley F. Chen, Joshua Goodman. "An Empirical Study of Smoothing Techniques for Language Modeling." Computer Speech & Language 13(4), 1999, pp. 359-384（Kneser-Ney 平滑的基準）.
