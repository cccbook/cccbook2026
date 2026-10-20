# 附錄 A：符號與術語對照表

> 離散數學橫跨邏輯、集合、組合、圖論、代數與計算理論，各領域符號繁多且偶有衝突。本附錄統一本書用法並提供中英對照。

## A.1 邏輯符號

| 符號 | 讀法 | 英文 |
|---|---|---|
| $\neg P$ | 非 | negation |
| $P \land Q$ | 且 | conjunction |
| $P \lor Q$ | 或 | disjunction |
| $P \to Q$ | 蘊含 | implication |
| $P \leftrightarrow Q$ | 若且唯若 | biconditional |
| $\forall$ | 對所有 | universal quantifier |
| $\exists$ | 存在 | existential quantifier |
| $\vdash$ | 可推導 | syntactic consequence |
| $\vDash$ | 語意蘊含 | semantic consequence |

## A.2 集合與關係

| 符號 | 意義 | 英文 |
|---|---|---|
| $x \in A$ | 屬於 | membership |
| $\emptyset$ | 空集合 | empty set |
| $A \cup B,\ A \cap B,\ A^c$ | 聯集、交集、補集 | union, intersection, complement |
| $A \times B$ | 卡氏積 | Cartesian product |
| $\mathcal P(A)$ | 冪集 | power set |
| $R^{-1}$ | 逆關係 | inverse relation |
| $[a]$ | 等價類 | equivalence class |
| $\cong$ | 同構 | isomorphism |
| $|A|$ | 基數 | cardinality |

## A.3 計數與組合

| 符號 | 意義 | 英文 |
|---|---|---|
| $P(n,k)$ 或 ${}_nP_k$ | $n$ 取 $k$ 排列 | permutation |
| $\binom{n}{k}$ | 二項式係數 | binomial coefficient |
| $\binom{n}{0}+\cdots+\binom{n}{n}=2^n$ | 冪集計數 | sum of binomials |
| $\sum_{k=0}^n \binom{n}{k}^2 = \binom{2n}{n}$ | Vandermonde 恆等式 | Vandermonde's identity |

## A.4 圖論

| 符號 | 意義 | 英文 |
|---|---|---|
| $G=(V,E)$ | 圖 | graph |
| $d(v)$ | 節點度數 | degree |
| $\sum_v d(v) = 2|E|$ | 握手定理 | handshaking lemma |
| $A_G,\ L_G$ | 鄰接矩陣、Laplacian | adjacency / Laplacian matrix |
| $\chi(G)$ | 著色數 | chromatic number |
| $\kappa(G)$ | 連通度 | vertex connectivity |

## A.5 數論與代數

| 符號 | 意義 | 英文 |
|---|---|---|
| $a \equiv b \pmod n$ | 同餘 | congruence |
| $a \mid b$ | 整除 | divides |
| $\gcd(a,b)$ | 最大公因數 | greatest common divisor |
| $\varphi(n)$ | Euler 函數 | Euler's totient |
| $Z_n$ 或 $\mathbb Z/n\mathbb Z$ | 模 $n$ 餘數環 | integers mod n |
| $\langle g \rangle$ | 產生子群 | cyclic subgroup |

## A.6 計算理論

| 符號 | 意義 | 英文 |
|---|---|---|
| $\Sigma$ | 字母集 | alphabet |
| $\Sigma^*$ | 所有字串（含空字串 $\epsilon$ ） | Kleene star |
| $L(M)$ | 機器 $M$ 接受的語言 | language accepted |
| $O(f),\ \Theta(f)$ | 複雜度上界、緊界 | big-O, big-Theta |
| $\mathcal P,\ \mathcal{NP}$ | 多項式時間類 | complexity classes |

## 小結

同一符號在不同章節可能意義不同（如 $|\cdot|$ 可指基數或絕對值），閱讀時需靠上下文判斷——這正是「符號即抽象」的雙面性，也是本書鼓勵讀者練習「翻譯回自然語言」的原因。
