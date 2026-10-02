# 1742 - 哥德巴赫猜想

## 案件摘要
1742 年 6 月 7 日，普魯士外交官 Christian Goldbach 寫信給 Euler，提出：**每個大於 2 的偶數都是兩個素數之和**？

$$4 = 2+2, \quad 6 = 3+3, \quad 8 = 3+5, \quad 10 = 3+7 \text{ 或 } 5+5, \dots$$

Euler 回信加強（「每個偶數 = 兩素數之和」），並說「我雖然不能證明，但我確信它是定理」——**284 年懸案**（至今未解），數論最著名的未解猜想之一。**一封信、一句猜想、284 年的攻擊**——與費馬定理（358 年，見 `1994-Wiles費馬定理.md`）、孿生素數（見 `2013-ZhangYitang素數間距.md`）並列數論的中心謎題。

## 前因 -- 為什麼會有這個案子
**Goldbach 的背景**：普魯士外交官（駐莫斯科、聖彼得堡），業餘數學家——與 Euler（聖彼得堡科學院）通信 30 年。**數論的愛好者**。

**1742 年 6 月 7 日的信**（義大利文）：原版猜想——「每個數 = 1 + 素數 + 半素數」——Euler 回信簡化為現代版：

**哥德巴赫猜想**：每個大於 2 的偶數都是兩個素數之和。

**數值證據**：電腦驗證到 $4 \times 10^{18}$（Oliveira e Silva 2013）——**無一反例**——但**無窮性未證**。

## 線索與推理 -- 數學式、程式、理論

### 攻擊的譜系
**284 年的攻擊**（每個失敗都產生新數學）：

- **Hardy–Littlewood（1923）**：**圓法**（circle method）——假設廣義黎曼假設下，大偶數的表示法數量漸近：

$$\text{表示法數} \sim 2C_2 \frac{n}{(\ln n)^2} \prod_{p \mid n, p > 2} \frac{p-1}{p-2}$$

（$C_2 \approx 0.6602$ 是孿生素數常數——**表示法的平均密度**。）

- **陳景潤（1966/1973）**：「**1+2**」——每個大偶數 = 素數 + 「半素數」（至多兩個素數的積）：

$$N = p + P_2 \quad \text{（} p \text{ 素數，} P_2 \text{ 至多兩素數之積）}$$

——**最近的結果**（篩法的巔峰，見 `2013-ZhangYitang素數間距.md` 的篩法傳統）
- **Helfgott（2013）**：**弱哥德巴赫猜想**（奇數 = 三素數之和）**已證**！——$N > 5$ 奇數 = $p_1 + p_2 + p_3$——**圓法的勝利**

**弱猜想的勝利**：奇數版（三素數）已解（2013），偶數版（兩素數）仍懸——**「3 素數容易、2 素數極難」**（與 Jacobi 的最速降線、Wiles 的費馬的「最後一步」同源）。

### 圓法（circle method）
**Hardy–Littlewood 的方法**：把「表示法數量」寫成**生成函數**：

$$r(n) = \sum_{p_1 + p_2 = n} 1 = \int_0^1 S(x)^2 e^{-2\pi i n x}\, dx, \quad S(x) = \sum_p e^{2\pi i p x}$$

**推理**：積分的主項來自 $x$ 接近「有理數」$a/q$ 的區間（**主弧** major arcs）——**素數在等差數列的分佈**（Dirichlet 1837，見 `1837-Dirichlet算術級數.md`）控制主項；副弧（minor arcs）的估計是難點。

**與傅立葉的同源**：圓法本質是**傅立葉分析**（見 `../傅立葉轉換/README.md`）——**用頻域研究數論**（與 ζ 函數的譜理論同源，見 `1859-Riemann假設.md`）。

### 程式碼：哥德巴赫的驗證

```python
def sieve_primes(n):
    is_p = [True] * (n+1)
    is_p[0] = is_p[1] = False
    for i in range(2, int(n**0.5)+1):
        if is_p[i]:
            for j in range(i*i, n+1, i): is_p[j] = False
    return [i for i in range(n+1) if is_p[i]]

def goldbach_pairs(n, primes):
    """偶數 n 的兩素數表示"""
    pairs = []
    ps = set(primes)
    for p in primes:
        if p > n//2: break
        if n - p in ps:
            pairs.append((p, n-p))
    return pairs

primes = sieve_primes(100000)
# 前幾個偶數的表示
for n in [4, 6, 10, 100, 1000]:
    pairs = goldbach_pairs(n, primes)
    print(f"{n} = {pairs[0]}{'...' if len(pairs) > 1 else ''}（{len(pairs)} 種表示）")

# 表示法數量隨 n 增長（Hardy–Littlewood 的漸近）
for n in [1000, 10000, 100000]:
    print(f"{n}：{len(goldbach_pairs(n, primes))} 種表示（~ n/ln²n = {n/math.log(n)**2:.0f}）")

# 弱哥德巴赫（奇數 = 三素數，Helfgott 2013 已證）
print("\n弱哥德巴赫（Helfgott 2013 已證）：奇數 > 5 = 三素數之和")
for n in [7, 9, 11, 27]:
    found = [(p, q, r) for p in primes for q in primes if p+q < n and n-p-q in set(primes)]
    print(f"  {n} = {found[0] if found else '?'}")
```

### 陳景潤的悲壯
**陳景潤（1933–1996）**：中國數論學家——**文革期間**在 6 平方米的房間、煤油燈下計算——**「1+2」的證明（1973 發表）**用掉幾麻袋的草稿紙。**數學的苦行僧**——與張益唐的賽百味歲月（見 `2013-ZhangYitang素數間距.md`）、Perelman 的隱居（見 `2003-Perelman龐加萊猜想.md`）同源：**數學不問環境**。

**偵探筆記**：哥德巴赫猜想的推理困境是「**偶數 = 兩素數**的精確控制」——素數的「加法結構」比「乘法結構」（ζ 函數）更難——**加法數論 vs 乘法數論**的分離（與 Dirichlet 的算術級數、圓法的傳統）。**陳景潤的「1+2」是篩法的極限**——要「1+1」需要新的工具（與張益唐的「繞過障礙」同源）。

## 結案 -- 後果與影響
- **284 年懸案**：偶數版仍懸——數論最著名的未解猜想（與費馬定理、孿生素數並列）。
- **弱哥德巴赫已證**（Helfgott 2013）：奇數 = 三素數——圓法的勝利。
- **圓法的帝國**：Hardy–Littlewood 的方法——Waring 問題、華林-哥德巴赫——**加法數論的武器**。
- **陳景潤的「1+2」**：篩法的巔峰——**中國數學的象徵**（徐遲的報告文學 1978 激勵一代人）。
- **計算驗證的極限**：$4 \times 10^{18}$ 無反例——**證據大量，證明為零**（與黎曼假設的 $10^{13}$ 零點同源）。
- **Goldbach 的遺產**：一封信、一句猜想——**業餘愛好者的深遠影響**。

## 關鍵人物與文獻
- **Christian Goldbach**（1690–1764）：1742 的信——普魯士外交官
- **Leonhard Euler**（1707–1783）：回信簡化猜想（見 `1734-Euler巴塞爾問題.md`）
- **G. H. Hardy / J. E. Littlewood**：圓法 (1923)
- **陳景潤**（1933–1996）：「1+2」(1966/1973)——篩法的巔峰
- **Harald Helfgott**：弱哥德巴赫 (2013)
- **T. Oliveira e Silva**：$4 \times 10^{18}$ 的計算驗證 (2013)
- 交叉參照：`1994-Wiles費馬定理.md`、`2013-ZhangYitang素數間距.md`、`1837-Dirichlet算術級數.md`、`1859-Riemann假設.md`
