# 2009：ECMAScript 5——嚴格模式與 JSON

## 事件
2009年12月，**ECMAScript 5（ECMA-262 第五版）** 發佈。這是 ES3 之後**十年來的第一個新版本**，由 ES4 內戰失敗後的務實路線（ES3.1）演變而來。

## 新語法與特性

### 1. 嚴格模式（"use strict"）
- **為何加入**：ES3 的語言有大量歷史陷阱（隱式全域變數、`with`、重複參數、`this` 混亂）。ES4 失敗後，社群共識是「與其重造，不如提供一個修正版模式」。
- **理論原因**：語言演化中的「**漸進修正**」策略——新語義放進 opt-in 模式，舊程式碼不受影響（向後相容是 Web 的鐵律）。
- **實用原因**：在嚴格模式下，`foo = 1`（未宣告）會報錯而非默默建立全域變數，可在開發期捕捉錯誤。
- **彌補缺陷**：靜默錯誤（silent errors）——JS 最惡名昭彰的除錯噩夢。

### 2. JSON 原生支援（JSON.parse / JSON.stringify）
- **為何加入**：JSON（2001，Crockford）已成為 Ajax 時代的事實標準，但各家瀏覽器要靠外部函式庫解析（且 `eval()` 解析有安全風險）。
- **彌補缺陷**：`eval()` 解析 JSON 的**安全性缺陷**（任意程式碼執行）與效能問題。

### 3. 物件屬性的 getters/setters 與屬性描述器（Object.defineProperty）
- **為何加入**：Firefox 已有非標準的 getter/setter，需要標準化；屬性描述器讓「屬性可否寫入、可否列舉、可否重新定義」變成可程式化的。
- **理論原因**：補齊物件模型——ES3 的屬性全是「可寫可刪」，無法做封裝（encapsulation）與不變性（immutability）。
- **實用原因**：函式庫（如 jQuery）需要防篡改的物件；框架需要存取器攔截（後來 Vue 2 的響應式系統就建立在 `Object.defineProperty` 上）。
- **彌補缺陷**：物件屬性無封裝、無存取控制。

### 4. 陣列高階方法：map / filter / reduce / forEach / some / every
- **為何加入**：直接借鑑 **LISP/ML 的 list operation 傳統**（map/reduce 源自1950年代 LISP 與 APL），以函數式思維取代手寫 for 迴圈。
- **實用原因**：Ajax 時代的資料處理（過濾清單、轉換格式）用 for 迴圈寫既冗長又易錯（`for (var i = 0; i < arr.length; i++)` 的閉包陷阱）。
- **彌補缺陷**：迴圈樣板程式碼（boilerplate）與閉包陷阱。

### 5. Function.prototype.bind
- **為何加入**：`this` 依呼叫方式動態決定是 ES1 的設計缺陷，回呼函數的 `this` 經常丟失。
- **理論原因**：部分應用（partial application）是函數式程式設計的基礎概念。
- **彌補缺陷**：回呼中 `this` 丟失、需要 `var self = this` 的駭客寫法。

### 6. 其他
- `String.trim`、`Array.isArray`、`Date.now`、`Object.keys`、保留字放寬。

## 理論總結
ES5 的哲學是「**務實補丁**」：放棄 ES4 的革命（類別、型別、命名空間），改用嚴格模式做漸進修正，補上函數式工具與物件封裝。它證明了「向後相容 + opt-in 新語義」是 Web 語言演化的唯一可行路徑。

## 實用總結
ES5 + Node.js（同年問世，見 [2009-Nodejs問世](2009-Nodejs問世.md)）+ Chrome V8（2008）構成 JavaScript 重生的三駕馬車。ES5 的 map/filter/reduce 成為後來函數式風格（Redux、React）的基礎詞彙。

## 相關條目
- [1999-ECMAScript3正則表達式與例外處理](1999-ECMAScript3正則表達式與例外處理.md)
- [2015-ES6現代化的黎明](2015-ES6現代化的黎明.md)

## 程式範例

### 1. 嚴格模式：靜默錯誤變成明確報錯

```js
// ES5 之前（非嚴格）：靜默錯誤
function sloppy() {
  oops = 1;          // 沒宣告 → 默默建立「全域變數」！
}
sloppy();
oops;                 // 1 —— 汙染全域，誰改的都查不到

// ES5：嚴格模式（檔案或函數開頭加字串）
function strict() {
  "use strict";
  oops = 1;           // ReferenceError —— 開發期立即報錯
}
// 其他修正：重複參數報錯、八進位字面量報錯、with 禁用
```

### 2. 陣列高階方法：取代手寫 for 迴圈

```js
var users = [
  { name: "Ada",   age: 36, admin: true },
  { name: "Alan",  age: 41, admin: false },
  { name: "Grace", age: 85, admin: true }
];

// ES5 之前：手寫 for 迴圈
var admins = [];
for (var i = 0; i < users.length; i++) {
  if (users[i].admin) admins.push(users[i].name);
}

// ES5：函數式一行（map/filter/reduce 源自 LISP 1950年代）
users.filter(function (u) { return u.admin; })
     .map(function (u) { return u.name; });      // ["Ada", "Grace"]
users.reduce(function (sum, u) { return sum + u.age; }, 0);  // 162
```

### 3. this 丟失與 bind

```js
"use strict";
var counter = {
  count: 0,
  incrementLater: function () {
    setTimeout(function () {
      this.count++;          // this 是 undefined（嚴格模式）——回呼丟失 this！
    }, 100);
  }
};

// ES5 解方：bind（部分應用）
incrementLater: function () {
  setTimeout(function () { this.count++; }.bind(this), 100);  // 正確
}
// 或 ES5 時代的駭客寫法：var self = this; 用 self 代替
```

### 4. 物件封裝：defineProperty 與 getter/setter

```js
var user = {};
Object.defineProperty(user, "name", {
  value: "Ada",
  writable: false,     // 不可寫
  enumerable: true,    // 可列舉
  configurable: false  // 不可刪除/重定義
});
user.name = "Bob";     // 靜默失敗（嚴格模式下報 TypeError）

var temp = { _c: 0 };
Object.defineProperty(temp, "celsius", {
  get: function () { return this._c; },
  set: function (v) { this._c = v; }  // 存取器攔截——Vue 2 響應式的基礎
});
```
