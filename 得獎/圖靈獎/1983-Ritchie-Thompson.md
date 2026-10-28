# 1983 Dennis Ritchie & Ken Thompson —— UNIX：一座被低估的教堂

> 「兩位貝爾實驗室研究員，只為了想在一台淘汰的 PDP-7 上
> 玩『太空旅行』遊戲，順手寫下了作業系統與語言，改寫了
> 一切計算的歷史。」

## 案件檔案

| 項目 | 內容 |
|---|---|
| 得主 | Dennis M. Ritchie (1941–2011)、Ken Thompson (1943–) |
| 得獎理由 | 通用作業系統理論與 UNIX 的實作 |
| 關鍵詞 | UNIX、C 語言、管道 |

## 前因

1969 年貝爾實驗室退出 Multics 專案（目標過度膨脹的公用
電腦系統）。Thompson 手癢，在 PDP-7 上自寫簡化系統
（Unics：UNiplexed Information and Computing Service，
戲仿 Multics）。疑點：**Multics 敗於龐大，UNIX 為何成於簡小？**

## 線索與推理

### 線索一：哲學三原則

1. **一切皆檔案**（統一介面：磁碟、終端、管道皆同介面）
2. **小程式各司一職**
3. **以文字流組合**：

```
cat access.log | grep 404 | awk '{print $1}' | sort | uniq -c | sort -rn
```

管道（Thompson 1972/1973 發明）使程式如樂高——**組合性
取代客製**。這是 Bachman「領航員」（1973 案）的反面：
介面標準化勝過功能專門化。

### 線索二：C 語言（1972–73）

UNIX 自 Multics 時代起用組語。Ritchie 的決定性一步：
**用 C 重寫 UNIX（1973）**。C 的設計即「可攜的組語」：

```
指標＝位址運算（逼近機器）
指標算術 + 陣列衰減：p[i] ≡ *(p+i)
不藏抽象成本——「信任程式設計師」
```

K&R《The C Programming Language》（1978）以一個 hello, world
開場——成為此後所有語言入門書的儀式範本。C 成為跨界
通用語：Linux 核心到 Python 直譯器皆以 C 寫成。

### 線索三：可攜性革命

「一次撰寫、處處編譯」終結了每台機器重寫 OS 的史前時代。
1974 年 CACM 論文使 UNIX 為學界採用（AT&T 當時受反壟斷
限制不能賣軟體，**廉價授權給大學反而造就生態**——歷史的
反諷伏筆）。

## 理論評析

UNIX 的深層成功律：

```
簡單元件 + 強組合介面 > 複雜單體
（與 Hoare 的 CSP、網際網路的分層協定同構）
```

Thompson 另以 UTF-8（1992，與 Pike）終結字元編碼戰國，
以 B ( precursor of C) 與 Plan 9 留下更多足跡。

## 後果

- Linux（1991）、macOS、Android 核心皆 UNIX 系；雲端的
  底層是 UNIX 哲學的全面勝利。
- C 的語法成為 Java/JS/Go 的骨架——「花括號家族」。
- Thompson 晚年與 Pike 打造 Go（2009）：以 goroutine/channel
  兌現 CSP（1980 案）。

## 關聯案件

→ [1980-C.A.R.-Hoare](1980-C.A.R.-Hoare.md)、[1990-Fernando-Corbato](1990-Fernando-Corbato.md)、[1984-Niklaus-Wirth](1984-Niklaus-Wirth.md)
