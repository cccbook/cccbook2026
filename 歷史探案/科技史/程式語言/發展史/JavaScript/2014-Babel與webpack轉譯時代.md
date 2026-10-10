# 2014：Babel 與 webpack——轉譯與打包時代

## 事件
2014年，**6to5**（後更名 **Babel**）與 **webpack** 相繼問世：
- **Babel**：將 ES6+ 新語法轉譯（transpile）為 ES5，讓開發者立刻使用尚不支援的新特性。
- **webpack**：模組打包器，將 CommonJS/AMD/ESM 模組與資源打包成瀏覽器可用的檔案。

## 為何重要
- **解決了「語言演進」與「瀏覽器支援落差」的矛盾**：ES6（2015）的語法再新，使用者瀏覽器不一定支援；Babel 讓「使用新語法」與「相容舊瀏覽器」同時成立。
- **轉譯文化改變語言政治**：提案尚未標準化即可用 Babel 試用（如 decorator、optional chaining），形成「社群先試、TC39 後收」的新模式，加速了語言演進。
- **webpack 統一模組戰國**：終結了 CommonJS vs AMD vs RequireJS 之爭，`import/export`（ESM）得以在舊環境落地。
- 後繼者 Rollup（2015，tree-shaking）、Parcel（2017）、**esbuild（2020，Go 重寫，快百倍）**、**Vite（2020，見 [2020-Vite新一代建構工具](2020-Vite新一代建構工具.md)）** 不斷重寫效率極限。

## 理論與實用原因
- **理論原因**：編譯器的「語法糖降級（desugaring）」理論——新語法只是舊語法的組合（如 `class` 降級為 `prototype` 操作、`async/await` 降級為 generator+Promise 狀態機），所以任何新語法理論上都可轉譯。
- **實用原因**：IE 8/9 存活到2015年之後；企業使用者無法升級，開發者卻想用新語法，轉譯是唯一解。

## 彌補了什麼缺陷
彌補了「標準演進慢、瀏覽器碎片化」造成的新語法落地延遲；也彌補了瀏覽器原生沒有模組系統時期的相依管理缺陷。

## 相關條目
- [2015-ES6現代化的黎明](2015-ES6現代化的黎明.md)
- [2012-TypeScript問世](2012-TypeScript問世.md)

## 程式範例

### 1. 轉譯理論：新語法只是舊語法的「降級」

```js
// ES6 class（新語法）
class Point {
  constructor(x, y) { this.x = x; this.y = y; }
  sum() { return this.x + this.y; }
}
```

```js
// Babel 轉譯出的 ES5：本質是 prototype 操作（語法糖降級）
"use strict";
var Point = (function () {
  function Point(x, y) { this.x = x; this.y = y; }
  Point.prototype.sum = function () { return this.x + this.y; };
  return Point;
})();
```

```js
// async/await 也是降級：generator + Promise 狀態機
async function load() {
  const res = await fetch("/api");
  return res.json();
}
// 降級為：_regeneratorRuntime + switch 狀態機 + Promise.then 鏈
```

### 2. Babel 設定：新語法與舊瀏覽器同時成立

```json
{
  "presets": [["@babel/preset-env", { "targets": "> 0.25%, not dead" }]]
}
```

### 3. webpack：模組戰國的統一

```js
// webpack.config.js
module.exports = {
  entry: "./src/index.js",
  output: { filename: "bundle.js" },
  module: {
    rules: [
      { test: /\.js$/, use: "babel-loader" },   // Babel 掛進打包流程
      { test: /\.css$/, use: ["style-loader", "css-loader"] }  // CSS 也是模組
    ]
  }
};
// index.js 中 import 的所有模組（JS/CSS/圖片）打包成單一 bundle.js
import { add } from "./math";   // ESM 語法，瀏覽器不支援也能用
```
