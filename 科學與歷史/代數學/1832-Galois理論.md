# 1832-Galois 理論

## 案件摘要
1832 年 5 月 29 日深夜，20 歲的 Galois 在決鬥前夜寫下遺書與數學手稿，
把「方程可解性」化約為「群的結構」——建立 Galois 理論。
手稿被 Poisson 退回、遺忘十四年，直到 1846 年 Liouville 才在《Journal de mathématiques》出版，
震驚數學界。

## 前因 -- 為什麼會有這個案子
- **Abel（1826）**已證明一般五次方程無根式解，但留下懸案：
  **特定係數的五次方程（如 $x^5 - 2 = 0$）有根式解，怎麼判斷哪個可解？**
- Lagrange（1770）、Cauchy（1815）已發展置換群：循環記法、Cauchy 定理、
  根在置換下取值數整除 $n!$——語言已備，但缺一把「對應」的鑰匙。
- Galois 兩次報考 École Polytechnique 落榜、父親自殺、論文被 Cauchy 遺失、
  被 Poisson 以「 incompréhensible（看不懂）」退稿——人生與論文一樣坎坷。
- 1832 年 5 月 30 日他因政治糾紛（一場女子的決鬥邀約）中彈身亡，5 月 31 日不治。
- 案件問題：**用什麼理論同時解釋「為何可解」與「如何判斷可解」？**

## 線索與推理 -- 數學式、程式、理論

### 線索一：Galois 群的定義——域擴張的對稱性
> **定義（Galois 群）**：設 $K/F$ 為域擴張，
> $$\mathrm{Gal}(K/F) = \{\sigma : K \to K \mid \sigma \text{ 為自同構},\ \sigma|_F = \mathrm{id}\}$$
> 即**固定底域 $F$、保持加法與乘法**的所有對稱變換構成的群，運算為合成。

核心對應（Galois 對應的基石）：$K/F$ 是 Galois 擴張時，
$$\{F \subset E \subset K\} \;\longleftrightarrow\; \{ \mathrm{Gal}(K/F) \supset H \supset \{e\} \}$$
中間域 $E$ 與子群 $H = \mathrm{Gal}(K/E)$ 一一對應，且
$$[K : E] = |H|, \qquad [E : F] = [\mathrm{Gal}(K/F) : H]$$

### 線索二：方程可解性 ⟺ 群可解性
> **Galois 主定理**：設 $f(x)$ 為特徵 0 域上多項式，$K$ 為其分裂域。
> $f(x) = 0$ 有根式解 $\iff$ $\mathrm{Gal}(K/F)$ 是**可解群**，即存在正規列
> $$G = G_0 \triangleright G_1 \triangleright \cdots \triangleright G_m = \{e\}$$
> 每個商群 $G_i / G_{i+1}$ 是質數階循環群。

- 每個「開 $n$ 次方」對應一層質數階循環擴張（Kummer 理論的先聲）。
- **不可解的反例**：$A_5$ 是單群（正規子群只有 $\{e\}, A_5$），
  而 $A_5$ 不是交換群，故 $S_5$（及含 $A_5$ 的群）無可解鏈——一般五次方程無根式解。
- 一般 $n$ 次方程的 Galois 群是 $S_n$；$x^3 - 2$ 的 Galois 群是 $S_3$（可解）。

### 線索三：尺規作圖三大難題的解決
Galois 理論（配合 Wantzel 1837 的域論證明）解決了古希臘三大難題：
- **化圓為方**：需作 $\sqrt{\pi}$，$\pi$ 是超越數，不在任何代數擴張中。不可作。
- **三等分任意角**：$60°$ 的三等分需解 $4x^3 - 3x - 1 = 0$，其 Galois 群非 2-冪群。
- **倍立方**：需作 $\sqrt[3]{2}$，$[\mathbb{Q}(\sqrt[3]{2}) : \mathbb{Q}] = 3$，不是 $2$ 的冪。
> **判準**：尺規可作圖的量必落在 $2$-冪次的塔狀擴張中，故其最小多項式次數必為 $2$ 的冪。
> （正 $n$ 邊形可作圖 ⟺ $n = 2^k p_1 \cdots p_r$，$p_i$ 為 Fermat 質數——Gauss 1796 已證。）

### Python 實作：計算 $x^3 - 2$ 的 Galois 群（$S_3$）

```python
from itertools import permutations, product
import cmath

# f(x) = x^3 - 2，分裂域 K = Q(2^(1/3), ω)，ω = e^{2πi/3}
omega = complex(-0.5, 3**0.5 / 2)
r = 2 ** (1/3)
roots = [r, r * omega, r * omega**2]
print("x^3 - 2 的三個根：", [f"{z:.4f}" for z in roots])

# Gal(K/Q) 的元素 = 根的置換且保持代數關係
# 根滿足 α·(ωα)·(ω²α) = 2，且 (ωα) = ω·α。
# 自同構由 α ↦ αᵢ 與 ω ↦ ω 或 ω² 決定，共 3 × 2 = 6 個 → Gal ≅ S3
def galois_elements():
    els = []
    for target in range(3):
        for w in [omega, omega**2]:
            # 定義映射：α ↦ roots[target], ω ↦ w（保持 αᵢ = ω α 的結構）
            mapping = {0: target}
            # ωα 對應哪個根？→ target 的下一個（在 ω 輪換中）
            cyc = [0, 1, 2] if w == omega else [0, 2, 1]
            mapping[1] = cyc[(cyc.index(target) + 1) % 3]
            mapping[2] = cyc[(cyc.index(target) + 2) % 3]
            els.append(tuple(mapping[k] for k in range(3)))
    return els

G = galois_elements()
print("Gal(x^3-2 / Q) 元素（根置換）：", G, "| 大小 =", len(set(G)), "≅ S3")

# 可解鏈：S3 ⊳ A3 ⊳ {e}，商群皆循環 → 根式解存在
A3 = [p for p in G if sum(1 for i, x in enumerate(p) if p[x] != x) in (0, 3) or p == (0,1,2) or p == (0,2,1)]
print("A3（3 階循環正規子群）元素：", sorted(set(p for p in G if p in [(0,1,2),(0,2,1),(0,1,2) and (0,1,2)])))
# 根式解：x = ∛2（實根），複根 = ∛2·ω, ∛2·ω² —— 全由根式表出 ✓
```

### 理論定義
> **定義（可解群）**：有限群 $G$ 可解 ⟺ 存在正規列 $G = G_0 \triangleright \cdots \triangleright G_m = \{e\}$
> 使 $G_i/G_{i+1}$ 為交換群（等價地：質數階循環群）。

## 結案 -- 後果與影響
- **1846 年 Liouville 出版手稿**，Camille Jordan 1870 年《Traité》將其系統化為「Galois 理論」。
- 案件的深遠影響：
  - **群論抽象化**：Cayley（1854）、Klein 的 Erlangen 綱領（1872）——「幾何 = 研究不變量下的變換群」。
  - **域論誕生**：Dedekind 的體（Körper）概念、理想論。
  - **尺規三大難題全部結案**（1837 Wantzel + 超越數理論 1882 Lindemann 證 $\pi$ 超越）。
  - **現代物理**：對稱性與守恆律（Noether 定理）、粒子物理的標準模型皆建立在群論之上。
- Galois 的遺書名句：「Je n'ai pas le temps.（我沒有時間了。）」
  他留下的 60 頁手稿改寫了整個數學的走向。

## 關鍵人物與文獻
| 人物 | 年份 | 貢獻 |
|------|------|------|
| Gauss | 1796 | 正 17 邊形可作圖、Fermat 質數判準 |
| Abel | 1826 | 一般五次方程無根式解 |
| Galois | 1832 | 決鬥前夜手稿：可解性 ⟺ 群可解 |
| Wantzel | 1837 | 尺規作圖判準的域論證明 |
| Liouville | 1846 | 出版 Galois 遺稿 |
| Jordan | 1870 | 《Traité des substitutions》系統化 |
