# UNIX 發展史 -- AI 偵探風格

以「推理探案」的方式，追查 Unix 與其後裔（BSD、Linux、GNU、Android、Docker）的每一步：
前因是什麼？線索在哪裡？推理如何展開？後果又如何改變了整個電腦科學與數位世界？

核心謎題只有一個：**為什麼一個 1969 年的極簡系統，能統治 2026 年的手機、伺服器與雲端？**

答案藏在 Unix 的四大發明中：
$$\text{一切皆檔案} + \text{管道組合} + \text{可移植性（C）} + \text{開放原始碼} = \text{Unix 的不朽}.$$

## 案件卷宗（歷史年表）

### 誕生與奠基（1969–1978）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1969 | Unix 誕生——Thompson 在 PDP-7 上寫出極簡作業系統：一切皆檔案、單一檔案樹、fork/exec | [1969-Unix誕生.md](1969-Unix誕生.md) |
| 1971 | 第一版手冊——inode 檔案系統、man page 傳統、roff 文字處理 | [1971-第一版手冊與檔案系統.md](1971-第一版手冊與檔案系統.md) |
| 1973 | Unix 以 C 重寫與管道——可移植性與組合性雙勝利 | [1973-Unix以C重寫與管道.md](1973-Unix以C重寫與管道.md) |
| 1974 | CACM 論文與授權擴散——AT&T 管制反而讓 Unix 免費流傳全美大學 | [1974-CACM論文與授權擴散.md](1974-CACM論文與授權擴散.md) |
| 1975 | Version 6 與 BSD 起源——Thompson 休假進 Berkeley，vi 誕生 | [1975-Version6與BSD起源.md](1975-Version6與BSD起源.md) |
| 1978 | Version 7 與 2.8BSD——Bourne shell、awk、第一個可移植 Unix（所有 Unix 的共同祖先） | [1978-Version7與2.8BSD.md](1978-Version7與2.8BSD.md) |

### 網路化與大分岔（1983–1989）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1983 | BSD 4.2 的 TCP/IP 與 Socket——第一個內建網路的作業系統，socket API 誕生 | [1983-BSD4.2TCP_IP與Sun.md](1983-BSD4.2TCP_IP與Sun.md) |
| 1983 | System V 與 GNU 計畫——商業化與自由化的大分岔，GPL、GCC 誕生 | [1983-SystemV與GNU計畫.md](1983-SystemV與GNU計畫.md) |
| 1987 | MINIX 微核心——教科書 Unix、微核心思想、Linux 的催化劑 | [1987-MINIX微核心.md](1987-MINIX微核心.md) |
| 1989 | POSIX 標準與 BSD 授權——統一戰國的介面規格書，兩大自由授權定型 | [1989-POSIX標準與BSD授權.md](1989-POSIX標準與BSD授權.md) |

### Linux 與自由軟體的勝利（1991–2003）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1991 | Linux 誕生——Torvalds 的 10,000 行核心，網路協作 + GPL 的勝利 | [1991-Linux誕生.md](1991-Linux誕生.md) |
| 1993 | 發行版與 FreeBSD 誕生——Slackware/Debian/NetBSD/FreeBSD，套件管理與依賴解決 | [1993-發行版與FreeBSD誕生.md](1993-發行版與FreeBSD誕生.md) |
| 2001 | Mac OS X 以 BSD 為基礎——Mach + FreeBSD + Aqua，Unix 的帝國化 | [2001-MacOSX以BSD為基礎.md](2001-MacOSX以BSD為基礎.md) |
| 2003 | ext3 日誌式檔案系統——資料庫交易理論移植到檔案系統，當機恢復從小時到秒 | [2003-ext3日誌式檔案系統.md](2003-ext3日誌式檔案系統.md) |

### 現代 Unix：口袋、雲端與全面相容（2008–2014）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 2008 | Android 以 Linux 為核心——雙層授權 + Binder IPC，Unix 後裔成為最普及的 OS | [2008-Android以Linux為核心.md](2008-Android以Linux為核心.md) |
| 2013 | Docker 容器——cgroups + namespaces 的包裝革命，不可變基礎設施 | [2013-Docker容器.md](2013-Docker容器.md) |
| 2014 | systemd 與 WSL——init 之戰（並行啟動、socket 激活）與 Windows 的 Unix 相容 | [2014-systemd與WSL.md](2014-systemd與WSL.md) |

## 每個新功能的「為何加上」總覽

| 年份 | 新功能 | 彌補的缺陷 | 理論基礎 |
|------|--------|-----------|----------|
| 1969 | 一切皆檔案、fork/exec | 每種設備一套專用 API；spawn 設計複雜 | 統一抽象、行程模型分解 |
| 1971 | inode、man page | 檔名與資料耦合；口說無憑 | 資料與索引分離、文件即規格 |
| 1973 | C 重寫、管道 | 組語不可移植；工具無法組合 | 機器無關層、串流與協程 |
| 1975 | vi、BSD 發行版 | ed 浪費終端機能力；單點維護 | 硬體驅動的介面革命 |
| 1978 | Bourne shell、awk | Thompson shell 無控制流；資料處理層缺位 | shell 即程式語言、模式掃描 |
| 1983 | TCP/IP、socket | 網路 API 五花八門；單機 OS 不夠 | 四元組連線模型、分層協定 |
| 1983 | GPL、GNU 工具 | 封閉 Unix 綁死使用者 | copyleft、軟體自由論 |
| 1987 | 微核心（MINIX） | 巨核心一錯全當 | 最小特權、訊息傳遞 |
| 1989 | POSIX、BSD 授權 | Unix 介面碎片化；GPL 嚇跑商業 | Liskov 代換、授權光譜 |
| 1991 | Linux（GPL 巨核心） | MINIX 不許成長；微核心太慢 | 網路協作、實用主義 |
| 1993 | 套件管理（APT 前身） | 手動安裝的依賴地獄 | 依賴圖 + 拓撲排序 |
| 2001 | 日誌式檔案系統 | ext2 當機後 fsck 數小時 | WAL 預寫日誌、ACID 原子性 |
| 2001 | Mac OS X 混合核心 | Mac OS 9 無保護、協作式多工 | Mach 微核心 + BSD 實用層 |
| 2008 | Android 雙層授權、Binder | 封閉行動 OS 授權費；IPC 太底層 | 沙箱隔離、物件導向 RPC |
| 2013 | Docker 容器 | VM 太重；環境不一致 | namespaces、cgroups、不可變基礎設施 |
| 2014 | systemd、WSL | init 序列啟動慢；Windows 無 POSIX | 依賴圖並行、socket 激活、宣告式 |

## 關鍵人物年表

| 年代 | 人物 | 貢獻 |
|------|------|------|
| 1969 | Ken Thompson / Dennis Ritchie | Unix 誕生、C 語言 |
| 1971 | Thompson / Ritchie / Ossanna | 第一版手冊、inode、troff |
| 1973 | Ritchie / McIlroy | C 重寫、管道 |
| 1975–78 | Bill Joy | vi、csh、BSD 發行 |
| 1978 | S. Bourne / Aho-Weinberger-Kernighan | Bourne shell、awk |
| 1983 | Bill Joy / Sam Leffler | 4.2BSD TCP/IP、socket |
| 1983 | Richard Stallman | GNU 計畫、GPL、GCC |
| 1987 | Andrew Tanenbaum | MINIX 微核心 |
| 1991 | Linus Torvalds | Linux 核心（2005 再創 Git） |
| 1993 | Ian Murdock / Theo de Raadt | Debian、OpenBSD/OpenSSH |
| 2001 | Steve Jobs / Rick Rashid | Mac OS X（NeXT + Mach + BSD） |
| 2003 | Stephen Tweedie | ext3 日誌式檔案系統 |
| 2008 | Andy Rubin | Android（Linux 核心） |
| 2013 | Solomon Hykes | Docker 容器 |
| 2014 | Lennart Poettering | systemd |

## 歷史的教訓（偵探結案陳詞）

1. **極簡勝於雄心**：Multics 數百萬行敗給 Unix 幾千行——「Do one thing well」是永恆定律。
2. **介面統一勝於功能齊全**：一切皆檔案（1969）、socket（1983）——統一介面讓組合成為可能。
3. **可移植性是工程紀律**：C 重寫（1973）、POSIX（1989）——把機器相關碼隔離到 1%。
4. **開放原始碼是最強的行銷**：AT&T 管制（1974）、GPL（1991）——流通自會放大。
5. **理論與務實的辯證**：微核心理論（1987）輸給 Linux 務實（1991）又贏回嵌入式市場——**兩者各有戰場**。
6. **最老的元件最需要現代化**：init（1969→2014 systemd）、檔案系統（1971→2003 ext3）——基礎服務的革命影響最深遠。
