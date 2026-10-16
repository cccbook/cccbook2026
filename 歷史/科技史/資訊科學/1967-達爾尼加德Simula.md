# 1967 - Simula 67（物件導向程式設計的誕生）

## 案件摘要
1967 年，挪威計算中心（Norwegian Computing Center, NCC）的 **Ole-Johan Dahl（1931–2002）**
與 **Kristen Nygaard（1926–2002）** 發表 **Simula 67**——
$$\boxed{\text{世界上第一個物件導向程式設計語言}}$$
他們為了**模擬港口與工廠的作業流程**，在 **ALGOL 60** 的骨架上加入了三個革命性的概念：
- **類別（class）與物件（object）**：資料與操作資料的程式碼**綁在一起**；
- **封裝（encapsulation）**與**繼承（inheritance）**：子類別**複用並擴充**父類別；
- **协程（coroutine）與虛擬函式（virtual）**：多個物件**交替執行**、行為可被**覆寫**。
$$\text{類別} + \text{繼承} + \text{虛擬函式} = \text{物件導向程式設計}.$$
三十餘年後，**C++、Java、Python——一切現代物件導向語言都是 Simula 的後裔**——
**2001 年，兩人共同獲得圖靈獎**；隔年（2002），兩人**相繼逝世**。

## 前因 -- 為什麼會有這個案子
- **ALGOL 60 的遺產（1958–1960）**：
  國際委員會設計的 **ALGOL 60** 是**最優雅的程式語言**：
  **區塊結構（begin ... end）**、**遞迴程序**、**BNF 文法**（見 `1968-克努特演算法藝術.md`）。
  但 ALGOL 60 是**為數值計算而生**——它**沒有**：
  $$\text{ALGOL 60：區塊離開即銷毀} \xrightarrow{\text{問題：模擬需要「活得比區塊久」的物件}} \text{難題}.$$
- **挪威計算中心的現實需求（1961–1965）**：
  Nygaard 在 NCC 負責**作業研究（operations research）**顧問工作：
  為港口、工廠、排隊系統**建立模擬模型**。
  他發現：傳統的數學公式無法描述**成千上萬個互相作用的「個體」**——
  $$\boxed{\text{港口 = 船隻 + 碼頭 + 起重機，各自獨立運作、互相等待}}$$
  每個「船」有自己的狀態（到達、等待、卸貨、離開）——
  **這正是「物件」的原型**。Dahl 隨後加入，兩人先做出 **Simula I（1964）**，
  再於 1965–1967 年重新設計出**通用的** Simula 67。
- **垃圾回收的先例（1958 LISP）**：
  物件在執行期**動態誕生、動態消亡**——
  **誰來釋放記憶體？** **McCarthy 的 LISP（1958）** 已示範：
  $$\text{動態物件} \xrightarrow{\text{LISP：垃圾回收（GC）}} \text{程式設計師不必手動釋放}.$$
  Dahl 在 Simula 中實作了**類似的自動記憶體管理**——
  這條血脈後來流入 **Java、Python、C#**（見 `1958-麥卡錫LISP.md`）。
- **結構化程式設計的浪潮（1968）**：
  就在 Simula 67 問世隔年，Dijkstra 發表 **goto 有害論**（見 `1968-結構化程式設計.md`）——
  $$\text{程式的混亂} \xrightarrow{\text{兩條解藥}} \begin{cases}\text{結構化：由上而下的流程控制} \\ \text{物件導向：由下而上的資料封裝}\end{cases}$$
  **這兩條路線在 1980 年代合流**——成為現代軟體工程的兩大支柱。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：類別與物件——資料與程式碼的合體
**Simula 的 class** 是一個**藍圖**：
$$\text{class} = (\text{資料成員}, \text{程序成員}, \text{初始化程式碼})$$
**物件（object）**是 class 的**實例（instance）**：
$$\text{object} = \text{new } \text{Class} \quad\text{（配置記憶體 + 執行初始化）}.$$
**封裝**：物件的內部狀態**只能透過其程序存取**——
$$\boxed{\text{資料} + \text{操作} = \text{物件（資訊隱藏的邊界）}}$$
這看似簡單，卻是**程式設計思維的哥白尼革命**：
程式的單位不再是「程序」（先有動作、再找資料），
而是「物件」（先有資料、動作跟著資料走）。

### 第二條線索：繼承與虛擬函式——複用與多型
**繼承（inheritance）**：子類別**自動擁有**父類別的全部成員，並可**新增或覆寫**：
$$\text{class } B \text{ extends } A \implies B \supseteq A \text{ 的成員} + B \text{ 的新增}.$$
**虛擬函式（virtual）**：父類別宣告一個「可被覆寫」的程序——
呼叫時**依物件的實際類別**（而非變數的宣告型別）分派：
$$\text{呼叫 } obj.f() \implies \text{執行 } obj.\text{實際類別的 } f \text{（動態分派）}.$$
$$\boxed{\text{同一個呼叫，不同物件，不同行為 = 多型（polymorphism）}}$$
這是 C++ 的 `virtual`、Java 的 `@Override`、Python 的方法覆寫的**共同祖先**。

### 第三條線索：协程與離散事件模擬——Simula 的出生理由
**协程（coroutine）**：多個程序**交替執行**、彼此**讓位**（resume/detach）——
每個模擬物件是一條协程，在模擬時間中**輪流「活著」**。
**離散事件模擬（discrete-event simulation）**的數學骨架：
- **模擬時鐘**只在事件發生時推進：
  $$t_{k+1} = \min\{ e.\text{time} \mid e \in \text{事件佇列} \}$$
- **事件佇列（event queue）**按時間排序（優先佇列，heap 實現）：
  $$\text{事件佇列} = \{(t_1, e_1), (t_2, e_2), \dots\}, \quad t_1 \le t_2 \le \cdots$$
- 每取出一個事件，執行它、可能產生**新事件**（如顧客到達產生下一個到達）：
  $$\boxed{\text{取出事件} \to \text{執行} \to \text{排入新事件} \to \text{時鐘跳躍} \to \cdots}$$
  這就是 Simula 內建的 **Simulation class**——
  也是今天一切模擬軟體（排隊、物流、遊戲引擎）的核心迴圈。

### Python：類別繼承 + 離散事件模擬（單一服務台佇列）

```python
import heapq

class Event:
    """事件：time = 發生時刻（heapq 需要可比較的 key）"""
    def __init__(self, time, kind, cust):
        self.time, self.kind, self.cust = time, kind, cust
    def __lt__(self, other):          # 運算子覆寫：多型的 Python 味道
        return self.time < other.time

class Customer:
    """顧客：記錄到達與離開"""
    def __init__(self, name):
        self.name, self.arrive, self.leave = name, None, None

class Simulator:
    """模擬器：事件佇列（heap）+ 模擬時鐘"""
    def __init__(self):
        self.queue, self.clock = [], 0.0
    def schedule(self, time, kind, cust):
        heapq.heappush(self.queue, Event(time, kind, cust))
    def run(self):
        while self.queue:
            ev = heapq.heappop(self.queue)   # 取最早的事件
            self.clock = ev.time             # 時鐘跳躍到事件時刻
            self.handle(ev)
    def handle(self, ev):
        raise NotImplementedError            # 虛擬函式：留給子類別覆寫

class SingleServerQueue(Simulator):
    """單一服務台佇列：繼承 Simulator，覆寫 handle"""
    def __init__(self, lam, mu, horizon):
        super().__init__()                   # 呼叫父類別初始化（繼承）
        self.mu, self.horizon = mu, horizon
        self.server_busy, self.waits = False, []
        first = self.next_arrival(lam, 0.0)
        self.c = Customer("C1")
        self.schedule(first, "arrive", self.c)
        self.lam = lam
    def next_arrival(self, lam, t):          # 指數到達間隔的均值近似
        return t + 1.0 / lam
    def handle(self, ev):
        if ev.kind == "arrive":
            if not self.server_busy:
                self.server_busy = True
                self.schedule(ev.time + 1.0 / self.mu, "depart", ev.cust)
            else:
                self.waits.append(ev.time)   # 簡記：排隊者到達時刻
            if ev.time < self.horizon:
                nc = Customer(f"C{len(self.waits) + len(self.queue) + 2}")
                nc.arrive = ev.time + 1.0 / self.lam
                self.schedule(nc.arrive, "arrive", nc)
        elif ev.kind == "depart":
            ev.cust.leave = ev.time
            self.server_busy = False

sim = SingleServerQueue(lam=1.0, mu=1.5, horizon=20.0)
sim.run()
done = [c for c in [sim.c] if c.leave is not None]
print("單一服務台佇列模擬（Simula 67 精神）")
print(f"  完成服務的顧客數：{len(done)}")
print(f"  模擬結束時鐘：{sim.clock:.2f}")
print(f"  事件佇列依時間排序執行：heapq（優先佇列）")
```
輸出：
```
單一服務台佇列模擬（Simula 67 精神）
  完成服務的顧客數：1
  模擬結束時鐘：20.67
  事件佇列依時間排序執行：heapq（優先佇列）
```

## 結案 -- 後果與影響
- **物件導向的三大支柱（1967）**：
  $$\boxed{\text{封裝 + 繼承 + 多型——全部誕生於 Simula 67}}$$
  Dahl 與 Nygaard 在 ALGOL 60 的區塊結構上，種下了**現代軟體的基因**：
  $$\text{Simula 的 class} \xrightarrow{\text{35 年}} \text{Java 的 class、Python 的 class、C++ 的 class}.$$
- **後裔譜系**：
  - **Smalltalk（1972/1980，Alan Kay，2003 圖靈獎）**：
    Kay 承認 Simula 是 Smalltalk 的直接靈感——**把「訊息傳遞」推向極致**，
    **一切皆物件**；
  - **C++（1983，Bjarne Stroustrup）**：
    名字直白——「**帶類別的 C**」最初就叫 C with Classes，
    **virtual 函式直接取自 Simula**；
  - **Java（1995）、Python（1991）、C#（2000）**：
    **一切現代物件導向語言都是 Simula 的後裔**——
    class、繼承、方法覆寫、垃圾回收，**全套血統**。
- **離散事件模擬的標準（1967 → 今日）**：
  $$\text{事件佇列} + \text{時鐘跳躍} = \text{Simula 的 Simulation class}$$
  今日的排隊論軟體、物流系統、遊戲引擎（如事件驅動架構）、
  甚至**離散事件網路模擬器**，用的都是同一個迴圈。
- **圖靈獎（2001）與雙星的殞落（2002）**：
  ACM 於 2001 年將**圖靈獎**授予 Dahl 與 Nygaard——
  **「物件導向程式設計的誕生來自他們的研究」**。
  悲喜交集的是：**得獎隔年，兩人相隔一個月先後逝世**（Dahl 2002 年 6 月、Nygaard 2002 年 8 月）——
  $$\text{Simula（1967）} \xrightarrow{34\text{ 年}} \text{圖靈獎（2001）} \xrightarrow{1\text{ 年}} \text{雙星殞落（2002）}.$$
  他們生前都看到了自己的思想**征服整個軟體世界**。
- 歷史定位：**Dahl 與 Nygaard 是軟體世界的「孟德爾」**——
  他們沒有設計最快的語言，卻找到了**軟體的遺傳法則**：
  $$\text{港口模擬（1961）} \xrightarrow{} \text{Simula I（1964）} \xrightarrow{} \text{Simula 67} \xrightarrow{} \text{Smalltalk/C++/Java/Python}.$$
  **今天你寫的每一個 class，都是 1967 年挪威計算中心的一場模擬**。

## 關鍵人物與文獻
- **O.-J. Dahl**、**K. Nygaard**：*SIMULA—An ALGOL-Based Simulation Language*（1967，CACM）；Simula I（1964）；**2001 圖靈獎**。
- **K. Nygaard**：作業研究顧問——港口與工廠模擬的需求起點。
- **J. McCarthy**：LISP（1958）——垃圾回收的先例（見 `1958-麥卡錫LISP.md`）。
- **A. Kay**：Smalltalk（1972/1980）——Simula 的直接繼承者，2003 圖靈獎。
- **B. Stroustrup**：C++（1983）——C with Classes，virtual 取自 Simula。
- 相關案件：`1958-麥卡錫LISP.md`、`1968-結構化程式設計.md`、`1968-克努特演算法藝術.md`。
