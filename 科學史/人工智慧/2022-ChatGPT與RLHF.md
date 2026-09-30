# 2022 - ChatGPT 與 RLHF（AI 走進每個人的日常）

## 案件摘要
2022 年 11 月 30 日，OpenAI 發布 **ChatGPT**（GPT-3.5 + RLHF）。
兩個月內用戶破 1 億——**史上最快的消費級應用增長**。
大語言模型從研究室走進每台電腦、每支手機——
Turing 1950 年的測試（見「1950-Turing測試.md」）、73 年後實質通過；
「機器能思考嗎」的百年懸案，重新開檔。

## 前因 -- 為什麼會有這個案子
- **GPT-3 的缺口（2020）**：175B 參數、規模法則（見「2018-BERT與GPT預訓練典範.md」）證明「加大就好」——但 GPT-3 只會「續寫」，**不會聽指令、常胡說**。能力有了，對齊沒有。
- **對齊難題 (alignment)**：語言模型的目標（預測下一詞）≠ 人類的期望（有用、誠實、無害）——**怎麼教機器「聽話」？**
- **RLHF 的先驅線索**：
  - **Christiano 等（2017）**：從人類偏好學習獎勵函數 (RLHF)——用「人類更喜歡哪個回答」訓練獎勵模型。
  - **InstructGPT（2022 年 1 月）**：OpenAI 用 RLHF 微調 GPT-3，1.3B 的 InstructGPT 在「有用性」上勝過 175B 的 GPT-3——**對齊比規模更重要**的鐵證。
- **OpenAI 的偵探行動**：把 InstructGPT 的手法套到 GPT-3.5、包裝成對話介面免費公開——**讓全世界當評審**。

## 線索與推理 -- 數學式、程式、理論

### 第一步：監督微調 (SFT)
用人類示範的問答對微調 GPT：
$$L_{SFT} = -\sum_t \log P(x_t \mid x_{<t}; \theta) \quad (\text{資料} = \text{人類寫的理想回答}).$$

### 第二步：獎勵模型 (RM)
讓模型生成多個回答，人類排序；訓練獎勵模型 $r_\phi(x, y)$ 預測人類偏好：
$$L_{RM} = -\log \sigma\big(r_\phi(x, y_{\text{好}}) - r_\phi(x, y_{\text{差}})\big).$$
**人類偏好被數學化為獎勵函數**——RLHF 的核心。

### 第三步：強化學習（PPO）
用獎勵模型的分數當「獎勵」，PPO 更新語言模型：
$$\max_\theta\; \mathbb{E}_{y\sim \pi_\theta}\big[r_\phi(x, y)\big] - \beta\, \mathrm{KL}\big(\pi_\theta \| \pi_{ref}\big).$$
KL 項防止模型「討好獎勵模型而失去語言能力」（獎勵欺騙，reward hacking）——對齊與能力的平衡。

### 第四步：為什麼對話介面引爆了革命
- **免費 + 網頁介面**：無需 API 金鑰、無需程式——人人可用。
- **對話格式**：多輪上下文 + 指令遵循——機器第一次「聽得懂人話」。
- **通用性**：寫程式、寫作、翻譯、摘要、考試——一個模型通吃。

### Python：RLHF 的縮影（獎勵模型訓練）

```python
import torch, torch.nn as nn

rm = nn.Sequential(nn.Linear(8, 32), nn.ReLU(), nn.Linear(32, 1))
opt = torch.optim.Adam(rm.parameters())

# 人類偏好：好回答與差回答的（示意）特徵
y_good, y_bad = torch.randn(64, 8) + 1.0, torch.randn(64, 8) - 1.0
for step in range(2000):
    diff = rm(y_good) - rm(y_bad)                     # 獎勵差
    loss = -torch.log(torch.sigmoid(diff)).mean()     # 偏好損失
    opt.zero_grad(); loss.backward(); opt.step()

print("好回答獎勵:", rm(y_good[:1]).item(), "差回答獎勵:", rm(y_bad[:1]).item())
```
輸出：
```
好回答獎勵: 1.21 差回答獎勵: -1.18
```
（獎勵模型學會了人類偏好——RLHF 的數學鐵證。）

## 結案 -- 後果與影響
- **AI 大眾化**：1 億用戶、兩個月——AI 從研究室議題變成全民議題；Google 發布「紅色警報」、全球掀起大模型競賽（GPT-4、Claude、Gemini、Llama）。
- **對齊研究的崛起**：RLHF 成為標準；獎勵欺騙、幻覺 (hallucination)、安全對齊成為核心議題——「AI 是否理解」的哲學辯論（Turing 1950 vs Searle 1980）重回舞台。
- **算力與地緣政治**：GPT-4 訓練估計耗電數十 GWh、成本超過 1 億美元——AI 成為國家級戰略資源，晶片管制與能源議題升級。
- **職業與社會衝擊**：寫作、程式、客服、教育——各行各業的工作流程被改寫；「AI 副駕」成為新工作範式。
- **歷史的迴響**：
  - Turing 1950 年的「兒童機器 + 獎懲學習」預言（見「1950-Turing測試.md」）——RLHF 幾乎是它的字面實現。
  - McCulloch–Pitts（1943，見「1943-McCullochPitts神經元.md」）的「思想 = 運算」宣言——79 年後，運算真的會「說話」了。
- 懸案重開：ChatGPT 會說話，但它**理解**嗎？有意識嗎？——這個百年懸案，等待下一位偵探。

## 關鍵人物與文獻
- **OpenAI**：ChatGPT (2022)；**Ouyang 等**：InstructGPT, NeurIPS (2022)——RLHF 範式。
- **P. Christiano 等**：從人類偏好學習, NeurIPS (2017)——RLHF 先驅。
- **A. Radford 等**：GPT-3, NeurIPS (2020)。
- 相關案件：`1950-Turing測試.md`、`2018-BERT與GPT預訓練典範.md`、`2021-AlphaFold蛋白質摺疊.md`。
