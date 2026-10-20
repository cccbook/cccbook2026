# 附錄 C：量子化學計算軟體背後的數學演算法簡介

> Gaussian、ORCA、PySCF、VASP 等軟體「點一下就跑」，但內部是一連串經典數學演算法。本附錄簡介其核心，讓讀者明白本書第 3–4 章的理論如何在工業級程式中落地。

## C.1 計算化學的層次結構

```mermaid
graph TD
    A[分子座標] --> B[決定理論層級]
    B --> C[分子力學 MM<br>牛頓力學 + 經驗力場]
    B --> D[半經驗法<br>Hückel / AM1]
    B --> E[HF / DFT<br>自洽場迭代]
    B --> F[後 HF<br>MP2 / CCSD(T)]
    C --> G[能量・優化・光譜]
    D --> G
    E --> G
    F --> G
```

層級越高越準確、越昂貴：MM（ $10^3$ 原子以上）→ 半經驗（ $10^2$ ）→ DFT（ $10^2$ ）→ CCSD(T)（ $10$ ）。

## C.2 自洽場（SCF）迭代

Hartree-Fock 是「雞生蛋」問題：軌域決定 Fock 矩陣，Fock 矩陣又決定軌域。解法是迭代：

1. 猜初始密度 $P^{(0)}$ （常用疊加原子密度）。
2. 組 Fock 矩陣 $F^{(k)} = H + G(P^{(k)})$ 。
3. 解廣義本徵值問題 $F C = S C \varepsilon$ 。
4. 更新密度 $P^{(k+1)}$ ，檢查收斂 $\|P^{(k+1)}-P^{(k)}\| < \epsilon$ 。
5. 未收斂則回 2（常用 DIIS 外插加速）。

數學核心：**迭代不動點 + 廣義本徵值分解**，正是 4.3 節矩陣對角化的工業版。

## C.3 積分計算：Gaussian 基底的設計動機

電子排斥積分（ERI）

$$
(\mu\nu|\lambda\sigma) = \iint \frac{\chi_\mu(1)\chi_\nu(1)\chi_\lambda(2)\chi_\sigma(2)}{r_{12}}\,d\tau_1 d\tau_2
$$

若基函數是高斯型 $e^{-\alpha r^2}$ ，兩高斯乘積仍是高斯（Gauss 乘積定理），四中心積分可解析計算——這正是名為 Gaussian 的軟體的命名由來，也是 Boys (1950) 選擇高斯基底（犧牲波函數在核處的正確尖峰）換取計算可行性的歷史決策。

## C.4 DFT 與數值格點

Kohn-Sham 方程（1965）形式上與 HF 相同，但交換相關項 $v_{xc}[\rho]$ 依賴密度 $\rho(\mathbf r)$ ，需在 3D 格點上數值積分：

$$
E_{xc} = \int v_{xc}(\mathbf r)\,\rho(\mathbf r)\,d\mathbf r \approx \sum_g w_g\, v_{xc}(\mathbf r_g)\,\rho(\mathbf r_g)
$$

用 Lebedev 球面格點 + 徑向格點。數學核心：**數值積分 + 泛函近似**。

## C.5 幾何優化：多元微積分的應用

找能量極小值 = 解 $\nabla E = 0$ ：

* **梯度** $\mathbf g = \partial E/\partial \mathbf R$ ：解析可得（Hellmann–Feynman 定理）。
* **Hessian** $\mathbf H = \partial^2 E/\partial R_i\partial R_j$ ：判斷極小（全正）或過渡態（恰一負特徵值）。
* 演算法：牛頓法、BFGS 準牛頓法——這正是第 7 章動態系統穩定性分析（Jacobian 特徵值）的化學對應。

## C.6 平行化與複雜度

| 方法 | 標度（電子數 $N$ ） | 加速技巧 |
|---|---|---|
| HF / DFT | $O(N^3) \sim O(N^4)$ | 密度擬合（DF）、線性標度分區 |
| MP2 | $O(N^5)$ | 局域相關 |
| CCSD(T) | $O(N^7)$ | 只用於小分子「黃金標準」 |

**密度擬合（Resolution of Identity）**用輔助基底近似四指標積分：

$$
(\mu\nu|\lambda\sigma) \approx \sum_{ab}(\mu\nu|a)\,V^{-1}_{ab}\,(b|\lambda\sigma)
$$

把 $O(N^4)$ 降為 $O(N^3)$ ——典型的「以線性代數換指數痛」。

## C.7 開源實作建議

想看數學如何寫成程式，推薦閱讀：

* **PySCF**（Python）：HF、DFT、CC 全都可用百行內讀懂核心。
* **Psi4**：演算法文件極完整。
* **Hückel 教學實作**：第 4.3 節的矩陣對角化，用 NumPy 十行即可重現丁二烯的 $\pi$ 軌域。

## 小結

量子化學軟體沒有任何「魔法」，只有三件事：**解析積分（高斯乘積）、線性代數（對角化）、迭代收斂（不動點）**。本書第 3、4 章的每一條數學，都能在這些程式中找到對應的函式呼叫。
