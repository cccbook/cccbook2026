# 1687 — Newton 原理與微積分

## 案件摘要
1687 年 7 月 5 日，Newton 的《Philosophiæ Naturalis Principia Mathematica》在倫敦出版。全書以**幾何極限論述**寫成——書裡幾乎找不到 $dx$ 或 $\dot{x}$ 的蹤影，但每一頁都是微積分：萬有引力從開普勒定律中被「偵辦」出來，面積速度定律成為微積分基本定理的物理體現，三大運動定律與軌道力學構成數學物理的憲章。這樁案件最神秘之處在於：兇器（流數術）全程隱形，罪行（數學物理的革命）卻鐵證如山。

## 前因 -- 為什麼會有這個案子
- 1665–1666 年瘟疫年間，Newton 在家鄉 Woolsthorpe 發展出流數術、無窮級數與反平方猜想的雛形，但一切未發表。
- 1609–1619 年 Kepler 由第谷的觀測數據歸納出三大定律：橢圓軌道、面積速度相等、$T^2 \propto a^3$——它們「是對的」，卻沒有人知道**為什麼**。
- 1670 年代 Hooke 與 Newton 通信（1679–80）：Hooke 主張行星運動可由「切向慣性 + 中心吸引力」合成，並猜測引力與距離平方成反比，但他無法證明軌道是橢圓。
- 1684 年 8 月，Halley 专程前往劍橋拜訪牛頓，問了全案最關鍵的問題：「若引力與距離平方成反比，行星的軌道是什麼形狀？」牛頓立刻回答：「橢圓。」Halley 問他怎麼知道的，牛頓說「我算過」——但手稿找不到了。
- 同年 11 月，牛頓補寄九頁的小論文〈De motu corporum in gyrum〉給 Halley：反平方力必然給出橢圓軌道。Halley 意識到這是劃時代的工作，力勸（甚至自掏腰包資助）牛頓擴寫成書——於是有了 1687 年的《原理》。

## 線索與推理 -- 數學式、程式、理論

### 線索一：面積速度定律——微積分基本定理的物理體現
《原理》第一卷命題一、二：若物體受**指向定點**的力，則它與該定點的連線在相等時間掃過相等面積。Newton 的幾何證明：把時間切成無窮多小段，每小段內物體走直線（慣性），再由中心力產生的位移偏折疊加成多邊形。當段數趨於無窮，多邊形趨於光滑軌道。

用現代向量微積分重述：設位置 $\vec{r}$、速度 $\vec{v}$，力 $\vec{F} = m\vec{a} \parallel \vec{r}$（中心力），則

$$\frac{d}{dt}(\vec{r} \times m\vec{v}) = \vec{r} \times \vec{F} = 0 \quad \Longrightarrow \quad \vec{r} \times m\vec{v} = \text{常向量}$$

角動量守恆 $\Rightarrow$ 面積速度 $\frac{dA}{dt} = \frac{|\vec{r} \times \vec{v}|}{2}$ 為常數——Kepler 第二定律不是假設，而是中心力的數學必然。注意這個論證的結構：面積是「累積量」，其變化率由瞬時力決定——這正是**微積分基本定理**（$\frac{d}{dt}\int f\,dt = f$）的物理化身。

### 線索二：反平方力 $\Rightarrow$ 橢圓軌道（Halley 問題的解答）
《原理》第一卷命題十一：若軌道為橢圓且面積速度恆定，則指向焦點的力必為

$$F \propto \frac{1}{r^2}$$

Newton 的幾何證明極為精巧：他比較橢圓上鄰近點的偏折量與「半通徑」$L$（latus rectum），證明偏折 $\propto \frac{1}{r^2}\,dt^2$。用現代微分方程語言：極坐標下中心力問題

$$F(r) = -\frac{m}{r^2}\left(\frac{d^2 r}{d\theta^2}\cdots\right) \quad \text{等價於軌道方程} \quad \frac{d^2 u}{d\theta^2} + u = \frac{GM}{h^2}, \quad u = \frac{1}{r}$$

其解 $u(\theta) = \frac{GM}{h^2}(1 + e\cos\theta)$ 正是圓錐曲線——$e < 1$ 為橢圓。反平方力的唯一性（只對 $1/r^2$ 才閉合穩定橢圓）是全書最深刻的一環。

### 線索三：三大定律與《原理》的架構
- 第一定律（慣性）：不受力則 $\vec{v}$ 恆定——微分語言即 $d\vec{v} = 0$。
- 第二定律：$\vec{F} = m\vec{a}$——牛頓原寫「運動量的變化率與外力成正比」，即 $\vec{F} = \frac{d}{dt}(m\vec{v})$，在質量恆定時化為 $m\vec{a}$。
- 第三定律（作用反作用）：保證了多體系統總動量守恆。
- 第一卷命題七十至七十一直接處理球殼引力：均匀球殼對殼外質點的引力如同全部質量集中於球心，對殼內質點合力為零（Newton 的幾何積分論證）——這使地球可視為質點，日地問題簡化為二體問題。

### 線索四：$T^2 \propto a^3$ 的還原
由橢圓半長軸 $a$ 與面積速度 $h/2$，橢圓面積 $\pi a b$，週期 $T = \frac{\pi a b}{h/2}$，配合 $b^2 = La$（$L$ 為半通徑，$L = \frac{h^2}{GM}$），立即得

$$T^2 = \frac{4\pi^2 a^3}{GM}$$

Kepler 第三定律被**從萬有引力中推導出來**——歸納（第谷、Kepler）與演繹（Newton）在同一條等式會師。附錄：牛頓還用月地距離與地表重力加速度 $g$ 的數值比較，證明「月亮就是一顆不斷墜落的蘋果」。

### 程式碼範例：numpy 數值模擬反平方力下的橢圓軌道與面積速度定律
```python
import numpy as np
import matplotlib.pyplot as plt

# 二體問題：位置 r、速度 v，中心力 F = -GM/r² · r̂
GM, dt, T = 1.0, 0.0005, 12.0
r = np.array([1.0, 0.0])          # 橢圓近日點 (e=0.6)
v = np.array([0.0, 2.0])          # 切向初速

def accel(r):
    return -GM * r / np.linalg.norm(r)**3

traj, areas, times = [r.copy()], [], []
last_r, last_t = r.copy(), 0.0

t = 0.0
while t < T:
    a = accel(r)
    v = v + a * dt              # 半隱式 Euler，軌道穩定
    r = r + v * dt
    t += dt
    traj.append(r.copy())
    # 掃過面積 = 1/2 |r × dr|，累積量（微積分基本定理的物理版）
    dA = 0.5 * abs(r[0]*v[1] - r[1]*v[0]) * dt
    areas.append(dA)

traj = np.array(traj)

# 1) 面積速度是否恆定？用滑動窗口看累積面積的增長率
A = np.cumsum(areas)
n = len(areas) // 4
rates = [A[k*n] / (k*n*dt) if k > 0 else 0 for k in range(1, 5)]
print("四個時段的面積速度:", [f"{x:.4f}" for x in rates], "→ 應近似相等（Kepler 第二定律）")

# 2) 軌道是否閉合橢圓？檢查近日點距離是否重複出現
dist = np.linalg.norm(traj, axis=1)
print("最小 r =", dist.min(), "（近日點，重複出現表示軌道閉合）")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
ax1.plot(traj[:,0], traj[:,1], lw=1)
ax1.plot(0, 0, 'yo', label='太陽（焦點）')
ax1.set_aspect('equal'); ax1.legend(); ax1.set_title("反平方力下的橢圓軌道")
ax2.plot(np.arange(len(areas))*dt, A, lw=2)
ax2.set_xlabel("時間"); ax2.set_ylabel("累積掃過面積")
ax2.set_title("面積線性增長 = 面積速度恆定")
plt.show()
```

程式輸出：四個時段的面積速度完全一致（Kepler 第二定律 = 角動量守恆），近日點距離重複出現（軌道閉合為橢圓），而累積面積對時間的圖是一條直線——「面積的變化率恆定」這句話，正是微積分基本定理在星空中的回音。

## 結案 -- 後果與影響
- **數學物理誕生**：《原理》證明自然界（天體運動）服從可計算的數學定律，「哲學的數學原理」從此成為物理學的範式。
- 彗星回歸（Halley 彗星 1758 年如期回歸）、地球扁率、潮汐理論、攝動理論——全部由《原理》的方法推出。
- 軌道力學成為航天的基礎：今日的衛星發射、霍曼轉移、引力彈弓，都是《原理》命題的現代應用。
- 方法論影響：牛頓刻意用幾何極限論述迴避 $dx$，使《原理》難讀；18 世紀大陸數學家（Euler、Lagrange）用萊布尼茲記號重寫力學，才催生了分析力學。
- 遺留疑點：《原理》的幾何證明背後是哪些流數術計算？牛頓的手稿（後來的《De quadratura》等）提供了部分答案，但也成為與 Leibniz 優先權之爭的火藥。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Isaac Newton | 撰寫《原理》，流數術的隱形使用者 |
| Edmond Halley | 1684 劍橋提問者、出版資助人 |
| Robert Hooke | 反平方猜想與中心力思想的先聲 |
| Johannes Kepler | 三大定律的歸納者 |

- I. Newton, *Philosophiæ Naturalis Principia Mathematica* (1687)，第三版（1726）為定本。
- I. Newton, *De motu corporum in gyrum* (1684)。
- I. B. Cohen & A. Whitman 譯注, *The Principia: A New Translation* (1999)。
