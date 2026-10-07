# 1973-Actor 模型

## 案件摘要

1973 年，MIT AI Lab 的 Carl Hewitt 發表《A Universal Modular ACTOR Formalism for Artificial Intelligence》（IJCAI 1973），提出一個驚世駭俗的主張：計算的基本單位不是函數，而是「actor」——一個擁有信箱、永不同步等待、只靠非同步訊息傳遞溝通的獨立個體。Hewitt 用「小惡魔」（little demons）比喻這些並行運作的感知器：AI 系統需要一群各自為政的小惡魔同時窺探世界，而不是一個大型序列程序依序巡邏。同一年，Gerry Sussman 想比較 actor 與 closure 的異同，辯論的副產品是 Scheme 語言的誕生。本案追查：Actor 的三條定律是什麼，它與 closure、與 Hoare 的 CSP 有何本質差異，以及它如何成為 Erlang、Akka、Go 的思想祖源。

## 前因 -- 為什麼會有這個案子

- LISP（1958/1960）的計算模型是純序列的：一次求值一個 expression，等待結果、再求下一個——對 AI 中需要並行感知的「小惡魔」架構完全不夠用。
- 1970 年代初，共享記憶體並行程式設計一片混亂：race condition、deadlock、semaphore 的正確性無人能保證，debug 靠運氣。
- Hewitt 的 Planner 語言（1971）已經用「pattern-directed invocation」做 AI 推理，但仍是單機序列；他想要一個「universal modular」的形式論，讓模組可以任意並行組合。
- 1972 年，Gerry Sussman 與 Guy Steele 受邀在 Hewitt 的組裡實作 actor 語言的小版本；他們想搞清楚「actor 到底比 closure 多了什麼」。
- 同期，Hoare 正醞釀 Communicating Sequential Processes（1978），陣營對峙：同步（rendezvous）對非同步（信箱）——兩條路線的戰爭延燒四十年。
- 硬體層面，多處理器機器（如 MIT 的 Concurrent LISP 機器）開始出現，軟體理論必須跟上。

## 線索與推理 -- 數學式、程式、理論

### 線索一：Actor 的三條定律

一個 actor 收到訊息後，能且只能做三件事（Hewitt 1973；Baker-Hewitt 1977 形式化為「laws for communicating parallel processes」）：

1. **傳送**有限個訊息給其他 actors（位址可以是自己的、別人的、或訊息裡附帶的）。
2. **創造**有限個新的 actors（新 actor 的行為由定義給定，位址即時可用）。
3. **指定**下一則訊息到來時要採用的**行為**（可以更換自己的行為——這就是狀態演化的唯一途徑）。

形式化地，actor 的計算是一個非同步事件系統：每個事件 $e = (\text{actor}, \text{message}, \text{audience})$ 表示「actor 收到 message，把訊息發給 audience」。事件之間只有偏序（partial order）關係——發送先於接收——不存在全域時鐘：

$$
e \prec e' \;\equiv\; e \text{ 的訊息傳送 } \to e' \text{ 的訊息接收}
$$

整個系統的「計算」就是這個偏序集合的極小模型。沒有共享變數、沒有鎖、沒有全域順序——一切因果關係都被顯式寫在訊息傳遞裡。

### 線索二：actor vs closure——Sussman 的疑惑

Sussman 當年的關鍵問題：「actor 與 LISP closure 到底差在哪？」Steele 與 Sussman 實作後發現：兩者驚人地相似——都是「攜帶環境的程序」。唯一差別是**通訊協定**：

- closure：呼叫後**同步等待**返回值（functional 風格）。
- actor：發訊息後**不等**，繼續做別的事；結果若需要，必須以「回程訊息」送達另一個 actor。

為了研究這個差異，他們造了一個叫 Schemer 的玩具直譯器（磁帶機命名限制下縮短為 Scheme）——原本是 actor 研究的副產品，結果成了函數式編程的支柱。

### 線索三：CSP 的對照——同步 vs 非同步

Hoare 1978 年的 CSP 選了相反的路：程序間通訊是同步的 rendezvous——`P ! x` 與 `Q ? x` 必須兩邊同時到位，否則雙方都阻塞。CSP 的數學核心是 trace model：

$$
\text{trace}(P) = \langle a_1, a_2, \ldots \rangle \quad (\text{可觀測事件序列，} a_i \in \Sigma)
$$

CSP 用「事件序列的集合」定義程序等價性；Actor 用「事件偏序」定義。同步 CSP 容易證明（時序簡單），非同步 Actor 容易規模化（不阻塞）。Erlang 選 Actor，occam 選 CSP，Go 的 channel 介於兩者之間。

### 程式示範：Python mini Actor 模型

用 `queue.Queue` 當信箱，`threading` 當排程器，實作 Actor 三定律：

```python
import threading, queue, time

class Actor:
    def __init__(self):
        self.mailbox = queue.Queue()
        self.behavior = self.default_behavior
        threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self):
        while True:
            msg = self.mailbox.get()
            # 三條定律的執行點：行為內部可傳送、可 spawn、可換行為
            self.behavior(self, msg)

    def default_behavior(self, ctx, msg):
        print("unknown:", msg)

    def send(self, msg):
        self.mailbox.put(msg)   # 非同步：不等對方處理

def spawn(behavior):
    a = Actor()
    a.behavior = behavior
    return a

class Cell(Actor):
    # 一個「可變儲存格」actor：狀態只靠行為更替演化（定律三）
    def value_behavior(self, ctx, msg, val):
        op = msg[0]
        if op == "get":
            msg[1].send(("ok", val))          # 定律一：回程訊息
        elif op == "set":
            self.behavior = lambda c, m: self.value_behavior(c, m, msg[1])

c = Cell(); c.behavior = lambda ctx, m: c.value_behavior(ctx, m, 0)
client = spawn(lambda ctx, m: print("client got", m))
c.send(("set", 42)); c.send(("get", client))
time.sleep(0.2)
```

注意 `client.send` 與 `c.send` 都是非同步的：發送者從不等待。儲存格的「狀態」不存在共享變數裡，而是編碼在行為函數的參數中——這正是 Baker-Hewitt 定律三的展現。

### 破案時刻

Steele 與 Sussman 在 1975-76 年間的實驗報告中寫下結論：actor 就是「不能同步回傳值的 closure」。Hewitt 對這個化約不以為然，但兩條路線就此分家：一條通往 Scheme 與純函數式，一條通往 Erlang 與訊息傳遞。案件的真相是：**並行的本質不是共享狀態，而是訊息的因果序**。

## 結案 -- 後果與影響

- Erlang（1986 開發，1993 穩定，Ericsson）直接採用 Actor 行程模型：每個行程一個信箱、無共享、非同步訊息，成為電信級容錯系統的支柱。
- Akka（2009，Scala）把 Actor 模型帶進 JVM 生態；Elixir（2012）繼承 Erlang VM。
- Go 的 goroutine 與 channel（2009）屬於同一「訊息傳遞而非共享狀態」傳統——"Don't communicate by sharing memory; share memory by communicating."
- 「並行正確性靠隔離與訊息」的哲學成為分散式系統的預設思維，影響雲端微服務架構。
- Scheme 從 actor 研究的副產品，成為 continuation、尾呼叫優化、函數式教學的標準載體——案件的意外收穫。
- Actor 的事件偏序模型影響了分散式系統理論（Lamport 的 happened-before 關係，1978，與 Hewitt 的偏序同源）。

## 關鍵人物與文獻

- Carl Hewitt, Peter Bishop, Richard Steiger, "A Universal Modular ACTOR Formalism for Artificial Intelligence", *Proceedings of IJCAI 1973*, pp. 235–245.
- Henry Baker & Carl Hewitt, "Laws for Communicating Parallel Processes", *Proceedings of IFIP Congress 1977*, pp. 987–992.
- Carl Hewitt & Henry Baker, "Actors and Continuous Functionals", *Proceedings of IFIP Working Conference on Formal Description of Programming Concepts*, 1977.
- Gerald Jay Sussman & Guy Lewis Steele Jr., "SCHEME: An Interpreter for Extended Lambda Calculus", MIT AI Memo 349, 1975.
- C. A. R. Hoare, "Communicating Sequential Processes", *Communications of the ACM* 21(8), 1978, pp. 666–677.
- Joe Armstrong, "Making reliable distributed systems in the presence of software errors", PhD thesis, KTH, 2003（Erlang 的 Actor 模型總結）.
