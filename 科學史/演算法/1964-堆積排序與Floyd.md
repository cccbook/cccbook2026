# 1964-堆積排序與Floyd

## 案件摘要

1964 年，加拿大計算機科學家 J.W.J. Williams 在《Communications of the ACM》上發表《Algorithm 232: Heapsort》，提出以「堆積（heap）」這種資料結構實現的排序法。同年 Robert Floyd 以《Algorithm 245: Treesort 3》改良其建堆步驟，把建堆時間從 $O(n \log n)$ 降到 $O(n)$，全案臻於完美：保證 $O(n \log n)$、原地、無額外記憶體。這樁案件同時解開了另一個謎題——優先佇列的高效實現，其影響遠超排序本身。

## 前因 -- 為什麼會有這個案子

- 合併排序雖是 $O(n \log n)$，卻需要 $O(n)$ 的額外記憶體。
- 快速排序原地又快，但最壞情況 $O(n^2)$，對某些應用（如即時系統）無法接受。
- 需要一種「保證 $O(n \log n)$ 且原地」的排序演算法。
- 完全二元樹（complete binary tree）可以完美地塞進陣列而不需指標，這是堆積的物理基礎。
- 優先佇列（priority queue）當時缺乏高效實現，排序之外的需求早已浮現。

## 線索與推理 -- 數學式、程式、理論

### 線索一：堆積的性質

max-heap 是一棵完全二元樹，滿足父節點 $\ge$ 子節點。用陣列表示，節點 $i$ 的父節點為 $(i-1)/2$，子節點為 $2i+1$ 與 $2i+2$，不需任何指標：

$$a[\text{parent}(i)] \ge a[i] \quad \Rightarrow \quad a[0] = \max_i a[i]$$

樹高為 $\lfloor \log_2 n \rfloor$，這是所有複雜度的根源。

### 線索二：sift-down 與 sift-up

- **sift-up（上濾）**：新元素放在尾端，與父節點比較、必要時上移，用於插入，$O(\log n)$。
- **sift-down（下濾）**：元素與較大的子節點比較、必要時下移，用於刪除最大值與建堆，$O(\log n)$。

### 線索三：建堆的複雜度 —— 破案時刻

樸素做法是逐個 sift-up 插入，總計 $O(n \log n)$。Floyd 的改良是「自底向上建堆」：從最後一個非葉節點開始，對每個節點執行 sift-down。因為絕大多數節點都在底層、下濾距離極短，求和級數顯示總工作是線性的：

$$\sum_{h=0}^{\log n} \frac{n}{2^{h+1}} \cdot O(h) = O\left(n \sum_{h=0}^{\log n} \frac{h}{2^{h+1}}\right) = O(n)$$

因為 $\sum_h h/2^{h+1} \le 1$，建堆只需 $O(n)$——這是本案的破案時刻。

### 線索四：排序流程與代價

堆積排序 = 建堆（$O(n)$）+ 反覆把根與尾端交換、對根 sift-down（$n-1$ 次，每次 $O(\log n)$）：

$$T(n) = O(n) + O(n \log n) = O(n \log n)$$

代價有二：一是交換破壞相等元素的相對順序（不穩定排序）；二是 sift-down 的存取模式跨跳陣列（parent $\to 2i+1$），快取局部性不如快排的順序掃描。

### 程式碼示範

```python
import random

def sift_down(a, i, size):
    while True:
        l, r = 2*i + 1, 2*i + 2
        largest = i
        if l < size and a[l] > a[largest]:
            largest = l
        if r < size and a[r] > a[largest]:
            largest = r
        if largest == i:
            return
        a[i], a[largest] = a[largest], a[i]
        i = largest

def build_heap(a):
    n = len(a)
    for i in range(n // 2 - 1, -1, -1):
        sift_down(a, i, n)

def heapsort(a):
    n = len(a)
    build_heap(a)
    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        sift_down(a, 0, end)

data = [random.randint(0, 999) for _ in range(1000)]
heapsort(data)
assert data == sorted(data)
print("heapsort 正確，n =", len(data))
```

`build_heap` 即 Floyd 的 $O(n)$ 自底向上建堆；整體保證 $O(n \log n)$。

## 結案 -- 後果與影響

- 堆積成為優先佇列的標準實現：加速 Dijkstra 最短路徑（從 $O(V^2)$ 到 $O((V+E)\log V)$）與 A* 搜尋。
- Python 的 `heapq` 模組、C++ 的 `priority_queue` 皆以二元堆積為基礎。
- 堆積排序保證 $O(n \log n)$ 且原地，成為嵌入式與即時系統、以及 introsort（快排退化時切換至堆積排序）的安全後盾。
- Floyd 的建堆分析（依層求和、節點高度分布）是攤還分析（amortized analysis）思想的先聲。
- Robert W. Floyd 因在演算法分析方面的貢獻獲 1978 年圖靈獎（其 1962 年的 Floyd-Warshall 全源最短路徑演算法亦是經典）。

## 關鍵人物與文獻

- J.W.J. Williams (1964). Algorithm 232: Heapsort. *Communications of the ACM*, 7(6), 347-338.
- R.W. Floyd (1964). Algorithm 245: Treesort 3. *Communications of the ACM*, 7(12), 701.
- R.W. Floyd (1962). Algorithm 97: Shortest Path. *Communications of the ACM*, 5(6), 345.
- T.H. Cormen, C.E. Leiserson, R.L. Rivest, C. Stein (2022). *Introduction to Algorithms* (4th ed.). MIT Press.（第六章：Heapsort）
- R.W. Floyd (1978). The Paradigms of Programming. *Communications of the ACM*, 22(8), 455-460.（1978 圖靈獎演講）
- D.E. Knuth (1998). *The Art of Computer Programming, Vol. 3: Sorting and Searching* (2nd ed.). Addison-Wesley.（5.2.3 節）
