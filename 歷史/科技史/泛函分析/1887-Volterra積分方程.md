# 1887-Volterra積分方程

## 案件檔案表

| 項目 | 內容 |
|------|------|
| 發生時間 | 1887 年（Vito Volterra 發表系列論文） |
| 發生地點 | 義大利比薩、杜林 |
| 報案人 | 積分方程理論本身（無人能證解存在且唯一） |
| 偵探 | Vito Volterra |
| 兇器 | 無窮維線性系統的「不可解」表象 |
| 結論 | 第二類 Volterra 積分方程的解存在且唯一，Neumann 級數給出顯式解 |

## 案發現場

十九世紀末，數學物理遍地開花：熱傳導、彈性力學、天體力學都把問題化成了「未知函數出現在積分號下」的方程。這類方程的典型形式是

$$
\phi(x) = f(x) + \lambda \int_a^x K(x,t)\,\phi(t)\,dt ,
$$

其中 $K(x,t)$ 是已知的核（kernel）， $f(x)$ 是已知函數， $\lambda$ 是參數， $\phi(x)$ 是未知函數。

**謎題有三層：**

1. 這種方程**有解嗎**？（存在性）
2. 解**只有一個嗎**？（唯一性）
3. 若有解，能不能**真的把它寫出來**？（構造性）

當時的數學家手上只有古典分析的工具：極限、級數、積分。對付一個「未知函數套在積分號下」的怪物，顯得力不從心。更麻煩的是，方程兩邊的 $\phi$ 出現在不同位置——右邊的 $\phi(t)$ 被 $K(x,t)$ 「揉捏」過，想直接解開幾乎不可能。

Volterra 在比薩大學任教時接下這宗懸案。他注意到一件別人忽略的事：這個方程的積分上限是 $x$ 本身，不是固定區間 $[a,b]$ 。這個「積分上限會動」的特徵，正是破案的關鍵線索。

## 偵查過程

### 線索一：上限會動，核就「溫柔」

Volterra 的第一個觀察：若積分上限是固定的 $b$ （即 Fredholm 型方程），則積分算子在整個區間 $[a,b]$ 上對 $\phi$ 施加影響，迭代後的貢獻**不會縮小**。但 Volterra 方程的上限是 $x$ ，每一次迭代，新的積分區間都會縮短。

具體來說，令積分算子

$$
(T\phi)(x) = \int_a^x K(x,t)\,\phi(t)\,dt ,
$$

則方程就是 $\phi = f + \lambda T\phi$ 。迭代 $T$ 一次：

$$
(T^2\phi)(x) = \int_a^x K(x,s)\,(T\phi)(s)\,ds = \int_a^x \left( \int_s^x K(x,s)K(s,t)\,dt \right) \phi(s)\,ds .
$$

注意內層積分區間是 $[s,x]$ ，比 $[a,x]$ 短。定義 $K_2(x,s) = \int_s^x K(x,s)K(s,t)\,dt$ ，一般地有疊核（iterated kernel）

$$
K_n(x,t) = \int_t^x K_{n-1}(x,s)\,K(s,t)\,ds .
$$

### 線索二：疊核被積分區間壓垮

設 $|K(x,t)| \le M$ 在三角形區域 $\{a \le t \le x \le b\}$ 上成立。則用歸納法可證：

$$
|K_n(x,t)| \le \frac{M^n (x-t)^{n-1}}{(n-1)!} .
$$

**驗證**： $n=1$ 時 $|K_1| \le M$ 成立。若 $n$ 時成立，則

$$
|K_{n+1}(x,t)| \le \int_t^x \frac{M^n (x-s)^{n-1}}{(n-1)!} \cdot M \, ds = \frac{M^{n+1}}{(n-1)!} \cdot \frac{(x-t)^n}{n} = \frac{M^{n+1}(x-t)^n}{n!} .
$$

關鍵來了：疊核的估計裡藏著 $(x-t)^{n-1}/(n-1)!$ ——這是**階乘壓制**。不管 $\lambda$ 多大，級數

$$
\sum_{n=1}^\infty |\lambda|^n \frac{M^n (b-a)^{n-1}}{(n-1)!} = |\lambda| M \, e^{|\lambda| M (b-a)} < \infty
$$

**永遠收斂**。這與 Fredholm 方程「 $|\lambda|$ 必須小於收斂半徑」的處境截然不同：Volterra 方程沒有半徑限制。

### 線索三：Neumann 級數 = 逐次逼近

把 $\phi = f + \lambda T\phi$ 反覆代入自身，形式上得到

$$
\phi = f + \lambda T f + \lambda^2 T^2 f + \lambda^3 T^3 f + \cdots = \sum_{n=0}^\infty \lambda^n T^n f .
$$

寫成積分形式，就是著名的 **Neumann 級數**：

$$
\phi(x) = f(x) + \lambda \int_a^x K(x,t) f(t)\,dt + \lambda^2 \int_a^x K_2(x,t) f(t)\,dt + \cdots .
$$

因為疊核有階乘壓制，這個級數在 $[a,b]$ 上一致收斂，逐項積分合法，因此 $\phi$ 是良定的連續函數。

### 收網：存在性與唯一性

**存在性**：令 $\phi_N = \sum_{n=0}^N \lambda^n T^n f$ 。則

$$
\phi_N - \lambda T \phi_N = f - \lambda^{N+1} T^{N+1} f ,
$$

而 $\|\lambda^{N+1} T^{N+1} f\|_\infty \le |\lambda|^{N+1} \dfrac{M^{N+1}(b-a)^{N+1}}{(N+1)!} \|f\|_\infty \to 0$ 。故 $\phi_N$ 的極限 $\phi$ 滿足 $\phi = f + \lambda T\phi$ 。

**唯一性**：設 $\phi_1, \phi_2$ 都是解，令 $u = \phi_1 - \phi_2$ ，則 $u = \lambda T u$ 。取 $[a,c]$ 上 $|u|$ 的最大值點 $c$ ：

$$
|u(c)| \le |\lambda| \int_a^c M |u(t)|\,dt \le |\lambda| M (c-a) |u(c)| .
$$

當 $c$ 靠近 $a$ 時 $|\lambda| M (c-a) < 1$ ，故 $|u(c)| = 0$ ；逐步向右推進，得 $u \equiv 0$ 。

### 對照表：Volterra 型 vs Fredholm 型

| 特徵 | Volterra（1887） | Fredholm（1900） |
|------|------------------|------------------|
| 積分上限 | 動態： $\int_a^x$ | 固定： $\int_a^b$ |
| 收斂條件 | 對所有 $\lambda$ 收斂 | $\lvert\lambda\rvert$ 小於收斂半徑 |
| 證明工具 | 疊核的階乘壓制 | 行列式理論 |
| 解的行為 | 恆存在且唯一 | 可能出現特徵值與二擇一 |

## 結案報告

1. **解存在且唯一**：對任意連續的 $f$ 與核 $K$ ，第二類 Volterra 積分方程 $\phi = f + \lambda T\phi$ 在 $[a,b]$ 上有唯一的連續解，對**一切** $\lambda$ 成立——沒有特徵值障礙。
2. **Neumann 級數是顯式解**： $\phi = \sum_{n=0}^\infty \lambda^n T^n f$ ，逐項可寫成疊核積分。
3. **算子觀念的萌芽**：Volterra 把「未知函數」當作可以被算子 $T$ 作用的對象，這正是泛函分析「函數即點、方程即算子方程」思想的開山之作。
4. **遺產**：Volterra 方程的「階乘壓制」精神日後演化為 Banach 不動點定理與壓縮映射原理；他的算子思維直接啟發了 Fredholm（1900）與 Hilbert（1906）。積分方程從此從雜技變成理論。

## 證據與工具

| 證據/工具 | 陳述 | 用途 |
|-----------|------|------|
| 第二類 Volterra 方程 | $\phi(x) = f(x) + \lambda\int_a^x K(x,t)\phi(t)\,dt$ | 案發現場的嫌犯 |
| 疊核 | $K_n(x,t) = \int_t^x K_{n-1}(x,s)K(s,t)\,ds$ | 迭代算子的顯式表達 |
| 階乘壓制估計 | $\lvert K_n(x,t)\rvert \le M^n(x-t)^{n-1}/(n-1)!$ | 保證級數對所有 $\lambda$ 收斂 |
| Neumann 級數 | $\phi = \sum_{n=0}^\infty \lambda^n T^n f$ | 顯式解、構造性證明 |
| 逐步推進法 | 區間分小段、先左後右 | 唯一性證明的核心技巧 |

**證明骨架**（存在唯一）：

```
疊核定義 → 階乘壓制估計 → Neumann 級數一致收斂
        → 部分和驗證方程（存在性）
        → u = λTu 取最大值點 + 逐步推進（唯一性）
```

**一句話結案**：積分上限會動的方程，被自己不斷縮短的積分區間馴服——Volterra 用階乘壓制擒獲無窮維的第一隻怪物，泛函分析就此開山。
