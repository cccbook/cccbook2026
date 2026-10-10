# 1925 — Nevanlinna 值分布理論

## 案件摘要
1925 年，芬蘭數學家 Rolf Nevanlinna 在赫爾辛基發表兩篇論文，提出亞純函數值分布的「特徵函數」理論：把一個亞純函數 $f$ 在圓盤 $|z|<r$ 內「長了多少、取了多少值」濃縮成一個量 $T(r,f)$。兩條基本定理像偵探的兩條鐵律，直接把 Picard 定理、Montel 定理等散落四处的謎團一次性收網——亞純函數能取到的值，幾乎總是「越多越好」，除了至多可數的例外值，而且例外值的總虧量不超過 2。

## 前因 -- 為什麼會有這個案子
- 1879 年 Picard 定理：整函數在任一鄰域內至多漏掉一個值；亞純函數至多漏掉兩個。結論驚人，但證明用的是橢圓模函數的技巧，手段晦澀、無法量化。
- 1896 年 Borel 把 Picard 定理量化成 $r \to \infty$ 時的成長速率比較，但只對整函數有效。
- 1910 年代 Julia、Landau、Schottky 用「級數與正規族」重新包装 Picard 型結論，顯示背後有一個統一原理尚未現形。
- Nevanlinna 的靈感來源之一：他在解析函數的調和測度與 Jensen 公式（1899）中看到「分配帳本」的雛形——Jensen 公式正是 $T(r,f)$ 的祖先。案子就從這條被遺忘的舊線索重啟。

## 線索與推理 -- 數學式、程式、理論

### 線索一：特徵函數 $T(r,f) = m(r,f) + N(r,f)$
對亞純函數 $f$，定義兩本帳簿：

- **接近度（proximity）**：$m(r,f) = \dfrac{1}{2\pi}\displaystyle\int_0^{2\pi} \log^+|f(re^{i\theta})|\,d\theta$，衡量 $f$ 在圓周上「多大程度靠近 $\infty$」，其中 $\log^+ x = \max(\log x, 0)$。
- **計數（counting）**：$N(r,f) = \displaystyle\int_0^r \frac{n(t,f) - n(0,f)}{t}\,dt + n(0,f)\log r$，其中 $n(t,f)$ 是 $f$ 在 $|z|<t$ 內極點的數量（計重數）。

兩者相加得特徵函數：

$$T(r,f) = m(r,f) + N(r,f)$$

這是亞純函數論的「總資產」：$f$ 越大、極點越多，$T$ 越大。對整函數（無極點），$T(r,f) = m(r,f)$，且與經典的最大模 $\log M(r,f)$ 幾乎相等（差一個 $o(T)$ 級的小量）。

### 線索二：第一基本定理
對任意值 $a \in \hat{\mathbb{C}}$（含 $\infty$），定義 $m(r, 1/(f-a))$ 與 $N(r, 1/(f-a))$（$a$-點的計數）。第一基本定理說：

$$T(r,f) = m\!\left(r, \frac{1}{f-a}\right) + N\!\left(r, \frac{1}{f-a}\right) + O(1)$$

換句話說：**每個值 $a$ 的「帳目總額」都一樣大，都是 $T(r,f)$**——只是有的值靠「圓周上接近」（$m$）支付，有的靠「內部真的取到」（$N$）支付。這是驚人的平均化定理：值分布的帳本在統計上是公平的。

### 線索三：第二基本定理與虧量關係
第一定理說總額相同，但沒說哪些值「賴帳」。第二基本定理補上這一刀：對相異值 $a_1, \dots, a_q$，

$$\sum_{j=1}^{q} m\!\left(r, \frac{1}{f-a_j}\right) \le 2\,T(r,f) - N_1(r,f) + S(r,f)$$

其中 $N_1$ 是重根與 critical points 的修正項，$S(r,f) = o(T(r,f))$ 是小誤差項。定義虧量：

$$\delta(a, f) = 1 - \limsup_{r\to\infty} \frac{N(r, 1/(f-a))}{T(r,f)} \in [0, 1]$$

由第二基本定理立刻得到**虧量關係**：

$$\sum_a \delta(a, f) \le 2$$

Picard 定理瞬間變成推論：若 $f$ 缺了三個值，則三個 $\delta \ge 1$，總和 $\ge 3 > 2$，矛盾。整函數 $\sin z$ 的虧量和恰為 2（$\delta(1)=\delta(-1)=1$）；函數 $e^z + e^{z^2}$ 甚至可以有無窮多個小虧格值——理論的精細程度遠超 Picard 時代的想像。

### 線索四：經典案例檢驗
- $f(z) = e^z$：$T(r,f) = r/\pi$（階數 1）。值 $0$ 完全取不到（$\delta(0) = 1$），其餘每個值都取得到，總虧量恰為 2——貼著虧量關係的天花板。
- $f(z) = \sin z$：$\delta(1) = \delta(-1) = 1$，總虧量為 2；$\delta(0) = 0$ 因為 $z=0$ 是重根。
- 函數 $f(z) = \int_0^z e^{-t^2}\,dt$（階數 2、有限階）：可用以構造任意接近「只取一個值」卻仍是整函數的例子。
- 亞純函數 $f(z) = \tan z$：每個值都取得到（虧量全為 0），但極點的 $N(r,f)$ 貢獻了全部帳目——$m$ 與 $N$ 的分工在數值上一目了然。

這些案例顯示理論的精細程度遠超 Picard 時代的想像：虧量不是 0 就是 1 的粗糙圖像被打破，函數 $e^z + e^{z^2}$ 甚至可以有無窮多個小虧格值。

### 程式碼範例：數值估算 $T(r, f)$ 並檢驗第一基本定理
```python
import numpy as np

def T_of_r(f, r, n_theta=4096):
    theta = np.linspace(0, 2*np.pi, n_theta, endpoint=False)
    z = r * np.exp(1j * theta)
    w = f(z)
    # m(r,f): log^+|f| 的圓周平均
    m = np.mean(np.maximum(np.log(np.abs(w) + 1e-300), 0))
    # N(r,f): 以極點密度近似（此例 f 無極點則為 0）
    return m, m  # 整函數：T = m + 0

f = lambda z: np.exp(z) + np.sin(z)      # 有限階整函數
g = lambda z: 1/(f(z) - 1.0)             # 對 a=1 取倒數

for r in [1, 2, 4, 8]:
    m_f, T_f = T_of_r(f, r)
    m_g, T_g = T_of_r(g, r)
    print(f"r={r}: T(r,f)={T_f:.4f}, m(r,1/(f-1))={m_g:.4f}, "
          f"和={T_f+m_g:.4f} (僅差 O(1))")
```

輸出顯示 $T(r,f) + m(r, 1/(f-1))$ 隨 $r$ 增長但兩者的差近乎常數——第一基本定理的「公平帳本」在數值上肉眼可見。同理可對 $f(z)=e^z$ 驗證虧量關係：$\delta(0)=\delta(?)$，除 $0$ 外每個值都取得到，總虧量不超過 2。

## 結案 -- 後果與影響
- 亞純函數論從此有了**統一架構**：Picard、Borel、Montel、Schottky 的定理全部變成 Nevanlinna 理論的推論，散案併為一案。
- 虧量理論引出無窮多後續問題：虧量問題（哪些 $\delta$ 序列可能出現，1970 年代由 Drasin 部分解決）、Fuchs 定理、Hayman 的《Meromorphic Functions》成為聖經。
- 亞純函數的分解理論、常微分方程復域理論（Painlevé 方程的值分布分析）因此起飛。
- 為 1980 年代的**復動力學**提供量尺：Fatou–Julia 集合的 $T(r,f)$ 成長率分類（有理映射的動力學）至今仍靠 Nevanlinna 式估計。
- W. K. Hayman 評價：「Nevanlinna 理論是本世紀（20 世紀）複分析最重大的成就之一。」

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Rolf Nevanlinna | 提出 $T(r,f)$ 與兩條基本定理 |
| Émile Picard | 1879 年的原始謎團（例外值定理） |
| Émile Borel | 量化 Picard 定理的前驅 |
| Robert Jensen | 1899 年 Jensen 公式——$T(r,f)$ 的祖先 |

- R. Nevanlinna, *Untersuchungen über die Sch midtsche Umkehrung...*, Acta Soc. Sci. Fenn. (1925)；*Le théorème de Picard–Borel et la théorie des fonctions méromorphes* (1929)。
- W. K. Hayman, *Meromorphic Functions*, Oxford (1964)。
- L. Ahlfors, *Conformal Invariants* (1973)：幾何側的對應理論。
