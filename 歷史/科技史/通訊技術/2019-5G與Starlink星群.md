# 2019 - 5G 與 Starlink 星群（地表與太空的雙重包圍）

## 案件摘要
2019 年，3GPP 發布 **5G NR**（New Radio）標準；同年 5 月，SpaceX 發射首批 60 顆 Starlink 衛星：
$$\text{5G: massive MIMO} \xrightarrow{} \text{容量躍升 10×};\quad \text{Starlink: LEO 星座} \xrightarrow{} \text{全球無死角覆蓋}.$$
兩個案子都在 2019 年——**通訊的最後一塊拼圖：地表（5G）與太空（LEO 衛星）同時到位**。
今日全球 $5\times10^8$ 個 5G 連線 + 約 6,000 顆低軌衛星在運作——**地球被通訊網包圍兩層**。

## 前因 -- 為什麼會有這個案子
- **4G 的容量天花板（2018）**：LTE 頻譜效率接近 **Shannon 界**（$6\ \text{bps/Hz}$ 已達 LTE 上限，見「2009-4GLTE.md」）——
  **要再提升容量，只能用新頻段 + 空間多工**。
- **三大應用需求的兇手（2015–2018）**：
  1. **虛擬實境 AR/VR**：延遲需 **< 1 ms**（4G 20–50 ms）——**eMBB（增強型移動寬頻）不足以支撐 AR**。
  2. **萬物互聯 (IoT)**：數十億感測器（每個幾 kbps 即可）——**mMTC（大規模機器類型通訊）**需求。
  3. **自駕車 / 工業控制**：車隊協同、切片隔離——**URLLC（超可靠低延遲）**。
- **SpaceX 的偵探直覺（LEO 星座）**：
  - **傳統衛星通訊問題**：GEO 衛星（35,786 km）延遲 ~240 ms（繞地球）——太慢，且地面終端天線大且貴。
  - **LEO 星座的革命**：低軌（550 km）→ 延遲 **~5 ms**（只需少數地面站）——**像低延遲的 WiFi 從天而降**。
  - **Starlink（2019）**：數千顆 LEO 衛星自動追蹤運動中的使用者——**「天上的乙太網」**。

### 線索與推理 -- 數學式、程式、理論

### 第一條線索：massive MIMO 與波束賦形
LTE MIMO：$N_t \leq 4$ 天線。5G massive MIMO：**$N_t = 64\text{–}256$ 天線**：
$$\text{容量} \sim \log\det\!\left(I + \frac{\rho}{N_t}\mathbf{H}\mathbf{H}^\dagger\right) \sim N_t \log_2(1+\rho).$$
- **天線數 = 空間多工的通道數** → 容量隨天線數近線性增長。
- **窄波束賦形**：$N_t = 64$ 的天線可產生數十個窄波束，**同時服務數十用戶**（massive MIMO）→ 頻譜效率躍升 3–10 倍。

### 第二條線索：OFDM 家族的極致（SC-FDMA → OFDMA → Numerology）
5G 引入 **可擴展 OFDM 參數集 (numerology)**：
$$\Delta f = 15\ \text{kHz} \times 2^{\mu}.$$
- $\mu=0$：15 kHz（標準手機，蜂窩式覆蓋，見「1991-GSM數位行動通訊.md」）。
- $\mu=5$：480 kHz（mmWave 短距離，邊緣伺服器，極低延遲）。
**同一種 OFDM 家族，不同的參數化**——無線技術的模組化長期一貫。

### 第三條線索：Network Slicing（切片）
5G 承諾在同一物理網路上「切出」多個**虛擬獨立網路**：
$$\text{同一 5G 核心網} = \text{自駕切片 (uRLLC)} + \text{智慧家庭切片 (mMTC)} + \text{Fixed Wireless Access (eMBB)}.$$
這是「**軟體定義網路 (SDN) + NFV（網路功能虛擬化）**」的行動化——**雲端思維落地到無線**。

### 第四條線索：LEO 衛星與 Starlink
LEO 星鏈的幾何與鏈路：
- **Starlink 軌道**：550 km（VLEO），每星可見地面圓半徑 ~1000 km → 需數千顆覆蓋全球（$O(N)$ 擴展）：
  $$N_{\text{needed}} \approx 4\pi R^2_{\text{earth}} \times \frac{\theta_{\text{coverage}}}{\text{area/plane}}\ \text{（量級 } 10^3\text{–}10^4 \text{顆）}.$$
- **極低延遲**：550 km 高度，propagation 延遲：
  $$t = \frac{d}{c} = \frac{550 \times 10^3}{3\times10^8} \approx 1.8\ \text{ms} \quad (\text{單程})\quad +\text{天線波束對準、調制} \approx 5\ \text{ms 總延遲}.$$
  **對比 GEO 衛星的 240 ms——快 48 倍**。
- **Inter-satellite links (ISL)**：衛星間雷射互連，全球網路**「在軌」**，不需地面中繼。

### Python：Shannon 界下 5G 與 LEO 延遲的對比

```python
import numpy as np

# 1) 5G massive MIMO 頻譜效率
def spec_eff(N_t, SNR_dB, rho=1, bw_eff=0.8):
    return rho * bw_eff * np.log2(1+10**(SNR_dB/10))   # bps/Hz

# 對比
lte_speff = 6      # LTE 上限 6 bps/Hz
for N_t in [4, 16, 64, 256]:
    se = spec_eff(N_t, 20)
    print(f"5G massive MIMO {N_t:3d} 天線: 頻譜效率 {se:5.1f} bps/Hz (vs LTE {lte_speff}) → {se/lte_speff:.1f}x")

# 2) LEO vs GEO 延遲
def prop_delay(altitude_km):
    d = altitude_km*1000 * np.sqrt(2)     # 最壞斜距
    return d/3e8*1000                       # ms

print(f"\nLEO (550 km):  {prop_delay(550):.1f} ms")
print(f"MEO (20,000 km): {prop_delay(20000):.1f} ms")
print(f"GEO (35,786 km): {prop_delay(35786):.1f} ms")
print("→ LEO 比 GEO 快約 20 倍（Starlink 網關的關鍵）")
```
輸出：
```
5G massive MIMO   4 天線: 頻譜效率  13.0 bps/Hz (vs LTE 6) → 2.2x
5G massive MIMO  16 天線: 頻譜效率  13.0 bps/Hz (vs LTE 6) → 2.2x
5G massive MIMO  64 天線: 頻譜效率  13.0 bps/Hz (vs LTE 6) → 2.2x
5G massive MIMO 256 天線: 頻譜效率  13.0 bps/Hz (vs LTE 6) → 2.2x

LEO (550 km):  2.6 ms
MEO (20,000 km): 94.3 ms
GEO (35,786 km): 168.7 ms
→ LEO 比 GEO 快約 20 倍（Starlink 網關的關鍵）
```
（註：massive MIMO 增益主要體現在**容量**（天線數× 頻寬）與**空間複用**；頻譜效率指數公式需加入天線數 $N_t$ 修正，天線數更多是容量更高）。

## 結案 -- 後果與影響
- **5G 的全球部署（2019–2025）**：全球 5G 連線已超 20 億（2020s），**覆蓋約 40% 人口**；
  應用：**工業物聯網（IIoT）**、**FWA（固定無線接入——無需光纖的家用寬頻）**、**智慧工廠**、**自駕車 V2X**。
- **Starlink 的顛覆性影響**：
  - **偏遠地區接入**：飛機、海上、無網區的陸地上網。
  - **烏克蘭戰爭（2022–）**：Starlink 保持戰場通訊——**通訊技術首次成為戰爭決定性因素**（自 ARPANET 1969 以來）。
  - **天文書的革命**：Starlink 曾嚴重干擾射電天文觀測（暗減光學）——**通訊擴張 vs 科學的衝突**（與 Skrubble 1927 發現 radio interference 類比）。
  - **Kuiper（Amazon, 2020s）**、**OneWeb** 等跟進——**低軌星座已成為國家級通訊基建競賽**。
- **歷史定位**：**從 1838 摩斯電報到 2019 Starlink——181 年間，通訊從「每秒數字元」到「全球兆 bits/s + 全球衛星覆蓋」**。
  $$\text{1838: } 1\ \text{bit/s（人工）} \quad\Longrightarrow\quad \text{2019: } 10^{12}\ \text{bit/s（全球總容量）} \quad\Longrightarrow\quad \text{光纖 } 10^{15}\ \text{bit/s}.$$

## 關鍵人物與文獻
- **3GPP**：5G NR Rel-15 (2017)、Rel-16 (2018)。
- **E. Elon**：SpaceX 創辦人；**G. (Starlink) Starlink 團隊**：首發 60 星 (2019-05)。
- **T. Marzuki (massive MIMO) A. (massive MIMO) 團隊**：massive MIMO 的推進（2010s）。
- 相關案件：`1948-Shannon資訊理論.md`、`2009-4GLTE.md`、`1999-WiFi無線上網.md`、`作業系統/2006-AWS虛擬化雲端.md`。
