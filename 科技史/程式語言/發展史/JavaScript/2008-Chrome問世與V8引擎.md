# 2008：Chrome 問世與 V8 引擎

## 事件
2008年9月2日，Google 發佈 **Chrome 瀏覽器**，核心是自研的 **V8 JavaScript 引擎**（由 Lars Bak 團隊開發，Lars Bak 曾主導 HotSpot JVM 與 Self 語言實作）。Chrome 以「多行程架構 + JIT 即時編譯」將 JavaScript 執行速度提升一個數量級。

## 為何重要
- **V8 改寫了 JavaScript 的命運**：JIT 編譯（搭配隱藏類別 hidden classes 與內聯快取 inline caching）讓 JS 從慢速直譯語言變成接近原生速度的語言。
- **V8 是 Node.js 能存在的先決條件**：2009年 Ryan Dahl 選擇 V8 打造 Node.js（見 [2009-Nodejs問世](2009-Nodejs問世.md)），JavaScript 因此離開瀏覽器成為伺服器端語言。
- Chrome 引發**效能軍備競賽**：Firefox 隨後推出 TraceMonkey/JägerMonkey，Safari 推出 Nitro，瀏覽器全面進入一年一版的高速迭代。
- Chrome 的**自動更新機制與多行程沙箱**成為現代瀏覽器標準。

## 理論與實用原因
- **理論原因**：V8 源自 Self 語言的動態型別優化研究（隱藏類別即 Self 的 maps 機制），證明動態語言也能 JIT 到接近靜態語言的速度。
- **實用原因**：Google 的網頁應用（Gmail、Google Maps、Google Docs）受制於當時瀏覽器 JS 效能瓶頸，自己造引擎是最快解方。

## 彌補了什麼缺陷
彌補了 JavaScript「效能不可預期、太慢而無法寫大型應用」的根本缺陷；也彌補了瀏覽器單行程架構下一個分頁當機整個瀏覽器掛掉的問題。

## 相關條目
- [2009-Nodejs問世](2009-Nodejs問世.md)
- [2009-ES5嚴格模式與JSON](2009-ES5嚴格模式與JSON.md)

## 程式範例

### 1. V8 的 JIT 效果：同一行程式碼，速度差一個數量級

```js
// V8 內部：隱藏類別（hidden classes）與內聯快取（inline caching）
function Point(x, y) {
  this.x = x;   // V8 依屬性賦值順序建立隱藏類別
  this.y = y;   // 順序一致的物件共享同一個 hidden class → 快
}
var points = [];
for (var i = 0; i < 1000000; i++) points.push(new Point(i, i));
// V8：JIT 編譯為機器碼，百萬次迴圈毫秒級
// 1995年的直譯器：同樣的迴圈慢 10~100 倍
```

### 2. 破壞 hidden class 的寫法（效能教學案例）

```js
var p1 = new Point(1, 2);
p1.z = 3;                  // 事後加屬性 → 產生新的 hidden class → 變慢

// 好寫法：屬性在建構函式一次給齊，順序一致
function Point3D(x, y, z) { this.x = x; this.y = y; this.z = z; }
```

### 3. V8 讓「大型 JS 應用」成為可能（Node 的先決條件）

```js
// 這種規模的程式碼，在 V8 之前的瀏覽器引擎上根本跑不動
var sum = points.reduce(function (acc, p) { return acc + p.x + p.y; }, 0);
```
