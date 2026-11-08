# 《Veryl HDL：從 Verilog 的歷史走向現代硬體設計》

本書講解 Veryl HDL——一個以 Rust 撰寫、可轉譯（transpile）為 SystemVerilog 的現代硬體描述語言。除了語法本身，本書也花了相當篇幅回顧 HDL 四十年的歷史脈絡：Gat e Array 到 Verilog 的誕生、商業 EDA 的形成、語言標準化的政治、開源 FPGA 工具鏈的興起，以及軟體工程方法論如何回頭重塑硬體設計流程。歷史部分均為真實事件，並盡量說明科技、經濟、制度、文化之間的驅動關係。

## 目錄

* 第1章-硬體描述語言的四十年長路
    * [1.1-從閘級網表到 Verilog：語言為何而生](01.1-從閘級網表到Verilog.md)
    * [1.2-VHDL 與 Verilog 的雙雄競爭與標準化政治](01.2-VHDL與Verilog的競爭.md)
    * [1.3-SystemVerilog 的膨脹與工程界的疲乏](01.3-SystemVerilog的膨脹.md)
    * [1.4-軟體工程的回頭浪潮：Cargo、LSP 與新一代 HDL](01.4-軟體工程的回頭浪潮.md)
    * [1.5-Veryl 的定位與哲學：零額外成本的可讀轉譯](01.5-Veryl的定位與哲學.md)
* 第2章-開發環境建置
    * [2.1-安裝 verylup 與工具鏈版本管理](02.1-安裝verylup.md)
    * [2.2-編輯器整合：VS Code、Neovim 與 LSP](02.2-編輯器整合與LSP.md)
    * [2.3-Veryl.toml：專案設定的核心](02.3-Veryl.toml專案設定.md)
    * [2.4-第一個專案：建立、build 與觀察轉譯輸出](02.4-第一個專案.md)
* 第3章-型別系統與基礎語法
    * [3.1-位寬與型別：讓 width 進入型別檢查](03.1-位寬與型別.md)
    * [3.2-logic、bit 與內建整數型別](03.2-logic與bit型別.md)
    * [3.3-Struct 與 Enum：資料結構的現代化](03.3-Struct與Enum.md)
    * [3.4-Package 與 pub：模組化的型別共享](03.4-Package與pub.md)
* 第4章-模組與連接
    * [4.1-Module 宣告與省略 port 方向的革新](04.1-Module宣告與port.md)
    * [4.2-Instance 與自動連線：`<>` 運算子](04.2-Instance與自動連線.md)
    * [4.3-Interface 與 Modport：匯流排連接的解方](04.3-Interface與Modport.md)
    * [4.4-Proto Module 與 Proto Package：行為契約](04.4-ProtoModule與契約.md)
* 第5章-時序與組合邏輯
    * [5.1-comb 區塊：組合邏輯的明確化](05.1-comb區塊.md)
    * [5.2-ff 區塊與 clock/reset 型別：把慣例變成語言](05.2-ff區塊與時脈重置.md)
    * [5.3-Reset 的三種極性與非同步議題](05.3-Reset極性與非同步.md)
    * [5.4-狀態機設計模式：從兩段式到 enum 驅動](05.4-狀態機設計模式.md)
* 第6章-泛型與產生邏輯
    * [6.1-參數化模組與 generic 語法](06.1-參數化模組.md)
    * [6.2-generate：條件與迴圈生成](06.2-generate生成.md)
    * [6.3-通用元件實作：FIFO、Mux、Arbiter](06.3-通用元件實作.md)
    * [6.4-函式與運算子的擴充能力](06.4-函式與運算子.md)
* 第7章-驗證與模擬
    * [7.1-Testbench 的結構與模擬器生態](07.1-Testbench結構.md)
    * [7.2-embed 機制：與 SystemVerilog 共存](07.2-embed嵌入機制.md)
    * [7.3-搭配 Verilator 進行快速模擬](07.3-搭配Verilator.md)
    * [7.4-Cocotb 與 Python 驗證的混搭](07.4-Cocotb與Python驗證.md)
    * [7.5-veryl test 與自動化測試流程](07.5-veryl-test自動化.md)
* 第8章-工具鏈與工程化實務
    * [8.1-veryl check：靜態檢查與除錯](08.1-veryl-check靜態檢查.md)
    * [8.2-veryl fmt：把格式之爭交給機器](08.2-veryl-fmt格式化.md)
    * [8.3-veryl doc 與文件自動化](08.3-veryl-doc文件.md)
    * [8.4-Git 與 CI/CD：HDL 的持續整合](08.4-Git與CICD.md)
    * [8.5-從既有 SystemVerilog 專案漸進遷移](08.5-漸進遷移策略.md)
* 第9章-實戰專案（一）：流水線處理單元
    * [9.1-專案目標與架構設計](09.1-專案目標與架構.md)
    * [9.2-握手協定與 valid/ready 模式](09.2-握手協定.md)
    * [9.3-流水線實作與 hazards 處理](09.3-流水線實作.md)
    * [9.4-轉譯輸出分析與資源對比](09.4-轉譯輸出分析.md)
* 第10章-實戰專案（二）：AXI4-Lite 匯流排控制器
    * [10.1-AXI4-Lite 協定與其歷史](10.1-AXI4-Lite協定.md)
    * [10.2-以 Interface 建構 Master 與 Slave](10.2-Interface建構Master與Slave.md)
    * [10.3-暫存器模組與記憶體映射](10.3-暫存器模組.md)
* 第11章-實戰專案（三）：RV32I CPU 核心
    * [11.1-RISC-V 的誕生：開放 ISA 的思想史](11.1-RISC-V的誕生.md)
    * [11.2-五階段管線：IF、ID、EX、MEM、WB](11.2-五階段管線.md)
    * [11.3-冒險與繞送：資料相關的處理](11.3-冒險與繞送.md)
    * [11.4-上 FPGA：綜合與部署流程](11.4-上FPGA綜合部署.md)
* 第12章-生態、社群與未來
    * [12.1-開源 EDA 的興起：從 ICCAD 競賽到 Yosys](12.1-開源EDA的興起.md)
    * [12.2-Veryl 的發展史與設計決策記錄](12.2-Veryl的發展史.md)
    * [12.3-與 Chisel、SpinalHDL、Amber 等的比較](12.3-與其他現代HDL比較.md)
    * [12.4-HDL 的下一個十年](12.4-HDL的下一個十年.md)
* 附錄
    * [A.1-Veryl 與 SystemVerilog 對照速查表](A.1-Veryl與SystemVerilog對照表.md)
    * [A.2-關鍵字與內建函式清單](A.2-關鍵字與內建函式清單.md)
    * [A.3-參考文獻與延伸閱讀](A.3-參考文獻.md)
