# 1980s - NAND Flash 快閃記憶體：斷電也不會忘記的偵探筆記本

## 案件摘要
1980 年，東芝的舛岡富士雄（Fujio Masuoka）提出「Flash」構想：一整塊閘極可以瞬間集體抹除，快如閃光。
1984 年他在 ISSCC 發表 NOR 型快閃的前身技術，1987 年再發表真正的 NAND 陣列。
這個案子追查的是：記憶體如何同時做到「非揮發、高密度、可電寫」——最終颠覆了硬碟與磁片，成為 SSD 與手機儲存的基礎。

## 前因 -- 為什麼會有這個案子
- **DRAM 會失憶**：1970 年代的 DRAM（見《1970-DRAM與MOS記憶體》）斷電即失去資料，主記憶體之外的儲存層仍靠磁碟與 EPROM。
- **EPROM 罩門**：Dov Frohman-Bentchkowsky（Intel, 1971）發明浮閘電晶體 EPROM，但**抹除要拆下來用紫外線照十幾分鐘**，無法在系統內電性擦除。
- **EEPROM 太貴**：電性可抹除的 EEPROM 每個 cell 要兩顆電晶體（select + storage），位元成本高。
- **硬碟是機械的**：磁碟靠馬達與磁頭，體積大、怕震、延遲在毫秒級——行動裝置時代需要固態的非揮發性儲存。
- **關鍵推理**：舛岡注意到 EEPROM 的兩顆電晶體中，select 電晶體的功能其實可以**串聯在陣列裡互相分擔**——一整個位元線串共用一顆地選擇閘，cell 數從 $O(\text{contact})$ 降為 $O(\text{bits})$，密度優勢就此出現。

## 線索與推理 -- 數學式、程式、理論

### 1. 凶器本體：浮閘電晶體

浮閘（floating gate）是被絕緣層（氧化矽 ONO 疊層）完全包住的導電層，懸浮在通道上方：

```
    Control Gate（控制閘）
    ───────────────────
    ONO 介電層（絕緣）
    ───────────────────
    Floating Gate（浮閘，存電荷）
    ───────────────────
    tunnel oxide（穿隧氧化層）
    ───────────────────
    Si 通道（源極 S ─ 洩極 D）
```

- 浮閘上**有無電荷**改變通道的臨界電壓 $V_T$：無電荷 → $V_{T,\text{low}}$（讀為 1），有電荷 → $V_{T,\text{high}}$（讀為 0）。寫入/抹除的門檻位移：
$$\Delta V_T = \frac{Q_{FG}}{C_{PP}} = \frac{Q_{FG}}{\varepsilon_{ox}/t_{ONO}}$$
- 電荷被絕緣層困住，室溫下可保持 **10 年以上**——這就是「非揮發」的物理根據。

### 2. 寫入與抹除的兩種手法

- **熱電子注入（CHE, channel hot electron）**：寫 NOR 時把漏極電壓拉高，電子在通道獲得高動能，翻越約 $3.2\ \text{eV}$ 的氧化層勢壘跳上浮閘。快（微秒級）但耗電，且只能逐 bit 寫。
- **Fowler–Nordheim 隧穿（FN tunneling）**：在閘極加強電場，電子直接**量子穿隧**通過氧化層。FN 電流密度：
$$J_{FN} = A E^2 e^{-B/E}, \qquad E = \frac{V_{gate}}{t_{ox}}$$
  其中 $A, B$ 為與氧化層材料相關的常數（$B \approx 2.4\times10^8\ \text{V/cm}$，SiO₂）。FN 隧穿電流雖小，但**可以在系統內集體操作**——一整個區塊（block）同時抹除，這正是「Flash」名稱的由來。NAND 的寫入與抹除**都靠 FN 隧穿**。

### 3. NOR vs NAND：兩種陣列拓撲

```
NOR：每個 cell 並聯在位元線與地線之間      NAND：8~64 顆 cell 串成一串
  BL ──┬──┬──┬──                          BL ─[C0]─[C1]─…─[Cn]─[GSL]─ GND
      C0  C1  Cn（各有獨立 contact）       共用 GSL/SSL，省下大量 contact
  → 隨機存取、可直接執行程式碼（XIP）      → 只能頁（page）存取，但密度高、
  → BIOS、手機早期程式碼儲存                 位元成本低，適合大量資料儲存
```

- NOR 隨機存取延遲低，讀取像 DRAM；NAND 以**頁**為單位（4–16 KB），序列讀出如磁帶。
- **NAND 的密度優勢**：串聯結構讓相鄰 cell 直接頭尾相接，**省掉每顆 cell 独立的 contact**（contact 面積遠大於 cell 本身）。位元密度：
$$\text{NAND 密度} \propto \frac{\text{可用面積}}{\text{cell 面積}} \approx O(\text{bits}), \qquad \text{NOR 密度} \propto O(\text{bits} + \text{contacts})$$
- 代價：串聯中任一顆 cell 漏電或壞掉，整串資料受影響 → NAND 需要 **ECC 錯誤更正**與壞塊管理（wear leveling）。

### 4. SLC → MLC → TLC → QLC：每 cell 位元數的賭局

把 $V_T$ 的分佈窗口切成 $2^b$ 份，每 cell 存 $b$ 個位元：

| 世代 | 每 cell 位元數 | $V_T$ 分佈層數 | 容量倍數 | P/E cycle 壽命（典型）|
|---|---|---|---|---|
| SLC | 1 | 2 | 1× | ~100,000 |
| MLC | 2 | 4 | 2× | ~3,000–10,000 |
| TLC | 3 | 8 | 3× | ~500–3,000 |
| QLC | 4 | 16 | 4× | ~100–1,000 |

- **可靠度代價**：每 cell 位元數翻倍，相鄰 $V_T$ 分佈間的餘裕（margin）縮小，電荷雜訊、retention 漏電、read disturb 更容易把位元翻錯：
$$\text{margin} \propto \frac{\Delta V_T}{2^b} \;\Rightarrow\; b \uparrow \;\Rightarrow\; \text{ECC 需求與壞塊率上升}$$
- 容量與壽命是零和賽局：QLC 便宜但只能寫幾百次——靠控制器 wear leveling 把寫入均攤到整顆晶片。

### 5. 2D 微縮終結 → 3D NAND：往上蓋樓

2D 微縮到十幾奈米後，cell 之間的電荷干擾與製造誤差讓 $V_T$ 分佈無法再縮小——平面微縮的摩爾定律在 NAND 上**率先終結**（比邏輯製程早了十年）。

解法：把 cell **垂直堆疊**。2013 年 Samsung 推出 24 層 V-NAND，如今已超過 200 層、往 400 層邁進：

$$\text{容量} \propto \text{layers} \times \text{bits/cell} = O(\text{layers})$$

- 3D NAND 用**垂直通道**（channel hole 貫穿所有層），cell 圍繞在孔壁上，尺寸可以放回 50 nm 級，$V_T$ 分佈餘裕恢復，MLC/TLC/QLC 才能穩定量產。
- 堆疊是**疊代式的**：一批 24 層蝕刻完、疊上另一批，層數從 24 → 32 → 64 → 96 → 128 → 176 → 232，成長如摩天大樓。

### 6. NAND 的管理層：ECC、wear leveling 與壞塊

NAND 的 cell 會衰老、出廠就有壞塊，控制器必須做三件事：

- **ECC 錯誤更正**：從 BCH 碼進化到 LDPC（TLC/QLC 標配）。每 cell 位元數愈多，原始誤碼率（RBER）愈高，ECC 需求從 SLC 的 1 bit/512B 升到 QLC 的數十 bit/1KB。
- **Wear leveling（磨損均攤）**：把寫入均攤到整顆晶片，避免熱區塊提前死亡——實際壽命由最差的 cell 決定，故：
$$\text{有效壽命} = \frac{\text{總 P/E cycle} \times \text{容量}}{\text{寫入放大係數（WAF）}}$$
- **Garbage collection**：NAND 只能整塊（block）抹除、整頁寫入，更新資料要先把有效頁搬到新塊再抹除舊塊——這就是寫入放大的來源（WAF 常在 2–5 之間）。

### 7. Python 實作：FN 隧穿與 SLC/MLC/TLC/QLC 容量模擬

```python
import math

# --- Fowler–Nordheim 隧穿電流（相對值）與寫入時間 ---
A = 4e-15                  # 前指數常數，SiO2 的典型量級 (A/(V/cm)^2)
B = 2.4e8                  # 指數常數，SiO2 的典型值 (V/cm)
t_ox = 1e-6                # 穿隧氧化層 10 nm = 1e-6 cm

def j_fn(v_gate):
    E = v_gate / t_ox      # 電場 (V/cm)
    return A * E**2 * math.exp(-B / E) if E > 0 else 0.0

for v in [8, 12, 15, 18, 20]:
    print(f"V_gate={v:>2} V  ->  J_FN = {j_fn(v):.3e} A/cm^2")
# V_gate= 8 V  ->  J_FN = 2.4e-14 A/cm^2   （電場不足，隧穿被指數壓制）
# V_gate=12 V  ->  J_FN = 1.2e-09 A/cm^2
# V_gate=15 V  ->  J_FN = 1.0e-07 A/cm^2
# V_gate=18 V  ->  J_FN = 2.1e-06 A/cm^2
# V_gate=20 V  ->  J_FN = 9.8e-06 A/cm^2   （指數項 e^{-B/E} 主導，電壓略增電流暴增）

# --- SLC/MLC/TLC/QLC 容量與 P/E cycle 對照 ---
gen = [("SLC", 1, 100_000), ("MLC", 2, 3_000), ("TLC", 3, 1_000), ("QLC", 4, 300)]
bits_die = 256e9  # 假設 SLC 基準容量 256 Gb

print(f"\n{'世代':<5}{'bits/cell':>9}{'容量':>10}{'P/E cycle':>12}")
for name, b, pec in gen:
    cap = bits_die * b / 8  # bits -> bytes
    print(f"{name:<5}{b:>9}{cap/1e9:>8.0f}GB{pec:>12,}")
# 世代   bits/cell      容量   P/E cycle
# SLC          1       32GB     100,000
# MLC          2       64GB       3,000
# TLC          3       96GB       1,000
# QLC          4      128GB         300
```

FN 隧穿的指數項 $e^{-B/E}$ 讓電流對電場極端敏感——寫入電壓從 15 V 加到 18 V，電流密度放大四個數量級。這既解釋了為何 NAND 寫入只需微秒（高電壓泵浦），也解釋了為何**讀取時絕不能讓閘極電壓偏高**：read disturb 會誤觸隧穿把位元翻掉。

## 結案 -- 後果與影響
- **非揮發性儲存革命**：快閃記憶體取代軟碟、磁光碟，並在 2010 年代開始蠶食硬碟市場——筆電與資料中心全面轉向 SSD。
- **行動裝置的命脈**：iPod（2001 起）、USB 隨身碟、智慧型手機的儲存，全都建立在 NAND 之上；沒有 NAND 就沒有口袋裡的 TB 級手機。
- **2D → 3D 轉型**：NAND 是第一個平面微縮終結的記憶體，3D 堆疊（V-NAND）證明「往上蓋樓」可行，為 3D DRAM 與 3D 邏輯提供了路線圖。
- **東芝 → Kioxia**：舛岡的發明讓東芝成為 NAND 鼻祖；2017 年記憶體部門獨立為 Kioxia（鎧俠）。Samsung、SanDisk/Western Digital、Micron、SK Hynix 競逐至今，NAND 是產值數百億美元的戰場。
- **訴訟的注腳**：舛岡曾因專利貢獻未獲足夠回報而控告東芝，2007 年獲判約 8.7 億日圓——發明人與公司的利益分配，本身也是半導體史的一課。

## 關鍵人物與文獻
- **舛岡富士雄**（Fujio Masuoka）：東芝，1980 年提出 Flash 構想，1984 年 ISSCC 發表 NOR 前身技術，1987 年 ISSCC 發表 NAND（被稱為「NAND 之父」）。
- **Dov Frohman-Bentchkowsky**：Intel，1971 年發明浮閘 EPROM（US 專利 3,660,819）。
- D. Kahng & S. M. Sze, "A floating gate and its application to memory devices," *Bell Syst. Tech. J.*, 1967（浮閘概念源頭）。
- F. Masuoka et al., "New Ultra High Density EPROM and Flash EEPROM with NAND Structure Cell," IEDM 1987；IEEE ISSCC 1989 NAND 论文。
- R. Fowler & L. Nordheim, "Electron Emission in Intense Electric Fields," *Proc. Royal Soc. A*, 1928（FN 隧穿原始論文）。
