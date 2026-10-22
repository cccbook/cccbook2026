# 1979：VisiCalc — 殺手級應用的誕生與軟體王國的初啼

## 案情
1979 年 10 月，Personal Software（後改名 VisiCorp）發表 VisiCalc：史上第一套電子試算表，由哈佛 MBA 學生 Dan Bricklin 構想、Bob Frankston 在麻州以 6502 組合語言實作，售價 100 美元，僅供 Apple II 使用。Apple II 的銷量因 VisiCalc 大增，Apple 甚至一度考慮買下 Personal Software；商業界第一次出現「人們為了跑某套軟體而買整台電腦」的現象——殺手級應用（killer application）概念自此確立。

## 前因
- Bricklin 在哈佛商學院上課時，看教授用黑板調整財務模型的個別參數、全班跟著重算——他想「如果黑板會自動重算呢？」
- 1978 年個人電腦尚無「商務軟體」概念：Apple II 主要賣給愛好者與學校。
- Frankston 在 MIT 曾參與 Multics 與分時系統工程，具備系統級編程能力。
- 既有財務工具是大型主機上的報表產生器（如 RPG），改一個數字要重新跑整份程式，迴圈時間以小時計。

## 線索與推理
偵探指出，VisiCalc 的破案關鍵不在演算法艱深，而在「把重算的權力交給使用者」。傳統報表由程式設計師主導；VisiCalc 讓商人自己操作：

- 稀疏陣列：只存使用者碰過的儲存格，記憶體有限的 Apple II 也能容納大表。
- 依賴圖＋遞迴重算：每個儲存格記錄其依賴，修改上游時只重算受影響的下游。Frankston 用拓撲排序式的遍歷，保證公式求值順序正確。

偵探的第二個觀察是商業面的推理：Bricklin 選 Apple II 而非 TRS-80 或 PET，是因為 Apple II 有 48 KB RAM 上限與軟碟機（1978 年 Disk II 上市），且當時 Apple 對開發者友善。這一賭讓 VisiCalc 與 Apple II 互為引力——根據 Apple 內部估計，VisiCalc 售出了約 10 萬台 Apple II。

第三個線索是策略失誤：Personal Software 未及時保護或擴張。IBM PC 出現後，VisiCalc 移植遲緩；Lotus Development 於 1983 年推出 Lotus 1-2-3（專為 IBM PC 最佳化），一年內奪走王座。Bricklin 曾說：「我們證明了市場存在，卻沒有能力守住它。」

## 理論
VisiCalc 的核心資料結構可抽象為一張有向依賴圖：

$$
G = (V, E),\quad V = \{\text{儲存格}\},\; E = \{(u,v) \mid v \text{ 的公式引用 } u\}
$$

重算即對 G 做拓撲排序後逐一求值：

$$
\text{recalc}(v) = f_v\big(\text{recalc}(u_1), \dots, \text{recalc}(u_k)\big),\quad \forall (u_i, v) \in E
$$

循環參照即 G 中存在環，需偵測並報錯。現代 Excel 仍是這套模型的直系後裔。

VisiCalc 1.0（1979）規格：

| 項目 | 數值 |
|---|---|
| 平台 | Apple II（48 KB） |
| 實作 | 6502 組合語言，約 16 KB |
| 網格 | 63 欄 × 254 列 |
| 售價 | $100 |
| 銷量 | 約 13 萬份（至 1983） |

## 後果
- 殺手級應用模式確立：此後 Lotus 1-2-3（1983）帶動 IBM PC、Word/Excel 帶動 Mac 與 Windows、瀏覽器帶動網際網路、App Store 帶動 iPhone——每次平台革命的敘事皆同。
- 1983 年 Lotus 1-2-3 奪冠；1985 年 Microsoft Excel 隨 Mac 問世，1987 年隨 Windows 成為霸主至今。
- Bricklin 未申請專利（當時法律不確定軟體可否專利），後世認為這反而讓電子試算表概念自由擴散。
- VisiCorp 後沒落；Bricklin 轉型為軟體創業教父與評論者。

## 冷案檔案
- 時間：1979-10 發表；1983 被 Lotus 1-2-3 超越
- 案由：MBA 課堂黑板的靈感，轉化為史上第一套電子試算表
- 歷史定位：「軟體賣硬體」的第一次實證——App 為王，平台為僕，此理自 VisiCalc 始。
