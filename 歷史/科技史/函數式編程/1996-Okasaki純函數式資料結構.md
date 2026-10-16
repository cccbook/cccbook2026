# 1996-Okasaki純函數式資料結構

## 案件摘要

純函數式語言堅持「不可變」，但傳統資料結構——可變連結串列、可變陣列——全依賴原地更新（in-place update），這讓「FP 必然慢」成為當時學界的偏見。偵探 Chris Okasaki 於 1996 年在 CMU 完成博士論文《Purely Functional Data Structures》（1998 年由 Cambridge University Press 出版成書），系統性地破案：只要善用結構共享（structural sharing）與惰性評估的攤還分析，不可變資料結構也能達到與命令式版本同級的效率。這樁案子讓「持久化資料結構」從理論好奇變成工業標配。

## 前因 -- 為什麼會有這個案子

- 純函數式語言（Haskell、SML）的資料不可變：每次「修改」都必須產生新版本，傳統資結構教科書（如 Knuth 的演算法）全部假設可變記憶體。
- 原地更新（in-place update）在純函數世界是禁手：一個結構可能被多個「時間點」共享，改了它就會破壞歷史版本。
- 如果 FP 想證明自己實用，必須正面回答：「不可變也有高效結構嗎？」
- 先前已有零星線索：Hood-Melville 的 real-time queue（1981 年提出、Okasaki 1995 年重新分析）證明某些結構可以做到最壞情況 O(1)，但缺乏統一的方法論。
- 另一個障礙：攤還分析（amortized analysis）本身假設「結構被用掉即丟棄」，在持久化世界（舊版本仍存活）會失效——需要新工具。

## 線索與推理 -- 數學式、程式、理論

### 線索一：持久化與結構共享

持久化資料結構的定義：每次修改返回新版本，舊版本仍然可用。關鍵在於新舊版本共享未改變的部分，因此單次修改的成本不必是整份結構的拷貝。若結構大小為 $n$、共享後只需改動路徑長度 $d$，則更新成本為 $O(d)$ 而非 $O(n)$：

$$
\text{update}: \; v \mapsto v' \quad \text{其中 } |v' \setminus v| = O(d), \; |v' \cap v| = n - d
$$

持久化的代價是「歷史版本都活著」：命令式的攤還分析假設結構消費後即亡，但持久化版本可以被反覆回退重放，攤還界線會被打破。

### 線索二：惰性評估拯救攤還分析 -- banker's method

Okasaki 的核心破案技術：用惰性評估（suspension）把「昂貴的重算」延後，並用記帳法（banker's method）證明攤還界在持久化世界仍然成立。令每個 suspension 帶有信用值（credits），信用總和不減，則未來任一操作序列的總成本仍有界：

$$
\hat{c}_i = c_i + \Delta(\text{credits}_i) \quad \text{且} \quad \sum_{i=1}^{m} \hat{c}_i \le m \cdot O(1)
$$

因為 suspension 一旦被強制求值（force），結果會被共享——即使多個歷史版本都指著同一個 suspension，昂貴計算只做一次。這是命令式結構做不到的「免費備忘錄」。

### 線索三：兩個堆疊反轉的佇列與 real-time queue

Okasaki 的 lazy queue 用兩個堆疊（front、rear）實作佇列：入隊 push 進 rear，出隊從 front 取；front 空了就把 rear 反轉接上。攤還 $O(1)$。Hood-Melville 的 real-time queue（Okasaki 1995 年以惰性技術重新推導）更進一步做到最壞情況 $O(1)$：

$$
\text{queue} = (\text{front}, \text{rear}) \quad \text{invariant: } |\text{front}| \ge |\text{rear}|
$$

### 線索四：為什麼 C++ STL 不可能持久化

STL 的容器（`vector`、`list`）語義綁定原地突變：迭代器失效、引用不穩定、修改即毀滅歷史。Okasaki 同時示範了純函數式 red-black tree 插入——只用模式匹配與局部重平衡，不需要 parent 指標與 in-place 旋轉，程式更短且自動持久化。

### 可執行程式碼：Python 實作 Okasaki 式持久化 queue

```python
import copy

class PQueue:
    """Okasaki 式持久化佇列：front + rear（反轉不變量）。
    每次 snoc/dequeue 返回新版本，舊版本共享未變的 list。"""
    def __init__(self, front=(), rear=()):
        self.front = front   # tuple：取出端（可共享、不可變）
        self.rear = rear     # tuple：插入端（反序存放）
        self._check()

    def _check(self):
        # 不變量：|front| >= |rear|；違反就把 rear 反轉接上（攤還 O(1) 的重算時刻）
        if len(self.front) < len(self.rear):
            self.front = self.front + tuple(reversed(self.rear))
            self.rear = ()

    def snoc(self, x):
        # 新版本：front 共享（不拷貝），只有 rear 多一個元素
        return PQueue(self.front, (x,) + self.rear)

    def dequeue(self):
        if not self.front:
            raise IndexError("empty")
        return self.front[0], PQueue(self.front[1:], self.rear)

q0 = PQueue()
q1 = q0.snoc(1).snoc(2).snoc(3)
x, q2 = q1.dequeue()          # 攤還 O(1)

print("q1 出隊:", x)           # 1
print("q1 仍完整:", list(q1.front))  # [1, 2, 3]  -- 舊版本存活
print("q2 內容:", list(q2.front))    # [2, 3]    -- 與 q1 共享尾部

# 版本共享驗證：q1 與 q2 的 front 沒有被拷貝重算
print("共享:", q1.front[1:] == q2.front)
```

### 攤還界的簡易驗證

```python
q = PQueue()
for i in range(100000):
    q = q.snoc(i)             # 均攤 O(1)：反轉只在 |front|<|rear| 時發生
total = 0
for _ in range(100000):
    v, q = q.dequeue()
    total += v
print(total)                   # 4999950000，全程線性時間
```

## 結案 -- 後果與影響

- Clojure 的 persistent vector（Rich Hickey，2007，32 分支樹）直接受 Okasaki 影響，成為該語言的標配容器。
- Haskell 的 containers、Scala 的 immutable collection 皆採用書中的結構與分析。
- immutable.js（JavaScript）把持久化資料結構帶進前端開發。
- 「不可變資料結構」成為多核與併發時代的標配：沒有共享可變狀態，就沒有資料競爭。
- 《Purely Functional Data Structures》成為 FP 經典教材，攤還分析 + 惰性評估成為標準方法論。
- 本案宣告破案：「FP 資料結構必然慢」的偏見被正式推翻——方法對了，不可變與高效可以並存。

## 關鍵人物與文獻

- Chris Okasaki：本案偵探，US Military Academy 教授，持久化資料結構方法論的確立者。
- Robert Hood 與 Robert Melville：real-time queue 的原創者。
- Chris Okasaki, "Purely Functional Data Structures", PhD thesis, Carnegie Mellon University, 1996.
- Chris Okasaki, "Purely Functional Data Structures", Cambridge University Press, 1998.
- Chris Okasaki, "Simple and efficient purely functional queues and deques", Journal of Functional Programming, 5(4), 1995.
- Robert Hood, Robert Melville, "Real-time queue operations in pure Lisp", Information Processing Letters, 13(2), 1981.
- Chris Okasaki, "The Role of Lazy Evaluation in Amortized Functional Data Structures", ICFP, 1995.
