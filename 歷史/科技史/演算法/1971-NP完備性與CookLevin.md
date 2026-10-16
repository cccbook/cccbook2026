# 1971-NP完備性與CookLevin

## 案件摘要

1971 年，Stephen Cook 在 STOC 會議上發表〈The Complexity of Theorem-Proving Procedures〉，證明布爾可滿足性問題（SAT）是「NP-complete」——所有 NP 問題都可以多項式時間歸約到它。 同一年，蘇聯的 Leonid Levin 在完全隔離的環境下獨立發現了相同的定理（因蘇聯期刊審稿拖延，1973 年才發表）。 這樁案子的真相是：計算世界存在一類「本質困難」的問題——只要其中任何一個有多項式時間演算法，全部 NP 問題就瞬間可解。 P vs NP 這個世紀懸案就此正式誕生。

## 前因 -- 為什麼會有這個案子

- Jack Edmonds（1965）提出「好演算法 = 多項式時間」的定義，把「有效率」從模糊的實務感受變成精確的數學標準，並在論文中明確追問：「是否存在本質上需要指數時間的問題？」
- 圖靈機的複雜性類別研究在 1960 年代已經成熟：P（確定性多項式時間）與 NP（非確定性多項式時間）的定義已就位，但沒有人知道兩者的關係。
- Cook 的動機是定理證明：他想證明「自動定理證明本質困難」，結果發現 SAT 是整個 NP 世界的「最難縮影」。
- Levin 在 Kolmogorov 複雜性傳統下獨立研究（莫斯科大學，Kolmogorov 的學生），從「搜尋問題的普遍性」角度得出等價結論——兩地隔着鐵幕，卻抵達同一現場。

## 線索與推理 -- 數學式、程式、理論

### 線索一：P 與 NP 的正式定義

P 是確定性圖靈機在多項式時間內可解的語言：

$$
P = \bigcup_{k \geq 1} \text{TIME}(n^k)
$$

NP 是非確定性圖靈機在多項式時間內可解的語言，等價地——多項式時間內可驗證：

$$
L \in NP \iff \exists\, R, k:\ x \in L \iff \exists\, y,\ |y| \leq |x|^k,\ R(x, y) = 1
$$

其中 $y$ 是證書（certificate，如 SAT 的一組賦值），$R$ 是多項式時間的驗證器。顯然 $P \subseteq NP$；懸案是反向包含是否成立。

### 線索二：多項式歸約

Karp 歸約 $A \leq_p B$ 的定義：存在多項式時間可計算的函數 $f$，使得

$$
x \in A \iff f(x) \in B
$$

歸約的威力：「B 若可解，則 A 可解」——把問題的困難度沿歸約方向傳遞。

### 線索三：NP-complete 與 Cook-Levin 定理

NP-complete 的定義（兩個條件）：

1. $L \in NP$
2. $\forall A \in NP:\ A \leq_p L$

Cook-Levin 定理：

$$
SAT \in NP\text{-complete}
$$

證明的核心：對任意 NP 機器 $M$ 與輸入 $x$，構造一個多項式大小的布爾公式 $\phi_{M,x}$，使其可滿足當且僅當 $M$ 在多項式時間內接受 $x$。構造方法是「表格式模擬」：用布爾變數表示每個時間步的圖靈機格局（狀態、磁頭位置、帶內容），用子句強制相鄰時間步符合 $M$ 的轉移規則。模擬 $t(n)$ 步只需 $O(t(n) \log t(n))$ 大小的公式——多項式歸約就此完成。

### 線索四：P vs NP 懸案的正式誕生

由歸約的傳遞性，若 SAT 有多項式時間演算法，則：

$$
SAT \in P \implies \forall A \in NP:\ A \leq_p SAT \in P \implies P = NP
$$

一切 NP 問題——排程、路徑、密碼、藥物設計——瞬間皆可解。這個「一即全部」的結構，是 NP-complete 概念最深刻之處。

### 線索五：Python 實作——驗證 vs 求解的不對稱

以下程式實作暴力 SAT 求解器（枚舉全部賦值），並對照「驗證一組賦值」的成本：

```python
from itertools import product

CNF = [(1, -2), (2, 3), (-1, 3), (-2, -3)]   # 每個 tuple 是一個子句
VARS = sorted({abs(l) for c in CNF for l in c})

def verify(assign, cnf):          # 驗證：O(子句數)，多項式時間
    return all(any(assign[abs(l)] == (l > 0) for l in c) for c in cnf)

def solve_bruteforce(cnf):        # 求解：最壞 O(2^n) 組賦值，指數時間
    vars_ = sorted({abs(l) for c in cnf for l in c})
    for tried, bits in enumerate(product([False, True], repeat=len(vars_))):
        assign = dict(zip(vars_, bits))
        if verify(assign, cnf):
            return assign, tried + 1
    return None, 2 ** len(vars_)

sol, tried = solve_bruteforce(CNF)
print("satisfying assignment:", sol, "| verify(sol) =", verify(sol, CNF))
print(f"n={len(VARS)}: tried {tried} assignments")

print(f"\n{'n':>4} {'tried':>12}  (滿足賦值放在枚舉序列的最後 = 最壞情況)")
for n in [10, 15, 20]:
    cnf = [(i,) for i in range(1, n + 1)]    # 僅全 True 可滿足
    _, t = solve_bruteforce(cnf)
    print(f"{n:>4} {t:>12}")
```

驗證一組賦值只需掃過子句一次（多項式）；求解最壞卻要枚舉 $2^n$ 組賦值（指數）——上表中 n 從 10 到 20，嘗試次數從 $10^3$ 暴漲到 $10^6$。這正是 $P \neq NP$ 懷疑論者的實證直覺，也是 Cook-Levin 定理捕捉的不對稱。

## 結案 -- 後果與影響

- 1972 年 Karp 發表《Reducibility Among Combinatorial Problems》：用 Karp 歸約證明 21 個經典組合問題（頂點覆蓋、漢米頓路徑、子集和等）皆 NP-complete，掀起歸約浪潮。
- P vs NP 成為千禧年七大數學難題之一（Clay 研究所，2000 年設百萬美元獎金），至今未解。
- 密碼學的理論基礎：若 P=NP，則單向函數不存在，RSA 與所有公鑰密碼崩潰；現代密碼學建立在「NP 中存在困難問題」的假設上。
- 計算複雜性理論誕生為學科：NP-complete、多項式層級、隨機化類別、近似困難度等，全部由此案延伸；SAT 求解器（DPLL、CDCL）與近似演算法則是對抗 NP 困難性的兩大工業。
- Cook 獲 1982 年圖靈獎；Levin 後移民美國（波士頓大學），Cook-Levin 定理以兩人並列，成為「獨立發現」的科學史經典案例。

## 關鍵人物與文獻

- Stephen Cook：多倫多大學教授，NP 完備性的發現者，1982 年圖靈獎得主。
- Leonid Levin：蘇聯（Kolmogorov 學生）獨立發現者，後為波士頓大學教授。
- Jack Edmonds：「好演算法 = 多項式時間」定義的提出者（1965）；Richard Karp 則以 1972 年 21 題歸約將 NP-complete 概念發揚光大。
- Alan Turing：圖靈機（1936），一切複雜性類別的計算模型源頭。

主要文獻：

- Cook, S. A. (1971). "The Complexity of Theorem-Proving Procedures". *Proceedings of the 3rd Annual ACM Symposium on Theory of Computing (STOC)*, 151–158.
- Levin, L. A. (1973). "Universal Search Problems". *Problemy Peredachi Informatsii*, 9(3), 115–116.（俄文；英譯見 *SIAM Journal on Computing*, 1986）
- Edmonds, J. (1965). "Paths, Trees, and Flowers". *Canadian Journal of Mathematics*, 17, 449–467.
- Karp, R. M. (1972). "Reducibility Among Combinatorial Problems". In *Complexity of Computer Computations*, Plenum Press, 85–103.
- Garey, M. R., & Johnson, D. S. (1979). *Computers and Intractability: A Guide to the Theory of NP-Completeness*. W. H. Freeman.
