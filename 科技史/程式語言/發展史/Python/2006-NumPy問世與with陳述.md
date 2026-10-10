# 2006：NumPy 問世與 `with` 陳述——科學計算的地基與資源管理

## 事件
2005–2006 年，兩件大事：

1. **NumPy 誕生**：2005 年，科學家 **Travis Oliphant** 把 1995 年的 **Numeric** 與後繼的 **numarray** 兩個互不相容的陣列套件統一重寫，2006 年發佈 **NumPy 0.9.6/1.0**——核心是 `ndarray` 多維陣列與向量化運算，底層以 C/Fortran（BLAS/LAPACK）實作。
2. **Python 2.5（2006 年 9 月）**：**`with` 陳述式**（PEP 343）——上下文管理協議 `__enter__`/`__exit__`。

## 為何重要
- **NumPy 是整個 Python 科學/AI 生態的基石**：沒有 NumPy 的 `ndarray`，就沒有 pandas（2008）、scikit-learn（2007）、TensorFlow（2015）、PyTorch（2016）——它們全部建立在 NumPy 陣列語意之上。
- **`with` 陳述**把「開檔用完要關」這類資源管理從手動 try/finally 變成一行語法，是 Python 現代化的關鍵一步。

## 理論與實用原因
- **理論原因（NumPy）**：
  - 純 Python 的 list 是「指標陣列」，每個元素都是完整物件——對百萬筆數值做加法，效能差 C 兩個數量級。**陣列程式設計（array programming）**理論源自 **APL（1962）** 與 **Fortran（1957）** 的向量機：資料連續儲存（cache-friendly）、以整批向量化操作取代逐元素迴圈。
  - 統一 Numeric/numarray 的理論理由：**生態碎片化是自殺**——兩個陣列套件互不兼容，科學家無法共享程式碼；NumPy 統一 API 後，生態才可能指數成長。
- **實用原因（NumPy）**：科學家不想手寫 C；NumPy 讓「用 Python 語法、享受 C 速度」成真，關鍵是「內層迴圈在 C，外層控制流在 Python」的分層。
- **理論原因（with）**：資源管理的不變式（file descriptor 用完必須釋放）靠**人工記得**寫 `finally: f.close()` 容易遺漏——這是 RAII（C++ 1985）與 Scheme 的 `dynamic-wind` 要解決的同一問題。`with` 把「進入/離開作用域的配對動作」協議化，由語法保證配對執行。
- **實用原因（with）**：PEP 343 的直接動機來自社群多年對 `try/finally` 樣板的抱怨。

## 彌補了什麼缺陷
- NumPy 彌補了「純 Python 數值運算慢兩個數量級」與「科學生態碎片化」的缺陷。
- `with` 彌補了「資源釋放靠人工記得、try/finally 樣板氾濫、易洩漏檔案與鎖」的缺陷。

## 程式範例

NumPy 的向量化——「Python 語法、C 速度」：

```python
import numpy as np

n = 1_000_000
py_list = list(range(n))
arr = np.arange(n)          # ndarray：連續儲存（cache-friendly）

# 純 Python：對 list 逐元素迴圈，慢兩個數量級
%timeit [x * 2 for x in py_list]    # ~50 ms

# NumPy：整批向量化，內層迴圈在 C
%timeit arr * 2                     # ~1 ms
```

NumPy 讓「用 Python 語法、享受 Fortran 速度」：

```python
a = np.random.rand(1000, 1000)
a @ a                       # 矩陣乘法走 BLAS/LAPACK（Fortran）
a.mean(axis=0)              # APL 式的整批統計運算
```

`with` 陳述（PEP 343）——前後對比：

```python
# 2.5 之前：資源釋放靠人工記得寫 finally
f = open("data.txt")
try:
    data = f.read()
finally:
    f.close()               # 忘了這行就洩漏 file descriptor

# 2.5 之後：語法保證配對執行
with open("data.txt") as f: # __enter__/__exit__ 協議
    data = f.read()         # 離開作用域自動關檔，即使拋出例外
```

## 相關條目

- [2008-pandas與科學計算生態系](2008-pandas與科學計算生態系.md)
- [2004-裝飾器與Python-2-4](2004-裝飾器與Python-2-4.md)
- [2016-PyTorch問世](2016-PyTorch問世.md)
