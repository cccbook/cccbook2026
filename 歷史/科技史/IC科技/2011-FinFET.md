# 2011 - FinFET（Intel 22nm 三維電晶體量產）

## 案件摘要
2011 年 4 月，Intel 宣布 22nm 製程（Ivy Bridge）量產世界首款 FinFET——閘極從「趴在」通道上變成「三面包夾」通道。這是平面 MOSFET 統治 50 年後的第一次結構革命，幕後推理者是 Berkeley 的胡正明教授（1999 年發明）。

## 前因 -- 為什麼會有這個案子
- 平面 MOSFET 通道長度微縮到 30nm 以下，**短通道效應**（short channel effect）失控：閘極對通道的控制力被源/汲極「搶走」。
- 後果是漏電流 $I_{off}$ 暴增：即使閘極關閉，電流仍從源極流向汲極。晶片靜態功耗（leakage power）在 90nm~65nm 世代逼近甚至超過動態功耗。
- DIBL（Drain-Induced Barrier Lowering）：汲極電壓把源極端的位能障壁拉低，等於閘極失效一部分。
- 傳統對策（縮薄閘氧化層、halo doping、SOI）只能延緩，無法根治。需要**結構性**解法：讓閘極電場從四面八方包住通道。

## 線索與推理 -- 數學式、程式、理論

### 1. 短通道效應與漏電流的物理
平面 MOSFET 的次臨界漏電流（subthreshold leakage）：

$$I_{off} = I_0 \cdot e^{-qV_{th}/nkT}$$

關鍵指標是**次臨界擺幅（Subthreshold Slope, SS）**：閘極電壓每改變多少，電流才變化一個數量級：

$$SS = n\,\frac{kT}{q}\ln 10 \approx n \cdot 59.6 \,\text{mV/decade}\quad (T=300K)$$

其中 $n = 1 + \dfrac{C_{dep}}{C_{ox}}$ 是體效應因子。**平面電晶體的物理極限是 $SS \geq 60$ mV/dec**：因為 $C_{dep}$ 無法為零——閘極電場有一部分浪費在「穿透基板」上，控制不到通道表面。

DIBL 的量化描述：

$$\Delta V_{th} = -\lambda_{DIBL} \cdot V_{DS}$$

$\lambda_{DIBL}$ 隨 $L$ 指數惡化（$\propto e^{-L/\lambda}$），這就是「越縮越漏」的數學根源。

### 2. 胡正明與 FinFET 的發明（1999）
1999 年，UC Berkeley 胡正明（Chenming Hu）團隊（與 Tsu-Jae King、Jeffrey Bokor）提出兩種解法：
- **FinFET**：通道是一片垂直的「鰭」（fin），閘極像鞍座般跨上去，從左右兩側＋頂面包夾通道。
- **UTB-SOI（Ultra-Thin-Body SOI）**：超薄基板（<10nm），讓 $C_{dep}$ 趨近零。

FinFET 的核心推理：讓「閘控的自然終止面」由結構決定——通道厚度即矽體厚度，$t_{Si} \lesssim L/3$ 時，DIBL 幾乎消失。等效地：

$$n = 1 + \frac{C_{dep}}{C_{ox}} \to 1 \quad\Rightarrow\quad SS \to 60 \,\text{mV/dec}$$

閘控能力以「電容比」衡量：FinFET 使有效 $C_{ox}$ 增大（雙面通道），$g_m = \dfrac{\partial I_D}{\partial V_G}$ 提升，同電壓下驅動電流更強，或同電流下電壓更低、功耗更省。

### 3. 3D 閘極包覆與閘控能力
| 面向 | 平面 MOSFET | FinFET |
|------|-------------|--------|
| 閘極包覆 | 單面（上方） | 三面（左右＋上） |
| 通道方向 | 水平面內 | 垂直鰭片 |
| 矽體厚度 | 由摻雜 junction 決定（不可控） | 由 fin 蝕刻決定（可控，$t_{Si}\sim$ 數 nm） |
| DIBL | 嚴重（$L<30$nm） | 幾乎消除 |
| $I_{off}$ | 指數暴增 | 低 1~2 個數量級以上 |
| 驅動電流 | 單通道寬度 | 多 fin 並聯 $W_{eff} = 2H_{fin} + W_{fin}$ |
| SS | $\geq 60$ mV/dec（難逼近） | 可達 ~65-70 mV/dec 實用量產 |
| 量化寬度 | 連續 | 以 fin 數量化（2-fin/3-fin 模組） |

### 4. 量產之路：Intel 22nm（2011）
- Intel 在 22nm 世代採用 FinFET（官方名 Tri-Gate），搭配 high-k 金屬閘（HKMG，45nm 已導入）。
- 量產難點：fin 蝕刻的均勻度、fin 端的源/汲磊晶（selective epitaxy）、閘極對 fin 的應力與開關路徑（gate cut）。
- 台積電於 16nm（2014~2015）、三星於 14nm 跟進，FinFET 統治 16nm~10nm~7nm 三個世代近十年。

### 5. GAA（Gate-All-Around）奈米片（2020s）
推理的下一步：三面包夾仍不夠？那就**四面包夾**。把鰭「躺平」切成一片片水平奈米片（nanosheet），閘極完全環繞：

$$n \to 1 \;\text{(極限)},\quad W_{eff} = 4 \times W_{sheet} \;\text{(每片)}$$

- Samsung 3nm（2022）率先量產 GAA；台積電 N2（2025~）採用 GAA 奈米片。
- GAA 使寬度可連續調整（stacked sheets 寬度可調），恢復了 FinFET 失去的設計彈性。

### 6. Python：畫出短通道漏電 vs 閘控示意

```python
import numpy as np
import matplotlib.pyplot as plt

kT_over_q = 0.02585          # 300K 的 kT/q (V)

def id_sub(vg, vth, ss_mv, n_norm=1.0):
    """次臨界電流（正規化），SS 由體效應因子 n 決定"""
    n = ss_mv / 59.6         # SS = n * kT/q * ln10
    return n_norm * np.exp((vg - vth) / (n * kT_over_q)) / np.exp(0)

vg = np.linspace(-0.4, 0.6, 400)
planar = id_sub(vg, 0.3, 100)   # 平面：SS=100mV/dec（短通道惡化）
fin    = id_sub(vg, 0.3, 70)    # FinFET：SS=70mV/dec，接近 60 極限

plt.semilogy(vg, planar, label='Planar (SS=100 mV/dec)')
plt.semilogy(vg, fin,    label='FinFET (SS=70 mV/dec)')
plt.axvline(0.3, ls='--', c='gray', label='Vth=0.3V')
plt.axhline(1e-12, ls=':', c='r', label='Ioff 目標')
plt.xlabel('V_G (V)'); plt.ylabel('I_D (norm., log scale)')
plt.title('Subthreshold leakage: FinFET vs Planar')
plt.legend(); plt.grid(True, which='both', alpha=0.3)
plt.show()

# 同一 Vth 下，Vg=0.3V（關閉）時的漏電比：
print(f"FinFET 漏電 / 平面漏電 = {fin[100]/planar[100]:.2e}")
# (1/70 - 1/100 的指數差) → FinFET 漏電低約 2.5 個數量級
```

## 結案 -- 後果與影響
- FinFET 讓摩爾定律多活了十年（22nm → 3nm），漏電流危機解除，行動裝置功耗驟降。
- 胡正明被譽為「FinFET 之父」，其兩篇 1999/2000 年論文是 21 世紀微縮的聖經。
- 製造結構從 2D 轉 3D，催生蝕刻、磊晶、選擇性沉積的新一代設備產業（Lam、AMAT、ASML）。
- GAA 奈米片接棒（Samsung 3nm、TSMC N2），證明「讓閘極包覆最大化」的推理路線仍是微縮的主旋律；下一站或是 CFET（堆疊 NMOS/PMOS）。

## 關鍵人物與文獻
- 胡正明（Chenming Hu）、Tsu-Jae King、Jeffrey Bokor：FinFET 發明（UC Berkeley, 1999）。
- D. Hisamoto et al., "FinFET—a Self-Aligned Double-Gate MOSFET Scalable to 20 nm," IEEE Trans. Electron Devices (2000)。
- X. Huang et al., "Sub 50-nm FinFET: PMOS," IEDM (1999)。
- Intel，Tri-Gate transistor 22nm 量產宣告（2011）。
- Y. Taur、T. Ning：《Fundamentals of Modern VLSI Devices》——短通道效應與 SS 的理論經典。
