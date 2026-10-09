# 1986 年 Isabelle：通用邏輯框架的連環探案

> 報案人：Lawrence Paulson（劍橋，師從 Gordon）。
> 案件性質：HOL 雖好，但每個邏輯都重寫一台證明器，太浪費。能否一台證明器容納多種邏輯？

## 案發現場

1986 年，Gordon 的 HOL 正如日中天，但 Paulson 看到一個盲點：
LCF 架構綁死單一物件邏輯。想玩一階邏輯、Zermelo 集合論、
直覺主義邏輯，就得另起爐灶。證明器的 tactic、搜尋、解析器全得重寫。

與此同時，歐洲各派邏輯百花齊放：Martin-Löf 型別論、
模態邏輯、構造性數學，各有信徒。沒有通用框架，
自動推理就會分裂成互不相通的孤島。

Paulson 在劍橋與慕尼黑工大（Nipkow 加入後）立志：
打造一台「邏輯的邏輯」的證明器——Isabelle。
它的物件邏輯應如插件般可換，核心推理引擎保持不變。

## 偵查過程

### 線索一：元邏輯——邏輯的邏輯

Isabelle 的絕招是引進一個極小的**元邏輯**（meta-logic），
只有蘊含 $\Longrightarrow$ 、全稱 $\bigwedge$ 與等式 $\equiv$ 三個連接詞。
一切物件邏輯的規則都被編碼為元邏輯公理。

例如一階邏輯的合取消去：

$$
\frac{P \land Q}{P} \quad \leadsto \quad \bigwedge P \, \bigwedge Q \, . \, (P \land Q) \Longrightarrow P
$$

物件邏輯的證明即元邏輯的證明，Isabelle 的核心只懂元邏輯的歸結：
由 $A \Longrightarrow B$ 與 $A$ 得 $B$ ，外加高階合一。

| 層次 | 例子 | 角色 |
|---|---|---|
| 元邏輯 | $\bigwedge x \, . \, P(x) \Longrightarrow Q$ | 通用黏合劑 |
| 物件邏輯 | HOL、一階邏輯、ZF | 可插拔的規則集 |
| 證明腳本 | Isar、tactic | 使用者介面 |

換邏輯＝換一組元邏輯公理，引擎、tactic、搜尋全部沿用。
這就是「通用邏輯框架」的含義。

### 線索二：Isabelle／HOL 與 Isar——從 tactic 堆到可讀證明

早期 Isabelle 允許各家物件邏輯並存，但實務上勝出的是 Isabelle／HOL：
以 HOL 為物件邏輯，兼得 HOL 的表達力與 Isabelle 的靈活性，
後來反超原生 HOL，成為 Flyspeck 與 seL4 的主力之一。

更大的變革是 Isar（Intelligible semi-automated reasoning）結構化證明語言。
傳統 tactic 腳本是「操作錄影」：

```isabelle
apply (induct x)
apply auto
```

人類看不懂，壞了難修。Isar 改寫為可讀的類自然語言：

```isabelle
proof (induct x)
  case Nil show ?case by simp
next
  case (Cons a xs) thus ?case by simp
qed
```

每個 $have$ 、 $show$ 、 $hence$ 都是顯式的邏輯斷言，
機器檢查每一步，讀者讀懂每一步。證明從「咒語」變成「文章」。

### 線索三：Sledgehammer 伏筆——人機聯手的預告

Isabelle 的另一條伏線是自動化整合。tactic 雖強，
但大量瑣碎引理仍需手工餵。Paulson 早早佈局：
讓外部自動證明器（ATP）與 SMT 求解器當 Isabelle 的打手。

後來的 Sledgehammer（2000 年代末成形）正是此伏筆的開花：
把目標丟給 E、Vampire、Z3，找回的證明再重建成 Isabelle 可信核心認可的步驟。
本案先埋線，第四幕的 SMT 革命將回來引爆。

| 工具 | 分工 |
|---|---|
| Isabelle 核心 | 唯一可信，檢查每步 |
| tactics＋Isar | 人類指揮結構 |
| Sledgehammer＋ATP | 機器填補瑣碎間隙 |

## 結案報告

Isabelle 於 1986 年問世，1990 年代由 Paulson 與 Nipkow 持續打磨，
成為與 HOL、Coq 鼎足而立的三大證明器之一。

結案意義：

1. **框架戰勝單品**：證明通用引擎＋可插拔邏輯是可行且划算的。
2. **可讀證明**：Isar 證明了機器證明也可以是人類文獻，影響 Lean 的結構化 tactic。
3. **人機協作範式**：可信核心＋自動打手的分工，預告了今天的 hammer 文化。

Isabelle 案是 LCF 血脈的第二次演化：從單一邏輯走向邏輯廣場。

## 證據與工具

- 元蘊含： $P \Longrightarrow Q$ 為框架層蘊含，區別於物件層 $P \to Q$ 。
- 元全稱： $\bigwedge x \, . \, P(x)$ 為框架層全稱，區別於物件層 $\forall x \, . \, P(x)$ 。
- 規則編碼例：合取引入編碼為 $\bigwedge P \, \bigwedge Q \, . \, P \Longrightarrow Q \Longrightarrow (P \land Q)$ 。

```isabelle
lemma app_nil: "app xs [] = xs"
  by (induct xs) auto
(* Sledgehammer 會建議: by (simp add: app_def) *)
```

- 實驗：在 Isabelle／HOL 中分別用 $apply$ 腳本與 $Isar$ 重寫同一個串列引理，
  比較可讀性與報錯定位，體會結構化證明的價值。
- 文獻：Paulson 1994 年《Isabelle: A Generic Theorem Prover》，
  Wenzel 2007 年 Isar 參考手冊。
