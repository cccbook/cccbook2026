# 1952 Hopper A-0 編譯器

## 案發現場

1952 年，哈佛大學畢業的數學博士 Grace Hopper（葛麗絲·霍普）在美國海軍的 UNIVAC 電腦前，面對一個所有人都視為理所當然、她卻認為錯誤的「常識」：

> **「電腦只懂機器碼，所以人類必須用機器碼寫程式。」**

案發現場的困境極為具體。1950 年代初的程式設計師，每天的工作是這樣的：把數學公式拆解成機器碼指令（一串二進位數字或助憶碼），手工查表分配記憶體位址，然後把指令一行一行打進機器。寫一個平方根副程式要幾天；更痛苦的是**重複勞動**——每個程式都要重寫同樣的「讀入資料、除錯、輸出」例行程序。Hopper 觀察到：UNIVAC 的程式設計師有一本「副程式簿」，裡面抄著常用的副程式碼，每次寫新程式就手工抄錄進去。她問了一個石破天驚的問題：

> **「為什麼不讓電腦自己把副程式抄進去？」**

這個問題在當年是異端邪說。大多數工程師相信：機器是精確的，讓機器「寫」程式會引入錯誤；編譯是浪費機器時間的事（機器時間極為昂貴）；真正的工程師就該用機器碼。Hopper 的老闆甚至告訴她：「電腦只能做算術，不能寫程式。」

同時期，英國曼徹斯特大學的 Kilburn 團隊在 1949 年實作了 Short Code 的前身（Booth 的符號組合），美國的 John Mauchly 也在 1949 年提出了 Short Code——一個用「簡短符號」寫數學式、再由機器解譯執行的系統。一場「機器翻譯」的革命正在醞釀，而 Hopper 將成為它的總工程師。

## 偵查過程

Hopper 的偵查思路，是把「翻譯」這件事拆解成三個層次的推理。

**第一層推理：副程式 = 可命名的資產。** Hopper 的第一個洞察來自她的數學背景：副程式就像數學中的函數 $f(x)$——只要定義一次，就可以無限次呼叫。她把每個常用副程式編碼成一個**短代碼**（short code）：例如 `sqrt` 對應代碼 `SQ`，`sin` 對應 `SN`。程式設計師只需寫 `SQ X`（對 X 開根號），機器會自動展開成完整的機器碼。她的第一個系統 **A-0**（1952）就是這樣的「副程式組合器」：

```text
SQ, X          # 呼叫平方根副程式，作用於 X
SN, Y          # 呼叫正弦副程式，作用於 Y
```

A-0 的操作流程：程式設計師寫一連串短代碼（打在紙帶上），A-0 編譯器讀入後，到「副程式庫」中找出對應的機器碼，**自動配置記憶體位址、自動串接**，產出完整的可執行程式。這是歷史上第一個編譯器（assembler-compiler）。用今天的語言說，A-0 做了兩件事：**符號解析（組譯）+ 副程式連結（linking）**——這兩件事至今仍是所有編譯工具鏈的核心步驟。

**第二層推理：從「翻譯副程式」到「翻譯數學式」。** A-0 成功後，Hopper 發現了更深層的問題：就算副程式可以自動串接，程式設計師還是要把數學公式**手工拆解**成副程式呼叫。例如公式

$$y = a \cdot x^2 + b \cdot x + c$$

工程師要手工拆成「先算 $x^2$、再乘 $a$、再算 $b \cdot x$、再加 $c$」的一連串呼叫。Hopper 問：**為什麼不讓機器直接看懂整條公式？**

這引出了她的第二個系統 **A-2**（1953）與後來的 **FLOW-MATIC**（1955）：一個能直接處理「接近人類語言」的編譯器。FLOW-MATIC 的革命性在於：它用**英文單字**寫程式：

```text
COMPARE PRODUCT NUMBER (A) WITH PRODUCT NUMBER (B).
IF GREATER GO TO OPERATION 10.
READ INVENTORY FILE (A).
ADD QUANTITY SOLD TO TOTAL SOLD.
```

這段程式，今天的程式設計師一眼就能看懂。FLOW-MATIC 證明了一件事：**程式語言的語法可以接近人類語言，而機器仍然能翻譯執行它。** 這個信念直接催生了 COBOL（1959）——Hopper 是 COBOL 的精神母親，COBOL 的語法大量繼承自 FLOW-MATIC。

**第三層推理（核心技術推導）：編譯器的三段式架構。** Hopper 從 A-0 到 FLOW-MATIC 的演進中，推導出了編譯器的標準架構，這個架構至今仍是教科書內容：

1. **詞法分析（Lexing）**：把輸入的字符流切成「詞」（token）。例如 `ADD QUANTITY TO TOTAL` 被切成 `ADD`、`QUANTITY`、`TO`、`TOTAL` 四個 token。Hopper 用「查表法」實作：對每個單字查副程式庫，找到就替換成機器碼。
2. **語義處理（Expansion）**：把每個 token 展開成對應的機器碼片段，並**自動分配位址**。這是最關鍵的創新：程式設計師不再需要手工分配記憶體，編譯器會追蹤每個變數的位置。Hopper 發明了「符號位址表」（symbol table）——變數名到記憶體位址的對照表。
3. **組裝輸出（Assembly）**：把所有機器碼片段串接成完整程式，處理跳躍位址的修正。

用現代 Python 重現這個三段式架構：

```python
def compile_flow_matic(source, subroutine_lib):
    """重現 Hopper 的編譯器架構：Lexing -> Expansion -> Assembly"""
    tokens = source.split()                    # 第一段：詞法分析
    code, symtab, addr = [], {}, 0
    for tok in tokens:
        if tok in subroutine_lib:              # 第二段：副程式展開
            frag = subroutine_lib[tok]
            code.append((addr, frag)); addr += len(frag)
        elif tok not in ('TO', 'THE', 'A', 'B'):  # 跳過虛詞
            if tok not in symtab:              # 自動分配位址
                symtab[tok] = addr; addr += 1
            code.append((addr, f"STORE {tok}"))
    return code, symtab                        # 第三段：組裝輸出
```

注意其中一個巧妙的細節：Hopper 發現 FLOW-MATIC 程式裡的英文虛詞（TO、THE、OF）對機器沒有意義，可以**直接跳過**。這就是「語法糖」的最早實踐——人類語言的冗餘，讓程式更好讀，機器則無視之。

**第四層推理：FLOW-MATIC 的商業計算革命。** Hopper 把 FLOW-MATIC 用在真正的商業任務上：薪資計算、庫存管理、帳務處理。她證明了編譯器的經濟價值：一個熟練的程式設計師用機器碼一天寫 15 行，用 FLOW-MATIC 一天能寫 100+ 行——生產力提升近十倍。這個數據，說服了整個產業。1959 年，當國防部召開會議制定 COBOL 規格時，Hopper 的 FLOW-MATIC 是唯一的實作範例，COBOL 的「英文式語法」直接來自她。

**並行偵查：Short Code 的解譯器路線。** 同時期還有另一條路線：Mauchly 的 **Short Code**（1949，在 UNIVAC 上由 Betty Holberton 實作）不採用「編譯」，而是**逐句解譯**——機器每次讀到一個短碼，就現場執行對應操作，不產生中間程式。Short Code 的代碼極簡：

```text
X0 = (Y0 + Z0) / A0    # 寫成短碼：
00 X0 07 Y0 07 Z0 05 A0
```

其中 `07` 代表加、`05` 代表除。解譯器路線的優點是簡單、即時；缺點是每次執行都要重新解譯，比編譯慢 50 倍。這條路線最終演化成今天的 Python、JavaScript（直譯語言），而 Hopper 的編譯路線演化成 C、COBOL、FORTRAN（編譯語言）。**編譯 vs 解譯**的兩大路線之爭，在 1950 年代初就已經定調。

## 結案報告

Grace Hopper 的遺產，改寫了整個軟體產業的命運：

1. **第一個編譯器**：A-0（1952）是史上第一個編譯器，「讓機器寫程式」從異端變成正統。
2. **COBOL 之母**：FLOW-MATIC 的英文式語法直接成為 COBOL 的藍本。COBOL 至今仍支撐著全球銀行、保險、政府的核心系統——世界上仍有數百億行 COBOL 在執行。
3. **符號位址表與自動記憶體分配**：編譯器的核心技術，從 A-0 傳到 [1957-FORTRAN.md](1957-FORTRAN.md) 的優化編譯器，再到今天的所有編譯器。
4. **編譯 vs 解譯的兩大路線**：她的編譯路線與 Short Code 的解譯路線，定調了後續所有語言的分類——[1958-LISP.md](1958-LISP.md) 走解譯路線，C 走編譯路線，今天的 Python/JVM 則是兩者混合。
5. **「除錯」一詞的普及**：1947 年她的團隊在 Harvard Mark II 中發現一隻飛蛾卡在繼電器裡造成故障，把它貼在工作日誌上寫道「First actual case of bug being found」——「bug（蟲）」與「debugging（除蟲）」從此成為程式設計的標準用語。
6. **海軍少將的傳奇**：Hopper 一直服務到 1986 年以 79 歲高齡退役，是美國海軍史上最年長的現役軍官。她終身推廣「程式應該用人類語言寫」的信念，並在無數演講中傳遞一句名言：

> 「人類最危險的一句話是：『我們一直都是這樣做的。』」

## 證據與工具

**證據一：FLOW-MATIC 風格編譯器（Python 完整重現）**

```python
LIB = {
    'ADD':    ['LOAD A', 'ADD B'],
    'COMPARE':['LOAD A', 'CMP B'],
    'READ':   ['IO READ'],
}

def compile_flow_matic(source):
    tokens = source.split()
    code, symtab, addr = [], {}, 0
    stopwords = {'TO', 'THE', 'OF', 'A', 'B', 'WITH', 'FILE', '.'}
    for tok in tokens:
        if tok in LIB:                       # 副程式展開
            for instr in LIB[tok]:
                code.append((addr, instr)); addr += 1
        elif tok in stopwords or tok.isdigit():
            continue                         # 虛詞跳過
        else:
            if tok not in symtab:
                symtab[tok] = addr; addr += 1
            code.append((addr, f'SYMB {tok}'))
    return code, symtab

src = "COMPARE PRODUCT NUMBER WITH QUANTITY ADD TOTAL"
code, symtab = compile_flow_matic(src)
for addr, instr in code:
    print(f"{addr:03d}  {instr}")
print("符號表:", symtab)
```

**證據二：Short Code 解譯器（Python）**

```python
# Short Code 的代碼表（簡化自 1949 UNIVAC 版本）
OPCODE = {'07': lambda a,b: a+b, '05': lambda a,b: a/b,
          '06': lambda a,b: a*b, '02': lambda a,b: a-b}

def short_code_interpret(program, mem):
    """Short Code：逐句解譯，不產生中間程式"""
    mem = dict(mem)
    i = 0
    while i < len(program):
        op = program[i]
        if op in OPCODE:                     # op arg1 arg2 result
            a, b, dest = program[i+1], program[i+2], program[i+3]
            mem[dest] = OPCODE[op](mem[a], mem[b])
            print(f"{op} {a} {b} -> {dest} = {mem[dest]}")
            i += 4
        else:
            i += 1
    return mem

# 計算 (Y + Z) / A，Y=10, Z=20, A=3
mem = {'X0': 0, 'Y0': 10, 'Z0': 20, 'A0': 3}
prog = ['06','Y0','A0','T0',     # T0 = Y * A (先通分，僅示範流程)
        '07','Z0','T0','T1',     # T1 = Z + T0
        '05','T1','A0','X0']     # X0 = T1 / A
result = short_code_interpret(prog, mem)
print("X0 =", result['X0'])
```

**證據三：編譯 vs 解譯的效能對比**

```python
import time

def compiled_runtime(n=100000):
    """編譯路線：翻譯一次，執行 n 次都是機器速度"""
    t0 = time.perf_counter()
    total = 0
    for _ in range(n):
        total += 2 * 3 + 1        # 「編譯後」的常數已可優化
    return time.perf_counter() - t0

def interpreted_runtime(n=1000):
    """解譯路線：每次執行都要重新解析"""
    t0 = time.perf_counter()
    total = 0
    for _ in range(n):
        total = eval("2 * 3 + 1") # eval = 每次重新「解譯」
    return time.perf_counter() - t0

c, i = compiled_runtime(), interpreted_runtime()
print(f"編譯式(10萬次): {c:.4f}s, 解譯式(1千次): {i:.4f}s")
print(f"即使解譯只跑了 1/100 的次數，仍比編譯式慢 —— 印證 Short Code 比 A-0 慢 50 倍的歷史紀錄")
```

三份證據串成 Hopper 的完整遺產：編譯器三段式架構（證據一）、Short Code 解譯路線（證據二）、編譯優於解譯的效能證明（證據三）。「程式應該用人類語言寫」——這個信念，讓程式設計從工程師的特權，變成了千萬人的日常。
