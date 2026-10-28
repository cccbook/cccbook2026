# 2024：Faster CPython、去 GIL 與未來——Python 的效能革命

## 事件
2020 年代，Python 面對 AI 時代的效能挑戰，展開內部革命：

- **2021**：**Faster CPython** 專案啟動（微軟贊助，Guido 加入微軟）；**Python 3.11**（2022 年 10 月）憑**特化自適應直譯器**（PEP 659，specializing adaptive interpreter）平均快 **10–60%**。
- **2023**：**Python 3.12**——**型別參數語法**（PEP 695）：`class Foo[T]: ...`、`def f[T](x: T) -> T`；per-interpreter GIL（PEP 684）。
- **2024**：**Python 3.13**——**自由執行緒（free-threaded）實驗版**（PEP 703）：可選的**無 GIL** 建置；JIT 編譯器原型（copy-and-patch）合併。
- **生態**：uv（2024，Astral 以 Rust 寫的極速套件管理器）與 ruff（2022，Rust 寫的 linter）席捲 Python 工具鏈——**用 Rust 重寫 Python 工具**成為風潮；PyTorch 2.0（2023）的 `torch.compile` 亦然。

## 為何重要
- **GIL 是 Python 30 年的歷史債**：1991 年為了簡化實作與記憶體安全而引入的全域直譯器鎖，使多執行緒無法真正並行——Python 補上多程序（multiprocessing，2.6）與非同步（async/await）作為繞道，但 CPU 並行始終是硬傷。PEP 703 是這筆債的正式清償起點。
- **特化直譯器/JIT**：Python 直譯器 30 年來幾乎未做指令層優化；PEP 659 讓熱點程式碼在執行期「特化」為更快的專用指令——這是 30 年技術債的效能清償。
- **工具鏈的 Rust 化**：ruff/uv 把 linter 與套件安裝加速 10–100 倍，證明「Python 語法 + Rust 引擎」的分層是新典範（正如 NumPy 的「Python 語法 + C 引擎」）。

## 理論與實用原因
- **理論原因（去 GIL）**：GIL 的問題是「**並行單位與鎖粒度錯置**」——全域單一鎖讓多核浪費。去 GIL 的理論路線：把引用計數改為**偏向引用計數（biased reference counting）**（物件歸屬執行緒 + 共享原子計數），消除計數更新的全域爭用；這是 PEP 703（Meta 贊助、Sam Gross 主導）的核心設計。
- **理論原因（特化直譯器）**：**自適應直譯**理論（JIT 的中間形態）：直譯器觀察運算元的實際型別，把通用指令（`BINARY_OP`）就地替換為特化指令（`BINARY_OP_ADD_INT`）；型別假設錯誤時退回通用指令——比 JIT 便宜、比通用直譯快。
- **實用原因**：AI 訓練/推論的資料前處理是純 Python 熱點；LLM 時代 Python 是最上層的控制流語言，其直譯器效能直接影響整個 AI 基礎設施。

## 彌補了什麼缺陷
- 去 GIL 彌補了「多執行緒無法並行、多核浪費」30 年的歷史缺陷。
- 特化直譯器/JIT 彌補了「直譯器 30 年未優化、比同類動態語言慢」的缺陷。
- ruff/uv 彌補了「pip/slow linter 在大型專案中速度不足」的工具鏈缺陷。

## 程式範例

GIL 的歷史債——多執行緒無法並行：

```python
# 30 年來：GIL 使多執行緒無法真正並行
import threading

def cpu_task():
    total = sum(i * i for i in range(10_000_000))

# 兩個執行緒「輪流」執行，比單執行緒更慢（鎖爭用開銷）
threads = [threading.Thread(target=cpu_task) for _ in range(2)]
# 3.13 自由執行緒版（PEP 703）：真正的並行
# $ python3.13t app.py   ← no-GIL 建置，兩核真正同時跑
```

型別參數語法（PEP 695，3.12）——泛型的新語法：

```python
# 3.12 之前：要從 typing 匯入 TypeVar，樣板碼多
from typing import TypeVar
T = TypeVar("T")
def first(items: list[T]) -> T: ...

# 3.12 之後：型別參數直接寫在宣告上
def first[T](items: list[T]) -> T: ...
class Stack[T]:
    def push(self, item: T): ...
```

特化自適應直譯器（PEP 659，3.11）——執行期觀察型別並特化：

```python
# 熱點程式碼在執行期被「特化」：通用指令 → 專用指令
def total(xs):
    s = 0
    for x in xs:
        s += x        # BINARY_OP → BINARY_OP_ADD_INT（觀察到都是 int 後）
    return s
# 3.11 平均快 10–60%——30 年未優化的直譯器開始進化
```

ruff/uv——用 Rust 重寫 Python 工具：

```bash
# ruff（2022）：linter 快 10-100 倍；uv（2024）：套件安裝快 10 倍+
pip install ruff uv
ruff check .        # Rust 引擎，取代 flake8 + isort
uv pip install -r requirements.txt   # 秒級解析與安裝
```

## 相關條目

- [2021-結構化模式比對與Python-3-10](2021-結構化模式比對與Python-3-10.md)
- [2016-PyTorch問世](2016-PyTorch問世.md)
- [2008-pip-virtualenv與套件生態](2008-pip-virtualenv與套件生態.md)
