# 1979：VisiCalc — 第一個殺手級應用：軟體賣出了硬體

## 案情

1979 年 10 月，Personal Software 公司（後改名 VisiCorp）推出 VisiCalc——史上第一套電子試算表，由哈佛商學院學生 Dan Bricklin 構想、Bob Frankston 實作，首發平台是 Apple II。這套 49.95 至 100 美元的軟體，被廣泛認為是 Apple II 打入企業市場的直接原因；Apple II 約有兩成到三成的銷量直接由 VisiCalc 驅動。

## 前因

- **Bricklin 的課堂頓悟**：1978 年，Bricklin 在哈佛商學院看教授用黑板做「假設分析」——每改一個數字就得擦掉重算整列。他心想：何不用電腦讓所有公式自動重算？
- **試算表的史前史**：會計用的「工作底稿」（spreadsheet）是人類數百年的紙上工具；大型主機上的財務規劃軟體（如 Interactive Financial Planning Program, IFPS）昂貴且難用。
- **Apple II 的硬體條件**：Apple II 有 48KB 記憶體上限、可加 Disk II 軟碟機、有 80 欄顯示能力——剛好夠跑一個試算表。
- **Personal Software 的成立**：Bricklin 與 MIT 同窗 Bob Frankston 共創公司，並由 Dan Fylstra 提供早期資金與行銷。

## 線索與推理

這樁案子的核心推理只有一句話：「先有雞的應用，才會有雞生蛋的硬體市場。」在 VisiCalc 之前，個人電腦的客戶是電子迷；VisiCalc 之後，客戶是會計師、財務長、小老闆。軟體第一次成為硬體的銷售引擎——這個因果方向的反轉，比軟體本身的技術更重要。

工程上的推理同樣精緻：Frankston 必須在 Apple II 的 6502 上、48KB 記憶體內，實作一個「依賴圖重算引擎」。他的解法是鏈式維護（cell dependency chain）+ 增量重算：

$$\delta(\text{某儲存格}) \Rightarrow \text{僅重算其下游依賴閉包}$$

而非每次都從頭算整張表——這是讓「改一個數字、全部瞬間更新」成為現實的關鍵演算法。三人月（Frankston 與 Bricklin）就寫出了主程式，1979 年 4 月已有可運作版本，10 月正式發售。

商業推理的一個關鍵轉折：Personal Software 起初無力負擔多平台開發，押注 Apple II 作為首發平台——這個選擇讓 Apple II 從「玩家機」升格為「商用機」，而蘋果在行銷上樂得把 VisiCalc 當賣點。個人電腦史上第一次，「軟體綁硬體」的共生關係成形。

## 理論

**電子試算表的抽象**：將工作底稿形式化為有向圖 $G=(V,E)$：

- $V$：儲存格集合，每格含常數或公式
- $E$：依賴邊，$(u,v) \in E$ 表示 $v$ 的公式引用 $u$

計算是圖上的拓撲序求值：

$$\text{eval}(v) = f_v\big(\text{eval}(u_1), \ldots, \text{eval}(u_k)\big), \quad u_i \in \text{pred}(v)$$

**增量重算的複雜度**：

| 策略 | 每次修改成本 |
|---|---|
| 全表重算 | $O(\|V\|)$ |
| 拓撲增量重算 | $O(\text{受影響閉包大小})$ |
| 紙上重寫 | $O(\text{人工小時})$（無限大） |

**VisiCalc 規格**：畫面 20 列 × 5 欄、可擴至 254 欄 × 63 列、公式支援 +−×÷ 與 SUM/AVG、隱藏式選單操作、佔用約 27KB 記憶體。

## 後果

- **Apple II 銷量暴衝**：1980–81 年，會計師事務所與企業成為 Apple II 新客源，「VisiCalc 機器」之名不脛而走。
- **競爭爆發**：1982 年 Lotus 1-2-3（Mitch Kapor）在 IBM PC 上以速度與圖表擊敗 VisiCalc，VisiCorp 轉手賣出資產；1985 年 Microsoft Excel 問世（1987 年 Excel 2.0 for Windows 成主流），試算表王座最終由微軟接手。
- **殺手級應用理論**：本案確立了「每個平台都需要一個殺手級應用」的產業鐵律——之後 Mac 的 DTP、PC 的 DOS 遊戲、智慧手機的 App Store，皆循此模式。
- **Bricklin 的選擇**：他放棄了專利申請（當時軟體專利爭議未定），認為讓市場繁榮比壟斷更有價值——電子試算表因此快速普及。

## 冷案檔案

- 時間：1979 年 10 月（Apple II 版上市）
- 案由：Bricklin 構想、Frankston 實作的 VisiCalc，讓 Apple II 進入企業，證明軟體可以銷售硬體
- 歷史定位：史上第一個殺手級應用——「應用程式驅動平台」產業邏輯的發明時刻
