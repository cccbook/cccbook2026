# 1822年 · 傅立葉與 Navier-Stokes：連續體雙屍案

> 卷宗編號：Case-1822-Continuum｜偵探：Fourier、Navier、Stokes｜法醫：Cauchy

## 案發現場

十九世紀初的巴黎，兩具「屍體」同時被抬進科學院：一具是熱，一具是水。

第一現場在鑄炮廠與溫室。傅立葉想知道熱量如何在鐵棒裡竄動。熱看不見摸不著，只量得到溫度 $u$ 隨時間空間的變化。當時的熱質說與量熱術爭吵不休，沒人能把「熱流」寫成方程。

第二現場在運河與血管。海軍工程師納維想算水流對橋墩的推力，醫生想懂血液，工廠想懂潤滑油。水明明由無數分子組成，可工程師只關心宏觀的速度場 $v$ 與壓力場 $p$ 。要追蹤每顆分子是不可能的任務。

兩案的共同難點是：研究對象不是牛頓式的質點，而是**連續分佈的場**。偵探必須發明偏微分方程（PDE），把「每一點的變化」與「鄰居的差異」掛鉤。

## 偵查過程

### 線索一：傅立葉的熱流自白

傅立葉1822年《熱的解析理論》開宗明義：熱通量正比於溫度梯度的負方向。設溫度場為 $u(x,t)$ ，熱擴散率為 $\alpha$ ，則一維熱方程為 $u_t = \alpha u_{xx}$ ，三維推廣為：

$$
u_t = \alpha \Delta u
$$

其中 $\Delta$ 為拉普拉斯算子， $u_t$ 表時間導數。上式說：某點溫度上升的速率，正比於它比周圍平均冷多少——冷熱不均是熱流的動機。

傅立葉更掏出第二件兇器：任何初始溫度分佈都能展成正弦餘弦級數。用現代符號，區間長度 $L$ 上的解可寫為：

$$
u(x,t) = \sum_{n} b_n \sin(n\pi x / L) e^{-\alpha (n\pi/L)^2 t}
$$

其中 $b_n$ 為初始條件的正弦係數。高頻模態衰減最快，這解釋了為何尖銳的溫度稜角最先被磨平。

### 線索二：Navier-Stokes 的流體口供

納維（1822）、柯西、泊松、聖維南、斯托克斯（1845）接力偵辦流體案。設流體密度為 $\rho$ ，速度場為 $v$ ，壓力為 $p$ ，黏性係數為 $\mu$ ，不可壓縮 Navier-Stokes 方程為：

$$
\rho (v_t + v \cdot \nabla v) = -\nabla p + \mu \Delta v + f
$$

其中 $f$ 為體積力（如重力）。左端是加速度（含非線性對流項 $v \cdot \nabla v$ ），右端是壓力梯度與黏性擴散。輔以不可壓縮約束：

$$
\nabla \cdot v = 0
$$

| 項 | 物理意義 | 數學性格 |
|---|---|---|
| $v_t$ | 局部加速度 | 線性時間導數 |
| $v \cdot \nabla v$ | 流體攜帶自身動量 | 非線性，最難搞 |
| $-\nabla p$ | 壓力推動 | 約束力，維持 $\nabla \cdot v = 0$ |
| $\mu \Delta v$ | 黏性摩擦抹平速度差 | 線性擴散，與熱方程同源 |

非線性對流項讓方程既能預言層流之美，也能藏匿湍流之魔，至今千禧年大獎仍懸賞其光滑解存在性。

### 線索三：連續體假設的不在場證明

兩案能併案，全靠一紙「連續體假設」：當觀測尺度遠大於分子自由程時，把流體、固體看成無限可分的連續介質。定義 Knudsen 數 $Kn$ 為分子自由程與特徵尺度之比，則：

- $Kn < 0.01$ ：連續體成立， Navier-Stokes 可用。
- $Kn > 0.1$ ：稀薄氣體，須用 Boltzmann 方程或 DSMC 粒子法。

熱方程是標量擴散的原型， Navier-Stokes 是向量對流擴散的原型。後世的有限元素、有限體積、光滑粒子法，全是為這兩位嫌犯量身打造的手銬。

### 理論定性：CFD 母方程

本案確立了計算流體力學（CFD）的起點：

1. **場觀點**：未知量是時空函數 $u$ 與 $v$ ，而非質點軌跡。
2. **守恆律加本構律**：質量、動量、能量守恆配上傅立葉熱傳導律、牛頓黏性律，即得封閉方程。
3. **邊界條件即案情**：無滑移壁面、入口速度、出口壓力，定錯一條全盤皆錯。

## 結案報告

雙屍案表面告破：熱有熱方程，流體有 Navier-Stokes，工程師終於能算鑄件冷卻、管路壓降、機翼升力。但深層懸案才剛開始：湍流無解析解，光滑存在性未證，數值離散稍有不慎就 blow up。

遺產清單：

- **直接遺產**：鍋爐、氣象、海洋、血液、半導體製程模擬，全從這兩式分家。
- **數值遺產**： CFL 條件、迎風格式、壓力 Poisson 求解器、有限元素法，皆為馴服本案而生。
- **理論遺產**：傅立葉級數催生調和分析與快速傅立葉變換； Navier-Stokes 催生邊界層理論與湍流模式。
- **未竟線索**：湍流封閉問題移交雷諾平均、 LES、 DNS；稀薄與微納尺度移交分子動力學與格子 Boltzmann。

1822年是連續體模擬的元年：從此風、水、熱，都成了網格上的數字。

## 證據與工具

- **熱方程**： $u_t = \alpha \Delta u$ ，線性拋物型，解具無限傳播速度與磨光效應。
- **動量方程**： $\rho (v_t + v \cdot \nabla v) = -\nabla p + \mu \Delta v + f$ ，配上 $\nabla \cdot v = 0$ 。
- **傅立葉級數**：正弦餘弦基底展開，是譜方法的祖先。
- **無量綱數**：雷諾數 $Re$ 、 Prandtl 數 $Pr$ 、 Knudsen 數 $Kn$ ，用於判定流態與連續體有效性。
- **可重演實驗**：一維熱方程取 $\alpha = 0.01$ ，初值方波，用顯式差分推進，觀察高頻如何先消失。
- **延伸閱讀**：《Théorie analytique de la chaleur》；後續案件直通 Richardson，因為天氣正是大氣版的 Navier-Stokes。

## 補充：程式實作

對應程式：[1822-heat_equation_ftcs.py](_code/1822-heat_equation_ftcs.py)

本文核心理論是一維熱方程 $u_t = \alpha u_{xx}$ ，搭配零邊界與正弦初值的擴散行為。
顯式 FTCS 格式的穩定參數為 $r = \alpha dt / dx^2$ ，穩定條件是 $r \le 0.5$ 。
取 $r = 0.4$ 時數值解跟隨真解指數衰減，高頻稜角先被抹平，呼應傅立葉級數預言。
取 $r = 0.6$ 時格式越過穩定邊界，再小的擾動也會被逐層放大。
值守的 $r = 0.4$ 平穩交班、越界的 $r = 0.6$ 當場炸鍋，穩定邊界正是本案的分水嶺。

執行指令：

```bash
python3 _code/1822-heat_equation_ftcs.py
```

實測關鍵輸出（本機真實執行結果抄錄）：

```
stable r=0.4000 dx=0.0100 dt=4.00e-05 steps=2500
  max|u_num-u_exact| = 4.236174e-05 (理論衰減 e^-pi2αt=0.372708)
unstable r=0.5999 dx=0.0100 dt=6.00e-05 steps=1667
  max|u| = 1.443581e+226 (初值 max=1，穩定應衰減至約 $0.37$ )
VERIFY stable_err = 4.236e-05（小於 $1e-3$ ，通過）
VERIFY unstable_max = 1.444e+226（遠大於 $1e3$ ，確認發散）
PASS
```

讀者可改網格 $nx = 51$ 或參數 $r = 0.5$ 臨界值，重跑並比較最大誤差與是否出現振盪發散。

上述穩定例以 $101$ 點網格推進 $2500$ 步所得，最大誤差僅 $4.236174e-05$ ，印證熱方程線性擴散項可用顯式差分馴服。

完整程式如下：

```python
# -*- coding: utf-8 -*-
"""1822 熱方程顯式 FTCS（對應 wiki：計算模擬學 / Fourier 熱傳與顯式差分）
一維熱方程 u_t = α u_xx, x∈[0,1], Dirichlet u=0 邊界，初值 sin(pi·x)，
真解 u=sin(pi·x)·exp(-pi²αt)。顯式 FTCS：r=α·dt/dx²，穩定條件 r≤0.5。
穩定例 r=0.4 驗證 t=0.1 誤差<1e-3；不穩定例 r=0.6 展示爆掉。
只用 numpy，固定種子。
"""
import numpy as np

np.random.seed(0)

alpha = 1.0
nx = 101
L = 1.0
dx = L / (nx - 1)
x = np.linspace(0.0, L, nx)
t_final = 0.1


def run_ftcs(r, t_final):
    dt = r * dx * dx / alpha
    steps = int(round(t_final / dt))
    dt = t_final / steps  # 微調使恰好到 t_final
    r_eff = alpha * dt / dx / dx
    u = np.sin(np.pi * x)
    u[0] = 0.0
    u[-1] = 0.0
    with np.errstate(over="ignore", invalid="ignore"):
        for _ in range(steps):
            u[1:-1] = u[1:-1] + r_eff * (u[2:] - 2.0 * u[1:-1] + u[:-2])
    return u, steps, dt, r_eff


def exact_sol(t):
    return np.sin(np.pi * x) * np.exp(-np.pi ** 2 * alpha * t)


# 穩定：r=0.4
u_st, steps_st, dt_st, r_st = run_ftcs(0.4, t_final)
uex = exact_sol(t_final)
err_st = float(np.max(np.abs(u_st - uex)))
print(f"stable r={r_st:.4f} dx={dx:.4f} dt={dt_st:.2e} steps={steps_st}")
print(f"  max|u_num-u_exact| = {err_st:.6e} (理論衰減 e^-pi²αt={np.exp(-np.pi**2*alpha*t_final):.6f})")

# 不穩定：r=0.6
u_un, steps_un, dt_un, r_un = run_ftcs(0.6, t_final)
with np.errstate(invalid="ignore"):
    blown = (not np.all(np.isfinite(u_un))) or (float(np.nanmax(np.abs(u_un))) > 1e3)
    umax = float(np.nanmax(np.abs(u_un))) if np.any(np.isfinite(u_un)) else float("inf")
print(f"unstable r={r_un:.4f} dx={dx:.4f} dt={dt_un:.2e} steps={steps_un}")
print(f"  max|u| = {umax:.6e} (初值 max=1, 穩定應衰減至~0.37；遠大於此即爆掉)")

# 驗證數字：理論值 vs 實測
ok_stable = err_st < 1e-3
print(f"VERIFY stable_err={err_st:.3e} (<1e-3? {ok_stable})")
print(f"VERIFY unstable_max={umax:.3e} (blowup>1e3或inf/nan? {blown})")
assert ok_stable, f"穩定 FTCS 誤差太大: {err_st}"
assert blown, f"r=0.6 未觀察到不穩定爆掉: max={umax}"
print("PASS")
```
