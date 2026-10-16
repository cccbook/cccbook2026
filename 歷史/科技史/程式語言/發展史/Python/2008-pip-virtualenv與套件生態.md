# 2008：pip、virtualenv 與套件生態——從散裝腳本到完整體系

## 事件
Python 的套件管理在 2003–2012 年間逐步成形：

- **2003**：**PyPI**（Python Package Index）上線——中央套件索引。
- **2004**：**setuptools**（由 Phillip J. Eby 開發）——在 distutils 之上加入依賴宣告與 `easy_install`。
- **2007**：**virtualenv**（Ian Bicking）——為每個專案建立隔離的 Python 環境。
- **2008**：Ian Bicking 寫下 **pyinstall**，後更名為 **pip**（2010 年 1.0）；pip 取代 easy_install，成為事實標準。
- **2012**：**wheel** 二進位套件格式（PEP 427）問世，取代「安裝時編譯原始碼」的 sdist。

## 為何重要
- **「套件管理是語言的第二生命」**：Python 語言本身優雅，但真正讓它統治科學/AI 的是十萬計的第三方套件與一鍵安裝（`pip install`）。
- **virtualenv 解決了「依賴地獄」**：不同專案需要不同版本的同一套件，全域安裝必然衝突。
- **wheel 解決了「安裝即編譯」**：NumPy 這類含 C/Fortran 的套件，用戶機器上編譯常失敗；wheel 預先編好二進位，`pip install` 秒裝。

## 理論與實用原因
- **理論原因（virtualenv）**：**環境隔離**是依賴解析理論的必要條件——全域單一版本空間必然產生版本衝突（「diamond dependency」）；每專案一個版本空間，讓衝突侷限在專案內。此思想日後影響 Node.js 的 node_modules、Rust 的 Cargo target 目錄。
- **理論原因（pip）**：setuptools 的 easy_install 有嚴重設計缺陷——無法解除安裝、先裝依賴才解析版本、遇到衝突半途而廢。pip 採用「**先解析全部依賴圖、再下載安裝**」的正確順序，支援 uninstall 與 `requirements.txt` 鎖定。
- **實用原因**：2000 年代後期，Python 社群規模暴增，中央索引（PyPI）+ 隔離（virtualenv）+ 正確解析（pip）+ 二進位（wheel）四件套缺一不可。

## 彌補了什麼缺陷
- virtualenv 彌補了「全域安裝導致專案間依賴衝突」的缺陷。
- pip 彌補了 easy_install「無法解除安裝、解析順序錯誤、無鎖定」的缺陷。
- wheel 彌補了「含 C 擴充套件安裝即編譯、在無編譯環境的機器上必然失敗」的缺陷。

## 程式範例

四件套的日常使用：

```bash
# 2007 virtualenv：每專案一個隔離環境，依賴衝突侷限在專案內
virtualenv venv
source venv/bin/activate

# 2008/2010 pip：先解析全部依賴圖、再下載安裝（easy_install 是先裝才解析）
pip install numpy pandas        # easy_install 無法解除安裝；pip 可以
pip uninstall numpy
pip freeze > requirements.txt   # 鎖定版本，重現環境
```

wheel（PEP 427）解決「安裝即編譯」：

```bash
# sdist 時代：在用戶機器上編譯 C/Fortran，常失敗
pip install --no-binary :all: numpy   # 需要 gcc + gfortran + BLAS

# wheel 時代：預先編好的二進位，秒裝
pip download numpy --only-binary :all: --platform manylinux2014_x86_64
```

setuptools 的依賴宣告（setup.py 時代，對比）：

```python
# setup.py（2004 setuptools）：pip 出現前唯一的依賴宣告方式
from setuptools import setup
setup(
    name="mypackage",
    install_requires=["numpy>=1.20", "pandas"],
)
```

## 相關條目

- [2006-NumPy問世與with陳述](2006-NumPy問世與with陳述.md)
- [2008-pandas與科學計算生態系](2008-pandas與科學計算生態系.md)
