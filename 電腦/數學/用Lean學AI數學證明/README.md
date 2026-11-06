# Lean 與 AI 數學證明：從形式化基礎到 AI 攻克數學難題

本書講述一條橫跨近百年的故事線：**數學如何被「形式化」、證明如何被「機器檢查」、AI 如何最終學會寫出人類級別的數學證明**。

從 Hilbert 計畫與哥德爾不完備定理出發，經過證明論、Curry–Howard 對應、Coq/Agda 的類型論傳統，深入 Lean 4 的型別系統、 dependent types、tactic 與 Mathlib；最後落到近年最熱門的戰場 —— AlphaProof 在 IMO 2024 拿下銀牌、AlphaGeometry 攻克平面幾何、Formal Conjectures 資料庫與 OpenAI/DeepMind 的 LLM 證明代理（Harmonic/Axiom 等 2024–2026 新進展）。

全書延續本系列「理論驅動實務」的風格：每一項技術（型別論、 tactic engine、RL、資料合成）的出現，都是為了解決前一代方法的某個缺陷；理解這些前因後果，才能看懂 AI 證明真正突破在哪裡、還缺什麼。

## 本書特色

- **雙主線交織**：一條是「數學基礎與形式化」的哲學/邏輯史，一條是「機器定理證明」的工程史，兩線在 Lean 匯合
- **可動手**：第 3～6 章全部有 Lean 4 實作，可在電腦上逐行驗證
- **緊跟前沿**：涵蓋至 2026 年的 AlphaProof、LeanDojo、PutnamBench、Formal Conjectures 等最新成果
- **前因後果**：每章說明「上一代為什麼不夠 → 這一代解決了什麼 → 還留下什麼問題」

## 目錄

* 第1章-數學基礎危機：證明為何需要被形式化
    * [1.1-1874 與 1897：Cantor 集合論與第三次數學危機的引爆點](01.1-Cantor集合論與第三次數學危機.md)
    * [1.2-1900 Hilbert 計畫：23 個問題與「證明可以被機械檢查」的夢想](01.2-Hilbert計畫.md)
    * [1.3-1931 哥德爾不完備定理：夢想的天花板與意外開啟的計算時代](01.3-哥德爾不完備定理.md)
    * [1.4-1936 與 1940：圖靈機、Church 的 λ 演算，以及 Gentzen 的自然演繹](01.4-圖靈機、λ演算與自然演繹.md)

* 第2章-證明助理的前史：從 LCF 到 Coq
    * [2.1-1972 AUTOMATH 與 de Bruijn：讓電腦檢查證明的先驅](02.1-AUTOMATH與deBruijn.md)
    * [2.2-1977 LCF 方案：可信核心與 tactic 的誕生](02.2-LCF方案：可信核心與tactic的誕生.md)
    * [2.3-1984 Coq 與 1990 年代：Curry–Howard 對應如何把證明變成程式](02.3-Coq與Curry-Howard對應.md)
    * [2.4-2004 四色定理與 2012 奇異吸引子：大型形式化的里程碑年代](02.4-四色定理與大型形式化里程碑.md)

* 第3章-Lean 的誕生與型別論基礎
    * [3.1-2013 Leonardo de Moura：從 Coq/Z3 走向 Lean 的動機](03.1-LeandeMoura與Lean的誕生.md)
    * [3.2-依值型別論：從 LF、Calculus of Constructions 到 Lean 的 CIC](03.2-依值型別論與CIC.md)
    * [3.3-命題即型別、證明即項：Curry–Howard 在 Lean 中的實體化](03.3-命題即型別：證明即項.md)
    * [3.4-2017 Lean 3 與 2023 Lean 4：從 metalang 到 C/C++ 可信核心的重生](03.4-Lean3到Lean4的重生.md)

* 第4章-Lean 4 實戰入門
    * [4.1-環境建置與第一個定理：elan、Lake、VS Code](04.1-Lean4環境建置與第一個定理.md)
    * [4.2-基礎邏輯：And/Or/Not/存在量詞的 tactic 證明](04.2-基礎邏輯與tactic證明.md)
    * [4.3-自然數與歸納法：從 Peano 到 mathlib 的 Nat](04.3-自然數與歸納法.md)
    * [4.4-集合、函數與實數：在 Lean 中重建大學數學](04.4-集合、函數與實數.md)

* 第5章-Mathlib：數學的大教堂
    * [5.1-2017 至今 Mathlib 社群：一個百萬行的形式化數學圖書館如何運作](05.1-Mathlib社群與運作.md)
    * [5.2-class、instance 與 hierarchy：群、環、體的代數結構層級](05.2-代數結構層級與typeclass.md)
    * [5.3-2022 liquid tensor experiment：Peter Scholze 親自驗證的極限挑戰](05.3-liquid_tensor_experiment.md)
    * [5.4-形式化數學的寫作風格：如何把論文翻譯成 Lean](05.4-把論文翻譯成Lean.md)

* 第6章-自動化證明的譜系
    * [6.1-1965 Robinson resolution：自動定理證明的起點與一階邏輯飽和法](06.1-Resolution與自動定理證明起點.md)
    * [6.2-SMT 求解器與 Z3：de Moura 的第一場革命](06.2-SMT求解器與Z3.md)
    * [6.3-decidability、AESOP 與 Mathlib 自動化：tactic 的工程學](06.3-AESOP與tactic自動化工程.md)
    * [6.4-與 NeurIPS 時代的對比：符號搜尋為何無法單獨攻克 IMO](06.4-符號搜尋的極限.md)

* 第7章-AI 與形式化數學的相遇
    * [7.1-2017 transformer 與 GPT：語言模型能學到「數學語感」嗎](07.1-Transformer與數學語感.md)
    * [7.2-2019 GPT-f 與 Metamath：第一批 LLM 證明的嘗試](07.2-GPT-f與首批LLM證明.md)
    * [7.3-2020 LeanDojo、miniF2F 與 ReProver：基準與檢索如何改變賽局](07.3-LeanDojo、miniF2F與ReProver.md)
    * [7.4-2022 AlphaCode 與 HoTT/程式合成的啟示：從寫程式到寫證明的距離](07.4-從寫程式到寫證明.md)

* 第8章-AlphaGeometry、AlphaProof：DeepMind 的 IMO 突圍
    * [8.1-2024.01 AlphaGeometry：語言模型＋符號引擎的「雙腦」架構](08.1-AlphaGeometry雙腦架構.md)
    * [8.2-2024.07 AlphaProof 與 IMO 銀牌：MCTS、RL 與 Lean 回饋訊號](08.2-AlphaProof與IMO銀牌.md)
    * [8.3-2025 AlphaGeometry2 與後續：TremTrin 合成資料與接近金牌](08.3-AlphaGeometry2與金牌之路.md)
    * [8.4-2025.06 IMO 金牌級 AI 系統：Google DeepMind 與 OpenAI 的正面交鋒](08.4-IMO金牌級AI系統.md)

* 第9章-開源生態與 LLM 代理時代
    * [9.1-Lean copilot、Harmonic、Axiom：新創公司與開源社群的證明代理](09.1-證明代理與新創生態.md)
    * [9.2-2024-2025 PutnamBench、miniCTX 與 Formal Conjectures：AI 能解多少競賽與研究難題](09.2-競賽基準與FormalConjectures.md)
    * [9.3-RLVR 與 process reward model：如何用 Lean 作為完美的獎勵函數](09.3-RLVR與獎勵函數.md)
    * [9.4-vibe proving：一般人如何用 AI 在 Lean 中證明自己的第一個定理](09.4-vibeproving實戰.md)

* 第10章-未竟之路：AI 能解決未解猜想嗎？
    * [10.1-從競賽到研究數學的鴻溝：為什麼 IMO ≠ 研究前沿](10.1-從競賽到研究數學的鴻溝.md)
    * [10.2-形式化研究數學的先行者：Fernando、Kevin Buzzard 的 FTC、以及 2024-2026 的 Fermat 最後定理計畫](10.2-形式化研究數學的先行者.md)
    * [10.3-大模型＋符號系統＋超算：通往「AI 數學家」的三階段路線圖](10.3-通往AI數學家的路線圖.md)
    * [10.4-哲學反思：當證明不再由人寫下，數學是什麼？](10.4-當證明不再由人寫下.md)

## 閱讀方式

- 第 1～2 章是歷史與邏輯基礎，不需要會寫程式
- 第 3～6 章是 Lean 實作核心，建議邊讀邊在電腦上跑
- 第 7～10 章是 AI 主線，讀懂前六章才能看懂為什麼 AlphaProof 選擇 Lean 而不是直接讓 LLM 自由發揮
- 趕時間的讀者：1.3 → 2.3 → 3.2 → 3.4 → 7.3 → 8.2 → 8.4 → 10.3 這條主軸也可以連成故事

## 需要的背景知識

- 高中數學與基礎邏輯（命題邏輯、簡單證明）
- 建議有一點程式設計經驗（任何語言皆可）
- 不需要先學過型別論或數理邏輯

---

如需調整章節（例如加深 Lean 實作比重、增加類型論章節、或加入 Coq/Isabelle 對比專章），請告訴我。
