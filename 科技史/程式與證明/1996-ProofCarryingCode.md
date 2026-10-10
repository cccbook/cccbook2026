# 1996 Proof-Carrying Code：讓程式自帶不在場證明

> 案件編號：1996-PCC。報案人：作業系統與行動碼世界。案情：外來程式碼不可信，重驗一次又太貴。破案者：Necula 與 Lee。

## 案發現場

1990 年代中期，網路興起，Java applet、瀏覽器外掛、作業系統核心擴充四處流竄。主機收到一段陌生機器碼：它會不會竄改核心？會不會讀走機密？會不會除以零當機？

傳統對策有兩種，都不理想。軟體容錯隔離（SFI）用執行期檢查圍堵，付出效能代價；密碼簽章只能證明「誰寫的」，不能證明「是否安全」。核心需要的不是身分證，而是無罪證明。

1996 年，CMU 的 Necula 與 Lee 在 PLDI 與後續論文中報案並破案：與其讓主機重新驗證程式，不如讓程式「自帶證明」。主機只做一件便宜到不可能出錯的事：檢查證明。

這就是 Proof-Carrying Code（PCC，攜帶證明的程式碼）。

## 偵查過程（含數學式/表格/理論）

### 線索一：VCgen 把安全變成邏輯公式

偵探的第一步是定義安全政策（safety policy）。例如記憶體安全：「每次讀寫都在邊界內」；或控制流安全：「只跳到合法目標」。

程式發布者先對程式標註前後條件與迴圈不變式，再用驗證條件產生器（VCgen）算出驗證條件 $V_c$ 。主機的安全政策記為 $Safe$ 。程式安全當且僅當：

$$
\models V_c \Rightarrow Safe
$$

白話：驗證條件邏輯蘊含安全政策。 $V_c$ 從程式文本機械產生， $Safe$ 由主機定義，兩者都是一階邏輯公式。

表格：PCC 分工。

| 角色 | 工作 | 成本 |
|---|---|---|
| 程式發布者 | 寫標註、跑證明器、產生證明 $P$ | 貴，可離線 |
| 主機（核心） | 跑 VCgen 得 $V_c$ 、檢查 $P$ 證明 $V_c \Rightarrow Safe$ | 便宜，須可信 |
| 可信基 | VCgen + 證明檢查器 + 安全政策 | 極小 |

### 線索二：LF 作為證明的通用證物袋

證明可能很大，格式若不統一，主機無法檢查。Necula 與 Lee 選用 Harper 等人的 LF（Logical Framework）作為證明表示語言。LF 是依賴型別的 $\lambda$ 演算，判斷 $M : A$ 即「 $M$ 是命題 $A$ 的證明」。

檢查於是變成型別檢查：給定證明項 $M$ 與公式 $V_c \Rightarrow Safe$ ，檢查 $M$ 是否確具該型別。型別檢查器只有數千行，卻能檢查任意複雜的證明。這正是 LCF 可信核心思想在分散式場景的重演。

偵查筆記：PCC 信任鏈。

$$
Code + Annot \xrightarrow{VCgen} V_c \xrightarrow{Prove} P \xrightarrow{Check} Accept/Reject
$$

主機不相信編譯器、不相信證明器，只相信 VCgen 與檢查器。若 $P$ 偽造，檢查必失敗；若 $V_c$ 計算正確，則接受即安全。

### 線索三：從作業系統到行動碼

PCC 的第一個戰場是作業系統核心擴充：封包過濾器、驅動程式。核心在載入前檢查證明，通過才以原生速度執行，無需沙箱。這比 SFI 更徹底：安全在載入時已靜態確立。

第二個戰場是行動碼與智慧卡：頻寬與算力有限，檢查器必須小而快。Necula 證明檢查器可小到手寫可審計的程度，證明雖大但可壓縮、可用 oracle 重建。

理論對照表：

| 方法 | 保證 | 執行期成本 | 信任什麼 |
|---|---|---|---|
| SFI 沙箱 | 隔離 | 高 | 改寫器 |
| 簽章 | 來源 | 低 | 發布者 |
| PCC | 語意安全 $Safe$ | 零 | VCgen + 檢查器 |

## 結案報告

案件告破。PCC 把「驗證一次」拆成「證明一次（貴）＋檢查多次（便宜）」，讓不可信程式碼得以在可信主機上裸奔而不出軌。

遺產深遠：

1. Typed Assembly Language（TAL）把型別帶進組合語言，可視為 PCC 的編譯器自動化版本。
2. Proof-Carrying Authentication、Certified Code 風潮，影響了 Java 位元組碼驗證與 .NET 安全模型。
3. 通往 CompCert 的橋樑：PCC 問「如何相信外來碼」，CompCert 問「如何相信編譯器」。兩者共享 VCgen、語意保持、 LF/Coq 證據表示的思想。Necula 的後續工作直接討論驗證編譯器中的證明攜帶。

用一句話結案：PCC 不是讓主機更聰明，而是讓程式自己證明清白。

## 證據與工具

證據 A：核心蘊含式，獨立成行再看一次。

$$
\models V_c \Rightarrow Safe
$$

其中 $V_c$ 為驗證條件， $Safe$ 為主機安全政策， $\models$ 表邏輯有效。

證據 B：陣列讀取的安全規則示例。若指令為 $x := a[i]$ ，VCgen 產生 $0 \le i \land i < len(a)$ 作為前置義務。迴圈則需不變式 $Inv$ ，滿足啟動、保持、退出三條件。

證據 C：LF 判斷示例。命題 $A \Rightarrow B$ 的證明項為 $\lambda x . M$ ，其中 $M : B$ 在假設 $x : A$ 下成立。檢查器只需遞迴比對型別，無需搜尋。

證據 D：延伸閱讀。Necula 與 Lee 1996 年〈Safe Kernel Extensions Without Run-Time Checking〉；Necula 1997 年博士論文《Proof-Carrying Code》；Appel 2001 年《Foundations for Proof-Carrying Code》對 TAL 與邏輯的統一整理。
