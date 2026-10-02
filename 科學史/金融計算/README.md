# 金融計算史 -- AI 偵探風格

以「推理探案」的方式，追查金融計算（Financial Computation / Quantitative Finance）從 1900 年 Bachelier 的投機理論，到 2023 年 LLM 進入量化金融的每一步：
前因是什麼？線索在哪裡？推理如何展開？後果又如何改變了整個金融世界？

金融計算的核心信念是：**金融市場是一台可以計算的機器**——用機率論、隨機過程、偏微分方程、蒙地卡羅模擬與最佳化演算法，把「價格、風險、報酬」變成可計算、可對沖、可交易的數學物件。

## 案件卷宗（歷史年表）

### 遠古序幕：計算與機率的前身（1202–1738）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1202 | Fibonacci《計算之書》：阿拉伯數字與複利/現值計算進入歐洲，一切金融計算的算術基礎 | [1202-Fibonacci計算之書.md](1202-Fibonacci計算之書.md) |
| 1494 | Pacioli 複式簿記：用「借貸守恆律」讓商業行為可稽核、可彙總——現代會計的誕生 | [1494-Pacioli複式簿記.md](1494-Pacioli複式簿記.md) |
| 1654 | Pascal–Fermat 賭金分配問題：機率論誕生，「條件期望 + 遞迴」的第一次精確使用 | [1654-PascalFermat賭金分配.md](1654-PascalFermat賭金分配.md) |
| 1671 | Jan de Witt 的年金定價：機率論第一次應用於金融商品——期望現值 = 生存機率 × 折現 | [1671-DeWitt年金定價.md](1671-DeWitt年金定價.md) |
| 1738 | Daniel Bernoulli 聖彼得堡悖論：期望效用與風險厭惡的誕生——現代金融理論的心理學基礎 | [1738-Bernoulli聖彼得堡悖論.md](1738-Bernoulli聖彼得堡悖論.md) |

### 序幕：隨機性進入金融（1900–1965）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1900 | Louis Bachelier《投機理論》：第一個用隨機漫步（布朗運動）為股價建模，比 Einstein 早五年 | [1900-Bachelier投機理論.md](1900-Bachelier投機理論.md) |
| 1933 | Alfred Cowles《股票市場預測家能預測嗎？》：用統計檢驗擊碎「預測大師」神話 | [1933-Cowles股票預測檢驗.md](1933-Cowles股票預測檢驗.md) |
| 1952 | Harry Markowitz《投資組合選擇》：用平均數—變異數最佳化把「分散風險」變成數學 | [1952-Markowitz投資組合理論.md](1952-Markowitz投資組合理論.md) |
| 1958 | Modigliani–Miller 定理：在完美市場中資本結構無關緊要，套利論證成為金融學的基石 | [1958-ModiglianiMiller定理.md](1958-ModiglianiMiller定理.md) |
| 1964 | William Sharpe 的 CAPM：從 Markowitz 一般均衡中提煉出「 beta 」單因子風險定價 | [1964-SharpeCAPM.md](1964-SharpeCAPM.md) |
| 1965 | Eugene Fama 的有效市場假說：股價是隨機漫步，「市場已經知道一切」 | [1965-Fama有效市場假說.md](1965-Fama有效市場假說.md) |
| 1965 | Paul Samuelson 的幾何布朗運動：修正 Bachelier——價格可以為負嗎？不能！ | [1965-Samuelson幾何布朗運動.md](1965-Samuelson幾何布朗運動.md) |

### 定價革命：衍生性商品與電腦（1973–1994）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1973 | Black–Scholes–Merton 選擇權定價公式：用 PDE 與動態避險解出「選擇權值多少錢」，開啟衍生性商品時代 | [1973-BlackScholes選擇權定價.md](1973-BlackScholes選擇權定價.md) |
| 1977 | Phelim Boyle 把蒙地卡羅方法引進選擇權定價：高維度衍生品的計算武器 | [1977-Boyle蒙地卡羅選擇權定價.md](1977-Boyle蒙地卡羅選擇權定價.md) |
| 1979 | Cox–Ross–Rubinstein 二項樹模型：用離散的二叉樹逼近 Black–Scholes，讓定價走進每台電腦 | [1979-CRR二項樹模型.md](1979-CRR二項樹模型.md) |
| 1982 | Robert Engle 的 ARCH 模型：波動率不是常數——用時間序列為「風險本身」建模 | [1982-EngleARCH模型.md](1982-EngleARCH模型.md) |
| 1986 | Tim Bollerslev 的 GARCH 模型：ARCH 的一般化，成為風險管理與計量經濟的工業標準 | [1986-BollerslevGARCH模型.md](1986-BollerslevGARCH模型.md) |
| 1987 | 黑色星期一：投資組合保險的動態避險程式反噬市場，道瓊單日暴跌 22.6% | [1987-黑色星期一與投資組合保險.md](1987-黑色星期一與投資組合保險.md) |
| 1992 | Heath–Jarrow–Morton 利率模型：把整條遠期利率曲線變成隨機過程 | [1992-HJM利率模型.md](1992-HJM利率模型.md) |
| 1993 | Steven Heston 的隨機波動率模型：波動率本身也是隨機過程，解開微笑曲線之謎 | [1993-Heston隨機波動率模型.md](1993-Heston隨機波動率模型.md) |
| 1994 | J.P. Morgan 的 RiskMetrics：Value at Risk (VaR) 成為全球風險管理的通用語言 | [1994-RiskMetricsVaR.md](1994-RiskMetricsVaR.md) |

### 危機與教訓：模型的極限（1998–2008）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1998 | LTCM 長期資本管理公司崩潰：兩位諾貝爾獎得主與 25 倍槓桿的教訓 | [1998-LTCM長期資本管理.md](1998-LTCM長期資本管理.md) |
| 2000 | David X. Li 的高斯 Copula：用相關結構為違約建模，後來成為 CDO 的「定時炸彈」 | [2000-Li高斯Copula.md](2000-Li高斯Copula.md) |
| 2000 | Almgren–Chriss 最佳執行演算法：如何用最佳化把大單拆小、最小化市場衝擊 | [2000-AlmgrenChriss最佳執行.md](2000-AlmgrenChriss最佳執行.md) |
| 2001 | Longstaff–Schwartz 最小平方法蒙地卡羅：終於能為美式選擇權等高維路徑相依商品定價 | [2001-LongstaffSchwartz蒙地卡羅.md](2001-LongstaffSchwartz蒙地卡羅.md) |
| 2008 | 金融海嘯：CDO 定價失敗、高斯 Copula 的崩潰與 VaR 的失靈 | [2008-金融海嘯與CDO.md](2008-金融海嘯與CDO.md) |

### 現代金融計算（2010–至今）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 2010 | 閃電崩盤與高頻交易：毫秒級的市場、做市演算法與監管的賽跑 | [2010-閃電崩盤與高頻交易.md](2010-閃電崩盤與高頻交易.md) |
| 2017 | Buehler 等人的深度避險（Deep Hedging）：用深度學習取代 Black–Scholes 動態避險 | [2017-深度避險.md](2017-深度避險.md) |
| 2023 | LLM 與量化金融：大型語言模型進入研究、情感分析、程式碼生成與投資決策 | [2023-LLM與量化金融.md](2023-LLM與量化金融.md) |

## 關鍵人物年表

### 遠古序幕（1202–1738）

| 年代 | 人物 | 貢獻 |
|------|------|------|
| 1202 | Leonardo of Pisa (Fibonacci) | 阿拉伯數字引進歐洲、複利/現值計算 |
| 1494 | Luca Pacioli | 複式簿記、會計學之父 |
| 1654 | Blaise Pascal / Pierre de Fermat | 機率論誕生、賭金分配問題 |
| 1671 | Jan de Witt | 年金定價、精算科學的先驅 |
| 1738 | Daniel Bernoulli | 聖彼得堡悖論、期望效用與風險厭惡 |

### 現代（1900–至今）

| 年代 | 人物 | 貢獻 |
|------|------|------|
| 1202 | Leonardo of Pisa (Fibonacci) | 阿拉伯數字引進歐洲、複利/現值計算 |
| 1494 | Luca Pacioli | 複式簿記、會計學之父 |
| 1654 | Blaise Pascal / Pierre de Fermat | 機率論誕生、賭金分配問題 |
| 1671 | Jan de Witt | 年金定價、精算科學的先驅 |
| 1738 | Daniel Bernoulli | 聖彼得堡悖論、期望效用與風險厭惡 |
| 1900 | Louis Bachelier | 投機理論、金融中的布朗運動與隨機漫步 |
| 1933 | Alfred Cowles | 股票預測的統計檢驗、Cowles 委員會創辦人 |
| 1952 | Harry Markowitz | 投資組合理論、平均數—變異數最佳化（1990 諾貝爾獎） |
| 1958 | Franco Modigliani / Merton Miller | MM 定理、套利論證（皆獲諾貝爾獎） |
| 1964 | William Sharpe | CAPM、beta（1990 諾貝爾獎） |
| 1965 | Eugene Fama | 有效市場假說（2013 諾貝爾獎） |
| 1965 | Paul Samuelson | 幾何布朗運動、認股權證理性定價（1970 諾貝爾獎） |
| 1973 | Fischer Black / Myron Scholes / Robert Merton | 選擇權定價公式（Scholes、Merton 獲 1997 諾貝爾獎） |
| 1977 | Phelim Boyle | 蒙地卡羅選擇權定價 |
| 1979 | John Cox / Stephen Ross / Mark Rubinstein | 二項樹模型、風險中立評價 |
| 1982 | Robert Engle | ARCH 模型（2003 諾貝爾獎） |
| 1986 | Tim Bollerslev | GARCH 模型 |
| 1992 | David Heath / Robert Jarrow / Andrew Morton | HJM 利率模型 |
| 1993 | Steven Heston | Heston 隨機波動率模型 |
| 1994 | Dennis Weatherstone / J.P. Morgan RiskMetrics 團隊 | Value at Risk |
| 1998 | Myron Scholes / Robert Merton（LTCM） | 長期資本管理公司崩潰的教訓 |
| 2000 | David X. Li | 高斯 Copula 違約相關模型 |
| 2000 | Robert Almgren / Neil Chriss | 最佳執行演算法 |
| 2001 | Francis Longstaff / Eduardo Schwartz | 最小平方法蒙地卡羅 |
| 2017 | Hans Buehler 等（J.P. Morgan） | 深度避險 |
| 2023 | OpenAI / 各大量化基金 | LLM 進入量化金融 |

## 貫穿全書的主線

1. **計算的基礎**：從 Fibonacci 的阿拉伯數字（1202）到 Pacioli 的複式簿記（1494）——「能寫下、能計算、能稽核」是一切金融科學的前提。
2. **隨機性**：從 Pascal–Fermat 的機率論（1654）與 Bernoulli 的風險厭惡（1738），到 Bachelier 的隨機漫步（1900）與 GARCH 的波動率聚類（1986）——金融價格的本質是不確定的，問題是如何為「不確定」本身定價。
2. **無套利**：從 MM 定理到 Black–Scholes 再到 HJM——「沒有免費午餐」是所有定價公式的引擎。
3. **無套利**：從 MM 定理到 Black–Scholes 再到 HJM——「沒有免費午餐」是所有定價公式的引擎。
4. **計算**：從二項樹、有限差分到蒙地卡羅再到深度學習——每一次理論突破，都伴隨一次計算方法的革命。
5. **危機**：從黑色星期一、LTCM 到金融海嘯——模型失靈的方式不只是「算錯」，而是「所有人都用同一個模型」。

## 延伸閱讀（本書內部交叉參照）

- [../隨機算法/1905-布朗運動.md](../隨機算法/1905-布朗運動.md) — 布朗運動的物理源頭
- [../隨機算法/1946-Ulam蒙地卡羅.md](../隨機算法/1946-Ulam蒙地卡羅.md) — 蒙地卡羅方法的誕生
- [../機率統計/](../機率統計/) — 機率與統計的基礎
- [../微分方程/](../微分方程/) — Black-Scholes PDE 的數學基礎
