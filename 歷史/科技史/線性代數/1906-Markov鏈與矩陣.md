# 1906 — Markov 鏈與矩陣

## 案件摘要
1906 年，聖彼得堡的 Andrey Markov 發表論文〈Extension of the law of large numbers to dependent quantities〉，研究一列**相互依賴**的隨機變數：下一步的狀態只依賴當下狀態。他用一個矩陣——後世所稱的**轉移矩陣** $P$——刻劃狀態之間的跳躍機率，並證明即使在依賴的情況下，大數法則依然成立：長期頻率收斂到**穩態分布**。隨機過程理論的偵探檔案，就此立案。

## 前因 -- 為什麼會有這個案子
- **1713 年 Bernoulli 大數法則**：Jacob Bernoulli 證明獨立重複試驗中，頻率 $\hat{p} \to p$。但整個 19 世紀，機率論幾乎都以「獨立性」為前提。
- **1866 年 Chebyshev 學派**：Markov 的老師 Chebyshev 用初等方法證明大數法則的推廣，但方法仍限於相當特殊的依賴形式。
- **矩陣譜理論成熟**：Cayley（1858）的矩陣代數、Perron（1907）與 Frobenius（1912）稍後證明的正矩陣譜定理（其中 Frobenius 的工作部分正是受 Markov 鏈問題刺激），為「矩陣冪收斂」提供了代數工具。
- **案發導火線**：Nekrasov 主張大數法則需要獨立性；Markov 決心用一個**最簡單的依賴模型**反駁他——這就是馬可夫鏈的誕生動機。

## 線索與推理 -- 數學式、程式、理論

### 線索一：馬可夫鏈與轉移矩陣
設系統有有限個狀態，$P_{ij}$ 為「這一刻在狀態 $i$、下一刻跳到狀態 $j$」的機率，滿足

$$\sum_j P_{ij} = 1, \qquad P_{ij} \geq 0 \quad\Longrightarrow\quad P \text{ 為隨機矩陣（列和為 1）}$$

Markov 的「無記憶性」假設：下一步的條件分布只依賴當前狀態。若 $\pi_n$ 是第 $n$ 步的狀態分布（列向量），則

$$\pi_{n+1} = \pi_n P, \qquad \pi_n = \pi_0 P^n$$

整條隨機過程的命運，被壓縮成一個矩陣的**冪**。Markov 1906 年著名的例子是只有兩個狀態的文字鏈（母音/子音），他還真的分析了 Pushkin《葉甫蓋尼・奧涅金》的前兩萬個字母。

### 線索二：穩態分布與 Perron–Frobenius 定理
穩態分布 $\pi^*$ 滿足不動點方程

$$\pi^* = \pi^* P, \qquad \sum_i \pi_i^* = 1$$

即 $\pi^*$ 是 $P^T$ 對應特徵值 $\lambda = 1$ 的特徵向量。**Perron–Frobenius 定理**保證：若 $P$ 是不可約的非負矩陣（正則鏈：某個 $P^k > 0$），則

- $\lambda = 1$ 是譜半徑 $\rho(P) = 1$ 的單根，且是最大的實特徵值；
- 存在唯一的嚴格正穩態分布 $\pi^*$；
- 對任何初始分布，$\pi_0 P^n \to \pi^*$。

長期行為與起點無關——這就是 Markov 證明的大數法則推廣：狀態頻率收斂到 $\pi^*$，即使變數**相互依賴**。偵探的結論：獨立性不是大數法則的必要條件。

### 線索三：兩狀態鏈的解析驗證
最簡單的案情：兩狀態鏈，轉移矩陣

$$P = \begin{pmatrix} 1-a & a \\ b & 1-b \end{pmatrix}$$

解不動點方程可得穩態分布的顯式解：

$$\pi^* = \left(\frac{b}{a+b},\; \frac{a}{a+b}\right)$$

而 $P^n$ 的冪有解析形式：

$$P^n = \frac{1}{a+b}\begin{pmatrix} b & a \\ b & a \end{pmatrix} + \frac{(1-a-b)^n}{a+b}\begin{pmatrix} a & -a \\ -b & b \end{pmatrix}$$

第二項隨 $n \to \infty$ 消失（當 $|1-a-b| < 1$），剩下的正是穩態。偵探看到兇器逐漸「冷卻」：偏差項 $(1-a-b)^n \to 0$，收斂到穩態分布。

### 線索四：Pushkin 的兩萬個字母
Markov 不只做純理論：1913 年（慶祝三百年數學系紀念的演講）他把《葉甫蓋尼・奧涅金》前兩萬個字母序列化成二狀態鏈（母音/子音），實測得到轉移矩陣約為

$$P = \begin{pmatrix} 0.128 & 0.872 \\ 0.663 & 0.334 \end{pmatrix}$$

穩態分布給出母音占比約 $0.663 / (0.128 + 0.663) \approx 0.43$，與直接統計吻合。這是史上第一次用隨機過程分析文學文本——文字偵探學的開端。

### 程式碼範例：Markov 轉移矩陣冪迭代收斂到穩態分布
```python
import numpy as np

# 三狀態馬可夫鏈：例「晴天 / 多雲 / 雨天」
P = np.array([
    [0.7, 0.2, 0.1],   # 晴 -> 晴/多雲/雨
    [0.3, 0.4, 0.3],   # 多雲 -> ...
    [0.2, 0.3, 0.5],   # 雨 -> ...
])

# 冪迭代：任意初始分布，反覆乘上 P
pi = np.array([1.0, 0.0, 0.0])   # 從「晴天」出發
for n in range(1, 51):
    pi = pi @ P
    if n in (1, 2, 5, 10, 50):
        print(f"n={n:3d}  pi = {np.round(pi, 6)}")

# 驗證一：不動點方程 pi* P = pi*
print("檢驗 pi@P == pi :", np.allclose(pi @ P, pi, atol=1e-12))

# 驗證二：與線性代數解（P^T 的特徵向量）比對
vals, vecs = np.linalg.eig(P.T)
pi_star = np.real(vecs[:, np.argmin(np.abs(vals - 1))])
pi_star /= pi_star.sum()
print("特徵向量法 pi* =", np.round(pi_star, 6))

# 驗證三：Perron-Frobenius——譜半徑為 1 且為單根
print("譜半徑 =", round(max(abs(vals)), 12))
```

執行可見：無論從哪個初始分布出發，$\pi_n = \pi_0 P^n$ 在數十步內收斂到同一個穩態向量；$\pi^* P = \pi^*$ 與特徵值 $\lambda = 1$ 的證據完全吻合——代數與機率在案發現場互相指認。注意冪迭代的收斂速度由第二特徵值 $\lambda_2$ 控制：$|\lambda_2|$ 越接近 1，收斂越慢——這條線索在九十年後的 PageRank 中再次出現（阻尼因子正是為了加速收斂而引入的「干擾項」）。

## 結案 -- 後果與影響
- **隨機過程誕生**：Markov 鏈是第一個被嚴格研究的隨機過程，後由 Kolmogorov（1931）擴展到連續時間與一般狀態空間，奠定現代機率論公理化。
- **Perron–Frobenius 定理**：Frobenius 1912 年的工作直接受 Markov 鏈啟發，成為非負矩陣理論的基石。
- **遍歷理論與統計力學**：動力系統的遍歷性假設，被 Markov 鏈提供了可計算的模型；MCMC（Metropolis 1953、Hastings 1970）用馬可夫鏈做蒙地卡羅模擬。
- **Google PageRank（1998）**：Brin 與 Page 把網頁瀏覽建模為巨大的馬可夫鏈，PageRank 向量就是穩態分布 $\pi^*$——Google 的核心演算法是這件 1906 年案件的直系後代。
- 大數法則推廣到依賴變數，Nekrasov 的主張被正式駁回。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Andrey Markov | 1906 年提出馬可夫鏈與大數法則推廣 |
| Pafnuty Chebyshev | Markov 的老師，機率論聖彼得堡學派創始人 |
| Oskar Perron / Georg Frobenius | 正矩陣譜定理（1907/1912） |
| Andrey Kolmogorov | 1931 年將隨機過程公理化 |
| Sergey Brin / Larry Page | 1998 年 PageRank，馬可夫鏈的現代應用 |

- A. Markov, *Extension of the law of large numbers to dependent quantities*, Izv. Fiz.-Matem. Obsch. Kazan Univ. (1906)。
- S. Brin, L. Page, *The Anatomy of a Large-Scale Hypertextual Web Search Engine*, WWW (1998)。
