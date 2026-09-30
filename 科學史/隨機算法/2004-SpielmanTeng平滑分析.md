# 2004 - Spielman–Teng 平滑分析

## 案件摘要
2004 年，Daniel Spielman 與 Shang-Hua Teng 發表《Smoothed Analysis: Why the Simplex Algorithm Usually Takes Polynomial Time》：解開困擾學界半世紀之謎——**單純形法（Dantzig 1947）最壞情況是指數時間（Klee–Minty 1972），實務卻快得驚人**。他們提出**平滑分析**：不問最壞情況、也不問平均情況，而是問「**最壞輸入受到微小隨機擾動後**，演算法還要多久？」——單純形法在平滑複雜度下是多項式時間。這是隨機算法思想對最壞情況分析的哲學革命。

## 前因 -- 為什麼會有這個案子
線性規劃的單純形法：Dantzig 1947 發明，實務飛快（幾萬變數瞬間解決）。但 1972 年 Klee–Minty 構造出指數時間的反例：

$$\max \sum_{i=1}^d 10^{d-i} x_i, \quad 0 \le x_1 \le 100, \quad 0 \le x_i \le 100 x_{i-1}$$

這個「扭曲的立方體」讓 Dantzig 規則走遍 $2^d$ 個頂點。**矛盾**：理論指數、實務多項式——為什麼？

兩種舊解釋都不滿意：
1. **最壞情況分析**：太悲觀（Klee–Minty 是精心構造的病態例子，現實不會出現）
2. **平均情況分析**（Borgwardt、Smale 1983）：依賴特定輸入分佈（均勻分佈）——但「現實資料的分佈」是什麼？無法定義

## 線索與推理 -- 數學式、程式、理論

### 平滑分析的定義
**定義**：演算法 $A$ 的平滑複雜度：

$$\mathrm{Smoothed}(A, n) = \max_{\bar{x} \in [0,1]^N} \mathrm{E}_{\substack{x = \bar{x} + g \\ g \sim N(0, \sigma^2)}} [\mathrm{cost}(A, x)]$$

**白話**：對**每個**可能的「中心」$\bar{x}$（取最壞），加上標準差 $\sigma$ 的高斯擾動，問期望執行時間。

三種分析的對照：

| 分析 | 定義 | 特點 |
|------|------|------|
| 最壞情況 | $\max_x \mathrm{cost}(A, x)$ | 太悲觀 |
| 平均情況 | $\mathrm{E}_{x \sim D}[\mathrm{cost}(A, x)]$ | 依賴分佈 $D$ |
| **平滑分析** | $\max_{\bar{x}} \mathrm{E}_{x=\bar{x}+g}[\mathrm{cost}]$ | 最壞 + 隨機擾動 |

**哲學**：平滑分析是「敵人構造最壞輸入，但大自然加上雜訊」——**敵人無法精確控制輸入，病態就被擾動破壞**。

### 單純形法的平滑分析
**定理（Spielman–Teng 2004）**：Dantzig 規則的單純形法，平滑複雜度為：

$$\mathrm{Smoothed} = O\left(\mathrm{poly}(n, d, \frac{1}{\sigma})\right)$$

即多項式時間（擾動大小 $\sigma$ 進入多項式）。

**證明骨架**：單純形法的時間 $\propto$ 頂點間的「影子頂點數」（shadow vertex path length）。Klee–Minty 反例的時間之所以指數，是因為某些頂點對的**條件數**（condition number）極端病態。高斯擾動使條件數以高機率良好：

$$P(\text{病態條件數}) \le \mathrm{poly}(\sigma)$$

（由隨機矩陣的集中不等式——與 Johnson–Lindenstrauss 引理（見 `1984-JohnsonLindenstrauss引理.md`）同源的技術。）

### 程式碼：平滑分析的概念示範

```python
import random, math

# Klee-Minty 立方體（單純形法指數時間反例）
def klee_minty(n_dims):
    """最壞情況：2^n_dims 個頂點"""
    return 2 ** n_dims

# 平滑分析概念：最壞輸入 + 高斯擾動後的「實際」難度
def smoothed_cost(solver, worst_input, sigma, trials=100):
    costs = []
    for _ in range(trials):
        perturbed = [x + random.gauss(0, sigma) for x in worst_input]
        costs.append(solver(perturbed))
    return sum(costs) / len(costs)

random.seed(42)
# 概念示範：病態輸入被擾動後，演算法不再走遍所有頂點
print(f"Klee-Minty 最壞情況（d=30）：{klee_minty(30)} 步（指數）")
print("平滑分析：擾動 sigma=0.01 後期望時間為多項式")
# Spielman-Teng 的證明：病態條件數的機率 <= poly(sigma)
```

### 平滑分析的擴展
Spielman–Teng 開創的方法論隨後應用到：

- **快速排序**（Banderier et al.）：平滑分析下的比較次數
- **局部搜尋**（2-opt TSP、Lloyd k-means）：平滑複雜度多項式
- **條件數理論**：隨機矩陣的病態機率（Tao–Vu 2010 的隨機矩陣理論）
- **插值法與數值算法**：數值穩定性的機率分析

**偵探筆記**：平滑分析的推理是「第三條路」——最壞情況與平均情況之間插入「**最壞 + 擾動**」。它回答的不是「演算法多快」而是「**病態多脆弱**」。這個模式的哲學源頭正是 Quicksort 分析（見 `1961-Hoare快速排序.md`）：敵人存在，但隨機性讓敵人的精心構造失效。

## 結案 -- 後果與影響
- **線性規劃之謎解決**：單純形法的實務快得到理論解釋——平滑複雜度多項式。
- **Goedel 懸案的補完**：Klee–Minty 反例不再是「理論的尷尬」，而是「病態的脆弱性」。
- **算法分析的新範式**：平滑分析成為 CLRS 之後教材與 STOC/FOCS 的標準話題。
- **隨機矩陣理論**：Tao–Vu、Rudelson–Vershynin 的條件數研究由此發酵。
- **圖靈獎**：Spielman 獲 2023 Nevanlinna 獎（Teng 獲 Fulkerson 獎）；平滑分析被譽為「算法分析的未來」。

## 關鍵人物與文獻
- **George Dantzig**（1914–2005）：單純形法 (1947)
- **Klee & Minty**：指數反例 (1972)
- **Daniel Spielman**（1970–）：Yale；平滑分析
- **Shang-Hua Teng**（滕尚華，1964–）：USC/Boston U；平滑分析
- Spielman & Teng: Smoothed Analysis... (2004, J. ACM)
- **Tao & Vu**：隨機矩陣條件數 (2010)
- 交叉參照：`1961-Hoare快速排序.md`、`1984-JohnsonLindenstrauss引理.md`、`1985-Yao計算隨機性.md`
