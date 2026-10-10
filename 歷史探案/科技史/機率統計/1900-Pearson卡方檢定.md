# 1900 - Pearson 卡方檢定

## 案件摘要
1900 年，Karl Pearson 發表卡方適合度檢定，第一次讓「假設檢定」擁有精確的數學基礎。他還用這把新武器，發現孟德爾的遺傳數據「完美得可疑」，留下統計史上一樁著名的懸案。

## 前因 -- 為什麼會有這個案子
19 世紀末，統計學家面對的核心難題是：**觀察到的頻率與理論期望的偏差，是隨機波動，還是理論錯了？**

在 Pearson 之前，人們只能憑直覺判斷「偏差大不大」。需要的是一個能將偏差化為**單一機率**的統計量——即給定理論正確時，偏差這麼大的機率有多低。

- 假設檢定的雛形：H0（理論成立）vs H1（理論不成立）。
- 需求：一個不依賴特定分佈形狀、適用於任何離散頻率數據的通用方法。

## 線索與推理 -- 數學式、程式、理論

### 線索一：卡方統計量的誕生
設 $k$ 個類別，觀察頻率 $O_i$，理論期望頻率 $E_i = n p_i$，Pearson 定義：

$$\chi^2 = \sum_{i=1}^{k} \frac{(O_i - E_i)^2}{E_i}$$

**Pearson 的重大定理（1900）**：當 $n \to \infty$ 且 H0 成立時，$\chi^2$ 收斂到自由度 $k-1$ 的卡方分佈。因此可計算 p 值：

$$p = P(\chi^2_{k-1} \ge \chi^2_{obs}) = 1 - F_{\chi^2_{k-1}}(\chi^2_{obs})$$

### 線索二：卡方分佈 $\chi^2_k$ 的性質
若 $Z_1,\dots,Z_k \overset{iid}{\sim} N(0,1)$，則

$$\chi^2_k = \sum_{i=1}^k Z_i^2$$

服從自由度為 $k$ 的卡方分佈，密度函數：

$$f(x;k) = \frac{x^{k/2-1} e^{-x/2}}{2^{k/2}\,\Gamma(k/2)}, \quad x > 0$$

- 均值 $E[\chi^2_k] = k$，變異數 $\text{Var}[\chi^2_k] = 2k$。
- 卡方分佈由 Hermert (1875) 與 Pearson 在常態理論中分別出現，但 Pearson 首次將其用於**任意頻率數據的檢定**。

### 線索三：自由度的概念
自由度 $df = k - 1 - (\text{被估計參數數})$。Pearson 最初誤認為永遠是 $k-1$；後來 **Fisher (1922/1924)** 糾正：當 $E_i$ 中的機率是從數據估計出來時，每估計一個參數要扣掉 1 個自由度。這場「Pearson–Fisher 爭論」也是統計史名案。

### 線索四：孟德爾數據的懸案
孟德爾豌豆雜交實驗預期顯性:隱性 $= 3:1$。Pearson 對孟德爾的 F2 比例數據計算卡方，發現：

$$\chi^2 \text{ 過小} \;\Rightarrow\; p \text{ 過高（趨近 1）}$$

**偏差比隨機波動還小**——數據「太完美」。1936 年 Fisher 計算孟德爾全部實驗的聯合 p 值約為 $10^{-8}$，即若孟德爾造假，他可能是整理數據時「讓結果朝期望值修飾」。至今無定論，但成為「數據不應完美」的統計偵辦經典。

### Python 實作：卡方檢定
```python
import numpy as np
from scipy import stats

# 孟德爾 F2 代：預期顯性:隱性 = 3:1，實際觀察 5474:1850（總 7324）
obs = np.array([5474, 1850])
exp = np.array([3/4, 1/4]) * obs.sum()
chi2 = ((obs - exp) ** 2 / exp).sum()
p = 1 - stats.chi2.cdf(chi2, df=1)
print(f"手算 chi2 = {chi2:.4f}, p = {p:.4f}")

# scipy 內建適合度檢定
chi2_s, p_s = stats.chisquare(obs, f_exp=[3/4*obs.sum(), 1/4*obs.sum()])
print(f"scipy  chi2 = {chi2_s:.4f}, p = {p_s:.4f}")

# 「太完美」示範：若數據恰好等於期望值
obs_perfect = exp.round()
chi2_p, p_p = stats.chisquare(obs_perfect)
print(f"完美數據 chi2 = {chi2_p:.4f}, p = {p_p:.4f}  (偏差過小反而可疑)")

# 卡方分佈圖
xs = np.linspace(0, 20, 400)
for df in [1, 3, 5, 10]:
    plt.plot(xs, stats.chi2.pdf(xs, df), label=f"k={df}")
plt.legend(); plt.title("chi-square distributions")
plt.savefig("chi2.png", dpi=100)
```

## 結案 -- 後果與影響
- 1900 年論文被譽為「現代統計檢定的開端」：假設檢定從此有了可計算的精確機率。
- 卡方檢定衍生出適合度檢定、獨立性檢定、同質性檢定三大用途。
- Fisher 修正自由度（1924）後，卡方檢定在大樣本近似下成為萬用工具。
- 孟德爾數據爭議促成現代「數據完整性稽核」（如 FISHER test of excess goodness）與造假偵測方法。
- 與 Student t 檢定、Fisher 的 ANOVA 一起，構成 20 世紀統計推論的三大支柱。

## 關鍵人物與文獻
- **Karl Pearson (1857–1936)**：卡方檢定發明人，Biometrika 創辦人。
- **R. A. Fisher (1890–1962)**：修正自由度，並對孟德爾數據提出「太完美」質疑。
- Pearson, K. (1900). *On the criterion that a given system of deviations...*. Phil. Mag. 50.
- Fisher, R. A. (1922). *On the interpretation of $\chi^2$ from contingency tables...*. JRSS 85.
- Fisher, R. A. (1936). *Has Mendel's work been rediscovered?* Annals of Science 1.
- Hermert, F. (1875). 多項分佈的卡方極限（先驅工作）。
