# 2018：dataclass 與 Python 3.7——宣告式資料類別

## 事件
2018 年 6 月，**Python 3.7** 發佈，主要新特性：

1. **`@dataclass`**（PEP 557）：宣告式產生 `__init__`、`__repr__`、`__eq__` 等方法
2. **`contextvars`**（PEP 567）：協程安全的上下文變數
3. **`breakpoint()`**（PEP 553）：統一的除錯入口
4. **資料類別與 typing 整合**：`ClassVar`、`InitVar`

## 為何重要
- **dataclass 是「樣板碼殺手」**：定義一個資料物件，過去要手寫 `__init__`（十幾行賦值）、`__repr__`、`__eq__`——全是機械性樣板；`@dataclass` 一行搞定。這是 Python 吸收 **Scala case class（2004）**、**Kotlin data class（2016）** 的跨界設計。
- **dataclass 也是 Python 邁向型別化資料建模的橋樑**：它與型別提示（PEP 484/526）深度整合——欄位型別就是宣告的一部分，日後成為 pydantic（資料驗證）、FastAPI（Web 框架）生態的基礎。
- **`breakpoint()`**：除錯從「記得 import pdb; pdb.set_trace()」變成一個內建函式，小改動大便利。

## 理論與實用原因
- **理論原因（dataclass）**：
  - 在 3.7 之前，與 3.0 相同的功能由第三方 **attrs**（2015）提供——attrs 證明了「宣告式產生方法」的需求真實存在；PEP 557 明確以 attrs 為參考（但刻意做較小、內建）。
  - 理論上這是**產品型別（product type）**的便利語法：資料物件 = 欄位的笛卡爾積；`__eq__`/`__hash__` 的語意（按欄位值比較）是結構化相等（structural equality）理論的實踐，對照 Java 的引用相等。
  - 與 **NamedTuple（2.6）**、**typing.NamedTuple** 一脈相承：不可變資料的宣告化。
- **理論原因（contextvars）**：async/await（3.5）帶來新問題——傳統 thread-local 儲存在協程間會互相污染（多個協程共用一個執行緒）；contextvars 提供協程感知的上下文，是**邏輯並行單位與狀態隔離單位對齊**的理論修正。
- **實用原因**：API/設定/記錄等場景需要大量「資料容器」類別；樣板碼占專案行數比例驚人，且手寫 `__eq__` 容易出錯（忘了比較某欄位）。

## 彌補了什麼缺陷
- dataclass 彌補了「資料類別樣板碼氾濫、手寫 __eq__/__repr__ 易錯」的缺陷。
- contextvars 彌補了「協程中 thread-local 狀態污染」的缺陷——這是 async/await 之後必修的技術債。
- `breakpoint()` 彌補了「除錯入口不統一、要記 import」的缺陷。

## 程式範例

dataclass（PEP 557）——前後對比：

```python
# 3.7 之前：資料類別全是機械性樣板
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"
    def __eq__(self, other):            # 手寫易錯：忘了比較某欄位
        return self.x == other.x and self.y == other.y

# 3.7 之後：一行搞定（參考 Scala case class / Kotlin data class）
from dataclasses import dataclass, field

@dataclass
class Point:
    x: float
    y: float = 0.0
    tags: list[str] = field(default_factory=list)  # 可變預設值的正確寫法

Point(1.0, 2.0)      # Point(x=1.0, y=2.0, tags=[]) —— __repr__ 自動生成
Point(1.0) == Point(1.0)  # True —— 結構化相等（structural equality）
```

與型別提示深度整合——pydantic/FastAPI 的基礎：

```python
from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int

# 日後生態：pydantic（驗證）、FastAPI（Web 框架）都建立在此宣告模式上
```

contextvars（PEP 567）——協程安全 vs thread-local 污染：

```python
import contextvars

request_id = contextvars.ContextVar("request_id", default="-")

# 多個協程共用一個執行緒：thread-local 會互相污染
# contextvars 是協程感知的——每個協程有自己的視圖
async def handler(rid):
    request_id.set(rid)
    await asyncio.sleep(0)     # 讓出控制權，request_id 仍是本協程的值
    log(f"request {request_id.get()}")
```

## 相關條目

- [2015-async-await與型別提示](2015-async-await與型別提示.md)
- [2016-f-string與Python-3-6](2016-f-string與Python-3-6.md)
- [2004-裝飾器與Python-2-4](2004-裝飾器與Python-2-4.md)
