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
