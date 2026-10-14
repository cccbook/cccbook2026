# 1976：Apple I 與 Cray-1 — 車庫裡的微機與冷卻塔上的巨獸，兩條平行線的極端對照

## 案情

1976 年 4 月 1 日，Steve Wozniak 與 Steve Jobs 在加州 Los Altos 的車庫創立 Apple Computer，並於 Homebrew Computer Club 展示 Apple I——單一印刷電路板、售價 666.66 美元。幾乎同一時間，在明尼蘇達與威斯康辛邊界的 Chippewa Falls，Seymour Cray 完成了 Cray-1——當時全球最快的超級電腦，時脈 80 MHz、售價 5 至 800 萬美元，1976 年由 Los Alamos 國家實驗室購得首台。兩台機器同年問世，性能相差萬倍，卻共同畫出了電腦產業的兩個極端。

## 前因

- **Apple I 的線索**：Wozniak 是 HP 的工程師，參加了 1975 年 3 月成立的自造者聚會 Homebrew Computer Club，目睹 Altair 8800 後決定自己做一台「更好的」：直接內建鍵盤、能接一般電視當顯示器、開機即跑 BASIC。
- **MOS 6502 的降臨**：1975 年，MOS Technology 以 25 美元的價格推出 6502（Chuck Peddle 領導，工程師包括跳槽自 Motorola 的 Bill Mensch），比 Intel 8080 便宜十倍以上，成為 Wozniak 的心臟選擇。
- **Jobs 的商業嗅覺**：Wozniak 原本只想免費送出設計圖，Jobs 說服他「把電路板當商品賣」；Jobs 並透過 Bits Shop 老闆 Paul Terrell 獲得第一筆訂單：50 台完整主機板，每台 500 美元。
- **Cray 的血統**：Seymour Cray 是 Control Data Corporation（CDC）6600（1964，首台公認超級電腦）的設計者；1972 年因理念不合離開 CDC，自立 Cray Research，獲 Fairchild 半導體投資。

## 線索與推理

把兩案並排，偵探看到的是同一條技術規律的兩種解法。Wozniak 的推理：既然 6502 這麼便宜，「精簡」就能取代「昂貴」——他用極少數晶片（Apple I 全機約僅 30 顆）完成別人需要上百顆才能做到的事，靠的是巧妙的時脈與視訊電路設計。這是「以設計智慧對抗零件成本」。

Cray 的推理則相反：與其省零件，不如讓零件更難做——他把邏輯電路做成 S 積體電路，並讓整個機櫃呈 C 形佈局，使訊號走線盡量短：

$$t_{\text{delay}} \propto \frac{\text{線長}}{v_{\text{signal}}}$$

在 80 MHz（每週期 12.5 奈秒）下，光走 3.75 公尺都來不及——線長即性能。Cray-1 的另一張王牌是向量暫存器（8 組 64 元素的 64-bit 向量暫存器），配合鏈水（chaining）技術讓多條向量指令重疊執行，使浮點峰值達 80 MFLOPS。散熱則採用 Freon 冷卻系統沿機櫃流動，機身因外形被暱稱為「世界上昂貴的躺椅」。

兩案的當事人都成功了，但商業路徑完全分化：Apple I 憑「低價 + 開放 + 業餘市場」滾出正循環；Cray-1 憑「極致性能 + 國家實驗室與石油公司等少數大客戶」站穩金字塔頂端。1976 年，電腦產業同時擁有了地板與天花板。

## 理論

**Cray-1 的向量運算模型**：

$$\mathbf{C} = \mathbf{A} + \mathbf{B}, \quad C_i = A_i + B_i, \quad i = 0 \ldots 63$$

一條向量指令即處理 64 個元素；向量長度暫存器 VL 控制實際元素數。鏈水技術使「向量加法」與「向量乘法」的結果可在流水線中相接：

$$\mathbf{D} = s \times \mathbf{C} \text{（乘法流水線直接讀取加法流水線輸出）}$$

**兩機規格對照**：

| 項目 | Apple I | Cray-1 |
|---|---|---|
| CPU | MOS 6502 @ 1 MHz | Cray 自製 ECL 邏輯 @ 80 MHz |
| 記憶體 | 4–8 KB | 8 MB（256K × 64-bit words） |
| 售價 | 666.66 美元 | 500–800 萬美元 |
| 目標客戶 | 業餘玩家 | 國家實驗室、氣象、石油、國防 |
| 產量 | 約 200 台 | 約 80 餘台 |

## 後果

- **Apple I → Apple II**：1977 年 Apple II 上市（詳見 1977 篇），蘋果崛起；Apple I 原型板如今是拍賣會上的天價古董（2014 年一台以 90.5 萬美元成交）。
- **超級電腦競賽**：Cray-1 稱霸 1976–82 年，其後 Cray-2、Cray X-MP 延續王座至 1990 年代，直到日本 NEC Earth Simulator（2002）與後來的 GPU 叢集接棒。
- **向量架構的遺產**：Cray 的向量思想影響了 SIMD 指令集（MMX、SSE、AVX）與 GPGPU 的設計哲學。
- **車庫創業神話**：Apple 的車庫故事（雖然初期工作地點其實包含 Jobs 家的臥室與廚房）成為矽谷創業文化的原型敘事。

## 冷案檔案

- 時間：1976 年 4 月（Apple 公司成立、Apple I 展示）；1976 年（Cray-1 交付 Los Alamos）
- 案由：兩位天才設計師（Wozniak 與 Cray）以完全相反的策略，分別定義了「最便宜的電腦」與「最貴的電腦」
- 歷史定位：電腦產業的雙極原點——個人電腦的民主化與超級電腦的精英化，同一年份的兩份判決書
