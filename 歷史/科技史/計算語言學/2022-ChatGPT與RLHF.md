# 2022-ChatGPT與RLHF

## 案件摘要

2022 年 11 月 30 日，OpenAI 發布 ChatGPT：一個基於 GPT-3.5、以 RLHF（人類回饋強化學習）訓練的對話模型。它解開了一樁懸案：為什麼擁有驚人生成能力的 GPT-3「不聽話」——會有毒輸出、幻覺、無視指令。破案手法來自 Paul Christiano 等人 2017 年《Deep Reinforcement Learning from Human Preferences》奠定的偏好學習框架，以及 Ouyang 等人 2022 年 InstructGPT 論文把「指令跟隨」變成可規模化的訓練流程。本案把 LLM 從「能力展示」推向「可用產品」，也讓對齊（alignment）研究成為核心技術。

## 前因 -- 為什麼會有這個案子

- GPT-3 會寫、會譯、會編程，但它只是「下一詞預測器」：它模仿訓練語料的分佈，而不是優化「人類想要的回應」。毒性、偏見與幻覺是分佈的直接後果。
- 「下一詞預測」的訓練目標與「有用、無害、誠實」之間存在目標錯位：一個只學著續寫網路文本的模型，沒有理由聽從指令。
- 強化學習的工具已經成熟：PPO（Schulman 等人，2017）是穩定、好調的策略梯度演算法；OpenAI 的 alignment 團隊（Christiano 等，2017）已證明人類偏好可以訓練出有效的獎勵模型。
- OpenAI 的策略判斷：能力（capability）已經足夠，缺的是可用性（usability）。把「能力」轉成「聽話的助理」需要新的訓練範式——RLHF 就是答案。

## 線索與推理 -- 數學式、程式、理論

### RLHF 三階段訓練流程

第一條線索是 InstructGPT 的三階段配方，ChatGPT 正是其對話版：

1. **SFT（監督微調）**：人類標註員撰寫高品質示範回應，對預訓練模型做監督微調，得到初步「聽話」的策略 $\pi^{\text{SFT}}$。
2. **獎勵模型訓練**：標註員對模型的多個輸出做偏好排名，訓練獎勵模型 $r_\phi(x, y)$，讓人類偏好可被自動計算。
3. **PPO 強化學習**：以 $r_\phi$ 為獎勵，用 PPO 優化策略；同時加 KL 懲罰防止模型偏離原模型太遠（否則獎勵模型會被「攻破」）。

### Bradley-Terry 偏好模型

第二條線索：如何把「人類偏好排名」變成數學。Bradley-Terry 模型（1952）假設偏好由潛在分數（獎勵）決定：

$$
P(A \succ B \mid x) = \frac{e^{r_\phi(x, y_A)}}{e^{r_\phi(x, y_A)} + e^{r_\phi(x, y_B)}} = \sigma\left( r_\phi(x, y_A) - r_\phi(x, y_B) \right)
$$

獎勵模型的損失就是這個二元機率的負對數似然：

$$
L(\phi) = -\mathbb{E}_{(x, y_w \succ y_l)} \left[ \log \sigma\left( r_\phi(x, y_w) - r_\phi(x, y_l) \right) \right]
$$

注意：只有「獎勵差」可被觀測，獎勵的絕對值不可辨識——這是模型只能學到相對好壞的數學根源。

### PPO 目標函數與 KL 懲罰

第三條線索：強化學習階段的實際目標。純粹最大化 $r_\phi$ 會導致 reward hacking（模型鑽獎勵模型的漏洞，生成獎勵高但品質差的文本），因此加入對參考策略 $\pi^{\text{ref}}$（通常是 SFT 模型）的 KL 懲罰：

$$
\max_\theta \; \mathbb{E}_{y \sim \pi_\theta} \left[ r_\phi(x, y) \right] - \beta \, \mathrm{KL}\left( \pi_\theta(\cdot \mid x) \,\|\, \pi^{\text{ref}}(\cdot \mid x) \right)
$$

PPO 的 clip 式代理目標保證更新穩定：

$$
L^{\text{CLIP}}(\theta) = \mathbb{E} \left[ \min\left( \rho_t A_t, \; \mathrm{clip}(\rho_t, 1-\epsilon, 1+\epsilon) A_t \right) \right], \quad \rho_t = \frac{\pi_\theta(y_t \mid x, y_{<t})}{\pi^{\text{old}}(y_t \mid x, y_{<t})}
$$

$\beta$ 是對齊的鬆緊旋鈕：太大則模型退回原樣，太小則獎勵模型被攻破。

### DPO：跳過獎勵模型的捷徑

第四條線索由 Rafailov 等人（2023）指出：Bradley-Terry 的最優策略與獎勵之間有閉式解 $r(x,y) = \beta \log \frac{\pi(y|x)}{\pi^{\text{ref}}(y|x)} + \text{const}$，代入偏好損失後，獎勵模型可以被消去，直接對偏好資料做簡單的分類式損失：

$$
L_{\text{DPO}}(\theta) = -\mathbb{E}_{(x, y_w \succ y_l)} \left[ \log \sigma\left( \beta \log \frac{\pi_\theta(y_w|x)}{\pi^{\text{ref}}(y_w|x)} - \beta \log \frac{\pi_\theta(y_l|x)}{\pi^{\text{ref}}(y_l|x)} \right) \right]
$$

DPO 不是新理論，而是 RLHF 這條線索的代數重新偵辦：它證明三階段流程在數學上可以壓縮成一步，成為開源社群（Zephyr、Llama 的變體）的實務首選。

### 程式示範：Bradley-Terry 偏好模型與 PPO 式更新

以下 Python（numpy）實作「獎勵差 → 偏好機率」與簡化的 PPO clip 更新：

```python
import numpy as np

rng = np.random.default_rng(0)

# --- 1. Bradley-Terry：獎勵差 -> 偏好機率 ---
def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

def pref_prob(rA, rB):
    return sigmoid(rA - rB)

print("P(A>B) when rA-rB = 0.0 :", pref_prob(0.0, 0.0))   # 0.5（無偏好）
print("P(A>B) when rA-rB = 2.0 :", pref_prob(2.0, 0.0))   # ~0.88
print("P(A>B) when rA-rB = -1.0:", pref_prob(-1.0, 0.0))  # ~0.27

# --- 2. 從偏好排名學獎勵（梯度上升最大化對數似然） ---
r = np.zeros(4)  # 4 個候選回應的獎勵，真實偏好: 0 > 1 > 2 > 3
pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
for step in range(500):
    grad = np.zeros(4)
    for w, l in pairs:
        p = sigmoid(r[w] - r[l])
        grad[w] += 1 - p
        grad[l] -= 1 - p
    r += 0.1 * grad
print("learned rewards:", np.round(r, 3))  # 應單調遞減，反映偏好排名

# --- 3. 簡化 PPO clip 目標 ---
def ppo_clip_term(ratio, advantage, eps=0.2):
    unclipped = ratio * advantage
    clipped = np.clip(ratio, 1 - eps, 1 + eps) * advantage
    return np.minimum(unclipped, clipped)

for adv in (1.0, -1.0):
    ratios = np.array([0.5, 0.9, 1.0, 1.1, 1.5])
    terms = ppo_clip_term(ratios, adv)
    print(f"advantage={adv:+.0f}:", np.round(terms, 3))
# 觀察：ratio 偏離 1 太遠時被 clip，防止單次更新過大
```

## 結案 -- 後果與影響

- ChatGPT 兩個月破一億使用者，成為史上成長最快的消費級應用——RLHF 第一次讓「研究原型」直接變成大眾產品。
- NLP 從「每任務一個模型」轉向「一個通用助理」：任務模型、搜尋引擎、程式編輯器都被重新設計為對話介面。
- LLM 軍備競賽全面開打：Claude（Anthropic，2023，以 Constitutional Language Models 變體做對齊）、Gemini（Google，2023）、Llama（Meta，2023，開源，帶動 DPO 生態）。
- RLHF 成為對齊（alignment）研究的核心技術，獎勵模型、reward hacking、偏好資料品質成為獨立研究領域。
- 幻覺問題成為新戰場：RLHF 能讓模型「看起來誠實」，卻無法保證「真的正確」——這條懸案由 RAG 與多模態時代接手偵辦。

## 關鍵人物與文獻（條列，含真實文獻書目）

- Paul Christiano、Jan Leike、Tom Brown 等人：Deep Reinforcement Learning from Human Preferences. NeurIPS 2017（arXiv:1706.03741）。
- Long Ouyang、Jeff Wu、Ryan Lowe 等人（OpenAI）：Training language models to follow instructions with human feedback（InstructGPT）. NeurIPS 2022（arXiv:2203.02155）。
- John Schulman、Filip Wolski 等人：Proximal Policy Optimization Algorithms. arXiv:1707.06347, 2017。
- Ralph Rafailov、Archit Sharma 等人：Direct Preference Optimization: Your Language Model is Secretly a Reward Model. NeurIPS 2023（arXiv:2305.18290）。
- Ralph Allan Bradley 與 Milton E. Terry：Rank Analysis of Incomplete Block Designs, I. The Method of Paired Comparisons. Biometrika 39(3/4):324-345, 1952。
- OpenAI：ChatGPT: Optimizing Language Models for Dialogue. OpenAI Blog, 2022 年 11 月 30 日。
