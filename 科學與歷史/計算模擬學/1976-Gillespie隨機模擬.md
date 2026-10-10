# 1976 年 Gillespie 隨機模擬：化學主方程的精確口供

> 報案人：細胞裡的低拷貝分子。案情：濃度方程謊報軍情，漲落才是真兇。
> 偵探 Daniel Gillespie 用 propensity 審訊每個反應，寫出精確 SSA 筆錄。

| 案件檔案 | 內容 |
|----------|------|
| 發生時間 | 1976 至 1977 年 |
| 發生地點 | 美國 Maryland，Naval Research Lab |
| 報案人 | 化學動力學、生物漲落 |
| 偵探 | Daniel T. Gillespie |
| 兇器 | propensity  $a_j$  、主方程、SSA |
| 結論 | 精確隨機模擬誕生，系統生物學點火 |

## 案發現場

1976 年的化學動力學是一間過於整潔的辦公室。

質量作用定律把分子數當連續濃度，寫下常微分方程，
卻在細胞裡頻頻失靈。大腸桿菌某轉錄因子僅十個拷貝，
濃度概念成了偽證，漲落大到改寫命運。

現場有兩具屍體。確定性速率方程只給平均，
殺死了分布與隨機開關。Langevin 加了高斯雜訊，
卻在小數目下給出負分子數的荒唐口供。

Gillespie 回到分子碰撞第一性原理，不近似不抹平，
直接模擬每次反應何時發生、哪個通道開火。
關鍵證人是化學主方程，它追蹤機率  $P(x,t)$  ，
即時間  $t$  處於狀態  $x$  的機率，寫得出卻解不出，
偵探決定不解它，而是直接扮演它。

## 偵查過程

偵查從 propensity 定義開始。每個通道  $j$  ，
賦予函數  $a_j(x)$  ，意義是無窮小時間開火的機率率。
總 propensity 記為  $a_0$  ，為所有通道之和：

$$
a_0(x) = \sum_j a_j(x)
$$

其中求和遍歷全部通道， $a_0$  決定下一步急迫程度。

全案最關鍵的聯合分布：已知當前狀態，
下一等待時間為  $\tau$  且通道為  $j$  的密度為：

$$
P(\tau,j) = a_je^{-a_0\tau}
$$

其中  $\tau$  為等待時間， $j$  為通道，
 $a_j$  取當前狀態的值。指數部分是全體沉默的存活機率，
前因子是  $j$  率先打破沉默的比率。

抽樣拆成兩步，史稱直接法。等待時間  $\tau$  服從指數分布，
用均勻隨機數  $r_1$  反演：

$$
\tau = \frac{1}{a_0}\ln\frac{1}{r_1}
$$

其中  $r_1$  為均勻隨機數， $a_0$  為總 propensity。
再以機率  $a_j / a_0$  選通道，用  $r_2$  落點判定。

| 方法 | 精確性 | 適用區間 | 代價 |
|------|--------|----------|------|
| ODE 速率方程 | 平均近似 | 大體積極限 | 最便宜 |
| Langevin | 高斯近似 | 中等拷貝 | 中等 |
| SSA 直接法 | 精確 | 全區間 | 逐反應昂貴 |
| tau-leaping | 近似加速 | 大  $a_0$  | 可調誤差 |

SSA 不是近似，它就是主方程的精確抽樣器，
軌道系綜嚴格服從主方程，證據鏈無斷點。

## 結案報告

Gillespie 1976 年論文發表在計算物理期刊，
1977 年再發物理詮釋，合計引用數萬。

遺產有三。第一，隨機化學動力學立國，
低拷貝體系非 SSA 作證不可。第二，加速家族誕生，
tau-leaping 與 Gibson-Bruck 法全是子孫。
第三，跨界系統生物學，從噬菌體抉擇到晝夜節律，
SSA 是細胞模擬器的陪審團。

兇手確定性幻覺定罪，漲落聘為首席證人。

## 證據與工具

關鍵證物一：SSA 直接法虛擬碼。

```python
# x 為分子數向量，t 為時間
while t < Tmax:
    a = [propensity(j, x) for j in channels]
    a0 = sum(a)
    r1, r2 = rand(), rand()
    tau = log(1.0 / r1) / a0
    j = pick_channel(a, a0, r2)
    x, t = x + stoichiometry[j], t + tau
```

關鍵證物二：propensity 對照。

| 反應類型 | 實例 | propensity  $a_j$  |
|----------|------|---------------------|
| 單分子 | 降解 | 常數乘以  $x$  |
| 異種雙分子 | 結合 | 常數乘以  $x_A x_B$  |
| 同種雙分子 | 二聚 | 常數乘以  $x(x-1)/2$  |

延伸閱讀伏筆：SSA 哲學將呼應 1980 年量子 Monte Carlo。

## 補充：程式實作

> 報案說濃度方程粉飾太平，偵探決定把每次碰撞都叫來問話，口供全錄在此。

對應程式：[1976-gillespie_ssa.py](_code/1976-gillespie_ssa.py)

本程式辦的是出生-死亡案：恆定出生率 $lambda$ 對上正比於分子數的死亡率，正是主方程可解的鐵證。
總 propensity 仍是老規矩 $a_0(x) = a_1 + a_2$ ，其中 $a_1 = lambda$ 為出生， $a_2 = mu x$ 為死亡。
每一步按本文直接法抽等待時間 $tau = ln(1/r_1)/a_0$ ，再以機率 $a_1/a_0$ 決定生或死。
跑完兩萬個反應後做時間加權平均，理論定常分布是均值為 $lambda/mu = 2$ 的 Poisson 分布。
時間加權是關鍵證人：SSA 軌道必須按停留時間計權，算術平均會被短步長霸凌。

執行指令：

```bash
python3 _code/1976-gillespie_ssa.py
```

實測口供（種子固定為 0，捨去前 1000 步熱身）：

```text
reactions=20000 burn=1000
time_weighted_mean=1.99548 plain_mean=2.50463 target=2.0
final_X=1 total_time=5099.99
VERIFY mean=1.99548 target=2.0 err=0.00452 (<0.15? True)
PASS
```

解讀要點：

- 時間加權均值 1.99548 對上理論 2.0，誤差僅 0.00452，遠小於 0.15 的結案門檻。
- 未加權的 plain_mean 高達 2.50463，正好示範為何不能拿算術平均充數。
- 終態分子數 1、總模擬時間 5099.99，證明漲落活口未被抹平。
- 種子固定故每次重跑口供一致，可放心對質。

讀者可改出生率 $lambda$ （如改為 5.0）或死亡係數 $mu$ ，重跑看均值是否跟著移到 $lambda/mu$ ，再試把反應數砍半看誤差如何變大。

完整程式如下：

```python
# -*- coding: utf-8 -*-
"""1976 Gillespie SSA：出生-死亡過程
對應 wiki：Gillespie (1976) Stochastic Simulation Algorithm，Doob-Gillespie。
模型：X -> X+1 速率 lambda=2（恆定出生），X -> X-1 速率 mu*X, mu=1。
定常分佈 Poisson(lambda/mu)，均值=2。SSA 跑 20000 反應，時間加權均值驗證誤差<0.15。
只用 numpy，固定種子。
"""
import numpy as np

np.random.seed(0)

lam = 2.0
mu = 1.0
N_REACT = 20000
BURN = 1000  # 捨去前 1000 反應


def run_ssa():
    x = 0  # 初值
    t = 0.0
    xs = np.empty(N_REACT, dtype=float)
    taus = np.empty(N_REACT, dtype=float)
    for i in range(N_REACT):
        a1 = lam
        a2 = mu * x
        a0 = a1 + a2
        u1 = np.random.rand()
        u2 = np.random.rand()
        tau = -np.log(u1) / a0
        taus[i] = tau
        xs[i] = x
        t += tau
        if u2 < a1 / a0:
            x += 1
        else:
            x = max(0, x - 1)
    return xs, taus


xs, taus = run_ssa()
# 時間加權均值（捨 burn-in）
w = taus[BURN:]
v = xs[BURN:]
mean_tw = float(np.sum(v * w) / np.sum(w))
mean_plain = float(np.mean(v))
target = lam / mu
err = abs(mean_tw - target)
print(f"reactions={N_REACT} burn={BURN}")
print(f"time_weighted_mean={mean_tw:.5f} plain_mean={mean_plain:.5f} target={target}")
print(f"final_X={xs[-1]:.0f} total_time={np.sum(taus):.2f}")
print(f"VERIFY mean={mean_tw:.5f} target=2.0 err={err:.5f} (<0.15? {err < 0.15})")
assert err < 0.15, f"mean error too large: {err}"
print("PASS")
```
