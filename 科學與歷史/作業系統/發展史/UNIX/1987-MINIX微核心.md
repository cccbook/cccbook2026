# 1987 - MINIX 微核心（教科書的逆襲）

## 案件摘要
1987 年，**Andrew Tanenbaum**（Vrije Universiteit Amsterdam）為教學寫出 **MINIX**——一個 12,000 行的 Unix 相容系統，隨《Operating Systems: Design and Implementation》教科書出版。
MINIX 採用**微核心（microkernel）架構**：驅動程式與檔案系統跑在使用者空間——
$$\text{Monolithic（巨核心，Unix/Linux）} \quad \text{vs} \quad \text{Microkernel（微核心，MINIX）}.$$
16 年後（2003–），MINIX 3 更成為 **Intel 晶片內建的隱藏作業系統**——教科書的終極逆襲。

## 前因 -- 為什麼會有這個案子
- **AT&T 的授權限制**：1980 年代 Unix 原始碼授權昂貴且禁止用於教學（不能在課堂講解核心）——**Lions 書被禁多年**。Tanenbaum 決心寫一個「乾淨重寫、零 Unix 程式碼」的系統，合法用於教學。
- **IBM PC/AT 的普及**：1984 年 IBM PC/AT（80286）普及，學生終於能在家用電腦上跑 Unix——MINIX 就為 PC 而寫。
- **彌補的缺陷**：巨核心（如 Unix）的驅動程式錯誤會**整個系統崩潰**——微核心把服務搬到使用者空間，一個驅動當掉只需重啟該驅動。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：微核心的架構
$$\text{微核心} = \text{行程排班} + \text{IPC} + \text{基本記憶體管理} \quad (\text{僅此三項})$$
$$\text{檔案系統、驅動、網路} \; \in \; \text{使用者空間行程}.$$
- **理論基礎**：最小特權原則（least privilege）——核心只做必須特權的事，其餘全部降級。
- **彌補的缺陷**：巨核心一個驅動 bug = 全機當機（kernel panic）；微核心的隔離讓故障半徑縮小。

### 第二條線索：IPC 訊息傳遞
微核心的行程間通訊用**訊息傳遞（message passing）**而非共享記憶體：
$$\text{send/receive} \quad \text{取代} \quad \text{共用記憶體}.$$
- **彌補的缺陷**：共享記憶體有競態條件（race condition）風險；訊息傳遞天然序列化，較易證明正確。

### 第三條線索：與 Linux 的歷史公案（1992）
1992 年 Tanenbaum 與 Torvalds 的著名辯論：Tanenbaum 批評 Linux 巨核心是「1970 年代的過時設計」；Torvalds 回應「實用主義戰勝理論純潔」——**歷史證明兩者都有道理**：Linux 贏了市場，微核心贏了理論（後來 L4、seL4、QNX 都證明微核心可行）。

### C 範例：MINIX 的訊息傳遞

```c
/* MINIX 風格：驅動程式在使用者空間，用訊息與核心溝通 */
message m;
m.m_type = DEV_READ;
m.m1_i1 = fd;
send(FS_PROC_NR, &m);        /* 送訊息給檔案系統行程 */
receive(FS_PROC_NR, &m);     /* 等待回覆 */
```

### Shell 範例：MINIX 在 PC 上的教學用法

```bash
# 1987 年：學生第一次能在 80286 PC 上讀懂整個 OS
$ minix &
$ ps
$ cat /usr/src/kernel/main.c   # 原始碼就在手邊，可以改、可以重編
```

## 結案 -- 後果與影響
- **Linux 的催化劑**：1991 年 Torvalds 正是買了 MINIX 來學習，才寫出 Linux（見 `1991-Linux誕生.md`）——**MINIX 是 Linux 的直接催生者**。
- **微核心的理論遺產**：QNX（1982）、L4（1995）、seL4（2009，數學證明正確性）——微核心在嵌入式與高安全領域大放異彩。
- **MINIX 3（2005–）**：Tanenbaum 重新設計為高可靠系統；**Intel ME（Management Engine）晶片內建 MINIX 3**——2017 年曝光後震驚世界：全球逾億台電腦都跑著它。
- 歷史教訓：**教科書系統的影響力，不在市場，而在人心**。

## 關鍵人物與文獻
- **A. S. Tanenbaum**：《Operating Systems: Design and Implementation》(1987)。
- **J. Herder et al.**：〈MINIX 3: a highly reliable, self-repairing operating system〉(2006)。
- 相關案件：`1983-SystemV與GNU計畫.md`、`1991-Linux誕生.md`。
