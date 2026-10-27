# 2001 Ole-Johan Dahl & Kristen Nygaard —— 物件導向的挪威起源

> 「兩位挪威科學家為了寫**核電廠模擬程式**，發明了物件。
> 為什麼模擬世界的人，最先想到把資料和行為綁在一起？」

## 案件檔案

| 項目 | 內容 |
|---|---|
| 得主 | Ole-Johan Dahl (1931–2002)、Kristen Nygaard (1926–2002) |
| 得獎理由 | 物件導向程式設計的起源：Simula I 與 Simula 67 |
| 關鍵詞 | Simula、類別、虛擬函式、繼承 |

## 前因

1960s，挪威計算中心承接核反應爐與作業研究的模擬案。
當時的困境：Monte Carlo 模擬中的「港口的船、工廠的機器」
各有狀態與行為，用副程式+資料表的傳統寫法**程式結構與
問題結構完全脫節**。謎題：能否讓程式的單位 = 模型中的
實體？

## 線索與推理

### 線索一：Simula I（1964–65）

Nygaard 與 Dahl 在 UNIVAC/ALGOL 60 基礎上造出模擬語言：
每個「程序活動」變成可獨立存活的物件。關鍵洞見：
**模擬需要「同時存在的大量實體，各自有狀態與行為」**
——這正是物件的定義。

### 線索二：Simula 67（1967）—— 物件導向的正式誕生

引進今日 OOP 的全部核心：

```
class Account;
  begin real balance;
    procedure Deposit(amount); ... end;

Account ref a;  a :- new Account(0);
a.Deposit(100);
```

| 發明 | 後裔 |
|---|---|
| class（類別 = 資料+程序） | 一切 OO 語言 |
| ref（參照語義） | Java 物件參照 |
| 虛擬程序（動態分派） | C++ virtual、Java override |
| 子類繼承 | C++/Java/Swift 繼承 |
| 協同程式（coroutine） | 現代 async/await 的祖先 |

**ALGOL 的區塊結構（1966 案）「出了棧還能活」就是物件**——
類別本質上是帶詞彙閉包的記錄型別。

### 線索三：Bjarne Stroustrup 的取經

1979 年 Stroustrup 在劍橋做 Simula 效能研究，之後在
貝爾實驗室把「class」裝進 C——**C++（1983 定名）**。
再往下：Objective-C→NeXT→Apple；Java（1995）以 Simula
血統統治企業後端。

## 理論評析

物件導向的偵探學解讀：**把狀態的邊界畫在哪裡**。

```
程序式：狀態是全域可達的 → 任何函式可能弄髒任何資料
OO：狀態被封裝在物件內 → 存取經過介面（資訊隱藏，Parnas 1972）
OO 的數學本體：abstract data type ≈ 帶操作契約的代數
   Liskov 替換原則（2008 案）為繼承補上正確性條件：
   子類型不得違反父類型的契約
```

## 後果

- 1990s–2000s OOP 成為業界正統（Java、C#、設計模式）。
- 2010s 後函數式思潮回歸，OOP 轉為「組件化」工具——
  但 GUI、遊戲引擎、瀏覽器 DOM 至今是物件的世界。

## 關聯案件

→ [1966-Alan-Perlis](1966-Alan-Perlis.md)、[2003-Alan-Kay](2003-Alan-Kay.md)、[2008-Barbara-Liskov](2008-Barbara-Liskov.md)
