# 1970-Pascal與自舉

## 案件摘要
1960 年代末，Niklaus Wirth 在 ALGOL 68 的委員會裡被二層文法（two-level grammar）折磨得筋疲力盡，憤而退出、自立門戶。他要辦的案子很明確：造一個「教學語言 + 可靠編譯器」。1970 年 Pascal 設計完成、1971 年發表，而真正的絕招出現在 1973–1975：**P-code**——把 Pascal 編譯器編譯成一台虛擬堆疊機的中間碼，任何機器只要寫幾百行的直譯器，就能自舉整個編譯器。Pascal 由此傳遍全球大學。本案的核心線索是一個古老而迷人的技巧：**用語言 L 來寫 L 自己的編譯器**。

## 前因 -- 為什麼會有這個案子
- **ALGOL 68 的挫敗**：ALGOL 68 的定義使用 van Wijngaarden 的**二層文法**（超語言描述文法，表達力極強但難以閱讀與實作）。Wirth 與 Dijkstra 等人在 1968 年發表少數派報告反對；ALGOL 68 通過後，Wirth 退出委員會。
- **Euler 與 ALGOL W 的教訓**：Wirth 早年設計 Euler、後與 Hoare 合作 ALGOL W，深知「語言定義清楚 + 編譯器單趟完成」的重要性。
- **教學的需求**：大學需要一個能在一學期內教完、且學生能親手寫出編譯器的語言。當時 FORTRAN 太骯髒、ALGOL 60 缺資料結構、ALGOL 68 太複雜。
- **移植的痛**：每台新機器（CDC 6000、IBM 360、PDP-11……）都要重寫整個編譯器——有沒有辦法只重寫一小部分？

## 線索與推理 -- 數學式、程式、理論

### Pascal 的設計決策：單趟編譯
Pascal（1970 完成、1971 "The Programming Language Pascal" 發表於 *Acta Informatica*）的關鍵取捨：

1. **單趟（one-pass）編譯**：語法設計成可以「讀到哪、編到哪」——變數與型別必須**先宣告後使用**，程序必須先宣告才能呼叫（或向前宣告 `forward`）。
2. 區塊結構、遞迴、強型別、使用者自定資料結構（record、set、file）。
3. 編譯器直接產生**堆疊機碼**，不做複雜最佳化——可靠性與正確性優先。

單趟編譯的代價可用「先宣告後使用」條件刻畫：若文法 $G$ 滿足每個標識符在使用點之前已進入符號表，則解析時可線性時間完成語意檢查：
$$\text{use}(x) \Rightarrow x \in \text{symtab}(\text{scope}_{\text{use}(x)})$$

### 自舉：用 L 寫 L 的編譯器
自舉（bootstrapping）的核心問題：編譯器 $C_L$ 把語言 $L$ 編譯到機器 $M$。**用 $L$ 自己寫 $C_L$**，之後：

$$C_L \xrightarrow{\ C_{L0}\ } M \text{ 碼的 } C_L$$

先用已有編譯器 $C_{L0}$ 編譯新版（用 $L$ 寫的）$C_L$，得到能跑的 $C_L$；之後 $C_L$ 就能編譯自己，甚至改進自己：

$$C_L^{new} \xrightarrow{\ C_L^{old}\ } C_L^{new} \quad (\text{編譯器自我改進的飛輪})$$

### P-code 與 T-diagram：移植的祕密
1973 年 ETH Zürich 的 P-code（Pascal-P 系統，1975 廣泛流傳）把整個編譯器編到一台**虛擬堆疊機** P 上。移植到新機器 M 只需兩步：

| 步驟 | 工作 | 大小 |
|---|---|---|
| 1 | 用 M 的組合語言寫 **P 直譯器** | 幾百行 |
| 2 | P 直譯器跑「P 碼版 Pascal 編譯器」，重新產生 M 碼編譯器 | 不用改 |

T-diagram（文字版）記號：編譯器 `S→T` 跑在機器 `I` 上寫成三層。組合規則——兩個編譯器串接時中間語言必須相容：

```
 ┌─────────┐          ┌─────────┐
 │ C: P → M │  跑在    │ C: P → P │   ⇒   ┌─────────┐
 │ (M 碼)   │  P 碼機  │ (M 碼)   │       │ C: P → M │ (M 碼)
 └─────────┘          └─────────┘       └─────────┘
   「用 P 碼機 執行 M 碼編譯器」＝ 一台新的 M 碼編譯器
```

這個組合律就是 P-code 傳教的數學基礎：**移植成本從「重寫整個編譯器（數萬行）」降到「寫直譯器（數百行）」**，比例懸殊：

$$\frac{\text{直譯器}}{\text{編譯器}} \approx \frac{10^2}{10^4} = 1\%$$

### Python 模擬：P-code 堆疊機
P-code 的核心指令：`ldc`（載入常數）、`lod`（載入變數）、`sto`（存回變數）、`add`/`mul`（堆疊頂運算）。以下模擬一台迷你堆疊機，執行運算式 `(a + b) * 2` 的 P-code：

```python
# 迷你 P-code 堆疊機（模擬 Pascal-P 的直譯器核心）
def p_machine(code, vars_):
    stack = []            # 運算堆疊
    for op, *args in code:
        if op == 'ldc':   # 載入常數
            stack.append(args[0])
        elif op == 'lod': # 載入變數（args[0] = 位址）
            stack.append(vars_[args[0]])
        elif op == 'sto': # 彈出、存入變數
            vars_[args[0]] = stack.pop()
        elif op == 'add': # 堆疊頂兩數相加
            b, a = stack.pop(), stack.pop(); stack.append(a + b)
        elif op == 'mul':
            b, a = stack.pop(), stack.pop(); stack.append(a * b)
        elif op == 'fjp': # 條件為假跳躍（while/if 的基礎）
            if not stack.pop(): 
                args[0]  # 跳到目標（此例省略）
    return stack, vars_

# (a + b) * 2 的 P-code 序列
code = [('lod', 0), ('lod', 1), ('add',), ('ldc', 2), ('mul',)]
result, vars_ = p_machine(code, {0: 3, 1: 4})
print(result)   # 14 —— (3+4)*2
```

堆疊機的妙處：**指令不需要位址欄位描述運算元位置**（運算元永遠在堆疊頂），因此 P-code 緊�、直譯器極簡——這正是「任何機器都能快速自舉」的原因。堆疊機的求值就是後序走訪運算式樹：

$$\text{eval}(E_1\ op\ E_2) = \text{eval}(E_1)\ \text{eval}(E_2)\ op$$

### Pascal 的自舉實錄
Wirth 團隊的順序：先在 CDC 6000 上寫 Pascal 編譯器 → 把它改寫成**用 Pascal 寫**、目標是 P 碼 → 用舊編譯器自舉出新編譯器 → 發布「P 碼版編譯器 + 原始碼」。加州 UCSD 由此發展出 UCSD Pascal 與 P-system（1978），甚至成為早期 Apple II 的作業系統之一。

## 結案 -- 後果與影響
- **Pascal 傳遍大學**：1970–80 年代 Pascal 成為全球計算機科學系的標準教學語言；1983 年 ISO 標準化。
- **自舉技術成為標準做法**：C 編譯器（GCC）、Rust、Go 都用「前版編譯器編譯後版」的自舉流程；中間碼 + 虛擬機的路線直接預告了 Java byte-code 與 LLVM IR。
- **T-diagram 成為教材標準**：編譯器課程自此用 T 圖講授移植與交叉編譯。
- **教學遺產**：Wirth 的「演算法 + 資料結構 = 程式」（1976）延續同一精神；Pascal 的強型別影響了 Ada、Modula-2 與型別系統的後續發展。

## 關鍵人物與文獻
- **Niklaus Wirth**（ETH Zürich）：1971 "The Programming Language Pascal," *Acta Informatica* 1, 35–63；1984 圖靈獎。
- **P-code / Pascal-P**：Wirth 與團隊，1973–1975；UCSD Pascal（Kenneth Bowles, 1978）。
- 文獻：
  - N. Wirth, *Algorithms + Data Structures = Programs*, Prentice-Hall, 1976.
  - A. M. Addyman et al., "A Draft Description of Pascal," *SIGPLAN Notices*, 1980.
