# 1937 - Turing 等價性證明

## 案件摘要

1936–37 年，年輕的 Alan Turing 在普林斯頓師從 Church，發表論文
《Computability and λ-definability》，證明 λ 可定義函數與 Turing 機器
可計算函數**完全等價**。兩條看似毫無關聯的偵查路線，指向同一個凶手：
「可計算」這個概念終於被鎖定。

## 前因 -- 為什麼會有這個案子

- 1931 年 Gödel 的不完備定理摧毀了 Hilbert 的「完備公理化數學」夢想，
  但留下懸案：什麼樣的函數是「可計算的」？
- Gödel 用「一般遞迴函數」刻劃，但這個定義太依賴形式系統本身，有循環
  論證之嫌。
- Church（1933–36）主張 λ 可定義函數 = 可計算函數（Church 論題）。
- Turing（1936）獨立提出「機器計算」模型：一條紙帶、一個讀寫頭、有限
  狀態——直覺上更接近「人拿筆在紙上計算」的物理過程。
- 懸案：這兩個定義圈定的範圍是否相同？若是，就有令人信服的獨立證據。

## 線索與推理 -- 數學式、程式、理論

### Turing 機器的定義

一個 Turing 機器是七元組 $M = (Q, \Gamma, \Sigma, \delta, q_0, B, F)$：

- $Q$：有限狀態集合；$q_0 \in Q$ 起始狀態；$F \subseteq Q$ 接受狀態
- $\Gamma$：紙帶符號集（含空白符 $B$）；$\Sigma \subseteq \Gamma \setminus \{B\}$ 輸入符號
- 轉移函數 $\delta : Q \times \Gamma \to Q \times \Gamma \times \{L, R\}$

組態（瞬時描述）記為 $\alpha q \beta$，其中 $\alpha\beta$ 是紙帶內容，
$q$ 是當前狀態，讀寫頭停在 $q$ 右側第一格。計算即組態序列：

$$
C_0 \vdash_M C_1 \vdash_M C_2 \vdash_M \cdots
$$

機器 $M$ 計算函數 $f$：起始紙帶為 $n$ 的一進制編碼（如 $1^{n+1}$），
若最終停機且紙帶為 $f(n)$ 的編碼，則 $f(n)$ 有定義。

### 方向一：λ → TM（Church 的模擬）

Turing 在 1937 年論文中證明：**每個 λ 可定義函數都可由 Turing 機器計算**。

策略：對 λ 項 $M$ 給出機器編碼，機器在紙帶上維護 $(\beta, x, \delta)$ 三元組
（環境、變數、待約簡項的編碼），反覆執行：

1. 找到紅色（可約簡）子項 $(\lambda x. N)\ P$ —— 即 β-redex
2. 執行替換 $N[x := P]$ —— 即 β-約簡
3. 直到無 redex 為止（正規形式）

Church–Rosser 定理保證此過程的終點唯一，模擬是良定的。

### 方向二：TM → λ（Turing 的模擬）

Turing 在 1936 年論文附錄中證明：**每個 Turing 可計算函數都是 λ 可定義的**。

策略：把 TM 的每個「機機組態」編碼為 λ 頁上的項，用 λ 演算模擬單步轉移。
組態 $\alpha q \beta$ 編碼為

$$
\ulcorner \alpha q \beta \urcorner = \lambda f.\ \cdots
$$

利用 Church 數字與前驅函數（predecessor）、條件式等 λ 可定義工具，
可以構造「單步模擬器」$\mathrm{Step}$，使得

$$
\mathrm{Step}\ \ulcorner C \urcorner = \ulcorner C' \urcorner \quad \text{其中 } C \vdash_M C'
$$

再以不動點組合子 $Y = \lambda g.(\lambda x. g\ (x\ x))(\lambda x. g\ (x\ x))$
迭代 $\mathrm{Step}$ 直到停機組態出現。

λ 演算與 Turing 機器的對照表：

| λ 演算 | Turing 機器 |
|---|---|
| λ 項 $M$ | 機器編碼 $\ulcorner M \urcorner$ |
| β-redex $(\lambda x.N)P$ | 狀態轉移 $\delta(q, a)$ |
| β-約簡 $N[x := P]$ | 紙帶讀寫與改寫 |
| 正規形式 | 停機組態 |
| 環境 / 綁定 | 紙帶上的暫存區 |
| 不動點 $Y$ 組合子 | 無限迴圈 / 迭代控制 |
| Church 數字 $\lambda f.\lambda x.f^n x$ | 一進制 $1^{n+1}$ |

### Church–Turing 命題的確立

兩方向合流，得到定理：

> **定理（Church–Turing）**：函數 $f : \mathbb{N} \to \mathbb{N}$ 是 λ 可定義的
> $\iff$ $f$ 是 Turing 機器可計算的。

這使「有效可計算」從模糊直覺升級為**有雙重獨立證據的數學概念**。
Kleene 的遞迴函數、Post 的 Post 機器後來也證明等價——四路合流，
「可計算性」的定義再也無可動搖。

## 結案 -- 後果與影響

- Hilbert 的 **Entscheidungsproblem（判定問題）** 被證明無解：不存在演算法
  判定任意一階邏輯語句是否可證。Church 與 Turing 各自獨立發表此結果。
- 「通用機器」$U$（模擬任意 TM）的觀念誕生——這是現代電腦的理論藍圖。
- 可計算性理論成為數理邏輯與理論計算機科的基石。
- 1937 年 Turing 赴普林斯頓隨 Church 讀博士（1938 年獲博士學位），
  兩位「凶手獵人」正式會師。

## 關鍵人物與文獻

- **Alan Turing**（1912–1954）：Turing 機器與等價性證明的作者。
- **Alonzo Church**（1903–1995）：λ 演算創始人，Turing 的博士導師。
- Turing, A. M. (1936). *On Computable Numbers, with an Application to the
  Entscheidungsproblem*. Proc. London Math. Soc.
- Turing, A. M. (1937). *Computability and λ-definability*. J. Symbolic Logic 2(4).
- Church, A. (1936). *An Unsolvable Problem of Elementary Number Theory*. Am. J. Math.
