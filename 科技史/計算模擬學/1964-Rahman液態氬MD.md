# 1964：Rahman 液態氬 MD — 重演一杯液體

> 副標題：864 個氬原子的舞蹈，跳給中子散射看。

## 案發現場

1964 年，阿貢的 Rahman 接下一樁硬案。
Alder 用硬球證了相變，但真液體是連續軟勢。
氬最單純：單原子球對稱，交互接近理想。
中子散射剛能測液體動力學，理論卻跟不上。
流體力學只懂黏度，統計力學只會算平衡分佈。
沒人能預言原子如何擴散、如何被鄰居彈回。
關鍵證人是 Lennard-Jones 對勢，短程排斥長程吸引。
代入牛頓方程， $N$ 體軌跡解析求解無望。
Rahman 的賭注：讓 864 個氬原子按牛頓定律跑。
速度自相關對上實驗，連續勢 MD 即成立。

## 偵查過程

### 線索一：LJ 勢的指紋

LJ 勢僅兩參數：阱深 $\epsilon$ 與直徑 $\sigma$ 。
行內記為 $4\epsilon[(\sigma/r)^{12}-(\sigma/r)^6]$ 的函數。
其中 $r$ 為對距離， $\epsilon$ 為阱深， $\sigma$ 為零點距離。
12 次方模擬泡利排斥，陡峭堅硬。
6 次方模擬色散吸引，溫柔長程。
氬參數由維里係數與晶體數據標定。
截斷取約 $2.5\sigma$ ，尾部解析修正補回能量壓強。
週期邊界消表面效應，最小鏡像處理交互。
### 線索二：864 粒子的牛頓劇場

盒中裝 864 粒子，約為面心立方倍數。
初速按目標溫度抽取，扣除質心漂移。
步長約皮秒百分之一，逐對算力，複雜度正比 $N^2$ 。
先熔化晶格達液態，平衡後微正則生產。
能量守恆被嚴密監控，漂移超標即判步長太大。
生產軌跡數十皮秒，足以看清擴散全程。
### 線索三：速度自相關對質實驗

速度自相關記為 $Z$ ，初值為一，碰撞後迅速衰減。
液體中跌入負值再回彈，即籠效應指紋。
原子撞上鄰居籠子被彈回，負谷就是鐵證。
擴散係數由 $Z$ 積分得到，與示蹤實驗兩成內吻合。
van Hove 函數直接對上中子散射譜。
| 觀測量 | 模擬趨勢 | 實驗對照 |
|--------|----------|----------|
| 擴散係數 | 隨溫度升增 | 示蹤法吻合 |
| 自相關 | 出現負谷 | 籠效應證實 |
| 徑向分佈 | 第一峰尖銳 | X 光衍射吻合 |
LJ 對勢獨立公式如下，為本案兇器。
$$ V(r) = 4\epsilon[(\sigma/r)^{12}-(\sigma/r)^6] $$
其中 $\epsilon$ 為阱深， $\sigma$ 為尺度， $r$ 為對距離。
牛頓方程獨立公式如下，為劇場劇本。
$$ m\ddot r_i = -\sum_{j \ne i} \nabla V(r_{ij}) $$
其中 $m$ 為質量， $r_i$ 為第 $i$ 原子座標。

## 結案報告

1964 年第一個逼真液體 MD 完成，氬的擴散由牛頓定律算出。
連續勢 MD 可行，統計力學從此有了動力學之眼。
後續是 1967 年 Verlet 積分，步長更大更穩。
1977 年蛋白模擬、1985 年從頭算皆此血脈延續。
864 成了時代標誌，今天動輒百萬原子。
結語：真實液體可在電腦裡倒出來，只是很小一杯。

## 證據與工具

LJ 約化單位表是重現必備工具。
| 量綱 | 約化方式 | 氬實例 |
|------|----------|--------|
| 長度 | 以 $\sigma$ 為單位 | 約 3.4 埃 |
| 能量 | 以 $\epsilon$ 為單位 | 約 120 克耳文 |
| 時間 | 以 $\sqrt{m\sigma^2/\epsilon}$ 為單位 | 約皮秒量級 |
重現： $N = 108$ ，密度 0.85 ，溫度 0.7 ，皆約化單位。
截斷 $2.5\sigma$ 加尾修正，速度 Verlet 步長 0.005 。
算 $Z$ 曲線與均方位移，驗證負谷與擴散段。
畫徑向分佈，對照第一峰與第二劈裂。
因果鏈：Alder 1957 年硬球開案，本案升級為連續軟勢。
Verlet 1967 年改進積分器，能量守恆更穩步長更大。
本案檔案編號 LJ-1964 ，狀態已結案，液體仍在流動。
864 粒子是時代標誌，今天動輒百萬原子起跳。
均方位移斜率除以六，即得擴散係數估計。

## 補充：程式實作

八百多顆氬跑不動沒關係，本探先押六十四顆上庭作證也一樣定罪。

### 對應程式

[1964-lennard_jones_md.py](_code/1964-lennard_jones_md.py)

### 理論呼應

本文核心是連續軟勢取代硬球，粒子服從牛頓方程，受力來自 $V(r)$ 的梯度。

程式以速度 Verlet 在約化單位下推進，截斷取 $2.5\sigma$ 並做能量平移修正。

週期邊界加最小鏡像消除表面效應，正是 Rahman 當年盒子的縮影。

能量守恆與徑向分佈第一峰，就是呈給中子散射看的兩張指紋卡。

### 執行方式

```bash
python3 _code/1964-lennard_jones_md.py
```

### 實測輸出

```text
E0=2.4413, E1=2.4467, drift=0.2179% (驗證 <2%: PASS)
RDF 第一峰 r=1.025σ (驗證約 1.1: PASS)
VERIFY: drift=0.002179, r_peak=1.025000
ALL CHECKS PASS
```

關鍵數字有二：兩千步總能量漂移僅 $0.2179$ 百分比，通過 $2$ 百分比門檻。

徑向分佈第一峰落在 $1.025\sigma$ ，正中 Lennard-Jones 近鄰殼層靶心。

能量不漂、峰位不偏，液體結構證詞成立，籠效應便有據可查。

### 讀者實驗

把溫度定標從 $1.0$ 改為 $0.7$ 或 $2.0$ ，或把截斷 $RC$ 從 2.5 改為 3.5 ，觀察能量漂移與第一峰高低變化。

完整程式如下：

```python
# -*- coding: utf-8 -*-
"""1964 二維 Lennard-Jones 分子動力學 (對應 wiki: 計算模擬學 / 平衡態 MD)
只用 numpy,固定種子。N=64,Verlet(NVE)跑 2000 步。
驗證:總能量漂移 < 2% 且徑向分佈第一峰約在 r≈1.1σ。
"""
import numpy as np

np.random.seed(0)
N = 64
Lbox = 8.0
dt = 0.005
STEPS = 2000
RC = 2.5
# shift 使截斷處能量連續
UCUT = 4.0 * ((1.0 / RC) ** 12 - (1.0 / RC) ** 6)

def forces_and_pe(pos):
    d = pos[:, None, :] - pos[None, :, :]       # (N,N,2)
    d -= Lbox * np.round(d / Lbox)              # 最小鏡像
    r2 = np.sum(d * d, axis=-1)
    np.fill_diagonal(r2, np.inf)
    mask = r2 < RC * RC
    inv2 = np.zeros_like(r2)
    inv2[mask] = 1.0 / r2[mask]
    inv6 = inv2 ** 3
    inv12 = inv6 ** 2
    pe = float(np.sum(4.0 * (inv12 - inv6) - UCUT * mask)) / 2.0
    fmag = np.zeros_like(r2)
    fmag[mask] = 24.0 * (2.0 * inv12[mask] - inv6[mask]) * inv2[mask]
    F = np.sum(fmag[:, :, None] * d, axis=1)
    return F, pe

# 方格初位 (8x8,間距 1.0),隨機初速去質心並定標至 T≈1
n_side = 8
grid = np.array([[i % n_side, i // n_side] for i in range(N)], dtype=float)
pos = (grid + 0.5) * (Lbox / n_side)
vel = np.random.rand(N, 2) - 0.5
vel -= vel.mean(axis=0)
ke0_target = N * 1.0  # 2D: T=KE/N,目標 T=1
scale = np.sqrt(ke0_target / (0.5 * float(np.sum(vel * vel))))
vel *= scale

acc, pe = forces_and_pe(pos)
ke = 0.5 * float(np.sum(vel * vel))
E0 = ke + pe
for _ in range(STEPS):
    pos = pos + vel * dt + 0.5 * acc * dt * dt
    pos = np.mod(pos, Lbox)
    acc_new, pe = forces_and_pe(pos)
    vel = vel + 0.5 * (acc + acc_new) * dt
    acc = acc_new
ke = 0.5 * float(np.sum(vel * vel))
E1 = ke + pe
drift = abs(E1 - E0) / abs(E0)

# 徑向分佈:末態對距離直方圖,找 [0.8,2.0] 內第一峰
d = pos[:, None, :] - pos[None, :, :]
d -= Lbox * np.round(d / Lbox)
dist = np.sqrt(np.sum(d * d, axis=-1))
iu = np.triu_indices(N, 1)
rr = dist[iu]
bins = np.linspace(0.0, 4.0, 81)
hist, edges = np.histogram(rr, bins=bins)
cent = 0.5 * (edges[:-1] + edges[1:])
lo = int(0.8 / 0.05); hi = int(2.0 / 0.05)
seg = hist[lo:hi]
peak_idx = lo + int(np.argmax(seg))
r_peak = float(cent[peak_idx])
ok_e = drift < 0.02
ok_r = 0.9 < r_peak < 1.4
print(f"E0={E0:.4f}, E1={E1:.4f}, drift={drift*100:.4f}% (驗證 <2%: {'PASS' if ok_e else 'FAIL'})")
print(f"RDF 第一峰 r={r_peak:.3f}σ (驗證約 1.1: {'PASS' if ok_r else 'FAIL'})")
print(f"VERIFY: drift={drift:.6f}, r_peak={r_peak:.6f}")
assert ok_e, "能量漂移過大"
assert ok_r, "RDF 第一峰偏離 1.1σ"
print("ALL CHECKS PASS")
```
