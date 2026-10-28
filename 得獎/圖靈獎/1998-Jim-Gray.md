# 1998 Jim Gray —— 事務的數學家與資料海洋的失蹤者

> 「資料庫的一筆轉帳涉及兩台機器、中途斷電怎麼辦？Jim Gray
> 用『事務』與『日誌』回答了這題，然後在 2007 年獨自駕船
> 消失於太平洋——至今仍是計算機科學最著名的懸案。」

## 案件檔案

| 項目 | 內容 |
|---|---|
| 得主 | James N. Gray (1944–2007 失蹤) |
| 得獎理由 | 事務處理與資料庫系統的奠基貢獻 |
| 關鍵詞 | ACID、兩階段提交、System R、Terraserver |

## 前因

1970s，Codd 的關聯模型（1981 案）給了「資料」形狀，
但**「多個使用者同時讀寫、機器隨時當機」的正確性**尚無
理論。Gray 在 IBM System R 團隊面對的正是這個缺口。

## 線索與推理

### 線索一：事務與 ACID（1970s–80s）

```
Atomicity  原子性：全做或全不做（用 undo log 回滾）
Consistency 一致性：事務把資料庫從一合法狀態帶到另一合法狀態
Isolation  隔離性：併發事務互不看見中間狀態（鎖協定）
Durability 持久性：commit 後斷電不丟（WAL 先寫日誌）
```

**Write-Ahead Logging** 定律：先寫日誌、後寫資料頁——
崩潰恢復的全部密訣（重做/回滾皆以日誌為準）。

### 線索二：兩階段鎖與隔離等級

2PL 規則：所有鎖在事務結束才釋放 → 可序列化
（serializability = 併發結果等價於某種串行順序）。
Gray 與 Lorie 等提出隔離等級的務實階梯：

```
SERIALIZABLE > REPEATABLE READ > READ COMMITTED > READ UNCOMMITTED
效能與正確性的滑桿 —— SQL 標準採用
```

### 線索三：兩階段提交（與 Lampson 1992 案交會）

分散式事務的原子性協定（見 1992 案詳述）。Gray 並提出
著名的**容錯估算**：

```
MTBF 公式：系統可用性 = MTBF / (MTBF + MTTR)
千節點叢集若單機年故障率 1% → 每四天壞一台 →
  「軟體必須把故障當常態」（Fail-fast + 冗餘 + 檢查點）
```

### 線索四：從 OLTP 到資料海洋

Gray 晚年推動 Terabyte 專案、SkyServer（天文資料庫）、
並寫下《The Fourth Paradigm》（2007）：**科學第四範式
= 資料密集型科學**（實驗、理論、模擬之外）——
預言了今日大數據與資料科學。

## 懸案：2007 年 1 月 28 日

Gray 獨自駕 40 呎帆船 Tenacious 自舊金山出發，往 Farallon
群島撒母親骨灰，失蹤。史上最大規模民間海上搜救（含
衛星影像群眾外包）無果。海洋學家推測：船體失事沉沒於
深水區。**資料庫之父消失於無法恢復的儲存介質中。**

## 後果

- ACID 進入所有資料庫與區塊鏈設計詞彙。
- 「第四範式」成為資料科學學科的命名依據。
- Base（捨棄 C 的隔離）與 NoSQL 運動是對 ACID 教條的
  重新談判（2014 案）。

## 關聯案件

→ [1981-Edgar-Codd](1981-Edgar-Codd.md)、[1992-Butler-Lampson](1992-Butler-Lampson.md)、[2013-Leslie-Lamport](2013-Leslie-Lamport.md)
