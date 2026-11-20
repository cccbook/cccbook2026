# MLIR 核心解析：多層中間表示法與現代異質編譯器架構

> 副標題：從方言設計、漸進式降階到 CPU、GPU、NPU 與硬體後端的實戰之路

一本關於 **MLIR（Multi-Level Intermediate Representation，多層中間表示法）** 的技術教科書。
它不是 API 索引，也不是使用手冊；每一節都回答同一個問題：**「這個機制，是為了讓誰在什麼時候能做什麼事？」**

全書圍繞四條主線展開：

* **為什麼需要多層 IR**——單一 IR 在領域語意、資訊時機、異質硬體三方面的結構性瓶頸。
* **核心抽象與執行機制**——`Operation` / `Region` / `Block` / `Type` / `Attribute` 的資料模型，以及 PassManager、Pattern Rewrite、Dialect Conversion、Verifier、Interface 五套通用機制。
* **方言生態與漸進式降階**——從 `tensor`、`linalg`、`scf`、`affine`、`memref`、`vector` 到 `gpu`、`llvm` 的完整降階路徑。
* **自訂方言與多元後端實戰**——從零打造一個 NPU 方言，並對接自訂 ISA、Runtime、HLS 與 HDL。

---

## 目錄

* 序章：為什麼編譯器需要「多層」中間表示法
    * [0.1-單一IR的結構性瓶頸](00.1-單一IR的結構性瓶頸.md)
    * [0.2-多層IR的核心哲學](00.2-多層IR的核心哲學.md)
    * [0.3-MLIR的誕生與設計目標](00.3-MLIR的誕生與設計目標.md)
* 第1章：MLIR 的世界觀——Operation、Block 與 Region
    * [1.1-一切皆Operation](01.1-一切皆Operation.md)
    * [1.2-Block與BlockArgument](01.2-Block與BlockArgument.md)
    * [1.3-Region的兩種語意](01.3-Region的兩種語意.md)
* 第2章：型別系統、屬性與符號表
    * [2.1-MLIR型別系統](02.1-MLIR型別系統.md)
    * [2.2-Attribute與編譯期常數](02.2-Attribute與編譯期常數.md)
    * [2.3-SymbolTable與跨區域參照](02.3-SymbolTable與跨區域參照.md)
* 第3章：TableGen 與宣告式 IR 定義
    * [3.1-為什麼需要TableGen](03.1-為什麼需要TableGen.md)
    * [3.2-ODS定義Operation](03.2-ODS定義Operation.md)
    * [3.3-DRR宣告式重寫規則](03.3-DRR宣告式重寫規則.md)
* 第4章：Pass 管理器與平行執行模型
    * [4.1-Pass生命週期與巢狀執行](04.1-Pass生命週期與巢狀執行.md)
    * [4.2-多執行緒平行化](04.2-多執行緒平行化.md)
    * [4.3-Analysis快取與失效](04.3-Analysis快取與失效.md)
* 第5章：模式改寫引擎與 Dialect Conversion
    * [5.1-GreedyPatternRewriteDriver](05.1-GreedyPatternRewriteDriver.md)
    * [5.2-DialectConversion框架](05.2-DialectConversion框架.md)
    * [5.3-Partial與FullLowering](05.3-Partial與FullLowering.md)
* 第6章：驗證器、介面與除錯工具鏈
    * [6.1-Verifier與結構不變式](06.1-Verifier與結構不變式.md)
    * [6.2-OpInterface與TypeInterface](06.2-OpInterface與TypeInterface.md)
    * [6.3-除錯工具鏈](06.3-除錯工具鏈.md)
* 第7章：高階計算與張量語義方言
    * [7.1-tensor與結構化運算](07.1-tensor與結構化運算.md)
    * [7.2-linalg與命名化結構化運算](07.2-linalg與命名化結構化運算.md)
    * [7.3-高階圖方言與算子融合](07.3-高階圖方言與算子融合.md)
* 第8章：迴圈、多面體與記憶體抽象方言
    * [8.1-scf結構化控制流](08.1-scf結構化控制流.md)
    * [8.2-affine多面體模型](08.2-affine多面體模型.md)
    * [8.3-memref記憶體抽象](08.3-memref記憶體抽象.md)
    * [8.4-迴圈變換模式](08.4-迴圈變換模式.md)
* 第9章：向量化與低階硬體方言的降階之路
    * [9.1-vector方言](09.1-vector方言.md)
    * [9.2-GPU降階路徑](09.2-GPU降階路徑.md)
    * [9.3-CPU降階路徑與llvm方言](09.3-CPU降階路徑與llvm方言.md)
* 第10章：從零打造自訂 Dialect
    * [10.1-自訂方言的抽象層級設計](10.1-自訂方言的抽象層級設計.md)
    * [10.2-TableGen規格與C++實作](10.2-TableGen規格與C++實作.md)
    * [10.3-Verifier與自訂Pass](10.3-Verifier與自訂Pass.md)
    * [10.4-測試與mlir-opt整合](10.4-測試與mlir-opt整合.md)
* 第11章：面向 NPU / TPU 與專用加速器的編譯降階
    * [11.1-脈動陣列與NPU的IR需求](11.1-脈動陣列與NPU的IR需求.md)
    * [11.2-張量分塊與片上緩衝排程](11.2-張量分塊與片上緩衝排程.md)
    * [11.3-DMA搬移生成](11.3-DMA搬移生成.md)
    * [11.4-對接自訂ISA與Runtime](11.4-對接自訂ISA與Runtime.md)
* 第12章：延伸至 HLS、可重構硬體與未來演進
    * [12.1-MLIR在HLS與HDL降階的角色](12.1-MLIR在HLS與HDL降階的角色.md)
    * [12.2-管線化與資料流排程的IR表達](12.2-管線化與資料流排程的IR表達.md)
    * [12.3-方言生態碎片化與標準化](12.3-方言生態碎片化與標準化.md)
    * [12.4-編譯器最佳化與自動化搜尋](12.4-編譯器最佳化與自動化搜尋.md)

---

## 本書的樣章線索

第四部會以一個貫穿的範例方言 `npu` 為主線，從第 10 章的 ODS 規格與 C++ 實作，一路做到第 11 章的 DMA 生成與自訂 ISA 對接。閱讀時可以把它當成一個專案來追蹤。

## 環境說明

文中程式碼片段以 MLIR 上游（LLVM 17 以上）為基準：

```bash
# 建置（LLVM 官方流程）
cmake -G Ninja llvm \
  -DLLVM_ENABLE_PROJECTS="mlir" \
  -DLLVM_TARGETS_TO_BUILD="host" \
  -DLLVM_ENABLE_ASSERTIONS=ON \
  -DCMAKE_BUILD_TYPE=Release
ninja check-mlir
```

常用工具：`mlir-opt`（方言與 pass 的瑞士刀）、`mlir-translate`（與 LLVM IR / SPIR-V 互轉）、`mlir-reduce`（差異化測試）、`mlir-tblgen`（展開 ODS 規格）、`FileCheck` 與 `lit`（回歸測試）。

## 延伸資源

* MLIR 官方文件：<https://mlir.llvm.org/docs/>
* MLIR Dialects 一覽：<https://mlir.llvm.org/docs/Dialects/>
* MLIR Rationale（設計理由）：<https://mlir.llvm.org/docs/Rationale/>
* Chris Lattner, *MLIR: Scaling Compiler Infrastructure for Domain Specific Computation*, LLVM Blog, 2021-01-26：<https://blog.llvm.org/2021/01/mlir-scaling-compiler-infrastructure-for-domain.html>
