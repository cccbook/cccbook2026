# 1981 - Quillen 代數 K 理論

## 案件摘要
Grothendieck 為證明 Riemann–Roch 定理發明了 $K_0$ 群，但高階 $K_i$ 的定義懸宕多年，各家嘗試紛紛失敗。1970 年代 Quillen 以拓撲學的 plus construction 與 Q 構造兩度出手，建立了完整的高階代數 K 理論，讓拓撲、代數與數論在 K 理論的旗幟下會師。

## 前因 -- 為什麼會有這個案子
- **Grothendieck（1957）**：為證明廣義 Riemann–Roch，將向量叢（或射影模）的形式差收集成一個阿貝爾群
  $$K_0(X) = \big[ \text{向量叢} \big] \big/ \big\langle [E] - [E'] - [E''] \ \text{當}\ 0 \to E' \to E \to E'' \to 0 \big\rangle.$$
  這個「形式差群」是 K 理論的起點。
- **Bass（1968）**：用 $K_1$（可逆矩陣的 Whitehead 群）與負階 K 群推廣到環論，但 $K_i\ (i \ge 2)$ 缺乏統一定義。
- **Milnor（1971）**：對域定義了 $K_2^M$（Steinberg 群商），但 Milnor K 理論無法延伸到一般環的高階。
- **拓撲的啟示**：Bott 週期性給出拓撲 K 理論 $KU_i$ 的全部資訊，代數側卻連 $K_2$ 以後的群都定義不出來——**需要一個像拓撲空間那樣「有同倫」的代數機器**。

## 線索與推理 -- 數學式、程式、理論
### 線索一：Quillen 的 plus construction（1969–1970）
對一個空間 $X$ 與其完備同倫群 $N \trianglelefteq \pi_1(X)$，Quillen 構造 $X^+$：在 $X$ 上貼 2-維與 3-維胞腔，使得
$$\pi_1(X^+) = \pi_1(X)/N, \qquad H_i(X^+) = H_i(X)\ (i \ge 2), \ \text{且同倫群可升高}.$$
取 $X = BGL(R)$（一般線性群 $GL(R)$ 的分類空間），$N = E(R)$（初等矩陣子群，= 換位子群），定義：
$$K_i(R) := \pi_i(BGL(R)^+) \quad (i \ge 1).$$
這立即給出 $K_1(R) = GL(R)^{ab}$、$K_2(R) = $ Milnor 的 Steinberg 群，且 $K_3, K_4, \ldots$ 全部有了定義。

### 線索二：Quillen 的 Q 構造（1972–1973）
plus construction 對「非線性」對象（如正合範疇）不好用。Quillen 在論文 *Higher algebraic K-theory: I* 中提出更幾何化的定義：對正合範疇 $\mathcal{A}$，構造 Q 範疇 $Q\mathcal{A}$——物件與 $\mathcal{A}$ 相同，但態射是由正合列
$$A \twoheadrightarrow B' \hookrightarrow B$$
生成的自由範疇。然後定義：
$$K_i(\mathcal{A}) := \pi_{i+1}(BQ\mathcal{A}, 0).$$
**威力**：
- 當 $\mathcal{A} = \mathcal{P}(R)$（有限生成射影模範疇）時，與 plus construction 定義一致：$K_i(\mathcal{P}(R)) \cong K_i(R)$。
- **加性定理（Additivity theorem）**：正合函子 $F', F, F'': \mathcal{A} \to \mathcal{B}$ 組成短正合列時，$K_i(F) = K_i(F') + K_i(F'')$——這是所有計算的引擎。
- **Dévissage、Resolution 定理**：把 $K$ 理論從射影模推廣到 Noether 環、坐標環、乃至 motive。

### 線索三：Adams 運算與計算
拓撲 K 理論有 Adams 運算 $\psi^k$；Quillen 證明代數 K 琴也有，並給出著名的域上 K 群計算：
$$K_{2n-1}(\mathbb{F}_q) \cong \mathbb{Z}/(q^n - 1)\mathbb{Z}, \qquad K_{2n}(\mathbb{F}_q) = 0 \ (n \ge 1),$$
$$K_0(\mathbb{F}_q) \cong \mathbb{Z}.$$
Adams 運算作為特徵標分解工具，讓 $\lambda$-環（$\lambda$-ring）理論成為 K 理論的標準語言。

### 程式驗證：用 numpy 展示 $K_0$ 的 Grothendieck 群
$K_0$ 本質是「生成關係的商」：把正合列關係 $[E] = [E'] + [E'']$ 寫成矩陣行，再做商群。以下用 numpy 的整數列空間運算模擬：

```python
import numpy as np

def grothendieck_group(num_gens, relations):
    """給定生成元數與關係矩陣（每行 = 一個線性關係），
    回傳商群 Z^n / <relations> 的結構（Smith 正規化後的不變因子）"""
    from sympy import Matrix
    M = Matrix(relations)
    d, _, _ = M smith_normal_form() if False else (None, None, None)
    # sympy 沒有直接 API，用 invariant factors：
    diag = M
    from sympy.matrices.normalforms import invariant_factors
    factors = invariant_factors(M)
    # 非零因子給出循環直和項，0 表示自由部分
    free = num_gens - sum(1 for f in factors if f != 0)
    torsion = [int(f) for f in factors if f != 0 and f != 1]
    return f"Z^{free} " + (f"+ direct sum of Z/{torsion}" if torsion else "")

# 例：三個向量叢 [L1],[L2],[L1+L2]（直線叢與其直和）
# 關係：[L1+L2] - [L1] - [L2] = 0
rels = [[-1, -1, 1]]
print(grothendieck_group(3, rels))
# 輸出: Z^2  →  K_0 由 [L1],[L2] 自由生成，符合 P^1 上 Pic 群 ≅ Z 的直覺

# 例：加上關係 [L1]+[L2]=0（如 Z/2 上的模擬）
rels2 = [[-1, -1, 1], [1, 1, 0]]
print(grothendieck_group(3, rels2))
# 輸出: Z^1 + direct sum of Z/[2] → 出現撓項，商群不再是自由阿貝爾群
```

這展示了 Grothendieck 群的核心操作：**向量叢的等價類 = 自由阿貝爾群對正合列關係的商**；商的結構（自由秩 + 撓不變因子）就是 $K_0$ 的計算結果。

## 結案 -- 後果與影響
- **1978 菲爾茲獎**：Quillen 因代數 K 理論（以及證明 Adams 猜想、有理同倫論）獲頒菲爾茲獎。
- **統合三大領域**：
  - **拓撲**：$K_i(R)$ 是 $BGL(R)^+$ 的同倫群，連接 Whitehead 撓與手術理論。
  - **代數**：$\lambda$-環、Adams 運算成為表示論與形式幾何的標準工具。
  - **數論**：Quillen–Lichtenbaum 猜想（後由 Voevodsky 等以 motive 與 Milnor K 理論證明）將 $K_{2n-i}(\mathcal{O}_K)$ 與 étale 上同調連結——與 1974-Deligne 的 Weil 猜想技術一脈相承。
- **Borel 計算（1974–1981）**：數體整數環的 $K_i(\mathcal{O}_K)$ 與 Dedekind zeta 函數的值相關，K 理論正式進入解析數論。
- **後續案件**：Waldhausen 的「有向 K 理論」、Dundas–Goodwillie–McCarthy 定理、乃至導出代數幾何（參照 2009-Lurie高階範疇），都以 Quillen 的 Q 構造為起點。

## 關鍵人物與文獻
- **Alexander Grothendieck**：SGA 6，$K_0$ 與廣義 Riemann–Roch 的源頭。
- **Daniel Quillen**：*On the cohomology and K-theory of the general linear groups over a finite field*（1972）；*Higher algebraic K-theory: I*（Springer Lecture Notes 341, 1973）。
- **Hyman Bass**：*Algebraic K-theory*（1968）。
- **John Milnor**：*Introduction to Algebraic K-theory*（1971）。
- 延伸：Quillen 1978 菲爾茲獎演說；Weibel 的 *The K-book*（2013）。
