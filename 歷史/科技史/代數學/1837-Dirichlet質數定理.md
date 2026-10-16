# 1837-Dirichlet質數定理

## 案件摘要
1837 年，狄利克雷（Peter Gustav Lejeune Dirichlet）證明：算術級數 $a, a+n, a+2n, \dots$（$\gcd(a,n)=1$）中存在**無窮多個質數**。為此他發明了 Dirichlet $L$ 函數與「特徵函數」$\chi$——解析數論就此誕生。

## 前因 -- 為什麼會有這個案子
- 歐拉（1737）用 $\sum \frac{1}{p}$ 發散證明質數無窮多，並發現 zeta 乘積公式，但方法不能處理「限制在特定剩餘類」的質數。
- 勒讓德（1785/1798）**猜想**了此定理卻證不出來；高斯幼年時憑計算相信「每個剩餘類的質數一樣多」。
- 核心困難：條件「$p \equiv a \pmod n$」是**乘法結構**問題，需要把「同餘類」翻譯成「可乘的解析工具」。

## 線索與推理 -- 數學式、程式、理論

### 線索一：特徵函數 χ 的誕生
Dirichlet 為「在同餘類裡挑質數」發明了群特徵：對 $\gcd(a,n)=1$，Dirichlet 特徵 $\chi \bmod n$ 滿足

$$\chi(ab) = \chi(a)\chi(b), \quad \chi(a) = 0 \iff \gcd(a,n) > 1$$

（即 $(\mathbb{Z}/n\mathbb{Z})^\times$ 的群同態。）關鍵的**正交性**用來隔離單一剩餘類：

$$\frac{1}{\varphi(n)} \sum_{\chi} \overline{\chi(a)}\,\chi(k) = \begin{cases} 1, & k \equiv a \pmod n \\ 0, & \text{否則} \end{cases}$$

```python
# 模 5 的實特徵（Legendre 符號）：χ(k) = k^2 mod 5 的取值
def chi_mod5(k):
    if k % 5 == 0:
        return 0
    return 1 if (k % 5) in (1, 4) else -1  # 二次剩餘 +1, 非剩餘 -1

print([chi_mod5(k) for k in range(1, 6)])  # [1, -1, -1, 1, 0]
# 正交性驗證：sum χ(k) = 0（非主特徵）
assert sum(chi_mod5(k) for k in range(5)) == 0
```

### 線索二：Dirichlet L 函數
對每個特徵定義

$$L(s, \chi) = \sum_{n=1}^{\infty} \frac{\chi(n)}{n^s} = \prod_{p}\left(1 - \frac{\chi(p)}{p^s}\right)^{-1} \quad (\mathrm{Re}(s) > 1)$$

Euler 乘積因 $\chi$ 的完全乘性而成立。兩大支柱：

1. **非主特徵** $\chi \ne \chi_0$ 時 $L(1,\chi) \ne 0$（最難的一步，Dirichlet 用類數公式與級數 $\sum \frac{\chi(p)}{p}$ 證得）；
2. **主特徵** $L(s,\chi_0) = \zeta(s)\prod_{p \mid n}(1-p^{-s})$，在 $s=1$ 發散。

組合後：$\sum_{p \equiv a \ (n)} \frac{1}{p} = \frac{1}{\varphi(n)} \ln\ln x + O(1) \to \infty$，故該剩餘類有無窮多質數。

### 線索三：定理陳述與數值檢驗

> **Dirichlet 定理（1837）**：設 $a, n$ 互質，則算術級數 $a + kn$（$k = 0, 1, 2, \dots$）中含無窮多質數。更強地，質數在 $\varphi(n)$ 個互質剩餘類中漸近均勻分佈。

```python
from sympy import primerange, totient
import matplotlib.pyplot as plt

n, a, b = 4, 1, 3   # 模 4 的兩類：1+4k 與 3+4k
primes = list(primerange(2, 100000))
counts = {a: 0, b: 0}
for p in primes:
    if p % 4 == 1: counts[a] += 1
    elif p % 4 == 3: counts[b] += 1

print(f"π(x)=100000 以內: p≡1 (mod 4) 有 {counts[a]} 個, p≡3 (mod 4) 有 {counts[b]} 個")
print(f"理論值 φ(4)=2, 應各佔一半 —— 實測比例 = {counts[a]/(counts[a]+counts[b]):.4f}")
assert counts[a] > 0 and counts[b] > 0  # 兩類都有無窮多（有限截斷下皆 > 0）

xs = range(1000, 100001, 1000)
r1 = [sum(1 for p in primerange(2, x) if p % 4 == 1) for x in xs]
r3 = [sum(1 for p in primerange(2, x) if p % 4 == 3) for x in xs]
plt.plot(xs, r1, label='p ≡ 1 (mod 4)')
plt.plot(xs, r3, label='p ≡ 3 (mod 4)')
plt.legend(); plt.xlabel('x'); plt.ylabel('質數個數'); plt.grid(True)
plt.title('Dirichlet: 剩餘類中的質數漸近均勻'); plt.savefig('dirichlet.png', dpi=120)
```

### 線索四：解析數論的開端
Dirichlet 的手法 —— 「把數論條件編碼成 $L$ 函數，再用 $L(1,\chi) \ne 0$ 的解析性質解鎖」—— 成為整門學科的模板：質數定理（1896, Hadamard–de la Vallée Poussin 用 $\zeta(s)$ 在 $s=1$ 無零點）、Dirichlet 近似定理（鴿籠原理）、類數公式 $h(n) = \frac{\sum \chi(a)a}{\text{...}}$ 皆出於此。

## 結案 -- 後果與影響
- 群特徵 $\chi$ 是現代**表示論**（群表示的特徵標）的先聲；傅立葉分析進入數論。
- 質數分佈知識直接支撐**密碼學**：RSA 需要大質數，其安全性的啟發式論證（質數密度 $\sim 1/\ln x$，不同剩餘類均勻）皆源於 Dirichlet–Riemann 傳統。
- Chebotarev 密度定理（1922）是 Dirichlet 定理在 Galois 擴張上的宏大推廣，通往朗蘭茲。

## 關鍵人物與文獻
- **Dirichlet, P. G. L.**（1837）：《Beweis des Satzes, dass jede unbegrenzte arithmetische Progression...》。
- **歐拉**（1737）：zeta 乘積公式。
- **Apostol, T.**（1976）：《Introduction to Analytic Number Theory》標準教材。
- **Iwaniec–Kowalski**（2004）：《Analytic Number Theory》現代進階。
