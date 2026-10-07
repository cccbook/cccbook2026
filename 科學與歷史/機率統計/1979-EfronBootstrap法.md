# 1979 - Efron Bootstrap 法

## 案件摘要
1979 年 Bradley Efron 在《The Annals of Statistics》發表 Bootstrap 方法，用「從樣本中重抽樣」這個看似偷懶的把戲，解開了無母數推論中「標準誤怎麼估」的死結。不靠任何分布假設，只靠計算能力，就能算出幾乎任何統計量的信賴區間。

## 前因 -- 為什麼會有這個案子
- 傳統推論依賴**參數假設**：例如「資料來自常態分布」，才有 $t$ 分配、$F$ 分配可用。
- 但現實資料常不遵循漂亮的分布；而許多統計量的抽樣分布**根本沒有解析解**——例如中位數、相關係數、迴歸係數比值、决策樹的準確率的標準誤。
- 早年有** jackknife**（Quenouille 1949、Tukey 1958，逐一留一重算）與**permutation test**（Fisher 1935，交換標籤重算）等重抽樣先驅，但它們各有局限：jackknife 對非平滑統計量（如中位數）失效，permutation test 主要用於檢定而非估計。
- 電腦運算能力在 1970 年代快速成長，「用計算換理論」成為可能——Efron 抓住了這個時機。

## 線索與推理 -- 數學式、程式、理論

### 核心思想：plug-in 原理
統計學中估計的根本策略是 **plug-in**：把經驗分布 $\hat F_n$ 代入理論公式中的真實分布 $F$：

$$
\theta = T(F) \quad\Longrightarrow\quad \hat\theta = T(\hat F_n)
$$

例如母體平均 $\theta = \int x \, dF(x)$，plug-in 估計就是 $\hat\theta = \bar x$。

### 難點：抽樣分布的 plug-in
我們想估的不只是 $\theta$，還有 $\hat\theta$ 的**變異程度**：

$$
\mathrm{Se}(\hat\theta) = \sqrt{\mathrm{Var}_F(\hat\theta)}
$$

但這需要知道真實分布 $F$——而 $F$ 未知。傳統做法靠數學推導（如中央極限定理給出 $\bar x$ 的漸近常態），但對一般 $T$ 無能為力。

### Bootstrap 的偷天換日
Efron 的洞察：**用 $\hat F_n$ 取代 $F$**，然後「重新扮演上帝」——從樣本本身模擬抽樣：

$$
X_1^*, \dots, X_n^* \stackrel{iid}{\sim} \hat F_n
\quad\text{（即：從原樣本中「抽出後放回」地抽 $n$ 次）}
$$

計算 $B$ 次 bootstrap 統計量：

$$
\hat\theta_b^* = T(X_1^{*(b)}, \dots, X_n^{*(b)}), \quad b = 1, \dots, B
$$

用這些 $\hat\theta_b^*$ 的經驗分布近似 $\hat\theta$ 的真實抽樣分布：

$$
\widehat{\mathrm{Se}}(\hat\theta) = \sqrt{\frac{1}{B-1}\sum_b (\hat\theta_b^* - \bar\theta^*)^2}
$$

### Bootstrap 信賴區間
**百分位法（percentile method）**最常用：取 bootstrap 分布的 $\alpha/2$ 與 $1-\alpha/2$ 分位數：

$$
\mathrm{CI}_{1-\alpha} = \left[ \hat\theta^*_{(\alpha B/2)},\; \hat\theta^*_{((1-\alpha/2)B)} \right]
$$

進階版本還有 basic 法、BCa（bias-corrected and accelerated）法，修正偏誤與偏度。

### 與 jackknife / permutation test 的對照

| 方法 | 原理 | 用途 | 局限 |
|------|------|------|------|
| **Bootstrap** | 放回重抽樣 | 估計（標準誤、信賴區間）、檢定 | 需大量計算；對極端相依結構需 block bootstrap |
| **Jackknife** | 逐一留一（$\binom{n}{n-1}$ 個子樣本） | 偏誤、標準誤估計 | 對非平滑統計量（中位數）失效 |
| **Permutation test** | 打亂標籤、所有排列 | 檢定（兩樣本比較） | 主要用於假設檢定，難給信賴區間 |

三者都屬「resampling」，但 bootstrap 最通用、最具擴展性。

### Python 實作：Bootstrap 信賴區間

```python
import numpy as np

np.random.seed(42)

# 母體：偏斜分布（指數），樣本數 n = 50
data = np.random.exponential(scale=2.0, size=50)
theta_hat = np.median(data)          # 我們想估計母體中位數
print(f"樣本中位數 = {theta_hat:.3f}")

B = 10_000
n = len(data)
boot = np.empty(B)

for b in range(B):
    idx = np.random.randint(0, n, n)   # 抽出後放回
    boot[b] = np.median(data[idx])

se = boot.std(ddof=1)
ci_lo, ci_hi = np.percentile(boot, [2.5, 97.5])
print(f"Bootstrap 標準誤 = {se:.3f}")
print(f"95% 信賴區間 = [{ci_lo:.3f}, {ci_hi:.3f}]")

# 驗證：真實中位數 = 2 * ln(2) ≈ 1.386，落在區間內
print(f"真實中位數 = {2 * np.log(2):.3f}")
```

輸出顯示 95% 信賴區間確實涵蓋真實中位數——而我們**完全沒有假設任何分布**。

## 結案 -- 後果與影響
- Bootstrap 成為現代統計的**標準工具**，被廣泛用於生物統計、經濟計量、機器學習模型評估。
- 對機器學習影響深遠：
  - **Bagging**（Breiman 1996）：bootstrap aggregating，對 bootstrap 樣本訓練多個模型再平均，降低變異。
  - **隨機森林**（Breiman 2001）：bagging + 特徵隨機選取，成為最強大的基礎學習器之一。
  - **Out-of-bag 誤差**：bootstrap 未抽到的資料（約 36.8%）可作為免費驗證集，機率為 $e^{-1}$。
- Efron 因此獲得多項榮譽（MacArthur Fellow、美國國家科學獎章 2005）。
- 理論持續發展：subagging、bagged V-statistics、與貝葉斯方法的結合（Bayesian bootstrap, Rubin 1981）。

## 關鍵人物與文獻
- **Bradley Efron**（史丹佛）：Bootstrap 之父，亦是 MacArthur 獎首位統計學家得主。
- Efron, B. (1979). *Bootstrap methods: Another look at the jackknife*. Annals of Statistics 7(1), 1–26.
- Efron, B., & Tibshirani, R. (1993). *An Introduction to the Bootstrap*. Chapman & Hall.
- Breiman, L. (1996). *Bagging predictors*. Machine Learning 24(2), 123–140.
- Breiman, L. (2001). *Random forests*. Machine Learning 45(1), 5–32.
