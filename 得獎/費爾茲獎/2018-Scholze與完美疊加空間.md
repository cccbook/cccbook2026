# 2018 · Scholze 與完美疊加空間：把「壞掉的」數字系統修好

> 2018 費爾茲獎（里約熱內盧 ICM）：**Peter Scholze**，表彰其**完美疊加空間（perfectoid spaces）**理論的創立與應用；同屆 Caucher Birkar（BCH 定理與 Fano 簇）、Alessio Figalli（最優輸運與曲率）、Akshay Venkatesh（自守形式的數論）亦同獲此獎

## 案情提要

現代數學有兩個互相不通氣的世界：**複數世界**（微積分、解析、複分析，工具齊備、業績輝煌）與 **p-進世界**（`Q_p`、`Z_p`，算術的真正棲身地）。兩者之間隔著一道無法用傳統方法跨越的牆：p-進世界沒有「微積分」——導數是野蠻的，函數連續都談不上，**連「極限」這個概念都殘缺不全**（`p` 進賦值的絕對值是離散的，`Z_p` 上的函數沒有中間值定理）。懸案：**能不能造一個 p-進世界的「微積分」，然後把複數世界的工具整批搬過去？** Scholze 在 2012 年給出的答案是：可以——但必須先**改造基礎設施**，造出一類「完美」的對象：**perfectoid 空間**。2018 年，他以 30 歲之齡獲獎（費爾茲獎史上最年輕得主之一）。

## 前因

| 年份 | 事件 |
|---|---|
| 1960s–70s | Serre 與 Grothendieck 在 p-進世界建立 étale 上同調（[1966-Grothendieck概形革命](1966-Grothendieck概形革命.md)）——**第一次把「複數的方法」搬進 p-進世界的嘗試** |
| 1990s | **Faltings 與 Wiles 的方法論**：局部—整體原則、Galois 表示、模形式；p-進 Hodge 理論（Kato 1990s）試圖為 p-進世界建立一套「像複分析」的理論，但受限於「良好約化」——**只覆蓋一小部分場所** |
| 2000s | 硬體層技術（Ichikawa 1990s）、Breuil–Mézard 叢、Buzzard 的 D-模理論：**「良好約化」的幕簾必須被拉開** |
| 2012-05 | **Scholze–Weinstein** 發表《p-adic Hodge theory for rigid analytic varieties》；Scholze 發表《Perfectoid spaces》——**本案的全部兇器** |
| 2012 | Scholze 與 Fargues 構造 **Fargues–Fontaine 曲線**：給 p-進世界一座「把所有 Galois 表示裝進去的橋」 |
| 2013 | Scholze 證明 **p-進 Hodge 理論的局部—整體比較**（完全版本）——**不需良好約化** |
| 2013 | Scholze 證明 **Bloch–Kato 猜想（局部域情形）**——為 Voevodsky 的 motivic 藍圖補上 p-進拼圖（[2002 案](2002-Voevodsky與動機同調.md)） |
| 2018 | 里約 ICM：Scholze 獲費爾茲獎（**最年輕得主**；同屆 Birkar 的獎章在會場遭竊，數分鐘後大會補發——**史上唯一「當場失竊」的獎章**） |

## 調查：關鍵是「讓 Frobenius 變成可逆」

**問題的診斷**：在 `Z_p` 上，`p` 進賦值是離散的——任何函數 `f: Z_p → Z_p` 都無法「連續地」插值出中間值。要想模仿複分析（用微積分、極限、解析函數），得有一種**能讓 `p` 變得「無窮小又無窮大」的對象**。

**Perfectoid 域的定義（技術核心）**：一個完整的非阿基米德域 `K`，其值群 `|K×|` 是**非離散**的，並存在拓撲零點 `ϖ`（`ϖ | p`），使得 Frobenius 映射 `x ↦ x^p` 在 `K/p` 上是**滿射**（且等距）。

這個定義只有一句話，但藏著整個破局點：

- **「Frobenius 滿射」= 「p-進的損失被補回來了」**。在 `Z_p` 上 Frobenius 不是滿射（損失了大量資訊）；而在 perfectoid 域上它是滿射——**資訊不再流失**。
- **「值群非離散」= 「有了連續性」**。非離散的值群讓 `K` 上存在真正的「小量」，於是**微積分得以存在**。

**致命武器——tilt（傾斜）**：對 perfectoid 域 `K`，定義

`K^♭ = lim_{x ↦ x^p} K/p`

（對 Frobenius 與 `p` 的極限）。這個「傾斜」有兩個驚人的性質：

1. `K^♭` 是**特徵 0** 的（!）——它不再是 p-進的，卻保有 p-進的「無窮小」結構。**於是複數世界（特徵 0）的整套工具可以搬進來**。
2. `K^♭` 與 `K` 共享**幾乎所有有訊息的結構**：上同調、Galois 表示、perfectoid 空間的類別。

**這就是整個案件的偵探邏輯**：

```
p-進世界（特徵 p，工具殘缺）
      │  造出 perfectoid 空間（讓 Frobenius 可逆 + 值群非離散）
      ▼
 tilt 到 特徵 0 的世界（K^♭），工具恢復完整
      ▼
把 Deligne 的權重、Faltings 的局部—整體、 motives 的計算全部搬回來
```

**「斜著看一眼，就能看見特徵 0」**——這是 21 世紀數學最漂亮的一次結構性發現。

### 具體成果：三塊拼圖

| 成果 | 內容 |
|---|---|
| **p-進 Hodge 理論（無需良好約化）** | 2013 年 Scholze 證明：對**任何**（proper, smooth）p-進族，`H^i(X_et, Q_p)` ≅ `H^i_fppf(X, Q_p(+i))`——**etale 與 fppf 同調的比較定理**。傳統上只在良好約化處成立，現在**全域成立** |
| **Bloch–Kato 猜想（局部域）** | 2013 年用 perfectoid 空間與 tilt 證明局部域上的 Bloch–Kato 猜想——**Voevodsky 1996 年的 motivic 定理獲得 p-進對偶** |
| **Fargues–Fontaine 曲線** | 與 Fargues 合作（2012）：一條曲線，其上的點對應 p-進 Galois 表示——**朗蘭茲綱領在 p-進世界的「具體舞台」**。Scholze 與 Schwanke 隨後在此舞台上建立 p-進朗蘭茲（2019 起） |

## 理論裁決

| 層面 | 結論 |
|---|---|
| p-進幾何 | 從此有了一門「自己的」微積分：**完美疊加空間的微分、解析**；Scholze–Scholze 證明了橢圓曲線在 `Q_p` 上的 BSD 猜想——**p-進世界的「費馬最後定理 + BSD」同時落網** |
| 與 motivic 的合流 | Voevodsky 的 motive（2002）在 p-進世界的對應物由 Scholze 建構；**「motivic + perfectoid」是當代數論的標準配備** |
| 朗蘭茲 | 2016 年起，p-進朗蘭茲（Breuil–Mézard 叢、模形式的 Galois 表示）成為可能；Scholze 與 Fargues 提出的綱領（Fargues 綱領）已可望局部性地建立 p-進對應 |
| 物理 | perfectoid 空間在 **AdS/CFT 與弦論的「swampland」語境**中也被用來討論「p-進 AdS/CFT 的可能性」——**數學家又一次走在物理前面** |

## 後果

| 層面 | 影響 |
|---|---|
| 學科 | 「p-進幾何」從一個技術性分支升格為**獨立學科**；Scholze 的學生與合作者（Fang、Han、Hinterlobner、Tian、Liu 等）在數年内建構了整個領域 |
| 工具 | **diamonds**（Scholze 2018 的抽象語言，把「完美化的局部」做成一個整體的「磚」）——**「用磚蓋房子」的建構法成為 p-進世界的通用語言** |
| 完整圈 | 2021 年起 p-進 Langlands 的「計數」版本（à la Hida、Ding 等）取得關鍵進展；p-進幾何測試向 conjectures 被提出——**未結卷宗，但主線清晰** |
| 傳承 | Scholze 2022 年獲 Wolf 獎；其導師 Michael Rapoport（也是 Rapoport–Zink 猜想的作者之一）——**學派血脈可追溯至 1990 年代的 Rapoport–Zink 綱領**（[2010-Ngô 案](2010-Ngô與基本引理.md) 的搭檔） |
| 同屆 | Birkar 的 BCH 定理（Fano 簇的有界性）為 **Kollár–Mori 理論**畫上句點；Figalli 的最優輸運與曲率對應把 PDE 的正則性理論推上舞台；Venkatesh 在自守形式的數論上大放異彩——**2018 屆是「幾何、運輸、算術」的 triple play** |

## 關聯

- 上游：[1966-Grothendieck概形革命](1966-Grothendieck概形革命.md)（étale 上同調的地基）、[2002-Voevodsky與動機同調](2002-Voevodsky與動機同調.md)（motive 藍圖的 p-進補完）、[2010-Ngô與基本引理](2010-Ngô與基本引理.md)（Rapoport–Zink 與朗蘭茲）
- 下游：[2022-Viazovska與球堆積](2022-Viazovska與球堆積.md)（模形式的專家級操控，p-進版本正在路上）
