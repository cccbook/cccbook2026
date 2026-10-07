# 1777 - Buffon 擲針實驗

## 案件摘要
1777 年，法國博物學家 Buffon 提出一個驚人的問題：在劃滿等距平行線的地板上隨機丟一根針，針壓到線的機率是多少？他不只算出答案，還發現**可以反過來用擲針的統計數據估計 π**——這是人類史上第一個用「隨機實驗」計算確定常數的方法，是蒙地卡羅方法的兩百年前預言。

## 前因 -- 為什麼會有這個案子
18 世紀的機率論只處理「骰子、紙牌」這類離散賭局（Pascal–Fermat，1654）。Buffon 問的是一個**連續**問題：針的位置與角度是連續隨機變數。這迫使機率論從「數出有利情況」升級為「在幾何空間中測量長度/面積」——**幾何機率**就此誕生。

## 線索與推理 -- 數學式、程式、理論

### 擲針問題的解答
設平行線間距為 $d$，針長 $l \le d$。針的位置由兩個隨機變數決定：

- $x$：針中點到最近一條線的距離，$x \sim \mathrm{Uniform}(0, d/2)$
- $\theta$：針與線的夾角，$\theta \sim \mathrm{Uniform}(0, \pi)$

針壓到線的條件是針的投影超過 $x$：

$$x \le \frac{l}{2} \sin\theta$$

在 $(\theta, x)$ 平面上，這是一塊面積對總面積的比值：

$$P = \frac{\displaystyle\int_0^\pi \frac{l}{2}\sin\theta \, d\theta}{\displaystyle \pi \cdot \frac{d}{2}} = \frac{l}{\pi d} \cdot [-\cos\theta]_0^\pi \cdot 1 = \frac{2l}{\pi d}$$

**注意這個結果**：機率裡出現了 $\pi$——一個來自圓的常數，竟從直線與直線的交錯中冒出來。

### 反向推論：用擲針估計 π
把公式倒過來：

$$\pi = \frac{2l}{d \cdot P} \approx \frac{2l \cdot N}{d \cdot H}$$

其中 $N$ 是總投擲次數，$H$ 是壓線次數。這是**第一次有人用隨機樣本估計一個數學常數**——蒙地卡羅方法的完整原型：定義隨機實驗 → 統計頻率 → 換算成目標量。

由大數法則（Bernoulli，1713），當 $N \to \infty$，$H/N \to P$，估計值收斂到 $\pi$。誤差為 $O(1/\sqrt{N})$（由中央極限定理）。

### 程式碼：Python 模擬 Buffon 擲針

```python
import random, math

def buffon_needle(n=1000000, l=1.0, d=2.0):
    hits = 0
    for _ in range(n):
        x = random.uniform(0, d/2)          # 中點到最近線的距離
        theta = random.uniform(0, math.pi)  # 針與線的夾角
        if x <= (l/2) * math.sin(theta):
            hits += 1
    return 2 * l * n / (d * hits)

random.seed(42)
print(buffon_needle())      # 約 3.14x
# N = 10^6 時誤差約 0.1%：誤差 ~ 1/sqrt(N)，要多一位精度需 100 倍樣本
```

### 變體：Lazzarini 的可疑紀錄
1901 年，義大利數學家 Lazzarini 宣稱擲針 3408 次得到 $\pi \approx 355/113$（精確到 6 位）。偵探檢查：3408 = 16 × 213，恰好使分數成立——這幾乎不可能只是巧合。**這可能是史上第一起「隨機實驗造假案」**：他很可能中途停手（選擇性停止），違反了大數法則要求的固定 $N$。

**偵探筆記**：選擇性停止會使頻率產生偏差——這個教訓在兩百年後的蒙地卡羅模擬中依然是頭號陷阱（「跑到我滿意為止」會污染統計）。

## 結案 -- 後果與影響
- **幾何機率誕生**：連續隨機變數進入機率論，催生 Bertrand 悖論（1889）與公理化機率（Kolmogorov，1933，見 `../機率統計/`）。
- **蒙地卡羅方法的原型**：Ulam (1946) 發明蒙地卡羅時，Buffon 擲針正是教科書裡的第一個例子。
- **反向問題的思想**：「從隨機樣本反推確定答案」成為整個隨機算法學科的靈魂——從估計 π 到估計體積、基數、集合相似度。
- **重要性取樣的前身**：Buffon 的「在幾何空間中測度」思想，後來發展成重要性取樣與 MCMC。

## 關鍵人物與文獻
- **Georges-Louis Leclerc, Comte de Buffon**（1707–1788）：Essai d'arithmétique morale (1777)
- **Lazzarini**：Un'applicazione del calcolo della probabilità (1901)——可疑的紀錄
- 交叉參照：`1946-Ulam蒙地卡羅.md`、`../機率統計/README.md`
