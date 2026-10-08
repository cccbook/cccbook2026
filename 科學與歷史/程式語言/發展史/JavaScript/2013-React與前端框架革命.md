# 2013：React 與前端框架革命

## 事件
2013年5月，Facebook 開源 **React**（Jordan Walke 基於內部 FaxJS 專案）。同年 AngularJS（2010年發佈）已成主流，Ember、Backbone 等框架群雄並起，前端進入**框架時代**。

## 為何重要
- **宣告式 UI + 虛擬 DOM（Virtual DOM）**：以 `render(state) => UI` 的函數式思維取代手動操作 DOM，徹底改變前端開發範式。
- **JSX 語法**：在 JavaScript 中內嵌 HTML，打破「結構與邏輯分離」的傳統教條，引發巨大爭議但最終獲勝——它證明「UI 即函數的回傳值」更符合組合原理。
- **單向資料流與不可變狀態**：催生了 Redux（2015）、狀態管理生態，也影響 ES2015 之後語言層面的不可變資料思維。
- React 的 **Hooks（2019）** 讓函數元件與狀態、副作用共存，是函數式程式設計進入主流的最大案例。

## 理論與實用原因
- **理論原因**：源自函數式反應式程式設計（FRP，Conal Elliott 1997）——UI 是狀態的純函數，狀態改變自動重算。
- **實用原因**：Facebook 的廣告管理介面 DOM 操作複雜到失控；直接操作 DOM 的命令式程式碼在狀態多時必然出現「UI 與資料不一致」的 bug。

## 彌補了什麼缺陷
彌補了原生 JavaScript「手動 DOM 操作繁瑣、狀態與畫面易失同步、程式碼不可預測」的缺陷，也彌補了 jQuery 時代「事件綁定散落各處、難以測試」的架構問題。

## 相關條目
- [2014-Babel與webpack轉譯時代](2014-Babel與webpack轉譯時代.md)
- [2015-ES6現代化的黎明](2015-ES6現代化的黎明.md)

## 程式範例

### 1. 命令式（jQuery/原生）vs 宣告式（React）

```js
// 2005–2013：命令式 DOM 操作——狀態與畫面易失同步
var count = 0;
document.getElementById("btn").addEventListener("click", function () {
  count++;
  document.getElementById("label").textContent = count;  // 手動同步 UI
});
```

```jsx
// React：宣告式——UI 是 state 的純函數，狀態改變自動重算
function Counter() {
  const [count, setCount] = React.useState(0);   // Hooks（2019）
  return (
    <button onClick={() => setCount(count + 1)}>
      點了 {count} 次
    </button>
  );
}
// 不用碰 DOM——React 自己算出虛擬 DOM 的差異並更新
```

### 2. JSX：在 JS 中內嵌 HTML（打破結構與邏輯分離的教條）

```jsx
const items = ["math", "code"];
const list = (
  <ul>
    {items.map((t) => (
      <li key={t}>{t}</li>       // JSX 本質是函數呼叫：React.createElement("li", ...)
    ))}
  </ul>
);
```

### 3. 單向資料流與不可變更新

```js
// Redux 風格：state 不可變——這催生了 ES2018 的物件展開運算子
function reducer(state, action) {
  switch (action.type) {
    case "increment":
      return { ...state, count: state.count + 1 };  // 回傳新物件，不改舊的
    default:
      return state;
  }
}
```

### 4. XSS 的解方：JSX 預設跳脫

```jsx
const userInput = '<script>alert("xss")</script>';
<div>{userInput}</div>   // React 自動跳脫為純文字——innerHTML 時代的 XSS 缺陷消失
```
