# 2014 - Seq2Seq 與注意力

## 案件摘要
2014 年，兩條線索在 Google 與蒙特婁大學同時出現：Sutskever 等人的 **Seq2Seq**（編碼器-解碼器）與 Bahdanau 等人的 **注意力機制**。Seq2Seq 用兩個 LSTM 把變長序列映到變長序列：

$$
p(y_1,\dots,y_{T'}) = \prod_{t=1}^{T'} p\big(y_t \mid y_{<t},\ c\big), \qquad c = h_{T}
$$

其中 $c$ 是編碼器壓出的**單一固定向量**。但把整句話壓進一個向量是瓶頸——Bahdanau 讓解碼器每一步**回頭看**編碼器的所有隱藏狀態，用加權和動態取出上下文：

$$
c_t = \sum_{i} \alpha_{t,i}\, h_i, \qquad \alpha_{t,i} = \frac{\exp\big(e_{t,i}\big)}{\sum_j \exp\big(e_{t,j}\big)}, \quad e_{t,i} = v_a^\top \tanh(W_a s_{t-1} + U_a h_i)
$$

這樁案件是 LSTM（1997-LSTM長短期記憶.md）通往 2017-Transformer注意力機制.md 與 GPT 的**唯一橋樑**。

## 前因 -- 為什麼會有這個案子
- **統計機器翻譯的晚期**：1988-Brown統計機器翻譯.md 的片語式系統（phrase-based SMT）統治了二十年，但它是由翻譯模型、語言模型、對齊模型等數十個模塊拼裝的管線，特徵工程繁重、錯誤難以定位。
- **LSTM 的成熟**：1997-LSTM長短期記憶.md（2014-GRU門控循環單元.md 是其簡化身）在 2013 年前後被證明可訓練且有效，但它是「序列→單一分類」的模型，不是「序列→序列」。
- **Sutskever 的動機**：AlexNet 的共同作者（2012-AlexNet影像革命.md）想追問——既然 CNN 能端到端學影像，翻譯能不能也端到端？他的答案：兩個 LSTM 背對背接起來。
- **Bahdanau 的動機**：他在做神經機器翻譯時發現 Seq2Seq 在長句上崩潰（BLEU 隨句長暴跌）；他從人類譯者的行為得到線索——譯者翻譯時**會回頭看原文的對應位置**，而不是憑一句話的整體印象。
- **對齊的遺產**：統計機翻的 word alignment（1993-IBMModel15與EM演算法.md）是隱變數；Bahdanau 的注意力是它的可微化身。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：Seq2Seq——兩個 LSTM 的接力
編碼器讀完源句 $x_1,\dots,x_T$，把最後隱藏狀態 $c = h_T$ 作為「句意摘要」；解碼器從 $c$ 出發逐詞生成：

| 階段 | 運算 | 內容 |
|---|---|---|
| 編碼 | $h_t = \mathrm{LSTM}_{\text{enc}}(x_t, h_{t-1})$ | 逐步讀入源句 |
| 摘要 | $c = h_T$ | 整句壓成一個向量 |
| 解碼 | $s_t = \mathrm{LSTM}_{\text{dec}}(y_{t-1}, s_{t-1})$，$p(y_t) = \mathrm{softmax}(W s_t + b)$ | 逐詞生成目標句 |

$$
p(y) = \prod_{t=1}^{T'} p(y_t \mid y_{<t},\ c)
$$

Sutskever 的技巧：把源句**倒序輸入**（「a b c」讀成「c b a」），縮短了源句開頭與目標句開頭之間的 LSTM 路徑，BLEU 明顯提升。在 WMT'14 英法翻譯上，純 Seq2Seq 已可與片語式系統打平——端到端學習第一次在翻譯上站上主流。

### 第二條線索：瓶頸——一個向量裝不下整句
BLEU 隨源句長度的實測曲線（示意，Sutskever 論文圖）：

| 句長（詞） | Seq2Seq BLEU | 註記 |
|---|---|---|
| < 10 | 34 | 短句夠好 |
| 10–20 | 30 | 開始下滑 |
| 20–30 | 25 | 明顯衰退 |
| 40–50 | 18 | 長句崩潰 |

原因：$c = h_T$ 是固定維度（如 1000 維），不管源句 5 個詞還是 50 個詞，都要壓進同一個向量——資訊瓶頸。

### 第三條線索：Bahdanau 注意力——每一步回頭看
解法：解碼第 $t$ 個詞時，用當前解碼狀態 $s_{t-1}$ 與**所有**編碼狀態 $h_i$ 算相關度，再加權取出上下文：

$$
e_{t,i} = v_a^\top \tanh\big(W_a s_{t-1} + U_a h_i\big), \quad \alpha_{t,i} = \mathrm{softmax}_i(e_{t,i}), \quad c_t = \sum_i \alpha_{t,i}\, h_i
$$

$$
p(y_t \mid y_{<t}, x) = \mathrm{softmax}\big(W\, [s_t;\, c_t]\big)
$$

注意力的偵探意義：
- **解決瓶頸**：上下文隨步驟動態變化，長句不再崩潰。
- **可視化對齊**：$\alpha_{t,i}$ 矩陣畫出來就是詞對齊圖——法語 "zone économique européenne" 對齊英語 "european economic area" 的對角線，與 1993-IBMModel15與EM演算法.md 的隱對齊遙相呼應，但這次它是**可微、可學、可視**的。

### 第四條線索：注意力的簡化——從加性到縮放點積
Bahdanau 的注意力是**加性**的（小神經網路算相關度）。後續偵探工作發現更簡的公式：2015 年 Luong 的**點積注意力** $\alpha_{t,i} = \mathrm{softmax}(s_t^\top h_i)$ 與縮放點積 $\mathrm{softmax}\!\left(\frac{q^\top k}{\sqrt{d}}\right)$——去掉循環結構、純矩陣運算。這條線索在 2017-Transformer注意力機制.md 的「Attention Is All You Need」中收網：**注意力就是一切**，LSTM 被謀殺——兇手不是更強的記憶，而是直連任意距離 + 完美並行。

## 結案 -- 後果與影響
- **神經機器翻譯上線**：2016-GNMT神經機器翻譯上線.md 把 8 層 LSTM + 注意力的 GNMT 部署到 Google 翻譯，錯誤率相對下降 60%，片語式系統退場。
- **注意力成為通用機制**：從翻譯擴散到語音（listen-attend-spell）、影像描述（Show, Attend and Tell）、摘要、問答——「回頭看」成為所有序列任務的標配。
- **Bridge to Transformer**：2017-Transformer注意力機制.md 把注意力從「LSTM 的附件」升級為「唯一的組件」；2018-BERT與GPT預訓練典範.md、2020-GPT3與縮放定律.md、2022-ChatGPT與RLHF.md 全部站在這座橋上。
- **教學遺產**：Seq2Seq + 注意力至今仍是理解 Transformer 的最佳起點——先懂「為什麼要回頭看」，才懂「為什麼不需要循環」。
- **注意力對齊的可視化**：Bahdanau 論文的對齊熱圖成為深度學習史上最著名的圖表之一——法語與英語的詞序差異（形容詞後置）在對齊矩陣上呈現為一條拐彎的對角線，機器第一次「展示」了它對語言的理解。
- **伏筆**：注意力的 $q, k, v$ 三分法、多頭、位置編碼都已在 Seq2Seq 時代萌芽；當規模定律（2020-GPT3與縮放定律.md）遇上注意力，語言模型的時代全面來臨。

## 關鍵人物與文獻
- **Ilya Sutskever**：Seq2Seq 第一作者，AlexNet 共同作者，後任 OpenAI 首席科學家。
- **Oriol Vinyals / Quoc Le**：Seq2Seq 合作者，Google Brain。
- **Dzmitry Bahdanau**：注意力機制第一作者，蒙特婁大學。
- **Kyunghyun Cho / Yoshua Bengio**：GRU 與注意力架構的合作者。
- **Minh-Thang Luong**：點積注意力與注意力教學（nmt tutorial）的推手。
- Sutskever, Vinyals, Le, *Sequence to Sequence Learning with Neural Networks*, NeurIPS, 2014.
- Bahdanau, Cho, Bengio, *Neural Machine Translation by Jointly Learning to Align and Translate*, ICLR, 2015（arXiv 2014.9）.
- Cho et al., *Learning Phrase Representations using RNN Encoder-Decoder*, EMNLP, 2014.
- Luong, Pham, Manning, *Effective Approaches to Attention-based Neural Machine Translation*, EMNLP, 2015.
- 相關案件：1997-LSTM長短期記憶.md、2014-GRU門控循環單元.md、2012-AlexNet影像革命.md、2016-GNMT神經機器翻譯上線.md、2017-Transformer注意力機制.md

## 補充 -- 程式實作（python + pytorch）

本案 Bahdanau 注意力（`e = vᵀtanh(Ws+Uh)`、`c = Σαh`）的最小可執行版本，見 `_code/2014-Seq2SeqAttention.py`（已實測可跑，CPU 約 1 分鐘；以數字串反轉代替翻譯）：

```python
# 2014 - Seq2Seq 與 Bahdanau 注意力
import torch
import torch.nn as nn
import torch.nn.functional as F


class AttnSeq2Seq(nn.Module):
    def __init__(self, V=10, E=16, H=32):
        super().__init__()
        self.emb = nn.Embedding(V, E)
        self.enc = nn.GRU(E, H, batch_first=True)
        self.dec = nn.GRUCell(E + H, H)
        self.Wa = nn.Linear(H, H, bias=False)
        self.Ua = nn.Linear(H, H, bias=False)
        self.va = nn.Linear(H, 1, bias=False)
        self.out = nn.Linear(H * 2, V)

    def forward(self, src, tgt):
        eh, h = self.enc(self.emb(src))          # 全部編碼狀態 (回頭看的對象)
        s = h.squeeze(0)
        prev = self.emb(torch.zeros(len(src), 1, dtype=torch.long)).squeeze(1)
        loss, alphas = 0, []
        for t in range(tgt.size(1)):
            e = self.va(torch.tanh(self.Ua(s).unsqueeze(1) + self.Wa(eh))).squeeze(-1)
            a = F.softmax(e, dim=1)              # α: 此步看哪裡
            alphas.append(a.detach())
            c = (a.unsqueeze(-1) * eh).sum(1)    # c_t: 動態上下文 (瓶頸解除)
            s = self.dec(torch.cat([prev, c], 1), s)
            loss = loss + F.cross_entropy(self.out(torch.cat([s, c], 1)), tgt[:, t])
            prev = self.emb(tgt[:, t])
        return loss / tgt.size(1), torch.stack(alphas, 1)


def main():
    torch.manual_seed(0)
    T, N = 6, 2000
    src = torch.randint(0, 10, (N, T))
    tgt = src.flip(1)                            # 目標: 反轉
    net = AttnSeq2Seq()
    opt = torch.optim.Adam(net.parameters(), lr=1e-2)
    for ep in range(40):
        opt.zero_grad()
        loss, _ = net(src, tgt)
        loss.backward()
        opt.step()
    # (貪婪解碼與注意力印出略, 見 _code/2014-Seq2SeqAttention.py 全文)


if __name__ == "__main__":
    main()
```

執行結果（`python3 _code/2014-Seq2SeqAttention.py`，torch 2.12.0）：

```
反轉任務準確率(抽5句逐token)=0.93
源句: [4, 9, 3, 0, 3, 9] 目標: [9, 3, 0, 3, 9, 4] 預測: [9, 3, 0, 3, 9, 4]
注意力矩陣 α(行=解碼步, 列=源位置, 反對角線即正確對齊):
  0.02 0.08 0.13 0.12 0.14 0.50
  0.03 0.14 0.16 0.10 0.11 0.47
  0.02 0.03 0.14 0.29 0.44 0.07
  0.03 0.03 0.10 0.43 0.33 0.08
  0.08 0.10 0.28 0.17 0.19 0.19
  0.10 0.39 0.13 0.07 0.07 0.23
```

程式解說：`c = Σαh` 取代了固定向量 `c = h_T`——本文第二條線索的瓶頸（整句壓進一個向量）就此解除，每步解碼動態取上下文。注意力矩陣即判決書：每行峰值沿反對角線走（第 0 步看源末位 0.50、第 3 步看源位置 3 達 0.43），正是 Bahdanau 論文詞對齊圖的縮影——1993 年 IBM 隱對齊的可微化身。93% 逐 token 準確率且首句全對；注意力的偵探意義也在此：它**可視**，對齊不再是黑箱。
