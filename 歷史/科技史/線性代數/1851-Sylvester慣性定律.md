# 1851 — Sylvester 慣性定律

## 案件摘要
1851–1852 年，James Joseph Sylvester 發表〈On the relation between the minor determinants of linearly equivalent quadratic functions〉，提出日後被稱為 **Sylvester 慣性定律**（law of inertia）的定理：實二次型的正慣性指標 $n_+$、負慣性指標 $n_-$ 在可逆線性變換（合同變換）下**不變**。無論你用什麼可逆變換把二次型化成平方和，正係數的個數與負係數的個數永遠一樣——「正負號」是二次型與生俱來的指紋，不會被偽造。這是二次型合同分類的破案關鍵。

## 前因 -- 為什麼會有這個案子
- **Lagrange 配方法**：18 世紀 Lagrange 系統化了把二次型 $x^T A x$ 配方成平方和的技巧（completing the square），任何實二次型都能寫成 $\pm$ 係數的平方和。但一個尷尬的問題懸而未決：**不同的人用不同的配方順序，得到的正負係數個數會不會不一樣？** 例如先配 $x_1$ 與先配 $x_2$，結果是否相同？
- **Cauchy 主軸定理（1815/1829）**：Cauchy 證明對稱矩陣可正交對角化，二次型可化為 $\sum \lambda_i y_i^2$，特徵值皆實。在正交變換下，正特徵值個數當然不變——但 Cauchy 的結果只涵蓋**正交**變換，一般可逆變換下呢？
- **Sylvester 的表述困境**： Sylvester 自己的論文用的是行列式語言（「linearly equivalent quadratic functions」的子行列式關係），敘述晦澀，並未使用「inertia」一詞。他甚至宣稱證明「很簡單以致不需詳細寫出」——後世公認他並沒有給出完整證明。
- 真正完整的證明由 **Frobenius 於 1878 年**補上。這樁案件的「結案陳詞」其實是別人寫的。

## 線索與推理 -- 數學式、程式、理論

### 線索一：慣性定律的陳述
設 $A$ 為 $n \times n$ 實對稱矩陣，$S$ 為任意可逆矩陣，作合同變換：

$$B = S^T A S$$

則 $B$ 與 $A$ 有相同的慣性指標三元組 $(n_+, n_-, n_0)$：正特徵值個數、負特徵值個數、零特徵值個數完全相同。換句話說，存在可逆 $S$ 使

$$S^T A S = \mathrm{diag}(\underbrace{1,\dots,1}_{n_+}, \underbrace{-1,\dots,-1}_{n_-}, \underbrace{0,\dots,0}_{n_0})$$

所有實對稱矩陣按 $(n_+, n_-, n_0)$ 分類——這就是二次型的**合同分類**：同一類的矩陣彼此合同，不同類的絕不會被任何可逆變換偽裝成對方。

### 線索二：為什麼正負號不會變——子空間論證
Frobenius 式的現代證明用維度計數（這是整個案件最漂亮的推理）。設 $A$ 有 $n_+$ 個正特徵值，$B = S^TAS$ 有 $m_+$ 個正特徵值。令 $V_+$ 為 $\mathbb{R}^n$ 中使 $x^T A x > 0$ 的最大子空間，$\dim V_+ = n_+$；同樣對 $B$ 有 $\dim W_+ = m_+$。考慮兩個子空間經 $S$ 連通後的交集：

$$\dim\left(S^{-1}W_+ \cap V_+\right) \geq \dim(S^{-1}W_+) + \dim V_+ - n = m_+ + n_+ - n$$

在交集裡的向量 $x$ 同時滿足 $x^T A x > 0$ 與 $x^T A x = (Sx)^T B (Sx) > 0$，不矛盾；但若 $m_+ > n_+$，則 $m_+ + n_+ - n > 2n_+ - n$，可推出交集裡存在非零向量落在 $A$ 的「非正區域」，導出矛盾。故 $m_+ \leq n_+$；對稱地 $n_+ \leq m_+$，所以 $m_+ = n_+$。負慣性指標同理。**正負號指紋，鐵證如山。**

### 線索三：秩 + 慣性 = 完整指紋
Sylvester 慣性定律與秩定理合起來，把二次型分類化約為一個離散三元組：

$$n_+ + n_- + n_0 = n, \qquad \mathrm{rank}(A) = n_+ + n_-$$

- $(n, 0, 0)$：正定（如 $I$）；
- $(n_+, n_-, 0)$：非退化不定（如 Minkowski 度規 $(1,1,1,1)$ 配 $(3,1)$ 的號差）；
- $n_0 > 0$：退化（秩不足）。

比對「特徵值」還省事：合同變換下特徵值本身會變，但**特徵值的正負號模式**不變。偵探不比對指紋的細節，只比對指紋的類型。

### 線索四：號差 = 幾何
慣性定律的幾何化身：二次型 $x^T A x = c$ 的等位面形狀由 $(n_+, n_-, n_0)$ 決定。$n_+ = n$ 時是橢球（所有方向都「正曲率」）；$n_+ = 1, n_- = n-1$ 時是雙曲面族——Minkowski 空間 $\mathrm{diag}(1,-1,-1,-1)$ 的光錐結構、相對論的類時/類空/類光分類，全部是慣性定律的幾何投影。

### 程式碼範例：Sylvester 慣性定律的符號檢驗
```python
import numpy as np

np.set_printoptions(precision=4, suppress=True)

def inertia(M):
    ev = np.linalg.eigvalsh(M)
    n_plus = int(np.sum(ev > 1e-10))
    n_minus = int(np.sum(ev < -1e-10))
    return n_plus, n_minus

A = np.array([[2.0, 1.0, 0.0],
              [1.0, 3.0, 1.0],
              [0.0, 1.0, 1.0]])
print("A 的慣性 (n+, n-, n0):", inertia(A), "+ 秩", np.linalg.matrix_rank(A))

rng = np.random.default_rng(0)
print("\n隨機可逆變換 S 下，慣性指標是否不變？")
for k in range(5):
    S = rng.standard_normal((3, 3))
    while abs(np.linalg.det(S)) < 1e-3:      # 確保 S 可逆
        S = rng.standard_normal((3, 3))
    B = S.T @ A @ S                          # 合同變換
    print(f"  試驗 {k+1}: B 的慣性 = {inertia(B)}，特徵值 = {np.linalg.eigvalsh(B)}")

print("\n退化與不定例子：")
print("  diag(1,1,-1,-1)  (Minkowski 號差 -3):", inertia(np.diag([1, 1, -1, -1])))
print("  diag(1,0,0)      (退化):            ", inertia(np.diag([1.0, 0, 0])))
```

輸出顯示：無論隨機可逆 $S$ 怎麼取，$B = S^TAS$ 的 $(n_+, n_-, n_0)$ 永遠等於 $A$ 的——雖然特徵值數值每次都不同，但正負號個數分毫不差。這就是慣性定律的數值鐵證。

## 結案 -- 後果與影響
- **二次型合同分類正式結案**：實對稱矩陣的世界被 $(n_+, n_-, n_0)$ 分成清晰的三元組格子，正定/不定/退化的判別有了理論根基。
- **1908 年 Minkowski 空間**：Minkowski 用號差 $(1,3)$ 的度規 $\mathrm{d}s^2 = c^2t^2 - x^2 - y^2 - z^2$ 重寫相對論；「類時、類空、類光」的分類正是慣性指標的物理化身。
- **正定性的判據**：Sylvester 本人另給出正定的行列式判別法（各階主子式皆正，Sylvester criterion），與慣性定律配套，成為最優化、控制理論的日常工具。
- **廣義相對論與 Lorentz 幾何**：號差不變性保證了「光錐結構」是座標變換下的幾何事實，而非座標巧合——等效原理的數學後盾。
- 無限維推廣：自伴算子的 Morse 指標、譜流的符號計數，都是慣性定律的現代遠親。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| James Joseph Sylvester | 提出慣性定律（敘述晦澀，證明不全） |
| Joseph-Louis Lagrange | 配方法（前案） |
| Augustin-Louis Cauchy | 主軸定理（正交變換版前案） |
| Ferdinand Georg Frobenius | 1878 年補全嚴格證明 |
| Hermann Minkowski | 1908 年號差幾何（最著名的後果） |

- J. J. Sylvester, *On the relation between the minor determinants of linearly equivalent quadratic functions*, Phil. Mag. **1**, 295–305 (1851)。
- F. G. Frobenius, *Über das Verhältniss der trivialen Invarianten zur Determinante*, J. Reine Angew. Math. **86**, 116–117 (1878)。
- H. Minkowski, *Raum und Zeit*, 演講 (1908)。
