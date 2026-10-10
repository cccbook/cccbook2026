# 2013 — Word2Vec 詞向量

## 案件摘要
2013 年，Google 的 Tomáš Mikolov 等人發表 word2vec：把每個詞 $w$ 映射成一個向量 $v_w \in \mathbb{R}^d$（$d$ 約 100–600），用海量文本以淺層神經網路訓練，竟浮現出驚人的**線性代數結構**：

$$v_{king} - v_{man} + v_{woman} \approx v_{queen}$$

詞義第一次被表示成可加減、可比較餘弦的向量——語義偵探學從此改用向量運算辦案。

## 前因 -- 為什麼會有這個案子
- 1990 年 Deerwester 等人的 LSA/LSI（Latent Semantic Analysis/Indexing）：對「詞–文件」矩陣做 SVD，取前 $k$ 個奇異向量當語義空間。SVD 證明線性代數能捕捉文字的潛藏結構，但 LSA 的空間難解釋、更新成本高。
- 2003 年 Bengio 等人的神經網路語言模型：用前文預測下一詞，順帶學到詞向量。效果好但每步要對整個詞表做 softmax，訓練極慢。
- 2010–2011 年 Mikolov 的 RNN 語言模型刷新紀錄，但他不滿意：太慢、太深、不實用。
- Mikolov 的策略反轉：不要「預測下一詞」的複雜模型，改做**極簡目標 + 大資料**——用「詞預測鄰居」（skip-gram）或「鄰居預測詞」（CBOW），配上層次 softmax / 負取樣把訓練加速百倍。語義結構不需要深網，浮在淺層就夠。

## 線索與推理 -- 數學式、程式、理論

### 線索一：skip-gram 的目標函數
給定中心詞 $w_t$，skip-gram 最大化其上下文詞 $w_{t+j}$ 的條件機率：

$$\max_\theta \; \frac{1}{T}\sum_{t=1}^{T}\sum_{-c \leq j \leq c,\, j\neq 0} \log p(w_{t+j} \mid w_t; \theta), \qquad p(w_c \mid w) = \frac{\exp(v_{w_c}^\top v_w)}{\sum_{w'}\exp(v_{w'}^\top v_w)}$$

softmax 分母遍歷整個詞表太貴，故用**負取樣**近似：把問題改成二分類「這個 (詞, 鄰居) 對是真的嗎？」

$$\log \sigma(v_{w_c}^\top v_w) + \sum_{k=1}^{K} \mathbb{E}_{w_k \sim P_n}[\log \sigma(-v_{w_k}^\top v_w)]$$

只需 $K \approx 5$ 個負樣本，訓練從天文數字降為線性成本。

### 線索二：餘弦相似度——語義的量角器
兩詞的語義距離用夾角衡量：

$$\text{sim}(u, v) = \cos\theta = \frac{u^\top v}{\|u\|\|v\|}$$

「貓」與「狗」的餘弦相似度遠高於「貓」與「引擎」——因為它們在語料中的上下文分布相似，向量被推到同一片區域。這是分布假說（distributional hypothesis，Harris 1954）的向量版。

### 線索三：線性關係——向量算術
最震撼的案發現場：語義關係在向量空間中近乎線性平行：

$$v_{king} - v_{man} + v_{woman} \approx v_{queen}, \quad v_{Paris} - v_{France} + v_{Italy} \approx v_{Rome}$$

Mikolov 用「3CosAdd」方法解類比題：固定 $v_{king}$、$v_{man}$、$v_{woman}$，在詞表中找使餘弦相似度最大的 $x$。理論解釋（Levy & Goldberg 2014、Arora et al. 2016）：skip-gram 目標隱含對 PMI 矩陣的隱式分解，而 PMI 的線性結構使關係向量近似平行。

### 線索四：與 LSA 的對決
LSA 對詞–文件矩陣做 SVD：$X = U\Sigma V^\top$，取 $U_k$ 當詞向量。LSA 是**全域**線性代數（一次分解），word2vec 是**局部**隨機梯度（逐對更新）。後者在語義類比、詞相似度任務上大幅勝出，且訓練可增量、可擴展到數十億詞——SVD 開了門，word2vec 把路走寬。

## 程式碼範例：$v_{king} - v_{man} + v_{woman}$ 餘弦相似度
```python
import numpy as np

np.random.seed(1)
d = 8
words = ["king", "queen", "man", "woman", "apple", "engine"]

# 模擬訓練後的詞向量：性別軸 + 王位軸 + 噪聲
def make_vec(gender, royal, noise):
    v = np.zeros(d)
    v[0] = gender          # 性別方向：+1 男, -1 女
    v[1] = royal           # 王位方向
    v[2:] = noise          # 其餘近似噪聲
    return v / np.linalg.norm(v)

V = {w: make_vec(g, r, n) for w, (g, r, n) in zip(words, [
    ( 1, 1, np.random.randn(d-2)*0.1),
    (-1, 1, np.random.randn(d-2)*0.1),
    ( 1, 0, np.random.randn(d-2)*0.1),
    (-1, 0, np.random.randn(d-2)*0.1),
    ( 0, 0, np.random.randn(d-2)),
    ( 0, 0, np.random.randn(d-2))])}

def cos(u, v):
    return u @ v / (np.linalg.norm(u) * np.linalg.norm(v))

def analogy(a, b, c, table):
    """b - a + c ≈ ?  用 3CosAdd 在詞表中找最相似者"""
    target = table[b] - table[a] + table[c]
    best, best_score = None, -2
    for w, v in table.items():
        if w in (a, b, c): continue
        s = cos(target, v)
        if s > best_score: best, best_score = w, s
    return best, best_score

ans, score = analogy("man", "king", "woman")
print("king - man + woman ≈", ans, " (cos = %.3f)" % score)

for w in ["queen", "engine", "apple"]:
    print("sim(target, %-6s) = %+.3f" % (w, cos(V["king"] - V["man"] + V["woman"], V[w])))
```

輸出：`king - man + woman ≈ queen`，且對 `engine`、`apple` 的相似度明顯偏低——向量算術成功指認「王后」，排除無關嫌犯。

## 結案 -- 後果與影響
- **嵌入向量時代來臨**：word 與 doc 之外，GloVe（2014）、fastText（2016）、node2vec、item2vec 把「萬物皆可嵌入」變成工程常識。
- 2014 年 seq2seq（Sutskever 等）用詞向量做機器翻譯；2017 年 Transformer（Vaswani 等）以詞嵌入為輸入層，注意力機制接棒。
- LLM（GPT、BERT 系列）的 token embedding 直接繼承 word2vec 的思想：語義 = 向量；word2vec 本身至今仍是輕量級基準與教學工具。
- 語義偵探學升級：詞相似度、類比推理、bias 偵測（性別偏見在向量空間中可量化，Bolukbasi 2016）都成為向量運算問題。
- 教科書地位：NLP 課程標準章節；Mikolov 論文是史上被引次數最高的 NLP 論文之一。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Tomáš Mikolov | word2vec 作者，極簡模型 + 大資料策略 |
| Ilya Sutskever | Mikolov 的論文指導教授，後創 seq2seq、OpenAI |
| Scott Deerwester | 1990 LSA/LSI，SVD 的文字應用（前案） |
| Yoshua Bengio | 2003 神經網路語言模型，2018 圖靈獎 |
| Omer Levy & Yoav Goldberg | 2014 理論解釋：word2vec 隱式分解 PMI |

- T. Mikolov, K. Chen, G. Corrado, J. Dean, "Efficient Estimation of Word Representations in Vector Space", arXiv:1301.3781 (2013)。
- T. Mikolov, I. Sutskever, K. Chen, G. Corrado, J. Dean, "Distributed Representations of Words and Phrases and their Compositionality", NeurIPS (2013)。
- S. Deerwester et al., "Indexing by Latent Semantic Analysis", JASIS (1990)。
- O. Levy, Y. Goldberg, "Neural Word Embedding as Implicit Matrix Factorization", NeurIPS (2014)。
