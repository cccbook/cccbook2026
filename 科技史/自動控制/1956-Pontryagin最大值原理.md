# 1956 - Pontryagin 最大值原理

## 案件摘要

1956 年，蘇聯數學家 Lev Pontryagin（龐特里亞金）與學生 Boltyansky、Gamkrelidze、Mishchenko
提出**最大值原理**（maximum principle，俄文的原意是「最大值原理」）：
最佳控制問題的**必要條件**——若控制 $u(t)$ 是最佳的，則存在「伴隨變數」$\lambda(t)$
（協態），使得 Hamiltonian

$$
\mathcal{H}(x, \lambda, u, t) = \lambda^\mathsf T f(x, u, t) + L(x, u, t)
$$

沿最佳軌跡對 $u$ 取**最大值**：

$$
u^*(t) = \arg\max_u \mathcal{H}(x^*, \lambda, u, t)
$$

這是變分法（Euler–Lagrange）對**控制約束問題**的推廣——
控制有飽和、有邊界（引擎推力有限、舵角有限），古典變分法失效，
最大值原理接手。**最佳控制理論誕生**。

## 前因

- **二戰與冷戰的國家需求**：飛彈攔截、火箭軌道、經濟規劃——「最佳化」是蘇聯與美國的共同國家需求。
- **古典變分法的限制**：Euler–Lagrange 方程（見哈密頓物理學 [1755-Lagrange變分法.md](../哈密頓物理學/1755-Lagrange變分法.md)）要求控制**無約束**；但真實控制處處有飽和（推力上限、舵角上限、電壓上限）。
- **最速降線的啟示**：Bernoulli 的 brachistochrone 問題（1696）——「時間最短」的最佳化問題，變分法的起源；但它的控制無約束。
- **蘇聯數學學派**：Pontryagin 是拓撲學家（盲人數學家），他的學校習慣「從具體問題反推一般理論」。

## 線索與推理

### 第 1 步：問題的精確形式

最佳控制問題：

$$
\min_{u(\cdot)} \; J = \int_0^{T} L(x, u, t)\, dt, \qquad \dot x = f(x, u, t), \qquad u \in U
$$

其中 $U$ 是**控制約束集**（如 $|u| \le 1$，推力飽和）。

古典變分法的 Euler–Lagrange 要求 $\dfrac{\partial \mathcal{H}}{\partial u} = 0$（內點駐定）——
但若最佳控制在**邊界**上（$u = \pm 1$，全推力），這個條件無解！

### 第 2 步：最大值原理的推導

Pontryagin 的偵探手法：引進**伴隨變數**（協態）$\lambda(t)$，構造 Hamiltonian：

$$
\mathcal{H}(x, \lambda, u, t) = \lambda^\mathsf T f(x, u, t) + L(x, u, t)
$$

**最大值原理**：沿最佳軌跡，

$$
u^*(t) = \arg\max_{u \in U} \mathcal{H}(x^*(t), \lambda(t), u, t)
$$

且協態滿足「伴隨方程」：

$$
\dot\lambda = -\frac{\partial \mathcal{H}}{\partial x}
$$

（注意形式與 Hamilton 正則方程 $\dot p = -\partial H/\partial q$ **完全同構**——
協態 $\lambda$ 就是控制版的「廣義動量」，見哈密頓物理學 [02.2-正則方程.md](../哈密頓物理學/02.2-正則方程.md)。）

### 第 3 步：為什麼是「最大值」而非「駐定」？

**駐定**（$\partial \mathcal{H}/\partial u = 0$）只在內點成立；
**最大值**在邊界也成立：若最佳控制是全推力 $u = 1$，那 $\mathcal{H}$ 在 $u = 1$ 取最大——
即使導數不為零。**「駐定」是內點特例，「最大值」涵蓋邊界**——
這就是最大值原理對變分法的推廣本質。

### 第 4 步：範例——最短時間控制（bang-bang）

推動一輛車（質量 1）在最短時間內從 $x = 0$ 到 $x = 1$ 且停下，推力 $|u| \le 1$：

$$
\ddot x = u, \qquad |u| \le 1
$$

Hamiltonian：$\mathcal{H} = \lambda_1 v + \lambda_2 u + 1$（終端時間自由，$L = 1$）。

最大值原理：$u^* = \arg\max_{|u| \le 1} \lambda_2 u = \text{sign}(\lambda_2)$。

**結論**：最佳控制是**全推力或全煞車**——bang-bang 控制！

$$
u^*(t) = \begin{cases} +1 & 0 \le t < T/2 \\ -1 & T/2 \le t \le T \end{cases}
$$

先用全推力加速、再全煞車——**最短時間 = 全開或全關，沒有中間值**。
這解釋了為何最佳控制常是「不連續的」——引擎要嘛全踩要嘛全鬆。

**最短時間** $T = 2\sqrt{1}$（對 $x_{final} = 1$：$T = 2$ 秒）：
前半程加速 $x = t^2/2$、後半程對稱減速，$T/2$ 時到達 $x = 1/4 \cdot$ …
（精確計算：$x(T/2) = 1/2$，$T = 2\sqrt{1} = 2$，驗證：$\frac{1}{2}(\frac{T}{2})^2 = \frac{1}{2} \Rightarrow \frac{T}{2} = 1 \Rightarrow T = 2$。）

## 後果

- 最佳控制理論誕生：「Hamiltonian 最大化 + 協態方程」成為最佳控制的必要條件。
- Bellman 動態規劃（1957）獨立誕生：另一條最佳化路線（見 [1957-Bellman動態規劃.md](1957-Bellman動態規劃.md)）——兩者互補（最大值原理 = 局部必要條件，動態規劃 = 全域充分條件）。
- 火箭軌道設計、飛彈攔截、月球登陸（Apollo 的軌道最佳化）的數學工具。
- bang-bang 控制成為最佳控制的招牌範例：化工批次製程、機器人快速運動。
- 與哈密頓力學的深層連結：協態變數 = 廣義動量，最佳控制 = 相空間的變分法。

## 結案陳詞

Pontryagin 的偵探手法是「把變分法推過約束的邊界」：駐定條件失效的地方，
最大值條件接手。**協態變數與哈密頓力學的同構**——廣義動量回來了，
最佳控制是哈密頓變分法的工程版。
