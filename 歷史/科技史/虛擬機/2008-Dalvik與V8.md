# 2008 - Dalvik 與 V8：兩台引擎，一場效能革命

## 案件摘要
2008 年，Google 同時點燃兩把火：Android 採用暫存器式（register-based）的 Dalvik 虛擬機，Chrome 內建 V8 引擎。兩者的共同嫌犯動機是——舊式堆疊機（stack-based）虛擬機在受限裝置與瀏覽器裡跑得太慢。

## 前因 -- 為什麼會有這個案子
- **行動端**：手機記憶體僅百 MB 級，JVM 的 stack-based bytecode 每條指令都要 push/pop，一次運算需 3 次堆疊存取，還要靠 JIT 慢慢熱身。
- **瀏覽器端**：JavaScript 長期被當成「玩具語言」，各家引擎（SpiderMonkey、JScript）直譯執行，動態型別讓每次 `a + b` 都是一場型別調查。
- Google 聘來 **Lars Bak**——此人曾在丹麥參與 Self 語言的研究、打造過 HotSpot 的前身——他的到案是破案關鍵。

## 線索與推理 -- 數學式、程式、理論

### 線索 1：stack-based vs register-based 的理論成本
對一次二元運算 `a + b`：
- 堆疊機需 **3 條指令**：`load a`、`load b`、`add`，共 $3$ 次堆疊讀寫。
- 暫存器機只需 **1 條指令**：`add-int v0, v1, v2`。

設每條指令解碼成本為 $c_d$，堆疊存取成本為 $c_s$，則：
$$T_{stack} = 3c_d + 3c_s, \qquad T_{reg} = c_d + 0c_s$$

程式碼越小（bytecode 較大約 25–47%），但指令數少、dispatch 次數少，在無 JIT 的直譯器上反而更快——這正是 Dalvik 的賭注。

### 線索 2：用 Python 現場比對兩種位元組碼
```python
# stack-based 機器（CPython 預設）的 bytecode
def add(a, b):
    return a + b

import dis
print("=== CPython: stack-based ===")
dis.dis(add)
#   LOAD_FAST  a      <- push a
#   LOAD_FAST  b      <- push b
#   BINARY_ADD        <- pop b, pop a, push result
#   RETURN_VALUE

# 模擬 register-based 位元組碼
def reg_add():
    code = ["add r2, r0, r1"]  # 一條指令完成
    reg = {"r0": 3, "r1": 4}
    op, dst, s1, s2 = code[0].replace(",", "").split()
    reg[dst] = reg[s1] + reg[s2]
    return reg["r2"]

print(reg_add())  # 7
```

### 線索 3：Dalvik 的演進──JIT 與 ART
- **Dalvik（2008）**：register-based、每個 App 一個 VM 實例（Zygote fork）、dex 格式、有 trace-based JIT（Android 2.2 加入）。
- **ART（Android 4.4 試驗、5.0 全面取代，2014）**：安裝時 AOT（ahead-of-time）編譯 dex 為機器碼（`dex2oat`），執行時免 JIT；後來又加入 profile-guided JIT 混合模式：
$$\text{ART} = \text{AOT(熱點)} + \text{JIT(冷路徑)} + \text{Profile}$$

### 線索 4：V8 的隱藏類（Hidden Classes）與 Inline Caching
V8 不用字典存物件屬性，而是為每個物件配置一個「隱藏類」（shape/Map）。當物件新增屬性，隱藏類沿著轉移鏈演進：
$$C_0 \xrightarrow{\text{add } x} C_1 \xrightarrow{\text{add } y} C_2$$

若所有物件形狀相同（同構 monomorphic），屬性存取是固定偏移量：
$$\text{addr}(o.x) = \text{base}(o) + \delta_x$$

Inline caching 把「上次查到的偏移與隱藏類」直接快取在呼叫點，下一次命中就免查表：
```python
# 模擬 hidden class + inline cache
class InlineCache:
    def __init__(self):
        self.cached_shape, self.offset = None, None

    def load(self, obj, prop, shapes):
        shape = shapes[id(obj)]
        if shape is self.cached_shape:      # monomorphic 命中
            return obj[self.offset]          # 直接用偏移，免查表
        self.offset = shape.index(prop)      # miss：重新查
        self.cached_shape = shape
        return obj[self.offset]

shapes = {1: ["x", "y"]}
o = {"x": 1, "y": 2}
ic = InlineCache()
print(ic.load(o, "x", shapes))  # 1（第二次起走快取路徑）
```

### 線索 5：Lars Bak 的譜系
$$\text{Self (1987,丹麦)} \to \text{HotSpot 團隊 (1994)} \to \text{Strongtalk} \to \text{V8 (2006–2008)}$$
Self 貢獻了 prototype-based 物件與「以 shape 最佳化」的技術，HotSpot 貢獻了 JIT 與自適應最佳化（adaptive optimization）——V8 繼承兩者。

## 結案 -- 後果與影響
- **JavaScript 從玩具到效能怪獸**：V8 讓 JS 快 10 倍以上，SunSpider benchmark 上 Chrome 碾壓同期瀏覽器。
- **Node.js（2009）**：Ryan Dahl 把 V8 抽出瀏覽器配上事件迴圈（event loop），JavaScript 一夜之間成為伺服端語言，「全端 JavaScript」時代降臨。
- **Dalvik → ART**：Android 的 VM 演進成 AOT+JIT 混合式，成為行動端 VM 的教科書案例。
- V8 的 hidden class、inline caching、TurboFan/Sparkplug/ Maglev 分層 JIT 管線，至今仍是動態語言 VM 的最佳實踐。

## 關鍵人物與文獻
- **Lars Bak**：V8 之父，Self/HotSpot 譜系傳人。
- **Dan Bornstein**：Dalvik VM 設計者。
- **Ryan Dahl**：Node.js 作者（2009）。
- 文獻：Chambers & Ungar, *An Efficient Implementation of SELF* (1991)；Google I/O 2008 Dalvik talk；V8 blog *Elements kinds and inline caches*。
