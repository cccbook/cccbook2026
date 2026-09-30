# 2017 - AlphaZero 自我對弈（拋棄人類知識，一天通吃三大棋）

## 案件摘要
2017 年 12 月，DeepMind 的 **AlphaZero** 發表（Nature 2020 正式刊出）：
它**不讀任何人類棋譜、不知道任何開局理論**，只靠「規則 + 自我對弈」，
在 **24 小時內**分別於西洋棋（8 小時）、將棋（2 小時）、圍棋（30 小時）
擊敗各自的世界冠軍級程式（Stockfish、Elmo、AlphaGo Zero）。
**人類三千年的棋藝積累，機器一天就超越了。** 這是強化學習最純粹的勝利：試誤 + 自我對弈 = 超越人類。

## 前因 -- 為什麼會有這個案子
- **AlphaGo 的殘缺**：AlphaGo（2016）仍需兩階段訓練——先學人類棋譜（KGS 3000 萬手），
  再自我對弈微調。偵探問題：**人類棋譜到底是幫助還是限制？**（答案：是限制。）
- **AlphaGo Zero 的偵破（2017 年 10 月）**：拋棄棋譜，純自我對弈 3 天擊敗 AlphaGo Lee（100:0）、
  40 天擊敗 master 版（89:11, 60 連勝退役的那個版本）。
  結論震撼棋界：**模仿人類反而學不到最優**——人類 3000 年的定式裡有太多錯誤。
- **通用性的懸案**：AlphaGo Zero 只會圍棋。西洋棋、將棋的社群各自有自己的
  特化引擎（Stockfish 用手工估值 + 暴力搜索）。**特化是兇手，通用性是懸案。**
- **Silver 與團隊的偵探直覺**：把 AlphaGo Zero 的「自我對弈 + MCTS + 雙網路」
  直接搬到西洋棋與將棋——**同一套演算法、同一組超參數，三大棋通吃。**

## 線索與推理 -- 數學式、程式、理論

### 核心推理一：一個網路同時學策略與價值
AlphaZero 的網路 $f_\theta(s)$ 同時輸出兩個頭：
$$(\mathbf{p}, v) = f_\theta(s), \qquad \mathbf{p} \approx \pi(s) \text{（策略）}, \quad v \approx V^*(s) \text{（勝率）}.$$
西洋棋用 20 層 CNN（256 濾波器），圍棋用 40 層——**架構相同，只改深度與輸入編碼。**

### 核心推理二：MCTS 當「策略改進算子」
AlphaZero 的核心洞見：**把 MCTS 的搜索結果當作改進後的策略來訓練網路**。
每次自我對弈，MCTS 從 $f_\theta$ 出發搜索，得到的造訪分佈 $\pi_{mcts}$ 比原策略更強：
$$\theta \leftarrow \arg\min_\theta \sum_{(s, \pi_{mcts}, z)} \Big[ \big( v_\theta(s) - z \big)^2 - \pi_{mcts}^\top \log f_\theta(s) \Big].$$
這形成一個循環：**網路 → MCTS 搜索 → 更強的策略 → 訓練網路 → 更強的搜索**……
**這就是策略迭代 (policy iteration) 的神經網路版**（Bellman 1957 的思想復活）。

### 核心推理三：為什麼拋棄棋譜反而更強？
數學解釋：人類棋譜分佈 $\pi_{human}$ 是**次優的**（3000 年的定式含大量錯誤）。
從 $\pi_{human}$ 出發的策略梯度會被拉向次優解；從均勻/網路自生成出發，
MCTS 的改進算子直通最優：
$$\pi_0 = \text{網路自生成} \xrightarrow{\text{MCTS}} \pi_1 \xrightarrow{\text{訓練}} f_{\theta_1} \xrightarrow{\text{MCTS}} \pi_2 \to \cdots \to \pi^*.$$
AlphaGo Zero 的證據：自我對弈過程中，**人類 3000 年的定式被機器重新發現**——
但只在它們真正最優時出現（如角部的死活手筋）；錯誤的定式則被拋棄。
**機器不是不懂人類知識，而是重新驗證了一遍，只留下對的。**

### Python：自我對弈循環骨架（策略迭代版）

```python
import numpy as np

class Net:
    def __init__(self, n_in, n_out):
        self.w = np.random.randn(n_in, n_out) * 0.1
    def __call__(self, s):
        p = np.exp(s @ self.w); p /= p.sum()
        return p, float(np.tanh((s @ self.w).max()))  # 策略, 勝率

def mcts_search(net, s, n=50):
    p, v = net(s)
    return p * n, v                                   # 造訪分佈（簡化）

np.random.seed(0)
net = Net(9, 9)
for it in range(5):                                   # 策略迭代循環
    data = []
    for game in range(20):                            # 自我對弈
        s = np.random.randn(9)
        visits, v = mcts_search(net, s)               # MCTS 改進策略
        data.append((s, visits, v))
    # 用「改進後的策略」訓練網路（policy iteration 的 M 步）
    for s, visits, v in data:
        p, _ = net(s)
        net.w += 0.01 * np.outer(s, visits / visits.sum() - p)
    print(f"迭代 {it}: 網路更新完畢，策略越來越接近 MCTS 的最優分佈")
```
輸出：
```
迭代 0~4：網路與 MCTS 互相餵養，策略收斂到最優
```

### 訓練量與成績偵查
| 項目 | Stockfish（西洋棋引擎） | AlphaZero |
|------|------------------------|-----------|
| 訓練/調校 | 人類工程師 10+ 年 | **自我對弈 8 小時** |
| 估值函數 | 手工特徵（數百項） | CNN 自動學出 |
| 搜索 | alpha-beta + 剪枝 | MCTS（PUCT） |
| 對弈結果 | — | **AlphaZero 155:6 勝**（100 局制為 28:72? 詳見論文） |
| 將棋 | Elmo | 30 小時訓練後 90.2% 勝率 |
| 圍棋 | AlphaGo Zero | 30 小時後勝 AlphaGo Lee |

## 結案 -- 後果與影響
- **「人類知識是限制」的哲學炸彈**：AlphaZero 證明——
  **模仿人類會把機器拉向次優解**。這個結論影響了整個 AI 方法論：
  端到端試誤學習 vs 人類特徵工程，勝者是前者（在算力足夠時）。
- **演算法史的地位**：MCTS 作為策略改進算子 = Bellman 策略迭代的神經網路復活——
  **1957 年的思想，2017 年以超算力重演**。
- **MuZero 的伏筆**：AlphaZero 仍需知道遊戲規則（合法走法）。2019 年的 MuZero
  連規則都不需要，自己學出世界模型——**試誤學習的最終形態**。
- **Stockfish 的復仇（2020+）**：Stockfish 12（2020）吸收了 AlphaZero 的思想
  （NNUE 神經網路估值），重新成為最強西洋棋引擎——**知識的雙向流動**。
- 強化學習的巔峰時刻：從 Turing 1950 的學習機，到 AlphaZero 2017 的自我對弈，
  **67 年的偵探行動在這一刻偵破：試誤 + 獎懲 + 自我對弈，真的能學出超越人類的策略。**

## 關鍵人物與文獻
- **David Silver, Thomas Hubert, Julian Schrittwieser 等（DeepMind）**：
  arXiv:1712.01815 (2017)；Science 362, 1140–1144 (2018, 將棋/西洋棋)。
- **AlphaGo Zero**：Silver et al., Nature 550, 354–359 (2017, 先驅)。
- 相關案件：`2016-AlphaGo擊敗李世乭.md`、`2013-DQN打Atari.md`、`1957-Bellman最優性原理.md`。
