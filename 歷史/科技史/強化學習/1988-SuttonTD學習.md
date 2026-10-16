# 1988 - Sutton TD 學習（時間差分：強化學習的心臟）

## 案件摘要
1988 年，Richard Sutton 在《Machine Learning》發表
〈Learning to Predict by the Methods of Temporal Differences〉——**TD 學習**。
他證明：預測一個緩慢顯現的結果，不必等到結果出現才學，
而可以在**每一步就用「預期的變化」來學**：
$$V(s_t) \leftarrow V(s_t) + \alpha \big[ r_{t+1} + \gamma V(s_{t+1}) - V(s_t) \big].$$
方括號裡的 $\delta = r + \gamma V(s') - V(s)$ 稱為 **TD 誤差**——它就是強化學習的心臟，
也是後來多巴胺研究的數學模型、DQN 與 AlphaGo 的學習引擎。

## 前因 -- 為什麼會有這個案子
- **監督式學習的困境**：預測「天氣明天下不下雨」可以等一天就拿到答案；
  但預測「這盤棋會不會贏」要等**幾百步之後**才知道。若每步都等最終結果（Monte Carlo 法），
  誤差大、樣本效率低、無法在線學習。**等待是兇手。**
- **前人的殘缺線索**：Samuel 1959 的「未來補償」、Klopf 1972 的「預期誤差」、
  Holland 1986 的 bucket brigade、Barto–Sutton–Anderson 1983 的
  自適應評價元 (actor–critic)——都是 TD 的碎片，但沒人把它們整合成一套理論。
- **Sutton 的偵探直覺**：1984 年的博士論文已提出 TD 思想，1988 年的論文把它變成
  **可證明收斂的正式演算法**，並指出它與動物學習（Klopf、Rescorla–Wagner 1972）
  及動態規劃（Bellman）的雙重血緣。

## 線索與推理 -- 數學式、程式、理論

### 核心推理：三種預測法的偵查對比
| 方法 | 更新時機 | 更新目標 | 偏差 | 變異數 |
|------|---------|---------|------|--------|
| Monte Carlo | 等到終局 | 實際回傳 $G_t = \sum_{k} \gamma^k r_{t+k}$ | 無偏 | 高（雜訊大） |
| 動態規劃 | 立即 | Bellman 算子（需知道模型） | — | — |
| **TD(0)** | **立即** | **$r + \gamma V(s')$（用估計代替模型）** | 有偏 | **低** |

TD 的更新目標 $r + \gamma V(s')$ 本身含估計值 $V(s')$（**bootstrap**），故有偏；
但每步都更新、只依賴一步轉移，變異數小、樣本效率高、**可以在線學習**。
$$\boxed{V(s_t) \leftarrow V(s_t) + \alpha\, \delta_t, \quad \delta_t = r_{t+1} + \gamma V(s_{t+1}) - V(s_t)}$$

### 收斂性偵查
Sutton 證明：線性函數近似 $V(s) = w^\top \phi(s)$ 下，若 $\sum \alpha_t = \infty$、$\sum \alpha_t^2 < \infty$，
則表格型 TD(0) 收斂到 $V$ 的最小均方解 $\Pi V^\pi$（投影到可表示空間）。
推廣 $TD(\lambda)$ 以指數衰減的資格跡 (eligibility trace) 混合所有步數：
$$V(s) \leftarrow V(s) + \alpha\, \delta_t\, e_t(s), \quad e_t(s) = \gamma\lambda\, e_{t-1}(s) + \mathbb{1}[s = s_t].$$

### Python：Monte Carlo vs TD(0) 樣本效率偵查

```python
import numpy as np

def random_walk(start=3, end=6):                 # 左端價值 0、右端價值 1
    s, states = start, [start]
    while 0 < s < end:
        s += np.random.choice([-1, 1]); states.append(s)
    return states

def mc_learn(V, alpha=0.1, episodes=100):
    for _ in range(episodes):
        states = random_walk()
        G = 1.0 if states[-1] == 6 else 0.0      # 等到終局才知道結果
        for s in states[:-1]: V[s] += alpha * (G - V[s])
    return V

def td_learn(V, alpha=0.1, episodes=100, gamma=1.0):
    for _ in range(episodes):
        states = random_walk()
        for t in range(len(states)-1):
            s, s2 = states[t], states[t+1]
            v_next = 1.0 if s2 == 6 else (V[s2] if s2 > 0 else 0.0)
            delta = gamma * v_next - V[s]        # 每步即學（TD 誤差）
            V[s] += alpha * delta
    return V

np.random.seed(0)
V = np.zeros(6)
mc_learn(V); print("MC 真值 [1/6..4/6]:", V[1:5].round(2))
V = np.zeros(6)
td_learn(V); print("TD 真值 [1/6..4/6]:", V[1:5].round(2))
```
輸出：
```
MC 真值 [1/6..4/6]: [0.19 0.42 0.74 0.89]
TD 真值 [1/6..4/6]: [0.12 0.28 0.41 0.73]
```
同樣 100 集，TD 的平均誤差約 0.06、MC 約 0.14（多 seed 驗證 TD 一致更接近解析解 [1/6, 2/6, 3/6, 4/6]）——**樣本效率的差距**。

### TD 誤差 = 多巴胺（後續偵查的橋）
Sutton 的 $\delta_t$ 與 Schultz 1990 年代的多巴胺放電模式完全吻合：
意外獎賞 → $\delta>0$ 放電；符合預期 → $\delta\approx 0$；預期落空 → $\delta<0$ 抑制。
**1972 年 Klopf 的假說 + 1988 年 Sutton 的數學 + 1997 年 Schultz 的實驗 = 完整偵破。**

## 結案 -- 後果與影響
- **強化學習的心臟**：之後所有主流演算法都是 TD 家族——
  Q-learning（1989）= TD 對 $Q$ 函數的 off-policy 版；
  DQN（2013）= TD + 深度網路 + 經驗回放；AlphaGo/AlphaZero = TD 思想的 MCTS 變體。
- **動物學習的數學化**：TD 模型成為解釋 Rescorla–Wagner、阻斷 (blocking) 等古典條件反射
  現象的標準框架，心理學與神經科學共用一套數學。
- **演算法史的地位**：Sutton 因此被稱為「強化學習之父」（2024 年圖靈獎得主，
  與 Barto 同獲）。**試誤 + 預期誤差 + bootstrap = RL 的完整公式。**

## 關鍵人物與文獻
- **Richard Sutton**：Machine Learning 3, 9–44 (1988)；博士論文 (1984, UMass)。
- **A. H. Klopf**：預期誤差假說（1972，先驅）；**Samuel**：未來補償（1959，先驅）。
- 相關案件：`1972-Klopf獎懲塑造.md`、`1989-WatkinsQ-learning.md`、`1992-TesauroTD-Gammon.md`。
