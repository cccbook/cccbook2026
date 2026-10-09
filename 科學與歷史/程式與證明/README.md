# 程式與證明的歷史年表（科學史）

> 程式與證明是同一枚硬幣的兩面：程式是「會執行的證明」，證明是「會說話的程式」。從亞里斯多德的三段論、布林代數、弗雷格的謂詞邏輯，到希爾伯特的形式主義夢想、哥德爾的粉碎與根岑的救贖，再到 Logic Theorist、歸結原理、Hoare 邏輯、LCF、Coq、Isabelle、模型檢測、SMT、CompCert、seL4，直到 Lean 與 AI 自動證明——這部歷史就是人類追問「機器能否替我們證明，程式能否保證正確」的兩千年探案史。
>
> 本書以「推理探案」的方式，為每個歷史事件寫一篇 wiki，包含前因後果、理論與公式。每篇檔名以年份開頭。

## 目錄（Wiki 書篇目）

### 第一幕：邏輯的誕生 — 從三段論到形式系統（前350–1934）

| 年份 | 事件 | Wiki |
|------|------|------|
| 前350 | 亞里斯多德三段論：史上第一套形式推理系統 | [-0350-Aristotle三段論.md](-0350-Aristotle三段論.md) |
| 1847 | Boole 布林代數：把邏輯變成計算 | [1847-Boole布林代數.md](1847-Boole布林代數.md) |
| 1879 | Frege《概念文字》：謂詞邏輯誕生，量詞與形式證明之源 | [1879-Frege概念文字.md](1879-Frege概念文字.md) |
| 1900 | Hilbert 23 問題與第二問題：公理化一切數學的夢想 | [1900-Hilbert23問題.md](1900-Hilbert23問題.md) |
| 1910 | 《數學原理》：Russell 與 Whitehead 用邏輯重建數學 | [1910-PrincipiaMathematica.md](1910-PrincipiaMathematica.md) |
| 1929 | Herbrand 定理：一階邏輯可證性歸約為命題邏輯，自動證明之母 | [1929-Herbrand定理.md](1929-Herbrand定理.md) |
| 1931 | Gödel 不完備定理：形式系統的極限，希爾伯特夢碎 | [1931-Godel不完備定理.md](1931-Godel不完備定理.md) |
| 1934 | Gentzen 自然演繹與矢列演算：現代證明論的結構 | [1934-Gentzen自然演繹.md](1934-Gentzen自然演繹.md) |

### 第二幕：計算與證明的交會 — 機器開始推理（1940–1969）

| 年份 | 事件 | Wiki |
|------|------|------|
| 1940 | Church 簡單型別理論：高階邏輯的起點，HOL 的祖先 | [1940-Church簡單型別理論.md](1940-Church簡單型別理論.md) |
| 1957 | Logic Theorist：Newell、Simon、Shaw 寫出第一個自動定理證明器 | [1957-LogicTheorist.md](1957-LogicTheorist.md) |
| 1960 | Davis–Putnam 程序：命題可滿足性的第一個實用演算法 | [1960-DavisPutnam程序.md](1960-DavisPutnam程序.md) |
| 1962 | DPLL 演算法：Davis、Logemann、Loveland 的回溯搜尋，SAT 求解器之祖 | [1962-DPLL.md](1962-DPLL.md) |
| 1963 | Robinson 歸結原理：合一演算法，一階證明的單一推理規則 | [1963-Robinson歸結原理.md](1963-Robinson歸結原理.md) |
| 1967 | Automath：de Bruijn 的第一個電腦證明檢查器，Coq 的精神祖先 | [1967-Automath.md](1967-Automath.md) |
| 1969 | Floyd–Hoare 邏輯：用斷言證明程式正確（含 Dijkstra 最弱前條件） | [1969-Hoare邏輯.md](1969-Hoare邏輯.md) |
| 1969 | Howard 公式即型別：Curry–Howard 對應完成，證明＝程式 | [1969-Howard公式即型別.md](1969-Howard公式即型別.md) |

### 第三幕：互動式證明與模型檢測 — 證明的工程化（1972–1989）

| 年份 | 事件 | Wiki |
|------|------|------|
| 1972 | Prolog：Colmerauer 與 Kowalski 把 Horn 子句變成程式語言 | [1972-Prolog邏輯程式.md](1972-Prolog邏輯程式.md) |
| 1973 | Boyer–Moore 定理證明器：Nqthm，歸納證明的自動化先鋒 | [1973-BoyerMoore證明器.md](1973-BoyerMoore證明器.md) |
| 1977 | LCF 與 ML：Milner 的可信核心架構＋函數式語言 | [1977-LCF與ML.md](1977-LCF與ML.md) |
| 1977 | Pnueli 時序邏輯：把「永遠」「終將」帶入程式驗證 | [1977-Pnueli時序邏輯.md](1977-Pnueli時序邏輯.md) |
| 1981 | 模型檢測誕生：Clarke、Emerson、Sifakis 窮舉狀態空間 | [1981-ModelChecking誕生.md](1981-ModelChecking誕生.md) |
| 1986 | HOL 系統：Mike Gordon 為硬体验證打造高階邏輯證明器 | [1986-HOL系統.md](1986-HOL系統.md) |
| 1986 | Isabelle：Paulson 的通用邏輯框架，開啟證明器家族 | [1986-Isabelle.md](1986-Isabelle.md) |
| 1988 | 構造演算 CoC 與歸納構造演算 CIC：Coquand、Huet、Paulin 的依賴型別宇宙 | [1988-CoC與CIC.md](1988-CoC與CIC.md) |
| 1989 | Coq 誕生：Dowek 等人實作，構造性證明的工程結晶 | [1989-Coq誕生.md](1989-Coq誕生.md) |
| 1989 | ACL2：Boyer、Kaufmann、Moore 的工業級歸納證明器 | [1989-ACL2.md](1989-ACL2.md) |

### 第四幕：自動化與大規模驗證 — 證明走進工業（1992–2009）

| 年份 | 事件 | Wiki |
|------|------|------|
| 1992 | SMV 與 BDD 符號模型檢測：McMillan 讓百萬狀態驗證成真 | [1992-SMV符號模型檢測.md](1992-SMV符號模型檢測.md) |
| 1996 | Proof-Carrying Code：Necula 與 Lee 讓程式自帶證明 | [1996-ProofCarryingCode.md](1996-ProofCarryingCode.md) |
| 1999 | TLA+：Lamport 的規格語言，並行系統的數學建模 | [1999-TLAplus.md](1999-TLAplus.md) |
| 2001 | Chaff 與現代 SAT 革命：CDCL 讓百萬變元求解成真 | [2001-Chaff與SAT革命.md](2001-Chaff與SAT革命.md) |
| 2005 | 四色定理的 Coq 驗證：Gonthier 封印百年爭議 | [2005-FourColor定理Coq驗證.md](2005-FourColor定理Coq驗證.md) |
| 2006 | CompCert 驗證編譯器：Leroy 證明編譯器 preserves 語意 | [2006-CompCert驗證編譯器.md](2006-CompCert驗證編譯器.md) |
| 2008 | Z3 與 SMT 革命：de Moura 與 Bjorner 的可滿足性模理論 | [2008-Z3與SMT革命.md](2008-Z3與SMT革命.md) |
| 2009 | seL4 微核心驗證：九千行 C＋六十萬行證明的作業系統核心 | [2009-seL4微核心驗證.md](2009-seL4微核心驗證.md) |

### 第五幕：數學大一統與 AI 證明 — 證明的未來（2012–至今）

| 年份 | 事件 | Wiki |
|------|------|------|
| 2012 | Odd Order 定理與 MathComp：Gonthier 用 Coq 征服群論巨著 | [2012-OddOrder與MathComp.md](2012-OddOrder與MathComp.md) |
| 2013 | HoTT 同倫型別論：Voevodsky 的 Univalence，數學基礎重構 | [2013-HoTT同倫型別論.md](2013-HoTT同倫型別論.md) |
| 2013 | Lean 誕生（Lean 1）：de Moura 打造人人可用的證明器 | [2013-Lean誕生.md](2013-Lean誕生.md) |
| 2014 | Flyspeck 落幕：Hales 用 HOL Light＋Isabelle 證完克卜勒猜想 | [2014-Flyspeck克卜勒猜想.md](2014-Flyspeck克卜勒猜想.md) |
| 2015 | Lean 2 正式發布：約束求解 elaborator＋Lua 前端，CADE 論文 | [2015-Lean2正式發布.md](2015-Lean2正式發布.md) |
| 2015 | Iris 並行分離邏輯：Jung 等人征服 Rust 與併發推理 | [2015-Iris並行分離邏輯.md](2015-Iris並行分離邏輯.md) |
| 2017 | Lean 3 與 mathlib：元程式框架＋百萬行函式庫大爆炸 | [2017-Lean3與mathlib.md](2017-Lean3與mathlib.md) |
| 2021 | Lean 4 自舉：用 Lean 重寫 Lean，證明器變程式語言 | [2021-Lean4自舉.md](2021-Lean4自舉.md) |
| 2024 | AlphaProof＋AlphaGeometry：AI 在 IMO 拿下銀牌逼近金牌 | [2024-AlphaProof與AI證明.md](2024-AlphaProof與AI證明.md) |

## 因果鏈總覽

```
亞里斯多德 (-350) ── 三段論 ── Boole (1847) ── 代數化 ── Frege (1879) ── 謂詞邏輯
     │                                                              │
     │                                                              ├─ Hilbert (1900) ── 公理化夢想
     │                                                              │      │
     │                                                              │      ├─ Principia (1910) ── 邏輯主義高峰
     │                                                              │      ├─ Herbrand (1929) ── 自動證明之母
     │                                                              │      └─ Gödel (1931) ── 夢碎 / 極限
     │                                                              │
     │                                                              └─ Gentzen (1934) ── 自然演繹/矢列 ── Howard (1969) ── Curry-Howard
     │                                                                                                          │
     │                                                                                                          ├─ Automath (1967) ── 證明檢查器
     │                                                                                                          ├─ CoC/CIC (1988) ── 依賴型別
     │                                                                                                          ├─ Coq (1989) ── 四色 (2005) ── Odd Order (2012)
     │                                                                                                          └─ Lean 1 (2013) ── Lean 2 (2015) ── Lean 3+mathlib (2017) ── Lean 4 自舉 (2021) ── AlphaProof (2024)
     │
     ├─ Church (1940) ── 簡單型別 ── HOL (1986) ── Isabelle (1986) ── Flyspeck (2014)
     │
     ├─ Logic Theorist (1957) ── DP (1960) ── DPLL (1962) ── Robinson歸結 (1963) ── Prolog (1972)
     │                                                              │
     │                                                              └─ Chaff/SAT (2001) ── Z3/SMT (2008) ── 軟硬體驗證
     │
     ├─ Floyd-Hoare (1969) ── Dijkstra ── Boyer-Moore (1973) ── ACL2 (1989) ── PCC (1996) ── CompCert (2006)
     │
     └─ Pnueli時序 (1977) ── Model Checking (1981) ── SMV/BDD (1992) ── TLA+ (1999) ── seL4 (2009)
              │
              └─ LCF/ML (1977) ── 可信核心 ── 所有現代證明器架構
```

## 寫作方式說明

每篇 wiki 採「推理探案」結構：

1. **案發現場（前因）**：當時的未解之謎是什麼？誰遇到的？為何重要？
2. **偵查過程（推理）**：主角如何思考？關鍵靈感為何？核心技術（邏輯規則、演算法、型別系統、證明策略）如何推導，含數學式與表格。
3. **結案報告（後果）**：謎題如何解？留下什麼遺產？影響了哪些後續事件？
4. **證據與工具**：關鍵公式、證明規則表、演算法虛擬碼或 Python 模擬程式、Coq/Lean/SMT 範例（非必要不硬寫程式，優先講清理論）。
