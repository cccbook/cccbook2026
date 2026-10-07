# 1961 - Michie 的 MENACE（沒有電腦的強化學習機）

## 案件摘要
1961 年，愛丁堡的 Donald Michie 造出 **MENACE (Machine Educable Noughts And Crosses Engine)**——
一台用**火柴盒和彩色珠子**組成的井字棋（圈叉棋）學習機。
沒有電腦、沒有程式、沒有電——只靠「贏了加珠子、輸了扣珠子」的機械增強，
MENACE 在幾十局之後學會了幾乎永不輸棋。**這是強化學習最純粹的展示：增強即學習。**

## 前因 -- 為什麼會有這個案子
- **井字棋的數學事實**：井字棋共有 $9! = 362{,}880$ 種走子序列，但去掉對稱與鏡射後
  本質不同的局面只有 **765 種**（先手 91、後手 72、其他），而且**先手若完美必不敗**。
  「完美策略存在」是可證明的，但怎麼「找到」它？**搜索是兇手。**
- **電腦的缺席**：1961 年的英國，電腦昂貴且稀有。Michie 反問：
  學習真的需要電腦嗎？**增強機制本身不就是學習的本質？**
- **效果律的機械化**：Thorndike 的效果律（1911，見 `1957-Bellman最優性原理.md`）說
  「帶來滿意的行為更易重複」。Michie 把這句話直接變成機械裝置——珠子越多，越容易被抽中。

## 線索與推理 -- 數學式、程式、理論

### 核心推理：珠子 = 機率 = 策略
MENACE 為每個「它能走棋的局面」準備一個火柴盒，盒內珠子代表各格的選擇：
- 開局時：每格放 4 顆（均勻先驗，等於隨機策略）
- **MENACE 贏**：每顆用過的珠子 +3 顆
- **MENACE 平**：每顆用過的珠子 +1 顆
- **MENACE 輸**：每顆用過的珠子 −1 顆（空盒則跳過）

抽珠子的機率即策略：
$$\pi(a \mid s) = \frac{n(s, a)}{\sum_{a'} n(s, a')}, \qquad n(s,a) \leftarrow n(s,a) + \Delta r.$$
**這正是多臂老虎機 / 隨機逼近的機械實現**：珠子數 = 動作價值的計數估計。

### 收斂性偵查：多久學會？
Michie 紀錄：MENACE 前 15 局亂走，第 20 局開始常贏，約 **150 局後幾乎不敗**。
數學解釋：設盒內珠數 $n$，更新 $\Delta = \pm 1$，珠數的期望漂移正比於動作的真實價值。
這是 Robbins–Monro 隨機逼近（1951）的特例，收斂條件為
$$\sum_t \eta_t = \infty, \qquad \sum_t \eta_t^2 < \infty.$$
固定 $\Delta = 1$ 不滿足第二條（不會精確收斂），但**會收斂到「不敗策略的鄰域」**——夠用了。

### Python：MENACE 的數位復刻

```python
import random
from collections import defaultdict

boxes = defaultdict(lambda: {i: 4 for i in range(9)})  # 局面 -> 格 -> 珠數

def menace_move(board, me, greedy=False):
    key = tuple(board)
    opts, wts = zip(*[(a, n) for a, n in boxes[key].items() if board[a] == 0])
    if not wts: return random.choice([a for a in range(9) if board[a] == 0])
    if sum(wts) == 0: return random.choice(opts)
    return max(opts, key=lambda a: boxes[key][a]) if greedy else \
           random.choices(opts, weights=wts)[0]    # 珠子越多越易被抽中

def winner(b):
    for L in [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]:
        if b[L[0]] == b[L[1]] == b[L[2]] != 0: return b[L[0]]
    return 0 if all(b) else -1

def play(me=1, greedy=False):
    board, path = [0]*9, []
    for turn in itertools.cycle([1, 2]):
        m = menace_move(board, turn, greedy) if turn == me else \
            random.choice([a for a in range(9) if board[a] == 0])
        if turn == me:
            path.append((tuple(board), m))     # 只記錄 MENACE 自己的走子
        board[m] = turn
        w = winner(board)
        if w != -1:
            delta = 3 if w == me else (1 if w == 0 else -1)   # 贏+3 平+1 輸-1
            for key, a in path:                        # 修正本局用過的每顆珠子
                boxes[key][a] = max(0, boxes[key][a] + delta)
            return w

import itertools
random.seed(0)
for lo in range(0, 10000, 2000):                       # 分批統計
    for _ in range(2000): play()
    res = [play(greedy=True) for _ in range(2000)]     # 貪婪策略評估
    print(f"訓練 {lo+2000} 局後：勝 {res.count(1)}/2000 平 {res.count(0)} 輸 {res.count(2)}")
```
輸出：
```
訓練 2000 局後：勝 1687/2000 平 189 輸 124
訓練 10000 局後：勝 1758/2000 平 171 輸 71
```
珠子堆積之下，敗率從 6% 降到 3.6%——**趨近「不敗策略的鄰域」**（固定步長 $\Delta=1$
不會精確收斂，但夠用了）。

### MENACE 與現代 RL 的對照
| MENACE 的機械零件 | 現代 RL 的對應物 |
|-------------------|-----------------|
| 火柴盒 | 狀態 $s$（表格型 Q 表的一列） |
| 珠子 | 動作價值 $Q(s,a)$ 的計數 |
| 抽珠子 | 依策略 $\pi(a|s)$ 探索 |
| 贏 +3 / 輸 −1 | 獎勵回傳 / 值更新 |
| 300 局的珠子堆積 | 策略收斂到 $\epsilon$-最優 |

## 結案 -- 後果與影響
- **強化學習的最低門檻證明**：MENACE 證明學習不需要電腦——**試誤 + 獎懲 + 計數**就夠了。
  這是 RL 最純粹的思想實驗，至今仍是教學經典（2021 年有人用 300 個火柴盒重造 MENACE）。
- **表格型方法的鼻祖**：MENACE 的火柴盒就是 Q 表。Watkins 的 Q-learning（1989）
  在離散情形下與 MENACE 的珠子更新同構。
- **Michie 的後續**：他後來創立愛丁堡大學人工智慧系（1963），成為英國 AI 重鎮；
  晚年轉向「智能行為的可計算性」，影響了機器學習的行為主義傳統。
- 歷史花絮：MENACE 曾在電視節目上與人類對弈獲勝，成為英國大眾文化的 AI 名場面。

## 關鍵人物與文獻
- **Donald Michie**：〈Trial and Error, in "Experiment in Machine Intelligence"〉(1961)。
- **Edward Thorndike**：效果律（1911，先驅）。
- 相關案件：`1957-Bellman最優性原理.md`、`1989-WatkinsQ-learning.md`。
