# 半導體設備史 -- AI 偵探風格

以「推理探案」的方式，追查半導體製造設備從拉晶爐到 High-NA EUV 的每一步：
前因是什麼？線索在哪裡？推理如何展開？後果又如何改變了整個產業與地緣政治？

核心謎題只有一個：**如何把「在矽片上畫出、長出、刻出奈米圖形」這件事，從手工藝變成機器、從機器變成雷射、從雷射變成電漿、電子束，最後變成原子層操作？**

設備史的邏輯是一個循環：
$$\text{理論（物理/化學）} \xrightarrow{\text{工程化}} \text{機台} \xrightarrow{\text{量產}} \text{製程} \xrightarrow{\text{良率壓力}} \text{新理論的需求}$$
理論、實驗、技術相互促進——每一次「摩爾定律危機」，都是一台新設備的誕生證明。

## 案件卷宗（歷史年表）

### 前奏：晶體與純度（1916–1955）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1916 | Czochralski 意外發明直拉法——單晶爐的起源，今日 90% 矽晶圓由此而生 | [1916-Czochralski直拉法.md](1916-Czochralski直拉法.md) |
| 1950 | Pfann 區域熔煉（9N 純度）+ Teal/Little 長出第一根鍺單晶 | [1950-區域熔煉與單晶爐.md](1950-區域熔煉與單晶爐.md) |
| 1953 | Veeco 成立——真空鍍膜（蒸鍍）設備工業的起點 | [1953-Veeco真空鍍膜.md](1953-Veeco真空鍍膜.md) |
| 1955 | Bell Labs Andrus/Bond 發明接觸式微影——在晶片上「照相」 | [1955-接觸式微影.md](1955-接觸式微影.md) |
| 1959 | Hoerni 平面製程定義了「設備清單」：氧化爐、擴散爐、光刻、蝕刻、蒸鍍 | [1959-平面製程設備.md](1959-平面製程設備.md) |

### 設備工業誕生（1961–1967）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1961 | Kasper 出貨第一台商用對準機（mask aligner）——「廠商設備」模式誕生 | [1961-Kasper對準機.md](1961-Kasper對準機.md) |
| 1963 | Tokyo Electron 成立——日本設備業從代理商爬到巨頭 | [1963-TokyoElectron成立.md](1963-TokyoElectron成立.md) |
| 1967 | Applied Materials 成立——「一站式設備供應商」的巨人誕生 | [1967-AppliedMaterials成立.md](1967-AppliedMaterials成立.md) |

### 微影革命（1973–1980）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1973 | Perkin-Elmer Micralign 投影式微影——第一次良率革命 | [1973-PerkinElmer投影微影.md](1973-PerkinElmer投影微影.md) |
| 1973 | Varian/Extrion 離子佈植機商用化——摻雜從高溫擴散到離子加速器 | [1973-離子佈植機.md](1973-離子佈植機.md) |
| 1974 | 電漿蝕刻商用化（Reinberg 反應器 + Tegal）——乾式蝕刻取代濕式 | [1974-電漿蝕刻.md](1974-電漿蝕刻.md) |
| 1976 | KLA 自動檢測設備——良率變成數學 | [1976-KLA檢測設備.md](1976-KLA檢測設備.md) |
| 1978 | GCA DSW4800——第一台商用步進機，微影的分水嶺 | [1978-GCA步進機.md](1978-GCA步進機.md) |
| 1980 | Nikon NSR-1010G——光學帝國的降維打擊，日本吞下七成微影市場 | [1980-Nikon步進機.md](1980-Nikon步進機.md) |

### 單片化與平坦化（1982–1995）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1982 | Lam Research AutoEtch——單片式蝕刻，良率與均勻性的勝利 | [1982-LamResearch蝕刻.md](1982-LamResearch蝕刻.md) |
| 1984 | ASML 從飛利浦誕生——微影霸主的存亡之路 | [1984-ASML成立.md](1984-ASML成立.md) |
| 1988 | IBM 發明 CMP——讓晶圓「絕對平坦」的魔法 | [1988-IBM化學機械研磨.md](1988-IBM化學機械研磨.md) |
| 1991 | Applied Endura 群集設備——把生產線縮進一個真空腔 | [1991-Endura群集設備.md](1991-Endura群集設備.md) |
| 1993 | KrF 248nm 深紫外微影——從水銀燈到準分子雷射的波長戰爭 | [1993-深紫外微影.md](1993-深紫外微影.md) |
| 1994 | Novellus HDP-CVD——填滿 0.25μm 的洞 | [1994-HDPCVD.md](1994-HDPCVD.md) |
| 1995 | Applied Mirra——CMP 從 IBM 祕密變成全民技術 | [1995-CMP量產化.md](1995-CMP量產化.md) |

### EUV 攻防與產業整併（1997–2013）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1997 | EUV LLC 成立——Intel/AMD/Motorola 與美國國家實驗室的末日賭局 | [1997-EUV聯盟.md](1997-EUV聯盟.md) |
| 1999 | 產業整併：KLA-Tencor、AMAT-Varian、ASML-SVG——寡佔時代來臨 | [1999-產業整併.md](1999-產業整併.md) |
| 2002 | 林本堅提出浸潤式微影——「一盆水」拯救了整個摩爾定律 | [2002-浸潤式微影.md](2002-浸潤式微影.md) |
| 2007 | Intel 45nm high-k + ALD——一次長一層原子的沉積革命 | [2007-HighK與ALD.md](2007-HighK與ALD.md) |
| 2010 | ASML NXE:3100 EUV 原型機出貨——「永遠還差兩年」的十年抗戰 | [2010-EUV原型機.md](2010-EUV原型機.md) |
| 2013 | ASML 併購 Cymer——把光源心臟握進自己手裡 | [2013-ASML併購Cymer.md](2013-ASML併購Cymer.md) |

### EUV 時代與地緣政治（2019–2025）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 2019 | TSMC N7+ EUV 量產——七年抗戰結束 | [2019-EUV量產.md](2019-EUV量產.md) |
| 2020 | 多束電子束檢測——EUV 時代的良率顯微鏡與 AI | [2020-電子束檢測.md](2020-電子束檢測.md) |
| 2023 | High-NA EUV 出貨 + 美日荷出口管制——0.55 NA 的物理與地緣刀鋒 | [2023-HighNAEUV與出口管制.md](2023-HighNAEUV與出口管制.md) |
| 2024 | 先進封裝設備（混合鍵合、CoWoS）——AI 算力時代的第二戰場 | [2024-先進封裝設備.md](2024-先進封裝設備.md) |

## 設備分類速查表

| 製程 | 設備 | 關鍵理論 | 代表廠商 |
|------|------|----------|----------|
| 晶體生長 | CZ 單晶爐 / FZ 區熔爐 | 相圖、分凝係數、Scheil 方程 | PVA TePla、Ferrotec |
| 薄膜沉積 | CVD / PECVD / HDP-CVD / PVD / ALD | Grove 模型、Arrhenius、自限反應 | AMAT、Lam、TEL、ASM |
| 微影 | 對準機 / 步進機 / 掃描機 / EUV | Rayleigh 公式 CD=k₁λ/NA、繞射 | ASML、Nikon、Canon、SMEE |
| 蝕刻 | 電漿蝕刻 / RIE / ICP / Bosch / ALE | 電漿物理、離子增強蝕刻、選擇比 | Lam、TEL、AMAT、AMEC |
| 摻雜 | 離子佈植機 / RTA | LSS 理論、高斯剖面、通道效應 | AMAT、Axcelis |
| 平坦化 | CMP 研磨機 | Preston 方程 R=KpPV | AMAT、Ebara |
| 檢測量測 | 光學檢測 / e-beam / CD-SEM | 良率模型、二次電子、電壓對比 | KLA、HMI、Onto |
| 測試封裝 | ATE / 焊線機 / 混合鍵合 / TSV | 電性測試、表面能、DRIE | Advantest、Teradyne、Besi、ASMPT |

## 關鍵人物年表

| 年代 | 人物 | 貢獻 |
|------|------|------|
| 1916 | Jan Czochralski | 直拉法（CZ）單晶生長 |
| 1950 | William Pfann | 區域熔煉（Zone refining） |
| 1950 | Gordon Teal / Morgan Little | 第一根鍺單晶（CZ） |
| 1952 | Henry Theuerer | 懸浮區熔法（FZ） |
| 1955 | Jules Andrus / Walter Bond | 接觸式微影（Bell Labs） |
| 1959 | Jean Hoerni | 平面製程（定義設備清單） |
| 1961 | William Kasper | 第一台商用對準機 |
| 1963 | Tokuo Kubo（久保德雄） | Tokyo Electron 創辦 |
| 1967 | Michael McNeilly | Applied Materials 創辦 |
| 1967 | Abe Offner | 反射式投影光學（Micralign） |
| 1971 | Peter Rose | Extrion／Nova（離子佈植） |
| 1973 | Alan Reinberg | 徑向流電漿反應器（PECVD/蝕刻） |
| 1976 | Ken Levy | KLA 自動檢測 |
| 1978 | David Mann / GCA 團隊 | DSW4800 第一台步進機 |
| 1979 | John Coburn / Harold Winters | 離子增強化學蝕刻（IBM） |
| 1980 | Roger Bonham / David Brandly | Lam Research 創辦 |
| 1984 | Arthur del Prado / Philips | ASML 誕生 |
| 1988 | IBM 製程團隊（Kaufman 等） | CMP 化學機械研磨 |
| 1991 | Applied Materials | Endura 群集設備 |
| 1994 | Richard Hill | Novellus HDP-CVD |
| 1997 | Chuck Gwyn / Don Sweeney | EUV LLC 與國家實驗室聯盟 |
| 1986 | Hiroo Kinoshita（木下博雄） | 最早 EUV 成像實驗（NTT） |
| 2002 | 林本堅（Burn Lin） | 浸潤式微影 |
| 2007 | Intel + ASM International | high-k 金屬閘 + ALD 量產 |
| 2010 | ASML / Zeiss / Cymer | NXE:3100 EUV 原型機 |
| 2019 | TSMC / Samsung | EUV 量產（N7+、7LPP） |
| 2023 | Intel / ASML / Zeiss | High-NA EUV 出貨 |

## 設備公司大事記（族譜）

| 年份 | 公司 | 大事 |
|------|------|------|
| 1953 | Veeco | 成立（真空鍍膜） |
| 1963 | Tokyo Electron | 成立（代理商 → 製造） |
| 1967 | Applied Materials | 成立（擴散爐起家） |
| 1972 | Veeco 併 Cobilt (1974) | 對準機血脈 |
| 1975 | KLA Instruments | 成立（光罩檢測） |
| 1980 | Lam Research | 成立（單片蝕刻） |
| 1984 | ASML | Philips+ASM 合資成立 |
| 1986 | Cymer | 成立（DUV 準分子雷射） |
| 1997 | KLA + Tencor | 合併（良率管理帝國） |
| 1999 | AMAT 併 Varian 佈植部門 | 摻雜版圖 |
| 2001 | ASML 併 SVG | 繼承 Perkin-Elmer 微影血脈 |
| 2013 | ASML 併 Cymer；Lam 併 Novellus | 光源整合、蝕刻+CVD |
| 2016 | ASML 併 Hermes、入股 Zeiss SMT 24.9% | 量測+光學整合 |
| 2019 | KLA 併 Orbotech | 顯示器+先進封裝檢測 |
| 2020s | 中國設備崛起 | Naura、AMEC、SMEE 在制裁中成長 |
