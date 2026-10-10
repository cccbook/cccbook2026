# 1988 年 CoC 與 CIC：構造演算的心臟探案

> 報案人：Thierry Coquand（1985 博士論文）與 Gérard Huet（INRIA），
> 增援：Christine Paulin-Mohring（歸納擴充）。
> 涉案物：一個依賴函數型 $\Pi x:A. B(x)$ 撐起的宇宙。

## 案發現場

1980 年代中期，證明器分裂為兩大陣營：
HOL／Isabelle 走古典高階邏輯，Boyer-Moore 走一階計算邏輯，
Automath 與 Martin-Löf 型別論走構造性路線，三方互不相通。

構造派有一個夢：把 Howard「公式即型別」的格言推到極致，
讓命題、證明、程式、型別全住在同一個演算裡。
但 Automath 語言龐雜，Martin-Löf 系統層次繁複，
缺一台既極簡又強大的核心演算。

1985 至 1988 年，Coquand 在 Huet 指導下交出構造演算 CoC（Calculus of Constructions），
1988 年論文正式發表；Paulin-Mohring 隨後加入歸納型別，
形成歸納構造演算 CIC。Coq 的心臟就此裝好。

## 偵查過程

### 線索一： $\Pi x:A. B(x)$ ——一個構造統治一切

CoC 的核心只有一個黏合劑：依賴函數型。記為 $\Pi x:A. B(x)$ ，
讀作「對一切 $x:A$ ，給出一個 $B(x)$ 」。它同時是三種東西：

| 讀法 | $\Pi x:A. B(x)$ 的含義 | 例子 |
|---|---|---|
| 邏輯讀法 | 全稱命題 $\forall x:A. B(x)$ | $\Pi n:nat. n \ge 0$ |
| 程式讀法 | 依賴函數，它的回傳型依賴輸入值 | `vec_add : Π n:nat. Vec n -> Vec n` |
| 證明讀法 | 證明對象，輸入 $x$ 的證明輸出 $B(x)$ 的證明 | 蘊含 $A \to B$ 只是 $B$ 不依賴 $x$ 的特例 |

普通函數型 $A \to B$ 、全稱量詞 $\forall x. P(x)$ 、蘊含 $P \to Q$ ，
全是 $\Pi$ 的特例。 $\lambda x:A. t$ 是構造， $f(a)$ 是消去，
$\beta$ 歸約 $(\lambda x. t)(a) \to t[a/x]$ 既是計算也是證明化簡。

宇宙層次 $Prop : Type_1 : Type_2 : \cdots$ 避免了 Girard 悖論，
$Prop$ 住命題， $Type_i$ 住資料型別，兩者用同一套規則管理。

### 線索二：脈絡＋歸納型別——從純函數到數學世界

CIC 的判斷形如 $\Gamma \vdash t : T$ ，其中脈絡 $\Gamma$ 是
$x_1:A_1, \dots, x_n:A_n$ 的有序名冊，記錄每個變元的型別。
推理即在脈絡中構造 well-typed 的項：

$$
\frac{\Gamma, x:A \vdash t : B(x)}{\Gamma \vdash \lambda x:A. t : \Pi x:A. B(x)}
$$

$$
\frac{\Gamma \vdash f : \Pi x:A. B(x) \quad \Gamma \vdash a : A}{\Gamma \vdash f(a) : B(a)}
$$

Paulin-Mohring 的關鍵增援是**歸納型別**：允許直接宣告

$$
nat := 0 \mid S(n: nat)
$$

$$
list(A) := nil \mid cons(a:A, l:list(A))
$$

並自動生成歸納原理與 $match$ 消去子。沒有它，
自然數得用 Church 編碼 $ \lambda f. \lambda x. f^n(x)$ 苦撐，
推理 painfully 間接；有了它， $induction$ 即 $match$ 加遞迴，
程式與證明終於同形。

| 演算 | 有無歸納型別 | 後果 |
|---|---|---|
| 純 CoC 1988 | 無原生歸納 | 表達力強但用起來痛 |
| CIC 1990s | 有 $Inductive$ | Coq 可直接寫 $nat$ 、 $list$ 、 $vec$ |

### 線索三：與 HOL 的分岔——構造 vs 古典

偵探把 CIC 與 HOL 並列驗屍：

| 維度 | HOL | CIC |
|---|---|---|
| 邏輯 | 古典，外加排中律無礙 | 構造性，排中律需另加公理 |
| 證明 | tactic 構造 $thm$ | 構造 $\lambda$ 項，型別檢查即驗證 |
| 計算 | 邏輯外另有求值 | $\beta \iota$ 歸約內建於轉換規則 |
| 萃取 | 困難 | 證明可萃取為 OCaml／Haskell 程式 |

CIC 選了一條更險的路：邏輯與計算合一，
代價是初學者要同時學會證明與依賴型別。但回報是
「可執行的數學」：證完 $sort$ 正確，連可跑的 $sort$ 都到手了。

## 結案報告

CoC 1988、歸納擴充 1990 年代初，CIC 定型，成為 Coq 的理論心臟。
它破了「一演算統治證明、程式、型別」的案件。

遺產有三：

1. **Coq 的地基**：下一案 1989 年 Coq 誕生直接建在此心臟上。
2. **依賴型別正統**：Agda、Idris、Lean 皆沿此路，只是宇宙與公理取捨不同。
3. **HoTT 伏筆**：Voevodsky 的同倫型別論正是對 CIC 等式的再偵查，第五幕將開棺驗屍。

## 證據與工具

- 明星型別： $\Pi x:A. B(x)$ ，特例 $A \to B$ 即 $B$ 不含 $x$ 時。
- 核心判斷： $\Gamma \vdash t : T$ ，脈絡 $\Gamma$ 即偵查筆記本。
- 歸納宣告： $nat$ 與 $list(A)$ 的構造子與 $match$ 消去。

```coq
Inductive nat : Type := O : nat | S : nat -> nat.
Check (fun n:nat => n) : (Π n:nat, nat).
(* ∀ n:nat, P n 即 Π n:nat, P n *)
```

- 實驗：對比 Church 編碼的 $nat$ 與 $Inductive$ 的 $nat$ ，
  分別寫加法並試證 $n + 0 = n$ ，體會原生歸納型別省了多少筆墨。
- 文獻：Coquand 與 Huet 1988 年〈The Calculus of Constructions〉，
  Paulin-Mohring 1993 年歸納族論文。
