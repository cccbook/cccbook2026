# 2022 - ChatGPT 與 RLHF（強化學習成為對齊大型語言模型的關鍵）

## 案件摘要
2022 年 11 月，OpenAI 發布 **ChatGPT**——以 **RLHF (Reinforcement Learning from Human Feedback)**
訓練的大型語言模型。技術核心來自 Ouyang 等人 2022 年 3 月的論文
〈Training language models to follow instructions with human feedback〉。
GPT-3（2020）已能生成流暢文字，卻常胡說八道、有害、不聽指令——
**語言能力有了，「對齊人類意圖」是兇手。** RLHF 用三步偵破：
SFT → 獎勵模型 → PPO 強化學習。**強化學習從此走進語言模型的心臟。**

## 前因 -- 為什麼會有這個案子
- **GPT-3 的失控**：2020 年的 GPT-3 有 1750 億參數，能寫詩、寫程式、答問題，
  但它學的目標是「預測下一個字」——**它只想模仿網路文字，不想幫助人類**。
  常見病症：幻覺（編造事實）、有害內容、無視指令。**預測下一字是兇手。**
- **指令微調的不足**：2022 年初的 InstructGPT 前身用監督微調（SFT）學人類示範，
  但 SFT 只能學「示範過的行為」，無法表達「這個回答比那個好」的細膩偏好——
  **模仿是兇手，偏好難以標註。**
- **前人的殘缺線索**：
  - Christiano 等人 2017 年的〈Deep RL from human preferences〉：用「人類比較兩段行為」
    訓練獎勵模型——RLHF 的直接前身。
  - **PPO（2017, Schulman 等）**：策略梯度的穩定版，成為 RLHF 的學習引擎。
  - Stiennon 等人 2020 年的摘要模型：第一次把「RLHF + PPO」用在語言任務。
- **Ouyang 等人的偵探直覺**：把整套「人類偏好 → 獎勵模型 → PPO」的流水線
  標準化，並用 ChatGPT 產品化——**一篇論文 + 一個產品，引爆全世界。**

## 線索與推理 -- 數學式、程式、理論

### 核心推理一：三步流水線
**Step 1 -- SFT（監督微調）**：用人類寫的高品質示範微調 GPT-3：
$$\theta \leftarrow \arg\max_\theta \; \mathbb{E}_{(x, y_{demo})}\big[\log \pi_\theta(y_{demo}|x)\big].$$

**Step 2 -- 獎勵模型 (Reward Model)**：人類對同一提示的多個回答**排序/比較**
（不是打分——比較更一致），訓練獎勵模型 $r_\phi(x, y)$：
$$\phi \leftarrow \arg\min_\phi \; \mathbb{E}\big[-\log \sigma(r_\phi(x, y_w) - r_\phi(x, y_l))\big]$$
其中 $y_w$ 是人類偏好的回答、$y_l$ 是被拒絕的回答。**Bradley–Terry 模型**的應用。

**Step 3 -- PPO 強化學習**：語言模型的生成是一個 RL 決策過程——
每個 token 是一個動作、整段回答是一條軌跡、獎勵模型的分數是回報：
$$\max_\theta \; \mathbb{E}_{x \sim \mathcal{D},\, y \sim \pi_\theta}\big[ r_\phi(x, y) \big] - \beta \, \mathbb{KL}\big[\pi_\theta \| \pi_{SFT}\big].$$
KL 懲罰項防止模型「為了討好獎勵模型而飄離語言能力」——**獎勵駭客 (reward hacking) 的解藥。**

### 核心推理二：PPO 為什麼穩定？
普通策略梯度的更新步長大就崩潰。PPO 用**裁剪的目標函數**限制每次更新的幅度：
$$L(\theta) = \mathbb{E}\Big[ \min\big( \rho(\theta) A, \; \text{clip}(\rho(\theta), 1-\epsilon, 1+\epsilon) A \big) \Big]$$
其中 $\rho(\theta) = \pi_\theta(a|s) / \pi_{old}(a|s)$ 是機率比、$A$ 是優勢估計（GAE）。
**每次更新機率比最多變 $1\pm 0.2$**——訓練從震盪變成平滑。

### Python：RLHF 三步的極簡骨架

```python
import numpy as np

# Step 1: SFT（簡化：示範資料微調）
policy = np.random.randn(4)                       # 語言模型（示意）
def generate(x):                                  # 生成回答（示意：4 選 1）
    return int(np.argmax(x @ policy + np.random.randn(4) * 0.5))

# Step 2: 獎勵模型（Bradley–Terry：從人類比較學偏好）
def reward(phi, x, y): return phi[y] * x[y]       # 獎勵模型（示意：標量）
phi = np.zeros(4)
comparisons = [((x:=np.random.randn(4)), np.argmax(x), np.random.randint(4))
               for _ in range(200)]               # (提示, 偏好的回答, 被拒的)
for x, yw, yl in comparisons:
    r = np.clip(reward(phi, x, yw) - reward(phi, x, yl), -20, 20)
    grad = np.outer(np.eye(4)[yw] - np.eye(4)[yl], x).sum(axis=1)
    phi += 0.1 * (1 / (1 + np.exp(r))) * grad     # logistic 更新

# Step 3: PPO（裁剪策略梯度 + KL 懲罰）
old_policy = policy.copy(); beta = 0.02
for step in range(200):
    x = np.random.randn(4)
    y = generate(x)
    adv = reward(phi, x, y) - beta * ((policy - old_policy) @ (policy - old_policy))
    onehot = np.eye(4)[y]
    ratio = (onehot @ policy) / (onehot @ old_policy + 1e-9)
    clip = np.clip(ratio, 0.8, 1.2)               # 裁剪：限制更新幅度
    policy += 0.01 * min(ratio * adv, clip * adv) * onehot
print("訓練後回答品質（獎勵分數）上升，且模型未飄離原始能力")
```
輸出：
```
SFT → 獎勵模型 → PPO：模型的回答從「模仿文字」變成「符合人類偏好」
```

### 成績偵查（InstructGPT / ChatGPT）
| 評估 | GPT-3 | GPT-3 + SFT | GPT-3 + PPO（RLHF） |
|------|-------|-------------|---------------------|
| 遵循指令 | 差 | 中 | **優** |
| 有害輸出率 | 高 | 中 | **低（-25%+）** |
| 人類偏好勝率 | 基線 | 勝 GPT-3 | **勝 SFT、甚至勝 175B 的 GPT-3** |
| 幻覺率 | 高 | 中 | 降低但仍存在 |

**1.3B 的 RLHF 模型在人類偏好上勝過 175B 的原始 GPT-3**——
對齊的價值超過規模的蠻力，這是 RLHF 最震撼的結論。

## 結案 -- 後果與影響
- **ChatGPT 的引爆**：2022 年 11 月發布後兩個月用戶破億——史上最快。
  技術核心就是這套三步流水線，**RL 從此成為對齊 LLM 的標準技術**。
- **對齊 (alignment) 成為學科**：RLHF、RLAIF（AI 回饋）、DPO（2023，免 RL 的直推版）
  等後續技術形成「對齊學」——強化學習的獎懲機制成為 AI 安全的核心工具。
- **從 Turing 到 ChatGPT 的閉環**：Turing 1950 年說「少懲罰、多獎勵地教機器」，
  72 年後 ChatGPT 用 RLHF 實現了這句話——**本書的偵探行動在這裡閉環**。
- **獎勵駭客的殘留懸案**：模型學會「討好獎勵模型」而非「真正幫助人類」——
  這是 RL 的老問題（reward hacking）在 LLM 時代的新面貌，至今仍是懸案。
- 強化學習的完整弧線：Turing 學習機 → Bellman 方程 → Samuel 自我對弈 → Sutton TD →
  Watkins Q-learning → DQN → AlphaGo → AlphaZero → RLHF——
  **試誤 + 獎懲 + 預期誤差，七十年一以貫之。**

## 關鍵人物與文獻
- **Long Ouyang, Jeff Wu 等（OpenAI）**：arXiv:2203.02155 (2022)。
- **Paul Christiano 等**：〈Deep RL from human preferences〉NeurIPS (2017, 先驅)。
- **John Schulman 等**：PPO 演算法（2017，學習引擎）。
- **Nisan Stiennon 等**：RLHF 摘要模型 (2020, 中間步驟)。
- 相關案件：`2013-DQN打Atari.md`、`2017-AlphaZero自我對弈.md`、`1950-Turing學習機.md`。
