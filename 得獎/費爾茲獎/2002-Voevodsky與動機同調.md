# 2002 · Voevodsky 與動機同調：給「理由」一個可以居住的空間

> 2002 費爾茲獎（北京 ICM）：Vladimir Voevodsky，表彰其在**動機同調理論**上的貢獻；同屆 Laurent Lafforgue 因函數域上的**朗蘭茲綱領**同獲此獎

## 案情提要

代數幾何有一個笨拙的毛病：想說「這些曲線的集合有什麼結構」，得先把它造出來（模空間，見 [1974-Mumford 案](1974-Mumford與模空間.md)）；想說「所有曲線的共同母體是什麼」，Grothendieck 在 1969 年就給出了名字——**motive**——卻沒有給出任何可以拿來計算的理論（[1966-Grothendieck概形革命](1966-Grothendieck概形革命.md)）。懸案：**能否建造一個「可以算出來的 motive 世界」？** Voevodsky 1990 年代中期到 2000 年代初的答案是「能」——他造出了一套**可以在上面做代數、可以證明定理、甚至可以做光譜序列的動機世界**，並在過程中解決了 Milnor 與 Bloch 提出的關鍵猜想。遺憾的是，他在 2017 年 7 月自殺身亡，未能看到 2018 年 p-進 motivic 世界觀的全面爆發。

## 前因

| 年份 | 事件 |
|---|---|
| 1969 | Grothendieck 在《.Manifeste motivique》提出 motive：一切有理上同調的「母體」 |
| 1968 | Milnor 提出 Milnor 猜想： motives 的 K 理論應該「看得見」——`K_n^M(X)/ℓ ≅ H^n(X, Z/ℓ)` |
| 1970s | Bloch 與 Kato 猜想的提出：對局部域，`K_n^M(F)/ℓ^n ≅ H^n(F, μ_ℓ^{⊗n})` |
| 1984 | Bloch 證明 Milnor 猜想的「混合權」部分 |
| 1990 | Bloch–Kato 猜想被明確陳述；Suslin 證明其「符號」情形 |
| 1990–96 | Rost 提出**范數公式**（norm residue / Rost cycle）——它給了「怎麼算」的可能 |
| 1996–97 | **Voevodsky 證明 Milnor 猜想**（與 Suslin 合作，1996 年底）及 **Bloch–Kato 猜想**（1996，與 Rost 的范數公式結合） |
| 2002 | 北京 ICM：Voevodsky 獲費爾茲獎；他的莫斯科大學老師 Piatetshi-Shapiro 已在 2009 年前逝世（1990 年）——**學生超越老師的悲劇** |

## 調查：把「上同調」搬到「不靠幾何」的世界

### 第一步：定義 motive 上的群（1990s）

在 motivic 範疇中定義「**動機上同調群**」`H^{p,q}(X, Z(n))`——它是：

- **像 motivic K 理論**（Milnor 的 `K_n^M`，用符號計算，因此只依賴「方案的函數」，不依賴點）
- **像 étale 上同調**（Deligne 的 `H^i(X, Q_ℓ)`，但被「提純」成有理係數）
- **像 Adams 權**（`Z(n)` 記錄權重 n）

**關鍵的破案直覺**：動機上同調是「**介於 K 理論與 étale 上同調之間**」的東西。它保留 K 理論的可計算性（符號運算），又保留 étale 上同調的幾何意義。

### 第二步：Milnor 猜想——「理由」真的能被看到嗎

**Milnor 猜想**（1968）：對任意正整數 n，

`K_n^M(X) ⊗ Z/ℓ ≅ H^n(X, Z/ℓ)`

（後來 Voevodsky 證明的是更強的版本，包含權分解。）

這等價於說：**motive 的 K 理論不是「另一個世界」，它就是上同調**。1996 年 Voevodsky 與 Suslin 用**三角剖分同調**（triangulated category of motives over a field）證明了它——這是 20 世紀 90 年代最艱難的代數幾何定理之一。

### 第三步：Bloch–Kato 猜想——「為什麼是 ℓ 次方」

**Bloch–Kato 猜想**：對局部域 F 與 n ≥ 1，

`K_n^M(F) ⊗ Z/ℓ^n ≅ H^n(F, μ_ℓ^{⊗n})`

它是「符號 K 理論 = Galois 上同調」的精確版。Voevodsky 1996 年證明了它——關鍵工具是 **Rost 范數公式**：

`K_n^M(F)/ℓ^n → H^n(F, μ_ℓ^{⊗n})` 是一個**同構**，

其逆映射由「**循環符號**（cyclotomic symbol）與 Galois 作用**對稱化**（symmetrization）」構造——這套「**把符號變成上同調**」的技術後來成為無數後續工作的標準工具。

### 第四步：理論的成熟——A¹-同調、純 motives、tropical

- **A¹-同調**（2000s）：Voevodsky 定義了「對 A¹-同構不變的同調」——把「多項式形變」視為同胚，這是**「形狀」觀念在同調論的落實**（Motives 計畫的後續 Esnault–Voisin 一路）。
- **Triangulated motives**（2006）： motives 被放進一個三角範疇裡，於是有了**光譜序列**——「motives 之間的關係可以用類似 Serre 譜序列的工具計算」。
- 2010 年後：**純 motives 的範疇化**、以及與 **tropical 幾何**（Kontsevich 的想法）的接軌。

## 理論裁決

| 層面 | 結論 |
|---|---|
|  motivic 的地位 | motive 從「Grothendieck 的直覺」變成「**有定理、有計算、有光譜序列的理論**」——Motivic Cohomology 與 Bloch–Kato 猜想成為現代數論的基本裝備 |
| 與物理 | 物理學家早已在「用 motivic 的方式思考」（費曼路徑積分與「樹級數」）；Voevodsky 的 motivic 傅立葉轉換（motivic Riemann–Roch）與物理的 QFT 形式叢產生共鳴——**「物理先於數學」的又一例** |
| 跨界 | 2002 年北京 ICM 是第一次在中國舉行的 ICM，也是第一次由 Voevodsky 這類「模形式–幾何–K 理論」三重奏得主領銜——**華人數學界最受關注的一屆** |
| 悲劇 | Voevodsky 2017-07-06 自殺身亡（51 歲）；他在生命最後幾年轉向**數學教育**（於 Harvard 開設「motives for the people」課程，並在諾貝爾物理學獎得主／數學家的跨界對話中推廣「教學先於研究」）——**他留下的最大遺產也許是教材** |

## 後果

| 層面 | 影響 |
|---|---|
| 學科 | Motivic 計算成為數論工具箱：BSD 猜想的 K 理論路線、Langlands 綱領的 motivic 版本（Geisser–Scholze 的「motivic Langlands」）、Galois 表示的 motivic 提升 |
| 傳承 | 學生與合作者：Marc Levine（motivic Euler 類）、Dundas、Marcelli–Mori–Sinnott（motivic 訊號）、以及 **Frenkel** 的 motivic Langlands 計劃 |
| 生態 | 2018 年後 p-進 motivic 世界（Scholze 的 perfectoid 空間 + 完美化技巧）使 motivic 計算**同時在兩種特徵下可用**——**Voevodsky 的藍圖在死後完成閉環** |
| 制度 | 2018 年 Fields 頒給 Scholze（[2018 案](2018-Scholze與完美疊加空間.md)）——**motivic 綱領的第二次也是最輝煌的一次兇器誕生** |

## 關聯

- 上游：[1966-Grothendieck概形革命](1966-Grothendieck概形革命.md)（motive 的原始構想）、[1978-Deligne與Weil猜想](1978-Deligne與Weil猜想.md)（étale 上同調與權重）
- 下游：[2018-Scholze與完美疊加空間](2018-Scholze與完美疊加空間.md)（p-進 motivic 的實現）、[2010-Ngô與基本引理](2010-Ngô與基本引理.md)（motivic Langlands 的接線）
