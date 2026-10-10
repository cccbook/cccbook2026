# 1963 年 Robinson 歸結原理：一招斃命的單一規則

> 案件編號：No.1963 — 偵探：John Alan Robinson。兇器：合一。證詞：一階邏輯只需一條推理規則。

## 案發現場

1960 年代初，自動證明界像一間堆滿雜物的偵探社。 [Herbrand 定理](1929-Herbrand定理.md) 說一階不可滿足可化為命題層窮舉， [Davis Putnam](1960-DavisPutnam程序.md) 與 [DPLL](1962-DPLL.md) 在命題層掃蕩子句， [Logic Theorist](1957-LogicTheorist.md) 留下啟發式傳統。但一階層仍是一團亂麻：全稱、存在、函數、變元交織，推理規則多達十幾條。

Gilmore 1960 年的程序會生成海量 Herbrand 基例，Prawitz 等人試圖改良卻仍逃不過組合爆炸。核心難題是：如何處理帶變元的文字 $P(x, f(y))$ 與 $\lnot P(a, z)$ ？何時它們「互補」可消？若每次都要先猜基例再命題消解，搜尋空間無邊無際。

1963 年夏天，在 Argonne 國家實驗室的 Robinson 盯著 [《數學原理》](1910-PrincipiaMathematica.md) 的公理 table 發呆，突然意識到：與其先例示再消解，不如讓消解本身去「求出」最一般的例示。這一念把兩步併成一步，也把十幾條規則併成一條。

## 偵查過程

Robinson 在 *A Machine-Oriented Logic Based on the Resolution Principle* 中宣告：一階證明只需歸結加合一。

### 線索一：單一歸結規則

命題層的歸結早已在 [Davis Putnam 消去規則](1960-DavisPutnam程序.md) 中現身。一階版本為：

$$
\frac{C \lor P \quad D \lor \lnot P}{C \lor D}
$$

其中 $C$ 與 $D$ 為子句， $P$ 為原子公式。讀作：若一子句含 $P$ ，另一子句含 $\lnot P$ ，則可消去這對互補文字，取其餘部分的析取。

一階的 twist 是 $P$ 與 $Q$ 不必字面相同，只需「可合一」。例如 $P(x, a)$ 與 $\lnot P(b, y)$ 可在代換 $x := b$ 、 $y := a$ 下變成互補。歸結於是升級為：

$$
\frac{C \lor P \quad D \lor \lnot Q}{(C \lor D)\sigma}
$$

其中 $\sigma$ 為 $P$ 與 $Q$ 的最一般合一者 MGU。加上因子化規則處理同一子句內多個可合一文字，即得完備系統。

### 線索二：合一演算法與 MGU 表

合一是本案的指紋比對術。給定兩項 $s$ 與 $t$ ，求代換 $\sigma$ 使 $s\sigma = t\sigma$ ，且 $\sigma$ 最一般。Robinson 的演算法遞迴拆解項結構，遇變元即綁定，並做 occur check 防止 $x$ 綁到含 $x$ 的項。

| 輸入 $s$ 、 $t$ | 結果 MGU $\sigma$ | 說明 |
|---------------|-------------------|------|
| $P(x, a)$ 與 $P(b, y)$ | $\{ x := b, y := a \}$ | 變元對常元，雙向綁定 |
| $P(f(x), y)$ 與 $P(z, g(a))$ | $\{ z := f(x), y := g(a) \}$ | 函數項整體搬移 |
| $P(x, x)$ 與 $P(a, b)$ | 失敗 | $a$ 與 $b$ 衝突，無合一者 |
| $P(x)$ 與 $P(f(x))$ | 失敗， occur check | $x$ 出現在 $f(x)$ 中，拒絕循環 |
| $Q(x, f(a))$ 與 $Q(g(y), z)$ | $\{ x := g(y), z := f(a) \}$ | 變元對複合項，合法 |

MGU 的關鍵性質是唯一性至多差變元重命名：若 $\sigma$ 與 $\theta$ 皆最一般，則存在重命名 $\rho$ 使 $\theta = \sigma\rho$ 。這保證歸結不做無用特化，永遠保留最大彈性。

### 線索三：祖先例子——蘇格拉底之死

經典一階問題：已知「所有人皆會死」與「蘇格拉底是人」，證「蘇格拉底會死」。子句化得：

- $C1$ ： $\lnot Human(x) \lor Mortal(x)$ ，即 $\forall x$ 版本。
- $C2$ ： $Human(Soc)$ ，其中 $Soc$ 為常元。
- 目標否定 $C3$ ： $\lnot Mortal(Soc)$ 。

偵辦過程： $C1$ 中文字 $\lnot Human(x)$ 與 $C2$ 中 $Human(Soc)$ 以 $\sigma = \{ x := Soc \}$ 合一，歸結得 $Mortal(Soc)$ 。再與 $C3$ 中 $\lnot Mortal(Soc)$ 歸結，無需代換，直接得空子句 $\Box$ 。空子句現身，全案終結：原假設集不可滿足，故原結論成立。

這正是 [亞里斯多德三段論](-0350-Aristotle三段論.md) 的機械重演：大前提、小前提、結論，三段論被一條歸結統攝。 [弗雷格](1879-Frege概念文字.md) 的量詞、 [Gentzen](1934-Gentzen自然演繹.md) 的推理，皆在此被壓縮。

### 線索四：策略與控制

空有規則不夠，還需搜尋策略。Robinson 提出支撐集策略、線性歸結等，約束每次至少一親本來自目標相關集，大幅剪枝。這直接預告 Horn 子句上的 SLD 消解——九年後 Colmerauer 與 Kowalski 將據此發明 Prolog。

## 結案報告

歸結原理一舉確立三件事：

- **單一規則的完備性**：對一階邏輯，反駁完備。若子句集不可滿足，則必可歸結出 $\Box$ 。證明經由 Herbrand 定理加提升引理：基例層的命題歸結可提升為一般層的合一歸結。
- **合一的獨立價值**：MGU 演算法成為符號計算的通用工具，從型別推論到 [Church 型別論](1940-Church簡單型別理論.md) 的實作皆用得上。
- **邏輯程式伏筆**：Horn 子句 $A \leftarrow B_1 \land \dots \land B_n$ 上的線性歸結即 SLD，正是 Prolog 的執行模型。偵探的筆記本，十年後變成程式語言。

影響所及：Boyer Moore 證明器、Otter、Vampire 等皆為歸結子孫； [Automath](1967-Automath.md) 走檢查路線，歸結走搜尋路線，兩路並進形塑證明自動化。

局限是：歸結證明難讀如天書，無高層結構；等式推理需另加 paramodulation； occur check 與搜尋爆炸仍是實務痛點。但 1963 年這一夜，一階推理終於有了統一制式手槍。

## 證據與工具

歸結反駁流程：欲證 $KB \models F$ ，先將 $KB \cup \{ \lnot F \}$ 化為子句集 $S$ ，重複取 $C1, C2 \in S$ 求 MGU 並生成歸結子 $R$ ，若 $R = \Box$ 則得證，否則將 $R$ 加入 $S$ 。

子句化四步：消蘊涵、移否定入內、Skolem 化存在量詞、分配合取並丟全稱。例如 $\exists y \forall x \, P(x, y)$ 化為 $P(x, f(x))$ 其中 $f$ 為 Skolem 函數。

習題：試歸結 $C1 = \{ P(x) \lor Q(x) \}$ 、 $C2 = \{ \lnot P(a) \}$ 、 $C3 = \{ \lnot Q(b) \}$ 加上 $x$ 需同時合一的困境，體會因子化與多步歸結之必要。答案：先 $C1$ 與 $C2$ 得 $Q(a)$ ，但與 $C3$ 需 $a = b$ 才可合一，故原集在 $a \neq b$ 時可滿足。

延伸閱讀：Robinson 1965 年期刊版、Chang Lee《Symbolic Logic and Mechanical Theorem Proving》、Bachmair Ganzinger 歸結綜述。欲看分裂路線請回 [DPLL](1962-DPLL.md) ，欲看檢查路線請進 [Automath](1967-Automath.md) 。
