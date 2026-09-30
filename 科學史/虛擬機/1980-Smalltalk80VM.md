# 1980 — Smalltalk-80 虛擬機：一切皆物件的虛擬世界

## 案件摘要
1980 年，Xerox PARC 發表 Smalltalk-80：一門「一切皆物件」的語言，搭配一個完整的虛擬機——bytecode 直譯器、物件記憶體、垃圾回收、映像檔。這是物件導向與動態語言 VM 的雙重犯罪現場，Java 的整套設計幾乎是它的翻案重審。

## 前因 -- 為什麼會有這個案子
- 1970 年代 Xerox PARC 的 Alan Kay 團隊發展 Smalltalk（-72、-76），追尋「個人運算 + 物件導向」的願景。
- Smalltalk 是**完全動態**的語言：每個操作都是訊息傳遞（含算術 `3 + 4`、控制結構 `if`），型別在執行期才確定——傳統編譯器無法直接編成高效機器碼。
- 系統須可在不同工作站間移植，且支援「活的系統」：程式在執行中被修改、物件在執行中存活與死亡。
- 線索：能否做一個 VM，同時提供 (1) 可攜的 bytecode、(2) 統一的物件記憶體、(3) 自動回收記憶體、(4) 映像檔保存整個活系統？

## 線索與推理 -- 數學式、程式、理論

### 1. 一切皆物件：$obj\ message$
Smalltalk-80 中唯一的計算原語是「訊息傳遞」：

$$\text{receiver}\ \text{selector}\ \text{args} \Rightarrow \text{lookup(selector)}\ \text{in}\ \text{class(receiver)}$$

方法查找沿類別繼承鏈向上：

$$M(c) = \begin{cases} m & \text{if } m \in \text{methods}(c) \\ M(\text{super}(c)) & \text{otherwise} \\ \text{doesNotUnderstand} & \text{if } c = \text{Object} \end{cases}$$

連 `3 + 4` 都是「送 `+ 4` 給物件 3」；`ifTrue: [...]` 是「送 `ifTrue:` 給布林物件」，以 block 為參數。控制流本身也是訊息傳遞——這是徹底的物件化。

### 2. Smalltalk-80 VM 架構
VM 三大件：

- **Bytecode 直譯器**：編譯器把方法編成緊湊 bytecode（push、send、return、jump、store 等 5 類指令），VM 以 fetch-decode-execute 執行。
- **物件記憶體（Object Memory）**：所有物件以統一格式的「物件表（object table）+ 物件空間」管理，每個物件有 header（class 指標、大小、GC 標記）。
- **映像檔（Image File）**：整個物件記憶體（含所有類別、方法、執行中物件、甚至 UI 狀態）可整體存成檔案——「凍結整個活的世界」，下次啟動即復原。這是 VM 快照概念在語言層的實現。

$$\text{Image} = \text{freeze}(O_t, O_{space}, \text{scheduler state})$$

### 3. GC 垃圾回收的先驅
物件導向 + 動態配置使手動釋放不可能，Smalltalk 大量採用自動回收：

- **標記-清除（mark-sweep）**：從根集合（roots）標記可達物件，清除不可達者。可達性定義：

$$R = \mu(\text{roots}), \quad \mu(S) = S \cup \{o \mid o \text{ 被某 } s \in S \text{ 引用}\}$$

- **世代式 GC（generational GC，David Ungar 於 Self 系統發揚）**：基於「大多數物件朝生暮死」的統計規律——弱分代假設（weak generational hypothesis），新生代用複製式回收，頻率與存活率成反比。

### 4. JIT 的先驅：Deutsch–Schiffman（1984）
L. Peter Deutsch 與 Allan Schiffman 在 ParcPlace 實作 *Efficient Implementation of the Smalltalk-80 System*（POPL 1984）：把熱門 bytecode **動態編譯成原生機器碼**、用 inline cache 加速訊息查找：

$$\text{speedup} = \frac{t_{interp}}{t_{JIT}} \approx 4\text{--}10\times$$

inline cache 把方法查找從 $O(\text{depth})$ 降為 $O(1)$（假設 receiver 型別不變）。這是 JVM HotSpot、V8、PyPy 全部 JIT 引擎的直系祖先。

### 5. Python 實作：簡單物件訊息傳遞 VM

```python
class STObject:
    def __init__(self, cls, fields=None):
        self.cls, self.fields = cls, fields or {}

    def send(self, selector, *args, vm=None):
        return vm.lookup(self.cls, selector)(self, *args)   # 動態查找

class STClass:
    def __init__(self, name, superclass, methods):
        self.name, self.super, self.methods = name, superclass, methods

class VM:
    def __init__(self):
        self.classes = {}
        self.define_class("Object", None, {
            "doesNotUnderstand": lambda self, sel: f"? {sel}"})

    def define_class(self, name, sup, methods):
        self.classes[name] = STClass(name, sup, methods)

    def lookup(self, cls, selector):                 # 沿繼承鏈查找
        c = cls
        while c is not None:
            m = self.classes[c].methods
            if selector in m: return m[selector]
            c = self.classes[c].super
        return self.classes["Object"].methods["doesNotUnderstand"]

vm = VM()
vm.define_class("Animal", "Object", {"speak": lambda self: "..."})
vm.define_class("Dog", "Animal", {"speak": lambda self: "Woof!"})

dog = STObject("Dog")
cat = STObject("Animal")
print(dog.send("speak", vm=vm))       # Woof!  (Dog 覆寫)
print(cat.send("speak", vm=vm))       # ...    (繼承自 Animal)
print(cat.send("fly", vm=vm))         # ? fly  (doesNotUnderstand)
```

## 結案 -- 後果與影響
- Smalltalk-80 的 bytecode + 物件記憶體 + image + GC，被 **Java JVM（1995）** 幾乎完整繼承（bytecode、class 載入、GC、可攜性）。
- 物件模型影響 **CLOS**（Common Lisp Object System）、**Objective-C**（訊息傳遞語法直接仿 Smalltalk）、**Ruby**（一切皆物件 + 訊息傳遞）。
- **Self**（Ungar、Chambers）繼承 Smalltalk VM 技術並發明 inline cache、adaptive optimization、prototypes——Self 的技術成為 HotSpot JIT 與 JavaScript V8 的核心。
- 映像檔概念活在今日的 Pharo、Squeak；「整個系統是活的物件世界」影響了 IDE、REPL、live programming 文化。

## 關鍵人物與文獻
- **Alan Kay、Adele Goldberg、Dan Ingalls**：Smalltalk 創始團隊。
- Goldberg & Robson, *Smalltalk-80: The Language and its Implementation*, Addison-Wesley, 1983.
- Deutsch & Schiffman, *Efficient Implementation of the Smalltalk-80 System*, POPL, 1984.
- Ungar, *Generation Scavenging: A Non-disruptive High Performance Storage Reclamation Algorithm*, SOSP/SPLASH, 1984.
- Kay, *The Early History of Smalltalk*, HOPL-II, 1993.
