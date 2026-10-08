# 2015：async/await 與型別提示——Python 3.5 的兩大支柱

## 事件
2015 年 9 月，**Python 3.5** 發佈，同時落地兩個劃時代的 PEP：

1. **`async`/`await` 語法**（PEP 492，Guido 親自主導）
2. **型別提示（type hints）**（PEP 484）：`def greet(name: str) -> str:` 與 `typing` 模組

同年 11 月，Google 發佈 **TensorFlow**（見下一篇）。

## 為何重要
- **async/await**：Python 的非同步從「裝飾器 + yield 產生器的駭客技巧」變成**一等公民語法**——這是 2.2 產生器、2.4/2.5 之後非同步演進的終點站。
- **型別提示**：Python（動態型別）第一次為大型專案提供**可選的靜態型別**——不是改變語言的執行模型，而是「註解即型別」的漸進式型別（gradual typing）。
- 兩者共同回答了同一個問題：「Python 如何在保持簡單的前提下支撐大型、長期維護的系統？」

## 理論與實用原因
- **理論原因（async/await）**：
  - 在 3.4 之前，非同步程式靠 **產生器 + `@coroutine` 裝飾器**模擬（Twisted 的 callback 地獄、gevent 的猴子補丁、3.4 asyncio 的 `@asyncio.coroutine` + `yield from`）——語法上與普通函式無法區分，`yield from` 鏈層層轉發難以追蹤。
  - 理論基礎是 **coroutine（協程）**理論（CLU 1975、Modula-2、Simula 67）：可暫停/恢復的子程式。`async def` 讓「這是協程」在語法層面明確，`await` 取代 `yield from` 的雙關語意。
  - 這是語言設計的對照實驗：JavaScript（ES2017）、C#（2012）、Rust（2019）都在同期採用同樣的 `async/await` 語法——**跨語言的趨同演化**。
- **理論原因（型別提示）**：**漸進式型別（gradual typing）**理論（Jeremy Siek 2006）：動態與靜態型別可以混合——型別標註是可選的、執行期不檢查、由外部工具（mypy，Jukka Lehtosalo 開發）靜態檢查。PEP 484 明確以 mypy 的語法為基礎，並用註解（PEP 3107，3.0 已加入的函式註解語法）承載——**不新增執行期語意，零成本**。
- **實用原因**：
  - 非同步：2010 年代網路服務（C10K 問題）需要高併發 IO；callback 風格在 Python 生態已碎片化。
  - 型別：Instagram、Dropbox 等百萬行 Python 專案，動態型別的重構成本太高；mypy 證明了「動態語言 + 漸進型別」可行。

## 彌補了什麼缺陷
- async/await 彌補了「callback 地獄、產生器模擬協程語意曖昧、非同步生態碎片化」的缺陷。
- 型別提示彌補了「大型專案中動態型別導致重構困難、IDE 補全無力、錯誤要到執行期才爆發」的缺陷——同時避免 Java/C#「型別宣告強制、樣板氾濫」的極端。

## 程式範例

async/await（PEP 492）——前後對比：

```python
# 3.4 之前：產生器 + 裝飾器模擬協程，語意曖昧
import asyncio

@asyncio.coroutine
def fetch(url):
    response = yield from aiohttp.request("GET", url)  # yield from 鏈層層轉發
    return (yield from response.read())

# 3.5 之後：一等公民語法，與 JavaScript/C#/Rust 同期趨同
async def fetch(url):
    async with aiohttp.ClientSession() as session:     # async with（3.6 補齊）
        async with session.get(url) as response:
            return await response.text()               # await：明確的暫停點

async def main():
    # 高併發 IO：C10K 問題的解方
    results = await asyncio.gather(
        fetch("https://a.com"), fetch("https://b.com")
    )
```

型別提示（PEP 484）——漸進式型別：

```python
def greet(name: str, times: int = 1) -> list[str]:
    return [f"Hello, {name}!"] * times

greet("World")          # 執行期完全不檢查——零成本
greet(42)               # 執行期不報錯！由 mypy/pyright 靜態檢查
# $ mypy app.py
# error: Argument 1 to "greet" has incompatible type "int"; expected "str"

# 大型專案的價值：重構有靜態安全網、IDE 補全精確
from typing import Optional   # 3.10 之後可用 int | None 取代
def find(id: int) -> Optional[str]: ...
```

## 相關條目

- [2001-IPython與新式類別](2001-IPython與新式類別.md)
- [2021-結構化模式比對與Python-3-10](2021-結構化模式比對與Python-3-10.md)
