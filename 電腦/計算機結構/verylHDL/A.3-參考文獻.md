# 附錄 A.3：參考文獻與延伸閱讀

本附錄列出全書引用或建議延伸閱讀的真實文獻，依主題分類。

## Veryl 官方資源

- Veryl 官方手冊：https://doc.veryl-lang.org
- verylup（工具鏈管理器）：https://github.com/veryl-lang/verylup
- Veryl 原始碼倉庫：https://github.com/veryl-lang/veryl

## 硬體描述語言標準

- IEEE Std 1364-2005, IEEE Standard for Verilog Hardware Description Language。
- IEEE Std 1800-2023, IEEE Standard for SystemVerilog—Unified Hardware Design, Specification, and Verification Language。
- IEEE Std 1076-2019, IEEE Standard VHDL Language Reference Manual。
- Sutherland, Davidmann, Flake, *SystemVerilog for Design*（Springer）。

## 架構與 RISC

- Hennessy, John L., and David A. Patterson. *Computer Architecture: A Quantitative Approach*, 6th ed., Morgan Kaufmann, 2017。
- Patterson, David A., and John L. Hennessy. *Computer Organization and Design: The Hardware/Software Interface*, RISC-V edition, Morgan Kaufmann, 2020。
- Patterson & Séquin, "RISC-I: A Reduced Instruction Set VLSI Computer", ISCA 1981。
- RISC-V ISA Specification（Volume I: Unprivileged ISA；Volume II: Privileged Architecture）：https://riscv.org/technical/specifications
- Waterman & Asanović 等人關於 RISC-V 的 Berkeley 技術報告與論文（見 riscv.org 與 UC Berkeley 文件庫）。

## 握手與 FIFO 設計經典

- Cummings, Clifford E., "Simulation and Synthesis Techniques for Asynchronous FIFO Design", SNUG San Jose 2002。http://www.sunburst-design.com/papers/
- Cummings, "Simulation and Synthesis Techniques for Asynchronous FIFO Design with Asynchronous Pointer Comparison", SNUG 2002。
- Cummings, "Clock Domain Crossing (CDC) Design & Verification Techniques Using SystemVerilog", SNUG Boston 2008。
- Gaisler, Jan, "A Structured VHDL Design Method"（設計慣例與 CSR 文件制度的參考）。

## AMBA 與匯流排

- ARM, *AMBA AXI and ACE Protocol Specification*（ARM IHI 0022，含 AXI4-Lite）。
- ARM, *AMBA 5 AXI Protocol Specification*（ARM IHI 0022 最新版）。
- Xilinx, *AXI Reference Guide*（UG1037）。

## 開源 EDA 與 FPGA

- Wolf, Clifford, "Yosys Open SYnthesis Suite"：https://yosyshq.net/yosys/
- nextpnr：https://github.com/YosysHQ/nextpnr
- Project IceStorm（iCE40 位元流反向工程）：http://www.clifford.at/icestorm/
- OpenROAD：https://theopenroadproject.org
- OpenPDKs / SkyWater SKY130 PDK：https://github.com/google/skywater-pdk
- Tiny Tapeout：https://tinytapeout.com
- efabless / Caravel 與 MPW shuttle 文件（efabless 已於 2025 年停止營運，文件存檔於社群鏡像）。
- Weste & Harris, *CMOS VLSI Design: A Circuits and Systems Perspective*, 4th ed., Addison-Wesley。

## 現代 HDL 官方文件

- Chisel：https://www.chisel-lang.org
- SpinalHDL：https://spinalhdl.github.io/SpinalDoc-RTD/
- Amaranth：https://amaranth-lang.org
- Bluespec：https://github.com/B-Lang-org
- Silice：https://github.com/sylefeb/silice

## 驗證

- SymbiYosys（開源 formal flow）：https://symbi-yosys.readthedocs.io 或 https://github.com/YosysHQ/symbiyosys
- cocotb 官方文件：https://www.cocotb.org
- Spear, Wile, Wodey 等, *SystemVerilog for Verification*（Springer）。

## 歷史與思想

- Mead, Carver, and Lynn Conway. *Introduction to VLSI Systems*, Addison-Wesley, 1980。
- Thornton, James E. *Design of a Computer: The Control Data 6600*, Scott, Foresman, 1970（CDC 6600 scoreboard 的第一手文獻）。
- Tomasulo, R. M., "An Efficient Algorithm for Exploiting Multiple Arithmetic Units", IBM Journal of R&D, 1967。
- Hennessy & Patterson, "A New Golden Age for Computer Architecture", Turing Award Lecture, CACM, 2019。
- Ross Freeman 之 FPGA 奠基專利（US 4,642,487，Xilinx, 1987）。

以上連結與文獻於撰寫當時皆為真實存在；網址可能隨時間變動，若失效請以搜尋文獻名稱為準。
