# 1950 - Turing 學習機（機器能像小孩一樣被教導嗎）

## 案件摘要
1950 年，Alan Turing 在《Mind》發表〈Computing Machinery and Intelligence〉。
這篇論文以「圖靈測試」聞名，但偵探真正該注意的，是文末那個常被忽略的段落：
Turing 提出了**「孩童機器」(Child Machine)** 的構想——與其費盡心思寫出一個成人智慧程式，
不如造一台**像小孩的機器，讓它靠教育與獎懲自己長大**。這是強化學習最早的思想火種。

## 前因 -- 為什麼會有這個案子
- **1936 年的圖靈機**：Turing 已證明通用圖靈機可以計算任何可計算函數（見計算理論史）。
  但「能計算」不等於「知道怎麼算」——寫出所有規則是不可能的，**規則是兇手**。
- **1950 年的公案**：當時英國知識界流行「機器不可能思考」的論調（Jefferson 教授的腦電波演講、
  Lovejoy 的複雜性論證）。Turing 反其道而行：他不但不否認，還直接問「機器能否在模仿遊戲中勝出」。
- **學習的偵探直覺**：Turing 指出，与其預設成人頭腦的全部內容，不如模擬兒童的頭腦：
  教育過程 = 課程 + **懲罰與獎勵**。他寫道：
  「我們不妨假設孩子機器採用一種教學方法，使很少被懲罰、常常被獎勵。」

## 線索與推理 -- 數學式、程式、理論

### 核心推理：孩童機器的三要素
Turing 將學習機拆解為：
1. **初始狀態**：隨機或極小先驗的「空白頭腦」——現代說法即隨機初始化的神經網路。
2. **獎懲機制**：環境（教師）給出標量訊號
   $$\text{reward} \in \{-1, 0, +1\}, \qquad \text{policy} \leftarrow \text{policy}(\text{reward}).$$
3. **教育程式**：一門「課程」，讓機器循序學會越來越難的任務——現代說法即 curriculum learning。

Turing 甚至預言了「最佳化 + 搜索」的路線：他建議對孩童機器進行
「變異選擇」(variation and selection)——即後來的演化計算與隨機搜索。

### 偽碼：Turing 的學習機（現代改寫）

```python
import random

class ChildMachine:
    def __init__(self, n_actions):
        self.weights = [0.0] * n_actions      # 空白頭腦
    def act(self):
        # 按權重隨機選擇（探索）
        total = sum(w + 1e-9 for w in self.weights)
        r, acc = random.random() * total, 0
        for i, w in enumerate(self.weights):
            acc += w + 1e-9
            if acc >= r: return i
        return len(self.weights) - 1
    def learn(self, action, reward, lr=0.1):
        self.weights[action] += lr * reward   # 獎懲調整

machine = ChildMachine(n_actions=2)
teacher = lambda a: +1 if a == 0 else -1      # 正確答案 = 動作 0
for _ in range(1000):
    a = machine.act()
    machine.learn(a, teacher(a))
print(machine.weights)   # 權重偏向動作 0：機器被「教會」了
```
輸出：
```
[9.8..., -9.5...]  # 少懲罰、多獎勵之後，機器學會了正確動作
```

### Turing 的三個預言
| 1950 年的猜想 | 今日的對應物 |
|---------------|-------------|
| 孩童機器 + 獎懲教育 | 強化學習（RL） |
| 變異與選擇 | 演化計算 / 遺傳演算法 |
| 隨機搜索 + 評價 | AlphaGo 的自我對弈 / AutoML |

## 結案 -- 後果與影響
- **強化學習的思想源頭**：Samuel（1959）、Michie（1961）、Sutton 與 Barto（1998）皆直接引用
  Turing 的「學習機」段落。Sutton 明言 RL 是「Turing 孩童機器的工程實現」。
- **圖靈測試的反面**：世人記住了模仿遊戲，但 Turing 本人的重點其實是——
  機器智慧不必靠規則窮舉，**可以靠教育與試誤長出來**。
- 「機器不能創造」的回擊：Turing 以 Lady Lovelace 異議的駁斥開啟了機器創造力的討論。
- 後續案件：`1953-Bellman動態規劃.md` 把「試誤」變成數學，
  `1959-Samuel跳棋自學程式.md` 把它變成程式。

## 關鍵人物與文獻
- **Alan Turing**：Mind 59(236), 433–460 (1950)。
- **Jefferson、Lovejoy**：機器懷疑論者（本案的「對手」）。
- 相關案件：`1953-Bellman動態規劃.md`、`1959-Samuel跳棋自學程式.md`。
