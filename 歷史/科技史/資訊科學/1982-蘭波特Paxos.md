# 1982 - Lamport Paxos（分佈式共識的聖經）

## 案件摘要
1982 年前後，**Leslie Lamport（1941–）** 寫下了分佈式共識的「聖經」——
**Paxos 演算法**，卻被藏了近二十年（1982 草稿，1998 才以
*The Part-Time Parliament* 正式發表）：
$$\boxed{\text{機器會崩溃、訊息會遺失，多數派活著，定案就不可推翻}}$$
**Paxos** 解決的是**崩潰容錯共識**問題：
- 一群節點中，**任一個節點都可能在任意時刻崩溃**；
- 它們仍必須對**單一的值**達成一致（共識）；
- 核心武器是**多數派（quorum）交集**與**兩階段協議**。
$$\text{多數派交集} + \text{兩階段協議} = \text{崩潰容錯的共識}.$$
這份被誤解十六年的手稿，後來成為**整個雲端時代的地基**——
**2013 年，ACM 把圖靈獎頒給了這位「時間的偵探」**（邏輯時鐘見 `1978-蘭波特邏輯時鐘.md`）。

## 前因 -- 為什麼會有這個案子
- **拜占庭將軍問題（1982）**：
  Lamport（與 Shostak、Pease）提出**拜占庭將軍問題**：
  $n$ 位將軍圍攻敵城，其中 $f$ 位是**叛徒**，會**任意說謊**；
  忠誠的將軍們必須行動一致。
  $$\boxed{n \geq 3f + 1 \quad\text{（容忍 } f \text{ 個拜占庭節點的必要條件）}}$$
  但拜占庭容錯太昂貴——現實中的機器多半只是**崩溃（crash）**，不會**說謊**。
  一個更便宜、更貼近實務的問題浮出水面：**崩潰容錯共識**。
- **資料庫複製與交易（1970 年代）**：
  Codd 的關聯式資料庫（1970，見 `1970-科德關聯式資料庫.md`）需要
  **交易（transaction）**的 ACID 保證：
  複製資料到多台機器後，**所有副本必須對「寫入順序」達成一致**——
  這正是**共識（consensus）**問題。
- **分佈式系統的現實（1970s–1980s）**：
  UNIX（1973）之後，多機協作成為常態；網路**會丟包、會分區、會重複**，
  節點**會當機、會重啟**——在這樣的世界裡達成一致，是**最兇險的懸案**。
- **FLP 不可能定理（1985）**：
  Fischer、Lynch、Paterson 證明：在**非同步系統**中，只要有一個程序可能崩溃，
  **確定性的共識演算法不存在**——
  $$\boxed{\text{非同步 + 崩溃容錯} \Rightarrow \text{共識不可能（確定性版本）}}$$
  但 Paxos 用「**安全保證 + 活躍性假設（訊息遲早會送達）**」繞過了這道牆——
  **不可能定理沒有殺死共識，只是劃清了戰場**：安全性永遠成立，
  活躍性（總能選出值）在非同步下只能「盡力而為」。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：問題設定與三種角色
Paxos 的戰場上有**三種角色**（同一台機器可兼任多角）：
- **提議者（proposer）**：提出方案（編號 $n$，值 $v$），說服大家接受；
- **接受者（acceptor）**：投票，決定哪個方案定案；
- **學習者（learner）**：得知定案結果。
**目標（安全性）**：**最多只有一個值被定案**——即使一半的接受者同時崩溃。
**目標（活躍性）**：只要多數派活著，**總能選出某個值**。

### 第二條線索：多數派 quorum 交集原理
設接受者總數 $n$，容忍 $f$ 個崩溃，則 $2f + 1 \leq n$；
**多數派** $Q$ 滿足 $|Q| \geq \lfloor n/2 \rfloor + 1$。
**核心武器：任意兩個多數派必交集**：
$$\boxed{|Q_1 \cap Q_2| \geq 2\lfloor n/2 \rfloor + 2 - n \geq 1 \qquad\text{（兩個多數派必交集）}}$$
- 兩個多數派各含 $\geq \lfloor n/2 \rfloor + 1$ 個節點；
- **交集非空** ⇒ 新提議必然「看見」舊的已定案值 ⇒ **安全性（不會出現兩個不同的值）**；
- 這是鴿籠原理的分佈式版本——**Paxos 一切的魔法都從這個交集開始**。

### 第三條線索：兩階段協議（Prepare/Promise + Accept/Accepted）
**階段一（Prepare / Promise）**：
1. 提議者選編號 $n$，向多數派發送 `prepare(n)`；
2. 接受者若 $n$ 大於它見過的所有編號，回覆 `promise(n, 已接受的值)`，
   並**承諾不再接受編號 $< n$ 的提議**。
$$\text{prepare}(n) \xrightarrow{\text{承諾}} \text{promise}(n, \text{已接受的值})$$
**階段二（Accept / Accepted）**：
1. 提議者收到**多數派**的 promise 後，提出 `accept(n, v)`——
   $v$ 取 promise 中**最高編號**已接受的值（若無則自選）；
2. 接受者接受後廣播 `accepted(n, v)`——**一旦多數派接受，值就定案**。
$$\text{accept}(n, v) \xrightarrow{\text{多數派接受}} \text{定案（chosen）}$$
**為什麼 $v$ 必須取最高編號的已接受值？**——因為那個值可能已經定案；
新提議者若看見它，就必須**沿用**它（而不是換成自己的值）——
**這是「不推翻定案」的關鍵一步**。

### Python：Paxos acceptor 與多數派投票模擬

```python
# 1) 簡化的 Paxos acceptor：驗證多數派交集原理
def quorum_intersects(q1, q2, n):
    return len(set(q1) & set(q2)) > n / 2

def quorum_safe(q1, q2, n):
    return len(set(q1) & set(q2)) >= 1   # 交集非空即安全

n = 5   # 5 個 acceptor，容忍 2 個崩溃
majorities = [[1, 2, 3], [3, 4, 5], [2, 4, 5]]
print("多數派交集（n=5，每派 3 個）：")
for i in range(len(majorities)):
    for j in range(i + 1, len(majorities)):
        q1, q2 = majorities[i], majorities[j]
        inter = sorted(set(q1) & set(q2))
        print(f"  Q{q1} ∩ Q{q2} = {inter}  交集非空？{quorum_safe(q1, q2, n)}")
print("  → 任意兩個多數派必交集 ⇒ 新提議必然看見舊的定案值 ⇒ 安全性 ✓")

# 2) Paxos 兩階段協議模擬（prepare/promise + accept/accepted）
class Acceptor:
    def __init__(self, aid):
        self.aid = aid
        self.promised = 0      # 承諾不再接受編號 < promised 的提議
        self.accepted_id = 0   # 已接受的最大提議編號
        self.accepted_val = None

    def prepare(self, ballot):
        if ballot > self.promised:
            self.promised = ballot
            return ("promise", self.accepted_id, self.accepted_val)
        return ("reject", None, None)

    def accept(self, ballot, val):
        if ballot >= self.promised:
            self.accepted_id, self.accepted_val = ballot, val
            return ("accepted", ballot, val)
        return ("reject", None, None)

acceptors = {i: Acceptor(i) for i in range(1, 6)}
quorum = [1, 2, 3]   # 多數派：acceptor 1, 2, 3

# 階段一：提議者 A 提案編號 1，值 = "v=A"
print("\n【階段一 Prepare/Promise】提議者提案編號 1，值 = v=A：")
for a in quorum:
    print(f"  acceptor {a}: {acceptors[a].prepare(1)}")

# 階段二：accept(n, v)
print("【階段二 Accept/Accepted】：")
results = []
for a in quorum:
    r = acceptors[a].accept(1, "v=A")
    results.append(r[0])
    print(f"  acceptor {a}: {r}")
chosen = results.count("accepted") > len(quorum) / 2
print(f"  多數派 {quorum} 已接受 → 值定案？{chosen}")

# 3) 新 leader 上場（舊提議亂入的阻擋）：編號 0 的過期 prepare 與編號 2 的新提案
print("\n【過期提議阻擋】新 acceptor 4 收到過期 prepare(0) 與 prepare(2)：")
print(f"  acceptor 4: prepare(0) → {acceptors[4].prepare(0)}")
print(f"  acceptor 4: prepare(2) → {acceptors[4].prepare(2)}")
print("  階段一的『承諾』機制阻擋過期提議 ⇒ 舊 leader 無法破壞定案 ✓")
print(f"\n最終狀態：acceptor 1–3 的定案值 = "
      f"{[acceptors[a].accepted_val for a in quorum]}")
```
輸出：
```
多數派交集（n=5，每派 3 個）：
  Q[1, 2, 3] ∩ Q[3, 4, 5] = [3]  交集非空？True
  Q[1, 2, 3] ∩ Q[2, 4, 5] = [2]  交集非空？True
  Q[3, 4, 5] ∩ Q[2, 4, 5] = [4, 5]  交集非空？True
  → 任意兩個多數派必交集 ⇒ 新提議必然看見舊的定案值 ⇒ 安全性 ✓

【階段一 Prepare/Promise】提議者提案編號 1，值 = v=A：
  acceptor 1: ('promise', 0, None)
  acceptor 2: ('promise', 0, None)
  acceptor 3: ('promise', 0, None)
【階段二 Accept/Accepted】：
  acceptor 1: ('accepted', 1, 'v=A')
  acceptor 2: ('accepted', 1, 'v=A')
  acceptor 3: ('accepted', 1, 'v=A')
  多數派 [1, 2, 3] 已接受 → 值定案？True

【過期提議阻擋】新 acceptor 4 收到過期 prepare(0) 與 prepare(2)：
  acceptor 4: prepare(0) → ('reject', None, None)
  acceptor 4: prepare(2) → ('promise', 0, None)
  階段一的『承諾』機制阻擋過期提議 ⇒ 舊 leader 無法破壞定案 ✓

最終狀態：acceptor 1–3 的定案值 = ['v=A', 'v=A', 'v=A']
```

**偵探的註記**：`quorum_intersects` 用 `> n/2` 判斷交集**大於半數**——
這是「單一多數派的大小」的條件，不是「兩派交集」的條件；
兩派的正確表述是**交集非空**（$|Q_1 \cap Q_2| \geq 1$），
配合每派**本身**滿足 $|Q| \geq \lfloor n/2 \rfloor + 1$，
鴿籠原理就保證了交集必然非空——**安全性由此成立**。

## 結案 -- 後果與影響
- **Paxos 的傳奇（1982 → 1998）**：
  拜占庭將軍（1982）與 Paxos 草稿完成後，Lamport 覺得**平鋪直敘的證明太枯燥**，
  於是寫成**希臘島嶼議會的寓言**——《The Part-Time Parliament》——
  審稿人**以為是科幻小說**，論文被擱置**十六年**；
  1998 年正式發表，2001 年再補一篇平實版 *Paxos Made Simple*。
  $$\text{寓言寫法（1982）} \xrightarrow{\text{被誤解 16 年}} \text{正式發表（1998）} \xrightarrow{} \text{工業界聖經}$$
- **雲端時代的共識（2000s–）**：
  $$\text{Paxos} \xrightarrow{} \text{Google Chubby / Spanner} \xrightarrow{} \text{ZooKeeper（Zab）} \xrightarrow{} \text{Raft（2014）}$$
  - **Google Chubby**（2006）：分散式鎖服務，**Paxos 的首個大規模工業實現**；
  - **Google Spanner**（2012）：全球分散式資料庫，靠 Paxos 跨洲複製，
    配合 TrueTime API 實現**外部一致性**；
  - **ZooKeeper**：Zab 協議（Paxos 的變體），支撐 Hadoop 生態的組態與協調；
  - **Raft**（2014，Ongaro & Ousterhout）：**為可理解性而設計**的共識演算法——
    成為教學與工業界的新寵（etcd、TiKV、Consul）。
  $$\boxed{\text{你每次存取雲端資料，背後都有一次 Paxos 式的共識}}$$
- **與邏輯時鐘的合流**：
  Paxos 負責「**選定哪個值**」（共識），
  邏輯時鐘（1978，見 `1978-蘭波特邏輯時鐘.md`）負責「**事件的順序**」（排序）——
  兩者合體就是**狀態機複製**：全序廣播一串定案值，每個副本執行同一串指令。
  $$\text{共識（Paxos）} + \text{排序（邏輯時鐘）} = \text{狀態機複製}$$
- **圖靈獎（2013）**：
  ACM 將 2013 年**圖靈獎**頒給 Lamport，
  表彰他對**分佈式系統理論與實踐的根本性貢獻**——
  從邏輯時鐘、拜占庭將軍到 Paxos，**分佈式共識的每塊基石都是他鋪的**。
  $$\text{邏輯時鐘（1978）} \xrightarrow{} \text{Paxos（1998）} \xrightarrow{} \text{圖靈獎（2013）}.$$
- **LaTeX 的副業（1984）**：
  同一位 Lamport 也是 **LaTeX** 的原作者——
  他寫作論文時嫌 TeX（Knuth，1978）太低階，包了一層**巨集與結構化標記**——
  **一個人在「共識」與「排版」兩個領域都留下了同名遺產**。
- 歷史定位：**Lamport 是分佈式系統的偵探**——
  他證明了：在機器會崩溃的世界裡，
  **一致性不是靠運氣，而是靠數學**；
  $$\text{無全局時鐘（1978）} \xrightarrow{} \text{共識可達（1998）} \xrightarrow{} \text{雲端時代（2000s–）}.$$
  **一切從那個被誤解十六年的希臘議會寓言開始。**

## 關鍵人物與文獻
- **L. Lamport**：*The Part-Time Parliament*（1998；草稿 1982）；*Paxos Made Simple*（2001）；*The Byzantine Generals Problem*（1982）；*Time, Clocks...*（1978，見 `1978-蘭波特邏輯時鐘.md`）；LaTeX（1984）；圖靈獎（2013）。
- **R. Shostak, M. Pease**：拜占庭將軍問題的共同作者（1982）。
- **M. Fischer, N. Lynch, M. Paterson**：FLP 不可能定理（1985）——劃定共識的理論邊界。
- **D. Ongaro & J. Ousterhout**：Raft（2014）——為可理解性而設計的共識演算法。
- **D. Knuth**：TeX（1978）——LaTeX 的地基。
- 相關案件：`1978-蘭波特邏輯時鐘.md`、`1973-UNIX作業系統.md`、`1970-科德關聯式資料庫.md`、`1936-圖靈機.md`。
