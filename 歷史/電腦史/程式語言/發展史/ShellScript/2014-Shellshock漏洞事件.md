# 2014：Shellshock 漏洞事件

## 事件
2014 年 9 月，安全研究人員 **Stéphane Chazelas** 發現 **Shellshock**（CVE-2014-6271 系列漏洞）——bash 中存在**超過 25 年**的遠端程式碼執行漏洞。全球數百萬台伺服器、路由器、IoT 裝置暴露在風險中，CVE 嚴重程度評分為 10/10。

## 漏洞的技術原理

### 1. 環境變數中的函數匯出
- **原理**：bash 支援把 shell 函數透過環境變數匯出給子行程（`export -f`）。實作上，函數以環境變數的形式傳遞，bash 啟動時會把形如 `BASH_FUNC_xxx=() { ... }` 的環境變數**當作函數定義執行**。
- **缺陷**：變數值後面若附加其他命令，會被一併執行——環境變數從「資料」變成了「程式碼」。
- **彌補缺陷（歷史）**：這個機制原本是為了讓子 bash 繼承父 bash 的函數（1980 年代的合理需求），但 25 年後在 CGI、DHCP、SSH 等新環境中成了致命入口。

### 2. CGI 時代的災難性放大
- **實用原因**：Web 伺服器的 CGI 介面把 HTTP Header 直接放進環境變數，遠端攻擊者只需送一個精心構造的 Header 就能執行任意命令。
- **彌補缺陷（反向）**：這暴露了「shell 是系統膠水」的代價——任何把不可信輸入送進 shell 的介面都是攻擊面。

## 修補與理論教訓

### 1. 修補（2014 年多輪）
- bash 陸續發佈多個修補版本，最終改為以**專用編碼**傳遞函數，且不再把環境變數後綴的內容當作程式碼執行。
- **理論教訓**：**資料與程式碼必須分離**（data/code separation）——這是程式語言設計的最基本原則，shell 的「字串即命令」傳統正是這原則的長期違反。

### 2. 語言設計的教訓
- **彌補缺陷**：Shellshock 證明了「把不可信輸入交給 shell」是危險的，催生了：
  - 更安全的替代（`execve` 直接呼叫、避免 shell 層的設計指南）
  - 容器時代的最小化 shell（Docker 影像移除 shell、distroless）
  - 結構化 shell 的安全論證（nushell 等）

## 程式範例：漏洞的重現與修補

```bash
# 漏洞重現：環境變數從「資料」變成「程式碼」
env X='() { :;}; echo VULNERABLE' bash -c "echo safe"
# 輸出：VULNERABLE   ← 變數後綴的命令被執行了！
# （修補後的 bash 只輸出 safe）
```

```bash
# CGI 攻擊示意：HTTP Header 進入環境變數
# 攻擊者送出：
#   User-Agent: () { :;}; /bin/cat /etc/passwd > /tmp/pwned
# Web 伺服器把 Header 放進環境變數 → CGI 腳本呼叫 bash → 命令執行
```

```bash
# 正常函數匯出（1980 年代的合理需求，漏洞的根源）
myfunc() { echo "hello"; }
export -f myfunc
bash -c 'myfunc'     # 子 bash 繼承父 bash 的函數
```

```bash
# 修補後的專用編碼：資料與程式碼分離
env BASH_FUNC_myfunc%%='() { echo hello }' bash -c 'myfunc'
# bash 只認專用編碼格式，後綴的任意命令不再執行
```

```sh
# 防禦實務：避免把不可信輸入送進 shell
# 容器時代：distroless 影像根本沒有 shell
# FROM gcr.io/distroless/cc   ← 沒有 /bin/sh，攻擊面歸零
```

## 歷史意義
Shellshock 是 shell script 語言史上最大的安全事件，讓「25 年前的設計決策如何在 25 年後爆炸」成為經典案例。它也加速了「最小化 shell」與「結構化 shell」的潮流。

## 相關條目
- [1977-BourneShell-sh問世](1977-BourneShell-sh問世.md)
- [1988-Bash誕生](1988-Bash誕生.md)
- [2023-現代Shell競爭時代](2023-現代Shell競爭時代.md)
