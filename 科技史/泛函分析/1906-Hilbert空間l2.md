# 1906-Hilbert空間l2

## 案件檔案表

| 項目 | 內容 |
|------|------|
| 發生時間 | 1906 年（David Hilbert 關於積分方程的第四篇通信） |
| 發生地點 | 德國哥廷根 |
| 報案人 | Fredholm 理論（行列式硬算無窮維，太笨重） |
| 偵探 | David Hilbert |
| 兇器 | 無窮維空間缺乏「幾何」：沒有內積、沒有距離、沒有正交 |
| 結論 | $\ell^2$ 空間幾何化成功，內積與正交理論誕生，Hilbert 空間現形 |

## 案發現場

Fredholm 在 1900 年用行列式打下了積分方程的江山，但他的方法有一個致命弱點：**每次都要硬算一個無窮重積分的行列式**。 $D(\lambda)$ 的每一項都是 $n$ 重積分的行列式，寫起來長如蜈蚣，用起來重如鉛塊。

Hilbert 在哥廷根接手這樁案子。他的問題是：

1. 能不能把積分方程**離散化成無窮維的線性代數**，用序列而非函數思考？
2. 無窮維序列空間裡，什麼取代了長度、角度、正交？
3. Fredholm 的特徵值理論，在序列空間裡長什麼樣？

Hilbert 從 1904 年開始發表系列論文《關於積分方程一般理論的通信》。前幾篇處理特殊核，1906 年的第四篇通信達到巔峰：他研究了平方可和序列構成的空間——日後被世人稱為 **Hilbert 空間 $\ell^2$ ** 的對象。

## 偵查過程

### 線索一：定義案發地點—— $\ell^2$ 空間

考慮所有平方可和的（複）數列：

$$
\ell^2 = \left\{ x = (x_1, x_2, x_3, \dots) \;:\; \sum_{n=1}^\infty |x_n|^2 < \infty \right\} .
$$

定義範數與內積：

$$
\|x\| = \left( \sum_{n=1}^\infty |x_n|^2 \right)^{1/2}, \qquad
\langle x, y \rangle = \sum_{n=1}^\infty x_n \overline{y_n} .
$$

第一個需要偵查的問題： $\langle x, y \rangle$ 真的對所有 $x, y \in \ell^2$ 都收斂嗎？

### 線索二：Cauchy–Schwarz 不等式壓場

由 $|x_n \overline{y_n}| \le \frac{1}{2}(|x_n|^2 + |y_n|^2)$ ，級數絕對收斂。更精確的界是 **Cauchy–Schwarz 不等式**：

$$
|\langle x, y \rangle| \le \left( \sum_{n=1}^\infty |x_n|^2 \right)^{1/2} \left( \sum_{n=1}^\infty |y_n|^2 \right)^{1/2} = \|x\|\,\|y\| .
$$

證明可先用有限維（ $n$ 維）的 Cauchy–Schwarz，再讓 $n \to \infty$ 取極限——有限維的幾何，就這樣合法地移植到無窮維。

### 線索三： $\ell^2$ 的幾何骨架

有了內積，歐氏幾何的全部概念都可以搬進來：

| 歐氏幾何 $\mathbb{R}^n$ | $\ell^2$ 空間 |
|--------------------------|----------------|
| 向量 $x \in \mathbb{R}^n$ | 序列 $x \in \ell^2$ |
| 長度 $\sqrt{\sum x_i^2}$ | $\|x\| = (\sum \lvert x_n\rvert^2)^{1/2}$ |
| 內積 $\sum x_i y_i$ | $\langle x, y\rangle = \sum x_n \overline{y_n}$ |
| 垂直： $\langle x, y\rangle = 0$ | 正交： $\langle x, y\rangle = 0$ |
| 標準正交基 $e_1, \dots, e_n$ | $e_1, e_2, e_3, \dots$ （ $e_n$ 第 $n$ 項為 $1$ ） |
| 畢氏定理 | $\|x\|^2 = \sum \lvert \langle x, e_n \rangle\rvert^2$ |

Hilbert 證明了無窮維的**平行四邊形法則**與**投影定理**：給定閉子空間 $M$ 與向量 $x$ ，存在唯一的正交分解 $x = m + n$ （ $m \in M$ ， $n \perp M$ ）。這是 $\ell^2$ 幾何最深刻的一塊基石。

### 線索四：完備性——無窮維與有限維的差別現身

Hilbert 證明 $\ell^2$ 是**完備**的：若 $(x^{(k)})$ 是 Cauchy 序列，即

$$
\|x^{(k)} - x^{(m)}\| \to 0 \quad (k, m \to \infty) ,
$$

則存在 $x \in \ell^2$ 使 $\|x^{(k)} - x\| \to 0$ 。

證明分兩步：

1. 對每個座標 $n$ ， $|x_n^{(k)} - x_n^{(m)}| \le \|x^{(k)} - x^{(m)}\|$ ，故座標序列 $(x_n^{(k)})_k$ 收斂，極限記為 $x_n$ 。
2. 對 Cauchy 序列取 $k \ge K$ ： $\sum_{n=1}^N |x_n^{(k)} - x_n|^2 \le \varepsilon^2$ 對一切 $N$ 成立，令 $N \to \infty$ 得 $x^{(k)} - x \in \ell^2$ ，再由逐項極限得 $x \in \ell^2$ 且 $\|x^{(k)} - x\| \to 0$ 。

### 線索五：Parseval 等式——座標系的終極形式

設 $\{e_n\}$ 是 $\ell^2$ 的完備標準正交系（沒有非零向量與所有 $e_n$ 正交），則每個 $x \in \ell^2$ 都有展開

$$
x = \sum_{n=1}^\infty \langle x, e_n \rangle e_n , \qquad
\|x\|^2 = \sum_{n=1}^\infty |\langle x, e_n \rangle|^2 .
$$

第二式即 **Parseval 等式**——畢氏定理在無窮維的完整版本。級數收斂性不是假設，而是從完備標準正交系**免費附贈**的結論。

### 收網：積分方程的序列化

Hilbert 的殺手鐧：把積分方程 $\phi = f + \lambda T\phi$ 中的核 $K(x,t)$ 按標準正交系展開，方程就變成 $\ell^2$ 中無窮多個未知數的線性組

$$
(I - \lambda A)\, \boldsymbol{c} = \boldsymbol{b} ,
$$

其中 $A$ 是由 $\langle T e_j, e_i \rangle$ 排成的無窮矩陣。Fredholm 的特徵值理論在這裡化身為無窮矩陣的譜理論——行列式硬算被幾何語言取代。

## 結案報告

1. ** $\ell^2$ 幾何化成功**：內積、範數、正交、投影、畢氏定理全部在無窮維成立， $\ell^2$ 是完備的內積空間。
2. **Parseval 等式**：完備標準正交系下， $\|x\|^2 = \sum |\langle x, e_n \rangle|^2$ ，Fourier 展開的平方收斂問題就地解決。
3. **Cauchy–Schwarz 是通行證**：有限維不等式經極限程序合法移植到無窮維。
4. **遺產**：
   - von Neumann（1929/1932）把 $\ell^2$ 公理化為抽象 Hilbert 空間，用於量子力學。
   - Riesz–Fischer（1907）證明 $L^2$ 與 $\ell^2$ 同構，函數空間與序列空間合流。
   - 譜理論從無窮矩陣出發，最終成為量子力學的數學母體。

## 證據與工具

| 證據/工具 | 陳述 | 用途 |
|-----------|------|------|
| $\ell^2$ 空間 | $\sum \lvert x_n\rvert^2 < \infty$ | 案發地點 |
| 內積 | $\langle x, y\rangle = \sum x_n \overline{y_n}$ | 幾何化的核心 |
| Cauchy–Schwarz | $\lvert\langle x,y\rangle\rvert \le \|x\|\,\|y\|$ | 一切估計的通行證 |
| 完備性 | Cauchy 序列在 $\ell^2$ 內收斂 | 極限操作合法化 |
| Parseval 等式 | $\|x\|^2 = \sum \lvert\langle x,e_n\rangle\rvert^2$ | 無窮維畢氏定理 |

**證明骨架**（完備性）：

```
Cauchy 序列 (x^(k))
  → 座標收斂（每個 n 的分量是 Cauchy 數列）
  → 固定 k、令 N → ∞：x^(k) − x ∈ ℓ²
  → ‖x^(k) − x‖ → 0，極限落在 ℓ² 內
```

**一句話結案**：Hilbert 把平方可和序列推上王座，內積讓無窮維有了幾何——長度、角度、正交、投影應有盡有，泛函分析從此有了自己的祖國。
