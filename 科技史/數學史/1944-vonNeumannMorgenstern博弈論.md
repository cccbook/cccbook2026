# 1944 - von Neumann–Morgenstern 博弈論

## 案件摘要
1944 年，John von Neumann 與經濟學家 Oskar Morgenstern 出版《博弈論與經濟行為》（Theory of Games and Economic Behavior）：把 1928 年的極小極大定理（見 `1928-vonNeumann極小極大.md`）推廣到**多人博弈、合作博弈**，並建立**期望效用理論**（utility theory）——**理性決策的公理化**。**經濟學的數學革命**——從「文字的敘述」到「公理的模型」——**諾貝爾經濟學獎的半壁江山**（納許、阿羅、謝林、奧曼……）源於此書。

## 前因 -- 為什麼會有這個案子
**經濟學的困境**（1940 年代）：

1. **文字的敘述**：經濟理論是「文字的論述」（馬歇爾、凱因斯的傳統）——**沒有嚴格的數學模型**
2. **理性的定義**：什麼是「理性的經濟人」？——**效用（utility）的概念含糊**
3. **多人博弈**：von Neumann 1928 只解決**兩人零和**——**多人、非零和、合作**沒有理論

**Morgenstern 的背景**：維也納的經濟學家（奧地利學派），1938 年納粹後逃亡美國（普林斯頓）——與 von Neumann（普林斯頓高等研究院）相遇。**1939–1944 的合作**：曼哈頓計畫之餘（von Neumann 同時在造原子彈），寫成 1200 頁的巨著。

**兩人的問題**：**理性的經濟行為**能否公理化——**效用、期望、博弈**的數學基礎？

## 線索與推理 -- 數學式、程式、理論

### 期望效用理論
**von Neumann–Morgenstern 公理**（理性行為的公理化）：

1. **完備性**：任何兩個結果可比較（$A \succ B$ 或 $B \succ A$ 或無差異）
2. **傳遞性**：$A \succ B$ 且 $B \succ C \implies A \succ C$
3. **連續性**：$A \succ B \succ C \implies$ 存在機率 $p$ 使「$pA + (1-p)C$」∼ $B$
4. **獨立性**：$A \succ B \implies pA + (1-p)C \succ pB + (1-p)C$（與無關選項無關）

**定理**：滿足公理 ⟺ 存在**效用函數** $u$，偏好 = 期望效用的比較：

$$A \succ B \iff E[u(A)] > E[u(B)]$$

**公理 ⟺ 效用函數的存在**——**理性的公理化**（與 Kolmogorov 公理化機率 1933 的範式同源，見 `1933-Kolmogorov公理化.md`）。

**風險態度**：效用函數的**凹凸**：

- $u$ 凹：**風險厭惡**（$E[u] < u(E)$——保險的動機）
- $u$ 凸：**風險偏好**（賭徒）
- $u$ 線性：風險中性

### 合作博弈與穩定集
**多人合作博弈**：聯盟（coalition）$S \subseteq N$ 的「特徵函數」$v(S)$（聯盟能保證的總收益）。

**問題**：合作收益怎麼分？——**分配（imputation）**：$\sum_{i \in N} x_i = v(N)$、每人至少得到單獨行動的收益。

**von Neumann–Morgenstern 的穩定集**（stable set）：沒有分配可以「支配」另一分配的集合——**聯盟的談判理論**。

**Shapley 值**（1953，後續）：公平分配的解——**按「邊際貢獻」平均分**：

$$\phi_i = \sum_{S \ni i} \frac{|S|!(|N|-|S|-1)!}{|N|!} (v(S) - v(S \setminus \{i\}))$$

——**成本分攤、投票權力、拍賣設計的標準**。

### 程式碼：期望效用與 Shapley 值

```python
import random, itertools

# 期望效用：風險態度
def utility_concave(x):  return math.sqrt(x)       # 風險厭惡
def utility_linear(x):   return x                  # 風險中性
def utility_convex(x):   return x**2               # 風險偏好

# 賭局：50% 得 100、50% 得 0（期望 50）
random.seed(42)
outcomes = [100, 0]
p = 0.5
E = p * 100 + (1-p) * 0

for name, u in [("凹（風險厭惡）", utility_concave),
                ("線性（風險中性）", utility_linear),
                ("凸（風險偏好）", utility_convex)]:
    E_u = p * u(100) + (1-p) * u(0)
    print(f"{name}：E[u] = {E_u:.2f}，u(E) = {u(E):.2f}，E[u] {'<' if E_u < u(E) else ('>' if E_u > u(E) else '=')} u(E)")

# Shapley 值：公平分配
def shapley_value(N, v):
    """Shapley 值：按邊際貢獻平均分"""
    from math import factorial
    phi = {i: 0.0 for i in N}
    for perm in itertools.permutations(N):
        s, prev = set(), 0
        for i in perm:
            s.add(i)
            marginal = v(frozenset(s)) - prev
            phi[i] += marginal
            prev = v(frozenset(s))
    n = len(N)
    return {i: phi[i] / factorial(n) for i in N}

# 三人博弈：v(空)=0, 單獨=1, 兩人=3, 三人=4
N = {1, 2, 3}
v = lambda S: {0: 0, 1: 1, 2: 3, 3: 4}[len(S)]
phi = shapley_value(N, v)
print(f"\nShapley 值：{phi}（公平分配，總和 = 4）")
print(f"驗證總和：{sum(phi.values()):.1f} = v(N) = 4 ✓")

# 期望效用的蒙地卡羅（保險的動機）
wealth = 1000
loss_prob, loss = 0.01, 500
premium = 6
no_ins = wealth - (loss if random.random() < loss_prob else 0)
with_ins = wealth - premium
print(f"\n保險：不買期望 = {wealth - loss_prob*loss:.1f}，買 = {with_ins}")
print("風險厭惡者偏好確定性（保險）——von Neumann–Morgenstern 的解釋")
```

### 經濟學的數學革命
**諾貝爾獎的譜系**（源於本書）：
- **Nash（1994）**：非合作均衡（見 `1950-Nash均衡.md`）
- **Arrow（1972）**：社會選擇（見 `1962-Arrow不可能性定理.md`）
- **Aumann & Schelling（2005）**：合作博弈與衝突
- **Shapley & Roth（2012）**：匹配市場（Shapley 值的應用）
- **Tirole（2014）**：產業組織的博弈論

**偵探筆記**：von Neumann–Morgenstern 的推理是「**公理化理性**」——不定義「理性是什麼」，而是**公理化偏好**，證明「公理 ⟺ 效用函數存在」。**與 Kolmogorov 公理化機率（1933，見 `1933-Kolmogorov公理化.md`）同一範式**：把「經驗的概念」變成「公理的數學」——**經濟學的數學革命**。

## 結案 -- 後果與影響
- **經濟學的數學革命**：從文字敘述到公理模型——**諾貝爾經濟學獎的半壁江山**源於此書。
- **期望效用理論**：理性的公理化——保險、投資、決策理論的基礎。
- **合作博弈的理論**：穩定集、Shapley 值——**成本分攤、投票權力、拍賣設計**的標準（FCC 頻譜拍賣 1994 用博弈論）。
- **風險態度**：效用函數的凹凸——**保險與投資的數學**（行為經濟學的反叛 1979 Kahneman–Tversky）。
- **von Neumann 的四棲**：數學、物理、經濟、電腦——**20 世紀最廣博的天才**（原子彈、電腦、博弈論）。
- **行為經濟學的反叛**：Kahneman–Tversky 的前景理論 (1979)——**獨立性公理被實驗違反**（諾貝爾 2002）——公理的實證檢驗。

## 關鍵人物與文獻
- **John von Neumann**（1903–1957）：Theory of Games and Economic Behavior (1944)——與 Morgenstern 合著
- **Oskar Morgenstern**（1902–1977）：維也納學派的經濟學家
- **John Nash**（1928–2015）：非合作均衡 (1950)——諾貝爾 1994（見 `1950-Nash均衡.md`）
- **Lloyd Shapley**（1923–2016）：Shapley 值 (1953)——諾貝爾 2012
- **Daniel Kahneman / Amos Tversky**：前景理論 (1979)——行為經濟學的反叛
- 交叉參照：`1928-vonNeumann極小極大.md`、`1950-Nash均衡.md`、`1962-Arrow不可能性定理.md`、`1933-Kolmogorov公理化.md`、`../機率統計/README.md`
