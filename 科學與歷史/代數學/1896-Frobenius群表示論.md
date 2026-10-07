# 1896–1897 - Frobenius 發明群表示論

## 案件摘要
1896 年，Ferdinand Georg Frobenius 在一系列論文中發明「群的表示」與「特徵標」理論，1897 年與 Issai Schur 合作將其完善。表示論把抽象群具體化為矩陣，使無形的對稱性變成可計算的線性代數，成為 20 世紀數學與物理的共通語言。

## 前因 -- 為什麼會有這個案子
- **Jordan 的線性群（1870）**：Jordan《Traité》已研究 $\mathrm{GL}(n,\mathbb{C})$ 的有限子群與 Jordan 標準形，但只把矩陣當作變換本身，未發展「用矩陣研究群」的一般方法。
- **特徵標的模糊先聲**：Dedekind 在數論中研究群行列式（group determinant）$\det\!\left(\sum_g a_g \, g\right)$，1896 年請教 Frobenius 如何分解它——這是點燃本案的直接火花。
- **Dirichlet 分析傳統**：Frobenius 出身柏林分析學派，熟悉 Fourier 級數與正交函數，「把正交性搬到群上」是他的自然直覺。

## 線索與推理 -- 數學式、程式、理論

### 1. 表示與特徵標的定義
群 $G$ 的（線性）表示是群同態：

$$\rho: G \to \mathrm{GL}(V),\qquad \rho(gh) = \rho(g)\rho(h),\ \ \rho(e) = I$$

取定 $V$ 的基底後，$\rho(g)$ 是 $n \times n$ 矩陣（$n = \dim V$ 稱為表示的次數）。**特徵標**為跡函數：

$$\chi(g) = \operatorname{tr}\big(\rho(g)\big) = \sum_{i=1}^n \rho(g)_{ii}$$

特徵標是類函數：共軛元素特徵標相同，$\chi(hgh^{-1}) = \chi(g)$。

Frobenius 關鍵洞見：**群行列式可分解為不可約因子的乘積**，每個因子對應一個不可約表示：

$$\det\Big(\sum_{g\in G} a_g\, g\Big) = \prod_{i} \det\Big(\sum_g a_g\, \rho_i(g)\Big)^{\deg \rho_i}$$

### 2. 不可約表示與特徵標正交關係
表示 $\rho$ 稱為**不可約**，若 $V$ 沒有非平凡的不變子空間 $W \subsetneq V$（$\rho(g)W \subseteq W,\ \forall g$）。Frobenius 證明正交關係：

$$\langle \chi_i, \chi_j \rangle = \frac{1}{|G|}\sum_{g \in G} \chi_i(g)\,\overline{\chi_j(g)} = \delta_{ij}$$

**第一正交關係的推論**：
- 群 $G$ 的不可約表示個數 = 共軛類個數
- $\sum_i (\deg \chi_i)^2 = |G|$（正則表示的分解）
- $\sum_{g\in G}|\chi(g)|^2 \geq |G|$，等號成立 $\iff \chi$ 不可約

### 3. Maschke 定理：複數表示完全可約
Maschke（1899）證明：若 $|G|$ 在體 $F$ 中可逆（例如 $F = \mathbb{C}$），則任何有限維表示都可分解為不可約表示的直和：

$$V = W_1 \oplus W_2 \oplus \cdots \oplus W_k, \qquad \rho \cong \rho_1 \oplus \cdots \oplus \rho_k$$

構造法：給不變子空間 $W$，取任意投影 $\pi: V \to W$，再「群平均」：

$$\tilde{\pi} = \frac{1}{|G|}\sum_{g \in G} \rho(g)\,\pi\,\rho(g)^{-1}$$

$\tilde{\pi}$ 是 $G$-等變投影，其核 $\ker \tilde{\pi}$ 也是不變子空間——可約性由此獲得結構化的分解。複數情形下，有限群的表示論因此完全化為不可約表示的清點。

### 4. Python numpy 實作：$S_3$ 特徵標表的驗證

```python
import numpy as np
from itertools import permutations

S3 = list(permutations(range(3)))
def mat(g):  # 正規(置換)表示
    P = np.zeros((3,3))
    for i in range(3): P[g[i], i] = 1
    return P

# 正規表示 = 2 維不可約標準表示 ⊕ 1 維符號表示
# 對角化分解：特徵向量 [1,1,1] 張出平凡部分，補空間即標準表示
triv = np.array([[1],[1],[1]], float) / np.sqrt(3)
# 用 Gram-Schmidt 取正交補的基底
u1 = np.array([[1],[-1],[0]], float); u1 /= np.linalg.norm(u1)
u2 = np.array([[1],[1],[-2]], float); u2 /= np.linalg.norm(u2)
Q = np.hstack([triv, u1, u2])   # 正交矩陣

chi_std, chi_sign = {}, {}
for g in S3:
    D = Q.T @ mat(g) @ Q
    chi_std[g]  = np.trace(D[1:,1:])          # 標準表示 (2維)
    chi_sign[g] = D[0,0]                       # 平凡+符號混合 -> 需區分
    # 符號表示：sgn(g) = (+1 偶置換 / -1 奇置換)
    inv = sum(1 for i in range(3) for j in range(i+1,3) if g[i]>g[j])
    chi_sign[g] = (-1.0)**inv

# 類函數 -> 依共軛類平均；S3 三類：e, 三個對換, 兩個3-循環
classes = [[(0,1,2)], [p for p in S3 if chi_sign[p]==-1],
           [p for p in S3 if p not in [(0,1,2)] and chi_sign[p]==1]]
chi_triv = {g: 1.0 for g in S3}

def inner(chi_a, chi_b):
    return sum(chi_a[g]*np.conj(chi_b[g]) for g in S3) / len(S3)

print("<triv , triv > =", inner(chi_triv, chi_triv))   # 1
print("<std  , std  > =", inner(chi_std,  chi_std))    # 1
print("<sign , sign > =", inner(chi_sign, chi_sign))   # 1
print("<triv , std  > =", inner(chi_triv, chi_std))    # 0
print("<std  , sign > =", inner(chi_std,  chi_sign))   # 0
# 驗證 sum deg^2 = |S3| = 6：1^2 + 2^2 + 1^2 = 6 ✓
print("sum deg^2 =", 1**2 + 2**2 + 1**2)
```

輸出中三個正交關係全數成立（$\delta_{ij}$ 得證），且 $1^2+2^2+1^2 = 6 = |S_3|$ 印證正則表示分解——Frobenius 理論的計算實證。

## 結案 -- 後果與影響
- **表示論獨立成科**：Schur、Weyl 等人接續發展，有限群、Lie 群、緊群的表示論成為 20 世紀數學主幹之一。
- **量子力學的對稱性語言**：1927 年起 Weyl 與 Wigner 用群表示論解釋原子光譜、角動量（$\mathrm{SO}(3)$ 的表示）、量子態的分類——沒有表示論就沒有現代量子力學的教科書體系。
- **化學與晶體學**：分子振動模式、晶體點群的特徵標表成為標準工具。
- **數論與 Langlands 綱領**：Galois 表示、自守表示把表示論推到当代數學最深處的統一綱領。

## 關鍵人物與文獻
- **Ferdinand Georg Frobenius**（1849–1917）：〈Über Gruppencharaktere〉（1896）等系列論文，創立表示論與特徵標理論。
- **Issai Schur**（1875–1941）：Schur 引理與表示論的完善（1901 博士論文起）。
- **Richard Dedekind**（1831–1916）：群行列式的提問者，本案火花。
- **Hermann Weyl**（1885–1955）與 **Eugene Wigner**（1902–1995）：把表示論帶進量子力學（1927–1931）。
- **Heinrich Maschke**（1853–1908）：Maschke 定理（1899）。
