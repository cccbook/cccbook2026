# 資料庫 -- AI 偵探風格

以「推理探案」的方式，追查資料庫六十年（1961–2012）的每一場危機與轉身：
前因是什麼？線索在哪裡？推理如何展開？後果又如何改變了整個世界？

本卷特別追蹤**三位圖靈獎得主的貢獻**——Bachman（1973）、Codd（1981）、Gray（1998）、
Stonebraker（2014）——每一屆得主都改寫了這門學科的一章。

核心謎題只有一個：**「資料」到底是什麼？它如何被組織、查詢、保護與分佈？**

## 案件卷宗（歷史年表）

### 導航時代：層次與網路模型（1961 – 1969）

| 年份 | 事件 | 圖靈獎 | 檔案 |
|------|------|--------|------|
| 1961 | IBM 的 IMS——**層次資料庫與阿波羅計畫** | — | [1961-IBM層次資料庫.md](1961-IBM層次資料庫.md) |
| 1969 | Bachman 的網路模型——**集合關係與導航式查詢** | Bachman（1973，首位資料庫得主） | [1969-巴赫曼網路模型.md](1969-巴赫曼網路模型.md) |

### 關聯式革命：數學取代導航（1970 – 1979）

| 年份 | 事件 | 圖靈獎 | 檔案 |
|------|------|--------|------|
| 1970 | Codd 的關聯式模型——**關聯代數與資料獨立** | Codd（1981） | [1970-科德關聯式模型.md](1970-科德關聯式模型.md) |
| 1974 | Chamberlin 與 Boyce 的 SEQUEL——**SQL 的誕生** | — | [1974-錢柏林SQL.md](1974-錢柏林SQL.md) |
| 1974 | Stonebraker 的 Ingres——**大學版關聯式原型** | Stonebraker（2014） | [1974-斯東布雷克Ingres.md](1974-斯東布雷克Ingres.md) |
| 1976 | Peter Chen 的 ER 模型——**資料庫設計的統一語言** | — | [1976-陳氏實體關係模型.md](1976-陳氏實體關係模型.md) |
| 1979 | Oracle V2——**第一個商業化 SQL 資料庫** | — | [1979-甲骨文ORACLE.md](1979-甲骨文ORACLE.md) |

### 交易與容錯：ACID 的誕生（1981 – 1995）

| 年份 | 事件 | 圖靈獎 | 檔案 |
|------|------|--------|------|
| 1981 | Jim Gray 的交易概念——**ACID 與兩階段提交** | Gray（1998） | [1981-葛雷交易ACID.md](1981-葛雷交易ACID.md) |
| 1986 | Stonebraker 的 Postgres——**物件關聯式資料庫** | Stonebraker（2014） | [1986-波斯特Postgres.md](1986-波斯特Postgres.md) |
| 1995 | MySQL——**開源資料庫與 Web 時代** | — | [1995-MySQL開源資料庫.md](1995-MySQL開源資料庫.md) |

### 分佈時代：NoSQL 與 NewSQL（2000 – 2012）

| 年份 | 事件 | 圖靈獎 | 檔案 |
|------|------|--------|------|
| 2000 | Brewer 的 CAP 猜想——**分佈式的三選二** | （2002 Gilbert/Lynch 證明） | [2000-布魯爾CAP定理.md](2000-布魯爾CAP定理.md) |
| 2005 | Stonebraker 的《One Size Fits All?》——**列存與分析型工作負載** | Stonebraker（2014） | [2005-斯東布雷克柱狀儲存.md](2005-斯東布雷克柱狀儲存.md) |
| 2007 | Amazon 的 Dynamo——**鍵值儲存與最終一致性** | — | [2007-迪納摩Dynamo.md](2007-迪納摩Dynamo.md) |
| 2012 | Google 的 Spanner——**全球資料庫與 TrueTime** | — | [2012-谷歌Spanner全球資料庫.md](2012-谷歌Spanner全球資料庫.md) |

## 四大歷史脈絡

1. **資料模型（IMS/Bachman → Codd → Stonebraker）**：從導航到數學，再從「一個尺寸」到「各得其所」。
2. **查詢語言（關聯代數 → SQL）**：宣告式語言「說你要什麼，不說怎麼拿」的五十年統治。
3. **容錯與交易（Gray → Spanner）**：從 ACID 到 TrueTime，崩潰與分區永遠是敵人。
4. **分佈（CAP → Dynamo → Spanner）**：從理論三選二，到工程上用硬體與 Paxos 繞路。

## 圖靈獎主線

$$\text{Bachman（1969，網路模型）} \to \text{Codd（1970，關聯式）} \to \text{Gray（1981，交易 ACID）} \to \text{Stonebraker（1974/1986/2005，Ingres/Postgres/列存）}$$

## 關鍵人物年表

| 年代 | 人物 | 貢獻 | 圖靈獎 |
|------|------|------|--------|
| 1961 | IBM（Vernon Watts 等） | IMS 層次資料庫 | — |
| 1969 | Charles Bachman | 網路模型、DBTG 報告 | 1973 |
| 1970 | Edgar F. Codd | 關聯式模型、關聯代數 | 1981 |
| 1974 | Donald Chamberlin / Raymond Boyce | SEQUEL（SQL） | — |
| 1974 | Michael Stonebraker | Ingres、QUEL | 2014 |
| 1976 | Peter Chen（陳品山） | ER 模型 | — |
| 1979 | Larry Ellison | Oracle V2 商業化 | — |
| 1981 | Jim Gray | ACID、兩階段提交、WAL | 1998 |
| 1986 | Michael Stonebraker | Postgres、物件關聯式 | 2014 |
| 1995 | Michael Widenius | MySQL、LAMP | — |
| 2000 | Eric Brewer | CAP 猜想 | — |
| 2005 | Michael Stonebraker / David Dewitt | 列存、《One Size Fits All?》 | 2014 |
| 2007 | Amazon（DeCandia 等） | Dynamo、一致性雜湊 | — |
| 2012 | Google（Corbett 等） | Spanner、TrueTime | — |
