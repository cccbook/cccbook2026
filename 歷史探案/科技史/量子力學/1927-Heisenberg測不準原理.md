# 1927 — Heisenberg 測不準原理

## 案件摘要
1927 年 3 月，Heisenberg 在論文〈Über den anschaulichen Inhalt...〉中提出：粒子的位置與動量**無法同時精確確定**，乘積下界為 $\hbar/2$。這不是儀器不夠好的問題，而是自然定律——這一原理成為量子力學與經典世界的分水嶺。

## 前因 -- 為什麼會有這個案子
- 1925–26 年量子力學（矩陣力學、波動力學）成立，但「電子在軌道上的位置」變得不可言說。
- Heisenberg 需要解釋：為什麼矩陣力學中 $x$ 與 $p$ **不對易**（$xp - px = i\hbar$），物理上代表什麼。
- Pauli 曾思考 γ 射線顯微鏡；Heisenberg 在哥本哈根與 Bohr 長夜辯論（兩人甚至吵到哭了），最後在 Bohr 去挪威滑雪期間寫下這篇論文。

## 線索與推理 -- 數學式、程式、理論

### 線索一：γ 射線顯微鏡思想實驗
想「看見」電子的位置，必須用光去照它。光子波長 $\lambda$ 越短，顯微鏡解析度越高：

$$\Delta x \approx \frac{\lambda}{\sin\theta}$$

但光子撞擊電子時透過 Compton 效應傳遞動量，反衝動量不確定量：

$$\Delta p \approx \frac{h}{\lambda}\sin\theta$$

兩式相乘：$\Delta x\,\Delta p \approx \frac{\lambda}{\sin\theta} \cdot \frac{h\sin\theta}{\lambda} = h$。**照得越清楚，擾動越大**——測量行為本身把不確定性寫進了結果。

### 線索二：測不準原理
**Heisenberg 不等式**（Kennard 1927 給出嚴格證明）：

$$\Delta x\,\Delta p \geq \frac{\hbar}{2}$$

其中標準差定義為 $\Delta x = \sqrt{\langle x^2\rangle - \langle x\rangle^2}$。注意下界 $\hbar/2 \approx 5.27\times 10^{-35}\,\text{J·s}$——這是自然常數，與測量技術無關。

### 線索三：用 Fourier 變換證明（位置波包越窄動量越寬）
波動力學中，位置波函數 $\psi(x)$ 與動量空間波函數 $\phi(p)$ 互為 Fourier 變換對：

$$\phi(p) = \frac{1}{\sqrt{2\pi\hbar}}\int e^{-ipx/\hbar}\,\psi(x)\, dx$$

Fourier 分析的基本定理：函數與其 Fourier 變換的寬度**乘積有下界**（時間-頻率不確定性 $\Delta t\,\Delta\omega \geq \frac{1}{2}$ 的推論）。代入 $p = \hbar k$ 即得 $\Delta x\,\Delta p \geq \frac{\hbar}{2}$。

- **高斯波包**是唯一達到下界的極小不確定態：$\psi(x) \propto e^{-x^2/4\sigma^2}$，其 Fourier 變換仍是高斯。
- 波包壓縮（$\sigma$ 變小）→ 動量空間展寬（$\Delta p \sim \hbar/2\sigma$）——「魚與熊掌不可兼得」的數學形式。

### 線索四：一般化的 Robertson 不等式
Heisenberg 的特殊結果可推廣到**任意兩個可觀測量** $A$、$B$（Robertson 1929）：

$$\Delta A\,\Delta B \geq \frac{1}{2}\left|\langle[A,B]\rangle\right|, \qquad [A,B] = AB - BA$$

對 $A = x$、$B = p$：$[x,p] = i\hbar$，還原為原式。對**能量-時間**：

$$\Delta E\,\Delta t \geq \frac{\hbar}{2}$$

（注意：時間在量子力學中不是算符，此式需以「演化速率」詮釋：狀態特徵變化越快的系統，其能量越不確定——例如壽命 $\Delta t$ 短的不穩定粒子，能階寬度 $\Delta E$ 大。）

### 程式碼範例：Python numpy 模擬高斯波包的寬度反比關係
```python
import numpy as np
import matplotlib.pyplot as plt

hbar = 1.0
x = np.linspace(-20, 20, 2048)

sigmas = np.array([0.3, 0.5, 1.0, 2.0, 4.0])
fig, ax = plt.subplots(1, 2, figsize=(11, 4))
results = []

for s in sigmas:
    psi = np.exp(-x**2 / (4 * s**2))          # 位置高斯波包
    psi /= np.sqrt(np.trapz(np.abs(psi)**2, x))  # 歸一化
    dx = x[1] - x[0]
    P = np.abs(psi)**2
    x_mean = np.trapz(x * P, x)
    Dx = np.sqrt(np.trapz((x - x_mean)**2 * P, x))

    # 動量空間：Fourier 變換
    k = np.fft.fftfreq(len(x), dx) * 2 * np.pi
    phi = np.fft.fftshift(np.fft.fft(psi))
    Pp = np.abs(phi)**2; Pp /= np.trapz(Pp, k)
    p_mean = np.trapz(k * Pp, k)
    Dp = np.sqrt(np.trapz((k - p_mean)**2 * Pp, k))

    results.append((s, Dx, Dp, Dx * Dp))
    ax[0].plot(x, P, label=f"Δx={Dx:.2f}")
    ax[1].plot(k, Pp, label=f"Δp={Dp:.2f}")

print("σ      Δx      Δp     Δx·Δp  (下界 hbar/2 = 0.5)")
for r in results:
    print(f"{r[0]:.1f}  {r[1]:.3f}  {r[2]:.3f}  {r[3]:.5f}")

ax[0].set_title("位置空間：波包越窄"); ax[0].legend()
ax[1].set_title("動量空間：Fourier 展寬"); ax[1].legend()
plt.tight_layout(); plt.show()
```

輸出顯示：$\sigma$ 從 0.3 增到 4.0 時，$\Delta x$ 變大、$\Delta p$ 變小，且 $\Delta x\,\Delta p \approx 0.5 = \hbar/2$ **恆等於下界**——高斯波包正是極小不確定態。

## 結案 -- 後果與影響
- 「電子軌道」正式從物理學中除名：沒有同時確定的位置與動量，就沒有軌道。
- 哥本哈根詮釋的支柱之一：量子力學只能預言機率分佈（見 1927 Solvay 會議）。
- 成為 EPR 悖論（1935）的攻防焦點：Einstein 試圖用「同時測量」攻擊，最終由 Bell 不等式實驗裁決。
- 深遠影響：量子場論的真空漲落、Casimir 效應、量子光學的壓縮光（squeezed light）、LIGO 的量子極限測量，全部以測不準原理為基石。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Werner Heisenberg | 提出測不準原理，1932 諾貝爾獎 |
| Niels Bohr | 互補原理，與 Heisenberg 辯論並修正其詮釋 |
| Earle Kennard | 給出 $\hbar/2$ 下界的嚴格證明 |
| Howard Robertson | 一般化為對易子不等式 |

- W. Heisenberg, Über den anschaulichen Inhalt der quantentheoretischen Kinematik und Mechanik, Z. Phys. **43**, 172 (1927)。
- E. H. Kennard, Z. Phys. **44**, 326 (1927)。
- H. P. Robertson, Phys. Rev. **34**, 163 (1929)。
