# 1998-PageRank與Google

## 案件摘要

1998 年，史丹佛大學博士生 Larry Page 與 Sergey Brin 在 WWW 會議上發表《The Anatomy of a Large-Scale Hypertextual Web Search Engine》，公開了一個即將改變網路世界的演算法：PageRank。這樁「案子」的核心謎題是：如何在擁有數十億網頁、且充滿垃圾操縱的網路上，客觀地判斷「哪些網頁最重要」？他們的破案關鍵不在語義分析，而在網路的結構本身——把每一條超連結視為一張「選票」，再用馬可夫鏈的平穩分佈算出全局權威。這個源自 Eugene Garfield 1960 年代引文分析的思想，最終成為 Google 的數學心臟。

## 前因 -- 為什麼會有這個案子

- 1990 年代的搜尋引擎（AltaVista、Lycos、Yahoo）主要依賴關鍵詞匹配與 TF-IDF 排序，完全不看網頁之間的連結結構。
- 這種設計極易被操縱：網頁作者只要在頁面裡堆砌熱門關鍵詞（keyword stuffing，甚至用白色文字藏在背景裡），就能讓垃圾頁面擠進搜尋結果前排。
- 資訊科學家 Eugene Garfield 早在 1964 年便創立科學引文索引（SCI），主張「引用次數即重要性」：一篇論文被引用得越多，越可能是重要文獻；被重要論文引用，權重更高。
- 超連結與學術引用結構同構：連結 = 引用，入鏈數 = 被引次數。Garfield 的引文分析因此可以直接移植到 web 上。
- 1996 年，Page 與 Brin 在史丹佛啟動 BackRub 專案，爬取整個網路的連結圖，實驗「以連結投票」的排序想法，PageRank 是這個專案的產物。
- 剩下的難題是數學上的：如何在數億節點的循環連結圖上，定義一個「全域重要性」且能實際算得出來。

## 線索與推理 -- 數學式、程式、理論

### 線索一：連結即投票

最基本的想法：一個網頁的重要性等於指向它的鏈結的加權總和。但若只數入鏈，會遇到循環（A 投 B、B 投 A）與權威傳遞的難題——需要一個能處理整張圖的定義。

### 線索二：PageRank 的遞迴定義

PageRank 給每個網頁 $p_i$ 一個分數，由所有指向它的頁面按其出鏈數分配：

$$
PR(p_i) = \frac{1-d}{N} + d \sum_{p_j \in M(p_i)} \frac{PR(p_j)}{L(p_j)}
$$

其中 $N$ 是網頁總數，$L(p_j)$ 是頁面 $p_j$ 的出鏈數，$d \approx 0.85$ 是阻尼係數（damping factor）。這是一組互相引用的方程：每頁的分數取決於其他頁的分數。

### 線索三：隨機漫遊的馬可夫鏈解釋（破案時刻）

把上式改寫成矩陣形式，PageRank 正是「隨機漫遊者（random surfer）」模型下馬可夫鏈的平穩分佈（stationary distribution）：想像一個網路衝浪者，每一步以機率 $d$ 隨機點擊目前頁面上的一條連結，以機率 $1-d$ 跳到網路上任一頁。他長期停留在各頁的機率，就是該頁的 PageRank。

$$
\mathbf{x}_{k+1} = M \mathbf{x}_k, \qquad \lim_{k \to \infty} \mathbf{x}_k = \pi
$$

由 Perron-Frobenius 定理，當轉移矩陣 $M$ 為隨機矩陣且圖強連通（正向量、不可約），平穩分佈 $\pi$ 存在且唯一，與初始值無關。這就是破案時刻：全域重要性不僅有明確定義，還有唯一解。

### 線索四：阻尼係數的雙重作用

- 懸空節點（dangling nodes，沒有出鏈的頁面）會讓機率「漏掉」，破壞隨機矩陣性質；阻尼項 $1-d$ 相當於隨時可以傳送（teleport）到任意頁，補回流失的機率質量。
- 數學上，傳送保證 $M$ 成為不可約、非週期的隨機矩陣，使冪迭代法（power iteration）必然收斂到唯一平穩分佈，收斂速率約為 $d^k$。

### 線索五：與 TF-IDF 的對照

TF-IDF 衡量的是「這個詞在這頁有多獨特」，屬於語義層面的內容相關性；PageRank 衡量的是「這頁在整張網路圖中有多權威」，屬於結構層面的全域訊號。兩者互相獨立，恰好互補——這正是 Google 排序強於同時代引擎的原因。

### 程式：Python 實作 PageRank（冪迭代）

```python
import numpy as np

def pagerank(adj, d=0.85, tol=1e-10, max_iter=1000):
    n = len(adj)
    adj = np.asarray(adj, dtype=float)
    out = adj.sum(axis=0)          # 每欄的出鏈數
    M = np.where(out > 0, adj / out, 1.0 / n)  # 處理懸空節點
    M = d * M + (1 - d) / n        # 傳送矩陣
    x = np.ones(n) / n             # 均勻初始值
    for k in range(max_iter):
        x_new = M @ x              # 冪迭代
        if np.linalg.norm(x_new - x, 1) < tol:
            return x_new, k + 1
        x = x_new
    return x, max_iter

# 小圖：A<->B 互相連結，A、B 都指向 C，C 只指向 A
adj = {
    "A->A": 0, "A->B": 1, "A->C": 1,
    "B->A": 1, "B->B": 0, "B->C": 1,
    "C->A": 1, "C->B": 0, "C->C": 0,
}
G = np.array([[0, 1, 1],
              [1, 0, 1],
              [1, 0, 0]])  # 欄 j = 頁 j 指向的頁

pr, iters = pagerank(G)
print(f"收斂迭代次數: {iters}")
for name, score in zip("ABC", pr):
    print(f"PR({name}) = {score:.4f}")
print(f"總和 = {pr.sum():.4f}")   # 應為 1.0（平穩分佈為機率分佈）
```

執行後可見分數收斂且總和為 1，驗證了平穩分佈的存在性；C 雖然只有一條入鏈，仍因「從高權威頁面獲得選票」而取得可觀分數。

## 結案 -- 後果與影響

- 1998 年 Page 與 Brin 據此創立 Google，PageRank 成為其搜尋引擎的數學心臟，讓 Google 在品質上碾壓 AltaVista 與 Yahoo。
- 馬可夫鏈平穩分佈首次獲得如此大規模的工業應用，線性代數與機率論在 web 工程中的地位自此確立。
- 「連結 = 投票」成為 web 的治理哲學，影響了後續的 HITS、TrustRank 等連結分析演算法。
- 有投票就有選戰：連結農場（link farms）與付費連結催生了 SEO 產業，Google 展開長達數十年的操縱與反操縱軍備競賽（PageRank 後來不再公開更新）。
- 隨機漫遊思想延伸出 random walk with restart，成為推薦系統（Personalized PageRank）與圖神經網路中鄰居取樣的理論基礎。

## 關鍵人物與文獻

- Larry Page：史丹佛博士生，BackRub 專案與 PageRank 的提出者，後為 Google 共同創辦人。
- Sergey Brin：史丹佛博士生，負責大規模爬蟲與系統工程，Google 共同創辦人。
- Eugene Garfield：資訊科學家，SCI 創立者，引文分析思想的源頭。
- 關鍵文獻：
  - Brin, S., & Page, L. (1998). The Anatomy of a Large-Scale Hypertextual Web Search Engine. Computer Networks and ISDN Systems, 30(1-7), 107-117.（WWW 1998 會議論文）
  - Page, L., Brin, S., Motwani, R., & Winograd, T. (1999). The PageRank Citation Ranking: Bringing Order to the Web. Stanford InfoLab Technical Report.
  - Garfield, E. (1979). Citation Indexing: Its Theory and Application in Science, Technology, and Humanities. John Wiley & Sons.
