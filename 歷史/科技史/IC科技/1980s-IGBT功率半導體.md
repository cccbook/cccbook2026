# 1980s - IGBT 功率半導體：電力電子革命的無名引擎

## 案件摘要
1980 年代初，一種奇怪的混血元件悄悄量產：它有 MOSFET 的絕緣閘，卻藏著一顆 BJT 的身體。
它讓數百伏特、數百安培的電流可以用「電壓輕輕一按」的方式開關，導通壓降卻小得驚人。
馬達驅動、變頻器、高鐵、電動車、風電——現代電力電子革命的幕後真兇，就是 IGBT（絕緣閘雙極電晶體）。
本檔案追查這顆「MOS+BJT 混血兒」的誕生、它的宿敵（導通損耗 vs 開關損耗），以及 2010 年代寬能隙半導體（SiC/GaN）接棒的續集。

## 前因 -- 為什麼會有這個案子
- **功率半導體的意義**：發電是交流、用電卻常要直流或變頻——變流器（inverter）、馬達驅動、開關電源都需要「高壓大電流的開關」。開關越快、損耗越低，系統效率就越高。
- **BJT 時代的困境**：1970 年代主導的功率雙極電晶體導通壓降小（$V_{CE(sat)} \approx 1{-}2\,\text{V}$），但它是**電流控制**元件——基極驅動電路笨重耗電，開關慢，且二次崩潰（secondary breakdown）容易燒毀。
- **功率 MOSFET 的困境**：1970s 後期問世的功率 MOSFET 是電壓控制、開關快，但高壓下導通電阻爆衝：

$$R_{on} \propto V_{BR}^{2.5}$$

  擊穿電壓翻倍，導通電阻暴增約 5.7 倍；要扛 600V 就得並聯幾十顆矽片，成本與面積爆炸。
- **關鍵推理**：能不能「MOS 閘負責控制（電壓驅動、快），BJT 負責導通（電導調變、壓降小）」？把兩者垂直疊在同一片矽上，讓 MOS 的汲極充當 BJT 的基極——導通時少數載子注入漂移區（電導調變，conductivity modulation），把那個 $V_{BR}^{2.5}$ 的致命電阻「灌水稀釋」掉。1982 年前後，GE 的 **B. Jayant Baliga** 與 HP 的 **J. P. Plummer、M. Beckher**（及 RCA 等團隊）各自獨立做出這顆元件，1980s 量產後改名 IGBT。

## 線索與推理 -- 數學式、程式、理論

### 1. 案件現場：MOS 閘 + BJT 尾電流
IGBT 的等效電路：一顆 NMOS 驅動一顆 PNP BJT（MOS 汲極接 PNP 基極，漂移區即 PNP 基極）。
- **關閉**：$V_G < V_{th}$，MOS 不導通，PNP 沒有基極電流，元件像一個背對背的 PN 二極體，耐壓可達 $V_{BR}$（600V~6.5kV）。
- **導通**：$V_G > V_{th}$，MOS 提供基極電流，PNP 導通；同時少數載子（電洞）大量注入漂移區：

$$n_{drift} \rightarrow p_{inj} \gg N_D \quad\Longrightarrow\quad \rho_{drift} = \frac{1}{q\mu n} \text{ 驟降數十倍}$$

  這就是**電導調變**：導通壓降 $V_{CE(on)} \approx 1{-}3\,\text{V}$，幾乎不隨擊穿電壓的平方惡化。
- **代價（尾電流）**：關閉時漂移區裡的儲存電荷（電洞）要靠復合慢慢抽走，形成數 μs 級的**尾電流（tail current）**——這正是 IGBT 開關損耗的來源。

### 2. 擊穿電壓與導通電阻：MOSFET 的宿命

功率 MOSFET 高壓版的導通電阻由漂移區主導：

$$R_{on,on} = \frac{4 V_{BR}^{2}}{\epsilon_s \mu_n E_c^{3}} \;\propto\; V_{BR}^{2.5}$$

（$E_c$ 為矽的臨界電場 $\approx 3\times 10^5\,\text{V/cm}$；指數 2.5 來自臨界電場隨摻雜的緩慢變化。）
Baliga 的**優劣因子（BFOM, Baliga Figure of Merit）**把這條定律寫成材料評分：

$$\text{BFOM} = \epsilon_s \mu_n E_c^{3}$$

這個式子直接預言了 SiC 與 GaN 的崛起（見第 4 節）。

### 3. 導通損耗 vs 開關損耗：取捨的數學
功率開關一個週期的總損耗：

$$P_{total} = \underbrace{I^2 R_{on}\cdot D}_{\text{導通損耗}} + \underbrace{\tfrac{1}{2} V I (t_r + t_f)\, f}_{\text{開關損耗}}$$

- 開關頻率 $f$ 越高，變壓器/電感可以越小（系統省錢省體積），但開關損耗線性上升。
- MOSFET：$R_{on}$ 大（高壓下）、$(t_r+t_f)$ 極小（無尾電流）→ 適合**高頻低壓**。
- IGBT：$R_{on}$ 等效極小（電導調變）、$(t_r+t_f)$ 數 μs（尾電流）→ 適合**低頻高壓**。
- 電力電子工程師的日常，就是在這條取捨線上選元件、選頻率。

### 4. FBSOA、擎住效應與寬能隙接棒
- **FBSOA（Forward-Biased Safe Operating Area）**：導通狀態下電壓-電流的安全邊界。早期 IGBT 因 NPN 寄生電晶體而受限。
- **擎住效應（latch-up）**：IGBT 內部天然含有 PNPN 四層結構（寄生 NPN+PNP 晶閘管）；一旦電流過大或 $dv/dt$ 過猛，寄生晶閘管被觸發**自己鎖死導通**，閘極失去控制，直到燒毀。對策：降低寄生 NPN 的 $r_b$（分流孔）、加大 $R_{body}$、後來的「穿通（punch-through）+ 場阻斷層」設計把 latch-up 基本消除。
- **寬能隙半導體（2010s）**：Baliga 的 BFOM 指路——

$$E_g:\ \text{SiC}\ 3.26\,\text{eV},\ \text{GaN}\ 3.4\,\text{eV}\ \text{vs Si}\ 1.12\,\text{eV}$$

  能隙大 → 臨界電場 $E_c$ 高一個數量級（SiC $\approx 3\times 10^6\,\text{V/cm}$）→ 同耐壓下漂移區薄 10 倍、電阻低百倍，且耐溫 200°C 以上。SiC MOSFET 與 GaN HEMT 開始在 650V~1200V 戰場與 IGBT 爭地。

### 5. 元件對照表：三代功率開關的同台偵訊

| 面向 | 功率 BJT (1970s) | 功率 MOSFET (1970s末) | IGBT (1980s) | SiC MOSFET (2010s) |
|------|------------------|----------------------|--------------|--------------------|
| 控制方式 | 電流控制 | 電壓控制 | 電壓控制 | 電壓控制 |
| 耐壓範圍 | <1kV | <900V | 600V~6.5kV | 650V~3.3kV |
| 導通壓降/電阻 | $V_{CE(sat)}\approx1{-}2$V | $R_{on}\propto V_{BR}^{2.5}$ 爆衝 | $V_{CE(on)}\approx1{-}3$V | $R_{on}$ 低百倍 |
| 開關速度 | 慢（儲存時間） | 極快（ns 級） | 慢（尾電流 μs 級） | 快（與 Si MOSFET 相當） |
| 適用頻率 | <10kHz | 100kHz~1MHz | 5~50kHz | 50~500kHz |
| 驅動電路 | 笨重耗電 | 簡單 | 簡單 | 簡單（但閘壓較高） |
| 主要戰場 | 小家電 | 電源、低壓 | 變頻器、電動車、高鐵 | 電動車、快充、資料中心 |

偵訊結論：IGBT 佔據了 BJT 與 MOSFET 都到不了的「高壓中頻」无人区——這正是變頻器與電動車逆變器最需要的甜點區。

### 6. 量產之路：從「IGT」到「IGBT」的命名偵查
- 1982-83 年間，各團隊對這顆元件的命名各自為政：GE 的 Baliga 稱 **IGT**（insulated gate transistor）、RCA 稱 **COMFET**（conductivity-modulated FET）、HP 稱 **insulated gate rectifier**。
- 1980s 中期業界統一命名為 **IGBT**， GE（後來的功率部門併入英飛凌）、西門子、東芝、富士電機相繼量產。
- 量產難點：latch-up 抑制、尾電流縮短（壽命控制：電子照射、摻金）、高壓下的穿通（PT）與非穿通（NPT）設計取捨——NPT（1990s）用厚磊晶片取代外延，魯棒性大增，成本卻降。

### 7. Python 實作：MOSFET vs IGBT 總損耗 ＋ Si vs SiC

```python
import math

def total_loss(I, R_on, V, t_sw, f, D=0.5):
    """P = I^2*R*D + 0.5*V*I*(t_r+t_f)*f，t_sw = t_r+t_f (秒)"""
    return I**2 * R_on * D + 0.5 * V * I * t_sw * f

V, I, f = 600, 20, 20e3            # 600V 直流匯流排、20A、20kHz 變頻器
mosfet = total_loss(I, 0.50, V, 0.1e-6, f)   # 600V 功率 MOSFET：Ron 大、開關快
igbt   = total_loss(I, 0.025, V, 2.0e-6, f)  # IGBT：電導調變、尾電流拖慢開關
print(f"MOSFET 20kHz 總損耗 = {mosfet:.1f} W  (導通 {I**2*0.50*0.5:.0f} W 主導)")
print(f"IGBT   20kHz 總損耗 = {igbt:.1f} W  (開關 {0.5*V*I*2e-6*f:.0f} W 主導)")
# MOSFET 20kHz 總損耗 = 112.0 W  (導通 100 W 主導)
# IGBT   20kHz 總損耗 = 245.0 W  (開關 240 W 主導)
# → 若再往上拉頻率，IGBT 的尾電流損耗線性爆衝，20kHz 已是它的甜點區上限；
#   而 600V 下 MOSFET 的導通損耗因 Ron∝V^2.5 而失控，兩者各守一端。

# 若用 SiC MOSFET（同耐壓漂移區薄 ~10 倍、Ron 低 ~100 倍，開關如 Si MOSFET 般快）：
sic = total_loss(I, 0.005, V, 0.1e-6, f)
print(f"SiC    20kHz 總損耗 = {sic:.1f} W  → 兩頭通吃，IGBT 的 20kHz 戰場被奪")
# SiC    20kHz 總損耗 = 13.0 W  → 兩頭通吃，IGBT 的 20kHz 戰場被奪

# BFOM：能隙與臨界電場的勝負（Baliga Figure of Merit，正規化 Si=1）
eps_mu = {'Si': 1.0, 'SiC': 0.8, 'GaN': 0.9}   # ε*μ 相對值（粗估）
Ec     = {'Si': 3e5, 'SiC': 3e6, 'GaN': 3.5e6} # 臨界電場 (V/cm)
for m in eps_mu:
    print(f"{m}: BFOM = {eps_mu[m]*(Ec[m]/Ec['Si'])**3:.0f}x")
# Si: BFOM = 1x / SiC: BFOM = 800x / GaN: BFOM = 1429x
# → E_c 高一個數量級 ⇒ BFOM 高三個數量級：這就是 SiC/GaN 的材料紅利。
```

### 8. 應用現場：變頻器的數學

變頻器（inverter）把直流變成可調頻率的交流，驅動馬達：馬達轉速正比於頻率（$n \propto f/p$），
所以「控制頻率」就是「控制轉速」——這正是電動車與高鐵牽引的核心：

$$P_{motor} = \tau \cdot \omega = \tau \cdot 2\pi \frac{f}{p},\qquad \eta_{system} = \frac{P_{out}}{P_{out} + P_{total}^{(switch)}}$$

- 6 顆 IGBT 組成三相橋，以 PWM（脈寬調變）切換：開關頻率 $f_{sw}$ 越高，輸出波形越接近正弦、馬達越安靜，但 $P_{total}^{(switch)}$ 線性上升——又是那條取捨線。
- 感應馬達 + IGBT 變頻器 vs 傳統定速馬達：省電 30% 以上；這也是 1990s 日本家電（冷氣、冰箱）全面變頻化的動力。
- 電動車：電池（直流 400V/800V）→ 逆變器（IGBT/SiC）→ 馬達（交流變頻）；逆變器效率每提升 1%，續航多約 2-3 km。
- 高鐵：架空線 25kV 交流 → 變壓器整流 → IGBT 牽引變流器 → 馬達；新幹線與中國高鐵的功率模組都以 IGBT 為心臟。
- 風電與太陽能：變流器把不穩定的發電轉成電網等級的交流，IGBT 模組是併網效率的關鍵。

## 結案 -- 後果與影響
- **電力電子革命**：IGBT 讓變頻器、開關電源、感應馬達驅動全面普及，工業馬達省電 30% 以上；被譽為「電子訊號與電力世界之間的翻譯官」。
- **交通電氣化**：高鐵牽引變流器、電動車逆變器（Toyota Prius 1997 起大量採用）、充電樁——沒有 IGBT 就沒有現代電動車。
- **再生能源**：風電變流器與太陽能逆變器都以 IGBT 為心臟，功率半導體自此從「小訊號配角」變成獨立的戰場。
- **Baliga 的定律**：BFOM 成為功率材料學的評分標準，直接為 SiC（Wolfspeed、意法半導體、英飛凌）與 GaN（快充、資料中心電源）鋪路；2010s 寬能隙開始吞噬 IGBT 的 20kHz+ 戰場，IGBT 退守低頻超高壓（3.3kV~6.5kV）。
- Baliga 因 IGBT 獲 2014 年 IEEE 榮譽獎章，「IGBT 之父」名號與胡正明的「FinFET 之父」相互輝映。

## 關鍵人物與文獻
- **B. Jayant Baliga**（GE → NC State）：1982-83 年 IGBT 發明與理論（BFOM）集大成者。
- **J. P. Plummer、M. Beckher**（HP）及 RCA 團隊：1982 年前後獨立做出同類結構（insulated gate rectifier / COMFET 等多種早期命名）。
- B. J. Baliga, "Power Semiconductor Device Figure of Merit for High-Frequency Applications," IEEE Electron Device Letters, 1989。
- B. J. Baliga, *Fundamentals of Power Semiconductor Devices*, Springer, 2008（功率元件理論聖經）。
- N. Mohan, T. Undeland, W. Robbins, *Power Electronics: Converters, Applications, and Design*, Wiley（電力電子標準教科書）。
