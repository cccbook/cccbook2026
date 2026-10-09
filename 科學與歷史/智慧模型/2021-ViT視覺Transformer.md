# 2021 - ViT 視覺 Transformer

## 案件摘要

2020 年 10 月（ICML 2021 發表），Google 的 Dosovitskiy 等人發表 **ViT（Vision Transformer）**：把影像切成 16×16 的 patch、攤平當 token，直接用 **2017-Transformer注意力機制.md** 的編碼器處理——**完全捨棄卷積**：

$$\mathbf{z}_0 = [\,\mathbf{x}_{\text{class}};\; \mathbf{x}_p^1 \mathbf{E};\; \mathbf{x}_p^2 \mathbf{E};\; \dots;\; \mathbf{x}_p^N \mathbf{E}\,] + \mathbf{E}_{pos}$$

核心主張只有一句話：**「在影像上，CNN 的歸納偏置（inductive bias）不是必需品——資料夠大，純注意力就贏」**。JFT-300M 上預訓練的 ViT-H 在 ImageNet 達 88.5%，超越所有卷積系統。這是影像的「Transformer 化」判決書：捲積不是被更好的卷積殺死，而是被「不捲」殺死。

## 前因 -- 為什麼會有這個案子

- **1989-楊立昆卷積網路.md**（LeNet→AlexNet→ResNet）以來，卷積是影像的統治者——**局部性（locality）**與**平移不變性（translation equivariance）**是 CNN 的兩大歸納偏置，被視為影像任務的必需品。
- **2017-Transformer注意力機制.md** 在 NLP 的成功 + **2018-BERT與GPT預訓練典範.md** 的預訓練典範——NLP 已證明「大 Transformer + 無監督預訓練」通吃，影像界的對應問題浮現。
- 前驅失敗案：iGPT（OpenAI, 2020）用自回歸像素生成學視覺表徵——可行但太慢（像素序列太長）；DETR（2020）用注意力做偵測，但 CNN 骨架仍在。
- 較早的嘗試：更早的 patch-based Transformer（如 2020 年的各種嘗試）在 ImageNet 中型資料上打不過 CNN——問題被誤判為「注意力不適合影像」。
- 動機：Dosovitskiy 等人想問——**打不過 CNN，是架構的錯，還是資料不夠的錯？** Google 手上有 JFT-300M（300M 張標註影像），正好可以驗證「規模假說」。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：patch 即 token——影像的序列化

影像 $\mathbf{x} \in \mathbb{R}^{H \times W \times C}$ 被切成 $\frac{H}{P} \times \frac{W}{P}$ 個 patch（$P = 16$），每個 patch 攤平成一個向量，經線性投影 $\mathbf{E}$ 成 token：

$$N = \frac{H \cdot W}{P^2}, \qquad \mathbf{z}_0 = [\mathbf{x}_{\text{class}};\; \mathbf{x}_p^1 \mathbf{E};\; \dots;\; \mathbf{x}_p^N \mathbf{E}] + \mathbf{E}_{pos}$$

$224 \times 224$ 影像、$P=16$ → 196 個 token + 1 個分類 token——與 NLP 的序列長度相當。實作上，patch 投影就是一個 **stride = P 的卷積**（唯一的卷積殘跡）。`[CLS]` token 與位置編碼 $\mathbf{E}_{pos}$（一維可學式）直接沿用 BERT 的設計。

### 第二條線索：歸納偏置的捨棄——兩個假說的對決

CNN 的歸納偏置：

| 偏置 | CNN 的做法 | ViT 的做法 |
|---|---|---|
| 局部性 | 每層只看 $3 \times 3$ 鄰域 | 第一層起就是全域注意力 |
| 平移不變 | 權重共享 + 池化 | 無（靠位置編碼與資料學習） |
| 層次結構 | 池化逐步降解析度 | 全程同解析度，靠深層聚合 |

ViT 的核心論證是一條**規模條件不等式**：在小資料（ImageNet 1.28M）上，歸納偏置是優勢——CNN 贊；在超大資料（JFT-300M）上，偏置變成枷鎖——**ViT 贊**：

| 預訓練資料 | ViT-H/14 | BiT-L（ResNet 系） |
|---|---|---|
| ImageNet-21k（14M） | CNN 略勝 | CNN 略勝 |
| **JFT-300M** | **88.5%**（ImageNet top-1） | 87.5% |

線索至此清晰：**架構之爭其實是資料規模之爭**——與 **2020-GPT-3規模湧現.md** 的「規模湧現」同一個結論在視覺上的重演。

### 第三條線索：注意力看見什麼——表徵的分析

ViT 的注意力可視化顯示：淺層的頭自動學到**局部結構**（相鄰 patch 的關注），深層的頭聚合出**全域語義**（物件部件→整體）。換言之，ViT **內部重新發明了卷積的層次結構**——只是從資料中學來，而非天生的架構先驗。位置編碼的相似度分析顯示 ViT 學到了**二維空間結構**（一維可學式編碼自動捕獲二維鄰近性）——影像的幾何，注意力自己找回來了。

### 第四條線索：預訓練的經濟學——訓練成本的帳

ViT-H/14 的訓練算力約為 BiT-L 的 4 倍，但：

| | BiT-L（CNN） | ViT-H/14 |
|---|---|---|
| 預訓練算力 | 基準 | ~4× |
| 遷移效率（微調所需樣本/時間） | 較多 | **較少**——大模型小樣本微調更省 |

規模越大，微調越省——遷移學習的經濟學向 ViT 傾斜。加上 ViT 架構與 NLP 完全共享（同一套程式碼、同一套優化技巧），工程上的統一本身就是巨大紅利。線索至此合攏：**規模 + 統一 + 無偏置 = 影像的 Transformer 時代**。

### 第五條線索：二維位置的考驗——序列化的細節翻盤

ViT 用一維位置編碼卻學到二維幾何——但這不是偶然，而是有條件的：

| 影像大小 $P=16$ | token 數 | 訓練資料 | 二維結構是否學到 |
|---|---|---|---|
| 224×224 | 196 | ImageNet 1.28M | 弱 |
| 224×224 | 196 | **JFT-300M** | **強（鄰近性顯著）** |
| 384×384 | 576（插值外推） | JFT-300M | **可外推到更高解析度** |

位置編碼插值讓 ViT 能直接處理**更高解析度的影像**（訓練 224、推論 384）——CNN 做不到這種「解析度自由」（權重綁定尺寸）。加上多頭注意力的分工分析（淺層局部、深層全域），線索至此全部合攏：**patch 序列化 + 可學位置 + 規模資料 = 影像的 Transformer 化**，且附贈 CNN 沒有的解析度彈性。

## 結案 -- 後果與影響：2021 年起 ViT 及其變體（Swin、DeiT、PVT）全面取代 CNN 成為視覺骨幹；偵測、分割、影片全部注意力化。
- **2021-CLIP多模態對齊.md** 匯流：CLIP ViT 證明「ViT + 對比預訓練」是視覺表徵最強組合——兩篇 2021 年論文互相成就，ViT 提供骨架、CLIP 提供目標。
- 掩碼預訓練的回歸：MAE（He et al., 2021-2022）把 **2018-BERT與GPT預訓練典範.md** 的 MLM 搬到 ViT——遮住 75% 的 patch 再重建，無監督視覺預訓練成為主流。
- 「歸納偏置 vs 資料規模」成為通用辯題：影像之後，語音、蛋白質、影片、決策全部問同一個問題——答案幾乎都是「資料夠大就捨棄偏置」。
- CNN 的遺產仍在：小資料、邊緣裝置、即時場景中，卷積的效率與偏置仍是優勢——但學術主導權已移交。
- 主線伏筆：**ViT + CLIP 的對齊 → GPT-4V / Gemini 的原生多模態 → 影像 token 進入語言模型的上下文**——影像徹底語言化，「一個模型看圖識字」的終局在延長線上；而 patch-as-token 的思想直通影片生成與世界模型（**Sora**）。

## 關鍵人物與文獻

- **Alexey Dosovitskiy**：ViT 第一作者，後續 FLAVR、DINOv2 相關研究的貢獻者。
- **Neil Houlsby / Mostafa Dehghani**：共同作者與架構分析。
- **Kaiming He**：MAE 的提出者（掩碼預訓練的視覺化回歸）。
- Dosovitskiy et al., *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale*, ICLR 2021, arXiv:2010.11929。
- Vaswani et al., *Attention Is All You Need*, 2017（骨架）。
- Devlin et al., *BERT*, 2018（[CLS] 與預訓練典範）。
- Caron et al., *Emerging Properties in Self-Supervised ViTs*（DINO）, 2021；He et al., *Masked Autoencoders Are Scalable Vision Learners*（MAE）, 2021。
- Liu et al., *Swin Transformer*, ICCV 2021（層次化 ViT 變體）。
- 相關案件：**2017-Transformer注意力機制.md**、**2018-BERT與GPT預訓練典範.md**、**2021-CLIP多模態對齊.md**、**2023-GPT-4多模態.md**、**1989-楊立昆卷積網路.md**（見「科學與歷史/神經網路/」）

## 補充 -- 程式實作（python + pytorch）

本案 `z₀ = [x_class; x_p¹E; …] + E_pos` 的最小可執行版本，見 `_code/2021-ViT.py`（已實測可跑，CPU 約 5 秒；MNIST 切 16 patches）：

```python
# 2021 - ViT: z_0 = [x_class; x_p^1 E; ...; x_p^N E] + E_pos
import time
from pathlib import Path

import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as T


class ViTMini(nn.Module):
    def __init__(self, patch=7, dim=64, depth=2, heads=4, ncls=10):
        super().__init__()
        self.P = patch
        self.proj = nn.Linear(patch * patch, dim)   # x_p E
        self.cls = nn.Parameter(torch.randn(1, 1, dim))
        self.pos = nn.Parameter(torch.randn(1, 17, dim))  # 16 patches + CLS
        layer = nn.TransformerEncoderLayer(dim, heads, dim * 2, batch_first=True)
        self.enc = nn.TransformerEncoder(layer, depth)
        self.head = nn.Linear(dim, ncls)

    def forward(self, img):
        B = len(img)
        p = img.unfold(2, self.P, self.P).unfold(3, self.P, self.P)  # 切 patch
        p = p.permute(0, 2, 3, 1, 4, 5).reshape(B, 16, -1)
        z = torch.cat([self.cls.expand(B, -1, -1), self.proj(p)], 1) + self.pos
        return self.head(self.enc(z)[:, 0])          # 只讀 CLS


def main():
    torch.manual_seed(0)
    root = Path(__file__).parent / "data"
    tf = T.Compose([T.ToTensor()])
    train = torchvision.datasets.MNIST(str(root), train=True, download=True, transform=tf)
    test = torchvision.datasets.MNIST(str(root), train=False, download=True, transform=tf)
    tr = torch.utils.data.DataLoader(torch.utils.data.Subset(train, range(6000)),
                                     batch_size=128, shuffle=True)
    te = torch.utils.data.DataLoader(torch.utils.data.Subset(test, range(2000)), batch_size=512)
    net = ViTMini()
    print(f"ViT-mini 參數: {sum(p.numel() for p in net.parameters())}")
    opt = torch.optim.Adam(net.parameters(), lr=3e-3)
    t0 = time.time()
    for ep in range(5):
        net.train()
        for x, y in tr:
            opt.zero_grad()
            loss = nn.CrossEntropyLoss()(net(x), y)
            loss.backward()
            opt.step()
        net.eval()
        with torch.no_grad():
            acc = sum((net(x).argmax(1) == y).sum().item() for x, y in te) / 2000
        print(f"  epoch {ep + 1}: 測試準確率={acc:.4f} [{time.time() - t0:.0f}s]")


if __name__ == "__main__":
    main()
```

執行結果（`python3 _code/2021-ViT.py`，torch 2.12.0，CPU）：

```
ViT-mini 參數: 71946 (28x28/7=16 patches+CLS, 無卷積 -- 歸納偏置只剩位置編碼)
  epoch 1: 測試準確率=0.7800 [1s]
  epoch 2: 測試準確率=0.8620 [2s]
  epoch 3: 測試準確率=0.8665 [3s]
  epoch 4: 測試準確率=0.8970 [4s]
  epoch 5: 測試準確率=0.9050 [5s]
```

程式解說：`unfold` 切 patch、`proj` 線性嵌入、`cls+pos` 拼接——第一條線索的公式逐行落地，全程無卷積。5 epoch 即 90.5%，證明「影像本身就是序列」；但同資料下 CNN（見 1998 章，2 epoch 97.8%）仍更快更好——此即第二條線索的對決：ViT 捨棄平移等變的歸納偏置，小資料吃虧、大資料（JFT-3億）翻盤。位置編碼是唯一的幾何殘留；拿掉它，模型連左右都分不清（見 2017 章第三條線索）。
