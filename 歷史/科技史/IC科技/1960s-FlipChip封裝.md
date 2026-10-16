# 1960s - Flip Chip 倒裝封裝：晶片面向下的革命

## 案件摘要
1964 年，IBM 推出 C4（controlled collapse chip connection）工藝：晶片**面向下**、以焊料凸塊（solder bump）直接接上基板，靠表面張力自我對準。
這是為 System/360 的高可靠性需求而生，解決了打線封裝（wire bond）I/O 數受限與寄生電感的雙重罩門。
這個案子追查的是：封裝如何從「周邊繞線」走向「面積陣列」，為 CPU/GPU 的標準封裝與日後的 2.5D/3D 先進封裝鋪路。

## 前因 -- 為什麼會有這個案子
- **封裝的意義**：裸晶（die）脆弱、怕水氧、散熱差、I/O 無法直接使用——封裝要同時做到**保護、散熱、訊號傳輸、I/O 擴展**四件事。
- **Wire bond 的罩門一：I/O 數**：打線封裝只能沿晶片**周邊**放焊墊（pad），I/O 數 $O(\text{perimeter})$；1960 年代 IBM System/360 的處理器需要數百個 I/O，周邊繞線把 die 邊緣擠爆。
- **Wire bond 的罩門二：寄生電感**：打線是懸空的細金線，電感量約每根 $1\ \text{nH}$ 級。高速開關時的感應雜訊：
$$V = L\,\frac{di}{dt}$$
  當電流切換愈快（$di/dt$ 大）、I/O 愈多，電源與接地彈跳（ground bounce）愈嚴重——雜訊會把邏輯誤觸發。
- **繞線長度**：打線從 pad 繞到基板，長度可達數 mm，訊號延遲與串擾（crosstalk）都與線長成正比。
- **關鍵推理**：若晶片**面向下**、整個 die 表面都可以放 bump，I/O 就從 $O(\text{perimeter})$ 升級為 $O(\text{area})$；bump 高度僅數十微米，電感比打線低一個數量級——電性與密度雙贏，唯一的問題是：焊料熔融後晶片會不會掉？答案出人意料：**不會，它會自己站好**。

## 線索與推理 -- 數學式、程式、理論

### 1. C4 原理：controlled collapse 自我對準

C4 的工序：在 wafer 上每個 pad 蒸鍍/電鍍高鉛焊料凸塊（如 Pb/Sn 97/3，熔點約 315°C），回焊時晶片面向下放在基板對應焊墊上：

```
      Wire bond（傳統）            Flip chip（C4）
   die ── pad                      die ▽ ─ bump ─ bump ─ ▽
          ╲                          ╲│╱  ╲│╱
           ╲ 金線（~1nH, 數mm）       基板（bump ~50um, 電感極小）
            ╲
             基板
```

- **自我對準（self-alignment）**：回焊時焊料熔融成球，**表面張力**把晶片自動拉回與基板焊墊對齊的位置——對位精度可容許 ±50 μm 級誤差，遠低於 wire bond 的 wire bonder 精度需求：
$$\Delta x \;\xrightarrow{\;\text{表面張力}\;}\; 0, \qquad F_{\gamma} = \gamma \,\frac{\partial A}{\partial x} \ \text{（表面張力驅動的最小化自由表面積）}$$
- **controlled collapse**：熔融焊料理論上會讓晶片塌到基板上短路，但焊料凸塊與周圍的**鈍化層限制**（ball-limiting metallurgy, BLM）把焊料「捏」成一個受控的球——晶片懸浮在 bump 之上，不會塌陷。
- 這個物理巧合讓倒裝不需要高精度對位機台，量產成本反而更低。

### 2. I/O 密度：周邊 vs 面積陣列

給定 die 尺寸 $s \times s$、pad/bump 間距 pitch $p$：

- **Wire bond（周邊）**：pad 只能放在四邊，每邊約 $s/p$ 個，扣除角落：
$$N_{\text{wire}} \approx 4\,\frac{s}{p} - 4 \;\propto\; O(\text{perimeter}) = O(s)$$
- **Flip chip（面積陣列）**：bump 鋪滿整個 die 表面：
$$N_{\text{flip}} \approx \left(\frac{s}{p}\right)^2 \;\propto\; O(\text{area}) = O(s^2)$$
- **比值**：$N_{\text{flip}}/N_{\text{wire}} \approx s/(4p)$——die 愈大，面積陣列的優勢呈**平方級**放大。10 mm die、200 μm pitch 時，面積陣列約可放 2,500 個 bump，周邊只能放約 196 個。
- 這個 $O(s)$ vs $O(s^2)$ 的差異，正是現代 CPU/GPU 動輒數千個 I/O 的唯一解方。

### 3. 電性優勢：寄生電感的量化

bump 的電感遠低於打線：

| 封裝互連 | 高度 | 典型電感 L | 典型電阻 |
|---|---|---|---|
| Wire bond | ~2 mm | ~1 nH | ~50 mΩ |
| Flip chip bump | ~50–100 μm | ~0.05–0.1 nH | ~10 mΩ |
| TSV（3D） | ~50 μm（穿晶圓）| ~0.03 nH | ~20 mΩ |

- 電源完整性：$V = L\,di/dt$。若 100 個 I/O 同時切換、每個 $di/dt = 10\ \text{mA/ns}$：
$$V_{\text{wire}} = 100 \times 1\ \text{nH} \times 10\ \text{mA/ns} = 1\ \text{V} \quad\text{（足以誤觸發！）}$$
$$V_{\text{flip}} = 100 \times 0.1\ \text{nH} \times 10\ \text{mA/ns} = 0.1\ \text{V} \quad\text{（可接受）}$$
- 這正是高速訊號（GHz 級 clock、SerDes）非 flip chip 不可的原因——**電感是速度的天花板**。

### 4. Underfill：讓 bump 撐過熱膨脹

矽的熱膨脹係數（CTE，約 $2.6\ \text{ppm/°C}$）與有機基板（約 $17\ \text{ppm/°C}$）相差近 7 倍，溫度循環會對 bump 施加剪應力：

$$\Delta x = \Delta\alpha \cdot \Delta T \cdot \frac{s}{2}, \qquad \tau \propto \frac{G\,\Delta x}{h_{\text{bump}}}$$

- 1990 年代引入 **underfill**（毛細流動的環氧樹脂填滿 bump 間隙），把剪應力均攤到整個面積，bump 的熱循環壽命（如 $N_f \propto \tau^{-2}$，Coffin–Manson 律）提升一個數量級——flip chip 才能在消費性產品的溫度循環下存活。
- 無鉛焊料（2000s，RoHS）與 Cu pillar bump（銅柱凸塊，細間距）是後續的兩次製程升級。

### 5. 此後演進：BGA → CSP → 2.5D/3D

- **BGA（Ball Grid Array, 1990s）**：以焊球陣列取代周邊引腳，把 flip chip 的面積陣列概念帶到**封裝對 PCB** 的層級——I/O 從數百升到數千，成為 CPU/GPU 的標準封裝。
- **CSP（Chip Scale Package）**：封裝尺寸 ≈ 裸晶尺寸，手機記憶體與感測器的最小封裝方案。
- **TSV（Through-Silicon Via）**：矽穿孔直接貫穿晶圓，電感最低（見上表），是 3D 堆疊的關鍵——HBM 記憶體與 3D NAND 都靠它。
- **2.5D/3D 先進封裝**：把多顆 die 用矽中介層（interposer）或直接堆疊（如 TSMC CoWoS、Intel Foveros、台積 SOIC）——這條線延續到〈2020s-Chiplet先進封裝〉，此處不重複展開；重點是：**所有先進封裝的地基，都是 1964 年 IBM 的「晶片面向下」**。

### 6. 量產的經濟學：對位精度與良率

C4 能勝出的另一個原因是**成本結構相反**：

- **Wire bond**：每根線要逐一打（焊線機 speed ~10 線/秒），工時隨 I/O 數線性上升；且 pad 間距縮到 50 μm 以下時金線的球頸（ball neck）成為可靠度極限。
- **Flip chip**：所有 bump 在 wafer 階段**一次鍍上**（電鍍或蒸鍍，整片 wafer 同時加工），回焊也是整批同時——工時幾乎與 I/O 數無關。表面張力自我對準把對位精度需求放寬到 ±50 μm，die bonder 便宜且快。
- **良率帳**：雖然 bump 數多、單點失誤風險高，但 bump 焊點的可靠度（配合 underfill）遠高於打線；失效的 bump 可以用 redundant bump（冗餘凸塊）救回。
- **重定尺度的極限**：bump pitch 微縮到 40 μm 以下時，相鄰 bump 間的微短路（bridging）與電磁耦合抬頭——這條線通向 micro-bump → hybrid bonding（銅銅直接接合，無焊料，間距 <10 μm），是 3D 堆疊的最後一哩。

### 7. Python 實作：I/O 密度——wire bond vs flip chip

```python
def io_count(s_mm, pitch_mm):
    """給定 die 尺寸 s_mm 與 pitch_mm，回傳 wire bond 周邊與 flip chip 面積陣列的最大 I/O"""
    n_side = s_mm / pitch_mm                       # 每邊可放的 pad/bump 數
    io_wire = max(0, 4 * n_side - 4)               # 周邊：扣四角
    io_flip = n_side ** 2                          # 面積陣列：整面鋪滿
    return io_wire, io_flip

print(f"{'die (mm)':>9}{'pitch (mm)':>10}{'wire bond':>10}{'flip chip':>10}{'倍率':>8}")
for s, p in [(5, 0.2), (10, 0.2), (20, 0.15), (20, 0.1)]:
    w, f = io_count(s, p)
    print(f"{s:>9}{p:>10}{w:>10.0f}{f:>10.0f}{f/w:>7.1f}x")
# die (mm) pitch (mm) wire bond flip chip     倍率
#        5        0.2        96       625     6.5x
#       10        0.2       196     2,500    12.8x
#       20        0.15       529    17,778    33.6x
#       20        0.1        796    40,000    50.3x
# die 愈大、pitch 愈細，面積陣列的 I/O 優勢以平方級放大——
# 這正是 CPU/GPU（數千 I/O）必用 flip chip、wire bond 只能退守小晶片的數學原因。

# --- 寄生電感造成的電源彈跳 ---
L_wire, L_bump = 1.0e-9, 0.1e-9   # 電感 (H)：打線 vs bump
di_dt = 10e-3 / 1e-9              # 10 mA/ns
n_io = 100                        # 同時切換的 I/O 數
print(f"\nn_io={n_io}, di/dt=10mA/ns")
print(f"  wire bond: V = {n_io * L_wire * di_dt:.2f} V （誤觸發！）")
print(f"  flip chip: V = {n_io * L_bump * di_dt:.2f} V （可接受）")
# n_io=100, di/dt=10mA/ns
#   wire bond: V = 1.00 V （誤觸發！）
#   flip chip: V = 0.10 V （可接受）
```

## 結案 -- 後果與影響
- **高速晶片的標準封裝**：今日所有高效能 CPU、GPU、FPGA 都用 flip chip；wire bond 退守低價、低 I/O 的小晶片（消費性 IC、部分記憶體）。
- **IBM 的遺產**：C4 從 System/360（1964）一路用到大型主機與 AS/400，IBM 證明了「封裝是效能的一部分」——這個觀念日後成為先進封裝產業的靈魂。
- **BGA 標準化**：1990 年代 BGA 成為 JEDEC 標準，封裝對 PCB 的面積陣列接點讓主機板設計徹底改寫（多層板、盲埋孔皆因 BGA 而生）。
- **為 2.5D/3D 與 Chiplet 鋪路**：flip chip → underfill → Cu pillar → TSV → interposer → 3D 堆疊，這條線直接通向 HBM 與 2020s 的 Chiplet 生態（詳見〈2020s-Chiplet先進封裝〉）。
- **業界競逐**：TSMC（CoWoS、InFO）、Intel（EMIB、Foveros）、Samsung（I-Cube）、ASE/Amkor（先進封裝代工）——先進封裝已是摩爾定律減速後的主要戰場。

## 關鍵人物與文獻
- **L. F. Miller**：IBM，1969 年 "Controlled Collapse Reflow Chip Joining," *IBM J. Res. Dev.*——C4 理論的經典論文。
- **IBM System/360 團隊**：1964 年首次將 C4 用於 Solid Logic Technology（SLT）模組。
- **George Riley / Texas Instruments**：1990 年代 BGA 的推手；JEDEC JESD21 BGA 標準。
- P. Totta & R. Sopher, "SLT Device Metallurgy and Its Manifestations," *IBM J. Res. Dev.*, 1969。
- J. Lau（ed.）, *Flip Chip Technologies*, McGraw-Hill, 1996；Coffin–Manson 疲勞律為焊料可靠度分析的標準工具。
