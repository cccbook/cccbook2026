# 2017 John Hennessy & David Patterson —— RISC 的理論與教材

> 「1980 年，兩條校園計畫分別叫 RISC（伯克利）與 MIPS
> （史丹佛）。四十年的軍備賽後，全世界絕大多數處理器
> 核心是 RISC 血統。」

## 案件檔案

| 項目 | 內容 |
|---|---|
| 得主 | John L. Hennessy (1952–)、David A. Patterson (1947–) |
| 得獎理由 | RISC 架構的開創，以及量化設計方法的貢獻 |
| 關鍵詞 | RISC、MIPS、量化設計、Amdahl 定律 |

## 前因

1980 年，CISC（x86、VAX）的指令越來越複雜。Cocke
（1987 案）在 IBM 801 內部已發現「20% 指令佔 80% 執行
時間」，但未公開傳播。兩位教授各自重新偵破同一案件：
**複雜指令是設計債，不是資產**。

## 線索與推理

### 線索一：RISC 原理的公開論證

```
Patterson（伯克利 RISC-I, 1981）：
  測量 → 大多數指令簡單、頻繁
  設計 → 固定長度指令、load/store 架構（只有讀寫記憶體指令）
        大量暫存器（編譯器分配，Cocke 的 graph coloring）
Hennessy（史丹佛 MIPS, 1981）：
  「微處理器無互鎖管線階段」→ 硬體更簡、頻率更高
  編譯器承擔排程 → 硬體/軟體協同設計
```

### 線索二：量化設計方法（教科書體系）

《Computer Architecture: A Quantitative Approach》（1990）：

```
Amdahl 定律：加速比 S = 1 / ((1−f) + f/k)
  f = 可加速部分比例，k = 該部分加速倍數
  → 最佳化「熱點」優先，長尾無關緊要
CPU time = IC × CPI × 時脈週期 —— 一切效能討論的公理
```

**架構決策必須用測量與模型回答**——告別直覺式設計。

### 線索三：商業化與轉折

SPARC（Sun）、MIPS、PowerPC 一度百花齊放；最終 **ARM**
（指令簡潔 + 授權模式）統治行動端。2010s 的翻案：
**功耗牆**（Dennard 縮放失效）終結單核頻率賽，架構
重回設計中心——兩人在 2018 圖靈獎演講宣布「新黃金
時代」：DSA（領域專用架構，TPU 等）。

### 線索四：RISC-V 與開源 ISA

Patterson 晚年推動 RISC-V（2010 UC Berkeley）：開源、
模組化指令集——把 ISA 從專利武器變成公共品。

## 理論評析

RISC 戰役的偵探學：**複雜性必須有測得的收益才配存在**。

| CISC 主張 | RISC 反證 |
|---|---|
| 硬體多做事省軟體 | 編譯器更擅長排程（1987 案） |
| 指令多 = 能力強 | 80% 時間在簡單指令上 |
| 微碼靈活 | 微碼是隱藏的慢速直譯器 |

與 1984 Wirth 案、1999 Brooks 案同一哲學在硬體的回聲：
**簡單性是效能的前提**。

## 後果

- 智慧手機時代 = RISC 的全面勝利（ARM 核心 + Apple
  Silicon）。
- 「量化」文化進入系統研究（benchmark、performance
  counter）。
- DSA 路線直通深度學習加速器（2018 案的硬體支柱）。

## 關聯案件

→ [1987-John-Cocke](1987-John-Cocke.md)、[2018-Bengio-Hinton-LeCun](2018-Bengio-Hinton-LeCun.md)、[1984-Niklaus-Wirth](1984-Niklaus-Wirth.md)
