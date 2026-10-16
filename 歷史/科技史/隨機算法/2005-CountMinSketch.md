# 2005 - Count-Min Sketch

## 案件摘要
2005 年，Graham Cormode 與 S. Muthukrishnan 發表《An Improved Data Stream Summary: The Count-Min Sketch and its Applications》：資料串流只能掃一遍、記憶體只有幾 KB，卻要回答「每個元素出現幾次？」——用 $d \times w$ 的隨機雜湊表計數，查詢答案**只多不少**（向上偏差），誤差可控。Count-Min Sketch（CMS）成為串流算法的基石，是現代大數據系統（Redis、Kafka、Spark）的標配資料結構。

## 前因 -- 為什麼會有這個案子
2000 年代大數據崛起：網路流量監控、搜尋引擎熱門查詢、資料庫查詢優化——資料是**串流**（只能掃一遍、存不下全部）。問題：十億個元素流過，記憶體幾 KB，回答「元素 $e$ 出現幾次」「最熱門的元素是誰」？

確定性方法（精確雜湊表）需要 $O(n)$ 記憶體——不可能。**必須犧牲精度換記憶體**——但如何用數學保證誤差可控？

## 線索與推理 -- 數學式、程式、理論

### Count-Min Sketch 的結構
$d$ 個獨立雜湊函數 $h_1, \dots, h_d: U \to [1, w]$，維護 $d \times w$ 的計數矩陣 $C$。

**更新**（元素 $e$ 出現）：每列計數加一：

$$C[i][h_i(e)] \mathrel{+}= 1, \quad \forall i \in [1, d]$$

**查詢**（$e$ 的計數）：取 $d$ 個計數的**最小值**：

$$\hat{c}_e = \min_{i=1}^d C[i][h_i(e)]$$

**保證**：$\hat{c}_e \ge c_e$（真實計數）——**只會多估，不會少估**。且以機率 $\ge 1 - \delta$：

$$\hat{c}_e \le c_e + \frac{\epsilon \cdot \|\text{counts}\|_1}{w} \cdot \ldots \quad \text{更精確：} \hat{c}_e \le c_e + \epsilon N$$

其中 $N = \sum_e c_e$ 是串流總量，參數 $w = \lceil e/\epsilon \rceil$、$d = \lceil \ln(1/\delta) \rceil$。

### 誤差分析
$e$ 的干擾（overestimate）來自「碰撞」：其他元素撞到同格。單列的期望干擾：

$$E[\text{干擾}_i] = \sum_{e' \ne e} c_{e'} \cdot P(h_i(e') = h_i(e)) = \frac{N - c_e}{w} \le \frac{N}{w} \le \epsilon N$$

由 Markov 不等式：$P(\text{干擾}_i > \epsilon N) \le 1/2$。$d$ 列獨立，取最小值全部干擾都大的機率：

$$P(\hat{c}_e > c_e + \epsilon N) \le (1/2)^d \le \delta \quad \blacksquare$$

**偵探筆記**：誤差分析的推理是「獨立冗餘」——單列有 1/2 機率被污染，$d$ 列獨立取最小值，污染機率指數衰減 $(1/2)^d$。**多個獨立視角 + 取最保守**——這個模式與 Miller–Rabin（見 `1980-Rabin質數檢驗.md`）的多數決、MinHash（見 `1997-BroderMinHash.md`）的多雜湊一脈相承。

### 程式碼：Count-Min Sketch

```python
import random, hashlib, math

class CountMinSketch:
    def __init__(self, epsilon=0.001, delta=0.01):
        self.w = math.ceil(math.e / epsilon)        # 寬度
        self.d = math.ceil(math.log(1/delta))       # 深度
        self.C = [[0] * self.w for _ in range(self.d)]

    def _h(self, i, e):
        return int(hashlib.md5(f"{i}:{e}".encode()).hexdigest(), 16) % self.w

    def update(self, e, count=1):
        for i in range(self.d):
            self.C[i][self._h(i, e)] += count

    def query(self, e):
        return min(self.C[i][self._h(i, e)] for i in range(self.d))

random.seed(42)
cms = CountMinSketch(epsilon=0.001, delta=0.01)
# 模擬十億級串流（此處示範 10^6）
import collections
true_counts = collections.Counter()
for _ in range(1000000):
    e = random.choice([f"item{k}" for k in range(10000)])
    cms.update(e); true_counts[e] += 1

# 查詢只多不少
for e in ["item0", "item1", "item2"]:
    print(f"{e}: CMS={cms.query(e)} 真實={true_counts[e]}")
# CMS ≥ 真實，誤差 ≤ ε·N = 0.001 × 10^6 = 1000

# 記憶體：d × w ≈ 5 × 2719 個計數器 ≈ 13.6 KB（vs 精確表 10000 項）
```

### 變體與擴展
- **點查詢 vs 範圍查詢**：CMS 回答「$e$ 出現幾次」；dyadic intervals 擴展到範圍計數。
- **重金屬（heavy hitters）**：Space-Saving、Sticky Sampling 找最熱門元素。
- **Count-Min 的親戚**：Bloom Filter（1970，成員查詢）、Count Sketch（Charikar et al. 2002，無偏估計）。
- **矩陣恢復**：頻率矩陣的 sketch（Liberty 2013 的 Frequent Directions）。

**偵探筆記**：CMS 的設計哲學是「**偏差換記憶體，數學保證誤差**」——不追求無偏（Count Sketch 才無偏），而是保證**單邊誤差 + 可控機率**。實務上「只多不少」反而有用（容量規劃寧可高估）。

## 結案 -- 後果與影響
- **大數據標配**：Redis（Bloom + CMS）、Kafka Streams、Spark、Flink 內建 sketch。
- **網路監控**：Cisco/Juniper 路由器的流量統計、DDoS 偵測。
- **資料庫**：查詢優化器的頻率估計（PostgreSQL、SQL Server）。
- **sketch 理論**：與 HyperLogLog（見 `2007-HyperLogLog.md`）、Bloom Filter 共同構成概要資料結構（sketching）學科。
- **機器學習**：詞頻統計、特徵雜湊（feature hashing）的空間優化。

## 關鍵人物與文獻
- **Graham Cormode**（1977–）：Warwick；sketching 大師
- **S. Muthukrishnan**（1969–）：Rutgers/Google；串流算法
- Cormode & Muthukrishnan: An Improved Data Stream Summary... (2005, J. Algorithms)
- **Bloom**：Bloom Filter (1970)
- **Charikar et al.**：Count Sketch (2002)
- 交叉參照：`1997-BroderMinHash.md`、`2007-HyperLogLog.md`、`1980-Rabin質數檢驗.md`
