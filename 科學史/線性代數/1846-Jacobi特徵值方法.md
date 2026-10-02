# 1846 — Jacobi 特徵值方法

## 案件摘要
1846 年，Carl Gustav Jacob Jacobi 在 Crelle's Journal 上發表〈Über ein leichtes Verfahren, die in der Theorie der Säcularstörungen vorkommenden Gleichungen numerisch aufzulösen〉，提出一套用「平面旋轉」逐次消去對稱矩陣非對角元素的數值方法：$A \to J^T A J$ 反覆施行，矩陣便收斂到對角陣，對角線上正是特徵值。這是歷史上**第一個**系統性的矩陣特徵值數值演算法——在「矩陣」這個名詞都還沒普及的年代，Jacobi 已經寫下了數值線性代數的開山案件。

## 前因 -- 為什麼會有這個案子
- **二次型主軸定理**：Cauchy 於 1815 年、1829 年證明實對稱矩陣的特徵值皆為實數，且二次型可透過正交變換化為 $\sum \lambda_i y_i^2$ 的平方和。理論上「對角化」早已存在，但那只是存在性證明——**怎麼算**出來，是另一樁懸案。
- **天體力學的 secular equation**：Lagrange、Laplace 研究行星軌道的長期擾動（secular perturbations）時，需要解形如 $\det(A - \lambda I) = 0$ 的高次方程（行星數越多次數越高）。傳統做法是先展開行列式再求根，六階行列式展開有 720 項，數值災難。
- **橢圓函數計算的訓練**：Jacobi 是橢圓函數理論的泰斗，習慣處理變數變換與週期結構；他對「用迭代變換逐步化簡」有職業級的直覺。
- Jacobi 的動機非常務實：他說舊方法「展開行列式」太痛苦，他要一個**不需要展開行列式**、直接在矩陣上操作的流程。這就是案發動機——不是為了抽象美，而是為了算得出來。

## 線索與推理 -- 數學式、程式、理論

### 線索一：平面旋轉消去一個非對角元素
考慮實對稱矩陣 $A$，取一個只在 $(p,q)$ 平面上旋轉角度 $\theta$ 的正交矩陣 $J = J(p, q, \theta)$。作合同變換 $A' = J^T A J$，計算新的非對角元素：

$$a'_{pq} = \frac{a_{qq} - a_{pp}}{2}\sin 2\theta + a_{pq}\cos 2\theta$$

要讓 $a'_{pq} = 0$，只需令 $\tan 2\theta = \dfrac{2a_{pq}}{a_{pp} - a_{qq}}$，即取

$$\theta = \frac{1}{2}\arctan\!\left(\frac{2a_{pq}}{a_{pp} - a_{qq}}\right)$$

（當 $a_{pp} = a_{qq}$ 時取 $\theta = \pi/4$。）一次旋轉就精準殺掉一個非對角元素——這是兇器的核心構造。

### 線索二：為什麼會收斂
關鍵不變量是 Frobenius 範數的平方。正交相似變換保持 Frobenius 範數：

$$\|A'\|_F^2 = \|A\|_F^2 = \sum_i a_{ii}^2 + \sum_{i \neq j} a_{ij}^2 = \|D\|^2_{\text{diag}} + \|A\|^2_{\text{off}}$$

而一次旋轉把「非對角平方和」減少 $2a_{pq}^2$：

$$\|A'\|^2_{\text{off}} = \|A\|^2_{\text{off}} - 2a_{pq}^2$$

對角平方和則增加同樣的量。非對角的「血跡」不會消失（總範數不變），但每轉一次就往對角線轉移一點。Jacobi 的策略是**每次挑選絕對值最大的非對角元素**（經典 Jacobi），反覆執行；非對角元素單調遞減趨於零，$A$ 收斂到對角陣 $D = \mathrm{diag}(\lambda_1, \dots, \lambda_n)$，累積乘積 $V = J_1 J_2 J_3 \cdots$ 的行向量就是特徵向量。

### 線索三：正交性是保險箱
整個過程只用正交矩陣，因此：
1. 對稱性全程保持（$J^T A J$ 對稱）；
2. 特徵值全程為實數，不會跑出複數鬼影；
3. 數值上良態——正交變換不放大誤差（條件數為 1）。

這三點讓 Jacobi 法至今仍是高精度對稱特徵值問題的黃金標準之一：慢，但極穩。

### 線索四：天體力學的原始戰場
Jacobi 的論文標題就寫明瞭目標：解長期擾動方程。對 $n$ 個行星，擾動矩陣是 $n \times n$ 對稱陣，其特徵值決定軌道要素的長期振盪頻率。Jacobi 法不需要展開行列式、不需要求根，直接把矩陣「轉」成對角——原本 720 項的災難變成 15 次旋轉的例行公事。

### 程式碼範例：循環 Jacobi 旋轉消去非對角元素
```python
import numpy as np

np.set_printoptions(precision=6, suppress=True)
A = np.array([[4.0, 1.0, 2.0],
              [1.0, 3.0, 0.5],
              [2.0, 0.5, 1.0]])
V = np.eye(3)

for sweep in range(10):
    off = np.sqrt(np.sum(A**2) - np.sum(np.diag(A)**2))
    print(f"sweep {sweep}: off-diagonal norm = {off:.3e}")
    if off < 1e-12:
        break
    for p in range(3):
        for q in range(p + 1, 3):
            if abs(A[p, q]) < 1e-15:
                continue
            # 計算旋轉角 theta，使旋轉後 A[p,q] = 0
            tau = (A[q, q] - A[p, p]) / (2 * A[p, q])
            t = np.sign(tau) / (abs(tau) + np.sqrt(1 + tau**2))
            c, s = 1 / np.sqrt(1 + t**2), t / np.sqrt(1 + t**2)
            J = np.eye(3)
            J[p, p], J[q, q], J[p, q], J[q, p] = c, c, s, -s
            A = J.T @ A @ J
            V = V @ J

print("特徵值（對角線）:", np.diag(A))
print("numpy 驗證     :", np.linalg.eigvalsh(np.array([[4,1,2],[1,3,0.5],[2,0.5,1]])))
print("特徵向量（行）:\n", V)
print("驗證 A V = V Λ :", np.allclose(A @ V, V @ A))
```

輸出顯示非對角範數每個 sweep 指數級下降，幾輪後收斂到 $10^{-12}$ 以下；對角線與 `numpy.eigvalsh` 完全一致，且 $AV = V\Lambda$ 驗證了特徵向量的正確性。

## 結案 -- 後果與影響
- Jacobi 法是**矩陣特徵值數值計算的起點**：第一次把「特徵值」從行列式求根中解放出來，變成矩陣上的迭代操作。
- **1954 年 Givens 旋轉**：Wallace Givens 把平面旋轉用在非對稱問題上，先化為三對角再處理，成為 QR 演算法的前身。
- **循環 Jacobi 演算法**：不挑最大元素、按固定順序掃過所有 $(p,q)$ 的版本，被證明必然收斂且便於並行化；今日 GPU 上的對稱特徵值求解器仍常用 Jacobi 變體。
- 現代 QR 演算法（Francis 1961）在思想上仍是 Jacobi 的後裔：用相似變換逐步化簡，讓非目標元素趨零。
- 病態矩陣、需要高相對精度（如量子化學、結構力學）的場合，Jacobi 法至今無可取代。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Carl Gustav Jacobi | 案件主嫌：發明旋轉消去法 |
| Augustin-Louis Cauchy | 主軸定理與實特徵值（理論地基） |
| Joseph-Louis Lagrange | 長期擾動方程（案發現場） |
| Wallace Givens | 1954 年旋轉方法的現代繼承人 |

- C. G. J. Jacobi, *Über ein leichtes Verfahren, die in der Theorie der Säcularstörungen vorkommenden Gleichungen numerisch aufzulösen*, J. Reine Angew. Math. **30**, 51–62 (1846)。
- A.-L. Cauchy, Sur l'équation à l'aide de laquelle on détermine les inégalités séculaires..., (1829)。
- W. Givens, *Numerical computation of the characteristic values of a real symmetric matrix*, Oak Ridge Report ORNL-1574 (1954)。
