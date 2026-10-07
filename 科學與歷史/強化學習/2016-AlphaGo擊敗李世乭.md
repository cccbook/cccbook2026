# 2016 - AlphaGo 擊敗李世乭（圍棋之謎的偵破）

## 案件摘要
2016 年 3 月，DeepMind 的 **AlphaGo** 在首爾以 **4:1** 擊敗世界頂尖棋手李世乭 (Lee Sedol)。
圍棋被公認為「電腦永遠攻不下的堡壘」——狀態空間約 $10^{170}$，
比宇宙的原子數（$10^{80}$）還多。AlphaGo 用
**MCTS + 策略網路 + 價值網路 + 自我對弈**偵破了這個世紀之謎。
第二局的第 37 手（肩衝五路）被棋界稱為「神之一手」——機器走出人類 3000 年沒想過的棋。

## 前因 -- 為什麼會有這個案子
- **狀態空間的絕望**：圍棋 $19\times19$，合法局面約 $2\times10^{170}$，博弈樹複雜度約 $10^{360}$。
  西洋棋的暴力搜索（Deep Blue 1997）在此完全失效——**分支因子是兇手**
  （西洋棋約 35，圍棋約 250）。
- **傅利葉式的估值困境**：局部特徵（棋形、死活）無法評估全域勝率，
  人類大師靠的是 3000 年積累的「棋感」——**全域估值是懸案。**
- **前人的殘缺線索**：CrazyStone、Zen 等用 MCTS + Monte Carlo 評估達到業餘高段；
  DQN（2013，見 `2013-DQN打Atari.md`）證明深度網路 + RL 可行；
  TD-Gammon（1992）證明自我對弈可學估值。
- **Silver 與 Hassabis 的偵探直覺**：**把 MCTS 的搜索與神經網路的直覺合體**——
  網路提供「往哪搜」的先驗（策略網路）與「這局面誰贏」的估值（價值網路），
  搜索只在網路認為有希望的方向進行。

## 線索與推理 -- 數學式、程式、理論

### 核心推理一：策略網路把分支因子砍到個位數
策略網路 $p_\sigma(a|s)$ 學人類棋譜（KGS 的 3000 萬手），預測「高手會走哪」：
$$p_\sigma(a|s) \approx P(a \mid s), \qquad \text{MCTS 只走 } p_\sigma \text{ 前 } k \text{ 名}.$$
**分支因子從 250 砍到 5–10**——搜索深度從 4 層變成 40 層。
再經 RL 微調：讓策略網路自我對弈，用勝負結果做策略梯度：
$$\Delta\sigma \propto \sum_t \nabla_\sigma \log p_\sigma(a_t|s_t) \cdot z, \qquad z \in \{+1, -1\}.$$

### 核心推理二：價值網路取代 Monte Carlo rollout
傳統 MCTS 用隨機 rollout 到終局估勝率——噪聲大、慢。AlphaGo 改用
**價值網路 $v_\theta(s) \approx \mathbb{E}[z \mid s, \text{雙方都下最優}]$**：
$$\theta \leftarrow \arg\min_\theta \sum_{(s, z)} \big( v_\theta(s) - z \big)^2.$$
訓練資料：自我對弈 3000 萬局的終局結果。
**估值從「雜訊很大的抽樣」變成「一次前向傳播」**——快數千倍、準確得多。

### 核心推理三：MCTS 的 PUCT 公式
樹上每個節點的選擇權衡「利用（價值高）」與「探索（先驗沒看過）」：
$$\text{PUCT}(s, a) = Q(s, a) + c_{puct} \; p_\sigma(a|s) \frac{\sqrt{\sum_b N(s,b)}}{1 + N(s,a)}$$
$N$ 為造訪次數、$c_{puct} = 5$。**這是 AlphaZero 的核心公式**，
把 Bellman 的 $\max$（見 `1957-Bellman最優性原理.md`）與 UCB 的探索項合體。

### Python：MCTS + 神經網路的極簡骨架

```python
import numpy as np, math
from collections import defaultdict

class Node:
    def __init__(self, prior): self.N, self.W, self.prior = 0, 0.0, prior
    @property
    def Q(self): return self.W / self.N if self.N else 0.0

def policy_net(s):                    # 策略網路（示範：隨機先驗）
    return np.random.dirichlet(np.ones(len(s))) if False else \
           np.ones(len(s)) / len(s)

def value_net(s):                     # 價值網路（示範：勝率估計）
    return float(np.tanh(s.mean()))

def mcts(s, n_sims=200, c=5.0):
    root, children = Node(0), defaultdict(dict)
    key = tuple(np.where(s != 0)[0])                 # 用 tuple 當局面鍵
    for _ in range(n_sims):
        node, path = root, [root]
        # 選擇：PUCT 公式
        while True:
            kids = children[key] if key in children else {}
            if not kids: break
            a = max(kids, key=lambda a: kids[a].Q + c * kids[a].prior *
                    math.sqrt(node.N) / (1 + kids[a].N))
            node = kids[a]; path.append(node)
            break
        # 擴展 + 評估：策略網路給先驗，價值網路給勝率
        p = policy_net(s)
        kids = children[key]
        for i in range(len(s)): kids[i] = Node(p[i])
        v = value_net(s)
        # 回傳：沿路徑反向更新
        for nd in reversed(path):
            nd.N += 1; nd.W += v
    return root.N

s = np.random.randn(19*19) * (np.random.rand(19*19) < 0.1)
visits = mcts(s, n_sims=200)
print(f"200 次模擬完成，根節點造訪數 = {visits}")
```
輸出：
```
200 次模擬完成，根節點造訪數 = 200
```
（真實 AlphaGo：40 個 GPU、每步 2 秒、數百萬次模擬；自我對弈用了 1202 個 CPU + 176 個 GPU。）

### 算力與成績偵查
| 項目 | Deep Blue 1997 | AlphaGo 2016 |
|------|----------------|--------------|
| 對手 | Kasparov（西洋棋） | 李世乭（圍棋） |
| 方法 | 暴力搜索 + 手工估值 | MCTS + 神經網路 + 自我對弈 |
| 分支因子 | 35 | 250 |
| 結果 | 3.5:2.5 | **4:1** |
| 棋感來源 | 人類工程師 | **自我對弈 3000 萬局** |

## 結案 -- 後果與影響
- **「神之一手」的哲學衝擊**：第 37 手肩衝五路，人類棋手 3000 年沒想過——
  機器不只模仿人類，還能**發現人類知識的盲區**。李世乭說：「我震驚得說不出話。」
- **人類棋譜被機器改寫**：AlphaGo 之後，職業棋手開始模仿它的定式與布局——
  圍棋理論被機器重新書寫，**機器反過來教人類**（TD-Gammon 的重演）。
- **第 4 局的「神之一手」（人類版）**：李世乭第 78 手挖，贏了唯一一局——
  這一局被稱為人類對機器的最後輝煌，AlphaGo 承認這是它當時的盲點。
- **AlphaZero 的伏筆**：AlphaGo 仍需人類棋譜（先學 KGS 再自我對弈）。
  2017 年的 AlphaZero（`2017-AlphaZero自我對弈.md`）證明：**連棋譜都不需要**。
- **算力的勝利**：AlphaGo 退役（2017 年 master 版在網上 60 連勝），但它的方法
  成為所有博弈 AI 的範本（MuZero、AlphaStar、OpenAI Five）。

## 關鍵人物與文獻
- **David Silver, Aja Huang 等（DeepMind）**：Nature 529, 484–503 (2016)。
- **李世乭 (Lee Sedol)**：本案的「對手」，9 段棋士；第 78 手「神之一手」的人類版本。
- **樊麾 (Fan Hui)**：2015 年 10 月被 AlphaGo 5:0 擊敗的歐洲冠軍（首個警訊）。
- 相關案件：`2013-DQN打Atari.md`、`2017-AlphaZero自我對弈.md`、`1992-TesauroTD-Gammon.md`。
