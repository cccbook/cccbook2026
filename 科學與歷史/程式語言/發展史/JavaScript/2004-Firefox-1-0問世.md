# 2004：Firefox 1.0 問世

## 事件
2004年11月9日，Mozilla 基金會發佈 **Firefox 1.0**，上市首年下載量破億，市佔率從不到5%攀升至兩位數，終結了 IE 6 的絕對壟斷。

## 為何重要
- **第二次瀏覽器大戰開打**，瀏覽器重新進入快速迭代時代。
- Firefox 對 **W3C 標準（DOM 2、CSS 2）的忠實實作**，加上2006年的 Firebug 除錯工具，讓 Ajax 應用（見 [2005-Ajax革命](2005-Ajax革命.md)）的開發從「地獄模式」變成可行。
- Firefox 的 **XPCOM/XUL 擴充套件機制**是最早的「用 JS 打造平台生態」實驗，啟發了後來的瀏覽器擴充與 Node.js 模組思維。

## 理論與實用原因
- **實用原因**：網頁開發者與使用者苦 IE 6 安全漏洞與停滯已久；市場需要一個現代替代品。
- **理論原因**：Mozilla 證明「標準優先 + 社群開發」可以對抗商業壟斷，確保 JavaScript 的演進不由單一公司決定。

## 彌補了什麼缺陷
彌補了2001–2004年間瀏覽器創新停滯、JavaScript 語言本身也因 ES4 內戰而凍結的「雙重停滯」——Firefox 用標準實作讓既有 ECMAScript 3 的能力（見 [1999-ECMAScript3正則表達式與例外處理](1999-ECMAScript3正則表達式與例外處理.md)）真正發揮出來。

## 相關條目
- [2008-Chrome問世與V8引擎](2008-Chrome問世與V8引擎.md)

## 程式範例

Firefox 時代的標準實作，與 IE 專屬寫法的對照：

```js
// 阻止預設行為：兩個世界
function handler(e) {
  // W3C 標準（Firefox 正確實作）
  e.preventDefault();
  e.stopPropagation();

  // IE 專屬（return false 存在 window.event returnValue）
  window.event.returnValue = false;
  window.event.cancelBubble = true;
}
```

以及 Firefox 的 XUL 擴充套件機制——最早的「JS 打造平台生態」實驗：

```xml
<!-- Firefox 擴充套件的 XUL 介面（XML-based UI） -->
<toolbarbutton id="my-button" label="我的按鈕" oncommand="alert('hi')" />
```

XPCOM/XUL 後來被更簡單的 WebExtensions API 取代，但「瀏覽器是可程式化平台」的概念由此確立——影響了 Chrome 擴充、Node 模組與 Electron 的設計。
