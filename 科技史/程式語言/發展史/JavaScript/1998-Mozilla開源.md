# 1998：Mozilla 開源與自由軟體瀏覽器之路

## 事件
1998年1月，面對微軟 IE 的猛烈攻勢（IE 已靠 Windows 綁定逆轉市佔），Netscape 宣布**開放 Navigator 程式碼**，成立 mozilla.org。這是史上第一個大型商業軟體開源化的案例之一。

## 為何重要
- 開源的程式碼庫後來重寫為 Gecko 引擎，成為 **Firefox**（2004）的核心。
- Mozilla 成立後持續推動網頁標準（CSS、DOM、ECMAScript），並在2003年推出 **Firebird/Thunderbird**，2004年推出 Firefox 1.0。

## 理論與實用原因
- **實用原因**：Netscape 市佔崩盤，閉源商業模式已無法與微軟競爭；開源能動員社群維持瀏覽器多元性。
- **理論原因**：呼應「網路必須是開放平台」的信念——瀏覽器若被單一廠商壟斷，網頁標準（包括 JavaScript）就會碎片化。

## 彌補了什麼缺陷
彌補了瀏覽器市場單一壟斷（IE 6 一度市佔95%以上）造成的創新停滯與標準碎片化問題。Firefox 2004年的問世直接促成第二次瀏覽器大戰，也間接刺激 Google 開發 Chrome（2008）。

## 相關條目
- [2002-Mozilla與Firefox之路](2002-Mozilla與Firefox之路.md)（Phoenix 專案）
- [2004-Firefox-1-0問世](2004-Firefox-1-0問世.md)

## 程式範例

開源化後，Gecko 引擎的「標準優先」哲學可以用一個例子說明——W3C DOM Level 2 事件模型：

```js
// Gecko（Mozilla/Firefox）忠實實作 W3C 標準
element.addEventListener("click", (e) => {
  e.preventDefault();        // 標準介面：事件物件由參數傳入
  console.log(e.target.id);  // e.target 指向實際目標
}, false);

// 同期 IE 的專屬實作（標準缺席的對照組）
element.attachEvent("onclick", function () {
  window.event.returnValue = false;   // IE：全域 event、無 preventDefault
  console.log(window.event.srcElement.id);
});
```

Firefox 推出後，「標準碼」逐漸成為主流； Gecko 的實作更成為標準測試的基準——這正是「標準優先的開源瀏覽器」對 JavaScript 生態的最大貢獻：**語言與 API 的演進不由單一廠商決定**。
