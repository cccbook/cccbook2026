# 附錄 B：化學中常見的微積分與線性代數公式總覽

> 本附錄彙整本書各章使用的數學工具，方便查閱與複習。

## B.1 熱力學（第 5 章）

| 公式 | 意義 |
|---|---|
| $dU = T\,dS - P\,dV$ | 熱力學基本關係 |
| $G = H - TS = U + PV - TS$ | Gibbs 自由能 |
| $dG = -S\,dT + V\,dP$ | 定溫定壓下的判準 |
| $\left(\frac{\partial S}{\partial V}\right)_T = \left(\frac{\partial P}{\partial T}\right)_V$ | Maxwell 關係式之一 |
| $\mu_i = \mu_i^\circ + RT \ln a_i$ | 化學勢 |
| $\Delta G^\circ = -RT\ln K$ | 平衡常數與自由能 |

**全微分的判定**：$dZ = M\,dx + N\,dy$ 為全微分 $\iff \frac{\partial M}{\partial y} = \frac{\partial N}{\partial x}$（Euler 互逆定理），這是所有 Maxwell 關係式的共同源頭。

## B.2 動力學（第 6–7 章）

| 反應級數 | 微分方程 | 積分式 | 半衰期 |
|---|---|---|---|
| 零級 | $-\frac{d[A]}{dt}=k$ | $[A]=[A]_0-kt$ | $\frac{[A]_0}{2k}$ |
| 一級 | $-\frac{d[A]}{dt}=k[A]$ | $[A]=[A]_0e^{-kt}$ | $\frac{\ln 2}{k}$ |
| 二級 | $-\frac{d[A]}{dt}=k[A]^2$ | $\frac{1}{[A]}=\frac{1}{[A]_0}+kt$ | $\frac{1}{k[A]_0}$ |

* **Arrhenius 方程**：$k = Ae^{-E_a/RT}$；$\ln k = -\frac{E_a}{R}\frac{1}{T} + \ln A$（直線斜率給 $E_a$）。
* **穩態近似**：中間體 $I$ 滿足 $\frac{d[I]}{dt}\approx 0$。
* **線性化系統的穩定性**：Jacobian $J$ 的特徵值——實部全負（穩定）、正實部（不穩）、純虛數對（振盪候選）。

## B.3 量子化學（第 3–4 章）

| 公式 | 意義 |
|---|---|
| $\hat H\psi = E\psi$ | 時間獨立薛丁格方程（本徵值問題） |
| $\hat p = -i\hbar\frac{d}{dx}$ | 動量算子 |
| $[\hat x,\hat p]=i\hbar$ | 正則交換子 → 測不準原理 $\Delta x\Delta p\ge\hbar/2$ |
| $E[\psi] = \frac{\langle\psi|\hat H|\psi\rangle}{\langle\psi|\psi\rangle} \ge E_0$ | 變分原理 |
| $E^{(1)}=\langle\psi^{(0)}|\hat V|\psi^{(0)}\rangle$ | 一階微擾能量 |
| $\hat A\hat B \ne \hat B\hat A \Rightarrow$ 不可同時測量 | 交換子與相容性 |

**矩陣對角化**：Hückel / Hartree-Fock 最終都化為

$$
HC = SCE
$$

（廣義本徵值問題），其中 $S$ 是軌域重疊矩陣；用 Löwdin 正交化 $S^{-1/2}$ 轉為標準本徵值問題。

## B.4 圖論與拓撲（第 8–9 章）

| 公式 | 意義 |
|---|---|
| $W = \frac{1}{2}\sum_{i,j} d_{ij}$ | Wiener 指數（最短路徑距離和） |
| $L = D - A$ | Laplacian 矩陣 |
| $\det(L \text{去掉一行}) = \text{生成樹數}$ | Matrix–Tree 定理 |
| $V - E + F = 2(1-g)$ | Euler–Poincaré 示性數（$g$ 為虧格） |
| $n_{\text{五元環}}=12,\ n_{\text{六元環}}=\text{任意}$ | C60 與富勒烯的組合限制 |

## B.5 統計力學（第 11 章）

| 公式 | 意義 |
|---|---|
| $p_i = \frac{e^{-\varepsilon_i/k_BT}}{Z}$ | Boltzmann 分佈 |
| $Z = \sum_i e^{-\varepsilon_i/k_BT}$ | 分劃函數 |
| $U = -\frac{\partial \ln Z}{\partial \beta}$ | 內能（$\beta = 1/k_BT$） |
| $S = k_B \ln \Omega = -k_B\sum_i p_i \ln p_i$ | Boltzmann／Gibbs 熵（與 Shannon 熵同構） |
| $F = -k_BT \ln Z$ | Helmholtz 自由能 |

## B.6 常用積分技巧

* 分離變數（一級動力學）、積分因子（線性 ODE）。
* 部分積分推 Maxwell 關係式時的循環偏微分：$\left(\frac{\partial x}{\partial y}\right)_z\left(\frac{\partial y}{\partial z}\right)_x\left(\frac{\partial z}{\partial x}\right)_y = -1$。
* 高斯積分 $\int_{-\infty}^\infty e^{-\alpha x^2}dx = \sqrt{\pi/\alpha}$——統計力學配分函數的基石。

## 小結

本書的主線可以用一句話概括：**化學現象 = 數學結構 + 物理假設**。掌握這些公式背後的數學結構（本徵值問題、全微分、動態系統、圖、機率分佈），化學就不再是記憶之學，而是推演之學。
