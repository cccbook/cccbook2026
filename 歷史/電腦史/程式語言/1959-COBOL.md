# 1959 COBOL：讓程式說英文的商業語言

## 案發現場

1950 年代末，美國的商業與政府機關陷入一場「資料處理災難」。軍方與保險公司、銀行買了 Univac、IBM 的機器，卻發現兩個致命問題：第一，每台機器的語言都不一樣，換機器就得重寫所有程式；第二，FORTRAN 這種為科學家設計的數學語言，對會計與事務人員而言如同天書——他們要處理的是「薪資冊」「保險給付」「庫存報表」，不是矩陣求逆。

當時美國國防部面對每年數億美元的資料處理支出，決定親自出手。1959 年 5 月，國防部召集各廠商與用戶在五角大廈開會，成立 CODASYL 委員會（Conference on Data Systems Languages），目標是設計一種**通用商業語言**（Common Business Oriented Language），並要求它具備三個特質：機器無關、接近英文、資料描述能力強。委員會僅用六個月就產出 COBOL 規格（1959 年 12 月），1960 年正式發布。

在這場偵查中，最關鍵的「線人」是海軍的 Grace Hopper——她早在 1952 年就寫出世界第一個編譯器 A-0，1955 年又開發了 FLOW-MATIC（原名 B-0），這是第一個用近似英文寫成的資料處理語言。COBOL 的整個哲學，幾乎是 FLOW-MATIC 的放大重演。

## 偵查過程

### 線索一：Grace Hopper 的預言——「程式應該讓人讀得懂」

Hopper 的靈感來自一個深刻的觀察：她發現 FLOW-MATIC 的用戶居然能直接讀懂別人寫的程式，並修改兩三行就讓它跑起來。她由此推導出一個當時駭人聽聞的命題：**程式語言應該以「人的可讀性」為第一目標**，因為軟體的生命週期遠長於開發時間，維護者是人而不是機器。她甚至在國會作證時說過：「為什麼不能讓銀行經理用他自己的語言——英文——來取資料？」

這個推理直接塑造了 COBOL 的語法。COBOL 的敘述讀起來像英文句子：

```cobol
IF SALARY IS GREATER THAN 50000
   PERFORM BONUS-ROUTINE
ELSE
   ADD OVERTIME-PAY TO TOTAL-WAGES.
```

名稱幾乎就是英文單字：`ADD ... TO ...`、`MOVE ... TO ...`、`PERFORM ... UNTIL ...`。委員會還刻意讓 COBOL 支援「縮寫模式」與「完整英文模式」兩種寫法，並規定程式裡可以保留註解行，方便非程式設計師閱讀。這種「像英文」的堅持後來常被嘲諷為冗長（有人說 COBOL 的全名該是 Compiles Only Because Of Legibility），但它的核心訴求——自文件化（self-documenting）——在六十年後的今日已是所有語言的共識。

### 線索二：資料描述部——把「檔案格式」寫進語言

商業運算的本質不是數學公式，而是**大量固定格式紀錄的批次處理**。COBOL 的偵查推導出一個革命性設計：語言必須內建「資料描述」能力。COBOL 程式分為四大部（division）：`IDENTIFICATION DIVISION`（識別部）、`ENVIRONMENT DIVISION`（環境部，描述機器）、`DATA DIVISION`（資料部）、`PROCEDURE DIVISION`（程序部）。

資料部用層級編號描述檔案結構：

```cobol
DATA DIVISION.
FILE SECTION.
FD  EMPLOYEE-FILE.
01  EMPLOYEE-RECORD.
    05  EMP-NAME        PIC X(20).
    05  EMP-SALARY      PIC 9(7)V99.
    05  EMP-BIRTH-DATE.
        10  EMP-YEAR    PIC 9(4).
        10  EMP-MONTH   PIC 99.
        10  EMP-DAY     PIC 99.
```

`PIC`（picture clause）子句用「圖樣」描述資料：`X(20)` 是 20 個字元，`9(7)V99` 是 7 位整數加 2 位小數（`V` 表示隱含的小數點，實際存在固定格式欄位裡）。這種宣告式資料描述，正是後世 record type、C 的 `struct`、SQL 的 schema、乃至 JSON/IDL 的祖先。層級編號（01/05/10）讓巢狀資料結構一目了然，也讓程式能直接按欄位名存取，而不必像組合語言那樣手算位移量。

### 線索三：為「批次報表」設計的控制結構

COBOL 的程序部圍繞商業處理的迴圈模型設計：讀一筆紀錄、處理、寫一筆輸出，直到檔案結束。語言內建 `READ ... AT END`、`PERFORM ... UNTIL`、報表分頁與小計的敘述。委員會的推理是：商業程式設計師不需要遞迴與複雜的數學抽象（COBOL 直到 2002 年才有遞迴與指標），需要的是可靠、直觀、能處理百萬筆紀錄的批次邏輯。

## 結案報告

COBOL 立刻大獲成功。到 1970 年代，它已是全球最廣泛使用的語言；美國國防部規定採購的機器必須支援 COBOL，促成了語言標準化（COBOL-68、74、85、2002、2014 由 ANSI/ISO 制定）。它與 FORTRAN 的分野確立了程式語言世界的兩大陣營：科學計算 vs 商業資料處理。

COBOL 的遺產與包袱是一體兩面：

- **遺產**：資料描述（record/struct/schema 的概念）、自文件化程式的理念、語言標準化的先河、以及至今仍在全球銀行、保險、政府主機上運行的數百億行程式碼。2020 年新冠疫情期间，美國多州還緊急徵求 COBOL 工程師來修改失業給付系統，證明它仍是活著的語言。
- **包袱**：因為舊系統「能用就不動」，無數核心系統被鎖死在 COBOL 上，維護工程師日漸稀少，形成著名的「COBOL 遺留系統危機」。年份只用兩位數的習慣更釀成 2000 年的 Y2K 危機，全球耗費數千億美元修補。

一句話總結：FORTRAN 給科學家數學，COBOL 給商業世界英文；而這份英文契約，人類至今仍在履約。

## 證據與工具

以下用 COBOL 語法示範薪資計算，並用 Python 模擬 COBOL 的 `PIC` 資料描述與批次處理：

```cobol
IDENTIFICATION DIVISION.
PROGRAM-ID. PAYROLL.
DATA DIVISION.
WORKING-STORAGE SECTION.
01  WS-EMP.
    05  WS-NAME    PIC X(10) VALUE "CHEN".
    05  WS-HOURS   PIC 9(3)  VALUE 172.
    05  WS-RATE    PIC 9(3)V99 VALUE 350.50.
    05  WS-PAY     PIC 9(7)V99.
PROCEDURE DIVISION.
    COMPUTE WS-PAY = WS-HOURS * WS-RATE
    DISPLAY "NAME: " WS-NAME " PAY: " WS-PAY
    STOP RUN.
```

```python
# 模擬 COBOL 的 PIC 子句：固定長度欄位、隱含小數點 V
class Pic:
    def __init__(self, picture):
        self.picture = picture
        if "V" in picture:
            ints, decs = picture.split("V")
        else:
            ints, decs = picture, ""
        self.int_len = sum(int(c.isdigit()) for c in ints)   # 9 的個數
        self.dec_len = sum(int(c.isdigit()) for c in decs)

    def pack(self, value):          # 存入固定格式（類比 COBOL 內部表示）
        scaled = round(value * 10 ** self.dec_len)
        total = self.int_len + self.dec_len
        return str(scaled).zfill(total)

    def unpack(self, packed):       # 讀出（V 是隱含小數點）
        v = int(packed) / 10 ** self.dec_len
        return round(v, self.dec_len)

salary = Pic("9(7)V99")
print("打包後內部儲存:", salary.pack(172 * 350.50))
print("解包回數值    :", salary.unpack(salary.pack(172 * 350.50)))

# 模擬 COBOL 的批次處理：READ ... AT END 迴圈
records = [("CHEN", 172, 350.50), ("LIN", 160, 320.00), ("WANG", 185, 400.00)]
total = 0.0
it = iter(records)
while True:                          # PERFORM ... UNTIL / AT END 的等價
    try:
        name, hours, rate = next(it)  # READ
    except StopIteration:             # AT END
        break
    pay = hours * rate
    total += pay
    print(f"NAME: {name:<10s} PAY: {pay:,.2f}")
print(f"TOTAL WAGES: {total:,.2f}")
```

執行可見：`Pic` 類別重現了 COBOL 資料描述的核心——用「圖樣」宣告欄位、用隱含小數點 `V` 存放數值；批次迴圈則重現了 COBOL 程序部「讀一筆、算一筆、加總」的典型流程，正是六十年來銀行主機上每天都在執行的邏輯。
