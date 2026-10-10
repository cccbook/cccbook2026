# 1925-Pauli 不相容原理

## 案件摘要
1925 年 1 月，25 歲的 Wolfgang Pauli 提出「不相容原理」：同一量子態不能容納兩個電子。這一條規則解開了週期表結構與反常 Zeeman 效應兩大謎題，並引出電子自旋 $s=\frac{1}{2}$ 的存在。它是費米子世界的根本法則，也是物質穩定性的最終守護者。

## 前因 -- 為什麼會有這個案子
- 1913 年 Bohr 模型解釋了氫原子，但**為何週期表是 2, 8, 18, 32… 的殼層結構**完全無解。
- **反常 Zeeman 效應**：譜線在磁場中分裂的方式（如鈉 D 線分裂成 4 條）無法用 Sommerfeld 理論解釋，被 Pauli 稱為「一半量子數的謎」。
- 原子「不塌縮」的謎：為何所有電子不擠進基態？經典物理無法回答。
- 1922 年 Stern–Gerlach 實驗發現銀原子束在非均勻磁場中分裂成**兩道**，與軌道角動量量子化預言（$2l+1$ 為奇數道）不符——這是「二分」之謎。

## 線索與推理 -- 數學式、程式、理論

### 不相容原理 (1925)
Pauli 在 *Über den Zusammenhang des Abschlusses der Elektronengruppen im Atom mit der Komplexstruktur der Spektren* 中提出：

> 一個原子中不可能有兩個電子具有完全相同的四個量子數 $(n, l, m_l, m_s)$。

用波函數語言：兩電子系統的總波函數對交換必須**反對稱**：

$$
\Psi(1,2) = -\Psi(2,1)
\quad\Longrightarrow\quad
\Psi(1,1) = 0 \;(\text{同態機率為零})
$$

這解釋了：原子中電子必須逐層填充 → 週期表結構 $2, 8, 18, 32$（每殼容量 $2n^2$）→ 物質的穩定與化學的多樣性。Pauli 自己稱之為「一種經典理論無法解釋的新型統計法則」。

### 電子自旋 $s = \frac{1}{2}$
1925 年 10 月，Uhlenbeck 與 Goudsmit 提出電子自旋假說解釋反常 Zeeman 效應。電子具有內秉角動量：

$$
S^2 = s(s+1)\hbar^2 = \frac{3}{4}\hbar^2, \qquad S_z = m_s\hbar, \quad m_s = \pm\frac{1}{2}
$$

只有**兩個**投影值 $m_s = \pm\frac{1}{2}$——正是 Stern–Gerlach 實驗中「分裂成兩道」的原因（銀原子總角動量來自最外層 $5s^1$ 電子的自旋）。第四個量子數 $m_s$ 補齊了 Pauli 的四量子數框架。

### Pauli 矩陣
自旋算符以 **Pauli matrices** 表示，$\mathbf{S} = \frac{\hbar}{2}\boldsymbol{\sigma}$：

$$
\sigma_x = \begin{pmatrix}0&1\\1&0\end{pmatrix}, \quad
\sigma_y = \begin{pmatrix}0&-i\\i&0\end{pmatrix}, \quad
\sigma_z = \begin{pmatrix}1&0\\0&-1\end{pmatrix}
$$

滿足對易關係：

$$
[\sigma_i, \sigma_j] = 2i\,\epsilon_{ijk}\sigma_k, \qquad
\{\sigma_i, \sigma_j\} = 2\delta_{ij} I
$$

$\sigma_z$ 的本徵態 $|\uparrow\rangle = \begin{pmatrix}1\\0\end{pmatrix}$、$|\downarrow\rangle = \begin{pmatrix}0\\1\end{pmatrix}$ 就是自旋兩態——量子計算的量子位元 $|0\rangle, |1\rangle$ 由此而來。

### 反對稱波函數與 Slater 行列式
兩電子總波函數 = 空間部分 × 自旋部分。反對稱性由 Slater 行列式保證：

$$
\Psi(1,2) = \frac{1}{\sqrt{2}}\begin{vmatrix} \psi_a(1) & \psi_b(1) \\ \psi_a(2) & \psi_b(2) \end{vmatrix}
= \frac{1}{\sqrt{2}}\left[\psi_a(1)\psi_b(2) - \psi_b(1)\psi_a(2)\right]
$$

若 $a = b$ 則 $\Psi = 0$——兩電子自動互斥。氦原子基態（兩電子同佔 $1s$）自旋部分必須反對稱（單態 $S=0$），空間部分對稱，正是實驗觀察到的結果。

### Python numpy 演示
```python
import numpy as np

sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)

print("[sx, sy] =", sx @ sy - sy @ sx)        # = 2i sz
print("[sx, sy] = 2i·sz ?", np.allclose(sx@sy - sy@sx, 2j*sz))
print("σ² = 3I ?", np.allclose(sx@sx + sy@sy + sz@sz, 3*np.eye(2)))

up, dn = np.array([1, 0], complex), np.array([0, 1], complex)
print("sz|up> =", sz @ up, " sz|dn> =", sz @ dn)   # 本徵值 ±1 → ms = ±1/2

# 反對稱波函數：兩電子同態 → 為零
def psi2(w1, w2):   # w = (空間函數值, 自旋態)
    return 0.5**0.5 * (w1[0]*w2[1] - w2[0]*w1[1])

s1 = (1.0, up); s2 = (1.0, dn)
print("Ψ(1,2) =", psi2(s1, s2))              # ≈ 0.707·1
print("Ψ(1,1) =", psi2(s1, s1))              # = 0  → 不相容原理！
```

## 結案 -- 後果與影響
- 判決：費米子波函數必須反對稱（Pauli 不相容），電子自旋 $s=\frac{1}{2}$ 是真實的內秉自由度。Stern–Gerlach 之謎、週期表之謎、反常 Zeeman 之謎三案同時告破。
- 週期表結構獲得理論根基 → 化學鍵、原子光譜、物質穩定性全部可計算。
- 1927 年 Pauli 引入自旋矩陣將自旋納入波動力學；1928 年 Dirac 方程使自旋從相對論中自然湧現；1940 年 Pauli 證明自旋–統計定理（半整數自旋 ↔ Fermi–Dirac）。
- 現代應用：量子位元（$|\uparrow\rangle,|\downarrow\rangle$）、Pauli 矩陣作為量子閘、電子簡併壓力支撐白矮星與中子星（否則恆星塌縮成黑洞）。

## 關鍵人物與文獻
- **Wolfgang Pauli**（1900–1958），蘇黎世聯邦理工學院；以「上帝之鞭」的毒舌聞名。
- **George Uhlenbeck**（1900–1988）與 **Samuel Goudsmit**（1902–1978）：提出電子自旋。
- **Otto Stern** 與 **Walther Gerlach**：1922 年實驗。
- W. Pauli, Z. Phys. 31, 765 (1925)（不相容原理）；W. Pauli, Z. Phys. 43, 601 (1927)（自旋矩陣）。
- Pauli 獲 1945 年諾貝爾物理獎（因不相容原理，由 Einstein 提名）。
