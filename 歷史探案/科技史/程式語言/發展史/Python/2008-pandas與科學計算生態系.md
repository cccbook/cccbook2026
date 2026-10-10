# 2008：pandas 與科學計算生態系——matplotlib、scikit-learn、科學棧成形

## 事件
2000 年代後期，Python 科學棧快速成形：

- **2003**：**matplotlib**（John D. Hunter，神經科學家）——MATLAB 風格的繪圖庫。
- **2007**：**scikit-learn**（David Cournapeau 的 Google Summer of Code 專案）——機器學習工具箱。
- **2008**：**pandas**（Wes McKinney，AQR 資本的分析師）——DataFrame 表格資料結構。
- **2010**：pandas 開源（BSD），迅速成為資料分析標準。

## 為何重要
- **生態系統的「三層結構」成形**：NumPy（陣列地基）→ pandas（資料分析）→ scikit-learn（機器學習），加上 matplotlib（視覺化）——這就是後來資料科學課程教的「Python 科學棧」。
- **pandas 的 DataFrame** 是 Python 從「程式語言」變成「資料分析平台」的轉捩點；沒有 pandas，就沒有 2010 年代的「資料科學熱」。
- **跨界人物的故事**：matplotlib、pandas 的作者都不是軟體工程師，而是科學家/分析師為解決自己的問題而寫的——這是 Python「用戶即開發者」文化的最佳註腳。

## 理論與實用原因
- **理論原因（pandas）**：DataFrame 源自 **R 語言（1993）** 的 data.frame 與更早的統計軟體（S、SAS）傳統——「帶標籤的二維表格」是統計學的基本資料結構。Wes McKinney 在金融業苦於 R 的記憶體限制與 Python 缺乏表格工具，於是「把 R 的 data.frame 移植到 NumPy 上」。對齊（alignment）、向量化操作、groupby（源自 SQL 與 split-apply-combine 理論）成為核心設計。
- **理論原因（matplotlib）**：繼承 **MATLAB（1984）** 的繪圖語法（`plot(x, y)`），降低科學家的學習成本；底層用 Python 物件模型重建（Figure/Axes 階層）。
- **實用原因（scikit-learn）**：2000 年代中期機器學習文獻用的都是 MATLAB/C 代碼，難以重現；scikit-learn 以統一的 `fit`/`predict` API 把所有演算法介面標準化——API 一致性是可重現研究的基礎。

## 彌補了什麼缺陷
- pandas 彌補了「NumPy 只有無標籤陣列、處理表格資料（缺失值、異質欄位、時間序列）極其痛苦」的缺陷。
- matplotlib 彌補了「Python 無出版級繪圖工具」的缺陷。
- scikit-learn 彌補了「機器學習演算法分散在各家實作、API 不一致」的缺陷。

## 程式範例

pandas DataFrame——把 R 的 data.frame 帶到 NumPy 上：

```python
import pandas as pd

df = pd.DataFrame({
    "city":  ["台北", "台中", "高雄", "台北"],
    "temp":  [28.5, 30.2, 31.0, 29.1],
    "rain":  [0.0, None, 12.5, 3.2],      # 缺失值是表格資料的日常
})

df[df["temp"] > 29]               # 帶標籤的過濾：NumPy 只有位置，無標籤
df["rain"].fillna(0).mean()       # 缺失值處理
df.groupby("city")["temp"].mean() # groupby：split-apply-combine（源自 SQL）
```

matplotlib——MATLAB 語法、Python 物件模型：

```python
import matplotlib.pyplot as plt

plt.plot([1, 2, 3], [1, 4, 9], "o-")   # MATLAB 風格：plot(x, y)
plt.xlabel("x"); plt.ylabel("y")       # 出版級標註
plt.savefig("fig.png", dpi=300)
```

scikit-learn——統一 `fit`/`predict` API：

```python
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

# 所有演算法共用同一介面：可重現研究的基礎
for model in [LinearRegression(), RandomForestRegressor()]:
    model.fit(X_train, y_train)    # 訓練
    print(model.score(X_test, y_test))  # 評估
```

## 相關條目

- [2006-NumPy問世與with陳述](2006-NumPy問世與with陳述.md)
- [2014-Jupyter問世](2014-Jupyter問世.md)
