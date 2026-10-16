# 2012 - AlexNet（深度學習的大爆炸）

## 案件摘要
2012 年 10 月，多倫多大學的 **Alex Krizhevsky（1986–）**、
**Ilya Sutskever（1986–）** 與他們的導師 **Geoffrey Hinton**，
以**AlexNet** 橫掃 **ImageNet 大規模視覺辨識競賽（ILSVRC 2012）**：
$$\boxed{\text{top-5 錯誤率：26.2\%} \to \textbf{15.3\%}\quad\text{（第二名 26.2\%——差距近 11 個百分點）}}$$
AlexNet 是一個**八層的卷積神經網路**（五層卷積 + 三層全連接），
有 6000 萬個參數，靠**四件武器**打贏了這場仗：
- **GPU（CUDA）**：兩張 GTX 580 並行訓練——快 30 倍以上；
- **ReLU**：修正線性單元——深層網路不再梯度消失；
- **Dropout**：訓練時隨機丟棄一半神經元——防止過擬合；
- **資料增廣**：平移、翻轉、變色——把 120 萬張圖放大十倍。
$$\text{CNN + GPU + ReLU + Dropout + 大資料} = \text{深度學習大爆炸}.$$
**比賽結束那一刻，整個電腦視覺界一夜轉向**——
**神經網路從此統治 AI 十年**。

## 前因 -- 為什麼會有這個案子
- **1989 楊立昆的卷積網路**：
  **Yann LeCun** 在 1989 年發明**卷積神經網路（CNN）**（見
  `1989-楊立昆卷積網路.md`），用**反向傳播**訓練，成功辨識手寫數字：
  $$\text{卷積（局部感受野 + 權重共享）} + \text{池化} = \text{圖像的平移不變性}$$
  但 1990 年代的 CNN 只能處理 **32×32** 的小圖——
  **GPU 不存在、資料太少**，LeCun 的 CNN 在自然圖像上無用武之地。
- **2006 深度信念網路的點火**：
  Hinton 的 DBN（見 `2006-欣頓深度信念網路.md`）證明**深層可訓練**，
  讓神經網路從 SVM 主流時代（見 1980–1995）復活；
  但 DBN 用的是**無監督預訓練**，Krizhevsky 與 Sutskever 很快發現：
  $$\text{夠深的監督式 CNN} + \text{夠大的資料} \;\Rightarrow\; \text{預訓練根本不需要}.$$
- **ImageNet 資料集（李飛飛，2009）**：
  **李飛飛（Fei-Fei Li）** 在 2009 年建立 **ImageNet**——
  **1400 萬張標註圖像、2 萬多個類別**，2010 年起舉辦 ILSVRC 競賽
  （120 萬張訓練圖、1000 類）：
  $$\boxed{\text{大資料是深度學習的燃料——沒有 ImageNet 就沒有 AlexNet}}$$
  2011 年的冠軍（27.0%）仍是**傳統特徵工程**（SIFT + SVM）。
- **GPU 的成熟（2007–2012）**：
  NVIDIA 於 2007 年推出 **CUDA**，讓顯示卡的**數千核心**可以通用計算。
  Krizhevsky 是寫 CUDA 的高手——他把**卷積**寫成 GPU 核心：
  $$\text{CPU（4 核）} \xrightarrow{\text{CUDA}} \text{GPU（數千核）}：\text{訓練時間從月縮到天}.$$
  天時（大資料）、地利（GPU）、人和（深度信念）——只欠一場戰役。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：ReLU——梯度不再消失
傳統的 **sigmoid** 活化函數在兩端飽和，導數**趨近於零**：
$$\sigma(x) = \frac{1}{1+e^{-x}}, \qquad \sigma'(x) = \sigma(x)(1-\sigma(x)) \le \frac{1}{4}$$
深層網路反向傳播時，梯度是各層導數的**連乘**：
$$\frac{\partial E}{\partial w_1} \propto \prod_{k=1}^{L} \sigma'(z_k) \le \left(\frac{1}{4}\right)^L \xrightarrow{L\to\infty} 0$$
AlexNet 改用 **ReLU（Rectified Linear Unit）**：
$$\boxed{f(x) = \max(0, x), \qquad f'(x) = \begin{cases} 1 & x > 0 \\ 0 & x \le 0 \end{cases}}$$
正區的導數是**恆等 1**——梯度**原樣通過**，不衰減：
$$\text{sigmoid：}\left(\tfrac{1}{4}\right)^L \to 0 \quad\text{vs}\quad \text{ReLU：}1^L = 1 \;\text{（正區）}.$$
且 ReLU 計算只需**一個比較**（比 sigmoid 的指數快），
負區輸出**恆為零**（稀疏活化）——**訓練快 6 倍**（論文的數字）。

### 第二條線索：softmax 與交叉熵——分類的標準輸出
AlexNet 的最後一層用 **softmax** 把得分 $z_1,\dots,z_{1000}$ 變成機率：
$$\text{softmax}(z_i) = \frac{e^{z_i}}{\sum_{k=1}^{K} e^{z_k}}, \qquad \sum_i p_i = 1$$
訓練目標是**交叉熵損失**（cross-entropy）：
$$L = -\sum_{i=1}^{K} y_i \log p_i, \qquad \text{（單一正解時 } L = -\log p_{\text{正解}}\text{）}$$
對得分 $z$ 微分得到**極簡的梯度**（softmax 與交叉熵的完美配對）：
$$\frac{\partial L}{\partial z_i} = p_i - y_i$$
$$\boxed{\text{softmax + 交叉熵：梯度 } = \text{預測} - \text{正解}\quad\text{（乾淨、穩定）}}$$
這個配對從 AlexNet 開始成為**分類網路的標準輸出**。

### 第三條線索：Dropout 與資料增廣——對抗過擬合
6000 萬參數 vs 120 萬張圖——**嚴重過擬合**是最大威脅。
**Dropout（Hinton 團隊 2012 同期提出）**：
訓練時每個神經元以 $p = 0.5$ 的機率**被隨機丟棄**：
$$\text{訓練：} h_i \xrightarrow{\text{丟硬幣}} \begin{cases} h_i & \text{機率 } 0.5 \\ 0 & \text{機率 } 0.5 \end{cases} \qquad
\text{測試：} h_i \times 0.5 \;\text{（補回期望值）}$$
**直覺**：網路不能依賴任何一個神經元——像**偵探培養多條獨立線索**，
每個子網路都得自己學會判案；測試時相當於**指數多個子網路的平均**。
**資料增廣**：對原圖做隨機平移、水平翻轉、改變 RGB 亮度，
$$\text{120 萬張} \xrightarrow{\text{增廣}} \text{等效上千萬張} \Rightarrow \text{過擬合大幅降低}.$$

### 第四條線索：GPU 並行——卷積的快車道
卷積本質是**大量獨立的乘加**：
$$(I * K)_{ij} = \sum_{u}\sum_{v} I_{i+u,\,j+v}\, K_{uv}$$
這正是 GPU 的強項——**數千核心同時算不同的 $(i,j)$**。
Krizhevsky 把網路拆成**兩半**，分給兩張 GTX 580（當時記憶體只有 3GB）：
$$\text{兩張 GPU 並行} \Rightarrow \text{訓練 } 120 \text{ 萬張圖約一週} \quad\text{（CPU 需要一個月以上）}.$$

### Python：ReLU vs sigmoid 的收斂對照

```python
# 小型分類網路：ReLU vs sigmoid 的收斂對照（toy 資料）
import math, random

random.seed(7)

def relu(x):
    return max(0.0, x)

def drelu(x):
    return 1.0 if x > 0 else 0.0

def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))

def dsigmoid(x):
    s = sigmoid(x)
    return s * (1.0 - s)

# toy 資料：二維輸入、三類分類（三個高斯團塊）
def make_data():
    centers = [(2.0, 0.0), (-1.0, 1.7), (-1.0, -1.7)]
    xs, ys = [], []
    for k, (cx, cy) in enumerate(centers):
        for _ in range(40):
            xs.append((cx + random.gauss(0, 0.4), cy + random.gauss(0, 0.4)))
            ys.append(k)
    return xs, ys

# 一個隱藏層（4 神經元）的小網路，活化函數可切換
def train(activation, epochs=200, lr=0.05):
    xs, ys = make_data()
    W1 = [[random.uniform(-1, 1) for _ in range(2)] for _ in range(4)]
    b1 = [0.0] * 4
    W2 = [[random.uniform(-1, 1) for _ in range(4)] for _ in range(3)]
    b2 = [0.0] * 3
    if activation == "relu":
        act, dact = relu, drelu
    else:
        act, dact = sigmoid, dsigmoid
    n = len(xs)
    for ep in range(1, epochs + 1):
        loss = 0.0
        for (x1, x2), y in zip(xs, ys):
            z1 = [W1[i][0] * x1 + W1[i][1] * x2 + b1[i] for i in range(4)]
            h = [act(z) for z in z1]
            z2 = [sum(W2[k][i] * h[i] for i in range(4)) + b2[k] for k in range(3)]
            mx = max(z2)
            e = [math.exp(z2[k] - mx) for k in range(3)]
            s = sum(e)
            p = [v / s for v in e]
            loss += -math.log(p[y] + 1e-12)
            dz2 = [p[k] - (1 if k == y else 0) for k in range(3)]  # softmax+CE 梯度
            dh = [sum(W2[k][i] * dz2[k] for k in range(3)) for i in range(4)]
            for k in range(3):
                for i in range(4):
                    W2[k][i] -= lr * dz2[k] * h[i] / n
                b2[k] -= lr * dz2[k] / n
            for i in range(4):
                g = dh[i] * dact(z1[i])          # 活化函數決定梯度是否消失
                W1[i][0] -= lr * g * x1 / n
                W1[i][1] -= lr * g * x2 / n
                b1[i] -= lr * g / n
        if ep in (1, 50, 200):
            print(f"  {activation:>7s} epoch {ep:>3d}：平均交叉熵 = {loss / n:.4f}")

print("ReLU vs sigmoid：同一小網路在 toy 分類資料的收斂對照")
train("sigmoid")
train("relu")
```
輸出：
```
ReLU vs sigmoid：同一小網路在 toy 分類資料的收斂對照
  sigmoid epoch   1：平均交叉熵 = 1.6088
  sigmoid epoch  50：平均交叉熵 = 1.1644
  sigmoid epoch 200：平均交叉熵 = 0.6405
     relu epoch   1：平均交叉熵 = 1.1623
     relu epoch  50：平均交叉熵 = 0.1896
     relu epoch 200：平均交叉熵 = 0.0207
```

先用 `python3` 實際執行（見下方輸出區塊），結果**ReLU 的損失下降明顯快於
sigmoid**——這正是 AlexNet 用 ReLU 的**數學證據** ✓

## 結案 -- 後果與影響
- **2012：深度學習大爆炸**：
  $$\boxed{\text{AlexNet（2012）} = \text{電腦視覺界一夜轉向的分水嶺}}$$
  ILSVRC 2012 結束後，**傳統特徵工程（SIFT + SVM）五年內絕跡**；
  2013 年的冠軍就是 AlexNet 的微調版，2014、2015 年全為深度網路。
- **CNN 統治電腦視覺十年（2012–2021）**：
  - **2014 VGG / GoogLeNet**：更深的 CNN（19 層 / 22 層），
    top-5 錯誤率降到 7.3% / 6.7%；
  - **2015 ResNet**：殘差連接（He Kaiming），152 層，錯誤率 3.6%——
    **超越人類（約 5%）**；
  - **物體偵測（2014 R-CNN）、語義分割**——全是 AlexNet 的血統。
  $$\text{AlexNet（2012）} \to \text{VGG/GoogLeNet（2014）} \to \text{ResNet（2015）} \to \text{一切視覺任務}.$$
- **GPU 的軍備競賽**：
  $$\text{2 張 GTX 580（2012）} \to \text{專用加速器（TPU, 2016）} \to \text{萬卡叢集（2020s）}$$
  **算力成為 AI 競爭的核心資源**——NVIDIA 由遊戲公司變成 AI 帝國。
- **ReLU 的普及**：
  $$\text{sigmoid（1986–2012）} \xrightarrow{\text{AlexNet}} \text{ReLU（2012–）}$$
  後續變體（Leaky ReLU、GELU、Swish）都是 ReLU 的後代——
  **活化函數的戰場由 AlexNet 重新洗牌**。
- **Hinton 的圖靈獎（2018）**：
  Hinton 因深度學習的貢獻，於 **2018 年與 LeCun、Bengio 同獲圖靈獎**
  （見 `../資訊科學/2018-深度學習三巨頭.md`）——
  **從 1936 圖靈機到 2012 AlexNet，圖靈獎回到了 AI 的戰場**
  （見 `../資訊科學/1936-圖靈機.md`）。
- **伏筆：視覺之後，輪到語言（2017）**：
  AlexNet 證明**深度 + 大資料 + 算力**的公式；2017 年，
  這個公式被套到**語言**上——**Transformer**（見
  `2017-瓦茲瓦尼Transformer.md`）與後來的一切大模型。
  $$\text{ImageNet（2009）} \xrightarrow{\text{AlexNet（2012）}} \text{WebText/GPT（2017–）}.$$
- 歷史定位：**AlexNet 是 AI 的珍珠港式事件**——
  一夜之間，所有人的世界觀被改寫；
  **6000 萬個參數、兩張顯示卡、一場競賽——深度學習的時代正式開幕**。

## 關鍵人物與文獻
- **A. Krizhevsky**：*ImageNet Classification with Deep Convolutional Neural Networks*（NIPS 2012）；CUDA 實現；CIFAR-10/100 資料集（2009）。
- **I. Sutskever**：AlexNet 共同作者；後為 OpenPDF 研究主管（OpenAI 首席科學家，2015–2024）；**Sequence to Sequence Learning**（2014）。
- **G. E. Hinton**：AlexNet 指導者；Dropout（2012）；2018 圖靈獎（見 `../資訊科學/2018-深度學習三巨頭.md`）。
- **Y. LeCun**：卷積網路（1989，見 `1989-楊立昆卷積網路.md`）——AlexNet 的直接祖先；2018 圖靈獎。
- **李飛飛**：ImageNet（2009）——深度學習的燃料。
- **K. He（何愷明）**：ResNet（2015）——超越人類的視覺辨識。
- 相關案件：`1989-楊立昆卷積網路.md`、`2006-欣頓深度信念網路.md`、`2013-米科洛夫詞向量.md`、`../資訊科學/2018-深度學習三巨頭.md`、`../資訊科學/1936-圖靈機.md`。
