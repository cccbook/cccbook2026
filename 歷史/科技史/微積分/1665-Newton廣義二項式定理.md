# 1665 — Newton 廣義二項式定理

## 案件摘要
1665 年初，22 歲的 Isaac Newton 在 Cambridge 讀 Wallis《無窮算術》時，接手了 Wallis 留下的插值懸案：把 $(1+x)^\alpha$ 的二項式展開從正整數指數推廣到**任意**指數（分數、負數），得到廣義二項式定理

$$(1+x)^\alpha = \sum_{k=0}^{\infty} \binom{\alpha}{k} x^k, \qquad \binom{\alpha}{k} = \frac{\alpha(\alpha-1)\cdots(\alpha-k+1)}{k!}$$

並用 $\sqrt{1+x}$、$\frac{1}{1+x}$ 等級數逐項積分，插值出圓的面積 $\frac{\pi}{4}$。這條級數成為流數術（微積分）的基石——Newton 的微積分是從**無窮級數**長出來的。

## 前因 -- 為什麼會有這個案子
- 1655 年 Wallis 在《無窮算術》中用數列插值求出圓面積與 Wallis 乘積，並嘗試插值 $(1+x)^{1/2}$ 的展開係數——但他沒有成功，把懸案寫進書中。
- Cavalieri/Fermat 的積分 $\int_0^1 x^n dx = \frac{1}{n+1}$ 只對正整數 $n$ 有效；圓面積需要指數 $\frac{1}{2}$：$\int_0^1 (1-x^2)^{1/2}dx = \frac{\pi}{4}$。
- Newton 在 Cambridge 師從 Barrow，兩年內自修歐氏幾何、Descartes《幾何學》、Viète、Wallis——他的筆記本（Trinity College 借書紀錄）顯示 1664–1666 年的閱讀軌跡。
- 案件的動機：圓面積、雙曲線面積、對數（雙曲線下面積）都涉及**分數與負指數**——必須把二項式展開推廣到任意指數，才能打開這批案卷。

## 線索與推理 -- 數學式、程式、理論

### 線索一：從插值到級數
Wallis 的方法是對整數冪的係數列表插值。Newton 更進一步：他注意到整數指數的二項式係數滿足遞推

$$\binom{\alpha}{k} = \binom{\alpha}{k-1}\cdot\frac{\alpha - k + 1}{k}$$

對整數 $\alpha$，這遞推在 $k > \alpha$ 時歸零（級數截斷）；對 $\alpha = \frac{1}{2}$，它**永不歸零**：

$$(1+x)^{1/2} = 1 + \frac{1}{2}x - \frac{1}{8}x^2 + \frac{1}{16}x^3 - \frac{5}{128}x^4 + \cdots$$

Newton 用「根式開方驗證」（把級數自乘，看是否得回 $1+x$）與插值兩種方式確認此式——級數自乘後 $x$ 項、$x^2$ 項逐一抵消，這是他的「驗屍報告」。

### 線索二：負指數與幾何級數
$\alpha = -1$ 時遞推給出 $\binom{-1}{k} = (-1)^k$：

$$\frac{1}{1+x} = 1 - x + x^2 - x^3 + \cdots$$

這正是古人已知的幾何級數。Newton 注意到：逐項積分得

$$\ln(1+x) = \int_0^x \frac{dt}{1+t} = x - \frac{x^2}{2} + \frac{x^3}{3} - \cdots$$

對數——這個 17 世紀的天文計算工具——竟然是雙曲線下面積的級數展開（Mercator 1668 年也獨立發表，Newton 藏了三年才出版）。

### 線索三：圓面積與 $\frac{\pi}{4}$
對 $(1 - x^2)^{1/2}$ 展開並逐項積分：

$$\arcsin(x) = \int_0^x \frac{dt}{\sqrt{1-t^2}} = x + \frac{1}{6}x^3 + \frac{3}{40}x^5 + \frac{5}{112}x^7 + \cdots$$

取 $x = \frac{1}{2}$：$\arcsin(\frac{1}{2}) = \frac{\pi}{6}$，故

$$\pi = 6\left(\frac{1}{2} + \frac{1}{6}\cdot\frac{1}{8} + \frac{3}{40}\cdot\frac{1}{32} + \cdots\right)$$

Newton 用這個收斂極快的級數把 $\pi$ 算到 15 位以上（他自己在信中說「恥於算了這麼多位」）——超過了 Archimedes 以來的所有方法。

### 線索四：級數即積分的引擎
Newton 的關鍵洞見：**任何**函數只要能展開成冪級數 $\sum a_k x^k$，它的積分就是 $\sum \frac{a_k}{k+1} x^{k+1}$——積分從此變成「逐項降冪求和」的代數操作。這把 Cavalieri/Fermat 的 $\int x^n dx = \frac{1}{n+1}$（只對整數 $n$）推廣到一切冪級數，也預示了 1666 年流數術的正式誕生。

### 程式碼範例：廣義二項式級數展開與逐項積分驗證
```python
import numpy as np

# (1) 廣義二項式係數遞推：(1+x)^alpha 的級數
def binom_series(alpha, x, terms=30):
    c, s = 1.0, 1.0
    for k in range(1, terms):
        c *= (alpha - k + 1) / k
        s += c * x**k
    return s

# 驗證 Newton 的「級數自乘得回 1+x」：sqrt(1+x)^2 = 1+x
x = 0.5
s = binom_series(0.5, x)
print(f"sqrt(1+0.5) 級數 = {s:.10f}, numpy = {np.sqrt(1.5):.10f}")
print(f"級數自乘 s^2 = {s*s:.10f}（應 = 1.5）")

# (2) 負指數：1/(1+x) 與 ln(1+x) 逐項積分
s_inv = binom_series(-1, x)
print(f"1/(1+0.5) 級數 = {s_inv:.10f}, 理論 = {1/1.5:.10f}")

# 逐項積分得 ln(1+x) = x - x^2/2 + x^3/3 - ...
def ln_series(x, terms=30):
    s = 0.0
    for k in range(1, terms):
        s += (-1)**(k+1) * x**k / k
    return s
print(f"ln(1.5) 級數 = {ln_series(0.5):.10f}, numpy = {np.log(1.5):.10f}")

# (3) 圓面積：arcsin 級數 -> pi
def arcsin_series(x, terms=30):
    c, s = 1.0, x          # c: 係數, s: 級數和（從 x^1 項開始）
    for k in range(1, terms):
        c *= (2*k - 1)**2 / ((2*k) * (2*k + 1))
        s += c * x**(2*k + 1)
    return s

pi_est = 6 * arcsin_series(0.5)
print(f"pi 估計 = {pi_est:.12f}, numpy pi = {np.pi:.12f}")
```

程式輸出：$\sqrt{1.5}$ 的級數與 numpy 一致、級數自乘得回 $1.5$（Newton 的驗證方法）；$\ln(1.5)$ 的逐項積分級數吻合；$\arcsin(\frac{1}{2})$ 級數給出 $\pi \approx 3.141592653590$——Newton 的 15 位級數計算在數值上完全重現。

## 結案 -- 後果與影響
- 廣義二項式定理成為**冪級數時代的開端**：函數 = 級數，積分 = 逐項積分，微分 = 逐項微分。
- $\ln(1+x)$、$\arcsin x$、$\arctan x$ 的級數開啟了 $\pi$ 與對數的高速計算，Machin 1706 年用 arctan 級數算 $\pi$ 到 100 位。
- Newton 把這些結果寫進 1669 年的〈分析學〉（De Analysi per Aequationes Numero Terminorum Infinitas）與 1676 年的兩封致 Leibniz 的信（Epistola prior / posterior），廣義二項式是核心內容。
- 級數是流數術的基石：1666 年 Newton 的〈論流數〉把正/反流數問題系統化，二項式級數是「反流數」（積分）的主要武器。
- 案件的影響：今日計算機的浮點函式庫（`math.sqrt`、`math.log`）底層仍用多項式/級數逼近——Newton 的作案手法沿用至今。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Isaac Newton | 廣義二項式定理，級數積分 |
| John Wallis | 插值懸案的留下者，Newton 的起點 |
| Isaac Barrow | Newton 的老師，Cambridge Lucasian 教授 |
| Nicolaus Mercator | 1668 獨立發表對數級數 |
| Henry Oldenburg | Royal Society 書信秘書，傳遞兩封信 |

- I. Newton, *De Analysi per Aequationes Numero Terminorum Infinitas* (1669，由 Barrow 呈 Royal Society)。
- I. Newton, *Epistola prior / Epistola posterior* 致 Oldenburg（1676）：廣義二項式與插值方法。
- J. Wallis, *Arithmetica Infinitorum* (1655)。
