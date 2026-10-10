# 1908 年六行神探：Langevin 方程閃電破案

> Einstein 用了十幾頁推導擴散，Langevin 只用了六行。1908 年春天，法國物理學家 Paul Langevin 在課堂上即興寫下一條牛頓方程，加了一個看不見的噪聲，全場譁然。這是歷史上第一條隨機微分方程。

| 欄位 | 內容 |
|------|------|
| 發生時間 | 1908 年，論文 Sur la théorie du mouvement brownien 僅六頁，核心推導只六行 |
| 地點 | 巴黎法蘭西學院，Langevin 講授布朗運動的課堂與 Comptes Rendus 期刊 |
| 報案人 | Paul Langevin（1872–1946），Curie 的學生，社會主義者，物理教學名家 |
| 偵探 | Langevin 本人；後續 Ornstein 與 Uhlenbeck（1930）補上速度相關完整解 |
| 兇器 | 阻尼加噪聲 $m \\dot v = -\\gamma v + \\xi$ ，白噪聲 $\\xi$ 均值零，強度由溫度鎖定 |
| 結論 | 六行還原 Einstein 均方位移，OU 過程雛形誕生，漲落–耗散的另一條大道打通 |

## 案發現場

1908 年的巴黎物理學界，Einstein 的擴散理論已經發表三年，但許多人覺得它太統計、太迂迴。

Einstein 的路線是：先猜位移分佈，再展成擴散方程，再解高斯，再算均方位移。邏輯無懈可擊，物理圖像卻隔了一層：粒子到底每一秒受到什麼力。

Langevin 想把牛頓請回現場。他的直覺是：布朗粒子每一瞬間都受兩種力。一是黏滯阻力，與速度反向，正比於 $\\gamma v$ 。二是水分子的瘋狂撞擊，時正時負，平均為零，記為 $\\xi(t)$ 。

案發現場於是有了一條看似胡鬧的牛頓方程。胡鬧之處在於， $\\xi(t)$ 每一刻都是隨機的，方程的解不再是一條軌跡，而是一束軌跡。牛頓的決定論在此分叉了。

但 Langevin 說，決定論分叉，平均值不分叉。只要對噪聲取平均，軌跡束的統計量依然服從乾淨的微分方程。這一念之轉，就是隨機微分方程的誕生。

## 偵查過程

Langevin 的六行推導是科學史上最短的破案之一。本節完整重現，並補上現代符號的註解。

### 六行推導

設粒子質量為 $m$ ，速度為 $v$ ，位置為 $x$ 。方程為

$$
m \\dot v = -\\gamma v + \\xi
$$

其中 $\\xi(t)$ 為白噪聲，滿足 $E[\\xi] = 0$ 且與位置無關。這是 OU 過程的速度版雛形。

推導開始。方程兩邊同乘 $x$ ，再取系綜平均。利用 $x \\dot v = d(xv)/dt - v^2$ ，可得

$$
m dE[xv]/dt - m E[v^2] = -\\gamma E[xv] + E[x \\xi]
$$

Langevin 論證交叉項 $E[x \\xi] = 0$ ，因為撞擊方向與當前位置無關，正負抵消。又由能量均分，$m E[v^2] = kT$ ，其中 $k$ 為波茲曼常數， $T$ 為溫度。

於是 $y = E[xv]$ 滿足一階線性方程

$$
m \\dot y + \\gamma y - kT = 0
$$

解得 $y(t)$ 指數趨向 $kT / \\gamma$ 。注意到 $y = E[xv] = (1/2) dE[x^2]/dt$ ，積分一次即得長期行為

$$
E[x^2] \\approx 2 (kT / \\gamma) t
$$

與 Einstein 的 $E[x^2] = 2 D t$ 對照，立刻讀出 $D = kT / \\gamma$ 。若代入 Stokes 阻力 $\\gamma = 6 \\pi \\eta a$ ，則與 Stokes–Einstein 關係完全一致。六行，收網。

| 步驟 | 操作 | 物理意義 |
|------|------|----------|
| 第一步 | 寫下 $m \\dot v = -\\gamma v + \\xi$ | 牛頓方程加噪聲，阻尼與漲落並列 |
| 第二步 | 同乘 $x$ 再取平均 | 從隨機軌跡轉向統計矩，消滅噪聲細節 |
| 第三步 | 用 $E[x \\xi] = 0$ 化簡 | 撞擊與位置不相關，正負抵消 |
| 第四步 | 代入均分 $m E[v^2] = kT$ | 熱平衡鎖定動能，溫度入場 |
| 第五步 | 解 $y = E[xv]$ 的弛豫方程 | 短期指數過渡，長期趨於常數 |
| 第六步 | 積分得 $E[x^2] \\approx 2 D t$ | 還原 Einstein 預言，讀出 $D$ |

### OU 過程的雛形

Langevin 只算了位置的均方位移，沒有解出速度的完整相關函數。1930 年 Ornstein 與 Uhlenbeck 補上了這一塊。

速度方程的解為指數加權的噪聲積分，速度自相關呈指數衰減

$$
E[v(t) v(s)] = (kT / m) \\exp(-\\gamma \\lvert t - s \\rvert / m)
$$

特徵時間為 $m / \\gamma$ ，即布朗粒子的動量記憶時間。遠大於此時間看位置，得到擴散。遠小於此時間看速度，看到彈道。這一座橋，連接了牛頓與 Einstein。

今日所謂 Ornstein–Uhlenbeck 過程，正是速度版 Langevin 方程的數學化身，也是利率 Vasicek 模型、神經元漏電積分模型的共同祖先。

## 結案報告

Langevin 方程的歷史判決有三條。

第一，它證明 Einstein 是對的，而且是從另一條路證明的。擴散路線走系綜分佈，Langevin 路線走單粒子受力，兩者在 $D = kT / \\gamma$ 會合。兩條獨立口供指向同一兇手，案子就鐵了。

第二，它發明了隨機微分方程的寫法。把確定性漂移 $-\\gamma v$ 與隨機驅動 $\\xi$ 並列，後來成了所有 SDE 的模板：漂移項加擴散項，$dx = a dt + b dW$ 。Itô 積分就是要讓這個寫法嚴格化。

第三，它埋下了漲落–耗散定理。阻尼 $\\gamma$ 越大，運動越遲鈍，但噪聲也必須越強，否則能量均分被破壞。耗散與漲落被溫度 $T$ 鎖死，這個思想在 1950 年代開花為 Callen–Welton 定理，在金融裡開花為風險與波動的對偶。

Langevin 本人沒有追成嚴格化。他是物理學家，覺得平均操作天經地義。數學家看了直搖頭： $\\xi(t)$ 到底是什麼函數。這個問題留給 Wiener 與 Itô，留給 1923 年與 1942 年的後續檔案。

探案格言：最短的路往往最難找。Einstein 繞了遠路，Langevin 走了捷徑，但捷徑需要更大的勇氣，因為它假裝噪聲可以直接寫進牛頓方程。

## 證據與工具

| 證物 | 數學形式 | 偵查意義 |
|------|----------|----------|
| Langevin 方程 | $m \\dot v = -\\gamma v + \\xi$ | 第一條 SDE，阻尼加白噪聲 |
| 交叉項消失 | $E[x \\xi] = 0$ | 位置與瞬時撞擊不相關，推導鑰匙 |
| 能量均分 | $m E[v^2] = kT$ | 熱平衡約束，引入溫度 |
| 均方位移 | $E[x^2] \\approx 2 D t$ | 長期擴散，與 Einstein 會合 |
| 速度相關 | $E[v(t)v(s)] \\propto \\exp(-\\gamma \\lvert t-s \\rvert / m)$ | OU 雛形，動量記憶時間 $m / \\gamma$ |
| Stokes 對應 | $\\gamma = 6 \\pi \\eta a$ | 還原 $D = kT / 6 \\pi \\eta a$ |

辦案備註：數值實驗可用 Euler–Maruyama 離散 Langevin 方程，統計平穩速度變異數應為 $kT / m$ ，位置均方位移斜率應為 $2 D$ 。對應程式見 _code 目錄中 1908 年 Langevin OU 程式，內含指數相關與 $\\sigma^2 / 2 \\theta$ 平穩變異數驗證。

## 補充：程式實作

### 對應程式

[1908-langevin_ou.py](_code/1908-langevin_ou.py)

### 理論呼應

本文起點為 Langevin 方程 $m \\dot v = -\\gamma v + \\xi$ ，阻尼與白噪聲並列。
長期位置均方位移滿足 $E[x^2] \\approx 2 D t$ ，與 Einstein 預言會合於 $D = kT / \\gamma$ 。
速度自相關呈指數衰減，記憶時間為 $m / \\gamma$ ，平穩速度變異數為 $kT / m$ 。
程式以精確離散驗證平穩變異數為 $\\sigma^2 / 2 \\theta$ ，正是漲落與耗散被溫度鎖死的體現。

### 執行方式

`python3 _code/1908-langevin_ou.py`

### 實測輸出

```text
OU theta=1.5 sigma=0.8 dt=0.01 N=300000 burn=20000
target_var=0.213333 sample_var=0.204652 rel_err=0.040692 (tol 0.05)
sample_mean=0.009298 (tol |mean|<0.03)
VERIFY 1908-langevin_ou PASS var=0.2047 target=0.2133 mean=0.00930
```

### 讀者實驗

試將 $\\sigma$ 由 $0.8$ 改為 $1.0$ ，觀察平穩變異數是否約按平方比放大。

完整程式如下：

```python
# 對應 wiki：1908 年 Langevin 方程 / Ornstein-Uhlenbeck 過程（漲落-耗散）
# 說明：OU dX = -theta*X*dt + sigma*dW，theta=1.5, sigma=0.8；
# 採精確離散 X_{n+1} = e^{-theta dt} X_n + sqrt(sigma^2/(2theta)(1-e^{-2theta dt})) Z；
# 平穩變異數 sigma^2/(2theta)，均值 0。驗證變異數誤差 < 5% 且均值 ~= 0。
# 僅用 numpy，固定種子，不畫圖只印數字。
import numpy as np

SEED = 1908
THETA = 1.5
SIGMA = 0.8
DT = 0.01
N = 300_000
BURN = 20_000

rng = np.random.default_rng(SEED)
a = float(np.exp(-THETA * DT))
target_var = SIGMA ** 2 / (2.0 * THETA)
step_var = target_var * (1.0 - float(np.exp(-2.0 * THETA * DT)))
step_sd = float(np.sqrt(step_var))

Z = rng.standard_normal(N)
x = np.empty(N, dtype=np.float64)
v = 0.0
for n in range(N):
    v = a * v + step_sd * float(Z[n])
    x[n] = v

seg = x[BURN:]
m = float(seg.mean())
vhat = float(seg.var(ddof=0))
rel_err = abs(vhat - target_var) / target_var

print(f"OU theta={THETA} sigma={SIGMA} dt={DT} N={N} burn={BURN}")
print(f"target_var={target_var:.6f} sample_var={vhat:.6f} rel_err={rel_err:.6f} (tol 0.05)")
print(f"sample_mean={m:.6f} (tol |mean|<0.03)")

assert rel_err < 0.05, f"OU var rel_err {rel_err} >= 5%"
assert abs(m) < 0.03, f"OU mean {m} not ~= 0"
print(f"VERIFY 1908-langevin_ou PASS var={vhat:.4f} target={target_var:.4f} mean={m:.5f}")
```
