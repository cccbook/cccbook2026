# 1995 - Karger–Klein–Tarjan 隨機最小生成樹

## 案件摘要
1995 年，Karger、Klein 與 Tarjan 發表《A Randomized Linear-Time Algorithm to Find Minimum Spanning Trees》：用隨機取樣 + 驗證（Borůvka 步驟），實現**期望線性時間 $O(m)$** 的最小生成樹算法。這是「隨機化突破確定性下界感覺」的里程碑——確定性算法經過數十年仍停在 $O(m \alpha(m,n))$，隨機化輕鬆達到線性。**取樣 + 驗證**的兩段式設計成為隨機化圖算法的新範式。

## 前因 -- 為什麼會有這個案子
最小生成樹（MST）是圖算法的百年經典：Borůvka (1926)、Kruskal (1956)、Prim (1957) 的算法是 $O(m \log m)$；Chazelle (2000) 的軟堆達到 $O(m \alpha(m,n))$（反 Ackermann，實務上近線性但理論不是）。**問題**：MST 能否線性時間？確定性答案卡了幾十年。Karger 的洞察：**隨機取樣把問題「分而治之」**——採樣一小部分邊，其 MST 結構告訴我們哪些邊「安全」可丟棄。

## 線索與推理 -- 數學式、程式、理論

### 兩個關鍵引理
**採樣引理（Sampling Lemma）**：隨機獨立取樣每條邊機率 $p$，得子圖 $G_p$。對 $G_p$ 的 MST $F$，原圖中「比 $F$ 中路徑上所有邊都重」的邊（F-heavy 邊）數量期望值：

$$E[\#\text{F-heavy 邊}] \le \frac{n-1}{p} \cdot \frac{1}{1 - 2p/3}\cdot\ldots \quad \text{（取 } p = 1/2 \text{ 時 } E \le 2(n-1) \cdot c\text{）}$$

**直覺**：F-heavy 邊在原圖的任何環上都「太重」——隨機子圖的 MST 捕捉了這個結構。取 $p=1/2$ 時，F-heavy 邊期望只有 $O(n)$ 條，**可以安全丟棄**（它們不可能在原圖 MST 中）。

**驗證引理**：給定生成樹 $F$，判定每條邊是否 F-heavy，$O(m + n)$ 時間（用最小生成樹驗證算法，Komlós 1985 的線性時間驗證）。

### 演算法
```
KKT(G):
    1. Borůvka 步驟數輪：收縮安全邊，點數至少減半 -> G'（O(m)）
    2. 隨機取樣 G' 每條邊機率 1/2 -> G_p
    3. 遞迴 KKT(G_p) 得 F
    4. 驗證 G' 中每條邊相對 F 是否 heavy；丟棄 heavy 邊 -> G''
    5. 遞迴 KKT(G'') 得 F'
    6. 回答：F ∪ F'（加上 Borůvka 邊）
```

**遞迴分析**：每層點數減半、邊數從 $m$ 到 $m/2$（採樣）再 $O(n)$（驗證後丟棄）：

$$T(m, n) = T(m/2, n/2) + T(O(n), n/2) + O(m)$$

解得：

$$T(m, n) = O(m) \quad \text{期望線性時間！}$$

### 程式碼：概念骨架（Kruskal 風格簡化）

```python
import random

def kruskal_mst(n, edges):
    """edges: [(w, u, v), ...]"""
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    mst, total = [], 0
    for w, u, v in sorted(edges):          # Kruskal: O(m log m)
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
            mst.append((u, v)); total += w
    return mst, total

random.seed(42)
n = 10
edges = [(random.randint(1, 100), i, j)
         for i in range(n) for j in range(i+1, n)]
mst, total = kruskal_mst(n, edges)
print(f"MST 權重 = {total}，邊數 = {len(mst)}（應為 n-1 = {n-1}）")

# KKT 的核心思想：隨機取樣一半邊 -> 遞迴求 MST -> 驗證丟棄 heavy 邊
# 期望 O(m)，確定性算法至今未達到
```

### 「取樣 + 驗證」的範式
KKT 的設計模式成為隨機化圖算法的範本：

1. **隨機取樣**：從大問題抽小樣本（$m \to m/2$）
2. **遞迴求解**：在小樣本上解（便宜）
3. **驗證/丟棄**：用樣本的解過濾原問題（線性時間）

**偵探筆記**：這個模式與 Rabin 指紋（見 `1981-Rabin指紋比對.md`）異曲同工——**用隨機樣本的結構性質過濾大物件的候選**。取樣引理的證明同樣是「機會追蹤」：F-heavy 邊被採樣「暴露」的機率分析。

## 結案 -- 後果與影響
- **線性時間 MST**：期望 $O(m)$ 至今是最快的（Chazelle 2000 確定性 $O(m\alpha)$ 仍非線性）。
- **隨機化圖算法的範式**：取樣+驗證出現在最小割、连通分量、動態圖算法中。
- **動態 MST**：Karger 的技術延伸到動態圖（邊插入刪除下維護 MST）。
- **Petit 的實務**：隨機化算法在實務上也極快，常被函式庫採用。
- **理論意義**：證明「隨機化能突破確定性漸進下界的感覺」——雖然 $\alpha(m,n)$ 實務上可忽略，理論上隨機化乾淨地達到 $O(m)$。

## 關鍵人物與文獻
- **David Karger**（1967–）：MIT；收縮算法、採樣引理
- **Philip Klein**（Brown 大學）：圖算法
- **Robert Tarjan**（1948–）：圖靈獎 1986（資料結構與算法分析）
- Karger, Klein, Tarjan: A Randomized Linear-Time Algorithm... (1995, J. ACM)
- **Chazelle**：Soft Heap (2000)——確定性近線性
- 交叉參照：`1989-Karger最小割.md`、`1981-Rabin指紋比對.md`、`1961-Hoare快速排序.md`
