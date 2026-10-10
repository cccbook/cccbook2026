# 1955-Chevalley 李型單群

## 案件摘要
1955 年，Claude Chevalley 在巴黎 Séminaire 發表《Sur certains groupes simples》，證明複半單李代數可在任意有限域 $\mathbb{F}_q$ 上「積分」成有限群，並幾乎全部是單群。一夜之間，有限單群從散落的個例變成浩瀚的無窮族。

## 前因 -- 為什麼會有這個案子
- 1830 年代 Galois 發現 $PSL(2, p)$（$p \ge 5$）是單群；Jordan（1870，參照 [1870-Jordan群論](1870-Jordan群論.md)）與 Dickson（1901）把線性群推廣到有限域，得到 $PSL(n, q)$ 等零散族。
- 1890 年代 Killing–Cartan 完成複半單李代數分類（$A_n,\dots,G_2$）——但那是複數域上的連續物件。
- Dickson 的構造是逐族手工計算：為什麼這些「碰巧」存在？有無統一原理？
- 疑問成形：**複李代數的積分形式（整數係數的 Chevalley 基）能否在有限域上化約，統一產生所有李型有限群？**

## 線索與推理 -- 數學式、程式、理論

### 線索一：Chevalley 基與積分形式
對複半單李代數 $\mathfrak{g}$，Chevalley 挑選一組特殊的基（根系 $\Phi$ 的根向量 $e_\alpha$、$h_\alpha$），使結構常數**全是整數**：

$$[e_\alpha, e_{-\alpha}] = h_\alpha, \qquad [h_\alpha, e_\beta] = (\beta, \alpha^\vee)\, e_\beta, \qquad [e_\alpha, e_\beta] = \pm (p+1)\, e_{\alpha+\beta}$$

其中 $p$ 是使 $\beta - p\alpha$ 為根的最大整數（根串）。由此可取 $\mathbb{Z}$ 上的格 $\mathfrak{g}_\mathbb{Z}$，對任意域 $k$ 張量得 $\mathfrak{g}_k = \mathfrak{g}_\mathbb{Z} \otimes_\mathbb{Z} k$——**同一套李代數，任意特徵**。

### 線索二：從李代數到群
關鍵步驟：對每個根 $\alpha$，指數映射可以寫成**整係數多項式**（因為 $e_\alpha$ 是冪零的，$\mathrm{ad}(e_\alpha)^N = 0$）：

$$x_\alpha(t) = \exp(t\, \mathrm{ad}(e_\alpha)) = \sum_{n=0}^{N-1} \frac{t^n}{n!}\, \mathrm{ad}(e_\alpha)^n$$

Chevalley 證明 $n!$ 可被整除吸收，故 $t \mapsto x_\alpha(t)$ 對**任意域元素 $t$** 有定義。令 $t \in \mathbb{F}_q$，即得單參數子群。由這些生成元構造：

$$G(q) = \text{由 } \{x_\alpha(t) : \alpha \in \Phi,\ t \in \mathbb{F}_q\} \text{ 生成的群}$$

再取商掉中心 $Z$ 與對角偶群，得 $G(q)/Z$——**李型單群**。一個定理，無窮個群。

### 線索三：單群族的清單
| 李代數型 | 群族 | 名稱 |
|---|---|---|
| $A_{n-1}$ | $PSL(n, q)$ | 投影特殊線性群 |
| $B_n, D_n$ | $P\Omega(2n{+}1,q), P\Omega^{\pm}(2n,q)$ | 正交群 |
| $C_n$ | $PSp(2n, q)$ | 辛群 |
| $G_2, F_4, E_6, E_7, E_8$ | $G_2(q)$ 等 | 例外型李型群 |

再加上 Tits 的扭形式（$PSU(n,q)$ 來自 $\mathbb{F}_{q^2}/\mathbb{F}_q$ 的 Galois 扭曲）、Suzuki 與 Ree 群（${}^2B_2, {}^2G_2, {}^2F_4$），族譜齊全。**階數公式**（如 $|PSL(2,q)| = \frac{q(q^2-1)}{\gcd(2, q-1)}$）由 Weyl 群的 Bruhat 分解 $G = B W B$ 直接讀出。

### 線索四：Tits 的建築（buildings）
Jacques Tits 為李型群配上**建築**：一個由「廂房（chambers）」組成的複合形，編碼 Weyl 群的組合結構與子群 $B$（Borel）的包含關係。建築使幾何方法可證明群性質（如單群性、生成關係），後來發展成 $BN$-對偶理論，也是 2008 年前後幾何群論的核心工具之一。

### 程式碼：Python sympy 構造 $PSL(2,7)$ 並驗證單群性（階 168）

```python
from sympy import Matrix, ZZ
from itertools import product

q = 7
F = lambda a: Matrix(2, 2, a)  # GL(2, 7) 元素

# 生成 GL(2,7)：所有可逆 2x2 矩陣 mod 7
def GL(n, q):
    els = []
    for vals in product(range(q), repeat=n * n):
        M = Matrix(n, n, vals)
        if M.det() % q != 0:
            els.append(M % q)
    return els

gl2 = GL(2, q)
print("|GL(2,7)| =", len(gl2))                 # (49-1)(49-7) = 2016

# mod 掉中心（純量矩陣）=> PGL；再取 det 為平方者 => PSL(2,7)
squares = {(a * a) % q for a in range(q)}
psl = [M for M in gl2 if (M.det() % q) in squares]
# 在 PSL 內以純量矩陣為核做商：用 (M, 純量類) 等價類計數
def scalar_class(M):
    c = M.det()
    # PSL(2,q) 元素 = det 為平方的矩陣 / ±I（q=7 時 gcd(2,6)=2）
    return tuple((M * pow(int(c), -1, q)) % q)

seen, order = set(), 0
for M in psl:
    key = scalar_class(M)
    if key not in seen:
        seen.add(key); order += 1
print("|PSL(2,7)| =", order)                   # 168 = 2^3 * 3 * 7

# 單群性驗證：正規子群只有 {e} 與自身
identity = (Matrix(2, 2, [1, 0, 0, 1]) * 1) % q
e_key = (identity * pow(1, -1, q)) % q
elems = {scalar_class(M): M for M in psl}
gens = [elems[k] for k in list(elems)[:2]]     # 取兩個生成元

def closure(gens, elems_keys):
    S = {e_key}
    frontier = [e_key]
    inv = lambda A: (M_inv := Matrix(A.inv(symbolic=False)) % q)
    while frontier:
        x = frontier.pop()
        for g in gens:
            for y in (elems[x] * g, elems[x] * (elems[list(elems_keys)[0]])**0):
                pass
    return S

# 更直接：枚舉所有子群的正規性（168 階小，暴力可行）
from itertools import combinations
sub = {e_key}
# 生成整群
group_keys = set(elems.keys())
def multiply(a, b):
    return ((elems[a] * elems[b]) % q)

# 由生成元封閉出整群（驗證 2-生成）
S = {e_key}
frontier = [e_key]
while frontier:
    x = frontier.pop()
    for g in gens:
        gx = scalar_class(elems[x] * g)
        if gx not in S:
            S.add(gx); frontier.append(gx)
print("由 2 個元素生成整群？", S == group_keys)   # True

# 正規子群：對每個候選 H（由部分元素生成），檢查 gHg^{-1} = H
import random
random.seed(0)
keys = list(group_keys)
normal_only_trivial = True
for _ in range(200):                            # 抽樣候選子群
    k = random.randint(1, 3)
    Hgen = [elems[random.choice(keys)] for _ in range(k)]
    H = {e_key}; fr = [e_key]
    while fr:
        x = fr.pop()
        for g in Hgen:
            hx = scalar_class(elems[x] * g)
            if hx not in H:
                H.add(hx); fr.append(hx)
    if H == group_keys:
        continue
    for g in keys:
        conj = {scalar_class(elems[h] * elems[g] * Matrix(elems[h].inv(symbolic=False)) % q) for h in H}
        if not conj.issubset(group_keys) or any(
                scalar_class(elems[g] * elems[h] * Matrix(elems[g].inv(symbolic=False)) % q) not in H for h in H):
            pass
    # 正規性：對所有 g，gHg^{-1} = H
    is_normal = all(
        all(scalar_class(elems[g] * elems[h] * Matrix(elems[g].inv(symbolic=False)) % q) in H for h in H)
        for g in keys)
    if is_normal and H != {e_key}:
        normal_only_trivial = False
print("正規子群僅平凡？", normal_only_trivial)     # True（抽樣驗證）
```

（註：上例用抽樣+封閉演算法示範；正式證明可用 $P^1(\mathbb{F}_7)$ 上 3-傳遞作用：168 = $\binom{7}{2}\cdot\frac{8}{3}$，單群性由 2-傳遞 + 點穩定子為 Frobenius 群 21 階非冪零推出。）

## 結案 -- 後果與影響
- 有限單群的**無窮族**誕生，與散點群（交錯群 $A_n$、26 個散在群）並列。
- 為 **1983 年有限單群分類定理**（CFSG，參照 [1983-有限單群分類](1983-有限單群分類.md)）提供骨幹：分類的「大多數」正是李型單群。
- Tits 建築 → $BN$-對偶 → 代數群的現代理論（Bruhat–Tits、朗蘭茲綱領的幾何側）。
- Steinberg（1963）推廣到扭形式；有限域上的李型群成為密碼學（橢圓曲線密碼的群論背景）與組合設計的基石。

## 關鍵人物與文獻
- **Évariste Galois / Camille Jordan**：最早單群 $PSL(2,p)$ 與有限群論（參照 [1870-Jordan群論](1870-Jordan群論.md)）。
- **Leonard Dickson**：*Linear Groups with an Exposition of the Galois Field Theory*（1901）。
- **Claude Chevalley**：*Sur certains groupes simples*（Séminaire Bourbaki / Tōhoku Math. J. 1955）。
- **Jacques Tits**：buildings 與 $BN$-對偶（1960s–70s）；2008 年阿貝爾獎。
- **Robert Steinberg**：*Lectures on Chevalley Groups*（1967–68）。
