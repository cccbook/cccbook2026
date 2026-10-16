# 1926 — Schrödinger 波動力學

## 案件摘要
1926 年初，Schrödinger 在四篇系列論文〈Quantisierung als Eigenwertproblem〉中，把 de Broglie 的物質波假說轉化為一條波動方程，用量子力學的「特徵值問題」重新解釋原子光譜。波動力學與 Heisenberg 的矩陣力學表面形式迥異，同年即被證明數學等價，成為今日教科書的標準語言。

## 前因 -- 為什麼會有這個案子
- 1913 年 Bohr 模型硬性規定電子軌道角動量 $L = n\hbar$，能算氫光譜卻「說不出為什麼」。
- 1924 年 de Broglie 提出物質波：$\lambda = h/p$，電子也是波。
- 1925 年 Heisenberg 矩陣力學問世，但代數抽象難懂。
- Debye 在蘇黎世研討會上挑釁：「如果電子是波，就該有波動方程。Schrödinger，你的波動方程呢？」——這句話就是案發現場的起點。

## 線索與推理 -- 數學式、程式、理論

### 線索一：從 de Broglie 到波動方程
對自由粒子平面波 $\psi = e^{i(kx - \omega t)}$，用 $E = \hbar\omega$、$p = \hbar k$ 代入相對論關係或非相對論能量式 $E = p^2/2m$，反推得到**時間相關 Schrödinger 方程**：

$$i\hbar\frac{\partial \psi}{\partial t} = \hat{H}\psi = \left(-\frac{\hbar^2}{2m}\nabla^2 + V\right)\psi$$

對穩態 $\psi(x,t) = \phi(x)e^{-iEt/\hbar}$ 分離變數，得到**穩態（與時間無關）方程**：

$$-\frac{\hbar^2}{2m}\nabla^2\psi + V\psi = E\psi$$

這是一個 Sturm–Liouville 特徵值問題：邊界條件會「自動」篩出離散能階——Bohr 的 $n$ 不再是假設，而是數學的必然。

### 線索二：一維無限深位能井
位能 $V(x) = 0$（$0 < x < L$），井外 $V = \infty$，故 $\psi(0) = \psi(L) = 0$。解為：

$$\psi_n(x) = \sqrt{\frac{2}{L}}\sin\left(\frac{n\pi x}{L}\right), \qquad E_n = \frac{n^2\pi^2\hbar^2}{2mL^2}, \quad n = 1, 2, 3, \dots$$

注意能階 $E_n \propto n^2$：能階間距越來越大，基態能量不為零（零點能），這是測不準原理的直接後果。

### 線索三：諧振子
$V = \frac{1}{2}m\omega^2 x^2$，Schrödinger 方程的解（用 Hermite 多項式）：

$$\psi_n(x) = \frac{1}{\sqrt{2^n n!}}\left(\frac{m\omega}{\pi\hbar}\right)^{1/4} e^{-m\omega x^2/2\hbar}\, H_n\!\left(\sqrt{\frac{m\omega}{\hbar}}x\right), \qquad E_n = \hbar\omega\left(n + \frac{1}{2}\right)$$

能階**等間距** $\hbar\omega$，完美重現 Planck 1900 年的黑體輻射假設 $E = nh\nu$——但多了 $\frac{1}{2}$ 的零點能。

### 線索四：證明波動力學與矩陣力學等價
1926 年 Schrödinger 在〈Über das Verhältnis...〉中證明：若定義矩陣元素

$$x_{mn} = \int \psi_m^*\, x\, \psi_n\, dx$$

則波動力學的特徵函數 $\psi_n$ 與 Heisenberg 矩陣力學給出**完全相同**的物理預測。同年 Eckart、Pauli（用么正變換）也獨立證明等價性。兩套「兇器」其實是同一件。

### 程式碼範例：numpy 模擬無限深位能井的前三個波函數
```python
import numpy as np
import matplotlib.pyplot as plt

L, N = 1.0, 200
x = np.linspace(0, L, N)

# 解析解：前三個本徵態
fig, ax = plt.subplots(figsize=(8, 5))
for n in range(1, 4):
    psi_n = np.sqrt(2 / L) * np.sin(n * np.pi * x / L)
    En = (n**2 * np.pi**2 * 1.0546e-34**2) / (2 * 9.109e-31 * L**2)  # 電子
    ax.plot(x, psi_n + 2.2 * n, label=f"n={n}, E∝n²={n**2}")
    ax.axhline(2.2 * n, ls="--", c="gray", lw=0.5)

# 數值驗證：數值微分算第二階導數檢查方程
psi1 = np.sqrt(2 / L) * np.sin(np.pi * x / L)
d2 = (np.roll(psi1, 1) - 2 * psi1 + np.roll(psi1, -1)) / (x[1] - x[0])**2
ratio = -d2 / psi1  # 應為常數 (π/L)²
print("數值 (π/L)² =", np.mean(ratio[2:-2]), "理論 =", (np.pi / L)**2)

ax.set_title("Infinite Square Well: first three eigenstates")
ax.legend(); plt.show()
```

數值輸出中 $-d^2\psi/\psi = (\pi/L)^2$ 為常數，直接驗證了穩態方程 $-\frac{\hbar^2}{2m}\psi'' = E\psi$。

## 結案 -- 後果與影響
- 波動力學成為量子力學的**標準表述**：偏微分方程可解、可視覺化、化學家可用。
- 離散能階來自邊界條件，原子光譜之謎正式結案。
- 為 1926 年 Born 的機率詮釋提供舞台：$|\psi|^2$ 從此有意義。
- 1927 年 Dirac 推廣到相對論、1930 年《量子力學原理》整合全書架構。
- 影響至今：分子軌道理論、量子化學、半導體能帶理論（Kronig–Penney 模型）皆源於此。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Erwin Schrödinger | 提出波動方程，1933 諾貝爾獎 |
| Louis de Broglie | 物質波假說，1929 諾貝爾獎 |
| Werner Heisenberg | 矩陣力學（與波動力學等價） |
| Peter Debye | 蘇黎世研討會的「點火者」 |

- E. Schrödinger, *Quantisierung als Eigenwertproblem*, Ann. Phys. **79**, 361, 489, 734 (1926)。
- E. Schrödinger, Ann. Phys. **79**, 734 (1926)：波動力學與矩陣力學等價性證明。
