# 1990-Elman循環神經網路

## 案件摘要
1990 年，UCSD 的認知科學家 Jeffrey Elman 在《Cognitive Science》發表《Finding Structure in Time》，提出 Simple Recurrent Network（SRN，俗稱 Elman 網路）。這個網路把「上一刻的隱層狀態」複製回輸入端，讓網路第一次真正擁有了「時間的記憶」。Elman 用它做了一個驚人的實驗：只訓練網路預測下一個詞，隱層表示中竟自動浮現出名詞、動詞、生命體等語法類別——不需要任何手工標記。這是詞向量（word embedding）思想的哲學先聲，也是循環神經網路成為序列建模標準的破案時刻。

## 前因 -- 為什麼會有這個案子
- 前饋網路（perceptron、多層感知器）的輸入是固定長度的向量，但語言是變長的序列：「我昨天去了書店」和「去」的長度天差地遠，前饋網路無從下手。
- 1987 年 Waibel 等人的時間延遲網路（TDNN）用固定長度的滑動視窗處理語音，仍只能看見有限窗口內的線索，記不住遠處的上下文。
- 1986 年 Rumelhart、Hinton、Williams 在《Nature》發表反傳播（backpropagation），多層網路的訓練難題已解，工具箱齊備。
- 1986 年 Michael Jordan 在《Serial Order: A Parallel Distributed Processing Approach》中提出輸出回饋式的循環架構（Jordan 網路），證明「回饋」是處理序列的可行路線。
- Elman 的核心疑問：網路能不能**自己**發現詞的語法類別，而不靠語言學家手工標記？要回答這題，網路必須能「記得」剛剛看過什麼。

## 線索與推理 -- 數學式、程式、理論

### Elman 網路（SRN）的架構
Elman 的關鍵手法：把隱層在時刻 $t-1$ 的狀態 $h_{t-1}$ 複製到一組 context unit，與當前輸入 $x_t$ 一起送入隱層：

$$h_t = \sigma(W_{hx} x_t + W_{hh} h_{t-1} + b)$$

其中 $\sigma$ 是 sigmoid 函數。context unit 就像偵探的筆記本：每次看新線索前，先把上一頁的筆記攤在桌上。隱層因此同時「看到」現在與（壓縮後的）過去。

### BPTT：沿時間展開的反傳播
訓練時，把循環網路沿時間展開成 $T$ 層的深層前饋網路，再用標準反傳播。隱層梯度沿時間倒傳：

$$\frac{\partial L}{\partial h_{t-k}} = \left( W_{hh}^\top \right)^k \frac{\partial L}{\partial h_t} \prod_{j=0}^{k-1} \mathrm{diag}\big(\sigma'(a_{t-j})\big)$$

這條式子預告了下一個案子：若 $W_{hh}$ 的譜半徑小於 1，梯度會連乘而**消失**；大於 1 則爆炸（vanishing/exploding gradient，Hochreiter 1991、Bengio 1994 將正式立案）。

### 破案時刻：隱層聚類自動浮現語法類別
Elman 訓練小型人工文法生成的句子，任務只有一個：預測下一個詞。訓練完後對隱層表示做階層式聚類，樹狀圖上自動分出名詞／動詞、有生命／無生命等類別。網路從「預測下一詞」這個單純的監督訊號中，自己學出了語法結構——這正是今日「分散式語義表示」的哲學起點。

### 對照：Jordan 網路
Jordan（1986）回饋的是**輸出層** $h_t = \sigma(W_{hx} x_t + W_{ho}\, y_{t-1})$；Elman 回饋的是**隱層**。隱層是可學習的壓縮表示，容量遠大於輸出，這是 SRN 勝出的關鍵差異。

### Python 示範：numpy 手刻 SimpleRNN
以下用 numpy 手刻 Elman 網路，訓練它預測人工文法的下一個詞，並展示隱層自動分群：

```python
import numpy as np
rng = np.random.default_rng(0)
words = ["boy", "girl", "chase", "see", "dog", "cat"]
V = len(words); w2i = {w: i for i, w in enumerate(words)}

def sample_sentence():
    # 簡單文法: [N-life N] [V] [N-life]
    s = [["boy", "girl"][rng.random() < .5], ["dog", "cat"][rng.random() < .5]]
    s += [["chase", "see"][rng.random() < .5], ["boy", "girl"][rng.random() < .5]]
    return s

def onehot(i):
    v = np.zeros(V); v[i] = 1.0; return v

d = 12  # Elman 網路參數
Wx = rng.normal(0, .3, (d, V)); Wh = rng.normal(0, .3, (d, d)); b = np.zeros(d)
Wy = rng.normal(0, .3, (V, d)); by = np.zeros(V)
sigmoid = lambda z: 1 / (1 + np.exp(-z))
softmax = lambda z: np.exp(z - z.max()) / np.exp(z - z.max()).sum()
lr = 0.3
for epoch in range(300):
    sent = sample_sentence()
    xs = [onehot(w2i[w]) for w in sent]
    T = len(xs)
    hs = [np.zeros(d)]
    for t in range(T):                     # 前向
        h = sigmoid(Wx @ xs[t] + Wh @ hs[-1] + b)
        hs.append(h)
    # 簡化 BPTT：只對最後數步截斷反傳（truncated BPTT）
    K = min(3, T)
    dWh = np.zeros_like(Wh); dWx = np.zeros_like(Wx)
    dWy = np.zeros_like(Wy); dby = np.zeros_like(by); db = np.zeros_like(b)
    dh_next = np.zeros(d)
    for t in range(T - 1, T - 1 - K, -1):
        y = softmax(Wy @ hs[t + 1] + by)
        dy = y.copy(); dy[w2i[sent[t]]] -= 1
        dh = Wy.T @ dy + dh_next
        dWy += np.outer(dy, hs[t + 1]); dby += dy
        dh_raw = dh * hs[t + 1] * (1 - hs[t + 1])
        dWh += np.outer(dh_raw, hs[t]); dWx += np.outer(dh_raw, xs[t])
        dh_next = Wh.T @ dh_raw
    for P, G in [(Wx, dWx), (Wh, dWh), (b, db), (Wy, dWy), (by, dby)]:
        P -= lr * G

# Elman 式觀察：收集每個詞在各上下文中出現時的隱層狀態，比較類內/跨類相似度
H = {w: [] for w in words}
for _ in range(3000):
    sent = sample_sentence(); h = np.zeros(d)
    for w in sent:
        h = sigmoid(Wx @ onehot(w2i[w]) + Wh @ h + b)
        H[w].append(h.copy())
cos = lambda a, c: float(a @ c / (np.linalg.norm(a) * np.linalg.norm(c)))
mn = lambda w: np.mean(H[w], axis=0)
nouns, verbs = ["boy", "girl", "dog", "cat"], ["chase", "see"]
intra = np.mean([cos(mn(a), mn(c)) for a in nouns for c in nouns if a < c])
cross = np.mean([cos(mn(a), mn(v)) for a in nouns for v in verbs])
print("類內(名詞-名詞)相似度:", round(intra, 3), "| 跨類(名詞-動詞):", round(cross, 3))
print("差異:", round(intra - cross, 3), "(>0 代表語法類別在隱層中自動分離)")
```

## 結案 -- 後果與影響
- 循環神經網路（RNN）正式成為變長序列建模的標準架構，語言與語音研究有了新武器。
- BPTT 的梯度消失問題隨後被正式立案（Hochreiter 1991、Bengio et al. 1994），埋下 LSTM（1997）的伏筆；Elman 的隱層聚類實驗則是現代詞嵌入的哲學先聲——「預測下一詞就能學出語義結構」在 word2vec（2013）應驗。
- RNN 在 2010 年代成為語音辨識與 NLP 主力（2014 年 Seq2Seq 的編碼器就是 RNN）；「連結主義 vs 規則主義」之爭也因 SRN 出現新戰場。

## 關鍵人物與文獻（條列，含真實文獻書目）
- Jeffrey L. Elman (1990). Finding Structure in Time. *Cognitive Science*, 14(2), 179–211.
- Michael I. Jordan (1986). Serial Order: A Parallel Distributed Processing Approach. ICS Report 8604, UC San Diego.
- Rumelhart, Hinton & Williams (1986). Learning representations by back-propagating errors. *Nature*, 323, 533–536.
- Hochreiter (1991). Untersuchungen zu dynamischen neuronalen Netzen. Diploma thesis, TU München.
- Bengio, Simard & Frasconi (1994). Learning Long-Term Dependencies with Gradient Descent is Difficult. *IEEE Trans. Neural Networks*, 5(2), 157–166.
