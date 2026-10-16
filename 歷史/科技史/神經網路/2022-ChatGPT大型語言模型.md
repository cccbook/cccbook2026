# 2022 - ChatGPT 大型語言模型（RLHF 與對齊）

## 案件摘要
2022 年 11 月 30 日，**OpenAI** 上線 **ChatGPT**——
$$\boxed{\text{兩個月破 1 億使用者——史上成長最快的消費級應用}}$$
它的核心不是新架構，而是**新訓練法**：前身 **InstructGPT**
（**Long Ouyang** 等 28 人，2022 年 3 月）用**人類回饋強化學習（RLHF）**
把一個「會預測下一個詞」的 GPT-3，變成**聽話的助理**：
- **第一階段 SFT（監督微調）**：人類標註員示範「理想回答」——模仿學習；
- **第二階段獎勵模型（RM）**：人類對答案**排序**，訓練一個會打分的模型；
- **第三階段 PPO**：用獎勵模型的分數**強化學習**微調語言模型。
$$\text{GPT-3（2020）：能力} \xrightarrow{\text{RLHF（2022）：對齊}} \text{ChatGPT：走入大眾}.$$
**這是「對齊（alignment）」從研究論文變成產品的關鍵案件**——
**大型語言模型（LLM）從此成為家家戶戶的工具**。

## 前因 -- 為什麼會有這個案子
- **GPT-3 有能力但不聽話（2020）**：
  **2020 年 GPT-3**（見 `2020-布朗GPT-3.md`）證明了規模帶來質變——
  但它只會**續寫**，不會**回答**：
  $$\text{問：「法國首都是哪裡？」} \to \text{GPT-3：「這是個常見的地理問題……」（續寫，不給答案）}$$
  使用者需要**提示詞技巧（prompt engineering）**才能榨出答案——
  **模型沒有跟「人類的意圖」對齊**。
- **語言模型的根本錯位（2021–2022）**：
  訓練目標是「預測**網路上**的下一個詞」——但**網路文本 ≠ 人類想要的回答**：
  $$P_{\text{訓練}}(\text{下一個詞} \mid \text{網路語料}) \neq P_{\text{人類想要的}}(\text{回答} \mid \text{指令}).$$
  模型會**幻覺**（一本正經地胡說）、**盲從偏見**、
  被誘導寫出**有害內容**——2019 年 GPT-2「太危險」的疑慮到 GPT-3 仍未解決。
- **RLHF 的先行者（2017–2020）**：
  - **2017 深度強化學習**：OpenAI 早已用 **PPO（Proximal Policy Optimization，
    Schulman 2017）** 在遊戲（Dota 2）上訓練代理人；
  - **2020 年**，OpenAI 的 **Paul Christiano** 等發表
    *Learning from Human Preferences*——用**成對偏好**訓練獎勵模型，
    在**蒼蠅 backflip**（Backflipper）這類遊戲上驗證——
    $$\text{強化學習的獎勵} \xrightarrow{\text{人類偏好}} \text{「獎勵」不用手寫，用標註學出來}.$$
  - **2021 年 1 月**，**Jan Leike** 團隊發表 RLHF 用於語言模型的論文——
    **六個月後 Anthropic 從 OpenAI 分裂**（Dario Amodei），對齊是核心理由。
- **InstructGPT 的整合（2022 年 3 月）**：
  **Ouyang 等把三件事拼在一起**：SFT + 獎勵模型 + PPO——
  只有 **1.3B 參數**的 InstructGPT，在人類偏好評測上**勝過 175B 的 GPT-3**：
  $$\boxed{\text{對齊 beats 規模：1.3B 的「聽話模型」 > 175B 的「能力模型」}}$$
  **九個月後，這條配方掛上了 ChatGPT 的名字**。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：RLHF 三階段流程
**第一階段：SFT（Supervised Fine-Tuning）**——
人類標註員對每個指令寫出**示範回答**（約 13,000 筆），做監督微調：
$$\max_{\theta} \; \mathbb{E}_{(x, y) \sim \mathcal{D}_{\text{SFT}}} \big[ \log \pi_\theta(y \mid x) \big]$$
- $x$：指令、$y$：人類示範的回答、$\pi_\theta$：語言模型策略；
- **這是模仿**：模型學會「回答的格式」，但人類示範有限，品質有上限。

**第二階段：獎勵模型（Reward Model）**——
標註員對同一指令的多個回答**排序**（約 33,000 筆成對比較）：
$$\boxed{L(\phi) = -\log \sigma\big(r_\phi(x, y_{\text{chosen}}) - r_\phi(x, y_{\text{rejected}})\big)}$$
- $r_\phi(x, y)$：獎勵模型給「回答 $y$」的分數；
- $\sigma$：sigmoid——**Bradley–Terry 模型**：勝率
  $$P(y_{\text{chosen}} \succ y_{\text{rejected}}) = \sigma(r_{\text{chosen}} - r_{\text{rejected}});$$
- **為什麼用排序不用打分？** 人類打分不一致（有人給 7 分、有人給 8 分），
  但「**誰比較好**」的判斷穩定得多——**只學差值，不學絕對值**。

**第三階段：PPO（強化學習微調）**——
用獎勵模型當**評審**，強化學習更新語言模型：
$$\max_{\theta} \; \mathbb{E}_{x \sim \mathcal{D}, \, y \sim \pi_\theta} \big[ r_\phi(x, y) \big] - \beta \, \mathrm{KL}\big(\pi_\theta \,\|\, \pi_{\text{SFT}}\big)$$
- **第一項**：生成的回答得分越高越好；
- **第二項（KL 懲罰）**：**不要離 SFT 模型太遠**——防止
  「**獎勵駭客（reward hacking）**」（模型鑽評審的漏洞、生成評審愛但人類討厭的文字）；
- $\beta$：KL 的力度。

### 第二條線索：Bradley–Terry 的梯度
**對損失求導**：令 $d = r_{\text{chosen}} - r_{\text{rejected}}$、$p = \sigma(d)$：
$$\frac{\partial L}{\partial d} = \sigma(d) - 1 = p - 1$$
- **直覺**：若 $p \approx 1$（模型已把好答案排對）→ 梯度 $\approx 0$（不用再學）；
  若 $p \approx 0$（排錯了）→ 梯度 $\approx -1$（強力修正：**拉高 $r_{\text{chosen}}$、壓低 $r_{\text{rejected}}$**）；
- **這就是「從錯誤中學習」的數學形式**——與感知器（1958）、
  logistic 迴歸（1958，Cox）一脈相承：
  $$\text{感知器（1958）} \to \text{logistic（1958）} \to \text{Bradley–Terry（1952，Bradley \& Terry）} \to \text{RLHF（2022）}.$$
  （Bradley–Terry 原是 1952 年的**統計排序模型**——
  用於棋類、體育比賽的實力排名——**70 年後變成 AI 的獎勵函數**。）

### 第三條線索：PPO 的直覺
**強化學習的老問題**：策略梯度（policy gradient）一步跨太大，
策略崩壞，訓練爆炸。
**PPO（2017，Schulman）的解法**：**裁剪（clipping）**——
限制新舊策略的機率比在 $[1-\epsilon, 1+\epsilon]$ 內：
$$L^{\text{CLIP}}(\theta) = \mathbb{E} \Big[ \min\big( \rho(\theta) A, \; \mathrm{clip}(\rho(\theta), 1-\epsilon, 1+\epsilon) A \big) \Big], \quad \rho(\theta) = \frac{\pi_\theta(y \mid x)}{\pi_{\text{old}}(y \mid x)}$$
- $A$：優勢（advantage）——這個回答比「平均」好多少；
- **直覺**：好的更新**慢慢走**，壞的更新**不許走**——
  $$\text{一步千里（崩壞）} \xrightarrow{\text{PPO 裁剪}} \text{小步穩走（收斂）}.$$
- **在 RLHF 中**：PPO 讓語言模型在獎勵模型的引導下，
  **小步試探**「人類會喜歡什麼」——**試探而不失控**。

### Python：簡化版 Bradley-Terry 獎勵模型

```python
# 純 Python 實作：簡化版 Bradley-Terry 獎勵模型（成對偏好 + 梯度下降）
import math, random

random.seed(7)

# 候選答案（獎勵模型要學出每個答案的「人類偏好分數」）
answers = ["拒答", "幻覺瞎編", "籠統含糊", "條列清楚", "正確詳解"]
idx = {a: i for i, a in enumerate(answers)}
N = len(answers)

# 人類標註的成對偏好資料：(較好, 較差)
#   正確詳解 > 條列清楚 > 籠統含糊 > 幻覺瞎編 > 拒答
pairs = []
truth = ["正確詳解", "條列清楚", "籠統含糊", "幻覺瞎編", "拒答"]
for i in range(N):
    for j in range(i + 1, N):
        pairs.append((truth[i], truth[j]))
pairs = [(a, b) for (a, b) in pairs for _ in range(30)]  # 模擬 30 位標註員
print("Bradley-Terry 獎勵模型（成對偏好訓練）")
print(f"偏好資料筆數 = {len(pairs)}\n")

# 訓練：梯度下降最小化 L = -log sigma(r_chosen - r_rejected)
r = [0.0] * N
lr = 0.5
for epoch in range(300):
    grad = [0.0] * N
    loss = 0.0
    for chosen, rejected in pairs:
        d = r[idx[chosen]] - r[idx[rejected]]
        p = 1.0 / (1.0 + math.exp(-d))      # sigma(d)
        loss += -math.log(p)
        g = p - 1.0                          # dL/d(d) = sigma(d) - 1
        grad[idx[chosen]] += g
        grad[idx[rejected]] -= g
    for k in range(N):
        r[k] -= lr * grad[k] / len(pairs)
    if epoch in (0, 299):
        print(f"epoch {epoch:3d}: loss = {loss/len(pairs):.4f}")

print("\n學到的獎勵分數（排序，高 = 人類偏好）：")
for a, s in sorted(zip(answers, r), key=lambda t: -t[1]):
    print(f"  {a}：{s:+.3f}")

print("\n驗證：勝率 P(正確詳解 > 幻覺瞎編) = "
      f"{1/(1+math.exp(-(r[idx['正確詳解']]-r[idx['幻覺瞎編']]))):.4f}")
```
輸出：
```
Bradley-Terry 獎勵模型（成對偏好訓練）
偏好資料筆數 = 300

epoch   0: loss = 0.6931
epoch 299: loss = 0.0472

學到的獎勵分數（排序，高 = 人類偏好）：
  正確詳解：+4.396
  條列清楚：+2.036
  籠統含糊：-0.000
  幻覺瞎編：-2.036
  拒答：-4.396

驗證：勝率 P(正確詳解 > 幻覺瞎編) = 0.9984
```

## 結案 -- 後果與影響
- **產品的分水嶺（2022 年 11 月）**：
  $$\boxed{\text{ChatGPT：AI 第一次走入大眾}}$$
  **兩個月破 1 億使用者**（TikTok 用了 9 個月、Instagram 用了 2.5 年）——
  **1936 年圖靈問「機器能思考嗎？」**（見 `../資訊科學/1936-圖靈機.md`），
  86 年後，**數億人每天在跟機器對話**。
- **圖靈測試的回歸**：
  - **2023–2025 的研究**：GPT-4 在某些設定下的對話**騙過半數人類評審**——
    圖靈測試從思想實驗變成**實測項目**；
  - 圖靈當年問的是「機器**能**思考嗎」——
    ChatGPT 逼問的是「**分得出来嗎**」——
    $$\text{圖靈（1950）：機器能思考嗎？} \xrightarrow{\text{ChatGPT（2022）}} \text{你分得出来嗎？}$$
- **AI 助理時代（2023–）**：
  - **2023 GPT-4**（OpenAI）：多模態、專業考試**超越多數人類考生**；
  - **2023 開源浪潮**：**LLaMA**（Meta，2023 年 2 月）外洩後，
    **Alpaca、Vicuna** 等用 RLHF 微調的開源模型**遍地開花**——
    **ChatGPT 的配方公開了**；
  - **2023 Claude**（Anthropic）：** Constitutional AI**——
    用「原則」代替部分人類標註的對齊變體；
  - Copilot、寫作、翻譯、程式設計——**AI 助理成為基礎設施**。
- **新產業鏈（2022–）**：
  $$\text{算力（GPU）} + \text{資料（標註）} + \text{RLHF} = \text{AI 產業的三根支柱}$$
  - **標註產業**：RLHF 需要**大量人類偏好資料**——Kenya 的標註工人、
    Scale AI、Surge AI——**人類的判斷成為訓練資料**；
  - **提示詞工程**→**系統提示**→**代理（agent）**——
    與模型溝通成為新職業。
- **對齊與安全的未解案件**：
  $$\boxed{\text{獎勵駭客、幻覺、越獄、價值對齊——案件仍未結}}$$
  - **幻覺（hallucination）**：模型仍然**一本正經地胡說**——
    RLHF 壓低了頻率，但**沒有根除**（獎勵模型自己也會幻覺）；
  - **獎勵駭客（reward hacking）**：模型鑽評審漏洞——
    Goodhart 定律：「當一個指標變成目標，它就不再是好指標」；
  - **越獄（jailbreak）**：對齊可以被提示詞繞過——**防線與攻防持續**；
  - **價值對齊**：對齊「誰」的價值？標註員的？公司的？人類的？
    $$\text{RLHF（2022）：對齊的第一步} \xrightarrow{?} \text{可擴展監督（scalable oversight）——未解}.$$
- 歷史定位：**Ouyang 等人沒有發明新架構**——
  Transformer 是 2017 年的、GPT-3 是 2020 年的、PPO 是 2017 年的——
  他們把**三件舊事拼成一件新事**，然後**讓全人類看到了 AI**：
  $$\text{圖靈機（1936）} \xrightarrow{} \text{Transformer（2017）} \xrightarrow{} \text{GPT-3（2020）} \xrightarrow{} \text{ChatGPT（2022）}.$$
  **「預測下一個詞」+「人類的偏好」= 對話的機器**——
  **圖靈的問題，第一次有了大眾版的答案**。

## 關鍵人物與文獻
- **L. Ouyang 等 28 人**：*Training language models to follow instructions with human feedback*（2022）——InstructGPT、RLHF 三階段。
- **P. Christiano**：*Learning from Human Preferences*（2020）——成對偏好訓練獎勵模型。
- **J. Schulman**：PPO（2017）——裁剪的策略梯度。
- **R. Bradley & M. Terry**：Bradley–Terry 模型（1952）——排序的統計模型。
- **T. B. Brown 等 31 人**：GPT-3（2020）——ChatGPT 的能力基礎（見 `2020-布朗GPT-3.md`）。
- **A. Vaswani 等**：Transformer（2017）——骨架（見 `2017-瓦茲瓦尼Transformer.md`）。
- **S. Amodei / D. Amodei**：OpenAI 對齊團隊 → Anthropic（2021）、Constitutional AI（2023）。
- 相關案件：`2020-布朗GPT-3.md`、`2017-瓦茲瓦尼Transformer.md`、`../資訊科學/1936-圖靈機.md`。
