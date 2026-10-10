# 1978 - GDSII 版圖格式：把整顆晶片裝進一個檔案

## 案件摘要
1978 年，Calma 公司為其 GDS（Graphic Data System）數位化系統推出 **GDSII Stream Format**——
一種記錄式二進位格式，把版圖的層次結構（library / cell / boundary / path / sref）壓進單一檔案。
GDSII 在 1980 年代成為版圖交換的事實標準，至今仍是 tape-out 交棒給晶圓廠的統一語言。

## 前因 -- 為什麼會有這個案子
- **版圖資料各說各話**：1970 年代的 CAD 系統（Calma、Applicon、Auto-trol）各有私有的內部格式，設計公司與 mask house 之間交換版圖得靠磁帶「翻譯」，錯一個座標就整批報廢。
- **數位化儀器需要統一輸出**：Calma 的 GDS 數位化工作站（digitizer）把圖紙上的版圖轉成向量資料；要讓下游（製版機、光繪機、各家 CAD）讀得懂，必須有一個**中立、可串流（stream）**的格式——GDSII 由此誕生，「stream」意即資料以連續記錄（record）依序寫入磁帶。
- **層次化是唯一的救星**：一顆晶片的版圖由大量重複的單元（cell）構成——RAM 位元、標準閘、IO pad。若每個 instance 都展開成實際幾何，檔案大小為 $O(\text{geometry})$；若用**層次引用（sref / array）**，只需 $O(\text{instances})$：

$$
\text{壓縮率} = \frac{|\text{展開後幾何}|}{|\text{層次化描述}|} \approx \frac{N \cdot g}{N} = g \quad (g = \text{單元平均圖形數})
$$

一個 100 圖形的 RAM 位元被引用 10 萬次，層次化描述就省下約 **100 倍**的儲存量。
- **關鍵推理**：Calma 選擇「記錄式二進位 + 層次引用」而非純文字展開——磁帶空間與讀取速度都撐不住展開式描述，層次化結構同時解決儲存、傳輸與顯示三個問題。

## 線索與推理 -- 數學式、程式、理論

### 1. 案件現場：GDSII 的資料結構

GDSII 檔案是一棵樹：library 底下掛 cell，cell 底下掛元素（element）：

| 元素 | 意義 | 內容 |
|------|------|------|
| LIBRARY / BGNLIB | 檔案庫 | 名稱、時間戳 |
| STRUCTURE / BGNSTR | 單元（cell） | 名稱、時間戳 |
| BOUNDARY | 多邊形版圖 | LAYER、DATATYPE、XY 座標 |
| PATH | 走線（有寬度的線段） | LAYER、WIDTH、XY |
| SREF | 單元引用（instance） | SNAME、座標（可旋轉/鏡射） |
| AREF | 陣列引用 | SNAME、行列數、間距 |
| TEXT | 文字標註 | TEXTTYPE、字串 |
| ENDSTR / ENDLIB | 結尾記錄 | — |

層次引用 SREF/AREF 是 GDSII 的靈魂：單元只定義一次，被引用任意次。

### 2. 記錄式二進位格式：length + type + payload

每筆記錄的開頭是 4 個位元組：

$$
\underbrace{2\,\text{B}}_{\text{length（含 header）}} \; \underbrace{1\,\text{B}}_{\text{record type}} \; \underbrace{1\,\text{B}}_{\text{data type}} \; \underbrace{n\,\text{B}}_{\text{payload}}
$$

- **length**：含 4 位元組 header 在內的總長度（big-endian）。
- **record type**：如 0x00 HEADER、0x01 BGNLIB、0x05 BGNSTR、0x08 BOUNDARY、0x0C SREF、0x11 TEXT。
- **data type**：0x00 無資料、0x01 位元陣列、0x02 2-byte 整數、0x03 4-byte 整數、0x06 ASCII 字串、0x05 8-byte 實數。
- **座標系**：GDSII 座標是有號整數，以 **database unit**（如 1 nm）為刻度；**user unit**（如 1 μm）透過 UNITS 記錄換算：$\text{座標值} = \text{物理長度} / \text{db unit}$。例如 1.5 μm 線寬、db unit = 1 nm，座標值即 1500。

### 3. 層次化壓縮率的數學

設晶片含 $N$ 個 instance，每個 cell 平均 $g$ 個圖形（polygon）：

- **展開式**（flatten）：檔案大小 $S_{\text{flat}} \approx N \cdot g \cdot s$，其中 $s$ 為單一圖形的描述成本（8 個座標 × 4 bytes ≈ 32 B）。
- **層次化**（hierarchical）：$S_{\text{hier}} \approx (N + M \cdot g) \cdot s'$，其中 $M$ 為**不同** cell 的種類數、$s'$ 為含引用開銷的成本。當 $N \gg M$（重複率高）時：

$$
\frac{S_{\text{flat}}}{S_{\text{hier}}} \approx \frac{N \cdot g}{N + M \cdot g} \xrightarrow{N \to \infty} \frac{g}{M \cdot g / N} \;\approx\; \frac{N}{M} \;\text{倍}
$$

DRAM、SRAM、快閃記憶體的 $N/M$ 比可達數千以上——這就是為什麼 GDSII 存得下整顆晶片。
- **代價**：下游工具（DRC、mask writer）往往需要 flatten 後的幾何才能正確處理；flatten 之後檔案又爆回 $O(\text{geometry})$，於是 **quadtree / clip**（空間切割）登場。

### 4. Quadtree 與 clip：處理超大版圖

先進製程的 flatten 版圖動輒數百 GB，記憶體裝不下。解法是把版圖切成 tile（瓷磚），每個 tile 建一棵 quadtree：

- **quadtree**：把矩形遞迴四分，直到每個節點的圖形數低於門檻；查詢「點 $(x,y)$ 上有什麼圖形」為 $O(\log n)$，區域查詢為 $O(\sqrt{n} + k)$。
- **clip**：把跨越多個 tile 的圖形在 tile 邊界切開（clipping），每個 tile 可獨立處理（平行化、分散式運算）——mask data preparation（MDP）的工具（如 fracturing、shot assignment）都建立在此架構上。
- **層次化 DRC**：現代工具更進一步——不 flatten，直接在層次結構上做 DRC，只處理「每種 cell 一次」再複製結果；這是 1990s hierarchical verification 的核心思想。
- **時間戳與可重現性**：每個 BGNLIB/BGNSTR 記錄都帶修改與存取時間；儘管沒有實際功能意義，卻讓「同一份版圖經過誰的手」有跡可循——EDA 偵探追溯 tape-out 歷史時的第一條線索。

### 5. GDSII 的 UNITS 記錄與精度換算

GDSII 用 UNITS 記錄存兩個實數：$\text{db unit in user units}$ 與 $\text{db unit in meters}$，例如 $(0.001, 1\times10^{-9})$ 表示 1 user unit = 1 μm、1 db unit = 1 nm。所有座標都是有號整數乘以 db unit，因此精度由製程決定：0.35 μm 世代用 1 nm 足夠，EUV 世代圖形邊界需 0.1 nm 以下精度，UNITS 的選擇直接影響檔案大小與 mask writer 的解析成本。

### 6. 事實標準的誕生與接班

- **1980s 事實標準**：Calma GDSII 因「中立 + 可串流 + 層次化」被各家 CAD 與 mask house 採用；即便 Calma 公司本身（1981 年被 GE 收購）消逝，格式卻活了下來。
- **OASIS（2004, SEMI P39）**：GDSII 的二進位編碼冗餘（每個座標 4 bytes、每筆記錄 4 bytes header）在先進製程的巨型版圖上吃不消；SEMI 推出 OASIS，用變動長度整數（variable-length integer）與重複壓縮，檔案可小 10 倍以上。
- **GDSII 仍是 tape-out 標準**：儘管 OASIS 更優，GDSII 因相容性與工具支援度，至今仍是 foundry 交棒的首選格式——「舊但不死」的經典案例。
- **格式演進的偵探筆記**：從 GDS（1974）→ GDSII（1978）→ OASIS（2004），三代的演化主軸都是「更大的版圖逼出更緊的編碼」；判斷一個格式能否存活，看的不是技術優劣，而是生態系的慣性。

### 7. Python 實作：迷你 GDSII 記錄解析器

```python
import struct

RECORDS = {0x00: "HEADER", 0x01: "BGNLIB", 0x02: "LIBNAME", 0x04: "UNITS",
           0x05: "BGNSTR", 0x06: "STRNAME", 0x08: "BOUNDARY", 0x0D: "LAYER",
           0x0E: "DATATYPE", 0x10: "XY", 0x11: "ENDEL", 0x07: "ENDSTR"}

def parse_records(data):
    """逐筆解析 GDSII stream：4-byte header (length, type, datatype) + payload"""
    out, i = [], 0
    while i < len(data):
        length, rtype, dtype = struct.unpack('>HBB', data[i:i+4])
        payload = data[i+4:i+length]
        name = RECORDS.get(rtype, f"0x{rtype:02X}")
        if rtype == 0x10 and len(payload) >= 8:          # XY：成對 4-byte 座標
            pts = [struct.unpack('>ii', payload[j:j+8]) for j in range(0, len(payload) - 7, 8)]
            out.append((name, pts))
        elif rtype in (0x0D, 0x0E):                      # LAYER / DATATYPE
            out.append((name, struct.unpack('>H', payload)[0]))
        else:
            out.append((name, payload))
        i += length
    return out

def mini_boundary(layer, datatype, pts, db_unit_nm=1):
    """組一筆 BOUNDARY 記錄鏈：座標以 db unit 為刻度"""
    xy = b''.join(struct.pack('>ii', int(x / db_unit_nm), int(y / db_unit_nm)) for x, y in pts)
    recs = [(0x08, 0x00, b''), (0x0D, 0x02, struct.pack('>H', layer)),
            (0x0E, 0x02, struct.pack('>H', datatype)), (0x10, 0x03, xy), (0x11, 0x00, b'')]
    return b''.join(struct.pack('>HBB', 4 + len(p), t, d) + p for t, d, p in recs)

blob = mini_boundary(layer=1, datatype=0, pts=[(0, 0), (1500, 0), (1500, 800), (0, 800), (0, 0)])
print([r for r in parse_records(blob)])
# [('BOUNDARY', b''), ('LAYER', 1), ('DATATYPE', 0), ('XY', [(0, 0), (1500, 0), (1500, 800), (0, 800), (0, 0)]), ('ENDEL', b'')]
```

解析結果顯示：一個 1.5 μm × 0.8 μm 的長方形（db unit = 1 nm）被存成 LAYER=1、DATATYPE=0、五個座標點的 BOUNDARY 記錄鏈——GDSII 的全部祕密就在這 4-byte header 與層次引用之間。

## 結案 -- 後果與影響
- **tape-out 的統一語言**：設計公司把 GDSII 交給晶圓廠，晶圓廠以此為 mask data preparation（MDP）起點——fracturing、shot assignment、OPC 全部從 GDSII 出發。
- **EDA 工具間的互換格式**：Cadence Virtuoso、Synopsys ICC、Siemens Calibre、開源的 KLayout 與 gdspy，全都讀寫 GDSII；版圖在工具之間流通不再需要「翻譯」。
- **後進製程的檔案爆炸**：28 nm 世代 GDSII 約數十 GB，7 nm 以下破百 GB——OASIS 的壓縮與分散式 MDP（如 tiling + 雲端運算）正是為了治這個病。
- **層次化設計的催化劑**：SREF/AREF 引用讓「設計一次、引用千萬次」可行，直接影響後來的 hierarchical verification 與 hierarchical routing 思想。
- **OASIS 接班但 GDSII 不死**：2004 年 SEMI P39（OASIS）以更小的檔案接班，但 GDSII 因相容性至今仍是 tape-out 事實標準——一個 1978 年的格式，服役近半世紀。

## 關鍵人物與文檔
- **Calma 公司**：GDS 數位化工作站與 GDSII Stream Format（1978）的發明者；公司本身後被 GE（1981）、Valid（1988）輾轉收購，格式卻成為產業遺產。
- **SEMI**：OASIS 標準（SEMI P39, 2004）的制定單位，GDSII 的接班者。
- **KLayout / gdspy / gdstk**：開源社群的 GDSII 讀寫工具，讓這個 1978 年的格式在 Python 時代繼續被使用。
- **Calma, *GDSII Stream Format Manual*, 1978**（作業系統內部文件，後被業界廣泛流傳）。
- SEMI P39（OASIS）標準文件與 KLayout 官方文件：GDS→GDSII→OASIS 格式演進的第一手比較資料。
