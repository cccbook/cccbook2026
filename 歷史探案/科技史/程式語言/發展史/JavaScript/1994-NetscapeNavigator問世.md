# 1994：Netscape Navigator 問世

## 事件
1994年10月，Marc Andreessen 與 Jim Clark 創立的 Mosaic Communications（後更名 Netscape Communications）發佈 **Netscape Navigator 1.0**。它迅速成為市佔率超過80%的瀏覽器，是第一個「商業上成功」的圖形化瀏覽器。

## 為何重要
- Navigator 的爆發式成長讓網頁不再只是靜態文件，網景意識到**瀏覽器需要腳本語言**讓網頁「動起來」。
- 1994年底網景內部已有多種提案（包括 Java 小型版、Scheme 版），直接促成1995年 Brendan Eich 創造 JavaScript（見 [1995-JavaScript誕生](1995-JavaScript誕生.md)）。

## 理論與實用背景
- **實用原因**：當時表單驗證必須送回伺服器，在撥接網路下動輒數十秒。一個在瀏覽器端執行的語言可以立即驗證、立即反應。
- **理論原因**：Andreessen 提出「瀏覽器是作業系統」的願景——如果瀏覽器是平台，就必須有平台語言。

## 彌補了什麼缺陷
彌補了 HTML 完全靜態、無互動能力的缺陷；也彌補了使用者體驗上「每次互動都要往返伺服器」的延遲問題。

## 後續影響
- Navigator 的成功引來微軟的 Internet Explorer（1995，見 [1996-JScript大戰與瀏覽器相容性危機](1996-JScript大戰與瀏覽器相容性危機.md)），開啟第一次瀏覽器大戰。
- 1998年網景開源瀏覽器程式碼，成為 Mozilla 與後來 Firefox 的基礎。

## 程式範例

1994年前的世界：表單驗證必須往返伺服器（撥接網路下動輒數十秒）：

```html
<!-- 純 HTML 時代：驗證錯誤 → 整頁重載 → 才看到錯誤訊息 -->
<form action="/validate" method="POST">
  <input name="email" type="text">
  <input type="submit">  <!-- 按下去才發現錯，整頁重來 -->
</form>
```

Navigator 2.0 + JavaScript 後，驗證在瀏覽器端瞬間完成：

```html
<script>
function validate() {
  var email = document.forms[0].email.value;
  if (email.indexOf("@") === -1) {
    alert("Email 格式錯誤！");  // 不用重載頁面，立即反應
    return false;               // 取消表單送出
  }
  return true;
}
</script>
<form onsubmit="return validate()">
  <input name="email" type="text">
  <input type="submit">
</form>
```

這就是 JavaScript 誕生的原始動機——「把驗證從伺服器搬到使用者的瀏覽器裡」。
