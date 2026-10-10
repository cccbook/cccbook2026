# 1951 - UNIVAC 商業電腦

## 案件摘要
1951 年，UNIVAC I（UNIVersal Automatic Computer I）正式交付美國人口普查局，成為第一部商業化量產的電子電腦。1952 年它在電視上預測艾森豪勝選，一夕成名，宣告「商業資料處理」時代的誕生。

## 前因 -- 為什麼會有這個案子
- Eckert 與 Mauchly 在完成 ENIAC 後，於 1946 年離開賓州大學（因專利歸屬爭議），1947 年創立 **Eckert–Mauchly Computer Corporation（EMCC）**，目標是造出「能賣的」電腦。
- 他們承接了 EDVAC 的儲存程式設計理念，並於 1948–1949 年建造 BINAC（Northrop 訂購）作為練習。
- 資金壓力巨大：造電腦的成本遠超預期，靠訂金與借貸苦撐。

商業模型的困境可以用不等式刻劃：

$$\text{成本}(C_i) > \sum_{j \le i} \text{訂金}_j \quad \Rightarrow \quad \text{持續的現金流危機}$$

## 線索與推理 -- 數學式、程式、理論

### 定義：UNIVAC I 規格
| 項目 | UNIVAC I |
|---|---|
| 首台交付 | 1951 年 3 月，美國人口普查局 |
| 記憶體 | 1000 字組，汞延遲線（每字組 12 字元） |
| 輸入/輸出 | UNISERVO 磁帶機、打孔卡 |
| 加法速度 | 約 2,250 次/秒 |
| 售價 | 約 100–150 萬美元 |
| 總產量 | 約 46 台 |

### Remington Rand 收購
- EMCC 財務無法支撐，1950 年 2 月被**Remington Rand** 收購（1955 年 Remington Rand 又與 Sperry 合併為 Sperry Rand）。
- Eckert 與 Mauchly 保留技術主導權，繼續完成 UNIVAC。
- 副作用：1950 年代後期，Sperry Rand 以 ENIAC 專利控告其他電腦廠商（Honeywell 案），1968 年法院判決 ENIAC 專利無效（因 ENAIC 概念早有先例如 Atanasoff–Berry Computer），終結了電腦專利壟斷。

### 1952 年總統大選預測的成名
- CBS 電視台租用 UNIVAC，在 1952 年 11 月 4 日開票夜進行即時預測。
- UNIVAC 根據早期開票率外推，預測 **Eisenhower**（艾森豪）將以 438 張選舉人票大勝 Stevenson（只給 Stevenson 93 票）。
- 因結果太懸殊，CBS 不敢播出，人工改成「8:7 险勝」的假數據；最終實際結果 442:89，UNIVAC 幾乎命中。
- 預測模型本質是外推：以開票比例 $p_i$ 加權外推各州選票

$$\hat{E} = \sum_{\text{州}} \frac{\text{已開票}(s)}{\text{總票數}(s)}^{-1} \cdot \text{投票傾向}(s)$$

（細節為商業機密，但精神是樣本比例的統計外推。）

這是電腦第一次在大眾媒體上展現「預測未來」的能力，公共形象從「軍用計算器」轉為「萬能的資料處理機」。

### 磁帶取代打孔卡
- UNIVAC 配備 UNISERVO 磁帶機，速度約每秒 7,200 字元，遠快於讀卡機。
- 磁帶是順序存取媒體，適合「批次處理」：排序→合併→報表，正是商業資料處理的骨架。

$$\text{讀卡機} \approx 250\ \text{卡/s} \times 80\ \text{字元} = 2\times10^4\ \text{字元/s? 不——實際僅約 } 2\times10^2\text{–}10^3\ \text{字元/s} \ll \text{磁帶 } 7.2\times10^3\ \text{字元/s}$$

磁帶讓「大量交易記錄的批次彙總」成為日常，會計、薪資、庫存首次自動化。

### Python 對照：批次處理的縮影
```python
# UNIVAC 式批次處理：讀入交易磁帶（串列）、排序、彙總、輸出報表
records = [("C01", 120), ("C03", 80), ("C01", 200), ("C02", 50)]
records.sort(key=lambda r: r[0])                 # 排序（UNIVAC 用合併排序）
total = {}
for cust, amt in records:                        # 依序掃描磁帶
    total[cust] = total.get(cust, 0) + amt       # 彙總
for cust, amt in total.items():                  # 報表
    print(f"{cust}: {amt}")
# C01: 320 / C02: 50 / C03: 80
```

## 結案 -- 後果與影響
- UNIVAC I 證明電腦可以是「商品」，開啟了電腦產業：IBM 在 1952 年推出 IBM 701 應戰，隨後以 IBM 702/704 系列在商業市場反超。
- 「電腦預測選舉」成為媒體常態，資料科學與民調預測的精神先聲。
- 商業資料處理（批次、磁帶、報表）成為 1950–60 年代企業 IT 的主流樣貌，直接孕育了 COBOL（1959）的誕生動機。
- Remington Rand 收購案與之後的 Honeywell 訴訟，確立了「電腦硬體思想不應被專利壟斷」的法律先例。

## 關鍵人物與文獻
- **J. Presper Eckert、John Mauchly**：EMCC 創辦人，UNIVAC 總設計師。
- **Grace Hopper**：在 Remington Rand 開發 UNIVAC 的 A-0 編譯器（1952）與 FLOW-MATIC，為 COBOL 鋪路。
- 文獻：Eckert, J. P., "A Survey of Digital Computer Memory Systems", *Proceedings of the IRE*, 1953；Stern, N., *From ENIAC to UNIVAC*, 1981。
