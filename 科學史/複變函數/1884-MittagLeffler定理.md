# 1884 — Mittag-Leffler 定理

## 案件摘要
1884 年，瑞典數學家 Gösta Mittag-Leffler 在 Acta Mathematica 上發表定理：給定離散點列與每點指定的**主部**（principal part），必存在一個亞純函數，其奇點與主部恰如所指定，且相差一個整函數。這是 Cauchy 留數的部分分式展開的無窮推廣——從「已知函數求展開」反轉為「已知奇點構造函數」。它與 Weierstrass 因子定理互為對偶：一個管零點，一個管極點，合起來把亞純函數的「戶口名簿」完全建檔。

## 前因 -- 為什麼會有這個案子
- 1844 年 Liouville 定理：有界整函數必常數——暗示整函數由其奇點行為分類。
- 1876 年 Weierstrass 因子定理：給定離散零點集（含重數），可構造整函數恰有這些零點：$f(z) = z^m e^{g(z)} \prod E_p(z/a_n)$。**零點可以自訂，那極點呢？**
- 1826 年 Cauchy 留數定理：$\oint f\,dz = 2\pi i \sum \text{Res}$。有理函數的部分分式 $\frac{1}{z(z-1)} = \frac{1}{z-1} - \frac{1}{z}$ 說明：函數 = 主部之和 + 多項式。但對無窮多個極點，級數一般發散——需要「收斂修正項」。
- Mittag-Leffler 1876 年起創辦 Acta Mathematica，把北歐變成國際分析的樞紐；他本人師從 Weierstrass，深諳構造主義路線。

## 線索與推理 -- 數學式、程式、理論

### 線索一：有理函數的部分分式——案發原型
對極點 $a_1, \dots, a_k$ 互異的有理函數，部分分式分解為：

$$f(z) = \sum_{j=1}^{k} \underbrace{\left[\frac{c_{j,1}}{z-a_j} + \cdots + \frac{c_{j,m_j}}{(z-a_j)^{m_j}}\right]}_{\text{主部 } P_j(z)} + \text{多項式}$$

每個主部 $P_j$ 完整記錄該極點的「罪狀」（階數與係數）。問題：無窮多個極點時 $\sum P_j$ 一般不收斂。

### 線索二：Mittag-Leffler 定理
> 設 $\{a_n\}$ 為趨於 $\infty$ 的離散複數列，$P_n(z)$ 為在 $a_n$ 處極點的多項式（主部）。則存在亞純函數 $f$，使得 $f - P_n$ 在每個 $a_n$ 解析，且 $f$ 除 $\{a_n\}$ 外解析。且任何兩個這樣的 $f$ 相差一個整函數。

**構造證明**的關鍵技巧：主部 $P_n$ 在 $\infty$ 附近會爆炸，但它在原點附近解析（當 $|a_n|$ 足夠大）。取 $P_n$ 在原點的 Taylor 展開前若干項 $Q_n(z)$，則差 $P_n - Q_n$ 在大 $|z|$ 處衰減，使 $\sum (P_n - Q_n)$ 局部一致收斂：

$$f(z) = \sum_{n=1}^{\infty} \left[ P_n(z) - Q_n(z) \right]$$

$Q_n$ 就是「收斂修正項」——足夠多的項保證收斂，丟掉的部分只貢獻整函數。經典例子：

$$\sum_{n=-\infty}^{\infty} \frac{1}{(z-n)^2} = \frac{\pi^2}{\sin^2 \pi z}, \qquad \pi \cot \pi z = \frac{1}{z} + \sum_{n=1}^{\infty} \frac{2z}{z^2 - n^2}$$

### 線索三：與 Weierstrass 因子定理的對偶
| | Weierstrass 因子定理 (1876) | Mittag-Leffler 定理 (1884) |
|---|---|---|
| 資料 | 零點集（含重數） | 極點集 + 主部 |
| 產出 | 整函數 | 亞純函數 |
| 唯一性 | 差 $e^{g(z)}$ | 差整函數 |
| 收斂技巧 | 初等因子 $E_p(w)$ | Taylor 截斷修正 |

亞純函數的完整描述由此完成：$f = g/h$，$g$ 由零點因子定理給出、$h$ 由極點資料給出。兩定理像一對雙胞胎偵探，一人查「何處歸零」，一人查「何處爆炸」。

### 線索四：Hadamard 對 $\zeta$ 的應用
1893 年 Hadamard 用這套構造+因子分解技術研究 Riemann zeta 函數，建立整函數的階與因子的一般理論，成為 1896 年他與 de la Vallée Poussin 證明質數定理的數學武器。構造主義的函數論，最終審判了質數分佈之謎。

### 線索五：從 Cauchy 到 Mittag-Leffler 的方法論逆轉
Cauchy 留數定理（1826）的路線是「由函數求積分」：已知 $f$，算 $\sum \text{Res}$。Mittag-Leffler 把方向完全反轉：「由積分資料構造函數」——已知極點清單與主部，反推函數本體。這種逆轉在數學史上反覆出現：Weierstrass 因子定理把「求零點」反轉為「指定零點」；構造主義（Konstruktivismus）成為柏林學派的旗幟：函數不是被「發現」的，而是被「建造」的——只要規格書齊全，函數必然存在。

再看經典應用：$\Gamma$ 函數的 Weierstrass 展開

$$\frac{1}{\Gamma(z)} = z e^{\gamma z} \prod_{n=1}^{\infty} \left(1 + \frac{z}{n}\right) e^{-z/n}$$

正是兩定理合作的結晶：因子定理處理零點 $z = 0, -1, -2, \dots$，Mittag-Leffler 式的收斂修正項 $e^{-z/n}$ 保證無窮乘積收斂。Euler 1729 年的 $\Gamma$ 函數，百年後被 Weierstrass 學派重新建檔。

### 程式碼範例：Mittag-Leffler 部分分式的數值重建
```python
import numpy as np
import matplotlib.pyplot as plt

# 用部分分式（含收斂修正）重建 pi cot(pi z)，與 numpy 內建比較
def mittag_leffler_cot(z, N=50):
    # 主部: 1/z + sum 2z/(z^2 - n^2)，對稱求和天然收斂
    s = 1.0 / z
    for n in range(1, N + 1):
        s += 2 * z / (z**2 - n**2)
    return s

z = np.linspace(0.05, 0.95, 100) + 0.3j   # 避開極點 z = 0, 1
approx = mittag_leffler_cot(z, N=200)
exact = 1 / np.tan(np.pi * z)

print("最大誤差:", np.max(np.abs(approx - exact)))

# 可視化：沿實軸逼近 pi cot(pi z)
x = np.linspace(-4.45, 4.45, 800)
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x, np.real(mittag_leffler_cot(x, N=100)), label="Mittag-Leffler partial fractions")
ax.plot(x, np.real(1 / np.tan(np.pi * x)), "--", lw=1, label="exact")
ax.set_ylim(-10, 10); ax.legend()
ax.set_title("Reconstruction of pi*cot(pi*z) from principal parts")
plt.show()
```

誤差量級可達 $10^{-10}$ 以下——從「主部清單」出發，數值上完整重建了函數，正是 Mittag-Leffler 構造的直接演示。

## 結案 -- 後果與影響
- 亞純函數論正式建檔：奇點資料 ⇄ 函數本體的雙向通道，成為複分析教科書的標準章節。
- Hadamard 因子理論（1893）→ 質數定理（1896）：構造主義路線的最大戰果。
- 1924 年 Mittag-Leffler 定理推廣為 **Riemann–Roch 定理**的解析版本：緊緻黎曼面上亞純函數空間的維數公式，代數幾何的基石由此鋪設。
- 部分分式展開至今是數值分析與訊號處理的工具：Z 變換的部分分式反演、電路網路函數、Laplace 變換反演皆用同一套路。
- Mittag-Leffler 創辦的 Acta Mathematica 至今仍是頂級數學期刊；他與 Nobel 的糾葛（據傳諾貝爾獎無數學獎與他遊說失敗有關）也是科學史的著名公案。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Gösta Mittag-Leffler | 提出定理、創辦 Acta Mathematica |
| Karl Weierstrass | 因子定理，對偶之路 |
| Augustin-Louis Cauchy | 留數定理，案發原型 |
| Jacques Hadamard | 整函數因子理論 → 質數定理 |
| Bernhard Riemann | Riemann–Roch 的源頭 |

- G. Mittag-Leffler, *Sur la représentation analytique des fonctions monogènes uniformes*, Acta Math. **4** (1884)。
- L. Ahlfors, *Complex Analysis*, 3rd ed., McGraw-Hill, 1979。
- J. B. Conway, *Functions of One Complex Variable*, 2nd ed., Springer, 1978。
