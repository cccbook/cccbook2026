# 2004-MapReduce函數式大數據

## 案件摘要

2004 年 12 月，OSDI 會議上，Google 的 Jeff Dean 與 Sanjay Ghemawat 發表了《MapReduce: Simplified Data Processing on Large Clusters》。這篇六頁思路、十二頁細節的論文，宣告了一件驚人的事：工程師不再需要手寫任何分散式程式碼，只要寫兩個純函數，框架就能在數千台機器上完成分片、排程、容錯與資料搬運。Google 內部自 2003 年起已用 MapReduce 重建整個網頁索引。本案的謎題是：為什麼「只准寫純函數」這個看似嚴苛的限制，反而是征服數十億頁網頁的數學鑰匙？答案藏在冪等性（idempotence）與容錯的同構關係裡。

## 前因 -- 為什麼會有這個案子

- Google 的網頁索引在 2000 年代初已達數十億頁，倒排索引的重建在任何單機上都算不完——這不是優化問題，是數量級問題。
- 2000 年代初的分散式程式設計是手工業：機器故障、網路分割、平行切分、負載平衡、部分失敗（partial failure），每一項都要工程師手寫處理邏輯。
- 每個新 pipeline 都重複造輪子：索引、日誌分析、PageRank、爬蟲壓縮，每個專案都自己寫一套「把資料切碎、平行算、再合併」的程式碼。
- 共享可變狀態在分散式環境是致命的：兩台機器同時改一份資料，一致性無從保證。
- 哲學先聲早就在：John Backus 在 1977 年的圖靈獎演說《Can Programming Be Liberated from the von Neumann Style?》大力提倡 map 與 reduce 高階函數；LISP 的 `mapcar` 與 `reduce` 更早就是函數式處理集合的標準工具。

## 線索與推理 -- 數學式、程式、理論

### 線索一：兩個函數的介面

MapReduce 的使用者介面只有兩個函數：

$$
\text{map} : (k, v) \rightarrow \text{list}(k', v')
$$

$$
\text{reduce} : (k', \text{list}(v')) \rightarrow v
$$

`map` 吃一對 key/value，吐出一串中間 key/value；`reduce` 吃一個中間 key 與它所有的值，合併成一個結果。使用者只寫這兩個純函數，框架接手其餘的一切：把輸入切成 16–64MB 的分片（sharding）、把 map 任務排程到閒置機器、把中間結果依 key 洗牌（shuffle）給 reducer、失敗就重試。

### 線索二：冪等性是容錯的數學基礎

破案的關鍵推理在此。因為 `map` 與 `reduce` 都是純函數——相同輸入必得相同輸出、無副作用——所以同一個任務重試任意次，結果都不變：

$$
f(x) = f(f(x)) = \underbrace{f(f(\cdots f(x)\cdots))}_{n \text{ 次}}
$$

這就是冪等性。在數千台廉價商用機器上，機器故障是常態而非例外；有了冪等性，「偵測到 worker 沒回應」只需要一個動作：換一台機器重跑，不必擔心結果不一致，也不必擔心重試會污染其他資料。容錯的工程問題，被純函數的數學性質直接消解。

反面對照：如果 map 允許副作用（例如邊算邊寫共享檔案），重試兩次就會寫兩份，冪等性崩潰，容錯機制隨之失效。純度不是潔癖，是容錯的前提。

### 線索三：word count——最小偵察實驗

論文的經典範例 word count，其 map/reduce 定義為：

$$
\text{map}(k, \text{doc}) = [(\text{word}, 1) \mid \text{word} \in \text{doc}]
$$

$$
\text{reduce}(\text{word}, \text{counts}) = \sum \text{counts}
$$

用 Python 實作一個 mini MapReduce（含 map、shuffle、reduce 三階段與多 worker 模擬）：

```python
import multiprocessing as mp
from collections import defaultdict

def mapper(doc):
    # 純函數：相同輸入必得相同輸出，無副作用
    return [(w.lower(), 1) for w in doc.split()]

def reducer(counts):
    return sum(counts)

def shuffle(mapped):
    grouped = defaultdict(list)
    for kv_list in mapped:
        for k, v in kv_list:
            grouped[k].append(v)
    return grouped

def mini_mapreduce(docs):
    # map 階段：每個 doc 分派給一個 worker（此處用 process pool 模擬）
    with mp.Pool(processes=2) as pool:
        mapped = pool.map(mapper, docs)
    # shuffle 階段：依 key 分組
    grouped = shuffle(mapped)
    # reduce 階段：對每個 key 合併
    return {k: reducer(v) for k, v in grouped.items()}

docs = [
    "the quick brown fox",
    "the lazy dog",
    "the fox and the dog",
]
print(mini_mapreduce(docs))
# {'the': 5, 'quick': 1, 'brown': 1, 'fox': 2, 'lazy': 1, 'dog': 2, 'and': 1}
```

`pool.map` 正是分布式 map 的單機縮影：mapper 是純函數，所以隨便分派給哪個 worker、失敗重跑幾次都無所謂。

### 線索四：shuffle 的代價與 Spark 的繼承

MapReduce 的弱點在 shuffle：每次 reduce 都要從磁碟讀中間結果，多階段 pipeline（如迭代式 PageRank）要反覆寫盤讀盤。2012 年 Matei Zaharia 的 Spark RDD 把整個計畫表達為函數組合圖（lineage）：

$$
\text{RDD}_{n} = f_n(\text{RDD}_{n-1}) = f_n \circ f_{n-1} \circ \cdots \circ f_1(D)
$$

RDD 是不可變的，容錯不靠備份而靠重算——沿著 lineage 圖重放純函數即可重建任何遺失的分區。這是 MapReduce「純函數可重算」思想的推廣：從兩個函數推廣到任意深度的函數組合。

## 結案 -- 後果與影響

- 大數據時代自此開啟：Doug Cutting 與 Mike Cafarella 於 2006 年發表 Hadoop，是 MapReduce 的開源複製品，成為 Yahoo、Facebook 等公司的資料骨幹。
- Google 內部用 MapReduce 重寫整個索引 pipeline，索引重建從數月縮短到數天。
- Spark（2012）、Flink、Beam 延續函數式資料模型：不可變 RDD、lineage 重算、宣告式轉換鏈。
- 「純函數可重試」成為分散式系統的設計準則：冪等寫入、at-least-once 語意、事件溯源（event sourcing），全是同一條數學定理的工程變形。
- Backus 1977 年「從 von Neumann 風格解放編程」的呼籲，在三十年後以數千台機器的規模兌現。

## 關鍵人物與文獻（條列）

- Jeff Dean 與 Sanjay Ghemawat——MapReduce 原作者，Google Fellows。
- Jeffrey Dean and Sanjay Ghemawat, "MapReduce: Simplified Data Processing on Large Clusters", Proceedings of OSDI 2004, USENIX, 2004.
- Sanjay Ghemawat, Howard Gobioff, Shun-Tak Leung, "The Google File System", SOSP 2003——MapReduce 賴以存儲分片的檔案系統。
- John Backus, "Can Programming Be Liberated from the von Neumann Style? A Functional Style and Its Algebra of Programs", ACM Turing Award Lecture, Communications of the ACM 21(8), 1978.
- Matei Zaharia et al., "Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing", NSDI 2012.
- Konstantin Shvachko et al., "The Hadoop Distributed File System", MSST 2010；Doug Cutting, "Hadoop", 2006, https://hadoop.apache.org.
- Harold Abelson, Gerald Jay Sussman, Julie Sussman, "Structure and Interpretation of Computer Programs", MIT Press, 1985——`map`/`reduce` 高階函數思想的教科書源頭。
