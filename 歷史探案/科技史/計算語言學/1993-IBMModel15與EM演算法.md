# 1993-IBMModel15與EM演算法

## 案件摘要

1993 年，Brown 等人在 Computational Linguistics 19(2) 發表《The Mathematics of Statistical Machine Translation: Parameter Estimation》，把統計機翻的數學基礎徹底寫清楚。1988 年的 Model 1-2 用均勻對齊假設太粗糙，無法處理詞序重排與一詞多譯。本案的懸案是：詞對齊是隱變量，沒有人標註哪個英文詞對應哪個法文詞，如何在看不見對齊的情況下學出精確的翻譯模型？破案工具是 EM 演算法：先猜對齊（E-step），再按猜測更新參數（M-step），迴圈直到收斂。

## 前因 -- 為什麼會有這個案子

- 1988 年 IBM Model 1-2 太粗糙：均勻對齊假設忽略詞序重排（英法文的形容詞位置不同）、也無法處理「一個英文詞對應多個法文詞」。
- EM 演算法已經成熟：Baum-Welch 1970 用於 HMM，Dempster-Laird-Rubin 1977 的論文給出一般性證明。
- 需要更精確的對齊模型才能提升翻譯品質；Canadian Hansards 的 220 萬句對等著被更有效地利用。
- IBM 團隊要在數學上證明：這套「隱變量 + 迭代估計」的方法有理論保證（概似單調上升）。

## 線索與推理 -- 數學式、程式、理論

### IBM Model 1-5 的漸進複雜化

五個模型像推理劇的層層揭案，每一代修正前一模型的假設：

- Model 1（均勻對齊）：每個英文詞等機率對齊每個法文詞，$P(a \mid e, f)$ 均勻。
- Model 2（位置對齊）：對齊機率取決於位置，$P(a_j \mid j, l_e, l_f)$。
- Model 3（fertility 發射次數 + NULL 詞）：引入 fertility $\phi(i)$——英文詞 i 產生幾個法文詞；加入虛構的 NULL 詞吸收插入的詞。
- Model 4（相對位置扭曲 distortion）：對齊位置以「相對位移」建模，$P(a_j - a_{j-1})$ 取代絕對位置。
- Model 5（避免重複佔位）：修正 Model 3-4 中多個詞佔同一位置的機率洩漏。

翻譯機率的完整式（Model 3 簡化形式）：

$$
P(f, a \mid e) = \prod_{i=1}^{l_e} \binom{l_f}{\phi(i)} \phi(i)!\, n(\phi(i) \mid e_i) \prod_{j=1}^{l_f} t(f_j \mid e_{a_j})\, d(j \mid a_j, l_e, l_f)
$$

### 對齊變數的 EM 推導

對齊變數 $a_j$ 是法文位置 j 對應的英文位置。因為 $a$ 是隱變量，對數概似 $\log P(f \mid e)$ 中對 $a$ 的求和無法分離，EM 藉下界迭代：

**E-step**：在當前參數 $\theta^{(t)}$ 下，計算後驗對齊機率：

$$
Q(a) = P(a \mid f, e; \theta^{(t)}), \qquad \delta_{ij} = P(a_j = i \mid f_j, e_i) = \frac{t(f_j \mid e_i)}{\sum_{i'} t(f_j \mid e_{i'})}
$$

**M-step**：最大化期望對數概似，更新參數：

$$
t^{(t+1)}(f_j \mid e_i) = \frac{\text{累積的 } \delta_{ij}}{\text{對 } j \text{ 累積的 } \delta_{ij}}
$$

### EM 的數學與單調上升證明

Dempster-Laird-Rubin 1977 證明：每次迭代概似不減——

$$
\theta^{(t+1)} = \arg\max_\theta E\left[\log L(\theta) \,\middle|\, \theta^{(t)}\right] \implies L(\theta^{(t+1)}) \geq L(\theta^{(t)})
$$

證明骨架：$\log L(\theta) = Q(\theta \mid \theta^{(t)}) + H(\theta \mid \theta^{(t)})$，其中 $H \geq 0$ 由 Jensen 不等式保證；最大化 $Q$ 就抬高了下界，故概似單調上升。這個保證讓「看不見對齊也能學模型」從啟發式變成有理論根基的方法。GIZA++（Och 與 Ney 2003）將 Model 1-5 + HMM 的訓練流程實作成高效工具。

### Python 實作 IBM Model 1-3 的 EM 迭代

```python
# IBM Model 1 -> 簡化 Model 3（含 fertility）的 EM 迭代，小語料收斂示範
parallel = [
    (["the", "house"],          ["la", "maison"]),
    (["the", "green", "house"], ["la", "maison", "verte"]),
    (["green", "book"],         ["livre", "vert"]),
]

en_vocab = sorted({w for e, _ in parallel for w in e})
fr_vocab = sorted({w for _, f in parallel for w in f})

def em_model1(parallel, en_vocab, fr_vocab, epochs=12):
    t = {(fe, ee): 1 / len(fr_vocab) for fe in fr_vocab for ee in en_vocab}
    ll_hist = []
    for _ in range(epochs):
        count, total, ll = {}, {}, 0.0
        for e_sent, f_sent in parallel:
            for fj in f_sent:
                s = sum(t.get((fj, ei), 0) for ei in e_sent)
                ll += (s / len(e_sent)) if s > 0 else 1e-12   # E-step 概似追蹤
                for ei in e_sent:
                    delta = t.get((fj, ei), 0) / s             # 後驗對齊機率
                    count[(fj, ei)] = count.get((fj, ei), 0) + delta
                    total[ei] = total.get(ei, 0) + delta
        t = {k: count[k] / total[k[1]] for k in count}         # M-step 更新
        ll_hist.append(ll)
    return t, ll_hist

def fertility(t, e_sent, f_sent):
    """簡化 Model 3：每個英文詞的期望發射次數（期望 fertility）"""
    fert = {ei: 0.0 for ei in e_sent}
    for fj in f_sent:
        z = sum(t.get((fj, ei), 0) for ei in e_sent)
        for ei in e_sent:
            fert[ei] += t.get((fj, ei), 0) / z
    return fert

t, ll_hist = em_model1(parallel, en_vocab, fr_vocab)

print("對數概似（應單調上升）：")
print([round(v, 4) for v in ll_hist])
print("\n收斂後的關鍵詞對機率 t(f|e)：")
for pair in [("maison", "house"), ("verte", "green"), ("livre", "book"), ("la", "the")]:
    print(f"t({pair[0]} | {pair[1]}) = {t.get(pair, 0):.4f}")
print("\n期望 fertility（'the' 攤到多個法文詞 -> 低 fertility）：")
print(fertility(t, ["the", "green", "house"], ["la", "maison", "verte"]))
```

## 結案 -- 後果與影響

- SMT 的數學基礎確立：GIZA++（對齊）+ n-gram 語言模型 + 解碼器 = phrase-based SMT（Och 2003），成為 2000s 的標準架構。
- Google Translate（2006）以此架構上線，統計機翻贏得對規則法的最終勝利。
- EM 演算法成為 NLP 標配：HMM 訓練（Baum-Welch）、詞對齊、主題模型 LDA（2003）都用 EM 迭代。
- 「隱變量 + EM」的思想影響日後的無監督學習：先猜隱結構、再更新參數的迴圈是變分推斷與 EM 型深度學習的先祖。
- 對齊模型的可解釋性成為資產：詞對齊圖至今仍是分析翻譯與跨語言詞向量的診斷工具。

## 關鍵人物與文獻

- Peter F. Brown, Stephen A. Della Pietra, Vincent J. Della Pietra & Robert L. Mercer (1993). The Mathematics of Statistical Machine Translation: Parameter Estimation. Computational Linguistics 19(2), 263-311.
- A. P. Dempster, N. M. Laird & D. B. Rubin (1977). Maximum Likelihood from Incomplete Data via the EM Algorithm. Journal of the Royal Statistical Society B 39(1), 1-38.
- Leonard Baum et al. (1970). A Maximization Technique Occurring in the Statistical Analysis of Probabilistic Functions of Markov Chains. Annals of Mathematical Statistics 41(1), 164-171.
- Franz Josef Och & Hermann Ney (2003). A Systematic Comparison of Various Statistical Alignment Models. Computational Linguistics 29(1), 19-51（GIZA++）.
- Franz Josef Och (2003). Minimum Error Rate Training in Statistical Machine Translation. ACL 2003.
- Philipp Koehn, Franz Josef Och & Daniel Marcu (2003). Statistical Phrase-Based Translation. NAACL 2003.
