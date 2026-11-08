# 開放晶片之路：OpenROAD 與開源 EDA 的誕生

一本寫給晶片設計工程師、學生與開源硬體愛好者的 OpenROAD 深度導覽。本書不只講工具怎麼用，更講這一切是怎麼來的：從 1980 年代 EDA 產業的成形、DARPA 的押注、學術界演算法的沉澱，到 RISC-V 與 SkyWater 130nm 開源 PDK 匯流成「24 小時內無人值守完成 RTL-to-GDSII」的浪潮。技術、經濟、制度與文化如何互相驅動，將貫穿全書。

## 目錄

* 第1章-為什麼晶片設計需要開源
    * [1.1-被授權費鎖住的設計牆](01.1-被授權費鎖住的設計牆.md)
    * [1.2-EDA 產業的四十年簡史](01.2-EDA產業的四十年簡史.md)
    * [1.3-DARPA 的賭注與 OpenROAD 誕生](01.3-DARPA的賭注與OpenROAD誕生.md)
    * [1.4-RISC-V 與開源硬體運動的合流](01.4-RISC-V與開源硬體運動的合流.md)

* 第2章-OpenROAD 的架構與開發環境
    * [2.1-單一應用程式與模組化資料庫 OpenDB](02.1-單一應用程式與模組化資料庫OpenDB.md)
    * [2.2-建置環境：原始碼編譯與 Docker](02.2-建置環境：原始碼編譯與Docker.md)
    * [2.3-Tcl 與 Python：兩種驅動晶片的方式](02.3-Tcl與Python：兩種驅動晶片的方式.md)
    * [2.4-ORFS：把整條流程裝進一個 Makefile](02.4-ORFS：把整條流程裝進一個Makefile.md)

* 第3章-從邏輯到版圖的第一步
    * [3.1-Yosys 與邏輯綜合的開源之路](03.1-Yosys與邏輯綜合的開源之路.md)
    * [3.2-讀懂 PDK：LEF、DEF 與 Liberty](03.2-讀懂PDK：LEF、DEF與Liberty.md)
    * [3.3-Floorplanning：在矽上畫出城市的街道](03.3-Floorplanning：在矽上畫出城市的街道.md)
    * [3.4-Macro Placement：記憶體巨塊的放置難題](03.4-MacroPlacement：記憶體巨塊的放置難題.md)

* 第4章-擺放：數十億電晶體的座位表
    * [4.1-Global Placement 與 RePlAce 演算法](04.1-GlobalPlacement與RePlAce演算法.md)
    * [4.2-擁塞與密度：繞線塞車的預防醫學](04.2-擁塞與密度：繞線塞車的預防醫學.md)
    * [4.3-Detailed Placement：合法化與 OpenDP](04.3-DetailedPlacement：合法化與OpenDP.md)

* 第5章-時間就是一切：時脈與時序
    * [5.1-OpenSTA：靜態時序分析的核心](05.1-OpenSTA：靜態時序分析的核心.md)
    * [5.2-TritonCTS：時脈樹綜合](05.2-TritonCTS：時脈樹綜合.md)
    * [5.3-Skew、Latency 與功耗的三角習題](05.3-Skew、Latency與功耗的三角習題.md)

* 第6章-繞線與簽核：通往 GDSII 的最後一哩
    * [6.1-FastRoute：全域繞線的擁塞地圖](06.1-FastRoute：全域繞線的擁塞地圖.md)
    * [6.2-TritonRoute：詳細繞線與先進製程 DRC](06.2-TritonRoute：詳細繞線與先進製程DRC.md)
    * [6.3-OpenRCX：寄生參數萃取與 SPEF](06.3-OpenRCX：寄生參數萃取與SPEF.md)
    * [6.4-時序修復與 Signoff 的最後衝刺](06.4-時序修復與Signoff的最後衝刺.md)

* 第7章-PDK 實戰：從 ASAP7 到 SkyWater 130nm
    * [7.1-ASAP7：一個為研究而生的 7nm 預測型 PDK](07.1-ASAP7：一個為研究而生的7nm預測型PDK.md)
    * [7.2-SkyWater 130nm：真正可以流片的開源 PDK](07.2-SkyWater130nm：真正可以流片的開源PDK.md)
    * [7.3-Google MPW 與 Efabless：開源晶片上天的制度創新](07.3-GoogleMPW與Efabless：開源晶片上天的制度創新.md)
    * [7.4-Magic 與 KLayout：DRC 與 LVS 驗證](07.4-Magic與KLayout：DRC與LVS驗證.md)

* 第8章-端到端實作：從 RISC-V 到 GDSII
    * [8.1-Ibex 與 Rocket：開源處理器的流程實測](08.1-Ibex與Rocket：開源處理器的流程實測.md)
    * [8.2-PPA 與 Design Space Exploration](08.2-PPA與DesignSpaceExploration.md)
    * [8.3-自動調優：機器學習走進 EDA](08.3-自動調優：機器學習走進EDA.md)

* 第9章-社群、制度與未來
    * [9.1-3D-IC 與先進封裝的下一戰場](09.1-3D-IC與先進封裝的下一戰場.md)
    * [9.2-如何參與 OpenROAD 開源社群](09.2-如何參與OpenROAD開源社群.md)
    * [9.3-結語：開放如何重塑半導體的創新模式](09.3-結語：開放如何重塑半導體的創新模式.md)

* 附錄
    * [A.1-OpenROAD 常用 Tcl 命令速查表](A.1-OpenROAD常用Tcl命令速查表.md)
    * [B.1-DRC 與時序違規排查指南](B.1-DRC與時序違規排查指南.md)
    * [C.1-開源 EDA 術語對照表](C.1-開源EDA術語對照表.md)
