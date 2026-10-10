# 1933 - Kolmogorov 公理化

## 案件摘要
1933 年，30 歲的俄國數學家 Andrey Kolmogorov 出版《機率論的基礎》（Grundbegriffe der Wahrscheinlichkeitsrechnung）：用**測度論**公理化機率——機率是「事件的集合函數」，滿足三條公理：

$$P(\Omega) = 1, \quad P(A) \ge 0, \quad P(A \cup B) = P(A) + P(B) \text{（互斥時）}$$

**機率論從賭徒的經驗法則（Pascal–Fermat，1654）變成嚴格的數學**——與歐幾里得的公理化（見 `-0300-Euclid幾何原本.md`）、Hilbert 的公理化（1899）同一範式。Kolmogorov 的公理使**連續機率、大數法則、中央極限定理**全部嚴格化——機率統計（見 `../機率統計/README.md`）與隨機過程的數學基礎。

## 前因 -- 為什麼會有這個案子
**270 年的機率論**（1654–1933）是「手藝」：

- **Pascal–Fermat（1654）**：骰子賭局的期望值——離散、有限
- **Bernoulli（1713）**：大數法則——頻率收斂
- **Laplace（1812）**：《機率的解析理論》——古典定義「有利情況數 / 總情況數」
- **Buffon（1777）**：幾何機率（見 `../隨機算法/1777-Buffon針實驗.md`）——**連續的引入**

**古典定義的危機**：

1. **Bertrand 悖論（1889）**：「圓內隨機弦長 > 邊長的機率」——**三種「等可能」的定義給三個不同答案**（1/2、1/3、1/3）——「等可能」是**曖昧的**！
2. **無窮事件的困惑**：丟銅板無窮次，出現無窮次正面的機率？——「情況數」無法定義
3. **測度論的成熟**：Lebesgue（1902）的積分與測度——**剛好是機率需要的工具**

**Kolmogorov 的問題**：能否用 Lebesgue 測度論，把機率從「經驗法則」變成「公理化數學」？

## 線索與推理 -- 數學式、程式、理論

### 三條公理
**Kolmogorov 公理**：樣本空間 $\Omega$、事件 σ-代數 $\mathcal{F}$、機率測度 $P: \mathcal{F} \to \mathbb{R}$：

1. **非負性**：$P(A) \ge 0$
2. **規範性**：$P(\Omega) = 1$
3. **可數可加性**：互斥事件 $A_1, A_2, \dots$：

$$P\left(\bigcup_{i=1}^{\infty} A_i\right) = \sum_{i=1}^{\infty} P(A_i)$$

**就這三條**——全部機率論從三條公理演繹。

**機率 = 測度**：$P$ 是測度（$\Omega$ 的總測度為 1）——**隨機變數 = 可測函數**、期望 = Lebesgue 積分：

$$E[X] = \int_\Omega X \, dP$$

**Bertrand 悖論的解決**：「等可能」=「均勻測度」——**選不同的測度就是不同的機率模型**（弦的端點均勻 vs 弦心距均勻 vs 弦方向均勻是**三個不同的模型**）——悖論不是矛盾，是**模型選擇的歧義**。

### 大數法則的嚴格化
**Bernoulli（1713）**的直覺——頻率收斂到機率——Kolmogorov 的**強大數法則**：

$$\frac{X_1 + X_2 + \dots + X_n}{n} \xrightarrow{a.s.} E[X_1]$$

（幾乎必然收斂——不僅機率收斂，是**樣本路徑**的收斂。）

**證明**：用 Chebyshev 不等式 + Borel–Cantelli 引理——**測度論的工具**。**Buffon 擲針估 π（見 `../隨機算法/1777-Buffon針實驗.md`）與蒙地卡羅方法（見 `../隨機算法/1946-Ulam蒙地卡羅.md`）的正確性由此保證**——「用頻率估計機率」是數學定理，不是經驗法則。

### 中央極限定理的嚴格化
**CLT**：獨立同分佈變數的和收斂到高斯：

$$\frac{X_1 + \dots + X_n - n\mu}{\sigma\sqrt{n}} \xrightarrow{d} \mathcal{N}(0, 1)$$

**Lindeberg 條件**（1922）與 Kolmogorov 的嚴格化——**高斯分佈的普遍性**（見 `../機率統計/README.md`）成為定理。

### 程式碼：公理與大數法則

```python
import random, math

# Kolmogorov 公理的驗證（丟銅板）
def coin(n=1000000, p=0.5):
    return sum(1 for _ in range(n) if random.random() < p) / n

random.seed(42)
# 公理 2：P(Ω) = 1（所有結果的機率和 = 1）
print(f"P(正) + P(反) = {coin(10000)} + {1-coin(10000):.5f} ≈ 1 ✓")

# 強大數法則：頻率收斂到機率
for n in [10, 100, 1000, 100000]:
    print(f"n={n:7d}: 頻率 = {coin(n):.6f}")
# 收斂到 0.5——Bernoulli 的直覺成為定理

# Bertrand 悖論：三種「等可能」= 三個不同的測度
def bertrand_three_ways(R=1.0, trials=100000):
    """圓內隨機弦，弦長 > √3 R 的機率——三種取樣方式三個答案"""
    import math
    # 方式一：端點均勻
    hits = 0
    for _ in range(trials):
        t1, t2 = random.random()*2*math.pi, random.random()*2*math.pi
        chord = 2*R*math.sin(abs(t1-t2)/2)
        if chord > R*math.sqrt(3): hits += 1
    w1 = hits/trials
    # 方式二：弦心距均勻
    hits = 0
    for _ in range(trials):
        d = random.random()*R
        if 2*math.sqrt(R*R - d*d) > R*math.sqrt(3): hits += 1
    w2 = hits/trials
    return w1, w2

random.seed(42)
w1, w2 = bertrand_three_ways()
print(f"\nBertrand：端點均勻 = {w1:.3f}，弦心距均勻 = {w2:.3f}——不同測度不同答案")
print("Kolmogorov：悖論 = 模型選擇的歧義（不是矛盾）")
```

### 隨機過程的誕生
**Kolmogorov 的帝國**：
- **隨機過程**（1931）：Markov 鏈、擴散過程的公理化——布朗運動（見 `../隨機算法/1905-布朗運動.md`）的嚴格化
- **Kolmogorov 方程**：隨機過程的轉移方程（與 Einstein 的擴散方程同源）
- **複雜度理論**（1965）：Kolmogorov 複雜度——**資訊的最小描述長度**（見 `../計算理論/README.md`）
- ** turbulence**：流體亂流的統計理論

**偵探筆記**：Kolmogorov 的推理是「**用測度論公理化機率**」——與歐幾里得（前 300）、Hilbert（1899）、Cantor（1874）的公理化同一範式：**把「經驗的科學」變成「公理的數學」**。這是數學化的最後一步——機率論、乃至整個不確定性的數學，從此嚴格。

## 結案 -- 後果與影響
- **機率論成為數學**：三條公理 + 測度論——270 年的手藝變成嚴格科學。
- **Bertrand 悖論的解決**：「等可能」= 測度選擇——模型歧義不是矛盾。
- **大數法則的嚴格化**：蒙地卡羅方法、統計推論的正確性保證（見 `../隨機算法/README.md`）。
- **隨機過程的誕生**：Markov 鏈、布朗運動、隨機分析的基礎（Itô 微積分 1944）——金融工程（Black–Scholes 1973）。
- **Kolmogorov 複雜度**（1965）：資訊的最小描述——演算法資訊理論、壓縮、Gödel 式的自指。
- **蘇聯數學學派**：Kolmogorov 的學生（Arnold、Gelfand、Shiryaev）——20 世紀數學的半壁江山。

## 關鍵人物與文獻
- **Andrey Kolmogorov**（1903–1987）：Grundbegriffe der Wahrscheinlichkeitsrechnung (1933)；隨機過程 (1931)、Kolmogorov 複雜度 (1965)
- **Henri Lebesgue**（1875–1941）：測度論 (1902)——Kolmogorov 的工具
- **Joseph Bertrand**（1822–1900）：悖論 (1889)
- **Andrey Markov**（1856–1922）：Markov 鏈——Kolmogorov 的先驅
- 交叉參照：`../機率統計/README.md`、`../隨機算法/1777-Buffon針實驗.md`、`../隨機算法/1946-Ulam蒙地卡羅.md`、`../計算理論/README.md`
