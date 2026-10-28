# 2014 Michael Stonebraker —— 兩次資料庫革命的總工程師

> 「別人一生做好一個資料庫，他做了四個，而且每次都故意
> 打臉上一次。2010 年代 NoSQL 大戰中，他是最固執的
> 『關聯派衛道士』。」

## 案件檔案

| 項目 | 內容 |
|---|---|
| 得主 | Michael Stonebraker (1943–) |
| 得獎理由 | 關聯式資料庫的基礎系統與實務影響（Ingres、Postgres） |
| 關鍵詞 | Ingres、Postgres、C-Store/Vertica、H-Store/VoltDB |

## 前因

1970s，Codd 的理論（1981 案）需要**實體證明**：關聯模型
的效能是否真的可行？Berkeley 的 Stonebraker 接下這個
工程賭注。

## 線索與推理

### 線索一：Ingres（1973–1985）

與 System R（IBM，Gray 1998 案）平行的學術實作：

```
QUEL 查詢語言（比 SQL 更代數化）
查詢最佳化：動態規劃枚舉連接順序（worst-case 指數 → 剪枝）
結局：公開原始碼 → Ingres 公司、Sybase、SQL Server
  的血緣皆溯於此（「伯克利的分封體系」）
```

### 線索二：Postgres（1986–）—— 自我推翻

Stonebraker 判決：**第一代關聯模型太瘦**——只會存
「數字與字串」。Postgres 引入：

```
ADT（抽象資料型別）：可自訂型別與運算子
繼承、複雜物件、規則系統（active database）
PostGIS、JSONB 等延伸的基礎 → 今日地理/文件混合場景的主流
```

### 線索三：2010 年代的四連發

| 系統 | 挑戰的教條 | 理論 |
|---|---|---|
| C-Store/Vertica | 行儲存萬能 | 列儲存 + 壓縮 → 分析型查詢 10–100× |
| H-Store/VoltDB | 磁碟為王 | 主記憶體 + 單線程分區 → OLTP 極速 |
| SciDB | 「關聯包打天下」 | 陣列資料庫（科學計算） |
| DBOS | OS 與 DB 分家 | 以資料庫為作業系統核心 |

### 線索四：與 NoSQL 的論戰

2010 年 Stonebraker 連發檄文（「MapReduce 是倒退」等），
主張：NoSQL 犧牲一致性與代數是**技術倒退**；真相是
「分區 + 列儲存 + 記憶體」等工程手段已解決規模問題。
2020s 的實務（NewSQL、分散式 SQL）大體站在他這邊。

## 理論評析

Stonebraker 的元方法論：**「工作負載決定架構」**。

```
OLTP（小而多的事務）→ 行儲存、B+Tree、鎖
OLAP（大而少的分析）→ 列儲存、向量化、無鎖掃描
一刀切的 universal DBMS 必然妥協 —— one size does NOT fit all
```

此命題直接對抗 1981 案的「通用關聯王國」夢想，構成
資料庫史的最大張力。

## 後果

- Postgres 成為開源資料庫之王（2020s 開發者調查
  常年最受歡迎）。
- 列儲存思想進入 Parquet、DuckDB、ClickHouse——
  大數據的隱性基礎設施。

## 關聯案件

→ [1981-Edgar-Codd](1981-Edgar-Codd.md)、[1998-Jim-Gray](1998-Jim-Gray.md)、[1973-Charles-Bachman](1973-Charles-Bachman.md)
