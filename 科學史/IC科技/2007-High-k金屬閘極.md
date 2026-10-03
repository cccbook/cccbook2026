# 2007 - High-k 金屬閘極：Intel 45nm 的漏電危機解除戰

## 案件摘要
2007 年 1 月，Intel 宣布 45nm 製程（Penryn）量產，全球首次採用 hafnium 基 high-k 介電層＋金屬閘極。
SiO2 閘極氧化層被微縮到只剩 5 顆原子厚，隧道漏電失控——這是摩爾定律面臨的第一道「材料牆」。
偵探的解法不是把氧化層做薄，而是**換一種介電常數更大的材料**：同樣的閘控能力，物理厚度卻可以厚 10 倍。
本檔案追查這場「換材料不換定律」的偵查，以及它如何為 2011 年的 FinFET 革命鋪路。

## 前因 -- 為什麼會有這個案子
- **SiO2 的終局**：從 1970 年代起，閘極氧化層每個世代縮 0.7 倍，到 65nm 時 $t_{ox} \approx 1.2\,\text{nm}$（不到 5 層 SiO2 分子）；再縮下去漏電與良率一起崩盤。
- **隧道漏電爆衝**：閘極氧化層薄到 2nm 以下，電子開始**直接穿隧**（direct tunneling）穿過氧化層，漏電流隨厚度**指數**上升（$I_{leak} \propto e^{-d}$）。90nm→65nm 世代，閘極漏電功耗逼近甚至超過動態功耗，筆電電池被閘極「偷電」。
- **poly depletion 的內憂**：多晶矽閘極自身有一層耗盡層（約 0.5-1nm），等於在 $t_{ox}$ 之外再加一段串聯電容，讓有效閘控能力再縮水。
- **傳統對策失效**：氮化氧化層（SiON）只能延緩一個世代；再往下，物理上已無路可走。
- **關鍵推理**：閘控能力由電容 $C = \kappa \epsilon_0 A / t_{phys}$ 決定——要同樣的 $C$，可以縮 $t_{phys}$，也可以**放大 $\kappa$**。找一種 $\kappa$ 比 SiO2（3.9）大 6 倍以上的材料，物理厚度就能厚 6 倍以上，隧道漏電指數下降。這正是 high-k 的推理核心。

## 線索與推理 -- 數學式、程式、理論

### 1. EOT：把「不同材料」換算成「等效 SiO2 厚度」

$$\text{EOT} = t_{phys} \cdot \frac{\kappa_{SiO_2}}{\kappa_{high-k}} = t_{phys} \cdot \frac{3.9}{\kappa}$$

- 45nm 世代的目標：EOT $\approx 1.0\,\text{nm}$。若用 HfO2（$\kappa \approx 25$），物理厚度可達：

$$t_{phys} = 1.0 \times \frac{25}{3.9} \approx 6.4\,\text{nm} \quad(\approx 15\ \text{層 HfO2}）$$

  比原來的 1.2nm 厚 5 倍以上——隧道穿隧機率隨厚度**指數**下降，這就是「換材料救漏電」的數學本質。

### 2. 隧道漏電：指數下降的偵查數學

矩形位能障壁的 WKB 近似：

$$I_{leak} \propto e^{-A \sqrt{\phi_m}\, d}$$

其中 $\phi_m$ 為障壁高度（電子親合力差，SiO2 $\approx 3.1\,\text{eV}$、HfO2 $\approx 1.5\,\text{eV}$）、$d$ 為物理厚度、$A = \dfrac{2\sqrt{2m^*q}}{\hbar}$。
- SiO2 1.2nm：$\sqrt{\phi_m} d \approx \sqrt{3.1} \times 1.2 \approx 2.1$ → 漏電巨大。
- HfO2 6.4nm：$\sqrt{\phi_m} d \approx \sqrt{1.5} \times 6.4 \approx 7.8$ → 指數衰減快 3.7 倍，漏電**下降數個數量級**。
- 偵查重點：**比的不是 $\kappa$，也不是厚度，而是 $\sqrt{\phi_m} \times d$ 的乘積**——這也是為什麼 $\phi_m$ 偏低的 HfO2 依然能大幅救漏電：厚度贏的比障壁輸的多太多。

### 3. 金屬閘極：解 poly depletion 與功函數調變
- **取代 poly depletion**：金屬閘極沒有耗盡層，$C_{gate} = \kappa\epsilon_0 A / t_{high-k}$ 直接成立，等效又多省 0.5-1nm EOT。
- **功函數調變**：CMOS 需要 NMOS（低功函數）與 PMOS（高功函數）兩種閘極。HfO2 上的金屬功函數會被 **Fermi-level pinning** 拉向中間（N-type 靠 TiN/Hf、P-type 靠 AlN/W 的配方對抗），這是 45nm 研發最大的戰場之一。
- **CMOS 雙金屬閘**：Intel 45nm 用 NMOS/PMOS 兩種不同金屬（成分保密至今），加上 HfO2 介電層，合計 3 種新材料、超過 100 道新工序。

### 4. 閘極漏電 vs 通道遷移率的取捨
- HfO2 與 Si 介面的聲子散射會拉低**通道遷移率**（effective mobility 下降 20-30%）；對策：在 HfO2 與 Si 之間夾一層超薄 SiO2 介面層（interfacial layer，$\sim$0.5-1nm）——最終結構是「SiO2 界面層 + HfO2 + 金屬閘」的三明治。
- **Vth roll-off**：金屬閘極與 HfO2 的固定電荷使 $V_{th}$ 隨尺寸漂移，需靠 halo/閘極間距設計壓制。
- 取捨的結論：漏電降 1-2 個數量級，遷移率損失 10-20%，驅動電流不降反升（金屬閘多出的 EOT 紅利），淨效益為正。

### 5. 對照表：SiO2 vs High-k 的同台偵訊

| 面向 | SiO2/SiON (≤65nm) | HfO2 + 金屬閘 (45nm) |
|------|-------------------|----------------------|
| 介電常數 κ | 3.9（SiON 約 4.2-7） | ~25 |
| 物理厚度（同 EOT=1nm） | 1.0-1.2nm（~5 層原子） | ~6.4nm（~15 層） |
| 閘極漏電 | 爆衝（direct tunneling） | 低 1-2 個數量級（Intel：降 25 倍） |
| 閘極耗盡層 | poly depletion ~0.5-1nm | 無（金屬閘） |
| 通道遷移率 | 基準 | 降 10-20%（聲子散射，靠界面層補償） |
| 驅動電流 | 基準 | 提升 15-20%（EOT 紅利） |
| Vth 控制 | poly 功函數，成熟 | Fermi pinning、固定電荷（新戰場） |
| 新材料/新工序 | 無 | 3 種新材料、>100 道新工序 |

### 6. 量產之路：Intel 45nm 與 FinFET 鋪路
- 2007 年 1 月 Intel 宣布 Penryn 量產，45nm 全球首度採用 high-k/metal gate（HKMG）；閘極漏電降 **25 倍**以上（Intel 官方數據），驅動電流提升 15-20%。
- 此後 HKMG 成為 **28nm 以下先進製程的標準配備**：台積電 28nm（2011）導入 HKMG，三星 32/28nm 跟進。
- 2011 年 Intel 22nm Ivy Bridge 在 HKMG 基礎上疊加 **FinFET**——先解「材料牆」（2007），再解「結構牆」（2011），摩爾定律的兩堵牆被同一條推理線拆掉（銜接 2011-FinFET 檔案）。
- 下一站：GAA 奈米片（2020s）繼續沿用 HKMG，閘極包覆再進化。

### 7. 時間軸：閘極介電層的縮微型案史

| 世代 | 年代 | $t_{ox}$ (nm) | 閘極材料 | 介電層 |
|------|------|---------------|----------|--------|
| 鋁閘時代 | 1970s | 100+ | Al | SiO2 |
| 矽閘時代 | 1978~ | 10-20 | Poly-Si | SiO2 |
| 180nm | 1999 | ~3.0 | Poly-Si | SiO2 |
| 130nm | 2001 | ~2.0 | Poly-Si | SiO2（氮化開始） |
| 90nm | 2003 | ~1.5 | Poly-Si | SiON |
| 65nm | 2005 | ~1.2 | Poly-Si | SiON（漏電爆衝） |
| **45nm** | **2007** | **EOT ~1.0** | **金屬（雙金屬閘）** | **HfO2 high-k** |
| 32/28nm | 2009~2011 | EOT ~0.9 | 金屬 | HKMG 標準化 |
| 22nm/16nm | 2011~2014 | EOT ~0.8 | 金屬 | HKMG + FinFET |
| 7nm~3nm | 2018~ | EOT ~0.5 | 金屬 | HKMG + FinFET/GAA |

時間軸的偵查結論：2007 年是「微縮 $t_{ox}$」路線的終點、與「放大 $\kappa$」路線的起點——材料取代尺寸，正是 EOT 公式 $\text{EOT} = t_{phys} \cdot 3.9/\kappa$ 的直接推論。

### 8. Python 實作：EOT 與漏電計算

```python
import math

K_SIO2 = 3.9
k_hf   = 25.0                       # HfO2 介電常數

def eot(t_phys, kappa):
    """EOT = t_phys * 3.9 / kappa (nm)"""
    return t_phys * K_SIO2 / kappa

def tunnel_ratio(A_phi_d_1, A_phi_d_2):
    """I ∝ exp(-A·sqrt(φ)·d)，回傳兩組 (sqrt(φm)*d) 的漏電比"""
    return math.exp(-(A_phi_d_2 - A_phi_d_1))

# 目標 EOT = 1.0 nm：SiO2 需要 1.0nm，HfO2 反算物理厚度
t_hf = 1.0 * k_hf / K_SIO2                   # t_phys = EOT · κ / 3.9
print(f"同 EOT=1.0nm：SiO2 = 1.0nm，HfO2 = {t_hf:.2f}nm（厚 {t_hf:.1f} 倍）")
# 同 EOT=1.0nm：SiO2 = 1.0nm，HfO2 = 6.41nm（厚 6.4 倍）

# 漏電比：I ∝ exp(-A·sqrt(φm)·d)，d 以 nm 計（係數歸一）
sio2_factor = math.sqrt(3.1) * 1.2          # SiO2: φm=3.1eV, d=1.2nm
hf_factor   = math.sqrt(1.5) * 6.41         # HfO2: φm=1.5eV, d=6.41nm
ratio = math.exp(sio2_factor - hf_factor)   # 漏電下降倍數
print(f"HfO2 / SiO2 漏電比 = {ratio:.2e}（下降 {1/ratio:.0f} 倍）")
# HfO2 / SiO2 漏電比 = 3.22e-03（下降 310 倍）
# → 厚度贏的比障壁輸的多太多：即使 φm 偏低，漏電仍降兩個數量級以上。

# 若只加厚 SiO2 到 6.4nm（不換材料）：漏電下降多少？
sio2_thick = math.exp(math.sqrt(3.1) * (1.2 - 6.4))
print(f"SiO2 加厚到 6.4nm（同 EOT？不，EOT=6.4nm 閘控太弱）漏電 = {sio2_thick:.2e} 檔")
# SiO2 加厚到 6.4nm（同 EOT？不，EOT=6.4nm 閘控太弱）漏電 = 1.06e-04 檔
# → 單純加厚 SiO2 漏電更低，但 EOT 爆到 6.4nm、閘控失效；
#   high-k 的價值 = 漏電下降 AND 閘控(EOT)不變，兩者兼得。

# 延伸偵查：不同 high-k 候選材料的 EOT（同樣目標 EOT=1.0nm 所需物理厚度）
for name, k in [('SiO2', 3.9), ('Al2O3', 9.0), ('ZrO2', 22.0), ('HfO2', 25.0), ('La2O3', 30.0)]:
    print(f"{name}: κ={k:>4}, 同 EOT=1.0nm 需物理厚度 {1.0*k/K_SIO2:.2f}nm")
# SiO2: κ= 3.9, 同 EOT=1.0nm 需物理厚度 1.00nm
# Al2O3: κ= 9.0, 同 EOT=1.0nm 需物理厚度 2.31nm
# ZrO2: κ=22.0, 同 EOT=1.0nm 需物理厚度 5.64nm
# HfO2: κ=25.0, 同 EOT=1.0nm 需物理厚度 6.41nm
# La2O3: κ=30.0, 同 EOT=1.0nm 需物理厚度 7.69nm
# → 產業最終選 HfO2：κ 夠大、熱穩定性好、且與 Si 的熱力學相容性最佳——
#   κ 最大者（La2O3）未必是贏家，穩定性與界面品質才是判決關鍵。
```

## 結案 -- 後果與影響
- **閘極漏電危機解除**：HKMG 讓閘極漏電降 1-2 個數量級，靜態功耗重新低於動態功耗，筆電與手機電池續航保住。
- **high-k/metal gate 成為標準**：28nm 以下先進製程全部採用 HKMG，材料創新（而不只是微縮）自此成為摩爾定律的主引擎之一。
- **Intel 最後一次製程領先的標誌**：45nm 的 3 種新材料＋100 道新工序是 Intel 製程霸權的高峰；2011 FinFET 之後，台積電與三星在先進製程上逐漸追平並反超。
- **為 FinFET/GAA 鋪路**：HKMG 先解材料牆（2007），FinFET 再解結構牆（2011），GAA 奈米片（2020s）繼續沿用——「閘極包覆最大化＋介電層最優化」的推理路線仍是微縮的主旋律。
- hafnium 從冷門元素變成半導體產業的戰略物資；介電材料研究（ZrO2、LaO、Al2O3 摻雜調 κ 與功函數）成為學界顯學。

## 關鍵人物與文獻
- **Ghavam Shahidi、Mark Bohr**（Intel 45nm 技術團隊領導）：2007 年 Penryn 量產宣告。
- Intel, "Breaking Barriers: Intel's 45nm High-k Metal Gate" 技術白皮書（2007）。
- G. D. Wilk, R. M. Wallace, J. M. Anthony, "High-κ gate dielectrics: Current status and materials properties," *Journal of Applied Physics*, 2001（high-k 材料聖經）。
- Y. Taur、T. Ning：《Fundamentals of Modern VLSI Devices》——閘極氧化層與隧道漏電的理論經典。
- K. Mistry et al., "A 45nm Logic Technology with High-k+Metal Gate Transistors," IEDM 2007。
