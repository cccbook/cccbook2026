# 2002：Phoenix 專案——Firefox 的前身

## 事件
2002年9月，Mozilla 社群內部的 Blake Ross 與 Dave Hyatt 啟動 **Phoenix** 專案（因商標問題先更名 Firebird，2004年定名 **Firefox**），目標是做出一個「輕量、快速、只做瀏覽器該做的事」的獨立瀏覽器，擺脫 Mozilla Suite 的龐雜。

## 為何重要
- Firefox 1.0（2004）在上市一年內衝上市佔約30%，證明 IE 壟斷可以被打破。
- Firefox 帶來**分頁瀏覽普及化、彈出視窗封鎖、擴充套件生態**，並大幅改善對 W3C DOM 標準的支援，讓「跨瀏覽器 JavaScript」第一次變得可行。

## 理論與實用原因
- **實用原因**：IE 6 長期不更新（2001–2006間無重大改版），開發者飽受 IE 專屬語法（如 `document.all`、`attachEvent`）與標準缺失之苦。
- **理論原因**：Mozilla 堅持實作 W3C 標準而非微軟的「Embrace, extend, extinguish」策略，讓 DOM Level 2 事件模型（`addEventListener`）成為事實標準。

## 彌補了什麼缺陷
彌補了 IE 時代 JavaScript 開發體驗的缺陷：除錯只能靠 `alert()`、無主控台。Firefox 的 **Firebug 擴充套件（2006）** 開創了現代開發者工具（DevTools）的典範，後來被所有瀏覽器模仿。

## 相關條目
- [2004-Firefox-1-0問世](2004-Firefox-1-0問世.md)
- [2008-Chrome問世與V8引擎](2008-Chrome問世與V8引擎.md)

## 程式範例

Phoenix/Firefox 堅持 W3C DOM 2 標準，讓「跨瀏覽器」第一次變得可行：

```js
// 標準事件模型（Firefox 忠實實作，IE 要等很久才跟上）
function onClick(e) {        // W3C：事件物件用參數傳入，this 指向元素
  e.preventDefault();        // 標準的取消預設行為
  console.log(this.id);
}
element.addEventListener("click", onClick, false);      // 標準
element.attachEvent("onclick", function () { ... });    // IE 專屬對照
```

以及 Firebug（2006）開創的 DevTools 範例：

```js
// Firebug 之前（IE 6 時代）：只有 alert
alert(user.profile.email);

// Firebug 之後：主控台 + 物件檢視器 + 斷點
console.log(user.profile.email);   // 物件可展開檢視
console.table(users);              // 表格化顯示
debugger;                          // 中斷點，逐步執行
```

這套 console API 後來成為所有瀏覽器（Chrome、Safari）的標配，也是開發者工具（DevTools）的雛形。
