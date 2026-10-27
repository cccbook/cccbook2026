# 2024 Andrew Barto & Richard Sutton —— 強化學習的兩位奠基者

> 「沒有老師、沒有標籤，只有獎勵與懲罰——機器如何學會
> 下棋、走迷宮、開車？兩位學者用四十年回答：**試錯 +
> 價值函數 + 一條貝爾曼方程**。」

## 案件檔案

| 項目 | 內容 |
|---|---|
| 得主 | Andrew G. Barto (1948–)、Richard S. Sutton (1957–) |
| 得獎理由 | 強化學習的開創性貢獻 |
| 關鍵詞 | TD 學習、策略梯度、Q-learning、MCTS+RL |

## 前因

1980s，監督學習（有標籤）與符號 AI（有規則）之外的
第三條路無人問津。行為心理學的「操作制約」（Skinner）、
最優控制的**動態規劃**（Bellman 1950s）、以及 Minsky
式學習機——三股線索等待匯流。Barto 與 Sutton 在
UMass Amherst 的實驗室接下了這個「無人區」。

## 線索與推理

### 線索一：馬可夫決策過程（MDP）的形式化

```
環境：(S, A, P, R, γ)
  P(s'|s,a) 轉移機率；R(s,a) 獎勵；γ ∈ (0,1) 折扣
目標：找策略 π 使期望累積獎勵最大
  V^π(s) = E[Σ γ^t · r_t]
貝爾曼方程（一切的方程式）：
  V^π(s) = Σ_a π(a|s) Σ_s' P(s'|s,a)[R + γ V^π(s')]
最優性：V*(s) = max_a Σ_s' P(s'|s,a)[R + γ V*(s')]
```

**價值 = 自身 + 折扣的未來**——遞迴結構使學習可以
「邊走邊算」。

### 線索二：TD 學習（Sutton, 1988）

突破：**不必等整回合結束才學**——時序差分：

```
V(s) ← V(s) + α[ r + γV(s') − V(s) ]
                    ↑ TD 誤差：預測差的差
 animal psychology 呼應：獎勵預測誤差（dopamine 假說，
  Schultz 1997：多巴胺神經元編碼的正是 TD 誤差！）
```

**演算法與神經科學在 1997 年互認**——AI 史上最動人
的跨學科會師。

### 線索三：Q-learning 與策略梯度（1989 Watkins / 1999 Sutton）

```
Q-learning（off-policy）：
  Q(s,a) ← Q(s,a) + α[r + γ max_a' Q(s',a') − Q(s,a)]
  收斂定理：充分探索下收斂到最優 Q*（隨機逼近理論）
REINFORCE / 策略梯度（Sutton 1999, Williams 1992）：
  ∇J(θ) = E[Σ ∇log π_θ(a|s) · Q(s,a)]
  ——直接對策略求導，連續動作空間的鑰匙
```

教科書《Reinforcement Learning: An Introduction》
（1998/2018 兩版）成為領域聖經。

### 線索四：2010s–2020s 的大爆發

```
2013/2015 DQN（DeepMind, Mnih 等）：Q-learning + CNN → ATARI
2016 AlphaGo：MCTS + 策略/價值網 + 自我對弈 → 勝李世石
2017 AlphaZero：純自我對弈（無人類棋譜）
2022–23 RLHF：強化學習對齊大型語言模型（GPT/ChatGPT）
  ——RL 從遊戲走進生成式 AI 的核心工序
```

Sutton 的《The Bitter Lesson》（2019）成為時代宣言：
**通用方法（靠算力的搜尋與學習）終將勝過人類知識
注入**——六十年方法論之戰的總結。

## 理論評析

強化學習的偵探學：**在沒有「正確答案」的世界裡定義
進步**。

```
監督學習：答案由老師給 → 模仿
無監督：無答案 → 結構
強化學習：答案延遲、稀疏、且由行動造成 → 信用分配問題
  （credit assignment）是本質難點：n 步前的決定如何
  為此刻的失敗負責？TD 誤差 = 逐層回溯的解法
```

與 1975 Newell–Simon 案的對照：符號派靠「問題空間」，
RL 派靠「獎勵信號」——兩派在 2020s 的 LLM 訓練中
合流（預訓練=模仿，RLHF=獎勵）。

## 後果

- 機器人控制、自動駕駛決策、晶片佈局（AlphaChip）、
  核聚變電漿控制。
- RLHF 使語言模型可用——**本案是 ChatGPT 時代的
  直接理論前置**。
- Barto/Sutton 獲獎時（2025 公布 2024 獎）皆強調：
  這是四十年的長期主義勝利。

## 關聯案件

→ [1975-Newell-Simon](1975-Newell-Simon.md)、[2018-Bengio-Hinton-LeCun](2018-Bengio-Hinton-LeCun.md)、[2010-Leslie-Valiant](2010-Leslie-Valiant.md)
