# 1988-Brown統計機器翻譯

## 案件摘要

1988 年，IBM T.J. Watson 研究中心的 Peter Brown 等人在 COLING 會議發表《A Statistical Approach to Machine Translation》（正式版刊於 Computational Linguistics 16(2), 1990），把翻譯徹底重新定義為「機率推斷」問題。他們借用語音識別的 noisy channel 數學，用 220 萬句對的 Canadian Hansards 語料訓練翻譯模型。本案的懸案是：規則式機器翻譯三十年來在 ALPAC 1966 報告的陰影下停滯不前，翻譯品質始終無法突破。破案時刻：翻譯 = 找出「最像英文、最可能由法文產生」的英文句子。

## 前因 -- 為什麼會有這個案子

- 規則法 MT 的失敗：ALPAC 1966 報告否定了機翻的進展，研究經費冷卻近二十年；SYSTRAN 仍在運作但品質有瓶頸。
- 規則法的結構性問題：詞典 + 語法規則 + 轉換規則的手工工程，每加一種語言組合成本倍增。
- IBM 的語音識別傳統：noisy channel model 在語音識別已經成功——語音的數學可以直接移植到翻譯。
- Canadian Hansards（加拿大國會英法雙語記錄，220 萬句對）是現成的大規模平行語料庫，免費、高品質。
- Brown 等人大多是語音識別出身的數學家與工程師，沒有翻譯理論包袱，敢於「用資料暴力」。

## 線索與推理 -- 數學式、程式、理論

### Noisy Channel Model

翻譯被建模成「法文句子 f 是由英文句子 e 經過雜訊通道扭曲而來」。要翻譯，就是反推最可能的源頭：

$$
\hat{e} = \arg\max_{e} P(e \mid f) \propto \arg\max_{e} P(f \mid e)\, P(e)
$$

- 翻譯模型 $P(f \mid e)$：英文如何產生法文（詞的對應關係）。
- 語言模型 $P(e)$：英文句子本身有多通順（n-gram 機率）。

兩個模型分開估計，再組合解碼——這個分解是整個統計機翻的架構核心。

### IBM Model 1 與 Model 2

Model 1 假設詞對齊均勻：英文句 e 的每個詞「等機率」地產生法文句 f 的每個詞：

$$
P(f \mid e) = \frac{\epsilon}{l_f^{l_e}} \prod_{j=1}^{l_f} \sum_{i=1}^{l_e} t(f_j \mid e_i)
$$

其中 $t(f_j \mid e_i)$ 是詞對詞的翻譯機率，$\epsilon$ 是正規化常數。Model 2 加入位置對齊機率：

$$
P(j \mid i, l_e, l_f)
$$

讓「英文第 i 個詞對齊到法文第 j 個位置」有自己的機率分佈。

### EM 演算法

詞對齊是隱變量（沒有人標註哪個詞對應哪個詞），用 Baum-Welch 1970 的 EM 演算法估計：

- E-step：在當前參數下，計算每個對齊的後驗機率。
- M-step：按後驗機率加權重新統計詞翻譯機率 $t(f_j \mid e_i)$。
- 迭代至收斂，對數概似單調上升。

### 語言模型評估：perplexity

語言模型用困惑度（perplexity）評估：

$$
\text{PP} = P(w_1 w_2 \cdots w_n)^{-\frac{1}{n}} = \exp\left( -\frac{1}{n} \sum_{i=1}^{n} \log P(w_i \mid w_{i-1}) \right)
$$

PP 越低，模型對文本的「預測能力」越強。這些元素（翻譯模型 + 語言模型 + 解碼）構成了 Candide 計劃（1990s）的藍圖。

### Python 實作 mini IBM Model 1

```python
# mini IBM Model 1：EM 迭代估計詞對齊機率（小語料 demo）
parallel = [
    (["the", "house"],   ["la", "maison"]),
    (["the", "green", "house"], ["la", "maison", "verte"]),
    (["green", "book"],  ["livre", "vert"]),
]

en_vocab = sorted({w for e, _ in parallel for w in e})
fr_vocab = sorted({w for _, f in parallel for w in f})

def train_em(parallel, en_vocab, fr_vocab, epochs=10):
    # 初始化：t(f|e) 均勻分佈
    t = {(fe, ee): 1 / len(fr_vocab) for fe in fr_vocab for ee in en_vocab}
    for _ in range(epochs):
        count, total = {}, {}
        # E-step：對每個句對，計算後驗對齊機率
        for e_sent, f_sent in parallel:
            for fj in f_sent:
                z = sum(t.get((fj, ei), 0) for ei in e_sent)
                for ei in e_sent:
                    delta = t.get((fj, ei), 0) / z
                    count[(fj, ei)] = count.get((fj, ei), 0) + delta
                    total[ei] = total.get(ei, 0) + delta
        # M-step：按後驗加權更新 t(f|e)
        t = {k: count[k] / total[k[1]] for k in count}
    return t

t = train_em(parallel, en_vocab, fr_vocab)

def translate_word_probs(e_sent, t):
    """對英文句每個詞，列出最可能的法文對應"""
    out = {}
    for ei in e_sent:
        pairs = sorted(((fe, p) for (fe, ee), p in t.items()
                        if ee == ei), key=lambda x: -x[1])
        out[ei] = pairs[:3]
    return out

for ei, pairs in translate_word_probs(["the", "green", "house"], t).items():
    print(ei, "->", pairs)
# 收斂後："the" 的機率質量攤到 la/maison/verte（因均勻對齊假設），
# 但 "house -> maison"、"green -> verte" 應取得最高機率。
```

## 結案 -- 後果與影響

- 統計機器翻譯（SMT）誕生，規則法 MT 全面退守；翻譯研究的重心從語言學轉向統計學。
- IBM Model 3-5（Brown et al. 1993）補齊完整數學，形成漸進複雜化的模型家族。
- Candide 計劃在 1990s 展示 SMT 的可行性；Google Translate（2006）用 phrase-based SMT 上線，統計法贏得最終勝利。
- 「資料 + 機率 > 手工規則」的哲學定調，成為 1990s-2000s NLP 的主流意識形態。
- noisy channel 的思想延續到語音識別、拼字校正、日後的 seq2seq 與神經機器翻譯。

## 關鍵人物與文獻

- Peter F. Brown, John Cocke, Stephen A. Della Pietra, Vincent J. Della Pietra, Fredrick Jelinek, John D. Lafferty, Robert L. Mercer & Paul S. Roossin (1990). A Statistical Approach to Machine Translation. Computational Linguistics 16(2), 79-85（1988 COLING 會議先發）.
- Peter F. Brown, Stephen A. Della Pietra, Vincent J. Della Pietra & Robert L. Mercer (1993). The Mathematics of Statistical Machine Translation: Parameter Estimation. Computational Linguistics 19(2), 263-311.
- John Hutchins (1986). Machine Translation: Past, Present, Future. Ellis Horwood.
- ALPAC (1966). Language and Machines: Computers in Translation and Linguistics. National Research Council Report.
- Leonard Baum et al. (1970). A Maximization Technique Occurring in the Statistical Analysis of Probabilistic Functions of Markov Chains. Annals of Mathematical Statistics 41(1), 164-171.
- Adam Lopez (2008). Statistical Machine Translation. ACM Computing Surveys 40(3), 1-49.
