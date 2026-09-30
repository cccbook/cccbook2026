# 1925 - Fisher 統計方法

## 案件摘要
1925 年，R. A. Fisher 出版《Statistical Methods for Research Workers》，將顯著性檢定、p 值、ANOVA 與實驗設計打包成「研究者工具箱」。這本書被尊為「統計學聖經」，也讓 $p < 0.05$ 成為百年來最受愛戴與爭議的慣例。

## 前因 -- 為什麼會有這個案子
Fisher 自 1919 年起任職於英國的 **Rothamsted 農業實驗站**（The Laboratory for Agricultural Experimentation，1843 年創立），面對的是現實的難題：

- 農業實驗的**田地變異**極大：土壤肥力、日照、排水在不同位置都不一樣。
- 實驗成本高，樣本數有限，且**天氣不可重複**。
- 當時的研究者（生物、農業、醫學）大多不懂數學，需要一本**不推公式、直接給方法**的實用手冊。

**懸案**：如何在充滿雜訊、無法完美控制的實驗中，做出可靠的因果結論？

## 線索與推理 -- 數學式、程式、理論

### 線索一：Rothamsted 的實驗困境
Rothamsted 有長達 70 年的長期田間實驗數據（如 Broadbalk wheat experiment），但田地異質性使得「處理 A 比處理 B 好」的結論常常不可信。Fisher 的破案關鍵是**用隨機化把不可控變異轉化為可估計的誤差**。

### 線索二：顯著性檢定與 p 值
Fisher 在書中正式推廣顯著性檢定流程：

1. 設定 H0（如「處理無效應」）。
2. 選擇檢定統計量 $T$。
3. 在 H0 下計算**p 值**：

   $$p = P_0(T \ge t_{obs})$$

4. 若 $p$ 足夠小，則 H0「顯著不成立」，拒絕 H0。

書中列出 $t$、$\chi^2$、$F$ 分佈的表格，使研究者能直接查表完成檢定——這是**統計方法平民化**的關鍵一步。

### 線索三：$p < 0.05$ 慣例的誕生
Fisher 在書中寫道（大意）：

> "…we shall not often be astray if we draw a conventional line at 0.05."

這句話是 $p < 0.05$ 慣例的**直接來源**。Fisher 原意是「常用門檻」而非「神聖界線」，但後世將其制度化為學術出版的硬門檻，造成：

- **正面爭議**：0.05 是方便的共識語言，易於比較。
- **負面爭議**：p-hacking、發表偏誤（publication bias）、可重複性危機（reproducibility crisis）。
- 2016 年 ASA 發表聲明：p 值不應作為唯一的科學結論依據。

### 線索四：變異數分析（ANOVA）
ANOVA 將總變異分解為「處理效應」與「隨機誤差」：

$$\underbrace{\sum_i (y_i - \bar{y})^2}_{SS_{total}} = \underbrace{\sum_g n_g(\bar{y}_g - \bar{y})^2}_{SS_{between}} + \underbrace{\sum_i (y_i - \bar{y}_g)^2}_{SS_{within}}$$

檢定統計量為 **F 統計量**：

$$F = \frac{SS_{between} / (k-1)}{SS_{within} / (N-k)} = \frac{MS_{between}}{MS_{within}} \;\sim\; F_{k-1,\,N-k} \;\;(\text{H0 下})$$

其中 $k$ 為組數、$N$ 為總樣本數。這是 Gosset t 檢定的推廣：兩組時 $F = t^2$。

### 線索五：實驗設計三原則
Fisher 總結實驗設計的三大支柱：

1. **隨機化（randomization）**：處理隨機分配到實驗單位，使未知干擾因素在期望上抵消。
2. **對照（control / replication）**：設對照組，並重複觀察以估計誤差。
3. **區集（blocking）**：將同質的實驗單位分組，使組內比較更精確（如同一塊田切成幾個小區）。

經典範例：**隨機區集設計（Randomized Block Design）**與**拉丁方格（Latin Square）**，至今仍是農業與醫學實驗的標準設計。

### Python 實作：ANOVA
```python
import numpy as np
from scipy import stats
import pandas as pd

rng = np.random.default_rng(3)
# 三種肥料的作物產量（隨機區集概念下的單因子 ANOVA）
groups = [rng.normal(50, 5, 20), rng.normal(53, 5, 20), rng.normal(56, 5, 20)]

k, N = len(groups), sum(len(g) for g in groups)
grand = np.concatenate(groups).mean()
ss_between = sum(len(g) * (g.mean() - grand)**2 for g in groups)
ss_within = sum(((g - g.mean())**2).sum() for g in groups)
F = (ss_between / (k-1)) / (ss_within / (N-k))
p = 1 - stats.f.cdf(F, k-1, N-k)
print(f"手算 F = {F:.3f}, p = {p:.4f}")

# scipy 內建
F_s, p_s = stats.f_oneway(*groups)
print(f"scipy F = {F_s:.3f}, p = {p_s:.4f}")
print("顯著" if p_s < 0.05 else "不顯著", "（p < 0.05 慣例）")

# 實驗設計示範：隨機化分配處理
units = np.arange(30)
rng.shuffle(units)
assign = np.array(['A', 'B', 'C'] * 10)
print("隨機化分配:", dict(zip(*[list(units[:9]), list(assign[:9])])))

# 視覺化
df = pd.DataFrame({'yield': np.concatenate(groups),
                   'fertilizer': np.repeat(['A','B','C'], 20)})
df.boxplot(column='yield', by='fertilizer')
plt.title("One-way ANOVA"); plt.savefig("anova.png", dpi=100)
```

## 結案 -- 後果與影響
- 《Statistical Methods for Research Workers》共出 14 版（1925–1970），譯成多國語言，被譽為 **20 世紀最有影響力的統計學書籍**，地位等同「統計學聖經」。
- 顯著性檢定 + ANOVA + 實驗設計三件套，成為農業、醫學、心理學、經濟學的標準研究流程。
- 1935 年 Fisher 出版《The Design of Experiments》，進一步發展實驗設計理論（含著名的「女士品茶」實驗）。
- Neyman–Pearson 的「假設檢定理論」（1933）與 Fisher 的顯著性檢定在概念上競爭，但後世教材將兩者混合成今日通行的「NHST」。
- $p < 0.05$ 慣例造成的可重複性危機，促成 2010 年代後的預註冊（preregistration）、效應量報告與 ASA 聲明（2016）。
- Fisher 的 ANOVA 是日後廣義線性模型、混合效應模型的理論源頭。

## 關鍵人物與文獻
- **R. A. Fisher (1890–1962)**：顯著性檢定、ANOVA、實驗設計、p 值慣例的奠基者。
- **Jerzy Neyman & Egon Pearson (1933)**：對立假設與檢定力理論，與 Fisher 長期論戰。
- **Rothamsted 農業實驗站**：Fisher 1919–1933 年任職處，實驗設計的搖籃。
- Fisher, R. A. (1925). *Statistical Methods for Research Workers*. Oliver & Boyd.
- Fisher, R. A. (1935). *The Design of Experiments*. Oliver & Boyd.
- ASA (2016). *Statement on Statistical Significance and P-Values*. The American Statistician 70.
- Salsburg, D. (2001). *The Lady Tasting Tea*. （統計史通俗讀物）
