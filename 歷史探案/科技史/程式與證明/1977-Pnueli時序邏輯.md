# 1977 年 Pnueli 時序邏輯：把「永遠」與「終將」寫進程式的探案

> 報案人：Amir Pnueli（特拉維夫大學，1977 年 FOCS 論文）。
> 涉案物：四個時態運算子 $G$ 、 $F$ 、 $X$ 、 $U$ 。兇器：Kripke 結構。

## 案發現場

1970 年代，並行程式與作業系統興起，Hoare 邏輯卻失靈了。
Hoare 三元組 $\{P\} \, C \, \{Q\}$ 只講「輸入輸出」，
不講執行過程中「會不會死鎖」「請求會不會永遠等不到回應」。

工業界的慘案很具體：兩個行程互等對方釋放資源，
程式「部分正確」卻永遠卡住。傳統前後條件對這種
「進行中」的性質一言不發。

Pnueli 是邏輯學家出身，熟悉哲學家的時態邏輯。
他盯著現場問：能否把「永遠（always）」「終將（eventually）」
「下一步（next）」「直到（until）」變成程式規格的正式語言？
1977 年 FOCS 論文〈The Temporal Logic of Programs〉就是報案筆錄。

## 偵查過程

### 線索一：LTL 四運算子——時間的指紋

Pnueli 引進線性時序邏輯 LTL。公式在「無窮執行路徑」上求值，
路徑 $\pi = s_0, s_1, s_2, \dots$ 的每個位置 $i$ 都有真值。

| 運算子 | 讀法 | 語義（ $\pi, i \models$ ） |
|---|---|---|
| $X \, \phi$ | 下一步 $\phi$ | $\pi, i+1 \models \phi$ |
| $G \, \phi$ | 永遠 $\phi$ | 對一切 $j \ge i$ 有 $\pi, j \models \phi$ |
| $F \, \phi$ | 終將 $\phi$ | 存在 $j \ge i$ 使 $\pi, j \models \phi$ |
| $\phi \, U \, \psi$ | $\phi$ 直到 $\psi$ | 存在 $k \ge i$ 使 $\pi, k \models \psi$ 且其前皆滿足 $\phi$ |

$G$ 與 $F$ 互為對偶： $F \, \phi \equiv \neg G \, \neg \phi$ 。
$U$ 最強， $F$ 與 $G$ 皆可由它定義： $F \, \psi \equiv true \, U \, \psi$ 。

### 線索二： $G(req \to F ack)$ ——一個規格的解剖

本案的明星證物是這條公式：

$$
G(req \to F ack)
$$

讀作「永遠：若此刻有請求 $req$ ，則未來終將有回應 $ack$ 」。
它是典型的**活性（liveness）**：好事終將發生。

對照組是**安全性（safety）**：壞事永不發生，例如互斥 $G(\neg (crit_1 \land crit_2))$ ；
以及**公平性**： $G \, F \, enabled \to G \, F \, taken$ 之類的無窮回應。

偵探用一條路徑驗屍：

$$
s_0(req) \to s_1(\emptyset) \to s_2(ack) \to s_3(req) \to s_4(ack) \to \cdots
$$

在 $s_0$ 的 $req$ 於 $s_2$ 被回應，在 $s_3$ 的 $req$ 於 $s_4$ 被回應，
故整條路徑滿足 $G(req \to F ack)$ 。
若存在一個 $req$ 之後永無 $ack$ ，公式即被判為假，反例就是那條字尾。

### 線索三：Kripke 結構——時間的舞台

時序公式要在模型上求值。Kripke 結構 $M = (S, R, L)$ 定義為：

- $S$ 為有限狀態集， $R \subseteq S \times S$ 為轉移關係。
- $L : S \to 2^{AP}$ 標示每狀態成立的原子命題。
- 路徑為滿足 $(s_i, s_{i+1}) \in R$ 的無窮序列。

驗證問題即： $M \models \phi$ 是否成立，亦即是否一切自初態出發的路徑皆滿足 $\phi$ ？

| 成分 | 例子（紅綠燈＋按鈕） |
|---|---|
| 狀態 $S$ | $\{idle, req, grant\}$ |
| 轉移 $R$ | $idle \to req \to grant \to idle$ |
| 標示 $L$ | $L(req) = \{req\}$ ， $L(grant) = \{ack\}$ |
| 性質 | $G(req \to F ack)$ 在此模型為真 |

Pnueli 把「程式正確性」從「前後斷言」擴張為「路徑性質」，
後來的模型檢測（1981）與工業規格語言（TLA+、PSL）全站在這個舞台上。

## 結案報告

Pnueli 一案把哲學邏輯變成了軟體工程的規格語言。
他區分了安全性與活性，給了並行程式第一套能講「永遠」與「終將」的數學。

遺產有三：

1. **LTL／CTL 分家**：Pnueli 開 LTL 線，Clarke 與 Emerson 開分支時序 CTL 線，兩派爭輝二十年。
2. **模型檢測的規格端**：1981 年 Clarke、Emerson、Sifakis 的演算法驗的正是這類公式。
3. **工業落地**：硬體性質語言 PSL、SVA 的時序運算子皆是 $G$ 、 $F$ 、 $U$ 的子孫。

Pnueli 因此獲 1996 年圖靈獎。時間，從此成為可以證明的對象。

## 證據與工具

- 對偶律： $G \, \phi \equiv \neg F \, \neg \phi$ ， $F \, \phi \equiv true \, U \, \phi$ 。
- 明星公式： $G(req \to F ack)$ 為活性， $G(\neg bad)$ 為安全性。
- Kripke 三元組 $M = (S, R, L)$ ，驗證即問 $M \models \phi$ 。

```text
狀態圖：idle --req--> waiting --ack--> idle
反例路徑：idle, waiting, waiting, waiting, ...
  -> 在 waiting 的 req 永無 ack，違反 G(req -> F ack)
```

- 實驗：在紙上畫三狀態 Kripke 結構，列出兩條無窮路徑，
  逐位置判定 $X \, p$ 、 $F \, p$ 、 $p \, U \, q$ 的真假，體會時序求值的遞迴。
- 文獻：Pnueli 1977 年 FOCS 論文，Clarke 等 1999 年《Model Checking》第一章。
