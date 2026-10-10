# 1986 - 波斯特 Postgres（物件關聯式資料庫）

## 案件摘要
1986 年，**Michael Stonebraker（1943–）** 在 Berkeley 啟動
**Postgres**（*Post-Ingres*）——Ingres 之後的第二戰場：
$$\boxed{\text{第一個物件關聯式資料庫（object-relational）——自訂型別・繼承・規則系統}}$$
**Stonebraker 的問題**：關聯式模型的表格太「平」——
真實世界的資料是**複雜物件**（地圖、CAD 圖形、文件、影像）：
$$\text{表格（平坦的行列）} \neq \text{真實資料（巢狀的複雜物件）}.$$
**他的解法**：**擴充關聯式模型**，而非推翻它——
- **自訂型別（ADT）**：使用者自己定義資料型別與函式；
- **繼承（inheritance）**：表可以繼承表（物件導向的思想進了資料庫）；
- **規則系統與觸發器**：資料庫主動反應（rules、triggers）。
$$\text{Ingres（1974）：關聯式} \xrightarrow{\text{Postgres（1986）}} \text{物件關聯式}.$$
**1995 年，Berkeley 把 Postgres 交棒給兩名學生**——
他們加上 SQL 直譯器，改名 **PostgreSQL**，開源釋出——
**至今最強的開源資料庫之一**。
**2014 年，Stonebraker 獲圖靈獎**——表彰他對資料庫
「概念與原型」的兩度革命（Ingres 與 Postgres）。

## 前因 -- 為什麼會有這個案子
- **Ingres 的成功與極限（1974–1985）**：
  見 `1974-斯東布雷克Ingres.md`（稍後建立）——
  Stonebraker 在 Berkeley 用 Ingres 證明了關聯式資料庫的工程可行性
  （QUEL 語言、關係代數的實現）。
  **但 Ingres 之後**，Stonebraker 問：**下一個問題是什麼？**
  $$\text{Ingres：證明 Codd 可行} \xrightarrow{10\text{ 年}} \text{關聯式已經贏了——然後呢？}$$
  1985 年，他把 Ingres 商業化交棒（Ingres Corporation），
  **回到 Berkeley 啟動 Postgres**。
- **新應用的複雜資料（1980s）**：
  1980 年代的新應用——**地理資訊系統（GIS）、CAD/CAM、影像文件**——
  資料不是「員工姓名、薪水」的平坦表格：
  $$\text{地圖上的多邊形、零件的幾何、影像的像素} = \text{複雜物件}.$$
  用關聯式表格存多邊形？**要拆成十幾個數字欄位**——查詢時再組合——
  $$\boxed{\text{「平的模型裝不下彎的世界」}}$$
- **Simula 的物件導向思想（1967）**：
  見 `../資訊科學/1967-達爾尼加德Simula.md`——
  **Dahl 與 Nygaard** 的 Simula 67 引入**類別、繼承、物件**：
  $$\text{類別（資料 + 操作封裝）} \xrightarrow{\text{Simula 67}} \text{物件導向} \xrightarrow{\text{Postgres}} \text{物件關聯式}.$$
  **物件 = 資料 + 方法**——這個思想從程式語言**移植到資料庫**：
  表格若能「知道自己的型別與操作」，就能存複雜物件。
- **Chen 的實體關係模型（1976）**：
  見 `1976-陳氏實體關係模型.md`（稍後建立）——
  **Peter Chen** 的 E-R 模型把「實體、屬性、關係」變成設計語言——
  $$\text{E-R 模型（1976）：實體與關係} \xrightarrow{\text{Postgres}} \text{關係可以是「實體」本身}.$$
  Chen 的「實體」與 Stonebraker 的「物件」是同源的概念。
- **物件導向資料庫的競爭（1980s）**：
  OODBMS 陣營（GemStone、ObjectStore）主張**推翻關聯式**、全面物件化——
  **Stonebraker 反對**：SQL 與關聯式的 20 年投資不能丟——
  $$\text{OODBMS：推翻} \quad vs \quad \boxed{\text{Postgres：擴充}}$$
  **歷史站在 Stonebraker 這邊**。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：型別系統的擴充（自訂型別 ADT）
**關聯式模型的型別**（內建、固定）：整數、字串、日期——
$$\text{屬性 } A \in \{\text{int}, \text{string}, \text{date}\}.$$
**Postgres 的擴充**：使用者自訂**抽象資料型別（ADT）**——
型別 = **內部表示 + 操作函式**：
$$\text{型別 } T = (\text{repr}_T,\ \text{ops}_T)$$
例如自訂「圓」型別：
$$\text{circle} = \left(\langle c_x, c_y, r\rangle,\ \{\text{area}, \text{contains}, \text{overlap}\}\right)$$
- 內部表示：圓心與半徑；
- 操作：面積、包含、相交——**使用者用 C 語言寫、動態載入**。
$$\boxed{\text{資料庫不再只認識內建型別——它認識你教它的型別}}$$
**查詢語言 POSTQUEL 直接呼叫**：
```
retrieve (s.name) where area(s.shape) > 50
```

### 第二條線索：複雜物件查詢與繼承
**繼承（inheritance）**：表可以有「父表」：
```sql
CREATE TABLE shapes (name text);
CREATE TABLE circles (r real) INHERITS (shapes);
```
查父表 `shapes` **自動包含**子表 `circles` 的所有列：
$$\text{shapes} \supseteq \text{circles} \quad\text{（查詢父表 = 查詢所有子類別）}$$
**這是 Simula 的類別階層直接搬到資料表**——
$$\text{Simula 67：類別繼承} \xrightarrow{\text{Postgres 1986}} \text{表格繼承}.$$
**複雜物件的查詢**：物件欄位可以**巢狀**（Postgres 早期版本支援
路徑表示式）：
$$\text{employee.address.city} \quad\text{（沿著物件路徑取值）}$$
**規則系統（rules）**：資料主動反應——
$$\text{ON INSERT INTO orders DO UPDATE inventory SET qty = qty - 1}$$
**這是觸發器（trigger）的前身**——資料庫從「被動的倉庫」
變成「主動的代理人」。

### 第三條線索：貝葉斯式的取捨——擴充而非推翻
**Stonebraker 的論證（1986）**：
$$\text{關聯式（ algebra + SQL）20 年的積澱} + \text{物件的表達力} = \text{物件關聯式}$$
**取捨**：
- **保留**：關係代數、SQL（後來）、事務、優化器——
  **20 年的理論與工程不能丟**；
- **新增**：自訂型別、繼承、規則——
  **表達複雜世界**。
$$\boxed{\text{革命有兩種：推翻（OODBMS）與擴充（Postgres）——後者活得久}}$$
**工程代價**：Postgres 的**規則系統**太慢（早期版本），**繼承**讓
優化器頭痛——**理想的擴充被現實折衷**（1995 交棒時大幅精簡）。
$$\text{理想（1986）} \xrightarrow{\text{工程現實}} \text{精簡（1995）} \xrightarrow{} \text{PostgreSQL 的務實路線}.$$

### Python：用 sqlite3 自訂函式/JSON 模擬物件關聯式查詢

```python
# 1) 自訂型別 + 複雜物件：用 JSON 模擬 Postgres 的物件欄位
import sqlite3, json

conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.execute("CREATE TABLE shapes (name TEXT, data TEXT)")  # data = 物件（自訂型別）
# data 欄位存「自訂型別」：circle / rect 物件（Postgres 允許這種複合型別）
objs = [
    ("紅圓",   json.dumps({"type": "circle", "cx": 0, "cy": 0, "r": 5})),
    ("藍矩形", json.dumps({"type": "rect", "x": 1, "y": 2, "w": 4, "h": 3})),
    ("綠圓",   json.dumps({"type": "circle", "cx": 10, "cy": 10, "r": 1})),
]
cur.executemany("INSERT INTO shapes VALUES (?,?)", objs)
conn.commit()

def area(data):        # 相當於 Postgres 的自訂函式（C 語言擴充 → 這裡用 Python）
    o = json.loads(data)
    if o["type"] == "circle":
        return 3.14159 * o["r"] ** 2
    return o["w"] * o["h"]

conn.create_function("area", 1, area)   # 註冊自訂函式 → SQL 可直接呼叫！

print("物件關聯式查詢：自訂函式 area() 算複雜物件面積")
cur.execute("SELECT name, data, area(data) FROM shapes ORDER BY area(data) DESC")
for name, data, a in cur.fetchall():
    o = json.loads(data)
    desc = f"半徑 {o['r']} 的圓" if o["type"] == "circle" else f"{o['w']}×{o['h']} 矩形"
    print(f"  {name}（{desc}）：面積 {a:.2f}")

# 2) 依「物件內部欄位」查詢：JSON 提取（模擬 Postgres 的路徑表示式 data->'type'）
print("\n查詢物件內部欄位（data->'type' = 'circle'）")
cur.execute("SELECT name FROM shapes WHERE json_extract(data, '$.type') = 'circle'")
print("  圓形物件：", [r[0] for r in cur.fetchall()])

# 3) 繼承（inheritance）：circles 表「繼承」shapes 表
print("\n繼承測試（Postgres：CREATE TABLE circles () INHERITS (shapes)）")
cur.execute("""CREATE TABLE circles (
    data TEXT CHECK(json_extract(data, '$.type') = 'circle')
)""")
cur.execute("INSERT INTO shapes VALUES ('紫圓', ?)",
    (json.dumps({"type": "circle", "cx": 3, "cy": 3, "r": 2}),))
cur.execute("SELECT name FROM shapes WHERE json_extract(data, '$.type') = 'circle'")
print("  shapes + 子類別的圓：", [r[0] for r in cur.fetchall()])
conn.close()
```
輸出：
```
物件關聯式查詢：自訂函式 area() 算複雜物件面積
  紅圓（半徑 5 的圓）：面積 78.54
  藍矩形（4×3 矩形）：面積 12.00
  綠圓（半徑 1 的圓）：面積 3.14

查詢物件內部欄位（data->'type' = 'circle'）
  圓形物件： ['紅圓', '綠圓']

繼承測試（Postgres：CREATE TABLE circles () INHERITS (shapes)）
  shapes + 子類別的圓： ['紅圓', '綠圓', '紫圓']
```

## 結案 -- 後果與影響
- **PostgreSQL 的誕生（1995）**：
  $$\boxed{\text{1995：Berkeley POSTgres 交棒給學生，開源釋出 PostgreSQL}}$$
  **兩名學生**：Andrew Yu 與 Jolly Chen 把 POSTQUEL 換成 **SQL 直譯器**，
  改名 **Postgres95 → PostgreSQL**——開源釋出（BSD 授權）。
  $$\text{Postgres（1986，Berkeley）} \xrightarrow{\text{學生交棒（1995）}} \text{PostgreSQL（開源）}.$$
- **至今最強開源資料庫之一（1995 → 2026）**：
  PostgreSQL 30 年由**全球社群**接力維護：
  - **JSON 支援（2012）**：物件關聯式的理想在 30 年後以 JSON 落地——
    $$\text{自訂型別（1986）} \xrightarrow{26\text{ 年}} \text{JSONB（2012）}——\text{理想成真}.$$
  - **GIS 的 PostGIS**：全球地理資訊系統的事實標準——
    **Postgres 原始目標（複雜資料）的勝利**；
  - **雲端時代的寵兒**：AWS Aurora、Google AlloyDB、Supabase——
    **都選 PostgreSQL 為基底**。
- **OODBMS 陣營的消亡**：
  $$\text{GemStone・ObjectStore（1980s）} \xrightarrow{\text{1990s 末}} \text{邊緣化}$$
  **Stonebraker 的「擴充而非推翻」贏了**——
  物件的思想（自訂型別、JSON、複合型別）**被吸進關聯式**，
  而非取代它。
- **Stonebraker 的圖靈獎（2014）**：
  $$\text{Ingres（1974）} + \text{Postgres（1986）} \xrightarrow{\text{2014}} \text{圖靈獎}$$
  **表彰**：對資料庫系統「概念與原型」的奠基貢獻——
  兩度革命、兩度交棒（Ingres 公司、PostgreSQL 社群）。
  **他也是 CQS 的反例演說家**：晚年推動 NewSQL 與
  「one size does not fit all」——見 `2012-谷歌Spanner全球資料庫.md`
  （稍後建立）的時代背景。
- **規則系統的遺產**：
  Postgres 的規則系統演變成**觸發器（triggers）**與
  **具體化視圖（materialized views）**——
  $$\text{rules（1986）} \xrightarrow{} \text{triggers・views（現代 SQL 標準）}.$$
- **開源的伏筆**：
  $$\text{PostgreSQL（1995，BSD）} \xrightarrow{\text{開源資料庫運動}} \text{MySQL（1995，GPL）}——\text{伏筆}$$
  同年開源的 **MySQL**（見 `1995-MySQL開源資料庫.md`，稍後建立）
  與 PostgreSQL 展開 30 年的雙雄競爭——
  **開源資料庫時代的兩位主角就此登場**。
- **理論的迴響**：
  $$\text{圖靈機（1936）：可計算} \xrightarrow{} \text{Codd（1970）：可查詢} \xrightarrow{} \text{Stonebraker（1974/1986）：可擴充}.$$
  **Ingres 證明了關聯式可行，Postgres 證明了關聯式可以進化**。

## 關鍵人物與文獻
- **M. Stonebraker**：*The Design of POSTGRES*（1986）；Ingres（1974）；
  Postgres（1986）；2014 圖靈獎；「one size does not fit all」。
- **O. Dahl & K. Nygaard**：Simula 67（1967）——物件導向思想（繼承的來源）。
- **P. Chen**：實體關係模型（1976）——實體概念的先驅。
- **A. Yu & J. Chen**：Postgres95（1995）——SQL 直譯器與開源釋出。
- **Lawrence Rowe**：Postgres 的共同研究者（Berkeley）。
- 相關案件：`1974-斯東布雷克Ingres.md`（稍後建立）、
  `../資訊科學/1967-達爾尼加德Simula.md`、`1976-陳氏實體關係模型.md`（稍後建立）、
  `1979-甲骨文ORACLE.md`、`1981-葛雷交易ACID.md`、`1995-MySQL開源資料庫.md`（稍後建立）、
  `../資訊科學/1936-圖靈機.md`。
