# 2000 - P vs NP 千禧年大獎

## 案件摘要
2000 年 5 月，Clay 數學研究所（CMI）公布七大「千禧年大獎難題」，每題懸賞 100 萬美元，P vs NP 名列其中。這是計算理論史上最大的一樁「懸案」：高效計算與可驗證計算究竟是否等價？至今尚未結案。

## 前因 -- 為什麼會有這個案子
- 1936 年 Turing 以圖靈機釐清「可計算」，但「計算的代價」仍未量化。
- 1965 年 Edmonds 提出「多項式時間 = 好演算法」，Cobham 亦獨立提出同樣見解。
- 1971 年 Cook 在《The complexity of theorem-proving procedures》中提出 NP-完備性，指出 SAT 是「最難的 NP 問題」。
- 1973 年 Levin（蘇聯）獨立發現同樣現象。
- 1972–1974 年 Karp 展示 21 個組合優化問題皆為 NP-完備，案情急遽擴大。
- 到了 2000 年，這樁 30 年懸案已影響密碼學、運籌學、AI，Clay 基金會遂將其「立案懸賞」。

## 線索與推理 -- 數學式、程式、理論

### 1. 問題敘述：$\text{P} \stackrel{?}{=} \text{NP}$

**定義（P）**：多項式時間可解的語言類：

$$\text{P} = \bigcup_{k \geq 1} \text{TIME}(n^k)$$

**定義（NP）**：多項式時間可**驗證**的語言類：

$$\text{NP} = \bigcup_{k \geq 1} \text{NTIME}(n^k)$$

即語言 $L \in \text{NP}$ 若存在多項式時間驗證器 $V$ 使得：

$$x \in L \iff \exists y,\ |y| \leq |x|^k,\ V(x, y) = 1$$

**問題核心**：

$$\text{P} \stackrel{?}{=} \text{NP}$$

「找到解」（求解）是否不難於「檢查解」（驗證）？例：SAT 是否存在滿足指派是 NP 的原型；而檢查一個指派只需線性時間。

### 2. 多數學者相信 $\text{P} \neq \text{NP}$ 的理由

**Sipser 民調**：2002 年 William Gasarch 對理論計算機科學家做了著名調查，2002 年約 61 位受訪者中 61%（Sipser 等多數學者）相信 $\text{P} \neq \text{NP}$；2019 年重做時比例更升至約 88%。30 年來無人找到任何 NP-完備問題的多項式演算法，這是「計算上的經驗證據」。

**觀點補充**：Sipser 主張，若 P = NP，那麼「數學創造力」可被機械化——找證明與驗證證明一樣容易，這與數學家數十年經驗相悖。

### 3. 三大障礙的數學內容

即使動用最強的證明技術，也撞上三堵牆：

**(a) 相對化障礙（Relativization, Baker–Gill–Solovay 1975）**
存在oracle $A$ 使 $\text{P}^A = \text{NP}^A$，也存在 oracle $B$ 使 $\text{P}^B \neq \text{NP}^B$。因此任何「僅模擬計算、對 oracle 不敏感」的證明技術（相對化技術）都無法證明 P ≠ NP。

**(b) 自然證明障礙（Natural Proofs, Razborov–Rudich 1994）**
定義：對電路類 $\mathcal{C}$ 的下界證明若滿足「建設性」與「廣泛性」（natural），則可反過來破解偽隨機數產生器。在標準密碼學假設（單向函數存在）下，自然證明無法區分 $\text{P/poly}$ 中的真假隨機函數。Razborov 本人在 1985 年對單調電路的 clique 下界證明，正是自然證明的犧牲品。

**(c) 代數化障礙（Algebrization, Aaronson–Wigderson 2008）**
將相對化推廣到「代數擴充 oracle」：若證明技術在代數化 oracle 下依然成立，則無法證明 P ≠ NP。IP = PSPACE 的證明（Shamir 1992）是非代數化的，這提示未來證明需要「代數式互動」的技巧。

### 4. 若 P = NP 的世界會怎樣

- **密碼學崩潰**：RSA、Diffie–Hellman、橢圓曲線皆依賴「求解難、驗證易」的不對稱性。若 P = NP，因數分解與離散對數將有多項式演算法：

  $$\text{FACTORING} \in \text{NP} \implies \text{FACTORING} \in \text{P}$$

- **優化問題全解**：TSP、排程、蛋白質摺疊、線性規劃整數版皆可高效求解。
- **數學自動化**：找長度為 $n^k$ 的證明變成多項式時間可解（因 BOOLE FORMULA 證明是 NP 完備的），數學家失業（或升級）。
- **機器學習**：許多學習問題（如尋找最小電路）落入 P。

### 5. 程式碼範例：SAT 的「驗證易、求解難」

```python
import itertools

def verify(clauses, assignment):
    """驗證器：O(n) 時間檢查指派是否滿足"""
    return all(any((l > 0) == assignment[abs(l)] for l in c) for c in clauses)

def solve_brute(clauses, n):
    """求解器：暴力枚舉 2^n，這就是『難』的來源"""
    for bits in itertools.product([False, True], repeat=n):
        a = {i + 1: bits[i] for i in range(n)}
        if verify(clauses, a):
            return a
    return None

clauses = [[1, -2], [-1, 3], [2, 3]]
print(solve_brute(clauses, 3))   # 求解：指數級
print(verify(clauses, {1: True, 2: True, 3: True}))  # 驗證：線性級
```

## 結案 -- 後果與影響
- **未結案**：至今無人領走 100 萬美元，案件仍在偵辦。
- **影響 1**：確立「複雜度類」為 21 世紀理論電腦科學的核心語言，衍生 $\text{P} \subseteq \text{NP} \subseteq \text{PSPACE}$ 等階層研究。
- **影響 2**：刺激密碼學從「經驗安全」走向「基於複雜度假設的安全性」（one-way function、P ≠ NP 假設）。
- **影響 3**：帶動近似演算法、參數化複雜度（FPT）、平均情況複雜度等「繞道」研究——既然最壞情況可能無解，就在放寬條件下求解。
- **影響 4**：催生新的下界技術路線——幾何複雜度理論（GCT）、代數複雜度，試圖突破三大障礙。
- **影響 5**：2019 年後與機器學習交叉，「神經網路能否學到 NP-難結構」成為新問題。

## 關鍵人物與文獻
- **Stephen Cook**（1971）：提出 NP-完備性，1997 年圖靈獎。
- **Leonid Levin**（1973）：蘇聯獨立發現。
- **Richard Karp**（1972）：21 個 NP-完備問題，1985 年圖靈獎。
- **Baker, Gill, Solovay**（1975）：相對化障礙。
- **Razborov, Rudich**（1994）：自然證明障礙。
- **Aaronson, Wigderson**（2008）：代數化障礙。
- **Clay 數學研究所**（2000）：七題懸賞。
- 文獻：S. Cook, "The P versus NP Problem" (CMI official problem description, 2000)；Gasarch, "The P=?NP Poll" (SIGACT News, 2002, 2019)。
