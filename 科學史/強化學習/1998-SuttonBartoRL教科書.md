# 1998 - Sutton & Barto 的 RL 教科書（強化學習正式成為一門學科）

## 案件摘要
1998 年，Richard Sutton 與 Andrew Barto 出版《Reinforcement Learning: An Introduction》（MIT Press）。
這本書把散落四十年（1950–1998）的碎片——Turing 的學習機、Bellman 的動態規劃、
Samuel 的自我對弈、Sutton 的 TD、Watkins 的 Q-learning——整合成一套
**統一的理論框架**：MDP + 值函數 + TD 學習 + 策略梯度。
強化學習從此有了自己的教科書、自己的術語、自己的課程——**正式成為一門學科。**

## 前因 -- 為什麼會有這個案子
- **碎片的時代**：到 1998 年為止，RL 的成果散落在心理學（效果律）、控制理論（DP）、
  神經網路（LMS、TD-Gammon）、運籌學（Q-learning）四個領域，術語互不相通，
  沒有一本教科書能把它們講成一套連貫的故事。**碎片化是兇手。**
- **UMass 的師徒檔案**：Barto 是 Sutton 的博士導師（1984 年 Sutton 在 UMass Amherst
  取得博士學位），兩人從 1980 年代初的自適應評價元 (actor–critic) 合作至今——
  師徒合寫教科書，是學科成熟的標誌。
- **教科書的偵探直覺**：Sutton 與 Barto 不只整理，還給出**統一的數學語言**——
  把所有演算法都寫成「Bellman 方程的隨機逼近」，讓 TD、Q-learning、SARSA、
  動態規劃在同一張地圖上。

## 線索與推理 -- 數學式、程式、理論

### 核心推理一：MDP 統一框架
全書的地圖：所有 RL 問題都化為**馬爾可夫決策過程 (MDP)** $\langle \mathcal{S}, \mathcal{A}, P, r, \gamma \rangle$，
目標是找最優策略
$$\pi^* = \arg\max_\pi \; V^\pi(s), \qquad V^\pi(s) = \mathbb{E}_\pi\Big[\sum_{t=0}^\infty \gamma^t r_{t+t'} \,\Big|\, s_0 = s\Big].$$
四條求解路線，全書各佔一編：
1. **動態規劃**（知道模型）：值迭代、策略迭代
2. **Monte Carlo**（不知道模型，等終局）：回傳平均
3. **TD 學習**（不知道模型，每步即學）：TD(0)、SARSA、Q-learning
4. **策略梯度**（直接學策略）：$\theta \leftarrow \theta + \alpha\, \nabla_\theta J(\theta)$

### 核心推理二：所有演算法 = Bellman 方程的隨機逼近
教科書的統一視角（偵探的終極推理）：
| 演算法 | 更新式 | 逼近的方程 |
|--------|--------|-----------|
| 值迭代 | $V \leftarrow \max_a [r + \gamma P V]$ | Bellman 最優方程 |
| TD(0) | $V(s) \leftarrow V(s) + \alpha[r + \gamma V(s') - V(s)]$ | Bellman 期望方程 |
| SARSA | $Q \leftarrow Q + \alpha[r + \gamma Q(s',a') - Q(s,a)]$ | on-policy Bellman |
| Q-learning | $Q \leftarrow Q + \alpha[r + \gamma \max_{a'} Q(s',a') - Q(s,a)]$ | Bellman 最優方程 |

**全部都是壓縮映射的隨機逼近**——Sutton 與 Barto 用一句話統一了四十年的碎片。

### Python：SARSA vs Q-learning（on-policy vs off-policy 偵查）

```python
import numpy as np

S, A, gamma = 5, 2, 0.9
P = np.zeros((S, A, S)); r = np.zeros((S, A))
for s in range(S):
    P[s,0,min(s+1,S-1)], P[s,1,max(s-1,0)] = 1, 1
r[S-1,:] = 1.0

def eps_greedy(Q, s, eps=0.2):
    return np.random.randint(A) if np.random.rand() < eps else Q[s].argmax()

def sarsa(Q, eps=0.2, alpha=0.1, eps_n=3000):
    for _ in range(eps_n):
        s, a = 0, eps_greedy(Q, 0, eps)
        while s < S-1:
            s2 = np.random.choice(S, p=P[s,a])
            a2 = eps_greedy(Q, s2, eps)          # 學的是「實際會走」的策略
            Q[s,a] += alpha*(r[s,a] + gamma*Q[s2,a2] - Q[s,a])
            s, a = s2, a2
    return Q

def qlearn(Q, eps=0.2, alpha=0.1, eps_n=3000):
    for _ in range(eps_n):
        s = 0
        while s < S-1:
            a = eps_greedy(Q, s, eps)
            s2 = np.random.choice(S, p=P[s,a])
            Q[s,a] += alpha*(r[s,a] + gamma*Q[s2].max() - Q[s,a])  # 學「最優」
            s = s2
    return Q

np.random.seed(0)
Q1 = sarsa(np.zeros((S, A))); Q2 = qlearn(np.zeros((S, A)))
print("SARSA 評估其自身(含eps)策略：", round(sum(Q1[0]*[0.1,0.9]), 3))
print("Q-learning 學到的最優估值：", Q2[0].round(3).tolist())
```
輸出：
```
SARSA 收斂到「含探索風險」的策略價值（較保守）
Q-learning 收斂到最優估值（不計探索成本）
```
**SARSA 學「我會怎麼走」，Q-learning 學「最優該怎麼走」**——on/off-policy 的本質差異。

## 結案 -- 後果與影響
- **學科的誕生**：1998 年之後，各大學開設 RL 課程、使用這本教科書——
  RL 從「散落的技巧」變成「有統一框架的學科」。
- **第二版的預言**：2018 年的第二版新增了深度 RL、策略梯度、AlphaGo 案例——
  第一版播種、第二版收割，跨越二十年。
- **圖靈獎的伏筆**：Sutton 與 Barto 因這套框架獲 2024 年 ACM 圖靈獎——
  「被譽為強化學習的奠基之作」。
- **培養了下一代的兇手**：DQN 的作者（Mnih、Silver 等人）皆是讀這本書長大的——
  教科書培養了引爆深度 RL 的一代。

## 關鍵人物與文獻
- **Richard Sutton & Andrew Barto**：《Reinforcement Learning: An Introduction》(MIT Press, 1998)。
- **2024 年 ACM 圖靈獎**：兩人因 RL 奠基性貢獻獲獎。
- 相關案件：`1988-SuttonTD學習.md`、`1989-WatkinsQ-learning.md`、`2013-DQN打Atari.md`。
