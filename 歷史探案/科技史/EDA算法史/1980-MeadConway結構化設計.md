# 1980-MeadConway結構化設計

## 案件摘要
1970 年代的 VLSI 惡夢：每家公司的設計規則各寫各的、每個製程要重畫所有版圖，設計與製造緊緊綁死。1980 年，Caltech 的 Carver Mead 與 Xerox PARC 的 Lynn Conway 出版《Introduction to VLSI Systems》，端出三件套破案：**λ 設計規則**（一切尺寸以 λ 為單位，製程升級只改 λ）、**結構化設計**（階層化、規則化、局部性）、**符號版圖**（設計者畫「棒狀圖」，工具生成實體幾何）。這不是單一演算法，而是一套「把設計與製造解耦」的方法學——它催生 MPC79 多專案晶片與 MOSIS 服務（1981），為 TSMC 晶圓代工模式（1987）預演了整個劇本。

## 前因 -- 為什麼會有這個案子
- **設計與製造的綁架**：每家廠的微影套刻誤差、摻雜深度不同，設計規則互不相容——換一個 fab 等於重畫所有版圖。
- **手繪版圖的天花板**：1970 年代設計者用紅藍鉛筆在方格紙畫版圖，一顆 LSI 要數人年；MOS 技術的潛力（元件密度增長）被人力鎖死。
- **Mead 的系統觀**：Mead 主張「晶片設計應像寫軟體一樣有結構」；Conway 則在 IBM 與 Xerox 有動態架構與超大型系統的經驗——兩人 1976-77 在 PARC 合流。
- **大學無法教 VLSI**：沒有 fab 的大學做不了晶片，人才斷層——需要一個「設計可攜帶」的解法。

## 線索與推理 -- 數學式、程式、理論

### 線索一：λ 規則——尺度不變性
把所有最小尺寸表達成 λ 的倍數（λ = 閘長的一半，隨製程縮放）：

| 規則 | λ 表達 |
|------|--------|
| 最小線寬 | $2\lambda$ |
| 最小間距 | $2\lambda$ |
| 接觸孔 | $2\lambda \times 2\lambda$ |
| 多晶矽閘對擴散的延伸 | $2\lambda$ |

**推理**：微影誤差、套刻誤差都與特徵尺寸成比例（線性縮放），因此把安全餘量表達成 λ 的比例，設計就對製程**尺度不變**——換製程只改一個常數。這是數學上的相似變換（scaling transform）：座標 $\times s$，設計不變。

### 線索二：結構化設計三原則
1. **階層化（hierarchy）**：大系統 = 小單元的巢狀組合，設計複雜度從 $O(n)$ 降到 $O(\log n)$ 層級管理；
2. **規則化（regularity）**：記憶體、ALU 用重複單元，一個單元設計好，處處復用（iteration + replication）；
3. **局部性（locality）**：介面規範清楚，模組內部與外界解耦——平行設計成為可能。

### 線索三：符號版圖與工具鏈
設計者畫「棒狀圖（sticks）」——只標拓撲連接與相對位置，工具按 λ 規則生成實體幾何：

$$\text{sticks (拓撲)} \xrightarrow{\ \lambda\ \text{規則生成器}\ } \text{geometry (實體)}$$

這是「設計表示與物理實現分離」的第一次工程實踐，直接預示了後來的 EDIF、GDSII 工作流與生成的 layout generator 語言（如 1980s 的 silicon compilers）。

### MPC79：方法學的實彈演習
1979-80 年，Conway 組織 MPC79：12 所大學、數百個設計，集合成一張多專案晶片（multi-project chip）流片——證明「設計可攜 + 遠端整合 + 共享流片」閉環可行。這個模式就是 MOSIS（1981）與晶圓代工（TSMC 1987）的預演。

## 結案 -- 後果與影響
- **VLSI 教育革命**：這本書配上 MPC79，讓沒有 fab 的大學也能教與做 VLSI，十年間催生一代晶片設計師。
- **設計與製造解耦**：λ 規則 + 標準介面，使「設計公司不擁有 fab」成為可能——1987 年 TSMC 純代工模式的觀念前哨。
- **工具鏈的規格書**：設計規則檢查（DRC）從此以 λ 規則為標準輸入；符號版圖直接啟發 Magic（1983）的角針織編輯。
- **結構化設計的長影**：階層化、規則化、局部性三原則，至今仍是標準單元流程、FPGA 架構與 RTL 設計的鐵律。

## 關鍵人物與文獻
- **Carver Mead**（1934–）：Caltech 教授，VLSI 系統觀念與類比神經晶片先驅。
- **Lynn Conway**（1938–2024）：IBM→Xerox PARC→Michigan，VLSI 方法學與 MPC79 組織者，動態指令排程（1960s）的先驅。
- 文獻：
  - C. A. Mead, L. A. Conway, *Introduction to VLSI Systems*, Addison-Wesley, 1980.
  - L. Conway et al., "The MPC79 VLSI Microelectronic System Implementation Project," 1981（實彈演習報告）。
  - C. Mead, M. Rem, "Minimum Area VLSI Design," *VLSI Systems and Computations*, 1981（結構化設計的理論化）。
