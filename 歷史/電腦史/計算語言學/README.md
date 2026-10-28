# 計算語言學歷史年表

> 副標題：從規則法到統計法，再到大型語言模型——一場持續七十年的「讓機器讀懂人話」運動。
>
> 每一個條目對應本目錄中的一篇「推理探案」風格 wiki：`年份-標題.md`

## 第一幕：規則法的誕生（1950–1975）

| 年份 | 事件 | wiki |
|---|---|---|
| 1950 | Turing 在《Computing Machinery and Intelligence》提出模仿遊戲（圖靈測試），並首次討論「機器翻譯」與字典攻擊的困境 | [1950-圖靈測試與機器翻譯之問](1950-圖靈測試與機器翻譯之問.md) |
| 1954 | Georgetown-IBM 實驗：60 句俄譯英的公開展示，機器翻譯（MT）的第一聲號角——也是第一次「過度承諾」 | [1954-GeorgetownIBM實驗](1954-GeorgetownIBM實驗.md) |
| 1956 | Chomsky 發表《Three Models for the Description of Language》：定義語言的層級（regular ⊂ context-free ⊂ context-sensitive ⊂ unrestricted），為計算語言學提供數學骨架 | [1956-Chomsky語言層級](1956-Chomsky語言層級.md) |
| 1957 | Chomsky 出版《Syntactic Structures》：轉換生成語法誕生，「英語句子不能用有限狀態機描述」的論證改寫了 NLP 的方向 | [1957-SyntacticStructures](1957-SyntacticStructures.md) |
| 1965 | Chomsky 出版《Aspects of the Theory of Syntax》：深層結構/表層結構、普遍語法、能力/表現之分——規則法的理論高峰 | [1965-Aspects與轉換生成語法](1965-Aspects與轉換生成語法.md) |
| 1970 | Jay Earley 發表 Earley 剖析器：O(n³) 的上下文無關文法解析演算法，Chart parsing 的經典 | [1970-Earley剖析器](1970-Earley剖析器.md) |
| 1970 | Terry Winograd 在 MIT 完成 SHRDLU：積木世界中的自然語言對話系統，規則法（LISP + 語法 + 語義 + 推理整合）的巔峰之作 | [1970-SHRDLU](1970-SHRDLU.md) |
| 1970 | William Woods 發明 ATN（Augmented Transition Networks）：在有限狀態機上掛暫存器與遞迴，突破 Chomsky 對有限狀態模型的否定 | [1970-WoodsATN](1970-WoodsATN.md) |
| 1972 | Roger Schank 提出「概念依存理論」（Conceptual Dependency）：語義表達的跨語言表示法，腳本（script）的先聲 | [1972-Schank概念依存](1972-Schank概念依存.md) |
| 1975 | Gerald Salton 發表「向量空間模型」與 TF-IDF 加權：文件 = 向量、相似度 = 餘弦，資訊檢索（IR）的數學基礎——也是日後詞向量的先聲 | [1975-向量空間模型與TFIDF](1975-向量空間模型與TFIDF.md) |
| 1990 | Elman 發表《Finding Structure in Time》：循環神經網路（RNN）讓時間進入神經網路，隱層聚類自動浮現語法類別——詞向量的先聲 | [1990-Elman循環神經網路](1990-Elman循環神經網路.md) |
| 1997 | Hochreiter 與 Schmidhuber 發表 LSTM：細胞狀態＋三個門破解梯度消失，統治序列建模 20 年 | [1997-LSTM長短期記憶](1997-LSTM長短期記憶.md) |

## 第二幕：規則法黃金期的尾聲與統計革命的號角（1975–1990）

| 年份 | 事件 | wiki |
|---|---|---|
| 1975 | Minsky 發表《A Framework for Representing Knowledge》（框架理論）：用 frame/slot/filler 表達常識，知識表示法的另一支柱 | [1975-Minsky框架理論](1975-Minsky框架理論.md) |
| 1985 | George Miller 普林斯頓團隊開始建構 WordNet：以同義詞集合（synset）與語義關係組織 15 萬詞彙——第一個大規模機器可讀詞庫 | [1985-WordNet](1985-WordNet.md) |
| 1988 | Kenneth Church 使用 HMM 做詞性標記（part-of-speech tagging）：統計方法第一次在真實 NLP 任務上擊敗規則法 | [1988-HMM詞性標記](1988-HMM詞性標記.md) |
| 1988 | IBM 的 Brown 團隊發表《A Statistical Approach to Machine Translation》：IBM Model 1-2，統計機器翻譯（SMT）誕生——Candide 計劃的前奏 | [1988-Brown統計機器翻譯](1988-Brown統計機器翻譯.md) |

## 第三幕：統計革命全面勝利（1990–2003）

| 年份 | 事件 | wiki |
|---|---|---|
| 1993 | Brown 等人發表《The Mathematics of Statistical Machine Translation》（Computational Linguistics 19(2)）：IBM Model 1-5 完整數學（EM 演算法、對齊模型），統計法正式取代規則法 | [1993-IBMModel15與EM演算法](1993-IBMModel15與EM演算法.md) |
| 2001 | Lafferty 等人（CMU）發表 CRF（條件隨機場）：判別式序列標記，解決 HMM 的標記偏誤（label bias） | [2001-CRF條件隨機場](2001-CRF條件隨機場.md) |
| 2002 | Papineni 等人（IBM）發表 BLEU 評估指標：n-gram 精確率的機器翻譯自動評分，NLP 評估的標準化 | [2002-BLEU評估](2002-BLEU評估.md) |

## 第四幕：表示學習與神經轉折（2003–2016）

| 年份 | 事件 | wiki |
|---|---|---|
| 2003 | Yoshua Bengio 發表《A Neural Probabilistic Language Model》：用神經網路學詞向量與 n-gram 分佈，「詞 = 向量」的轉折點 | [2003-Bengio神經語言模型](2003-Bengio神經語言模型.md) |
| 2013 | Mikolov 等人（Google）發表 Word2Vec：skip-gram 與 CBOW，word2vec 的向量算術（king - man + woman ≈ queen）讓「詞語義 = 向量空間幾何」爆紅 | [2013-Word2Vec](2013-Word2Vec.md) |
| 2014 | Cho 等人發表 GRU（門控循環單元）與 RNN Encoder-Decoder：兩個門的輕量序列建模，NMT 的孿生起點 | [2014-GRU門控循環單元](2014-GRU門控循環單元.md) |
| 2014 | Sutskever 等人發表 Seq2Seq、Bahdanau 等人發表注意力機制（attention）：編碼器-解碼器架構讓神經機器翻譯（NMT）一舉超車 SMT | [2014-Seq2Seq與注意力機制](2014-Seq2Seq與注意力機制.md) |
| 2016 | Google 宣布 GNMT（神經機器翻譯）全面上線，翻譯錯誤率下降 60%——統計機器翻譯時代落幕 | [2016-GNMT神經機器翻譯上線](2016-GNMT神經機器翻譯上線.md) |

## 第五幕：Transformer 與大型語言模型（2017–2020s）

| 年份 | 事件 | wiki |
|---|---|---|
| 2017 | Vaswani 等人（Google）發表《Attention Is All You Need》：Transformer 架構（self-attention、multi-head、位置編碼），拋棄 RNN/CNN | [2017-Transformer](2017-Transformer.md) |
| 2018 | ELMo（Peters 等人）與 BERT（Devlin 等人，Google）：雙向預訓練 + fine-tuning 範式，「預訓練-微調」成為 NLP 標準流程 | [2018-BERT與預訓練範式](2018-BERT與預訓練範式.md) |
| 2020 | OpenAI 發表 GPT-3（1750 億參數）與 Kaplan 等人的縮放定律（scaling laws）：zero-shot/few-shot 學習，「規模就是能力」 | [2020-GPT3與縮放定律](2020-GPT3與縮放定律.md) |
| 2022 | OpenAI 發布 ChatGPT（GPT-3.5 + RLHF）：對話式 AI 進入億級使用者日常；NLP 從「任務專用模型」轉向「通用助理」 | [2022-ChatGPT與RLHF](2022-ChatGPT與RLHF.md) |
| 2020s | 多模態與代理時代：GPT-4V、Claude、Gemini 的視覺+語言；RAG（檢索增強生成）與工具呼叫（function calling）；LLM 作為「推理引擎」引發對 Chomsky「語言能力 vs 大模型」的世紀辯論——計算語言學七十年後，回到圖靈 1950 年的原點：機器到底能不能「懂」語言？ | [2020s-多模態與RAG時代](2020s-多模態與RAG時代.md) |

## 主線索回顧（偵探筆記）

1. **規則 vs 統計**：Chomsky 的層級給了規則法數學骨架（1956-1975），但規則法在真實世界的雜訊面前节節敗退——1988 年 HMM 詞性標記與 IBM SMT 是兩次致命一擊。
2. **語義的表達**：從 Schank 的概念依存、Minsky 的框架、WordNet 的同義詞集，到 TF-IDF 向量、Word2Vec 的幾何——「語義 = 向量」路線最終全面勝利。
3. **評估與數據**：BLEU（2002）讓 MT 可以自動評分；大語料（Brown Corpus 1961、Google Books）讓統計法有彈藥——沒有數據就沒有革命。
4. **表示學習**：Bengio 2003 的神經語言模型是種子，Word2Vec（2013）讓它發芽，Seq2Seq（2014）讓它開花，Transformer（2017）讓它結果。
5. **規模與湧現**：縮放定律（2020）證明「更多資料 + 更多參數 = 更強能力」；RLHF（2022）把「能力」轉成「可用性」——LLM 時代的核心方程。

## 關鍵人物

- **Alan Turing**：模仿遊戲、機器翻譯之問
- **Noam Chomsky**：語言層級、轉換生成語法
- **Jay Earley**：Earley 剖析器
- **Terry Winograd**：SHRDLU
- **William Woods**：ATN
- **Roger Schank**：概念依存理論
- **Gerald Salton**：向量空間模型、TF-IDF
- **Marvin Minsky**：框架理論
- **George Miller**：WordNet
- **Kenneth Church**：HMM 詞性標記
- **Peter Brown / IBM 團隊**：統計機器翻譯、IBM Model 1-5
- **John Lafferty**：CRF
- **Kishore Papineni**：BLEU
- **Yoshua Bengio**：神經語言模型、注意力
- **Jeffrey Elman**：RNN/循環神經網路
- **Sepp Hochreiter / Jürgen Schmidhuber**：LSTM
- **Kyunghyun Cho**：GRU、RNN Encoder-Decoder
- **Tomas Mikolov**：Word2Vec
- **Ilya Sutskever / Dzmitry Bahdanau**：Seq2Seq、注意力
- **Ashish Vaswani**：Transformer
- **Jacob Devlin**：BERT
- **Alec Radford / Jared Kaplan**：GPT、縮放定律
- **Paul Christiano / Jan Leike**：RLHF
