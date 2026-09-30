# 強化學習史 -- AI 偵探風格

以「推理探案」的方式，追查強化學習（Reinforcement Learning）從圖靈的學習機之謎到 ChatGPT 的 RLHF 對齊術的每一步：
前因是什麼？線索在哪裡？推理如何展開？後果又如何改變了整個人工智慧、控制理論與數位世界？
核心謎題只有一個：**一個只靠「試誤 + 獎懲」的 agent，真的能學出超越人類的策略嗎？**

## 案件卷宗（歷史年表）

### 前奏：學習機與控制的啟蒙（1950–1957）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1950 | Turing 發表《Computing Machinery and Intelligence》，主張「孩童式學習機」：機器可以像小孩一樣被教導、靠獎懲學習 | [1950-Turing學習機.md](1950-Turing學習機.md) |
| 1953 | Bellman 在 RAND 發明動態規劃與 Bellman 方程，把「多期決策」化為遞迴 | [1953-Bellman動態規劃.md](1953-Bellman動態規劃.md) |
| 1957 | Bellman 出版《Dynamic Programming》，最優性原理與 $V^*, Q^*$ 正式問世；同一年 Skiner 的《Verbal Behavior》與 Rommetveit 的隨機學習理論並行，心理學的增強（reinforcement）概念流入工程 | [1957-Bellman最優性原理.md](1957-Bellman最優性原理.md) |

### 案發與試誤：會下棋、會配線的機器（1959–1962）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1959 | Samuel 寫出西洋跳棋自學程式：自我對弈 + 評價函數 + 未來補償，機器首次「自己變強」 | [1959-Samuel跳棋自學程式.md](1959-Samuel跳棋自學程式.md) |
| 1960 | Widrow 與 Hoff 發表 ADALINE 與 LMS 最小均方演算法，神經元開始會「按獎懲調整權重」 | [1960-WidrowHoff-LMS最小均方.md](1960-WidrowHoff-LMS最小均方.md) |
| 1961 | Michie 用火柴盒造出 MENACE 井字棋學習機：沒有電腦，只靠「加分珠子」學會永不輸棋 | [1961-MichieMENACE井字棋.md](1961-MichieMENACE井字棋.md) |

### 從心理學到數學：TD 學習的誕生（1972–1989）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1972 | Klopf 提出神經元的「獎懲性異質塑造」，動物心理學的 TD 思想流入 AI | [1972-Klopf獎懲塑造.md](1972-Klopf獎懲塑造.md) |
| 1988 | Sutton 發表〈Learning to Predict by the Methods of Temporal Differences〉：$V(s) \leftarrow V(s) + \alpha[r + \gamma V(s') - V(s)]$，TD 誤差成為學習的引擎 | [1988-SuttonTD學習.md](1988-SuttonTD學習.md) |
| 1989 | Watkins 博士論文提出 Q-learning，證明在適當條件下無模型學習必收斂到 $Q^*$ | [1989-WatkinsQ-learning.md](1989-WatkinsQ-learning.md) |

### 數位革命：神經網路遇上 RL（1992–1998）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1992 | Tesauro 的 TD-Gammon 只靠自我對弈學會西洋雙陸棋，達到人類大師級水準 | [1992-TesauroTD-Gammon.md](1992-TesauroTD-Gammon.md) |
| 1998 | Sutton 與 Barto 出版《Reinforcement Learning: An Introduction》，強化學習正式成為一門學科 | [1998-SuttonBartoRL教科書.md](1998-SuttonBartoRL教科書.md) |

### 深度強化學習：從 Atari 到棋盤世界（2013–2017）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 2013 | DeepMind 的 DQN 直接看像素玩 Atari 遊戲，經驗回放 + 目標網路引爆深度 RL | [2013-DQN打Atari.md](2013-DQN打Atari.md) |
| 2016 | AlphaGo 以 4:1 擊敗李世乭，MCTS + 深度網路 + 自我對弈破解圍棋之謎 | [2016-AlphaGo擊敗李世乭.md](2016-AlphaGo擊敗李世乭.md) |
| 2017 | AlphaZero 拋棄人類棋譜，自我對弈一天內通吃西洋棋、將棋、圍棋 | [2017-AlphaZero自我對弈.md](2017-AlphaZero自我對弈.md) |

### 對齊術：RL 走進語言模型（2022）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 2022 | OpenAI 以 RLHF（人類回饋強化學習）訓練 ChatGPT，強化學習成為對齊大型語言模型的關鍵技術 | [2022-ChatGPT與RLHF.md](2022-ChatGPT與RLHF.md) |

## 關鍵人物年表

| 年代 | 人物 | 貢獻 |
|------|------|------|
| 1950 | Alan Turing | 學習機、機器智慧 |
| 1953/1957 | Richard Bellman | 動態規劃、Bellman 方程、最優性原理 |
| 1959 | Arthur Samuel | 跳棋自學程式、自我對弈 |
| 1960 | Bernard Widrow / Ted Hoff | ADALINE、LMS 最小均方 |
| 1961 | Donald Michie | MENACE 火柴盒學習機 |
| 1972 | A. Harry Klopf | 獎懲性異質塑造、TD 思想 |
| 1988 | Richard Sutton | 時間差分（TD）學習 |
| 1989 | Christopher Watkins | Q-learning 及收斂性證明 |
| 1992 | Gerald Tesauro | TD-Gammon |
| 1998 | Richard Sutton / Andrew Barto | 《Reinforcement Learning: An Introduction》 |
| 2013 | DeepMind（Mnih 等） | DQN 深度 Q 網路 |
| 2016/2017 | DeepMind（Silver 等） | AlphaGo、AlphaZero |
| 2022 | OpenAI（Ouyang 等） | RLHF 與 ChatGPT |
