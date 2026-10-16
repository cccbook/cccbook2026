# 1837 - Dirichlet 算術級數

## 案件摘要
1837 年，Gustav Lejeune Dirichlet 發表《論小於給定值的素數在等差級數中的分佈》：證明**任何等差數列** $a, a+k, a+2k, \dots$（$\gcd(a, k) = 1$）**中有無窮多個素數**——素數不只在自然數列（歐幾里得前 300，見 `-0300-Euclid幾何原本.md`），**在任何互質的等差級數中都無窮**。證明武器是**Dirichlet L-函數**——把分析（歐拉的 ζ 傳統，見 `1734-Euler巴塞爾問題.md`）引入數論的里程碑。**解析數論的誕生**（與歐拉、黎曼同源的傳統）。

## 前因 -- 為什麼會有這個案子
**素數的分佈之謎**：歐幾里得證明素數無窮（前 300）；歐拉的 ζ 乘積（1737）連結素數與分析（見 `1734-Euler巴塞爾問題.md`）；Gauss 的猜測（1792）$\pi(x) \approx x/\ln x$。

**新問題（歐拉與拉格朗日的討論）**：等差級數中的素數：

- $3, 13, 23, 33, 43, \dots$（$a = 3, k = 10$）——有無窮多素數？
- $4, 9, 14, 19, 24, 19, \dots$（$a = 4, k = 5$）——**只有一個**（4 不與 5 互質，除 4 以外全是合數？不——4 與 5 互質嗎？$\gcd(4,5) = 1$——所以有無窮多？但 4, 9, 14, 19, 24 中只有 19 是素數……不對，$4+5k$：4, 9, 14, 19, 24, 29, 34, 39, 44, 49, 54, 59——29, 59, 79……有無窮多 ✓）

**必要條件**：$\gcd(a, k) = 1$（否則 $a$ 的質因數整除全部項——至多一個素數）。

**Dirichlet 的問題**：互質的等差級數，**有無窮多素數嗎？**

## 線索與推理 -- 數學式、程式、理論

### Dirichlet L-函數
**核心武器**：歐拉 ζ 乘積的**推廣**——用「特徵」（character）過濾：

**Dirichlet 特徵** $\chi$：完全乘性、週期性的函數（$\chi(nm) = \chi(n)\chi(m)$、$\chi(n + k) = \chi(n)$）——**模 $k$ 的群特徵**（與 Galois 理論的對偶同源，見 `1832-Galois群論.md`）。

**L-函數**：

$$L(s, \chi) = \sum_{n=1}^{\infty} \frac{\chi(n)}{n^s} = \prod_{p} \frac{1}{1 - \chi(p) p^{-s}}$$

**歐拉乘積的推廣**——**過濾素數的「同餘類」**。

### 證明骨架
**推理**：要證明 $a \bmod k$ 中有無窮多素數，考慮**调和平均**：

$$\sum_{p \equiv a \bmod k} \frac{1}{p} = \infty$$

**證明**（Dirichlet）：構造特徵的組合（正交性），從 $\log L(s, \chi)$ 的極限分離出「$p \equiv a \pmod k$ 的貢獻」——**關鍵：$L(1, \chi) \ne 0$**（非零性——需要**類數公式**的證明）。

**L(1, χ) ≠ 0 的證明**：Dirichlet 的**類數公式**——$L(1, \chi)$ 與二次型的類數連結（**代數數論的先聲**）：

$$L(1, \chi) = \frac{2\pi h}{w\sqrt{|D|}} \cdot \ldots$$

**於是**：等差級數中的素數無窮。$\blacksquare$

**深遠的意義**：
- **素數在每個「互質類」中均勻分佈**（PNT for AP，1968 的證明）——**素數的分佈是「民主的」**
- **L-函數的帝國**：Dirichlet L → ζ → Hasse–Weil L → Langlands 的 L-函數——**數論與表示論的統一**

### 程式碼：等差級數中的素數

```python
def sieve_primes(n):
    is_p = [True] * (n+1)
    is_p[0] = is_p[1] = False
    for i in range(2, int(n**0.5)+1):
        if is_p[i]:
            for j in range(i*i, n+1, i): is_p[j] = False
    return [i for i in range(n+1) if is_p[i]]

# 等差級數中的素數
primes = sieve_primes(100000)
ps = set(primes)

for a, k in [(3, 10), (4, 5), (1, 4), (7, 100)]:
    in_ap = [p for p in primes if p % k == a][:8]
    count = sum(1 for p in primes if p % k == a)
    print(f"p ≡ {a} (mod {k})：{in_ap}... 共 {count} 個")
# 每個互質類都有大量素數——「民主的分佈」✓

# Dirichlet L-函數（特徵過濾）
def dirichlet_char(n, k=4):
    """模 4 的特徵：χ(n) = 1 若 n≡1, -1 若 n≡3, 0 若偶"""
    if n % 2 == 0: return 0
    return 1 if n % 4 == 1 else -1

def L_series(s, k=4, terms=100000):
    return sum(dirichlet_char(n, k) / n**s for n in range(1, terms))

print(f"\nL(1, χ₄) = {L_series(1):.6f}（= π/4 = {math.pi/4:.6f} ✓）")
# 類數公式：L(1, χ) ≠ 0——Dirichlet 證明的關鍵
print("L(1, χ) ≠ 0 → 等差級數中的素數無窮（Dirichlet 1837）")
```

### 解析數論的誕生
**譜系**：
- **歐拉（1737）**：ζ 乘積——素數與分析的橋樑（見 `1734-Euler巴塞爾問題.md`）
- **Dirichlet（1837）**：L-函數——**過濾素數的同餘類**
- **Riemann（1859）**：ζ 的解析延拓與黎曼假設（見 `1859-Riemann假設.md`）
- **素數定理（1896）**：Hadamard–de la Vallée Poussin
- **Langlands 綱領（1967）**：L-函數的大統一——**數論與表示論**（Wiles 的費馬證明 1995 是 Langlands 的一角，見 `1994-Wiles費馬定理.md`）

**偵探筆記**：Dirichlet 的推理是「**過濾 + 非零性**」——用特徵過濾素數類，證明 $L(1, \chi) \ne 0$（類數公式）。**「非零性」的證明是難點**（與黎曼假設的「零點不在臨界線外」、孿生素數的「無窮性」同源——**數論的難題常是「非零/非消失」的證明**）。

## 結案 -- 後果與影響
- **解析數論的誕生**：L-函數把分析引入數論——歐拉 → Dirichlet → Riemann 的譜系。
- **素數的「民主分佈」**：每個互質類均勻分佈——**素數不偏心**（AP 的素數定理 1968）。
- **L-函數的帝國**：Dirichlet L → ζ → Langlands——**數論與表示論的統一**（費馬定理的證明、BSD 猜想）。
- **類數公式**：$L(1,\chi)$ 與二次型的類數——**代數數論的先聲**（Kummer 的理想數、Noether 的環論）。
- **密碼學的間接連結**：素數的同餘類分佈影響 RSA 的金鑰選擇（見 `../密碼學/1977-RSA.md`）。
- **Dirichlet 的地位**：Gauss 的繼任者（Göttingen）——**解析數論之父**。

## 關鍵人物與文獻
- **Gustav Lejeune Dirichlet**（1805–1859）：Beweis des Satzes, dass jede unbegrenzte arithmetische Progression... (1837)；類數公式
- **Leonhard Euler**（1707–1783）：ζ 乘積的傳統（見 `1734-Euler巴塞爾問題.md`）
- **Bernhard Riemann**（1826–1866）：ζ 的解析延拓（見 `1859-Riemann假設.md`）
- **Johann Dirichlet 的繼任**：Gauss 的 Göttingen 講座（1855）
- **Robert Langlands**（1936–）：Langlands 綱領 (1967)——L-函數的大統一
- 交叉參照：`1734-Euler巴塞爾問題.md`、`1859-Riemann假設.md`、`1832-Galois群論.md`、`1994-Wiles費馬定理.md`、`../密碼學/1977-RSA.md`
