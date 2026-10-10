# 1924-BoseEinstein 統計

## 案件摘要
1924 年，印度無名物理學家 Satyendra Nath Bose 以「光子計數」新方法重新推導 Planck 黑體輻射定律，論文被拒後寄給 Einstein。Einstein 親自翻譯成德文並推薦發表，再推廣到物質粒子，預言 70 年後才證實的 Bose–Einstein 凝聚。一個新的統計力學王國就此誕生。

## 前因 -- 為什麼會有這個案子
- 1900 年 Planck 以「絕望之舉」湊出黑體輻射定律，但他的推導混合了經典與量子邏輯，邏輯根基可疑。
- Einstein 1905 年的光量子假說仍有爭議：光是粒子還是波？
- Bose 的洞察：Planck 定律的關鍵不在輻射本身，而在**光子的統計計數方式**——把每個能態的佔據數當成獨立自由度。
- 當時 Maxwell–Boltzmann 統計是唯一標準，它假設粒子可分辨。

## 線索與推理 -- 數學式、程式、理論

### Bose 的光子計數推導
Bose 將相空間（動量 $\mathbf{p}$，體積 $V$）劃分為體積 $h^3$ 的相格，每格對應一個量子態。動量在 $p$ 到 $p+dp$ 之間的態數（含兩個偏振）：

$$
g(p)\,dp = \frac{2 \cdot 4\pi p^2 V\,dp}{h^3}
$$

將 $p = h\nu/c$ 代入，得到頻率 $\nu$ 附近每單位頻率的態數 $g(\nu) = \frac{8\pi V \nu^2}{c^3}$。

關鍵一步：Bose 把 $N_\nu$ 個光子分配到 $g_\nu$ 個相格中，**光子不可分辨、每格可容納任意多個光子**。將 $N_\nu$ 個相同光子與 $g_\nu-1$ 個隔板排成一列的方法數：

$$
W = \frac{(N_\nu + g_\nu - 1)!}{N_\nu!\,(g_\nu-1)!}
$$

配合理論極大化（$W$ 最大）並以 $\bar{n} = N_\nu/g_\nu$ 表示平均佔據數，Bose 得到：

$$
\bar{n} = \frac{1}{e^{h\nu/kT} - 1}
$$

再乘上 $g(\nu)\cdot h\nu$，立即得到 Planck 定律：

$$
u(\nu)\,d\nu = \frac{8\pi h \nu^3}{c^3}\frac{d\nu}{e^{h\nu/kT}-1}
$$

**整個推導完全沒有經典電磁學，純粹是計數**——這說明 Planck 定律的本質是光子的統計性質。

### 三種量子統計
Einstein 將此方法推廣到理想氣體，得到 **Bose–Einstein 統計**。後來 Dirac/Fermi 加入 Pauli 不相容限制，得到 **Fermi–Dirac 統計**：

$$
\text{BE:}\quad \bar{n}_i = \frac{1}{e^{(\epsilon_i-\mu)/kT}-1}
\qquad
\text{FD:}\quad \bar{n}_i = \frac{1}{e^{(\epsilon_i-\mu)/kT}+1}
$$

| 統計 | 粒子類型 | 自旋 | 每態佔據 | 分母 |
|---|---|---|---|---|
| Maxwell–Boltzmann | 可分辨經典粒子 | 任意 | 無限制 | 無量子修正，$\bar{n}_i = e^{-(\epsilon_i-\mu)/kT}$ |
| Bose–Einstein | 玻色子 | 整數（0,1,2,…） | 無限制 | $e^{(\epsilon_i-\mu)/kT}-1$ |
| Fermi–Dirac | 費米子 | 半整數（1/2, 3/2,…） | 最多 1 個 | $e^{(\epsilon_i-\mu)/kT}+1$ |

高溫低密度時三者趨於一致；低溫高密度時 BE 有凝聚、FD 有 Fermi 面。

### Bose–Einstein 凝聚 (BEC) 預言
Einstein 1925 年發現：對理想玻色氣體，當溫度低於臨界溫度 $T_c$ 時，基態佔據數劇增：

$$
T_c = \frac{2\pi\hbar^2}{mk}\left(\frac{n}{\zeta(3/2)}\right)^{2/3}
$$

巨量粒子「凝聚」進同一量子態，形成宏觀量子波。1995 年 Cornell、Wieman（銣-87）與 Ketterle（鈉）在冷原子氣體中製成 BEC，溫度約 170 nK，證實 70 年前的預言，三人獲 2001 年諾貝爾獎。

### 自旋與統計的關係
- 整數自旋 → Bose–Einstein 統計；半整數自旋 → Fermi–Dirac 統計。
- 這一「自旋–統計定理」由 Pauli (1940) 以相對論性量子場論證明，是量子力學與相對論結合的深刻結果。

### Python 驗證三種統計
```python
import numpy as np

kT = 1.0                          # 以 kT 為單位
mu = 0.0
eps = np.linspace(0.05, 5, 500)

n_BE = 1 / (np.exp((eps - mu)/kT) - 1)
n_FD = 1 / (np.exp((eps - mu)/kT) + 1)
n_MB = np.exp(-(eps - mu)/kT)

print(f"ε=0.05kT: BE={n_BE[0]:.2f}  FD={n_FD[0]:.2f}  MB={n_MB[0]:.2f}")
print(f"ε=5.0kT : BE={n_BE[-1]:.4f} FD={n_FD[-1]:.4f} MB={n_MB[-1]:.4f}")
# 高能區三者趨同；ε→0 時 BE 發散（凝聚前兆），FD 封頂為 1
```

## 結案 -- 後果與影響
- 判決：量子統計有三種，粒子不可分辨性是量子世界的根本特徵；光的統計性質即 Planck 定律之源。
- 玻色子（光子、介子、He-4、膠子）與費米子（電子、質子、中微子）的世界自此分野，與 Pauli 不相容原理互為表裡。
- BEC 成為超流、超導理論的概念基礎；雷射（光子大量佔據同一模式）本質上就是光的「凝聚」近親。
- 現代應用：BEC 原子干涉儀、量子模擬、宇宙學中的 Bose 氣體模型。

## 關鍵人物與文獻
- **Satyendra Nath Bose**（1894–1974），達卡大學；「boson」即以其名命名。
- **Albert Einstein**（1879–1955）：翻譯並推薦 Bose 論文，再推廣至物質。
- S. N. Bose, *Planck's Law and the Light Quantum Hypothesis*, Z. Phys. 26, 178 (1924).
- A. Einstein, *Quantentheorie des einatomigen idealen Gases*, Sitzungsber. Preuss. Akad. Wiss. (1924, 1925).
- W. Pauli, *The Connection Between Spin and Statistics*, Phys. Rev. 58, 716 (1940).
