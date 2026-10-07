# 函數式編程與 λ-Calculus 歷史年表

> 副標題：從希爾伯特計劃的廢墟，到 GPU 上的 monad——一場持續百年的「以函數為萬物本源」運動。
>
> 每一個條目對應本目錄中的一篇「推理探案」風格 wiki：`年份-標題.md`

## 第一幕：邏輯的奠基與危機（1918–1941）

| 年份 | 事件 | wiki |
|---|---|---|
| 1918 | Moses Schönfinkel 發表組合子邏輯：只用 S、K 兩個組合子即可表達一切函數應用，徹底消除「變數」 | [1924-Schönfinkel組合子邏輯](1924-Schonfinkel組合子邏輯.md) |
| 1928 | Hilbert 提出「判定問題」（Entscheidungsproblem）：是否存在演算法能判定一切數學命題的真偽 | （併入 1936-ChurchTuring 案） |
| 1932–1936 | Alonzo Church 提出 λ-Calculus（起初的系統有矛盾，1936 年修正為「單純型 λ-Calculus」），以 λx.M 定義函數、以「應用」為唯一運算 | [1936-ChurchLambdaCalculus](1936-ChurchLambdaCalculus.md) |
| 1936 | Church 用 λ-Calculus 證明判定問題不可解（停機問題）；Turing 同年以圖靈機獨立證明，並證明 λ-Calculus 與圖靈機等價——Church-Turing 論題誕生 | [1936-ChurchTuring論題與不可判定性](1936-ChurchTuring論題與不可判定性.md) |
| 1941 | Haskell Curry 出版《組合邏輯的形式化》，復興 Schönfinkel 的組合子，提出 Curry 化（currying）、組合邏輯等價於 λ-Calculus；Curry-Howard 對應的「Curry」即源自此人 | [1941-Curry組合邏輯](1941-Curry組合邏輯.md) |

## 第二幕：程式語言的誕生（1958–1970）

| 年份 | 事件 | wiki |
|---|---|---|
| 1958 | John McCarthy 在 MIT 設計 LISP：以 λ-Calculus 為靈魂、S-expression 為肉身，「程式即資料」，LISP 1.5 的 `function` 即 λ | [1958-LISP誕生](1958-LISP誕生.md) |
| 1960 | McCarthy 團隊為 LISP 發明垃圾回收（GC）：自由變數的世代問題催生了「不再手動管理記憶體」的革命 | [1960-垃圾回收](1960-垃圾回收.md) |
| 1960 | ALGOL 60 報告引入遞迴程序與 call-by-name（傳名呼叫）：遞迴從禁忌變成標準，傳名語義即 β 歸約的前身 | [1960-ALGOL60遞迴與傳名](1960-ALGOL60遞迴與傳名.md) |
| 1966 | Peter Landin 發明 SECD 虛擬機與 ISWIM 語言：證明 λ-Calculus 可以「機械化執行」；ISWIM 的 `where`、縮排語法影響 ML、Haskell 五十年 | [1966-LandinSECD與ISWIM](1966-LandinSECD與ISWIM.md) |
| 1969 | Dana Scott 提出「域理論」（Domain Theory）與 Strachey 的指稱語義：為「遞迴函數到底『是』什麼」給出數學答案（不動點定理）；Scott 恰是當年證明「單純型 λ-Calculus 模型不存在」的人，五十年後自己給出了模型 | [1969-Scott域理論與指稱語義](1969-Scott域理論與指稱語義.md) |
| 1973 | Carl Hewitt 提出 Actor 模型：無共享狀態、一切靠非同步訊息傳遞，「小惡魔」並行感知的數學 | [1973-Actor模型](1973-Actor模型.md) |
| 1974 | Strachey 與 Wadler 用 continuation 破解 goto 的語義之謎：goto = 換 continuation；CPS 成為編譯器中間表示 | [1974-Continuation與Goto](1974-Continuation與Goto.md) |

## 第三幕：類型革命與 FP 宣言（1972–1985）

| 年份 | 事件 | wiki |
|---|---|---|
| 1973 | Edinburgh 的 Milner 等人為 LCF 定理證明器開發 ML：多型類型推論（Hindley-Milner）讓程式「不寫型別卻全程型別安全」，Exception 也是在此誕生 | [1973-ML誕生](1973-ML誕生.md) |
| 1975 | Gerald Sussman 與 Guy Steele 在 MIT 創造 Scheme：極簡 Lisp，一詞多義的 `lambda` 成為一等公民；Steele 的「Lambda: the Ultimate…」系列論文確立函數呼叫=goto 的編譯理論 | [1975-Scheme與Lambda終極系列](1975-Scheme與Lambda終極系列.md) |
| 1975 | Burstall 等人在 Edinburgh 創造 Hope：第一個有代數資料型別（ADT）與 pattern matching 的語言 | [1975-Hope語言與模式匹配](1975-Hope語言與模式匹配.md) |
| 1977 | John Backus 的圖靈獎演說《Can Programming Be Liberated from the von Neumann Style?》：大力鼓吹函數式編程（FP）與代數程式變換，FP 第一次登上主流舞台 | [1977-BackusFP宣言](1977-BackusFP宣言.md) |
| 1978 | Robin Milner 發表型別推論演算法 W（即 Hindley-Milner 系統）：`let` 多型的數學基礎，日後 Haskell、OCaml、F#、Swift、Rust 的型別推論皆源於此 | [1978-HindleyMilner型別推論](1978-HindleyMilner型別推論.md) |
| 1985 | David Turner 發表 Miranda：第一個商業化「惰性求值」純函數式語言；Turner 的 SASL/KRC 已示範 pattern matching 與守衛式，並證明惰性語言可用組合子圖（G-machine）高效編譯 | [1985-Miranda與惰性求值](1985-Miranda與惰性求值.md) |
| 1986 | 《The Definition of Standard ML》報告：functor/signature 模組系統、第一個用型別規則完整定義動態語義的主流語言 | [1986-StandardML報告](1986-StandardML報告.md) |

## 第四幕：Haskell 與純函數式成熟（1987–2000）

| 年份 | 事件 | wiki |
|---|---|---|
| 1987 | FPCA 會議上，25 餘位研究者決議統一「太多惰性語言」的亂象，成立 Haskell 委員會；命名致敬 Haskell Curry | [1987-Haskell誕生會議](1987-Haskell誕生會議.md) |
| 1990 | 《Haskell 1.0 報告》發表：純函數、惰性求值、型別類別（type class，由 Phil Wadler 與 Stephen Blott 提出）、monadic I/O 雛形；1997 年 Haskell 98 成為穩定標準 | [1990-Haskell報告與型別類別](1990-Haskell報告與型別類別.md) |
| 1993 | Ericsson 的 Joe Armstrong 等人發表 Erlang：為電信九個九（99.9999999%）可用性而生，以函數式語法＋Actor 行程模型證明「FP 能扛得住真實世界的錯誤」 | [1993-ERLANG電信級函數式](1993-ERLANG電信級函數式.md) |
| 1996 | Chris Okasaki 的博士論文《Purely Functional Data Structures》：證明「不可變也有高效結構」，結構共享＋惰性攤還分析 | [1996-Okasaki純函數式資料結構](1996-Okasaki純函數式資料結構.md) |
| 1997 | Conal Elliott 發表 Fran（Functional Reactive Animation）：Behavior = time -> a，響應式程式（FRP）的數學 | [1997-FRP與響應式程式](1997-FRP與響應式程式.md) |

## 第五幕：函數式復興與大數據時代（2004–2020s）

| 年份 | 事件 | wiki |
|---|---|---|
| 2004 | Google 發表 MapReduce：以 Backus 式的 map/reduce 高階函數重寫分散式計算，數千台機器如同一次函數呼叫；同年 OCaml 系企業（Jane Street）以 FP 做高頻交易 | [2004-MapReduce函數式大數據](2004-MapReduce函數式大數據.md) |
| 2005 | Don Syme（Microsoft Research）發表 F#：OCaml 的 .NET 變體，async workflow（monad 包裝非同步）比 C# await 早兩年 | [2005-FSharp與.NET函數式](2005-FSharp與.NET函數式.md) |
| 2007 | Rich Hickey 發表 Clojure：JVM 上的現代 Lisp，不可變資料結構＋持久化向量（RRB/persistent vector），證明「不可變」在多核時代反而更快 | [2007-Clojure不可變資料結構](2007-Clojure不可變資料結構.md) |
| 2012 | Matei Zaharia 發表 Spark 與 RDD：不可變分散式資料集＋血緣圖，容錯靠重算——純函數可重試的數學 | [2012-SparkRDD](2012-SparkRDD.md) |
| 2014 | Java 8 正式引入 lambda 與 Stream API：全球最大語言群體第一次在日常用上 λ-Calculus 語法 | [2014-Java8Lambda](2014-Java8Lambda.md) |
| 2015 | Rust 1.0 發布：ownership/borrowing 是線性型別 λ-Calculus 的工程變體，無 GC 的記憶體安全 | [2015-Rust與線性型別](2015-Rust與線性型別.md) |
| 2013 | Facebook 發表 React：以「UI = f(state)」的純函數模型重寫前端；虛擬 DOM、單向資料流、後來的 Hooks（2019）皆為函數式思想進入億級使用者日常的證據 | [2013-React函數式UI](2013-React函數式UI.md) |
| 2020s | 函數式思想全面內建：Rust 的 Result/Option monad、Swift 的 enum+pattern matching、Scala 3、GPU 上的 Futhark，以及 Haskell/OCaml 在區塊鏈（Cardano/Plutus、Tezos/Michelson）中的應用——λ-Calculus 誕生九十年後，成為機器學習、區塊鏈與平行運算的底層語法 | [2020s-函數式思想的全面內建](2020s-函數式思想的全面內建.md) |

## 主線索回顧（偵探筆記）

1. **消除變數**（Schönfinkel/Curry/組合子）→ λ-Calculus 的純化 → 編譯器的中間表示（CPS、STG、G-machine）。
2. **Church-Turing 等價**：λ-Calculus 從「邏輯工具」升格為「計算模型」，LISP 讓它成為可執行的程式語言。
3. **型別對應邏輯**（Curry-Howard）：命題即型別、證明即程式——ML/Haskell 的型別系統是「可執行的數學」。
4. **純函數 + 不可變**：從 Backus 的宣言、Haskell 的實踐，到 MapReduce、React、多核時代的必然選擇。
5. **Monad 抽象**：把「副作用」裝進盒子裡，讓純函數世界重新包容 I/O、狀態、例外、非同步——這是 1990 年代 Haskell 案中最精采的一筆。

## 關鍵人物

- **Moses Schönfinkel**：組合子邏輯（1924）
- **Alonzo Church**：λ-Calculus、Church-Turing 論題
- **Haskell Curry**：組合邏輯、Curry 化、Curry-Howard
- **Alan Turing**：圖靈機與等價性證明
- **John McCarthy**：LISP、垃圾回收
- **Peter Landin**：SECD 機器、ISWIM
- **Dana Scott / Christopher Strachey**：域理論、指稱語義
- **Robin Milner**：ML、LCF、型別推論
- **Gerald Sussman / Guy Steele**：Scheme、Lambda 終極系列
- **John Backus**：FP 宣言（1977 圖靈獎）
- **David Turner**：SASL/KRC/Miranda、惰性求值編譯
- **Phil Wadler**：型別類別、Monad 教科書化
- **Joe Armstrong**：Erlang
- **Jeff Dean / Sanjay Ghemawat**：MapReduce
- **Rich Hickey**：Clojure
- **Jordan Walke**：React
- **Carl Hewitt**：Actor 模型
- **Christopher Wadler**：continuation、type class、monad
- **Rod Burstall**：Hope、代數資料型別
- **Chris Okasaki**：純函數式資料結構
- **Conal Elliott**：FRP/Fran
- **Don Syme**：F#
- **Matei Zaharia**：Spark/RDD
- **Brian Goetz**：Java 8 Lambda
- **Graydon Hoare**：Rust
