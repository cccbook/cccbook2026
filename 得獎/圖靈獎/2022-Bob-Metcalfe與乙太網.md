# 2022 Bob Metcalfe —— 乙太網：最簡單的仲裁，最長的壽命

> 「1973 年，一位 PARC 工程師要連接上百台 Alto 電腦。
> 中央交換機太貴、令牌環太脆弱。他的答案是：**一條
> 共享電纜，大家都聽，撞了就退。** 這個『粗暴』方案
> 贏了五十年。」

## 案件檔案

| 項目 | 內容 |
|---|---|
| 得主 | Robert M. Metcalfe (1946–) |
| 得獎理由 | 乙太網的發明、標準化與商業化 |
| 關鍵詞 | 乙太網、CSMA/CD、Metcalfe 定律 |

## 前因

1972–73 年，PARC 需要連接 Alto（2009 案）與雷射印表機。
候選方案偵查：

| 方案 | 缺陷 |
|---|---|
| 中央交換機 | 單點故障、成本隨 n² 增長 |
| 令牌環（token ring） | 令牌丟失即全網癱瘓 |
| ALOHA（夏威夷無線電） | 純隨機發射，利用率上限僅 18% |

## 線索與推理

### 線索一：CSMA/CD 的三段論

Metcalfe 在 Xerox PARC 與 Boggs 設計 Ethernet（1973
備忘錄），核心是對 ALOHA 的兩步改良：

```
1. Carrier Sense（先聽）：線上有人說話就閉嘴
   → 撞機率大幅下降
2. Collision Detect（邊說邊聽）：撞了立即停，別浪費整包
3. Binary exponential backoff：第 k 次碰撞後
   隨機等待 ∈ [1992-Butler-Lampson與個人電腦及分散式系統](1992-Butler-Lampson與個人電腦及分散式系統.md)、2009-Charles-Thacker、[2004-Cerf-Kahn與TCPIP及網際網路](2004-Cerf-Kahn與TCPIP及網際網路.md)
