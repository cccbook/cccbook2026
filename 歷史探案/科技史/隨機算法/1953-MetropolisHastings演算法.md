# 1953 - Metropolis–Hastings 演算法

## 案件摘要
1953 年，Metropolis、Rosenbluth 夫婦、Teller 夫婦（Ulam 也有貢獻）在 Los Alamos 發表《Equation of State Calculations by Fast Computing Machines》：要從一個無法直接取樣的機率分佈 $\pi(x)$ 中抽樣，就設計一條**隨機漫步**，其平穩分佈恰好是 $\pi$。這是 Markov Chain Monte Carlo（MCMC）的誕生——後來 Hastings (1970) 一般化它，成為整個貝葉斯統計與計算物理的引擎。

## 前因 -- 為什麼會有這個案子
統計力學的核心需求：給定能量函數 $E(x)$（$x$ 是 $10^{23}$ 個粒子的組態），要計算配分函數與各種期望值：

$$Z = \sum_x e^{-E(x)/kT}, \qquad \langle f \rangle = \frac{1}{Z}\sum_x f(x) e^{-E(x)/kT}$$

狀態空間天文數字般巨大，逐項求和不可能；均勻取樣又沒用（高能組態才重要，但機率極小）。**必須按重要性取樣**：多在 $e^{-E/kT}$ 大的區域抽樣。Metropolis 的靈感：讓電腦「 biased 地隨機漫步」——往能量低處走總是接受，往高處走偶爾接受。

## 線索與推理 -- 數學式、程式、理論

### Metropolis 演算法
目標分佈 $\pi(x) \propto e^{-E(x)/kT}$（只需知道到常數倍比例！）。從當前狀態 $x$：

1. 提議新狀態 $x'$（對稱提議：$q(x'|x) = q(x|x')$）
2. 計算接受機率

$$A(x \to x') = \min\left(1, \frac{\pi(x')}{\pi(x)}\right) = \min\left(1, e^{-(E(x')-E(x))/kT}\right)$$

3. 以機率 $A$ 移動到 $x'$，否則留在 $x$

**神來之筆**：$\pi$ 的歸一化常數 $Z$ 在比值中**抵消了**——不用算 $Z$！這解開了統計力學的死結（$Z$ 本身就是最難算的量）。

### 為什麼平穩分佈是 π：細緻平衡
鏈的轉移機率 $P(x \to x') = q(x'|x) A(x \to x')$ 滿足**細緻平衡**（detailed balance）：

$$\pi(x) P(x \to x') = \pi(x') P(x' \to x)$$

驗證：$\pi(x) q(x'|x) \min(1, \pi(x')/\pi(x)) = \min(\pi(x)q(x'|x), \pi(x')q(x'|x))$，對稱成立。$\blacksquare$

由馬可夫鏈理論：若鏈不可約且非週期，細緻平衡 $\implies$ $\pi$ 是平穩分佈 $\implies$ 分佈收斂到 $\pi$。**於是長期漫步的統計就是目標分佈**。

### Hastings 一般化 (1970)
Hastings 放寬對稱提議的限制，接受機率改為：

$$A(x \to x') = \min\left(1, \frac{\pi(x') q(x|x')}{\pi(x) q(x'|x)}\right)$$

細緻平衡依然成立。這讓任意提議分佈都可用（如向高機率區傾斜的提議），大大加速收斂。

### 程式碼：Metropolis 取樣

```python
import random, math

def metropolis(E, x0, proposal, n=100000, T=1.0):
    """E: 能量函數；proposal: 對稱提議 x -> x'"""
    x, samples, accepted = x0, [], 0
    for _ in range(n):
        x2 = proposal(x)
        # 接受機率 min(1, exp(-(E(x')-E(x))/T))
        if random.random() < math.exp(min(0, (E(x) - E(x2)) / T)):
            x = x2
            accepted += 1
        samples.append(x)
    return samples, accepted / n

random.seed(42)
# 例：從標準常態分佈取樣（E(x) = x^2/2）
samples, rate = metropolis(lambda x: x*x/2, 0.0,
                           lambda x: x + random.uniform(-2, 2))
mean = sum(samples[10000:]) / len(samples[10000:])
var  = sum(x*x for x in samples[10000:]) / len(samples[10000:]) - mean**2
print(f"mean={mean:.3f} var={var:.3f} 接受率={rate:.2f}")
# mean≈0 var≈1：成功取樣 N(0,1)，儘管從未計算歸一化常數
```

### 二維 Ising 模型
磁性系統：格點上自旋 $\sigma_i = \pm 1$，能量 $E = -J\sum_{\langle i,j\rangle} \sigma_i\sigma_j$。Metropolis 步驟：隨機翻轉一個自旋，若 $\Delta E \le 0$ 接受，否則以 $e^{-\Delta E/kT}$ 機率接受。模擬顯示相變：低溫磁化、高溫失磁——**統計力學最深刻的現象，用擲骰子看見**。

**偵探筆記**：整個方法的推理鏈是「逆向工程」——先確定想要的平穩分佈 $\pi$，反推轉移規則使其滿足細緻平衡。**設計收斂到目標的隨機過程**，這個模式後來出現在 PageRank、2-SAT 隨機算法、混合時間理論中。

## 結案 -- 後果與影響
- **計算物理**：Ising 模型、量子蒙地卡羅、格點 QCD——統計力學全面數值化。
- **貝葉斯統計革命**（1980s–90s）：後驗分佈 $p(\theta|D) \propto p(D|\theta)p(\theta)$ 無法解析時，MCMC 是唯一工具。BUGS、Stan 等軟體把它變成統計學標配。
- **混合時間理論**：鏈多久收斂？這個問題催生了 Markov 鏈混合時間的豐富理論（耦合、譜隙、收縮），並與 PSPACE 算法（1991, Dyer–Frieze–Kannan 體積估計）連結。
- **Hastings 一般化**：Gibbs 取樣（Geman–Geman, 1984）、Slice 取樣、HMC（Hamiltonian Monte Carlo，現代貝葉斯深度學習的引擎）都是其後代。
- 交叉參照：`1905-布朗運動.md`、`1946-Ulam蒙地卡羅.md`、`1985-Yao計算隨機性.md`

## 關鍵人物與文獻
- **Nicholas Metropolis**（1915–1999）：Los Alamos、命名蒙地卡羅
- **Arianna & Marshall Rosenbluth、Edward & Mici Teller**：共同作者
- **Wilfred Keith Hastings**（1930–2024）：Biometrika (1970) 一般化
- Metropolis et al.: Equation of State Calculations by Fast Computing Machines (1953, J. Chem. Phys.)
- 交叉參照：`1946-Ulam蒙地卡羅.md`、`1953-MetropolisHastings演算法.md`
