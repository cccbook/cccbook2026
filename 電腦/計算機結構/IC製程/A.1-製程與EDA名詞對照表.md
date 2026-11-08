# A.1 製程與 EDA 名詞對照表

本附錄整理書中出現的製程（process）與 EDA 常用術語之中英對照，供閱讀各章時快速查閱。排版慣例為「英文原文 — 中文譯名（常用簡稱）：一句話說明」。

## 晶圓製程結構

| 英文 | 中文 | 說明 |
|---|---|---|
| FEOL (Front-End-Of-Line) | 前段製程 | 製作電晶體本體（井、閘極、源/汲極）的製程階段。 |
| BEOL (Back-End-Of-Line) | 後段製程 | 以金屬層與介電層完成晶上互連（interconnect）的製程階段。 |
| MOL (Middle-Of-Line) | 中段製程 | 介於電晶體與第一層金屬之間的接觸層（contact/via0）製程。 |
| FinFET | 鰭式電晶體 | 以垂直鰭狀通道包覆閘極的 3D 電晶體結構。 |
| GAA (Gate-All-Around) | 環繞閘極電晶體 | 閘極四面完全包覆奈米片（nanosheet）通道的電晶體，為 FinFET 的後繼者。 |
| BSPDN (Backside Power Delivery Network) | 背面供電網路 | 將電源軌移到晶圓背面、與訊號互連分離的供電架構。 |
| TSV (Through-Silicon Via) | 矽穿孔 | 貫穿晶圓本體、連接上下晶粒的垂直導孔。 |
| Hybrid bonding | 混合鍵合 | 銅墊與介電層同時直接鍵合、實現超高密度晶粒間互連的技術。 |
| CMP (Chemical Mechanical Polishing) | 化學機械研磨 | 以化學腐蝕加上機械研磨將晶圓表面磨平的製程。 |
| Dual damascene | 雙大馬士革製程 | 先蝕刻溝槽與通孔、一次填銅再研磨的 BEOL 金屬成形方式。 |
| Ion implantation | 離子佈植 | 以高能離子束將摻雜原子打入矽晶圓指定區域的摻雜方法。 |
| Anneal | 退火 | 以高溫（如 RTA 快速退火）修復晶格損傷並活化摻雜原子的熱處理。 |

## 微影與圖案化

| 英文 | 中文 | 說明 |
|---|---|---|
| Lithography | 微影（曝光）製程 | 以光線經光罩將電路圖案轉印到光阻上的核心製程。 |
| Mask / Reticle | 光罩／雷射圖版 | 承載電路圖案、在曝光機上使用的石英版，reticle 特指縮小投影式曝光用的單一圖版。 |
| EUV (Extreme Ultraviolet) | 極紫外光微影 | 使用 13.5 nm 波長光源的先進微影技術。 |
| MPP (Multi-Patterning) | 多重圖案化 | 以多次曝光／蝕刻突破單次曝光解析度限制的技術總稱。 |
| SADP (Self-Aligned Double Patterning) | 自我對準雙重圖案化 | 以間隔層（spacer）方式將圖案密度倍增的多重圖案技術。 |
| SAQP (Self-Aligned Quadruple Patterning) | 自我對準四重圖案化 | SADP 做兩次、將密度再倍增至四倍的圖案化技術。 |
| OPC (Optical Proximity Correction) | 光學鄰近效應校正 | 在光罩上預先補償圖形變形，使晶圓上圖案接近設計意圖。 |
| RET (Resolution Enhancement Technique) | 解像度增強技術 | 提升（193 nm）微影可解析度之技術的統稱，如 OPC、PSM、off-axis illumination。 |
| ILT (Inverse Lithography Technology) | 反向微影技術 | 以逆向求解直接算出最佳光罩圖形的先進 RET 方法。 |
| DTCO (Design-Technology Co-Optimization) | 設計與製程共同最佳化 | 讓設計規則與標準單元架構和製程能力共同演進以最大化 PPAC 的方法學。 |
| STCO (System-Technology Co-Optimization) | 系統與製程共同最佳化 | 將系統層級（晶粒切割、封裝）納入製程決策的更上層共同最佳化。 |

## 設計自動化與驗證

| 英文 | 中文 | 說明 |
|---|---|---|
| PDK (Process Design Kit) | 製程設計套件 | 由晶圓廠提供、包含元件模型與設計規則的完整設計套件。 |
| DRC (Design Rule Check) | 設計規則檢查 | 檢查版圖線寬、間距、包覆等是否滿足可製造性規則。 |
| LVS (Layout Versus Schematic) | 版圖電路比對 | 比對版圖抽出的電路與原始設計電路圖是否一致。 |
| DFT (Design for Test) | 可測試性設計 | 在晶片內加入掃描鏈、BIST 等結構以便製造後測試。 |
| DFM (Design for Manufacturability) | 可製造性設計 | 在設計階段考慮製程變異與缺陷，提升良率與可製造性。 |
| Yield | 良率 | 晶圓上合格晶粒（good die）所佔的比例。 |
| Critical area | 臨界面積 | 版圖中一旦出現缺陷（橋接或斷路）就會導致故障的面積，用於估算良率。 |
| Corner | 製程角落 | 製程／電壓／溫度極端組合下模型化的設計情境，如 SS、TT、FF。 |
| PVT | 製程、電壓、溫度 | 決定電路速度與功耗的三大環境變數，signoff 分析必須涵蓋各 corner。 |
| EM (Electromigration) | 電致遷移 | 大電流造成金屬原子遷移、長期導致斷線的可靠度問題。 |
| IR drop | 電壓降 | 電流通過電源網路電阻造成的電壓損失，會影響電路速度。 |
| Parasitic extraction | 寄生參數萃取 | 由版圖計算電阻／電容／電感（RC/RLC）寄生值的程序，產出 SPEF。 |
| Signoff | 簽核 | 晶片送交製造前，以黃金工具完成的所有驗證（時序、DRC、LVS 等）總稱。 |
| Tapeout | 下線（設計定案） | 版圖定案並交付光罩製作的里程碑。 |
| Foundry | 晶圓代工廠 | 專門接受客戶設計、代工製造晶片的廠商，如 TSMC。 |
