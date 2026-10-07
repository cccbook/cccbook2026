# 1989 - Karger 最小割

## 案件摘要
1989 年，還是 MIT 博士生的 David Karger 提出**收縮算法（Contraction Algorithm）**：找圖的全域最小割，只需反覆「隨機選一條邊、把兩端點合併」，直到剩兩個點——就這麼簡單，$O(n^2)$ 一次成功率 $2/n^{2}$，重複 $O(n^2 \log n)$ 次後錯誤機率指數級消失。這個算法的驚人之處：**它不知道任何深度結構，卻能找到最脆弱的連接**——「瞎貓碰死耗子」被證明是優雅而正確的算法，也開啟了 Karger 的隨機化圖算法帝國。

## 前因 -- 為什麼會有這個案子
全域最小割：把圖分成兩部分的最少邊數（網路容錯、電路分割、聚類的核心問題）。1989 年前的最佳確定性算法（Stoer–Wagner 之前）基於最大流，複雜 $O(n^3)$ 或更高，且實作繁瑣。Karger 的問題：**這個問題的結構，能否用「無知」的隨機化捕捉？**

## 線索與推理 -- 數學式、程式、理論

### 收縮算法
```
Contraction(G):
    while |V| > 2:
        隨機選一條邊 (u, v)
        合併 u, v 成一點（自環刪除，平行邊保留）
    剩下的邊集 = 一個候選割
```

每次收縮少一個點、至少少一條邊。**直覺**：平行邊多的「粗管」（大概率不是最小割）難被選中，細管（可能屬於最小割）容易被選中——但收縮越少，最小割越安全。

### 成功率分析
**關鍵引理**：若圖的最小割為 $k$（$k$ 條邊），則圖的邊數 $\ge kn/2$（每點度數 $\ge k$）。

一次隨機收縮選中某條最小割邊的機率：

$$P(\text{選中割邊}) \le \frac{k}{kn/2} = \frac{2}{n}$$

**反向**：不選中的機率 $\ge 1 - 2/n$。要完整保住最小割，需在 $n-2$ 次收縮中**都不選中**：

$$P(\text{成功}) \ge \left(1-\frac{2}{n}\right)\left(1-\frac{2}{n-1}\right)\cdots\left(1-\frac{2}{3}\right) = \frac{2}{n(n-1)}$$

（連乘 telescopically：$\prod_{i=3}^{n} \frac{i-2}{i} = \frac{2}{n(n-1)}$。）

**錯誤放大**：重複 $N = c n^2 \ln n$ 次取最好：

$$P(\text{全失敗}) \le \left(1 - \frac{2}{n^2}\right)^{c n^2 \ln n} \le n^{-2c}$$

**偵探筆記**：分析的推理是「機會追蹤」——不問「最小割在哪」，只問「每次收縮傷害最小割的機率多小」。**乘積式機率分析**（每步的存活機率連乘）成為隨機圖算法的標準技術。

### 程式碼：Karger 收縮

```python
import random

def karger_contract(vertices, edges):
    """vertices: 點集；edges: [(u, v), ...]（允許平行邊）"""
    v_set = set(vertices)
    e_list = list(edges)
    while len(v_set) > 2:
        u, v = random.choice(e_list)
        # 合併 v 進 u：先改標籤，再刪自環
        e_list = [(u if a == v else a, u if b == v else b)
                  for a, b in e_list]
        e_list = [e for e in e_list if e[0] != e[1]]
        v_set.discard(v)
    return e_list                       # 剩下的邊 = 候選割

def karger_min_cut(vertices, edges, N):
    best = None
    for _ in range(N):
        cut = karger_contract(vertices, edges)
        if best is None or len(cut) < len(best):
            best = cut
    return best

random.seed(42)
V = list(range(8))
E = [(0,1),(0,1),(1,2),(2,3),(2,3),(3,4),(3,4),(4,5),(5,6),(5,6),(6,7),(7,0)]
# 最小割是 2（例如割 (1,2),(2,3) 之間的邊… 實際上此圖多處 k=2）
cut = karger_min_cut(V, E, N=500)
print(f"最小割大小 = {len(cut)}：{cut}")
```

### 改進：Karger–Stein (1996)
收縮到 $\lceil n/\sqrt{2} \rceil$ 個點就**分叉重複**（兩份遞迴），成功機率從 $2/n^2$ 提升到 $1/\log n$ 級：

$$T(n) = 2T(n/\sqrt{2}) + O(n^2) \implies T(n) = O(n^2 \log n)$$

**至今這是接近最快的全域最小割算法之一**（確定性算法至今沒有 $O(n^2)$）。

## 結案 -- 後果與影響
- **隨機化擊敗確定性**：Karger 收縮比當時所有確定性算法都簡單且漸進相當——隨機算法學科的最美範例。
- **Karger–Stein**：$O(n^2 \log n)$ 至今是實務與理論的參考點（2019 年有利用現代最大流的 $m^{1+o(1)}$ 算法）。
- **網路可靠性**：CDN、P2P 網路的容錯分析、社交網路的社群偵測。
- **隨機收縮的技術**：混合時間分析、圖上的隨機過程（PageRank、隨機漫步）。
- **Karger 的帝國**：隨機最小生成樹（1995，見 `1995-KargerKleinTarjan隨機MST.md`）、割樹（cut tree）、網路可靠性的隨機算法。

## 關鍵人物與文獻
- **David Karger**（1967–）：MIT 教授；Contraction Algorithm (1989)、Karger–Stein (1996)
- **Clifford Stein**：Karger–Stein 共同作者
- Karger: Random sampling in cut, flow, and network design (1994, PhD thesis / STOC)
- 交叉參照：`1961-Hoare快速排序.md`、`1995-KargerKleinTarjan隨機MST.md`、`1985-Yao計算隨機性.md`
