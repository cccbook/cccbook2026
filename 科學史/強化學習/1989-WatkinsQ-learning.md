# 1989 - Watkins Q-learning（無模型學習必收斂到 $Q^*$）

## 案件摘要
1989 年，Christopher Watkins 在劍橋大學的博士論文《Learning from Delayed Rewards》中提出
**Q-learning**，並證明其收斂性定理：
一個不知道轉移模型 $P, r$ 的 agent，只靠試誤與下列更新
$$Q(s,a) \leftarrow Q(s,a) + \alpha \big[ r + \gamma \max_{a'} Q(s',a') - Q(s,a) \big],$$
在適當條件下**必定收斂到最優動作價值函數 $Q^*$**。
這是強化學習史上最重要的定理之一——**無模型 + off-policy + 必收斂**，三大特性合體。

## 前因 -- 為什麼會有這個案子
- **TD 的 off-policy 懸案**：Sutton 1988 的 TD(0) 學習的是**當前策略** $\pi$ 的價值 $V^\pi$。
  但真正的目標是**最優策略** $\pi^*$ 的價值 $V^*$——怎麼在探索（試別的動作）的同時
  學最優策略？**探索與學習的矛盾是兇手。**
- **動態規劃的模型依賴**：Bellman 的值迭代需要知道 $P(s'|s,a)$，現實中（下棋、機器人）
  模型不可得。**模型是兇手。**
- **Watkins 的偵探直覺**：在 BP 資助的博士研究中（為了做自適應序列預測），
  他把 Bellman 方程的 $\max$ 算子直接搬進試誤更新——用 $\max_{a'} Q(s',a')$
  代替「當前策略的估值」，於是探索的動作不污染最優價值的學習。

## 線索與推理 -- 數學式、程式、理論

### 核心推理：off-policy 的數學魔術
關鍵：更新目標用的是 $\max_{a'} Q(s',a')$（**最優**的估值），而不是 $Q(s', \pi(s'))$（**當前**的估值）。
即使執行的動作 $a$ 是隨機探索選的（行為策略 $\mu \ne$ 目標策略 $\pi^*$），
更新仍朝 $Q^*$ 收斂——因為 Bellman 最優算子是壓縮映射（見 `1957-Bellman最優性原理.md`）：
$$TQ(s,a) = r + \gamma \max_{a'} Q(s',a'), \qquad \|TQ_1 - TQ_2\|_\infty \le \gamma\|Q_1 - Q_2\|_\infty.$$
Q-learning 是這個壓縮算子的**隨機逼近**。收斂定理（Watkins & Dayan 1992 補全證明）：
> 若每個 $(s,a)$ 被無限次造訪，且學習率 $\alpha_t$ 滿足 Robbins–Monro 條件
> $\sum_t \alpha_t = \infty, \sum_t \alpha_t^2 < \infty$，
> 則 $Q_t \to Q^*$ 以機率 1 收斂。

### 收斂偵查：探索必須夠多
Q-learning 本身不保證探索——需要 $\epsilon$-greedy 等策略保證每個 $(s,a)$ 無限造訪：
$$\pi(a|s) = \begin{cases} 1-\epsilon+\frac{\epsilon}{|\mathcal{A}|} & a = \arg\max Q(s,a)\\ \frac{\epsilon}{|\mathcal{A}|} & \text{其他}\end{cases}$$
若探索不足，Q 會卡在次優策略——**這是後來 DQN 過估 (overestimation) 問題的遠因。**

### Python：Q-learning 走迷宮（收斂到 $Q^*$ 偵查）

```python
import numpy as np

S, A, gamma = 4, 2, 0.9                          # 狀態 0~3，終點 = 3
P = np.zeros((S, A, S)); r = np.zeros((S, A))    # 真實模型（僅供驗證）
for s in range(S-1):
    P[s,0,s+1], P[s,1,max(s-1,0)] = 1, 1
    r[s,0], r[s,1] = (1.0 if s+1 == S-1 else 0.0), 0.0

# 解析解 Q*（值迭代，終點價值 = 0）
V_star = np.zeros(S)
for _ in range(200):
    V = (r + gamma * np.einsum('sak,k->sa', P, V_star)).max(axis=1)
    V_star = np.append(V[:S-1], 0.0)
Q_star = r + gamma * np.einsum('sak,k->sa', P, V_star)

np.random.seed(0)
Q = np.zeros((S, A))
for ep in range(3000):
    s = 0
    while s < S-1:
        a = np.random.randint(A) if np.random.rand() < 0.2 else Q[s].argmax()
        s2 = np.random.choice(S, p=P[s,a])
        Q[s,a] += 0.1 * (r[s,a] + gamma * Q[s2].max() - Q[s,a])  # Q-learning 更新
        s = s2
print("Q*       =", Q_star.round(3).tolist())
print("Q 學到的  =", Q.round(3).tolist())
print("最大誤差  =", f"{np.abs(Q[:S-1] - Q_star[:S-1]).max():.4f}")
```
輸出：
```
Q*       = [[0.81, 0.729], [0.9, 0.729], [1.0, 0.81], [0.0, 0.0]]
Q 學到的  = [[0.81, 0.729], [0.9, 0.729], [1.0, 0.81], [0.0, 0.0]]
最大誤差  = 0.0000
```
3000 局後誤差為 0——**隨機逼近確實收斂到 $Q^*$**，Watkins 定理驗證成功。

### Q-learning 家族樹
| 年份 | 演算法 | 改進點 |
|------|--------|--------|
| 1989 | Q-learning | 無模型 + off-policy + 收斂證明 |
| 1992 | Watkins & Dayan | 補全收斂性證明 |
| 2013/2015 | DQN | + 深度網路 + 經驗回放 + 目標網路 |
| 2015 | Double DQN | 解決 $\max$ 算子的過估偏差 |

## 結案 -- 後果與影響
- **無模型 RL 的基石**：Q-learning 證明「不需要模型也能學到最優」——
  這句話讓 RL 從控制理論的附庸變成獨立學科。
- **DQN 的直接祖先**：2013 年 DeepMind 的 DQN 就是「Q-learning + 深度網路」，
  Atari 革命（`2013-DQN打Atari.md`）完全建立在 Watkins 的更新規則上。
- **收斂定理的範本**：Watkins & Dayan 1992 的證明成為之後所有 RL 收斂性論文的範本
  （SARSA、Double Q、soft Q……）。
- 歷史花絮：Watkins 的論文原是 BP 資助的序列預測研究，Q-learning 最初被視為腳註，
  如今卻成為引用數萬次的經典——**配角變主角的經典翻案**。

## 關鍵人物與文獻
- **C. J. C. H. Watkins**：《Learning from Delayed Rewards》(PhD thesis, Cambridge, 1989)。
- **Watkins & Dayan**：Machine Learning 8, 279–292 (1992)。
- 相關案件：`1957-Bellman最優性原理.md`、`1988-SuttonTD學習.md`、`2013-DQN打Atari.md`。
