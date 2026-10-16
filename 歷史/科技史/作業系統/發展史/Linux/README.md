# Linux 發展史 -- AI 偵探風格

以「推理探案」的方式，追查 Linux 核心從 0.01（1991）到 6.x（2022+）的每一步，
以及其生態（發行版、systemd、KVM、Docker、eBPF、Rust）的版本與年份：
前因是什麼？線索在哪裡？推理如何展開？後果又如何改變了整個數位世界？

核心謎題只有一個：**一個學生的 10,000 行嗜好專案，如何成為地球最普及的核心？**

$$\text{0.01（1991）} \xrightarrow{\text{GPL + 網路協作}} \text{1.0（1994）} \xrightarrow{\text{SMP}} \text{2.x} \xrightarrow{\text{2.6 革命}} \text{通用核心} \xrightarrow{\text{容器/雲端}} \text{6.x}.$$

## 案件卷宗（歷史年表）

### 誕生與起飛（1991–1996）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1991 | Linux 0.01 誕生——10,264 行、無網路、386 分頁、Minix FS | [1991-Linux0.01誕生.md](1991-Linux0.01誕生.md) |
| 1994 | Linux 1.0 與發行版——TCP/IP、X Window、ext FS、RPM（1995） | [1994-Linux1.0與發行版.md](1994-Linux1.0與發行版.md) |
| 1996 | Linux 2.0 與 SMP——spinlock、ext2 標準化、伺服器入場券 | [1996-Linux2.0與SMP.md](1996-Linux2.0與SMP.md) |

### 通用核心的成形（2003–2008）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 2003 | 2.6 核心革命——O(1) 排班、NPTL 執行緒、可搶佔、ALSA、udev | [2003-2.6核心革命.md](2003-2.6核心革命.md) |
| 2004 | Ubuntu 與桌面化——Live CD、半年一版、sudo 預設 | [2004-Ubuntu與桌面化.md](2004-Ubuntu與桌面化.md) |
| 2007 | KVM 虛擬化進入核心 2.6.20——硬體輔助、VM 即行程 | [2007-KVM虛擬化.md](2007-KVM虛擬化.md) |
| 2007 | CFS 排班（2.6.23）——紅黑樹取代啟發式、vruntime 公平會計 | [2007-CFS排班與2.6.23.md](2007-CFS排班與2.6.23.md) |
| 2008 | cgroups（2.6.24）與 LXC——容器的地基 | [2008-cgroups與LXC.md](2008-cgroups與LXC.md) |

### 雲端與可程式化時代（2014–2022+）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 2014 | eBPF（3.18）與 systemd 普及——核心安全可程式化、init 世代交替 | [2014-eBPF與systemd普及.md](2014-eBPF與systemd普及.md) |
| 2019 | io_uring（5.1）——非同步 I/O 終極解法、共享記憶體環 | [2019-io_uring與5.x.md](2019-io_uring與5.x.md) |
| 2022 | 6.0/6.1 與 Rust 核心——記憶體安全語言進場、MGLRU | [2022-6.0與Rust核心.md](2022-6.0與Rust核心.md) |

## 重要技術的版本與年份總覽

### 核心版本里程碑

| 版本 | 年份 | 重要新功能 |
|------|------|-----------|
| 0.01 | 1991.9 | 386 分頁、TSS 任務切換、Minix FS（**無網路**） |
| 0.12 | 1992.2 | 改用 GPL 授權 |
| 0.96 | 1992.7 | 初步 TCP/IP |
| 1.0 | 1994.3 | TCP/IP 完整、X Window、SCSI（176K 行） |
| 1.2 | 1995.3 | Alpha/SPARC 平台——首次跨出 x86 |
| 2.0 | 1996.6 | **SMP**（spinlock）、RAID、IP masquerade（780K 行） |
| 2.2 | 1999.1 | SMP 16 CPU、VM/網路改進 |
| 2.4 | 2001.1 | 日誌 FS 支援、USB、IPv6 |
| 2.6 | 2003.12 | **O(1) 排班、NPTL、可搶佔、ALSA、udev、NUMA** |
| 2.6.20 | 2007.2 | **KVM** 虛擬化 |
| 2.6.23 | 2007.10 | **CFS** 排班（紅黑樹）、群組排班 |
| 2.6.24 | 2008.1 | **cgroups** |
| 2.6.28 | 2008.10 | **ext4** 正式 |
| 3.18 | 2014.12 | **eBPF** |
| 4.6 | 2016.5 | **cgroup v2** |
| 5.1 | 2019.5 | **io_uring** |
| 5.6 | 2020.3 | io_uring 零拷貝 |
| 6.1 | 2022.12 | **Rust 核心**、MGLRU |
| 6.6 | 2023.10 | **EEVDF** 排班取代 CFS |
| 6.8 | 2024.3 | 第一個 Rust 真實驅動（Phy） |

### 生態軟體的版本與年份

| 軟體 | 年份 | 事件 |
|------|------|------|
| XFree86 | 1992 | Linux 上的 X11 |
| Slackware 1.0 | 1993.7 | 第一個 Linux 發行版 |
| Debian | 1993.8 | 社群治理的發行版（dpkg） |
| ext2 進入核心 | 1993.1 | 標準檔案系統 |
| RPM | 1995 | Red Hat 二進位套件 |
| YUM / DNF | 2003 / 2014 | 依賴自動求解 |
| APT | 1998 | Debian 依賴解決 |
| ALSA | 2003 | 音訊架構取代 OSS |
| udev | 2003.12 | 動態 /dev 管理 |
| Ubuntu 4.10 | 2004.10 | 桌面化、半年一版 |
| libvirt | 2007.7 | 統一虛擬化管理 API |
| LXC 0.1 | 2008.8 | Linux 容器 |
| systemd | 2010→2014 | init 革命 |
| Docker | 2013→2014.7 | 容器包裝革命 |
| Kubernetes 1.0 | 2015.7 | 容器編排 |
| bcc（eBPF Python） | 2015 | eBPF 工具鏈 |
| Snap | 2016 | 容器化套件 |
| bpftrace | 2018 | eBPF 一行式觀察 |
| Git | 2005 | Torvalds 的版本控制 |

## 每個新功能的「為何加上」總覽

| 年份 | 新功能 | 彌補的缺陷 | 理論基礎 |
|------|--------|-----------|----------|
| 1991 | 386 分頁、巨核心 | MINIX 訊息傳遞太慢 | 實用主義 |
| 1992 | GPL | 修改不回饋 | copyleft |
| 1992 | ext FS | Minix FS 14 字元檔名 | 索引分離 |
| 1996 | SMP + spinlock | 多 CPU 閒置；競態條件 | 臨界區互斥（Dijkstra 1965） |
| 2003 | O(1) 排班 | 2.4 O(n) 掃描 | 優先度佇列 |
| 2003 | NPTL | LinuxThreads 的 pid 怪異 | POSIX 執行緒語義 |
| 2003 | 可搶佔核心 | 桌面音訊延遲 | 搶佔式多工 |
| 2004 | sudo 預設、Live CD | root 危險；安裝門檻 | 最小特權、審計 |
| 2007 | KVM | Xen 需改 guest | 硬體輔助虛擬化 |
| 2007 | CFS | O(1) 啟發式猜錯 | vruntime 公平共享 |
| 2008 | cgroups | 無群組級資源配額 | 資源會計 |
| 2014 | eBPF | 核心模組當機風險 | 驗證器（形式化驗證） |
| 2019 | io_uring | 系統呼叫開銷、libaio 窄 | 共享記憶體環、批次 |
| 2022 | Rust 核心 | C 的 70% 記憶體安全漏洞 | 所有權 + 借用檢查 |
| 2023 | EEVDF | CFS 無延遲敏感度 | 公平 + deadline |

## 關鍵人物年表

| 年代 | 人物 | 貢獻 |
|------|------|------|
| 1991 | Linus Torvalds | Linux 0.01、2005 再創 Git |
| 1992 | Remy Card | ext 檔案系統 |
| 1993 | Alan Cox / Ian Murdock | 網路整合、Debian |
| 1995 | Marc Ewing / Miguel Ewing | RPM |
| 2002–03 | Ingo Molnar / Ulrich Drepper | O(1)、NPTL |
| 2003 | Greg Kroah-Hartman | udev |
| 2004 | Mark Shuttleworth | Ubuntu/Canonical |
| 2006–07 | Avi Kivity / Ingo Molnar | KVM、CFS |
| 2008 | Paul Menage（Google） | cgroups |
| 2010–14 | Lennart Poettering | systemd |
| 2013 | Solomon Hykes | Docker |
| 2014 | Alexei Starovoitov | eBPF |
| 2019 | Jens Axboe | io_uring |
| 2022 | Miguel Ojeda | Rust for Linux |

## 歷史的教訓（偵探結案陳詞）

1. **務實戰勝純潔，但有時純潔翻案**：巨核心（1991）贏了市場；CFS 數學公平（2007）贏了啟發式。
2. **硬體進步改寫軟體設計**：386 分頁（1991）→ VT-x（2007 KVM）→ NVMe（2019 io_uring）——每次硬體革命都逼出軟體革命。
3. **一次革命三戰場**：2.6（2003）同時服務桌面（可搶佔/ALSA）、伺服器（O(1)/NUMA）、手機（後繼 Android）。
4. **地基與包裝是兩回事**：cgroups/ns（2008）是地基，Docker（2013）是包裝——**包裝決定普及**。
5. **驗證器讓核心可程式化**：eBPF（2014）證明形式化驗證能讓「擴展核心」零風險。
6. **系統語言 50 年換一次血**：C（1973）→ Rust（2022）——**當一類 bug 佔漏洞 70%，就該換語言**。
