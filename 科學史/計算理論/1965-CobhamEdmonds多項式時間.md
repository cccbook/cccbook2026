# 1965 - Cobham 與 Edmonds：多項式時間的誕生

## 案件摘要
1965 年，Cobham 在論文〈The Intrinsic Computational Difficulty of Functions〉中首次主張「多項式時間」是「可行計算」的內在分界；同年 Edmonds 在研究匹配與 TSP 時提出「good algorithm」一詞，明確將其定義為多項式時間演算法。兩人各自獨立地劃下了那條改變計算理論命運的分水嶺。

## 前因 -- 為什麼會有這個案子
1950–60 年代，圖靈機可計算性理論已經成熟：Church–Turing 論題告訴我們什麼「算得出來」。但實務上出現了尷尬的現象——

- 許多問題**可計算**，卻慢到天荒地老（如整數規劃、TSP）；
- 另一些問題卻有「快」的演算法（如排序、線性規劃的單體法雖無理論保證卻很快）。

「可計算」這把刀太鈍，切不出「實務可行」與「實務不可行」。案情的核心問題是：

> **什麼是演算法「快」與「慢」的客觀、機器無關的分界線？**

Edmonds 在 1965 年論文〈Paths, Trees, and Flowers〉中為匹配問題給出第一個多項式時間演算法，並寫下名言：他希望有一個理論能證明某演算法是 "good algorithm"（好演算法）。

## 線索與推理 -- 數學式、程式、理論

### 線索一：P 類的定義（Cobham）
Cobham 主張：一個問題是「易處理的」（tractable），若且唯若它可在多項式時間內被判定。形式化後即複雜度類：

$$\text{P} = \bigcup_{k \geq 1} \text{TIME}(n^k)$$

其中 $\text{TIME}(f(n))$ 表示可被圖靈機在 $O(f(n))$ 步內判定的語言類。這個定義有三個關鍵性質：

1. **機器無關性**（robustness）：任何「合理」計算模型（單帶圖靈機、多帶圖靈機、RAM）上的多項式時間定義都互相封閉——這是圖靈機線性加速模擬定理的推論：多帶圖靈機 $T(n)$ 步可被單帶圖靈機以 $O(T(n)^2)$ 步模擬，多項式仍是多項式。
2. **封閉性**：$\text{P}$ 對加法、乘法（合成）、子程式呼叫封閉——多項式合成多項式仍是多項式：$(n^a)^b = n^{ab}$。
3. **數學上自然**：$n^k$ 在尺度變換下穩定，對應「成長率只差常數倍冪次」的等價類。

### 線索二：「good algorithm」= 多項式時間（Edmonds）
Edmonds 在〈Paths, Trees, and Flowers〉（1965）中寫道（大意）：

> 「關於效率的一個很好的數學定義是：計算步數以輸入規模的多項式為上界。」

他為**最大匹配**問題給出第一個多項式演算法，關鍵在處理「花」（blossom，奇圈）的收縮技巧。此演算法複雜度約 $O(n^4)$，後續被改進，但重點是：**它在 P 中**。

Python 概念示範（Edmonds 求增廣路的貪心框架，略去 blossom 收縮細節）：

```python
def find_augmenting_path_simple(graph, match):
    """二分圖匈牙利式增廣；Edmonds 推廣到一般圖需 blossom 收縮。"""
    for u in graph:
        seen = set()
        def try_k(x):
            for y in graph[x]:
                if y not in seen:
                    seen.add(y)
                    if y not in match or try_k(match[y]):
                        match[y] = x
                        return True
            return False
        try_k(u)
    return match
```

### 線索三：指數 vs 多項式的分水嶺
為什麼分界畫在「多項式」而不是「線性」或「$n \log n$」？Cobham 的論證是：

- $n^{10}$ 雖然實務上可能很慢，但 $2^n$ 在數學上更糟：只要輸入多長一個 bit，時間就翻倍。
- 指數函數違反**尺度不變性**：$f(cn)$ 與 $cf(n)$ 對指數而言差異是本質的（$(2n)^k = 2^k n^k$ 仍多項式，但 $2^{2n} \gg 2 \cdot 2^n$）。

| $n$ | $n^2$ | $2^n$ |
|---|---|---|
| 10 | 100 | 1,024 |
| 30 | 900 | $\approx 10^9$ |
| 100 | 10,000 | $\approx 10^{30}$ |

分水嶺的直覺：**多項式 = 可靠放大規模；指數 = 規模稍增即崩潰。**

### 線索四：為 NP 完備性鋪路
Edmonds 在 1965 年的另一篇論文（關於 TSP 的分支界限法，Maximum matching and a polyhedron with 0,1-vertices）中問道：

> TSP 有沒有 good algorithm？**沒有人知道。**

他清楚地區分了：
- 已有 good algorithm 的問題（匹配、最短路、線性規劃的橢球法時代之前仍存疑）；
- 明顯可指數搜尋、但不知有無多項式演算法的問題（TSP、整數規劃）。

這個「**搜尋容易驗證容易，但求解未知**」的陰影，正是 $\text{P}$ vs $\text{NP}$ 問題的前身，為 1971 年 Cook–Levin 定理與 NP 完備性理論直接鋪路。

## 結案 -- 後果與影響
1. **P 成為「易處理」的標準定義**，此後所有教科書沿用至今。
2. **複雜度分類從描述性變成規範性**：設計演算法的目標被明確為「找到多項式時間演算法」。
3. 直接催生了 **NP 與 NP 完備性**理論（Cook 1971、Karp 1971）。
4. Edmonds 的匹配演算法開啟了**組合優化**中「多面體組合學」的研究路線。
5. Cobham 定理（1965）另證明了：僅用乘法與加法可定義的函數恰是 $\text{FP}$（多項式時間可計算函數），顯示多項式時間在數理邏輯中亦有內刻刻畫。

## 關鍵人物與文獻
- **Alan Cobham**（IBM）：〈The Intrinsic Computational Difficulty of Functions〉, *Logic, Methodology and Philosophy of Science*, 1965.
- **Jack Edmonds**（NBS/滑鐵盧）：〈Paths, Trees, and Flowers〉, *Canadian J. Math.*, 1965（一般圖多項式匹配演算法）。
- **Jack Edmonds**：〈Maximum matching and a polyhedron with 0,1-vertices〉, 1965（分支界限、TSP、good algorithm 術語）。
- 後續：Cook (1971)、Karp (1971)、Garey & Johnson《Computers and Intractability》(1979)。
