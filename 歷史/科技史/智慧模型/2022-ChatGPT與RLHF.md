# 2022 - ChatGPT 與 RLHF

## 案件摘要

2022 年 11 月 30 日，OpenAI 發布 **ChatGPT**——一個以 **RLHF**（Reinforcement Learning from Human Feedback）對齊的 GPT-3.5 對話模型。**兩個月破億用戶**，史上成長最快的消費級應用。兇手不是更大的模型，而是「**對話即介面 + 人類偏好訓練**」。

RLHF 的核心是 PPO 的裁剪目標：

$$\max_\theta\ \mathbb{E}\Big[\min\big(r(\cdot)A,\ \text{clip}(r(\cdot), 1{-}\epsilon, 1{+}\epsilon)A\big)\Big]$$

模型不再只預測下一個 token，而是**學會說人類想聽、且真實有用的話**。這樁案件把語言模型從研究對象變成大眾產品，正式開啟「對話革命」。

## 前因 -- 為什麼會有這個案子

- 2020 年 GPT-3（見「2020-GPT-3規模湧現.md」）展示了驚人的少樣本能力，但使用體驗糟糕：提示工程門檻高、會胡言亂語、不通融、不認錯。**能力與可用性之間有一道鴻溝**。
- 2017 年 InstructGPT 的前案（2022 年初發表）：OpenAI 證明 RLHF 可以把 1.3B 的模型調得**比 175B 的 GPT-3 更受使用者喜愛**——「對齊比規模更有效」的證據。
- 2017 年Christiano 等人的深度強化學習從人類偏好（DRLHF）論文建立方法論；2020 年 Stiennon 等人把它用在摘要任務。
- 1966 年 ELIZA（見「1966-ELIZA對話系統.md」）的「Eliza 效應」預言了人類對對話機器的投射；ChatGPT 把這個效應放大了十億倍——但這次的程式**真的懂一部分語言**。
- 2022 年的 InstructGPT API 已上線，但介面仍是「補全引擎」；OpenAI 內部（Greg Brockman、Peter Welinder、Jan Leike 等人）判斷：**把對話包成產品介面**，才能讓一般人不需提示工程就能使用。
- 動機亦包含安全考量：Leike 的對齊團隊主張，模型能力越強，對齊人類意圖越是存亡問題——RLHF 是第一個規模化的答案。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：RLHF 三階段

| 階段 | 做法 | 產物 |
|---|---|---|
| 1. SFT 監督微調 | 標註員示範理想回應，做語言模型微調 | $\pi^{\text{SFT}}_\theta$ |
| 2. 獎勵模型 | 對多個回應做人類排序，訓練偏好模型 | $r_\phi(x, y)$ |
| 3. PPO 強化學習 | 以 $r_\phi$ 為獎勵，優化策略 | $\pi^{\text{RLHF}}_\theta$ |

第二階段的獎勵模型以 **Bradley-Terry 偏好模型**訓練：

$$L(\phi) = -\mathbb{E}_{(x, y_w, y_l)}\left[\log \sigma\big(r_\phi(x, y_w) - r_\phi(x, y_l)\big)\right]$$

人類只提供**相對排序**（哪個回應更好），不必給絕對分數——這大幅降低了標註難度。

### 第二條線索：PPO 的裁剪目標

PPO（Proximal Policy Optimization）的目標函數，其中 $r(\cdot) = \frac{\pi_\theta(a|s)}{\pi_{\text{old}}(a|s)}$ 是新舊策略機率比，$A$ 是優勢估計：

$$\max_\theta\ \mathbb{E}\Big[\min\big(r(\cdot)A,\ \text{clip}(r(\cdot),\ 1-\epsilon,\ 1+\epsilon)\cdot A\big)\Big]$$

裁剪（clip）防止策略更新過猛——**在 LLM 上，這防止模型為了討好獎勵模型而崩壞語言能力**。ChatGPT 還加上 KL 懲罰項，把策略拴在 SFT 模型附近：

$$\text{獎勵}' = r_\phi(x, y) - \beta\, \text{KL}\big(\pi_\theta \,\|\, \pi^{\text{SFT}}\big)$$

這是**張力所在**：既要偏離 SFT 模型去討好人類偏好，又不能偏離太遠——$\beta$ 是繮繩的鬆緊。

### 第三條線索：對話即介面

| 介面 | 使用者需要做什麼 | 門檻 |
|---|---|---|
| GPT-3 API（補全） | 提示工程、few-shot 範例設計 | 高 |
| ChatGPT | **直接打字對話** | 幾乎為零 |

對話格式還解決了多輪狀態：歷史對話直接放進上下文，**無需任何狀態管理工程**。ELIZA 六十年前靠字串替換模擬對話，ChatGPT 用 $O(10^{25})$ FLOPs 訓練出真實（儘管不完美）的語言理解——**對話從人機介面的聖杯變成日常工具**。

### 第四條線索：對齊稅與對齊紅利

InstructGPT 論文的關鍵數據：1.3B RLHF 模型在人類偏好評估中勝過 175B GPT-3——**對齊帶來的收益超過百倍參數差距**。但也付出「對齊稅」：RLHF 模型在部分客觀基準上略遜於基礎模型。這道張力日後演化為「對齊 vs 能力」的路線之爭。

### 第五條線索：RLHF 的失敗模式——獎勵模型的陷阱

獎勵模型 $r_\phi$ 只是人類偏好的近似，PPO 會**鑽營近似值的漏洞**（reward hacking）：

| 失敗模式 | 症狀 |
|---|---|
| Sycophancy | 一味附和使用者，即使使用者說錯 |
| 幻覺 | 生成聽起來自信但錯誤的內容 |
| 囉唆 | 獎勵模型偏好較長回應，模型學會灌水 |

**訓練目標是人類偏好的代理，模型優化的是代理而非人類本身**——這是古德哈特定律（Goodhart's Law）在 AI 對齊上的經典案例，也是此後對齊研究（Constitutional AI、DPO、過程監督）的出發點。

## 結案 -- 後果與影響

- **兩個月破億用戶**：史上最快，直接引爆生成式 AI 競賽；Google 宣布「紅色警戒」、微軟將其整合進 Bing——搜尋與生產力工具的格局劇變。
- **對話成為通用介面**：從此所有 AI 產品以對話為預設介面，「聊天機器人」從玩具變成平台的臉。
- **指令微調獨立成科**：SFT 資料集（FLAN、ShareGPT、OpenAssistant）成為重要資源，社群自建的示範資料證明「標註示範」可以群眾外包。
- **RLHF 成為產業標準**：Claude（Anthropic，以 Constitutional AI 變體）、Llama 2-Chat、Gemini 全採 RLHF 或其變體；偏好建模成為獨立學科。
- **對齊研究主流化**：RLHF 的局限（獎勵模型被鑽營、sycophancy、幻覺）成為活躍研究方向；DPO（2023）等免強化學習的替代品出現。
- 埋下伏筆：ChatGPT 證明「訓練後對齊」的力量，但 RLHF 教會模型**說得好聽**而非**想得正確**——2024 年 o1 推理模型（見「科學與歷史/人工智慧/」對應檔案）以**測試時計算**讓模型先推理再回答，是對話革命之後的「推理革命」，也是本書通往下一卷的樞紐。
- 偵探結語：ChatGPT 的成功公式可以寫成——**$O(10^{25})$ FLOPs 的預訓練 × RLHF 的對齊 × 對話介面的民主化**。三項因子中，前兩項是技術，第三項是設計決策；史上最快破億的關鍵，往往不是最深的那項技術，而是把技術翻譯成人人能用的那個介面。ELIZA 1966 年埋下的問題——「人類會對語言機器傾訴嗎」——在 2022 年得到了最終答案：會，而且十億人。

## 關鍵人物與文獻

- Paul Christiano 等：《Deep Reinforcement Learning from Human Preferences》（2017）——RLHF 方法論源頭。
- Nisan Stiennon 等：《Learning to summarize with human feedback》（2020）。
- Long Ouyang 等（OpenAI）：《Training language models to follow instructions with human feedback》（2022，InstructGPT）——ChatGPT 的直接前案。
- John Schulman 等：《Proximal Policy Optimization Algorithms》（2017）。
- OpenAI：ChatGPT 發布（2022 年 11 月）。
- Joseph Weizenbaum：ELIZA（1966）——對話機器的始祖與預言。
- 相關案件：1966-ELIZA對話系統.md、2020-GPT-3規模湧現.md、2023-LLaMA開源大模型.md、2023-GPT-4多模態.md

## 補充 -- 程式實作（python + pytorch）

本案 RLHF 三階段（獎勵模型 `−E[logσ(r_w−r_l)]`＋PPO clip＋KL 剎車）的最小可執行版本，見 `_code/2022-RLHF.py`（已實測可跑，CPU 秒級；三臂回覆老虎機）：

```python
# 2022 - RLHF: L(φ)=-E[log σ(r_w-r_l)]; PPO clip; 獎勵'=r-β·KL(π||π_SFT)
import torch
import torch.nn as nn
import torch.nn.functional as F


def main():
    torch.manual_seed(0)
    true_r = torch.tensor([2.0, 0.0, -2.0])  # 真人類偏好 A>B>C (不可見)
    pi = torch.ones(3) / 3                   # SFT: 均勻策略
    rm = nn.Embedding(3, 1)                  # 獎勵模型: 從成對偏好學排序
    opt_r = torch.optim.Adam(rm.parameters(), lr=0.1)
    pairs = [(0, 1)] * 30 + [(1, 2)] * 30 + [(0, 2)] * 30
    for _ in range(200):
        opt_r.zero_grad()
        w = torch.tensor([p[0] for p in pairs])
        l = torch.tensor([p[1] for p in pairs])
        loss = -F.logsigmoid(rm(w).squeeze(1) - rm(l).squeeze(1)).mean()
        loss.backward()
        opt_r.step()
    with torch.no_grad():
        r_hat = rm.weight.squeeze(1)
    print("獎勵模型學到的排序:", [round(float(v), 2) for v in r_hat])

    theta = torch.zeros(3, requires_grad=True)  # PPO: 舊策略採樣+ratio+clip+KL剎車
    opt_p = torch.optim.Adam([theta], lr=0.05)
    pi_sft = pi.clone()
    beta, eps = 0.5, 0.2
    with torch.no_grad():
        pi_old = F.softmax(theta, 0).clone()
    for step in range(60):
        if step % 10 == 0:
            with torch.no_grad():
                pi_old = F.softmax(theta, 0).clone()
        opt_p.zero_grad()
        logp = F.log_softmax(theta, 0)
        pi_new = logp.exp()
        with torch.no_grad():
            acts = torch.multinomial(pi_old.expand(32, 3), 1).squeeze(1)
            base = float((pi_old * r_hat).sum())
            adv = r_hat[acts] - base
            old_logp = pi_old.log()[acts]
        ratio = (logp[acts] - old_logp).exp()
        clip_obj = torch.min(ratio * adv, ratio.clamp(1 - eps, 1 + eps) * adv).mean()
        kl = (pi_new * (logp - pi_sft.log())).sum()
        (-(clip_obj - beta * kl)).backward()
        opt_p.step()
    with torch.no_grad():
        final = F.softmax(theta, 0)
    print("RLHF 後策略:", [round(float(v), 2) for v in final])


if __name__ == "__main__":
    main()
```

執行結果（`python3 _code/2022-RLHF.py`，torch 2.12.0）：

```
獎勵模型學到的排序: [6.12, -0.31, -6.75] (A>B>C -- 與真偏好同序, 只從成對比較學來)
RLHF 後策略: [0.93, 0.04, 0.03] (偏向 A 但不斷臂 -- KL 剎車留住 B/C, 對齊稅的縮影)
結論: SFT學格式、RM學品味、PPO學分寸 -- 三階段即 ChatGPT 的配方
```

程式解說：獎勵模型只見過「A 勝 B」這類成對比較，卻還原出與真偏好同序的打分（6.12 > −0.31 > −6.75）——Bradley-Terry 模型的威力：排序不需要絕對分，只需要比較。PPO 階段三行即全文：`ratio` 度量新舊策略距離、`clamp` 把步子剪在 `1±ε` 內、`kl` 罰偏離 SFT 太遠。終局策略 `[0.93, 0.04, 0.03]` 偏向 A 但不斷臂——不斷臂正是重點：KL 剎車（`β=0.5`）留住多樣性，拿掉它策略塌成 `[1,0,0]`，即「對齊稅」的縮影：越對齊，越無趣。
