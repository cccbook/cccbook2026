# 2023 - LLaMA 開源大模型

## 案件摘要

2023 年 2 月，Meta 發表 **LLaMA**：7B 至 65B 的基礎語言模型，並（最初僅限研究申請、後因權重外洩而事實開源）公開權重。核心貢獻是**用更小的規模、更乾淨的資料與現代化零件，達到 GPT-3/Gopher 級的品質**：

$$\text{LLaMA-65B} \approx \text{Chinchilla-70B} > \text{GPT-3-175B}, \qquad \text{零件：RMSNorm + SwiGLU + RoPE}$$

其中旋轉位置編碼的角度為 $\theta_i = 10000^{-2i/d}$。兇手不是更大的模型，而是**「開源權重」這個分發決策**——LLaMA 是 Alpaca、Vicuna、Mistral、DeepSeek 等開源生態的源頭，改寫了大模型的權力結構。

## 前因 -- 為什麼會有這個案子

- 2022 年 Chinchilla（見「2022-Chinchilla規模法則.md」）證明 70B 級模型配合充足資料即可達頂級品質——**「小而對」的技術前提已備**。
- 2022 年 ChatGPT（見「2022-ChatGPT與RLHF.md」）引爆消費級需求，但 OpenAI 權重封閉；學術界與開源社群面臨「**沒有權重，就無法做複現、安全與可解釋性研究**」的困境。
- Meta（Yann LeCun、Guillaume Lample 等）的動機：開放權重可建立生態、吸引人才、避免被單一公司壟斷；LeCun 長期主張開放研究是 AI 進步的引擎。
- 前驅線索：2022 年 EleutherAI 的 GPT-J/GPT-NeoX 與 BigScience 的 BLOOM 已嘗試開源，但品質落後封閉前沿一個世代——問題是**能不能用開源追上前沿**。
- 工程累積：Meta 的 GPU 叢集與 OPT（2022，品質不佳的開源嘗試）提供了教訓——開源不夠，還要**夠好**。
- 現代化零件的累積：RMSNorm（2019）、SwiGLU（2020）、RoPE（2021 RoFormer）各自在小規模驗證，等待一次組合的勝利。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：現代化零件的組合

LLaMA 的配方是「舊架構 + 三個新零件」：

| 零件 | 公式/機制 | 取代 |
|---|---|---|
| RMSNorm | $\text{RMSNorm}(x) = \dfrac{x}{\sqrt{\frac{1}{d}\sum_i x_i^2 + \epsilon}} \odot g$ | LayerNorm（去掉均值中心化，省算力） |
| SwiGLU | $\text{SwiGLU}(x) = (\text{Swish}(xW_1) \odot xW_2)W_3$ | ReLU 前饋層 |
| RoPE | $\theta_i = 10000^{-2i/d}$ 旋轉位置編碼 | 絕對位置編碼 |

RoPE 的本質：把 query 與 key 的每個二維子空間**旋轉**位置相關的角度，使注意力分數只依賴**相對位置**：

$$\langle R_m q,\ R_n k \rangle = \langle q,\ R_{n-m} k \rangle$$

**相對位置內建於注意力，外推更自然**——這成為此後幾乎所有開源模型的標準配備。

### 第二條線索：資料配方——規模不在大，在乾淨

LLaMA-65B 用 1.4T token（延續 Chinchilla 的啟示），但關鍵在**資料混合**：

| 資料源 | 佔比 | 特性 |
|---|---|---|
| CommonCrawl | 67% | 經 CCNet 管線過濾 |
| C4 | 15% | 清潔網路文字 |
| GitHub | 4.5% | 程式碼 |
| Wikipedia | 4.5% | 百科知識 |
| Books | 4.5% | 長文 |
| ArXiv | 2.5% | 學術 |
| StackExchange | 2% | 問答 |

品質過濾（去重、語言分類、n-gram 過濾）是重點：**同樣 1.4T token，乾淨混合打敗 GPT-3 的 300B 髒資料配方**。

### 第三條線索：效能判決書

| 模型 | 參數 | 常識推理（平均） | MMLU | 程式碼 HumanEval |
|---|---|---|---|---|
| GPT-3 | 175B | ~69 | 43.9% | ~0% |
| Gopher | 280B | ~70 | 60.0% | ~10% |
| Chinchilla | 70B | ~73 | 67.6% | ~19% |
| LLaMA-65B | 65B | **~77** | 63.4% | ~24% |

65B 在常識與程式碼上超越 Gopher/Chinchilla，逼近 GPT-3 數倍的品質於一體——**開源第一次站上前沿**。

### 第四條線索：權重外洩——計畫外的分發實驗

LLaMA 權重以「研究申請」名義發布，兩週內即被外洩至 4chan 與 Hugging Face。Meta 選擇**不回收**，反而在 2023 年 7 月以 Llama 2 名義正式商業開源。**這樁意外成為史上最重要的「洩密」**：Alpaca（Stanford，$600 微調成本）、Vicuna、WizardLM 在數月內湧現，證明小模型 + 指令微調 + RLHF 可以逼近 ChatGPT 體驗。

### 第五條線索：GQA——推論成本的預留

LLaMA 2 70B 版本導入**分組查詢注意力**（Grouped-Query Attention）：多個 query 頭共享一組 key/value 頭：

$$\text{MHA：} H_q = H_{kv} = H \qquad \to \qquad \text{GQA：} H_q = H,\ H_{kv} = H/g$$

KV cache 的記憶體占用下降 $g$ 倍，**推論吞吐量大幅提升**——這是 Chinchilla 忽略推論成本之後的補償設計：訓練可以只顧最優，部署必須顧帳單。GQA 從此成為開源長上下文模型的標準配備。

## 結案 -- 後果與影響

- **開源生態爆發**：Alpaca、Vicuna → Mistral（2023）、Qwen、Gemma、Llama 3 → **DeepSeek（2024–2025）**。開源陣營從落後一個世代縮短到數月。
- **權力結構改寫**：大模型能力不再由少數公司壟斷；本地部署、微調、蒸餾成為普遍實務。
- **對齊與安全研究的民主化**：任何人可研究 RLHF、可解釋性、越獄——同時引發「開源是否危險」的政策爭論（歐盟 AI 法案、美國行政命令）。
- **配方標準化**：RMSNorm + SwiGLU + RoPE + GQA 成為此後所有開源模型的預設零件，Transformer 的「現代變體」就此定型。
- **微調即定製**：Alpaca 式低成本微調使企業可自建專屬模型，「基礎模型 + 微調」從研究方法變成工程實務。
- 埋下伏筆：LLaMA 證明「小而對」的路線，DeepSeek 更進一步——以**低成本的訓練效率革命**與強化學習推理（見「2025-DeepSeek-R1.md」），證明開源可以在推理能力上站上前沿。本書的開源主線自此直通終章。
- Meta 以 Llama 系列持續迭代（2024 年 Llama 3 過訓練 15T token，修正 Chinchilla 最優解），開源與封閉的競賽成為 AI 史的主旋律之一。
- 偵探結語：LLaMA 案件的偵探學教訓——**「夠好」是開源革命的門檻，不是「最好」**。BLOOM 與 GPT-NeoX 開源了但太弱，LLaMA 開源了而且夠強，革命就在兩者之間分岔。權重外洩的意外則提醒我們：技術的命運有時不由發布者決定，而由**分發的物理定律**決定——檔案一旦存在於網路，就無法收回。

## 關鍵人物與文獻

- Hugo Touvron、Thibaut Lavril、Guillaume Lample、Timothée Lacroix 等（Meta AI）：《LLaMA: Open and Efficient Foundation Language Models》（2023）。
- Zhang & Sennrich：《Root Mean Square Layer Normalization》（2019，RMSNorm）。
- Shazeer：《GLU Variants Improve Transformer》（2020，SwiGLU）。
- Su 等：《RoFormer: Enhanced Transformer with Rotary Position Embedding》（2021，RoPE）。
- Hoffmann 等：《Training Compute-Optimal Large Language Models》（2022，Chinchilla）。
- Rohan Taori 等：《Stanford Alpaca: An Instruction-following LLaMA Model》（2023）。
- 相關案件：2022-Chinchilla規模法則.md、2022-ChatGPT與RLHF.md、2023-GPT-4多模態.md、2025-DeepSeek-R1.md
