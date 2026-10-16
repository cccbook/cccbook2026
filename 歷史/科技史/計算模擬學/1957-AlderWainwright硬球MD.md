# 1957：Alder–Wainwright 硬球 MD — 相變的電腦證據

> 副標題：幾百顆不會變軟的球，撞出了固液之謎的答案。

## 案發現場

1957 年前統計力學有樁懸案：流體如何變成固體？
van der Waals 說吸引力造成凝結，排斥只是配角。
許多人懷疑純排斥硬球不可能相變，因無能量尺度。
硬球勢最單純：不重疊能量零，重疊能量無窮大。
溫度只改碰撞頻率，相變似乎無從談起。
解析理論在稠密處全滅，維里展開只在稀薄有效。
證人是 Livermore 的 Alder 與 Wainwright 。
他們決定讓硬球自己動起來，看是否自發結晶。
若電腦硬球結晶，懷疑派必須閉嘴。

## 偵查過程

### 線索一：事件驅動的時鐘詭計

硬球無連續力，只有瞬間碰撞，固定步進全浪費。
妙計是事件驅動：直接算出下一對碰撞時間。
設相對位置為 $r$ ，相對速度為 $v$ ，直徑為 $d$ 。
碰撞條件是距離等於 $d$ ，化為時間二次方程。
取最小正根推進系統，處理彈性碰撞即可。
規則是動量能量守恆，沿連心線交換法向分量。
切向速度不變，無積分誤差，只有浮點捨入。
### 線索二：相變口供

初態隨機分佈，速度服從麥克斯韋分佈。
壓強由碰撞動量傳遞統計，密度逐步推高。
起初壓強平滑上升，懷疑派面露微笑。
越過閾值後系統自發有序，壓強曲線出現轉折。
徑向分佈從單調衰減變成尖銳峰列。
從晶格出發做熔化，轉折在同一密度附近。
| 密度區 | 結構 | 判讀 |
|--------|------|------|
| 稀薄 | 無序流體 | 氣體 |
| 中等 | 短程有序 | 稠密液體 |
| 共存區 | 兩相並存 | 一級相變 |
| 高密度 | 長程有序 | 固體 |
### 線索三：與 van der Waals 對決

擁護者辯稱吸引力才是兇手。
硬球證據打臉：無吸引力，相變依然發生。
真相是熵：有序固體給每粒子更多局域自由體積。
平動熵增補償位形熵損，自由能取得平衡。
粒子僅 32 至 500 顆，卻敢斷言熱力學極限。
轉折銳利度隨系統增大而增強，證據被法庭採納。
硬球對勢獨立公式如下。
$$ U(r) = 0 $$
上式適用於 $r > d$ ，其中 $r$ 為球心距， $d$ 為直徑。
重疊情形能量無窮，獨立公式如下。
$$ U(r) = \infty $$
上式適用於 $r < d$ ，表示絕對不可穿透。

## 結案報告

1957 年第一次分子動力學誕生，硬球被證明可以凍結。
相變不需吸引力，排斥體積同樣驅動有序化。
電腦首次作為理論證人出庭，而不只是計算器。
直接遺產是 1964 年 Rahman 液態氬連續勢模擬。
事件驅動至今用於顆粒物質與膠體模擬。
結語：讓原子自己走路，真相會撞出來。

## 證據與工具

碰撞時間獨立公式如下，為事件驅動核心。
$$ t_c = \frac{-b - \sqrt{b^2 - v^2(r^2 - d^2)}}{v^2} $$
其中 $r$ 為相對位置模， $v$ 為相對速度模， $b$ 為內積。
碰撞更新獨立公式如下。
$$ v_i' = v_i - \frac{(v_{ij} \cdot r_{ij})}{d^2} r_{ij} $$
其中 $v_{ij}$ 為相對速度， $r_{ij}$ 為連心向量。
| 符號 | 意義 | 備註 |
|------|------|------|
| $d$ | 硬球直徑 | 唯一長度尺度 |
| $t_c$ | 碰撞時間 | 取最小正根 |
虛擬碼：算所有對 $t_c$ ，取最小推進並處理碰撞。
由動量傳統計壓強，畫壓強密度曲線找轉折。
因果鏈：本案開創 MD ，Rahman 1964 年接棒連續勢。
自由能計算後證實凍結為熵驅動一級相變。
本案檔案編號 MD-1957 ，狀態已結案，碰撞仍在繼續。
今日膠體實驗在顯微鏡下重演了同樣的結晶。

## 補充：程式實作

兇手自稱碰撞天衣無縫，本探就拿兩顆球當場驗屍給你看。

### 對應程式

[1957-hardsphere_gas.py](_code/1957-hardsphere_gas.py)

### 理論呼應

本文核心是硬球只有接觸瞬間才交互，直徑為 $d$ 的兩球靠連心線交換法向動量。

程式以等質量彈性碰撞實作此規則，切向分量不動，正是文中 $v_i'$ 更新式的簡化版。

扮演事件驅動的窮人版：固定小步推進加牆面反射，省去解碰撞時間二次方程。

動量與動能若不守恆，後面的壓強統計與相變轉折全是偽證。

### 執行方式

```bash
python3 _code/1957-hardsphere_gas.py
```

### 實測輸出

```text
兩球碰撞: dP/P=0.000e+00, dK/K=8.224e-16 (驗證 <1e-9: PASS)
隨機5組最大: dP/P=0.000e+00, dK/K=0.000e+00
N=64 MD 2000步: K_init=20.7065, K_final=20.7065, drift=3.431e-16
VERIFY: errP=0.000000e+00, errK=8.223874e-16, drift=3.431488e-16
ALL CHECKS PASS
```

關鍵數字有三：兩球碰撞動量相對誤差為 $0$ ，動能相對誤差約 $8.224e-16$ ，全小於 $1e-9$ 門檻。

六十四顆球跑兩千步，總動能從 $20.7065$ 到 $20.7065$ ，漂移僅 $3.431e-16$ 。

守恆過關，壓強證詞才可採信，這正是 Alder 敢斷言凍結的底氣。

### 讀者實驗

把球數 $N$ 從 64 改為 256 ，或把半徑 $R$ 調大、步長 $dt$ 調小，重看碰撞頻率與漂移如何變化。

完整程式如下：

```python
# -*- coding: utf-8 -*-
"""1957 二維硬碟氣體 (對應 wiki: 計算模擬學 / Alder-Wainwright 硬球分子動力學)
只用 numpy,固定種子。事件驅動簡化版:小步 MD + 彈性碰撞,N=64。
驗證:直接兩球碰撞函數的總動量/動能相對誤差 < 1e-9 (動能守恆)。
"""
import numpy as np

np.random.seed(0)
N = 64
Lbox = 10.0
R = 0.2
dt = 0.01
STEPS = 2000

def collide_pair(v1, v2, x1, x2):
    """等質量彈性碰撞,沿連心線交換法向分量。回傳 (v1', v2')。"""
    n = x1 - x2
    d = float(np.linalg.norm(n))
    if d == 0.0:
        return v1.copy(), v2.copy()
    n = n / d
    p = float(np.dot(v1 - v2, n))
    if p >= 0:
        return v1.copy(), v2.copy()  # 正在分離,不碰撞
    return v1 - p * n, v2 + p * n

# --- 直接兩球碰撞驗證 (動量/動能守恆) ---
v1 = np.array([1.0, 0.3])
v2 = np.array([-0.7, -0.2])
x1 = np.array([-0.5, 0.0])
x2 = np.array([0.5, 0.1])
P0 = v1 + v2
K0 = 0.5 * (np.dot(v1, v1) + np.dot(v2, v2))
w1, w2 = collide_pair(v1, v2, x1, x2)
P1 = w1 + w2
K1 = 0.5 * (np.dot(w1, w1) + np.dot(w2, w2))
errP = float(np.linalg.norm(P1 - P0) / max(1e-300, np.linalg.norm(P0)))
errK = abs(K1 - K0) / max(1e-300, abs(K0))

# 第二組:隨機斜碰撞
np.random.seed(1)
ok2 = True
errP2 = errK2 = 0.0
for _ in range(5):
    a = np.random.rand(2) * 2 - 1
    b = np.random.rand(2) * 2 - 1
    xa = np.random.rand(2)
    xb = xa + (np.random.rand(2) - 0.5)
    c1, c2 = collide_pair(a, b, xa, xb)
    eP = float(np.linalg.norm((c1 + c2) - (a + b)) / max(1e-300, np.linalg.norm(a + b)))
    KA = 0.5 * (np.dot(a, a) + np.dot(b, b))
    KB = 0.5 * (np.dot(c1, c1) + np.dot(c2, c2))
    eK = abs(KB - KA) / max(1e-300, abs(KA))
    errP2 = max(errP2, eP); errK2 = max(errK2, eK)
np.random.seed(0)

# --- N=64 小步 MD 演示 (牆面彈性反射 + 重疊對彈性碰撞) ---
pos = np.random.rand(N, 2) * (Lbox - 2 * R) + R
vel = (np.random.rand(N, 2) - 0.5) * 2.0
K_init = 0.5 * float(np.sum(vel * vel))
for _ in range(STEPS):
    pos = pos + vel * dt
    # 牆面反射
    for d in range(2):
        lo = pos[:, d] < R
        hi = pos[:, d] > Lbox - R
        vel[lo, d] = np.abs(vel[lo, d])
        vel[hi, d] = -np.abs(vel[hi, d])
        pos[:, d] = np.clip(pos[:, d], R, Lbox - R)
    # 對碰撞 (O(N^2),N=64 可接受)
    for i in range(N):
        for j in range(i + 1, N):
            dx = pos[i] - pos[j]
            if float(np.dot(dx, dx)) < (2 * R) ** 2:
                vi, vj = collide_pair(vel[i], vel[j], pos[i], pos[j])
                vel[i], vel[j] = vi, vj
                # 位置分開避免黏連
                dist = float(np.linalg.norm(dx)) + 1e-12
                overlap = 2 * R - dist
                nrm = dx / dist
                pos[i] += 0.5 * overlap * nrm
                pos[j] -= 0.5 * overlap * nrm
K_final = 0.5 * float(np.sum(vel * vel))
drift = abs(K_final - K_init) / abs(K_init)

ok = (errK < 1e-9) and (errP < 1e-9) and (errK2 < 1e-9) and (errP2 < 1e-9)
print(f"兩球碰撞: dP/P={errP:.3e}, dK/K={errK:.3e} (驗證 <1e-9: {'PASS' if (errK<1e-9 and errP<1e-9) else 'FAIL'})")
print(f"隨機5組最大: dP/P={errP2:.3e}, dK/K={errK2:.3e}")
print(f"N=64 MD {STEPS}步: K_init={K_init:.4f}, K_final={K_final:.4f}, drift={drift:.3e}")
print(f"VERIFY: errP={errP:.6e}, errK={errK:.6e}, drift={drift:.6e}")
assert ok, "碰撞不守恆"
print("ALL CHECKS PASS")
```
