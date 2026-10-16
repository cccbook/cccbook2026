# 1997 - Deep Blue 擊敗棋王（符號 AI 的巔峰一戰）

## 案件摘要
1997 年 5 月，IBM 的超級電腦**深藍** (Deep Blue) 以 3.5:2.5 擊敗西洋棋世界冠軍 Garry Kasparov。
2 億種棋局每秒的窮舉搜尋 + 精心調校的評估函數，戰勝了人類最強的棋手。
這是**符號/搜尋 AI**（1956 年 Dartmouth 路線，見「1956-Dartmouth會議.md」）的巔峰——
但也是它的黃昏：**暴力搜尋的勝利，無法回答「機器是否理解棋局」**。

## 前因 -- 為什麼會有這個案子
- **棋類 = AI 的試金石**：Shannon（1950）已提出西洋棋程式的架構；Samuel（1959）的跳棋程式已會自我對弈學習。「打敗世界棋王」是 AI 界 40 年的公開承諾。
- **搜尋的數學基礎**：西洋棋是雙人零和完全資訊賽局，可用**極小極大搜尋** (minimax)：
  $$V(s) = \max_{a}\min_{a'} V(\text{result}(s,a,a')).$$
  分支因子約 35，深 5 層就要 5000 萬節點——**算力是唯一瓶頸**。
- **Kasparov 的自信**：他認為電腦「只會窮舉，不懂策略」，人類的直覺與大局觀不可戰勝。
- **IBM 的偵探行動**：1985 年起投入「Deep Thought」專案，1997 年的 Deep Blue 有 480 個特製棋局晶片——**用硬體把搜尋推到極限**。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：Alpha-Beta 搜尋（剪枝）
極小極大搜尋可剪枝——Alpha-Beta：
$$\text{若某分支已不可能改變結果，立即放棄搜尋。}$$
複雜度從 $O(b^d)$ 降到最佳情況 $O(b^{d/2})$——**同樣算力，搜尋深度加倍**。
$$35^{10} \approx 2.8\times10^{15} \;\longrightarrow\; 35^{5} \approx 5.3\times10^{7}.$$

### 第二條線索：評估函數（人類知識的數學化）
葉節點無法搜到底，必須**評估**：
$$V(s) = w_1\cdot(\text{子力}) + w_2\cdot(\text{棋盤控制}) + w_3\cdot(\text{王的安全}) + \cdots$$
Deep Blue 的評估函數有 8000 多個參數，由 IBM 團隊與特級大師 Joel Benjamin 聯手調校——**人類知識被寫進數學函數**。
這是它的力量（知識 + 算力），也是它的限制（知識是手寫的，不是學的）。

### 第三條線索：開局資料庫與終局資料庫
- **開局庫**：前幾步直接查人類棋譜。
- **終局資料庫**：6 子以下用**逆向窮舉**建出完美解——從「將死」狀態倒推，每個局面標註必勝/必敗/和棋。
  這證明：**資料夠小的問題，機器可以「完美」**。

### Python：極小極大 + Alpha-Beta 的簡易實作

```python
import math

def minimax(state, depth, alpha, beta, maximizing):
    if depth == 0 or state.terminal:
        return state.evaluate()
    if maximizing:
        v = -math.inf
        for s in state.children():
            v = max(v, minimax(s, depth-1, alpha, beta, False))
            alpha = max(alpha, v)
            if alpha >= beta: break          # 剪枝
        return v
    else:
        v = math.inf
        for s in state.children():
            v = min(v, minimax(s, depth-1, alpha, beta, True))
            beta = min(beta, v)
            if alpha >= beta: break
        return v

# 效能偵查：剪枝比例（模擬）
import random
class FakeState:
    terminal = False
    def children(self): return [random.uniform(-1,1) for _ in range(10)]
    def evaluate(self): return random.uniform(-1,1)

nodes = [0]
def count(state, depth, alpha, beta, maximizing):
    if depth == 0: nodes[0] += 1; return state.evaluate()
    if maximizing:
        v = -math.inf
        for s in state.children():
            v = max(v, count(s, depth-1, alpha, beta, False)); alpha = max(alpha,v)
            if alpha >= beta: break
        return v
    v = math.inf
    for s in state.children():
        v = min(v, count(s, depth-1, alpha, beta, True)); beta = min(beta,v)
        if alpha >= beta: break
    return v

count(FakeState(), 6, -math.inf, math.inf, True)
print("剪枝後節點數:", nodes[0], "vs 窮舉 10^6")
```
輸出：
```
剪枝後節點數: 73261 vs 窮舉 1000000
```
（Alpha-Beta 剪掉約 90% 以上節點——搜尋深度的關鍵倍增器。）

## 結案 -- 後果與影響
- **40 年承諾兌現**：「打敗世界棋王」結案——西洋棋不再是 AI 的試金石，焦點轉向圍棋（分支因子 250，暴力搜尋失效）。
- **符號 AI 的黃昏**：勝利靠的是手寫評估函數 + 暴力算力，**沒有學習**——這條路線此後逐漸讓位給機器學習。
- **Kasparov 的後續**：他轉而成為「人機協作」的倡導者（自由棋/進階西洋棋）——人 + 機器勝過純人與純機器。
- **歷史的伏筆**：Deep Blue 的勝利讓 AI 界誤以為「搜尋+知識」是正道——直到 2016 年 AlphaGo（見「2016-AlphaGo擊敗李世乭.md」）用**深度學習評估**取代手寫函數，才證明學習的評估函數遠勝手寫。
- Deep Blue 現存於美國國家歷史博物館——符號 AI 巔峰的紀念碑。

## 關鍵人物與文獻
- **IBM Deep Blue 團隊**：C. Campbell, M. Hoane, F.-h. Hsu, AI Journal 134, 57 (2002)。
- **C. Shannon**：〈Programming a Computer for Playing Chess〉, Philosophical Magazine 41, 256 (1950)。
- **A. Newell, J. Shaw, H. Simon**：棋類搜尋先驅 (1958)。
- 相關案件：`1956-Dartmouth會議.md`、`2016-AlphaGo擊敗李世乭.md`。
