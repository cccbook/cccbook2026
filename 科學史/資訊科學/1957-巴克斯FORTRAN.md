# 1957 - Backus 的 FORTRAN（第一個成功的編譯器）

## 案件摘要
1957 年 4 月，**John Backus（1924–2007）** 帶領 IBM 的 13 人團隊，
發布了 **FORTRAN**（FORmula TRANslation）——**第一個成功的編譯器**：
$$\boxed{\text{高階語言的程式碼} \xrightarrow{\text{編譯器}} \text{機器碼（效率接近手工）}}$$
在 FORTRAN 之前，所有人都用**組合語言**（assembly）寫程式——
一行人類指令對應一行機器碼，**程式設計是苦役**。
$$\text{組合語言（機器思維）} \xrightarrow{\text{FORTRAN 1957}} \text{高階語言（人類思維）}.$$
**FORTRAN I 編譯器**產生的機器碼**效率接近手工最佳化的組合語言**——
這說服了懷疑者：**「程式設計師不需要懂機器」**。
**1977 年，Backus 獲得圖靈獎**。

## 前因 -- 為什麼會有這個案子
- **組合語言的苦役（1946–1957）**：
  - **ENIAC（1946）**的「程式設計」是**插電線**（重接電纜，需要幾天）；
  - **儲存程式電腦（1948–）**：程式用組合語言寫——
    每一行都是機器碼的助記符（`ADD R1, R2`）；
    **寫一個 1000 行的程式需要數週**。
  $$\text{程式設計} = \text{苦役（機器碼的一行行翻譯）}.$$
- **Backus 的背景**：
  Backus 是 IBM 的程式設計師，負責 **IBM 701** 的程式庫。
  他發現：**大部分時間都在寫「同樣的」程式碼**（迴圈、矩陣運算）——
  $$\text{「為什麼不能讓機器自己翻譯？」}$$
- **IBM 的支持（1954）**：
  IBM 當時面臨 **Univac**（競爭對手）的壓力——
  Univac 已有 **A-0 編譯器**（Grace Hopper 的作品）但效率低。
  IBM 投資 Backus 的團隊，目標：
  $$\boxed{\text{「編譯器的機器碼效率要接近手工組合語言」}}$$
  （**這個目標是 FORTRAN 成功的關鍵**——之前的編譯器都因效率低而被拒用。）
- **13 人的團隊（1954–1957）**：
  Backus 帶領 13 人（包括 **Irving Ziller、Robert Nelson、Lois Haibt**），
  花了 **2.5 年、228 人年**寫出 FORTRAN I 編譯器——
  **約 25,000 行組合語言**。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：FORTRAN 的語言設計
FORTRAN I（1957）的關鍵特性：
- **算術運算式**：`X = (A + B) * C`（人類的數學寫法）；
- **DO 迴圈**：`DO 10 I = 1, 100`；
- **IF 判斷**：`IF (X) 10, 20, 30`（三路分支）；
- **副程式**：`CALL SUB(X, Y)`。
**對照組合語言**：
```assembly
; X = (A + B) * C 的組合語言
LOAD  A        ; 載入 A 到暫存器
ADD   B        ; 加 B
STORE  T1      ; 存到暫存器 T1
LOAD  T1
MUL   C        ; 乘 C
STORE  X       ; 存到 X
```
$$\text{1 行高階} \approx 6 \text{ 行組合語言}.$$

### 第二條線索：編譯器的技術（最佳化的誕生）
**FORTRAN I 編譯器的技術**（1957，當時最先進）：
1. **詞法分析**：把字元流切成記號（token）；
2. **語法分析**：建立運算式的樹狀結構；
3. **暫存器分配**：把變數分配到 CPU 暫存器（**效率的關鍵**）；
4. **迴圈最佳化**：把不變的計算移出迴圈；
5. **程式碼生成**：產生機器碼。
$$\text{詞法} \to \text{語法} \to \text{最佳化} \to \text{生成} \quad\text{（編譯器的四段式管線）}.$$
**BNF 范式（Backus Normal Form, 1959/1960）**：
Backus 在 1959 年發明了**語法描述的形式語言**：
$$\langle \text{expr} \rangle ::= \langle \text{term} \rangle \mid \langle \text{expr} \rangle + \langle \text{term} \rangle$$
**這是程式語言理論的基礎**——所有語言的規格書都用 BNF 寫。

### 第三條線索：效率的證明（1957 的說服力）
**FORTRAN I 的效率**（IBM 704）：
$$\text{編譯器產生的機器碼效率} \approx \text{手工組合語言的 } 50\% \sim 100\%.$$
**結果（1958）**：FORTRAN 迅速被接受——
**到 1958 年，超過一半的 IBM 704 程式用 FORTRAN 寫**。
$$\text{「程式設計師不需要懂機器」} \xrightarrow{\text{FORTRAN 1957}} \text{軟體工業的誕生}.$$

### Python：編譯器管線的簡化示範

```python
import re

# 1) 詞法分析：把字元流切成記號
def tokenize(expr):
    """詞法分析：數字、識別字、運算子"""
    token_spec = r'\d+\.?\d*|[A-Za-z_]\w*|[+\-*/()]'
    return re.findall(token_spec, expr)

# 2) 遞迴下降語法分析：expr → term → factor
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self):
        tok = self.peek()
        self.pos += 1
        return tok

    def expr(self):
        """expr := term (('+'|'-') term)*"""
        node = self.term()
        while self.peek() in ('+', '-'):
            op = self.consume()
            node = (op, node, self.term())
        return node

    def term(self):
        """term := factor (('*'|'/') factor)*"""
        node = self.factor()
        while self.peek() in ('*', '/'):
            op = self.consume()
            node = (op, node, self.factor())
        return node

    def factor(self):
        """factor := number | ident | '(' expr ')'"""
        tok = self.consume()
        if tok == '(':
            node = self.expr()
            self.consume()   # 吃掉 ')'
            return node
        return tok

# 3) 程式碼生成：從語法樹產生（虛擬）機器碼
def gen_code(node, temps=[], counter=[0]):
    """後序走訪：產生虛擬機器碼（LOAD/ADD/MUL/STORE）"""
    if isinstance(node, str):
        return f"LOAD {node}"
    op, left, right = node
    opname = {'+':'ADD', '-':'SUB', '*':'MUL', '/':'DIV'}[op]
    code_l = gen_code(left, temps, counter)
    code_r = gen_code(right, temps, counter)
    counter[0] += 1
    temp = f"T{counter[0]}"
    return f"{code_l}\nPUSH\ncode_r = {code_r}\n{opname}\nSTORE {temp}".replace("code_r = ", "")

# 簡化的程式碼生成（避免嵌套字串問題）
def gen_simple(node):
    """產生三地址碼（three-address code）"""
    lines = []
    def walk(n):
        if isinstance(n, str):
            return n
        op, l, r = n
        tl = walk(l)
        tr = walk(r)
        t = f"t{len(lines)}"
        opname = {'+':'ADD', '-':'SUB', '*':'MUL', '/':'DIV'}[op]
        lines.append(f"{opname} {tl}, {tr} -> {t}")
        return t
    walk(node)
    return lines

# 測試：X = (A + B) * C
expr = "(A + B) * C"
tokens = tokenize(expr)
print(f"原始運算式：{expr}")
print(f"詞法分析：{tokens}")
parser = Parser(tokens)
tree = parser.expr()
print(f"語法樹：{tree}")
code = gen_simple(tree)
print("\n產生的三地址碼：")
for line in code:
    print(f"  {line}")
print("\n→ 編譯器管線：詞法 → 語法 → 最佳化 → 生成（FORTRAN 1957 的架構）")

# 4) BNF 范式示範
print("\nBNF 范式（Backus Normal Form, 1959）：")
print("  <expr>  ::= <term> | <expr> + <term> | <expr> - <term>")
print("  <term>  ::= <factor> | <term> * <factor> | <term> / <factor>")
print("  <factor>::= number | ident | ( <expr> )")
print("  → 所有程式語言的規格書都用 BNF 寫（1959 的發明）")
```
輸出：
```
原始運算式：(A + B) * C
詞法分析：['(', 'A', '+', 'B', ')', '*', 'C']
語法樹：('*', ('+', 'A', 'B'), 'C')

產生的三地址碼：
  ADD A, B -> t0
  MUL t0, C -> t1

→ 編譯器管線：詞法 → 語法 → 最佳化 → 生成（FORTRAN 1957 的架構）

BNF 范式（Backus Normal Form, 1959）：
  <expr>  ::= <term> | <expr> + <term> | <expr> - <term>
  <term>  ::= <factor> | <term> * <factor> | <term> / <factor>
  <factor>::= number | ident | ( <expr> )
  → 所有程式語言的規格書都用 BNF 寫（1959 的發明）
```

## 結案 -- 後果與影響
- **軟體工業的誕生（1957）**：
  $$\boxed{\text{FORTRAN 是「軟體」成為工業的起點}}$$
  - 1958 年：IBM 704 的一半程式用 FORTRAN；
  - 1960 年代：FORTRAN 成為科學計算的標準（**至今仍在用**——
    天氣預報、流體力學、核模擬的超級電腦程式用 FORTRAN）；
  - **FORTRAN 的版本**：FORTRAN II（1958）、FORTRAN 66（標準化）、
    FORTRAN 77（結構化）、Fortran 90/95/2003/2018。
- **編譯器理論的誕生（1957–1960s）**：
  - **BNF（1959）**：語法的形式描述；
  - **ALGOL 60 報告（1960）**：**第一個用 BNF 寫的語言規格**——
    現代語言（Pascal、C、Java、Python）的祖先；
  - **編譯器的理論**：詞法分析的自動機（**Kleene**、**Rabin–Scott**）、
    語法分析的下推自動機——**形式語言理論（Chomsky 階層，1956）**的應用。
- **Backus 的轉向（1977）**：
  Backus 獲 1977 年圖靈獎，演講題為《程式設計能從 von Neumann 風格中解放嗎？》
  （*Can Programming Be Liberated from the von Neumann Style?*）——
  他**批評自己發明的命令式語言**，提倡**函數式程式設計**（FP）：
  $$\text{命令式（FORTRAN）} \xrightarrow{\text{Backus 的自我批判（1977）}} \text{函數式（Haskell、F\#）}.$$
  **函數式語言（Haskell 1990、Erlang 1986、Scala 2004）**的興起，
  以及**Python 的高階函數、JS 的 arrow function**——
  **Backus 1977 的批判影響了整個現代程式設計**。
- **Hopper 的先驅地位（1952）**：
  **Grace Hopper** 1952 年寫出 **A-0 編譯器**（第一個編譯器），
  1957 年的 **FLOW-MATIC** 是 COBOL（1959）的前身——
  **Hopper 沒得圖靈獎**（1991 年獲國家科技獎章），但她是「編譯器之母」。
- **現代編譯器（2000s–）**：
  - **LLVM（2003，Chris Lattner）**：模組化編譯器基礎設施——
    Swift、Rust、Julia 的後端；
  - **JIT 編譯（Java 1995、V8 2008）**：執行時編譯；
  - **MLIR（2019）**：機器學習的編譯器——**AI 時代的編譯器**。
  $$\text{FORTRAN（1957）} \xrightarrow{} \text{LLVM（2003）} \xrightarrow{} \text{AI 編譯器（2019）}.$$
- 歷史定位：**Backus 是「讓程式設計師解脫」的人**——
  $$\text{苦役（組合語言）} \xrightarrow{\text{FORTRAN 1957}} \text{創造（高階語言）} \xrightarrow{} \text{軟體工業（1960s）}.$$
  **現在的每一行程式碼，都是 FORTRAN 的後代**。

## 關鍵人物與文獻
- **J. Backus**：*The FORTRAN Automatic Coding System*（1957，與 Ziller 等）；BNF（1959）；1977 圖靈獎演講。
- **G. Hopper**：A-0 編譯器（1952）；FLOW-MATIC（1957）；COBOL 的前身。
- **J. McCarthy**：LISP（1958）——符號計算的路線（1971 圖靈獎）。
- **N. Chomsky**：形式語言階層（1956）——編譯器的理論基礎。
- **C. Lattner**：LLVM（2003）——現代編譯器基礎設施。
- 相關案件：`1958-麥卡錫LISP.md`、`1968-克努特演算法藝術.md`、`2006-艾倫編譯器最佳化.md`、`程式語言/1957-FORTRAN.md`。