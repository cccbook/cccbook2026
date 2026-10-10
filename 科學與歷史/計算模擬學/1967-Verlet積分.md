# 1967 年 Verlet 積分：時間可逆的守護神

> 報案人：分子動力學。案情：所有軌道都在慢慢死去，能量像漏水的水桶。
> 偵探 Loup Verlet 接案，在液態氬的深夜裡找到一條不會留下腳印的路。

| 案件檔案 | 內容 |
|----------|------|
| 發生時間 | 1967 年 |
| 發生地點 | 法國 Orsay，液體理論實驗室 |
| 報案人 | Alder、Rahman 的 MD 繼承者們 |
| 偵探 | Loup Verlet |
| 兇器 | 能量漂移、數值耗散 |
| 結論 | 位置 Verlet 公式成為 MD 標準積分器 |

## 案發現場

1967 年的分子動力學是一間漏水的密室。

Alder 與 Wainwright 在 1957 年用硬球證明電腦可重演相變，
Rahman 在 1964 年用連續勢算出液態氬，案子看似偵破了。
但所有長期模擬都有同一個怪談：跑得越久，能量漂得越遠。

當時的積分器多半是 Runge-Kutta 或 Euler 類格式。
它們每一步都很準，卻偷走時間的方向。
正向跑與逆向跑不對稱，真相逐漸失真。

Verlet 面對兩具屍體。第一具是能量守恆，
總能量  $E$  應守恆，卻在數千步後系統性漂移。
第二具是時間可逆性，牛頓方程在  $t \to -t$  下不變，
數值格式卻把過去與未來區別對待。

Verlet 的問題於是成形：能否只用當前受力  $a_n$  ，
走出一條可逆、不耗散、長期穩定的軌道。

## 偵查過程

偵探回到牛頓案卷。粒子位置  $x$  滿足  $F = ma$  ，
加速度  $a_n$  由第  $n$  步位置決定，步長記為  $h$  。
靈感像法醫的雙向取證：同時向前與向後展開 Taylor 級數，
速度一次項符號相反，相加湮滅。

核心證據只有一條公式：

$$
x_{n+1} = 2x_n - x_{n-1} + a_nh^2
$$

式中  $x_n$  為當前位置， $x_{n-1}$  為上一步位置，
 $a_n$  為當前加速度， $h$  為時間步長。

推理鏈有三。其一，速度憑空消失，奇數階誤差抵消，
局部誤差達  $O(h^4)$  ，卻只用一次受力評估。
其二，時間可逆自動成立，把  $n+1$  與  $n-1$  互換，
公式形式不變，通過「倒帶測試」。
其三，辛結構近似保持，能量誤差有界振盪而不漂移。

下表是嫌疑積分器的比對筆錄：

| 積分器 | 每步受力 | 時間可逆 | 能量行為 |
|--------|----------|----------|----------|
| Euler | 1 次 | 否 | 快速漂移 |
| Runge-Kutta 4 | 4 次 | 否 | 長期漂移 |
| 位置 Verlet | 1 次 | 是 | 有界振盪 |
| 速度 Verlet | 1 次 | 是 | 有界振盪 |

速度 Verlet 是後來的標準改寫，顯式攜帶速度  $v$  ：

$$
x_{n+1} = x_n + v_nh + \frac{1}{2}a_nh^2
$$

$$
v_{n+1} = v_n + \frac{1}{2}(a_n + a_{n+1})h
$$

兩式聯立與位置形式等價，但可直接控溫算動能，
成為教科書預設版本。步長  $h$  須小於最快週期十分之一，
有機體系約取 1 飛秒。

## 結案報告

Verlet 在 1967 年液體結構論文中亮出手術刀，
順手算出 Lennard-Jones 流體相圖，一戰成名。

判決遺產有三。第一，MD 有了標準引擎，
從 Rahman 的氬到 1977 年蛋白質，皆踩此腳印。
第二，幾何數值積分誕生，可逆與辛性成為審美標準，
影響 SHAKE 與多時間步法。第三，長時模擬成為可能，
科學家敢問「一百萬步之後會如何」。

兇手能量漂移被收押，改判有界振盪。
時間之箭在數值世界裡被馴服了。

## 證據與工具

關鍵證物一：速度 Verlet 單步虛擬碼。

```python
# x 為位置，v 為速度，a 為加速度，h 為步長
x_next = x + v * h + 0.5 * a * h * h
a_next = compute_force(x_next) / m
v_next = v + 0.5 * (a + a_next) * h
```

關鍵證物二：倒帶測試。任取軌道跑  $N$  步，
反轉速度再跑  $N$  步，Verlet 能回到起點附近，
而非辛格式則回不去，此即時間可逆指紋。

延伸閱讀伏筆：速度 Verlet 將支撐 1977 年 BPTI 蛋白質 MD，
辛思想將在 1984 年 Nosé-Hoover 案中再次出場。

## 補充：程式實作

能量漏水案拖了十年，本探只用一個諧振子就讓兩名嫌疑積分器現形。

### 對應程式

[1967-verlet_oscillator.py](_code/1967-verlet_oscillator.py)

### 理論呼應

本文核心是只用當前受力 $a_n$ 走出可逆軌道，奇數階誤差相加抵消。

程式以諧振子 $m = k = 1$ 打擂台，步長 $0.02$ 連跑一百個週期。

顯式 Euler 每步便宜卻偷走時間方向，能量注定越跑越胖。

速度 Verlet 同樣每步一次受力，卻以有界振盪通過倒帶測試。

### 執行方式

```bash
python3 _code/1967-verlet_oscillator.py
```

### 實測輸出

```text
steps=31416 dt=0.02 T=628.319 (100 periods)
E0=0.500000
Euler:  E_final=1.430201e+05 rel_drift=2.860391e+05
Verlet: E_final=5.000000e-01 rel_drift=1.425987e-08
VERIFY verlet_drift=1.426e-08 (<1e-3? True)
VERIFY euler_drift=2.860e+05 (diverged>1? True)
PASS
```

關鍵數字有二：Verlet 相對漂移僅 $1.426e-08$ ，遠小於 $1e-3$ 門檻。

Euler 相對漂移高達 $2.860e+05$ ，能量從 $0.5$ 膨脹到 $1.430201e+05$ 。

一守一崩，對照筆錄完成，長期模擬該僱誰一目了然。

### 讀者實驗

把步長 $h$ 從 0.02 改為 0.1 或 0.005 ，重看 Verlet 誤差何時由振盪轉為失穩。

完整程式如下：

```python
# -*- coding: utf-8 -*-
"""1967 Verlet 積分器：諧振子能量穩定性
對應 wiki：Loup Verlet (1967) 經典分子動力學積分器；比較顯式 Euler vs 速度 Verlet。
諧振子 m=k=1, omega=1，跑 100 週期 (T=200*pi)，dt=0.02。
驗證：Verlet 相對能量漂移 < 1e-3（辛積分器能量有界），Euler 發散（能量暴增）。
只用 numpy，固定種子。
"""
import numpy as np

np.random.seed(0)

# 參數
omega = 1.0
T_total = 200.0 * np.pi  # 100 週期
dt = 0.02
nsteps = int(round(T_total / dt))
x0, v0 = 1.0, 0.0
E0 = 0.5 * (v0 ** 2 + omega ** 2 * x0 ** 2)


def run_euler(x0, v0, dt, nsteps):
    x, v = x0, v0
    for _ in range(nsteps):
        # 顯式 Euler：先用舊速度/加速度更新
        a = -omega ** 2 * x
        x = x + v * dt
        v = v + a * dt
    E = 0.5 * (v ** 2 + omega ** 2 * x ** 2)
    return x, v, E


def run_verlet(x0, v0, dt, nsteps):
    x, v = x0, v0
    for _ in range(nsteps):
        a = -omega ** 2 * x
        x = x + v * dt + 0.5 * a * dt * dt
        a_new = -omega ** 2 * x
        v = v + 0.5 * (a + a_new) * dt
    E = 0.5 * (v ** 2 + omega ** 2 * x ** 2)
    return x, v, E


xe, ve, Ee = run_euler(x0, v0, dt, nsteps)
xv, vv, Ev = run_verlet(x0, v0, dt, nsteps)

drift_euler = abs(Ee - E0) / E0
drift_verlet = abs(Ev - E0) / E0

print(f"steps={nsteps} dt={dt} T={T_total:.3f} (100 periods)")
print(f"E0={E0:.6f}")
print(f"Euler:  E_final={Ee:.6e} rel_drift={drift_euler:.6e}")
print(f"Verlet: E_final={Ev:.6e} rel_drift={drift_verlet:.6e}")

# 驗證數字
ok_verlet = drift_verlet < 1e-3
ok_euler = drift_euler > 1.0  # 發散：能量至少翻倍（實際大數百倍）
print(f"VERIFY verlet_drift={drift_verlet:.3e} (<1e-3? {ok_verlet})")
print(f"VERIFY euler_drift={drift_euler:.3e} (diverged>1? {ok_euler})")
assert ok_verlet, f"Verlet drift too large: {drift_verlet}"
assert ok_euler, f"Euler did not diverge: {drift_euler}"
print("PASS")
```
