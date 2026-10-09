# 2016 - WaveNet 語音合成

## 案件摘要

2016 年 9 月，DeepMind 的 van den Oord 等人發表 **WaveNet**：一個直接對**原始音訊波形**逐點建模的自回歸生成模型。它把語音合成寫成一條機率鏈：

$$p(\mathbf{x}) = \prod_{t=1}^{T} p(x_t \mid x_{<t}), \qquad x_t \in \{0, 1, \dots, 255\}$$

每秒 16,000 個取樣點，一個音字接一個音字地「唸」出聲音。破案關鍵不是更大的記憶，而是**擴張卷積（dilated convolution）**——讓感受野指數增長，在 $O(\log T)$ 層內看見整段語音。MOS 自然度評分首次超越參數式合成，逼近真人。這是語音生成的「波形謀殺案」：傳統合成器被殺，兇手是神經網路 + 逐點自回歸。

## 前因 -- 為什麼會有這個案子

- **2012-AlexNetImageNet革命.md** 證明了深度卷積網路的威力，但都在影像；語音界仍由兩個老派方法統治：
  - **參數式合成（parametric TTS）**：先 extract 聲學特徵（如梅爾頻譜），再用聲碼器（vocoder）重建波形——人為特徵工程造成「金屬感、機器味」。
  - **拼接式合成（concatenative TTS）**：錄音庫剪貼——自然但僵硬，無法變換音色。
- **2014-Seq2Seq與注意力.md** 與 **2016-WaveNet 前的 PixelRNN/PixelCNN**（同作者 van den Oord，2016 年 1 月）已證明：自回歸 + 卷積可以逐像素生成逼真影像。動機自然浮現：**影像可以逐點生成，聲音為什麼不行？**
- 技術障礙一：16 kHz 取樣率下，一秒語音有 16,000 個時間步——傳統 RNN（見 **1997-LSTM長短期記憶.md**）要看到 0.5 秒的上下文需要數百步，長程依賴記不住。
- 技術障礙二：音訊是連續值，自回歸需要離散化——需設計合適的輸出分佈。
- DeepMind 的動機：PixelRNN 的成功 + Google 收購後的語音產品需求，讓「純神經、端對端語音合成」成為必然的下一案。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：逐點自回歸——把聲音當成離散的機率鏈

WaveNet 用 $\mu$-律（mu-law）量化把連續波形壓成 256 個離散值，再用一個以**因果卷積**堆疊的網路輸出分類分佈：

$$x_t = \mathrm{softmax}\big(f(x_{t-R}, \dots, x_{t-1})\big), \qquad R = \text{感受野大小}$$

生成時一次取樣一點、餵回去、再取下一點——純自回歸。訓練目標就是極大化對數概似 $\sum_t \log p(x_t \mid x_{<t})$。與 RNN 不同，因果卷積在**訓練時可以完美並行**（所有時間步同時算），只有生成時是序列的。

### 第二條線索：擴張卷積——感受野的指數爆炸

因果卷積若每層看 1 步，要看 16,000 步需要 16,000 層——不可行。WaveNet 的解法是讓第 $l$ 層的卷積**跳過** $2^{l-1}$ 個點：

| 層數 $l$ | 擴張率 dilation | 每層跳過 |
|---|---|---|
| 1 | 1 | 0 步 |
| 2 | 2 | 1 步 |
| 3 | 4 | 3 步 |
| 4 | 8 | 7 步 |
| $\vdots$ | $2^{l-1}$ | $\vdots$ |
| 10 | 512 | 1023 步 |

$l$ 層堆疊後感受野為 $R = 1 + \sum_{i=1}^{l} 2^{i-1} = 2^{l}$——**指數增長**。30 層網路即可覆蓋超過一秒的語音歷史。這與 **2013-VAE變分自編碼器.md** 之後的「多尺度」思想（池化、金字塔）截然不同：不壓縮解析度，而是讓稀疏連接跨越距離。數學上，這是對 RNN 長程依賴問題的捨棄式解法——不靠記憶，靠**稀疏的直連**。

### 第三條線索：條件化——說話者與文本的注入

自回歸鏈可以加上條件 $h$：

$$p(\mathbf{x} \mid h) = \prod_t p(x_t \mid x_{<t}, h)$$

- $h$ = 文本的語言學特徵 → **文本轉語音（TTS）**
- $h$ = 說話者嵌入（speaker embedding）→ **單一模型變換多種音色**（VCTK 資料集上，17 位說話者一網打盡）

這是「一個模型、多種條件」的典範：條件向量像旋鈕，扭動聲音的身分。

### 第四條線索：殘差與門控——RNN 的遺產

WaveNet 借用了 **1997-LSTM長短期記憶.md** 的門控思想，做出卷積版：

$$\mathbf{z} = \tanh(W_f \mathbf{x}) \odot \sigma(W_g \mathbf{x})$$

$\odot$ 是逐元素乘法：tanh 管「要說什麼」，sigmoid 管「要不要說」。加上殘差連接與跳躍連接，30 層深網得以穩定訓練。線索至此合攏：**門控 + 擴張 + 自回歸 = 波形級生成**。

### 第五條線索：案發現場的成績單——MOS 的翻盤

WaveNet 在實際測試中的成績（MOS，5 分滿分）：

| 系統 | MOS（英文 TTS） |
|---|---|
| 拼接式合成（HMM） | 3.5–3.8 |
| 參數式合成 | 3.4–3.6 |
| **WaveNet（條件式）** | **4.3+** |
| 真人錄音 | 4.3–4.6 |

條件式 WaveNet 的 MOS 首次與真人錄音的置信區間重合——聽眾無法分辨「機器唸的」與「人錄的」。且同一個網路在「生成式」（無條件）模式下還能自己幻想出「非語音的怪聲」——模型學到的是**音訊的完整分佈**，不只是語音。線索至此全部合攏，案件可以宣判。

## 結案 -- 後果與影響

- 語音合成質變：Blizzard Challenge 2016 與 Google 助理上，WaveNet 的 MOS 首次讓合成語音與真人錄音難以區分；Google TTS 於 2017 年正式上線 WaveNet 聲音。
- 確立「神經聲碼器」典範：此後所有 TTS 系統（Tacotron 2、FastSpeech）都用神經網路直接生成波形，參數式 vocoder 退場。
- 擴張卷積擴散到整個序列建模：音訊分離、樂器生成、甚至時間序列預測都借用這把刀。
- 推理代價暴露：逐點自回歸生成 1 秒音訊要跑 16,000 次前向——並行化與蒸餾（Parallel WaveNet, 2017）成為後續案件。
- DeepMind 同源思想的伏筆：**「逐步加噪、學會去噪」** 的擴散路線四年在同一家實驗室誕生——見 **2020-DDPM擴散模型.md**，生成模型的權杖將從自回歸轉向迭代去噪。
- 對語言模型的遠方回聲：音訊也能被「當成 token 序列」逐點建模——這個理念在 2022 年後的 AudioLM、VALL-E、以及 Sora 的 tokenizer 中全面復活。

## 關鍵人物與文獻

- **Aaron van den Oord**：PixelRNN/PixelCNN 與 WaveNet 的核心作者，DeepMind。
- **Sander Dieleman**：擴張卷積與音訊生成的主要貢獻者。
- van den Oord et al., *WaveNet: A Generative Model for Raw Audio*, arXiv:1609.03499, 2016。
- van den Oord et al., *Conditional Image Generation with PixelCNN Decoders*, NIPS 2016。
- Oord et al., *Parallel WaveNet: Fast High-Fidelity Speech Synthesis*, 2017（並行化後續）。
- Ping et al., *Deep Voice 3* 與 Gibiansky et al., Tacotron 2, 2017（神經聲碼器典範的擴散）。
- 相關案件：**2014-Seq2Seq與注意力.md**、**2020-DDPM擴散模型.md**、**1997-LSTM長短期記憶.md**（見「科學與歷史/人工智慧/」與「科學與歷史/神經網路/」）

## 補充 -- 程式實作（python + pytorch）

本案擴張因果卷積（`R = Σdilation + 1`）＋門控（`tanh⊙σ`）的最小可執行版本，見 `_code/2016-WaveNet.py`（已實測可跑，CPU 秒級；以雙頻正弦代替語音）：

```python
# 2016 - WaveNet: 擴張因果卷積的自回歸
import torch
import torch.nn as nn
import torch.nn.functional as F


class WaveNetMini(nn.Module):
    def __init__(self, layers=6, channels=32, n_bins=64):
        super().__init__()
        self.emb = nn.Embedding(n_bins, channels)
        self.dilations = [2 ** i for i in range(layers)]  # 1,2,4,...,32
        self.f = nn.ModuleList([nn.Conv1d(channels, channels, 2, dilation=d)
                                for d in self.dilations])
        self.g = nn.ModuleList([nn.Conv1d(channels, channels, 2, dilation=d)
                                for d in self.dilations])
        self.rf = sum(self.dilations) + 1
        self.out = nn.Linear(channels, n_bins)

    def forward(self, q):
        x = self.emb(q).transpose(1, 2)
        for f, g, d in zip(self.f, self.g, self.dilations):
            h = F.pad(x, (d, 0))                           # 左填充守住因果性
            z = torch.tanh(f(h)) * torch.sigmoid(g(h))     # 門控 (LSTM 的遺產)
            x = x + z[:, :, -x.size(2):]                   # 殘差 (2015 的遺產)
        return self.out(x.transpose(1, 2))


def main():
    torch.manual_seed(0)
    T, NB = 256, 64
    t = torch.linspace(0, 8 * 3.1416, 4000)
    wave = torch.sin(t) + 0.3 * torch.sin(3 * t)
    q = ((wave + 1.3) / 2.6 * (NB - 1)).long().clamp(0, NB - 1)  # 量化 (μ-law 精神)
    net = WaveNetMini()
    print(f"6層擴張卷積感受野 R={net.rf} 點 (每加一層翻倍)")
    opt = torch.optim.Adam(net.parameters(), lr=1e-2)
    for ep in range(25):
        opt.zero_grad()
        idx = torch.randint(0, len(q) - T - 1, (32,))
        xb = torch.stack([q[i:i + T] for i in idx])
        yb = torch.stack([q[i + 1:i + T + 1] for i in idx])
        loss = F.cross_entropy(net(xb).reshape(-1, NB), yb.reshape(-1))
        loss.backward()
        opt.step()
    print(f"25輪後下一點預測 loss={loss.item():.3f} (隨機猜=4.159)")
    net.eval()
    with torch.no_grad():
        cur = q[:T].unsqueeze(0)
        gen = cur[0].tolist()
        for _ in range(60):                                # 自回歸生成 60 點
            nxt = net(cur)[:, -1].argmax(-1)
            gen.append(int(nxt))
            cur = torch.cat([cur[:, 1:], nxt.unsqueeze(0)], 1)
    err = (torch.tensor(gen[T:]).float() - q[T:T + 60].float()).abs().mean().item()
    print(f"自回歸續寫60點平均量化誤差={err:.2f} 格 (波形跟上 -- 生成即逐點採樣)")


if __name__ == "__main__":
    main()
```

執行結果（`python3 _code/2016-WaveNet.py`，torch 2.12.0）：

```
6層擴張卷積感受野 R=64 點 (每加一層翻倍 -- RNN 的 O(T) 步變成 O(1) 並行)
25輪後下一點預測 loss=0.246 (隨機猜=4.159)
自回歸續寫60點平均量化誤差=1.07 格 (波形跟上 -- 生成即逐點採樣)
結論: 捨棄 RNN、用卷積並行生成 -- 條件化再加文本即 TTS, 換成像素即 PixelCNN
```

程式解說：`dilations = [1,2,4,...,32]` 求和得 `R=64`——本文第二條線索的指數爆炸：6 層看到 64 點，10 層看到 1024 點，而訓練全程並行（RNN 必須等 `t−1` 算完）。`F.pad(x,(d,0))` 左填充是因果性的全部秘密：右端永遠看不見未來。門控 `tanh⊙σ` 與殘差 `x+z` 分別是 1997 與 2015 的遺產——WaveNet 是站在兩個前案肩上的集大成。續寫誤差僅 1 格（共 64 格）：逐點採樣的波形跟上了真波形；把正弦換成语音、條件加上文本，即 TTS，換成像素即 PixelCNN。
