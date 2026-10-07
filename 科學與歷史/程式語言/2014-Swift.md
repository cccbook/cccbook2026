# 2014 Swift：Objective-C 的救贖與 LLVM 之母

## 案發現場

2014 年 6 月 2 日，Apple 的 WWDC 大會上，Chris Lattner 走上台，宣布了一門沒人聽過的語言：Swift。現場開發者的反應是先錯愕、後瘋狂——因為所有人都知道 Objective-C 的痛。

當時的未解之謎：

1. **Objective-C 的語法之痛。** Objective-C 是 1983 年在 C 語言上疊加 Smalltalk 訊息傳遞的產物。三十年的技術債一目了然：訊息語法 `[array insertObject:obj atIndex:5]` 囉唆難讀、沒有命名空間（類別名前綴如 `NSString` 全靠手動約定）、記憶體管理從手動 retain/release 演化到 ARC（自動引用計數）依然處處陷阱、字串與陣列的型別不安全（都是 id，出錯要到執行時期才崩潰）。
2. **空指標之謎。** Tony Hoare 在 2009 年公開道歉，稱 1965 年發明的 null reference 是「十億美元的錯誤」。Objective-C 對 nil 傳訊雖然靜默返回（不崩潰），但這只是把 bug 藏得更深：一個 nil 沿著呼叫鏈傳播，最後在某處默默產生錯誤結果。C 系語言的空指標解引用則直接 segfault。**「這個值可能不存在」這件事，在型別系統裡沒有位置。**
3. **新手入門之難。** iOS 開發的第一課是「先理解指標、再理解訊息傳遞、再理解 retain count」——Apple 急需一門讓新手（以及替換舊手）都能快速上手的語言。

誰遇到？數百萬 iOS/Mac 開發者，以及 Apple 自己——App Store 生態是 Apple 的命根，而它的語言已經三十歲了。為何重要？因為這是行動時代最後一次「大平台親自操刀設計語言」。

## 偵查過程

Chris Lattner 的履歷就是最大的線索：他不是先設計語言、再建工具，而是**先建工具、語言是工具的果實**。2000 年他在伊利諾大學的博士論文就是 LLVM（Low Level Virtual Machine）——一套「任何語言前端 → 中間表示 IR → 任何 CPU 後端」的編譯器基礎設施。Apple 於 2005 年雇下他，LLVM 從此成為 Apple 的核心技術：C/C++/Objective-C 編譯器（Clang）、GPU 著色器、Xcode 的除錯器全都建立在 LLVM 上。

$$
\text{Swift source} \xrightarrow{\text{swiftc}} \text{LLVM IR} \xrightarrow{\text{llc}} \text{ARM/x86 machine code}
$$

**有了 LLVM 這台引擎，設計一門新語言的成本從「十年造船」降到「幾年裝帆」。** 這是 Swift 誕生的工程前提，也是本篇最關鍵的推導。Lattner 的推理可拆解如下：

**推理一：Optional 型別 $\mathtt{T?}$——消滅空指標之謎。** 這是 Swift 對「十億美元錯誤」的正面回擊，靈感來自 Haskell 的 Maybe 與 Rust 的 Option。核心推導：**把「可能不存在」變成型別的一部分，讓編譯器強迫你處理它。**

$$
\texttt{Optional<T>} = \texttt{none} \;|\; \texttt{some(T)}
$$

```swift
var name: String? = nil          // 可能沒有值
// let count = name.count        // 編譯錯誤！name 是 Optional
if let n = name {                // 必須先解包
    print("\(n) 字")
} else {
    print("沒有名字")
}
```

`?` 語法糖的背後是「null 的缺席」：普通型別 `String` **根本不可能**是 nil，只有 `String?` 才可能——空指標這一整類 bug 在編譯時期被判死刑。`nil` 傳播則由 `?.` 與 `??` 運算子處理：

```swift
let upper = name?.uppercased()       // Optional 鏈式傳播
let final = name?.uppercased() ?? "DEFAULT"  // nil 合併
```

**推理二：值型別（struct 為王）。** Objective-C 一切皆引用型別（class），別名與共享可變狀態處處皆是。Swift 反轉：**struct 是一等公民，語言標準庫的 String、Array、Dictionary 全是值型別**——賦值即複製（寫時複製最佳化），別名問題天然消失。這與 [2010-Rust.md](2010-Rust.md) 的所有權系統遙相呼應，是 2010 年代「回歸值語意」浪潮的一部分。

**推理三：Playground 即時回饋。** Swift Playground 讓程式碼一邊打、結果一邊顯示——靈感來自 Smalltalk 的工作區與 Bret Victor 的即時程式設計演示。這把學習曲線砍掉了大半：iOS 入門的第一天就能看到畫面，而不是先學三十年的技術債。

**推理四：與 Objective-C 的和平共存。** Swift 沒有推翻舊世界，而是能與 Objective-C 混編（bridge header），讓百萬行的舊程式碼可以一段一段遷移。這是語言遷移史的教科書案例。

## 結案報告

Swift 的遺產：

1. **LLVM 工具鏈之母。** Swift 是 LLVM 生態最重要的旗艦應用，證明了「編譯器基礎設施先行」的路線可行。LLVM 之後成為半導體與語言設計的世界標準：Rust、Julia、Zig、Crystal 都建在 LLVM 上；連 AMD、NVIDIA 的 GPU 工具鏈也在用。Lattner 後來又創造了 MLIR（多層次 IR），繼續擴張這條路線。
2. **Optional 型別的普及。** Swift 之後，「消滅 null」成為新語言的標配：Kotlin 的 `T?`、Dart 的 null safety（Dart 2.12）——同一波「null safety 潮流」席捲所有主流語言。Java 的 `Optional<T>` 也從「可有可無的 API」變成「遲到的補救」。
3. **Objective-C 的退位。** 2019 年 SwiftUI 發布（宣告式 UI 框架），Objective-C 正式成為「維護模式語言」。Apple 完成了三十年技術債的清償。
4. **現代語言設計的同潮流。** Swift、Kotlin（2011/2016）、Dart（2011）構成了 2010 年代「平台親生子語言」的三巨頭：都強調 null safety、都支援函數式風格、都與舊語言和平共存、都靠現代編譯基礎設施（LLVM/JVM）加持。

Lattner 的推理路線圖值得每個語言設計者銘記：**先造引擎（LLVM），再造船（Swift），最後連 ocean（App Store 生態）都是你的。**

## 證據與工具

用 Swift 展示 Optional、值型別與 protocol 導向設計：

```swift
// Optional：消滅空指標
var stock: Int? = nil
let display = stock.map { "庫存 \($0) 件" } ?? "查無庫存"
print(display)  // 查無庫存

// 值型別：struct 賦值即複製
struct Point: Equatable {
    var x: Int, y: Int
    static func + (a: Point, b: Point) -> Point {  // 運算子多載
        Point(x: a.x + b.x, y: a.y + b.y)
    }
}
var p = Point(x: 1, y: 2)
var q = p
q.x = 100
print(p, q)  // Point(x: 1, y: 2) Point(x: 100, y: 2) —— p 未受影響

// protocol 導向：型別安全的泛型函數
func first<T: Equatable>(_ xs: [T], equalTo v: T) -> T? {
    xs.first { $0 == v }
}
print(first([1, 2, 3], equalTo: 2) ?? "none")  // Optional(2)
```

再用 Python 模擬 Optional 型別的核心機制——把「可能不存在」編入型別檢查：

```python
from dataclasses import dataclass
from typing import Optional, Union, TypeVar

T = TypeVar("T")

@dataclass
class Some(Generic[T] if False else object):
    value: object

# 模擬 Optional<T>：some(T) | none
class Optional:
    def __init__(self, value=None, present=False):
        self.value, self.present = value, present

    @classmethod
    def some(cls, v): return cls(v, True)

    @classmethod
    def none(cls): return cls()

    def map(self, f):                        # ?. 鏈式傳播
        return Optional.some(f(self.value)) if self.present else Optional.none()

    def unwrap_or(self, default):            # ?? nil 合併
        return self.value if self.present else default

name = Optional.none()
upper = name.map(str.upper)                  # 不會崩潰，只是傳播 none
print(upper.unwrap_or("DEFAULT"))            # DEFAULT

name = Optional.some("swift")
print(name.map(str.upper).unwrap_or("DEFAULT"))  # SWIFT
```

再模擬 Swift 編譯管線的核心——「原始碼 → LLVM IR → 機器碼」的抽象層次：

```python
# 模擬：高階運算式 → 類 LLVM IR（SSA 形式的三地址碼）→ 求值
def to_ir(expr, counter=[0]):
    if isinstance(expr, int):
        return str(expr)
    op, a, b = expr
    ra, rb = to_ir(a, counter), to_ir(b, counter)
    counter[0] += 1
    tmp = f"%{counter[0]}"
    print(f"  {tmp} = {op} i64 {ra}, {rb}")   # SSA 形式的 IR
    return tmp

# Swift: let r = (1 + 2) * 3
print("IR:")
r = to_ir(("*", ("+", 1, 2), 3))
print("ret i64", r)
#  %1 = add i64 1, 2
#  %2 = mul i64 %1, 3
#  ret i64 %2
```

2014 年的 Swift 用一個 `?`、一個 struct 與一台 LLVM 引擎，回答了 Objective-C 三十年的技術債——現代語言設計自此有了新的範本。
