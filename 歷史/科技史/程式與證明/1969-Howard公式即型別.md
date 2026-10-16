# 1969 年 Howard 公式即型別：證明就是程式

> 案件編號：No.1969-B — 偵探：Haskell Curry、William Howard。真相：邏輯與計算本是同一人。

## 案發現場

1934 年，Haskell Curry 在備忘錄裡寫下一句無人理會的話：組合子的型別很像邏輯公理。直覺主義邏輯的 $A \to B$ ，看起來就像函數型別 $A \to B$ 。當時 [希爾伯特](1900-Hilbert23問題.md) 正紅， [Gentzen](1934-Gentzen自然演繹.md) 剛發明自然演繹，沒人有空理會這條冷線索。

三十五年後，William Howard 在 1969 年的手稿 *The Formulae-as-Types Notion of Construction* 中把冷案重啟。他發現：Gentzen 自然演繹的每條推理規則，都精確對應 typed $\lambda$ 演算的一條構造規則；證明化簡正對應程式求值。這不是比喻，而是同構。

案發現場的吊詭是：邏輯學家與程式語言學家三十年來用兩套語言講同一件事。 [Church](1940-Church簡單型別理論.md) 發明型別以避悖論， [Gentzen](1934-Gentzen自然演繹.md) 發明自然演繹以解剖證明，兩人從未謀面，結構卻鏡像對稱。Howard 的任務就是掀開面具：他們是同一人。

同一時間， [Automath](1967-Automath.md) 正用依賴型別檢查數學， [Hoare 邏輯](1969-Hoare邏輯.md) 正用斷言規範程式，Howard 的發現為兩者提供了共同地基。

## 偵查過程

Howard 的手法是逐條比對：一邊是直覺主義自然演繹，一邊是簡單型別 $\lambda$ 演算。

### 線索一：命題等於型別，證明等於程式

| 邏輯側：命題 $A$ | 計算側：型別 $A$ | 對應 |
|------------------|------------------|------|
| 命題 $A$ | 型別 $A$ | 公式即型別 |
| $A$ 的證明 $p$ | $A$ 的居民 $M : A$ | 證明即程式 |
| 蘊涵 $A \to B$ | 函數型別 $A \to B$ | 證明即函數 |
| 合取 $A \land B$ | 積型別 $A \times B$ | 證明即對偶 |
| 析取 $A \lor B$ | 和型別 $A + B$ | 證明即分支 |
| 真 $True$ | 單元型別 $Unit$ | 唯一證明即空元組 |
| 假 $False$ | 空型別 $Void$ | 無證明即無居民 |

例如蘊涵引入規則：由假設 $x : A$ 證出 $M : B$ ，得 $\lambda x . M : A \to B$ 。這正是自然演繹的 $\to$ 引入。蘊涵消去即函數應用：由 $M : A \to B$ 與 $N : A$ 得 $M \, N : B$ ，正是肯定前件。在 [亞里斯多德](-0350-Aristotle三段論.md) 那裡是三段論，在這裡是求值。

合取引入為對偶構造 $(M, N) : A \land B$ ，消去為投影 $fst$ 與 $snd$ 。析取引入為 $inl$ 與 $inr$ ，消去為 $case$ 分析。每一條 [Gentzen 規則](1934-Gentzen自然演繹.md) 都有 $\lambda$ 搭檔，毫無例外。

### 線索二：化簡就是求值

Gentzen 擔心證明走彎路：先引入 $A \to B$ 再消去，等於繞一圈。Howard 指出這正是 $\beta$ 歸約：

$$
(\lambda x . M) \, N \to M[x := N]
$$

左邊是「先證蘊涵再用它」的彎路證明，右邊是化簡後的直路證明，而計算側正是函數呼叫的求值一步。證明正規化等於程式執行， Prawitz 的正規化定理等於 $\lambda$ 演算的強正規化。

更妙的是， Curry 在 1934 年早已給出組合子版本： $K : A \to B \to A$ 對應公理 $A \to (B \to A)$ ， $S : (A \to B \to C) \to (A \to B) \to A \to C$ 對應 [《數學原理》](1910-PrincipiaMathematica.md) 的第二公理。公理即組合子，演繹即組合——三十五年的伏筆至此收束。

### 線索三：Gentzen 連結

Gentzen 自然演繹的引入消去對稱，在 Howard 手中變成構造解構對稱：

- $\land$ 引入對 $(M, N)$ ，消去對投影，化簡為投影歸約。
- $\lor$ 引入對 $inl$ ，消去對 $case$ ，化簡為分支選路。
- $\to$ 引入對 $\lambda$ ，消去對應用，化簡為 $\beta$ 。

矢列演算的 cut 消去亦對應歸約，只是視角從自底向上改為自頂向下。直覺主義的限制不可少：古典排中律 $A \lor \lnot A$ 無直覺證明，正如無總體程式能判定任意型別 $A$ 之居民存在。這解釋了為何 Howard 對應先在直覺側成立，古典需另加 continuations。

此發現同時照亮 [布林](1847-Boole布林代數.md) 到 [弗雷格](1879-Frege概念文字.md) 的路線：邏輯代數化之後，下一步是邏輯程式化。

## 結案報告

Howard 證明：命題是型別，證明是程式，化簡是求值。三句話統一了邏輯與計算：

- **證明即程式**：寫證明就是寫 typed $\lambda$ 項，檢查證明就是檢查型別。這給 [Automath](1967-Automath.md) 遲來的理論背書，也給 LCF、Coq、Lean 立下法統。
- **求值即推理**：執行程式就是化簡證明，程式的型別安全就是邏輯的一致性。 [Church 型別](1940-Church簡單型別理論.md) 不再只是防悖論的籬笆，而是程式的規格語言。
- **構造主義登基**：直覺邏輯從哲學偏好變成計算必然。後來的 Martin-Löf 型別論、CoC、CIC 全是此表的縱向擴充：加上依賴型別 $\Pi$ 與 $\Sigma$ ，一階二階邏輯盡入彀中。

局限是：1969 年手稿直到 1980 年才正式發表，古典邏輯、多態、效應仍在表外。但正因如此，它成為第二幕最優雅的收束：從 [哥德爾](1931-Godel不完備定理.md) 的極限出發，經機器搜尋與檢查，最終發現證明與程式本是一體兩面。

第二幕落幕，第三幕的 LCF、Prolog、Coq 都將在此 Entrée 之上開席。

## 證據與工具

對照速查：欲證 $A \to B \to A$ ，程式為 $K = \lambda x . \lambda y . x$ ，型別推導為兩次 $\to$ 引入。欲證 $(A \land B) \to A$ ，程式為 $fst = \lambda p . fst \, p$ 。欲證 $(A \lor B) \to (B \lor A)$ ，程式為 $\lambda s . case \, s \, of \, inl \, a \Rightarrow inr \, a \mid inr \, b \Rightarrow inl \, b$ 。每一步推理皆可機械譯為項構造。

正規化示例：證明 $(\lambda x . x) \, M : A$ 化簡為 $M : A$ ，對應消去引入對的彎路。此即 $\beta$ 歸約，亦即求值。強正規化保證： typed 項的任何歸約序列皆終止，正如直覺證明的任何化簡皆終止。

古典擴充預告：若加入控制算子 $callcc : ((A \to B) \to A) \to A$ ，即得 Peirce 定律，對應古典邏輯。若加入多型 $\forall X . T(X)$ ，即得 System F，對應二階邏輯。Howard 表的每一縱向擴充都是一次邏輯升級，這正是後來 CoC 與 CIC 的路線圖。

與 [Church](1940-Church簡單型別理論.md) 的呼應：Church 用型別擋下悖論，Howard 用型別裝下證明。前者是防守，後者是進攻。兩案合看，型別既是邏輯的護欄，也是程式的藍圖。

習題：寫出 $A \land B \to B \land A$ 的證明項。答案為 $\lambda p . (snd \, p, fst \, p)$ ，型別為 $(A \times B) \to (B \times A)$ 。再試 $Curry$ 化： $(A \land B \to C)$ 同構於 $A \to B \to C$ ，體會蘊涵與合取的伴隨。

延伸閱讀：Howard 1980 年刊版、Wadler 2015 年科普《Propositions as Types》、Sørensen Urzyczyn《Lectures on the Curry-Howard Isomorphism》。回顧起點請見 [Gentzen](1934-Gentzen自然演繹.md) 與 [Church](1940-Church簡單型別理論.md) ，續集請期待 LCF 與 Coq。
