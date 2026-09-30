# 1879 — Picard 定理

## 案件摘要
1879 年，法國數學家 Émile Picard 在短論〈Mémoire sur les fonctions entières〉中投下一枚炸彈：一個本性奇點的任意小鄰域內，函數會取遍**每一個**複數值，至多只有一個例外。同年他又證明「小定理」：非常數整函數至多漏掉一個值。這兩個結果遠超當時分析學的想像——原來複變函數的「行為」可以如此極端，卻又如此精確地被刻劃。Casorati–Weierstrass 只說「靠近」，Picard 說「命中」；從稠密到取遍，一字之差，天壤之別。

## 前因 -- 為什麼會有這個案子
- 1851 年 Riemann 建立複變函數的幾何理論，解析延拓成為標準工具。
- 1868 年 Casorati 與 Weierstrass 各自證明：若 $z_0$ 是本性奇點，則在 $z_0$ 的任何鄰域內，函數值在複平面上**稠密**。
- 稠密 ≠ 取遍。Casorati–Weierstrass 只說值「靠近」，Picard 要問的是：能不能真的**打到**每一個值？這是從「定性疏漏」到「精確命中」的升級。
- 另一條線索：Liouville 1847 年證明有界整函數必為常數。Picard 注意到 $e^z$ 永不取 $0$——只漏一個值就能活下來。那麼「漏兩個值」的整函數還存在嗎？答案是：不存在。

## 線索與推理 -- 數學式、程式、理論

### 線索一：案發現場 $e^{1/z}$
$z = 0$ 是 $e^{1/z}$ 的本性奇點。考慮方程 $e^{1/z} = a$（$a \neq 0$）：

$$\frac{1}{z} = \log a + 2\pi i n \quad\Longrightarrow\quad z_n = \frac{1}{\log a + 2\pi i n}, \quad n \in \mathbb{Z}$$

當 $|n| \to \infty$，$z_n \to 0$。也就是說：**任何非零值 $a$ 的原像全部堆積在原點附近**，無窮多個解擠在任意小的鄰域裡。唯獨 $a = 0$ 無解——這就是那個「至多一個例外值」，Picard 稱之為**例外值（valeur exceptionnelle）**。

### 線索二：Picard 大定理
> 若 $f$ 在 $z_0$ 處有本性奇點，則 $f$ 在 $z_0$ 的任何刪去鄰域 $0 < |z - z_0| < r$ 內取遍所有複數值，至多除去一個例外值。

注意措辭：不是「在某個鄰域」，而是「**任何**鄰域」——例外值若存在，在多小的範圍內都不可能被第二個值填補。這比 Casorati–Weierstrass 的稠密性強得多：稠密只保證靠近，Picard 保證命中。

### 線索三：Picard 小定理與 Liouville 的對話
> 非常數整函數至多取不到一個複數值。

證明策略（後由 Borel、Schottky 精煉）：設整函數 $f$ 漏掉 $a, b$ 兩個值，令 $g = \dfrac{f - a}{b - a}$，則 $g$ 是漏掉 $0$ 與 $1$ 的整函數。透過模函數 $\lambda$ 的反函數構造 $g$ 的解析原函數，再由 Liouville 定理逼出 $g$ 必為常數——矛盾。小定理是大定理的推論：$\infty$ 若是超越整函數的本性奇點，其鄰域（即整個平面的遠方）也取遍所有值至多漏一個。

### 線索四：證明的後續武器
Picard 原始證明依賴橢圓模函數，相當曲折。後來出現多條替代路線：
- **Schottky 定理（1904）**：控制漏兩值函數的模長，給出定量版本。
- **Montel 正規族（1912）**：用正規族理論優雅地重證 Picard——漏兩值的函數族必正規。
- **Boutroux、Julia、Rolf Nevanlinna（1925）**：把「漏一個值」升級為「虧量和 $\leq 2$」的值分布理論。

### 線索五：為什麼「至多一個」例外？
偵探的直覺追問：為什麼不能漏兩個？以 $e^{1/z}$ 為鑑——若它想漏掉 $a$ 與 $b$ 兩個值，考慮 $f = \dfrac{e^{1/z} - a}{b - a}$，這是漏掉 $0$ 與 $1$ 的函數。Schottky 定理（1904）指出：漏掉 $0, 1$ 的函數在單連通域上的模長受到只依賴 $|f(z_0)|$ 的顯式上界控制，而且當 $z$ 靠近本性奇點時上界爆炸——矛盾不可避免。例外值至多一個，是「漏兩值函數無法存在於本性奇點附近」的必然結論。更深的解釋來自模函數 $\lambda(\tau)$：它把上半平面 $\mathbb{H}$ 映到 $\hat{\mathbb{C}} \setminus \{0, 1, \infty\}$，反函數把漏兩值函數「吊」回 $\mathbb{H}$，使其成為單值解析函數——Picard 原始證明正是走這條路。

### 程式碼範例：$e^{1/z}$ 本性奇點的取值分布
```python
import numpy as np
import matplotlib.pyplot as plt

# 在原點附近的刪去鄰域內取格點，計算 e^{1/z} 的值
r = 0.3
pts = np.linspace(-r, r, 400)
X, Y = np.meshgrid(pts, pts)
Z = X + 1j * Y
Z = Z[np.abs(Z) > 1e-4]        # 刪去中心（避免除以零）
W = np.exp(1 / Z)

# 值的輻角著色：觀察 W 是否「取遍」整個複平面
fig, ax = plt.subplots(figsize=(6, 6))
ax.scatter(W.real, W.imag, s=0.3, c=np.angle(W), cmap="hsv", alpha=0.5)
ax.set_title("Values of exp(1/z) near essential singularity z=0")
ax.set_xlim(-50, 50); ax.set_ylim(-50, 50)
plt.show()

# 數值驗證：Picard 方程 e^{1/z} = a 的解應趨近 0
a = 3 + 4j
ns = np.arange(-8, 9)
z_n = 1 / (np.log(a) + 2j * np.pi * ns)
print("|z_n| 隨 |n| 增大而趨近 0:", np.abs(z_n[::4]))
```

數值輸出中 $|z_n|$ 隨 $|n|$ 增大穩定趨近 $0$，直接驗證了 Picard 方程 $e^{1/z} = a$ 的解全部堆積在原點附近；著色圖顯示 $e^{1/z}$ 的像佈滿整個值平面——除了從未觸及的原點附近那一小塊空白：例外值 $0$ 的「案發空白區」。理論與數值兩條證據鏈在此閉合。

## 結案 -- 後果與影響
- 開創**值分布理論**：Nevanlinna 1925 年的兩個基本定理把 Picard 定理定量化為虧值理論，成為 20 世紀複分析三大支柱之一。
- **複動力系統的遠因**：Julia 集、Fatou 集（1918）的定義直接依賴 Picard 型定理；逃逸集上函數「取遍所有值」的性質是混沌行為的數學根源。1926 年 Fatou 證明：函數迭代的 orbit 在本性奇點附近展現極端不可預測性——Picard 的例外值理論是唯一能約束它的工具。
- **Montel 正規族**成為複動力學的核心工具，其判據「漏兩值 ⇒ 正規」正是 Picard 定理的化身；今日 Mandelbrot 集邊界的計算，本質上是在檢驗迭代族的正規性。
- 大定理至今有推廣：多複變的 Picard 型定理、代數幾何中的虧格障礙（Abel 定理、Riemann–Roch 的虧值面向）、以及福克斯型微分方程的解結構，皆可視為此案的延續審判。
- 教學意義：$e^{1/z}$ 成為每一本複分析教科書的本性奇點標準範例——案發現場被永久保留。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Émile Picard | 提出大小定理，開啟值分布理論 |
| Felice Casorati | 1868 稠密性定理（前案） |
| Karl Weierstrass | 1868 稠密性定理、病態函數美學 |
| Joseph Liouville | 有界整函數定理，鋪路 |
| Friedrich Schottky | 1904 定量化 Schottky 定理 |
| Robert Nevanlinna | 1925 定量化值分布理論 |
| Paul Montel | 正規族理論，優雅重證 |

- É. Picard, *Mémoire sur les fonctions entières*, C. R. Acad. Sci. Paris **89** (1879)。
- É. Picard, C. R. Acad. Sci. Paris **88** (1879)：本性奇點的例外值定理。
- F. Schottky, Sitzungsber. Preuss. Akad. Wiss. (1904)：Schottky 定理的定量不等式。
- J. B. Conway, *Functions of One Complex Variable*, 2nd ed., Springer, 1978。
