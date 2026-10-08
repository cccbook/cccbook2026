# 1999：IE 5 首創 XMLHttpRequest

## 事件
1999年3月，微軟在 **Internet Explorer 5** 中以 ActiveX 元件形式推出 **XMLHTTP**（開發者後來稱 XMLHttpRequest / XHR）。它是微軟 **Outlook Web Access** 團隊（Alex Hopmann 等人）為了讓 Web 版 Outlook 能「不換頁就收發郵件」而創造的。

## 為何重要
- **史上第一個「不換頁就能向伺服器取得資料」的瀏覽器 API**：在此之前，任何伺服器互動都必須整頁重新載入。
- 微軟以 IE 專屬 ActiveX 形式實作（`new ActiveXObject("Microsoft.XMLHTTP")`），其他瀏覽器要等到 **2006年** 才以 `XMLHttpRequest` 原生物件跟進（Firefox 1.0、Safari 1.2 等）。
- 它是七年後 **Ajax 革命（2005）** 的技術基礎（見 [2005-Ajax革命](2005-Ajax革命.md)）——Jesse James Garrett 命名 "Ajax" 時的核心就是這個物件。

## 理論與實用原因
- **理論原因**：突破「HTTP 請求 = 整頁換新」的 Web 基本模型，實現「局部更新」（partial page update）——應用程式思維（desktop-like）進入瀏覽器。
- **實用原因**：Outlook Web Access 若每次收信都要整頁重載，體驗完全無法與桌面 Outlook 競爭；Exchange 團隊需要「背景取回 XML 資料」的能力。

## 彌補了什麼缺陷
彌補了 Web「每個互動都要整頁重載、無法做局部非同步更新」的根本缺陷。諷刺的是，這個改變 Web 命運的 API 是 IE 專屬擴充策略的產物——微軟沒有標準化它，最終反被開放實作（其他瀏覽器）與 Ajax 生態（主要建立在 Firefox/Chrome 上）收割了成果。

## 相關條目
- [2005-Ajax革命](2005-Ajax革命.md)
- [1996-JScript大戰與瀏覽器相容性危機](1996-JScript大戰與瀏覽器相容性危機.md)

## 程式範例

IE 5 的 XMLHTTP：史上第一次「不換頁取得伺服器資料」：

```js
// 1999年，IE 5 專屬：ActiveX 元件
var xhr = new ActiveXObject("Microsoft.XMLHTTP");
xhr.open("GET", "/inbox.xml", true);  // true = 非同步
xhr.onreadystatechange = function () {
  if (xhr.readyState === 4) {          // 4 = 完成
    var doc = xhr.responseXML;         // XML 要透過 DOM API 層層取出
    var subject = doc.getElementsByTagName("subject")[0].firstChild.nodeValue;
    updateInbox(subject);              // 局部更新，不換頁！
  }
};
xhr.send();
```

六年後其他瀏覽器的標準化版本（2006）：

```js
var xhr = new XMLHttpRequest();        // 原生物件，不用 ActiveX
xhr.open("GET", "/inbox.json", true);
xhr.onload = function () {
  var data = JSON.parse(xhr.responseText);  // JSON 直接是物件（2001 後）
  updateInbox(data.subject);
};
xhr.send();
```

注意 1999 版的兩個缺陷：ActiveX 偵測分支 + XML 需透過 DOM 解析——後來分別由標準化 XHR 與 JSON 解決。
