# 2014：Jupyter 問世——文學編程的執行環境

## 事件
- **2011**：IPython 團隊（Fernando Pérez、Brian Granger 等）推出 **IPython Notebook**——瀏覽器中的互動式筆記本：程式碼、執行結果、數學公式（MathJax）、圖表共存於一份文件。
- **2014**：Notebook 功能已超越「Python shell」的範疇（支援 40+ 種語言的 kernel），專案從 IPython 獨立為 **Jupyter Project**（名稱取自 **Ju**lia、**Py**thon、**R** 三語言）。2015 年 **Jupyter 1.0** 與 JupyterHub 問世。

## 為何重要
- **文學編程（literate programming）的實踐**：Knuth（1984）提出「程式應寫給人讀、交織說明與代碼」的理論；Jupyter 是第一個把此理論變成大規模日常實踐的工具。
- **科學研究的可重現性革命**：論文 + 資料 + 程式碼 + 執行結果合為一份 Notebook，「研究即程式碼」成為可能。2016 年的 LIGO 重力波論文即附帶 Jupyter Notebook。
- **Jupyter 是教育與資料科學的標準介面**：GitHub 原生渲染 Notebook、Colab 提供免費 GPU——整個 AI 學習生態建立在 Jupyter 之上。

## 理論與實用原因
- **理論原因**：
  - **文學編程**（Knuth 1984）：程式與文檔不該分離；Notebook 的 cell 結構把「說明、代碼、結果」交織。
  - **REPL 驅動開發**：源自 LISP（1958）的互動式傳統——「先試、後寫、再存檔」的探索式計算，特別適合資料分析（你不知道資料裡有什麼，直到你看過）。
  - **kernel 分離架構**：Notebook 前端（瀏覽器）與執行後端（kernel）以 ZeroMQ 訊息協議分離——這個「語言無關」的架構設計讓 Jupyter 超越 Python。
- **實用原因**：科學家與分析師需要「分析的推理過程也要被保存」——傳統腳本只保存代碼，丟失了探索過程與中間結果。

## 彌補了什麼缺陷
- 彌補了 IPython（純 shell）「無法保存圖表與格式化說明、分析過程不可重現」的缺陷。
- 彌補了傳統腳本「探索式計算的過程遺失」的缺陷——這是資料科學的核心工作流。

## 程式範例

Notebook 的工作流——說明、代碼、結果交織（.ipynb 的 cell 概念）：

```python
# Cell 1（markdown）:
#   ## 資料探索
#   我們先看看 iris 資料集的分佈……

# Cell 2（code）:
import pandas as pd
iris = pd.read_csv("iris.csv")
iris.head()                    # 執行結果直接顯示在 cell 下方——

# Cell 3（code）:
iris.groupby("species").mean() # 分析過程與中間結果都被保存
```

Kernel 分離架構——語言無關：

```bash
# Notebook 前端（瀏覽器）與後端 kernel 以 ZeroMQ 訊息協議分離
pip install jupyter
jupyter notebook               # 預設 Python kernel

# 支援 40+ 種語言的 kernel——Jupyter 超越了 Python
python -m ipykernel install --user        # Python
# julia> Pkg.add("IJulia")                # Julia kernel
# R>    IRkernel::installspec()           # R kernel
```

魔術指令與 LIGO 式可重現研究：

```python
In [1]: %matplotlib inline     # 圖表內嵌在 notebook 中
In [2]: %timeit sum(range(1000))
In [3]: %run -t analysis.py    # 計時執行外部腳本

# 論文 + 資料 + 程式碼 + 結果合為一份 .ipynb——「研究即程式碼」
```

## 相關條目

- [2001-IPython與新式類別](2001-IPython與新式類別.md)
- [2016-PyTorch問世](2016-PyTorch問世.md)
