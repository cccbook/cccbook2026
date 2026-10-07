# 1911 - Rutherford 原子模型

## 案件摘要
1911 年，Rutherford 由 α 粒子散射實驗的「不可思議」大角度散射，推理出原子中央有一個微小、帶正電、幾乎含全部質量的**原子核**——棗糕模型就此崩塌，核式原子誕生。

## 前因 -- 為什麼會有這個案子
- **1897 年 Thomson** 發現電子，原子必須有內部結構。
- **Thomson 棗糕模型（1904）**：原子是半徑約 $10^{-10}$ m 的均勻正電球，電子如葡萄乾嵌在其中。
- 棗糕模型的**問題**：正電荷均勻分散，電場處處微弱，α 粒子穿過時只會小角度偏折——理論預測大角度散射的機率小到「不可能」。
- Rutherford 想用 α 散射檢驗棗糕模型，沒想到檢驗出一場革命。

## 線索與推理 -- 數學式、程式、理論

### 線索：Geiger–Marsden 實驗（1908–1909）
**裝置**：α 粒子（來自鐳衰變，$E_\alpha \approx 5\,\text{MeV}$）射向金箔（厚度約 400 nm，僅數千層原子），以螢光屏觀測散射角分佈。

**驚人結果**：
1. 絕大多數 α 粒子直線穿過（小角度散射 < 1°）。
2. **約 1/8000 的 α 粒子被散射到 > 90°**，甚至有粒子被**彈回來**！

Rutherford 的名言：「這就像你對著一張衛生紙發射 15 吋砲彈，砲彈卻彈回來打到你——簡直不可思議。」

### 推理一：只有「強而集中的正電荷」能造成大角度散射
大角度散射需要極強的庫侖排斥力。若正電荷均勻分佈在 $R \sim 10^{-10}$ m 的球內，α 粒子在原子內受到的力被電荷遮蔽，最大偏折角估算只有約 $0.02°$——完全無法解釋。

若正電荷集中在半徑 $r_N$ 的核心，α 粒子接近核心時勢能可達

$$
U = \frac{1}{4\pi\epsilon_0}\frac{Z_1 Z_2 e^2}{r_N}
$$

要能讓 $E_\alpha = 5\,\text{MeV}$ 的 α 粒子調頭，需 $r_N \lesssim 10^{-14}$ m——**比原子小一萬倍**。這就是原子核。

### 推理二：Rutherford 散射公式
Rutherford 推導了 α 粒子在庫侖斥力下的散射角分佈（微分截面）：

$$
\frac{d\sigma}{d\Omega} = \left(\frac{Z_1 Z_2 e^2}{16\pi\epsilon_0 E}\right)^2 \csc^4\!\left(\frac{\theta}{2}\right)
$$

其中 $Z_1 = 2$（α 粒子）、$Z_2 = 79$（金）、$E$ 為 α 粒子動能。

**三個可檢驗的預測**：
1. $d\sigma/d\Omega \propto \csc^4(\theta/2)$，即大角散射 $\propto 1/\sin^4(\theta/2)$——在 150° 的散射機率是 15° 的約 $10^4$ 分之一，實驗完全吻合。
2. $d\sigma/d\Omega \propto Z_2^2$（靶電荷平方）——改變靶材吻合。
3. $d\sigma/d\Omega \propto 1/E^2$——改變 α 能量吻合。
4. 薄箔中多層散射機率 $\propto t$（厚度）。

**幾何關係**（碰撞參數 $b$ 與散射角 $\theta$）：

$$
b = \frac{Z_1 Z_2 e^2}{8\pi\epsilon_0 E} \cot\!\left(\frac{\theta}{2}\right)
$$

大角度對應小碰撞參數 $b \to 0$——α 粒子「正中」原子核。

### 程式驗證：散射角分佈模擬

```python
import numpy as np
import matplotlib.pyplot as plt

k = 8.988e9; e = 1.602e-19
Z1, Z2 = 2, 79                      # alpha, gold
E = 5e6 * e                          # 5 MeV
b0 = Z1*Z2*e**2*k / (2*E)            # 特徵長度

# 以蒙地卡羅取碰撞參數，計算散射角
N = 200000
b = b0 * 10 * np.sqrt(np.random.rand(N))   # 均勻面積分佈
theta = 2*np.arctan(b0/b)                  # b -> theta 幾何關係

plt.figure(figsize=(7,5))
plt.hist(np.degrees(theta), bins=200, log=True, color='steelblue')
plt.axvline(90, ls='--', c='r')
plt.xlabel(r'scattering angle $\theta$ (deg)'); plt.ylabel('counts (log)')
plt.title(f'Rutherford scattering: {np.sum(theta>np.radians(90))/N*1e4:.0f} '
          f'per 10000 scattered beyond 90 degrees')
plt.show()

# csc^4 定律檢驗
th = np.radians(np.linspace(10, 150, 50))
ds = (Z1*Z2*e**2*k/(4*E))**2 / np.sin(th/2)**4
plt.loglog(np.degrees(th), ds, 'o-')
plt.xlabel(r'$\theta$ (deg)'); plt.ylabel(r'$d\sigma/d\Omega$')
plt.title(r'$\propto \csc^4(\theta/2)$: slope = -4 on log-log in $\sin(\theta/2)$')
plt.show()
```

執行結果：大部分粒子小角度穿過，極少數（約萬分之一）大於 90°；$d\sigma/d\Omega$ 服從 $\csc^4$ 律，與 Geiger–Marsden 數據一致。

### 結案推理：核式原子模型
1911 年 Rutherford 發表核式原子：

- 原子中央是**原子核**：半徑 $\sim 10^{-14}$ m，帶正電 $+Ze$，含幾乎全部質量。
- 電子在核外 $\sim 10^{-10}$ m 的空間中運動（「像行星繞太陽」）。
- 原子內部**幾乎是空的**——所以大多數 α 粒子直線穿過。

## 結案 -- 後果與影響
- 棗糕模型結案；核式原子成為一切原子物理的基礎。
- **不穩定性的難題**：經典電磁理論要求繞核加速的電子輻射能量（Larmor 公式 $\frac{dE}{dt} = -\frac{e^2 a^2}{6\pi\epsilon_0 c^3}$），電子會在約 $10^{-11}$ 秒內螺旋墜入原子核——原子不應存在！這個懸念為 **Bohr 1913 量子化模型鋪路**。
- 中子（Chadwick 1932）補齊核內結構；核式模型開啟核物理、核能時代。
- Rutherford 散射至今是材料分析（RBS）與高能物理（盧瑟福散射 → Rutherford 地道實驗傳統）的基礎。

## 關鍵人物與文獻
- **E. Rutherford**：Phil. Mag. 21, 669 (1911)〈α 與 β 粒子被物質散射...〉；諾貝爾化學獎 1908（放射性的早期工作）。
- **H. Geiger & E. Marsden**：Proc. R. Soc. A 82, 495 (1909)。
- **J. J. Thomson**：棗糕模型，Phil. Mag. 7, 237 (1904)；諾貝爾獎 1906（電子）。
