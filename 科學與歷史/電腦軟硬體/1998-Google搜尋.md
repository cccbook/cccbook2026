# 1998-Google搜尋：用特徵向量統治網路

## 案件摘要
1998 年 9 月，史丹佛兩位博士生 Larry Page 與 Sergey Brin 在車庫創立 Google。他們的武器不是更快的硬體，而是一個數學演算法——PageRank：把整個網路當成一張巨型的隨機矩陣，用特徵向量替每個網頁算出「重要性」。

## 前因 -- 為什麼會有這個案子
- **1990 年代搜尋的品質危機**：AltaVista、Yahoo 等搜尋引擎依賴網頁本身的關鍵字（詞頻、meta 標籤），結果被垃圾站用「關鍵字堆砌」輕易操縱。搜尋品質每況愈下。
- **學術引用的啟示**：學術界早就用「被引用次數」衡量論文重要性（Science Citation Index, 1964）。Page 與 Brin 的洞見：**超連結 = 引用 = 推薦**。一個網頁被越多重要網頁連結，就越重要。
- **遞迴的難題**：「重要網頁推薦的才有效」——但「重要」本身又待定義。這形成自指遞迴，看似雞生蛋問題，實則是標準的線性代數：不動點（fixed point）問題。
- **兩人背景**：Larry Page 出身密西根大學（父母皆是電腦教授），Sergey Brin 是蘇聯移民數學天才。1996 年在史丹佛合作 BackRub 專案，1998 年拿到 Sun 創辦人 Andy Bechtolsheim 的 10 萬美元支票後正式成立 Google。

## 線索與推理 -- 數學式、程式、理論

### PageRank 演算法

$$PR(p) = \frac{1-d}{N} + d\sum_{q \in M(p)} \frac{PR(q)}{L(q)}$$

其中：
- $N$：全網網頁總數
- $d$：阻尼因子（damping factor），通常 $d = 0.85$，表示隨機跳轉者有 $d$ 機率沿連結走、$1-d$ 機率隨機跳到任一頁
- $M(p)$：所有連結到 $p$ 的網頁集合
- $L(q)$：網頁 $q$ 的出鏈總數（把 $PR(q)$ 平分給它推薦的每頁）

這是自指方程組，可改寫成矩陣形式的不動點問題。設 $M$ 為列隨機轉移矩陣（$M_{ij}$ = 從頁 $j$ 走到頁 $i$ 的機率），則：

$$PR = dM \cdot PR + \frac{1-d}{N}\mathbf{1}$$

整理得：

$$(I - dM)\,PR = \frac{1-d}{N}\mathbf{1}$$

由 Perron–Frobenius 定理，隨機矩陣 $G = dM + \frac{1-d}{N}\mathbf{1}\mathbf{1}^T$ 存在唯一的最大特徵值 $\lambda_1 = 1$，對應的特徵向量即為 PageRank：

$$G \cdot PR = \lambda_1 \cdot PR = 1 \cdot PR$$

阻尼因子 $d$ 的妙用：它保證 $G$ 是正矩陣（每個元素 $> 0$），使鏈路圖強連通、特徵向量唯一且疮度收斂——純數學保證了演算法不會發散、不會陷入「蜘蛛網孤島」。

### Python numpy 實作 PageRank 疊代

```python
import numpy as np

def pagerank(links, d=0.85, tol=1e-8, max_iter=1000):
    """links: dict, 頁面 -> 出鏈到的頁面列表"""
    pages = sorted(links)
    N = len(pages)
    idx = {p: i for i, p in enumerate(pages)}

    # 建轉移矩陣 M：M[i][j] = 從頁 j 走到頁 i 的機率
    M = np.zeros((N, N))
    for p, outs in links.items():
        if outs:
            for q in outs:
                M[idx[q], idx[p]] = 1.0 / len(outs)
        else:  # 無出鏈（dead end）：平分給所有頁
            M[:, idx[p]] = 1.0 / N

    pr = np.ones(N) / N                      # 均勻初始值
    for _ in range(max_iter):
        new = d * M @ pr + (1 - d) / N       # 不動點疊代
        if np.linalg.norm(new - pr, 1) < tol:
            break
        pr = new
    return dict(zip(pages, pr))

web = {
    "A": ["B", "C"],
    "B": ["C"],
    "C": ["A"],
    "D": ["C"],
}
ranks = pagerank(web)
for p, r in sorted(ranks.items(), key=lambda x: -x[1]):
    print(f"{p}: {r:.4f}")
# C 最重要（被最多頁推薦），D 幾乎為零（只出不進）
```

疊代收斂速度由第二大特徵值決定：

$$\|PR_{k+1} - PR^*\| \leq d \cdot \|PR_k - PR^*\|$$

誤差每輪至少衰減 $d = 0.85$ 倍，約 100 輪內收斂——1998 年的網路僅數千萬頁，數台電腦即可算完全網排名。

### Backlink 哲學與商業模式
- **backlink 哲學**：搜尋排名不由廣告費決定，而由「網路民主投票」決定——每條超連結是一票，重要網頁的票更重。垃圾關鍵字堆砌瞬間失效，因為垃圾站得不到 backlink。
- **AdWords（2000 年 10 月）**：商業模式的破格——廣告與搜尋結果嚴格分離，用競價（CPC）排序廣告。數學化：廣告排序分數 = 競價 × 點擊率預估值

$$\text{AdRank} = \text{bid} \times E[\text{CTR} \mid \text{query}]$$

「不干擾搜尋結果」反而贏得信任，成就史上最賺錢的廣告機器。

## 結案 -- 後果與影響
- Google 於 2004 年上市，市值數百億美元；2015 年重組為 Alphabet。
- PageRank 思想外溢：Google 的 Web Spam 排序、社交網路影響力分析、蛋白質交互網路、區塊鏈共識評估，處處可見特徵向量的影子。
- 「資料 + 演算法 > 硬體」成為網路時代的鐵律；Google 進一步推動分散式運算（MapReduce, 2004）、大數據與 AI 時代的來臨。
- 搜尋從「找檔案」變成「組織全世界的資訊」——Google 的使命宣言由此而來。

## 關鍵人物與文獻
- **Larry Page & Sergey Brin**：〈The Anatomy of a Large-Scale Hypertextual Web Search Engine〉（1998）
- **Sergey Brin & Lawrence Page**：〈The PageRank Citation Ranking: Bringing Order to the Web〉（1999）
- **Andy Bechtolsheim**：Sun 共同創辦人，第一張 10 萬美元支票的伯樂
- **Jon Kleinberg**：HITS 演算法（1999）——同期獨立的 hub/authority 排名理論
- **Perron & Frobenius**：非負矩陣譜理論——PageRank 背後的數學支柱
