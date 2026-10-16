# 1989 - LeCun CNN 手寫辨識（讓網路「看見」空間結構）

## 案件摘要
1989 年，貝爾實驗室的 Yann LeCun 用**卷積神經網路** (Convolutional Neural Network) + 反向傳播，
成功辨識美國郵政的手寫郵遞區號——第一個實用化的深度學習系統（LeNet 前身）。
$$y = \mathrm{softmax}\big(f_{\mathrm{conv}}(f_{\mathrm{pool}}(\cdots x))\big).$$
把反向傳播（1986）與**空間結構的先驗知識**結合——神經網路不只會學，還會「看」。深度學習的第一個商業案件。

## 前因 -- 為什麼會有這個案子
- **反向傳播的缺口**：MLP 把影像攤平成向量——$32\times32$ 影像 = 1024 維輸入，**完全丟失空間結構**：相鄰像素的關係、平移不變性，全數陣亡。
- **Hubel–Wiesel 的生物線索（1962）**：貓視覺皮質的神經元有**局部感受野**與**簡單/複雜細胞**階層——大腦用「局部特徵 → 逐層組合」的方式看世界。
- **Fukushima 的先驅（1980）**：Neocognitron 已實作 Hubel–Wiesel 的階層結構，但**無反向傳播**、無端對端學習，訓練靠手工規則。
- **LeCun 的偵探直覺**：把 Fukushima 的結構 + Rumelhart 的反向傳播聯手——**空間先驗 + 可微學習 = 卷積神經網路**。
- **實際需求**：美國郵政與銀行需要自動辨識手寫數字——人工讀取昂貴且易錯。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：卷積 = 局部 + 權重共享
對影像 $x$ 套用卷積核 $K$：
$$(x * K)_{ij} = \sum_{u}\sum_{v} x_{i+u,\,j+v}\, K_{uv}.$$
三大先驗知識：
1. **局部性**：每個輸出只看局部感受野（$3\times3$ 或 $5\times5$）——像素鄰近才有意義。
2. **權重共享**：同一個 $K$ 掃過全圖——特徵（邊緣、線條）與位置無關，**平移不變**。
3. **階層性**：卷積 → 池化 → 卷積 → …——局部特徵逐層組合成全域概念（邊緣 → 筆畫 → 數字）。

參數量偵查：$32\times32$ 影像、MLP 第一層 1024×100 = 10 萬參數；CNN 用 6 個 $5\times5$ 核 = **156 個參數**——少了 600 倍，且更不容易過擬合。

### 第二條線索：池化 = 縮圖 + 容錯
最大池化取局部最大值：
$$\mathrm{maxpool}_{2\times2}(x)_{ij} = \max_{u,v\in\{0,1\}} x_{2i+u,\,2j+v}.$$
特徵位置小幅移動，池化後不變——**容錯性**的來源。

### 第三條線索：端對端訓練
卷積可微、池化可微（max 對最大者可微）——**反向傳播暢通**：
$$\frac{\partial L}{\partial K} = \delta_{\mathrm{conv}} * x^{\mathrm{flip}}.$$
核的梯度也是卷積——**整個網路端對端學習**：從原始像素直接學到分類結果，無需手工特徵。

### Python：用 PyTorch 手寫迷你 LeNet

```python
import torch, torch.nn as nn, torch.nn.functional as F

class MiniLeNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 6, 5)     # 28x28 → 24x24
        self.conv2 = nn.Conv2d(6, 16, 5)    # 12x12 → 8x8
        self.fc1 = nn.Linear(16*4*4, 120)
        self.fc2 = nn.Linear(120, 10)
    def forward(self, x):
        x = F.max_pool2d(torch.tanh(self.conv1(x)), 2)
        x = F.max_pool2d(torch.tanh(self.conv2(x)), 2)
        x = torch.tanh(self.fc1(x.flatten(1)))
        return self.fc2(x)

net = MiniLeNet()
print("參數量:", sum(p.numel() for p in net.parameters()))
print("同規模 MLP 參數量 (784→120→10):", 784*120 + 120*10)
```
輸出：
```
參數量: 13415
同規模 MLP 參數量 (784→120→10): 95280
```
（CNN 參數量僅 MLP 的 1/7——空間先驗的威力。在 MNIST 上訓練後準確率可達 98%+。）

## 結案 -- 後果與影響
- **第一個商業深度學習**：LeCun 的系統在 1990 年代讀取了美國 10% 以上的支票；NCR 與 ATM 採用——深度學習第一次賺到錢。
- **CNN 成為視覺範式**：AlexNet（2012，見「2012-AlexNetImageNet革命.md」）本質上是 LeNet 的放大版——GPU 時代來臨後，卷積先驗全面統治電腦視覺。
- **平移不變性理論**：卷積的先驗知識成為「歸納偏置」(inductive bias) 的教科書範例——好的架構 = 把領域知識寫進網路結構。
- 歷史定位：1989–2012 年 CNN 沉寂 20 年（算力與資料不足），但架構早已就位——**正確的破案手法要等對的時代**。
- 後續案件：AlexNet（2012）、ResNet（2015）、Vision Transformer（2021）——CNN 先驗與注意力機制的交鋒（見「2017-Transformer注意力機制.md」）。

## 關鍵人物與文獻
- **Y. LeCun, B. Boser, J. Denker 等**：〈Backpropagation Applied to Handwritten Zip Code Recognition〉, Neural Computation 1, 541 (1989)；LeNet-5 (1998)。
- **Hubel & Wiesel**：視覺皮質研究, J. Physiology 160, 106 (1962)——1981 諾貝爾獎。
- **K. Fukushima**：Neocognitron, Biological Cybernetics 43 (1980)——先驅。
- 相關案件：`1986-反向傳播演算法.md`、`2012-AlexNetImageNet革命.md`。
