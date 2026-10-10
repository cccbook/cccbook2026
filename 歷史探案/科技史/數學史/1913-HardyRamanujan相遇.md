# 1913 - Hardy–Ramanujan 相遇

## 案件摘要
1913 年 1 月，劍橋的 G. H. Hardy 收到一封來自印度馬德拉斯的信——25 歲的會計員 Srinivasa Ramanujan 寫下他「自學」發現的數學定理（無任何大學訓練）。Hardy（與 Littlewood）檢視後驚為天人：「**這些定理必定是真的，因為如果它們是假的，沒有人能有足夠的想像力去發明它們**」。Hardy 邀請 Ramanujan 到劍橋——**數學史上最傳奇的合作**：兩人共同證明了 $\pi$ 的漸近公式、分割數理論、素數計數——Ramanujan 32 歲死於印度（飲食與疾病），留下 3900 個公式（多數後來被證明正確）。**直覺與嚴格的世紀合奏。**

## 前因 -- 為什麼會有這個案子
**Ramanujan 的背景**（1887–1920）：南印度（坦賈武爾）婆羅門家庭、貧困——

- **無大學訓練**：兩次退學（只顧數學，其他科目全不及格）
- **自學的數學**：唯一的教科書是 Carr 的《純粹與應用數學概要》（A Synopsis of Elementary Results，5000 個定理無證明）——**Ramanujan 自己重造了歐拉、高斯、雅可比的定理**（並推進到新的）
- **職業**：馬德拉斯港務局的**會計員**（月薪 20 盧比）

**1913 年 1 月 16 日的信**：Ramanujan 寫給劍橋的三位數學家（Baker、Hobson、Hardy）——前兩位**不回**——Hardy 回了。

**Hardy 的震撼**：信中的定理——

1. $\frac{1}{\sqrt{2}}$ 型的連分數與**無窮乘積**（正確且前所未見）
2. **分割數的漸近公式**（正確且深刻）
3. 一些**錯誤的**素數定理（Ramanujan 聲稱接近黎曼假設的結果——不嚴格）

**Hardy 的名言**：「這些定理必定是真的，因為**如果它們是假的，沒有人能有足夠的想像力去發明它們**。」

## 線索與推理 -- 數學式、程式、理論

### 分割數理論
**分割數 $p(n)$**：整數 $n$ 的分拆方式數（$n = 4$：$4 = 4 = 3+1 = 2+2 = 2+1+1 = 1+1+1+1$，$p(4) = 5$）。

**Ramanujan–Hardy 的漸近公式（1918）**：

$$p(n) \sim \frac{1}{4n\sqrt{3}} e^{\pi \sqrt{2n/3}}$$

**指數增長**——分割數爆炸（$p(200) = 3972999029388$，13 位數！）。

**Rademacher 的精確公式（1937）**：無窮級數（收斂到精確值）——**Ramanujan 的直覺 + Hardy 的嚴格**：兩人 1918 的漸近 → Rademacher 用 Hardy 的圓法（見 `1742-Goldbach猜想.md`）完成精確級數。

### Ramanujan 的直覺與 Hardy 的嚴格
**合作的分工**：

- **Ramanujan**：直覺——**公式從夢中來**（自述：女神 Namagiri 在夢中給他公式）——3900 個公式，**95% 後來被證明正確**
- **Hardy**：嚴格——證明、組織、傳播（歐陸的規範）

**經典案例**：
- **連分數**：$\frac{1}{1+\frac{e^{-2\pi}}{1+\frac{e^{-4\pi}}{1+\dots}}} = \left(\sqrt{\frac{5+\sqrt{5}}{2}} - \frac{\sqrt{5}+1}{2}\right)e^{2\pi/5}$——Ramanujan 的「夢中公式」（1913），Hardy 與 Watson 1927 證明
- **1729 的計程車數**：Hardy 看望病中的 Ramanujan，提到計程車號 1729「無趣」——Ramanujan 立即回答：「**不，它是最小的可表示為兩組立方和的數**：$1729 = 1^3 + 12^3 = 9^3 + 10^3$」——**taxicab 數的誕生**

### π 的計算與 Ramanujan 級數
**Ramanujan 的 π 級數（1914）**：

$$\frac{1}{\pi} = \frac{2\sqrt{2}}{9801} \sum_{n=0}^{\infty} \frac{(4n)! (1103 + 26390n)}{(n!)^4 396^{4n}}$$

**每項加 8 位精度**——**史上最快的 π 級數**（Chudnovsky 兄弟、Kanada 的 π 計算都用其變體）——**與 Buffon 擲針（見 `../隨機算法/1777-Buffon針實驗.md`）、割圓術（見 `0263-LiuHui割圓術.md`）的 π 譜系並列**。

### 程式碼：分割數與 π 級數

```python
import math

# 分割數（動態規劃）與漸近公式
def partition_dp(n):
    """分割數 p(n)：動態規劃"""
    p = [0] * (n+1)
    p[0] = 1
    for k in range(1, n+1):
        for i in range(k, n+1):
            p[i] += p[i-k]
    return p[n]

def partition_asym(n):
    """Ramanujan–Hardy 漸近：p(n) ~ exp(π√(2n/3)) / (4n√3)"""
    return math.exp(math.pi * math.sqrt(2*n/3)) / (4 * n * math.sqrt(3))

for n in [10, 50, 100]:
    exact = partition_dp(n)
    asym = partition_asym(n)
    print(f"p({n}) = {exact}，漸近 = {asym:.3e}（比率 {exact/asym:.3f}）")
# 漸近比率趨近 1——Ramanujan 的直覺 ✓

# Ramanujan 的 π 級數（每項加 8 位！）
def ramanujan_pi(terms=3):
    s = 0.0
    for n in range(terms):
        # (4n)! (1103 + 26390n) / ((n!)^4 396^{4n})
        f4 = math.factorial(4*n)
        s += f4 * (1103 + 26390*n) / (math.factorial(n)**4 * 396**(4*n))
    return 9801 / (2 * math.sqrt(2) * s)

print(f"\nRamanujan π 級數（3 項）= {ramanujan_pi(3):.15f}")
print(f"數學 π = {math.pi:.15f}——每項加 8 位精度 ✓")

# 1729：最小的兩組立方和
def taxicab_search(limit):
    """找最小的兩組立方和"""
    sums = {}
    for a in range(1, int(limit**(1/3))+1):
        for b in range(a, int(limit**(1/3))+1):
            s = a**3 + b**3
            sums.setdefault(s, []).append((a, b))
    for s in sorted(sums):
        if len(sums[s]) >= 2:
            return s, sums[s][:2]

n, reps = taxicab_search(20000)
print(f"\n最小的兩組立方和 = {n}：{reps}——1729 的故事 ✓")
```

### 硬水與命運
**Ramanujan 的健康**：劍橋的冬天（素食 + 缺乏維生素）——1917 年重病（肺結核與肝的寄生蟲）。

**1729 的故事**（1919）：Hardy 看望病中的 Ramanujan——「1729 無趣」——「不，它是最小的兩組立方和」——**計程車數**。

**1920 年 4 月 26 日**：Ramanujan 死於印度（32 歲）——**數學史上最深的遺憾之一**（與 Abel 26 歲、Galois 20 歲、Taniyama 31 歲並列）。

**遺產的勝利**：3900 個公式（「筆記本」），1980s–2000s 被系統證明——**95% 正確**。**Ramanujan 機器**（機器學習證明他的公式——見 `../密碼學/2022-LLM時代密碼學.md` 的 AI 與數學）。

**偵探筆記**：Hardy–Ramanujan 的推理是「**直覺與嚴格的合奏**」——Ramanujan 的公式（夢中來的直覺）+ Hardy 的證明（歐陸的嚴格）。**與歐拉的越界（見 `1734-Euler巴塞爾問題.md`）、阿基米德的槓桿（見 `-0250-Archimedes圓周率.md`）同源**：**直覺先於嚴格，最終都被證明**——但 Ramanujan 的直覺是「無訓練的」，更神秘。

## 結案 -- 後果與影響
- **數學史上最傳奇的合作**：Hardy–Ramanujan——直覺與嚴格的合奏。
- **分割數理論**：漸近公式 → Rademacher 精確級數——**數論與組合的橋樑**（與 Hardy 圓法同源，見 `1742-Goldbach猜想.md`）。
- **π 計算的革命**：Ramanujan 級數（每項 8 位）——現代 π 計算（Kanada、Chudnovsky）的基礎。
- **taxicab 數**：1729 的故事——**數論的浪漫**（taxicab(2) = 1729）。
- **印度數學的傳統**：Madhava 學派（14 世紀的無窮級數）、Ramanujan——**非西方傳統的勝利**。
- **早夭天才的遺憾**：32 歲——與 Abel、Galois、Taniyama 並列（見 `1832-Galois群論.md`）。
- **數學的神秘性**：「夢中公式」——數學直覺的本質（與 Poincaré 的無意識理論、Grothendieck 的「抽象之夢」對照）。

## 關鍵人物與文獻
- **Srinivasa Ramanujan**（1887–1920）：1913 的信、分割數、π 級數、taxicab 1729
- **G. H. Hardy**（1877–1947）：劍橋；圓法、「數學家的道歉」（A Mathematician's Apology 1940）
- **J. E. Littlewood**：Hardy 的合作者——三人組合（Hardy–Littlewood–Ramanujan）
- **Hans Rademacher**（1892–1969）：分割數的精確級數 (1937)
- **Bruce Berndt**：1985–2020 證明 Ramanujan 筆記本的系統工程
- 交叉參照：`1734-Euler巴塞爾問題.md`、`1742-Goldbach猜想.md`、`1832-Galois群論.md`、`2013-ZhangYitang素數間距.md`
