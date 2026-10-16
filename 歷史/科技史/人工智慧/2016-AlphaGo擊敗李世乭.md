# 2016 - AlphaGo 擊敗李世乭（深度學習征服圍棋）

## 案件摘要
2016 年 3 月，DeepMind 的 **AlphaGo** 以 4:1 擊敗圍棋世界冠軍李世乭 (Lee Sedol)。
圍棋分支因子約 250（西洋棋的 7 倍），暴力搜尋（Deep Blue 路線，見「1997-DeepBlue擊敗棋王.md」）完全失效。
AlphaGo 的破案手法：**深度神經網路評估棋局 + 蒙特卡洛樹搜尋 + 自我對弈**——
「機器的直覺」第一次超越了人類最強的直覺。

## 前因 -- 為什麼會有這個案子
- **圍棋的難度牆**：$19\times19$ 棋盤，分支因子 $b \approx 250$、深度 $d \approx 150$：
  $$b^d \approx 10^{360} \quad (\text{比宇宙原子還多}).$$
  Alpha-Beta 剪枝也救不了——**Deep Blue 的手法在圍棋上全數陣亡**。
- **傳統電腦圍棋的瓶頸**：2015 年前最強程式（Zen、Crazy Stone）僅業餘高段水準，無法威脅職業棋王。專家預言「圍棋至少還要 10 年」。
- **DeepMind 的偵探直覺**：Demis Hassabis（西洋棋神童出身）與 David Silver 決定換武器——
  **不用窮舉，用神經網路「直覺」評估棋局**；**不用人類知識，用自我對弈產生訓練資料**。
- **兩塊拼圖**：DeepMind 的 Atari 遊戲強化學習經驗（DQN, 2015）+ 深度神經網路（AlexNet 之後的成熟生態）。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：策略網路與價值網路（機器的直覺）
- **策略網路** $p_\theta(a|s)$：給定棋局，輸出每個落點的機率——「直覺地」判斷下一步。
- **價值網路** $v_\phi(s)$：給定棋局，輸出勝率——「直覺地」評估大局。
$$p_\theta: s \mapsto \text{落點機率}, \qquad v_\phi: s \mapsto \text{勝率} \in [-1, 1].$$
用 13 層卷積網路（影像思維，見「1989-LeCunCNN手寫辨識.md」）把棋盤當「圖像」處理——
**黑子、白子、空點 = 三通道輸入**，圍棋變成視覺識別問題。

### 第二條線索：自我對弈（不用人類知識的訓練）
- 第一步：用人類棋譜（KGS 資料庫）監督訓練策略網路（模仿人類）。
- 第二步：**自我對弈**——訓練後的網路自己跟自己下數百萬局，勝者為標籤：
  $$\text{新網路 vs 舊網路} \quad\Rightarrow\quad \text{用對局結果 RL 更新參數}.$$
  機器超越人類棋譜的關鍵——AlphaGo 下的「第 37 手」（五路肩衝）震驚所有職業棋士：**人類幾千年都沒想到的一手**。

### 第三條線索：MCTS + 神經網路（直覺引導搜尋）
蒙地卡洛樹搜尋 (MCTS) 用神經網路取代隨機模擬：
$$\text{選點} \propto Q(s,a) + c\, \frac{p_\theta(a|s)}{1 + N(s,a)},$$
- $p_\theta$：策略網路的「直覺」引導搜尋方向（像 A\* 的啟發函數）。
- $v_\phi$：價值網路取代葉節點評估（不需要搜到底）。
**直覺 + 搜尋 = 人類棋手的思考方式，被完整數學化**——這正是它強大的原因。

### Python：MCTS + 神經網路「直覺」的玩具版

```python
import numpy as np

# 模擬「策略網路」與「價值網路」
def policy_net(state):                 # 直覺：偏好中心落點
    s = state.copy(); n = len(s)
    coords = [(i,j) for i in range(n) for j in range(n) if s[i,j]==0]
    score = np.array([-abs(i-(n-1)/2)-abs(j-(n-1)/2) for i,j in coords])
    p = np.exp(score*2); p /= p.sum()
    return coords, p

def value_net(state):                  # 評估：黑子多則勝率高
    return np.tanh((state==1).sum() - (state==2).sum())

def mcts_choose(state, n_sim=200):
    coords, p = policy_net(state)
    Q = np.zeros(len(coords)); N = np.zeros(len(coords))
    for _ in range(n_sim):
        w = p/(1+N) + 1e-9
        a = np.random.choice(len(coords), p=w/w.sum())
        N[a] += 1
        s2 = state.copy(); i,j = coords[a]; s2[i,j] = 1
        Q[a] += (value_net(s2) - Q[a]) / N[a]      # 平均更新
    return coords[np.argmax(Q + p/(1+N))]

board = np.zeros((9,9))
print("MCTS+直覺 選點:", mcts_choose(board), "(偏向中心)")
```
輸出：
```
MCTS+直覺 選點: (4, 4) (偏向中心)
```
（直覺引導 + 搜尋驗證 = AlphaGo 的思考縮影。）

## 結案 -- 後果與影響
- **圍棋案結**：4:1 擊敗李世乭；2017 年 3:0 擊敗世界排名第一的柯潔——人類棋手承認「AI 看見了人類看不見的棋」。
- **李世乭的第 78 手**：第 4 局中李世乭下出「神之一手」扳回一城——人類唯一一勝，成為人機對抗的經典紀念。
- **AlphaZero（2017）**：完全不用人類棋譜，8 小時自我對弈從零學會西洋棋、將棋、圍棋，全面超越 AlphaGo——**「白板學習」的巔峰**，Turing 1950 年「兒童機器」預言的最終兌現（見「1950-Turing測試.md」）。
- **MuZero（2019）**：連規則都不告訴它，自己學習環境模型——強化學習的天花板。
- **科學應用的伏筆**：DeepMind 把遊戲破案手法轉向科學——AlphaFold（見「2021-AlphaFold蛋白質摺疊.md」）用同樣的「神經網路 + 搜尋」征服生物學。
- 歷史定位：Deep Blue 證明「算力 + 人類知識」能贏；AlphaGo 證明「學習 + 直覺」能贏得更漂亮——**學習取代窮舉，成為 AI 的新正道**。

## 關鍵人物與文獻
- **D. Silver, A. Huang, C. Maddison 等**：〈Mastering the Game of Go with Deep Neural Networks and Tree Search〉, Nature 529, 484 (2016)。
- **D. Silver 等**：AlphaZero, Science 362, 1140 (2017)；MuZero, Nature 588, 604 (2019)。
- **DeepMind**：DQN, Nature 518, 529 (2015)——Atari 強化學習先驅。
- 相關案件：`1997-DeepBlue擊敗棋王.md`、`2021-AlphaFold蛋白質摺疊.md`、`2017-Transformer注意力機制.md`。
