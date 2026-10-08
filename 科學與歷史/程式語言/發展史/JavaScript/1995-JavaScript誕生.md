# 1995：JavaScript 誕生

## 事件
1995年5月，網景公司的 **Brendan Eich** 以**十天時間**創造了 JavaScript 的第一版（初名 **Mocha**，9月改名 **LiveScript**，12月為搭行銷順風車改名 **JavaScript**）。1995年12月隨 Netscape Navigator 2.0 beta 問世。

## 語言的三大血統與其理論、實用原因

### 1. 原型繼承（prototype-based inheritance）
- **理論原因**：源自 **Self 語言（1987）**——物件不需類別，直接「複製他人並修改」。Eich 認為在十天的時間壓力下，類別系統太複雜，原型鏈是最小可行方案。
- **實用原因**：腳本語言要的是「馬上能寫」的物件，不需要宣告型別與類別階層。
- **彌補缺陷**：Java 的類別系統對腳本場景過於繁重。

### 2. 一級函數（first-class functions）與閉包
- **理論原因**：源自 **Scheme（1975）**——函數是值、詞法作用域、閉包。Eich 原本就想做「瀏覽器裡的 Scheme」。
- **實用原因**：事件處理需要回呼（callback），函數作為值是事件驅動程式設計的基礎。
- **彌補缺陷**：Java 1.0 沒有函數型別，事件處理必須寫匿名類別，極為冗長。

### 3. C 風格語法外殼
- **理論原因**：決策層要求「長得像 Java」以利行銷。
- **實用原因**：讓 Java/C 程式設計師零成本上手（`if`、`for`、`{}`、`while`）。

### 4. 動態型別與寬鬆轉換
- **理論原因**：腳本語言傳統（Perl、Tcl）——型別交給執行期推斷。
- **實用原因**：表單驗證等簡單任務不需要型別宣告。
- **缺陷伏筆**：寬鬆相等（`==` 的隱式轉換）成為日後最惡名昭彰的陷阱，也促成嚴格相等 `===` 與後來 TypeScript 的出現。

## 當時的語法範圍
`var`、函數宣告、物件字面量、原型鏈、`new` 運算子、`with` 語句（後來被廢棄）、基本事件模型。

## 彌補了什麼缺陷
彌補了網頁「完全靜態、表單驗證必須往返伺服器」的缺陷——在撥接網路時代，每次驗證都要數十秒的等待。

## 相關條目
- [1994-NetscapeNavigator問世](1994-NetscapeNavigator問世.md)
- [1997-ECMAScript1標準化](1997-ECMAScript1標準化.md)

## 程式範例

### 1. 原型繼承（Self 血統）——沒有 class，物件直接複製他人

```js
// 1995年的寫法：建構函式 + 原型鏈，沒有 class 關鍵字
function Point(x, y) {
  this.x = x;
  this.y = y;
}
Point.prototype.sum = function () {
  return this.x + this.y;
};

var p = new Point(3, 4);
p.sum(); // 7 —— 方法存在原型上，物件本身沒有 sum
```

### 2. 一級函數與閉包（Scheme 血統）——函數是值、可捕捉外層變數

```js
// 函數作為參數（事件驅動的基礎）
button.onclick = function () { alert("clicked!"); };

// 閉包：內層函數記住外層變數
function makeCounter() {
  var count = 0;
  return function () { return ++count; };
}
var next = makeCounter();
next(); // 1
next(); // 2 —— count 被「關」在閉包裡
```

### 3. 動態型別與寬鬆相等的陷阱伏筆

```js
1 == "1";        // true  —— 隱式轉換（日後的惡名昭彰陷阱）
null == undefined; // true
0 == "";         // true  —— 這些語義陷阱催生了 === 與後來的 TypeScript
```

### 4. 同期的 Java：冗長的對照（彌補了什麼）

```java
// Java 1.0 做同樣的事件處理要寫匿名類別——JavaScript 一行解決
button.addActionListener(new ActionListener() {
  public void actionPerformed(ActionEvent e) {
    System.out.println("clicked!");
  }
});
```
