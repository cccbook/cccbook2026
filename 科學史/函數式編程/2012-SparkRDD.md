# 2012-SparkRDD

## 案件摘要

2012 年，UC Berkeley AMP Lab 的 Matei Zaharia 在 NSDI 發表論文 "Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing"，宣告 Spark 誕生。這是一樁「謀殺磁碟 I/O」的案件：MapReduce 每個 job 都要讀寫 HDFS，迭代式機器學習被迫反覆掃描資料，Hadoop 慢如蝸牛。Zaharia 的破案關鍵是一個函數式的想法——不備份資料，改用「血緣（lineage）」：只要記得每份資料是如何被純函數產生的，故障時重算即可。RDD 於是成為不可變分散式資料集與血緣圖的結合。這樁案件證明：函數式的 DAG 思想不只是學術玩具，而是容錯與效能的工程解方。

## 前因 -- 為什麼會有這個案子

- MapReduce（Dean 與 Ghemawat，2004）以 map/reduce 兩階段處理海量資料，但每個 job 都要從 HDFS（磁碟）讀入、寫回，中間結果也落盤。
- 迭代式機器學習（PageRank、k-means、邏輯迴歸）需要在同一份資料上反覆掃描數十輪，Hadoop 每輪都付出磁碟與序列化代價，慢如蝸牛。
- 傳統容錯策略是「複製資料」（replication）或「檢查點（checkpointing）」，代價是儲存與網路頻寬。
- 函數式程式的洞見：純函數是確定性的、可重試的（冪等），因此「記住怎麼算」比「保存算好的結果」更便宜。
- AMP Lab 的研究者每天跑迭代式演算法，親身感受到 Hadoop 的痛，於是著手設計以記憶體為中心的新抽象。

## 線索與推理 -- 數學式、程式、理論

### 線索一：RDD 是什麼

RDD = 不可變（immutable）的分散式資料集 + 血緣圖（lineage graph）。每個 RDD 記錄兩件事：

1. 它由哪些「父 RDD」經過哪個 transformation 產生；
2. 資料的分區（partition）方式。

若以 $D_i$ 表示第 $i$ 個 RDD，則血緣是一張函數組合圖：

$$
D_3 = \text{filter}(f_3, \ \text{map}(f_2, \ D_1))
$$

整條鏈本質上是一個純函數 $D_3 = (f_3 \circ f_2 \circ \cdots)(D_0)$。因為 $f_i$ 是純函數，對相同輸入必得相同輸出：$\forall x: f(x) = f(x) \Rightarrow \text{重算} = \text{原值}$。

這就是容錯的數學基礎：不複製資料，故障時沿血緣重算即可（recompute from lineage），純函數可重試的冪等性（idempotence）取代備份。

### 線索二：lazy transformation vs eager action

RDD 的 API 分兩類：**transformation（lazy）**——`map`、`filter`、`join` 只把函數加進血緣圖，不執行；**action（eager）**——`count`、`collect` 觸發 DAG scheduler，把血緣圖編譯成分散式任務並執行。

lazy 的好處：scheduler 能看見整張 DAG，才能做全域優化（合併 pipeline、剪掉不用的分支）。

### 線索三：寬依賴 vs 窄依賴

血緣圖的邊有兩種，決定 shuffle（資料重分布）的邊界：

$$
\text{窄依賴}： \text{每個父分區至多被一個子分區使用} \ (\text{map, filter}) \quad | \quad \text{寬依賴}： \text{子分區依賴多個父分區} \ (\text{join, groupByKey})
$$

窄依賴的 partition 可以在同一台機器上 pipeline 執行；寬依賴必須跨網路 shuffle，是效能瓶頸與容錯斷點。DAG scheduler 以寬依賴為界，把 DAG 切成多個 stage。

### 破案時刻：mini RDD 實作

以下 Python 程式實作迷你 RDD：lazy transformation 鏈、血緣記錄、action 觸發計算，以及模擬「故障後沿血緣重算」：

```python
class MiniRDD:
    def __init__(self, parent=None, op=None, partitions=None):
        # 血緣：parent 是父 RDD，op 是產生本 RDD 的純函數
        self.parent = parent
        self.op = op
        self.partitions = partitions  # 根節點才有初始資料分區
        self.cached = None            # 模擬 in-memory cache

    def map(self, f):
        return MiniRDD(parent=self, op=lambda p: [f(x) for x in p])

    def filter(self, f):
        return MiniRDD(parent=self, op=lambda p: [x for x in p if f(x)])

    def collect(self):
        """action：沿血緣遞迴重算，並快取各層結果"""
        if self.partitions is not None:
            self.cached = self.partitions
            return [list(p) for p in self.partitions]
        if self.cached is None:
            parent_data = self.parent.collect()
            self.cached = [self.op(p) for p in parent_data]
        return [list(p) for p in self.cached]

    def crash_cache(self, level=0):
        """模擬故障：清掉第 level 層的 cache，資料本身從未備份"""
        if level == 0:
            self.cached = None
        elif self.parent:
            self.parent.crash_cache(level - 1)

data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
r0 = MiniRDD(partitions=data)
r1 = r0.map(lambda x: x * x)          # lazy：只記血緣
r2 = r1.filter(lambda x: x % 2 == 1)  # lazy：只記血緣

print("result:", r2.collect())        # action：觸發計算
# result: [[1, 9], [25], [49, 81]]

r2.crash_cache(level=0)               # 模擬記憶體故障
print("recovered:", r2.collect())     # 沿血緣重算，結果一致
# recovered: [[1, 9], [25], [49, 81]]
```

故障後重算結果與原結果完全一致——這就是「血緣取代備份」的破案證據。真實的 Spark 用同樣思想，但以 DAG scheduler 將血緣圖切 stage、跨叢集排程，並用檢查點截斷過長的血緣。

## 結案 -- 後果與影響

- Spark 成為大數據處理的事實標準；Zaharia 於 2013 年參與創立 Databricks，將 Spark 商業化。
- 「血緣 + DAG + lazy evaluation」的函數式思想成為資料工程標準：Airflow、dbt 等工具同樣以 DAG 為核心抽象。
- 機器學習迭代訓練（PageRank、k-means 等）在 Spark 上比 Hadoop 快 10-100 倍（論文實測 logistic regression 快逾 20 倍）。
- 深度學習需要大量迭代，Spark 的 in-memory 迭代能力助推了 2012 年後的深度學習浪潮的工程基礎設施。
- RDD 證明了純函數可重試性可以「取代」資料備份——容錯理論因此從儲存問題變成函數問題。

## 關鍵人物與文獻（條例，含真實文獻書目）

- **Matei Zaharia**：RDD 與 Spark 核心設計者，UC Berkeley AMP Lab 博士生（後為 MIT 助理教授、Databricks CTO）；**Chowdhury、Franklin、Shenker、Stoica** 為 NSDI 2012 論文共同作者。
- Zaharia, M., Chowdhury, M., Franklin, M. J., Shenker, S., & Stoica, I. (2012). *Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing*. Proceedings of the 9th USENIX Symposium on Networked Systems Design and Implementation (NSDI '12), 15-28.
- Dean, J., & Ghemawat, S. (2004). *MapReduce: Simplified Data Processing on Large Clusters*. Proceedings of OSDI '04, 137-147.
- Zaharia, M., et al. (2016). *Spark: The Definitive Guide*. O'Reilly Media.
