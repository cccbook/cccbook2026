# 1996：VBScript 問世

## 事件
1996年8月，微軟隨 **Internet Explorer 3** 推出 **VBScript**——以 Visual Basic 語法為基礎的瀏覽器腳本語言，用於在 IE 中取代/對抗 JavaScript。同時期也被廣泛用於經典 ASP 伺服器端腳本。

## 為何重要
- **微軟語言生態的延伸**：讓數百萬 VB/VBA 程式設計師能直接寫網頁腳本，降低學習門檻。
- **伺服器端腳本的先驅**：經典 ASP 的預設語言是 VBScript，是「在伺服器端用腳本語言生成網頁」的早期大規模實踐——比 Node.js（2009）早了13年。
- **與 JScript 並列於 IE**：IE 3 同時支援 VBScript 與 JScript，進一步加劇瀏覽器腳本碎片化。

## 理論與實用原因
- **理論原因**：BASIC 的設計哲學——「初學者的通用符號指令碼」，語法接近自然語言（`If ... Then ... End If`）。
- **實用原因**：微軟要讓自家龐大的 VB 開發者社群直接轉移到 Web 平台。

## 為何失敗
1. **只有 IE 支援**：Netscape（市佔仍高）與後來的 Firefox、Chrome 拒絕實作，VBScript 寫的網頁在其他瀏覽器直接失效。
2. **安全問題**：VBScript 可存取 ActiveX 物件，成為巨集病毒與網頁蠕蟲（如 ILOVEYOU 病毒，2000）的載體。
3. **瀏覽器大戰落幕**：IE 獲勝後微軟不再積極開發；IE 11（2017後）逐步移除 VBScript，2020年代完全淘汰。

## 彌補了什麼缺陷
彌補了 VB 開發者進入 Web 的學習曲線缺口，以及 ASP 時代「伺服器端動態網頁」的需求。它的失敗也反證了一件事：**跨瀏覽器支援是腳本語言的生死線**——JavaScript 因 ECMAScript 標準化存活，VBScript 因封閉而消亡。

## 相關條目
- [1996-JScript大戰與瀏覽器相容性危機](1996-JScript大戰與瀏覽器相容性危機.md)
- [1997-ECMAScript1標準化](1997-ECMAScript1標準化.md)

## 程式範例

### 1. 瀏覽器端：VBScript 與 JavaScript 的語法對照

```vbscript
' VBScript：BASIC 風格，接近自然語言
Function Validate(form)
  If form.Email.Value = "" Then
    MsgBox "Email 不可為空"
    Validate = False
  Else
    Validate = True
  End If
End Function
```

```js
// JavaScript：C 風格，符號密集
function validate(form) {
  if (form.Email.value === "") {
    alert("Email 不可為空");
    return false;
  }
  return true;
}
```

### 2. 伺服器端：經典 ASP 的 VBScript（比 Node.js 早13年的伺服器腳本）

```vbscript
<%
' ASP 頁面：伺服器端執行，動態生成 HTML
Dim name
name = Request.QueryString("name")
Response.Write "<h1>Hello, " & name & "</h1>"
%>
```

### 3. 致命傷：VBScript 可驅動 ActiveX → 病毒溫床

```vbscript
' ILOVEYOU 病毒（2000）的核心手法：VBScript 操作檔案系統與 Outlook
Set fso = CreateObject("Scripting.FileSystemObject")
fso.CopyFile WScript.ScriptFullName, "C:\LOVE-LETTER-FOR-YOU.TXT.vbs"
```

同樣的事，JavaScript 在瀏覽器沙箱中做不到（無檔案存取）——這正是 JavaScript 存活、VBScript 消亡的技術分水嶺。
