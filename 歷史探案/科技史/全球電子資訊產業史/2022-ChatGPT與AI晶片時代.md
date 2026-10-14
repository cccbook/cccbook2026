# 2022：ChatGPT 與 AI 晶片時代 — 封裝從後段雜工變成前線戰場

## 案情
2022 年 11 月 30 日，OpenAI 上線 ChatGPT，兩個月內月活躍用戶破億，創史上最快紀錄。其底層 GPT 系列模型以 Transformer 架構訓練於上萬片 NVIDIA GPU 之上；2022 年 NVIDIA 發表 H100，搭配台積電 4N 製程與 CoWoS 先進封裝。自此，AI 算力成為戰略物資，而過去被視為後段「雜工」的封裝測試，躍居產業最前線。

## 前因
- 2017 年 Google 團隊發表〈Attention Is All You Need〉，Transformer 取代 RNN 成為序列模型骨幹。
- 2020 年 GPT-3 有 1,750 億參數，訓練算力約 $3.14\times10^{23}$ FLOPs；模型規模與算力需求指數成長。
- 2020 年 A100 問世並以台積電 7nm＋CoWoS-S 封裝；2022 年 H100（4N 製程、HBM3 顯示記憶體）量產。
- 台積電 CoWoS 產能自 2023 年起長期供不應求，成為 AI 晶片出貨的真正瓶頸——不是晶圓，而是封裝。

## 線索與推理
偵探拆解本案的三層因果。第一層：為什麼是 Transformer？因為注意力機制可以完全平行化——RNN 必須逐字遞迴，Transformer 的 self-attention 卻能對整個序列一次算完，恰好匹配 GPU 的矩陣平行架構，訓練效率質變。第二層：為什麼瓶頸轉向封裝？因為單一晶粒（die）面積已逼近光罩極限（約 850 mm²），而模型愈大愈需要更多 HBM 記憶體頻寬；解方是異質整合——把運算晶粒與多顆 HBM 以矽中介層（interposer）併封成「2.5D」模組。良率是關鍵推理：晶粒愈大，良率以指數崩落，而切割成多顆 chiplet 再拼裝，可把良率壓力轉嫁給封裝。第三層：決策邏輯——NVIDIA 靠 CUDA 軟體護城河把 GPU 變成 AI 事實標準；台積電靠 CoWoS 綁定先進封裝霸權；微軟、Google、Meta 競相囤積 H100。三方合流，把「封裝」推上摩爾定律微縮趨緩後的新戰場。

## 理論
Transformer 自注意力（self-attention）：
$$\mathrm{Attention}(Q,K,V) = \mathrm{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V$$
其計算與記憶體搬移量隨序列長度 $n$ 成 $O(n^2)$，複雜度主要由 HBM 頻寬決定，故 HBM 堆疊與封裝成為效能核心。

GPU 需求成長分析：訓練所需 FLOPs 約為 $C \approx 6ND$（$N$ 為參數數、$D$ 為訓練 token 數，前向 2N＋反向 4N）。GPT-3 到 GPT-4 級模型算力需求成長數百倍，若訓練時限 $T$ 固定，需求 GPU 數
$$N_{GPU} = \frac{C}{\eta \cdot F \cdot T}$$
（$F$ 為單卡有效算力、$\eta$ 為使用率），呈指數上揚。

封裝良率模型（Chiplet 的數學勝利）：單一大晶粒良率 $Y_1 = e^{-D_0 A}$（$D_0$ 為缺陷密度、$A$ 為面積）；切成 $n$ 顆小晶粒（每顆面積 $A/n$），則 $Y_{chiplet} = \left(e^{-D_0 A/n}\right)^n$——雖然數學上等值，但壞一顆只換一顆，實際有效良率 $Y_{eff} \approx Y_{chiplet} + (1-Y_{chiplet})\cdot\text{更換回收率}$，加上 KGD（已知良品）篩選，遠優於全押大晶粒。

## 後果
1. NVIDIA 市值在 2023–2024 年突破數兆美元，成為 AI 時代的算力軍火商。
2. CoWoS 產能擴張數倍，台積電、日月光、Amkor 與記憶體三強（SK 海力士、三星、美光）全面受惠。
3. AMD、Intel、Google TPU、自研 ASIC 蜂擁投入 chiplet 與 2.5D/3D 封裝；UCIe 聯盟制定晶粒互聯標準。
4. 美國對中國 AI 晶片出口管制（A100/H100 禁售），算力成為地緣政治武器。
5. 封測產業由勞力與資本密集轉為技術密集，「後段」一詞自此名存實亡。

## 冷案檔案
- 時間：2022-11-30 ChatGPT 上線；2022 年 H100 發表。
- 案由：Transformer 大模型引爆算力需求，先進封裝（CoWoS、chiplet）成為半導體競爭新前線。
- 歷史定位：封裝地位大逆轉的元年——摩爾定律的接力棒，從光刻正式交給了封裝。
