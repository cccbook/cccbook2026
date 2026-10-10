# 1975-Yacc與Lex

## 案件摘要
1975 年，Bell Labs 的 Stephen Johnson 發布 Yacc（Yet Another Compiler-Compiler），Mike Lesk 發布 Lex——隨 Unix 第六版一起出貨。這對搭檔幹的是同一件案子：**把 Knuth 與 DeRemer 躺了十年的 LR 理論，變成每個程式員都能用的工具**。語法規則進去，LALR 表與 parser 出來；正則表示式進去，掃描器出來。編譯器寫作從手工藝變成工程。此後無數語言——awk、SQL 前端、config 工具、乃至 GCC 的前身——都從這對搭檔的產線上出廠。

## 前因 -- 為什麼會有這個案子
- **手寫 parser 的痛**：1970 年代初，寫一個編譯器的語法分析器仍靠手工——遞迴下降要繞過左遞迴、運算子優先法只是經驗法則。每個新語言都要重蹈覆轍，錯誤百出、耗時數月。
- **理論躺在紙上**：Knuth 的 LR(k)（1965）理論完美但不實用（見 1965-LR解析）；DeRemer 的 SLR/LALR（1969/1971）把狀態數壓到可行，但**建表演算法本身**仍複雜，沒有人願意每次手算。
- **Johnson 的洞察**：與其讓每個人學會 LALR 建表，不如**讓機器算**——程式員只寫文法與語意動作，表與 parser 全部自動產生。
- **Unix 的土壤**：Bell Labs 的 Unix 提供管道、工具鏈文化；「程式產生程式」正是 Unix 哲學的極致體現。

## 線索與推理 -- 數學式、程式、理論

### Yacc：語法規則進去、LALR parser 出來
Yacc 的輸入是擴充 BNF 文法，每條產生式可附**語意動作**（semantic action）`{ ... }`，在規約（reduce）時執行。語意值的傳遞用合成棧：

$$\$\$ = \$1\ op\ \$3$$

其中 `$$` 是左部非終端的語意值，`$n` 是右部第 $n$ 個符號的語意值——**規約本身就是語意值的組合函數**：

$$\text{val}(A) = f(\text{val}(X_1), \dots, \text{val}(X_n)) \quad \text{當 } A \to X_1 \cdots X_n \text{ 規約}$$

Yacc 內部跑 DeRemer 式的 LALR(1) 建表：先建 LR(0) 項目集，再用**局部 lookahead 合併**消除 shift/reduce 衝突（衝突時 Yacc 預設偏 shift，並發出警告）。

### 計算機範例：Yacc 文法
經典的桌上型計算機文法——注意優先級與結合律如何用**文法層次**表達：

```
%token NUM
%left '+' '-'        /* 同層左結合，優先級低 */
%left '*' '/'        /* 同層左結合，優先級高 */

E : E '+' E { $$ = $1 + $3; }   /* $1=E左, $3=E右；規約時相加 */
  | E '-' E { $$ = $1 - $3; }
  | E '*' E { $$ = $1 * $3; }
  | '(' E ')' { $$ = $2; }      /* 括號：取中間的 E */
  | NUM      { $$ = $1; }
  ;
```

`E '+' E` 這條會產生 shift/reduce 衝突（左遞迴 + 二義），Yacc 用 `%left` 宣告的優先級解決：遇到 `*` 時 shift、遇到 `+` 時 reduce——**優先級宣告被編譯成表中的決定**。這正是 Knuth 當年認為「不可行」的東西，如今只需十行文法。

### Lex：正則表示式 → 掃描器
Lesk 的 Lex 用正則表示式描述詞彙（token）模式，自動產生掃描器：

```
[0-9]+      { yylval = atoi(yytext); return NUM; }   /* 整數 */
[ \t\n]     ;                                        /* 略過空白 */
[-+*/()]    { return yytext[0]; }                    /* 運算子 */
```

正則到自動機的理論：Thompson 建構法（1968）先把正則 $r$ 轉成 NFA $\epsilon$-NFA，再以 **subset construction** 轉成 DFA：

$$\text{NFA 狀態數} = \mathcal{O}(|r|), \qquad \text{DFA 狀態數} \le 2^{\mathcal{O}(|r|)} \text{（最壞），實務通常線性}$$

掃描器的策略：**最長匹配**（maximal munch）+ 遇到無法延伸時回退並發出最後一個接受態的 token。

### Python 模擬：regex → DFA 的 subset construction
以下把正則 `(a|b)*abb` 轉成 DFA——這是 Lex 內部引擎的最小版本：

```python
# 正則 (a|b)*abb 的 NFA（epsilon-free 簡化版，手工展開）
# 狀態以 frozenset 命名（subset construction 的產物）
nfa = {  # 每狀態 -> {字元 -> 目標狀態集}
    0: {'a': {0, 1}, 'b': {0}},
    1: {'b': {2}},
    2: {'b': {3}},
    3: {},
}
accept = {3}

def move(states, ch):
    out = set()
    for s in states:
        out |= nfa[s].get(ch, set())
    return frozenset(out)

def subset_construction():
    start = frozenset({0})
    dfa, work, done = {}, [start], set()
    while work:                      # 不動點迭代：每個新狀態集
        S = work.pop()
        if S in done: continue
        done.add(S)
        for ch in 'ab':
            T = move(S, ch)
            dfa[(S, ch)] = T
            if T and T not in done: work.append(T)
    return dfa, start

def run_dfa(dfa, start, s):
    cur = start
    for ch in s:
        cur = dfa.get((cur, ch), frozenset())
        if not cur: return False
    return bool(cur & accept)

dfa, start = subset_construction()
print(run_dfa(dfa, start, "aabb"))     # True  —— 以 abb 結尾 ✔
print(run_dfa(dfa, start, "abba"))     # False —— 不以 abb 結尾
```

`subset_construction` 把 NFA 的狀態**集合**當成一個 DFA 狀態，用不動點迭代窮舉可達集合——這正是 Lex 產生掃描器的核心演算法。DFA 一次讀一個字元、無回溯，線性時間完成詞法分析。

### Yacc + Lex 的產線
組合流程：

```
字元流 ──→ [Lex 產生的 DFA 掃描器] ──→ token 流 ──→ [Yacc 產生的 LALR parser] ──→ 語意樹/計算
                （正則 → DFA）                    （BNF → LALR 表）
```

掃描器與 parser 之間用 `yylval` 傳語意值——兩台自動機串成編譯器前端的整條產線。

## 結案 -- 後果與影響
- **編譯器寫作民主化**：寫一個新語言的前端從「數月的手工藝」變成「數天的工程」；1970 年代末大量新語言與 DSL（awk 1977、SQL 前端、配置工具）用 Yacc/Lex 建立。
- **GCC 的血統**：GCC 最初（1987）的 C parser 即以 Yacc 式 LALR 為基礎；GNU 的後繼者 Bison 至今仍是標準工具。
- **理論的勝利**：Knuth 1965 的理論 → DeRemer 1969/71 的簡化 → Johnson 1975 的工具化——**從理論到工具的完整傳播鏈**，成為計算機科學「數學改變工程」的教科書案例。
- **後繼工具**：ANTLR（遞迴下降 + LL(\*)）、Rust 的 logos、各語言的 parser combinator——皆循「聲明式規則 → 自動產生解析器」的路線；LLVM 的表格生成（TableGen）同屬此案精神。

## 關鍵人物與文獻
- **Stephen C. Johnson**（Bell Labs）：Yacc，1975；後參與 Portable C Compiler。
- **Mike Lesk**（Bell Labs）：Lex，1975；後參與 Unix 工具鏈（tbl 等）。
- 文獻：
  - S. C. Johnson, "Yacc: Yet Another Compiler-Compiler," *Unix Programmer's Manual*, 1975.
  - M. E. Lesk, "Lex: A Lexical Analyzer Generator," *Unix Programmer's Manual*, 1975.
  - K. Thompson, "Regular Expression Search Algorithm," *CACM* 11(6), 1968.
