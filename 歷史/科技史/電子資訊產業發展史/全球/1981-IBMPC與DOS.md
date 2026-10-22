# 1981：IBM PC 與 DOS — 藍色巨人的開放式賭局與微軟的第二次幸運

## 案情
1981 年 8 月 12 日，IBM 在紐約發表 IBM Personal Computer（Model 5150）：Intel 8088 @ 4.77 MHz、16–256 KB RAM、兩個 5.25 吋軟碟槽、起售 1,565 美元。作業系統是 Microsoft 的 PC DOS 1.0——但微軟其實是從 Seattle Computer Products 買來 QDOS（86-DOS）改名後授權給 IBM。這台機器讓 IBM 一年內奪下個人電腦市場龍頭，也讓微軟從語言廠商蛻變為平台帝國。

## 前因
- 1980 年 Apple II 與 Tandy TRS-80 已占據辦公室與家庭；IBM 高層看到自家幾個部門以「非正式管道」採購 Apple II，被迫正視。
- IBM 在 Boca Raton 成立獨立專案組（Entry Systems Division），由 William Lowe 帶領，獲授權「一年內、跳脫 IBM 流程」。
- IBM 選擇外購零件：Intel 8088、Tandon 軟碟機、EEPROM BIOS 自製——卻未對 BIOS 做法律保護。
- 1980 年 7 月微軟原本只被請去談 BASIC；當 IBM 問及作業系統，蓋茲推薦了 Digital Research 的 CP/M，但 Gary Kildall 錯失會談，IBM 轉回微軟。

## 線索與推理
偵探指出，本案的「案中案」有三層。

第一層：IBM 為何開放？PC 專案組被要求「一年出貨、用現成零件」，根本沒時間自研；而 IBM 法務發現 8088 在數家廠商都有授權生產，可避免單一供應商依賴。開放是緊迫與分散風險的副產品，不是策略遠見。

第二層：CP/M 為何錯失？1980 年 IBM 代表赴佛州找 Digital Research，其妻/律師 Dorothy McEwen 對保密協議有異議，Kildall 本人錯過關鍵會議；雙方授權條款（每位用戶 250 美元 vs 微軟一次買斷約 5 萬美元）談判破裂。偵探指出，微軟隨後以 75,000 美元（含專利權與改名權）向 Seattle Computer Products 買下 QDOS 全權——Tim Paterson 的 86-DOS 本就是 CP/M 的 8086 移植品，介面幾乎逐條對應。這是產業史上最著名的「第二次幸運」：第一次是 1975 年 Altair，第二次是 CP/M 的失約。

第三層：BIOS 的疏漏。1984 年 Compaq 逆向工程 IBM BIOS（以乾淨室手法），推出 Compaq Portable；Phoenix Technologies 隨後賣「IBM 相容 BIOS」給任何廠商。相容機生態爆發，IBM 反而失去控制——到 1980 年代末，IBM PC 相容機市占超過 IBM 本尊。

## 理論
PC DOS 1.0 的 API 核心是 int 21h 系統呼叫（來自 CP/M 的 BDOS 慣例），包含字元 I/O、檔案控制塊（FCB）讀寫等約 80 個功能號。CP/M 與 DOS 的對應：

| 功能 | CP/M (BDOS) | DOS (int 21h) |
|---|---|---|
| 讀一個字元 | 01h | 01h |
| 顯示字元 | 02h | 02h |
| 開檔 | 0Fh | 0Fh（FCB） |
| 關檔 | 10h | 10h（FCB） |

IBM PC 記憶體配置：

$$
\text{0x00000–0x9FFFF：RAM（640 KB）} \quad \text{0xA0000–0xFFFFF：BIOS/ROM/視訊（384 KB）}
$$

「640K 上限」成為十年間最著名的瓶頸，催生 EMS 擴充記憶體與 80286 保護模式的呼聲。

IBM PC Model 5150 關鍵規格：Intel 8088 @ 4.77 MHz、16–256 KB RAM、5 個擴充槽、Cassette 介面選配、首發 OS：PC DOS 1.0 與 CP/M-86（同年 12 月）。

## 後果
- Wintel 聯盟成形：Intel 供 CPU、微軟供 OS，PC 產業的標準由這兩家而非 IBM 定義。
- 微軟保留 DOS 非專屬授權權利，向 Compaq、AST 等所有相容機廠收授權費，1990 年代初年營收破十億美元。
- Compaq、Dell、Gateway 等相容機崛起；IBM 於 1987 年推出封閉的 PS/2 與 OS/2 欲收復失土，失敗。
- 1985 年 Windows 問世；1990 年代 IBM PC 業務逐漸邊緣化，2005 年售予 Lenovo——藍色巨人親手創造了讓自己失去個人電腦市場的標準。

## 冷案檔案
- 時間：1981-08-12 發表；1982-08-13 Compaq Portable 相容機問世
- 案由：開放式設計＋CP/M 錯失＋微軟買下 QDOS，三方決策共同造就 PC 標準
- 歷史定位：產業史上影響最深遠的「無心插柳」——IBM 想快速趕進度，卻把整個 PC 時代的鑰匙交給了兩家小公司。
