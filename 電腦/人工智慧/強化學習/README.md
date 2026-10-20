# 強化學習：從 Gym 下棋到 LLM 推理

本書以「技術與理論的前因後果」為主軸，講述強化學習（Reinforcement Learning）從 1950 年代的試誤學習、1988 年 Sutton 的時序差分、2013 年的深度 Q 網路（DQN）與 OpenAI Gym，到 2016 年 AlphaGo 的自我對弈、2017 年 PPO，再到 2022 年 RLHF 對齊大語言模型、2024-2025 年 o1/DeepSeek-R1 用可驗證獎勵（RLVR）教模型「思考」，以及 2025-2026 年 RL、Agent 與世界模型的合流。全書貫穿三個問題：**當時遇到什麼問題、為何舊方法失效、新方法如何解決又引出什麼新問題**。數學（Bellman 方程、TD 誤差、策略梯度定理、GRPO）與程式碼（Gymnasium/PyTorch 可跑範例）並重，適合具備基礎機器學習知識的讀者。

* 第1章-強化學習導論：從試誤學習開始（1950-2026）
    * [1.1-試誤學習、Thorndike效果律與Sutton的起點（1950-1988）](01.1-試誤學習、Thorndike效果律與Sutton的起點（1950-1988）.md)
    * [1.2-強化學習與監督學習的本質差異及應用地圖](01.2-強化學習與監督學習的本質差異及應用地圖.md)
* 第2章-數學基礎：MDP 與動態規劃（1957）
    * [2.1-Markov決策過程：狀態、獎勵與策略（1957）](02.1-Markov決策過程：狀態、獎勵與策略（1957）.md)
    * [2.2-Bellman方程與價值迭代、策略迭代（1957）](02.2-Bellman方程與價值迭代、策略迭代（1957）.md)
* 第3章-無模型方法：TD 學習與 Q-Learning（1988-1989）
    * [3.1-蒙地卡羅與時序差分TDλ（1988）](03.1-蒙地卡羅與時序差分TDλ（1988）.md)
    * [3.2-Q-Learning（1989）與ε-greedy、表格方法的極限](03.2-Q-Learning（1989）與ε-greedy、表格方法的極限.md)
* 第4章-深度強化學習：DQN 與 OpenAI Gym（2013-2015）
    * [4.1-Gym環境與DQN：經驗回放、目標網路（2013-2015Atari）](04.1-Gym環境與DQN：經驗回放、目標網路（2013-2015Atari）.md)
    * [4.2-深度RL的不穩定性：DoubleDQN、Dueling、Rainbow（2015-2018）](04.2-深度RL的不穩定性：DoubleDQN、Dueling、Rainbow（2015-2018）.md)
* 第5章-策略梯度與 Actor-Critic（1999-2017）
    * [5.1-策略梯度定理、REINFORCE與Baseline（1999-2017）](05.1-策略梯度定理、REINFORCE與Baseline（1999-2017）.md)
    * [5.2-A2C與PPO：穩定訓練的工程學（2017）](05.2-A2C與PPO：穩定訓練的工程學（2017）.md)
* 第6章-博弈與自我對弈：從 TD-Gammon 到 AlphaGo（1992-2017）
    * [6.1-TD-Gammon（1992）與電腦下棋的漫長歷史](06.1-TD-Gammon（1992）與電腦下棋的漫長歷史.md)
    * [6.2-AlphaGo（2016）、MCTS與AlphaZero（2017）：自我對弈的勝利](06.2-AlphaGo（2016）、MCTS與AlphaZero（2017）：自我對弈的勝利.md)
* 第7章-模型基強化學習與世界模型（1989-2023）
    * [7.1-為何需要環境模型：Dyna（1991）與MPC](07.1-為何需要環境模型：Dyna（1991）與MPC.md)
    * [7.2-WorldModels（2018）與Dreamer系列（2019-2023）](07.2-WorldModels（2018）與Dreamer系列（2019-2023）.md)
* 第8章-強化學習馴服大語言模型：RLHF（2017-2024）
    * [8.1-從RL到人類偏好：PPO在LLM上的應用與RLHF三階段](08.1-從RL到人類偏好：PPO在LLM上的應用與RLHF三階段.md)
    * [8.2-InstructGPT（2022）、RLAIF與獎勵模型駭入問題](08.2-InstructGPT（2022）、RLAIF與獎勵模型駭入問題.md)
* 第9章-RL for Reasoning：推理模型與未來（2024-2026）
    * [9.1-OpenAIo1與DeepSeek-R1：用RL學會「思考」（2024-2025）](09.1-OpenAIo1與DeepSeek-R1：用RL學會「思考」（2024-2025）.md)
    * [9.2-強化學習與Agent、世界模型的合流（2025-2026）](09.2-強化學習與Agent、世界模型的合流（2025-2026）.md)
