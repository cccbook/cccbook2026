# 1962-Telstar通訊衛星

## 案件摘要
1962 年 7 月 10 日，Bell Labs 設計的 Telstar 1 發射升空，次日即轉播第一場跨大西洋電視節目。但范艾倫輻射帶的慢性損害很快使它失聰——這起意外反而教會了人類如何建造真正的衛星通訊時代。

## 前因 -- 為什麼會有這個案子
- 1945 年，科幻作家 Arthur C. Clarke 在《Wireless World》發表〈Extra-Terrestrial Relays〉：在赤道上空 35,786 km 的**地球同步軌道**放三顆衛星即可覆蓋全球。構想看似遙不可及。
- 1957 年 Sputnik 1 證明衛星可行；1958 年 NASA 的 **Echo 1** 是一顆被動鋁箔氣球——僅反射地面訊號，訊號衰減 150 dB 量級，電視轉播幾乎不可能。
- AT&T 需要跨大西洋電視與電話容量（當時靠海底電纜 TAT-1，僅 36 路語音）。
- Bell Labs 的 John Pierce 主張：與其被動反射，不如衛星自帶接收器與發射器——**主動式轉頻器（transponder）**。這是本案的關鍵推理。

## 線索與推理 -- 數學式、程式、理論
### 1. 主動式衛星 vs 被動反射
Echo 被動反射：地面接收功率 ~ $\left(\frac{\sigma_{sc}}{4\pi R_t^2 R_r^2}\right)$ 級，損耗巨大。
Telstar 主動轉頻：衛星先接收、放大、再變頻發射——鏈路損耗只需付一次衛星路徑的自由空間衰減。

### 2. Telstar 的設計
- 直徑 88 cm、重 77 kg 的球體，72 片太陽能電池供電。
- **微波轉頻器**：接收 6.39 GHz 上鏈，變頻轉發 4.17 GHz 下鏈，頻寬 50 MHz——足以傳一路電視或 600 路電話。
- 使用行波管放大器（TWT, Kompfner 1943 的發明）。
- 軌道：近地橢圓軌道（遠地點約 5,900 km），每圈可通訊約 20 分鐘。

### 3. 衛星通訊鏈路預算：Friis 公式
Friis 傳輸公式給出自由空間接收功率：

$$P_r = P_t\,G_t\,G_r\left(\frac{\lambda}{4\pi R}\right)^2$$

以 dB 表示的鏈路預算：

$$\frac{P_r}{P_n}\,(\text{dB}) = P_t + G_t + G_r - 20\log_{10}\!\left(\frac{4\pi R}{\lambda}\right) - \underbrace{10\log_{10}(kTB)}_{\text{雜訊功率}}$$

其中 $\frac{4\pi R}{\lambda}$ 是「自由空間路徑損耗」，距離每翻倍損耗加 6 dB。

### 4. Clarke 同步軌道的數學
同步軌道半徑由 Kepler 第三定律決定：軌道週期等於地球自轉（23h56m）：

$$T = 2\pi\sqrt{\frac{r^3}{GM_\oplus}} \;\Rightarrow\; r = \left(\frac{GM_\oplus T^2}{4\pi^2}\right)^{1/3} \approx 42{,}164\ \text{km}$$

減去地球半徑 6,378 km，得高度 **35,786 km**。

### 5. Python 計算鏈路預算

```python
import numpy as np
import math

def link_budget(Pt_dbw, Gt_db, Gr_db, f_GHz, R_km, Tsys_K=290, B_MHz=50):
    """Telstar 式鏈路預算（Friis 公式）"""
    lam = 0.299792458/f_GHz                       # 波長 m
    fspl = 20*math.log10(4*np.pi*R_km*1000/lam)   # 自由空間路徑損耗 dB
    Pr_dbw = Pt_dbw + Gt + Gr_db - fspl
    N_dbw  = 10*math.log10(1.38e-23*Tsys_K*B_MHz*1e6)
    return Pr_dbw, fspl, Pr_dbw - N_dbw

# Telstar 參數（近似）
Pt, Gt, Gr, f = 10.0, 18.0, 40.0, 4.17   # 地面站大天線 Gr≈40 dB
R = 4000.0                                # 通訊時平均距離 km
Pr, fspl, snr = link_budget(Pt, Gt, Gr, f, R)
print(f"下行 4.17 GHz、R = {R:.0f} km")
print(f"  自由空間路徑損耗 = {fspl:.1f} dB")
print(f"  接收功率 Pr = {Pr:.1f} dBW")
print(f"  接收 SNR   = {snr:.1f} dB（50 MHz 頻寬）")

# Clarke 同步軌道高度
GMe, Re, T = 3.986e14, 6378e3, 86164.0
r = (GMe*T**2/(4*np.pi**2))**(1/3)
print(f"\n同步軌道高度 = {(r-Re)/1000:,.0f} km（Clarke 1945 的構想）")
```

輸出：Telstar 下行鏈路在 4,000 km 時路徑損耗約 **177 dB**，配合地面站 40 dB 大天線仍可取得足夠 SNR 傳送電視；同步軌道高度 **35,786 km** 正是 Clarke 計算的數字。

## 結案 -- 後果與影響
- 1962.7.11，Telstar 轉播美國總統記者會與跨大西洋電視畫面，全球矚目；12 月起跨大西洋電話、傳真、電視常態化測試。
- **意外的破壞**：1962.7.9 美國 Starfish Prime 高空核試大幅加強范艾倫帶；Telstar 的電子元件在輻射下持續劣化，1963.2.21 永久失聰。這逼出了**太空輻射硬化（radiation hardening）**學科。
- 1963 年 **Syncom 2** 成為第一顆地球同步通訊衛星（Syncom 3 於 1964 轉播東京奧運）；1964 年 **Intelsat** 成立，全球衛星通訊體系誕生。
- Clarke 的構想 19 年後成真；今天超過 500 顆地球同步衛星同時在軌，衛星電視、GPS、衛星網路（Starlink）都是這條推理鏈的果實。

## 關鍵人物與文獻
| 人物 | 貢獻 |
|---|---|
| Arthur C. Clarke | 1945 地球同步衛星構想 |
| John R. Pierce | Telstar 主轉頻器計畫主持 |
| Rudolf Kompfner | 行波管放大器（1943） |
| Harald Friis | Friis 傳輸公式（1946） |

**文獻**
- Clarke, A. C., "Extra-Terrestrial Relays," *Wireless World*, Oct. 1945.
- Pierce, J. R., *Communication Satellites*, Scientific American, 1960.
- Friis, H. T., "A note on a simple transmission formula," *Proc. IRE*, 34, 254 (1946).
- Solomon, J., *Telstar*, Mandelbaum, 2012.
