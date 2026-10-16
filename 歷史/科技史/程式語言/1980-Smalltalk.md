# 1980 Smalltalk-80 誕生：Kay 的一切皆物件與 Dynabook 願景

## 案發現場

1970 年代初，Xerox PARC 的 Alan Kay 心中有一個瘋狂的願景：**Dynabook**——一台書本大小、人人可用的個人電腦，兒童能用它寫程式、畫畫、作曲。當時電腦是數百萬美元的怪獸，「個人電腦」被視為科幻。

但 Dynabook 需要的不只是硬體，而是一種**兒童也能掌握、又能表達複雜系統**的程式語言。Kay 受 Simula 67 的類別概念啟發（他說「我終於明白了，Simula 的類別就是細胞」），加上 LOGO 的建構主義教育哲學，決定設計一種新語言。

未解之謎是：**物件、類別、繼承這些概念，能不能推到極致——讓「一切皆物件」——而不崩潰？**

具體的技術難題：

1. Simula 中整數、陣列等基本型別不是物件，物件與非物件兩個世界並存。若一切皆物件，連 `if-else`、`+` 都變成物件間的訊息，效能與語義如何保證？
2. 若連程式本身（類別、方法、編譯器）都是執行期可修改的物件，系統如何自洽？
3. 如何讓非技術背景的使用者在圖形介面中「活」在系統裡？

Kay 與 Adele Goldberg、Dan Ingalls 等人在 PARC 經歷 Smalltalk-72、-74、-76 的多代演化，於 1980 年發表 Smalltalk-80，同時它不只是一個語言，而是一個**完整的作業系統、開發環境與圖形介面**。

## 偵查過程

Smalltalk 的核心技術推理：

**第一步：訊息傳遞作為唯一機制。** Smalltalk 中沒有函數呼叫，只有**訊息**（message）。物件收到訊息後，在自己的方法表中查找對應方法執行。關鍵差異：呼叫是「靜態綁定到程式碼」，訊息是「動態查找接收者」——這是後期綁定（late binding）的極致。

```smalltalk
3 + 4              "整數 3 收到 + 4 訊息"
#(1 2 3) do: [:each | Transcript show: each printString]
x > 0 ifTrue: [ Transcript show: 'positive' ]
                   "布林物件 x>0 收到 ifTrue: 區塊 訊息"
```

連 `ifTrue:` 都是訊息：`true` 與 `false` 是兩個布林物件的實例，各自以不同方法回應——`true` 執行區塊，`false` 忽略之。控制流被物件多型徹底取代。

**第二步：影像式（image）系統。** Smalltalk-80 的執行環境不是「檔案 + 編譯 + 執行」的迴圈，而是一個**持續存在的物件影像**：所有類別、方法、視窗、甚至編譯器本身都是影像中的物件，隨時可被檢視（inspect）與修改。修改一個方法，正在執行的系統立即採用——這是活體系統（live system）的先驅。編譯器是物件、類別瀏覽器（browser）是物件，系統用自己寫自己（self-hosting）。

**第三步：動態型別與類別階層。** 物件有類別，變數沒有型別（動態型別）。所有類別的根是 `Object`，其上是 `ProtoObject`。方法查找沿類別鏈向上：

```
接收者 class → 查該類方法表 → 找到則執行
                            → 找不到則向 superclass 查
                            → Object 都沒有 → doesNotUnderstand: 錯誤
```

**第四步：MVC。** Goldberg 等人提出 Model-View-Controller 模式：模型（資料與邏輯）、視圖（顯示）、控制器（輸入處理）三者分離、以訂閱-通知解耦。這成為 GUI 設計的普世範式，至今仍是 Web 框架（MVC、MVVM、React）的理論源頭。

## 結案報告

Smalltalk-80 的遺產：

- **語言系譜**：Objective-C（1984）直接借用訊息傳遞語法；Ruby（1995，見 [1987-Perl.md](1987-Perl.md) 同期的腳本革命）明言「Smalltalk 是我最愛的語言」；JavaScript（[1995-JavaScript.md](1995-JavaScript.md)）的原型機制也深受影響；Java（[1995-Java.md](1995-Java.md)）的 `Object` 根類別與單一根繼承樹就是 Smalltalk 的設計。
- **GUI 與開發環境**：Smalltalk-80 的視窗、滑鼠、圖示直接啟發了 Apple Macintosh 與 Windows；Refactoring 瀏覽器、單元測試（SUnit → JUnit → xUnit 家族）都源自 Smalltalk 社群。
- **動態語言的實踐**：影像式系統、REPL、活體除錯，成為 Lisp 與 Smalltalk 之後動態語言的標準配備。
- **教育遺產**：Kay 的「兒童寫程式」願景催生了 Squeak、Etoys、Scratch。

Kay 於 2003 年獲得圖靈獎，被尊稱為「個人電腦之父」。Smalltalk 證明：**把一個概念（物件）推到極致，可以重新定義整個運算模型——連控制流都可以是訊息。**

## 證據與工具

Smalltalk-80 示範——類別定義與訊息傳遞：

```smalltalk
Object subclass: #Counter
    instanceVariableNames: 'count'
    classVariableNames: ''
    poolDictionaries: ''
    category: 'Demo'

Counter >> initialize
    count := 0.

Counter >> increment
    count := count + 1.

Counter >> value
    ^ count.

| c |
c := Counter new.
c increment; increment.
Transcript show: c value printString.   "顯示 2"
```

用 Python 模擬 Smalltalk 的訊息傳遞與方法查找鏈：

```python
class STObject:
    def send(self, msg, *args):
        for klass in type(self).__mro__:          # 沿類別鏈向上查找
            if msg in klass.__dict__:
                return klass.__dict__[msg](self, *args)
        return self.doesNotUnderstand(msg)

    def doesNotUnderstand(self, msg):
        raise NameError(f"doesNotUnderstand: {msg}")

class Boolean(STObject): pass

class True_(Boolean):
    def ifTrue_ifFalse(self, tblock, f): return tblock()
class False_(Boolean):
    def ifTrue_ifFalse(self, t, fblock): return f()

class Counter(STObject):
    def initialize(self): self.count = 0
    def increment(self): self.count += 1; return self
    def value(self): return self.count

c = Counter(); c.send("initialize")
c.send("increment").send("increment")
print(c.send("value"))                       # 2

result = True_().send("ifTrue_ifFalse", lambda: "yes", lambda: "no")
print(result)                                # yes：控制流即訊息
```
