# Python 程式語言發展史年表

> Python 是 1989 年聖誕假期，由荷蘭 CWI 的 **Guido van Rossum** 以個人嗜案開始的語言。
> 目標是「在 C 與 shell 之間找到一個中間層：像 shell 一樣好寫好讀，像 C 一樣能呼叫系統功能」。
> 它繼承了 ABC（教學語言的易讀性）、Modula-3（例外與模組）、C（擴充介面）等傳統，
> 之後更以「 batteries included 」哲學與 NumPy / Jupyter / PyTorch 等生態系，
> 成為科學計算、資料科學與 AI 時代的共同語言。

## 前史：理論根源

| 年份 | 事件 | 意義 |
|------|------|------|
| 1958 | LISP 問世 | 動態型別、互動式 REPL、函式式程式設計的先驅 |
| 1970 | UNIX 與 C 語言 | 系統程式設計的事實標準；Python 的擴充模組以 C API 為基礎 |
| 1972 | Smalltalk | 物件導向模型；Python「一切皆物件」的思想來源 |
| 1977 | Bourne shell | 腳本自動化；Python 補足了 shell「難以寫大型程式」的缺陷 |
| 1980 | ABC 語言 | Guido 參與開發的教學語言：縮排語法、無型別宣告、高階集合——Python 的直系血親 |
| 1987 | Perl 問世 | 文字處理腳本的主流，但可讀性差——Python 以「可讀性即語法」與之對立 |
| 1988 | Modula-3 | 例外處理、模組系統的設計參考 |

## 正式年表

| 年份 | 標題 | 關鍵語法/特性 |
|------|------|---------------|
| 1989 | [聖誕假期的誕生](1989-聖誕假期的誕生.md) | Guido 開始實作直譯器：繼承 ABC、以縮排取代括號、動態型別 |
| 1991 | [0.9.0 首次公開](1991-0-9-0首次公開.md) | 函式、類別、例外、核心型別（list/dict/tuple/string）、`import` 模組 |
| 1994 | [Python 1.0 問世](1994-Python-1-0問世.md) | `lambda`、`map`、`filter`、`reduce`——函式式語法第一次進入 |
| 2000 | [Python 2.0 與 list comprehension](2000-Python-2-0與list-comprehension.md) | 列表推導式（PEP 202）、循環垃圾回收（PEP 205）、`+=` 擴充指定、Unicode 字串型別 |
| 2001 | [IPython 與新式類別](2001-IPython與新式類別.md) | IPython 互動環境誕生；2.2 統一型別與類別（新式類別）、產生器 `yield`（PEP 255） |
| 2004 | [裝飾器與 Python 2.4](2004-裝飾器與Python-2-4.md) | `@decorator` 語法（PEP 318）、內建 `set`/`frozenset、生成器運算式 |
| 2006 | [NumPy 問世與 `with` 陳述](2006-NumPy問世與with陳述.md) | NumPy 0.9.6/1.0 統一 Numeric/numarray；2.5 `with` 資源管理（PEP 343） |
| 2008 | [Python 3.0 大分裂](2008-Python-3-0大分裂.md) | `print()` 函式、Unicode 為預設字串、`/` 真除法（PEP 238）、新式 metaclass（PEP 3115） |
| 2008 | [pip、virtualenv 與套件生態](2008-pip-virtualenv與套件生態.md) | pip（2008/2010）、virtualenv（2007）、PyPI（2003）、wheel 格式（2012） |
| 2008 | [pandas 與科學計算生態系](2008-pandas與科學計算生態系.md) | pandas（2008）、matplotlib（2003）、scikit-learn（2007）——科學棧成形 |
| 2014 | [Jupyter 問世](2014-Jupyter問世.md) | IPython Notebook（2011）獨立為 Jupyter Project：多語言 Notebook、 literacy programming 實踐 |
| 2015 | [async/await 與型別提示](2015-async-await與型別提示.md) | `async`/`await`（PEP 492）、型別提示 `typing`（PEP 484）——3.5 的兩大支柱 |
| 2015 | [TensorFlow 與深度學習框架](2015-TensorFlow與深度學習框架.md) | Theano（2007）到 TensorFlow（2015）：宣告式計算圖時代 |
| 2016 | [PyTorch 問世](2016-PyTorch問世.md) | 動態計算圖、Lua Torch 血統、autograd；2018 年 1.0、2022 年 PyTorch 基金會 |
| 2016 | [f-string 與 Python 3.6](2016-f-string與Python-3-6.md) | f-string 格式化（PEP 498）、變數標註（PEP 526）、非同步產生器（PEP 525） |
| 2018 | [dataclass 與 Python 3.7](2018-dataclass與Python-3-7.md) | `@dataclass`（PEP 557）、`contextvars`、`breakpoint()`、環境變數 `PYTHONPATH` 之外的路徑設定 |
| 2019 | [海象運算子與 Python 3.8](2019-海象運算子與Python-3-8.md) | `:=` 指定運算式（PEP 572）、位置限定參數 `/`（PEP 570）、f-string `=` 除錯語法 |
| 2021 | [結構化模式比對與 Python 3.10](2021-結構化模式比對與Python-3-10.md) | `match`/`case`（PEP 634）、聯合型別 `X \| Y`（PEP 604）、括號化上下文管理器 |
| 2024 | [Faster CPython、去 GIL 與未來](2024-Faster-CPython-去GIL與未來.md) | 3.11/3.12 特化直譯器（PEP 659）、3.13 自由執行緒實驗（PEP 703）、型別參數語法（PEP 695） |

## 工具鏈與生態系發展主軸

1. **2003 PyPI → 2007 virtualenv → 2008 pip → 2012 wheel** —— 套件管理從 distutils 的零散腳本，走向「套件索引 + 虛擬環境 + 依賴解析 + 二進位 wheel」的完整體系。
2. **2001 IPython → 2011 Notebook → 2014 Jupyter** —— 互動式運算從加強版 shell，發展為文學編程（literate programming）的執行環境，成為科學教育與資料科學的標準介面。
3. **1995 Numeric → 2006 NumPy → 2008 pandas → 2015 TensorFlow → 2016 PyTorch** —— 科學計算生態以 NumPy 的 `ndarray` 與 C/Fortran 後端為地基，逐步長出資料分析與深度學習的整個森林。

## 發展主軸

1. **1989–1994：從 ABC 到 1.0** —— 補足「C 太低階、shell 太弱、Perl 不可讀」的空白，以縮排與可讀性立下語言性格。
2. **2000–2006：科學化與現代化** —— 列表推導式、新式類別、裝飾器、產生器、`with`、NumPy：Python 從腳本語言長成應用語言。
3. **2008–2010：Python 3 的陣痛** —— 打破「2 的歷史包袱」（字元編碼、除法、print），代價是長達十年的遷移期。
4. **2014–2016：AI 時代的共通語** —— Jupyter、型別提示、async/await、PyTorch：Python 成為機器學習的事實標準。
5. **2018–2024：成熟與自我革命** —— dataclass、模式比對、Faster CPython、自由執行緒：在保持可讀性的同時補上效能與並行的短板。

## 閱讀方式

每篇檔名以年份開頭（4 碼），建議按年份順序閱讀；每篇皆包含「事件、為何重要、理論與實用原因、彌補了什麼缺陷」等小節，說明每個新語法「為何」在那個時間點被加入。
