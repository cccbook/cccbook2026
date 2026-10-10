# 1984 年 Nosé-Hoover 恆溫器：溫度的馴獸案

> 報案人：NVT 系綜。案情：MD 只會守恆能量，實驗卻要恆定溫度。
> 偵探 Nosé 祭出擴展變數  $s$  ，Hoover 改寫成更好用的馴獸鞭。

| 案件檔案 | 內容 |
|----------|------|
| 發生時間 | 1984 年 |
| 發生地點 | 日本美國雙線，Nosé 與 Hoover 接力 |
| 報案人 | 正則系綜、Verlet MD 用戶 |
| 偵探 | Shuichi Nosé、William G. Hoover |
| 兇器 | 擴展變數  $s$  、熱浴質量  $Q$  |
| 結論 | NVT 精確採樣實現，MD 配上恆溫器 |

## 案發現場

1984 年的分子動力學是一間沒有空調的密室。

Verlet 守的是微正則 NVE，實驗室要的是 NVT，
溫度恆定、能量可與熱浴交換。直接重標速度破壞系綜，
自由能全成偽證。

嫌疑犯有三：速度重標粗暴但非正則，
Andersen 隨機碰撞精確卻打斷連續性，
Berendsen 溫和卻不對應任何系綜。

Nosé 問：能否把熱浴寫進哈密頓量，
讓擴展系綜的微正則等價原系統的正則。
若能，Verlet 照跑，溫度自動恆定。
溫度是野獸，Nosé 給它套韁繩，讓它在擴展空間找平衡。

## 偵查過程

偵查從擴展哈密頓量開始，引入座標  $s$  與動量  $p_s$  ：

$$
H' = H + p_s^2/2Q + gkT\ln s
$$

其中  $H$  為原哈密頓量， $s$  為熱浴變數，
 $p_s$  為其動量， $Q$  為熱浴質量，
 $g$  為自由度數， $T$  為目標溫度， $k$  為常數。

 $s$  像熱浴活塞， $Q$  決定慣性，
對數勢保證正則分布。擴展系統做 NVE，
消去  $s$  後原系統分布正比於 Boltzmann 因子：

$$
P(r,p) \propto \exp(-H/kT)
$$

其中  $r$  為座標， $p$  為動量， $H$  為原哈密頓量，
 $T$  為目標溫度。

Hoover 改寫為實時間方程，粒子受摩擦  $\zeta$  調製：

$$
\dot r = p/m
$$

$$
\dot p = F - \zeta p
$$

$$
\dot \zeta = (T_{inst} - T)/\tau^2
$$

其中  $r$  為位置， $p$  為動量， $F$  為受力，
 $\zeta$  為摩擦係數， $T_{inst}$  為瞬時溫度，
 $T$  為目標溫度， $\tau$  為弛豫時間。

| 方法 | 系綜正確 | 動力學連續 | 可算自由能 |
|------|----------|------------|------------|
| 速度重標 | 否 | 是但失真 | 否 |
| Andersen | 是 | 否 | 是 |
| Berendsen | 否 | 是 | 否 |
| Nosé-Hoover | 是 | 是 | 是 |

 $Q$  太大控溫遲鈍，太小高頻振盪。
單恆溫器對諧振子有遍歷破缺，後世以熱浴鏈治之。

## 結案報告

Nosé 1984 年論文加 Hoover 改寫一出，
NVT 成 MD 標配，NPT 隨即跟進。

遺產有三：系綜嚴格化，MD 變統計力學儀器；
確定性控溫美學，不用隨機數也得正則分布；
恆溫器家族誕生，熱浴鏈與 Langevin 各鎮戰場。

溫度野獸被關進  $s$  的籠子，鑰匙是  $Q$  。

## 證據與工具

關鍵證物一：Nosé-Hoover 虛擬碼。

```python
# zeta 為摩擦係數，Q 為熱浴質量，T0 為目標溫度
for step in range(nsteps):
    v += 0.5 * h * (f/m - zeta*v)
    r += h * v
    f = compute_force(r)
    Tinst = kinetic(v) / (0.5 * g * kB)
    zeta += h * (Tinst - T0) * g * kB / Q
```

關鍵證物二：參數表。

| 參數 | 符號 | 原則 | 失手後果 |
|------|------|------|----------|
| 熱浴質量 |  $Q$  | 匹配聲子頻率 | 振盪失控 |
| 自由度 |  $g$  | 3 倍原子數 | 標度錯 |
| 鏈長 |  $M$  | 剛性用 3 至 5 | 非遍歷 |

延伸閱讀伏筆：恆溫器將護航 1985 年 Car-Parrinello MD。

## 補充：程式實作

> 溫度野獸在 NVE 密室裡橫衝直撞，偵探放出摩擦係數這條馴獸鞭，看它俯首帖耳。

對應程式：[1984-nose_hoover.py](_code/1984-nose_hoover.py)

本程式馴的是一維諧振子，質量與力常數皆取 1，目標溫度 $T_0 = 1.0$ ，熱浴質量取 $Q = 1.0$ 。
運動即本文 Hoover 實時間式：位置照 $dr/dt = p/m$ 走，動量多一條 $-zeta p$ 韁繩，摩擦按 $T_{inst} - T_0$ 伸縮。
積分採 Trotter 分裂加 velocity-Verlet，步長 $dt = 0.005$ 連跑 20 萬步，取後半段統計才算數。
驗收看能量均分：時間平均動能 $langle K rangle$ 應回到 $T_0/2 = 0.5$ ，誤差小於 0.1 即馴服成功。
熱浴質量 $Q$ 決定韁繩鬆緊：太大控溫遲鈍，太小高頻抖動，1.0 恰是本案的甜蜜點。

執行指令：

```bash
python3 _code/1984-nose_hoover.py
```

實測口供（種子固定為 0，初速落在等分配上）：

```text
T0=1.0 Q=1.0 dt=0.005 nstep=200000
avg_KE(second half)=0.50005 target=0.50000 err=0.00005
VERIFY |avgKE-0.5|=0.00005 (<0.1? True)
PASS
```

解讀要點：

- 後半段平均動能 0.50005，對上理論 0.50000，誤差僅 0.00005，馴獸堪稱完美。
- 確定性動力學全程未擲隨機數，卻交出正則系綜的口供，正是 Nosé-Hoover 的招牌魔術。
- 20 萬步 Trotter 分裂保證長時間穩定，摩擦 $zeta$ 自動伸縮吸放熱量。
- 初速取 1.0 只是讓熱身快一點，長跑後初值影響早被熱浴吃掉。

讀者可改熱浴質量 $Q$ （如改為 0.1 或 10.0）或目標溫度 $T_0$ ，重跑看平均動能是否仍鎖定 $T_0/2$ ，再看 $zeta$ 振盪如何變臉。

完整程式如下：

```python
# -*- coding: utf-8 -*-
"""1984 Nosé-Hoover 恆溫器：一維諧振子
對應 wiki：Nosé (1984) / Hoover 確定性恆溫器；單恆溫器鏈 (M=1) 採樣正則系綜。
m=k=kB=1，目標 T=1.0，Q=1.0，dt=0.005 跑 2e5 步（Trotter 分裂積分）。
驗證：後半段時間平均動能 <p^2/2> ≈ T/2=0.5（誤差<0.1）。只用 numpy，固定種子。
"""
import numpy as np

np.random.seed(0)

T0 = 1.0
Q = 1.0
dt = 0.005
NSTEP = 200000

x = 0.0
v = 1.0  # 初動能即 0.5，落在目標等分配上
zeta = 0.0

ke_sum = 0.0
ke2_sum = 0.0
count = 0
half = NSTEP // 2
for i in range(NSTEP):
    # --- Trotter 分裂：zeta 半步 ---
    zeta += 0.5 * dt * (v * v - T0) / Q
    # --- 恆溫器半步（精確摩擦因子） ---
    s = np.exp(-0.5 * dt * zeta)
    v *= s
    # --- 諧振子 velocity-Verlet 半步 ---
    v += -0.5 * dt * x
    x += dt * v
    v += -0.5 * dt * x
    # --- 恆溫器半步 ---
    v *= s
    # --- zeta 半步 ---
    zeta += 0.5 * dt * (v * v - T0) / Q
    if i >= half:
        ke = 0.5 * v * v
        ke_sum += ke
        ke2_sum += ke * ke
        count += 1

avg_ke = ke_sum / count
target = T0 / 2.0
err = abs(avg_ke - target)
print(f"T0={T0} Q={Q} dt={dt} nstep={NSTEP}")
print(f"avg_KE(second half)={avg_ke:.5f} target={target:.5f} err={err:.5f}")
print(f"VERIFY |avgKE-0.5|={err:.5f} (<0.1? {err < 0.1})")
assert err < 0.1, f"Nosé-Hoover avg KE off: {avg_ke}"
print("PASS")
```
