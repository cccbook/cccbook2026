# 2017：ECMAScript 2017——async/await

## 事件
2017年6月，**ECMAScript 2017（ES8）** 發佈。最大亮點是 **async/await**，這是 JavaScript 非同步程式設計的終極範式。

## 新語法與特性

### 1. async/await
- **為何加入**：Promise（ES6）解決了回呼地獄，但 `.then().then().catch()` 鏈仍不像同步程式碼，且在條件分支與迴圈中難以組合。
- **理論原因**：源自 **C# 5（2012）** 的 async/await 設計（微軟 Anders Hejlsberg 團隊），其底層是 **協程（coroutine）** 與狀態機理論——`await` 把函數暫停，完成後恢復。JavaScript 的實作將 async 函數降級為 **generator + Promise 狀態機**。
- **實用原因**：`const data = await fetch(url)` 與同步寫法一樣直觀；try/catch 可以直接捕捉非同步錯誤（Promise 鏈做不到的統一錯誤處理）。
- **彌補缺陷**：Promise 鏈「不像同步程式碼」的可讀性缺陷，以及非同步錯誤處理無法用 try/catch 統一的缺陷。

### 2. 共享記憶體與 Atomics（SharedArrayBuffer、Atomics）
- **為何加入**：Web Worker 之間無法共享記憶體，只能用 postMessage 複製資料。
- **理論原因**：引入正式的**記憶體模型（memory model）**——ECMAScript 首次定義多執行緒的 happens-before 關係，借鑑 Java Memory Model。
- **實用原因**：高效能計算（WebAssembly、影像處理、遊戲引擎）需要零複製的共享記憶體。
- **彌補缺陷**：Worker 間資料只能複製的效能缺陷。（2018年因 Spectre 漏洞一度停用，2020年以 COOP/COEP 安全條件恢復。）

### 3. Object.values / Object.entries
- **為何加入**：ES5 只有 `Object.keys`，取值或鍵值對要手寫迴圈。
- **實用原因**：`Object.entries` 與 `Object.fromEntries`（2019）對稱，是物件↔陣列轉換的標準路徑。
- **彌補缺陷**：物件遍歷 API 的不完整。

### 4. 字串補白（padStart / padEnd）
- **為何加入**：格式化（對齊、補零）以前要手寫迴圈或 regex。
- **實用原因**：日期補零（`'05'.padStart(2, '0')`）、表格對齊是最常見需求。
- **彌補缺陷**：字串格式化工具缺失。

### 5. 函數參數尾逗號（trailing commas）
- **為何加入**：物件與陣列字面量早允許尾逗號，函數參數不允許造成 diff 噪音。
- **實用原因**：版本控制 diff 只顯示「新增一行」而非「修改一行」。
- **彌補缺陷**：語法規則不一致與維護摩擦。

## 理論總結
ES2017 的主軸是「**非同步的終局**」：從回呼（1995）→ Promise（2015）→ async/await（2017），歷經22年，JavaScript 終於有了既強大又可讀的非同步範式。借用 C# 的成熟設計而非自行發明，是「語言間彼此學習」的典範。

## 實用總結
async/await 與後來的頂層 await（2022）徹底改寫了 Node.js API 的設計方向——Deno（2020）甚至直接以「全 Promise API」為核心（見 [2020-Deno-1-0問世](2020-Deno-1-0問世.md)）。

## 相關條目
- [2015-ES6現代化的黎明](2015-ES6現代化的黎明.md)
- [2022-ES2022頂層await與類別欄位](2022-ES2022頂層await與類別欄位.md)

## 程式範例

### 1. async/await：非同步程式碼像同步一樣直觀

```js
// ES6 Promise 鏈：可讀但不像同步碼
function loadUser() {
  return fetch("/api/config")
    .then((res) => res.json())
    .then((cfg) => fetch(cfg.userUrl))
    .then((res) => res.json())
    .then((user) => fetch(user.avatarUrl))
    .then((res) => res.json());
}

// ES2017：async/await——三次請求寫成三行同步風格
async function loadUser() {
  const cfg = await (await fetch("/api/config")).json();
  const user = await (await fetch(cfg.userUrl)).json();
  const avatar = await (await fetch(user.avatarUrl)).json();
  return avatar;
}
```

### 2. try/catch 統一捕捉非同步錯誤（Promise 鏈做不到）

```js
async function load() {
  try {
    const res = await fetch("/api");   // 網路錯誤
    const data = await res.json();     // 解析錯誤——同一個 try 捕捉
  } catch (err) {
    console.error(err);                // 所有非同步錯誤都在這裡
  } finally {
    hideLoading();                     // 無論成敗都執行
  }
}
```

### 3. 迴圈與條件中 await（Promise 鏈很難寫）

```js
async function loadPages(pages) {
  const results = [];
  for (const p of pages) {
    if (p.enabled) {                         // 條件分支中 await——鏈式寫法幾乎不可能
      results.push(await (await fetch(p.url)).json());
    }
  }
  return results;
}
```

### 4. SharedArrayBuffer 與 Atomics：Worker 間共享記憶體

```js
// 主執行緒
const sab = new SharedArrayBuffer(8);
const arr = new Int32Array(sab);
worker.postMessage(sab);              // 零複製共享（以前 postMessage 是複製）

// Worker 執行緒
Atomics.add(arr, 0, 1);               // 原子操作，借用 Java Memory Model 語義
```

### 5. 字串補白與尾逗號

```js
"5".padStart(2, "0");     // "05"——日期補零
"7".padEnd(3, ".");       // "7.."
function f(a, b,) {}      // 參數尾逗號：diff 只顯示「新增一行」
```
