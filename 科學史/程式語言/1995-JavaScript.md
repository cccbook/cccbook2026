# 1995 JavaScript 誕生：Eich 十天寫出的瀏覽器腳本與原型繼承

## 案發現場

1995 年，網景（Netscape）正面臨存亡抉擇：Mosaic 團隊分家而去的競爭者 Sun 即將推出 Java（[1995-Java.md](1995-Java.md)）Applet，而網頁需要的是「能讓靜態 HTML 動起來」的輕量腳本——設計師與業餘者能寫、嵌入瀏覽器、即時執行。管理層決定網景必須擁有自己的腳本語言。

 Brendan Eich 被要求在**十天之內**做出原型。十天！這個瘋狂的時限決定了 JavaScript 的一切：沒有委員會審查、沒有長期設計、沒有回頭路——一旦進入 Netscape 2.0 beta，數百萬網頁就會依賴它的每一個怪癖。

未解之謎是：**在十天之內，如何把 Scheme 的一等函數、Self 的原型繼承、Java 的 C 風格語法，融成一個能跑在瀏覽器裡的動態語言？**

這個問題為何重要？這個「十天趕工的玩具」後來成為**世界上部署最廣的程式語言**——每一台瀏覽器、每一個網頁、最終透過 Node.js 征服了伺服器與全端開發。

## 偵查過程

Eich 的十天推理，可以拆解為四個關鍵決策：

**第一步：語法上像 Java，靈魂上像 Scheme。** 管理層要求「看起來像 Java」，但 Eich 真正的靈感來自：

- **Scheme**（Lisp 的方言）：一等函數（first-class functions）、閉包（closure）
- **Self**（Smalltalk 的後裔）：原型繼承（prototype-based inheritance）
- **Java**：C 風格語法、`var` 宣告

```javascript
// 一等函數與閉包（Scheme 的靈魂）
function makeCounter() {
    let count = 0;
    return function () { return ++count; };  // 閉包捕捉 count
}
```

**第二步：原型繼承——用自我機制替代類別。** 這是 JavaScript 最深遠的發明。Self 的洞察是：**物件不需要類別，物件可以直接從其他物件複製與委派**。Eich 的實作：每個物件有一個隱藏的 `[[Prototype]]` 連結指向另一個物件。屬性查找沿原型鏈向上：

```
obj.prop → obj 自己有嗎？
         → 沒有則問 [[Prototype]]
         → 沿鏈向上直到 Object.prototype
         → 都沒有 → undefined
```

Eich 用 C 語言的思維實作了這個機制：所謂「類別」不過是**建構子函數** + 其 `prototype` 物件：

```javascript
function Shape() {}
Shape.prototype.area = function () { return 0; };

function Circle(r) { this.r = r; }
Circle.prototype = Object.create(Shape.prototype);   // 委派鏈
Circle.prototype.area = function () { return 3.14159 * this.r * this.r; };

new Circle(2).area();   // 沿 Circle.prototype → Shape.prototype 查找
```

關鍵推導：**委派（delegation）比複製更省記憶體、比類別更靈活**——任何物件在執行期都能改變自己的原型（`__proto__`），類別階層的靜態性被完全打破。對比 Smalltalk（[1980-Smalltalk.md](1980-Smalltalk.md)）的類別方法表查找、C++（[1983-Cplusplus.md](1983-Cplusplus.md)）的編譯期 vtable，JavaScript 的原型鏈是三者的動態極端。

**第三步：動態型別與弱型別。** JavaScript 採動態型別，且是**弱型別**——`+` 運算子會自動做型別轉換（`1 + "2" === "12"`）。Eich 的推導：腳本語言的使用者是設計師與業餘者，型別錯誤應該寬容而非中斷。這個決策換來了易用性，代價是無窮的怪癖（`==` vs `===`、`NaN !== NaN`）與後世無數的笑話集。

**第四步：事件迴圈與非同步。** 瀏覽器環境的單執行緒 + 事件迴圈（event loop）模型：腳本不能阻塞，只能註冊回呼（callback）。這個「瀏覽器的限制」成為二十年後 Node.js 的核心架構。

**標準化**：1997 年 ECMA 發布 ECMAScript 1.0，從此語言的演進由 ECMA TC39 委員會主導——Netscape 的十天作品被馴服為國際標準。

## 結案報告

JavaScript 的遺產：

- **語言系譜**：原型繼承影響了 Lua、io；一等函數與閉包成為所有現代語言的標配；ECMAScript 2015（ES6）加入 `class` 語法糖與箭頭函數，收編了原型機制。
- **全端時代**：Node.js（2009）把 V8 引擎搬上伺服器，「JavaScript everywhere」成真；npm 成為世界最大的套件庫。
- **函數式復興**：一等函數、callback、Promise、async/await，使函數式思維（見 [1977-Backus函數式倡議.md](1977-Backus函數式倡議.md)、[1990-Haskell.md](1990-Haskell.md)）透過 JavaScript 進入主流。
- **十天作品的教訓**：TypeScript（2012）的誕生正是對 JavaScript 弱型別的回應——靜態型別終於回到 Web。

Eich 後來共同創辦 Mozilla。JavaScript 證明：**語言的成功不完全取決於設計品質——部署平台與時機，有時更重要。**

## 證據與工具

JavaScript 示範——原型繼承、閉包與事件迴圈：

```javascript
// 原型繼承
function Shape() {}
Shape.prototype.area = function () { return 0; };

function Circle(r) { this.r = r; }
Circle.prototype = Object.create(Shape.prototype);
Circle.prototype.area = function () { return Math.PI * this.r ** 2; };

console.log(new Circle(2).area());        // 12.566...
console.log(Object.getPrototypeOf(new Circle(1)) === Circle.prototype);

// 閉包
function makeCounter() {
    let count = 0;
    return () => ++count;
}
const c = makeCounter();
console.log(c(), c(), c());               // 1 2 3

// 事件迴圈：非同步不阻塞
setTimeout(() => console.log("非同步"), 0);
console.log("同步先執行");
```

用 Python 模擬原型鏈查找與閉包：

```python
class JSObject:
    def __init__(self, proto=None):
        self._props, self._proto = {}, proto

    def get(self, prop):                    # 沿原型鏈向上查找
        obj = self
        while obj is not None:
            if prop in obj._props:
                return obj._props[prop]
            obj = obj._proto
        return None                          # undefined

    def set(self, prop, val):
        self._props[prop] = val

Shape = JSObject()
Shape.set("area", lambda self: 0)

Circle = JSObject(proto=Shape)               # Circle.prototype -> Shape.prototype
Circle.set("area", lambda self: 3.14159 * self._props["r"] ** 2)

c = JSObject(proto=Circle)                   # new Circle(2)
c.set("r", 2)
print(c.get("area")(c))                      # 12.57，沿鏈查找

# 模擬閉包：內層函數捕捉外層變數
def make_counter():
    count = [0]
    def incr():
        count[0] += 1
        return count[0]
    return incr

cc = make_counter()
print(cc(), cc(), cc())                      # 1 2 3
```
