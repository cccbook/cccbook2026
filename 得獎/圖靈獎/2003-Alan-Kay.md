# 2003 Alan Kay —— 「預測未來最好的方式就是發明它」

> 「PARC 的夢想家：他想造的從來不是電腦，而是**孩子手中的
> 動態媒體**。Smalltalk 是他借給大人玩的原型。」

## 案件檔案

| 項目 | 內容 |
|---|---|
| 得主 | Alan C. Kay (1940–) |
| 得獎理由 | 個人運算與物件導向語言的貢獻：Smalltalk 的理念與實作 |
| 關鍵詞 | Smalltalk、Dynabook、視窗介面 |

## 前因

1968 年，Kay 拿著一本 Seymour Papert 的 LOGO 教育實驗
報告，在猶他大學構思 **Dynabook**：一台兒童可持有、可
編程的平板。問題：**孩子怎麼編程？** 答案指向「以圖形
物件對話」——程式要像積木一樣可觸摸。

## 線索與推理

### 線索一：一切皆物件

1970 年代初在 PARC（Lampson 1992 案、Thacker 2009 案
的環境），Kay 團隊（含 Dan Ingalls、Adele Goldberg）
造出 Smalltalk：

```
5 + 3          → 物件 5 收到訊息 + 3
[ :x | x * 2 ] → 區塊物件（閉包，λ 演算血統）
array do: [:each | each print]
一切計算 = 物件之間互傳訊息
```

與 Simula（2001 案）的血緣：Kay 承認「class」來自 Simula，
但把重點從**靜態型別繼承**轉向**動態訊息傳遞與late binding**：
「OOP 對我而言是關於**訊息**，不是物件。」

### 線索二：GUI 的發明

Smalltalk-80 的介面：重疊視窗、圖示、下拉選單、剪貼簿
——1979 年 Jobs 參觀 PARC 看到的正是它（+ Bravo/Alto）。
Kay 團隊證明了：**介面是語言的延伸**（程式與 UI 同構，
皆為物件訊息）。

### 線索三：媒體理論背景

Kay 深受 McLuhan「媒體即訊息」影響：電腦若只是計算器，
就是被誤用的媒體；若成為**可編程的表達媒介**（如紙筆
之於寫作），則改變思考本身。Dynabook 的哲學：孩子用
Smalltalk 畫圖、作曲、模擬物理——**教育即編程**。

## 理論評析

Smalltalk 的深層設計律：

```
late binding：訊息在執行期才決定接收者 → 最大彈性
反射系統：Smalltalk 用自己寫自己的 IDE（meta-circular）
MVC 模式（Model-View-Controller）在此誕生 → 一切 UI 框架的祖先
```

Kay 對後世的批評亦發人深省：他說 C++/Java 式 OOP
（繼承層次崇拜）**背叛了原意**——原意是生物式的
「細胞通訊」：每個物件只守自己的狀態，靠訊息協作。

## 後果

- 直系：Squeak、Pharo、Etoys（教育）；旁系：Objective-C
  （訊息傳遞語法直接抄 Smalltalk）、Python/Ruby 的動態性。
- Dynabook 的實體實現：iPad（2010）。Kay 名言：
  「預測未來最好的方式，就是發明它。」

## 關聯案件

→ [2001-Dahl-Nygaard](2001-Dahl-Nygaard.md)、[1992-Butler-Lampson](1992-Butler-Lampson.md)、[1988-Ivan-Sutherland](1988-Ivan-Sutherland.md)
