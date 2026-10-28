# 1992 Butler Lampson —— 個人運算與分佈式系統的總設計師

> 「他參與設計了第一台個人電腦、乙太網、雷射印表機、
> 兩階段提交……圖靈獎史上『參與發明一切』的人。」

## 案件檔案

| 項目 | 內容 |
|---|---|
| 得主 | Butler W. Lampson (1943–) |
| 得獎理由 | 個人電腦與分佈式系統技術的貢獻（Xerox PARC 主持 Alto） |
| 關鍵詞 | Alto、分佈式系統、兩階段提交 |

## 前因

1960s 末，電腦是機構的資產。Lampson 1968 年備忘錄
《Why Alto?》論證：**每人一台完整的電腦**才是正確終點——
在 IBM 主機霸權時代這是異端。

## 線索與推理

### 線索一：Alto（1973）

Lampson 拍板的設計規格（Thacker 負責硬體，2009 案）：

```
位圖顯示 8.5×11"（模擬一頁紙）＋ 滑鼠 ＋ 乙太網 ＋ 硬碟
口號：「什麼都能做」的通用個人機
```

軟體層：Bravo 所見即所得編輯器（Charles Simonyi，後寫 Word）、
Smalltalk（Kay 2003 案）、星形辦公系統——**GUI 時代的全套
積木在此一次備齊**。Steve Jobs 1979 參觀後做出 Macintosh。

### 線索二：乙太網（與 Metcalfe、Boggs）

區域網路的仲裁理論：CSMA/CD——

```
先聽後說（carrier sense）、邊說邊聽（collision detect）、
衝突後指數退避（exponential backoff）
```

**用統計仲裁取代中央控制**——去中心化的工程範式（2022 案）。

### 線索三：資料庫事務與兩階段提交（2PC）

分佈式系統的核心難題：多機器如何對「是否提交」達成一致？

```
2PC：
  Phase 1：協調者問全部參與者「準備好了嗎？」（預寫 log）
  Phase 2：全部 YES → commit；任一 NO → abort
不變式：一旦有人準備好，協調者必能帶全系統到同一終局
代價：阻塞問題（協調者掛掉則參與者懸置）→ 啟發 3PC/Paxos
```

### 線索四：《Hints for Computer System Design》（1983）

把分散式系統工程整理成**經驗法則集**：「不要內建通用性」、
「先做能用的版本」、「快取一切」——系統設計第一次有了
可傳授的方法論。

## 理論評析

Lampson 案的主線索：**端到端論證（end-to-end argument）**
的實踐版——功能應放在端點而非網路中間。Alto 把「智慧」
放在個人端點，乙太網讓網路保持笨，2PC 讓一致性的責任
集中於協調點。三案看似相反，實為同一原則：**每層只做
自己不可替代的事**。

## 後果

- PARC 的禮物清單：GUI、乙太網、雷射印表機、所見即所得
  ——Xerox 未收割，世界收割。
- 事務與共識理論直接孕育 Google Spanner、Kafka 等雲端基礎。

## 關聯案件

→ [2009-Charles-Thacker](2009-Charles-Thacker.md)、[1998-Jim-Gray](1998-Jim-Gray.md)、[2013-Leslie-Lamport](2013-Leslie-Lamport.md)
