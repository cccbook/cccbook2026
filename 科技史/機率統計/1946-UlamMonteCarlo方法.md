# 1946 - Ulam Monte Carlo 方法

## 案件摘要
1946 年，Stanislaw Ulam 在 Los Alamos 為 Manhattan 計畫研究「中子擴散」時，從紙牌接龍遊戲獲得靈感，與 John von Neumann 合作提出以亂數取樣做統計估計的方法，由 Nicholas Metropolis 命名為「Monte Carlo」。

## 前因 -- 為什麼會有這個案子
- Manhattan 計畫需計算中子在裂變材料中的行為（中子散射、吸收、連鎖反應機率），涉及高維、非線性的隨機過程，解析方法與確定性數值法（如網格法）都無能為力——維度災難。
- 當時 ENIAC 等早期電腦問世，第一次有機器可以執行大量重複計算。
- 早在 1908 年 Gosset（Student）已用亂數抽樣估計 t 分佈，但無電腦且未形成方法論。

## 線索與推理 -- 數學式、程式、理論
### Ulam 的紙牌接龍靈感
1946 年 Ulam 病癒養傷時玩 Canfield 接龍，想知道「成功過關的機率」。組合分析太難，他想到：**與其組合計算，不如玩幾百局數一數贏幾局**。他隨即意識到同樣思路適用於中子擴散——追蹤一顆顆中子的隨機軌跡，再統計結果。

### Monte Carlo 原理：亂數取樣 + 統計估計
以強大數法則為理論基礎：若 $X_i$ iid 且 $E[|X|] < \infty$，則
$$
\hat{I}_n = \frac{1}{n}\sum_{i=1}^n X_i \xrightarrow{a.s.} E[X] = \mu
$$
收斂速度由 CLT 給出：標準誤差為 $\sigma/\sqrt{n}$，即**誤差 $O(n^{-1/2})$，與維度無關**——這正是突破維度災難的關鍵。

積分估計：對 $\int_a^b f(x)\,dx$，令 $X \sim U(a,b)$：
$$
\int_a^b f(x)\,dx = (b-a)\, E[f(X)] \approx (b-a)\,\frac{1}{n}\sum_{i=1}^n f(X_i)
$$

### $\pi$ 估計範例（Buffon 丟針的電腦版）
在單位正方形內均勻撒點，落在四分之一圓內的機率為
$$
P\big(X^2 + Y^2 \leq 1\big) = \frac{\pi}{4} \quad \Rightarrow \quad \hat\pi = 4 \cdot \frac{\#\{x_i^2+y_i^2 \leq 1\}}{n}
$$

```python
import numpy as np
rng = np.random.default_rng(42)

# Monte Carlo 估計 pi
n = 2_000_000
x, y = rng.random(n), rng.random(n)
pi_hat = 4 * np.mean(x**2 + y**2 <= 1)
print(f"pi ≈ {pi_hat:.5f}（誤差 {abs(pi_hat - np.pi):.5f}）")

# Monte Carlo 估計積分 ∫₀¹ e^{-x²} dx
xs = rng.random(1_000_000)
integral = np.mean(np.exp(-xs**2))
print(f"∫₀¹ e^(-x²) dx ≈ {integral:.5f}（理論值 {np.pi**0.5/2 * (1 - __import__('math').erf(1)):.5f}）")
```

### Metropolis 演算法（1953，MCMC 的先驅）
Metropolis、Rosenbluth 夫婦、Teller 夫婦（1953）將 Monte Carlo 推廣到**非均勻分佈**的取樣：構造 Markov 鏈，使其平穩分佈為目標分佈 $\pi(x)$。提出接受機率
$$
A(x \to x') = \min\left(1, \frac{\pi(x')}{\pi(x)}\right)
$$
（對稱建議分佈下），鏈長期收斂到 $\pi$。1970 年 Hastings 推廣為 **Metropolis–Hastings 演算法**，$A = \min\!\left(1, \frac{\pi(x')q(x'|x)}{\pi(x)q(x|x')}\right)$，成為現代 MCMC（如 Gibbs sampling、HMC、Stan 與貝葉斯統計軟體）的基石。

### 命名典故
Metropolis 以親戚常去賭博的**摩納哥 Monte Carlo 賭場**命名——方法的核心就是「用賭場式的隨機性換取確定性的答案」。此名稱最初是 Los Alamos 的密碼代號。

## 結案 -- 後果與影響
- 中子擴散、核武與反應堆設計成功以 Monte Carlo 求解，奠定計算物理學。
- 滲透到計算金融（選擇權定價）、計算生物、電腦圖學（路徑追蹤）、貝葉斯統計（MCMC）。
- 「維度無關的 $O(n^{-1/2})$ 誤差」使其成為高維問題的預設解法。
- Ulam 的「用重複隨機試驗取代解析計算」思想，是計算科學時代的方法論宣言。

## 關鍵人物與文獻
- **Stanislaw Ulam**（1909–1984）：紙牌接龍的頓悟者，方法發明人。
- **John von Neumann**（1903–1957）：將想法形式化並規劃 ENIAC 實作。
- **Nicholas Metropolis**（1915–1999）：命名者，1953 年演算法第一作者。
- **Metropolis, N. & Ulam, S. (1949), "The Monte Carlo Method", JASA 44.**
- **Metropolis et al. (1953), "Equation of State Calculations by Fast Computing Machines", J. Chem. Phys. 21.**
- Buffon（1777）：丟針問題，Monte Carlo 估 $\pi$ 的手算先聲。
