# 1957-Bellman動態規劃

## 案件摘要

1957 年，理查德·貝爾曼（Richard Bellman）在普林斯頓大學出版社出版《Dynamic Programming》，為「多階段決策問題」建立了一套完整的理論與方法。案件的偵查對象是一類線性規劃無法處理的難題：決策是一連串相互牽動的選擇，眼前的最優選擇未必導致全域最優。貝爾曼的破案武器是「最佳化原理」——最優策略的任何子策略也必是最優的——這條原理把大問題拆成無數互相重疊的小問題，再用一張表格把每個小問題的答案存起來，徹底消滅重複計算。

## 前因 -- 為什麼會有這個案子

- RAND 公司（RAND Corporation）在 1950 年代投入控制論與最優控制研究，面臨的核心問題是多階段決策：飛彈導引、庫存管理、資源分配都要求在時間軸上一連串做出最優選擇。
- Dantzig 的線性規劃（1947）只能處理單階段的線性約束問題，對多階段、非線性、隨機性的決策問題無能為力。
- 貝爾曼在 RAND 有名的「名稱戰術」：他自述刻意選用「dynamic」這個詞，因為時任國防部長嫌「數學」太抽象，而「dynamic」聽起來充滿活力又「有點意思」，經費因此撥得下來——這個名字就這樣定案。
- 1953 年的 RAND 報告已是先聲，其中貝爾曼方程與最佳化原理的雛形已經出現，1957 年的專書則是正式結案陳詞。

## 線索與推理 -- 數學式、程式、理論

### 線索一：最佳化原理與貝爾曼方程

貝爾曼提出的最佳化原理（principle of optimality）：

> 最優策略具有如下性質：無論初始狀態與初始決策為何，其後的決策對於第一個決策所造成的狀態而言，必定也是一個最優策略。

這條原理把多階段問題化為遞迴的價值函數。以確定性離散系統為例，貝爾曼方程為：

$$
V(s) = \min_{u} \left\{ c(s, u) + V(s') \right\}, \quad s' = f(s, u)
$$

其中 $V(s)$ 是從狀態 $s$ 出發的最優總成本，$c(s,u)$ 是本步成本，$s'$ 是採取決策 $u$ 後轉移到的新狀態。問題從終端條件 $V(T)$ 倒推或自底向上順推求解。

### 線索二：重疊子問題與最佳子結構

DP 適用的兩大特徵：

- 最佳子結構（optimal substructure）：大問題的最優解由子問題的最優解組成——這正是最佳化原理的代數表現。
- 重疊子問題（overlapping subproblems）：遞迴展開時，同一個子問題會被反覆碰到。

對付重疊子問題有兩招：記憶化（memoization，遞迴時把算過的答案存進表格）與自底向上填表（bottom-up tabulation，按依賴順序直接迴圈填表）。兩者的哲學都是「用空間換時間」。

### 線索三：Fibonacci 的指數 vs 線性對照

Fibonacci 遞迴 $F(n) = F(n-1) + F(n-2)$ 的呼叫樹呈指數膨脹，呼叫次數 $T(n) = T(n-1) + T(n-2) + 1 = \Theta(\varphi^n)$（$\varphi \approx 1.618$）；記憶化後每個 $F(k)$ 只算一次：

$$
T(n) = O(n)
$$

### 線索四：最長共同子序列（LCS）

兩序列 $X[1..m]$ 與 $Y[1..n]$ 的最長共同子序列滿足遞迴式：

$$
L[i][j] =
\begin{cases}
L[i-1][j-1] + 1, & X[i] = Y[j] \\
\max(L[i-1][j],\, L[i][j-1]), & X[i] \neq Y[j]
\end{cases}
$$

以 $O(mn)$ 時間與空間填表求解——編輯距離（Levenshtein distance）與之同構。

### 破案時刻：可執行驗證

```python
calls_naive = 0
calls_memo = 0

def fib_naive(n):
    global calls_naive
    calls_naive += 1
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)

memo = {}
def fib_memo(n):
    global calls_memo
    calls_memo += 1
    if n <= 1:
        return n
    if n not in memo:
        memo[n] = fib_memo(n - 1) + fib_memo(n - 2)
    return memo[n]

n = 20
assert fib_naive(n) == fib_memo(n) == 6765
print(f"F({n}) = 6765")
print(f"naive 呼叫次數 = {calls_naive}")
print(f"memo  呼叫次數 = {calls_memo}")

def lcs(X, Y):
    m, n = len(X), len(Y)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]

print("LCS('ABCBDAB', 'BDCABA') =", lcs("ABCBDAB", "BDCABA"))
```

執行結果：naive 的 Fibonacci 在 n=20 時已呼叫上萬次（約 $2F(21)-1 = 21891$ 次），memo 版僅呼叫數十次；LCS 正確回傳 4，實證了「用空間換時間」的威力。

## 結案 -- 後果與影響

- 動態規劃成為演算法設計五大範式（分治、貪婪、DP、隨機化、近似）之一，編輯距離、背包問題、矩陣鏈乘、最短路徑（Floyd-Warshall）都有標準 DP 解法。
- 貝爾曼方程成為強化學習的理論基石：價值迭代、策略迭代直接源自 1957 年的框架，Q-learning（Watkins, 1989）與日後的深度強化學習都是貝爾曼方程的近代後裔。
- 最優控制理論（如線性二次調節器 LQR、Hamilton-Jacobi-Bellman 方程）自此有了離散與連續兩條主線。
- 「用空間換時間」成為演算法設計的核心哲學，記憶化成為函數式程式設計與競賽程式的日常工具。
- 貝爾曼本人的「名稱戰術」軼事，也成為科學命名政治學的經典案例。

## 關鍵人物與文獻

- Richard Bellman, *Dynamic Programming*, Princeton University Press, 1957.
- Richard Bellman, "On the Theory of Dynamic Programming", *Proceedings of the National Academy of Sciences*, 38(8), 1952, pp. 716–719.
- Richard Bellman, RAND Report P-480: *The Theory of Dynamic Programming*, RAND Corporation, 1953.
- Richard Bellman, *Eye of the Hurricane: An Autobiography*, World Scientific, 1984（自述「dynamic」名稱戰術）。
- Stuart Dreyfus, "Richard Bellman on the Birth of Dynamic Programming", *Operations Research*, 50(1), 2002, pp. 48–51.
- Christopher J. C. H. Watkins, Peter Dayan, "Q-learning", *Machine Learning*, 8, 1992, pp. 279–292.
