# 1870 - Jordan《Traité des substitutions》與群論的誕生

## 案件摘要
1870 年，Camille Jordan 出版《Traité des substitutions et des équations algébriques》，把散落於 Galois 手稿中的「 substitution（置換）」觀念整理成嚴密體系。這是史上第一本系統的群論專著，使「群」從解方程的工具躍升為獨立的數學研究對象。

## 前因 -- 為什麼會有這個案子
- **Galois 的遺產（1832）**：Évariste Galois 為判別五次方程何時可用根式求解，引入「根的置換集合在運算下封閉」的想法，但手稿晦澀、直到 1846 年才由 Liouville 出版。
- **置換群的前期工作**：Ruffini 與 Abel 證明一般五次方程無根式解；Cauchy 在 1815–1845 年間系統研究置換的循環結構，提出 Cauchy 定理（若素數 $p \mid |G|$ 則 $G$ 有 $p$ 階元素）。
- **懸案**：Galois 理論缺乏系統的語言與證明骨架；「什麼是群」尚未有公理化定義；線性變換的標準型也未釐清。Jordan 接手這樁懸案。

## 線索與推理 -- 數學式、程式、理論

### 1. 群的系統化定義
Jordan 書中對「 substitution 群」給出接近現代的定義（今日以抽象化後的公理表述）：

$$\text{群 } (G, \cdot)：\quad a,b \in G \Rightarrow ab \in G,\ \ (ab)c = a(bc),\ \ \exists e,\ a e = a,\ \ \exists a^{-1},\ aa^{-1} = e$$

由此催生了一整套詞彙：子群、正規子群、商群、同構、單群、可解群。

### 2. Jordan–Hölder 定理（合成列的因子唯一性）
Jordan（1870）證明合成列長度與因子的本質不變，Hölder（1889）補足完全嚴格的表述：

$$G = G_0 \triangleright G_1 \triangleright G_2 \triangleright \cdots \triangleright G_n = \{e\}$$

其中每一步 $G_{i+1} \trianglelefteq G_i$ 為極大正規子群，合成因子

$$G_i / G_{i+1} \quad \text{皆為單群}$$

**定理**：任意兩條合成列的合成因子（不計順序與同構）相同——這是有限群的「化學元素表」，群由這些單群因子一層層「堆疊」而成。

```python
from itertools import permutations

# S3 的合成列： S3 ⊃ A3 ⊃ {e}，因子 = S3/A3 ≅ Z2, A3 ≅ Z3
S3 = list(permutations(range(3)))
def compose(a, b):  # (a∘b)(x) = a(b(x))
    return tuple(a[b[i]] for i in range(3))
e = (0, 1, 2)
A3 = [g for g in S3 if sum(1 for i in range(3) for j in range(i+1,3) if g[i]>g[j]) % 2 == 0]
print("A3 =", A3, "|S3| =", len(S3), "|A3| =", len(A3))
print("合成因子階數：", len(S3)//len(A3), len(A3)//1)   # 2, 3 皆為素數 -> S3 可解
```

### 3. 可解性與 Galois 理論的系統化
Jordan 將「根式可解」精確翻譯成群的語言：方程 $f(x)=0$ 可用根式求解 $\iff$ 其 Galois 群**可解**，即存在合成列使所有因子皆為循環群：

$$\{e\} = G_n \trianglelefteq G_{n-1} \trianglelefteq \cdots \trianglelefteq G_0, \qquad G_i/G_{i+1} \cong \mathbb{Z}_{p_i}$$

五次以上一般方程的 Galois 群 $S_5$ 含單群 $A_5$（非循環），故不可解——Galois 的結論至此獲得清晰、可教的證明。

### 4. 線性群與 Jordan 正規形式
Jordan 在書中研究 $\mathrm{GL}(n,\mathbb{C})$ 的子群（今日稱「線性群」），並證明複數域上的矩陣在相似變換 $A \mapsto PAP^{-1}$ 下可化為 Jordan 標準形：

$$A \sim \begin{pmatrix} J_{k_1}(\lambda_1) & & \\ & \ddots & \\ & & J_{k_m}(\lambda_m) \end{pmatrix},\qquad J_k(\lambda) = \lambda I_k + N,\ N = \begin{pmatrix} 0 & 1 & & \\ & 0 & \ddots & \\ & & \ddots & 1 \\ & & & 0 \end{pmatrix}$$

這給出線性變換分類的完整答案，也是有限階矩陣 $A^n = I$ 構成有限線性群的結構基礎。

## 結案 -- 後果與影響
- **群論獨立成科**：從 Jordan 之後，「群」成為數學的基本語言，抽象群公理化由 Cayley（1854）奠基、經 Weber 與 Hölder 完成。
- **直接啟發 Klein 與 Lie**：Klein 的 Erlangen 綱領（1872）以變換群統一幾何；Sophus Lie 受 Jordan 的線性群影響，發展連續群（Lie 群）理論。
- **有限單群分類**：Jordan–Hölder 定理是 20 世紀有限單群分類（CFSG，1983）的起點。
- ** representation theory 的溫床**：Jordan 的學生與後繼者（如 Frobenius）在其線性群基礎上發明群表示論。

## 關鍵人物與文獻
- **Camille Jordan**（1838–1922）：《Traité des substitutions et des équations algébriques》（Paris: Gauthier-Villars, 1870）。
- **Évariste Galois**（1811–1832）：遺稿為本案的原始線索。
- **Otto Hölder**（1859–1937）：Jordan–Hölder 定理的完全證明（1889）。
- **Arthur Cayley**（1821–1895）：抽象群公理的先聲。
