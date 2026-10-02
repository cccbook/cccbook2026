# 1957 FORTRAN：第一個廣泛使用的高階編譯語言

## 案發現場

1950 年代初，IBM 704 大型主機上寫程式的方式是**組合語言**（甚至直接寫機器碼）。每寫一行程式，工程師都要親自翻譯成機器指令、管理暫存器與記憶體位址。科學計算（彈道、核物理、工程模擬）是當時最大的電腦應用，但撰寫一個數值程式往往耗時數週，而且換一種機器就要全部重寫。

謎題是：**機器只懂機器碼，人類卻只擅長數學式——中間的鴻溝能否由程式本身跨越？** 更尖銳的疑問來自當時的主流觀點：「自動翻譯出來的程式碼，效能一定遠不如手寫組語，誰會用它？」

1954 年，IBM 的 John Backus 接下這個案子，組成理論與實作兼備的團隊，目標是設計一個「用接近數學的語言寫程式，編譯出的機器碼要夠快，快到讓人願意放棄組語」。

## 偵查過程

Backus 團隊的推理分三步：

**第一步：確立語言樣貌。** 目標使用者是數學家與工程師，所以語法直接採用數學記號。1956 年定案的 FORTRAN（FORmula TRANslation）語法：

```fortran
      DIMENSION A(100), B(100)
      SUM = 0.0
      DO 10 I = 1, 100
      SUM = SUM + A(I) * B(I)
   10 CONTINUE
      STOP
      END
```

支援算術 IF、DO 迴圈、函數副程式、陣列下標——這些在今天看似平凡，在 1957 年卻是劃時代的抽象。

**第二步：攻克效能之謎。** 這是本案最關鍵的推理。當時的「翻譯器」只會逐行對映，產生低效碼。Backus 團隊發明**優化編譯器**：

1. **暫存器分配**：把最常使用的變數放入 704 的三個索引暫存器。DO 迴圈的計數變數就是首要目標——這解釋了為何 FORTRAN 的 DO 迴圈寫成 `DO 10 I = 1, 100`：迴圈次數在進入時就已知，編譯器可預先計算並用遞減計數實作。

2. **公共子表達式消除**：若程式中兩處都算 `A(I)*B(I)`，只算一次：

$$\text{Cost}(\text{手寫組語}) \approx \text{Cost}(\text{FORTRAN 編譯碼})$$

3. **展開與融合**：對迴圈內的運算重新排序，減少記憶體存取。

**第三步：驗證。** 1957 年 4 月 FORTRAN I 編譯器交付。實測結果震驚業界：在典型數值程式上，編譯碼效能達手寫組語的 50%–80%，部分程式甚至超越——因為優化編譯器能「看見」整個程式做全域優化，人類工程師反而會遺漏。

## 結案報告

FORTRAN 的成功證明了一個定理般的結論：**高階語言不必犧牲效能**。這一擊摧毀了「只有組語才夠快」的信仰，開啟了高階語言時代。

遺產清單：

1. **優化編譯器成為獨立學科**：資料流分析、暫存器分配演算法（後來的圖著色法）都源於 FORTRAN 編譯器工程。
2. **科學計算霸權六十年**：天氣模擬、CFD、有限元素法（見 [1952-有限元素法.md](../微分方程/1952-有限元素法.md)）至今仍以 FORTRAN 為核心，BLAS/LAPACK 數學庫持續被 NumPy 等現代工具呼叫。
3. **標準化的先聲**：FORTRAN II（1958）支援副程式，FORTRAN IV（1962）走向跨機器相容，催生 ANSI 標準（1966）。
4. **通往 ALGOL**：Backus 在 FORTRAN 之後參與 ALGOL 58 設計，並發明 BNF 文法（見 [1958-ALGOL.md](1958-ALGOL.md)）——從工程實作走向語言理論。

有趣的是，Backus 本人在 1977 年的 Turing 演講中批判了自己創造的指令式範式（見 [1977-Backus函數式倡議.md](1977-Backus函數式倡議.md)）——偵探最後質疑了自己破的案。

## 證據與工具

用 Python 模擬 FORTRAN 編譯器的核心思想：把 `DO` 迴圈翻譯成「低階碼」並展示暫存器分配：

```python
import re

def compile_fortran_do(source):
    """迷你 FORTRAN 編譯器：解析 DO 迴圈並產生偽組語"""
    lines = source.strip().splitlines()
    asm = []
    for line in lines:
        m = re.match(r'\s*DO\s+(\d+)\s+(\w+)\s*=\s*(\d+),\s*(\d+)', line)
        if m:
            label, var, lo, hi = m.groups()
            n = int(hi) - int(lo) + 1
            asm.append(f"LOAD  R1, #{lo}      ; 起始值 -> 暫存器")
            asm.append(f"MOV   R2, #{n}       ; 預先計算迴圈次數")
            asm.append(f"L{label}:")
        elif (m := re.match(r'\s*(\d+)\s+CONTINUE', line)):
            asm.append(f"ADD   R1, #1         ; {var} 遞增")
            asm.append(f"DEC   R2             ; 計數遞減")
            asm.append(f"JNZ   L{m.group(1)}  ; 不為零則跳回")
        else:
            asm.append(f"; 翻譯算式: {line.strip()}")
    return asm

fortran_src = """
      DO 10 I = 1, 100
   10 CONTINUE
"""
for a in compile_fortran_do(fortran_src):
    print(a)

# 展示「優化」：計數變數 I 存於暫存器 R1，全程不碰記憶體
# 這正是 1957 年 FORTRAN 編譯器超越手寫組語的秘密之一
```

執行後可看到：迴圈次數預先計算、計數變數駐留暫存器——兩個 1957 年的優化技巧，至今仍活在每一個現代編譯器（GCC、LLVM）中。
