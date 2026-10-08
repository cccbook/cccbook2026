# 2009：Node.js 問世——JavaScript 走出瀏覽器

## 事件
2009年5月，Ryan Dahl 在 JSConf EU 發表 **Node.js**：以 Chrome 的 V8 引擎為核心，加上**事件迴圈（event loop）與非同步 I/O**，讓 JavaScript 第一次能在伺服器端執行。

## 為何重要
- **JavaScript 成為通用語言**：前後端同一語言，全端開發（full-stack）的概念由此誕生。
- **事件驅動、非阻塞 I/O 模型**：以單執行緒事件迴圈處理大量併發連線，對比 Apache 的 thread-per-request 模型，在 I/O 密集場景效率驚人。
- Node.js 的成功反過來**迫使 TC39 加速語言演進**：伺服器端程式碼需要模組、類別、Promise——直接催生了 ES6（見 [2015-ES6現代化的黎明](2015-ES6現代化的黎明.md)）。
- Node 內建 **CommonJS 模組系統（`require`）**，首度讓 JavaScript 有正式的模組機制（瀏覽器要等到2015年的 ESM）。

## 理論與實用原因
- **理論原因**：Dahl 觀察到傳統伺服器用執行緒處理併發，切換成本高且程式設計困難；他借用 libev/libuv 的事件迴圈理論，證明「單執行緒 + 非同步回呼」可達到極高併發。
- **實用原因**：V8 剛好出現且開源、效能極強；JavaScript 沒有 I/O 函式庫包袱，適合從零設計非阻塞 API（`fs.readFile(path, callback)` 風格）。

## 彌補了什麼缺陷
彌補了 JavaScript「只能在瀏覽器沙箱執行、無檔案與網路 I/O、無模組系統」的缺陷；也彌補了伺服器端「執行緒模型在 C10K（萬級併發）問題上的低效率」。

## 後續影響
- 2010年 npm 問世（見 [2010-npm套件管理生態](2010-npm套件管理生態.md)），生態爆發。
- Express、React、webpack、Electron 等整個現代前端工具鏈都建立在 Node 之上。
- Ryan Dahl 本人在2018年反思 Node 的缺陷，創造了 Deno（見 [2018-Deno構想](2018-Deno構想.md)）。

## 程式範例

### 1. Node 的Hello World：JavaScript 第一次當伺服器

```js
// 2009年 Ryan Dahl 的原始示範
var http = require("http");            // CommonJS 模組（瀏覽器沒有的第一個能力）
http.createServer(function (req, res) {
  res.writeHead(200, { "Content-Type": "text/plain" });
  res.end("Hello World\n");
}).listen(1337);
console.log("Server running at http://127.0.0.1:1337/");
```

### 2. 非阻塞 I/O：回呼風格（當時的唯一選擇）

```js
// 非同步讀檔：不阻塞事件迴圈
var fs = require("fs");
fs.readFile("/etc/hosts", function (err, data) {   // error-first callback
  if (err) throw err;
  console.log(data.toString());
});
console.log("先執行到這裡");                        // 非同步：這行先印出
```

### 3. 回呼地獄：催生 ES6 Promise 的真實痛苦

```js
// 三層相依的非同步操作——ES3/ES5 時代的噩夢
fs.readFile("config.json", function (err, cfg) {
  if (err) return handleError(err);
  db.connect(JSON.parse(cfg).url, function (err, conn) {
    if (err) return handleError(err);
    conn.query("SELECT * FROM users", function (err, rows) {
      if (err) return handleError(err);
      // 錯誤要層層檢查、巢狀越來越深……
    });
  });
});
// 這段程式碼的痛苦 → Promise（ES6）→ async/await（ES2017）
```

### 4. 單執行緒事件迴圈的併發能力（C10K 問題的解方）

```js
// 一個執行緒處理萬級併發——對比 Apache 的 thread-per-request
http.createServer(function (req, res) {
  setTimeout(function () { res.end("ok"); }, 5000);  // 等待中不佔執行緒
}).listen(1337);
// 萬個連線同時等待，仍然只用一個執行緒
```
