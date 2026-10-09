# 2022 - Stable Diffusion 開源擴散

## 案件摘要

2022 年 8 月，Stability AI 與 LMU Munich 的 CompVis 團隊釋出 **Stable Diffusion**：以**潛空間擴散**（Latent Diffusion）訓練、權重完全開源的文生圖模型。核心公式是在壓縮 8 倍的潛空間中做條件去噪：

$$\epsilon_\theta(x_t, t, c) \quad \text{其中}\ c = \text{CLIP text embedding},\ x_t = \text{VAE 潛碼}$$

兇手不是更好的生成品質，而是**「開源權重 + 潛空間省算力」的組合拳**：DALL-E 2 把影像生成鎖在 API 裡，Stable Diffusion 把它放進每個人的顯示卡——**影像生成的民主化**，數月內衍生出數十萬個社群微調模型。

## 前因 -- 為什麼會有這個案子

- 2020 年 DDPM（見「2020-DDPM擴散模型.md」）證明擴散模型可以生成高品質影像，但**在像素空間訓練 512×512 影像的算力成本極高**。
- 2021 年 CLIP（見「2021-CLIP多模態對齊.md」）建立了影像與文字的對齊空間，使「文字條件生成」在數學上可行。
- 2022 年 4 月 OpenAI 的 DALL-E 2 與 5 月 Google 的 Imagen 展示了驚人的文生圖品質，但**權重封閉、僅限 API/內測**——生成能力成為少數公司的專利。
- 偵探視角：2022 年年中，文生圖的三條前驅線索（擴散、對齊、省算力）已各自到位，只差一次**組合 + 分發**——案件中真正的難題從來不是「能不能做」，而是「做給誰用」。
- CompVis 團隊（Robin Rombach、Patrick Esser 等）此前已發表 Latent Diffusion 論文（CVPR 2022）：**先壓縮、再擴散**，在潛空間訓練可省下大部分算力。
- Stability AI（Emad Mostaque）的動機：他深信生成式 AI 應該**開源、去中心化**，像 Linux 之於作業系統；他資助 CompVis 訓練更大版本並公開權重。
- Runway 團隊加入，帶來應用導向的工程能力。三方合力，LAION-5B 開放資料集（CLIP 過濾的 50 億圖文對）提供燃料。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：潛空間擴散——先壓縮，再去噪

DDPM 在像素空間對 $x_t$ 去噪，Stable Diffusion 先用 VAE 把影像壓縮 8 倍（512×512×3 → 64×64×4），再在潛空間擴散：

$$z = \mathcal{E}(x), \qquad z_t = \sqrt{\bar\alpha_t}\, z_0 + \sqrt{1-\bar\alpha_t}\, \epsilon$$

訓練目標是在潛空間預測加入的雜訊：

$$L_{\text{LDM}} = \mathbb{E}_{\mathcal{E}(x),\, \epsilon,\, t}\left[ \|\epsilon - \epsilon_\theta(z_t, t, c)\|^2 \right]$$

生成時反覆去噪得到 $\hat z_0$，再解碼 $\hat x = \mathcal{D}(\hat z_0)$。**8 倍邊長壓縮 = 64 倍像素數下降**，主要算力消耗被砍掉一個數量級——這就是消費級 GPU 能跑得動的原因。

### 第二條線索：交叉注意力——文字如何開口說話

文字條件 $c$ 不用簡單串接，而是透過 **cross-attention** 注入 U-Net 的每一層：

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^\top}{\sqrt{d}}\right)V, \quad Q = \phi(z_t),\ K = V = \tau_\theta(c)$$

其中 $\tau_\theta$ 是 CLIP 文字編碼器。每個影像位置「詢問」每個文字 token：「你跟我有關嗎？」——CLIP 的對齊空間（2021 年的遺產）讓這個詢問有意義。**分離式條件架構**（conditioning via cross-attention）從此成為多模態生成模型的標準零件。

### 第三條線索：CFG——無分類器的引導

生成品質的關鍵調味是**Classifier-Free Guidance**（Ho & Salimans, 2022）：訓練時隨機丟棄條件（10% 機率），推論時外推條件與無條件預測的差值：

$$\tilde\epsilon_\theta(z_t, t, c) = \epsilon_\theta(z_t, t, \varnothing) + w \cdot \big(\epsilon_\theta(z_t, t, c) - \epsilon_\theta(z_t, t, \varnothing)\big)$$

引導強度 $w$（常取 5–15）控制「聽話程度」與「多樣性」的取捨：$w$ 越大越忠於提示、越可能失真。**一個標量旋鈕，讓使用者直接操控生成行為**——這在介面史上意義重大。

### 第四條線索：開源權重——分發即革命

| 模型 | 權重 | 算力需求 | 發布方式 |
|---|---|---|---|
| DALL-E 2 | 封閉 | 雲端叢集 | API、內測 |
| Imagen | 封閉 | TPU 叢集 | 僅論文示意圖 |
| Stable Diffusion | **公開（OpenRAIL）** | **消費級 GPU（8GB 顯卡可跑）** | GitHub + Hugging Face |

權重一開源，社群即刻展開：ControlNet（可控生成）、LoRA（低成本微調）、動畫、修復、超解析……數月內 Hugging Face 上湧現數萬個衍生模型。**開源把生成模型從產品變成平台**。

LoRA 的數學值得一記：微調增量被約束為低秩矩陣乘積

$$W' = W_0 + \Delta W = W_0 + BA, \quad B \in \mathbb{R}^{d \times r},\ A \in \mathbb{R}^{r \times k},\ r \ll \min(d, k)$$

可訓練參數下降數個數量級，單張消費級顯卡即可微調——**低秩假說**（微調所需的本質變化維度很低）成為開源生態的另一根支柱。

## 結案 -- 後果與影響

- **影像生成民主化**：任何人可本地執行文生圖，插畫、設計、遊戲素材產業劇變；同時引發藝術家抗議、版權訴訟（Getty、藝術家集體訴 Stability AI）——生成時代的法律懸案。
- **訓練資料正當性成為戰場**：LAION-5B 爬取網路圖片的做法被挑戰，催生資料授權、選擇性退出（opt-out）機制的研究。
- **推論加速的研究爆發**：DDIM（跳步取樣）、latent consistency models、蒸餾——把數十步去噪壓到數步，消費級體驗再上層樓。
- **開源生態的正回饋**：Stable Diffusion 證明開源社群能追上封閉前沿，為「2023-LLaMA開源大模型.md」的開源策略提供心理與技術依據。
- **潛空間擴散成為標準**：此後影像與視訊模型幾乎全採潛空間路線，直達「2024-Sora世界模型.md」的視訊擴散 Transformer。
- 埋下伏筆：Sora 主張「影片生成 = 世界模擬器」；而 LeCun 陣營的「2024-VJEPA世界模型.md」提出另一條**預測表徵而非生成像素**的路線——兩條世界模型路線的對決自此埋下。
- DiT（Diffusion Transformer）在 2022 年底出現，把 U-Net 換成 Transformer，為 Sora 的架構直接鋪路。
- 偵探結語：這樁案件的兇器清單值得細數——**VAE 的壓縮**（省算力）、**cross-attention**（讓文字開口）、**CFG**（讓使用者操控）、**開源權重**（讓分發革命）。四者缺一，Stable Diffusion 都不會是 Stable Diffusion：少了 VAE 它跑不進消費級 GPU；少了開源它只是第二個 DALL-E 2。**技術零件與分發決策的乘積，才是革命的真正量測**。

## 關鍵人物與文獻

- Robin Rombach、Andreas Blattmann、Dominik Lorenz、Patrick Esser、Björn Ommer（LMU Munich CompVis）：《High-Resolution Image Synthesis with Latent Diffusion Models》（CVPR 2022）——Stable Diffusion 的學術前身。
- Jascha Sohl-Dickstein 等：《Deep Unsupervised Learning using Nonequilibrium Thermodynamics》（2015）——擴散思想的熱力學源頭。
- Jonathan Ho 等：《Denoising Diffusion Probabilistic Models》（2020，DDPM）——擴散模型實用的轉折點。
- Jonathan Ho、Tim Salimans：《Classifier-Free Diffusion Guidance》（2022）。
- Stability AI（Emad Mostaque）、Runway、CompVis：Stable Diffusion 權重發布（2022 年 8 月）。
- Alec Radford 等：《Learning Transferable Visual Models From Natural Language Supervision》（2021，CLIP）。
- Christoph Schuhmann 等：LAION-5B 資料集（2022）。
- William Peebles、Saining Xie：《Scalable Diffusion Models with Transformers》（2022，DiT）。
- 偵探手記：本篇是全書少數「分發決策與技術同等重要」的案件——同樣的潛空間擴散，封閉發布只是論文，開源發布才是革命。革命的量測不在品質榜，而在**誰的顯示卡能跑**。
- 依「科學與歷史/神經網路/」Transformer 檔案：U-Net 是 CNN 卷積世代的遺產，DiT 把它送進注意力世代——影像生成完成了從卷積到注意力的最後一步遷徙。
- 相關案件：2020-DDPM擴散模型.md、2021-CLIP多模態對齊.md、2023-LLaMA開源大模型.md、2024-Sora世界模型.md、2024-VJEPA世界模型.md

## 補充 -- 程式實作（python + pytorch + sklearn）

本案三件套（潛空間擴散＋文字條件＋CFG）的最小可執行版本，見 `_code/2022-StableDiffusion.py`（已實測可跑，CPU 約 2 分鐘；8×8 圓環／方框）：

```python
# 2022 - Stable Diffusion: L_LDM = E||ε-ε_θ(z_t,t,c)||²; CFG: ε̃=ε_∅+w(ε_c-ε_∅)
import torch
import torch.nn as nn
from sklearn.decomposition import PCA


def make_images(n=600):  # 圓環 vs 方框 (潛空間分得開的兩類)
    X = torch.zeros(n, 64)
    y = torch.zeros(n, dtype=torch.long)
    yy, xx = torch.meshgrid(torch.arange(8), torch.arange(8), indexing="ij")
    d2 = (xx - 3.5) ** 2 + (yy - 3.5) ** 2
    for i in range(n):
        c = i % 2
        y[i] = c
        img = torch.zeros(8, 8)
        if c == 0:
            img[(d2 > 3) & (d2 < 14)] = 1.0
        else:
            img[1:7, 1:7] = 1.0
            img[2:6, 2:6] = 0.0
        X[i] = img.reshape(-1) + torch.randn(64) * 0.05
    return X.clamp(0, 1), y


NULL = 2  # 第3個 id = 無條件 (CFG 的 ∅)


def main():
    torch.manual_seed(0)
    X, y = make_images()
    pca = PCA(n_components=8).fit(X.numpy())  # E(x): 壓縮器 (VAE 的精神縮影)
    Z = torch.tensor(pca.transform(X.numpy()), dtype=torch.float32)
    print("像素 64 維 -> 潛碼 8 維 (壓縮 8x -- 先壓縮再去噪)")
    T = 50
    beta = torch.linspace(1e-3, 0.05, T)
    abar = torch.cumprod(1 - beta, 0)
    txt = nn.Embedding(3, 4)  # τ(c): 圓環/方框/null 各一向量

    class Eps(nn.Module):
        def __init__(self):
            super().__init__()
            self.te = nn.Embedding(T, 4)
            self.m = nn.Sequential(nn.Linear(8 + 4 + 4, 64), nn.ReLU(),
                                   nn.Linear(64, 64), nn.ReLU(), nn.Linear(64, 8))

        def forward(self, zt, t, c):
            return self.m(torch.cat([zt, self.te(t), txt(c)], 1))

    net = Eps()
    opt = torch.optim.Adam(list(net.parameters()) + list(txt.parameters()), lr=1e-2)
    for ep in range(400):
        t = torch.randint(0, T, (256,))
        idx = torch.randint(0, len(Z), (256,))
        z0, c = Z[idx], y[idx]
        eps = torch.randn(256, 8)
        zt = abar[t].sqrt().unsqueeze(1) * z0 + (1 - abar[t]).sqrt().unsqueeze(1) * eps
        c_in = torch.where(torch.rand(256) < 0.1, torch.full_like(c, NULL), c)
        opt.zero_grad()
        ((net(zt, t, c_in) - eps) ** 2).mean().backward()  # L_LDM
        opt.step()
    # (CFG 採樣比較 w=0 vs 3, 見 _code/2022-StableDiffusion.py 全文)


if __name__ == "__main__":
    main()
```

執行結果（`python3 _code/2022-StableDiffusion.py`，torch 2.12.0／sklearn 1.9.0）：

```
像素 64 維 -> 潛碼 8 維 (壓縮 8x -- 先壓縮再去噪, 省計算)
CFG 效果 (生成落到『要求類別』的比例):
  w=0.0: 指派準確率=0.50 (不分條件亂生)
  w=3.0: 指派準確率=1.00 (聽從文字條件)
結論: 潛擴散(CPU秒級) + 交叉注意力(文字開口) + CFG(聽話旋鈕) = 開源擴散三件套
```

程式解說：PCA 潛碼（8 維）即第一條線索的 `z = E(x)`——此處以第一性原理的壓縮器代替 VAE，精神相同：擴散發生在潛空間而非像素。`txt` 的三個向量即 `τ(c)`：圓環、方框、null（∅），10% 丟條件練出無條件分支給 CFG 用。判決數字：`w=0` 指派 0.50（不分條件亂生）、`w=3` 指派 1.00（`ε̃ = ε_∅ + 3(ε_c − ε_∅)` 把採樣推向文字）——`w` 即「聽話旋鈕」。實測附帶兩課：(1) 潛空間必須先分得開類別（圓環／方框的類間距是類內的 30 倍；早期用實心圓／方，PCA 下完全重疊，條件無從學起——**壓縮器決定條件的天花板**）；(2) 指派度量正反寫反會得 0.00，驗屍要看公式不要看數字。
