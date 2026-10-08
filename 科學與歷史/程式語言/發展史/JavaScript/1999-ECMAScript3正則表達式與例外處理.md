# 1999：ECMAScript 3——正則表達式與例外處理

## 事件
1999年12月，**ECMAScript 3（ECMA-262 第三版）** 發佈。這是 JavaScript 前十年最重大的語言升級，此後十年（2000–2008）瀏覽器都以此為基準，ES3 成為「現代 JavaScript」的基石。

## 新語法與特性

### 1. 正則表達式（RegExp）
- **為何加入**：Perl 風格的正則在1990年代已是文字處理的標準工具；網頁開發（表單驗證、文字解析）大量需要。
- **理論原因**：正則語言的 Kleene 理論早已成熟，Perl 5 的語法成為事實標準，直接採用可零學習成本。
- **彌補缺陷**：ES1/ES2 完全沒有正則，開發者只能手寫字串解析。

### 2. 例外處理（try/catch/finally、throw）
- **為何加入**：ES1 的錯誤處理只有回傳特殊值，錯誤會靜默失敗或直接中斷。
- **理論原因**：C++（1985）與 Java 的例外機制已成主流範式；結構化錯誤處理取代檢查回傳值。
- **實用原因**：網頁腳本錯誤會讓整個頁面的互動失效，需要可控制的錯誤恢復。
- **彌補缺陷**：彌補「無法捕捉錯誤、錯誤處理無結構」的致命缺陷。

### 3. switch 語句
- **為何加入**：補齊 C 風格語法的完整性，多分支比 if/else 鏈清晰。

### 4. do-while 迴圈
- **為何加入**：「至少執行一次」的語義是 while 無法表達的，補齊 C 語法。

### 5. Number 與 String 強化
- `Number.MAX_VALUE`、`toFixed`、`toPrecision`、`charAt`、`indexOf`、`lastIndexOf`、`split` 等。
- **為何加入**：表單驗證與文字處理是當時 JS 的最大使用場景。
- **彌補缺陷**：數字格式化（金額、小數位）以前要手寫。

### 6. 其他
- 嚴格相等與型別轉換規則的精確定義、`in` 運算子、`undefined` 成為正式全域值、錯誤類型階層（Error/TypeError/RangeError 等）。

## 理論總結
ES3 的哲學是「**補齊 C/Java 的既有範式**」——例外處理學 Java/C++，正則學 Perl，switch/do-while 學 C。它沒有引入新範式，而是把1990年代主流語言的必備元素補齊。

## 實用總結
ES3 的十年統治期（2000–2008）正好是 Ajax 革命（見 [2005-Ajax革命](2005-Ajax革命.md)）——大量應用程式是用 ES3 寫的，證明這些補齊夠用但遠不理想（無模組、無塊級作用域、回呼地獄），這些痛點最終催生了 ES6。

## 相關條目
- [1998-ECMAScript2](1998-ECMAScript2.md)
- [2009-ES5嚴格模式與JSON](2009-ES5嚴格模式與JSON.md)

## 程式範例

### 1. 正則表達式：表單驗證從手寫掃描變成一行

```js
// ES2 之前：手寫字串掃描（見 1998 年範例）
// ES3 之後：Perl 風格正則，一行搞定
var isEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test("ada@example.com"); // true

"2026-10-08".match(/(\d{4})-(\d{2})-(\d{2})/);
// ["2026-10-08", "2026", "10", "08"] —— 群組擷取
```

### 2. 例外處理：結構化錯誤取代回傳 null

```js
// ES2 之前：錯誤 = 回傳特殊值（見 1998 年範例）
// ES3 之後：try/catch/finally + throw
function divide(a, b) {
  if (b === 0) throw new RangeError("除數不可為零");  // 錯誤類型階層
  return a / b;
}

try {
  divide(1, 0);
} catch (e) {
  e instanceof RangeError; // true
  e.message;               // "除數不可為零"
} finally {
  // 無論成敗都執行——資源清理的正統位置
}
```

### 3. switch 與 do-while：補齊 C 語法

```js
switch (status) {
  case 200: render(); break;
  case 404: showError(); break;
  default:  log(status);
}

do { retry(); } while (--attempts > 0);  // 至少執行一次，while 做不到
```

### 4. 數字與字串強化

```js
(3.14159).toFixed(2);          // "3.14"——以前要手寫四捨五入
"a,b,c".split(",");            // ["a", "b", "c"]
"hello".indexOf("l");          // 2
```
