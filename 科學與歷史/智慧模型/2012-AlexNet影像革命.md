# 2012 - AlexNet 影像革命

## 案件摘要
2012 年 9 月，多倫多大學的 Alex Krizhevsky、Ilya Sutskever 與 Geoffrey Hinton 以一個 8 層卷積神經網路 **AlexNet** 在 ImageNet 競賽（ILSVRC）中以 **15.3%** 的 top-5 錯誤率奪冠，比第二名（26.2%）低了近 11 個百分點——這不是改良，是屠殺。核心公式只有一行：**ReLU 激活函數**

$$
f(x) = \max(0, x)
$$

加上 Dropout、GPU 平行訓練與一百二十萬張標注影像，神經網路從 1969 年明斯基宣判的死刑中徹底復活（1969-明斯基感知機寒冬.md），開啟了**深度學習大爆炸**。

## 前因 -- 為什麼會有這個案子
- **1986-反向傳播復興.md**（1986-反向傳播演算法.md）讓多層網路可訓練，但深網在實務上總是訓不動：梯度消失、過擬合、算力不足。
- **1989-楊立昆卷積網路.md**（1989-LeCunCNN手寫辨識.md）證明卷積 + 權重共享在手寫數字上可行，但當時的網路只有幾層、資料只有幾萬張，學界認為 CNN 只適合小任務。
- **2006-欣頓深度信念網路.md** 用逐層預訓練繞過梯度消失，點燃了「深度學習」的名詞，但仍是無監督預訓練 + 有監督微調的迂迴戰術。
- **2009-ImageNet資料集.md**：李飛飛以 WordNet 結構建成 1400 萬張、2 萬類的影像資料集，ILSVRC 競賽提供 120 萬張訓練影像——資料的規模首次配得上演算法的野心。
- **GPU 的成熟**：NVIDIA CUDA（2007）讓數千核心的平行矩陣運算觸手可及；Krizhevsky 在宿舍裡用兩張 GTX 580 寫出了史上第一個大規模 GPU CNN。
- **SVM 的統治**：2010–2011 年的 ILSVRC 冠軍都是特徵工程 + SVM（錯誤率 ~28%），學界主流相信「特徵比模型重要」——AlexNet 直接推翻了這條教條。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：ReLU——殺死梯度消失
傳統網路用飽和的 tanh 激活 $g(x) = \tanh(x)$，其導數 $1-\tanh^2(x)$ 在 $|x|$ 大時趨近 0，反向傳播多層連乘後梯度消失。AlexNet 改用不飽和的線性整流：

$$
f(x) = \max(0, x), \qquad f'(x) = \mathbb{1}[x > 0]
$$

正區間導數恆為 1，深網的梯度不再枯竭。論文實測：在 CIFAR-10 上達到 25% 訓練錯誤率，tanh 需要六倍時間。這一行公式便宜、簡單，卻是整樁案件最重要的兇器。

### 第二條線索：Dropout——對抗過擬合
6 千萬參數對 120 萬張影像，過擬合是必然。AlexNet 的答案是訓練時隨機捨棄一半隱藏神經元：

$$
\tilde{h} = m \odot h, \quad m_i \sim \mathrm{Bernoulli}(0.5)
$$

等效於訓練 $2^{6000}$ 個子網路的集成（ensemble），測試時把權重乘 0.5。Hinton 後來形容靈感來自銀行的防詐騙機制：「銀行櫃員輪班——因為員工之間的勾結需要隨機性來破壞。」

### 第三條線索：GPU 平行訓練與架構
AlexNet 架構與 LeNet 同源，但規模放大數十倍：

| 層 | LeNet (1989/1998) | AlexNet (2012) |
|---|---|---|
| 卷積層數 | 2 | 5 |
| 全連接層 | 2 | 3 |
| 單層最大神經元 | ~100 | 4096 |
| 總參數量 | ~6 萬 | 6 千萬 |
| 訓練硬體 | CPU（數日） | 2× GTX 580 GPU（約 6 天） |
| 輸入影像 | 32×32 灰階手寫 | 224×224 彩色照片 |

雙 GPU 拆分：一半卷積核放在一張卡上，兩卡僅在特定層互通——用一台消費級工作站跑出了當年超級電腦級的訓練。

### 第四條線索：賽場上的屠殺
ILSVRC-2012 top-5 錯誤率：

| 名次 | 團隊 | 方法 | 錯誤率 |
|---|---|---|---|
| 1 | SuperVision（Hinton 組） | CNN + ReLU + Dropout + GPU | **15.3%** |
| 2 | NEC-UIUC | SIFT 特徵 + SVM | 26.2% |
| 3 | OXFORD VGG | 特徵 + SVM | 26.6% |

評審 Jürgen Schmidhuber 事後質疑 ConvNet 的優先權（LeNet 早已存在），但承認：**是 AlexNet 讓全世界相信了神經網路**。資料（ImageNet）＋演算法（CNN）＋算力（GPU）三股線索在此交會，缺一不可。

### 第五條線索：數據增廣與其他細節兇器
AlexNet 的勝利還靠兩個小兇器：
- **數據增廣（data augmentation）**：對訓練影像做隨機平移、水平翻轉、改變 RGB 通道強度（以 PCA 對 RGB 空間取主成分再加高斯擾動）：

$$
[\mathbf{p}_1, \mathbf{p}_2, \mathbf{p}_3][\alpha_1 \lambda_1, \alpha_2 \lambda_2, \alpha_3 \lambda_3]^{\top}, \quad \alpha_i \sim \mathcal{N}(0, 0.1)
$$

等效於把 120 萬張影像放大數十倍，抑制過擬合。
- **局部響應歸一化（LRN）**：在相鄰卷積核之間做側向抑制 $b = a / (k + \alpha \sum a^2)^\beta$，模擬生物神經元的側抑制——此組件後來被 BatchNorm 取代，但在 2012 年幫了一臂。
- **重疊池化（overlapping pooling）**：池化窗口步距小於窗口大小，保留更多空間資訊，錯誤率下降約 0.4%。

## 結案 -- 後果與影響
- **深度學習大爆炸**：2013 年 ILSVRC 前八名全是 CNN；2014 年 VGGNet 與 GoogLeNet；2015-ResNet殘差網路.md 把錯誤率壓到 3.57%，超過人類（5.1%）。
- **學界變天**：特徵工程退場，「端到端學習」成為新教條；計算機視覺、語音（2011-Siri語音助理.md 中的 DNN 轉折）、NLP 依次被神經化。
- **人才遷徙**：Hinton 的學生 Ilya Sutskever 後來成為 OpenAI 首席科學家；AlexNet 三人組在 2012 年 12 月被 Google 以收購 Hinton 新創公司的方式聘走。
- **產業基礎建設**：GPU 運算從遊戲轉向 AI，NVIDIA 由此成為 AI 時代的軍火商；PyTorch/TensorFlow 的生態由此奠基。
- **伏筆**：CNN 證明了「資料＋算力＋可微模型」的威力；同樣的配方即將轉向序列——2013-word2vec詞向量.md 與 2014-Seq2Seq與注意力.md 將把影像革命的戰火燒向語言，最終在 2017-Transformer注意力機制.md 匯流成 GPT。

## 關鍵人物與文獻
- **Alex Krizhevsky**：CUDA 程式的作者，AlexNet 的工程實作核心。
- **Ilya Sutskever**：演算法設計合作者，後任 OpenAI 首席科學家。
- **Geoffrey Hinton**：指導教授，神經網路復興的精神領袖。
- **李飛飛**：ImageNet 創建者，資料線索的關鍵人物。
- Krizhevsky, Sutskever, Hinton, *ImageNet Classification with Deep Convolutional Neural Networks*, NeurIPS, 2012.
- Krizhevsky, *CUDA-Convnet: An Implementation of Convolutional Neural Networks*, 2011–2012.
- Deng et al., *ImageNet: A Large-Scale Hierarchical Image Database*, CVPR, 2009.
- 相關案件：1989-楊立昆卷積網路.md、1969-明斯基感知機寒冬.md、2006-欣頓深度信念網路.md、2009-ImageNet資料集.md、2013-word2vec詞向量.md、2015-ResNet殘差網路.md

## 補充 -- 程式實作（python + pytorch + sklearn）

本案三兇器（ReLU＋Dropout＋增廣）組成的迷你 AlexNet，見 `_code/2012-AlexNet.py`（已實測可跑，CPU 約 2 分鐘；MNIST 沿用 `_code/data`）：

```python
# 2012 - AlexNet 影像革命 (Krizhevsky-Sutskever-Hinton)
# 公式: ReLU f(x)=max(0,x); Dropout h̃=m⊙h, m~Bernoulli(0.5)
import time
from pathlib import Path

import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as T
from sklearn.linear_model import LogisticRegression


class MiniAlexNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 48, 5, padding=2), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(48, 128, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(128, 192, 3, padding=1), nn.ReLU(),
            nn.Conv2d(192, 192, 3, padding=1), nn.ReLU(),
            nn.Conv2d(192, 128, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.Dropout(0.5), nn.Linear(128 * 4 * 4, 512), nn.ReLU(),
            nn.Dropout(0.5), nn.Linear(512, 512), nn.ReLU(),
            nn.Linear(512, 10))

    def forward(self, x):
        return self.classifier(self.features(x).flatten(1))


def main():
    torch.manual_seed(0)
    root = Path(__file__).parent / "data"
    tf = T.Compose([T.Resize(32), T.ToTensor()])
    train = torchvision.datasets.MNIST(str(root), train=True, download=True, transform=tf)
    test = torchvision.datasets.MNIST(str(root), train=False, download=True, transform=tf)
    tr = torch.utils.data.Subset(train, range(12000))
    te = torch.utils.data.Subset(test, range(3000))
    tr_l = torch.utils.data.DataLoader(tr, batch_size=128, shuffle=True)
    te_l = torch.utils.data.DataLoader(te, batch_size=1024)

    # 基線: 線性分類器 (只看3000張會過擬合 -- 正是小資料+大模型的困境)
    Xb = train.data[:3000].float().div(255).reshape(3000, -1).numpy()
    yb = train.targets[:3000].numpy()
    Xt = test.data[:3000].float().div(255).reshape(3000, -1).numpy()
    yt = test.targets[:3000].numpy()
    clf = LogisticRegression(max_iter=300).fit(Xb, yb)
    print(f"線性基線: 訓練準確率={clf.score(Xb, yb):.3f}, 測試準確率={clf.score(Xt, yt):.3f} "
          f"(過擬合 -- 呼應書中_dropout_要解決的問題)")

    net = MiniAlexNet()
    print(f"MiniAlexNet 參數: {sum(p.numel() for p in net.parameters())} "
          f"(原版6千萬, 此處縮小以便CPU演示; 三兇器 ReLU+Dropout+增廣全在)")
    opt = torch.optim.Adam(net.parameters(), lr=2e-3)
    aug = T.RandomAffine(degrees=0, translate=(0.08, 0.08))  # 數字不能水平翻轉
    t0 = time.time()
    for ep in range(4):
        net.train()
        for x, y in tr_l:
            opt.zero_grad()
            loss = nn.CrossEntropyLoss()(net(aug(x)), y)
            loss.backward()
            opt.step()
        net.eval()
        with torch.no_grad():
            acc = sum((net(x).argmax(1) == y).sum().item() for x, y in te_l) / len(te)
        print(f"  epoch {ep + 1}: 測試準確率={acc:.4f} (錯誤率={1 - acc:.2%}) [{time.time() - t0:.0f}s]")
    print("結論: ReLU(導數恆1)+Dropout(子網集成)+增廣 -- 論文 top-5 15.3% vs 次名 26.2%")


if __name__ == "__main__":
    main()
```

執行結果（`python3 _code/2012-AlexNet.py`，torch 2.12.0，CPU）：

```
線性基線: 訓練準確率=0.994, 測試準確率=0.849 (過擬合 -- 呼應書中_dropout_要解決的問題)
MiniAlexNet 參數: 2148202 (原版6千萬, 此處縮小以便CPU演示; 三兇器 ReLU+Dropout+增廣全在)
  epoch 1: 測試準確率=0.3663 (錯誤率=63.37%) [25s]
  epoch 2: 測試準確率=0.8613 (錯誤率=13.87%) [52s]
  epoch 3: 測試準確率=0.9353 (錯誤率=6.47%) [87s]
  epoch 4: 測試準確率=0.9480 (錯誤率=5.20%) [112s]
結論: ReLU(導數恆1)+Dropout(子網集成)+增廣 -- 論文 top-5 15.3% vs 次名 26.2%
```

程式解說：基線先示範困境——邏輯回歸在 3000 張上訓練 99.4%、測試只剩 84.9%，正是 6 千萬參數對 120 萬影像的過擬合縮影，Dropout 為此而生。MiniAlexNet 的曲線是三兇器的活體廣告：epoch 1 還在暖機（36%），ReLU 的恆定梯度讓深堆疊訓得動，epoch 4 即達 94.8%、超車線性基線 10 個點。實測附帶兩課：(1) 增廣必須尊重資料——數字不能水平翻轉（7 會變形），程式用平移增廣；(2) `torch.linalg.lstsq` 在 MNIST 這類秩虧矩陣上會回傳零解，基線改用 sklearn 邏輯回歸——工具有適用邊界，偵探要驗屍（`W.norm()==0`）而非盲信。
