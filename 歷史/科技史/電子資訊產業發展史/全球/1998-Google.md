# 1998：Google — 為整個網路投票的演算法

## 案情
1998 年 9 月 4 日，Stanford 博士生 Larry Page 與 Sergey Brin 在加州 Menlo Park 一間車庫正式註冊成立 Google Inc.，初始資金來自 Sun 共同創辦人 Andy Bechtolsheim 開出的 10 萬美元支票。此時 AltaVista、Yahoo!、Excite 稱霸搜尋，Google 看起來只是第 20 名之後的跟班。兩年後，它成為全球流量最大的搜尋引擎。

## 前因
- 1996 年，Page 在 Stanford 做 BackRub 計畫，研究「連結結構」：誰連到誰，藏著權威性的訊號。
- 當時主流搜尋引擎以「頁面內文字出現次數」排名，容易被關鍵字堆砌（keyword stuffing）操縱，搜尋結果充滿垃圾。
- Brin 與 Page 1998 年發表論文〈The Anatomy of a Large-Scale Hypertextual Web Search Engine〉，公開描述 PageRank。
- 兩人一度想以 100 萬美元賣掉技術（買方包括 Excite），被拒——因為當時業界認為「搜尋不賺錢，入口網站才是王道」。

## 線索與推理
偵探的第一個推理：為什麼 PageRank 能贏？因為它把排名的「證詞」從頁面作者身上轉移到整個網路社群。傳統引擎聽頁面自己說自己重要（on-page 訊號，可偽造）；PageRank 聽別人怎麼說（off-page 訊號，偽造成本高）。這是偵探學的經典原則：證人越多、且證人本身可信度需被驗證，證詞才有力——PageRank 的遞迴設計正是「證人的可信度也由其他證人投票決定」。

第二個推理：為什麼 Google 沒賣掉？Brin 與 Page 的決策邏輯是「使用者體驗至上、廣告必須與搜尋結果明確分離」——1998 年的〈Don't be evil〉不是道德口號，而是商業模型：只有搜尋結果可信，使用者才會回來，廣告才值錢。

第三個推理：錢從哪來？答案是 2002 年Bill Gross 的 GoTo.com（Overture）已驗證的競價排名，但 Google 加上第二把鑰匙：AdWords Select（2002）不只看出價，還看點擊率——廣告排序由「出價 × 品質」決定。這把拍賣機制與演算法品質鎖在一起：使用者體驗越好，廣告收入越高，兩者不再是對立。

## 理論
PageRank 的核心公式。設網頁 $`i`$ 的 PageRank 為 $`PR(i)`$ ，指向 $`i`$ 的頁面集合為 $`B(i)`$ ， $`L(j)`$ 為 $`j`$ 的出鏈數，阻尼係數 $`d \approx 0.85`$ ：

$$
PR(i) = \frac{1-d}{N} + d \sum_{j \in B(i)} \frac{PR(j)}{L(j)}
$$

寫成矩陣形式： $`\mathbf{r} = \left(\frac{1-d}{N}\mathbf{1}\right) + d\, \mathbf{M}\mathbf{r}`$ ，其中 $`\mathbf{M}`$ 為按行歸一化的連結矩陣。等價於隨機漫遊模型：一位網衝者以機率 $`d`$ 沿隨機連結前進、以 $`1-d`$ 跳到任意頁面，PageRank 即其平穩分布。因 $`d<1`$ ，轉移矩陣滿足收縮條件，Banach 不動點定理保證解存在唯一，可用冪迭代法求解：

$$
\mathbf{r}^{(k+1)} = \frac{1-d}{N}\mathbf{1} + d\, \mathbf{M}\mathbf{r}^{(k)}, \qquad \sum_i r_i = 1
$$

經濟面：AdWords 本質是 generalized second-price（GSP）拍賣。廣告主 $`i`$ 排名勝出需支付

$$
p_i = \frac{b_{i+1} \cdot CTR_{i+1}}{CTR_i} + \epsilon
$$

即「下一名的出價乘以對方點擊率，除以自己的點擊率」——誘因相容（incentive-compatible）：誠實出價近似於占優策略，這與 Vickrey 二價拍賣的機制設計精神一脈相承。學術根源可追溯到 2007 年 Edelman、Ostrovsky、Schwarz 的 GSP 理論分析。

## 後果
1. 2001 年 Eric Schmidt 出任 CEO，2004 年 IPO，拍賣式發行（荷蘭標）引發爭議。
2. 2002 年 AdWords Select、2003 年 AdSense，建立內容網站的長尾廣告生態。
3. 搜尋廣告成為網路經濟的最大金礦，Google 之後的市值軌跡把 Yahoo!、AltaVista 全部殲滅。
4. 「連結=投票」催生了 SEO 產業與黑帽手法，Google 與操縱者的軍備競賽延續至今。
5. 資本與演算法的結合成為範式：之後的 Facebook（社交圖譜）、Amazon（推薦系統）都是「演算法即資產」的變奏。

## 冷案檔案
- 時間：1998 年 9 月 4 日創立；2000 年 AdWords；2002 年 AdWords Select 競價模式
- 案由：兩個博士生用遞迴連結分析破解搜尋品質難題，再用機制設計把信任變現
- 歷史定位：PageRank 是「學術論文直接催生兆元企業」的極端案例，也是資本主義與演算法联姻的世紀原型
