# 1959 — COBOL 問世

## 案件摘要
1959 年，美國國防部召集 CODASYL 委員會，在極短時間內催生出 COBOL（Common Business-Oriented Language）。這門以英語式語法寫成的商業資料處理語言，成為史上壽命最長的程式語言「活化石」，至今仍驅動著全球銀行、保險與政府系統。

## 前因 -- 為什麼會有這個案子
1950 年代的電腦世界是科學計算的天下：Fortran（1957）服務工程師與物理學家，組合語言服務硬體。但商業世界有一種截然不同的需求——**資料處理（data processing）**：

- 銀行每天要處理数十萬筆存款、提款、轉帳記錄
- 保險公司要計算保費、理賠、精算報表
- 政府要發放薪俸、管理社會安全帳戶

這些工作的數學不難，但**資料量巨大、格式繁雜、報表規格嚴格**。1950 年代末，每家電腦廠商都有自己的組合語言，程式無法移植；一旦換機器，幾年累積的商業程式全部作廢。美國國防部（本身就是最大電腦買主）深受其害，於是 1959 年 5 月由國防部資助召開會議，成立 **CODASYL**（Conference on Data Systems Languages）委員會，目標只有一個：造出一門「通用商業語言」。

關鍵前驅是 **Grace Hopper**。她早在 1955 年就在 UNIVAC 上開發了 **FLOW-MATIC**（原名 B-0），這是史上第一門使用近似英語語法的資料處理語言。Hopper 堅信一個當時被視為異端的理念：

> 「程式應該用商業人士看得懂的語言來寫。」

CODASYL 委員會大量借鑒 FLOW-MATIC 的設計（Hopper 本人是重要顧問），另參考 IBM 的 Commercial Translator 與 Remington Rand 的 AIMACO。1959 年 12 月，COBOL 規格書出爐——從立項到定案只用了約六個月，堪稱語言設計史上最快的「破案」。

## 線索與推理 -- 數學式、程式、理論
### 1. 英語式語法：讓程式像句子
COBOL 的核心發明是把程式敘述寫成近似英語的句子，例如：

```cobol
MOVE A TO B.
ADD 1 TO COUNTER.
IF BALANCE < 0 THEN PERFORM OVERDUE-ROUTINE.
```

`MOVE A TO B` 這種「動詞—受詞」結構，本質上是一種**以動作為中心的 DSL**。以現代觀點看，它等價於賦值運算：

$$B \leftarrow A$$

當時主流觀點（如 Dijkstra）批評英語式語法「太囉唆」，但辯護方的推理是：**可讀性即可維護性**——商業系統壽命以十年計，讓非程式設計師（會計師、精算師）能讀懂程式邏輯，價值遠超打字成本。歷史證明這個推理在商業領域是對的。

### 2. 檔案結構與批次資料處理
COBOL 的第二大發明是**把「檔案」當成一級公民**。它的程式骨架分為四大部（DIVISION）：

```cobol
IDENTIFICATION DIVISION.   *> 程式身分證
PROGRAM-ID. PAYROLL.

DATA DIVISION.             *> 描述所有資料結構
FILE SECTION.
FD  EMPLOYEE-FILE.
01  EMPLOYEE-RECORD.
    05  EMP-ID         PIC 9(5).
    05  EMP-NAME       PIC X(20).
    05  EMP-SALARY     PIC 9(7)V99.   *> 7位整數+2位小數

WORKING-STORAGE SECTION.
01  TOTAL-PAY          PIC 9(9)V99 VALUE 0.

PROCEDURE DIVISION.        *> 主邏輯
    OPEN INPUT EMPLOYEE-FILE.
    READ EMPLOYEE-FILE
        AT END MOVE 'Y' TO EOF-FLAG
    END-READ.
    PERFORM UNTIL EOF-FLAG = 'Y'
        ADD EMP-SALARY TO TOTAL-PAY
        READ EMPLOYEE-FILE
            AT END MOVE 'Y' TO EOF-FLAG
        END-READ
    END-PERFORM.
    DISPLAY 'TOTAL PAY = ' TOTAL-PAY.
    CLOSE EMPLOYEE-FILE.
    STOP RUN.
```

其中 `PIC`（PICTURE 子句）是精妙的**資料格式宣告語言**：`9(5)` 表示五位數字、`X(20)` 表示二十個字元、`V` 表示隱含小數點。特別注意 `9(7)V99` ——COBOL 用**定點十進位**表示金額：

$$\text{金額} = \text{整數部分} + \frac{\text{小數部分}}{100}$$

這是一個被後世反覆驗證的洞察：浮點數（IEEE 754 二進位）**無法精確表示 0.1**，會產生累積捨入誤差；而金額計算必須分毫不差。這就是為什麼六十年後，處理金錢的系統仍然首選定點十進位——現代 Java 的 `BigDecimal`、Python 的 `decimal.Decimal` 都是 COBOL `PIC V` 的精神後裔。

### 3. 批次處理模型
COBOL 程式的典型形態是「讀一筆—處理一筆—寫一筆」的串流迴圈，這是磁帶時代的產物，也定義了此後三十年的**批次處理（batch processing）**正典：夜間跑批、日間報表。用數學描述，一個 COBOL 批次程式就是一個作用在記錄流上的摺疊（fold）：

$$\text{Total} = \bigoplus_{i=1}^{n} f(r_i)$$

這與今天的 MapReduce、Spark 的 reduce 操作在本質上是同一個抽象。

## 結案 -- 後果與影響
- **活化石**：估計至今全球仍有 2000 億行以上 COBOL 程式碼在生產環境運行，美國社會安全署、多國銀行核心系統每天仍在跑 COBOL。COVID-19 期間（2020），美國紐澤西州甚至公開徵求 COBOL 程式設計師來修復失業金系統。
- **語言影響**：`PIC` 定點十進位影響了所有商業計算語言；資料描述與邏輯分離（DATA/PROCEDURE DIVISION）預示了現代的 schema 與程式碼分離。
- **Y2K 危機**：COBOL 用兩位數表示年份（`PIC 99`），導致 1999 年全球耗費數千億美元修復千年蟲——這是「活化石」的另一面：太成功，所以太難淘汰。
- **人才斷層**：大學早已不教 COBOL，但生產系統還在用，形成獨特的「遺留系統考古學家」職業。

## 關鍵人物與文獻
- **Grace Hopper（1906–1992）**：FLOW-MATIC 之父、編譯器概念先驅、COBOL 的精神母親；也是第一位提出「程式應寫成英語式」的人。美國海軍驅逐艦 USS Hopper 以她命名。
- **CODASYL 委員會**：1959 年由美國國防部資助成立，六個月內產出 COBOL 規格；後來也主導了 1960–70 年代的資料庫網狀模型（CODASYL DBTG）。
- 文獻：*COBOL: Initial Specifications for a Common Business Oriented Language*（CODASYL, 1960）；Jean Sammet, *Programming Languages: History and Fundamentals*（1969）。
