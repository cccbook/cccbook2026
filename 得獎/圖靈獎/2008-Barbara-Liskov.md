# 2008 Barbara Liskov —— 抽象的立法者與替換原則

> 「程式要能被修改而不崩壞，需要一條關於『誰能替代誰』的
> 宪法。這條憲法以她的名字命名，出現在每一本 OOP 教科書。」

## 案件檔案

| 項目 | 內容 |
|---|---|
| 得主 | Barbara Liskov (1939–) |
| 得獎理由 | 程式設計方法論與抽象化的貢獻：資料抽象、容錯分散式計算 |
| 關鍵詞 | CLU、資料抽象、Liskov 替換原則、Paxos 前傳 |

## 前因

1960s 末，大型程式的崩壞模式：任何模組都能觸碰任何資料。
Parnas（1972 論文）提出「資訊隱藏」，但需要**語言級
機制**。Liskov 在 MIT 的謎題：**如何讓「資料」也擁有
存取控制與型別保證？**

## 線索與推理

### 線索一：CLU 語言（1974–79）

Liskov 與 Zilles 定義 **cluster**（CLU 的抽象資料型別）：

```
cluster IntSet is create, insert, member, ...
  rep = ...            （表示式，外界不可見）
  member = proc (s: cvt, x: int) returns (bool)
     return exists e: rep[s](e) = x
end IntSet
```

要點：

1. **表示式隱藏**：cvt 轉換為唯一邊界
2. **參數化型別（泛型）**：`Array[T]` 的 typegen——
   先於 Java/C++ 泛型二十年
3. **迭代器（yield）**：控制抽象與資料抽象並列——
   Python/C# 的 for-yield 直系

### 線索二：Liskov 替換原則（1987 OOPSLA 演講，1994 成文）

```
若 φ(x) 對型別 T 的物件 x 成立，則對 T 的子型別 S 的
物件 y，φ(y) 亦應成立（行為子型別）。
操作化：子類的每個方法 m 須滿足
  前置條件：不強於父類（req(m) ⊆ req(m'))
  後置條件：不弱於父類（ens(m') ⊇ ens(m)）
```

**繼承從「語法允許」升級為「契約相容」**——IS-A 必須是
行為意義的。這條原則是設計模式、SOLID 中的 L，
也是 Rust trait 與型別系統設計的倫理基準。

### 線索三：分散式容錯（1980s–90s）

Liskov 學派（MIT PDOS）在拜占庭容錯上先行：

```
拜占庭將軍問題（Lamport 1982）的工程化
PBFT 式複製：2f+1 台容忍 f 台任意故障（含作惡）
Viewstamped Replication（Oki–Liskov 1988）——
  與 Paxos（Lamport 2013 案）同期獨立發明的共識前作
```

### 線索四：Argus 與分佈式事務

以「guardian」封裝分散式物件事務——把 CLU 的抽象
思想搬進網路世界（Gray 1998 案的 ACID × Liskov 的
封裝）。

## 理論評析

Liskov 的統一母題：**契約（contract）**。

```
資料抽象 = 資料的契約（介面 vs 表示）
行為子型別 = 繼承的契約（不變式的保持）
容錯複製 = 機器間的契約（故障也要遵守承諾）
```

抽象層次每上一級，契約的強制力就由語言接管一分——
**把信任從人轉移到機制**，是她四十年工作的單一主線。

## 後果

- 泛型、迭代器、抽象類別成為主流語言標配。
- 她是圖靈獎第二位女性得主；2021 年與 Hoare 同年
  再次獲獎（唯二兩度得主）。

## 關聯案件

→ [2001-Dahl-Nygaard](2001-Dahl-Nygaard.md)、[1998-Jim-Gray](1998-Jim-Gray.md)、[2013-Leslie-Lamport](2013-Leslie-Lamport.md)
