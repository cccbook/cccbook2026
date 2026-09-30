# 1655 — Wallis 無窮分析

## 案件摘要
1655 年，牛津大學 Savilian 教授 John Wallis 出版《無窮算術》（Arithmetica Infinitorum），用純**算術**方法處理 Cavalieri 的幾何不可分量：計算數列 $\frac{0^k+1^k+\cdots+n^k}{n^{k+1}}$ 的極限、以插值在整數冪之間插入分數冪，從而猜出圓面積公式，得到著名的 Wallis 乘積 $\frac{\pi}{2} = \frac{2\cdot 2}{1\cdot 3}\cdot\frac{4\cdot 4}{3\cdot 5}\cdots$ 與 $\frac{4}{\pi}$ 的級數表達，並猜想廣義二項式定理。這本書直接啟發了 1664–1666 年的 Newton。

## 前因 -- 為什麼會有這個案子
- 1635 年 Cavalieri 的不可分量法已給出 $\int_0^1 x^n dx = \frac{1}{n+1}$ 的雛形，但方法充滿幾何爭議（Guldin 的攻擊懸而未決）。
- 1637 年 Fermat 用幾何級數（在 $[0,a]$ 上以等比分割）更嚴格地證明了同一公式，並寄給 Mersenne 網絡。
- Torricelli、Pascal 用不可分量算了擺線、圓扇形等，但**圓的面積**始終缺一個「算術化」的公式：$\pi$ 是無理數，$\int_0^1(1-x^2)^{1/2}dx$ 中的指數 $\frac{1}{2}$ 不在整數冪之列，Cavalieri/Fermat 的方法都無能為力。
- Wallis 是密碼學家、Oxford 幾何教授、Royal Society 創始會員。案件的動機：把幾何的不可分量**翻譯成算術**，並用插值突破分數指數的封鎖。

## 線索與推理 -- 數學式、程式、理論

### 線索一：算術化的積分
Wallis 計算「前 $n$ 個整數 $k$ 次冪之和與 $n^{k+1}$ 之比」的極限：

$$\lim_{n\to\infty} \frac{0^k + 1^k + 2^k + \cdots + n^k}{n^{k+1}} = \frac{1}{k+1}$$

這正是 $\int_0^1 x^k dx = \frac{1}{k+1}$ 的黎曼和形式（等分區間、取左端點）。Wallis 對 $k = 1, 2, 3, \dots$ 逐一列表，並宣稱「由归纳法」（per modum inductionis）此式對所有 $k$ 成立——他用「歸納」指的是**模式外推**，不是今日的數學歸納法，嚴格性後來由 Fermat 與 Fermat 式的論證補足。

### 線索二：插值突破 $\frac{1}{2}$ 指數
圓的面積 $A = \int_0^1 (1-x^2)^{1/2} dx = \frac{\pi}{4}$。定義 $I(p, q) = \int_0^1 (1 - x^{1/p})^{q}\,dx$，Wallis 對整數 $(p, q)$ 逐一算出 $I$ 值並列表，發現：

- $I(p, 0) = 1$，$I(p, 1) = \frac{1}{p+1}$
- 行列之間有規律，於是他**插值**出 $p = \frac{1}{2}$（即指數 $\frac{1}{2}$）那條缺失的列。

插值過程中他發現圓的 $I(\frac{1}{2}, \frac{1}{2}) = \frac{\pi}{4}$ 之值無法用有理數表達，只能用**無窮乘積**夾逼。

### 線索三：Wallis 乘積
由插值表逐步取極限，Wallis 得到：

$$\frac{\pi}{2} = \frac{2}{1}\cdot\frac{2}{3}\cdot\frac{4}{3}\cdot\frac{4}{5}\cdot\frac{6}{5}\cdot\frac{6}{7}\cdots = \prod_{n=1}^{\infty} \frac{2n}{2n-1}\cdot\frac{2n}{2n+1}$$

等價地，$\frac{4}{\pi} = \frac{3\cdot 3}{2\cdot 4}\cdot\frac{5\cdot 5}{4\cdot 6}\cdots$。這是 $\pi$ 的第一個**無窮乘積**表達式（此前 Viète 1593 有連乘的有限形式）。Brouncker 勳爵隨即給出連分數 $\frac{4}{\pi} = 1 + \frac{1^2}{2 + \frac{3^2}{2 + \frac{5^2}{2+\cdots}}}$。

### 線索四：廣義二項式猜想
Wallis 的插值表還隱藏著另一個寶藏：$(1+x)^\alpha$ 展開式係數的插值規律。他對整數 $\alpha$ 的二項式係數列表、試圖插值出 $\alpha = \frac{1}{2}$ 的係數，但沒有成功——他把這個未解之案寫進書中，留給讀者。1665 年大瘟疫期間，23 歲的 Newton 在 Woolsthorpe 讀到這一頁，接手了這個案子。

### 程式碼範例：二項式級數展開驗證與 Wallis 乘積
```python
import numpy as np
from math import comb

# (1) 算術化積分：lim (0^k+...+n^k)/n^{k+1} = 1/(k+1)
for k in [1, 2, 3, 4]:
    n = 10**6
    s = sum(j**k for j in range(n+1)) / n**(k+1)
    print(f"k={k}: 數值 {s:.6f}, 1/(k+1) = {1/(k+1):.6f}")

# (2) Wallis 乘積逼近 pi/2
N = 100000
prod = 1.0
for n in range(1, N+1):
    prod *= (2*n)**2 / ((2*n-1) * (2*n+1))
print(f"Wallis 乘積 = {prod:.6f}, pi/2 = {np.pi/2:.6f}")

# (3) 廣義二項式級數：sqrt(1+x) = (1+x)^{1/2} 展開驗證
def binom_series(alpha, x, terms=20):
    c, s = 1.0, 1.0
    for k in range(1, terms):
        c *= (alpha - k + 1) / k     # 係數遞推 C(k) = C(k-1)*(alpha-k+1)/k
        s += c * x**k
    return s

x = 0.5
print(f"級數 sqrt(1+{x}) = {binom_series(0.5, x):.8f}")
print(f"numpy sqrt(1+{x}) = {np.sqrt(1+x):.8f}")
```

程式輸出：冪和極限與 $\frac{1}{k+1}$ 逐項吻合；Wallis 乘積收斂到 $\pi/2 \approx 1.5708$；廣義二項式級數 $\sqrt{1.5} \approx 1.22474$ 與 numpy 結果一致——Wallis 留下的兩個懸案在數值上都被證實可解。

### 線索五：插值方法的哲學
Wallis 的插值之所以大膽，在於他假設：**連續性**——整數冪之間的分數冪，其行為應當與整數冪一致，因此數列表中的空格可以用「自然的內插」填補。這在嚴格意義上是有風險的（不是每個數列都有唯一自然的插值），但 Wallis 的賭注賭對了：圓面積、Wallis 乘積、廣義二項式係數，三次插值全部命中。他自己的辯護是：「真理的外觀」（由一致性與連續性引導）。Huygens 起初批評此法不可靠，但在驗算結果後轉為讚賞。這個案件揭示 17 世紀數學的一個特徵：**啟發式的外推**先行，嚴格證明後補——Newton 的廣義二項式定理正是同一套打法的直系傳承。

## 結案 -- 後果與影響
- 《無窮算術》把幾何求積**算術化**，掃除了不可分量的哲學障礙——數列、插值、極限成為合法工具。
- Wallis 乘積與 Brouncker 連分數開啟了 $\pi$ 的無窮級數時代：1671 年 Gregory 的 arctan 級數、1674 年 Leibniz 的 $\frac{\pi}{4} = 1 - \frac{1}{3} + \frac{1}{5} - \cdots$。
- 廣義二項式猜想的未解之頁直接啟發 Newton：1665 年 Newton 接手插值出 $(1+x)^{1/2}$ 的級數，進而建立流數術。
- Wallis 對整數冪和的「歸納」引發嚴格性之問，直到 Cauchy/Weierstrass 的極限語言才補上。
- 案件的影響：Royal Society 的《哲學會刊》1665 年創刊，Wallis 是核心作者——無窮分析從此成為英國數學的招牌。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| John Wallis | 《無窮算術》，插值、Wallis 乘積 |
| Bonaventura Cavalieri | 不可分量法的先驅 |
| Pierre de Fermat | $\int x^n dx$ 的嚴格證明 |
| William Brouncker | $\frac{4}{\pi}$ 連分數 |
| Isaac Newton | 1665 年接手廣義二項式懸案的讀者 |

- J. Wallis, *Arithmetica Infinitorum*, Oxford (1655)。
- J. Wallis, *De Sectionibus Conicis* (1655)：圓錐曲線的算術處理。
- B. Cavalieri, *Geometria Indivisibilibus* (1635)。
