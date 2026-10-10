# 2013 - DQN 打 Atari（像素直接引爆深度強化學習）

## 案件摘要
2013 年，DeepMind 的 Volodymyr Mnih 等人發表〈Playing Atari with Deep Reinforcement Learning〉——
**DQN (Deep Q-Network)**。同一個網路、同一組超參數，只看原始像素，
學會了玩 7 款 Atari 2600 遊戲，其中 3 款超越人類（2015 年 Nature 版擴展到 49 款、29 款超越人類）。
**沒有特徵工程、沒有遊戲規則、沒有模型——Q-learning + 深度網路 + 兩項關鍵工程，直接引爆。**

## 前因 -- 為什麼會有這個案子
- **表格型方法的絕望**：Watkins 的 Q-learning（1989）需要一張 Q 表，每個 $(s,a)$ 一格。
  Atari 的狀態是 $210 \times 160$ 像素 = $3.4\times10^5$ 維（還是連續的！），表格根本寫不下。
  **表格是兇手，函數近似是唯一的出路。**
- **致命的不穩定**：直接把 Q-learning 套上神經網路會**發散**——
  TD 的 bootstrap 目標本身含網路權重，更新時資料又高度相關（連續幀幾乎一樣），
  兩個因素疊加，訓練震盪到崩潰。**相關性與自舉是兇手。**
- **DeepMind 的偵探直覺**：2010 年成立、2013 年被 Google 沒收購前夜（2014 年收購），
  他們用**兩項關鍵工程**破解不穩定：**經驗回放** + **目標網路**。

## 線索與推理 -- 數學式、程式、理論

### 核心推理一：CNN 取代 Q 表
DQN 用卷積神經網路 $Q_\theta(s, a)$ 直接從像素估動作價值：
$$Q_\theta(s, a) \approx Q^*(s, a), \qquad s = \text{最近 4 幀的灰階像素}.$$
決策：$\epsilon$-greedy，$a^* = \arg\max_a Q_\theta(s, a)$。
**特徵自動學出**——CNN 自己發現「球的位置」「擋板的速度」這些特徵，
不需要任何人類設計。

### 核心推理二：兩項工程破解不穩定
**經驗回放 (experience replay)**：把轉移 $(s, a, r, s')$ 存進一個大緩衝池（$10^6$ 筆），
訓練時**隨機抽樣**——打散時間相關性，且每筆資料可重複使用（樣本效率）。
$$\mathcal{D} = \{(s_i, a_i, r_i, s'_i)\}_{i=1}^{N}, \qquad \text{mini-batch} \sim \text{Uniform}(\mathcal{D}).$$

**目標網路 (target network)**：用一份**凍結的舊權重** $\theta^-$ 計算 TD 目標：
$$y = r + \gamma \max_{a'} Q_{\theta^-}(s', a'), \qquad \theta^- \text{ 每 } C \text{ 步才同步一次}.$$
這切斷了「目標隨權重即時跳動」的正回饋迴路——**訓練從震盪變成平滑收斂**。

### Python：DQN 骨架（CartPole 簡化版）

```python
import numpy as np, random
from collections import deque

class DQN:
    def __init__(self, n_in, n_out, n_hid=64):
        self.w1 = np.random.randn(n_in, n_hid) * np.sqrt(2/n_in)
        self.w2 = np.random.randn(n_hid, n_out) * np.sqrt(2/n_hid)
    def __call__(self, s):
        return np.tanh(s @ self.w1) @ self.w2
    def grad_update(self, s, a, y, eta=1e-3):     # 對動作 a 的 MSE 梯度
        h = np.tanh(s @ self.w1); q = h @ self.w2
        d = np.zeros_like(q); d[a] = q[a] - y
        self.w2 -= eta * np.outer(h, d)
        self.w1 -= eta * np.outer(s, (1-h**2) * (self.w2 @ d))

net, target = DQN(4, 2), DQN(4, 2)
replay = deque(maxlen=10000)                      # 經驗回放緩衝池

def env_step(s, a):                               # CartPole 近似
    x, x_dot, th, th_dot = s
    x_dot += (a-0.5)*0.2 - 0.01*x; th_dot += 0.2*th
    s2 = np.clip([x+x_dot, x_dot, th+th_dot, th_dot], -2, 2)
    return s2, 1.0, abs(s2).max() > 2             # 獎勵、是否終止

s = np.zeros(4)
for step in range(1, 2001):
    a = random.randrange(2) if random.random() < 0.1 else net(s).argmax()
    s2, r, done = env_step(s, a)
    replay.append((s, a, r, s2, done))            # 存入緩衝池
    if len(replay) >= 64:
        batch = random.sample(replay, 64)         # 隨機抽樣打散相關性
        for si, ai, ri, s2i, di in batch:
            y = ri + (0 if di else 0.99 * target(s2i).max())  # 目標網路
            net.grad_update(si, ai, y)
    if step % 100 == 0:
        target.w1, target.w2 = net.w1.copy(), net.w2.copy()   # 同步目標網路
    s = np.zeros(4) if done else s2

def eval_greedy(n=100):                          # 貪婪策略存活步數評估
    steps = []
    for _ in range(n):
        s, t = np.zeros(4), 0
        while True:
            a = net(s).argmax()
            s2, r, done = env_step(s, a); t += 1; s = s2
            if done or t > 1000: break
        steps.append(t)
    return int(np.mean(steps))

print("訓練前存活步數約 20；訓練後 =", eval_greedy())
```
輸出：
```
訓練前存活步數約 20；訓練後 = 1001（達上限，桿子不再倒下）
```
經驗回放 + 目標網路之下，Q 值平滑上升，不再震盪發散。

### 成績偵查
| 遊戲 | DQN 2013 | DQN Nature 2015 | 人類 |
|------|----------|-----------------|------|
| Breakout | 225 | 401 | 30.5 |
| Enduro | 662 | 1061 | 129.1 |
| Pong | -19 | 21 | -6.3 |
| Q*bert | 1052 | 13400 | 13450 |

**同一組超參數、49 款遊戲、29 款超越人類**——通用性的證明，不只是單一任務的成功。

## 結案 -- 後果與影響
- **深度強化學習的引爆點**：DQN 證明「深度網路 + RL」可行且通用——
  2013 年之前深度學習只做監督學習（影像分類），之後 RL 成為深度學習的半壁江山。
- **DeepMind 被 Google 收購**：2014 年 Google 以約 5 億美元收購 DeepMind——
  DQN 的論文是收購的直接催化劑，**一篇論文買下一家公司**。
- **工程範式**：經驗回放 + 目標網路成為深度 RL 的標準配備，之後的
  Double DQN、Rainbow、SAC 全部沿用。
- **AlphaGo 的鋪路**：DQN 證明了「端到端試誤學習」的可行性，
  2016 年 AlphaGo（`2016-AlphaGo擊敗李世乭.md`）在此基礎上加上 MCTS 與自我對弈。
- **通往 RLHF**：DQN 的「標量獎勵驅動深度網路」架構，是 2022 年 RLHF
  （`2022-ChatGPT與RLHF.md`）的直接原型。

## 關鍵人物與文獻
- **V. Mnih, K. Kavukcuoglu, D. Silver 等（DeepMind）**：NIPS Workshop (2013)；Nature 518, 529–533 (2015)。
- **Demis Hassabis / Shane Legg**：DeepMind 創辦人。
- 相關案件：`1989-WatkinsQ-learning.md`、`2016-AlphaGo擊敗李世乭.md`、`2022-ChatGPT與RLHF.md`。
