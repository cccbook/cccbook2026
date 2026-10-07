# 1984 - Johnson–Lindenstrauss 引理

## 案件摘要
1984 年，William Johnson 與 Joram Lindenstrauss 在研究 Lipschitz 映射時證明一個意外的引理：**高維空間中的 $n$ 個點，可以用隨機投影降到僅 $O(\log n / \epsilon^2)$ 維，且兩兩距離幾乎不變**。一萬維、一百萬個點的資料，可以隨機投影到約 60 維——距離誤差不超過 10%。這是「隨機性壓縮維度」的奇蹟，成為現代機器學習降維、近似最近鄰搜尋、串流算法的基礎。

## 前因 -- 為什麼會有這個案子
Johnson–Lindenstrauss 原本在解決 Lipschitz 嵌入問題（Banach 空間理論）：能否把高維度量空間嵌入低維而保持距離？確定性答案是「不可能」（維度必須夠高）。但他們發現：**如果允許一點誤差（$\epsilon$-近似），隨機線性映射就夠了**——確定性做不到的事，隨機性輕鬆做到。

## 線索與推理 -- 數學式、程式、理論

### 引理的陳述
**定理**：對 $n$ 個點 $\{x_1, \dots, x_n\} \subset \mathbb{R}^d$，任取 $\epsilon \in (0, 1)$，設

$$k = O\left(\frac{\log n}{\epsilon^2}\right)$$

存在線性映射 $A \in \mathbb{R}^{k \times d}$，使得所有兩兩距離同時近似保持：

$$(1-\epsilon) \|x_i - x_j\|^2 \le \|A x_i - A x_j\|^2 \le (1+\epsilon) \|x_i - x_j\|^2$$

**關鍵：$k$ 與原維度 $d$ 無關，只依賴點數 $n$ 的對數！** 一百萬個點只需 $k \approx 30/\epsilon^2$ 維。

### 隨機投影的證明
構造：$A$ 的每個元素獨立取 $N(0, 1/k)$。對固定向量 $x$，隨機投影保持範數：

$$P\left( (1-\epsilon)\|x\|^2 \le \|Ax\|^2 \le (1+\epsilon)\|x\|^2 \right) \ge 1 - 2e^{-k\epsilon^2/4}$$

（由卡方分佈的集中不等式：$\|Ax\|^2/\|x\|^2 \sim \chi^2_k / k$，尾部指數衰減。）

**聯合界（union bound）**：$n$ 個點有 $\binom{n}{2} \le n^2$ 對，同時保持全部距離：

$$P(\text{全部保持}) \ge 1 - 2n^2 e^{-k\epsilon^2/4} > 0 \quad \text{當 } k = O(\log n / \epsilon^2)$$

機率大於零 ⟹ **這樣的映射存在**。$\blacksquare$

**偵探筆記**：證明的推理是「存在性用機率」——證明隨機映射成功的機率大於零，存在性就到手。**不用構造，擲骰子就是構造**：隨機矩陣 $A$ 直接用即可。

### 程式碼：隨機投影降維

```python
import random, math

def random_projection(X, k):
    """X: n 筆 d 維資料 -> n 筆 k 維"""
    d = len(X[0])
    A = [[random.gauss(0, 1/math.sqrt(k)) for _ in range(d)]
         for _ in range(k)]
    return [[sum(A[i][j] * x[j] for j in range(d)) for i in range(k)]
            for x in X]

random.seed(42)
n, d = 1000, 10000
X = [[random.gauss(0, 1) for _ in range(d)] for _ in range(n)]

# 兩兩距離在原空間 vs 投影後
def dist(a, b): return math.sqrt(sum((u-v)**2 for u, v in zip(a, b)))
i, j = 0, 1
d_orig = dist(X[i], X[j])
Xk = random_projection(X, k=100)   # 10000 維 -> 100 維
d_new = dist(Xk[i], Xk[j])
print(f"原距離={d_orig:.3f} 投影後={d_new:.3f} 比率={d_new/d_orig:.3f}")
# 比率 ≈ 1.0：距離幾乎不變，維度縮小 100 倍
```

### 下界：引理是最優的
Alon (2003) 證明：$k = \Omega(\log n / \epsilon^2)$ 是必要的——**JL 引理緊到不能再緊**。隨機性達到了理論極限。

## 結案 -- 後果與影響
- **機器學習降維**：隨機投影替代 PCA（快得多）；隨機特徵（Random Features, Rahimi–Recht 2007）核方法加速。
- **近似最近鄰搜尋**：LSH（局部敏感雜湊）與 JL 結合，高維相似度搜尋成為可能。
- **串流算法**：資料只能掃一遍時，用隨機投影維護 sketch。
- **矩陣近似**：隨機化 SVD、隨機化線性代數（Halko–Martinsson–Tropp 2011）。
- **理論意義**：「確定性不可能、隨機性輕鬆」的又一實例，強化隨機算法的地位。

## 關鍵人物與文獻
- **William Johnson**（1944–）：Banach 空間幾何
- **Joram Lindenstrauss**（1937–2012）：以色列數學家
- Johnson & Lindenstrauss: Extensions of Lipschitz mappings... (1984, Contemp. Math.)
- **Alon**：下界 (2003)
- **Achlioptas**：資料庫友好的隨機投影 (2003)——元素可取 $\{-1, 0, 1\}$
- 交叉參照：`1985-Yao計算隨機性.md`、`1997-BroderMinHash.md`、`2007-HyperLogLog.md`
