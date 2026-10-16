# 嵌入式作業系統 發展史 -- AI 偵探風格

以「推理探案」的方式，追查嵌入式與即時作業系統（VRTX、QNX、VxWorks、uClinux、FreeRTOS、Zephyr）的每一步：
前因是什麼？線索在哪裡？推理如何展開？後果又如何改變了整個電腦科學與數位世界？

核心謎題只有一個：**為什麼一個幾 KB 的極簡核心，能跑進 2026 年全球上千億顆晶片？**

答案藏在嵌入式系統的四大鐵律中：
$$\text{決定性（即時）} + \text{極小 footprint} + \text{硬體直接控制} + \text{低功耗} = \text{嵌入式 OS 的不朽}.$$

## 案件卷宗（歷史年表）

### 誕生與奠基（1976–1982）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1976 | VRTX 誕生——Hunter & Ready 賣出第一個「核心元件」：即時多工從寫程式變成買元件 | [1976-VRTX與即時核心誕生.md](1976-VRTX與即時核心誕生.md) |
| 1982 | QNX 微核心——10KB 核心訊息傳遞、一切皆訊息，嵌入式微核心的祖師爺 | [1982-QNX微核心與訊息傳遞.md](1982-QNX微核心與訊息傳遞.md) |

### 標準化與工業控制（1993–1998）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1993 | VxWorks 與 POSIX 即時標準——POSIX.1b 即時擴充、優先級繼承，火星探測車的心臟 | [1993-VxWorks與POSIX即時標準.md](1993-VxWorks與POSIX即時標準.md) |
| 1998 | uClinux 與 RTLinux——無 MMU 的 Linux 與硬即時補丁：Linux 進入嵌入式 | [1998-uClinux與RTLinux.md](1998-uClinux與RTLinux.md) |

### 開放原始碼與物聯網（2003–2015）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 2003 | FreeRTOS 誕生——開放原始碼即時核心、MIT 授權，跑進最多晶片的 RTOS | [2003-FreeRTOS誕生.md](2003-FreeRTOS誕生.md) |
| 2015 | Zephyr 與物聯網——Linux 基金會庇護、設備樹、Kconfig：嵌入式版的「發行版」 | [2015-Zephyr與物聯網.md](2015-Zephyr與物聯網.md) |

### 現代嵌入式：安全與記憶體安全（2020）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 2020 | Rust 嵌入式與 RTIC——embedded-hal 抽象、編譯期無資料競爭：記憶體安全進入 1KB 核心 | [2020-Rust嵌入式與RTIC.md](2020-Rust嵌入式與RTIC.md) |

## 每個新功能的「為何加上」總覽

| 年份 | 新功能 | 彌補的缺陷 | 理論基礎 |
|------|--------|-----------|----------|
| 1976 | 商用即時核心（VRTX） | 每個專案重寫多工迴圈 | 核心元件化、RTOS 抽象 |
| 1982 | QNX 微核心、一切皆訊息 | 巨核心驅動當機全死 | 最小特權、訊息傳遞 IPC |
| 1993 | POSIX.1b、優先級繼承 | 各 RTOS API 碎片化；優先級反轉 | 即時排程理論、優先級反轉協定 |
| 1998 | uClinux（無 MMU Linux） | Linux 需要 MMU、footprint 太大 | 軟體 MMU、行程即 vfork |
| 1998 | RTLinux 硬即時 | Linux 排班不確定性（毫秒級 jitter） | 雙核心架構、虛擬中斷 |
| 2003 | FreeRTOS（開源 MIT） | 商用 RTOS 授權費、原始碼封閉 | copyleft 光譜、開源即行銷 |
| 2015 | Zephyr 設備樹、Kconfig | 每張板子一份硬編碼驅動 | 宣告式硬體描述、組態空間裁剪 |
| 2020 | Rust embedded-hal、RTIC | C 指標漏洞、中斷資料競爭 | 所有權型別、編譯期優先級驗證 |

## 關鍵人物年表

| 年代 | 人物 | 貢獻 |
|------|------|------|
| 1976 | Jerry Hunter / Larry Ready | VRTX——第一個商用即時核心 |
| 1982 | Dan Dodge / Gordon Bell | QNX 微核心（一切皆訊息） |
| 1993 | Wind River / Jerry Fiddler | VxWorks 與 POSIX.1b |
| 1998 | Greg Ungerer / Victor Yodaiken | uClinux、RTLinux |
| 2003 | Richard Barry | FreeRTOS |
| 2015 | Linux 基金會 / Intel | Zephyr 專案 |
| 2020 | Jorge Aparicio / James Munns | embedded-hal、RTIC |

## 歷史的教訓（偵探結案陳詞）

1. **footprint 是生存條件**：主機 OS 幾 GB，嵌入式核心幾 KB——「最小可用」在資源受限世界是鐵律。
2. **決定性勝於平均效能**：平均快不重要，最壞情況可預測才重要——即時排程理論的勝利。
3. **標準介面戰國統一**：VRTX 各家 API → POSIX.1b（1993）→ CMSIS/embedded-hal——介面統一讓程式可攜。
4. **開源是最強的行銷**：FreeRTOS（2003）、Zephyr（2015）——免費流通自會放大，商用 RTOS 被逼向邊緣。
5. **硬體進步每次都改寫軟體設計**：無 MMU 晶片逼出 uClinux，MCU 進步逼出物聯網 RTOS。
6. **理論與務實的辯證**：QNX 微核心理論（1982）在桌面輸給 Linux 務實，卻在安全關鍵嵌入式市場長存——**兩者各有戰場**。
