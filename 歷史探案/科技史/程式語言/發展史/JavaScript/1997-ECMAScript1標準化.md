# 1997：ECMAScript 1 標準化

## 事件
1997年6月，ECMA International 發佈 **ECMA-262 第一版（ECMAScript 1）**，把 JavaScript 從網景的專屬技術變成國際標準。標準化由 Netscape 提交，微軟、Sun 等公司共同參與。

## 為何重要
- **解決碎片化**：JScript 與 JavaScript 行為不一樣的問題有了裁決依據——「ECMAScript 說了算」。
- **確立格局**：JavaScript 是 Netscape 的商標名稱，ECMAScript 是語言標準；JScript 是微軟的實作。這個「語言 vs 標準 vs 實作」的三層結構沿用至今。
- **名稱之謎**：ECMA 不允許使用商標名 JavaScript，故取 ECMAScript（Eich 本人事後表示「一直很後悔這個名字」）。

## 標準化的內容
以 Netscape JavaScript 1.1 為基礎，規範了：
- 型別系統（Undefined、Null、Boolean、Number、String、Object）
- 原型繼承與 `new`、建構函式
- 函數、閉包、詞法作用域
- C 風格控制流程

## 理論與實用原因
- **理論原因**：語言標準化是程式語言存活的必要條件——C 有 ANSI C（1989）、SQL 有 ISO 標準；沒有標準的語言會隨廠商起落而消亡。
- **實用原因**：瀏覽器大戰下開發者需要「寫一次、處處執行」的保證，碎片化正在扼殺 Web 開發。

## 彌補了什麼缺陷
彌補了1996年 JScript 與 JavaScript 各自為政的**碎片化缺陷**，以及「語言命運綁定單一公司」的風險。這是 JavaScript 能存活超過30年的最關鍵決定——VBScript 因封閉消亡（見 [1996-VBScript問世](1996-VBScript問世.md)），JavaScript 因開放標準長存。

## 相關條目
- [1996-JScript大戰與瀏覽器相容性危機](1996-JScript大戰與瀏覽器相容性危機.md)
- [1998-ECMAScript2](1998-ECMAScript2.md)

## 程式範例

ES1 規範的核心語言面（以 Netscape JavaScript 1.1 為基礎）：

```js
// 1. 六種型別：Undefined, Null, Boolean, Number, String, Object
typeof undefined; // "undefined"
typeof null;      // "object"（歷史 bug，至今未修）
typeof 42;        // "number"

// 2. 建構函式與原型鏈
function Person(name) { this.name = name; }
Person.prototype.hello = function () { return "Hi, " + this.name; };
var p = new Person("Ada");
p.hello(); // "Hi, Ada"

// 3. 詞法作用域與閉包
function outer() {
  var x = 10;
  return function () { return x; };
}
outer()(); // 10
```

標準化的意義在於：這段程式碼在 Netscape 與 IE 中的行為**必須一致**——在此之前，`document.all` 這類 API 各家不同，連基本語義都可能分歧。
