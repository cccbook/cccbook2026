# 1928 — Dirac 方程

## 案件摘要
1928 年 1 月，Dirac 尋求一個**相對論性且線性**於時間導數的波動方程，以解決 Klein–Gordon 方程的負機率問題。方程的平方根線性化技巧意外地強迫自旋湧現、預言負能量解，進而導致 1932 年正電子的發現——反物質從此進入物理學。

## 前因 -- 為什麼會有這個案子
- Schrödinger 方程**非相對論**（不含 $c$），不適用高能電子；Bohr 與 Sommerfeld 的精細結構理論只能半經典地處理。
- 1926 年 Klein–Gordon 方程（將 $E^2 = p^2c^2 + m^2c^4$ 直接量子化）問世，但有致命缺陷：機率密度可為**負**，且無法解釋自旋。
- Dirac 當時 25 歲，追求「美」的數學結構——他要一階時間導數（像 Schrödinger 方程那樣 $\psi$ 演化）加相對論協變。

## 線索與推理 -- 數學式、程式、理論

### 線索一：Klein–Gordon 方程的問題（負機率）
對相對論能量關係 $E^2 = p^2c^2 + m^2c^4$ 直接代入 $E \to i\hbar\partial_t$、$p \to -i\hbar\nabla$：

$$\left(\frac{1}{c^2}\frac{\partial^2}{\partial t^2} - \nabla^2 + \frac{m^2c^2}{\hbar^2}\right)\psi = 0$$

這是二階時間導數方程，其「機率密度」$\rho \propto \psi^*\partial_t\psi - \psi\,\partial_t\psi^*$ **可正可負**——違反 Born 的 $P = |\psi|^2 \geq 0$。此外它是純量方程，自旋 1/2 無處安放。

### 線索二：Dirac 的平方根線性化技巧
Dirac 的想法：對 $E^2 = p^2c^2 + m^2c^4$ **開平方並線性化**，設

$$E = \beta mc^2 + c\,\boldsymbol{\alpha}\cdot\mathbf{p}$$

即要求方程 $(\beta mc^2 + c\,\boldsymbol{\alpha}\cdot\mathbf{p})\psi = E\psi$。自乘後仍須還原能量關係，迫使係數滿足**反對易關係**：

$$\alpha_i\alpha_j + \alpha_j\alpha_i = 2\delta_{ij}, \qquad \alpha_i\beta + \beta\alpha_i = 0, \qquad \beta^2 = 1$$

純量（數）不可能滿足 $\alpha_i\beta = -\beta\alpha_i$ 且 $\alpha_i^2 = \beta^2 = 1$（除非零）——**它們必須是矩陣**。最小維度為 **4×4**。得到的方程（協變形式）：

$$\left(i\hbar c\,\gamma^\mu\partial_\mu - mc^2\right)\psi = 0, \qquad \{\gamma^\mu, \gamma^\nu\} = 2g^{\mu\nu}$$

這就是**Dirac 方程**，$\gamma^\mu$（$\mu = 0,1,2,3$）即狄拉克矩陣。

### 線索三：電子自旋自然湧現
Pauli 1927 為解釋自旋曾**手動**在 Schrödinger 方程中加入 2×2 Pauli 矩陣與二階自旋-軌道耦合。而 Dirac 方程中，$\boldsymbol{\alpha}$ 矩陣的結構**自動**給出：

- $\psi$ 有 4 個分量 → 自旋 1/2 的兩個分量 + 負能量態兩個分量。
- 自旋-軌道耦合 $\frac{1}{2m^2c^2}\frac{1}{r}\frac{dV}{dr}\,\mathbf{L}\cdot\mathbf{S}$ 在展開中**自然出現**，其係數精確解釋氫原子精細結構（Sommerfeld 精細結構常數 $\alpha \approx 1/137$ 的角色）。
- Pauli 矩陣 $\sigma_i$ 嵌入 4×4 狄拉克矩陣的塊狀結構：

$$\boldsymbol{\alpha} = \begin{pmatrix} 0 & \boldsymbol{\sigma} \\ \boldsymbol{\sigma} & 0 \end{pmatrix}, \qquad \beta = \begin{pmatrix} I & 0 \\ 0 & -I \end{pmatrix}$$

### 線索四：$E^2 = p^2c^2 + m^2c^4$ 的負能量解與正電子預言
Dirac 方程的能量本徵值：

$$E = \pm\sqrt{p^2c^2 + m^2c^4}$$

**負能量分支**：電子會躍遷到負能態、無限放能？Dirac 1930 年提出「空穴理論」（hole theory）：負能態被 Pauli 不相容原理**填滿**形成「Dirac 海」，一個空穴的行為如同**帶正電、質量與電子相同**的粒子——預言**正電子（positron）**。

1932 年，Carl Anderson 在宇宙射線雲室中發現正電子，Dirac 的預言確認。1955 年反質子也被發現，反物質成為標準模型的一部分。

### 程式碼範例：驗證狄拉克矩陣的反對易關係與色散關係
```python
import numpy as np

I2 = np.eye(2)
sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)

# 4x4 狄拉克矩陣（Dirac 表象）
alpha = [np.block([[0*I2, s], [s, 0*I2]]) for s in (sx, sy, sz)]
beta = np.block([[I2, 0*I2], [0*I2, -I2]])

# 驗證 {α_i, α_j} = 2δ_ij 與 {α_i, β} = 0
for i in range(3):
    for j in range(3):
        ac = alpha[i] @ alpha[j] + alpha[j] @ alpha[i]
        assert np.allclose(ac, 2 * np.eye(4) * (i == j)), f"α{i},α{j} 失敗"
    assert np.allclose(alpha[i] @ beta + beta @ alpha[i], 0), f"α{i},β 失敗"
print("反對易關係全部通過 ✓")

# 能量-動量色散：E = ±sqrt(p²c² + m²c⁴)（自然單位 ħ=c=1）
m, px, py, pz = 1.0, 0.6, 0.0, 0.8
H = m * beta + px * alpha[0] + py * alpha[1] + pz * alpha[2]
Eigs = np.linalg.eigvalsh(H)
p2 = px**2 + py**2 + pz**2
print("數值能階:", Eigs)
print("理論能階:", sorted([-np.sqrt(p2 + m**2), -np.sqrt(p2 + m**2),
                           np.sqrt(p2 + m**2), np.sqrt(p2 + m**2)]))
```

數值能階與 $\pm\sqrt{p^2c^2 + m^2c^4}$ 完全吻合，且每階二重簡併（自旋上下）——Dirac 方程的核心結構直接驗證。

## 結案 -- 後果與影響
- 反物質的預言與發現，開啟粒子物理學；Dirac 獲 **1933 諾貝爾獎**（與 Schrödinger 同年）。
- Klein–Gordon 方程獲得重生：它不是錯了，而是描述**自旋 0** 粒子（如 π 介子、Higgs）；「負機率」問題在量子場論中以「反粒子 = 沿時間反向的粒子」解決。
- Dirac 方程成為相對論性量子力學與量子場論（QED）的基礎：1930 年《量子力學原理》建立 bra-ket 語言。
- 自旋-軌道耦合精確解釋氫原子精細結構；1947 年 Lamb 位移的小偏差引出 QED 重整化。
- 深遠影響：PET 醫學影像（正電子湮滅）、QED 的 $g-2$ 精密檢驗、Dirac 海概念的拓撲量子材料（石墨烯、Weyl 半金屬）。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Paul Dirac | 提出方程、預言正電子，1933 諾貝爾獎 |
| Oskar Klein / Walter Gordon | Klein–Gordon 方程 |
| Wolfgang Pauli | 2×2 Pauli 矩陣（自旋），1945 諾貝爾獎 |
| Carl Anderson | 1932 發現正電子，1936 諾貝爾獎 |

- P. A. M. Dirac, The Quantum Theory of the Electron, Proc. R. Soc. A **117**, 610; **118**, 351 (1928)。
- P. A. M. Dirac, *The Principles of Quantum Mechanics* (1930)。
- C. D. Anderson, Science **76**, 238 (1932)。
