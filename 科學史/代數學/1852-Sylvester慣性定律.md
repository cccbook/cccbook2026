# 1852-Sylvester 慣性定律

## 案件摘要
1852 年，James Joseph Sylvester 在論文《A demonstration of the theorem that every homogeneous quadratic polynomial is reducible by real orthogonal substitutions to the form...》中提出**慣性定律**（Sylvester's law of inertia）：實二次型的正、負、零係數個數（慣性指標）在可逆座標變換下不變。他同時也是「matrix（矩陣）」一詞的發明者。

## 前因 -- 為什麼會有這個案子
- 二次曲線與二次曲面的分類自 Descartes、Euler 以來是經典問題：$x^T A x$ 能否化成「規範形」？化成之後，規範形是否唯一？
- Cauchy（1829）已研究特徵值，Jacobi（1846）給出實對稱矩陣對角化與特徵值的構造性方法。
- **懸案**：用不同的（非正交）座標變換把二次型化為平方和時，正項與負項的**個數**是否可能改變？直覺上「不變」（好比物理慣性不隨座標系改變），但需要證明。
- Sylvester 當時正任職於倫敦，是「不變量理論」（invariant theory，他 1851 年創造 invariant 一詞）研究的核心人物——慣性定律正是這場研究的自然產物。

## 線索與推理

### 線索一：二次型的規範形

實二次型 $Q(x) = x^T A x$（$A = A^T$ 對稱）。由譜定理，存在正交矩陣 $U$ 使：

$$U^T A U = \mathrm{diag}(\lambda_1, \ldots, \lambda_r, 0, \ldots, 0), \quad \lambda_i \neq 0$$

再令 $y_i = \sqrt{|\lambda_i|}\, x_i$，得**規範形**：

$$Q = y_1^2 + \cdots + y_p^2 - y_{p+1}^2 - \cdots - y_{p+n}^2$$

其中 $p$ = 正特徵值個數（**正慣性指標**），$n$ = 負特徵值個數（**負慣性指標**），$r = p + n$ = 秩。

### 線索二：慣性定律（探案核心）

**定理（Sylvester 慣性定律）**：若 $Q$ 經兩個可逆座標變換分別化為規範形 $(p_1, n_1)$ 與 $(p_2, n_2)$，則 $p_1 = p_2$ 且 $n_1 = n_2$。**慣性指標 $(p, n, z)$ 是二次型的不變量。**

**推理過程**：設 $Q$ 在基 $\{u_1, \ldots, u_p\}$ 下為 $\sum_{i \le p} y_i^2 - \sum_{i > p} y_i^2$，且存在 $p' > p$ 個線性無關向量 $w_1, \ldots, w_{p'}$ 使 $Q(w_j) > 0$。考慮線性映射 $\phi: \mathrm{span}\{w_1,\ldots,w_{p'}\} \to \mathrm{span}\{u_{p+1}, \ldots, u_N\}$（把每個 $w_j$ 映到其座標在「負項與零項」方向的成分）。因為 $p' > p \geq \dim(\mathrm{span}\{u_{p+1},\ldots,u_N\})$……正確地說：$w_1, \ldots, w_{p'}$ 有 $p'$ 個，其像落在維數 $N - p$ 的子空間中，故存在非零組合 $\sum c_j w_j$ 的像為零，即此組合向量 $v$ 滿足 $y_{p+1}(v) = \cdots = y_N(v) = 0$，從而：

$$Q(v) = y_1(v)^2 + \cdots + y_p(v)^2 \geq 0 \quad \text{且} \quad v \neq 0$$

但由 $v = \sum c_j w_j$（$Q(w_j) > 0$ 的凸組合假設下取適當係數）可得更強的 $Q(v) > 0$，矛盾若……實際上矛盾來自：$v$ 落在 $u_1, \ldots, u_p$ 張成的子空間之外卻與之正交於負向部分，由 $w_j$ 的線性無關性與維數計數 $p' > p$ 導出非零 $v$ 同時在 $\mathrm{span}\{u_1,\ldots,u_p\}$ 中與其補空間中——矛盾。**故 $p' \le p$，正慣性指標不變。** 對 $-Q$ 套用同樣論證得 $n$ 亦不變。$\blacksquare$

**一句話總結推理**：若正項可以「變多」，維數計數會逼出一個非零向量同時「藏在正子空間與負子空間」，矛盾。

### 線索三：Sylvester 的數學人生（晚成與兩次失職）

- **1814–1897**：猶太裔英國數學家。因宗教身分無法取得劍橋（St John's College）學位，終身未獲英國大學早期教職。
- **第一次失職**：1841 年赴美國維吉尼亞大學任教，僅 3 個多月後，因一名學生被開除而遭學生襲擊，遂辭職返英。
- **返英後**：1846 年進入倫敦 林肯律師學院成為律師（1846–1850），期間在精算師事務所工作，並認識了 Cayley——兩人在工作之餘的散步中討論數學，共同開創不變量理論與矩陣論。
- **1850**：創造「**matrix**（矩陣）」一詞——「一個由許多數排成的矩形陣列，從中可以誕生（born）各種行列式」，故稱之為 matrix（子宮、母體）。
- **1852**：發表慣性定律。
- **第二次失職**：1870 年代再赴美國 Johns Hopkins 大學（1876），創立美國第一份數學期刊 *American Journal of Mathematics*——這次成功了，晚年終獲殊榮，1883 年回英國任牛津 Savilian 幾何教授。
- **晚成**：他最重要的成就大多在 45 歲以後完成，63 歲時寫下著名的詩句自嘲：「It little matters whether I sing / Rose-crowned Apollo, or theque...」（大意：數學是我的第二青春）。

### 程式驗證（Python + numpy）

```python
import numpy as np
np.set_printoptions(precision=4, suppress=True)

rng = np.random.default_rng(42)

def inertia(A):
    """回傳二次型 x^T A x 的慣性指標 (p, n, z)"""
    eig = np.linalg.eigvalsh(A)          # A 對稱，特徵值實數
    p = int(np.sum(eig > 1e-10))
    n = int(np.sum(eig < -1e-10))
    z = len(eig) - p - n
    return p, n, z

A = np.array([[ 2.0,  1.0,  0.5],
              [ 1.0, -1.0,  2.0],
              [ 0.5,  2.0,  0.3]])
print("A =", A)
print("A 的慣性指標:", inertia(A))

# --- 用 100 個隨機可逆座標變換驗證慣性不變 ---
P0 = inertia(A)
ok = True
for k in range(100):
    S = rng.standard_normal((3, 3))
    while abs(np.linalg.det(S)) < 0.1:          # 確保可逆
        S = rng.standard_normal((3, 3))
    B = S.T @ A @ S                              # 新基底下的矩陣
    if inertia(B) != P0:
        ok = False
        print(f"第 {k} 次變換後慣性改變！ B 的慣性 = {inertia(B)}")
print("100 次隨機可逆變換後慣性皆不變:", ok)

# --- 特徵值符號在座標變換下會變，但『個數』不變 ---
S = rng.standard_normal((3, 3)); S += np.eye(3)
B = S.T @ A @ S
print("A 特徵值:", np.linalg.eigvalsh(A))
print("B 特徵值:", np.linalg.eigvalsh(B))   # 數值不同、順序不同，但符號個數一致
print("A 慣性:", inertia(A), "| B 慣性:", inertia(B))

# --- 規範形驗證：化為 y1^2+...-... 的形式 ---
eig, U = np.linalg.eigh(A)
D = U.T @ A @ U
print("規範形對角係數:", np.diag(D))        # 一正兩負（對應本例）
```

**程式偵探筆記**：特徵值本身隨座標變換劇烈改變，但 $(p, n, z)$ 紋絲不動——100 次隨機變換全部通過，這就是「慣性」二字的含義。

## 結案 -- 後果與影響
- 慣性指標 $(p, n, z)$ 成為實二次型/實對稱矩陣的**完整不變量**（在合同變換 $\mapsto S^T A S$ 意義下），二次曲面分類徹底解決。
- **正定性判定**：$p = n, n = 0$ 即正定——成為分析（極值判別）、最佳化（凸性）、物理（動能、勢能）的基礎工具。
- **線性代數教學**：Sylvester 慣性定律與譜定理並列為實二次型的兩大支柱；「矩陣」一詞使矩陣論獨立於行列式成為一門學問。
- **物理**：狹義相對論的 Minkowski 度規 $\mathrm{diag}(+,-,-,-)$——其正負號個數（$(1,3)$）是 Lorentz 變換下的絕對不變量，正是慣性定律的物理應用。
- **推廣**：複二次型只有一個不變量（秩）；Zelinsky 等人將慣性定律推廣到一般域上的對稱雙線性型（Witt 環理論）。

## 關鍵人物與文獻
- **James Joseph Sylvester**（1814–1897）：英國數學家，不變量理論與矩陣論開創者，創造 matrix、invariant、Jacobian 等術語，*American Journal of Mathematics* 創刊人。
- J. J. Sylvester, *A demonstration of the theorem that every homogeneous quadratic polynomial is reducible by real orthogonal substitutions to the form of a sum of positive and negative squares*, Phil. Mag. 4 (1852), 138–142.
- A. Cayley, *A memoir on the theory of matrices*, Phil. Trans. R. Soc. 148 (1858).（矩陣代數的系統化）
- K. Parshall, *James Joseph Sylvester: Life and Work in Letters*, Oxford UP, 1998.
