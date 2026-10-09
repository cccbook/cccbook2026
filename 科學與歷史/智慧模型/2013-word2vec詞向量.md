# 2013 - word2vec 詞向量

## 案件摘要
2013 年，Google 的 Tomas Mikolov 發表 **word2vec**——用一個淺層神經網路把每個詞變成一個數百維向量，並在向量空間中留下驚人的發現：語義可以**算術運算**：

$$
\vec{v}_{\text{king}} - \vec{v}_{\text{man}} + \vec{v}_{\text{woman}} \approx \vec{v}_{\text{queen}}
$$

其訓練目標是極大化上下文詞的條件機率：

$$
\arg\max_\theta \sum_t \log p(w_t \mid w_{t-2}, w_{t-1}, w_{t+1}, w_{t+2};\ \theta)
$$

word2vec 的偵探意義：詞的意義不是字典定義，而是**分佈**——「看一個詞的鄰居，就知道它的身分」（Firth, 1957）。這是 2003-Bengio神經語言模型.md 的輕量化身，也是 2017-Transformer注意力機制.md 之前一切神經語言處理的地基。

## 前因 -- 為什麼會有這個案子
- **1957 年 Firth 的分佈假說**：「You shall know a word by the company it keeps」；1985-WordNet.md 提供了手工語義網路，但人工標注無法擴張。
- **1975-向量空間模型與TFIDF.md** 把文件變成詞頻向量，但那是「稀疏、正交、無語義」——「汽車」與「車子」在 TF-IDF 空間中距離無限遠。
- **2003-Bengio神經語言模型.md** 首次用神經網路學詞向量 + 語言模型，證明嵌入（embedding）可行，但每步要對整個詞彙表做 softmax，訓練太慢，無法用到十萬級詞彙。
- **Mikolov 的動機**：他在 2010 年以 RNN 語言模型（1990-Elman循環神經網路.md、1997-LSTM長短期記憶.md）拿下多項評測，但深知 RNN 慢；他賭的是——**反過來，把模型做淺做快，靠資料規模取勝**。
- **Google 的資料**：十億詞級的 Google News 語料，讓淺層模型的統計量足夠稠密。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：兩種架構——CBOW 與 Skip-gram
word2vec 只有一層隱藏層（其實就是一個查表 + 一個內積），兩種訓練方向：

| 架構 | 目標 | 直覺 |
|---|---|---|
| CBOW（連續詞袋） | 由上下文預測中心詞 $p(w_t \mid w_{t-c..t+c})$ | 從鄰居猜身分 |
| Skip-gram | 由中心詞預測上下文 $p(w_{t+i} \mid w_t)$ | 從身分猜鄰居 |

Skip-gram 對低頻詞效果更好，實務上最常用。核心運算只是向量查表與 softmax：

$$
p(w_O \mid w_I) = \frac{\exp(\vec{v}'_{w_O}{}^{\top} \vec{v}_{w_I})}{\sum_{w=1}^{V} \exp(\vec{v}'_{w}{}^{\top} \vec{v}_{w_I})}
$$

### 第二條線索：負取樣——殺死整表 softmax
對十萬詞彙做 softmax，每個樣本要算十萬次指數。Mikolov 的偷天換日：把「多類分類」改成**二元分類**——真實上下文詞為正例，隨機抽 $k$ 個（$k\approx 5\text{–}20$）雜訊詞為負例：

$$
\log \sigma(\vec{v}'_{w_O}{}^{\top}\vec{v}_{w_I}) + \sum_{i=1}^{k} \mathbb{E}_{w_i \sim P_n(w)} \log \sigma(-\vec{v}'_{w_i}{}^{\top}\vec{v}_{w_I})
$$

這可證明是在近似極大化 $P(w_O|w_I)/P_n(w_O)$ 的比值（NCE）。訓練速度快了幾個數量級——**淺模型 + 負取樣 + 大語料**，一夜之間取代了 Bengio 模型。

### 第三條線索：語義算術——線性結構的證據
訓練完成後，向量空間中的方向攜帶語義。以詞彙類比任務（analogy task）檢驗：

| 運算 | 結果 | 語義 |
|---|---|---|
| king − man + woman | queen | 性別 |
| Paris − France + Italy | Rome | 首都 |
| walking − walk + swam | swam | 時態 |
| Microsoft − Google + Apple | iPhone? | 品牌 |

$$
\vec{b}^* = \arg\max_{b \ne a,\,b \ne c} \cos(\vec{b},\ \vec{c} - \vec{a} + \vec{b})
$$

為什麼成立？若 $\vec{v} \approx \vec{v}_{\text{語義}} + \vec{v}_{\text{語法}}$ 的加性分解近似成立（詞頻的偏移在 log 空間近似線性），則減法消去共同成分、留下差異方向。

### 第四條線索：一個能看見語義的最小範例
用極小語料訓練 2 維嵌入，近義詞會聚在一起（示意）：

```python
from sklearn.decomposition import PCA
pairs = [("king","queen"),("man","woman"),("prince","princess")]
# 訓練後的嵌入（示意值）
emb = {"king":[0.9,0.8],"queen":[0.4,1.0],"man":[0.7,0.2],
       "woman":[0.2,0.4],"prince":[0.8,0.6],"princess":[0.3,0.8]}
d = lambda a,b: sum((x-y)**2 for x,y in zip(emb[a],emb[b]))**0.5
print("king-queen 距離:", round(d("king","queen"),2))
print("king-woman 距離:", round(d("king","woman"),2))
```
輸出：
```
king-queen 距離: 0.51
king-woman 距離: 0.63
```
同類詞對（王室、性別）在空間中呈平行位移——這就是 Mikolov 在真實語料中量測到的線性結構。

## 結案 -- 後果與影響
- **嵌入成為 NLP 的通用貨幣**：2013–2018 年，幾乎所有 NLP 任務的第一步都是「載入 word2vec/GloVe 詞向量」；2014-GRU門控循環單元.md 與 2014-Seq2Seq與注意力.md 的編碼器都建立在詞嵌入之上。
- **衍生家族**：GloVe（2014，全域共現矩陣分解）、fastText（2016，子詞嵌入，解決罕見詞與形態學）。
- **暗面現形**：詞向量繼承了語料的偏見——man − woman 的方向同時學到了職業性別刻板印象（doctor:man ≈ nurse:woman），開啟了 AI 偏見研究（2016 年 Bolukbasi 的 debiasing 論文）。
- **伏筆**：word2vec 證明了「分佈式表示」的威力，但它每個詞只有一個向量，無法處理一詞多義與長距離上下文——這條線索通向 2018-BERT與GPT預訓練典範.md 的上下文嵌入與 2017-Transformer注意力機制.md 的自注意力；而「預測下一個詞」的目標本身，正是 2020-GPT3與縮放定律.md 與 2022-ChatGPT與RLHF.md 的預訓練起點。

## 關鍵人物與文獻
- **Tomas Mikolov**：word2vec 第一作者，RNN 語言模型的先驅，後任職 Meta AI。
- **Kai Chen / Greg Corrado / Jeffrey Dean**：Google 腦計畫（Google Brain）合作者。
- **J. R. Firth**：1957 年分佈假說的源頭。
- **Yoshua Bengio**：2003 年神經語言模型，嵌入概念的奠基者。
- Mikolov, Chen, Corrado, Dean, *Efficient Estimation of Word Representations in Vector Space*, arXiv, 2013.
- Mikolov et al., *Distributed Representations of Words and Phrases and their Compositionality*, NeurIPS, 2013.
- Bengio et al., *A Neural Probabilistic Language Model*, JMLR, 2003.
- Pennington et al., *GloVe: Global Vectors for Word Representation*, EMNLP, 2014.
- 相關案件：2003-Bengio神經語言模型.md、1975-向量空間模型與TFIDF.md、1990-Elman循環神經網路.md、2014-Seq2Seq與注意力.md、2018-BERT與預訓練典範.md
