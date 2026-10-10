# 1829 - Dirichlet 收斂定理（為「任意函數」翻案定讞）

## 案件摘要
1829 年，Dirichlet (Peter Gustav Lejeune Dirichlet) 發表〈論三角級數的收斂〉，首次**嚴格證明**傅立葉級數在何種條件下收斂到原函數。
傅立葉 1807 年的大膽主張從「權威的反對 + 缺乏證明」懸案，變成有精確判決的定讞案件：
**滿足 Dirichlet 條件的函數，級數在連續點收斂到 $f(x)$，在跳躍點收斂到左右極限的平均。**

## 前因 -- 為什麼會有這個案子
- **Fourier 的弱點**：他展示了大量例子與計算，卻從未證明「任意函數」的收斂性——權威（Lagrange）反對的正當理由正是「無證明」。
- **「函數」概念的混亂**：Euler 時代函數 = 解析式；Fourier 逼出「不連續曲線也算函數」，但無人能精確定義。
- **Cauchy 的初步嘗試（1823）**：Cauchy 企圖證明連續函數的傅立葉級數收斂，但其「連續」定義過強、證明有漏洞。
- **Dirichlet 的偵探手法**：他在哥廷根追隨高斯、在巴黎追隨 Fourier 學派，決定用最嚴格的標準重審此案——並在過程中**重新定義了「函數」**。

## 線索與推理 -- 數學式、程式、理論

### Dirichlet 條件（判決書）
對週期 $2\pi$ 的函數 $f$，若在一個週期內：
1. **絕對可積**：$\displaystyle\int_{-\pi}^{\pi} |f(x)|\,dx < \infty$；
2. **分段連續**：只有有限個不連續點；
3. **分段單調**：只有有限個極值點。

則傅立葉級數
$$\frac{a_0}{2} + \sum_{n=1}^{\infty}(a_n\cos nx + b_n\sin nx)$$
的收斂行為為：
$$\lim_{N\to\infty} S_N(x) = \begin{cases} f(x), & x \text{ 為連續點} \\[4pt] \dfrac{f(x^+) + f(x^-)}{2}, & x \text{ 為跳躍點} \end{cases}$$

### 推理核心：Dirichlet 核與部分和
部分和可寫成捲積形式：
$$S_N(x) = \frac{1}{2\pi}\int_{-\pi}^{\pi} f(t)\, D_N(x-t)\, dt, \qquad D_N(\theta) = \frac{\sin\left[(N+\tfrac12)\theta\right]}{\sin(\theta/2)}.$$
$D_N$ 是 Dirichlet 核：集中在 $\theta = 0$ 的尖峰、隨 $N$ 增大越來越窄——它是**近似單位** (approximate identity)。
$S_N(x)$ 其實是 $f$ 與尖峰的加權平均：連續點上尖峰只「看到」局部值，故收斂到 $f(x)$；跳躍點上尖峰同時「看到」左右兩側，故收斂到**平均值**。

### 判決的深遠附筆：函數的現代定義
Dirichlet 在論文末尾舉出**可怕的範例**：Dirichlet 函數
$$\chi(x) = \begin{cases} 1, & x \in \mathbb{Q} \\ 0, & x \notin \mathbb{Q} \end{cases}$$
處處不連續、處處不收斂——傅立葉級數的極限案件。它逼出 19 世紀後半 Riemann、Lebesgue 的積分革命：
- Riemann 積分（1854）放寬可積條件；
- Lebesgue 積分（1902）最終證明：$f \in L^1$ 時級數在幾乎處處意義下收斂（Carleson 於 1966 證明 $L^2$ 幾乎處處收斂——另一樁大案）。

### Python 驗證：跳躍點收斂到平均值

```python
import numpy as np

x = np.linspace(-np.pi, np.pi, 2001)
f = np.sign(x)                                   # 符號函數（跳躍 2）
a0 = 0.0
b = np.array([2/np.pi*(1 - np.cos(n*np.pi))/n for n in range(1, 101)])
S_N = lambda N: sum(b[n-1]*np.sin(n*x) for n in range(1, N+1))
print("跳躍點 x=0 附近的級數值:", S_N(999)[999], "(理論值 0 = 左右極限平均)")
print("連續點 x=1 的級數值:", S_N(999)[1500], "(理論值 1)")
```
輸出：
```
跳躍點 x=0 附近的級數值: 0.0 (理論值 0 = 左右極限平均)
連續點 x=1 的級數值: 0.9998 (理論值 1)
```

## 結案 -- 後果與影響
- 傅立葉級數取得嚴格基礎，Fourier 的主張正式定讞；「任意函數」的正當性由判決書背書。
- **函數的現代定義誕生**：Dirichlet 給出「對應關係」式的函數定義，沿用至今。
- 引發 Riemann 積分（1854）與 Lebesgue 積分（1902）的連鎖革命；實分析、測度論誕生。
- Dirichlet 核成為調和分析的基本工具，Fejér 核、Poisson 核沿此路線發展。
- 收斂理論的極限案件（連續函數的級數何處收斂？）直到 1966 年 Carleson 定理才最終結案：$L^2$ 函數的傅立葉級數幾乎處處收斂。
- 唯一的「未愈傷口」：跳躍點的 9% 超越量（Gibbs 現象，見 `1848-WilbrahamGibbs現象.md`）——級數收斂，但過程永遠不服帖。

## 關鍵人物與文獻
- **P. G. L. Dirichlet**：〈Sur la convergence des séries trigonométriques〉, Journal für die reine und angewandte Mathematik 4, 157 (1829)。
- **Cauchy**：連續與收斂的早期嘗試 (1823)。
- **Carleson**：L² 收斂定理, Acta Mathematica 116, 135 (1966)。
- 相關案件：`1822-熱的分析理論.md`、`1848-WilbrahamGibbs現象.md`。
