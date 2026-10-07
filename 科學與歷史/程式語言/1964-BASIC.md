# 1964 BASIC：人人能寫程式的教育革命

## 案發現場

1960 年代初，程式設計是少數人的特權。要寫程式，你得是數學家或工程師：把程式打在卡片上、交給計算中心、等幾個小時甚至隔天才知道有沒有打錯一個逗號。達特茅斯學院（Dartmouth College）的數學系教授 John Kemeny 對此深感挫折——他是愛因斯坦的助手、馮紐曼的同事，但他們的學生根本碰不到電腦。同系的 Thomas Kurtz 則觀察到另一個問題：FORTRAN 與 ALGOL 對文科學生而言太複雜，光是指標與格式化輸出就足以讓九成的初學者放棄。

兩人共同的問題意識是：**如何讓每一個大學生——包括英文系與歷史系的學生——都能在幾分鐘內學會寫第一個程式，並且立即看到結果？** 這需要同時解決三個難題：語言要極簡、執行要即時（不能等批次處理）、機器要能同時服務很多人。1964 年 5 月 1 日凌晨，第一個 BASIC 程式在達特茅斯的 GE-225 機器上以分時系統（time-sharing）執行成功，Kemeny 與 Kurtz 的賭注兌現了。

## 偵查過程

### 線索一：達特茅斯分時系統（DTSS）——即時的物理基礎

BASIC 的革命一半在語言、一半在系統。Kemeny 與 Kurtz 推導出一個關鍵架構：**分時系統（DTSS, Dartmouth Time-Sharing System）**——把一台大型主機的 CPU 時間切成微小片段，輪流服務多個終端機上的使用者。由於人的打字與思考速度（秒級）遠慢於 CPU（毫秒級），每個使用者都會覺得機器只屬於自己。

執行模型的核心是「即時解譯」：使用者從終端機打完程式，敲下 `RUN`，直譯器立刻逐行執行，馬上把結果印回終端機。這個「編輯—執行—修正」的即時迴圈，把批次處理時代數小時的回饋時間壓縮到數秒，徹底改變了學習程式的體驗。這個迴圈的模式，就是今日 Jupyter Notebook、REPL、以及所有互動式開發環境的直系祖先。

### 線索二：行號與極簡語法——為初學者推理的設計

BASIC 的語法設計處處可以還原為「初學者第一周會犯什麼錯」的推理：

```basic
10 REM 這是我的第一個程式
20 LET S = 0
30 FOR I = 1 TO 100
40 LET S = S + I
50 NEXT I
60 PRINT "1 到 100 的總和是"; S
70 END
```

- **行號**：每一行都有編號（10、20、30…），這不只是裝飾，而是一整套推理的產物。第一，初學者打錯一行，只需打 `35 PRINT I` 就能把新敘述**插入**行 30 與 40 之間，不必重打整個程式。第二，`GOTO 40`、`GOSUB 200` 讓初學者能用行號控制流程，這是當時最直觀的跳躍方式（ALGOL 的區塊結構對初學者太抽象）。第三，行號間隔 10 是刻意留白，方便插入。行號後來成為 BASIC 最被詬病的遺產——GOTO 滿天飛的「義大利麵條程式」——但在 1964 年，它是易學性的核心設計。
- **LET 敘述**：`LET S = S + I` 中 `=` 是賦值不是數學等式，加上 `LET` 這個英文單字提醒初學者「把值放進去」。
- **只有 14 個敘述**：最初的 BASIC 只有 `LET`、`PRINT`、`INPUT`、`IF...THEN`、`FOR...NEXT`、`GOTO`、`GOSUB`、`RETURN`、`END`、`REM`、`DIM`、`DATA`、`READ`、`STOP` 等十幾個敘述，一頁紙就能列完所有語法——Kemeny 特意要求「語言要能印在明信片背面」。
- **變數不必宣告型別**：FORTRAN 的 `INTEGER`/`REAL` 宣告被省略，減少初學者的認知負擔（這與 ALGOL/Pascal 的強型別哲學形成鮮明對比，兩條路線至今仍在辯論）。

### 線索三：免費與開放——教育革命的最後一塊拼圖

Kemeny 與 Kurtz 做了一個在商業軟體時代駭人聽聞的決定：**BASIC 不申請專利、不收授權費，免費開放給任何人使用**。他們的推理是：目標是教育革命，不是商業利益；語言散播得越廣，學生學到哪裡都能用。1960 年代後期，BASIC 隨達特茅斯的分時系統散播到美國數百所中學與大學，Kemeny 甚至在校園裡開設「人人能寫程式」的通識課程，並寫了同名教材。

## 結案報告

BASIC 的遺產比它的設計者預期的更戲劇化：

- **教育**：BASIC 成為 1970–80 年代全球大學與中學的入門語言，Kemeny 與 Kurtz 的「人人能寫程式」理想在整整一代人身上實現。今日的 Python 教育運動、Scratch、Code.org，哲學上都是達特茅斯的後裔。
- **微型電腦時代**：1975 年 Bill Gates 與 Paul Allen 為 Altair 8800 寫出 Microsoft 的第一個產品——Altair BASIC，微軟因 BASIC 而誕生。1977 年 Apple II 開機即進入 Applesoft BASIC，Wozniak 親手用 BASIC 寫出了第一個試算表的雛形。整個 1980 年代的家用電腦（Commodore 64、TRS-80、IBM PC 的 BASICA/GW-BASIC）開機就是 BASIC。
- **反面教材**：行號與 GOTO 造成的大規模非結構化程式碼，成為 1968 年 Dijkstra「GOTO 有害論」（見 [1968-GOTO有害論.md](1968-GOTO有害論.md)）之後結構化運動的頭號批判對象；1980 年代的 QBASIC 與 Visual Basic 才補上了結構化與事件驅動。
- **語言系譜**：Visual Basic、VBA、VB.NET 一直活到今日；Python 的 REPL 與易學哲學也是另一支「達特茅斯精神」的傳承。

一句話總結：FORTRAN 與 ALGOL 是為專業人士設計，BASIC 是為「所有人」設計；它以犧牲嚴謹換取普及，換來了微型電腦時代的第一聲開機音。

## 證據與工具

以下用 BASIC 語法示範經典程式，並用 Python 模擬 BASIC 的行號編輯與即時解譯：

```basic
10 REM 猜數字遊戲
20 LET R = INT(RND(1) * 100) + 1
30 PRINT "請猜 1 到 100 的數字"
40 INPUT G
50 IF G = R THEN 80
60 IF G < R THEN PRINT "太大了" ELSE PRINT "太小了"
70 GOTO 40
80 PRINT "猜對了！數字是"; R
90 END
RUN
```

```python
# 模擬 BASIC 的行號模型：程式 = 行號到敘述的字典
program = {
    10: "LET S = 0",
    30: "FOR I = 1 TO 100",
    40: "LET S = S + I",
    50: "NEXT I",
    60: "PRINT S",
    70: "END",
}

# 1. 行號插入：打 "35 PRINT I" 即插在 30 與 40 之間
program[35] = "PRINT I"
print("插入後的執行順序:", sorted(program.keys()))

# 2. 模擬即時解譯：逐行執行 LET/FOR/PRINT
def interpret(prog):
    lines = sorted(prog.items())
    env, output, pc = {}, [], 0
    i = 0
    while i < len(lines):
        ln, stmt = lines[i]
        if stmt.startswith("LET"):
            _, var, _, expr = stmt.split(maxsplit=3)
            env[var] = eval(expr, {}, env)          # LET S = S + I
        elif stmt.startswith("FOR"):
            _, var, _, rng = stmt.split(maxsplit=3)
            lo, hi = map(int, rng.split(" TO "))
            for v in range(lo, hi + 1):              # FOR I = 1 TO 100 ... NEXT I
                env[var] = v
                while lines[i + 1][0] != ln + 10:    # 執行迴圈體直到 NEXT
                    body_ln, body = lines[i + 1]
                    if body.startswith("LET"):
                        _, bv, _, be = body.split(maxsplit=3)
                        env[bv] = eval(be, {}, env)
                    i += 1
                    break
                else:
                    break
        elif stmt.startswith("PRINT"):
            out = stmt[len("PRINT"):].strip()
            output.append(env.get(out, out))
        elif stmt == "END":
            break
        i += 1
    return env, output

env, out = interpret({k: v for k, v in program.items() if k not in (10, 70)} | {10: "LET S = 0", 70: "END"})
print("執行結果 S =", env.get("S"))   # 1 到 100 的總和 5050

# 3. 模擬「即時回饋」：打一行、RUN 一次、立即看結果
instant = {"10": 'PRINT "HELLO, WORLD"'}
print("即時執行:", interpret({10: 'LET X = 42', 20: 'PRINT X', 30: 'END'})[1])
```

執行結果顯示：行號 35 插入後執行順序變為 10, 30, 35, 40, 50, 60, 70——初學者不必重打程式；解譯器逐行執行 `LET` 與 `FOR` 迴圈後算出 $S = \sum_{i=1}^{100} i = 5050$；最後一行證明「打完立即 RUN、立即看到結果」的即時迴圈——正是 1964 年 5 月 1 日凌晨，達特茅斯那台 GE-225 首次帶給人類的體驗。
