# 1900-Fredholm二擇一

## 案件檔案表

| 項目 | 內容 |
|------|------|
| 發生時間 | 1900 年（Erik Ivar Fredholm 發表里程碑論文） |
| 發生地點 | 瑞典斯德哥爾摩 |
| 報案人 | 積分方程理論（Volterra 型之外，一般積分方程無人能解） |
| 偵探 | Erik Ivar Fredholm |
| 兇器 | 積分上限固定的方程：影響不縮小，特徵值橫行 |
| 結論 | Fredholm 行列式理論建立，二擇一原理成立， $n$ 維線性代數的無窮維類比 |

## 案發現場

Volterra 在 1887 年馴服了「積分上限會動」的方程，但最自然的積分方程——熱傳導、位勢理論中出現的**積分上限固定**的方程——依然橫行無忌：

$$
\phi(x) = f(x) + \lambda \int_a^b K(x,t)\,\phi(t)\,dt .
$$

**謎題升級：**

1. 積分區間固定後，疊核的階乘壓制失效了—— $T$ 的迭代貢獻**不再自動縮小**。
2. 這種方程存在**特徵值**：對某些特殊的 $\lambda$ ，齊次方程 $\phi = \lambda T\phi$ 有非零解，此時非齊次方程可能無解。
3. 什麼時候有解、什麼時候沒解？有解時如何顯式寫出？

Fredholm 是斯德哥爾摩的數學家，他從 1890 年代末開始攻打這座城堡。他的靈感來自一個大膽的類比：把積分方程看成**無窮多個未知數的線性代數方程組**，然後照搬 $n$ 維線性代數的整套武器——行列式、伴隨矩陣、秩與維數的關係。

## 偵查過程

### 線索一：把積分切成 $n$ 段，線性代數現形

把 $[a,b]$ 切成 $n$ 等分，記 $x_i = a + i h$ （ $h = (b-a)/n$ ）。積分方程離散化為線性組：

$$
\phi(x_i) = f(x_i) + \lambda h \sum_{j=1}^n K(x_i, x_j)\,\phi(x_j) + \cdots ,
$$

這是 $n$ 個未知數 $\phi(x_1), \dots, \phi(x_n)$ 的線性方程組，矩陣形式為

$$
(I - \lambda h K_n)\,\boldsymbol{\phi} = \boldsymbol{f} ,
$$

其中 $(K_n)_{ij} = K(x_i, x_j)$ 。由 Cramer 法則：

$$
\boldsymbol{\phi} = \frac{\det(I - \lambda h K_n + \lambda h F_n)}{\det(I - \lambda h K_n)} ,
$$

其中 $F_n$ 是把矩陣第 $i$ 列換成 $f(x_i)$ 後的行列式。

### 線索二：讓 $n \to \infty$ ，Fredholm 行列式誕生

Fredholm 的神來之筆：當 $n \to \infty$ 時， $\det(I - \lambda h K_n)$ 的極限**不是**發散，而是收斂到一個整函數——**Fredholm 行列式**：

$$
D(\lambda) = 1 + \sum_{n=1}^\infty \frac{(-\lambda)^n}{n!} \int_a^b \cdots \int_a^b \det\big( K(x_i, x_j) \big)_{i,j=1}^n \, dx_1 \cdots dx_n .
$$

展開前幾項：

| $n$ | $D(\lambda)$ 中的項 |
|-----|---------------------|
| $0$ | $1$ |
| $1$ | $-\lambda \int_a^b K(x,x)\,dx$ |
| $2$ | $\dfrac{\lambda^2}{2} \displaystyle\int_a^b\!\!\int_a^b \det\begin{pmatrix} K(x_1,x_1) & K(x_1,x_2) \\ K(x_2,x_1) & K(x_2,x_2) \end{pmatrix} dx_1\,dx_2$ |
| $\vdots$ | $\dfrac{(-\lambda)^n}{n!} \displaystyle\int\cdots\int \det(K(x_i,x_j))\, d^n x$ |

因為 $|\det(K(x_i,x_j))| \le n!\, M^n$ （Hadamard 不等式的粗糙版本），級數被 $\sum |\lambda|^n M^n$ 壓制，故 $D(\lambda)$ 在整個複數平面上是**整函數**，其零點離散、至多可數。

### 線索三：Fredholm 第一子式與解的顯式

與 $D(\lambda)$ 配套的是**第一子式**（first minor）：

$$
D(x,t;\lambda) = \lambda\, K(x,t) + \sum_{n=1}^\infty \frac{(-\lambda)^{n+1}}{n!} \int\cdots\int \det\begin{pmatrix} K(x,t) & K(x,x_1) & \cdots \\ K(x_1,t) & K(x_1,x_1) & \cdots \\ \vdots & \vdots & \ddots \end{pmatrix} d^n x ,
$$

滿足恆等式

$$
D(x,t;\lambda) = \lambda K(x,t) D(\lambda) + \lambda \int_a^b K(x,s)\, D(s,t;\lambda)\, ds .
$$

當 $D(\lambda) \ne 0$ 時，非齊次方程的解是

$$
\phi(x) = f(x) + \frac{1}{D(\lambda)} \int_a^b D(x,t;\lambda)\, f(t)\, dt .
$$

### 線索四：二擇一（alternative）登場

當 $D(\lambda) = 0$ 時，Cramer 法則失效——但線性代數告訴我們該問什麼問題。Fredholm 證明了完整的**二擇一原理**：

| 情況 | 齊次方程 $\phi = \lambda T\phi$ | 非齊次方程 $\phi = f + \lambda T\phi$ |
|------|--------------------------------|----------------------------------------|
| $D(\lambda) \ne 0$ | 僅零解 | 對**任意** $f$ 有唯一解 |
| $D(\lambda) = 0$ | 有非零解（特徵函數，有限維解空間） | 有解 $\iff$ $f$ 與伴隨齊次方程的特徵函數正交 |

在 $D(\lambda) = 0$ 的情況，解存在的充要條件是：

$$
\int_a^b f(t)\,\psi(t)\,dt = 0 \quad \text{對所有滿足 } \psi = \lambda T^* \psi \text{ 的 } \psi \text{ 成立} ,
$$

其中 $T^*$ 是伴隨算子（核為 $K(t,x)$ 的轉置）。這正是 $n$ 維線性代數中「方程組可解 $\iff$ 右端向量與係數矩陣左零空間正交」的無窮維版本。

### 對照表：線性代數 vs 積分方程

| $n$ 維線性代數 | Fredholm 積分方程 |
|----------------|-------------------|
| $n \times n$ 矩陣 | 核 $K(x,t)$ |
| 行列式 $\det(I - \lambda A)$ | $D(\lambda)$ （整函數） |
| Cramer 法則 | $\phi = f + \dfrac{1}{D} \int D(x,t;\lambda) f\,dt$ |
| 伴隨矩陣 $A^T$ | 伴隨核 $K(t,x)$ |
| 可解判據（正交條件） | 二擇一的相容性條件 |

## 結案報告

1. **Fredholm 行列式**： $D(\lambda)$ 是整函數，其零點是積分方程的特徵值，至多可數、無有限累積點。
2. **二擇一原理**：齊次方程僅有零解 $\iff$ 非齊次方程對任意 $f$ 有解；特徵值出現時，可解性由正交條件判定。
3. ** $n$ 維線性代數的無窮維類比成功**：行列式、伴隨、正交判據全部照搬成功——這證明了「無窮維可以像有限維一樣推理」。
4. **遺產**：Hilbert 讀到 Fredholm 的工作後，於 1904–1906 年間以譜理論與 $\ell^2$ 空間重新鑄造整個理論，Hilbert 空間由此誕生；Fredholm 二擇一日後抽象化為 Riesz 緊算子理論（1916），成為緊算子譜論的基石。

## 證據與工具

| 證據/工具 | 陳述 | 用途 |
|-----------|------|------|
| Fredholm 方程 | $\phi(x) = f(x) + \lambda\int_a^b K(x,t)\phi(t)\,dt$ | 案發現場的嫌犯 |
| Fredholm 行列式 | $D(\lambda) = 1 + \sum_n \dfrac{(-\lambda)^n}{n!}\int\cdots\int \det(K(x_i,x_j))\,d^nx$ | 特徵值的偵測器 |
| 第一子式恆等式 | $D(x,t;\lambda) = \lambda K(x,t) D(\lambda) + \lambda\int K(x,s) D(s,t;\lambda)\,ds$ | 顯式解的來源 |
| 二擇一原理 | $D(\lambda) \ne 0$ ：唯一解； $D(\lambda) = 0$ ：正交條件判定 | 相容性的判官 |
| 伴隨核 | $K^*(x,t) = K(t,x)$ | 正交條件中的伴隨方程 |

**證明骨架**：

```
離散化（n 段） → Cramer 法則 → 讓 n → ∞
  → Fredholm 行列式 D(λ) 與第一子式 D(x,t;λ)
  → 恆等式驗證（D(λ) ≠ 0：顯式解）
  → D(λ) = 0：伴隨齊次方程 + 正交條件（二擇一）
```

**一句話結案**：Fredholm 把積分方程當成無窮維的線性方程組，行列式與正交判據全部照搬成功—— $n$ 維線性代數在無窮維留下了第一個完美的迴聲，也為 Hilbert 空間的誕生鋪好了路。
