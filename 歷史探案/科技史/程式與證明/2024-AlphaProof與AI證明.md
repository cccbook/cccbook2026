# 2024 AI 探員入局：AlphaProof 與 AlphaGeometry 勇闖 IMO

> 報案人：國際數學奧林匹亞（IMO）。案情：人類金牌選手守擂六十餘年，機器能否破門？
> 偵探：Google DeepMind 的 AlphaProof ＋ AlphaGeometry 團隊。兇器：Lean 形式化 ＋ 強化學習搜尋。

## 案發現場

2024 年之前，AI 證明有兩個難解的對立現場：

- 自然語言的數學 AI（如 GPT 系列）能寫出看似漂亮的證明，卻常藏著幻覺跳步，無法信任。
- 形式化的證明助理（如 Lean、Coq、Isabelle）絕對可信，卻需要人類逐行餵招，自動化程度低。

DeepMind 的判斷是：把兩者銬在一起。用 Lean 當法官，用大語言模型當線人，用強化學習當搜查策略。這就是 AlphaProof 的立案初衷。

同案的另一名探員是 AlphaGeometry，專攻歐氏幾何。它由吳宇懷等人打造，結合神經語言模型與符號演繹引擎，立志解決「輔助線」這種最考驗靈感的難題。

2024 年 7 月，英國巴斯 IMO 賽場成為公開審判庭。DeepMind 宣布：AlphaProof 與 AlphaGeometry 聯手，在 2024 年 IMO 六題中解出四題，總分 28 分，達到銀牌線，距離金牌僅一步之遙。這是 AI 首次在現役 IMO 規則下取得獎牌級成績。

## 偵查過程

### 線索一：AlphaProof——把證明變成強化學習的迷宮

AlphaProof 的辦案流程可以拆成三步：

1. **形式化翻譯**：先把 IMO 自然語言題目翻譯成 Lean 4 的形式化命題 $T$ 。這一步目前仍需人工校對，因為自然語言的一詞多義是最大干擾犯。
2. **候選證明搜尋**：語言模型不斷提出 tactic 序列 $s_{1}, s_{2}, \cdots, s_{n}$ ，Lean 核心即時裁判每一步是否合法。若狀態推進，則給予獎勵 $r$ ；若卡死，則回溯。
3. **專家迭代與強化**：所有成功與失敗的軌跡都被回收為訓練資料，模型用強化學習更新，形成「越證越強」的迴路。其優化目標可寫為：

$$
J(\theta) = E_{\tau \sim \pi_{\theta}} [R(\tau)]
$$

其中 $\pi_{\theta}$ 是策略模型， $\tau$ 是證明軌跡， $R(\tau)$ 是 Lean 裁判給出的成功獎勵，外加 FunSearch 風格的程式進化壓力。

關鍵在於 Lean 的二元裁判：證明要麼被內核接受，要麼被拒絕，沒有灰色地帶。這給了強化學習最乾淨的訊號，避免了自然語言評價的模糊與作弊。

AlphaProof 還引入了非正式先行的策略：先用自然語言草擬證明大綱，再逐段形式化，猶如偵探先寫推理假說，再逐條找證據。

### 線索二：AlphaGeometry——83% 解題率的幾何專家

幾何題是 IMO 的硬骨頭，人類往往要畫出神來一筆的輔助線。AlphaGeometry 的解法是雙引擎：

- 快思考：語言模型負責「靈感」，提議加入哪些輔助點線圓。
- 慢思考：符號引擎負責「 deducation」，用演繹資料庫把所有可推導的角度 $A_{ABC}$ 、比例 $AB / CD$ 、共圓關係窮舉到底。

兩者迴圈直到目標 $Goal$ 被推出或超時。其在 2000 至 2022 年 IMO 幾何題上的表現是：30 題中解出 25 題，解題率高達 83% ，超過人類金牌選手的平均水準。

2024 年 IMO 的第 4 題幾何，AlphaGeometry 在數分鐘內即給出全形式化證明，而人類選手平均耗時超過一小時。這樁速破案讓幾何教練們既興奮又焦慮。

### 線索三：SOTA 戰況表與 FunSearch 側翼

2024 年前後的 AI 證明戰況，可用下表總覽：

| 系統 | 機構 | 戰場 | 戰績 |
|------|------|------|------|
| AlphaProof | DeepMind | IMO 2024 全科 | 6 題中 4 題，銀牌級 |
| AlphaGeometry | DeepMind | IMO 幾何 | 30 題中 25 題，約 83% |
| FunSearch | DeepMind | 組合構造 | 發現 cap set 新上界構造 |
| GPT-f / PACT | OpenAI | mathlib 預測 | tactic 預測先驅 |
| Lean Copilot | 加州理工 | Lean 輔助 | 即時 tactic 建議 |

其中 FunSearch 值得單列一案：它讓大語言模型不斷寫程式、跑測試、留優勝，把數學發現變成進化搜尋。雖然不直接輸出 Lean 證明，但它找到了人類沒見過的構造，證明了「AI 不只能驗證，還能發明」。

專家迭代（expert iteration）則是貫穿全案的手法：模型每解出一題，就把自己的成功6868證明餵回 mathlib 語料，下一輪更強。這正是 2013 年 Lean 播種、2017 年 mathlib 灌溉、2024 年 AI 收割的因果鏈。

## 結案報告

IMO 2024 銀牌不是終點，而是一份階段性結案報告：

- **銀牌的含金量**：4/6 題、28 分，在 609 名人類選手中可排前 40%，且全程以 Lean 機器可驗形式交卷，人類銀牌選手的紙本證明反而不具備這種保證。
- **剩下的兩題**：組合數論題仍是 AI 的滑鐵盧，需要的全局洞察與結構構造，現有搜尋還捉襟見肘。這恰好指出了下一步：更長的規劃、更好的抽象。
- **對數學社群的衝擊**：mathlib 的貢獻者開始用 AI 起草證明，審查者變成「AI 證據的覆核官」，協作模式正在改寫。
- **未來展望**：全自動形式化翻譯、自然語言與 Lean 的雙向互譯、AI 發現新猜想、乃至重演 2012 年 Odd Order 規模的機器輔助大證明，都是立案在案的下一波行動。終極懸念是：AI 會不會先於人類，拿下第一個由機器主導的新定理菲爾茲級成果？

用探案的話說：2024 年，AI 探員第一次戴上了銀色徽章。金色徽章，還在後頭。

## 證據與工具

**證據一：IMO 2024 戰績表**

| 題號 | 領域 | AlphaProof 結果 |
|------|------|------|
| 1 | 代數 | 解出，Lean 驗證通過 |
| 2 | 組合 | 解出，Lean 驗證通過 |
| 3 | 數論 | 未解出 |
| 4 | 幾何 | AlphaGeometry 解出 |
| 5 | 數論 | 未解出 |
| 6 | 代數 | 解出，Lean 驗證通過 |

總計 4/6，28 分，銀牌線。金牌線為 29 至 30 分，僅一題之差。

**證據二：Lean 形式的 IMO 題目骨架**

```lean
theorem imo2024_p1 (a b : ℕ) (h : 0 < a ∧ 0 < b) : P a b := by
  -- AI 生成的 tactic 序列在此展開
  -- 每一步都由 Lean 核心即時裁判
  sorry
```

其中 $P(a, b)$ 是題目的形式化命題， $sorry$ 是待填的搜尋空間，AlphaProof 的任務就是用合法 tactic 把 $sorry$ 消滅。

**證據三：偵探工具箱**

| 工具 | 作用 |
|------|------|
| Lean 4 ＋ mathlib | 唯一的機器法官與證據庫 |
| AlphaProof | 通用證明搜尋 ＋ 強化學習大腦 |
| AlphaGeometry | 幾何專用快慢雙引擎 |
| FunSearch ＋專家迭代 | 發現構造、自我進化的側翼部隊 |

**延伸閱讀**：DeepMind "AI achieves silver-medal standard solving International Mathematical Olympiad problems"（2024）；Trinh et al., "Solving olympiad geometry without human demonstrations"（Nature，2024）；Romera-Paredes et al., "Mathematical discoveries from program search with large language models"（Nature，2024）。
