# 1992 - Tesauro 的 TD-Gammon（自我對弈學成大師）

## 案件摘要
1992 年，IBM 的 Gerald Tesauro 發表 **TD-Gammon**——一個只用 TD($\lambda$) 學習
+ 神經網路 + **自我對弈**訓練的西洋雙陸棋 (backgammon) 程式。
它不讀任何人類棋譜、不靠任何開局理論，純靠「自己跟自己下幾十萬局」，
達到了**人類世界頂尖水準**，改變了人類雙陸棋的開局定式。**這是 AlphaGo 的 24 年前預演。**

## 前因 -- 為什麼會有這個案子
- **雙陸棋的特殊地貌**：與跳棋、西洋棋不同，雙陸棋有**骰子**——轉移是隨機的。
  這使得窮舉搜索（下棋程式的標配）失效，但**恰好適合無模型的 TD 學習**：
  反正搜索不可靠，不如直接學估值。
- **Neural 1 的失敗**：Tesauro 1989 年的前作用「人類專家的棋譜」做監督學習，
  只達到中等業餘水準——**模仿專家是兇手，天花板太低。**
- **Sutton 的啟發**：1988 年的 TD 學習（見 `1988-SuttonTD學習.md`）提供了正確的引擎；
  Samuel 1959 的自我對弈（見 `1959-Samuel跳棋自學程式.md`）提供了正確的訓練法。
  Tesauro 的偵探直覺：**把兩者合體，並拋棄人類棋譜。**

## 線索與推理 -- 數學式、程式、理論

### 核心推理一：估值網路取代搜索
TD-Gammon 用三層神經網路 $V_\theta(s)$ 直接從局面（198 個輸入特徵）
預測「白方最終獲勝的機率」：
$$V_\theta(s) \approx P(\text{白方勝} \mid s), \qquad \theta \text{ 為網路權重}.$$
決策：對每個合法走法，取「走完後的期望局面」估值最高者：
$$a^* = \arg\max_{a \in \mathcal{A}(s)} \mathbb{E}_{\text{dice}}\big[ V_\theta(s') \big].$$
**沒有 minimax 搜索、沒有對手模型——單靠一個估值函數。**

### 核心推理二：TD($\lambda$) 自我對弈
每局白方 vs 黑方（同一網路），終局回傳 $z \in \{0, 1\}$（白方勝/負），
每一步用 TD 誤差更新：
$$\delta_t = V_\theta(s_{t+1}) - V_\theta(s_t), \qquad \theta \leftarrow \theta + \eta\, \delta_t\, e_t,$$
其中 $e_t$ 是資格跡：$e_t = \lambda e_{t-1} + \nabla_\theta V_\theta(s_t)$，$\lambda = 0.7$。
**自我對弈 = 無限的免費標註資料**；TD = 每步即學，不必等終局。

### Python：極簡 TD 自我對弈骨架

```python
import numpy as np

def sigmoid(x): return 1 / (1 + np.exp(-x))

class ValueNet:
    def __init__(self, n_in, n_hid=40):
        self.W1 = np.random.randn(n_in, n_hid) * 0.1
        self.W2 = np.random.randn(n_hid) * 0.1
    def __call__(self, s):
        h = np.tanh(s @ self.W1)
        return sigmoid(h @ self.W2)          # 勝率估計
    def grad(self, s):
        h = np.tanh(s @ self.W1)
        return np.outer(s, (1-h**2) * self.W2 * self.y_hat) if False else \
               np.outer(s, 1 - h**2) * self.W2   # 簡化梯度

net = ValueNet(n_in=8)
e = np.zeros((8, 40)); lam, eta = 0.7, 0.01
z = 1.0                                        # 終局：白方勝
s_prev = np.random.randn(8)
for t in range(200):                           # 一局 200 步（示意）
    s_next = np.random.randn(8)
    delta = net(s_next) - net(s_prev)          # TD 誤差
    e = lam * e + np.outer(s_prev, 1 - np.tanh(s_prev @ net.W1)**2)
    net.W1 += eta * delta * e                  # TD(lambda) 更新
    s_prev = s_next
print("訓練後終局估值（示意）:", round(float(net(np.random.randn(8))), 3))
```
輸出：
```
訓練後終局估值（示意）: 0.425
```
（真實 TD-Gammon：數十萬局自我對弈後，估值網路的勝率預測與實際勝率高度吻合。）

### 訓練量與成績偵查
| 版本 | 訓練局數 | 隱藏層 | 水準 |
|------|---------|--------|------|
| TD-Gammon 0.0 | 15,000 | 40 | 中等業餘 |
| TD-Gammon 1.0 | 300,000 | 80 | 強業餘 |
| TD-Gammon 2.1 | 1,500,000 | 80 | 大師級 |
| TD-Gammon 3.0 | 數百萬 | 80+ 搜索 | 世界頂尖 |

## 結案 -- 後果與影響
- **人類知識被機器改寫**：TD-Gammon 發現的開局定式（如「5 點早期佔領」）被職業棋手採用，
  改寫了雙陸棋開局理論——**機器反過來教人類**。
- **AlphaGo 的預演**：自我對弈 + 估值網路 + TD 思想，24 年後被 AlphaGo（2016）
  發揚光大（加上 MCTS 與更深的網路）。**1992 年的種子，2016 年開花。**
- **神經網路寒冬中的火種**：1990 年代神經網路研究低潮，TD-Gammon 是少數的高光成果，
  維持了學界對神經網路的信心。
- **方法論的翻案**：Tesauro 比較了監督版（學棋譜）與 TD 版（自我對弈）——
  TD 版的棋力遠超監督版，證明**超越老師必須靠試誤，不能靠模仿**。
  這個結論在 2017 年被 AlphaZero 再次驗證。

## 關鍵人物與文獻
- **Gerald Tesauro**：Communications of the ACM 38(3), 58–68 (1992)；Neural Computation 6(2), 1994。
- **Richard Sutton**：TD 學習（1988，引擎）；**Arthur Samuel**：自我對弈（1959，訓練法）。
- 相關案件：`1959-Samuel跳棋自學程式.md`、`1988-SuttonTD學習.md`、`2016-AlphaGo擊敗李世乭.md`。
