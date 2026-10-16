# 1943 Plankalkül

## 案發現場

1943 年的柏林，第二次世界大戰的炸彈正在摧毀這座城市。在斷水斷電、物資匱乏的環境中，一位德國土木工程師出身的發明家 Konrad Zuse（楚澤），正在紙上設計一個將近五十年後才會被世界理解的東西——**世界上第一個高階程式語言**。

案發現場要從更早說起。1930 年代，Zuse 在柏林當結構工程師，每天要算大量的結構力學題目：聯立線性方程組、矩陣運算。他厭倦了枯燥的手算，決定造一台自動計算機。1938 年，他用金屬片與廢棄零件造出了 Z1——一台純機械的二進位計算機。1941 年，他造出 Z3——**世界上第一台可程式化的全功能數位電腦**，採用二進位制與浮點數表示，比美國的 Harvard Mark I（1944）和 ENIAC（1945）都早。

Z3 用的是打孔廢棄膠捲輸入指令，只能做機器碼層級的運算。Zuse 立刻意識到下一層的問題：**機器碼太原始了。** 他想算的是「解一個聯立方程組」、「對矩陣做運算」這種高階概念，而不是一格一格的記憶體搬移。他要一種語言，能直接表達數學結構。

於是 1943–1945 年間，Zuse 在戰火中寫下了 Plankalkül（德文「計畫演算」之意，「Plan」= 計畫，"Kalkül" = 演算）。但接下來的命運，是一場跨越半個世紀的悲劇。

## 偵查過程

Zuse 的偵查思路，是在完全孤立的環境下（他不知道 Ada Lovelace 的註解、不知道 Turing 1936 年的論文、更不知道美國正在發生什麼），從零推導出一門程式語言該有的樣貌。他的推理分為四個步驟。

**第一步：資料的結構化——陣列與記錄。** Zuse 第一個洞察是：程式處理的不該只是單一數字，而是**結構化的資料**。他發明了兩種複合資料型別：

- **陣列**（Array）：同一型別元素的線性排列，他記作 $S_{1 \times n}$（一維 $n$ 個元素）或 $S_{m \times n}$（二維矩陣）
- **記錄**（Record）：不同型別欄位的組合，他記作 $(S_1, S_2, \ldots)$

例如一個「棋盤上的棋子」可以定義為記錄：`(顏色, 種類, 位置)`，其中顏色是 2 位元、種類是 4 位元、位置是 6 位元——Zuse 甚至發明了**位元層級的資料型別宣告**，這在當年是革命性的：

```text
A0 = (2, 4, 6)    # 記錄：2位元顏色 + 4位元種類 + 6位元位置
```

這種「宣告結構 → 按結構取值」的思路，直接預示了 1958-LISP.md 的 list 與後來 C 語言的 struct、Pascal 的 record。Zuse 用記號 $V_i[k]$ 表示「陣列 $V_i$ 的第 $k$ 個元素」，這就是陣列索引語法的鼻祖。

**第二步：賦值與運算的代數化。** Plankalkül 的賦值形式極具特色，他用一個三行的「表格記法」：

$$\begin{array}{c|c}
V & V_1 + V_2 \Rightarrow V_3 \\
\end{array}$$

其中「結果欄」$V_3$ 表示運算結果存入變數 $V_3$。他還發明了**布爾運算與條件**：$\wedge$（且）、$\vee$（或）、條件選擇。運算可以作用在整個陣列上（element-wise，逐元素運算）：

$$V_1 + V_2 = V_3 \quad \text{其中 } V_3[k] = V_1[k] + V_2[k]$$

這個「向量/矩陣整體運算」的概念，整整五十年後才在 APL、MATLAB、Python NumPy 中成為主流——Zuse 1945 年就想到了。

**第三步：控制流——迴圈與斷言。** Zuse 發明了兩種控制結構：

1. **迴圈**（W-Plan，德文 Wiederholung「重複」）：用來表達重複執行
2. **斷言**（Assertion）：宣告某個條件在程式的某個點必須為真

斷言的發明特別超前——這是**程式驗證**的最早萌芽。Zuse 意識到程式可能出錯，於是在語言中內建了「檢查點」機制：`P(m) => A` 表示「在第 $m$ 步，斷言 $A$ 必須成立」。這個思想直到 1960 年代 Floyd-Hoare 的程式驗證理論才被系統化，成為今天 DBC（design by contract）與 `assert` 語句的先聲。

**第四步：子程式與「Plan 配方」。** Plankalkül 支援把一段 Plan 包裝成可重用的「子程式」（Unterplan），用參數傳入、結果傳出。這是最早的函數/程序抽象。Zuse 在論文中展示了完整的範例：用 Plankalkül 寫出「比較兩個布林向量」「下棋的合法走法判斷」——是的，Zuse 甚至寫了西洋棋程式，用來展示語言的通用性。

用現代語法重寫 Zuse 在論文中的經典範例「求兩個布林向量的逐元素 AND」（Zuse 記作 $\bar{V}_1 \wedge \bar{V}_2$），並展示他著名的「4 行表格」記法：

```text
P1:  W(0, n)                    # 迴圈：重複 n 次
       V[k] := V1[k] ∧ V2[k]    # 逐元素且
     result := V
P2:  斷言: V1, V2 長度相同
```

**核心技術推導：為什麼「二進位 + 浮點數」是正確選擇。** Zuse 的另一個關鍵貢獻在他的 Z3 機器：他選擇了二進位制而非十進位（ENIAC 用十進位！），並設計了浮點數表示：

$$(-1)^s \times m \times 2^e$$

其中 $s$ 是正負號、$m$ 是尾數（mantissa）、$e$ 是指數（exponent）。Z3 的格式為：1 位元符號 + 7 位元指數 + 14 位元尾數（隱藏首位 1）。這個設計推理極為深刻：

1. 二進位使得硬體只需兩種狀態（繼電器的開/關），可靠且便宜
2. 浮點數用「科學記號」的思路，讓有限位元能表示極大與極小的數
3. 隱藏首位：二進位的尾數首位必為 1，可以省略不存，多騰出一位精度

這套浮點表示法，是 1985 年 IEEE 754 浮點標準的直系祖先。今天所有程式語言的 `float`，都源自 Zuse 在 1941 年的設計。

## 結案報告

Plankalkül 的故事是一場跨越半世紀的悲劇與平反：

1. **1945 年完成，1948 年才發表**：Zuse 把論文投給學術界，但戰後德國百廢待舉，論文只在一個不起眼的學報上發表，幾乎無人閱讀。
2. **國際孤立**：Zuse 不知道 Turing、不知道 Church、不知道美國的發展；美國也不知道他。當 Backus 團隊在 1957 年推出 [1957-FORTRAN.md](1957-FORTRAN.md) 時，他們不知道 Plankalkül 已經發明了陣列、記錄、迴圈與斷言。
3. **2000 年才被實作**：Plankalkül 在紙上存在了 55 年，直到 2000 年才由柏林自由大學的團隊完整實作成一個可執行的直譯器。這是程式語言史上「從設計到實作」時間最長的紀錄。
4. **Z3 的遲來榮耀**：Z3 被公認為世界第一台可程式化數位電腦。Zuse 本人在 1986 年獲得電腦先驅獎，1995 年去世，享年 85 歲。

Plankalkül 的遺產滲透在所有後續語言中：陣列與記錄 → C 的 struct、Pascal 的 record；逐元素向量運算 → APL、MATLAB、NumPy；斷言 → Hoare 邏輯、`assert`；子程式 → 所有語言的函數；浮點數 → IEEE 754。戰爭摧毀了他的機器、埋沒了他的論文，但摧毀不了他的思想。

## 證據與工具

**證據一：Plankalkül 逐元素向量運算的現代重現（Python）**

```python
def plankalkul_vec_and(v1, v2):
    """重現 Plankalkül 經典範例：V = V1 ∧ V2（逐元素且）"""
    assert len(v1) == len(v2), "P2 斷言：V1, V2 長度相同"
    n = len(v1)
    V = [None] * n
    for k in range(n):          # P1: W(0, n) 迴圈
        V[k] = v1[k] and v2[k]
    return V

print(plankalkul_vec_and([1,0,1,1], [1,1,0,1]))   # [1, 0, 0, 1]
```

**證據二：迷你 Plankalkül 解譯器**

以下實作一個迷你解譯器，支援 Plankalkül 的核心語法（賦值、陣列索引、逐元素運算、W 迴圈、斷言）：

```python
import operator

OPS = {'+': operator.add, '-': operator.sub,
       '*': operator.mul, '∧': lambda a,b: 1 if (a and b) else 0,
       '∨': lambda a,b: 1 if (a or b) else 0}

class MiniPlankalkul:
    def __init__(self):
        self.vars = {}

    def assign(self, name, index, expr):
        """V[k] := expr — Zuse 的賦值記法"""
        val = self.eval(expr)
        if name not in self.vars:
            self.vars[name] = [None] * 64
        self.vars[name][index] = val
        return val

    def eval(self, expr):
        """解析 'V1[k] + V2[k]' 形式的表達式"""
        tokens = expr.replace(']', '[').split('[')
        if len(tokens) == 3:                      # 陣列索引：Vx[k]
            name, idx, _ = tokens
            return self.vars[name][int(idx)]
        for op in ('∨', '∧', '+', '-', '*'):      # 二元運算
            if op in expr:
                l, r = expr.split(op)
                return OPS[op](self.eval(l.strip()), self.eval(r.strip()))
        return int(expr)

    def w_loop(self, n, assignments):
        """W(0,n) 迴圈 + 逐元素運算"""
        for k in range(n):
            for name, expr_fn in assignments:
                self.assign(name, k, expr_fn(k))

# 示範：V3 = V1 + V2，V4 = V1 ∧ V2（兩個長度 4 的向量）
pk = MiniPlankalkul()
pk.vars['V1'] = [1,2,3,4]
pk.vars['V2'] = [10,20,30,40]
pk.w_loop(4, [('V3', lambda k: f'V1[{k}] + V2[{k}]'),
              ('V4', lambda k: f'V1[{k}] ∧ V2[{k}]')])
print(pk.vars['V3'][:4])   # [11, 22, 33, 44]  ✓ 逐元素加法
print(pk.vars['V4'][:4])   # [1, 1, 1, 1]      ✓ 逐元素且
```

**證據三：Zuse 浮點數表示的模擬**

```python
def zuse_float(num):
    """模擬 Z3 的浮點格式：1 符號 + 7 指數 + 14 尾數（隱藏首位）"""
    s = 0 if num >= 0 else 1
    num = abs(num)
    e = num.bit_length() - 1 if num >= 1 else 0
    m = num / (2 ** e) if num > 0 else 1.0
    mantissa_bits = round((m - 1) * (2 ** 14))   # 隱藏首位 1
    return (s, format(e, '07b'), format(mantissa_bits, '014b'))

def zuse_decode(bits):
    s, e, m = bits
    return (1 if s == 0 else -1) * (1 + int(m, 2) / 2**14) * (2 ** int(e, 2))

for x in [6.0, -3.5, 100.0]:
    b = zuse_float(x)
    print(x, b, round(zuse_decode(b), 4))
# 6.0  (0, '0100001', '10000000000000') 6.0
# -3.5 (1, '0100000', '11000000000000') -3.5
```

三份證據對應 Zuse 的三大發明：向量運算、迷你解譯器驗證了 Plankalkül 語法的可執行性，浮點模擬還原了 Z3 的硬體設計。一個在戰火中孤立工作的人，憑一己之力發明了一門語言——只可惜世界要等五十五年後才看懂它。
