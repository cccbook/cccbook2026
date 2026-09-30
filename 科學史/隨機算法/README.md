# 隨機算法史 -- AI 偵探風格

以「推理探案」的方式，追查隨機算法從 Buffon 擲針到現代機器學取樣的每一步：
前因是什麼？線索在哪裡？推理如何展開？後果又如何改變了整個電腦科學？

隨機算法的核心信念是：**丟銅板也能算數學**——讓演算法「擲骰子」，往往能用遠比確定性算法更簡單、更快的程序，得到幾乎總是正確的答案。

## 案件卷宗（歷史年表）

### 序幕：機率與隨機的物理源頭（1777–1946）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1777 | Buffon 擲針實驗：第一個用隨機實驗「計算」數學常數 π | [1777-Buffon針實驗.md](1777-Buffon針實驗.md) |
| 1905 | Einstein 解釋布朗運動：隨機漫步的物理理論 | [1905-布朗運動.md](1905-布朗運動.md) |
| 1946 | Ulam 在 Los Alamos 發明蒙地卡羅方法 | [1946-Ulam蒙地卡羅.md](1946-Ulam蒙地卡羅.md) |
| 1953 | Metropolis–Hastings 演算法：MCMC 的誕生 | [1953-MetropolisHastings演算法.md](1953-MetropolisHastings演算法.md) |

### 隨機化的誕生：電腦科學遇見機率（1961–1985）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1961 | Hoare 快速排序：後來成為隨機化分析的經典案例 | [1961-Hoare快速排序.md](1961-Hoare快速排序.md) |
| 1976 | Miller 提出 Rabin–Miller 質數檢驗的基礎（確定性多項式時間檢驗假設 ERH） | [1976-Miller質數檢驗.md](1976-Miller質數檢驗.md) |
| 1980 | Rabin 提出機率式質數檢驗：BPP/RP 類的第一個殺手級應用 | [1980-Rabin質數檢驗.md](1980-Rabin質數檢驗.md) |
| 1981 | Rabin 指紋比對：用雜湊與模運算「比對」資料 | [1981-Rabin指紋比對.md](1981-Rabin指紋比對.md) |
| 1984 | Johnson–Lindenstrauss 引理：隨機投影降維 | [1984-JohnsonLindenstrauss引理.md](1984-JohnsonLindenstrauss引理.md) |
| 1985 | Blum–Micali 偽隨機產生器：從單向函數製造「假隨機」 | [1985-BlumMicali偽隨機產生器.md](1985-BlumMicali偽隨機產生器.md) |
| 1985 | Yao 的計算隨機性理論：BPP、弱隨機源與 Yao 原理 | [1985-Yao計算隨機性.md](1985-Yao計算隨機性.md) |

### 隨機算法的黃金年代（1987–2000）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1987 | Karp–Rabin 字串匹配：隨機化雜湊找子字串 | [1987-KarpRabin字串匹配.md](1987-KarpRabin字串匹配.md) |
| 1989 | Karger 的全域最小割收縮算法：簡單隨機化擊敗複雜確定性算法 | [1989-Karger最小割.md](1989-Karger最小割.md) |
| 1990 | PCP 定理（隨機化驗證的極致，交叉參照計算理論史） | [1990-PCP定理.md](../計算理論/1990-PCP定理.md) |
| 1995 | Karger–Klein–Tarjan 隨機線性時間最小生成樹 | [1995-KargerKleinTarjan隨機MST.md](1995-KargerKleinTarjan隨機MST.md) |
| 1997 | Broder 的 MinHash：用隨機雜湊估計集合相似度 | [1997-BroderMinHash.md](1997-BroderMinHash.md) |
| 1997 | Impagliazzo–Wigderson：P = BPP 若單向函數夠硬（去隨機化） | [1997-ImpagliazzoWigderson去隨機化.md](1997-ImpagliazzoWigderson去隨機化.md) |

### 現代隨機算法（2004–至今）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 2004 | Spielman–Teng 平滑分析：解開單純形法「實務很快」之謎 | [2004-SpielmanTeng平滑分析.md](2004-SpielmanTeng平滑分析.md) |
| 2005 | Cormode–Muthukrishnan Count-Min Sketch：串流資料的隨機統計 | [2005-CountMinSketch.md](2005-CountMinSketch.md) |
| 2007 | Flajolet 等人 HyperLogLog：用幾 KB 估計十億級基數 | [2007-HyperLogLog.md](2007-HyperLogLog.md) |
| 2020 | 隨機算法與現代機器學習：SGD、Dropout 與 LLM 取樣 | [2020-隨機算法與機器學習.md](2020-隨機算法與機器學習.md) |

## 關鍵人物年表

| 年代 | 人物 | 貢獻 |
|------|------|------|
| 1777 | Georges-Louis Leclerc (Comte de Buffon) | 擲針實驗、幾何機率 |
| 1905 | Albert Einstein | 布朗運動理論、隨機漫步 |
| 1946 | Stanisław Ulam | 蒙地卡羅方法 |
| 1946–1953 | Nicholas Metropolis | Metropolis 演算法、MCMC |
| 1953 | Wilfred Keith Hastings | Metropolis–Hastings 一般化 |
| 1961 | C. A. R. Hoare | 快速排序 |
| 1976 | Gary Miller | 質數檢驗（ERH 下確定性） |
| 1980 | Michael Rabin | 機率式質數檢驗、BPP 應用 |
| 1981 | Michael Rabin | 指紋比對 |
| 1984 | William Johnson / Joram Lindenstrauss | 隨機投影引理 |
| 1985 | Manuel Blum / Silvio Micali | 偽隨機產生器 |
| 1985 | Andrew Yao | 計算隨機性、Yao 原理 |
| 1987 | Richard Karp / Michael Rabin | Karp–Rabin 字串匹配 |
| 1989 | David Karger | 最小割收縮算法 |
| 1995 | Karger / Klein / Tarjan | 隨機線性 MST |
| 1997 | Andrei Broder | MinHash |
| 1997 | Impagliazzo / Wigderson | 去隨機化定理 |
| 2004 | Daniel Spielman / Shang-Hua Teng | 平滑分析 |
| 2005 | Graham Cormode / S. Muthukrishnan | Count-Min Sketch |
| 2007 | Philippe Flajolet 等 | HyperLogLog |

## 核心概念速查

### 隨機算法的分類

| 類型 | 定義 | 失敗模式 |
|------|------|----------|
| Las Vegas | 總是正確，執行時間隨機 | 可能跑很久（期望時間多項式） |
| Monte Carlo | 時間固定，答案可能錯 | 有機率出錯（可重複降低） |

### 複雜度類

| 類別 | 意義 |
|------|------|
| RP | 一邊可能出錯的 Monte Carlo（yes 實例至少 1/2 機率接受） |
| BPP | 兩邊都可能出錯，但誤差 ≤ 1/3 |
| ZPP | Las Vegas：期望多項式時間，總是正確 |

### 交錯參照
- 計算理論史（BPP 與 P vs NP）：[../計算理論/README.md](../計算理論/README.md)
- 機率統計史（機率論基礎）：[../機率統計/README.md](../機率統計/README.md)
