# 1844-Liouville 超越數

## 案件摘要
1844 年，Joseph Liouville 在給法國科學院的通信中首次**明確構造**出一個超越數，終結了「超越數是否存在且能否具體寫下」的懸案。他用的武器不是高深的分析，而是一條關於「代數數無法被有理數逼近得太好」的不等式。

## 前因 -- 為什麼會有這個案子
- 1744 年 Euler 證明 $e$ 是無理數；1761 年 Lambert 證明 $\pi$ 是無理數。無理數已被馴服。
- 但無理數分兩類：**代數數**（整係數多項式的根，如 $\sqrt{2}$、黃金比 $\frac{1+\sqrt5}{2}$）與**超越數**（不是任何整係數多項式的根）。
- 1840 年代，沒有人知道超越數是否存在。Cantor 1874 年的非對角線論證要晚 30 年才出現——而且 Cantor 只證明「存在很多」，並不能指出任何一個具體的超越數。
- 懸案：能否**寫下一個明確的數，並證明它是超越的**？

## 線索與推理

### 線索一：代數數的「逼近剛性」

Liouville 的關鍵洞察（探案核心）：若 $\alpha$ 是 $n$ 次整係數多項式 $f(x)$ 的根，則對任意有理數 $\frac{p}{q}$（$q \geq 1$，且 $\frac{p}{q} \neq \alpha$）：

$$\left|\alpha - \frac{p}{q}\right| > \frac{C_\alpha}{q^{n}}$$

其中 $C_\alpha > 0$ 是只依賴 $\alpha$ 的常數。

**推理過程**：設 $\alpha$ 是不可約多項式 $f \in \mathbb{Z}[x]$、次數 $n$ 的根。由均值定理：

$$\left|f\left(\frac{p}{q}\right)\right| = \left|f\left(\frac{p}{q}\right) - f(\alpha)\right| = \left|f'(\xi)\right|\left|\frac{p}{q} - \alpha\right|$$

若 $\left|\frac{p}{q} - \alpha\right| < 1$，則 $\xi$ 落在有界區間內，故 $\left|f'(\xi)\right| < M$。另一方面：

$$\left|f\left(\frac{p}{q}\right)\right| = \frac{\left|a_n p^n + \cdots + a_0 q^n\right|}{q^n} \geq \frac{1}{q^n}$$

（分子是非零整數，因為 $f$ 不可約且 $\frac{p}{q}$ 不是根）。合併兩式即得 Liouville 不等式。

**含義**：$n$ 次代數數是一個「有理數逼近的禁區」——分母越大，逼近精度反而受限於 $q^{-n}$。想要無限精準地逼近？那這個數就不是代數數。

### 線索二：反向構造——Liouville 常數

既然代數數不能被逼近得太好，那就**故意造一個能被任意好的有理數逼近的數**。Liouville 常數：

$$L = \sum_{k=1}^{\infty} 10^{-k!} = 0.110001000000000000000001000\ldots$$

（小數點後第 $1, 2, 6, 24, 120, \ldots$ 位是 1，其餘為 0。）

取部分和 $p_m/q_m = \sum_{k=1}^{m} 10^{-k!}$，其中 $q_m = 10^{m!}$。則誤差被「下一項」主導：

$$0 < L - \frac{p_m}{q_m} = \sum_{k=m+1}^{\infty} 10^{-k!} < 2 \cdot 10^{-(m+1)!} = \frac{2}{10^{m!\cdot m} \cdot 10^{m!}} \leq \frac{2}{q_m^{m+1}} \cdot \frac{1}{10^{m!}} < \frac{1}{q_m^{m}}$$

對任意大的 $m$ 成立。若 $L$ 是 $n$ 次代數數，取 $m > n$ 就與 Liouville 不等式矛盾。**結論：$L$ 是超越數。** $\blacksquare$

### 程式驗證（Python）

```python
from fractions import Fraction
from itertools import count
from math import factorial

def liouville_partial(m):
    """回傳 L 的前 m 項部分和（精確分數）與 L 的 Decimal 近似"""
    s = sum(Fraction(1, 10**factorial(k)) for k in range(1, m + 1))
    return s

# --- 1. 印出 Liouville 常數的小數展開（前 60 位） ---
from decimal import Decimal, getcontext
Decimal.prec = getcontext()
getcontext().prec = 60
L_approx = sum(Decimal(10) ** (-factorial(k)) for k in range(1, 25))
print("L ≈", L_approx)
# 0.110001000000000000000001000000000000000000000000000000000001...

# --- 2. 驗證「逼近太好」性質：|L - p/q| < 1/q^m ---
L = Decimal(10) ** (-factorial(30))  # 用超高精度近似 L 本身
getcontext().prec = 400
L = sum(Decimal(10) ** (-factorial(k)) for k in range(1, 60))

print(f"{'m':>3} {'分母 q=10^m!':>14} {'|L-p/q|':>12} {'1/q^m':>12}  逼近太好?")
for m in range(2, 8):
    pm = liouville_partial(m)
    qm = 10 ** factorial(m)
    err = abs(Fraction(str(L)) - pm) if False else None
    # 用分數精確計算誤差
    L_frac = sum(Fraction(1, 10**factorial(k)) for k in range(1, 12))
    err = abs(L_frac - pm)
    bound = Fraction(1, qm ** m)
    print(f"{m:>3} {qm:>14} {float(err):>12.3e} {float(bound):>12.3e}  {err < bound}")

# 輸出顯示每一行都是 True：部分和的逼近精度遠勝任何代數數允許的下界
```

**程式偵探筆記**：`Fraction` 保證精確有理算術，誤差 $< 1/q^m$ 對所有 $m$ 成立——這正是「超越」的算術指紋。任何代數數都做不到。

## 結案 -- 後果與影響
- **1873 年 Hermite**：證明 $e$ 是超越數——第一個「自然出現」的超越數，用的是恰當的積分恆等式與線性組合技巧。
- **1882 年 Lindemann**：證明 $\pi$ 是超越數，一舉解決了兩千多年的「化圓為方」問題（參見 [1882-Lindemann超越數.md](1882-Lindemann超越數.md)）。核心方法（Lindemann–Weierstrass 定理）正是 Hermite 方法的推廣。
- **Cantor 1874**：證明代數數可數、實數不可數——超越數「不可數地多」，但 Liouville 的構造仍是唯一能「點名」超越數的方法（Cantor 對角線構造除外）。
- **20 世紀**：Thue–Siegel–Roth 定理把逼近下界改進到 $\left|\alpha - \frac{p}{q}\right| > \frac{C_\varepsilon}{q^{2+\varepsilon}}$（Roth 獲 1958 菲爾茲獎），顯示代數數的「剛性」比 Liouville 猜想的更強。
- **Baker 1966**：對數線性形式理論，超越數論成為可計算的工具，解決了大量的 Diophantine 方程。

## 關鍵人物與文獻
- **Joseph Liouville**（1809–1882）：法國數學家，工作橫跨分析（Sturm–Liouville 理論）、複分析（Liouville 定理：有界整函數為常數）、數論。1844 年在 Comptes Rendus 發表超越數構造。
- J. Liouville, *Sur des classes très étendues de quantités dont la valeur n'est ni algébrique, ni même réductible à des irrationnelles algébriques*, Comptes Rendus 18 (1844), 883–885, 910–911.
- C. Hermite, *Sur la fonction exponentielle*, Comptes Rendus 77 (1873).
- F. Lindemann, *Über die Zahl π*, Math. Annalen 20 (1882).
- W. M. Schmidt, *Diophantine Approximation*, Lecture Notes in Math. 785, Springer, 1980.
