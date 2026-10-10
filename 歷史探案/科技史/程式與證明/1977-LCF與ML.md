# 1977 年 LCF 與 ML：可信核心的誕生探案

> 報案人：Robin Milner（愛丁堡，後赴史丹佛與劍橋）。

## 案發現場

1970 年代的定理證明器有個致命傷：證明器本身是幾萬行程式，誰能保證沒有 bug？
Boyer-Moore 用 Lisp 寫證明器，搜尋策略與邏輯糾纏在一起，錯一行就可能「證出」假定理。

Milner 在史丹佛研究 Scott 的計算理論 Logic for Computable Functions（LCF），
想把證明器建立在堅實基礎上。現場的三個難題是：

1. 如何讓證明器的可信部分小到可以人工審查？
2. 如何讓使用者自由撰寫證明策略，又不至於偽造證明？
3. 如何兼顧互動與自動，既讓人指揮，又讓機器苦幹？

1977 年左右，Milner 交出答案：LCF 架構＋ML 語言。
HOL、Isabelle、Coq 皆繼承此架構，影響延續至今。

## 偵查過程

### 線索一：抽象型別 thm——證明的封印

Milner 的神來一筆是借用抽象資料型別。系統中宣告一個型別 $thm$ ，
它只能由少數幾個「公理與推理規則」構造出來：

$$
\frac{}{\vdash A \quad (A 為公理)} \quad \frac{\vdash A \quad \vdash A \to B}{\vdash B}
$$

在 ML 中寫為：

```ocaml
abstype thm = Thm of formula
  with
    val axiom : formula -> thm
    val modus_ponens : thm * thm -> thm
    val gen : var -> thm -> thm
end
```

使用者可以在 $thm$ 之外寫任意程式，即使寫錯也造不出假的 $thm$ 值，
因為唯一能產生 $thm$ 的函數就是那幾個可信原語。
這就是**可信核心（trusted kernel）**：小到可審查，強到撐起一切。

| 設計 | 可信代碼量 | 風險 |
|---|---|---|
| 整台證明器皆可信 | 數萬行 | 一處 bug 即崩盤 |
| LCF 可信核心 | 數百至數千行 | 只需審查核心 |
| 核心＋證明物件 | 核心小，證明可獨立檢查 | 最穩，可第三方驗證 |

### 線索二：ML——為證明而生的函數式語言

為了寫證明策略，Milner 發明了 ML（Meta Language）。
它有三件利器：

1. 高階函數：策略本身就是函數， $tactic$ 類型為 $goal \to (subgoal \, list \times proof)$ 。
2. 多型與型別推論：寫策略不必寫型別標註， $let$ 多型自動推導。
3. 例外與模式匹配：搜尋失敗即丟例外，回溯乾淨俐落。

一個 $tactic$ 把目標 $G$ 化為子目標 $G_1$ 與 $G_2$ ，
一個 $tactical$ 把小策略組合成大策略，例如 $THEN$ 、 $ORELSE$ 、 $REPEAT$ ：

$$
TACTIC_1 \, THEN \, TACTIC_2 \quad,\quad REPEAT(TAC) \quad,\quad TAC_1 \, ORELSE \, TAC_2
$$

例如證明 $A \land B$ 的策略是先拆合取消去，再分別證明 $A$ 與 $B$ ：

```ocaml
let prove_conj = CONJ_TAC THENL [prove_A; prove_B]
```

策略語言與物件邏輯徹底分離：錯的策略最多證明失敗，絕不會證明出假定理。

### 線索三：血脈——HOL、Isabelle、Coq 皆繼承此架構

LCF 本是為 Scott 的 LCF 邏輯打造，但架構一出，人人仿效：

| 後裔 | 繼承點 | 差異 |
|---|---|---|
| HOL（Gordon 1986） | LCF 核心＋ML 策略 | 邏輯換為 Church 高階邏輯 |
| Isabelle（Paulson 1986） | 可信核心＋tactics | 核心改為通用邏輯框架 |
| Coq（1989） | 核心小而可信的精神 | 核心改為型別檢查器，證明即程式 |
| Lean、HOL Light | 同上 | 核心更小，強調獨立檢查 |

一句话：現代證明器都是「小核心＋大策略層」的兩層建築，
圖紙正是 Milner 在 1977 年畫下的。

## 結案報告

LCF 破了「誰來證明證明器」的後設案件。
它沒有讓證明器一次就全自動，而是讓人類寫高階策略、
機器執行低階細節，且一切结果都經核心封印認證。

遺產有三：

1. **可信核心原則**：今天審查 Coq、Lean、Isabelle，第一件事就是看核心有多小。
2. **ML 語言家族**：Standard ML、OCaml、F# 皆源於此，函數式程式因此發揚光大。
3. **tactics 範式**： $tactic$ 與 $tactical$ 的詞彙成為全行業通用語，
   從 Coq 的 $Ltac$ 到 Lean 的 $tactic$ 框架皆是回聲。

Milner 因此獲 1991 年圖靈獎。

## 證據與工具

- 核心三公設： $thm$ 只能由公理與原語構造，任何 $tactic$ 失敗只回傳失敗而非假 $thm$ ，核心程式碼行數即信任成本。
- $tactic$ 簽名： $tactic : goal \to ((goal \, list) \times (thm \, list \to thm))$ ，前者是子目標，後者是正當性函數。
- 最小模擬（概念 Python）：

```python
class Thm:
    def __init__(self, f): self.f = f  # 私有構造，外界禁調
def modus_ponens(th1, th2):
    # 僅當 th2 為 th1.f -> X 形狀才放行
    return Thm(conclusion)
```

- 實驗：寫一個錯的 $tactic$ ，觀察它只能「失敗」不能「造假」，體會封印威力。
- 文獻：Milner 1979 年〈LCF: A Way of Doing Proofs with a Machine〉，Gordon 2000 年回顧史。
