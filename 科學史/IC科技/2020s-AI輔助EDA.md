# 2020s — AI 輔助 EDA：當演算法學會畫晶片

## 案件摘要
2020 年前後，晶片設計自動化（EDA）遇上瓶頸：佈局繞線的組合爆炸與模擬時間動輒數週。Google（2021, Nature）、Synopsys DSO.ai、Cadence Cerebrus 先後用強化學習（RL）破解 floorplanning 難題，之後 LLM 更進場生成 RTL，EDA 進入 AI 時代。

## 前因 -- 為什麼會有這個案子
- 晶片設計流程中，**placement（佈局）** 要把數百萬至數十億個元件放到有限的版圖上，本質是 NP-hard 的組合最佳化問題，人工與傳統模擬退火（simulated annealing）方法耗時數週。
- **模擬驗證**（SPICE、formal verification）占設計週期 70% 以上；先進製程一次 tape-out 成本高達數千萬美元，錯一次就慘赔。
- 設計經驗長期鎖在資深工程師腦中，無法自動化傳承。這是「嫌疑人」：EDA 工具的效率天花板。

## 線索與推理 -- 數學式、程式、理論（本體）

### 線索一：佈局是組合爆炸的遊戲
Floorplanning 可視為「把 $n$ 個方塊放進棋盤」的問題。若每個方塊有 $k$ 個候選位置，狀態空間為 $k^n$。以 $n=10^7$、$k=10^3$ 計：

$$
|\text{states}| = k^n = (10^3)^{10^7} = 10^{3\times 10^7}
$$

天文數字，窮舉與局部搜尋都無力。**推理**：這與圍棋同構 —— 巨大狀態空間 + 延遲回報（placement 好壞要到繞線與時序分析才知道），正是 RL 擅長的場景。

### 線索二：強化學習公式（Q-learning / Bellman 更新）
Google 2021 Nature 論文《A graph placement methodology for fast chip design using a deep RL algorithm》將 floorplanning 視為馬可夫決策過程（MDP）：

- **狀態 $s$**：當前版圖（已放置的巨集與 netlist 特徵，以圖神經網路 GNN 編碼）
- **動作 $a$**：把下一個巨集放到某個座標
- **獎勵 $r$**：線長（wirelength）、擁塞（congestion）、密度（density）的加權負值

Q-learning 更新式：

$$
Q(s,a) \leftarrow Q(s,a) + \alpha\left[r + \gamma\max_{a'} Q(s',a') - Q(s,a)\right]
$$

其中 $\alpha$ 為學習率、$\gamma$ 為折扣因子。理論定義：**MDP** $= (S, A, P, R, \gamma)$，最佳策略 $\pi^*(s) = \arg\max_a Q^*(s,a)$。Google 用 RL 在 6 小時內產出與人類工程師數週成果相當、甚至更優的 TPU 佈局。

### 線索三：Surrogate Model —— AI 加速模擬
精確模擬（如 SPICE 電晶體級分析）太慢，可用代理模型（surrogate model）近似：

$$
\hat{f}_{\theta}(x) \approx f(x), \quad \min_{\theta} \| \hat{f}_{\theta}(x_i) - y_i \|^2
$$

例如以神經網路近似時序、功耗、良率評估，把單次評估從小時級降到毫秒級，讓 RL/貝葉斯最佳化能大量取樣。Synopsys **DSO.ai**（2020，業界首個商用 RL 晶片設計 AI）與 Cadence **Cerebrus**（2021）都以此路線自動搜尋 PPA（Power-Performance-Area）最佳解。

### 線索四：LLM 進入 EDA
2023 年起大型語言模型被用於 RTL 生成與驗證碼撰寫：

```python
# 概念示例：LLM 生成 Verilog 的 API 呼叫（偽碼）
prompt = "寫一個 8-bit 可飽和加法器的 Verilog 模組，附 testbench"
rtl_code = llm.generate(prompt)   # LLM 輸出 RTL
verify(rtl_code, formal_checker)  # 形式驗證把關
```

代表工具：ChipNeMo（NVIDIA，2023）、Newron/VeriGen 等研究，LLM 負責「寫碼」，RL 負責「佈局」，AI 全流程介入。

### Python 演示：簡化版 RL 佈局概念
```python
import random

# 簡化 floorplanning：4 個巨集放到 4x4 棋盤，目標最小化線長
macros = ["A", "B", "C", "D"]
nets = [("A", "B"), ("B", "C"), ("C", "D")]
Q = {}                       # Q[(state, action)] = 價值
alpha, gamma, eps = 0.5, 0.9, 0.3

def wirelength(place):       # 曼哈頓距離總和
    return sum(abs(place[a][0]-place[b][0]) + abs(place[a][1]-place[b][1])
               for a, b in nets)

for ep in range(500):
    placed, state = {}, ()
    reward = 0.0
    for m in macros:                       # 每步放一個巨集
        cells = [(x, y) for x in range(4) for y in range(4)
                 if (x, y) not in placed.values()]
        act = random.choice(cells) if random.random() < eps \
              else max(cells, key=lambda c: Q.get((state, c), 0))
        placed[m] = act
        new_state = tuple(sorted(placed.items()))
        r = -wirelength(placed)            # 負線長當獎勵
        best_next = max((Q.get((new_state, c), 0) for c in cells), default=0)
        key = (state, act)
        Q[key] = Q.get(key, 0) + alpha * (r + gamma * best_next - Q.get(key, 0))
        state, reward = new_state, reward + r

best = max(
    ({m: (x, y) for m, (x, y) in zip(macros, combo)}
     for combo in [tuple(sorted(random.sample(
         [(x, y) for x in range(4) for y in range(4)], 4)))]
     for _ in [0]), key=wirelength)
print("學到的最佳動作數：", len(Q), "初始線長參考：", wirelength(best))
```
（此為教學簡化版，展示「狀態 → 動作 → 獎勵 → Q 更新」的迴圈骨架；真實工具用 GNN 編碼 netlist 並以 PPA 為獎勵。）

## 結案 -- 後果與影響
- **結案陳詞**：EDA 的組合爆炸與模擬瓶頸，被「RL 當設計者 + surrogate 當加速器 + LLM 當寫碼者」三方合力破解。
- Google RL placement 用於 TPU v4 等量產晶片；DSO.ai 宣稱已協助完成上百個 tape-out，Cerebrus 使 PPA 調校自動化，設計週期從「數週人腦」壓到「數小時機器」。
- 深遠影響：設計經驗轉為可訓練的模型資產；EDA 三巨頭（Synopsys、Cadence、Siemens EDA）全面 AI 化；AI 晶片（GPU/TPU/NPU）需求爆發又反過來加速 AI-EDA，形成正迴圈。設計能力民主化，小團隊也有機會設計先進晶片。

## 關鍵人物與文獻
- **Anna Goldie（Google）與 Azalia Mirhoseini（Google/Stanford）**：2021 Nature 論文〈A graph placement methodology for fast chip design using a deep RL algorithm〉共同第一作者。
- **Jeff Dean**：Google AI 負責人，推動 RL-for-chip design 計畫。
- **Synopsys DSO.ai**（2020）：業界首個商用 RL 晶片設計 AI；**Cadence Cerebrus**（2021）：自動化 PPA 最佳化。
- **ChipNeMo**（NVIDIA, 2023）：LLM 用於晶片設計的域內模型研究。
- 延伸：Sutton & Barto《Reinforcement Learning: An Introduction》（Q-learning 理論基礎）。
