# 1979 - 甲骨文 ORACLE（第一個商業化關聯式資料庫）

## 案件摘要
1979 年，**Larry Ellison（1944–）** 與 partners（Bob Miner、Ed Oates）
成立的 **Software Development Laboratories** 搶先出貨
**Oracle V2**——世界上**第一個商業化關聯式資料庫**：
$$\boxed{\text{第一個用 SQL 的商業關聯式資料庫，跑在 DEC PDP-11 上}}$$
**最諷刺的細節**：沒有 V1——**版本號直接從 2 開始**，
因為 Ellison 深信「沒有人要買 1.0 版的軟體」。
**更驚人的是**：這整個事業的起點，**是讀別人公開的論文**——
Ellison 團隊讀了 IBM System R 的研究論文（Finkelstein 的
優化器論文、Chamberlin 與 Boyce 的 SQL 論文），
**把 IBM 的想法搶先做成產品賣錢**。
$$\text{IBM 的論文（公開）} \xrightarrow{\text{Ellison 讀論文創業}} \text{Oracle V2 搶先出貨}.$$
**IBM 慢了嗎**？System R 技術領先，但 IBM 迟遲不推出商業版
（擔心蠶食自家 IMS 的市場）——**直到 1983 年才有 SQL/DS**。
**這是「論文公開 → 搶先商品化」的商業傳奇**。

## 前因 -- 為什麼會有這個案子
- **Codd 的關聯式模型（1970）**：
  **E. F. Codd（1923–2003）** 在 IBM 發表
  *A Relational Model of Data for Large Shared Data Banks*：
  $$\boxed{\text{資料 = 關係（表）；查詢 = 關係代數}}$$
  詳見 `1970-科德關聯式資料庫.md`——
  **理論已備，只欠工程**。
- **Chamberlin 的 SQL（1974）**：
  **Donald Chamberlin** 與 Raymond Boyce 在 IBM 發表
  SEQUEL（*Structured English Query Language*）：
  $$\text{關係代數（數學）} \xrightarrow{\text{SQL（1974）}} \text{人類可讀的查詢語言}.$$
  **SELECT ... FROM ... WHERE** 的語法就此誕生——
  見 `1974-錢柏林SQL.md`（稍後建立）。
- **IBM System R 的論文公開（1975–1979）**：
  IBM 的 System R 專案驗證了關聯式資料庫的**工程可行性**：
  - **優化器**：依統計資訊選擇最便宜的查詢計畫
    （Finkelstein 1979 論文——Ellison 團隊逐字研讀）；
  - **成本-based optimization**：
    $$\text{查詢} \xrightarrow{\text{優化器}} \text{最低成本的執行計畫}.$$
  **關鍵**：IBM 只發論文、不賣產品——
  **論文成了 Ellison 的「免費研發報告」**。
- **Stonebraker 的 Ingres（1974）**：
  Berkeley 的 **Stonebraker** 做 Ingres（學術原型，QUEL 語言）——
  見 `1974-斯東布雷克Ingres.md`（稍後建立）。
  **學術界做原型，Ellison 做商品**——賽道不同，目標相同。
- ** Ellison 的洞察（1977）**：
  Ellison 在 Ampex 做過資料庫項目，看到 Codd 的論文後意識到：
  $$\boxed{\text{「關聯式資料庫是必然——誰先出貨，誰贏」}}$$
  他與 Miner、Oates 用 2,000 美元創業（Software Development Laboratories）——
  **目標：把 IBM 的想法做成 IBM 沒有的產品**。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：關聯式資料庫的銷售賣點
**Codd 的模型**：資料是**表**（關係），查詢是**關係代數**：
$$\pi_{\text{name}, \text{city}}\left(\sigma_{\text{amount} > 10000}(\text{customers} \bowtie \text{orders})\right)$$
- $\sigma$：選擇（WHERE）；$\pi$：投影（SELECT 欄位）；$\bowtie$：連接（JOIN）。
**客戶不需要懂數學**——SQL 把代數包成人類可讀的語法：
```sql
SELECT c.name, c.city FROM customers c JOIN orders o ON c.id = o.cust_id
WHERE o.amount > 10000;
```
$$\boxed{\text{SQL：數學（關係代數）→ 人類可讀 → 機器可執行}}$$
**這是 Oracle V2 的全部賣點**——客戶用 SQL 問資料庫問題，
**不需要寫程式**（對比 IMS/CODASYL 時代必須寫 COBOL 導航程式）。

### 第二條線索：優化器（Ellison 從論文學到的核心）
**System R 的革命**：同一個查詢有多種執行計畫，成本差**百倍**：
$$\text{計畫 1：全表掃描 } O(n) \quad vs \quad \text{計畫 2：索引查詢 } O(\log n)$$
**優化器**依**統計資訊**（表大小、索引、選擇性）選最低成本：
$$\text{Cost}(\text{計畫}) = \sum_i \text{I/O}_i + w \cdot \sum_i \text{CPU}_i$$
- **Finkelstein（1979）論文**描述了 System R 的 join-order 優化——
  **Ellison 團隊讀了，然後實現了它**。
  $$\text{IBM 的論文} \xrightarrow{\text{Oracle 實現}} \text{Oracle 的優化器}.$$
**這是「論文公開 → 商品化」的經典案例**——
**IBM 親手把核心技術免費送給了對手**。

### 第三條線索：V2 的工程選擇——PDP-11 與小型機
**Oracle V2（1979）跑在 DEC PDP-11**（16 位元小型機，64KB 記憶體）：
- **選小型機而非大型主機**：PDP-11 便宜（$10,000 vs 百萬美元）——
  **客戶買得起**；
- **用 FORTRAN 介面 + SQL**：讓 COBOL/FORTRAN 程式呼叫 SQL；
- **V2 的精簡**：64KB 只夠核心功能——
  $$\text{PDP-11（64KB）} + \text{SQL 核心} = \text{第一個商業 RDBMS}.$$
**對比 System R**：跑在 IBM 370 大型機上，技術更完整但**不賣**。
$$\boxed{\text{完整的產品不賣 vs 精簡的產品搶出貨——後者贏}}$$

### Python：模擬一個小型商業資料庫應用（SQL + 交易）

```python
# 1) 建立小型商業資料庫（模擬 Oracle V2 的客戶/訂單應用）
import sqlite3

conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.executescript("""
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY, cust_id INTEGER,
                     item TEXT, amount REAL,
                     FOREIGN KEY(cust_id) REFERENCES customers(id));
""")
cur.executemany("INSERT INTO customers VALUES (?,?,?)",
    [(1, "陳大明", "台北"), (2, "林小美", "台中"), (3, "王強", "高雄")])
cur.executemany("INSERT INTO orders VALUES (?,?,?,?)",
    [(101, 1, "印表機", 12000), (102, 1, "磁碟機", 25000),
     (103, 2, "終端機", 9000), (104, 3, "印表機", 12000)])
conn.commit()

print("SQL 查詢：每位客戶的訂單總額（JOIN + GROUP BY）")
cur.execute("""
SELECT c.name, c.city, COUNT(o.id), SUM(o.amount)
FROM customers c JOIN orders o ON c.id = o.cust_id
GROUP BY c.id ORDER BY SUM(o.amount) DESC
""")
for name, city, n, total in cur.fetchall():
    print(f"  {name}（{city}）：{n} 張訂單，總額 {total:,.0f} 元")

# 2) 交易（transaction）：轉帳必須原子性——全部成功或全部失敗
print("\n交易測試：訂單 105 開立（扣庫存 + 記帳，兩步必須同進退）")
try:
    cur.execute("INSERT INTO orders VALUES (105, 2, '伺服器', 80000)")
    raise ValueError("庫存不足！")   # 第二步失敗 → 整筆回滚
except ValueError as e:
    conn.rollback()                  # ROLLBACK：回到交易前的狀態
    print(f"  錯誤：{e} → ROLLBACK，訂單 105 已回滚")

cur.execute("SELECT COUNT(*) FROM orders WHERE id = 105")
print(f"  訂單 105 存在嗎？{bool(cur.fetchone()[0])}（原子性 ✓）")

# 3) 條件查詢：找出金額超過 10000 的訂單（WHERE）
print("\nSQL 查詢：金額 > 10,000 的訂單（WHERE）")
cur.execute("SELECT item, amount FROM orders WHERE amount > 10000 ORDER BY amount DESC")
for item, amt in cur.fetchall():
    print(f"  {item}：{amt:,.0f} 元")

conn.close()
```
輸出：
```
SQL 查詢：每位客戶的訂單總額（JOIN + GROUP BY）
  陳大明（台北）：2 張訂單，總額 37,000 元
  王強（高雄）：1 張訂單，總額 12,000 元
  林小美（台中）：1 張訂單，總額 9,000 元

交易測試：訂單 105 開立（扣庫存 + 記帳，兩步必須同進退）
  錯誤：庫存不足！ → ROLLBACK，訂單 105 已回滚
  訂單 105 存在嗎？False（原子性 ✓）

SQL 查詢：金額 > 10,000 的訂單（WHERE）
  磁碟機：25,000 元
  印表機：12,000 元
  印表機：12,000 元
```

## 結案 -- 後果與影響
- **資料庫產業的誕生（1979 → 1980s）**：
  $$\boxed{\text{Oracle V2（1979）：資料庫從學術論文變成產業}}$$
  1980 年代競爭者湧現：
  - **dBASE（Ashton-Tate，1980）**：PC 上的資料庫（非關聯式，xBase 語言）；
  - **DB2（IBM，1983）**：IBM 終於出貨（MVS 大型機，SQL）——
    **慢了四年**；
  - **Sybase（1984）**：client/server 架構的先驅。
    $$\text{Oracle（1979）} \xrightarrow{\text{dBASE（1980）、DB2（1983）、Sybase（1984）}} \text{資料庫產業}.$$
- **SQL 的商業勝利（1986）**：
  ANSI 於 1986 年把 SQL 訂為**標準**（SQL-86）——
  **QUEL 消失了**（Ingres 最終也改用 SQL）。
  $$\text{SQL（1974）} \xrightarrow{\text{Oracle V2（1979）}} \text{ANSI 標準（1986）} \xrightarrow{} \text{無人能取代}.$$
  **今天的 SQL**：SQLite（手機）、PostgreSQL、MySQL（網站）、
  BigQuery、Snowflake（雲端）——**50 年不敗**。
- **Oracle 成為軟體巨頭**：
  $$\text{2,000 美元創業（1977）} \xrightarrow{\text{Oracle V2（1979）}} \text{市值數千億美元}.$$
  Ellison 的策略——**讀論文、搶出貨、跨平台**（V3 重寫為 C 語言，
  跑遍所有機型）——成為軟體創業的教科書。
  1986 年 Oracle 上市（NASDAQ）——**Ellison 成為世界首富候選人之一**。
- **「論文公開 → 商品化」的模式**：
  $$\text{System R 的論文} \xrightarrow{\text{Oracle}} \text{商業產品} \xrightarrow{\text{SQL 標準}} \text{產業}.$$
  **這不是抄襲**——論文公開本來就是科學的義務；
  **這是「誰把想法變成產品，誰贏」的商業法則**。
  同樣的模式：Apple GUI（Xerox PARC 的論文/原型）、
  Google MapReduce（DFS 的想法）。
- **交易的伏筆**：
  V2 的交易處理簡陋（沒有 WAL、沒有完整的崩潰恢復）——
  **容錯的理論基石要等 Jim Gray**（1981）——
  見 `1981-葛雷交易ACID.md`。
- **理論的迴響**：
  從 Codd（1970）到 Ellison（1979）到圖靈機（1936）的長鏈：
  $$\text{圖靈機（1936）：可計算} \xrightarrow{} \text{Codd（1970）：可查詢} \xrightarrow{} \text{Oracle（1979）：可銷售}.$$
  **一切從那條無限長的紙帶開始**。

## 關鍵人物與文獻
- **L. Ellison**：Oracle V2（1979）——讀 System R 論文創業，搶先出貨。
- **E. F. Codd**：*A Relational Model of Data for Large Shared Data Banks*（1970）——關聯式模型的創世紀。
- **D. Chamberlin & R. Boyce**：SEQUEL 論文（1974）——SQL 的誕生。
- **S. Finkelstein**：System R 優化器論文（1979）——Ellison 團隊的核心教材。
- **B. Miner & E. Oates**：Oracle 的共同創辦人——Miner 是 V2 的工程靈魂。
- **M. Stonebraker**：Ingres（1974）——學術賽道的平行發展。
- 相關案件：`1970-科德關聯式資料庫.md`、`1974-斯東布雷克Ingres.md`（稍後建立）、
  `1981-葛雷交易ACID.md`、`1986-波斯特Postgres.md`、`../資訊科學/1936-圖靈機.md`。
