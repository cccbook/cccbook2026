# 1960-ALGOL60與BNF

## 案件摘要
1960 年 1 月，巴黎鐵道車站飯店，六人小組用六天時間寫出了 ALGOL 60 報告——史上第一份「以形式規格定義語言」的文件。Backus 的 BNF 記法借自 Chomsky 的形式語言層級（1956），Naur 的編輯使報告精確如數學定理。遞迴、區塊結構、begin/end 第一次進入語言。ALGOL 60 商業上失敗，卻在學術上統治了四十年——所有現代語言都是它的後裔。

## 前因 -- 為什麼會有這個案子
- **FORTRAN 的孤立**：FORTRAN 是 IBM 專屬語言，歐洲學界（GAMM）與美國學界（ACM）都想有一門「跨機器、跨國界」的通用演算法語言。
- **1958 蘇黎世會議**：GAMM（歐洲，Rutishauser、Bauer 領軍）與 ACM（美國，Perlis、Samelson）合會，產出 **ALGOL 58**（原稱 IAL）——但 ALGOL 58 語意模糊、定義粗糙，各家的實作互不相容。
- **「機器碼描述語言」的死路**：ALGOL 58 及之前的語言多用「自然語言 + 機器碼範例」描述，導致同一行敘述在不同實作有不同結果——學界需要**形式化**的語言定義。
- **Chomsky 的理論（1956）**：MIT 語言學家 Noam Chomsky 發表形式語言理論，提出層級（Type 0-3）與產生式規則——原本是為了描述自然語言，卻意外成為程式語言的語法學基礎。

## 線索與推理 -- 數學式、程式、理論

### 案件的證物：Chomsky 層級
Chomsky 把語言按產生式規則的限制分為四層：

| 層級 | 產生式形式 | 語言類型 | 辨識機器 |
|---|---|---|---|
| Type 0 | $\alpha \to \beta$（任意） | 遞迴可枚舉 | 圖靈機 |
| Type 1 | $\alpha A \beta \to \alpha \gamma \beta$ | 上下文有關 | 線性有界自動機 |
| Type 2 | $A \to \gamma$ | 上下文無關 | 下推自動機 |
| Type 3 | $A \to aB$ 或 $A \to a$ | 正則語言 | 有限自動機 |

$$L \subseteq \Sigma^*, \quad L_{regular} \subsetneq L_{CFL} \subsetneq L_{CSL} \subsetneq L_{RE}$$

程式語言的語法大多是 **Type 2（上下文無關）**——這正是 BNF 能描述的層級。

### Backus 的 BNF：借來的記法
1959 年，Backus 在巴黎 UNESCO 會議上提出一種記法描述 ALGOL 的語法；Nauer 的報告中 Naur 將其精煉為 **Backus-Naur Form**：

```text
<expr>   ::= <term> | <expr> + <term> | <expr> - <term>
<term>   ::= <factor> | <term> * <factor> | <term> / <factor>
<factor> ::= <digit> | ( <expr> )
<digit>  ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
```

這五條產生式完整定義了「整數算術運算式」——語法第一次成為**數學對象**。

### 用 BNF 推導一個運算式
以 `(3+4)*5` 為例，從起始符號 `<expr>` 推導：

```text
<expr> ⇒ <term>                    （取 <expr> ::= <term>）
      ⇒ <term> * <factor>          （取 <term> ::= <term> * <factor>）
      ⇒ <factor> * <factor>
      ⇒ ( <expr> ) * <factor>
      ⇒ ( <expr> + <term> ) * <factor>
      ⇒ ( <term> + <term> ) * <factor>
      ⇒ ( <digit> + <digit> ) * <factor>
      ⇒ ( 3 + 4 ) * <digit>
      ⇒ ( 3 + 4 ) * 5              ✓ 推導成功
```

推導的意義：每一行的改寫都是一次語法規則的套用——**語法分析（parsing）就是這個推導的逆向**。編譯器的 parser 正是在搜尋這棵推導樹（parse tree）。用 Python 模擬：

```python
# BNF 產生式的 Python 模擬：遞迴下降解析 (3+4)*5
TOKENS = "( 3 + 4 ) * 5".split()
pos = 0

def peek():  return TOKENS[pos] if pos < len(TOKENS) else None
def eat(t):
    global pos
    assert peek() == t, f"語法錯誤：期待 {t}，得到 {peek()}"
    pos += 1

def expr():                                  # <expr> ::= <term> ((+|-) <term>)*
    v = term()
    while peek() in ('+', '-'):
        op = peek(); eat(op); v = v + term() if op == '+' else v - term()
    return v

def term():                                  # <term> ::= <factor> ((*|/) <factor>)*
    v = factor()
    while peek() in ('*', '/'):
        op = peek(); eat(op); v = v * factor() if op == '*' else v / factor()
    return v

def factor():                                # <factor> ::= <digit> | ( <expr> )
    if peek() == '(':
        eat('('); v = expr(); eat(')'); return v
    v = int(peek()); eat(peek()); return v

print(expr())   # 23 —— BNF 產生式直接成為遞迴下降 parser！
```

關鍵意義：每個非終端符號對應一個函數——**BNF 產生式幾乎可以機械地翻譯成 parser**，這就是「遞迴下降法」，至今仍是手寫 parser 的主流方法。

### 六人小組的巴黎會議
1960 年 1 月 11-16 日，巴黎，六人小組：**Alan Perlis**（美國，報告宣讀）、**Peter Naur**（丹麥，編輯）、**Friedrich Bauer**（德國）、**Klaus Samelson**（德國）、**John Backus**（美國，BNF）、**Joseph Wegstein**（美國）。Naur 的編輯使報告精確——每個語意問題都用「敘述 + 範例」界定，模糊處則以註腳標明。

### ALGOL 60 的語言革命
- **遞迴**：第一次正式允許程序呼叫自己——Dijkstra 的證明使遞迴在無堆疊的機器上成為可能。
- **區塊結構**：`begin ... end` 第一次進入語言，變數的**作用域**（scope）概念誕生：

$$\text{scope}(x) = \text{最小包含 } x \text{ 的宣告區塊}$$

- **call by name**：Jensen 的裝置（call by name）使參數以「未求值表達式」傳入——優雅但難實作，後來被 call by value 取代。

## 結案 -- 後果與影響
- **商業上的失敗**：IBM 拒絕放棄 FORTRAN，ALGOL 60 缺乏 I/O 標準（報告刻意不定義 I/O）、實作稀少——商業市場幾乎歸零。
- **學術上的統治**：ALGOL 60 Report 成為「以形式規格定義語言」的典範——此後每門語言都有一份形式報告（Pascal、C、Ada、Java……）。
- **BNF 的普及**：BNF 成為語法描述的標準記法，擴充版 EBNF 至今用於所有語言標準與 parser 生成器（yacc、ANTLR）。
- **Pascal 與 C 的血統**：Wirth（ALGOL 60 的實作者）設計 Pascal；Ritchie 的 C 繼承 BCPL→B→ALGOL 的區塊結構——所有現代語言的 `begin/end` 或 `{}` 都是 ALGOL 60 的後裔。
- **形式語意學的誕生**：ALGOL 60 的語意模糊（如 call by name）直接催生 1960-70 年代的形式語意學（Denotational Semantics，Scott/Strachey）。
- **圖靈獎的加冕**：Perlis（1966 首屆）、Nauer、Bauer、Dijkstra、Wilkinson、Wirth 等六人小組相關者共獲七座圖靈獎——史上「學術密度最高」的會議。

## 關鍵人物與文獻
- **John Backus**：BNF 記法，1977 年圖靈獎。
- **Peter Naur**：ALGOL 60 Report 編輯，2005 年圖靈獎。
- **Noam Chomsky**：形式語言層級（1956），語法學的理論基礎。
- 文獻：
  - P. Naur (ed.), "Report on the Algorithmic Language ALGOL 60," *Comm. ACM* 3(5), 299-314 (1960).
  - N. Chomsky, "Three Models for the Description of Language," *IRE Trans. Information Theory* 2(3), 113-124 (1956).
  - J. W. Backus, "The Syntax and Semantics of the Proposed International Algebraic Language," *Proc. UNESCO Conference* (1959).
  - A. J. Perlis, "The American Side of the Development of ALGOL," *SIGPLAN Notices* (1978).
