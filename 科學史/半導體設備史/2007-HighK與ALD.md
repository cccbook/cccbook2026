# 2007 - Intel 45nm high-k 與 ALD（原子層沉積：一次長一層分子）

## 案件摘要
2007 年 11 月，**Intel** 出貨 **45 nm Penryn**——**HfO₂ high-k 閘介電層 + 金屬閘**，
**1960 年代以來 MOSFET 最重大的材料變革**：
$$\text{SiO}_2\text{ 閘氧化層（1.2 nm = 5 顆原子）} \xrightarrow{\text{HfO}_2\text{（物理厚、電學薄）}} \text{漏電流降 100 倍}$$
關鍵設備是 **ALD（原子層沉積，Atomic Layer Deposition）**——
**自限性表面反應，每個循環只長一層原子（~0.1 nm）**：
$$\text{CVD/PVD（無法均勻鍍 1 nm）} \xrightarrow{\text{ALD（自限反應）}} \text{100\% 階梯覆蓋}$$
ASM International 的 ALD 機台成為量產設備——**ALD 從此是每個節點的必需品**。

## 前因 -- 為什麼會有這個案子
- **SiO₂ 的原子級危機**：90 nm 世代閘氧化層只剩 **1.2 nm（5 顆原子厚）**——
  量子穿隧漏電（tunneling leakage）→ **功耗牆（power wall）**；
- **Dennard 縮放的崩潰**：傳統縮放（尺寸縮小、電壓同降）失效——
  **漏電不吃縮放的帳**——需要新材料（高介電常數 k）；
- **HfO₂ 的沉積難題**：high-k 材料（HfO₂，k~25）已知 20 年——
  但 **1 nm 級均勻沉積**，CVD/PVD 做不到（階梯覆蓋差、厚度不均）；
- **ALD 的舊發明**：1974 年芬蘭 **Tuomo Suntola** 發明 ALD（原為電致發光顯示器）——
  **發明 33 年後才找到殺手級應用**。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：EOT 的數學（為什麼 high-k 能救摩爾定律）
等效氧化層厚度（EOT）：
$$t_{SiO_2,eq} = \frac{k_{SiO_2}}{k_{high\text{-}k}} \times t_{high\text{-}k}$$
- HfO₂：k ≈ 25（SiO₂ 的 6 倍）→ **物理厚度 5 nm ≈ 電學厚度 1 nm**——
  **穿隧漏電看物理厚度、電容看 k 值**——兩者解耦了。

### 第二條線索：ALD 的自限性反應（為什麼每循環只長一層）
半反應（TMA + H₂O 例）：
$$\underbrace{\text{Surface-OH} + \text{Al(CH}_3)_3}_{\text{半反應 1}} \to \text{Surface-O-Al(CH}_3)_2 + \text{CH}_4 \uparrow$$
$$\underbrace{\text{Surface-CH}_3 + \text{H}_2\text{O}}_{\text{半反應 2}} \to \text{Surface-OH} + \text{CH}_4 \uparrow$$
- **反應位用完即停**（self-limiting）→ **每循環精確 0.1 nm**——
  與時間、溫度（在 ALD window 內）無關；
- **偵推**：CVD 的厚度是「時間 × 速率」（要控制）；ALD 的厚度是
  「**循環數 × 0.1 nm**」（**數數字**）——**從連續控制變離散控制**。

### 第三條線索：階梯覆蓋的物理（ALD 的殺手級特性）
反應位飽和 → 氣體可以「爬進」任何角落：
$$\text{階梯覆蓋} \approx 100\% \quad (\text{深寬比無關})$$
- 高深寬比 DRAM 電容（100:1）、3D NAND 的孔——**只有 ALD 填得進**。

### 第四條線索：ALD vs CVD 對照
| 特性 | CVD（連續） | ALD（循環） |
|------|-------------|-------------|
| 成長方式 | 連續（速率 × 時間） | 離散（0.1 nm/循環）|
| 厚度控制 | ±5% | ±0.1 nm（數循環）|
| 階梯覆蓋 | 50–80% | ~100% |
| 產能 | 高 | 低（循環時間）|
| 用途 | 厚膜 | **閘介電、阻障、襯墊** |

## 結案 -- 後果與影響
- **ALD 無所不在**：high-k 閘介電（2007）→ Co/W 襯墊 → 間隔層（spacer）
  → 封裝層——**每個先進節點的必需設備**。
- **ASM International 的勝利**：荷蘭小公司（1964 年 del Prado 創立）抓住 ALD——
  **利基設備商的教科書**。
- **Dennard 縮放的延壽**：high-k + 金屬閘讓摩爾定律多跑 15 年（45→3 nm）——
  **材料的變革由設備使能**。
- **Suntola 的遲來正典**：1974 年為顯示器發明 ALD，2004–07 年成為半導體的
  殺手級應用——**發明與應用相隔 33 年**——設備史的長程偵探案。
- **偵探教訓**：ALD 證明了「**自限性（self-limiting）是奈米時代的核心原理**」——
  ALD（沉積）、ALE（蝕刻，見 `1974-電漿蝕刻.md` 的 ALE 分支）——
  **奈米工程的哲學：讓化學自己停止**。

## 關鍵人物與文獻
- **Tuomo Suntola**（1974）：ALD 發明（芬蘭）——2018 年獲千禧科技獎。
- **Intel 45 nm 團隊**（2007）：high-k + 金屬閘量產。
- **ASM International**：ALD 量產設備（Pulsar 系列）。
- 相關案件：`1994-HDPCVD.md`、`1974-電漿蝕刻.md`、`2019-EUV量產.md`。
