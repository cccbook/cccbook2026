# 2023-LLM輔助EDA

## 案件摘要
AI 佈局（AlphaChip, 2021）之後，EDA 的最後一塊處女地：**設計本身**——寫 RTL、下約束、除錯、寫腳本，長期鎖在資深工程師腦中。2023 年，大語言模型（LLM）全面進場：NVIDIA 的 **ChipNeMo** 把 LLM 用於設計文件的問答與腳本生成；**ChatEDA**（2023-24）把 LLM 作為 EDA 流程的「自主代理」——自然語言下指令，LLM 編排工具鏈；**VerilogEval**（2023）基準讓 RTL 生成的品質可量化。LLM 從「程式碼助手」升級為「設計代理」，EDA 的自動化鏈從「演算法工具」延伸到「語意理解」——這是 Shannon 開關理論（1937）「設計可數學化」之後，第一次有工具試圖讓「設計意圖」本身可自動化。

## 前因 -- 為什麼會有這個案子
- **設計生產力差距（productivity gap）**：摩爾定律讓可做的晶片規模指數增長，工程師的生產力線性增長——設計人力是產業瓶頸。
- **經驗鎖在腦中**：腳本（Tcl/Perl）、約束（SDC）、除錯直覺都是「默會知識」，無法像演算法一樣自動化傳承。
- **LLM 就緒**（2022-2023）：GPT-4 等大模型在程式碼生成、文件理解上達到實用水準——「語意層的自動化」技術條件成熟。
- **驗證與腳本是 EDA 人力黑洞**：驗證佔設計週期 70%，腳本與約束的錯誤是流片失敗主因——LLM 的價值主張明確。

## 線索與推理 -- 數學式、程式、理論

### 核心：LLM 作為設計代理
LLM 的本質是**下一 token 機率分布**的建模：

$$P(x_t \mid x_{<t}) = \text{softmax}(W h_t), \quad h_t = \text{Transformer}(x_{<t})$$

EDA 的用法分三層：

| 層級 | 應用 | 實例 |
|------|------|------|
| 文件/知識層 | 規格問答、老手經驗檢索 | ChipNeMo（NVIDIA, 2023）|
| 腳本/工程層 | Tcl/SDC/Perl 腳本生成、工具命令 | ChipNeMo、Synopsys.ai（2023）|
| 設計/流程層 | RTL 生成、驗證計畫、流程編排 | ChatEDA、VerilogEval 基準 |

### ChatEDA：自然語言 → 工具鏈編排
ChatEDA 的架構：LLM 為「大腦」，EDA 工具為「手腳」——

$$\text{自然語言指令} \xrightarrow{\text{LLM 任務規劃}} \text{工具序列} \xrightarrow{\text{執行}} \text{結果回饋} \xrightarrow{\text{LLM 反思}} \cdots$$

LLM 把「用戶意圖」翻譯成 EDA 工具的調用序列（如：跑合成 → 時序分析 → 若違規調整約束重跑）——這是「代理（agent）」範式在 EDA 的第一次系統化：推理（reasoning）+ 工具使用（tool use）+ 回饋（reflection）的迴圈。

### VerilogEval：量化的基準
2023 年，NVIDIA 發布 VerilogEval 基準：156 個 Verilog 任務（由 HDLBits 題庫擴展），以功能正確率（模擬通過率）評分——RTL 生成的品質第一次可量化。初代 GPT-4 通過率約 50-60%，配 RAG/微調後更高——與當年 Chaff（2001）確立 SAT 求解基準同一「基準化」推理：可量化才能進步。

### 硬寫不出來的部分：LLM 的限制與工程化
- **幻覺（hallucination）**：LLM 生成的 RTL 可能有語意錯誤——必須配形式驗證（BDD/SAT/模型檢查）作守門員——「生成 + 驗證」的閉環是工程上的正解；
- **長上下文**：晶片規模的 netlist 遠超 LLM 上下文——層次化摘要（分層編碼模組）與檢索增強（RAG）是必要工程；
- **領域微調**：通用 LLM 對 RTL 語法不熟——ChipNeMo 用領域資料微調與 RAG，效率顯著提升。

## 結案 -- 後果與影響
- **EDA 自動化鏈的語意層**：從「演算法工具」（合成、佈局、繞線）到「語意代理」（LLM 編排）——自動化的最後一段（意圖 → 工具）被補上。
- **「生成 + 驗證」閉環的復興**：LLM 生成 + 形式驗證（BDD/SAT/SMC）守門——1986 年 BDD 案建立的驗證地基，在生成式時代成為必要配套。
- **設計知識的資產化**：腳本、約束、除錯經驗從默會知識變成可檢索、可生成的資產——EDA 的「傳承」方式改寫。
- **與 AlphaChip 的分工**：RL 佈局（空間決策）+ LLM 代理（語意編排）+ 演算法引擎（合成/驗證/物理驗證）——AI 時代 EDA 的三層架構成形。

## 關鍵人物與文獻
- **Mingjie Liu 等（NVIDIA）**：ChipNeMo 團隊。
- **Zhuoran Song 等**：ChatEDA 團隊。
- 文獻：
  - M. Liu et al., "ChipNeMo: Domain-Adapted LLMs for Chip Design," arXiv:2311.00176, 2023.
  - Z. Song et al., "ChatEDA: A Large Language Model Powered Autonomous Agent for EDA," *IEEE TCAD* 43, 2018 (2024)。
  - M. Liu et al., "VerilogEval: Evaluating Large Language Models for Verilog Code Generation," *ICCAD* 2023.
  - Synopsys.ai（2023）、Cadence JedAI（2023）——商業 AI-EDA 平台。
