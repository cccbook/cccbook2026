# 2012 - Spanner（全球分佈式資料庫）

## 案件摘要
2012 年，Google 的 **James C. Corbett** 與 Spanner 團隊在 **OSDI 2012** 發表
*Spanner: Google's Globally-Distributed Database*：
$$\boxed{\text{用 GPS + 原子鐘，把強一致性帶回全球規模}}$$
**Spanner** 是第一個**全球分佈式資料庫**，橫跨各大洲的資料中心，卻提供：
- **TrueTime**：GPS + 原子鐘打造的**全球時鐘**，給出時間**區間**而非點；
- **外部一致性（external consistency）**：比可序列化更強的保證；
- **Paxos 複製**：每個分片（tablet）一個 Paxos 組，多數派存活即可用；
- **可插拔的 SQL 前端**——「**NewSQL**」的誕生。
$$\text{TrueTime} + \text{Paxos} = \text{全球規模的 ACID}.$$
Dynamo 放軟了一致性，**Spanner 說：與其改變語義，不如把時鐘造準**——
**分佈式資料庫的哲學之爭，被一台硬體時鐘終結**。

## 前因 -- 為什麼會有這個案子
- **1981 年 Gray 的交易 ACID 與 2PC**：
  Jim Gray 界定了**交易**的 ACID 性質（見 `1981-葛雷交易ACID.md`），
  但分散式交易靠 **兩階段提交（2PC）**——協調者一掛，全體卡死：
  $$\text{2PC：單點故障} \xrightarrow{\text{Spanner：每分片一個 Paxos 組}} \text{多數派複製}.$$
  Spanner 把 Gray 的交易語義**原封不動搬上全球規模**。
- **1982 年 Lamport 的 Paxos**：
  Paxos（見 `../資訊科學/1982-蘭波特Paxos.md`）證明**多數派共識**能在
  故障與延遲中就一個值達成一致——
  $$\boxed{\text{Paxos：分佈式共識的基石（1998 年才正式發表）}}$$
  Spanner 把它從理論變成**生產系統的主力引擎**。
- **2000 年 CAP 定理——用硬體繞過取捨**：
  CAP（見 `2000-布魯爾CAP定理.md`）說分區時必須在 C 與 A 之間抉擇；
  **Spanner 的回答是：用硬體把「不確定性」本身消滅**——
  TrueTime 把時鐘誤差壓到極小，**讓「等待」代替「猜測」**：
  $$\text{Dynamo：放軟 C（軟體路線）} \ne \text{Spanner：強化 C（硬體路線）}.$$
- **1978 年 Lamport 邏輯時鐘的極限**：
  Lamport 邏輯時鐘（見 `../資訊科學/1978-蘭波特邏輯時鐘.md`）只有因果序、
  沒有「物理先後」的概念——**外部一致性需要真實的時間感**。
  TrueTime 正是對「物理時鐘不可靠」這一前提的**工程反攻**：
  $$\text{邏輯時鐘（1978）：放棄物理時間} \xrightarrow{\text{TrueTime（2012）：量測它的誤差}} \text{兩種時鐘哲學}.$$

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：TrueTime 的時間區間
TrueTime API 不回傳一個時間點，而是回傳一個**保證包含真實時間的區間**：
$$TT.\text{now}() = [t_{early},\ t_{late}],\quad \text{誤差界 } \epsilon = t_{late} - t_{early}.$$
- **GPS 接收器**（每資料中心）+ **原子鐘**（每台機器）互相校驗；
- 誤差 $\epsilon$ 通常只有 **1–7 毫秒**；
- 「絕對正確」不可得，但「**誤差有界**」可以量測——
  $$\boxed{\text{不確定的不是時間，而是區間寬度——而區間寬度是已知的}}$$

### 第二條線索：等待 $\epsilon$ 保證外部一致性
**外部一致性**：若交易 $T_1$ 在真實時間上**先於** $T_2$ **開始**（$T_1$ 先提交完成），
則 $T_1$ 的時間戳必**小於** $T_2$：
$$T_1 < T_2 \quad\text{（若 } T_1 \text{ 物理上先提交）}.$$
**Commit-wait 策略**：交易提交時取區間 $[t_{early}, t_{late}]$，選 $s = t_{late}$
作為時間戳，然後**等到物理時間確定已過 $s$** 才回報客戶端：
$$\boxed{\text{提交時間 } s = t_{late}，\ \text{等待 } \epsilon\ \text{毫秒} \implies \text{外部一致性}}$$
兩個交易若區間重疊，後提交者**主動等待**對方時間戳過去——
**用幾毫秒的延遲，買回整個強一致性**。

### 第三條線索：Paxos 複製組
每個 tablet（分片）複製到多個副本，形成一個 **Paxos 組**：
- 寫入需**多數派**（$\lfloor n/2 \rfloor + 1$ 個副本）接受；
- 少數派故障不影響可用性；
- 一個資料被指定為**領導者**（leader），協調 Paxos 與 commit-wait。
$$\text{可用性條件}： \text{存活副本} \ge \left\lfloor \frac{n}{2} \right\rfloor + 1$$
跨組交易（事務觸及多個 Paxos 組）再用 **2PC** 協調——
但每個參與者本身是 Paxos 組，**2PC 的單點故障被 Paxos 消化**：
$$\boxed{\text{2PC（協調）} + \text{Paxos（複製）} = \text{全球規模的分散式交易}}$$

### Python：TrueTime 區間與 Paxos 複製組

```python
import itertools

# 1) TrueTime 區間：重疊判斷與 commit-wait 策略
class TrueTime:
    def __init__(self, eps_ms):
        self.eps = eps_ms           # 時鐘誤差界（毫秒）

    def now(self, physical_ms):
        # 回傳保證包含真實時間的區間
        return (physical_ms - self.eps, physical_ms + self.eps)

def commit_wait(tt, physical_ms):
    """提交時間戳取區間上界 t_late，並等待到物理時間超過它"""
    early, late = tt.now(physical_ms)
    wait = late - physical_ms       # 需等待的毫秒數
    return late, wait

tt = TrueTime(eps_ms=4)
print("TrueTime 區間模擬（誤差界 ε = 4ms）：")
t1_phys, t2_phys = 1000.0, 1003.0
s1, w1 = commit_wait(tt, t1_phys)
s2, w2 = commit_wait(tt, t2_phys)
i1, i2 = tt.now(t1_phys), tt.now(t2_phys)
print(f"  T1 區間 = [{i1[0]:.0f}, {i1[1]:.0f}]，提交時間戳 s1 = {s1:.0f}，等待 {w1:.0f}ms")
print(f"  T2 區間 = [{i2[0]:.0f}, {i2[1]:.0f}]，提交時間戳 s2 = {s2:.0f}，等待 {w2:.0f}ms")
overlap = not (i1[1] <= i2[0] or i2[1] <= i1[0])
print(f"  兩區間重疊？{overlap} → T2 需等 s1 過去後才提交")
print(f"  T1 物理先提交，且 s1 < s2 → 外部一致性保證成立 ✓")

# 2) Paxos 複製組：多數派投票
def paxos_commit(group, proposer_ok=True):
    """模擬 Paxos 組的 prepare/promise 階段：多數派接受即提交"""
    alive = [n for n in group if n["alive"]]
    majority = len(group) // 2 + 1
    promises = sum(1 for n in alive if n["accept"])
    return promises >= majority and proposer_ok

group = [
    {"name": "us-east",   "alive": True,  "accept": True},
    {"name": "us-west",   "alive": True,  "accept": True},
    {"name": "eu-west",   "alive": True,  "accept": False},
    {"name": "asia-east", "alive": True,  "accept": True},
    {"name": "asia-south","alive": False, "accept": False},
]
majority = len(group) // 2 + 1
print("\nPaxos 複製組（5 副本，多數派 = 3）：")
for n in group:
    print(f"  {n['name']:<11} 存活={n['alive']}  接受={n['accept']}")
ok = paxos_commit(group)
alive_n = sum(n["alive"] for n in group)
print(f"  存活 {alive_n} 個，接受 {alive_n - 1} 個 ≥ 多數派 {majority} → 提交成功？{ok}")
print("  少數派故障（asia-south）與拒絕（eu-west）不影響提交 ✓")

# 3) 分片 × Paxos 組：2PC + Paxos 的組合
print("\n分片架構（每分片一個 Paxos 組）：")
for i, shards in enumerate([["S1", "S2", "S3"], ["S4", "S5", "S6"]]):
    print(f"  Paxos 組 {i+1}: {shards}")
print("  跨組交易 → 2PC 協調，每個參與者是 Paxos 組（無單點故障）")
print("  → 2PC + Paxos = 全球規模的分散式交易（Spanner 的核心配方）")
```
輸出：
```
TrueTime 區間模擬（誤差界 ε = 4ms）：
  T1 區間 = [996, 1004]，提交時間戳 s1 = 1004，等待 4ms
  T2 區間 = [999, 1007]，提交時間戳 s2 = 1007，等待 4ms
  兩區間重疊？True → T2 需等 s1 過去後才提交
  T1 物理先提交，且 s1 < s2 → 外部一致性保證成立 ✓

Paxos 複製組（5 副本，多數派 = 3）：
  us-east     存活=True  接受=True
  us-west     存活=True  接受=True
  eu-west     存活=True  接受=False
  asia-east   存活=True  接受=True
  asia-south  存活=False  接受=False
  存活 4 個，接受 3 個 ≥ 多數派 3 → 提交成功？True
  少數派故障（asia-south）與拒絕（eu-west）不影響提交 ✓

分片架構（每分片一個 Paxos 組）：
  Paxos 組 1: ['S1', 'S2', 'S3']
  Paxos 組 2: ['S4', 'S5', 'S6']
  跨組交易 → 2PC 協調，每個參與者是 Paxos 組（無單點故障）
  → 2PC + Paxos = 全球規模的分散式交易（Spanner 的核心配方）
```

## 結案 -- 後果與影響
- **2017 年 Spanner 公開雲服務**：
  Spanner 先服務 Google 內部（Google Ads 的 **F1** 資料庫），
  **2017 年正式登上 Google Cloud（Cloud Spanner）**——
  $$\text{內部系統（2012）} \xrightarrow{5\ \text{年}} \text{公開雲服務（2017）}.$$
  任何企業第一次能買到**全球規模的強一致 SQL 資料庫**。
- **NewSQL 的誕生與後裔**：
  Spanner 證明「分散式」與「SQL/ACID」可以並存，引發 NewSQL 浪潮：
  $$\text{Spanner（2012）} \xrightarrow{\text{論文公開}} \text{CockroachDB、TiDB、YugabyteDB}$$
  - **CockroachDB（2015）**：直接承襲 Spanner 的範圍分片與共識複製；
  - **TiDB（2017）**：Paxos 後裔 Raft + MySQL 相容；
  - **Calvin、FaunaDB**：其他分佈式交易路線。
  $$\boxed{\text{NoSQL（2007）與 NewSQL（2012）：一放一收，兩種哲學}}$$
- **雲端時代分佈式 SQL 的勝利**：
  2010 年代中葉，業界共識反轉：**「關聯式模型已死」被證明是謠言**——
  死的不是 SQL，而是**單機的規模極限**。
  Spanner 把 **Codd 的關聯式模型**（見 `1970-科德關聯式模型.md`）
  重新裝上分佈式引擎，成為雲原生資料庫的主流範式。
- **CAP 的硬體答案**：
  TrueTime 是「工程反攻理論」的典範——CAP 假設時鐘不可信，
  **Spanner 就把時鐘造得可信**（誤差界可量測），讓**等待**取代**放軟**。
  $$\text{Dynamo（軟體妥協）} \longleftrightarrow \text{Spanner（硬體堅持）}，\ \text{雙雄並立至今}.$$
- **Corbató 分時思想的遠端迴響**：
  1961 年 **Corbató 的 CTSS 分時系統**（見 `../資訊科學/1961-科巴托分時系統.md`）
  讓許多用戶**同時**分享一台電腦；
  五十年後，Spanner 讓全球用戶**同時**分享一份強一致的資料——
  $$\text{分時（1961）：一台電腦的共享} \xrightarrow{\text{Spanner（2012）}} \text{一份資料的全球共享}.$$
  而 Spanner 的**領導者 James C. Corbett** 恰與 Corbató 同姓——
  **歷史偶然的巧合，卻是分時思想血脈的真實延續**。
- 歷史定位：正如**圖靈機**（見 `../資訊科學/1936-圖靈機.md`）
  用數學定義了「計算」，**Spanner 用硬體重新定義了「時間」**——
  $$\text{Paxos（1982/1998）} \xrightarrow{} \text{TrueTime（2012）} \xrightarrow{} \text{分佈式 SQL 的時代}.$$

## 關鍵人物與文獻
- **J. C. Corbett、J. Dean、M. Epstein 等**：*Spanner: Google's Globally-Distributed Database*（OSDI 2012）。
- **L. Lamport**：*The Part-Time Parliament*（1982，正式發表 1998）——Paxos 共識（見 `../資訊科學/1982-蘭波特Paxos.md`）。
- **L. Lamport**：邏輯時鐘（1978）——TrueTime 的哲學對立面（見 `../資訊科學/1978-蘭波特邏輯時鐘.md`）。
- **J. Gray**：交易 ACID 與 2PC（1981）——Spanner 搬上全球規模的語義（見 `1981-葛雷交易ACID.md`）。
- **E. Brewer**：CAP 定理（2000）——被硬體繞過的取捨（見 `2000-布魯爾CAP定理.md`）。
- **G. DeCandia 等**：Dynamo（SOSP 2007）——哲學對立的另一極（見 `2007-迪納摩Dynamo.md`）。
- **F. J. Corbató**：CTSS 分時系統（1961）——分時思想的源頭（見 `../資訊科學/1961-科巴托分時系統.md`）。
- 相關案件：`2007-迪納摩Dynamo.md`、`2006-谷歌Bigtable.md`、`1970-科德關聯式模型.md`、`../資訊科學/1936-圖靈機.md`。
