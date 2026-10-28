# 2001：IPython 誕生與 Python 2.2 的新式類別、產生器

## 事件
2001 年發生了兩件影響深遠的事：

1. **IPython 誕生**：哥倫比亞大學博士生 **Fernando Pérez**（物理學背景）在 2000–2001 年間開發了 **IPython**——一個加強版的互動式 Python shell，提供彩色輸出、Tab 補全、指令歷史、魔術指令（`%timeit` 等）。
2. **Python 2.2（2001 年 12 月）**：**統一型別與類別**（PEP 252/253，「新式類別」new-style classes），以及**產生器** `yield`（PEP 255）。

## 為何重要
- **IPython 是科學 Python 生態的種子**：沒有 IPython，就沒有 2011 年的 IPython Notebook，也就沒有 2014 年的 Jupyter——整個「互動式科學計算」傳統從這裡開始。
- **統一型別與類別**是 Python 物件模型史上最重要的一次手術：修復了「內建型別（list、int）與使用者類別是兩個平行世界」的歷史缺陷。
- **產生器**讓 Python 有了惰性求值（lazy evaluation）的迭代抽象，日後成為 2.4 生成器運算式、甚至 async/await 的技術基礎。

## 理論與實用原因
- **理論原因（新式類別）**：在 2.2 之前，`int`、`list` 等內建型別無法被繼承——這違反 Smalltalk 以來「一切皆物件」的統一模型理論。2.2 引入 **descriptors** 協議（`__get__`/`__set__`），把屬性存取也統一成物件協議；統一後 `class MyList(list)` 才成為可能。
- **理論原因（產生器）**：源自 **CLU（1975）** 的 iterators 與 **Icon** 語言的 generators——「暫停/恢復函式執行」的 coroutine 理論。產生器把「實作迭代器」從「寫一個有狀態的類別（要實作 `__iter__`/`__next__`）」簡化為「一個含 `yield` 的函式」，狀態由直譯器自動保存。
- **實用原因（IPython）**：科學家需要 REPL 做「探索式計算」——即時看結果、即時畫圖；標準 Python shell 太陽春（無補全、無歷史搜尋）。
- **實用原因（產生器）**：處理大型檔案/資料流時，把整個列表放進記憶體不切實際；惰性逐項產出可以處理無限序列。

## 彌補了什麼缺陷
- 新式類別彌補了「內建型別不可繼承、兩套物件模型不一致」的缺陷。
- 產生器彌補了「自訂迭代器樣板碼太多、串流處理必須整批載入記憶體」的缺陷。
- IPython 彌補了標準 shell「無補全、無內省、不適合科學探索」的缺陷。

## 程式範例

2.2 之前 vs 之後：內建型別與使用者類別的統一

```python
# 2.2 之前：內建型別不可繼承！
# class MyList(list):   # TypeError: cannot inherit from built-in type

# 2.2 之後（新式類別）：統一物件模型
class MyList(list):
    def sum(self):
        return sum(self)

ml = MyList([1, 2, 3])
ml.sum()               # 6 —— 內建型別的行為 + 自訂方法
```

產生器 `yield`（PEP 255）——前後對比：

```python
# 2.2 之前：自訂迭代器要寫有狀態的類別，樣板碼多
class Countdown:
    def __init__(self, n): self.n = n
    def __iter__(self): return self
    def __next__(self):
        if self.n <= 0: raise StopIteration
        self.n -= 1
        return self.n + 1

# 2.2 之後：一個含 yield 的函式，狀態由直譯器自動保存
def countdown(n):
    while n > 0:
        yield n        # 暫停並回傳，下次從這裡恢復
        n -= 1

for i in countdown(3): print(i)   # 3 2 1
c = countdown(2)
next(c)                # 2 —— 可處理無限/串流序列
```

IPython 的互動式探索（對比標準 shell）：

```python
In [1]: data = [1, 2, 3]
In [2]: data.        # Tab 補全列出所有方法
In [3]: %timeit sum(data)   # 魔術指令：量測執行時間
In [4]: data?        # 內省：顯示物件的文件
```

## 相關條目

- [2004-裝飾器與Python-2-4](2004-裝飾器與Python-2-4.md)
- [2014-Jupyter問世](2014-Jupyter問世.md)
- [2006-NumPy問世與with陳述](2006-NumPy問世與with陳述.md)
