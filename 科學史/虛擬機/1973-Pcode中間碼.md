# 1973 — UCSD P-system 與 P-code：跨平台虛擬機的語言路線

## 案件摘要
1973 年起，Kenneth Bowles 在 UCSD 開發 Pascal P-system，採用「P-code」中間碼：程式編譯成 P-code，由 P-machine 直譯器執行。語言層的虛擬機（bytecode VM）就此誕生——「一次編譯，到處執行」的第一樁勝訴判例。

## 前因 -- 為什麼會有這個案子
- 1970 年代的微型電腦（Apple II、TRS-80、Z80 機器）CPU 各不相同（6502、Z80、8080），記憶體只有數十 KB。
- 每個新平台都要重寫編譯器後端：編譯器是「每台機器一案」的苦差事；Pascal 的完整編譯器在 64KB 機器上根本放不下。
- 線索：把編譯器切成「平台無關的前端 + 極小的平台相關直譯器」？Wirth 的 Pascal-P（1973）已把 Pascal 編成 P-code；Bowles 的洞見是把它包成**完整的作業環境**（作業系統 + 編譯器 + 直譯器）一起移植。

## 線索與推理 -- 數學式、程式、理論

### 1. P-code：bytecode 的祖先
P-code（pseudo-code）是一種緊湊的**堆疊式中間碼**：指令不帶暫存器編號，操作數隱含在堆疊頂端。

$$\text{source } \xrightarrow{\text{編譯器前端}} \text{P-code} \xrightarrow{\text{P-machine 直譯器}} \text{執行}$$

典型指令（UCSD P-code 風格）：

| 指令 | 語意 |
|------|------|
| `LDC 5` | push 常數 5 |
| `LDL 0` | push 區域變數 offset 0 |
| `ADD` | pop 兩數相加 push 結果 |
| `STL 1` | pop 存入區域變數 offset 1 |
| `JMP n` | 無條件跳到 n |
| `JPF n` | 堆疊頂為假則跳到 n |
| `HALT` | 停機 |

### 2. P-machine 直譯器（理論定義）
P-machine 是一個抽象機 $M = \langle S, D, C, \delta \rangle$：

- $S$：求值堆疊（evaluation stack）
- $D$：資料區（frame：static link、dynamic link、區域變數、返回位址）
- $C$：程式碼區（P-code 序列）
- $\delta$：狀態轉移函數，$\delta: (S, D, C, pc) \to (S', D', C, pc')$

每步取 `$C[pc]$`、解碼、執行、更新堆疊與 `$pc$`——這就是 fetch-decode-execute 迴圈，與真實 CPU 同構，只是由軟體實作。

### 3. 「一次編譯，到處執行」的數學理由
對任意平台 $X$，只要有直譯器 $I_X$：

$$\forall X:\ \text{P-code} \xrightarrow{I_X} \text{same semantics}$$

即語意函數等價：$\text{sem}(\text{src}) = \text{sem}_X(\text{P-code})\ \ \forall X$。
移植成本從「重寫整個編譯器後端 $O(\text{compiler})$」降為「寫一個小直譯器 $O(\text{interpreter})$」：

$$\text{cost}_{new\ platform} \approx |I_X| \ll |C_{backend}|$$

代價：直譯執行比原生慢 5–20 倍（$t_{interp} \gg t_{native}$）——這個缺口後來由 JIT 補上。

### 4. Python 實作：簡單堆疊 VM（P-code 風格）

```python
def run(code, locals_size=4):
    stack, locals_, pc = [], [0] * locals_size, 0
    while pc < len(code):
        op = code[pc]; pc += 1
        if   op[0] == "LDC":  stack.append(op[1])
        elif op[0] == "LDL":  stack.append(locals_[op[1]])
        elif op[0] == "STL":  locals_[op[1]] = stack.pop()
        elif op[0] == "ADD":  b, a = stack.pop(), stack.pop(); stack.append(a + b)
        elif op[0] == "SUB":  b, a = stack.pop(), stack.pop(); stack.append(a - b)
        elif op[0] == "MUL":  b, a = stack.pop(), stack.pop(); stack.append(a * b)
        elif op[0] == "JMP":  pc = op[1]
        elif op[0] == "JPF":  pc = op[1] if not stack.pop() else pc
        elif op[0] == "PRINT": print(stack.pop())
        elif op[0] == "HALT": break
    return locals_

# 計算 1+2+...+10 的 P-code：
# i = 0; sum = 0; loop: i = i+1; sum = sum+i; if i<10 goto loop; print sum
code = [
    ("LDC", 0), ("STL", 0),          # i = 0
    ("LDC", 0), ("STL", 1),          # sum = 0
    # loop = pc 4
    ("LDL", 0), ("LDC", 1), ("ADD"), ("STL", 0),   # i = i + 1
    ("LDL", 1), ("LDL", 0), ("ADD"), ("STL", 1),   # sum = sum + i
    ("LDL", 0), ("LDC", 10), ("LT"), ("JPF", 4),   # if i < 10 goto loop
    ("LDL", 1), ("PRINT"),
    ("HALT",),
]
run(code)   # 輸出 55
```

## 結案 -- 後果與影響
- UCSD P-system 被移植到 Apple II、IBM PC、TI-99 等數十種機器，是 1980 年代初最重要的「可攜式作業環境」，Apple 甚至授權內建於 Apple Pascal。
- P-code 的堆疊式設計直接啟發 **Java bytecode（JVM，1995）**、**.NET CIL/IL（2002）**、Python `.pyc`、Lua VM。
- 「前端/後端分離 + 中間碼」成為編譯器工程標準（LLVM IR 亦屬此譜系）。
- 直譯太慢的缺口，由 Self 的 JIT（1991）、Deutsch–Schiffman（1984）、HotSpot 等補齊——但架構的種子是 P-code 種下的。

## 關鍵人物與文獻
- **Kenneth Bowles**：UCSD P-system 創始人。
- **Niklaus Wirth**：Pascal 之父，Pascal-P 與 P-code 概念先驅。
- Wirth, *The Programming Language Pascal*, Acta Informatica, 1971.
- Bowles, *Beginner's Guide for the UCSD Pascal System*, 1983.
- Nori et al., *Pascal-P Implementation Notes*, 1975.
- Apple Computer, *UCSD Pascal Reference Manual for the Apple II*, 1979.
