# 2016 - AlphaGo

## 案件摘要
2016 年 3 月，DeepMind 的 **AlphaGo** 在首爾以 **4:1** 擊敗圍棋世界冠軍李世乭（Lee Sedol）。圍棋有 $10^{170}$ 量級的合法局面，暴力搜尋（1997-DeepBlue擊敗棋王.md 的路線）在此徹底失效。AlphaGo 的解法是三網一體：**策略網路（policy net）+ 價值網路（value net）+ 蒙特卡洛樹搜尋（MCTS）**。其訓練主幹是策略梯度：

$$
\nabla_\theta J = \mathbb{E}\big[\nabla_\theta \log p_\theta(a \mid s)\, R\big]
$$

價值網路則用回歸逼近 $v_\theta(s) \approx \mathbb{E}[\text{win} \mid s]$。這樁案件的偵探意義：深藍靠 $2\times10^8$ 步/秒的暴力，AlphaGo 靠 $10^3$ 步/秒的**直覺 + 評估**——機器第一次展現了被稱為「棋感」的東西。

## 前因 -- 為什麼會有這個案子
- **圍棋的不可搜尋性**：西洋棋 branching factor ~35，深藍硬搜可解；圍棋 branching factor ~250，且形勢判斷（厚薄、地盤）難以用手工評估函數刻畫——1997-DeepBlue擊敗棋王.md 之後，圍棋成為「AI 的聖杯」，人類冠軍宣稱機器至少還要十年。
- **傳統圍棋程式的天花板**：1990–2015 年，最強的圍棋程式（CrazyStone、Zen）用 MCTS + 手工模式，業餘高段水平，從未贏過職業頂尖。
- **DeepMind 的賭注**：2013-DQN打Atari.md 用同一個神經網路 + Q-learning 玩遍 49 款 Atari 遊戲，證明了深度強化學習的通用性；Demis Hassabis（前職業西洋棋童星）從創業起就宣稱目標是解決「一般智能」，圍棋是必經的試煉。
- **策略梯度的遺產**：REINFORCE（1992）與 2013-DQN打Atari.md 提供了兩條 RL 路線——策略梯度與價值學習；AlphaGo 把兩者**合流**。
- **資料線索**：KGS 圍棋伺服器的 3000 萬步人類棋譜——模仿人類直覺的教材。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：策略網路——模仿人類的直覺
用 13 層 CNN（2012-AlexNet影像革命.md 的捲積配方）在 3000 萬步人類棋譜上做監督學習，輸入是棋盤特徵平面（己方/對方棋子、氣、徵子等 48 個平面），輸出每個位置的落子機率：

$$
p_\sigma(a \mid s) = \mathrm{softmax}\big(\mathrm{CNN}_\sigma(s)\big)
$$

監督策略網路在保留測試上預測人類落子的準確率達 57%——這是「棋感」的第一個數值化身。再用**策略梯度自我對弈**微調（RL 版）：

$$
\nabla_\theta J = \sum_t \nabla_\theta \log p_\theta(a_t \mid s_t)\, (z_t - v(s_t)), \quad z_t = \text{最終勝負}(\pm 1)
$$

自我對弈的 RL 策略網路在人類棋譜預測上只有 41%（開始偏離人類），但**對戰勝率更高**——它學的是贏，不是像人。

### 第二條線索：價值網路——評估整個局面
MCTS 的葉節點需要形勢評估。傳統方法用快棋模擬（rollout），AlphaGo 訓練一個獨立的價值網路直接回歸：

$$
v_\theta(s) \approx \mathbb{E}\big[\text{win} \mid s\big], \qquad \mathcal{L}(\theta) = (z - v_\theta(s))^2
$$

訓練資料是 3000 萬個**自我對弈**局面（只用同一策略自我對弈的資料——混入人類棋譜會過擬合）。價值網路的評估與真實勝率的 MSE 僅 0.226，與一次完整 rollout 相當，但**快 15000 倍**。這是「用神經網路取代手工評估函數」的決定性一擊——1997-DeepBlue擊敗棋王.md 的手工評估在此被謀殺。

### 第三條線索：MCTS——三網一體的搜尋樹
AlphaGo 在比賽時把三個網路塞進蒙特卡洛樹搜尋：

| MCTS 階段 | 運算 | 使用的網路 |
|---|---|---|
| 選擇（Selection） | $a^* = \arg\max_a \big(Q(s,a) + u(s,a)\big)$，$u \propto p_\sigma(a\mid s)/N(s,a)$ | 策略網路（先驗） |
| 擴展（Expansion） | 葉節點展開，算先驗機率 | 策略網路 |
| 評估（Evaluation） | $v_\theta(s)$ 與 rollout 混合 | 價值網路 + 快速策略 |
| 回傳（Backup） | $N \mathrel{+}= 1$，$Q \mathrel{+}= \frac{1}{n}(v - Q)$ | — |

搜索量：單機 40 個 CPU + 8 GPU 約 $10^3$ 步/秒（分佈式版 $10^4$），對深藍的 $2\times10^8$——**少了五個數量級，卻贏了五個子**。搜尋不再是暴力，而是「直覺引導的深度思考」。

訓練的三階段管線也值得記錄：先在 KGS 人類棋譜上做監督學習（SL policy net）→ 用自我對弈做策略梯度強化（RL policy net）→ 用自我對弈局面做價值回歸（value net）。三個網路共用 CNN 架構但獨立訓練——2017-AlphaZero自我對弈.md 之後會把三網合一，拋棄人類棋譜與 rollout。

### 第四條線索：第 37 手——超越人類的證據
第二局第 37 手，AlphaGo 於第五路落子（人類絕不會下的位置，人類頂尖選手的估計勝率僅萬分之一）。李世乭愣了十七分鐘；解說的職業棋士起初都認為是失誤。最終 AlphaGo 以 4:1 獲勝（第四局李世乭以「神之一手」第 78 手扳回一城——人類尊嚴的最後一勝）。第 37 手證明了：**機器不只是在模仿人類，它發現了人類棋譜之外的下法**。

勝率的數學語言：AlphaGo 內部對每個候選手維護兩個量——平均勝率 $Q(s,a)$ 與探索加成 $u(s,a)$：

$$
a^* = \arg\max_a \left(Q(s,a) + \frac{c_p\, p_\sigma(a \mid s)}{1 + N(s,a)}\right)
$$

第 37 手的先驗 $p_\sigma$ 極低（策略網路認為人類不會下），但價值網路的評估 $v_\theta$ 與 MCTS 的深入分析發現其真實勝率極高——**當價值網路推翻了人類直覺，新時代的棋理就此誕生**。

## 結案 -- 後果與影響
- **圍棋易主**：2016 年後，人類棋手全面跟隨 AI 的開局理論（點三三、外靠等 AI 定式成為主流）；2017 年 AlphaGo 以 3:0 擊敗柯潔後退役，人類與頂尖 AI 的差距已被公認不可逆。
- **AlphaGo Zero（2017）**：拋棄人類棋譜，從零自我對弈 40 天即超越所有舊版——證明了「自我對弈 + 規模化」的威力，詳見 2017-AlphaZero自我對弈.md。
- **深度強化學習的爆發**：策略梯度 + 價值網路的組合成為標配（A3C、PPO）；強化學習（科學與歷史/強化學習/）從玩具問題進入主戰場。
- **超越棋盤**：DeepMind 的後續案件——AlphaZero（西洋棋、將棋）、AlphaStar（星海爭霸）、AlphaFold 蛋白質摺疊（2021-AlphaFold蛋白質摺疊.md）——把「直覺+評估+搜尋」的配方推向科學。
- **伏筆**：AlphaGo 證明了 RL + 深度網路 + 規模化的三重奏；同樣的三重奏在 2022-ChatGPT與RLHF.md 中以人類回饋的形式重現——從學會下棋到學會對話，強化學習成為對齊人類意圖的關鍵工具，見「科學與歷史/人工智慧/」的對齊智能相關檔案。

## 關鍵人物與文獻
- **David Silver**：AlphaGo 第一作者，強化學習大家，Sutton 的學生。
- **Aja Huang**：業餘六段棋手，AlphaGo 工程核心，代為落子的人機介面。
- **Demis Hassabis**：DeepMind 創辦人，圍棋西洋棋雙料背景的執棋者。
- **李世乭（Lee Sedol）**：十四冠世界冠軍，被擊敗的對照組。
- **樊麾（Fan Hui）**：歐洲圍棋冠軍，2015 年 5:0 被擊敗，是最早的人類對照組。
- Silver et al., *Mastering the Game of Go with Deep Neural Networks and Tree Search*, Nature, 2016.
- Silver et al., *Mastering the Game of Go without Human Knowledge (AlphaGo Zero)*, Nature, 2017.
- Mnih et al., *Human-level Control through Deep Reinforcement Learning (DQN)*, Nature, 2015.
- 相關案件：2013-DQN打Atari.md、1997-DeepBlue擊敗棋王.md、2012-AlexNet影像革命.md、2017-AlphaZero自我對弈.md、2021-AlphaFold蛋白質摺疊.md、2022-ChatGPT與RLHF.md

### 附錄線索：五局棋的偵探年表
2016 年 3 月 9–15 日首爾四季酒店的五局對弈，每局都是一條線索：

| 局 | 勝者 | 關鍵手 | 偵探意義 |
|---|---|---|---|
| 第 1 局 | AlphaGo | 白 186 扳 | 人類首次不敵，李世乭自認一時失誤 |
| 第 2 局 | AlphaGo | 白 37（第五路） | 「AI 的手」現身，震動棋界 |
| 第 3 局 | AlphaGo | 白 78 跨 | 連下三城，勝負已定 |
| 第 4 局 | **李世乭** | 白 78「神之一手」（挖） | 觸發 AlphaGo 的致命誤判——人類尊嚴之勝 |
| 第 5 局 | AlphaGo | 黑 161 | 終局 4:1，時代易主 |

第四局暴露了 MCTS 混合評估的弱點：第 78 手挖是「兩步之後才顯現威力」的陷阱手，rollout 的淺層模擬與價值網路的統計評估都低估了它——機器的「棋感」仍有盲區。這條線索證明：AlphaGo 不是全知，它是在「直覺引導下搜尋」的機器，而直覺本身可以被欺騙。樊麾（2015 年 5:0 被擊敗的歐洲冠軍）事後的觀察最有偵探味：「我看它的棋，越看越像活的。」

## 補充 -- 程式實作（python + numpy）

本案 MCTS＋UCT（`UCT = Q + c√(lnN(s)/N(s,a))`）的最小可執行版本，見 `_code/2016-AlphaGo.py`（已實測可跑；以井字棋代替圍棋，rollout 以純隨機代替策略網路）：

```python
# 2016 - AlphaGo: 策略直覺 + MCTS 搜尋 (井字棋縮影)
import numpy as np

LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
         (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]


def winner(b):
    for a, c, d in LINES:
        if b[a] != 0 and b[a] == b[c] == b[d]:
            return b[a]
    return 0 if 0 in b else 3  # 3=和棋


def legal(b):
    return [i for i, v in enumerate(b) if v == 0]


def mcts_move(board, player, sims=300, c=1.4, seed=0):
    """以 player 視角做 MCTS: Q+UCT 選子, 隨機 rollout 評估."""
    rng = np.random.default_rng(seed)
    N = {a: 0 for a in legal(board)}
    W = {a: 0.0 for a in legal(board)}
    tot = 0
    for _ in range(sims):
        untried = [a for a in N if N[a] == 0]
        a = rng.choice(untried) if untried else max(
            N, key=lambda m: W[m] / N[m] + c * np.sqrt(np.log(tot) / N[m]))
        b2 = board.copy()
        b2[a] = player
        turn = 3 - player
        while winner(b2) == 0:  # rollout: 隨機下完 (淺層模擬的極簡版)
            b2[rng.choice(legal(b2))] = turn
            turn = 3 - turn
        w = winner(b2)
        r = 1.0 if w == player else (0.5 if w == 3 else 0.0)
        N[a] += 1
        W[a] += r
        tot += 1
    return max(N, key=lambda m: W[m] / N[m])


def play(mcts_first=True, seed=0):
    rng = np.random.default_rng(seed)
    b = np.zeros(9, dtype=int)
    turn, go_first = 1, mcts_first
    while winner(b) == 0:
        if go_first:
            b[mcts_move(b, turn, seed=rng.integers(1e9))] = turn
        else:
            b[rng.choice(legal(b))] = turn
        turn, go_first = 3 - turn, not go_first
    return winner(b)


def main():
    mcts_wins = draws = rand_wins = 0
    for i in range(40):  # MCTS 先後手各 20 局
        w = play(mcts_first=(i % 2 == 0), seed=i)
        mcts_side = 1 if i % 2 == 0 else 2
        if w == 3:
            draws += 1
        elif w == mcts_side:
            mcts_wins += 1
        else:
            rand_wins += 1
    print(f"MCTS(300次模擬) vs 隨機走子 40局: 勝={mcts_wins} 和={draws} 負={rand_wins}")
    print("結論: 搜尋即直覺的放大器 -- AlphaGo 把 rollout 換成策略/價值網路, 把井字棋換成圍棋")


if __name__ == "__main__":
    main()
```

執行結果（`python3 _code/2016-AlphaGo.py`，numpy 2.4.5）：

```
MCTS(300次模擬) vs 隨機走子 40局: 勝=36 和=4 負=0
結論: 搜尋即直覺的放大器 -- AlphaGo 把 rollout 換成策略/價值網路, 把井字棋換成圍棋
```

程式解說：`mcts_move` 即 AlphaGo 搜尋心的最小骨架——UCT 的前項 `W/N` 是利用（走勝率高的子）、後項 `c√(lnN/N_a)` 是探索（沒試過的子加分），兩者相加即「直覺引導下搜尋」。36 勝 4 和 0 負說明：即使 rollout 是純隨機（AlphaGo 用策略網路 rollout＋價值網路評估，比這強得多），搜尋本身已是巨大的放大器。把井字棋換成圍棋、隨機 rollout 換成策略／價值網路、300 次換成上萬次——骨架不變，規模改寫結局；第 37 步肩衝、78 手挖，都是這同一個迴圈跑出來的。
