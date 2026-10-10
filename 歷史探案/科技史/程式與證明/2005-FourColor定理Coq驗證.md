# 2005 四色定理 Coq 驗證：百年懸案的封印

> 案件編號：2005-4CT。報案人：全體數學家。案情：四色定理人人相信，無人完全驗算。破案者：Gonthier、Werner 與 Coq。

## 案發現場

四色問題 1852 年由 Guthrie 提出：任何平面地圖只需四色即可使鄰國異色。1976 年 Appel 與 Haken 宣布用電腦證明：列出 1936 個可約構形，再以放電法證明任何極小反例必含其一，逐一機檢可約性。

數學界譁然。一方面是歷史性突破，另一方面是信任危機：1936 個構形的檢查程式誰審過？放電法的數百頁手寫論證誰全看完？有人說這不是證明，是實驗。爭議延燒二十年，期間 Robertson 等人把構形減到 633 個，但「電腦部分不可審」的心結未解。

案發現場的證物是一句話：「我們相信程式，正如我們相信審稿人——但兩者都可能錯。」要結案，必須把「相信程式」變成「檢查證明」。

2005 年，微軟劍橋的 Gonthier 與 INRIA 的 Werner 用 Coq 完成四色定理的形式驗證，一次封印爭議，並順手孵出 SSReflect。

## 偵查過程（含數學式/表格/理論）

### 線索一：可約構形＋放電法的雙重鎖

形式化之前，先重述 Appel–Haken 策略。假設存在極小反例 $G$ （頂點數最少的需五色平面圖），則：

1. $G$ 必為三角剖分（triangulation），否則可加邊得更小反例。
2. 列出一組構形集 $K$ ，證明 $K$ 不可避免（unavoidable）：任何三角剖分必含 $K$ 中一員，此即放電法（discharging）。
3. 證明 $K$ 中每員可約（reducible）：含該構形的圖不可為極小反例。

若 $K$ 又不可避免又可約，則極小反例不可能存在，定理得證。邏輯骨架為：

$$
Unavoidable(K) \land (\forall C \in K : Reducible(C)) \Rightarrow 4CT
$$

其中 $4CT$ 表「所有平面圖四可著色」。偵探的工作就是把這兩 conjunct 都變成 Coq 定理。

表格：證明規模演化。

| 版本 | 構形數 | 檢查方式 | 可信度 |
|---|---|---|---|
| Appel–Haken 1976 | 1936 | 自寫程式 | 爭議 |
| Robertson 等 1997 | 633 | C 程式 | 改善但仍不形式 |
| Gonthier–Werner 2005 | 633 | Coq 證明 | 機械檢查 |

### 線索二：Coq 封印如何運作

Gonthier 的策略不是重寫數學，而是把整個組合論證搬進構造演算（CIC）。平面圖、超圖（hypermap）、可約性檢查器，全部在 Coq 內定義；放電法的計數論證變成可計算的布林判斷。

關鍵技巧是「反射」（reflection）：把判定 $P$ 寫成布林函數 $b_P$ ，再證明 $b_P = true \leftrightarrow P$ 。於是 633 個構形的可約性檢查，在 Coq 內就是一次 $Compute$ ：

$$
CheckAll(K) = true \Rightarrow \forall C \in K : Reducible(C)
$$

機器檢查 $CheckAll(K)$ 歸約到 $true$ ，即完成上千個案例的驗證。信任基縮小到 Coq 核心與規格定義，不再信任一次性 C 程式。

偵查筆記：超圖形式化約 6 萬行 Coq，定義平面性、對偶、 Kempe 鏈等概念；放電部分把「電荷」分配寫成有理數計算， $ \sum charge = 12$ 一類的組合恆等式全部機械驗算。

### 線索三：SSReflect 的雛形

為駕馭大規模案例與計算反射，Gonthier 寫出 SSReflect（Small Scale Reflection）雛形：新的 Coq 策略語言與函式庫風格。它強調布林反射、小規模結構化證明、視圖（view）切換，讓「計算即證明」寫起來簡潔。

SSReflect 後來長成 MathComp 函式庫，支撐 2012 年 Odd Order 定理。四色案於是顺手生下下一個大案的兇器。

## 結案報告

案件告破。2005 年 Coq 腳本宣布：四色定理的每一行推理皆已通過核心檢查，633 個構形的計算皆可重跑。爭議從「程式對不對」變成「規格是否忠實」，而規格只有數百行，人人可審。

遺產有三：

1. 電腦證明獲得新正當性：可疑的不是電腦，而是不可檢查的電腦。
2. SSReflect/MathComp 路線確立，為群論大定理鋪路。
3. 示範「大規模反射證明」範式，影響 CompCert、seL4 的證明工程學。

從因果鏈看，四色案上承 1988 CIC、1989 Coq，下啟 2012 Odd Order 與 2014 Flyspeck：數學大一統時代就此開門。

## 證據與工具

證據 A：定理陳述（Coq 風格簡寫）。 $map$ 為平面超圖， $coloring$ 為四色函數，定理斷言 $\forall map : Planar \, map \Rightarrow \exists coloring : Proper \, coloring$ 。

證據 B：放電恆等式示例。初賦電荷 $ch(v) = deg(v) - 6$ ，面電荷 $ch(f) = 2 \, deg(f) - 6$ ，放電後總和不變，極小反例的正電荷頂點附近必現 $K$ 中構形。

證據 C：反射引理模式。

```
Lemma check_implies P b : reflect P b -> (b = true -> P).
```

一旦證明 $reflect$ 實例， $b = true$ 的計算即 $P$ 的證明。

證據 D：延伸閱讀。Gonthier 2008 年〈Formal Proof: The Four-Color Theorem〉；Robertson 等 1997 年簡化證明；MathComp/SSReflect 文件與 Coq 四色原始碼庫。
