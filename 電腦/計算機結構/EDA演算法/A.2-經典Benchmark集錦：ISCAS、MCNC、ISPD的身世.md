# A.2 經典 Benchmark 集錦：ISCAS、MCNC、ISPD 的身世

EDA 演算法研究的進步，很大程度繫於「大家用同一組題目、同一把尺」這件事。從 1980 年代中期開始，幾個關鍵的 benchmark 集——ISCAS、MCNC、ITC、EPFL，以及歷年 ISPD/ICCAD 競賽題——先後成為各子領域的通用度量衡。它們不只是測試檔案，更塑造了一種研究文化：論文必須給出可與前人對照的數字，方法的好壞才有公評。本附錄逐一考據這些資料集的身世、規模與至今的用途。

## ISCAS'85：組合電路的萬年標竿

ISCAS'85 由 AT&T Bell Labs 的 Franc Brglez 與 Hiroaki Fujiwara 等人在 1985 年 IEEE International Symposium on Circuits and Systems 上發表，是針對組合電路測試與合成而生的十個大型電路（c432、c499、c880、c1355、c1908、c2670、c3540、c5315、c6288、c7552），規模從數百個閘到五千多閘，並附上測試向量與 fault coverage 資料。它們多數改編自軍用與工業界的實際設計（如 c6288 是一個 16×16 乘法器）。四十年過去，ISCAS'85 仍是 ATPG、SAT-based verification、邏輯優化論文的必備題組；c6288 因為具有極深的算術結構，至今仍是 SAT solver 與 equivalence checking 的難題。

## ISCAS'89：把狀態機納入版圖

五年後，Brglez、Bryan 與 Kozminski 再以 ISCAS'89 補上了循序電路（s298、s5378、s9234、s15850、s38417、s38584 等），搭配掃描鏈（full-scan）假設，讓 ATPG 研究得以在含正反器的電路上進行。這組電路最大的貢獻是確立了「以 scan 化循序電路做測試生成」的實驗範式，s38417 與 s38584 至今仍是測試壓縮、scan-chain optimization 論文的標配。

## MCNC：布林函數與 FPGA 基準的搖籃

MCNC（Microelectronics Center of North Carolina，位於北卡羅來納州 Research Triangle Park）在 1991 年前後釋出一大批兩層式與多層式布林函數（alu4、apex1、table3、ex5p、misex3 等），以及配套的 Fred Yang 所整理之邏輯函數集。這些例子隨後成為兩個子領域的共同語言：一個是兩層式 PLD 的 minimization（ESPRESSO 時代），另一個是 FPGA 技術映射與 packing——VPR/VTR 的 benchmark suite 中，仍有大量 MCNC 電路經由 SIS/ABC 折疊成 LUT 網表後被沿用至今。MCNC 的意義在於它證明了「小而真實」的函數集足以驅動二十年的演算法研究。

## IWLS：以工作坊為名的小型實驗場

IWLS（International Workshop on Logic and Synthesis）自 1990 年代起由參與者輪流提供一些具有挑戰性的控制邏輯與算術電路，逐漸累積成 IWLS'93、IWLS'98、IWLS 2005 等小型集合。它們規模不大，但特別適合測試 state minimization、retiming、resynthesis 等細粒度演算法；Berkeley ABC 發布的例子中就有不少取自 IWLS。

## ITC'99：走向工業級的測試基準

ITC'99 由 IEEE Test Technology Technical Council（TTTC）在 1999 年推出（b01、b14、b17、b21、b22 等），直接取自法國 ITC 會議上公布的工業電路（原始設計來自 Synopsys/Philips 等單位），規模動輒數萬到數十萬閘，並以 VHDL 形式發布。它把測試研究的舞台從數千閘拉到數十萬閘，成為 BIST、scan 壓縮、test power 研究的後繼標竿。

## EPFL benchmark：現代邏輯優化的新標尺

隨著電路規模成長，ISCAS 電路在 2010 年代對現代合成器而言已太小，於 2015 年由 Luca Amarù（當時在 EPFL 的 Giovanni De Micheli 實驗室）、Pierre-Emmanuel Gaillardon 等人整理推出 EPFL Combinational Benchmark Suite，包含加法器（adder）、乘法器（multiplier、multiplier_dop756）、bar、sqrt、div、square 等十個大型算術/控制電路，最大者達百萬級節點。EPFL 系列也提供了完整的 AIG/XAG 優化競賽結果，使 ABC、mockturtle（LSOracle、MIG 之類的 mapper）等現代工具能直接比較 size 與 depth，成為近年邏輯優化論文的首選題組。

## ISPD / ICCAD Contest：實體設計演算法的年度武林大會

與邏輯層 benchmark 不同，實體設計領域的推動力來自「比賽」。IBM 在 1990 年代末、2000 年代初將真實工業設計（IBM01、IBM02……IBM18 等）釋出為 placement benchmark；至 2000 年代中期，ISPD 與 ICCAD 開始年年舉辦競賽：ISPD 2005/2006 placement contest（基於 IBM 場景，催生了 mPL、FastPlace 等新一代 placer 的直接對比）、ICCAD 2004/2007 placement、ISPD 2007 起的 clock tree、ISPD 2011/2012 的 routing（催生 NTUgr、BonnRoute 等強力 router）、ISPD 2013 的詳細繞線與 ISPD 2015/2016 的 blockage placement、ICCAD 2012 的 CAD Contest（含鄰域 routing、multi-net routing 題），以及近年 ICCAD/ISPD 的 macro placement（與 Google RL placement 論文的辯論直接相關）與 ML 賽題。這些比賽最大的制度貢獻，是把「演算法好不好」從主觀評述變成排行榜上的單一數字（HPWL、overflow、runtime），也把工業界（IBM、NVIDIA、Cadence、Intel）的真實題目帶進學術圈。VLSI CAD 的多位頂尖研究者——如德州大學的 Igor Markov、密西根大學、Georgia Tech、清大與台大許多團隊——的演算法生涯，都與某一年 contest 題目直接掛鉤。

## VTR benchmark suite：FPGA 架構研究的統一戰場

FPGA 端的對應物是 VTR（Verilog-to-Routing）專案自 2010 年代初隨 VPR 7 整理出的 VTR Benchmark Suite（後續版本稱 VTR 8 benchmarks），從 ch_intrinsics、diffeq1 至LU32peeng、spmxv、bgm 等共約二十個設計，橫跨 MCNC 舊題與新的 CHiP 控制器、訊號處理核心。配合固定的 FPGA 架構描述（k6_frac_N10_frac_chain_mem32K 等標準 arch），研究者可以單一指標（critical path delay、LUT/FF/BRAM 使用量）直接比較架構與 CAD 演算法。本書 FPGA 章節的實驗，即採用同一套準則。

## Benchmark 的研究文化意義

回顧這些資料集，可以歸納出 EDA 研究文化的一個核心機制：一個子領域要能快速進步，必須先「標準化題目」——ISCAS 與 MCNC 完成了測試與合成的標準化；EPFL 與 VTR 完成了現代邏輯優化與 FPGA CAD 的標準化；ISPD/ICCAD contest 則以競賽形式，把實體設計的標準化推到極致。有了共同的題目，才有 reproducibility（可重現性）的壓力：論文必須說明編譯器版本、機器、runtime 與所有次要參數，否則數字無法被引用。這種文化甚至反向塑造了工具本身——ABC、VPR 之所以把命令列、輸出格式、seed 控制做得如此嚴謹，正是為了讓別人能精確重跑。可以說，理解一個 benchmark 的身世，就是理解該子領域二十年演算法演進的座標系。

| 資料集 | 年份 | 發起單位/人物 | 電路規模 | 主要用途 |
|---|---|---|---|---|
| ISCAS'85 | 1985 | Bell Labs, Brglez & Fujiwara | 數百–數千閘，10 題 | ATPG、SAT、組合合成 |
| ISCAS'89 | 1989 | Brglez, Bryan & Kozminski | 數百–數萬閘（含 FF） | 循序測試、scan 優化 |
| MCNC | 1991 | 北卡 MCNC | 小型布林函數 | 兩層化簡、FPGA 映射 |
| IWLS | 1993– | IWLS 工作坊 | 小型控制邏輯 | 邏輯優化細部研究 |
| ITC'99 | 1999 | IEEE TTTC | 數萬–數十萬閘 | BIST、scan 壓縮 |
| EPFL | 2015 | EPFL, Amarù & De Micheli | 至百萬節點 | 現代邏輯優化 |
| ISPD/ICCAD contest | 2005– | ISPD/ICCAD、IBM、NVIDIA 等 | 工業級（百萬閘以上） | placement、routing、CTS、ML |
| VTR suite | 2013– | 多倫多大學 | 跨度大 | FPGA 架構與 CAD 比較 |
