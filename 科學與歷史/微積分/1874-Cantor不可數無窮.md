# 1874 — Cantor 不可數無窮

## 案件摘要
1874 年，Cantor 在《Crelle's Journal》發表〈Über eine Eigenschaft des Inbegriffes aller reellen algebraischen Zahlen〉，證明實數（甚至只是代數數）「多到」無法與自然數一一對應——無窮不止一種，而是有層級的。1891 年他又用更優雅的「對角線法」重擊此案。這樁案件把「無窮」從哲學玄談變成可證明、可運算的數學對象，卻也引爆了二十世紀的第三次數學危機。

## 前因 -- 為什麼會有這個案子
- **Fourier 級數的唯一性問題**：1850 年代，年輕的 Cantor 追隨 Weierstrass 研究三角級數。一個函數的 Fourier 展開若唯一，那麼「在哪些點上可以改動函數值而不破壞唯一性」？Cantor 證明：即使在一個無窮（但足夠「稀疏」）的點集上改動，唯一性仍成立。為了給「稀疏的無窮點集」分類，他被迫發明集合論——案件的原點。
- **Dedekind 切割**：1872 年 Dedekind 用有理數的「切割」嚴格定義實數，使實數成為一個完備的連續體。但一個尖銳的問題浮上檯面：實數到底比自然數「多」多少？有理數明明到處稠密，卻可以一個個數完（與 $\mathbb{N}$ 對應），實數呢？
- 當時的主流觀點（如 Kronecker）認為：數學只該研究「可以構造出來」的對象，無窮整體是不合法的。Cantor 等於要證明一件「不該存在」的東西。

## 線索與推理 -- 數學式、程式、理論

### 線索一：一一對應是「數量」的量尺
Cantor 的關鍵洞見：兩個集合「一樣大」不必去數，只需存在雙射（一對一且映成的函數）。如此一來：

$$|\mathbb{N}| = |\mathbb{Z}| = |\mathbb{Q}| = \aleph_0$$

有理數看似稠密，卻可依對角線順序列出 $\frac{1}{1}, \frac{1}{2}, \frac{2}{1}, \frac{1}{3}, \frac{2}{2}, \frac{3}{1}, \dots$ 全部數完。到處稠密 ≠ 不可數——第一個直覺被推翻。

### 線索二：1874 年的原始證明（區間套法）
Cantor 1874 年的證明並非對角線法，而是區間套：假設實數可列成序列 $x_1, x_2, x_3, \dots$，任取閉區間 $[a_1, b_1]$，在其中找兩個不在序列開頭的點造 $[a_2, b_2] \subset [a_1, b_1]$ 且 $x_1 \notin [a_2, b_2]$，依此類推使 $x_n \notin [a_{n+1}, b_{n+1}]$。區間套定理保證存在一點 $x$ 屬於所有區間，但這個 $x$ 不等於任何 $x_n$——序列漏掉了實數。實數不可數。

### 線索三：1891 年的對角線法
1891 年 Cantor 在德國數學會上提出更簡潔的殺手鐧。把每個實數寫成無窮小數，假設全部列出：

$$
\begin{aligned}
x_1 &= 0.\,d_{11}\,d_{12}\,d_{13}\,\cdots\\
x_2 &= 0.\,d_{21}\,d_{22}\,d_{23}\,\cdots\\
x_3 &= 0.\,d_{31}\,d_{32}\,d_{33}\,\cdots
\end{aligned}
$$

構造 $x^* = 0.\,d_1^* d_2^* d_3^* \cdots$，其中 $d_n^* \neq d_{nn}$（例如取 $d_n^* = 1$ 若 $d_{nn} \neq 1$，否則取 2，並避開 0 與 9 以躲開 $0.5000\cdots = 0.4999\cdots$ 的雙重表示陷阱）。$x^*$ 與列表中第 $n$ 個數在第 $n$ 位必不相同，故 $x^*$ 不在表中。任何列表都漏——不可數，證畢。

更一般的表述是冪集定理：對任何集合 $S$，不存在 $S \to \mathcal{P}(S)$ 的滿射，故

$$\aleph_0 < 2^{\aleph_0} < 2^{2^{\aleph_0}} < \cdots$$

無窮是一整座塔，不是一個點。

### 線索四：連續統假設——懸而未決的餘案
在 $\aleph_0$ 與 $2^{\aleph_0}$ 之間有沒有中間層級？Cantor 猜沒有，即連續統假設（CH）：

$$2^{\aleph_0} = \aleph_1$$

Cantor 窮盡餘生未能證明，抑鬱而終。1940 年 Gödel 證明 CH 與 ZFC 不矛盾（可構造宇宙 $L$），1963 年 Cohen 用力迫法證明 $\neg$CH 也與 ZFC 不矛盾——CH 獨立於 ZFC，永遠無法在標準公理內結案。

### 程式碼範例：對角線法在二進位小數上的實作
```python
import random

def diagonal_hit(N=8):
    # 假想「實數已被列出」：隨機生成 N 個二進位小數當作列表
    table = [[random.randint(0, 1) for _ in range(N)] for _ in range(N)]
    # 對角線構造：第 n 位刻意與第 n 個數的第 n 位相反
    rebel = [1 - table[n][n] for n in range(N)]
    # 檢查 rebel 與每一列都不同
    for i, row in enumerate(table):
        assert rebel != row, f"第 {i} 列居然相同！"
    print("列表 x_1..x_%d :" % N)
    for i, row in enumerate(table):
        print(f"  x_{i+1} = 0.{''.join(map(str, row))}...")
    print(f"叛逆者 x* = 0.{''.join(map(str, rebel))}... -> 不在任何列中")

diagonal_hit()
```

不論列表多長、怎麼生成，對角線構造出的 $x^*$ 必然漏網——程式就是對角線法的「實驗重演」：這不是機率碰巧，而是邏輯必然。

## 結案 -- 後果與影響
- **集合論成為數學基礎**：今日所有數學結構（數、函數、空間、機率）都以集合定義，ZFC 公理系統是公認的地基。
- **無窮的分層級**：$\aleph_0 < 2^{\aleph_0}$ 開啟了基數理論與序數理論，超窮算術成為一門學問。
- **第三次數學危機**：1902 年 Russell 悖論（「包含所有不包含自己的集合的集合」）直擊樸素集合論，迫使 Hilbert、Zermelo 等人發展公理化與證明論，最終引出 1931 年 Gödel 不完備定理。
- Kronecker 稱 Cantor 為「腐蝕青年的叛徒」，Hilbert 卻力挺：「沒有人能把我們從 Cantor 建造的天堂中驅逐出去。」

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Georg Cantor | 集合論創始人，證明不可數與冪集定理 |
| Richard Dedekind | 切割定義實數，Cantor 終生摯友與通信者 |
| Leopold Kronecker | 構造主義反對者，「叛徒」指控者 |
| David Hilbert | 公理化運動領袖，Cantor 天堂的守護者 |
| Kurt Gödel / Paul Cohen | 證明連續統假設獨立於 ZFC |

- G. Cantor, *Über eine Eigenschaft des Inbegriffes aller reellen algebraischen Zahlen*, J. reine angew. Math. **77** (1874)。
- G. Cantor, *Über eine elementare Frage der Mannigfaltigkeitslehre*, Jahresbericht der DMV **1** (1891)：對角線法。
- G. Cantor, *Beiträge zur Begründung der transfiniten Mengenlehre* (1895–1897)。
