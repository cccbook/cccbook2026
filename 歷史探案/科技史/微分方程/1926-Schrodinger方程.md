# 1926 Schrödinger 方程

## 案發現場

1925 年冬，瑞士蘇黎世。物理學界正陷入一場概念危機。Bohr 的原子模型——電子在固定軌道上繞核運行——能解釋氫原子光譜，卻無法解釋為什麼軌道是固定的，也無法處理多電子原子。更糟的是，de Broglie 在 1924 年的博士論文中提出了一個大膽猜想：不只是光有波粒二象性，**一切物質都有波動性**，電子的波長為

$$
\lambda = \frac{h}{p} = \frac{h}{mv}
$$

其中 $h$ 是 Planck 常數，$p$ 是動量。這個想法實驗上很快被 Davisson–Germer 的電子繞射實驗（1927）證實，但理論上沒人知道：**這個「物質波」到底遵守什麼方程？**

在蘇黎世大學，38 歲的 Erwin Schrödinger（1887–1961）剛被聘為理論物理教授。他的同事 Debye 在一次討論會上說：如果物質是波，那就該有一個波動方程；你講了半天波，波動方程在哪裡？這句話像偵探對嫌犯的當頭質問，逼出了物理學史上最重要的微分方程。

此謎題之所以重要：原子光譜的分立性（為何只有特定能量的光被吸收或發射？）是十九世紀以來的最大懸案之一。若波動方程 + 邊界條件能自然給出分立能階，這將是微分方程本徵值理論對物理學最壯觀的應用。

## 偵查過程

### 關鍵靈感一：Hamilton 的光學—力學類比

Schrödinger 的推理起點不是實驗，而是一百年前 Hamilton 留下的一條數學線索。Hamilton 在 1830 年代發現：幾何光學的 eikonal 方程與力學的 Hamilton–Jacobi 方程在數學結構上完全平行。波動光學的波動方程

$$
\nabla^2 \psi - \frac{n^2}{c^2} \frac{\partial^2 \psi}{\partial t^2} = 0
$$

在波長 $\lambda \to 0$ 的極限下，其短波近似正是 eikonal 方程 $\ |\nabla S|^2 = n^2$。而 Hamilton–Jacobi 方程

$$
\frac{\partial S}{\partial t} + \frac{1}{2m}|\nabla S|^2 + V = 0
$$

正是力學版的 eikonal 方程。Schrödinger 的靈感是：**既然「波動光學 ⊃ 幾何光學」成立，那麼「波動力學 ⊃ 古典力學」也應該成立**。古典力學只是波動力學在波長趨近於零時的短波極限——就像幾何光學是波動光學的短波極限。

### 關鍵靈感二：從 de Broglie 關係推出方程

設波函數形式為 $\psi(\mathbf{r}, t) = \varphi(\mathbf{r})\, e^{-iEt/\hbar}$，其中 $\hbar = h/2\pi$。de Broglie 關係給出 $E = \hbar\omega$、$\mathbf{p} = \hbar\mathbf{k}$。

第一步：對時間求導可得

$$
i\hbar \frac{\partial \psi}{\partial t} = E\,\psi
$$

第二步：對空間求導可得

$$
-i\hbar \nabla \psi = \mathbf{p}\,\psi \quad\Longrightarrow\quad -\hbar^2 \nabla^2 \psi = p^2\,\psi
$$

第三步：古典能量關係 $E = \frac{p^2}{2m} + V$ 中，把 $E$ 換成 $i\hbar\partial_t$、把 $p^2$ 換成 $-\hbar^2\nabla^2$，即得

$$
i\hbar \frac{\partial \psi}{\partial t} = \left(-\frac{\hbar^2}{2m}\nabla^2 + V\right)\psi = \hat H \psi
$$

這就是含時 Schrödinger 方程。注意其推理本質是「算符替換」：把古典力學的相空間函數 $E(\mathbf{r},\mathbf{p})$ 中的變數換成對應的微分算符 $\hat E = i\hbar\partial_t$、$\hat{\mathbf{p}} = -i\hbar\nabla$。這正是 Hamilton 力學（見 [1838-Jacobi與Hamilton-Jacobi方程.md](1838-Jacobi與Hamilton-Jacobi方程.md)）的結構在量子世界的再現。

### 氫原子解與本徵值奇蹟

對氫原子，$V(r) = -\dfrac{e^2}{4\pi\varepsilon_0 r}$。因位勢不隨時間變化，分離變數 $\psi = \varphi e^{-iEt/\hbar}$，得定態方程

$$
\left(-\frac{\hbar^2}{2m}\nabla^2 - \frac{e^2}{4\pi\varepsilon_0 r}\right)\varphi = E\,\varphi
$$

在球坐標下分離變數 $\varphi = R(r)\,Y_\ell^m(\theta,\phi)$，徑向方程為

$$
\frac{1}{r^2}\frac{d}{dr}\left(r^2\frac{dR}{dr}\right) + \left[\frac{2m}{\hbar^2}\left(E + \frac{e^2}{4\pi\varepsilon_0 r}\right) - \frac{\ell(\ell+1)}{r^2}\right]R = 0
$$

**這裡是微分方程偵查的破案關鍵**：物理上要求波函數在 $r \to \infty$ 處可積（歸一化），這是邊界條件。對徑向方程做無量綱化並代入 $R = \rho^\ell e^{-\rho/2} L(\rho)$（其中 $\rho = \dfrac{2r}{na_0}$，$a_0$ 是 Bohr 半徑），$L$ 滿足**伴隨 Laguerre 方程**：

$$
\rho \frac{d^2 L}{d\rho^2} + 2(\ell + 1 - \rho)\frac{dL}{d\rho} + (n - \ell - 1)L = 0
$$

此方程只有在 $n - \ell - 1$ 為非負整數時才有多項式解（否則級數解在無窮遠發散，違反歸一化）。因此：

$$
E_n = -\frac{m e^4}{2(4\pi\varepsilon_0)^2 \hbar^2}\cdot\frac{1}{n^2}, \qquad n = 1, 2, 3, \dots
$$

**分立能階不是假設，而是微分方程 + 邊界條件的數學必然**。Schrödinger 算出的 $E_n$ 與 Bohr 模型完全一致，且自然解釋了主量子數 $n$、角量子數 $\ell$、磁量子數 $m$ 的來源——它們是球諧函數與 Laguerre 多項式的指標。這是 Sturm–Liouville 本徵值理論（見 [1858-SturmLiouville理論.md](1858-SturmLiouville理論.md)）在物理學的巔峰應用。

### 結案前的最後一塊拼圖：Born 的機率詮釋

Schrödinger 原本想用電磁波詮釋 $\psi$，但波包會擴散，且多粒子情形 $\psi$ 是組態空間的函數，無法是物理波。1926 年，Max Born 在研究散射問題時提出：$|\psi(\mathbf{r})|^2$ 是**機率密度**——在 $\mathbf{r}$ 附近找到粒子的機率。測量問題從此成為量子力學的核心哲學議題，而 Schrödinger 本人在 1935 年用著名的「薛丁格的貓」思想實驗表達了對此的不安。

## 結案報告

Schrödinger 方程的偵破路線圖清晰可循：

1. **Hamilton 的光學—力學類比**（1830s）提供結構框架；
2. **Planck 與 de Broglie 的量子化關係**（1900/1924）提供算符替換的原料；
3. **Debye 的當頭質問**（1925）觸發偵查；
4. **本徵值理論 + 邊界條件**（1926）破案——分立光譜是數學必然。

其遺產無比深遠：

- **化學**：電子組態、化學鍵、分子軌道理論全部建立在 Schrödinger 方程之上。
- **半導體與現代電子業**：能帶理論是 Schrödinger 方程在週期位勢（Bloch 波）上的解。
- **數學**：譜理論、泛函分析、Hilbert 空間（正是 Hilbert 第 6 問的路線，見 [1900-Hilbert與微分方程問題.md](1900-Hilbert與微分方程問題.md)）因量子力學而爆發。
- **計算**：現代的密度泛函理論（DFT）、量子化學計算軟體，本質上都是數值求解 Schrödinger 方程——延續到 [1975-數值解與SciPy.md](1975-數值解與SciPy.md) 的數值大眾化。
- **混沌與量子混沌**：當系統變得非線性，古典方程走向混沌（[1963-Lorenz混沌與蝴蝶效應.md](1963-Lorenz混沌與蝴蝶效應.md)），量子對應物則催生了量子混沌學。

而 Schrödinger 方程本身是線性的——這是它與古典非線性方程最大的不同，也正是量子世界線性代數結構的根源。

## 證據與工具

以下程式數值求解一維定態 Schrödinger 方程（有限位勢井），展示「分立能階是邊界條件的數學必然」：

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh_tridiagonal

# 一維定態 Schrödinger 方程（自然單位 hbar = m = 1）：
#   -1/2 * psi'' + V(x) * psi = E * psi
# 用有限差分離散化：psi'' ≈ (psi[i-1] - 2 psi[i] + psi[i+1]) / dx^2
# 這將方程變成三對角矩陣的「本徵值問題」——正是 Sturm-Liouville 理論的離散版本

# 有限位勢井：寬度 L=4，深度 V0=-10，井外 V=0
L, V0 = 4.0, -10.0
x_min, x_max, N = -10.0, 10.0, 2000
x = np.linspace(x_min, x_max, N)
dx = x[1] - x[0]
V = np.where(np.abs(x) < L/2, V0, 0.0)

# 三對角矩陣的對角與次對角元素
main_diag  = 1.0/dx**2 + V[1:-1]          # 中央對角線（跳過邊界點）
off_diag   = -0.5/dx**2 * np.ones(N-3)    # 次對角線

# 邊界條件 psi(±10)=0 已含在離散化中——這是本徵值分立的關鍵
eigvals, eigvecs = eigh_tridiagonal(main_diag, off_diag, select='i',
                                    select_range=(0, 5))

# 解析解驗證：無限深井寬 L 的能階 E_n = n^2 * pi^2 / (2 L^2)
# 有限深井的能階會略低於無限深井（波函數滲入井外）
print("數值本徵值（前 6 個）:", np.round(eigvals, 4))
E_inf_well = [(n+1)**2 * np.pi**2 / (2 * L**2) for n in range(6)]
print("無限深井解析值     :", np.round(E_inf_well, 4))
print("=> 有限深井能階低於無限深井，因波函數滲出邊界")

# 畫出位勢與前幾個波函數（縱向偏移 = 能階位置）
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x, V, 'k-', lw=2, label='位勢 V(x)')
for i, E in enumerate(eigvals):
    psi = eigvecs[:, i]
    psi = psi / np.max(np.abs(psi)) * 1.5  # 歸一化顯示
    ax.plot(x, psi + E, lw=1.2, label=f'n={i+1}, E={E:.3f}')
ax.set_ylim(V0 - 1, 3)
ax.set_xlabel('x'); ax.set_ylabel('能量 / 波函數')
ax.set_title('一維 Schrödinger 方程的定態解：分立能階是邊界條件的必然')
ax.legend(fontsize=8); ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("schrodinger_well.png", dpi=120)
plt.show()

# 延伸：改變 V0 趨向無限深井（V0 -> -10000），數值能階應逼近 n^2 pi^2/(2L^2)
```

程式展示了偵查的核心：**把微分方程離散成本徵值問題**。1926 年 Schrödinger 用解析方法（Laguerre 多項式）破案；今天的化學家與工程師用數值矩陣本徵值破案——方法變了，偵探精神沒變：邊界條件決定一切。
