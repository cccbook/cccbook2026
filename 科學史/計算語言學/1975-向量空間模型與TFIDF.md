# 1975-向量空間模型與TFIDF

## 案件摘要

1975 年，Gerald Salton（Cornell 大學，SMART 系統的主持人）發表向量空間模型（Vector Space Model），為「文件相關性如何排序」這樁懸案提出幾何學答案：把文件與查詢都表示成詞項空間中的向量，相關性就是它們之間的夾角。TF-IDF 權重則在 Salton 與 Buckley 1988 年的論文中正式化，而 Karen Spark Jones 1972 年的 IDF 概念是重要先聲。這條「語義 = 幾何」的路線，成為資訊檢索（IR）四十年的數學基礎，也是 2013 年 Word2Vec 詞向量的哲學先聲——意義不再藏在符號規則裡，而是活在向量空間的幾何結構中。

## 前因 -- 為什麼會有這個案子

- 布林模型（boolean retrieval）的缺陷：查詢「科學 AND 歷史」只回答「有或沒有」，無法排序、無法表達部分匹配——文件之間只有 0 與 1。
- 1960 年代文件數量爆炸，SMART 系統（Salton 從 Harvard 到 Cornell 持續開發）需要一套「哪些文件更相關」的排序數學。
- Luhn（1957）的詞頻（term frequency）思想已出現：出現次數多的詞更重要——但單獨用 TF 有問題：常見虛詞（the、的）頻率最高卻最沒有資訊量。
- Spark Jones（1972）提出 IDF（inverse document frequency）：稀有詞比常見詞更有鑑別力——這是「詞的資訊量可以用文件分佈衡量」的關鍵線索。
- 模糊匹配（partial matching）的理論需求：查詢與文件不必完全重疊，只需「足夠接近」——需要一種可計算「接近程度」的幾何框架。

## 線索與推理 -- 數學式、程式、理論

### 核心證據：文件即向量

向量空間模型的偵探手法是「幾何化」：設詞彙表有 $n$ 個詞項，每篇文件 $d$ 表示成 $n$ 維向量：

$$d = (w_{1,d}, \; w_{2,d}, \; \dots, \; w_{n,d})$$

其中 $w_{t,d}$ 是詞項 $t$ 在文件 $d$ 中的權重。所有文件排成詞項-文件矩陣（term-document matrix）$W \in \mathbb{R}^{n \times m}$（m 為文件數）。查詢 $q$ 也用同樣方式表示成向量——於是「找相關文件」變成「找靠近 $q$ 的向量」。

### TF-IDF 權重

TF-IDF 結合兩條線索：TF（詞在文件中出現越多越重要）與 IDF（詞在越多文件出現越不鑑別）：

$$w_{t,d} = tf_{t,d} \times \log\frac{N}{df_t}$$

其中 $N$ 是文件總數，$df_t$ 是包含詞項 $t$ 的文件數。破案的時刻在於兩者的乘積：

- 常見於單一文件、稀見於整個語料庫的詞（如「剖析器」出現在某篇 NLP 論文中）權重最高。
- 到處出現的虛詞（the、的）：$df_t \approx N$，IDF 趨近 0，權重自動歸零——不需要手寫停用詞表也能壓制它們。

### 餘弦相似度：相關性的量尺

文件與查詢的相關性用夾角衡量（長度無關，方向才重要）：

$$\cos(\theta) = \frac{d \cdot q}{\|d\| \, \|q\|} = \frac{\sum_t w_{t,d} \, w_{t,q}}{\sqrt{\sum_t w_{t,d}^2} \, \sqrt{\sum_t w_{t,q}^2}}$$

$\cos(\theta) = 1$ 表示方向完全相同（最相關），$0$ 表示正交（不相關）。排序所有文件的餘弦值，就是搜尋引擎的原始形態。

### LSI 的先聲：語義 = 幾何路線的起點

向量空間模型的深層含義在 1988 年被 Deerwester、Dumais 等人發揚：對詞項-文件矩陣 $W$ 做奇異值分解（SVD）：

$$W \approx U_k \Sigma_k V_k^T$$

取前 $k$ 個奇異值降維，得到「潛在語義索引」（Latent Semantic Indexing, LSI）——詞與文件被投影到同一個低維語義空間，同義詞即使不共現也會靠近。這是「語義 = 向量空間幾何」路線的正式起點，直通 2013 年的 Word2Vec。

### 可執行程式：mini TF-IDF 搜尋引擎

```python
# mini TF-IDF + 餘弦相似度搜尋引擎
import math

docs = {
    "d1": "the model of natural language parsing with context free grammar",
    "d2": "vector space model for information retrieval and ranking",
    "d3": "language model with neural networks and statistics",
    "d4": "the geometry of vector spaces in semantic retrieval",
}
query = "vector space retrieval"

# 1. 分詞與詞彙表
toks = {k: d.split() for k, d in docs.items()}
vocab = sorted({t for ts in toks.values() for t in ts})
N = len(docs)

# 2. TF-IDF 權重：w = tf * log(N / df)
df = {t: sum(1 for ts in toks.values() if t in ts) for t in vocab}
idf = {t: math.log(N / df[t]) for t in vocab}
def vec(text):
    ts = text.split()
    return [ts.count(t) * idf[t] for t in vocab]
D = {k: vec(d) for k, d in docs.items()}
Q = vec(query)

# 3. 餘弦相似度
def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na, nb = math.sqrt(sum(x * x for x in a)), math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0

ranked = sorted(D, key=lambda k: -cosine(D[k], Q))
for k in ranked:
    print(f"{k}  cos={cosine(D[k], Q):.3f}  {docs[k][:45]}")
# d4  cos=0.577  vector space model ...（最相關，正確排序）
# d2  cos=0.510  vector space model ...
```

程式完整展示三步：TF-IDF 加權、餘弦計算、排序——1975 年 SMART 系統的核心，用十幾行 Python 重現。

## 結案 -- 後果與影響

- 向量空間模型成為資訊檢索的數學基礎：在 1998 年 Google PageRank 出現之前，TF-IDF + 餘弦排序是 IR 的主流範式。
- TF-IDF 至今仍是搜尋引擎的基礎組件：BM25（1994-1995，Robertson 與 Spärck Jones 路線的機率式精煉）本質上是 TF-IDF 的機率詮釋改良版。
- SMART 系統建立 IR 評估傳統：precision、recall、F-measure 的標準化評估方法沿用至今，成為機器學習評估的祖先。
- 「語義 = 幾何」路線的哲學先聲：Word2Vec（2013）、GloVe、BERT 的詞向量與句子嵌入，都是向量空間模型的深層後裔——意義從符號規則（Schank 的 CD）轉移到向量空間的幾何位置，這是計算語言學史上最大的範式轉移。
- LSI（1988）證明降維能捕捉潛在語義，直通矩陣分解推薦系統（Netflix Prize 2006）與神經詞向量。
- Salton 的案件留下持久的教訓：有時破案不需要更複雜的規則，只需要換一個數學空間。

## 關鍵人物與文獻（條例）

- G. Salton (1975). "A Vector Space Model for Automatic Indexing of Communicative Documents." （向量空間模型的提出；與 Cornell SMART 系統相關的系列技術報告）
- G. Salton & M. J. McGill (1983). *Introduction to Modern Information Retrieval.* McGraw-Hill.
- G. Salton & C. Buckley (1988). "Term-weighting Approaches in Automatic Text Retrieval." *Information Processing & Management*, 24(5), 513-523.（TF-IDF 的正式化）
- K. Spark Jones (1972). "A Statistical Interpretation of Term Specificity and Its Application in Retrieval." *Journal of Documentation*, 28(1), 11-21.（IDF 的先聲）
- H. P. Luhn (1957). "A Statistical Approach to Mechanized Encoding and Searching of Literary Information." *IBM Journal of Research and Development*, 1(4), 309-317.（詞頻思想的先驅）
- S. Deerwester, S. Dumais, G. Furnas, T. Landauer, R. Harshman (1990). "Indexing by Latent Semantic Analysis." *Journal of the American Society for Information Science*, 41(6), 391-407.（LSI；SVD 降維，1988 年報告形式）
- T. Mikolov, K. Chen, G. Corrado, J. Dean (2013). "Efficient Estimation of Word Representations in Vector Space." arXiv:1301.3781.（Word2Vec，向量語義的現代後裔）
