# 1995 - MySQL 開源資料庫（Web 時代的資料庫基石）

## 案件摘要
1995 年，瑞典 **Michael Widenius（暱稱 Monty，1962–）** 與 **David Axmark** 
首次公開發行 **MySQL**——一個**開源的關聯式資料庫**：
$$\boxed{\text{免費 + 開源 + 夠快 + 夠簡單 = Web 時代的資料庫}}$$
**MySQL 的破案關鍵**不是技術最深，而是**取捨精準**：
- **犧牲**部分transaction功能與複雜查詢的最佳化；
- **換來**極致的簡單、速度與零成本部署。
到了 2000 年代，**LAMP 架構**（Linux + Apache + MySQL + PHP）成為
**一切動態網站的標準配方**：
$$\text{Linux} + \text{Apache} + \text{MySQL} + \text{PHP} = \text{Web 1.0/2.0 的引擎}.$$
**在 Postgres 開源的同年（1995），資料庫史上最成功的開源案例悄悄上路**——
**全世界超過一半的網站後端，都曾跑在這個瑞典人寫的資料庫上**。

## 前因 -- 為什麼會有這個案子
- **Codd 的關聯式模型（1970）**：
  **E. F. Codd** 提出關聯式模型，SQL（1974）成為標準語言
  （見 `1970-科德關聯式模型.md`、`1974-錢柏林SQL.md`）。
  但 1990 年代的**商業資料庫**（Oracle、DB2、Sybase）**昂貴無比**：
  $$\text{一套 Oracle 授權} \approx \text{數萬美元} \Rightarrow \text{個人與小公司買不起}.$$
- **Postgres 的先聲（1986）**：
  **Stonebraker** 的 Postgres（見 `1986-波斯特Postgres.md`）證明
  **學術界可以做出先進的資料庫**，並於 **1995 年開源**（更名 PostgreSQL）——
  但 Postgres 當時**偏重功能先進性**，部署門檻較高。
  $$\text{Postgres（1995）：先進但重} \xrightarrow{\text{同年}} \text{MySQL（1995）：簡單但快}.$$
- **Web 的爆炸（1991–1995）**：
  **Tim Berners-Lee** 的全球資訊網（1991，見 `../資訊科學/1997-恩格巴特超文字.md`
  的超文字思想譜系）在 1993–1995 年**爆發性成長**——
  動態網站需要**便宜、易裝、易學**的後端資料庫。
- **Linux 與開源生態（1991）**：
  **Linus Torvalds** 的 Linux（1991）提供**免費的作業系統**，
  Apache（1995）提供**免費的網頁伺服器**——
  只缺一塊：**免費的資料庫**。Monty 補上了這一塊。
- **Monty 的出身（1977–1995）**：
  Widenius 從 1977 年開始寫資料庫工具（unireg），
  他的哲學：**「速度第一，功能夠用就好」**——
  這與學院派（Postgres）的路線**截然相反**。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：關聯式模型的最小實作
**Codd 的模型**只需要：**表（table）、列（row）、欄（column）與關係運算**。
一個最小的 Web 應用只需要：
$$\text{SELECT（查詢）} + \text{INSERT（寫入）} + \text{簡單索引} \Rightarrow \text{90\% 的 Web 需求}.$$
**MySQL 的取捨**：把這 90% 做到**極快**，其餘 10%（複雜交易、子查詢）
**初期乾脆不做或做得很慢**——
$$\boxed{\text{夠用的功能} \times \text{極致的速度} \times \text{零成本} > \text{完整的功能} \times \text{昂貴}}$$

### 第二條線索：B+樹索引——速度的祕密
MySQL（MyISAM/InnoDB 引擎）用 **B+ 樹**做索引：
- **B+ 樹**：$m$ 階的平衡樹，**資料全在葉節點**，葉節點串成鏈表；
- 查詢複雜度：$O(\log_m N)$，且 $m$ 很大（數百），
  所以**樹高極小**：$N = 10^9$ 筆資料只需 **3–4 層**。
$$h \approx \lceil \log_m N \rceil \quad\text{（} m = 500,\ N = 10^9 \Rightarrow h = 4 \text{）}$$
**每次查詢只需 3–4 次磁碟 I/O**——這就是 MySQL「快」的數學基礎。

### 第三條線索：LAMP 的組合爆炸經濟學
**LAMP 全部免費**：
$$\text{成本}_{\text{LAMP}} = 0 \quad\text{vs.}\quad \text{成本}_{\text{商業堆疊}} \approx \text{數萬美元/伺服器}.$$
對一個要部署 **$n$ 台伺服器**的新創公司：
$$\text{省下} = n \times (\text{作業系統} + \text{伺服器} + \text{資料庫}) \approx n \times \$50{,}000.$$
**Web 2.0 世代（Facebook 2004、YouTube 2005、WordPress 2003）
全部從 LAMP 起家**——零成本堆疊讓**車庫創業**成為可能。

### Python：用 sqlite3 模擬小型 Web 應用資料庫
（以 Python 內建的 `sqlite3` 模擬 MySQL 時代 Web 應用的核心操作：
使用者註冊與留言板的 `INSERT` + `SELECT`。）

```python
import sqlite3

conn = sqlite3.connect(":memory:")
cur = conn.cursor()

# 1) 建表（使用者 + 留言）——Web 應用的標準 schema
cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
cur.execute("""CREATE TABLE comments
               (id INTEGER PRIMARY KEY, user_id INTEGER, body TEXT)""")

# 2) 使用者註冊（INSERT）
for name in ["Monty", "David", "Linus"]:
    cur.execute("INSERT INTO users (name) VALUES (?)", (name,))
conn.commit()

# 3) 留言寫入（INSERT，含外鍵關聯）
posts = [(1, "MySQL 1.0 釋出！"), (1, "速度第一！"),
         (2, "開源萬歲"), (3, "Linux 也免費")]
for uid, body in posts:
    cur.execute("INSERT INTO comments (user_id, body) VALUES (?, ?)", (uid, body))
conn.commit()

# 4) 查詢：留言板的 JOIN（關聯式模型的殺手級應用）
print("留言板（JOIN users + comments）：")
cur.execute("""SELECT users.name, comments.body
               FROM comments JOIN users ON comments.user_id = users.id
               ORDER BY comments.id""")
for name, body in cur.fetchall():
    print(f"  [{name}] {body}")

# 5) 查詢：每位使用者的留言數（GROUP BY 聚合）
print("\n每人留言數（GROUP BY）：")
cur.execute("""SELECT users.name, COUNT(*) AS cnt
               FROM comments JOIN users ON comments.user_id = users.id
               GROUP BY users.name ORDER BY cnt DESC""")
for name, cnt in cur.fetchall():
    print(f"  {name}: {cnt} 則")

# 6) 參數化查詢：防 SQL Injection 的正確姿勢
cur.execute("SELECT name FROM users WHERE name = ?", ("Monty",))
print(f"\n參數化查詢 Monty → {cur.fetchone()[0]}")
print("→ SELECT + INSERT + JOIN + GROUP BY = 小型 Web 應用的全部 ✓")
```
輸出：
```
留言板（JOIN users + comments）：
  [Monty] MySQL 1.0 釋出！
  [Monty] 速度第一！
  [David] 開源萬歲
  [Linus] Linux 也免費

每人留言數（GROUP BY）：
  Monty: 2 則
  David: 1 則
  Linus: 1 則

參數化查詢 Monty → Monty
→ SELECT + INSERT + JOIN + GROUP BY = 小型 Web 應用的全部 ✓
```

## 結案 -- 後果與影響
- **LAMP 支撐 Web 1.0/2.0（1998–2010）**：
  $$\boxed{\text{LAMP = Web 時代的「Wintel」}}$$
  Wikipedia、YouTube、Facebook、Twitter 的早期架構**全部依賴 MySQL**——
  **開源資料庫第一次戰勝商業巨頭**。
- **2008 Sun 收購——波折的開始**：
  **Sun Microsystems** 以 **10 億美元**收購 MySQL AB（2008）——
  Monty 說：「我希望 MySQL 永遠開源。」
- **2010 Oracle 收購——最壞的劇本**：
  Oracle（商用資料庫的宿敵）併購 Sun，**MySQL 落入死對頭手中**。
  **Monty 立刻分支出 MariaDB（2009）**（以小女兒 Maria 命名），
  Wikipedia、Google 等陸續**遷移到 MariaDB**——
  $$\text{MySQL（1995）} \xrightarrow{\text{Sun（2008）}} \text{Oracle（2010）} \xrightarrow{\text{Monty}} \text{MariaDB（2009–）}.$$
- **開源資料庫的勝利**：
  **PostgreSQL**（同年開源）與 **SQLite**（2000，全世界部署量最大的資料庫）
  與 MySQL **三足鼎立**——
  2010 年代，**開源資料庫在 Web 世界的市佔率超過 80%**。
- **通往分散式時代**：
  Web 規模成長後，**單機 MySQL** 撐不住——
  這直接催生了 **NoSQL 運動**（見 `2000-布魯爾CAP定理.md` 的理論基礎、
  `2007-迪納摩Dynamo.md` 的分散式設計）。
- 歷史定位：**Monty 是 Web 時代的 Codd 實踐者**——
  他證明**免費 + 開源 + 夠快**可以打敗**昂貴 + 封閉 + 完整**；
  $$\text{Codd（1970）} \xrightarrow{\text{Oracle（1979）}} \text{商業時代} \xrightarrow{\text{MySQL（1995）}} \text{開源時代}.$$
  **理論源自圖靈機（見 `../資訊科學/1936-圖靈機.md`）的可計算模型，
  而勝利屬於把它交到每個人手裡的人**。

## 關鍵人物與文獻
- **Michael Widenius（Monty）**：MySQL（1995）、MariaDB（2009）——Web 時代的資料庫推手。
- **David Axmark**：MySQL 共同創辦人——開源授權策略的設計者。
- **E. F. Codd**：關聯式模型（1970）——MySQL 的理論源頭。
- **Michael Stonebraker**：Postgres（1986/1995）——同年的另一條路線。
- **Linus Torvalds**：Linux（1991）——LAMP 的 L。
- 相關案件：`1986-波斯特Postgres.md`、`1970-科德關聯式模型.md`、
  `1974-錢柏林SQL.md`、`2000-布魯爾CAP定理.md`、`2005-斯東布雷克柱狀儲存.md`、
  `../資訊科學/1936-圖靈機.md`、`../資訊科學/1997-恩格巴特超文字.md`。
