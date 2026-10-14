# 1981：IBM PC 與 DOS — 藍色巨人的開放式賭局，與微軟的第二次幸運

## 案情

1981 年 8 月 12 日，IBM 在紐約發表 IBM Personal Computer（Model 5150），搭載 Intel 8088 @ 4.77 MHz、16–256KB 記憶體，售價 1,565 美元起。作業系統是微軟提供的 MS-DOS 1.0（IBM 版稱 PC DOS）。這台機器在兩年內賣出逾百萬台，其「開放式規格」催生了 Compaq 等相容機產業，並讓 x86 + DOS/Windows 生態統治 PC 市場三十年以上。

## 前因

- **Apple II 的羞辱**：1970 年代末，Apple II 以每年倍增的銷量蠶食市場，IBM 內部視之為威脅，決定「小部隊突襲」。
- **Boca Raton 的跳脫程序**：IBM 主管 William Lowe 提出 12 個月出貨的計畫（打破 IBM 慣常的 4 年開發週期），獲董事會同意成立獨立的 Entry Systems Division，團隊約 12 人，地點在佛羅里達 Boca Raton。
- **外部採購的決策**：團隊幾乎所有零件外購——CPU 用 Intel 8088、軟碟用 Tandon、作業系統外購、連 BIOS 之外的軟體（BASIC）都找微軟。這在「什麼都自己做」的 IBM 文化中是革命。
- **Digital Research 的錯失**：IBM 原本屬意 Gary Kildall 的 CP/M-86。1980 年 11 月那次著名的會面中，Kildall 搭機出差（一說去飛行）、妻子 Dorothy McEwen 與律師在場，談判因保密協議與授權金額分歧而破裂；IBM 未能談成。

## 線索與推理

微軟的「第二次幸運」是本案最精彩的推理橋段。IBM 找上微軟時，先問的是 BASIC（微軟的招牌），再問「那你們能提供作業系統嗎？」Gates 坦言不會寫，但答應去找。他們隨即以 75,000 美元向 Seattle Computer Products 的 Tim Paterson 買下 86-DOS（QDOS，Quick and Dirty Operating System，一個基於 CP/M 精神的 8086 作業系統，1980 年 7 月由 Paterson 完成），改寫成 PC DOS 授權給 IBM——關鍵條款是：微軟保留非 IBM 版本的銷售權（MS-DOS）。

這個條款是全案樞紐。IBM 以為自己只是「外購作業系統」，實際上把整個作業系統市場的產權讓渡了出去。CP/M 錯失 + 86-DOS 購入 + 保留授權權，三步構成微軟崛起的完整推理鏈。

第二條推理線是「開放式設計」的深層動機。IBM 為了 12 個月出貨，必須用現成零件、發布技術參考手冊、開放擴充槽——這是被時間壓力逼出來的開放，卻產生了災難級（對 IBM 而言）的副作用：任何人都可以合法複製「機器的架構」（唯 BIOS 有版權）。Compaq 於 1982 年用逆向工程乾淨重寫 BIOS（1984 年 Compaq Portable 問世並快速成功）， phoenix 與 Award 隨後賣出相容 BIOS，相容機產業全面爆發。IBM 自己養出的開放生態，最終反噬了自己的 PC 業務。

## 理論

**IBM PC 規格**：

| 項目 | 規格 |
|---|---|
| CPU | Intel 8088 @ 4.77 MHz |
| 記憶體 | 16KB 起，最大 256KB |
| 顯示 | MDA（文字）或 CGA（4 色 320×200） |
| 儲存 | 5.25" 軟碟 160KB（無硬碟） |
| OS | PC DOS 1.0（微軟授權） |
| 擴充 | 5 個 ISA 插槽 |
| 售價 | 1,565 美元起（無軟碟版） |

**DOS 的本質**：一個薄殼的 CP/M 繼承者——檔案系統用 FAT12，系統呼叫介面（INT 21h）在語意上高度對應 CP/M 的 BDOS 呼叫，使 CP/M 軟體易於移植：

$$\text{CP/M BDOS 呼叫} \xrightarrow{\text{語意映射}} \text{DOS INT 21h}$$

**相容機經濟學**：IBM PC 的總體成本 = 整機售價 − 利潤率；相容機省去 IBM 的品牌溢價與研發攤提：

$$P_{\text{clone}} = P_{\text{IBM}} - \epsilon, \quad \epsilon \gg 0 \Rightarrow \text{市占席捲}$$

## 後果

- **1982–83 年的爆發**：PC 兩年內成為事實標準，Apple、Commodore 等競品節節敗退；1983 年 IBM PC/XT 加入硬碟。
- **相容機產業**：Compaq（1982）、Dell（1984）、Acer、華碩等百家爭鳴；「PC」從 IBM 商標變成通用名詞。
- **微軟的帝國基礎**：MS-DOS 靠相容機生態擴散，1985 年 Windows 1.0 登場，1990 年代 Windows 3.x 統治桌面，微軟成為 1990 年代市值之王。
- **IBM 的教訓**：1987 年 IBM 企圖以專利微通道架構（MCA）與 OS/2 收回主導權，均告失敗；2005 年將 PC 部門售予聯想，正式退出。
- **CP/M 的黃昏**：Kildall 的 Digital Research 在 1980 年代雖推出 DR-DOS 對抗，終究不敵微軟的生態鎖定，1991 年被 Novell 併購。

## 冷案檔案

- 時間：1981 年 8 月 12 日（發表）
- 案由：IBM 為求快速進入市場採開放式設計與外部採購，意外促成相容機產業；微軟以 75,000 美元購入 86-DOS 並保留授權權
- 歷史定位：PC 標準化的原點與「開放反而失去控制權」的經典教訓——x86 + DOS 生態自此統治資訊產業三十年
