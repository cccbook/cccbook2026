# 1997 - Broder MinHash

## 案件摘要
1997 年，Andrei Broder 在 AltaVista 搜尋引擎工作時發表《Syntactic Clustering of the Web》：要估計兩個大文件（或集合）的相似度，不必比對全部元素——**用隨機雜湊函數 $h$，兩集合的 MinHash（最小雜湊值）相等的機率恰好等於 Jaccard 相似度**：

$$P(\min_{a \in A} h(a) = \min_{b \in B} h(b)) = \frac{|A \cap B|}{|A \cup B|}$$

幾百個 MinHash 就能以小誤差估計十億級集合的相似度。這是「隨機化 = 相似度搜索」的奠基之作，成為搜尋引擎去重、推薦系統、大數據聚類的基礎。

## 前因 -- 為什麼會有這個案子
1997 年的 AltaVista 是最大搜尋引擎，網頁抄襲與鏡像氾濫——要判斷兩個億字元網頁是否「幾乎相同」，逐字比對太貴。Jaccard 相似度：

$$J(A, B) = \frac{|A \cap B|}{|A \cup B|}$$

（$A, B$ 是文件的 shingle 集合——連續 $k$ 個字元的片段。）直接計算需要 $O(|A| + |B|)$ 記憶體與時間，億級集合不可行。Broder 的問題：**能否用遠小的「概要」（sketch）估計 $J$？**

## 線索與推理 -- 數學式、程式、理論

### MinHash 的數學
取全域隨機雜湊函數 $h: U \to [0, 1]$（視為連續均勻；離散時用大值域隨機排列近似）。$A$ 的 MinHash：

$$\min_h(A) = \arg\min_{a \in A} h(a)$$

**定理**：

$$P(\min_h(A) = \min_h(B)) = \frac{|A \cap B|}{|A \cup B|} = J(A, B)$$

**證明**：並集 $A \cup B$ 中，$h$ 的最小值等機率地落在任一元素上（$h$ 均勻隨機）。最小值落在交集元素上 ⟺ 兩集合的 argmin 相同：

$$P = \frac{|A \cap B|}{|A \cup B|} \quad \blacksquare$$

**偵探筆記**：這個證明的美在「對稱」——並集中每個元素地位平等，最小值落在交集的機率就是交集佔比。**把集合相似度變成「一次擲骰子的機率」**。

### 估計與誤差
取 $k$ 個獨立雜湊函數 $h_1, \dots, h_k$，估計

$$\hat{J} = \frac{1}{k}\sum_{i=1}^k [\min_{h_i}(A) = \min_{h_i}(B)]$$

由 Chernoff 界，誤差 $\le \epsilon$ 需要：

$$k = O\left(\frac{1}{\epsilon^2}\right)$$

$\epsilon = 0.05$ 只需 $k \approx 400$ 個 MinHash——**與集合大小無關**！每個 MinHash 只存一個雜湊值，概要大小 $O(k)$。

### 程式碼：MinHash

```python
import random, hashlib

def minhash_signature(A, k=100):
    """A: 元素集合；k 個隨機雜湊"""
    sigs = []
    for i in range(k):
        seed = str(i).encode()
        sigs.append(min(int.from_bytes(
            hashlib.md5(seed + str(a).encode()).digest()[:8], 'big')
            for a in A))
    return sigs

random.seed(42)
doc1 = {f"w{i}" for i in range(100000)}
doc2 = {f"w{i}" for i in range(80000)} | {f"x{i}" for i in range(20000)}
true_j = len(doc1 & doc2) / len(doc1 | doc2)    # = 0.667

s1, s2 = minhash_signature(doc1), minhash_signature(doc2)
est_j = sum(a == b for a, b in zip(s1, s2)) / len(s1)
print(f"真實 Jaccard = {true_j:.3f}，MinHash 估計 = {est_j:.3f}")
# ≈ 0.667：幾百個雜湊值就能估計十萬級集合
```

### LSH：從 MinHash 到大規模搜尋
MinHash 只解決「一對」比較；大規模需要**局部敏感雜湊（LSH）**（Indyk–Motwani 1998）：把 $k$ 個 MinHash 分成 $b$ 個 band（每 band $r$ 個），band 內全相等才碰撞：

$$P(\text{至少一 band 碰撞}) = 1 - (1 - J^r)^b$$

這是 Jaccard 的 S 曲線：相似度高的對幾乎必碰撞，低的幾乎不碰——**可調參數 $b, r$ 控制閾值**。谷歌、Redis、Elasticsearch 的近似相似度搜尋都建立在此。

## 結案 -- 後果與影響
- **搜尋引擎去重**：谷歌、Bing 的網頁鏡像偵測。
- **推薦系統**：協同過濾的用戶/物品相似度，Spark MLlib 內建 MinHash。
- **大數據聚類**：億級文件的 syntactic clustering（Broder 原始應用）。
- **LSH 家族**：近似最近鄰搜尋（Indyk–Motwani 1998）、影像相似度（p-stable LSH）。
- **sketch 理論**：與 Count-Min Sketch（2005，見 `2005-CountMinSketch.md`）、HyperLogLog（2007，見 `2007-HyperLogLog.md`）共同構成串流/概要算法的支柱。

## 關鍵人物與文獻
- **Andrei Broder**（1958–）：AltaVista、IBM、Google；MinHash (1997)
- Broder: Syntactic Clustering of the Web (1997, WWW)
- **Indyk & Motwani**：LSH (1998)
- **Schleimer, Wilkerson, Aiken**：Winnowing (2003)——抄襲偵測的滑動窗口
- 交叉參照：`1984-JohnsonLindenstrauss引理.md`、`1987-KarpRabin字串匹配.md`、`2007-HyperLogLog.md`
