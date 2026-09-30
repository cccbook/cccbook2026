# 1991 Python 誕生：van Rossum 的可讀性革命與 AI 時代霸主

## 案發現場

1980 年代末，荷蘭 CWI 的 Guido van Rossum 參與了 ABC 語言的開發。ABC 是一門為非程式設計師設計的教學語言，有許多好點子：縮排區塊、無型別宣告、內建高階資料結構。但它有致命缺陷：**封閉**——無法呼叫作業系統功能、無法用 C 擴展、無法寫系統工具。van Rossum 說：「ABC 的失敗讓我學到，一個語言若不能接觸系統底層，再優雅也沒人用。」

當時他面臨的未解之謎：**能不能把 ABC 的優雅可讀性，與 C（[1972-C語言.md](1972-C語言.md)）的系統擴展能力結合，做出一門「既好讀又好用」的腳本語言？**

具體難題：同期 Perl（[1987-Perl.md](1987-Perl.md)）已經證明腳本語言有市場，但 Perl 的魔力變數與語境系統可讀性極差。van Rossum 想要的是對立面——**可讀性至上**（Pythonic：應該只有一種明顯的做法）。

1989 年聖誕假期，van Rossum 為打發時間開始寫直譯器，1991 年 2 月發布 Python 0.9.0。這個問題為何重要？三十多年後，Python 成為科學計算與 AI 時代的統治者——NumPy、PyTorch、TensorFlow 的生態全部建立在其上。

## 偵查過程

**第一步：ABC 的教訓與修正。** van Rossum 的推理：

- 保留 ABC 的縮排語法（indentation as syntax）：程式區塊由縮排決定，去掉 `{}` 與 `begin/end`。這強制了可讀性——**程式的視覺結構就是邏輯結構**。
- 保留 ABC 的動態型別與內建 dict/list。
- 修正 ABC 的封閉性：從第一天起就設計 **C API 擴展機制**，任何 C 函式庫都能包裝成 Python 模組。這是 Python 生態的命脈。

```python
# 縮排即語法
def quicksort(xs):
    if len(xs) <= 1:
        return xs
    pivot, *rest = xs
    less    = [x for x in rest if x < pivot]
    greater = [x for x in rest if x >= pivot]
    return quicksort(less) + [pivot] + quicksort(greater)
```

**第二步：可讀性原則。** 1999 年 van Rossum 寫下「Code Like a Pythonista」，Tim Peters 化為《The Zen of Python》（PEP 20）：

> There should be one—and preferably only one—obvious way to do it.

這是對 Perl TMTOWTDI 的直接回應。配套設計：關鍵字 `import this`、命名規範（PEP 8）、強制縮排、去掉了 Perl 式的魔法變數。

**第三步：CPython 直譯器架構。** van Rossum 的實作策略：

1. **位元組碼（bytecode）**：原始碼先編譯為簡單的堆疊式位元組碼，再由虛擬機逐條執行。這比純樹走訪直譯器快，又比編譯到機器碼簡單。

```python
import dis
dis.dis("x = 1 + 2")
#  LOAD_CONST 1、LOAD_CONST 2、BINARY_ADD、STORE_NAME x
```

2. **引用計數 + GIL**：記憶體管理用引用計數（配合標記-清除處理環狀引用）；為簡化實作，整個直譯器加了一把全域鎖（GIL, Global Interpreter Lock）——同一時刻只有一個執行緒執行 Python 位元組碼。這個「偷懶」的決策換來了 C 擴展的簡單性，卻成為二十年後多核時代的包袱。

3. **Batteries included**：標準庫自帶網路、文字、壓縮、GUI——「出廠即用」，這是 ABC「 batteries included 」哲學的實現。

**第四步：科學計算的起飛。** 1995 年的 Numeric、2006 年的 NumPy：Python 的 C API 讓 Fortran/C 的線性代數庫能以 NumPy 陣列的形式被呼叫。Python 成為「黏著劑」——上層好讀的腳本、下層高效能的 C。這個組合最終征服了 AI 時代。

## 結案報告

Python 的遺產：

- **科學計算與 AI 霸主**：NumPy、SciPy、pandas、PyTorch、TensorFlow、Jupyter——整個 AI 世代的工具鏈以 Python 為語言。
- **腳本革命**：與 Perl（[1987-Perl.md](1987-Perl.md)）、Ruby 並列，但以可讀性勝出，成為教學第一語言。
- **教育影響**：「Pythonic」成為程式風格的代名詞；The Zen of Python 成為最常被引用的語言哲學。
- **C API 與黏著劑文化**：以 C 擴展征服高效能領域的模式，影響了 Lua、Ruby 的擴展設計。
- **教訓的傳承**：GIL 的包袱催生了 2023 年後的 free-threading 實驗；引用計數的環狀引用問題影響了 Rust 的 `Rc`/`Arc` 設計（見 [1973-ML型別推導.md](1973-ML型別推導.md) 同源的型別血脈）。

van Rossum 被尊稱為「BDFL」（終身仁慈獨裁者）至 2018 年。Python 證明：**可讀性不是語言的裝飾，而是它征服世界的武器。**

## 證據與工具

Python 示範——縮排語法、生成器與 GIL 行為：

```python
# Batteries included：標準庫即用
from collections import Counter
import re

text = "the quick the lazy the dog"
words = Counter(re.findall(r"\w+", text))
print(words.most_common(2))        # [('the', 3), ('quick', 1)]

# 生成器：惰性求值
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

from itertools import islice
print(list(islice(fibonacci(), 8)))   # [0, 1, 1, 2, 3, 5, 8, 13]
```

用 Python 模擬 CPython 的位元組碼虛擬機與 GIL：

```python
# 模擬 CPython 堆疊式位元組碼 VM
import threading, time

class MiniVM:
    """模擬堆疊式 VM：LOAD_CONST / BINARY_ADD / STORE_NAME"""
    def __init__(self):
        self.stack, self.names = [], {}

    def exec(self, code):
        for op, arg in code:
            if op == "LOAD_CONST":  self.stack.append(arg)
            elif op == "STORE_NAME": self.names[arg] = self.stack.pop()
            elif op == "BINARY_ADD":
                b, a = self.stack.pop(), self.stack.pop()
                self.stack.append(a + b)
        return self.names

vm = MiniVM()
print(vm.exec([("LOAD_CONST", 1), ("LOAD_CONST", 2),
               ("BINARY_ADD", None), ("STORE_NAME", "x")]))   # {'x': 3}

# 模擬 GIL：兩個執行緒「輪流」執行，任一時刻只有一個在跑
lock = threading.Lock()
results = []

def worker(name):
    with lock:                          # GIL：全域鎖
        time.sleep(0.01)                # 持有鎖時其他執行緒停擺
        results.append(f"{name} 執行完畢")

threads = [threading.Thread(target=worker, args=(f"T{i}",)) for i in range(3)]
for t in threads: t.start()
for t in threads: t.join()
print(results)
```
