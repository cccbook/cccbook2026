# 1967 年 Automath：de Bruijn 的證明檢查局

> 案件編號：No.1967 — 偵探：Nicolaas de Bruijn。地點：Eindhoven。口號：「機器不必會破案，但必須會驗案。」

## 案發現場

1966 年的 Eindhoven 工業大學，數學家 de Bruijn 目睹一樁怪案：數學論文越來越長，審稿越來越不可靠。長達百頁的證明，誰敢說每一步都對？ [《數學原理》](1910-PrincipiaMathematica.md) 的三卷本已讓人卻步，而未來的數學只會更龐大。

同一時間，自動證明界正兵分兩路： [Logic Theorist](1957-LogicTheorist.md) 、 [DPLL](1962-DPLL.md) 與 [歸結原理](1963-Robinson歸結原理.md) 走「讓機器找證明」的搜尋路線，屢建奇功卻也屢遇爆炸。de Bruijn 提出第三條路：人類寫證明，機器做檢查。搜尋可以不完備、靠啟發式，但檢查必須嚴格、可判定、值得信任。

難題在於：用什麼語言寫證明，才能讓機器逐行驗過？ [Church 簡單型別](1940-Church簡單型別理論.md) 太弱，寫不了「對所有 $n$ 的證明」這種依賴命題；無型別集合論太強，檢查不可判定。需要一種既能表達數學、又能機械驗證的中間語言。

de Bruijn 從 1967 年起以 Automath 應戰，前後發展十年，親手驗證了 Landau《分析基礎》全書。這是史上第一個電腦證明檢查器。

## 偵查過程

Automath 的核心洞見是：命題、型別、證明三者可用同一套 $\lambda$ 機制統一處理，這正是依賴型別的雛形。

### 線索一：依賴型別雛形

在 [Church 系統](1940-Church簡單型別理論.md) 中，型別 $A \to B$ 的 $B$ 不能提及項。但數學需要「 $P(x)$ 隨 $x$ 而變」的型別族。Automath 允許 $\Pi x : A . B(x)$ ，其中後件 $B$ 可依賴前件 $x$ 。例如「長度為 $n$ 的向量」之型 $Vec(n)$ 依賴項 $n : Nat$ 。

| 層次 | Church 簡單型別 | Automath |
|------|----------------|----------|
| 函數 | $A \to B$ ， $B$ 固定 | $\Pi x : A . B(x)$ ， $B$ 可含 $x$ |
| 證明 | 與命題分離 | 命題 $P$ 即型別，證明 $p : P$ 即居民 |
| 檢查 | 型別檢查 | 型別檢查即證明檢查 |
| 例子 | $\lambda x . x : A \to A$ | $\lambda x . x : \Pi x : A . A$ 退化情形 |

於是全稱量詞 $\forall x : A . P(x)$ 不再是特殊邏輯符號，而就是依賴函數型別 $\Pi x : A . P(x)$ 。存在、合取、蘊涵皆可類似編碼。這比 [Gentzen 自然演繹](1934-Gentzen自然演繹.md) 更進一步：推理規則變成 typed $\lambda$ 項的構造規則。

### 線索二：De Bruijn index —— 告別變元名

人類愛用 $x$ 、 $y$ ，機器卻為 $\alpha$ 轉換與 capture 煩惱。de Bruijn 發明無名表示法：變元以距其 binder 的距離編號。例如 $\lambda x . \lambda y . x$ 寫成 $\lambda \lambda 2$ ，其中 $2$ 指外層第二個 $\lambda$ 。

| 具名寫法 | De Bruijn 寫法 | 說明 |
|----------|----------------|------|
| $\lambda x . x$ | $\lambda 1$ | 指最近 binder |
| $\lambda x . \lambda y . x$ | $\lambda \lambda 2$ | 跳過一層 |
| $\lambda x . \lambda y . y$ | $\lambda \lambda 1$ | 指內層 |
| $\forall x . P(x)$ | $\Pi 1$ 族實例 | 量詞即 binder |

好處是 $\alpha$ 等價變成語法相等，代換變成可計算的移位操作，檢查器實作大幅簡化。今日 Coq、Lean 核心仍用此術管理 binder，只是前端藏起來不讓用戶看見。

### 線索三：書本結構與驗證流程

Automath 文本是一連串「書行」：定義行引入常元 $c : T := M$ ，斷言行引入公理，證明行逐步填居民。檢查器逐行做型別推斷：若宣稱 $M : T$ 但推得 $T'$ 且 $T$ 與 $T'$ 在 $\beta$ 下不等價，即報錯。

de Bruijn 團隊以此驗完 Landau 分析，約一萬三千行，機器逐行蓋章。這是人類史上第一次「被電腦背書的數學書」。相對於 [哥德爾](1931-Godel不完備定理.md) 的悲觀，它證明：雖不能判定一切真理，但能判定「給定證明是否有效」。

## 結案報告

Automath 沒有大紅大紫，卻是精神祖先級的重案：

- **Coq 精神祖先**：其依賴型別、命題即型別思想直接通往 Martin-Löf 型別論、CoC 與 Coq。沒有 Automath，就沒有後來的構造演算。
- **檢查 vs 搜尋分家**：它確立「證明檢查可判定、證明搜尋可啟發」的分工，LCF 的可信核心、Isabelle 的核心架構皆沿此路。
- **De Bruijn index 長存**：所有現代證明器的核心實作仍用此術處理 binder，它是幕後無名英雄。

局限是：語法繁瑣，人類幾乎無法手寫大證明；缺乏 [Howard 對應](1969-Howard公式即型別.md) 的程式視角與 [Hoare 邏輯](1969-Hoare邏輯.md) 的程式驗證介面；當時硬體也撐不起大規模驗證。但 de Bruijn 證明了方向可行：數學可以是可驗證的程式碼。

偵探側寫：de Bruijn 本是數學物理學家，研究渦旋與漸近展開，卻對「證明何以可信」異常執著。他堅持檢查器核心必須小到可用肉眼審計，這正是後來 LCF 可信核心與 de Bruijn 準則的源頭：證明可以很大，但檢查者必須很小。

Automath 家族後來分化為 AUT-68、AUT-QE 等方言，差別在於 $\Pi$ 與 $\lambda$ 的允許層級。這張層級立方體的雛形，十五年後被 Barendregt 整理為 $\lambda$ 立方體，從簡單型別一路通往構造演算。

下一案我們轉向程式本身：如何證明程式正確？請見 [Hoare 邏輯](1969-Hoare邏輯.md) 。

Automath 與搜尋派的對照： [歸結原理](1963-Robinson歸結原理.md) 讓機器自己找證明，Automath 讓人類寫證明機器驗證。前者強在自動，弱在難讀；後者強在可信，弱在費工。兩派的聯姻要等到互動式證明器加自動戰術才實現。

## 證據與工具

最小 Automath 風格示例：定義自然數 $Nat : Type$ ， $zero : Nat$ ， $succ : Nat \to Nat$ 。定義謂詞 $P : Nat \to Prop$ 。欲證 $\forall n . P(n) \to P(n)$ ，只需項 $\lambda n . \lambda h . h$ ，其型別為 $\Pi n : Nat . P(n) \to P(n)$ 。檢查器驗證： $n : Nat$ 入脈絡， $h : P(n)$ 入脈絡，回傳 $h : P(n)$ 吻合，蓋章通過。

$\beta$ 歸約即計算： $(\lambda x . M) \, N$ 化為 $M[x := N]$ ，在 De Bruijn 表示下為移位加代換，無需擔心變元捕獲。

習題：把 $\lambda x . \lambda y . y \, x$ 譯為 De Bruijn 式。答案為 $\lambda \lambda (1 \, 2)$ 。再試 $\lambda x . (\lambda y . y) \, x$ 化簡後為 $\lambda 1$ ，體會檢查器如何用歸約判定型別相等。

驗證流程三步：脈絡相容檢查、型別合成、 $\beta$ 等價比對。任何一步失敗即退件，成功則蓋章並將新定義納入脈絡，供後續書行引用。這種線性累積式驗證，正是今日 Coq 與 Lean 長證明的雛形。

de Bruijn 準則至今有效：檢查器的可信不取決於證明有多聰明，而取決於檢查核心有多小。這句話刻在每一套現代證明器的案頭。

延伸閱讀：de Bruijn 1968/1970 年 Automath 報告、Nederpelt Geuvers《Type Theory and Formal Proof》首章。理論續集請見 [Howard 公式即型別](1969-Howard公式即型別.md) ，搜尋路線對照請見 [歸結原理](1963-Robinson歸結原理.md) 。
