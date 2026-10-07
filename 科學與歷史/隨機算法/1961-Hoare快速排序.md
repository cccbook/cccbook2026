# 1961 - Hoare 快速排序

## 案件摘要
1961 年，26 歲的 C. A. R. Hoare 發表快速排序（Quicksort）：分而治之，用一個樞紐（pivot）把陣列分成兩半。這個演算法最壞情況是 $O(n^2)$——但實務上快得驚人。之後的隨機化分析（隨機選樞紐，期望 $O(n \log n)$）成為**隨機算法分析的開山經典**：第一次用機率論嚴格證明「隨機化的演算法平均上遠優於最壞情況」。

## 前因 -- 為什麼會有這個案子
1960 年 Hoare 在莫斯科讀統計系統的機器翻譯計畫，需要按字母順序排序大量單字。當時的排序（合併排序需要額外記憶體；泡沫排序太慢）。Hoare 想到一個**原地、分而治之**的方法：選一個元素當樞紐，把小的放左邊、大的放右邊，再遞迴兩側。

## 線索與推理 -- 數學式、程式、理論

### 演算法

```python
import random

def quicksort(a, lo=0, hi=None):
    if hi is None: hi = len(a) - 1
    if lo >= hi: return a
    p = partition(a, lo, hi)
    quicksort(a, lo, p - 1)
    quicksort(a, p + 1, hi)
    return a

def partition(a, lo, hi):
    pivot = a[hi]                      # 固定選尾端（最壞情況來源）
    i = lo
    for j in range(lo, hi):
        if a[j] <= pivot:
            a[i], a[j] = a[j], a[i]
            i += 1
    a[i], a[hi] = a[hi], a[i]
    return i

random.seed(42)
print(quicksort([3, 1, 4, 1, 5, 9, 2, 6]))  # [1, 1, 2, 3, 4, 5, 6, 9]

def randomized_quicksort(a, lo=0, hi=None):
    if hi is None: hi = len(a) - 1
    if lo >= hi: return a
    r = random.randint(lo, hi)         # 隨機選樞紐！
    a[r], a[hi] = a[hi], a[r]
    p = partition(a, lo, hi)
    randomized_quicksort(a, lo, p - 1)
    randomized_quicksort(a, p + 1, hi)
    return a
```

### 最壞情況
固定選尾端、輸入已排序：每次分割只有一側，遞迴深度 $n$：

$$T(n) = T(n-1) + \Theta(n) \implies T(n) = \Theta(n^2)$$

### 隨機化分析：期望 O(n log n)
隨機選樞紐後，**沒有壞輸入，只有壞運氣**。關鍵技巧：只追蹤「兩兩比較」的機率。設元素排序後為 $z_1 < z_2 < \dots < z_n$，指示變數：

$$X_{ij} = [\,z_i \text{ 與 } z_j \text{ 被比較}\,]$$

比較總數 $X = \sum_{i<j} X_{ij}$。$z_i, z_j$ 被比較**若且唯若兩者中先被選為樞紐**（一旦有第三者介入其間，兩者就分開不再比較）：

$$P(X_{ij} = 1) = \frac{2}{j - i + 1}$$

於是：

$$E[X] = \sum_{i=1}^{n} \sum_{j=i+1}^{n} \frac{2}{j-i+1} = 2\sum_{d=1}^{n-1} \frac{n-d}{d+1} = O(n \log n)$$

（用調和級數 $\sum 1/d = \ln n + O(1)$。）

**偵探筆記**：這個「指示變數 + 機率求和」的技巧成為隨機算法分析的標準工具——不追蹤整棵遞迴樹，只算每對元素相遇的機率。

### 高機率界
不只期望值：隨機化 Quicksort 以機率 $\ge 1 - n^{-c}$ 在 $O(c\, n \log n)$ 時間內完成（由 Chernoff 界對遞迴深度的分析）。「壞運氣」發生的機率隨 $n$ 指數級消失。

## 結案 -- 後果與影響
- **隨機化成為設計策略**：Hoare 的分析確立了「隨機化對抗最壞情況輸入」的範式——隨機選樞紐讓**敵人無法預測**演算法行為。
- **實務標準**：C 語言 `qsort`、Java `Arrays.sort`（基本型別）、各種函式庫的排序核心。
- **選擇問題**：Hoare 的隨機選擇（quickselect，1971）期望 $O(n)$ 找第 $k$ 小——同一招的延伸。
- **對手模型**：Yao 原理（1985，見 `1985-Yao計算隨機性.md`）把「隨機化輸入 vs 隨機化演算法」的關係形式化，其思想源頭正是 Quicksort 分析。
- **平滑分析的先聲**：「為什麼實務很快、理論最壞很慘」之謎（Spielman–Teng 2004 最終解決，見 `2004-SpielmanTeng平滑分析.md`）從 Quicksort 開始發酵。

## 關鍵人物與文獻
- **Tony Hoare**（1934–2025）：Quicksort (1961, Comm. ACM)、quickselect；圖靈獎 1980
- 交叉參照：`1985-Yao計算隨機性.md`、`1989-Karger最小割.md`、`2004-SpielmanTeng平滑分析.md`
