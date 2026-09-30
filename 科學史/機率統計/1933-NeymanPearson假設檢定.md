# 1933 - Neyman–Pearson 假設檢定

## 案件摘要
1933 年，Jerzy Neyman 與 Egon Pearson（Karl Pearson 之子）發表〈論假設檢定最有效檢定問題〉，將假設檢定從 Fisher 的「顯著性檢定」升級為「兩假說對決」的決策理論，確立 Type I/II 錯誤、檢定力與最強力檢定的框架。

## 前因 -- 為什麼會有這個案子
- Fisher（1925）的顯著性檢定只有一個虛無假說 $H_0$ 與 p 值，但「不顯著」代表什麼？缺乏對照標的。
- 同一組資料可能有多種合理檢定統計量，Fisher 框架無法回答「哪個檢定最好」。
- Neyman 與 E. Pearson 在 1928–1933 年間合作，引入對立假說 $H_1$ 與錯誤率的雙重控制。

## 線索與推理 -- 數學式、程式、理論
### 兩假說對決與兩種錯誤
檢定問題：在 $H_0: \theta \in \Theta_0$ vs $H_1: \theta \in \Theta_1$ 之間抉擇。

| 真實\判決 | 接受 $H_0$ | 拒絕 $H_0$ |
|---|---|---|
| $H_0$ 真 | ✓ | **Type I 錯誤**（機率 $\alpha$） |
| $H_1$ 真 | **Type II 錯誤**（機率 $\beta$） | ✓ |

- 顯著水準：$\alpha = P(\text{拒絕 } H_0 \mid H_0 \text{ 真})$（誤判無辜）
- 檢定力：$1 - \beta = P(\text{拒絕 } H_0 \mid H_1 \text{ 真})$（成功定罪）
- 好的檢定：在固定 $\alpha$ 下，**最大化檢定力** $1-\beta$。

### Neyman–Pearson 引理（最強力檢定）
對簡單假說 $H_0: \theta=\theta_0$ vs $H_1: \theta=\theta_1$，最強力（MP）檢定為**概似比檢定**：給定顯著水準 $\alpha$，拒絕域為
$$
\Lambda(x) = \frac{L(\theta_0; x)}{L(\theta_1; x)} \leq k
$$
其中 $k$ 選擇使 $P_{\theta_0}(\Lambda(X) \leq k) = \alpha$。任何其他水準 $\leq \alpha$ 的檢定，其檢定力都不會超過此檢定。證明工具是 Markov 不等式的變形（Neyman–Pearson 不等式）。

### Fisher vs Neyman–Pearson 學派之爭
- **Fisher**：p 值是資料對 $H_0$ 的「不合理程度」證據，反對事先設定 $\alpha$、反對接受/拒絕的機械式決策。
- **Neyman–Pearson**：檢定是長期重複使用的行為準則，重點是控制錯誤率與檢定力，應事先選定 $\alpha$、$n$ 與對立假說。
- 兩人長年激烈筆戰，但現代教科書實務上是**混合體**：以 NP 框架設計檢定，用 Fisher 式 p 值報告證據。

```python
# 模擬 Type I / Type II 錯誤
import numpy as np
from scipy import stats

rng = np.random.default_rng(1)
n, mu0, mu1, alpha, reps = 30, 0.0, 0.6, 0.05, 20000
z_crit = stats.norm.ppf(1 - alpha/2)

typeI = typeII = 0
for _ in range(reps):
    x0 = rng.normal(mu0, 1, n)          # H0 為真
    z0 = (x0.mean() - mu0) / (1/np.sqrt(n))
    if abs(z0) > z_crit: typeI += 1

    x1 = rng.normal(mu1, 1, n)          # H1 為真
    z1 = (x1.mean() - mu0) / (1/np.sqrt(n))
    if abs(z1) <= z_crit: typeII += 1

print(f"實測 Type I  錯誤率 = {typeI/reps:.4f}（目標 alpha={alpha}）")
print(f"實測 Type II 錯誤率 = {typeII/reps:.4f}，檢定力 = {1-typeII/reps:.4f}")

# 理論檢定力：power = P(|Z|>z_crit | mu=mu1)
from scipy.stats import norm
power = norm.cdf(-z_crit - mu1*np.sqrt(n)) + 1 - norm.cdf(z_crit - mu1*np.sqrt(n))
print(f"理論檢定力 = {power:.4f}")
```

## 結案 -- 後果與影響
- 現代假設檢定框架（顯著水準、檢定力、樣本數設計）全由此案確立。
- 引理延伸出**廣義概似比檢定（GLRT）**與 Wilks 定理，成為統計實務主力。
- 檢定力分析成為臨床試驗與實驗設計的法定步驟。
- 學派之爭也間接促成後來的決策理論（Wald, 1950）。

## 關鍵人物與文獻
- **Jerzy Neyman**（1894–1981）：波蘭裔統計學家。
- **Egon Pearson**（1895–1980）：Karl Pearson 之子，承其父衣缽而轉向新理論。
- **J. Neyman & E. S. Pearson (1933), "On the Problem of the Most Efficient Tests of Statistical Hypotheses", Phil. Trans. R. Soc. A 231.**
- R. A. Fisher：顯著性檢定的原創者與論戰對手。
