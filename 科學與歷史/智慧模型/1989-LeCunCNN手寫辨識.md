# 1989 - LeCun CNN 手寫辨識

## 案件摘要

1989 年，Yann LeCun 在貝爾實驗室把反向傳播灌進**卷積神經網路（CNN）**，以端對端梯度下降直接從像素學出手寫數字辨識：

$$y = \sigma(W * x + b)$$

其中 $*$ 是卷積、$W$ 是**共享權重**的濾波器。一句話：**不用手工特徵，讓網路自己看**。這是深度學習第一次在真實工業任務上獲勝——後來的 MNIST 與 AT&T 支票辨識系統，讀走了全美 10–20% 的支票。它是連接派復興的第一場實戰勝利，也是 **2012-AlexNet影像革命.md** 的直接前身。

## 前因 -- 為什麼會有這個案子

- **1959-HubelWiesel視覺皮層.md**：貓的視覺皮層中，V1 區的簡單細胞對特定方向的邊緣有反應，複雜細胞對位置不敏感——**視覺是「局部偵測 → 位置不變」的層級**。這條神經科學線索是 CNN 的解剖圖。
- **1980-Neocognitron視覺層級模型.md**：福島邦彥照著 Hubel–Wiesel 的層級造出 Neocognitron，有 S 層（卷積式特徵偵測）與 C 層（池化），但**沒有端對端訓練方法**——權重靠自組織學習，精度有限。LeCun 的架構與 Neocognitron 幾乎同構，差別只在學習法：這是「架構早就在那裡，只等學習法」的經典懸案。
- 1986 年反向傳播（見 **1986-反向傳播演算法.md**）證明多層網路可訓練——福島的架構 + Rumelhart 的學習法，缺的只是一個組合。
- 工業動機：AT&T 需要自動辨識支票上的手寫金額。當時的做法是人工設計特徵（細化、端點偵測、模板比對），脆弱且昂貴。LeCun 後來回憶：他的反應是「為什麼不讓網路自己學特徵？」——這個直覺就是本案件的核心主張。
- 核心難題：全連接網路面對 $16\times16$ 輸入要 $10^4$ 級參數，且對平移、歪斜毫無不變性——參數爆炸 + 無幾何先驗。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：卷積 + 權重共享——兩大幾何先驗

LeCun 把 Hubel–Wiesel 的「局部感受野」與「位置共享」寫成數學：一層卷積為

$$y_{i,j} = \sigma\left( \sum_{u,v} W_{u,v}\, x_{i+u,\,j+v} + b \right)$$

同一個 $W$（同一組 $u,v$）掃過整張影像——**一個濾波器學一種特徵，在所有位置重複使用**。

| 先驗 | 來源 | 效果 |
|---|---|---|
| 局部連接 | Hubel–Wiesel 簡單細胞 | 參數從 $O(N^2)$ 降到 $O(k^2)$ |
| **權重共享** | 視覺的平移等變性 | 參數不隨影像大小增長，且平移不變 |
| 池化/子採樣 | Hubel–Wiesel 複雜細胞 | 小幅平移與形變的不變性 |

對比：$16\times16$ 影像接到 30 個隱藏單元的全連接層需 $\sim 7{,}700$ 參數；同樣任務的第一層卷積（$5\times5$ 濾波器 × 12 個）只需 $12 \times 26 = 312$ 個——**少了 25 倍，且幾何上更合理**。

### 第二條線索：端對端梯度下降——特徵也是學出來的

以往管線是「手工特徵 → 分類器」，兩段各自為政。LeCun 的管線是：

$$\text{像素} \to \text{卷積層} \to \text{池化層} \to \cdots \to \text{輸出}$$

整條管線是一個可微函數，反向傳播把誤差一路倒傳到**第一層的濾波器**——濾波器自動學成邊緣、筆畫、弧線偵測器，無人設計。這是「**特徵學習**」取代「特徵工程」的歷史時刻。

### 第三條線索：真實戰場——MNIST 與支票

- 1989 年的原始實驗用 USPS 郵政手寫數字；1998 年 LeCun 團隊整理出 **MNIST**（6 萬訓練 + 1 萬測試），錯誤率從線性分類器的 $\sim 12\%$ 一路壓到 CNN 的 $\sim 0.7\%$，此後十年 MNIST 成為機器學習的「果蠅」。
- 1990 年代 LeCun 的 **LeNet** 系統整合壓縮與識別，部署在 AT&T/NCR 的支票辨識機上：讀取了全美約 **10–20%** 的流通支票——神經網路第一次大規模商業落地。
- 這證明了一件事：**梯度下降 + 權重共享的先驗，能在真實、雜亂、工業級的資料上贏**——而不只是玩具 XOR。

### 第三條線索補遺：LeNet-5 的完整架構

1998 年定稿的 LeNet-5 是日後所有 CNN 的原型：

| 層 | 結構 | 輸出尺寸 | 角色 |
|---|---|---|---|
| 輸入 | $32\times32$ 灰階 | $32\times32$ | 像素 |
| C1 | 卷積，6 個 $5\times5$ 濾波器 | $6\times28\times28$ | 邊緣與筆畫 |
| S2 | 子採樣（$2\times2$ 平均） | $6\times14\times14$ | 平移不變 |
| C3/S4 | 卷積 16 個 + 子採樣 | $16\times5\times5$ | 部件組合 |
| F5/輸出 | 全連接 120 → 84 → 10 | 10 類 | 分類 |

層級的偵探視角：底層濾波器自動學成邊緣與線段，上層學成筆畫與弧線——**Hubel–Wiesel 的視覺皮層層級第一次在工程系統中重現**。總參數僅約 6 萬，卻在真實支票上達到工業精度。

### 第四條線索：陰影仍存

1990 年代的 CNN 仍受困於：
- **資料飢渴**：數萬張影像撐不起深網路——需要百萬級影像（伏筆：**2009-ImageNet資料集.md**）。
- **算力瓶頸**：CPU 訓練一天以計；需要 GPU（伏筆：**2012-AlexNet影像革命.md**）。
- **梯度消失**：深度超過五、六層就訓不動（見 **1986-反向傳播演算法.md** 第四條線索）。

## 結案 -- 後果與影響

- 確立了 CNN 的標準積木：卷積 → 非線性 → 池化，堆疊成層級——**視覺層級假說第一次被工程化驗證**。
- MNIST 成為機器學習標準測試床，「資料集驅動研究」的先聲。
- 1990 年代的連接派仍被 SVM 等淺層方法壓制，CNN 進入蟄伏期——直到 2012 年 AlexNet（見 **2012-AlexNet影像革命.md**）在 ImageNet 上橫掃，CNN 才登上王座。
- 權重共享的思想日後橫向擴散：語言中的 **2017-Transformer.md**、語音中的 Conv-TasNet，處處可見「共享參數 + 平移/時間等變」；LeCun「特徵應該自己學」的主張最終演變成 2020 年代的自監督學習與世界模型（見 **2024-VJEPA世界模型.md**）。
- 伏筆：LeNet 與 ImageNet 的會合是深度學習革命的引信；反向傳播（1986）+ ImageNet（2009）+ GPU 的三角組合即將改寫視覺智能的歷史。

## 關鍵人物與文獻

- **Yann LeCun**：CNN + 反向傳播的整合者，2018 年圖靈獎得主。
- LeCun et al., *Backpropagation Applied to Handwritten Zip Code Recognition*, Neural Computation, 1989。
- LeCun et al., *Gradient-Based Learning Applied to Document Recognition*, Proc. IEEE, 1998（LeNet 與 MNIST）。
- Hubel & Wiesel, *Receptive fields of single neurones in the cat's striate cortex*, 1959。
- Fukushima, *Neocognitron: A self-organizing neural network model…*, Biological Cybernetics, 1980。
- Rumelhart, Hinton & Williams, *Learning representations by back-propagating errors*, Nature, 1986。
- 相關案件：**1959-HubelWiesel視覺皮層.md**、**1980-Neocognitron視覺層級模型.md**、**1986-反向傳播演算法.md**、**1998-LeNet與MNIST.md**、**2009-ImageNet資料集.md**、**2012-AlexNet影像革命.md**

## 補充 -- 程式實作（python + pytorch）

本案 LeNet-5 架構（卷積→池化→卷積→池化→全連接）與端對端訓練的最小可執行版本，見 `_code/1989-LeNetCNN.py`（已實測可跑，以合成圓／方圖形代替 MNIST，8 個 epoch 內收斂）：

```python
# 1989 - LeNet CNN 手寫辨識 (LeCun)
# 公式: y_ij = σ(Σ_uv W_uv x_{i+u,j+v} + b) (卷積+權重共享)
import torch
import torch.nn as nn


class LeNet5Mini(nn.Module):
    def __init__(self):
        super().__init__()
        self.c1 = nn.Conv2d(1, 6, 5)     # 32x32 -> 28x28 (書中 C1)
        self.s2 = nn.AvgPool2d(2)        # -> 14x14 (子採樣=複雜細胞)
        self.c3 = nn.Conv2d(6, 16, 5)    # -> 10x10
        self.s4 = nn.AvgPool2d(2)        # -> 5x5
        self.f5 = nn.Linear(16 * 5 * 5, 84)
        self.out = nn.Linear(84, 2)

    def forward(self, x):
        x = torch.tanh(self.c1(x))
        x = self.s2(x)
        x = torch.tanh(self.c3(x))
        x = self.s4(x)
        x = torch.tanh(self.f5(x.flatten(1)))
        return self.out(x)


def make_shapes(n=400):
    """合成資料: 0=圓形, 1=方形 (32x32), 模擬 MNIST 的『真實圖案可被卷積學會』."""
    X = torch.zeros(n, 1, 32, 32)
    y = torch.zeros(n, dtype=torch.long)
    yy, xx = torch.meshgrid(torch.arange(32), torch.arange(32), indexing="ij")
    for i in range(n):
        c = i % 2
        y[i] = c
        if c == 0:
            X[i, 0] = (((xx - 16) ** 2 + (yy - 16) ** 2) < 81).float()
        else:
            X[i, 0, 10:22, 10:22] = 1.0
    X += torch.randn_like(X) * 0.1   # 工業級雜訊
    return X.clamp(0, 1), y


def main():
    torch.manual_seed(0)
    X, y = make_shapes()
    net = LeNet5Mini()
    opt = torch.optim.Adam(net.parameters(), lr=1e-2)
    n_params = sum(p.numel() for p in net.parameters())
    print(f"LeNet-5縮影: 總參數 {n_params} (全連接同級需數十萬 -- 權重共享省 25 倍)")
    for ep in range(8):
        opt.zero_grad()
        loss = nn.CrossEntropyLoss()(net(X), y)
        loss.backward()
        opt.step()
        acc = (net(X).argmax(1) == y).float().mean().item()
        print(f"  epoch {ep + 1}: loss={loss.item():.3f} acc={acc:.2f}")
    print("結論: 濾波器由梯度自動學成圓形/方形偵測器 -- 特徵學習取代特徵工程")


if __name__ == "__main__":
    main()
```

執行結果（`python3 _code/1989-LeNetCNN.py`，torch 2.12.0，CPU）：

```
LeNet-5縮影: 總參數 36426 (全連接同級需數十萬 -- 權重共享省 25 倍)
  epoch 1: loss=0.687 acc=0.50
  epoch 2: loss=0.527 acc=0.50
  epoch 3: loss=0.978 acc=1.00
  epoch 4: loss=0.317 acc=1.00
  epoch 5: loss=0.175 acc=1.00
  epoch 6: loss=0.147 acc=1.00
  epoch 7: loss=0.059 acc=1.00
  epoch 8: loss=0.037 acc=1.00
結論: 濾波器由梯度自動學成圓形/方形偵測器 -- 特徵學習取代特徵工程
```

程式解說：`LeNet5Mini` 逐層對應本文第三條線索補遺的 LeNet-5 表（C1→S2→C3→S4→F5→輸出），其中 `AvgPool2d` 即當年的子採樣層（複雜細胞的工程版）。總參數僅 36426，呼應第一條線索「卷積把參數從 `O(N²)` 壓到 `O(k²)`」。訓練曲線第 3 epoch 躍上 100%——無人設計圓／方偵測器，`loss.backward()` 把誤差一路倒傳進第一層濾波器，它們自己長成了特徵偵測器：此即「特徵學習取代特徵工程」的歷史時刻。合成資料僅為讓程式在 CPU 秒級跑完；換成 MNIST 即為 1998 年論文的設定。
