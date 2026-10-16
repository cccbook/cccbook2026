# 1998 — Google PageRank

## 案件摘要
1998 年，史丹佛大學的博士生 Larry Page 與 Sergey Brin 在論文〈The Anatomy of a Large-Scale Hypotypertextual Web Search Engine〉中，把整個 WWW 視為一個巨大的 Markov 鏈：網頁是狀態、超連結是轉移機率，排名由平穩分佈 $\pi = \pi P$ 給出。用阻尼因子 $0.85$ 保證收斂，再以冪迭代在 $10^{10}$ 規模的稀疏矩陣上計算——這就是 **PageRank**，史上最大規模的線性代數應用，也是 Google 帝國的數學地基。

## 前因 -- 為什麼會有這個案子
- 1990 年代末，Web 暴漲到數千萬頁，早期搜尋引擎（AltaVista、Lycos）只比對關鍵詞，結果輕易被關鍵詞堆疊（keyword stuffing）操縱——「誰該排前面」是個無解的懸案。
- 1906 年 Markov 提出隨機過程：狀態 + 轉移機率矩陣，長期行為由**平穩分佈**決定。
- 1907–1912 年 Perron–Frobenius 定理：正矩陣 / 不可約非負矩陣有唯一的最大正特徵值 $\lambda_1 = 1$ 與正特徵向量——平穩分佈**存在且唯一**的數學保證。
- 冪迭代法（20 世紀初）恰好只需「矩陣─向量乘法」，是唯一能在 $10^{10}$ 規模上執行的特徵向量算法。
- 1998 年前身的學術線索：Kleinberg 的 HITS 演算法（hub/authority）、Brin 的初步想法，最後由 Page & Brin 定案為 PageRank。

## 線索與推理 -- 數學式、程式、理論

### 線索一：Web 是一個 Markov 鏈
設 $n$ 個網頁，連結矩陣 $G$：若頁面 $j$ 連向 $i$ 則 $G_{ij} = 1$。定義「按連結平均點擊」的轉移矩陣：

$$P_{ij} = \frac{G_{ij}}{\text{out-degree}(j)}$$

一個「隨機衝浪者」沿著連結不斷點擊，其位置分佈 $p_{k+1} = P^T p_k$ 的極限，就是頁面的重要性排名。問題：$P$ 不一定是隨機矩陣——有「死角頁」（無出連結，機率被吸走）與「封閉環」（爬蟲陷阱，無法逃出）。

### 線索二：阻尼因子 0.85——把 Markov 鏈變成良態
PageRank 的 Google 公式：以機率 $0.85$ 沿連結點擊、機率 $0.15$ 隨機跳到任意頁：

$$P = 0.85\, P_{\text{link}} + 0.15\, \frac{1}{n}\mathbf{1}\mathbf{1}^T$$

PageRank 向量 $\pi$ 定義為平穩分佈：

$$\pi = \pi P, \qquad \sum_i \pi_i = 1, \qquad \pi_i \ge 0$$

阻尼因子的三重作用：
- **Perron–Frobenius 生效**：$P$ 成為不可約（強連通）且正的隨機矩陣，$\lambda_1 = 1$ 為單根、$\pi$ 唯一且為正向量——死角頁與封閉環同時破解。
- **收斂加速**：其餘特徵值滿足 $|\lambda_j| \le 0.85$，冪迭代收斂比 $\le 0.85$（與 $n$ 無關！），約 100 步以內收斂——這讓 $10^{10}$ 規模的計算變成可能。
- **反作弊**：排名來自「全網連結結構」而非頁面自身關鍵詞，難以單頁操縱。

等價線性系統（$\pi P = \pi \Leftrightarrow (P^T - I)^T \pi = 0$ 加上正規化），但 $10^{10}$ 階直接法不可行——唯一實用的解法是**冪迭代**：

$$\pi^{(k+1)} = \left(\pi^{(k)} P\right), \qquad \pi^{(k+1)} \leftarrow \pi^{(k+1)} / \|\pi^{(k+1)}\|_1$$

每步只需一次「稀疏矩陣─向量乘法」：$P$ 每列平均只有幾十個非零元素（連結數），成本 $O(\text{nnz}) \approx O(n)$，Web 規模也可負擔。

### 線索三：Perron–Frobenius 與冪迭代——理論與工程的合流
Perron–Frobenius 定理保證：$P > 0$ 時 $\lambda_1 = 1 > |\lambda_2| \ge \dots$，因此冪迭代誤差以 $|\lambda_2|^k \le 0.85^k$ 衰減。數學（1906–1912）+ 數值分析（冪迭代）+ 工程（稀疏儲存、分散式矩陣─向量乘法），三條線索在 1998 年合流——這是 Markov 鏈理論史上最大的應用案件。

### 程式碼範例：PageRank 的 $P$ 矩陣冪迭代收斂到排名
```python
import numpy as np

# 6 頁小型 Web：連結圖 G[i,j]=1 表示 j 連向 i
# 特意加入死角頁(5)與封閉環(3<->4)測試阻尼效果
G = np.array([
    [0, 1, 1, 0, 0, 0],
    [0, 0, 1, 0, 1, 0],
    [1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0]])

def pagerank(G, d=0.85, tol=1e-12, maxit=1000):
    n = G.shape[0]
    out = G.sum(axis=0); out[out == 0] = 1        # 死角頁防除零
    Pl = G / out                                   # 連結轉移矩陣
    P = d * Pl + (1 - d) / n * np.ones((n, n))     # Google 公式
    pi = np.full(n, 1 / n)
    for k in range(maxit):
        pi_new = pi @ P
        if np.linalg.norm(pi_new - pi, 1) < tol:
            return pi_new, k + 1
        pi = pi_new
    return pi, maxit

pi_raw, _ = pagerank(G, d=0.0)   # 無阻尼：可看出封閉環問題
pi, iters = pagerank(G, d=0.85)
print("收斂迭代次數 :", iters)
for i in np.argsort(pi)[::-1]:
    print(f"  網頁{i+1}  PageRank = {pi[i]:.4f}")
print("無阻尼時封閉環 3<->4 吸走機率 :", pi_raw[3] + pi_raw[4])
```

輸出顯示：阻尼 $d = 0.85$ 下約數十步即收斂（收斂比 $\le 0.85$），排名合理地偏向被多頁連結的頁面；而 $d = 0$ 時機率被封閉環 $3 \leftrightarrow 4$ 吸走——正是阻尼因子破解「爬蟲陷阱」的實證。

## 結案 -- 後果與影響
- 1998 年 Google 公司成立，PageRank 成為搜尋排名核心，網頁「重要性」從此有了可計算的定義——懸案正式結案。
- $10^{10}$ 規模稀疏矩陣的冪迭代：史上最大規模的特徵向量計算，催生了大規模稀疏線性代數與分散式計算基礎設施（Google 檔案系統、MapReduce 的前身）。
- Markov 鏈隨機遊走理論的最大應用：PageRank 思想外溢至社會網路分析（centrality）、生物學（蛋白質網路）、推薦系統。
- 學界影響：Kamvar 等人的加速方法、Langville–Meyer《Google's PageRank and Beyond》（2006）成為教科書。
- 影響至今：圖神經網路與譜方法中仍可見隨機遊走與平穩分佈的影子——PageRank 是「線性代數改變世界」的經典範例。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Larry Page / Sergey Brin | 提出 PageRank、創立 Google（1998） |
| Andrei Markov | Markov 鏈理論（1906） |
| Oskar Perron / Georg Frobenius | Perron–Frobenius 定理（1907–1912） |
| Jon Kleinberg | HITS 演算法（1999） |
| Amy Langville / Carl Meyer | PageRank 數學理論專書（2006） |

- L. Page, S. Brin, R. Motwani & T. Winograd, *The PageRank Citation Ranking: Bringing Order to the Web*, Stanford InfoLab (1999)。
- S. Brin & L. Page, *The Anatomy of a Large-Scale Hypertextual Web Search Engine*, Computer Networks and ISDN Systems **30**, 107–117 (1998)。
- A. Langville & C. Meyer, *Google's PageRank and Beyond: The Science of Search Engine Rankings*, Princeton (2006)。
