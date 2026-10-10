# 2012：TypeScript 問世——靜態型別回到 JavaScript

## 事件
2012年10月，微軟的 Anders Hejlsberg（Turbo Pascal、C# 之父）發佈 **TypeScript**：JavaScript 的超集，加上**靜態型別、介面、泛型與型別推論**，編譯後輸出純 JavaScript。

## 為何重要
- **解決 JavaScript 最大的工程化缺陷**：動態型別在小型腳本中靈活，但在數十萬行的大型專案中，型別錯誤只能在執行期發現。
- **漸進式型別（gradual typing）**：型別是可選的（`any` 逃逸口），讓既有 JS 專案可以逐步遷移——這是它在與 Dart、CoffeeScript 的競爭中勝出的關鍵。
- TypeScript 的型別系統**反哺語言**：ES6 的 class、ES2020 的 optional chaining 等提案都先在 TypeScript 生態驗證；`enum`、decorator 等則成為未來提案的試驗場。
- 2018年起，主流框架（Angular 全面採用、React/Vue 提供型別支援）皆以 TypeScript 為一等公民。

## 理論與實用原因
- **理論原因**：基於 Hindley–Milner 型別推論與漸進式型別理論（Siek & Taha, 2006）——「型別標註由程式設計師逐步補齊，推論器補其餘」。
- **實用原因**：微軟內部大型 Web 專案（後來的 Office Online、VS Code）飽受執行期型別錯誤之苦；「編譯期捕捉錯誤 + IDE 自動補全」的開發體驗收益巨大。

## 彌補了什麼缺陷
彌補了 JavaScript「無靜態型別、重構困難、IDE 補全無力、介面契約只能靠文件」的缺陷，同時保持與 JS 的完全互通（這正是純新語言 Dart 做不到的）。

## 相關條目
- [2015-ES6現代化的黎明](2015-ES6現代化的黎明.md)
- [2014-Babel與webpack轉譯時代](2014-Babel與webpack轉譯時代.md)

## 程式範例

### 1. 執行期錯誤 vs 編譯期捕捉

```js
// 純 JavaScript：錯誤在執行期才發現
function greet(user) {
  return "Hello, " + user.name.toUpperCase();  // user 為 null 時 → 執行期 TypeError
}
greet(null);  // 💥 上線後才爆

// TypeScript：編譯期就擋下
function greet(user: { name: string }) {
  return "Hello, " + user.name.toUpperCase();
}
greet(null);         // ❌ 編譯錯誤：Argument of type 'null' is not assignable
greet("Ada");        // ❌ 編譯錯誤：字串沒有 name 屬性
greet({ name: "Ada" }); // ✅
```

### 2. 介面與型別推論

```ts
interface User {
  name: string;
  age?: number;              // ? = 可選屬性
  tags: string[];
}

const user = { name: "Ada", age: 36, tags: ["math"] };  // 型別自動推論
user.age = "36";           // ❌ 編譯錯誤：型別不符

function first<T>(arr: T[]): T | undefined {  // 泛型
  return arr[0];
}
first(["a", "b"]);         // string | undefined —— 回傳型別自動推論
```

### 3. 漸進式型別：any 逃逸口讓舊專案可逐步遷移

```ts
// 舊 JS 程式碼直接改名 .ts 也能編譯（隱式 any）
function legacy(data) { return data.whatever; }

// 逐步補上型別
function legacy(data: unknown): string {
  return String(data.whatever);
}
```

### 4. 產出仍是純 JavaScript（與 Dart 的勝負關鍵）

```bash
tsc greet.ts   # 編譯輸出 greet.js——任何瀏覽器/Node 都能跑
```
