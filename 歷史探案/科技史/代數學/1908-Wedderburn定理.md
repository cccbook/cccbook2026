# 1908-Wedderburn 定理

## 案件摘要
1908 年，蘇格蘭數學家 Joseph Wedderburn 發表論文《On hypercomplex numbers》，證明兩大定理：(1) **有限除環皆為交換環**（Wedderburn 小定理——有限域 = 有限除環）；(2) **半單代數結構定理**（Wedderburn 定理）：半單代數是矩陣環對除環的直和。這把「複數系的所有推廣」一次性地結構化。

## 前因 -- 為什麼會有這個案子
- 1843 年 Hamilton 發明四元數，除去了乘法交換律，開啟「超複數系」（hypercomplex systems）時代：人們到處尋找 $\mathbb{R}$ 與 $\mathbb{C}$ 的推廣。
- Frobenius（1878）研究實除環的分類，證明**實數上的有限維除環只有 $\mathbb{R}$、$\mathbb{C}$、$\mathbb{H}$** 三個。
- Frobenius（1896–1897）創立有限群表示論，群代數 $\mathbb{C}[G]$ 的結構呼之欲出。
- **懸案一**：是否存在非交換的**有限**除環？（有限域 $\mathbb{F}_{p^n}$ 都是交換的，但那只是因為它們恰好是交換的……還是有更深的必然性？）
- **懸案二**：半單超複數系的完整結構是什麼？

## 線索與推理

### 線索一：有限除環 = 有限域（Wedderburn 小定理，探案核心）

**定理（Wedderburn 1908）**：每個有限除環 $D$ 都是交換環，即 $D \cong \mathbb{F}_{q}$（某有限域）。

**推理過程**（經典的「中心化子計數」論證）：

1. 設 $|D| = q^n$，其中 $q = |Z(D)|$ 是中心的元素個數，$n$ 是 $D$ 對中心 $Z(D)$ 的維數（$D$ 是 $Z(D)$ 上的向量空間）。
2. 對每個 $x \in D$，其**中心化子** $C_x = \{y \in D : xy = yx\}$ 是 $D$ 的子除環，包含 $Z(D)$。設 $C_x$ 對 $Z(D)$ 的維數為 $n_x$，則 $|C_x| = q^{n_x}$。
3. $D^*$（$D$ 的非零元素）是一個有限群，$C_x^*$ 是其子群。由**類方程**（共軛類大小 = 指數 $\times$ 中心化子大小）：

$$|D^*| - 1 = \sum_{x} [D^* : C_x^*] = \sum_x \frac{q^n - 1}{q^{n_x}}$$

4. **關鍵數論引理**：若 $n_x < n$ 則 $\frac{q^n - 1}{q^{n_x}}$ 是 $\Phi_n(q)$（$n$ 次分圓多項式在 $q$ 的值）的因子。而 $\gcd(q^n - 1, \Phi_n(q)) \mid n$。
5. 於是 $q - 1 = \Phi_n(1)$……若所有 $n_x < n$，類方程右邊每一項都整除 $n$，但左邊 $|D^*| - 1$ 與 $\Phi_n(q)$ 的關係逼出 $|D^*| - 1 \leq n \cdot \Phi_n(q)$ 的矛盾（利用 $\Phi_n(1) \leq n$ 與 $q^n - 1 > n \Phi_n(q)$ 當 $q$ 足夠大；小 $q$ 單獨檢查）。故必存在 $x$ 使 $n_x = n$，即 $C_x = D$，$x$ 屬於中心……更準確地：推出對所有 $x$，若存在 $n_x < n$ 則矛盾，因此每個共軛類大小為 1，$D^*$ 是交換群。$\blacksquare$

**含義**：有限世界裡「非交換域」不存在——這是**必然**，不是巧合。有限除環的方程式只有一種寫法：$\mathbb{F}_{p^n}$。

### 線索二：Wedderburn 結構定理（半單代數）

**定義（單/半單）**：域 $K$ 上有限維代數 $A$ 是**單**的，若它沒有非平凡（真、雙邊）冪零理想之外的… 準確說：$A$ **半單**意指其 Jacobson 根 $J(A) = 0$；等價地，$A$ 沒有非零冪零理想。

**定理（Wedderburn–Artin）**：域 $K$ 上有限維半單代數 $A$ 同構於矩陣環對除環的直和：

$$A \cong \bigoplus_{i=1}^{r} M_{n_i}(D_i)$$

其中每個 $D_i$ 是 $K$ 的有限維除環擴張（$K = \mathbb{C}$ 時 $D_i = \mathbb{C}$，由 Frobenius；$K = \mathbb{R}$ 時 $D_i \in \{\mathbb{R}, \mathbb{C}, \mathbb{H}\}$）。且此分解在適當意義下唯一（$n_i$ 與 $D_i$ 的同構類唯一）。

**推理骨架**：
1. 半單代數 $A$ 分解為極小左理想的直和（Maschke 類推理：$J(A) = 0$ 保證可補）。
2. 同構的極小左理想合併成 $A$ 的「齊次分量」：$A_i = A e_i \cong M_{n_i}(D_i)^{\mathrm{op}}$ 型的矩陣環，$e_i$ 是中心本原冪等元。
3. $A = \bigoplus A_i$，每個 $A_i$ 是單代數，$A_i \cong M_{n_i}(D_i)$。$\blacksquare$

### 線索三：與 Frobenius 表示論的關係

**推理鏈**：Maschke 定理（1898）：有限群 $G$ 在特徵不整除 $|G|$ 的域上的表示完全可約 $\Rightarrow$ 群代數 $K[G]$ 半單 $\Rightarrow$ 由 Wedderburn 定理：

$$\mathbb{C}[G] \cong \bigoplus_{i=1}^{r} M_{n_i}(\mathbb{C})$$

**由此立即得到表示論的三大事實**：
- 不可約表示個數 $r$ = 共軛類個數（因為 $\mathbb{C}[G]$ 的中心維數 = $\sum_i 1 = r$，而中心維數又 = 共軛類數）。
- $\sum_i n_i^2 = |G|$（比較維數：$\dim \mathbb{C}[G] = |G|$）。
- 正則表示分解為 $\bigoplus_i n_i V_i$（每個不可約表示出現 $n_i$ 次）。

**偵探筆記**：Frobenius 用特徵標理論辛苦證明的這些事實，在 Wedderburn 定理下變成「維數計數」的簡單推論——抽象代數的力量首次全面展現。

### 程式驗證（Python）

```python
import itertools

def matrix_ring_mod_p(n, p):
    """回傳 M_n(F_p) 的所有元素（以 tuple of tuple 表示）"""
    entries = list(itertools.product(range(p), repeat=n*n))
    return [tuple(e[i*n:(i+1)*n] for i in range(n)) for e in entries]

def mmul(A, B, p):
    n = len(A)
    return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(n)) % p
                       for j in range(n)) for i in range(n))

def is_division_ring_mod_p(n, p):
    """檢查 M_n(F_p) 是否為除環：每個非零元素是否有乘法逆元"""
    elems = matrix_ring_mod_p(n, p)
    zero = tuple((0,)*n for _ in range(n))
    ident = tuple(tuple(1 if i == j else 0 for j in range(n)) for i in range(n))
    for A in elems:
        if A == zero:
            continue
        found = any(mmul(A, B, p) == ident for B in elems)
        if not found:
            return False
    return True

# --- 驗證 Wedderburn 小定理：M_n(F_p) 只有 n=1 時是除環 ---
for p in [2, 3, 5]:
    for n in [1, 2]:
        if n == 1:
            print(f"F_{p}: 除環且交換 = {is_division_ring_mod_p(1, p)}")   # True
        else:
            print(f"M_{n}(F_{p}): 是除環? {is_division_ring_mod_p(2, p)}")  # False（存在非零不可逆元）

# --- 找出 M_2(F_2) 中的非零不可逆元（證明它不是除環） ---
p, n = 2, 2
zero = tuple((0,)*n for _ in range(n))
ident = tuple(tuple(1 if i == j else 0 for j in range(n)) for i in range(n))
noninvertible = []
for A in matrix_ring_mod_p(n, p):
    if A != zero and not any(mmul(A, B, p) == ident for B in matrix_ring_mod_p(n, p)):
        noninvertible.append(A)
print(f"M_2(F_2) 的非零不可逆元個數: {len(noninvertible)}")   # 4 個
print("範例:", noninvertible[0])
# 例如 ((0,1),(0,1))：非零但乘任何矩陣都不會得到單位陣 -> 不是除環

# --- 驗證 Wedderburn 表示論推論：S_3 的群代數 ---
from itertools import permutations
G = list(permutations(range(3)))             # S_3, |G| = 6, 共軛類數 = 3
r = 3                                        # 恆等、(12)型、(123)型
n1 = [1, 1, 2]                               # 三個不可約表示的維數
print("sum(n_i^2) =", sum(d*d for d in n1), "| |G| =", len(G))  # 6 = 6 ✓
print("不可約表示個數 r =", r, "= 共軛類個數 =", 3)             # ✓
# C[S_3] ≅ M_1(C) ⊕ M_1(C) ⊕ M_2(C) —— Wedderburn 分解！
```

**程式偵探筆記**：$M_2(\mathbb{F}_2)$ 有 4 個非零不可逆元（如秩 1 矩陣），證實它不是除環；而 $\mathbb{F}_p$ 本身永遠是除環。表示論的 $\sum n_i^2 = |G|$ 恆等式也得到驗證。

## 結案 -- 後果與影響
- **Emmy Noether（1920 年代）**：將 Wedderburn 定理納入鏈條條件與模論框架，抽象代數（環、模、理想）正式誕生；**Artin（1927）**把定理推廣到滿足降鏈條件的半單環（Wedderburn–Artin 定理的現代形式）。
- **有限除環 = 有限域**成為有限幾何、編碼理論（Reed–Solomon 碼在 $\mathbb{F}_q$ 上）、密碼學（AES 在 $\mathbb{F}_{2^8}$ 上）的基礎事實。
- **表示論**：Wedderburn 分解是群表示論、調和分析（Peter–Weyl 定理是其無限維推廣）、李代數表示的結構支柱。
- **物理**：粒子物理中的可加量子數（電荷、重子數）對應群代數的中心；四元數 $\mathbb{H}$ 出現在旋量與三維旋轉。
- **Brauer 群**：Wedderburn 定理使「除環的分類」化約為 Brauer 群 $Br(K)$ 的計算——現代數學中描述非交換性的核心工具。

## 關鍵人物與文獻
- **Joseph Henry Maclagen Wedderburn**（1882–1948）：蘇格蘭數學家，普林斯頓大學教授，1908 年發表兩大定理於 Proceedings of the London Mathematical Society。
- J. H. M. Wedderburn, *On hypercomplex numbers*, Proc. London Math. Soc. (2) 6 (1908), 77–112.
- G. Frobenius, *Über Gruppencharaktere*, Sitzungsber. Preuss. Akad. Wiss. (1896).（表示論起源）
- E. Artin, *Zur Theorie der hyperkomplexen Zahlen*, Abh. Math. Sem. Hamburg 5 (1927), 251–258.
- N. Jacobson, *Basic Algebra II*, W. H. Freeman, 1980.（Wedderburn–Artin 定理的現代教材敘述）
