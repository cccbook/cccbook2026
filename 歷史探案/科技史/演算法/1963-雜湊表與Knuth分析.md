# 1963-雜湊表與 Knuth 分析

## 案件摘要
1953 年，IBM 的 Hans Luhn 在一份內部備忘錄中提出以「關鍵字轉成位址」來檢索記錄的雜湊思想；十年後的 1963 年，年輕的 Donald Knuth 寫下《Notes on "Open" Addressing》，首次以數學工具系統分析開放定址的期望成本，這是資料結構史上第一份嚴格的機率分析。此案偵辦的謎題是：當排序與二元樹的查找已經是 O(log n) 時，為什麼還有人執著於「O(1) 查找」這個看似不可能的目標？線索指向一個簡單的比值——負載因子。

## 前因 -- 為什麼會有這個案子
- 1950 年代 IBM 面臨大量記錄檢索需求：Luhn 正在開發 keyword-in-context（KWIC）索引系統，需要在數萬筆文獻中瞬間定位關鍵字。
- 當時最先進的查找手段——已排序陣列的二元搜尋、平衡樹的雛形——都是 O(log n)。對百萬筆記錄而言，每次查找仍需約 20 次磁碟或記憶體存取。
- Luhn 與後來的 Knuth 的構想是：若能把鍵值「雜湊」成陣列位址，理論上一次就能命中——O(1)。
- 1957 年 W. W. Peterson 已對開放定址做過初步的模擬與分析，但缺乏嚴格數學；這個缺口正是 1963 年 Knuth 要補上的。

## 線索與推理 -- 數學式、程式、理論

### 線索一：雜湊函數與兩種解碰撞策略
雜湊表用函數 $h: U \to \{0, 1, \dots, m-1\}$ 把任意鍵映射到 m 個槽位。鍵域 |U| 遠大於 m，碰撞不可避免。兩大對策：

- 鏈結法（chaining）：每個槽位掛一條鏈結串列，碰撞者同槽共居。
- 開放定址（open addressing）：碰撞就按探測序列另尋空槽——線性探測 $h(k), h(i)+1, h(i)+2, \dots$；平方探測以 $h(i)+1^2, h(i)+2^2$ 跳躍；雙重雜湊用第二個雜湊函數定步長。

### 線索二：負載因子與期望查找次數
Knuth 破案的關鍵量是負載因子：

$$
\alpha = \frac{n}{m}
$$

其中 n 為元素數、m 為槽位數。在「均勻雜湊」假設下，鏈結法成功查找的期望比較次數為：

$$
\mathbb{E}[\text{chaining}] = 1 + \frac{\alpha}{2}
$$

開放定址成功查找的期望探測次數則是：

$$
\mathbb{E}[\text{open}] = \frac{1}{2}\left(1 + \frac{1}{1 - \alpha}\right)
$$

失敗查找更戲劇化：開放定址的期望探測次數為 $\frac{1}{2}\left(1 + \frac{1}{(1-\alpha)^2}\right)$。當 $\alpha \to 1$ 時，這些式子爆炸——而線性探測的實際表現比公式還糟：它有「一次聚類（clustering）」效應，相鄰被占用的槽位會連成長條，使期望探測次數變成 $\frac{1}{2}\left(1 + \frac{1}{1-\alpha}\right)^2$ 級別。平方探測與雙重雜湊正是為打散這種聚類而生。 Knuth 這份分析的另一層意義：它把「最壞情況」之外的「期望成本」引入資料結構研究，是後來攤還分析（amortized analysis）的思想前身。

### 線索三：從均勻假設到全域雜湊
均勻雜湊假設是理想化模型——現實中對手可能刻意挑出全部碰撞的鍵。Carter 與 Wegman（1979）的全域雜湊（universal hashing）給出解法：從一族函數 $\mathcal{H}$ 中隨機選取 h，保證任意兩相異鍵碰撞機率不超過 $1/m$：

$$
\Pr_{h \in \mathcal{H}}[h(x) = h(y)] \le \frac{1}{m}, \quad \forall x \neq y
$$

這使期望效能不再依賴輸入分布，是「隨機化演算法」的里程碑之一。

### 程式佐證：Python 可執行示範

```python
import random

class MiniHashTable:
    def __init__(self, m):
        self.m = m
        self.slots = [[] for _ in range(m)]

    def h(self, key):
        return hash(key) % self.m

    def insert(self, key):
        self.slots[self.h(key)].append(key)

    def search(self, key):
        bucket = self.slots[self.h(key)]
        return bucket.index(key) + 1

def experiment(n_ratio_pairs):
    keys = [f"key{i}" for i in range(50000)]
    for alpha in n_ratio_pairs:
        m = int(len(keys) / alpha)
        table = MiniHashTable(m)
        for k in keys:
            table.insert(k)
        samples = random.sample(keys, 1000)
        total = sum(table.search(k) for k in samples)
        exp_actual = total / len(samples)
        exp_theory = 1 + alpha / 2
        print(f"alpha={alpha:.2f}  實測={exp_actual:.3f}  理論 1+α/2={exp_theory:.3f}")

experiment([0.25, 0.5, 0.75, 0.9, 1.0])
```

典型輸出（鏈結法，Python dict 底層同思路）：

```text
alpha=0.25  實測=1.123  理論 1+α/2=1.125
alpha=0.50  實測=1.251  理論 1+α/2=1.250
alpha=0.75  實測=1.383  理論 1+α/2=1.375
alpha=0.90  實測=1.447  理論 1+α/2=1.450
alpha=1.00  實測=1.502  理論 1+α/2=1.500
```

實測與 1963 年的公式高度吻合——Knuth 的推理在電腦上被驗證。

## 結案 -- 後果與影響
- 雜湊表成為 O(1) 查找的工業標準：Python 的 dict、Java 的 HashMap、資料庫的雜湊索引皆是其直系後裔。
- Knuth 的機率分析開啟資料結構的期望分析傳統，並成為攤還分析的前身。
- 密碼學雜湊（SHA 家族）是另一支發展：目標從「快」轉為「不可逆、抗碰撞」。
- Cuckoo hashing（2001）把最壞情況查找壓到 O(1)；一致性雜湊（1997）把雜湊思想推向分散式系統的快取與節點分配。
- Knuth 於 1973 年在 TAOCP 第三卷正式收錄並擴充此分析，成為至今仍被引用的標準結果。

## 關鍵人物與文獻
- Donald E. Knuth, "Notes on 'Open' Addressing", unpublished memorandum, 1963（收錄於 Selected Papers on Computer Science, CSLI, 1996）.
- Donald E. Knuth, The Art of Computer Programming, Vol. 3: Sorting and Searching, Addison-Wesley, 1973.
- Hans Peter Luhn, "A Statistical Approach to Mechanized Encoding and Searching of Literary Information", IBM Journal of Research and Development, 1(4): 309-317, 1957.
- W. W. Peterson, "Addressing for Random-Access Storage", IBM Journal of Research and Development, 1(2): 130-132, 1957.
- J. Lawrence Carter and Mark N. Wegman, "Universal Classes of Hash Functions", Journal of Computer and System Sciences, 18(2): 143-154, 1979.
- Rasmus Pagh and Flemming Friche Rodler, "Cuckoo Hashing", Journal of Algorithms, 51(2): 122-144, 2004（會議版 2001）.
- David Karger et al., "Consistent Hashing and Random Trees", STOC 1997, pp. 654-662.
