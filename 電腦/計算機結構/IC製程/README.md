# 從矽砂到晶片：IC 製程與 EDA 的共舞

一本把「晶圓廠裡的物理世界」與「工程師螢幕前的軟體世界」接在一起的書。製程每往前一步——從微影解析度、電晶體結構到金屬連線——EDA 就被迫長出一套新的演算法；反過來，EDA 的抽象與驗證能力，又決定了製程能不能被設計師真正使用。本書沿著這條雙向的驅動關係，從 MOSFET 的物理講到 PDK 的檔案格式，從 OPC 的光學計算講到 Chiplet 時代的跨晶片協同設計，並穿插四十年來設備、經濟、地緣政治與教育制度如何塑造這場共舞的真實故事。

## 目錄

* 第1章-兩個世界的接口：製程與 EDA
    * [1.1-從矽砂到晶圓：FEOL 與 BEOL 的物理舞台](01.1-從矽砂到晶圓：FEOL與BEOL的物理舞台.md)
    * [1.2-摩爾定律的隱形成本：為什麼沒有 EDA 就做不出晶片](01.2-摩爾定律的隱形成本：為什麼沒有EDA就做不出晶片.md)
    * [1.3-Fabless 與 Foundry 分工：晶圓廠模式的制度革命](01.3-Fabless與Foundry分工：晶圓廠模式的制度革命.md)
    * [1.4-PDK：把一座晶圓廠裝進一個資料夾](01.4-PDK：把一座晶圓廠裝進一個資料夾.md)

* 第2章-前段製程與電路的世界觀
    * [2.1-電晶體的三代身材：Planar、FinFET 與 GAA](02.1-電晶體的三代身材：Planar、FinFET與GAA.md)
    * [2.2-微影、植入與退火：閘極是怎麼被「畫」出來的](02.2-微影、植入與退火：閘極是怎麼被畫出來的.md)
    * [2.3-BSIM 模型：把幾百道製程濃縮成幾百個參數](02.3-BSIM模型：把幾百道製程濃縮成幾百個參數.md)
    * [2.4-SPICE 與 Corner：在 TT、SS、FF 之間賭未來](02.4-SPICE與Corner：在TT、SS、FF之間賭未來.md)

* 第3章-後段製程與連線的世界觀
    * [3.1-鋁到銅：Dual Damascene 與低介電材質的冒險](03.1-鋁到銅：DualDamascene與低介電材質的冒險.md)
    * [3.2-寄生 RC 與天線效應：導線比電晶體更難搞](03.2-寄生RC與天線效應：導線比電晶體更難搞.md)
    * [3.3-RC 萃取與 SPEF：EDA 如何替製程「算帳」](03.3-RC萃取與SPEF：EDA如何替製程算帳.md)
    * [3.4-IR-Drop 與電遷移：電源網路的簽核戰場](03.4-IR-Drop與電遷移：電源網路的簽核戰場.md)

* 第4章-設計規則：製程寫給 EDA 的法律條文
    * [4.1-最小線寬、Enclosure 與 WPE：DRC 規則的物理出處](04.1-最小線寬、Enclosure與WPE：DRC規則的物理出處.md)
    * [4.2-LVS：版圖與電路的幾何拓撲對質](04.2-LVS：版圖與電路的幾何拓撲對質.md)
    * [4.3-從 Calibre 到開源驗證：物理簽核工具的權力結構](04.3-從Calibre到開源驗證：物理簽核工具的權力結構.md)
    * [4.4-Rule-Driven 的 P&R：繞線器如何在規則縫隙中生存](04.4-Rule-Driven的P&R：繞線器如何在規則縫隙中生存.md)

* 第5章-微影與計算微影：光學與數學的合謀
    * [5.1-從 g-line 到 EUV：一台微影機的六十年進化](05.1-從g-line到EUV：一台微影機的六十年進化.md)
    * [5.2-繞射極限與光學鄰近效應：艾利盤的統治](05.2-繞射極限與光學鄰近效應：艾利盤的統治.md)
    * [5.3-OPC 與 RET：把版圖改到光看得懂為止](05.3-OPC與RET：把版圖改到光看得懂為止.md)
    * [5.4-ILT 與 Mask Data Preparation：當遮罩檔案比作業系統還大](05.4-ILT與MaskDataPreparation：當遮罩檔案比作業系統還大.md)

* 第6章-可製造性設計：良率是設計出來的
    * [6.1-CMP 的 Erosion 與 Dishing：平坦化不平坦](06.1-CMP的Erosion與Dishing：平坦化不平坦.md)
    * [6.2-Dummy Metal 與 Density Rule：為了均勻而撒的假線](06.2-DummyMetal與DensityRule：為了均勻而撒的假線.md)
    * [6.3-多重曝光：LELE、SADP 與 SAQP 的顏色分配問題](06.3-多重曝光：LELE、SADP與SAQP的顏色分配問題.md)
    * [6.4-Critical Area Analysis：用機率幫良率定價](06.4-CriticalAreaAnalysis：用機率幫良率定價.md)

* 第7章-先進封裝：摩爾定律的平行宇宙
    * [7.1-超越摩爾：2.5D、CoWoS 與 InFO 的誕生](07.1-超越摩爾：2.5D、CoWoS與InFO的誕生.md)
    * [7.2-TSV、Micro-bump 與 Hybrid Bonding：垂直連接的工藝](07.2-TSV、Micro-bump與HybridBonding：垂直連接的工藝.md)
    * [7.3-Chiplet 時代的 EDA：跨晶片的 APR、熱與應力分析](07.3-Chiplet時代的EDA：跨晶片的APR、熱與應力分析.md)
    * [7.4-UCIe 與開放生態：封裝介面的標準化之爭](07.4-UCIe與開放生態：封裝介面的標準化之爭.md)

* 第8章-下一步：製程與 EDA 的共同未來
    * [8.1-BSPDN 與 PowerVia：電源改走背面之後](08.1-BSPDN與PowerVia：電源改走背面之後.md)
    * [8.2-AI for EDA：從 DRC 修復到布局生成](08.2-AIforEDA：從DRC修復到布局生成.md)
    * [8.3-DTCO 與 STCO：設計、製程、系統的三方談判桌](08.3-DTCO與STCO：設計、製程、系統的三方談判桌.md)
    * [8.4-結語：矽的物理極限與軟體的想像極限](08.4-結語：矽的物理極限與軟體的想像極限.md)

* 附錄
    * [A.1-製程與 EDA 名詞對照表](A.1-製程與EDA名詞對照表.md)
    * [B.1-PDK 檔案格式速查：Techfile、LEF、DEF、Liberty 與 SPEF](B.1-PDK檔案格式速查.md)
    * [C.1-半導體製程大事年表](C.1-半導體製程大事年表.md)
