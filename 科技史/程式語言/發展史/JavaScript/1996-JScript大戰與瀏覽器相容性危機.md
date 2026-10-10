# 1996：JScript 問世與第一次瀏覽器大戰

## 事件
1996年8月，微軟推出 **Internet Explorer 3**，內含逆向工程 Netscape JavaScript 而成的 **JScript**（商標問題使然，不能叫 JavaScript），同時推出 **VBScript**。同年瀏覽器大戰全面開打。

## 為何重要
- **JScript**：微軟在沒有授權的情況下逆向工程 JavaScript，兩種實作行為不一致，網頁開發者被迫寫「雙版本程式碼」——這是 JavaScript 歷史上最痛苦的碎片化時期。
- **碎片化的代價直接催生標準化**：網景把語言提交 ECMA International，1997年產生 ECMAScript 標準（見 [1997-ECMAScript1標準化](1997-ECMAScript1標準化.md)）。「JavaScript 是語言，ECMAScript 是標準」的格局由此確立。
- **第一次瀏覽器大戰（1995–2001）**：微軟將 IE 綁入 Windows、免費散佈、並推出 IE 專屬語法（`document.all`、`attachEvent`、`innerHTML`），迫使網景敗退。IE 專屬擴充成為日後「跨瀏覽器相容」噩夢的根源。
- 微軟同時在 IE 3 推出 **VBScript**（見 [1996-VBScript問世](1996-VBScript問世.md)），企圖以自家語言生態取代 JavaScript，但最終失敗。

## 理論與實用原因
- **理論原因**：微軟採取「Embrace, extend, extinguish（擁抱、擴充、消滅）」策略——先相容對手，再加專屬功能，最後讓標準失效。
- **實用原因**：IE 佔 Windows 平台優勢，網頁開發者以 IE 為第一目標，反過來讓 IE 專屬語法成為「事實標準」。

## 彌補了什麼缺陷
微軟本意是彌補「Windows 平台缺少網頁腳本語言」的缺口，但代價是製造了**跨瀏覽器相容性**這個更大的缺陷——直到1997年 ECMAScript 標準化、2000年代 W3C DOM 標準普及才逐步解決。

## 相關條目
- [1995-JavaScript誕生](1995-JavaScript誕生.md)
- [1996-VBScript問世](1996-VBScript問世.md)
- [2001-微軟反壟斷案與第一次瀏覽器大戰落幕](2001-微軟反壟斷案與第一次瀏覽器大戰落幕.md)

## 程式範例

碎片化的真實痛苦：同一段「找出元素」的程式碼要寫三個版本：

```js
// 1996年開發者的日常：偵測瀏覽器、分支處理
function findElement(id) {
  if (document.getElementById) {      // 標準路徑（W3C 後來採用）
    return document.getElementById(id);
  } else if (document.all) {          // IE 專屬（JScript 擴充）
    return document.all[id];
  } else if (document.layers) {       // Netscape 4 專屬
    return document.layers[id];
  }
}
```

事件綁定同樣分裂（IE 與標準語義不同）：

```js
// Netscape/W3C 標準
element.addEventListener("click", handler, false);
// IE 專屬：方法名不同、事件名有 "on" 前綴、this 指向 window
element.attachEvent("onclick", handler);
```

這種「每個 API 都要偵測分支」的噩夢，正是 ECMA 標準化（1997）與後來 jQuery（2006）存在的市場理由——jQuery 的核心價值就是「把上面的分支全部藏起來」。
