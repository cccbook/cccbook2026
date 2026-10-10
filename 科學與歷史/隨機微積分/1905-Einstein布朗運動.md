# 1905 年奇蹟年第四案：Einstein 布朗運動證明

> 伯恩專利局三等技師，一年連破四案。第四案沒有屍體，沒有血跡，只有一張紙：他說，看不見的原子可以用看得見的均方位移稱出來。這是原子論的數學逮捕令。

| 欄位 | 內容 |
|------|------|
| 發生時間 | 1905 年 5 月 11 日投稿，7 月刊於 Annalen der Physik，奇蹟年第四篇論文 |
| 地點 | 瑞士伯恩專利局辦公桌；思想實驗室橫跨熱力學、流體力學與統計力學 |
| 報案人 | Albert Einstein（1879–1955），時年二十六歲，專利局技師兼物理學游擊隊員 |
| 偵探 | Einstein 本人；理論驗證者為 Smoluchowski、Langevin；實驗收網者為 Perrin |
| 兇器 | 擴散係數 $D = kT / 6 \\pi \\eta a$ ，均方位移 $E[x^2] = 2 D t$ ，Stokes–Einstein 關係 |
| 結論 | 布朗運動定量可測，原子實在可證，唯能論退場倒數開始，Perrin 實驗終將收網 |

## 案發現場

1905 年的物理學有兩大陰影：原子是否存在，以太是否存在。

Ostwald 與 Mach 率領的唯能論陣營說，原子只是計算工具，不必當真。能測到的只有能量與現象，談什麼看不見的小球。Boltzmann 為原子論奮戰多年，身心俱疲，1906 年自殺，學界風聲鶴唳。

案發現場的三件遺物是這樣的。

第一件是 Brown 的舊檔案。1827 年的花粉之舞，現象清楚，成因空白，六十年無人能定量。

第二件是 Bachelier 的冷檔案。1900 年股市裡的布朗運動，數學已備，物理學家沒讀過。Einstein 後來說自己完全不知道 Bachelier，兩人獨立破案。

第三件是 Sutherland 的平行腳印。澳洲物理學家 Sutherland 幾乎同時導出分子質量與擴散的關係，但發表在澳洲期刊，影響有限。歷史只記得伯恩的那支筆。

Einstein 的處境是：沒有實驗室，沒有學生，沒有經費，只有一張專利局的桌子與晚上熬夜的時間。但他有統計力學，而統計力學正是本案的指紋粉。

## 偵查過程

Einstein 的推理分為四步，每一步都乾淨得像手術刀。

### 第一步：懸浮粒子的滲透壓

他把懸浮粒子看成大分子。濃度不均勻時，粒子群會產生滲透壓梯度，驅動擴散流。設數密度為 $n(x,t)$ ，溫度為 $T$ ，波茲曼常數為 $k$ ，則滲透壓為 $n k T$ 量級。

同時黏滯流體施加 Stokes 阻力。半徑 $a$ 的小球在黏滯係數 $\\eta$ 的液體中勻速運動時，阻力為 $6 \\pi \\eta a v$ ，其中 $v$ 為速度。

平衡兩者，可得擴散係數

$$
D = kT / 6 \\pi \\eta a
$$

這就是 Stokes–Einstein 關係。溫度 $T$ 提供動力，黏滯 $\\eta$ 與粒徑 $a$ 提供阻力，三者相除即為擴散能力。它把宏觀可測量 $D$ 、 $\\eta$ 、 $a$ 、 $T$ 與微觀常數 $k$ 綁在一起。

### 第二步：從隨機跳躍到擴散方程

Einstein 假設粒子在小時間 $\\tau$ 內的位移分佈為 $\\phi(\\xi)$ ，對稱且與位置無關。設 $p(x,t)$ 為時刻 $t$ 的粒子密度，則有 Chapman–Kolmogorov 式遞推

$$
p(x, t + \\tau) = \\int p(x - \\xi, t) \\phi(\\xi) d\\xi
$$

將 $p(x - \\xi, t)$ 對 $\\xi$ 展開至二階，奇次項因對稱消失，得到擴散方程

$$
\\partial_t p = D \\partial_{xx} p
$$

其中 $D$ 為跳躍變異數除以 $2 \\tau$ 。隨機漫步的微觀細節被洗掉，只剩一個宏觀參數 $D$ 。這是粗粒化的典範。

### 第三步：均方位移的預言

擴散方程初值為點源 $p(x,0) = \\delta(x)$ 時，解為高斯分佈

$$
p(x,t) = (4 \\pi D t)^{-1/2} \\exp(-x^2 / 4 D t)
$$

直接計算二階矩，得到本案最著名的證物

$$
E[x^2] = 2 D t
$$

注意這是 $t$ 的一次方，不是 $t^2$ 。若粒子做勻速直線運動，均方位移正比於 $t^2$ 。正比於 $t$ 正是隨機性的簽名：方向不斷被撞亂，走不遠，只能以平方根速度擴散。

三維情形各方向獨立疊加，均方半徑為 $6 D t$ ，二維為 $4 D t$ 。實驗者選哪個維度觀測，對照表如下。

| 觀測維度 | 均方位移預言 | 實驗對應 |
|----------|--------------|----------|
| 一維投影 $x$ | $E[x^2] = 2 D t$ | 顯微鏡單軸追蹤 |
| 二維平面 | $E[r^2] = 4 D t$ | 載玻片平面錄影 |
| 三維空間 | $E[r^2] = 6 D t$ | 懸浮液立體追蹤 |
| 擴散係數 | $D = kT / 6 \\pi \\eta a$ | 已知 $T$ 、 $\\eta$ 、 $a$ 反推 $k$ |

### 第四步：稱出原子

波茲曼常數 $k$ 與氣體常數 $R$ 、阿佛加厥常數 $N_A$ 的關係為 $k = R / N_A$ 。量出 $D$ ，即可解出 $N_A$ 。

Einstein 在論文末尾給出數量級估計：微米級粒子在水中一分鐘的均方根位移約為微米量級，顯微鏡可見。這不是哲學，是施工圖。Perrin 照圖施工，1909 年收網。

## 結案報告

1905 年論文沒有終結論戰，但把論戰變成了測量競賽。

Smoluchowski 在 1906 年獨立給出類似理論，互相印證。Langevin 在 1908 年給出更短的推導，殊途同歸。Perrin 在 1908 至 1911 年間以乳膠球測得 $N_A$ ，多路一致，唯能論崩盤。

Ostwald 在 1909 年公開承認原子存在，Mach 至死不從，但大勢已去。1913 年 Perrin 出版《原子》，1926 年獲 Nobel 獎，1926 年也是 Einstein 因光電效應獲獎後的第五年。原子從假說變成證物。

本案的歷史地位有三層。物理上，它是漲落–耗散關係的鼻祖：耗散係數 $\\eta$ 與漲落強度 $D$ 被溫度 $T$ 鎖死。數學上，它把布朗運動變成擴散方程的解，為 Wiener 構造鋪路。方法上，它示範了如何從不可見的微觀碰撞推出可見的宏觀統計，是理論物理的探案範本。

Einstein 此後很少再碰布朗運動。他留下一句話：這篇論文的價值在於讓原子無可抵賴。說完便轉身去追廣義相對論了。

## 證據與工具

| 證物 | 數學形式 | 偵查意義 |
|------|----------|----------|
| Stokes–Einstein 關係 | $D = kT / 6 \\pi \\eta a$ | 連接宏觀與微觀的橋樑，反推 $k$ 與 $N_A$ |
| 擴散方程 | $\\partial_t p = D \\partial_{xx} p$ | 微觀隨機的宏觀化身，與熱方程同構 |
| 均方位移 | $E[x^2] = 2 D t$ | 可直接測量的預言， $t$ 一次方為隨機簽名 |
| 高斯基本解 | $p = (4 \\pi D t)^{-1/2} \\exp(-x^2 / 4 D t)$ | 中央極限定理的物理現形 |
| 阿佛加厥常數 | $N_A = R / k$ | 終極獵物，多路測量互相鎖定 |

辦案備註：數值實驗可用隨機漫步模擬大量軌跡，計算均方位移對 $t$ 的斜率，還原 $D$ 。改變 $a$ 、 $\\eta$ 、 $T$ ，驗證 $D$ 的正反比關係。對應程式見 _code 目錄中 1905 年 Einstein 擴散程式，以及 1909 年 Perrin 沉降程式的擴散模組。

## 補充：程式實作

### 對應程式

[1905-einstein_diffusion.py](_code/1905-einstein_diffusion.py)

### 理論呼應

本文核心為擴散方程 $p(x,t) = (4 \pi D t)^{-1/2} \exp(-x^2 / 4 D t)$ 與均方位移 $E[x^2] = 2 D t$ 。
程式以 OU 過程逼近平穩後，取小時間差計算均方位移斜率，還原 $2 D$ 。
擴散係數滿足 $D = kT / 6 \pi \eta a$ ，溫度與黏滯分別控制漲落與耗散。
短時斜率逼近 $2 D$ 而非 $t^2$ ，正是隨機性簽名的數量驗證。

### 執行方式

`python3 _code/1905-einstein_diffusion.py`

### 實測輸出

```text
OU gamma=2.0 D=0.5 dt=0.001 N=300000 burn=50000
tau1=0.0100 MSD1=0.009833 tau2=0.0300 MSD2=0.029193
slope=0.967985 target_2D=1.000000
rel_err=0.032015 (tol 0.08)
VERIFY 1905-einstein_diffusion PASS slope=0.9680 target=1.0000 rel_err=3.2015%
```

### 讀者實驗

試將 $D$ 由 $0.5$ 改為 $1.0$ ，觀察短時斜率是否約變為兩倍。

完整程式如下：

```python
# 對應 wiki：1905 年 Einstein 擴散（MSD = 2Dt）與 Ornstein-Uhlenbeck 過程
# 說明：一維 OU dx = -gamma*x*dt + sqrt(2D)*dW，gamma=2, D=0.5；
# 平穩變異數 D/gamma；短時滯下 MSD(tau) ~= 2D*tau（Einstein 擴散）。
# 以精確離散跑至平穩，取小 tau1/tau2 的 MSD 斜率驗證 ~= 2D，誤差 < 8%。
# 僅用 numpy，固定種子，不畫圖只印數字。
import numpy as np

SEED = 1905
GAMMA = 2.0
D = 0.5
DT = 0.001
N = 300_000  # 總步數 (T=300)，夠長以達平穩並壓低 MC 誤差
BURN = 50_000  # 前段丟棄
K1 = 10  # tau1 = 0.01
K2 = 30  # tau2 = 0.03

rng = np.random.default_rng(SEED)
a = float(np.exp(-GAMMA * DT))
q = float((D / GAMMA) * (1.0 - np.exp(-2.0 * GAMMA * DT)))
s = float(np.sqrt(q))

Z = rng.standard_normal(N)
xs = np.empty(N, dtype=np.float64)
x = 0.0
for n in range(N):
    x = a * x + s * float(Z[n])
    xs[n] = x

seg = xs[BURN:]
tau1 = K1 * DT
tau2 = K2 * DT
msd1 = float(np.mean((seg[K1:] - seg[:-K1]) ** 2))
msd2 = float(np.mean((seg[K2:] - seg[:-K2]) ** 2))
slope = (msd2 - msd1) / (tau2 - tau1)
target = 2.0 * D
rel_err = abs(slope - target) / target

print(f"OU gamma={GAMMA} D={D} dt={DT} N={N} burn={BURN}")
print(f"tau1={tau1:.4f} MSD1={msd1:.6f} tau2={tau2:.4f} MSD2={msd2:.6f}")
print(f"slope={slope:.6f} target_2D={target:.6f}")
print(f"rel_err={rel_err:.6f} (tol 0.08)")

assert rel_err < 0.08, f"Einstein slope rel_err {rel_err} >= 8%"
print(f"VERIFY 1905-einstein_diffusion PASS slope={slope:.4f} target={target:.4f} rel_err={rel_err:.4%}")
```
