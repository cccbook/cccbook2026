# 2020-AMD收購Xilinx

## 案件摘要

2020 年 10 月 27 日，AMD 宣布以價值 350 億美元的全股票交易收購 Xilinx；2022 年 2 月 14 日交易完成。至此，全球 FPGA 雙雄先後被 CPU 巨頭收編——Altera 於 2015 年被 Intel 收購、Xilinx 於 2022 年歸入 AMD，可程式邏輯產業從獨立晶片時代進入「CPU 巨頭的異質運算子事業」時代。

## 前因 -- 為什麼會會有這個案子

2010 年代末期，半導體產業的遊戲規則改變了。摩爾定律放緩使單一製程節點的投資暴增（7nm 廠房動輒數百億美元），單一產品線的公司難以攤提成本；同時，資料中心的工作負載從「通用運算」轉向「AI 訓練/推論 + 通用運算」的混合負載，沒有任何一種單一架構能同時最佳化兩者。於是「異質運算」（CPU + GPU + FPGA/自適應 + 专用加速器）成為產業共識。

Xilinx 的處境尤其微妙。它在 2018 年推出 Versal ACAP，宣示從 FPGA 轉型為「自適應運算平台」，但轉型需要龐大的研發與行銷資源：7nm 製程的 NRE 成本、資料中心市場的生態投資（Vitis、Vitis AI）、5G 與自駕市場的認證成本——這些對一家年營收約 30 億美元的公司而言是沉重負擔。Xilinx 需要一個更大的母公司。

AMD 則正處於反攻的高峰。Zen 架構讓 Ryzen 與 EPYC 在 CPU 市場重奪市佔，但 AMD 清楚知道：在資料中心，CPU 只是入場券，真正的成長在 GPU 與自適應運算。AMD 已有 GPU（收購 ATI 而來），缺的是「可重組態加速」這一塊。Xilinx 的 FPGA/ACAP、以及它在航太國防、5G 通訊、工業嵌入式市場的深厚基礎，正好補上這個拼圖。

## 線索與推理 -- 數學式、程式、理論（本體，最詳細）

### 線索一：AMD 的異質運算戰略

AMD 的戰略藍圖是「全栈異質運算」：把 CPU（Zen）、GPU（RDNA/CDNA）、FPGA/自適應（Versal/Zynq）、以及軟體層（ROCm、Vitis）整合成一個平台。戰略的數學基礎是 **Amdahl's Law（Amdahl 定律）** 的反用：

$$S = \frac{1}{(1-p) + \frac{p}{k}}$$

其中 $S$ 是加速比、$p$ 是可平行化比例、$k$ 是加速倍率。Amdahl 定律原本警告「序列部分限制平行加速」，但 AMD 的解讀是：**如果連序列部分（控制流、作業系統、網路協定）都可以被異質加速器加速**（例如 DPU/SmartNIC 用 FPGA 加速網路協定、用 AIE 加速 AI），則「不可加速部分」的定義本身會縮小，加速上限被推高。

具體的產品矩陣：

| 市場 | AMD 原有 | Xilinx 帶來 | 整合後 |
|------|------|------|------|
| 資料中心 | EPYC CPU、Instinct GPU | Alveo 加速卡、Versal | CPU+GPU+自適應全棧 |
| 嵌入式 | Ryzen Embedded | Zynq SoC、Kintex | 完整嵌入式 SoC 線 |
| 通訊/5G | （薄弱） | Versal、RFSoC | 強勢（RFSoC 獨占性高） |
| 航太國防 | （有限） | Virtex、Space-grade 產品 | 深厚基礎 |
| 車用 | Ryzen/EPYC 車用 | Zynq UltraScale+ 車規 | ADAS 完整方案 |

RFSoC（整合 ADC/DAC 的 Zynq UltraScale+）是 Xilinx 最具獨占性的資產：5G Open RAN、相控陣雷達、衛星通訊都需要它，短期內無替代品。這是 AMD 願意付出高溢價的關鍵原因之一。

### 線索二：交易結構——全股票換股的財務計算

交易結構是「全股票換股」：每股 Xilinx 換 1.7234 股 AMD 股票。宣布日（2020-10-27）AMD 收盤價約 $78.31，故每股 Xilinx 的隱含收購價為：

$$1.7234 \times 78.31 \approx \$134.97$$

Xilinx 流通股數約 2.45 億股，故總股本對價為：

$$2.45 \times 10^8 \times 134.97 \approx \$331 \text{ 億}$$

加上承擔債務等調整，交易總值約 **350 億美元**。全股票交易的特點：

- **無現金流出**：AMD 不必籌措 350 億現金（當時 AMD 現金遠不足），只發行約 4.22 億股新股（$2.45 \times 1.7234 \approx 4.22$ 億股）。
- **風險共擔**：Xilinx 股東成為 AMD 股東，若 AMD 股價下跌，收購價值也縮水——宣布日到交割日之間 AMD 股價大漲，實際交割時交易價值已膨脹至約 500 億美元。
- **稅務遞延**：換股在美國稅法下可遞延資本利得稅，對 Xilinx 股東友好。
- **股權稀釋**：交割後原 AMD 股東持股約 74%，原 Xilinx 股東約 26%。

交割日（2022-02-14）AMD 股價約 $115，故實際交易價值為：

$$4.22 \times 10^8 \times 115 \approx \$485 \text{ 億}$$

這比宣布日的 350 億高出近四成——是 AMD 股價在這 16 個月間的漲幅「免費」送給了這筆交易。

### 線索三：Zynq/Versal 在 AMD 產品線中的定位

收購後，Xilinx 成為 AMD 的「Adaptive and Embedded Computing Group」（自適應與嵌入式運算事業群）。Zynq/Versal 的定位：

- **Zynq（PS+PL SoC）**：嵌入式市場的主力。工業控制、機器視覺、車用 ADAS、醫療設備。特點是「單晶片解決控制 + 運算 + 介面」，SKU 眾多、客戶黏性高、生命週期長（工業客戶常用 10 年以上）。
- **Versal（ACAP）**：高階市場的先鋒。5G 通訊、資料中心加速、國防雷達。AI Engine 是差異化武器。
- **RFSoC**：通訊與國防的皇冠明珠。整合 12-bit ADC/DAC 與 FPGA，是 5G Open RAN 與電子戰的關鍵元件。
- **Alveo**：資料中心加速卡。與 AMD 的 EPYC/Instinct 形成「伺服器內異質組合」。

策略推理：AMD 收購 Xilinx 不是為了「賣更多 FPGA」，而是為了「在資料中心賣更完整的異質平台」。Xilinx 獨立時難以進入 hyperscale 的核心採購清單（規模太小、生態不如 NVIDIA），但併入 AMD 後，「EPYC + Instinct + Alveo」可以作為整機櫃方案銷售，這是規模經濟與生態協同的乘數效應。

### 線索四：併購後 FPGA 市場版圖

併購後的可程式邏輯市場版圖（約 2022–2024 年市佔估計，全球 FPGA 市場年規模約 80–100 億美元）：

| 廠商 | 母公司 | 市佔（估計） | 主要產品 | 主力市場 |
|------|------|------|------|------|
| AMD (Xilinx) | AMD | 約 50% | Versal、Zynq、Kintex、Artix | 資料中心、通訊、國防、工業 |
| Intel (Altera) | Intel | 約 25–30% | Agilex、Stratix、Cyclone、MAX | 資料中心、通訊 |
| Lattice | 獨立 | 約 10% | iCE40、ECP5、CrossLink、Certus | 低功耗、邊緣 AI、消費電子 |
| Microchip (Microsemi/Microchip) | Microchip | 約 5–8% | PolarFire、SmartFusion、IGLOO | 國防、航太、工業（低功耗） |
| 其他（Gowin、Achronix 等） | 獨立 | 約 2–5% | Gowin FPGA、Speedster | 中小規模、設計服務 |

推理的關鍵觀察：**Lattice 成為唯一純 FPGA 獨立上市公司**，它以低功耗、小晶片、邊緣 AI 為利基，避開了與雙巨頭的正面对決。Microchip 則以「耐輻射、低功耗、長壽命」的國防航太利基生存。市場從「雙雄競爭」變成「兩個 CPU 巨頭的子事業 + 兩個利基獨立廠」的新格局。

## 結案 -- 後果與影響

交易完成後，AMD 保留了 Xilinx 的品牌（產品仍以 Xilinx/Versal/Zynq 名義銷售），並把資源投入 Versal 下一代與資料中心整合。Victor Peng 加入 AMD 成為執行副總裁，掌管自適應運算事業。2023 年起，AMD 推出「EPYC + Instinct + Versal」的整體資料中心方案，並開始把 Versal AI Engine 與 Instinct GPU 的軟體生態整合（ROCm + Vitis）。

對產業的深遠影響：FPGA 從獨立產業變成 CPU 巨頭的子事業，獨立 FPGA 公司的數量大幅減少，利基化成為生存法則。同時，「自適應運算」成為 AMD 的第二支柱（僅次於 CPU/GPU），在 2023 年後 AMD 的 AI 戰略中，Versal/Zynq 扮演邊緣與通訊 AI 的角色，與 Instinct GPU 的資料中心角色互補。

影響條列：

- **產業集中化**：FPGA 雙雄皆歸 CPU 巨頭，獨立廠剩 Lattice 與 Microchip 等利基玩家。
- **異質平台整合**：資料中心方案從「賣晶片」變成「賣 CPU+GPU+FPGA 整機方案」。
- **產品線延續**：Zynq/Versal/RFSoC 品牌保留，航太國防與通訊市場不受影響。
- **研發資源放大**：7nm→5nm→3nm 的先進製程投資有了更大的母公司支撐。
- **軟體生態整合**：Vitis 與 ROCm 整合，統一 AMD 的異質開發模型。
- **象徵意義**：可程式邏輯 40 年的獨立歷史（Xilinx 1984 創立）畫下句點，開啟「異質運算新紀元」。

## 關鍵人物與文獻

- **Lisa Su**：AMD 執行長，主導收購交易與後續整合，AMD 異質運算戰略的總設計師。
- **Victor Peng**：時任 Xilinx 執行長，收購後成為 AMD 執行副總裁，掌管自適應運算事業群。
- **AMD 官方新聞稿（2020-10-27）**："AMD to Acquire Xilinx, Creating the Industry's High Performance Computing Leader"，宣布交易。
- **AMD 官方新聞稿（2022-02-14）**："AMD Completes Acquisition of Xilinx"，宣布交割。
- **Amdahl, G.M., "Validity of the Single Processor Approach to Achieving Large Scale Computing Capabilities"**（AFIPS 1967）：Amdahl 定律原始論文。
- **Xilinx 10-K 年報（2020 財年）**：交易前的公司財務與市場地位資料。
