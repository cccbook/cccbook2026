# 1812 - Laplace 分析理論

## 案件摘要

1812 年，Pierre-Simon Laplace 出版《Théorie analytique des probabilités》，將此前一世紀半的機率成果（Bernoulli、de Moivre、Bayes/Price、Legendre、Gauss）整合為一套以分析學（微積分、生成函數、微分方程）為工具的完整體系。這是機率論史上第一部集大成之作，中央極限定理的早期形式與「Laplace 之魔」的決定論哲學都出自此書及其配套著作。

## 前因 -- 為什麼會有這個案子

到 1810 年前後，機率論已有豐富但零散的成果：

1. **Bernoulli**（1713）大數法則：頻率收斂於機率。
2. **de Moivre**（1718, 1733）：生成函數技巧、《The Doctrine of Chances》、鐘形曲線。
3. **Bayes/Price**（1763）與 **Laplace 自己**（1774 起）：逆向機率、後驗更新。
4. **Legendre**（1805）最小平方法、**Gauss**（1809）常態誤差理論。

問題：這些成果彼此獨立、證明方法不一，缺乏統一的分析架構。Laplace 作為「法國的 Newton」（他的五大卷《天體力學》剛完成），決定為機率論做同樣的事——像處理行星運動那樣，用微分方程與冪級數馴服隨機性。他同時有強烈的動機：把機率應用到人口、司法、天文、保險，為拿破崙時代的国家治理服務（Laplace 曾短暫出任內政部長）。

## 線索與推理 -- 數學式、程式、理論

### 一、生成函數（Generating Functions）

Laplace 的核心武器是**機率生成函數**與**矩母函數**——繼承 de Moivre 而發揚光大。對非負整數值隨機變數 $X$：

$$G(s) = E[s^X] = \sum_{k} p_k s^k$$

性質（Laplace 用來把卷積變乘法、把遞迴變微分方程）：

$$G_{X+Y}(s) = G_X(s)\, G_Y(s), \qquad E[X] = G'(1), \qquad \operatorname{Var}(X) = G''(1) + G'(1) - G'(1)^2$$

**矩母函數**（Laplace 變換的機率版）：

$$M(t) = E[e^{tX}], \qquad E[X^n] = M^{(n)}(0)$$

這使得獨立和的分佈計算從「複雜的卷積」變成「簡單的乘法」，是處理 $n$ 次重複試驗的關鍵。

### 二、中央極限定理的早期形式

Laplace 在 1810 年的論文與 1812 年書中，用特徵函數（現代記號）證明：獨立同分佈隨機變數 $X_1, \dots, X_n$（期望 $\mu$、變異數 $\sigma^2$）的和，經標準化後趨於常態：

$$\frac{\sum_{i=1}^n X_i - n\mu}{\sigma\sqrt{n}} \;\xrightarrow{d}\; N(0, 1), \qquad \text{即 } P\left(a \le \frac{\bar{X}-\mu}{\sigma/\sqrt{n}} \le b\right) \to \Phi(b) - \Phi(a)$$

這是繼 de Moivre（二項特例）之後的一般化版本，Laplace 特別用於：

1. **證明誤差常態性**：觀測誤差是大量微小獨立擾動之和 $\Rightarrow$ 服從常態 $\Rightarrow$ Gauss 的誤差理論有了根據 $\Rightarrow$ 最小平方法有了機率基礎。
2. **二項抽樣的常態近似**：$\frac{\hat{p} - p}{\sqrt{p(1-p)/n}} \approx N(0,1)$，用於估計法國人口與出生率的精確度。

（「中央極限定理」一名由 Pólya 於 1920 年提出；嚴格的一般證明由 Lyapunov 1901、Lindeberg 1922 完成。）

### 三、機率的分析理論體系

《Théorie analytique》的結構（兩卷，含附錄）：

| 部分 | 內容 |
|------|------|
| 決定性分析 | 生成函數、差分方程、無窮級數 |
| 一般機率論 | 條件機率、Bayes 定理的推廣 |
| 應用 | 雅各賓賭博問題、人口統計、保險年金、**司法判決機率**、誤差理論與最小平方法 |

### 四、Laplace 的決定論與「Laplace 之魔」

1814 年《機率的哲學試論》（*Essai philosophique sur les probabilités*，此書的通俗版）中，Laplace 寫下科學史上最著名的決定論宣言：

> 「一種智慧，若在某一瞬間知曉自然界所有的作用力與所有生物的位置，並有能力將這些資料加以分析，則它能把宇宙中最大天體與最輕原子的運動一併納入同一公式；對它而言，沒有任何事是不確定的，未來與過去一樣清晰可見。」

**Laplace 之魔**的邏輯：宇宙是決定論的，機率只是「人類無知」的度量——

$$P(\text{事件}) = \frac{\text{對我們有利的已知情況數}}{\text{全部可能情況數}}$$

機率是「相對於我們知識狀態」的信念程度，而非自然界的內在隨機性。

### 五、機率的哲學：頻率 vs 信念

Laplace 的立場是**混合體**，埋下日後百年論戰的種子：

1. **頻率面向**：他用大數法則與 CLT 分析出生率、死亡率等長期頻率——經驗貝葉斯的先聲（用資料估先驗）。
2. **信念面向**：他主張逆向機率（Bayes 定理）配合「無充分理由原則」（均勻先驗）是理性推理的工具，甚至用它計算「太陽明天升起的機率」$\frac{n+1}{n+2}$（$n$ 為已觀察日數）——此推論至今仍被批評為均勻先驗的濫用。
3. 矛盾在於：若宇宙完全決定論，機率作為「信念」的客觀性何在？這正是 20 世紀頻率學派（Fisher、Neyman）攻擊的主觀機率之靶。

### Python：CLT 演示

```python
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)
n, trials = 30, 100000

# 擲骰子的和（非常態分佈的獨立和）
rolls = rng.integers(1, 7, size=(trials, n))
sums = rolls.sum(axis=1)

# 標準化
mu, sigma = 3.5 * n, np.sqrt(35 / 12 * n)   # E=3.5, Var=35/12 per die
z = (sums - mu) / sigma

plt.hist(z, bins=80, density=True, alpha=0.6, label=f"擲 {n} 次骰子的和（標準化）")
x = np.linspace(-4, 4, 300)
plt.plot(x, np.exp(-x**2 / 2) / np.sqrt(2 * np.pi), 'r-', lw=2, label="N(0,1)")
plt.legend(); plt.title("中央極限定理：骰子和趨於常態")
plt.xlabel("標準化和"); plt.show()

# 生成函數驗證：一顆公平骰子的 PGF
from fractions import Fraction
p = [Fraction(1, 6)] * 6
# G(s) = (s + s^2 + ... + s^6)/6，兩顆骰子和 = G(s)^2 的係數
G2 = np.polynomial.polynomial.polymul(np.ones(7) / 6, np.ones(7) / 6)
print("兩顆骰子和的分佈（係數）:", G2[2:13])  # 2..12 的機率
```

## 結案 -- 後果與影響

1. **19 世紀統計的聖經**：此書及其哲學試論主導了 19 世紀的機率與統計——Quetelet 的社會物理學、Maxwell 的氣體分子速度分佈（1859，直接受誤差理論啟發）、統計力學的誕生。
2. **誤差理論的整合**：Laplace 用 CLT 補全了 Gauss–Legendre 最小平方法的機率基礎，「常態 = 誤差定律」成為世紀共識。
3. **決定論的統治與崩塌**：「Laplace 之魔」支配科學世界觀直到 20 世紀——量子力學（Heisenberg 1927 測不準原理）宣告其破產，機率成為自然的內在性質。但此書的方法論（生成函數、矩母函數、特徵函數）至今仍是機率論的標準工具。
4. **現代遺產**：Laplace 變換在工程與微分方程中無所不在；CLT 是統計推論（信賴區間、檢定）的支柱；他的經驗貝葉斯思想在 1950 年代被 Robbins 復興。

## 關鍵人物與文獻

- **Pierre-Simon Laplace**（1749–1827）：「法國的 Newton」，天體力學與機率論的雙料集大成者。
  - Laplace, P.-S. (1812). *Théorie analytique des probabilités*. Paris.
  - Laplace, P.-S. (1814). *Essai philosophique sur les probabilités*.
- **Abraham de Moivre**（1667–1754）：生成函數與鐘形曲線的先驅。
- **Thomas Bayes / Richard Price**（1763）：逆向機率的起點，Laplace 大力推廣。
- **Carl Friedrich Gauss**（1809）：常態誤差理論，Laplace 以 CLT 為其補證。
- **Aleksandr Lyapunov / Jarl Waldemar Lindeberg**：20 世紀完成 CLT 的嚴格一般化。
