# 1902 — Lebesgue 測度與積分

## 案件摘要
1902 年，28 歲的 Henri Lebesgue 在南錫大學發表博士論文《Intégrale, longueur, aire》，提出測度論與以「值域分割」為核心的新積分。Riemann 積分處理不了病態函數、無法安心交換極限與積分號——Lebesgue 的 $\int f\,d\mu$ 把這兩樁懸案一併偵破，為實分析與機率論的公理化打下地基。

## 前因 -- 為什麼會有這個案子
- **Riemann 積分的缺陷一：病態函數**。1875 年前後，Du Bois-Reymond 構造出可積函數的傅立葉級數卻在處處收斂到一個**不可積**的函數；Dirichlet 的狄利克雷函數（有理數處為 1、無理數處為 0）在 Riemann 意義下完全不可積。「到處不連續」到什麼程度才不可積？Riemann 理論答不上來。
- **Riemann 積分的缺陷二：極限交換困難**。分析學到處需要 $\lim \int f_n = \int \lim f_n$（例如傅立葉級數逐項積分），但 Riemann 積分只有在相當強的一致收斂下才允許交換，而一致收斂太苛刻、常常不成立。
- **Jordan 容度**：1892 年 Jordan 用有限個區間覆蓋來量「長度」，但只能處理邊界整齊的集合——對有理數集這種「到處稀疏卻稠密」的集合無能為力。測量的量尺必須升級。

## 線索與推理 -- 數學式、程式、理論

### 線索一：測度——可數可加的量尺
Lebesgue 的關鍵升級：不再用有限個區間，改用**可數個**區間覆蓋，取外測度

$$m^*(E) = \inf\left\{\sum_{n=1}^{\infty} (b_n - a_n) \;:\; E \subset \bigcup_{n=1}^{\infty} (a_n, b_n)\right\}$$

滿足 Carathéodory 可測條件的集合稱為可測集，其測度 $m$ 具**可數可加性**：若 $E_i$ 互不相交，則 $m\left(\bigcup_i E_i\right) = \sum_i m(E_i)$。

後果立現：單點測度為 0，故有理數集 $\mathbb{Q} \cap [0,1]$ 是可數個單點的聯集，測度為 0——「到處稠密」卻測量起來是零。無理數集的測度則是 $1$。狄利克雷函數案的兇手現形。

### 線索二：值域分割 vs 定義域分割
Riemann 積分切**定義域**：把 $[a,b]$ 切成小區間，每段取高 $\times$ 寬求和。Lebesgue 反其道而行，切**值域**：把 $f$ 的函數值分層，問「$f$ 的值落在 $[y, y+dy]$ 的 $x$ 有多少測度」：

$$\int_{[a,b]} f\,dm = \lim_{\Delta y \to 0} \sum_k y_k \; m\left(\{x : y_k \le f(x) < y_{k+1}\}\right)$$

用「錢袋比喻」：Riemann 是把一袋硬幣按時間順序一枚枚加總；Lebesgue 是先把硬幣按面額分堆，各堆數量乘面額再相加。對「亂序」的函數（如狄利克雷函數），分堆法輕鬆取勝：

$$\int_{[0,1]} \mathbf{1}_{\mathbb{Q}}\,dm = 1 \cdot m(\mathbb{Q}) + 0 \cdot m(\mathbb{Q}^c) = 0$$

狄利克雷函數可積了，積分值為 0——與直覺（「幾乎處處是 0」）完全吻合。

### 線索三：控制收斂定理——極限交換結案
Lebesgue 積分的殺手鐧是收斂定理。**單調收斂定理**：$0 \le f_1 \le f_2 \le \cdots$，則 $\int \lim f_n = \lim \int f_n$。**控制收斂定理（DCT, 1910 年正式表述）**：若 $|f_n| \le g$ 可積且 $f_n \to f$ 逐點，則

$$\lim_{n\to\infty}\int f_n\,dm = \int f\,dm$$

不需要一致收斂，只要一個可積的「上限擔保」$g$。傅立葉級數逐項積分、機率中的期望值極限，從此有了穩固的法律依據。配套的完整空間 $L^1$、$L^2$（Riesz–Fischer, 1907）讓傅立葉分析脫胎換骨。

### 線索四：從測度到機率
1933 年 Kolmogorov 把機率公理化：機率就是測度，樣本空間 $\Omega$ 上的 $\sigma$-代數 $\mathcal{F}$，$P: \mathcal{F} \to [0,1]$ 且 $P(\Omega)=1$；隨機變數的期望值就是 Lebesgue 積分：

$$E[X] = \int_\Omega X\,dP$$

大數法則、遍歷定理、隨機過程全部建立在 Lebesgue 的地基上。1902 年的積分理論，三十年後變成整座機率大廈。

### 程式碼範例：Lebesgue 積分的簡單模擬
```python
import numpy as np

def lebesgue_integral(f, a=0, b=1, n_levels=64, N=200000):
    # 值域分割：把 f 的「值」切成 n_levels 層，按層的測度加權
    x = np.random.uniform(a, b, N)          # 用蒙地卡羅近似 [a,b] 上的測度
    y = f(x)
    edges = np.linspace(0, y.max() + 1e-12, n_levels + 1)
    total = 0.0
    for k in range(n_levels):
        mask = (y >= edges[k]) & (y < edges[k+1])   # 值落在第 k 層的點集
        m = mask.mean() * (b - a)                    # 該點集的（近似）測度
        total += edges[k] * m                        # y_k * m(第 k 層)
    return total

# 案件一：狄利克雷函數（Riemann 不可積，Lebesgue 積分 = 0）
f_dirichlet = lambda x: (np.abs(x - np.round(x)) < 1e-9).astype(float)
print("狄利克雷函數 Lebesgue 積分 ≈", lebesgue_integral(f_dirichlet))  # ≈ 0

# 案件二：x^2 在 [0,1]，理論值 1/3
f_sq = lambda x: x**2
print("∫x² dx ≈", lebesgue_integral(f_sq), "（Riemann 應也得 1/3 ≈", 1/3, "）")
```

模擬顯示：狄利克雷函數在 Riemann 意義下「每個分割都取不準」而不可積，Lebesgue 分層法卻乾淨地得到 0；對光滑函數兩者一致——新量尺嚴格包含舊量尺。

## 結案 -- 後果與影響
- **實分析誕生**：測度論 + Lebesgue 積分成為二十世紀分析的標準語言，$L^p$ 空間、完備性、對偶理論構成泛函分析的基石。
- **傅立葉分析重生**：Parseval 等式、逐項積分、Carleson 定理（1966，$L^2$ 傅立葉級數幾乎處處收斂）都在 Lebesgue 框架內才可能證明。
- **機率論公理化**：Kolmogorov 1933 年以測度論重建機率，現代隨機過程、金融數學（Black–Scholes 的 Itô 積分）皆其後裔。
- Riemann 積分並未作廢——數值計算與光滑函數的世界仍是它的天下；Lebesgue 提供的是「幾乎處處」的理論法庭。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Henri Lebesgue | 測度與積分理論創始人 |
| Émile Borel | Borel 集合與可數覆蓋的前驅 |
| Camille Jordan | 容度理論（有限覆蓋版本） |
| Frigyes Riesz / Ernst Fischer | $L^p$ 完備性（Riesz–Fischer 定理） |
| Andrey Kolmogorov | 1933 年機率公理化 |

- H. Lebesgue, *Intégrale, longueur, aire*, Annali di Matematica (1902)；另見其博士論文版本。
- H. Lebesgue, *Leçons sur l'intégration et la recherche des fonctions primitives* (1904)。
- A. Kolmogorov, *Grundbegriffe der Wahrscheinlichkeitsrechnung* (1933)。
