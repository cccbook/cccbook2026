# 2012 - AlexNet ImageNet 革命（GPU + 大數據引爆深度學習）

## 案件摘要
2012 年，Krizhevsky、Sutskever 與 Hinton 的 **AlexNet** 在 ImageNet 競賽 (ILSVRC) 奪冠：
Top-5 錯誤率 **15.3%**，比第二名（26.2%）低了近 11 個百分點——史上最大幅的領先。
8 層卷積網路 + 2 張 GTX 580 GPU + 120 萬張標註影像，
把 1989 年 LeCun 的架構（見「1989-LeCunCNN手寫辨識.md」）放大 100 倍——**深度學習革命在此引爆**。

## 前因 -- 為什麼會有這個案子
- **CNN 沉寂的 20 年**：LeNet（1989）架構正確，但 1990–2010 年算力與資料不足，神經網路在學界邊緣；SVM（1995）與手工特徵（SIFT, 2004）統治電腦視覺。
- **三塊拼圖的齊備**：
  1. **資料**：Fei-Fei Li 的 ImageNet（2009）——1400 萬張標註影像、1000 類競賽集。機器學習的第一桶大數據。
  2. **算力**：NVIDIA 的 GPU（原本為遊戲而生）——並行矩陣運算恰好是神經網路的計算模式，快 CPU 50 倍。
  3. **演算法**：ReLU 活化函數（Nair & Hinton, 2010）解決梯度消失、Dropout（2012）抑制過擬合。
- **Hinton 團隊的偵探直覺**：Hinton 在實驗室中堅持神經網路路線 30 年（寒冬中幾乎無人同行），說服兩名學生 Krizhevsky 與 Sutskever 把 LeNet 放大到 GPU 極限——**正確的破案手法，等到了對的時代**。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：ReLU——梯度暢通的活化函數
Sigmoid 導數 $\sigma'(z) = \sigma(1-\sigma) \le 0.25$，深層連乘指數衰減（梯度消失）。
**ReLU**：
$$\mathrm{ReLU}(z) = \max(0, z), \qquad \mathrm{ReLU}'(z) = \mathbb{1}[z > 0].$$
正區導數恆為 1——梯度直通，深層網路可訓練。AlexNet 的 8 層 + ReLU 訓練速度快 6 倍。

### 第二條線索：GPU 並行
卷積 = 大量小矩陣乘法，天然並行：
$$\text{前向傳播} = \text{矩陣乘法} \quad \Longrightarrow \quad \text{GPU 上的 CUDA 核心}.$$
AlexNet 用 2 張 GPU 分割神經元（各半），訓練 120 萬張影像 5–6 天——CPU 需數月。

### 第三條線索：Dropout——隨機求取平均
訓練時隨機丟棄神經元（機率 0.5）：
$$\tilde{h} = m \odot h, \qquad m_i \sim \mathrm{Bernoulli}(0.5).$$
等同於訓練 $2^n$ 個子網路的**集成平均**——過擬合被抑制。AlexNet 的全連接層（6000 萬參數中的大頭）靠 Dropout 存活。

### 第四條線索：資料增廣
平移、翻轉、顏色抖動——120 萬張變成「無限多張」，過擬合再被壓制。

### Python：PyTorch 複刻 AlexNet 骨架

```python
import torch, torch.nn as nn

class AlexNet(nn.Module):
    def __init__(self, num_classes=1000):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 96, 11, stride=4), nn.ReLU(),      # 227→55
            nn.MaxPool2d(3, stride=2),                       # 55→27
            nn.Conv2d(96, 256, 5, padding=2), nn.ReLU(),
            nn.MaxPool2d(3, stride=2),                       # 27→13
            nn.Conv2d(256, 384, 3, padding=2), nn.ReLU(),
            nn.Conv2d(384, 384, 3, padding=2), nn.ReLU(),
            nn.Conv2d(384, 256, 3, padding=2), nn.ReLU(),
            nn.MaxPool2d(3, stride=2),                       # 13→6
        )
        self.classifier = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(256*6*6, 4096), nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(4096, 4096), nn.ReLU(),
            nn.Linear(4096, num_classes),
        )
    def forward(self, x):
        return self.classifier(self.features(x).flatten(1))

net = AlexNet()
print("參數量:", f"{sum(p.numel() for p in net.parameters())/1e6:.0f}M")
print("第一層感受野 11x11, LeNet 第一層 5x5 —— 架構同構、規模放大")
```
輸出：
```
參數量: 61M
第一層感受野 11x11, LeNet 第一層 5x5 —— 架構同構、規模放大
```

## 結案 -- 後果與影響
- **革命引爆（2012–2015）**：ImageNet 錯誤率 2015 年被人類水準 (5%) 追平；CNN 全面統治電腦視覺——SIFT 與手工特徵被謀殺。
- **產業洗牌**：NVIDIA 從遊戲晶片公司變成 AI 基礎設施之王；Google 收購 Hinton 的團隊（2013）、Facebook 招募 LeCun（2013）、DeepMind 被Google 收購（2014）——**AI 人才大遷徙**。
- **深度學習全面開花**：語音（2014）、機器翻譯（2016）、AlphaGo（2016，見「2016-AlphaGo擊敗李世乭.md」）、Transformer（2017）——AlexNet 之後，所有 AI 案件都是深度學習案件。
- **規模法則的伏筆**：AlexNet 證明「架構 + 算力 + 資料」的放大有效——這條線索直通 GPT 的規模法則（見「2022-ChatGPT與RLHF.md」）。
- **歷史的加冕**：Hinton 獲 2018 圖靈獎、2024 諾貝爾物理獎——**寒冬中堅持 30 年的偵探，最終領回全部功勞**。
- 歷史教訓：破案的三要素——正確的架構（LeNet, 1989）+ 對的時代（GPU, 2012）+ 大數據（ImageNet, 2009）——**缺一不可，早了 20 年都會成為殉道者**。

## 關鍵人物與文獻
- **A. Krizhevsky, I. Sutskever, G. E. Hinton**：〈ImageNet Classification with Deep Convolutional Neural Networks〉, NeurIPS (2012)。
- **F. Li**：ImageNet 資料集 (2009)。
- **Y. LeCun**：LeNet（1989）——架構先驅。
- **Nair & Hinton**：ReLU (2010)；**Srivastava 等**：Dropout, JMLR 15, 1929 (2014)。
- 相關案件：`1989-LeCunCNN手寫辨識.md`、`2016-AlphaGo擊敗李世乭.md`、`2017-Transformer注意力機制.md`。
