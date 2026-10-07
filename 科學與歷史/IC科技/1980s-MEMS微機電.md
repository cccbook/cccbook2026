# 1980s - MEMS 微機電：當矽學會了動作

## 案件摘要
1982 年，Kurt Petersen 發表經典論文 "Silicon as a Mechanical Material"，宣告矽不只是電子材料，也是優異的機械材料。
1980 年代，bulk 與 surface micromachining 兩條微加工路線成熟，MEMS（微機電系統）正式成形。
這個案子追查的是：半導體產業如何跨界機械——把感測器、致動器、微鏡片做進晶片，最終讓汽車安全氣囊與智慧手機感測器成為標配。

## 前因 -- 為什麼會有這個案子
- **壓力感測器的先行者**：1960 年代已有用矽壓阻效應（piezoresistivity）做的壓力感測器（Honeywell、NovaSensor），證明矽可以「有感覺」。
- **半導體製程是現成的工具箱**：光刻、蝕刻、薄膜沉積、摻雜——這些為電晶體開發的技術，天然就能拿來刻出微小的懸臂梁與薄膜。
- **矽的機械性質被低估**：單晶矽的楊氏係數 $E \approx 170\ \text{GPa}$（接近不鏽鋼）、無塑性變形、無疲勞、抗拉強度高於多數金屬——卻長期只被當電子材料。
- **汽車業的催生**：1980 年代美國立法要求安全氣囊（FMVSS 208），需要**便宜、可靠、可量產**的碰撞加速度感測器——機械式開關太貴，於是 MEMS 加速度計被逼上檯面。
- **關鍵推理**：用半導體量產方式做機械件，成本隨**面積**縮小而非隨精度上升——這是把機械感測器從精密儀器變成消費性晶片的關鍵一步。

## 線索與推理 -- 數學式、程式、理論

### 1. 矽作為機械材料（Petersen, 1982）

Petersen 系統整理了單晶矽的機械參數，與常見金屬對照：

| 材料 | 楊氏係數 E (GPa) | 密度 (g/cm³) | 屈服強度 |
|---|---|---|---|
| 單晶矽 Si | ~170（[100] 向）| 2.33 | 極高（無塑性區）|
| 不鏽鋼 | ~200 | 7.9 | 有疲勞 |
| 鋁 | ~70 | 2.7 | 有疲勞 |

- 矽的 $E/\rho$ 比值高 → 諧振頻率高、適合做高頻感測。
- 矽無塑性變形與疲勞 → MEMS 結構可振動 **10⁹ 次以上**不失效——這是「可靠」的物理根據。

### 2. 微加工的兩條路線

- **Bulk micromachining（體蝕刻）**：從晶圓背面用異向性蝕刻（KOH、EDP）蝕穿，利用〈100〉與〈111〉晶向蝕刻速率差（約 400:1）刻出 V 型溝槽與薄膜——壓力感測器的經典做法。
- **Surface micromachining（表面薄膜）**：在晶圓表面交替沉積**犧牲層**（sacrificial layer, 如 PSG）與結構層（polysilicon），蝕掉犧牲層後懸空結構自然浮現——ADXL 加速度計與 DLP 微鏡的路線。1980s Berkeley 的 polysilicon surface micromachining 是關鍵推手。
- **LIGA**（德文 Lithographie, Galvanoformung, Abformung）：X 光深度光刻＋電鑄＋模鑄，可做出數百微米高的高深寬比金屬結構——體積較大但精度極高。

### 3. 懸臂梁與質量彈簧系統：MEMS 的基本數學

加速度計的核心是質量—彈簧—阻尼系統：質量塊 $m$（可動）、懸臂梁（彈簧常數 $k$）、空氣阻尼 $c$。

懸臂梁（長 $l$、寬 $w$、厚 $t$）的等效彈簧常數（末端集中負載）：

$$k = \frac{E\,w\,t^3}{4\,l^3}$$

系統的諧振頻率：

$$f_0 = \frac{1}{2\pi}\sqrt{\frac{k}{m}}, \qquad m = \rho\,w\,t\,l \ \text{（質量塊體積 × 密度）}$$

- 加速度 $a$ 產生的慣性力 $F = ma$，位移 $x = F/k$。**靈敏度**：
$$\frac{x}{a} = \frac{m}{k} \;\Rightarrow\; \text{靈敏度} \propto \frac{m}{k} = \frac{4\rho\,l^4}{E\,t^2}$$
- 取捨浮現：靈敏度要 $m/k$ 大，頻寬要 $f_0$ 高（即 $k/m$ 大）——**靈敏度與頻寬互為倒數**。安全氣囊需數百 Hz 頻寬，導航級感測器可換取更高靈敏度。

### 4. 感測的方式：壓阻 vs 電容

- **壓阻式**：懸臂梁根部摻雜壓阻，梁彎曲時電阻變化 $\Delta R/R \approx \pi_{44}\,\sigma$（$\pi_{44}$ 為矽的剪切壓阻係數）。簡單但溫度漂移大。
- **電容式**：質量塊與固定電極間的電容 $C = \varepsilon A / d$，位移改變間隙 $d$：
$$\frac{\Delta C}{C} \approx \frac{\Delta d}{d} = \frac{m a}{k\,d}$$
  無溫度漂移、可做差動（兩個電極相減）抵消共模誤差——ADXL 系列採用此路線。

### 5. 案件現場：ADXL50（Analog Devices, 1991）

第一顆量產的 MEMS 加速度計 ADXL50，把**機械結構與量測電路做在同一顆晶片上**（monolithic integration）：

```
    固定齒 ──  ──  可動齒（質量塊伸出）
              ╲╱    形成 ± 電容
    固定齒 ──  ──  可動齒
       ↑ 加速度 → 質量塊位移 → 差動電容變化 → 片上解調 → 電壓輸出
```

- 量測範圍 ±50 g，頻寬 ~1 kHz，正好命中安全氣囊觸發需求。
- **MEMS 與 CMOS 整合**：surface micromachining 的結構層（polysilicon）可與 CMOS 前段製程共存，讓「感測＋運算」單晶化——這是 MEMS 有別於傳統精密機械的決定性優勢。

### 6. 案件現場：DLP 數位微鏡（Texas Instruments, 1987）

Larry Hornbeck 發明數位微鏡元件（DMD）：每個像素是一面可以靜電翻轉的鋁製微鏡（±10–12°），把光反射到鏡頭或吸收器：

$$\text{每像素} = 1 \text{ 面微鏡} + 2\text{ 個扭轉樞軸（torsion hinge）} + \text{靜電致動電極}$$

- 靠靜電力 $F = \frac{1}{2}V^2 \frac{\partial C}{\partial \theta}$ 翻轉，切換時間微秒級；灰階靠 PWM（時間調變），色彩靠色輪或三片式。
- DMD 是**純 surface micromachining 的極致**：數十萬到數百萬面微鏡做在一顆晶片上，每面鏡子要振動數十億次不疲勞——矽的機械性質再次立功。DLP 投影機 1996 年量產，席捲電影院與辦公室。

### 7. Python 實作：懸臂梁諧振頻率與加速度靈敏度

MEMS 的邊界很快越過了「純機械」，先算核心數學，再記延伸線索（見第 8 節）：

```python
import math

E   = 170e9   # 單晶矽楊氏係數 (Pa)
rho = 2330    # 矽密度 (kg/m^3)

def cantilever(l, w, t):
    """長 l、寬 w、厚 t 的懸臂梁＋質量塊系統：回傳 k, m, f0, 靈敏度 x/a"""
    k = E * w * t**3 / (4 * l**3)      # 彈簧常數 k = E w t^3 / 4 l^3
    m = rho * w * t * l                # 質量塊 m = rho * w * t * l
    f0 = math.sqrt(k / m) / (2 * math.pi)
    sens = m / k * 1e12                # x/a，單位 um per g 換算前的 pm/(m/s^2)
    return k, m, f0, sens

print(f"{'l (um)':>8}{'k (N/m)':>12}{'m (kg)':>12}{'f0 (Hz)':>12}")
for l in [100, 200, 400]:              # 梁長度微米
    k, m, f0, s = cantilever(l*1e-6, 20e-6, 2e-6)
    print(f"{l:>8}{k:>12.3e}{m:>12.3e}{f0:>12.0f}")
#   l (um)     k (N/m)       m (kg)     f0 (Hz)
#      100   6.800e+00   9.320e-12     135,946
#      200   8.500e-01   1.864e-11      33,987
#      400   1.063e-01   3.728e-11       8,497
# 梁長 l 翻倍 → k 降 8 倍、m 增 2 倍 → f0 降 4 倍（f0 ∝ 1/l²）

# 安全氣囊需求：頻寬 >= 500 Hz 且靈敏度足夠
for l in [100, 200, 400]:
    _, _, f0, _ = cantilever(l*1e-6, 20e-6, 2e-6)
    print(f"l={l} um -> f0={f0:.0f} Hz, 滿足氣囊頻寬: {f0 >= 500}")
# l=100 um -> 滿足 / l=200 um -> 滿足 / l=400 um -> 滿足
# 就這組參數而言三種梁長都過關——這正是 MEMS 設計的空間：
# 靈敏度 ∝ m/k，在頻寬許可下盡量選長梁；若要更高 f0（如振動陀螺儀的
# MHz 級諧振），就把梁縮短或加厚——t³ 項讓厚度對 k 的影響最為劇烈。
```

### 8. 延伸線索：微流道與 RF MEMS

- **微流道（microfluidics）**：在晶片刻出數十微米寬的流道，利用層流（Reynolds 數 $Re = \rho v d/\mu \ll 1$，微尺度下慣性力遠小於黏滯力）做精準操控——lab-on-chip、噴墨印表機（HP Thermal Inkjet, 1984 起量產，本身就是 MEMS 致動器）。
- **RF MEMS 開關**：靜電致動的懸臂梁替代 PN 二極體開關，插入損耗低於 0.5 dB、隔離度高於 30 dB——手機射頻前端的濾波器（BAW/SAW）成為 RF MEMS 最大戰場。
- **諾獎級應用**：LIGO 的雷射干涉儀懸掛鏡面、原子力顯微鏡（AFM，1986）的微懸臂探針——微懸臂梁的力感測極限達 pN 級，$k$ 愈小靈敏度愈高，與加速度計共用同一套數學。

## 結案 -- 後果與影響
- **安全氣囊的守護者**：ADXL50（1991）之後，MEMS 加速度計成為汽車氣囊的標準感測器，拯救無數生命；Bosch 的車用 MEMS（壓力、加速度、角速度）至今出貨數十億顆。
- **智慧手機感測器**：iPhone（2007）把 MEMS 加速度計、陀螺儀（旋轉偵測）、麥克風、自動對焦致動器帶進每個人口袋——MEMS 是手機裡「非電子」的靈魂。
- **DLP 投影**：Hornbeck 的 DMD 獲 2009 年奧斯卡科學與工程獎；電影院數位化很大程度靠 DLP 投影。
- **MEMS 產業成形**：Bosch、ST、ADI、TE 等大廠競逐，MEMS 從車用擴展到消費、醫療（血壓計、聽診）、IoT——**IoT 感測層**幾乎全是 MEMS。
- **典範的意義**：Petersen 的論文證明半導體製程可以跨界機械——「IC 科技史」的邊界從此不只在電子，機械、光學、流體都被收進晶片（微流道 lab-on-chip、微光學、RF MEMS 開關）。

## 關鍵人物與文獻
- **Kurt Petersen**：IBM Almaden，1982 年發表 "Silicon as a Mechanical Material," *Proc. IEEE*, 70(5)——MEMS 領域被引用最多的論文。
- **Larry Hornbeck**：Texas Instruments，1987 年發明 DMD（US 專利 5,061,049），2009 年獲奧斯卡科學與工程獎。
- **Analog Devices**：ADXL50（1991）團隊，monolithic MEMS 加速度計首例。
- **Richard Feynman**："There's Plenty of Room at the Bottom," 1959（微型化思想的先聲）。
- W. Trimmer（ed.）, *Micromechanics and MEMS: Classic and Seminal Papers to 1990*, IEEE Press, 1997。
