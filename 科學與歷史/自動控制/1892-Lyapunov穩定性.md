# 1892 - Lyapunov 穩定性

## 案件摘要

1892 年，Aleksandr Lyapunov（李亞普諾夫）出版博士論文《運動穩定性的一般問題》
(Общая задача об устойчивости движения)。
Routh–Hurwitz 判據（見 [1877-Routh穩定性判據.md](1877-Routh穩定性判據.md)）只處理線性系統；
Lyapunov 的偵探手法：借鑑 Dirichlet 的能量論證，定義**廣義能量函數**（Lyapunov 函數），
不用線性化、不用求解，直接判斷**非線性系統**的穩定性。
穩定性理論從線性推廣到一般系統——現代非線性控制的基石在此奠定。

## 前因

- **Routh–Hurwitz 的限制**：只適用線性定常系統；真實系統（蒸汽機、離心調速器的非線性飽和、飛球的 $\sin\theta$）處處非線性。
- **Dirichlet 的能量論證**：力學中，若位能 $V$ 在平衡點取極小，則平衡穩定（能量像山谷，球滾不出去）。
- **Poincaré 的動力系統研究**（1881–1890）：軌道的定性理論、極限環——非線性動力學的語言剛成形。

## 線索與推理

### 第 1 步：穩定性的精確定義

給定系統 $\dot x = f(x)$，平衡點 $x^* = 0$。Lyapunov 定義三層穩定性：

| 概念 | 定義 |
|------|------|
| 穩定（stable） | 給定 $\epsilon$，存在 $\delta$：初始偏差 $\|\delta x\| < \delta$ ⇒ 軌跡永遠留在 $\|x\| < \epsilon$ 內 |
| 漸近穩定（asymptotically stable） | 穩定，且 $\|x(t)\| \to 0$ |
| 指數穩定（exponentially stable） | $\|x(t)\| \le c\,e^{-\alpha t}\|x(0)\|$ |

### 第 2 步：Lyapunov 函數

Lyapunov 的核心想法：找一個「廣義能量」函數 $V(x)$，滿足

$$
V(0) = 0, \qquad V(x) > 0 \ (x \neq 0)
$$

（**正定性**：像一個碗。）若沿軌跡能量**單調下降**：

$$
\dot V(x) = \frac{\partial V}{\partial x} f(x) < 0 \quad (x \neq 0)
$$

則系統**漸近穩定**。直觀：球在碗裡有摩擦，能量一直減少，最後停在碗底。

**Lyapunov 第一法（線性化法）**：若線性化的特徵根實部皆非零，
則非線性系統在平衡點附近的穩定性與線性化一致。
**Lyapunov 第二法（直接法）**：上述能量函數法，不需要線性化。

### 第 3 步：為什麼這是推廣？

Routh–Hurwitz 需要線性系統；Lyapunov 第二法對**任何** $\dot x = f(x)$ 都適用——
唯一的困難是「找到 $V$」。對力學系統，總能量 $V = T + V_{pot}$ 常常就是候選：
若系統有阻尼，$\dot V = -(\text{耗散功率}) < 0$，自動漸近穩定。

### 範例：阻尼單擺的穩定性

阻尼單擺：

$$
m\ell^2\ddot\theta + b\dot\theta + mg\ell\sin\theta = 0
$$

寫成狀態方程 $x = (\theta, \dot\theta)$。取能量函數：

$$
V(x) = \frac{1}{2}m\ell^2\dot\theta^2 + mg\ell(1 - \cos\theta)
$$

沿軌跡求導：

$$
\dot V = m\ell^2\dot\theta\,\ddot\theta + mg\ell\sin\theta\,\dot\theta
= \dot\theta\,(m\ell^2\ddot\theta + mg\ell\sin\theta) = -b\dot\theta^2 \le 0
$$

**動能與位能的交換項相消，只剩耗散項** $-b\dot\theta^2$——能量單調減少。
用 LaSalle 不變集原理（$\dot V = 0$ 的集合是 $\dot\theta = 0$，
軌跡只能停在 $\theta = 0$）：系統**漸近穩定到碗底**。

這個計算是 Lyapunov 方法的第一範例：**不需要解非線性方程** $\ddot\theta = -\frac{g}{\ell}\sin\theta$（它沒有初等解！），就能證明穩定。

### 為什麼「不解方程」是關鍵？

非線性方程大多沒有初等解（三體問題、雙擺、混沌系統）。
Routh 的路（解根）與 Lyapunov 的路（找能量）都是「繞過求解」的偵探手法，
但 Lyapunov 的路**連線性化都不需要**——它處理的是全域的、非線性的穩定性。

## 後果

- 非線性控制的基石：一切非線性系統的穩定性證明，幾乎都用 Lyapunov 函數。
- LaSalle 不變集原理（1960）、Barbalat 引理：Lyapunov 方法的推廣。
- 自適應控制（adaptative control）：用 Lyapunov 函數設計參數自適應律——控制理論與穩定性證明的合流。
- 俄國學派的秘密武器：Lyapunov 方法在俄國流行了 50 年，1960 年代才被西方「重新發現」。

## 結案陳詞

Lyapunov 的貢獻是把「穩定」從線性系統的特例，推廣成**一般系統的能量論證**。
他的偵探手法——不解方程、找廣義能量——成為非線性控制百年來唯一的通用證明工具。
今天每篇非線性控制的論文，幾乎都有一個 Lyapunov 函數。
