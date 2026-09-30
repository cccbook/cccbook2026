# 1908 - Student t 檢定

## 案件摘要
1908 年，Guinness 啤酒廠的化學家 William Gosset 以筆名 "Student" 發表 t 檢定，解決了「樣本太少無法推論」的難題。這是統計史上最曲折的一樁案子：商業機密迫使偵探隱姓埋名，卻藏不住劃時代的發現。

## 前因 -- 為什麼會有這個案子
Guinness 啤酒廠想用科學方法檢測**大麥（barley）品質**與釀酒條件。但現實是殘酷的：

- 每批實驗只能取**少數幾份樣本**（$n = 2 \sim 10$），大量取樣成本太高。
- 當時的檢定理論（如 Pearson 卡方）都是**大樣本近似**，樣本少時完全失靈。
- 用樣本標準差 $s$ 代替母體 $\sigma$ 會引入額外的不確定性，小樣本下這個誤差會被放大。

**懸案**：樣本 $n$ 很小時，$\bar{X}$ 的抽樣分佈到底是什麼？

## 線索與推理 -- 數學式、程式、理論

### 線索一：Guinness 的商業機密（偵探故事）
Guinness 曾因員工洩露釀造配方而蒙受損失，因此**禁止員工發表任何研究**。Gosset 想發表 t 檢定，只好：
- 以筆名 **"Student"** 發表（據說是先用「學生」代筆簽名，再以此為名）。
- 論文不能提及 Guinness 與啤酒。

這解釋了為什麼這項影響巨大的發明，署名卻是化名——**商業機密藏住了名字，藏不住數學**。Gosset 在 Guinness 內部被稱為 "the student" 長達 30 年，直到 1937 年去世後真名才廣為人知。

### 線索二：t 統計量的定義
當 $X_1,\dots,X_n \overset{iid}{\sim} N(\mu, \sigma^2)$，且 $\sigma$ 未知、以樣本標準差 $s$ 估計時：

$$t = \frac{\bar{X} - \mu}{s / \sqrt{n}}, \qquad s = \sqrt{\frac{1}{n-1}\sum_i (X_i - \bar{X})^2}$$

Gosset 用蒙地卡羅方法（取 750 個樣本、$n=4$，手算各組的 $t$ 值）發現其分佈**比常態更厚尾**（fat tails）：

$$f(t; \nu) = \frac{\Gamma\!\left(\frac{\nu+1}{2}\right)}{\sqrt{\nu\pi}\,\Gamma\!\left(\frac{\nu}{2}\right)} \left(1 + \frac{t^2}{\nu}\right)^{-\frac{\nu+1}{2}}, \quad \nu = n-1$$

- 厚尾意味着：極端值出現的機率比常態分佈高，小樣本下用常態分佈會**低估 p 值**（過度自信）。
- $\nu = 1$ 為 Cauchy 分佈（均值不存在）；$\nu \to \infty$ 時 t 分佈收斂到 $N(0,1)$。

### 線索三：數學證明的補完
Gosset 只是**化學家**，數學證明不夠嚴謹（他以蒙特卡羅為主、推導為輔）。1915 年 **Fisher** 補上了嚴格證明：
- $\bar{X}$ 與 $s$ 在常態母體下**獨立**（這是 t 分佈成立的關鍵，也是 Fisher 的重要發現）。
- $(n-1)s^2/\sigma^2 \sim \chi^2_{n-1}$，且 $\bar{X} \sim N(\mu, \sigma^2/n)$，故

$$\frac{Z}{\sqrt{\chi^2_\nu/\nu}} \sim t_\nu, \qquad Z \sim N(0,1)$$

1925 年 Fisher 在《Statistical Methods for Research Workers》將 t 檢定發揚光大，成為標準工具。

### 推理重點
1. $t = \dfrac{\bar{X}-\mu}{s/\sqrt{n}}$ 中的 $s$ 是「估計值」而非「真值」，其波動會使分佈加厚。
2. 自由度 $\nu = n-1$：扣掉用於估計 $\bar{X}$ 的 1 個自由度。
3. 現代意義：**任何 $\sigma$ 未知、常態假設下的小樣本均值推論**，都應使用 t 而非 z。
4. 統計教學啟示：Gosset 用「模擬 + 直覺」發現定理，Fisher 用「嚴謹證明」補完——兩者都是科學推進的典範。

### Python 實作：t 分佈 vs 常態分佈
```python
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)
xs = np.linspace(-6, 6, 500)

plt.plot(xs, stats.norm.pdf(xs), 'k--', label="N(0,1)")
for df in [1, 4, 10, 30]:
    plt.plot(xs, stats.t.pdf(xs, df), label=f"t (df={df})")
plt.legend(); plt.title("t vs Normal: fat tails with small df")
plt.savefig("t_dist.png", dpi=100)

# 厚尾的數值驗證：t(4) 超過 3 的機率 vs N(0,1)
print(f"P(|t4|>3) = {2*stats.t.sf(3, 4):.4f}")
print(f"P(|z|>3)  = {2*stats.norm.sf(3):.4f}")   # t 檢定更保守

# 模擬 Gosset 的實驗：n=4，驗證 t 統計量的經驗分佈
mu, sigma, n, trials = 0, 1, 4, 750
ts = []
for _ in range(trials):
    x = rng.normal(mu, sigma, n)
    ts.append((x.mean() - mu) / (x.std(ddof=1) / np.sqrt(n)))
print(f"模擬 ks-test vs t(3): p = {stats.kstest(ts, 't', args=(3,)).pvalue:.4f}")

# 單樣本 t 檢定範例：n=5 的樣本
sample = [8.2, 9.1, 7.8, 8.6, 8.9]
t_s, p_s = stats.ttest_1samp(sample, popmean=8.0)
print(f"t = {t_s:.3f}, p = {p_s:.4f}")
```

## 結案 -- 後果與影響
- 1908 年論文《The Probable Error of a Mean》使**小樣本推論**從無到有。
- t 檢定衍生出單樣本、獨立雙樣本、配對樣本三大變體，成為應用統計使用率最高的方法之一。
- Fisher 的獨立性證明（1915）成為常態母體抽樣理論的里程碑，也是日後變異數分析的基石。
- Gosset 的真名在 1937 年才公開；「Student」筆名成為統計史最著名的化名。
- 商業機密與學術發表的張力，成為「企業科研是否該保密」的經典案例。

## 關鍵人物與文獻
- **William Sealy Gosset (1876–1937)**：Guinness 化學家，筆名 Student。
- **R. A. Fisher (1890–1962)**：1915 年補完 t 分佈數學證明，1925 年推廣 t 檢定。
- Student (1908). *The probable error of a mean*. Biometrika 6.
- Fisher, R. A. (1915). *Frequency distribution of the values of the correlation coefficient in samples from an indefinitely large population*. Biometrika 10.
- Fisher, R. A. (1925). *Statistical Methods for Research Workers*. Oliver & Boyd.
- E. S. Pearson & R. L. Plackett (1975/1990). Gosset 的傳記與書信研究。
