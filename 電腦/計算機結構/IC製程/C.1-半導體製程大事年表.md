# C.1 半導體製程大事年表

半導體產業的每一次跳躍，背後幾乎都伴隨一次 EDA 的進化：製程給出新的物理限制，EDA 就發明新的方法學去駕馭它。本年表以製程為主軸，標註關鍵的 EDA 里程碑，供對照本書各章。

## 年表

| 年份 | 事件 | 與 EDA 的關聯 |
|---|---|---|
| 1958 | Kilby 與 Noyce 分別示範／發明積體電路（IC） | 電路首次「做」在晶片上，版圖概念誕生。 |
| 1965 | Gordon Moore 提出摩爾定律 | 「電晶體數每兩年翻倍」成為整個產業與 EDA 的路線圖。 |
| 1970 | SPICE 誕生於 UC Berkeley | 電路模擬的基石，本書 `veryl-sim` 與各類模型的思想源頭。 |
| 1971 | Intel 推出 4004，首顆商用微處理器 | 2,300 顆電晶體，10 µm 製程。 |
| 1975 | Mead–Conway 提出 VLSI 設計方法學 | 以 λ 規則抽象化製程，讓設計與製程解耦，催生現代 PDK 概念。 |
| 1980s | CMP 逐漸成熟；Mentor 推出 Calibre | 平坦化讓多層金屬成為可能；Calibre 成為 DRC/LVS signoff 事實標準。 |
| 1984 | Verilog 問世 | 硬體描述語言（HDL）時代開始，RTL 設計取代畫電晶體。 |
| 1987 | TSMC 成立 | 純晶圓代工（foundry）模式誕生，fabless + PDK 生態系成形。 |
| 1990 | Synopsys 推出邏輯合成工具 Design Compiler | 「寫 RTL、自動變 netlist」成為主流設計方式。 |
| 1997 | IBM 發表銅互連製程（0.18 µm 世代導入） | 銅取代鋁，dual damascene 成為 BEOL 標準。 |
| 1999 | Chenming Hu（胡正明）團隊提出 FinFET 概念 | 為 2010 年代的 3D 電晶體鋪路。 |
| 2002 | 浸潤式微影（immersion lithography）投入量產 | 以水提高 193 nm 光學 NA，讓乾式微影多撐了十幾年。 |
| 2004 | 90/65 nm 世代 strain silicon 與 low-k 介電層普及 | 材料工程接棒尺寸微縮，PDK 內容大幅複雜化。 |
| 2007 | Intel 推出 45 nm high-k/metal gate 製程 | 電晶體閘極材料首次大改，EUV 量產前的最後一次「平面微縮」。 |
| 2011 | Intel 22 nm 量產，首款 FinFET 商用晶片（Ivy Bridge） | 3D 電晶體時代來臨，製程模擬與 OPC 需求暴增。 |
| 2012 | TSMC 推出 CoWoS 先進封裝 | 2.5D 封裝讓「先進封裝」與 DTCO 一起進入設計流程。 |
| 2016 | ASU 發表 ASAP7 開源 7 nm PDK；台積電推 InFO 封裝 | 學界有了免費先進 PDK；扇出型封裝開始量產。 |
| 2019 | EUV 微影正式量產（Samsung 7LPP、TSMC N7+） | 13.5 nm 光源終結多年多重圖案化的痛苦，ILS/ILT 重要性改寫。 |
| 2020 | SkyWater 開源 sky130 PDK | 首個開源成熟製程 PDK，是本書 veryl2chip ASIC 流程的目標製程。 |
| 2022 | UCIe 聯盟成立 | 晶粒間互連標準化，chiplet 生態系正式起步。 |
| 2023 | TSMC N3 量產、GAA（nanosheet）進入 HPC 裝置 | 電晶體從 FinFET 過渡到環繞閘極結構。 |
| 2024 | Intel 展示 PowerVia（BSPDN）量產製程 | 電源軌移到晶圓背面，繞線與 IR drop 分析被重新定義。 |
| 約 2026–2027 | TSMC A16 規劃導入 Super Power Rail（背面供電） | 預計 2026 下半年量產，BSPDN 成為先進製程標配。 |
| 未來 | CFET、2D 材料、系統級 3D 堆疊 | 設計—製程—系統三方共同最佳化（STCO）將主導下一個十年。 |

## 觀察

回顧這條時間線可以發現一個規律：製程的「物理創新」（銅互連、high-k、FinFET、EUV、BSPDN）平均每 5–10 年出現一次，而 EDA 的「方法學創新」（HDL、合成、signoff、DTCO）則持續不斷地填補其間的複雜度。開源 PDK（sky130、ASAP7）與開源工具鏈（本書主角 veryl2chip）的出現，代表這條共舞之路開始向所有人開放——這正是本書寫作的動機。
