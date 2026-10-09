# 2011 - Watson 問答系統

## 案件摘要
2011 年 2 月，IBM 的 Watson 在美國智力競賽《Jeopardy!》中擊敗了兩位人類冠軍——Ken Jennings（74 連勝紀錄保持者）與 Brad Rutter。Jeopardy! 的特點是「反問句」：主持人給答案，參賽者要用**問句**提問，題目橫跨歷史、文學、科學、流行文化，充滿雙關語、諧音與陷阱。Watson 的本質是一條**符號＋統計混合智慧**的問答管線：問題分析 → 假說生成 → 證據檢索與評分 → 置信度融合。其核心是對每個候選答案計算一個校準的分數：

$$
P(\text{answer} \mid \text{question}) \approx \sum_i w_i \cdot \text{score}_i(\text{answer}, \text{evidence})
$$

這是搜尋智能（1997-DeepBlue擊敗棋王.md）之後，機器第一次在「語言理解」而非「暴力搜尋」的賽場上戰勝人類頂尖選手。

## 前因 -- 為什麼會有這個案子
- **1997 年的深藍**擊敗 Kasparov，但那是在 64 格棋盤上用 $\sim 2 \times 10^8$ 步/秒的搜尋取勝，規則封閉、狀態有限。IBM 想追問：開放領域的**自然語言**也能贏嗎？（1997-DeepBlue擊敗棋王.md）
- **2004 年**，IBM 研究員 Charles Lickel 在餐廳看到客人們因 Ken Jennings 的連勝而集體抬頭看電視，萌生了「讓機器參加 Jeopardy!」的念頭，專案代號 Blue J。
- **搜尋引擎的困境**：Google 式關鍵字檢索能找回文件，但不能「回答問題」——它不做句法分析、不評分證據、不承擔風險。Jeopardy! 要求 3 秒內給出單一答案，答錯要扣錢。
- **前驅線索**：1966-ELIZA對話系統.md 證明了淺層模式匹配可騙過人，但 Watson 需要的是真實的證據推理，而非騙局。
- **動機**：IBM 想證明其 DeepQA 技術可商業化（後來的 Watson Health），並在 AI 冬天後重塑公眾對 AI 的信心。
- **賽制的狡猾**：Jeopardy! 題目刻意涵蓋雙關語（「Charm」可以是魔法也可以是夸克）、諺語、首字母縮寫與分類陷阱——IBM 統計後發現題目類別橫跨 2000 種以上，這正是「開放領域」的極限測試。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：問題分析——拆解反問句
Jeopardy! 題目如「This 'Father of Our Country' didn't really chop down a cherry tree」。Watson 先用解析器（深層句法 + ESG 英語資源語法）抽出：
- **答案類型（LAT, Lexical Answer Type）**：本題是 "Father"——答案應是一個人名。
- **焦點（focus）**：句子中待替換的位置。
- **關係語義**：「美國國父」「櫻桃樹傳說」兩個約束。

$$
\text{question} \rightarrow (\text{LAT},\ \text{focus},\ \text{relations})
$$

這條線索的血統可追溯到 1970 年代的符號 NLP：1970-WoodsATN.md 的增強轉移網路、1975-Minsky框架理論.md 的框架表示——Watson 把它們全部變成統計可評分的特徵，而不是硬編碼的規則。

**一個拆解實例**（Jeopardy! 真題）：

| 題目成分 | 抽出結果 |
|---|---|
| "This category is a 'dog's life'" | LAT = "category"（雙關：分類項目 vs 狗） |
| "Who was 'L' in the 1950s' TV cops?" | LAT = "Who" + 縮寫解謎（L = Law?） |
| "This 'Father of Our Country'" | LAT = "Father" + 焦點 + 慣用語 |

### 第二條線索：假說生成——廣撒網
用上百種檢索策略（命名實體改寫、文件標題檢索、以 LAT 過濾）同時查詢本地 4 TB 語料（含維基百科、WordNet、字典、百科全書），在 3 秒內生成數百個**候選答案**（假說）。這繼承了 Deep Blue 的「窮舉」哲學，但窮舉對象從棋步換成了候選實體。

### 第三條線索：證據評分——上百個異質特徵
對每個候選答案 $a$，重新檢索其相關證據，再用機器學習學出的權重 $w_i$ 融合上百個評分器：

| 特徵類型 | 例子 | 說明 |
|---|---|---|
| 詞彙匹配 | PAS（ passages 詞重疊） | 證據與題目的詞袋相似度 |
| 類型相容 | LAT 匹配 | 候選是否屬於答案類型 |
| 來源可靠度 | 維基/字典權重 | 證據出處的可信度 |
| 時間/地理關係 | 日期相容 | 題目與證據的時空約束 |
| 語義關係 | RelHav/RelPP | 謂詞論元結構的匹配度 |

$$
\text{Conf}(a) = \sigma\!\left(\sum_{i=1}^{N} w_i f_i(a) + b\right), \quad N \approx 100
$$

權重 $w_i$ 是在數千道歷屆 Jeopardy! 題上用機器學習學出的——評分器本身是符號 NLP 的產物，但「怎麼加權」是統計學的問題。這種「符號特徵 + 統計融合」的分工，正是 1980 年代專家系統（1965-DENDRAL專家系統.md）與 1990 年代統計 NLP 兩條路線的合流。

### 第四條線索：賭注與風險——校準的自信
Jeopardy! 允許搶答與 Daily Double 加倍下注。Watson 的 TD（Top-Answer）分數被校準成真實答對率，並有明確的**搶答門檻**（約 0.75 置信度）：低於門檻不按鈴，避免扣分。這是機器第一次在公開賽場上展示「知道自己不知道」。

### 第五條線索：硬體與賽場的分工
Watson 是 90 台 IBM Power 750 伺服器（2880 核心、16 TB RAM）組成的叢集，語料全部放在本地——因為 3 秒答題的時限容不下網路往返。整條 DeepQA 管線在比賽中的分工：

| 管線階段 | 時間占比 | 產出 |
|---|---|---|
| 問題分析 | ~10% | LAT、焦點、約束 |
| 假說生成 | ~30% | 數百個候選答案 |
| 證據檢索 | ~40% | 每個候選的支援段落 |
| 評分與融合 | ~20% | 校準的置信度排序 |

答錯的典型案例也揭露了管線的天性：2011 年 Final Jeopardy 題「Its largest airport is named for a World War II hero; its second largest for a WWII battle」，Watson 答了「Toronto」（美國城市類別下）——因為它只靠統計關聯（多倫多機場確實以戰爭英雄命名），缺乏「必須是美國城市」的硬約束檢查。這條線索預告了後續所有「混合智能」的困境。

## 結案 -- 後果與影響
- **混合智慧的證明**：Watson 證明了符號 NLP（解析、類型學）＋統計機器學習（權重學習）＋大規模檢索的組合可在開放領域擊敗人類，但它仍是**專家系統式的管線**，不是端到端學習。
- **三場比賽**：2011/2/14–16，Watson 以 $77{,}147 對 Rutter 的 $21,600 與 Jennings 的 $24,000 獲勝。Jennings 事後感嘆：「Watson 不會失眠，不會緊張，我們才像機器。」
- **商業化與挫折**：Watson Health 進軍醫療問答，但因語料偏窄、天真的統計關聯（如「癌症治療」與「便宜的化療藥」的錯誤連結）而聲譽受挫——暴露了管線式 AI 缺乏真正的推理。
- **後續案件**：Watson 的「問答」路線後來被 2013-word2vec詞向量.md 之後的詞向量語義匹配與 2017 年 Transformer 式閱讀理解（BERT/SQuAD）取代——符號管線逐步讓位給端到端神經模型，見「科學與歷史/人工智慧/」的問答智能相關檔案。
- **文化衝擊**：2011 年成為「機器理解語言」的公眾里程碑，與同年的 2011-Siri語音助理.md 一起，宣告 AI 從實驗室走進大眾視野。
- **伏筆**：Watson 的候選答案 + 證據評分思路，是「檢索增強生成（RAG, 2020s）」的先聲——先檢索證據、再推理作答的架構在大語言模型時代以新形式復活，見「科學與歷史/計算語言學/2020s-多模態與RAG時代.md」。

## 關鍵人物與文獻
- **David Ferrucci**：IBM DeepQA 首席研究員，Watson 專案主持人。
- **Charles Lickel**：發想 Jeopardy! 專案的 IBM 高管。
- **Ken Jennings / Brad Rutter**：Jeopardy! 人類冠軍，被擊敗的對照組。
- Ferrucci et al., *Building Watson: An Overview of the DeepQA Project*, AI Magazine, 2010.
- Lally et al., *Question Analysis: How Watson Reads a Clue*, IBM J. Res. Dev., 2012.
- Chu-Carroll et al., *Finding Needles in the Haystack: Search and Candidate Generation*, IBM J. Res. Dev., 2012.
- 相關案件：1997-DeepBlue擊敗棋王.md、1966-ELIZA對話系統.md、2011-Siri語音助理.md、2013-word2vec詞向量.md
