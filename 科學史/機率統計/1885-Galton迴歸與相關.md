# 1885 - Galton 迴歸與相關

## 案件摘要
1885 年，Francis Galton 在整理豌豆實驗與人類身高數據時，發現後代特徵會「向平均值退縮」。這條看似平凡的線索，最終引出了迴歸直線與相關係數，成為現代統計學的基石之一。

## 前因 -- 為什麼會有這個案子
維多利亞時代的英國瀰漫著優生學與遺傳研究的熱潮。Galton 是達爾文的表弟，他一心想回答：**天賦（如身高、智力）如何由父代傳到子代？**

當時流行的想法是：高個子的父親會生出越來越高的兒子，幾代之後人類將出現巨人。但 Galton 手中的數據卻暗示真相並非如此——這正是本案的「懸案」起點。

- 1877 年：Galton 完成豌豆實驗，發現小豌豆的後代平均比母代大，大豌豆的後代平均比母代小。
- 1885 年：他取得近 928 位成年子女與其父母的身高數據，發現同樣的「退縮」現象。

## 線索與推理 -- 數學式、程式、理論

### 線索一：豌豆實驗的謎團
Galton 將豌豆依母代大小分組（每組 $n=10$ 顆），種植後測量子代大小，發現：

$$\text{子代平均} = \bar{y}_{pop} + b\,(\text{母代大小} - \bar{x}_{pop})$$

其中斜率 $b < 1$（約 $0.33$）。**極端的母代，其子代會退回平均值附近**——他稱之為 "regression to mediocrity"（向平庸迴歸）。

### 線索二：身高數據的散佈圖
Galton 將 928 筆父子身高畫成散佈圖，並手繪等高線，發現等高線近似**同心橢圓**。這是雙變數常態分佈的視覺證據：

$$f(x,y) = \frac{1}{2\pi\sigma_X\sigma_Y\sqrt{1-\rho^2}} \exp\!\left(-\frac{1}{2(1-\rho^2)}\left[\frac{(x-\mu_X)^2}{\sigma_X^2} - \frac{2\rho(x-\mu_X)(y-\mu_Y)}{\sigma_X\sigma_Y} + \frac{(y-\mu_Y)^2}{\sigma_Y^2}\right]\right)$$

### 線索三：迴歸直線與相關係數
在雙變數常態分佈下，條件期望 $E[Y|X=x]$ 是一條直線：

$$E[Y|X=x] = \mu_Y + \rho\,\frac{\sigma_Y}{\sigma_X}(x-\mu_X)$$

其中**相關係數**：

$$r = \frac{\text{Cov}(X,Y)}{\sigma_X\sigma_Y} = \frac{\sum_i (x_i-\bar{x})(y_i-\bar{y})}{\sqrt{\sum_i (x_i-\bar{x})^2}\,\sqrt{\sum_i (y_i-\bar{y})^2}} \in [-1, 1]$$

Galton 身高數據的 $r \approx 0.5$：兒子身高的「可預測部分」只有父代身高偏差的一半。**退縮不是生物衰敗，而是常態分佈與不完全相關的必然數學結果。**

### 推理重點
1. 「迴歸」最初是生物學現象的名字，後來被抽象為**線性條件期望**的統計方法。
2. 相關係數 $r$ 同時是迴歸斜率（標準化後）：$\text{slope} = r \cdot \sigma_Y/\sigma_X$。
3. 迴歸到均值會產生「假效果」陷阱：例如補習後成績變差 ≠ 補習無效，可能是單純的均值迴歸。

### Python 模擬：父子身高迴歸
```python
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)
n = 928
father_h = rng.normal(69, 2.7, n)          # 父親身高（吋）
son_h = 69 + 0.5 * (father_h - 69) + rng.normal(0, 2.7 * np.sqrt(1 - 0.25), n)

# 最小平方迴歸
x, y = father_h, son_h
slope = np.cov(x, y)[0, 1] / x.var()
intercept = y.mean() - slope * x.mean()
r = np.corrcoef(x, y)[0, 1]
print(f"r = {r:.3f}, slope = {slope:.3f}, intercept = {intercept:.2f}")

# 驗證「極端組退縮」：父親最高 10% 的兒子平均
tall = father_h > np.quantile(father_h, 0.9)
print(f"高個父親組: 父 {x[tall].mean():.2f}, 子 {y[tall].mean():.2f} (子代退回平均)")

plt.scatter(x, y, s=6, alpha=0.5)
plt.plot(np.sort(x), intercept + slope * np.sort(x), 'r', lw=2, label='regression line')
plt.xlabel("father height"); plt.ylabel("son height"); plt.legend()
plt.title(f"Galton regression (r={r:.2f})"); plt.savefig("galton.png", dpi=100)
```

## 結案 -- 後果與影響
- 1886 年 Galton 發表《Regression towards Mediocrity in Hereditary Stature》，正式命名「迴歸」。
- 1888 年他提出相關係數的定義，並指出可用相關程度衡量遺傳強度。
- 1896 年 **Karl Pearson** 將相關與迴歸完全數學化，導出積差相關（product-moment correlation）、迴歸係數的抽樣誤差，並建立雙變數常態的嚴格理論。
- 迴歸成為日後最小平方法、多元迴歸、廣義線性模型的起點；Galton 的「向平庸迴歸」也成為社會科學中「均值迴歸謬誤」的經典警示。

## 關鍵人物與文獻
- **Francis Galton (1822–1911)**：英國博學家，統計遺傳學之父。
- **Karl Pearson (1857–1936)**：將 Galton 的直覺數學化，創辦《Biometrika》。
- Galton, F. (1877). *Typical laws of heredity*. — 豌豆實驗
- Galton, F. (1886). *Regression towards mediocrity in hereditary stature*. JRAS.
- Galton, F. (1888). *Co-relations and their measurement*. Proc. R. Soc.
- Pearson, K. (1896). *Mathematical contributions to the theory of evolution. III. Regression, heredity, and panmixia*. Phil. Trans. R. Soc. A.
