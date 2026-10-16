# 1918 — Julia 與 Mandelbrot 的復動力系統

## 案件摘要
1918 年，24 歲的 Gaston Julia 在戰場上失去鼻子、戴著面具回到數學界，發表長篇論文研究迭代 $z \mapsto z^2 + c$ 的軌道行為：哪些點的軌道有界、哪些逃向無窮、迭代的「邊界」是什麼形狀。他與 Pierre Fatou 幾乎同時描繪出今日稱為 **Julia 集合**的對象——但那時沒有人能「看見」它。直到 1980 年，Benoît Mandelbrot 在 IBM 用計算機把這些集合畫了出來：原來邊界是無窮複雜的分形，而在參數平面上還有一個以他命名的 **Mandelbrot 集合**。停滯 60 年的舊案，被一台計算機重新偵破。

## 前因 -- 為什麼會有這個案子
- 1879 年 Picard 定理：解析函數在任一鄰域內至多漏一個值——迭代 $n$ 次後的函數 $f^{\circ n}$ 也是解析函數，這預示迭代會有「狂野」的行為。
- 1879 年 Cayley 提出牛頓法在復平面的收斂域問題：解三次方程 $z^3 - 1 = 0$ 時，牛頓迭代 $z_{n+1} = z_n - (z_n^3-1)/(3z_n^2)$ 的吸引盆邊界長什麼樣？Cayley 自認「下期解答」，卻再也沒寫出來——因為邊界是無法用當時工具描述的分形。
- Poincaré 在三體問題中發現的混沌與「同宿軌道」，暗示動力系統普遍存在不可預測性。
- 1914–1918 年 Fatou 的系列論文與 Julia 1918 年的《Mémoire sur l'itération des fonctions rationnelles》幾乎同時問世，兩人競爭激烈，Fatou 晚了幾個月投稿，Grand Prix 揭曉時桂冠歸 Julia。

## 線索與推理 -- 數學式、程式、理論

### 線索一：迭代與法圖集、Julia 集
設 $f$ 為有理映射（最簡單：$f(z) = z^2 + c$），記 $f^{\circ n}$ 為 $n$ 次迭代。把複平面分成兩區：

- **Fatou 集（正規域）**：在這些點附近，迭代族 $\{f^{\circ n}\}$ 是正規族（Montel 意義下）——軌道行為「溫和」、可預測，通常收斂到吸引子或週期軌道。
- **Julia 集 $J(f)$**：Fatou 集的補集——混沌邊界。在 $J(f)$ 上，任何一點的任意小鄰域內，迭代都「狂野」：取值稠密、對初值極端敏感。

由 Picard 定理與 Montel 正規族理論可證：$J(f)$ 是完全集（閉、無孤立點）、完全不變（$f(J) = J = f^{-1}(J)$）、且在 $J$ 上迭代是拓撲傳遞的（chaos 的數學定義）。

### 線索二：二次映射 $z_{n+1} = z_n^2 + c$ 的分類
對每個參數 $c$，定義**填充 Julia 集**：

$$K_c = \{z : \text{軌道 } 0, f(0), f(f(0)), \dots \text{ 有界}\}$$

關鍵判別：若 $|z| > \max(|c|, 2)$ 則 $|f^{\circ n}(z)| \to \infty$ 逃逸——所以一切都在 $|z| \le 2$ 的圓盤內。Julia 集是 $K_c$ 的邊界：

- $c = 0$：$K_0$ 是閉單位圓盤，$J$ 是圓周——唯一「不奇怪」的情形。
- $c = -1$：$K_c$ 是線段狀的「樹」，$J$ 是碎裂的曲線。
- $c = -2$：$K_c$ 是線段 $[-2, 2]$，$J$ 就是這條線段。
- 一般的 $c$：$J$ 是無窮複雜的分形——連通、塵埃狀、或 Cantor 集，取決於 $c$。

### 線索三：Mandelbrot 集合（1980）
Mandelbrot 的洞見：不要在動力平面上看 $z$，改在**參數平面**上看 $c$。定義：

$$M = \{c \in \mathbb{C} : K_c \text{ 是連通的}\} = \{c : \text{軌道 } 0 \mapsto c \mapsto c^2 + c \mapsto \cdots \text{ 有界}\}$$

兩個定義相等（Douady–Hubbard 1982 的證明）。$M$ 集合位於 $|c| \le 2$ 內，邊界是已知最複雜的分形之一：局部處處像小号的 Julia 集合（「Mandelbrot 集是 Julia 集的地圖」），而 Julia 集連通當且僅當 $c \in M$——參數空間一把抓出所有動力行為。1982 年 Douady 與 Hubbard 用共形映射（外部尾聲場、Böttcher 映射 $\varphi$ 滿足 $\varphi(f(z)) = \varphi(z)^2$）給出嚴格理論。

### 程式碼範例：Julia 集合與 Mandelbrot 集合的迭代繪圖
```python
import numpy as np
import matplotlib.pyplot as plt

def julia(c, xlim=1.8, ylim=1.3, N=800, max_iter=100):
    x = np.linspace(-xlim, xlim, N)
    y = np.linspace(-ylim, ylim, N)
    z = x[None, :] + 1j * y[:, None]
    escape = np.zeros_like(z, dtype=int)
    for i in range(max_iter):
        mask = np.abs(z) <= 2
        z[mask] = z[mask]**2 + c
        escape[mask & (np.abs(z) > 2)] = i
    return escape

def mandelbrot(xlim=(-2.2, 0.8), ylim=(-1.2, 1.2), N=800, max_iter=100):
    x = np.linspace(*xlim, N); y = np.linspace(*ylim, N)
    c = x[None, :] + 1j * y[:, None]
    z = np.zeros_like(c); escape = np.zeros_like(c, dtype=int)
    for i in range(max_iter):
        mask = np.abs(z) <= 2
        z[mask] = z[mask]**2 + c[mask]
        escape[mask & (np.abs(z) > 2)] = i
    return escape

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].imshow(julia(-0.7 + 0.27j), extent=(-1.8, 1.8, -1.3, 1.3), cmap="magma")
axes[0].set_title("Julia set, c = -0.7 + 0.27i")
axes[1].imshow(mandelbrot(), extent=(-2.2, 0.8, -1.2, 1.2), cmap="magma")
axes[1].set_title("Mandelbrot set")
plt.show()
```

迭代 100 次、以 $|z| \le 2$ 為逃逸判據：左圖是 Julia 集合的「塵埃狀」邊界，右圖是 Mandelbrot 集合的主心形與圓盤芽——Cayley 1879 年看不到的圖像，被 numpy 的向量化迭代一次畫出。

## 結案 -- 後果與影響
- **分形幾何誕生**：Mandelbrot 1975 年造詞 fractal，1982 年《The Fractal Geometry of Nature》把 Julia 集合、Koch 曲線、Sierpiński 三角整合成新幾何學。
- **復動力系統成為獨立領域**：Douady–Hubbard 的結構理論、Sullivan 的不變測度定理（Fatou 集上無 roaming domains，結束了 Fatou–Julia 時代的懸案之一）、 Lyubich 的測度論結果。
- **混沌理論的視覺教材**：對初值敏感、無窮自相似、Feigenbaum 普適常數——分形與混沌在 1980 年代匯流。
- 應用外溢：圖像壓縮、隨機數生成檢驗、加密學中的迭代映射、牛頓法吸引盆的數值分析——Cayley 的舊案也在計算機上結案。
- 数学哲学的衝擊：計算機實驗成為數學「偵查」的正式手段——Mandelbrot 之前，沒有人認為畫圖能破案。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Gaston Julia | 1918 年迭代理論，一戰失容仍獲 Grand Prix |
| Pierre Fatou | 1917–1919 年獨立發現正規域理論 |
| Benoît Mandelbrot | 1980 年計算機繪出 $M$ 集合，分形之父 |
| Adrien Douady & John Hubbard | 1982 年 $M$ 集的嚴格理論 |
| Arthur Cayley | 1879 年牛頓法吸引盆的原始謎團 |

- G. Julia, *Mémoire sur l'itération des fonctions rationnelles*, J. Math. Pures Appl. (1918)。
- P. Fatou, *Sur les équations fonctionnelles*, Bull. Soc. Math. France (1919)。
- B. Mandelbrot, *The Fractal Geometry of Nature*, Freeman (1982)。
- A. Douady, J. Hubbard, *Étude dynamique des polynômes complexes*, Publ. Math. Orsay (1984–85)。
