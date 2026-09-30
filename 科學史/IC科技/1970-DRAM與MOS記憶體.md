# 1970-DRAM與MOS記憶體

## 案件摘要
1970 年 Intel 推出世界第一顆商用半導體記憶體 1103（1024-bit DRAM），用一顆 MOSFET 加一個電容取代磁芯。這場「磁芯殺手」案件宣告了主記憶體半導體時代的來臨，也讓 Intel 從一家新創變成記憶體巨人。

## 前因 -- 為什麼會有這個案子
- 1960 年代主記憶體主流是**磁芯記憶體**（magnetic core memory）：鐵氧體磁環穿線陣列，靠磁化方向儲存 0/1。
- 磁芯的致命傷：體積大、手工繞線、速度慢（微秒級）、難以與 CPU 整合。
- 1966 年 IBM 的 Robert Dennard 發明 1T1C DRAM 儲存胞；1968–69 年 Intel 成立，第一個目標就是「殺死磁芯」。
- 線索：MOSFET 的閘極電容天然就是一個可儲存電荷的容器。

## 線索與推理 -- 數學式、程式、理論

### 磁芯記憶體 vs 半導體記憶體

| 特性 | 磁芯 | DRAM (1103) |
|---|---|---|
| 儲存原理 | 磁化方向 | 電容電荷 |
| 存取時間 | ~1 μs | ~150 ns |
| 密度 | 手工繞線，低 | 光刻製程，高 |
| 揮發性 | 非揮發 | 揮發（需刷新）|
| 可製造性 | 人工，不可擴縮 | 晶圓製程，可按摩爾定律縮放 |

### MOSFET 原理
N 通道 MOSFET 飽和區電流：
$$I_D = \frac{1}{2}\mu_n C_{ox}\frac{W}{L}(V_{GS}-V_{th})^2, \quad C_{ox} = \frac{\varepsilon_{ox}}{t_{ox}}$$
- $V_{GS} > V_{th}$ 時，閘極電場在源漏之間形成反轉層（導電溝道），MOSFET 導通。
- MOSFET 同時是：開關（記憶體存取）、電容閘（儲存）、放大器（感測放大器讀取）——一顆元件三種角色，這正是 DRAM 得以極簡的數學基礎。

### DRAM 儲存胞（1T1C）與刷新
每個位元 = 1 個電晶體（存取閘）+ 1 個電容（儲存）：
- 寫入：位元線加電壓，字元線打開電晶體，電容充/放電。
- 讀取：**破壞性讀取**——電容電荷分享到位元線，讀後必須回寫。
- 儲存的位元電荷 $Q = C \cdot V$，但電容會漏電（結漏電、亞閾值漏電）：
$$\frac{dV}{dt} = -\frac{V}{R_{leak} \cdot C} \;\Rightarrow\; V(t) = V_0\, e^{-t/(R_{leak}C)}$$
- 必須在 $V(t)$ 掉到感測門檻前**刷新**（refresh）：傳統每 64 ms 全部列刷一次。

### SRAM vs DRAM 對照表

| 特性 | SRAM | DRAM |
|---|---|---|
| 儲存胞 | 6T（交叉耦合反相器）| 1T1C |
| 揮發性 | 通電即保持 | 需定期刷新 |
| 速度 | 快（1 ns 級）| 慢（數十 ns）|
| 密度/位元成本 | 低密度、貴 | 高密度、便宜 |
| 用途 | Cache（L1/L2/L3）| 主記憶體 |

### 記憶體階層
速度與成本無法兩全，於是形成金字塔：
```
        CPU 暫存器 (ns 內, 最貴)
       L1/L2/L3 Cache (SRAM)
      主記憶體 (DRAM)
     SSD / 磁碟 (GB-TB, 便宜)
```
階層有效性由**局部性原理**（ locality：時間局部性 + 空間局部性）保證；平均存取時間 $\approx t_{cache} + (1-h)\,t_{DRAM}$（$h$ 為命中率）。

### Python：模擬 DRAM 刷新週期與漏電
```python
import numpy as np
import matplotlib.pyplot as plt

C = 25e-15        # 儲存電容 25 fF
R_leak = 1e10     # 漏電等效電阻 10 GΩ
tau = R_leak * C  # 時間常數
V0, Vth_sense = 1.0, 0.5
t_refresh = 64e-3 # 64 ms 刷新週期

t = np.linspace(0, t_refresh, 500)
V = V0 * np.exp(-t / tau)
ok = V[-1] > Vth_sense
print(f"64ms 後電壓 = {V[-1]:.3f} V，感測門檻 = {Vth_sense} V，可讀取: {ok}")

plt.plot(t*1e3, V, label='V(t) = V0 * exp(-t/RC)')
plt.axhline(Vth_sense, color='r', ls='--', label='sense threshold')
plt.axvline(t_refresh*1e3, color='g', ls=':', label='refresh @ 64ms')
plt.xlabel('Time (ms)'); plt.ylabel('Cell Voltage (V)')
plt.title('DRAM Leakage & Refresh'); plt.legend(); plt.show()
```
時間常數 $\tau = R_{leak}C = 250\ \mu s$ 遠小於 64 ms？——不，漏電模型中多數漏電隨電壓降低而減緩，實際晶片靠足夠大的 $C$ 與低漏電製程把保持時間撐過 64 ms；若模擬顯示不可讀，就必須縮短刷新週期（如 32 ms），這正是製程演進中 DRAM 設計的核心取捨。

## 結案 -- 後果與影響
- Intel 1103（1970，1024-bit，$0.01/\text{bit}$ 級成本）在 1972 年成為全球銷量最大的半導體元件，磁芯記憶體在數年內絕跡。
- DRAM 沿摩爾定律成長：1K → 4K → 16K → … → 今日單晶 16 Gb+，每 18–24 個月密度翻倍。
- 奠定記憶體階層架構，成為馮紐曼機器 bottlenecks 的標準解法。
- Intel 1980 年代被日本 DRAM 廠逼退而轉型微處理器——DRAM 市場的興衰本身就是半導體地緣政治史。

## 關鍵人物與文獻
- **Robert Dennard**：IBM，1966 年發明 1T1C DRAM（專利 US 3,387,286）。
- **Ted Hoff / Federico Faggin / Les Vadasz**：Intel 1103 團隊。
- D. Kahng & S.M. Sze, "A floating gate and its application to memory devices," *Bell Syst. Tech. J.*, 1967.
- Intel 1103 datasheet（1970）。
