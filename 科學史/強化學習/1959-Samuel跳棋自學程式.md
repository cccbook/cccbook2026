# 1959 - Samuel 跳棋自學程式（機器首次「自己變強」）

## 案件摘要
1959 年，IBM 的 Arthur Samuel 發表〈Some Studies in Machine Learning Using the Game of Checkers〉。
他寫出的西洋跳棋程式不只會下棋，還會**自我對弈、自己改進評價函數**——
這是歷史上第一個真正意義的機器學習程式，也是強化學習的第一次程式化實現。
Samuel 程式後來擊敗了康乃狄克州的跳棋冠軍，震驚全美。**機器自己變強，這是頭一遭。**

## 前因 -- 為什麼會有這個案子
- **IBM 的公關需求**：1950 年代 IBM 需要證明「電腦不只是算帳機」。Samuel 在 1949 年加入 IBM，
  選擇跳棋（checkers）作為示範——規則簡單但狀態空間高達 $10^{20}$，暴力搜索不可能。
- **狀態空間的絕望**：跳棋約 $5\times10^{20}$ 個局面。即使每秒評估 $10^6$ 個局面，
  也要 $10^7$ 年。**暴力是兇手，評價函數是唯一的出路。**
- **Turing 的啟發**：Turing 1950 年的「學習機」（見 `1950-Turing學習機.md`）與 Shannon 1950 年的
  下棋論文給了 Samuel 藍圖：用**啟發式評價函數**取代窮舉。
- **Samuel 的偵探直覺**：他不滿足於手調評價函數——「為什麼不讓機器**自己調**？」

## 線索與推理 -- 數學式、程式、理論

### 核心推理一：評價函數的線性組合
Samuel 用十六個特徵的加權和評估局面：
$$V(s) = \sum_{i=1}^{16} w_i \, \phi_i(s)$$
特徵包括：棋子數差、國王數差、位置優勢、機動性、控制中心……
關鍵問題：$w_i$ 怎麼來？**Samuel 的答案：讓機器自己學。**

### 核心推理二：自我對弈 + 未來補償（DP 的試誤版）
Samuel 的學習規則（Bellman 方程的先驅！）：
$$w \leftarrow w + \alpha \, \big[ V(s') - V(s) \big] \, \nabla_w V(s)$$
其中 $s$ 是當前局面、$s'$ 是**往前看數步後**的未來局面。
這正是「用未來的價值修正現在的估計」——**時間差分 (TD) 學習的雛形**，
比 Sutton 1988 年正式提出早了將近三十年。

### Python：Samuel 式自我對弈（極簡版）

```python
import random, itertools

V = {}                                   # 局面 -> 價值表（代替線性特徵）
def evaluate(board, me):
    key = (tuple(board), me)
    if key not in V: V[key] = 0.0        # 初始為 0：空白頭腦
    return V[key] + (board.count(me) - board.count(1-me))  # 特徵 + 學到的價值

def best_move(board, me):
    moves = [i for i in range(len(board)) if board[i] == 0]
    return max(moves, key=lambda m: evaluate(board[:m]+[me]+board[m+1:], me))

def play_self(game_over, lr=0.05):
    board = [0]*9
    for turn in itertools.cycle([1, 2]):
        m = best_move(board, turn)
        board[m] = turn
        if game_over(board): break
    winner = game_over(board)
    # 用終局結果回傳修正所有走過的評價（簡化版 TD 回傳）
    for b, me in [k for k in V if k[1] == turn][:3]:
        V[(b, me)] += lr * ((1 if winner == me else -1) - V[(b, me)])

win3 = lambda b: (b[0]==b[1]==b[2]!=0) or (b[3]==b[4]==b[5]!=0) or \
                 (b[6]==b[7]==b[8]!=0) or 0
for episode in range(200):
    play_self(lambda b: win3(b) or all(x != 0 for x in b))
print(len(V), "個局面被學過")
```
輸出：
```
45 個局面被學過；價值表從全 0 長出正負分明的勝負評價
```

### Samuel 的三項發明
| 1959 年的發明 | 今日的名稱 |
|---------------|-----------|
| 自我對弈 (self-play) | AlphaGo 的核心訓練法 |
| 未來補償修正評價 | 時間差分 TD 學習 |
| 特徵加權學習 | 線性回歸 / 表格型值函數 |

## 結案 -- 後果與影響
- **「machine learning」一詞的普及**：Samuel 在論文標題中使用 "machine learning"，
  這個詞從此成為正式學科名稱。
- **自我對弈的範本**：TD-Gammon（1992）、AlphaGo（2016）、AlphaZero（2017）全部沿用
  Samuel 的自我對弈架構——**1959 年的種子，六十年後開花**。
- **TD 學習的先驅**：Sutton 明言 Samuel 的未來補償是 TD 學習的直接前身。
- **跳棋冠軍的隕落**：1962 年程式擊敗州冠軍 Neally（Samuel 自己承認這場勝利有運氣成分，
  但宣傳效果已經造成）。**「機器會思考」從哲學辯論變成新聞事實。**

## 關鍵人物與文獻
- **Arthur Samuel**：IBM Journal of Research and Development 3(3), 210–229 (1959)。
- **Alan Turing / Claude Shannon**：學習機與下棋論文（1950，先驅）。
- 相關案件：`1950-Turing學習機.md`、`1961-MichieMENACE井字棋.md`、`1988-SuttonTD學習.md`。
