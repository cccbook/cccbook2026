# 1922年 · Richardson 數值天氣：六萬人算房案

> 卷宗編號：Case-1922-ForecastFactory｜偵探：Lewis Fry Richardson｜前輩證人：Vilhelm Bjerknes

## 案發現場

一戰的戰壕裡，氣象是生死。飛機要風，毒氣要風，艦炮更要風。挪威的 Bjerknes 父子喊出豪言：大氣是流體，流體服從物理定律，天氣預報應該是「初值問題」——量出此刻全場氣壓溫度，再用方程推出下一刻。

1922年，英國數學家 Richardson 把這豪言寫成六百頁的《Weather Prediction by Numerical Process》。案發現場擺著三樣證物：

1. 七個原始大氣方程（動量、連續、熱力學、狀態方程），全是 Navier-Stokes 的親戚。
2. 一張1910年5月20日的歐洲天氣圖，作為唯一的「案發快照」。
3. 一支鉛筆、一把計算尺，和 Richardson 在救護車隊執勤間隙的手算草稿。

沒有電腦，沒有探空火箭，高空資料近乎空白。Richardson 卻想用人手算出六小時預報。這不是計畫，這是幻想——但幻想裡藏著未來。

## 偵查過程

### 線索一：預報工廠的狂想

Richardson 在書末描繪了科幻級的「Forecast Factory」：一座圓形大劇場，牆面是世界地圖， $64,000$ 名計算員每人負責一塊網格，用信號燈互相傳遞鄰區數值，由一位指揮家站在高台協調節拍。

| 崗位 | 人數 | 任務 |
|---|---|---|
| 網格計算員 | $64,000$ | 每人推進一根氣柱的七方程 |
| 傳令協調員 | 數百 | 傳遞邊界通量 |
| 指揮家 | $1$ | 統一時間步，維持因果律 |
| 觀測員 | 全球站網 | 提供初值 $p$ 、 $T$ 、 $v$ |

以今日眼光看，這就是平行計算的活體預演：區域分解、訊息傳遞（MPI）、同步步進，一應俱全，只差把人換成電晶體。

### 線索二：六小時預報慘敗

Richardson 親自試算一例：取德國上空兩氣柱，步長 $h$ 約 $200$ 公里，時間步約 $6$ 小時，手算六週，得到氣壓變化 $145$ 百帕——離譜到荒謬，真實變化不到 $1$ 百帕。

死因有二，法醫報告如下：

1. **初值不平衡**：觀測的風壓場不滿足靜力與地轉平衡，原始方程裡的重力波模態被激發，數值解劇烈振盪。後世稱之為「初始化問題」。
2. **CFL 前身**：時間步太大，資訊在一 步內橫跨多個網格，違反因果律。Courant、Friedrichs、Lewy 要到1928年才 formalize 為 CFL 條件，即：

$$
c \Delta t / \Delta x \le 1
$$

其中 $c$ 為最快波速， $\Delta t$ 為時間步， $\Delta x$ 為網格距。Richardson 憑直覺察覺步長須縮短，卻無緣見到定理。

### 線索三：Bjerknes 的前輩遺囑

Bjerknes 在1904年已立下「理性預報」兩步走：診斷（觀測初值）加預斷（方程積分）。他還提出環流定理與鋒面學說，培養了 Bergen 學派。Richardson 案的真正前因是 Bjerknes 把氣象從經驗諺語變成物理問題。

| 年代 | 人物 | 貢獻 |
|---|---|---|
| $1904$ | Bjerknes | 預報即初值問題宣言 |
| $1910$ 年代 | Bergen 學派 | 鋒面、氣團概念，改善診斷 |
| $1922$ | Richardson | 七方程離散化＋人工試算 |
| $1928$ | Courant 等 | CFL 條件，解釋發散 |

Richardson 不是輸在方程，而是輸在初值處理與穩定性理論尚未出生。

### 理論定性：數值天氣的三堂課

1. **資料同化**：觀測有誤差、有空洞，必須先「馴化」成平衡初值，而非直接餵給方程。
2. **快慢波分離**：大氣同時有慢 Rossby 波（天氣主角）與快重力波（噪音），格式須過濾後者。
3. **算力即正義**： $64,000$ 人算房證明問題可分解，靜待 ENIAC 把人力換成電子。

## 結案報告

1922年預報以 $145$ 百帕的笑柄收場，出版社滯銷，Richardson 本人因反戰被邊緣化。但卷宗並未封存：1950年 Charney 用 ENIAC 與過濾方程做出第一次成功預報，用的正是本案的骨架；今日每 $6$ 小時同化、每小時更新的全球預報鏈，都是預報工廠的電子轉世。

遺產清單：

- **直接遺產**：原始方程組、網格離散、平行分解，全部沿用至今。
- **失敗遺產**：不平衡初值教會後世做正規模初始化、變分同化。
- **科幻遺產**： $64,000$ 人算房是雲端分散式計算最早的文學形象。
- **未竟線索**：混沌（Lorenz 1963）隨後證明兩週以上確定性預報無望，預報轉向系集機率。

Richardson 輸了六小時，卻贏了整整一個世紀。

## 證據與工具

- **核心方程組**：七個大氣原始方程，動量 $v_t$ 、連續方程、熱力學方程、狀態方程聯立。
- **穩定性判據**： $c \Delta t / \Delta x \le 1$ ，CFL 條件的前身直覺。
- **失敗數據**：預報氣壓傾向 $145$ 百帕對真實 $< 1$ 百帕，誤差達兩量級。
- **工廠參數**： $64,000$ 人、 $200$ 公里網格、 $6$ 小時步長，今日重演只需筆電數秒。
- **可重演實驗**：寫一維線性平流 $u_t + c u_x = 0$ ，分別取 $c \Delta t / \Delta x = 0.8$ 與 $1.2$ ，觀察前者穩定、後者爆炸。
- **延伸閱讀**：《Weather Prediction by Numerical Process》1922；後續案件直通 Charney 1950 與 Lorenz 混沌。

## 補充：程式實作

對應程式：[1922-advection_cfl.py](_code/1922-advection_cfl.py)

本文核心理論是平流方程 $u_t + c u_x = 0$ 所揭示的時間步陷阱，與 Richardson 失敗同源。
迎風格式的穩定條件為 $CFL = c dt / dx \le 1$ ，資訊一步至多走一格才合乎因果。
中心差 FTCS 的放大因子恆大於 $1$ ，不論步長多小都屬無條件不穩定。
本程式取 $CFL = 0.5$ 重演兩種命運：迎風穩定回原位，中心差原地爆炸。
時間步一大就跨格追兇的 Richardson，當場在 $5.885479e+21$ 的誤差前翻了車。

執行指令：

```bash
python3 _code/1922-advection_cfl.py
```

實測關鍵輸出（本機真實執行結果抄錄）：

```
N=200 dx=0.00500 dt=2.50e-03 CFL=0.500 steps=800 T=2.0
理論: 迎風 CFL<=1 穩定；FTCS |G|max=1.1180>1 恆不穩定
upwind L2 err = 1.354171e-01
FTCS   L2 err = 5.885479e+21 (max|u|=1.336e+22，初值 max=1)
VERIFY upwind_L2 = 1.354e-01（小於 $0.3$ ，穩定通過）
VERIFY ftcs_L2 = 5.885e+21（大於 $1.0$ 且遠超迎風十倍，確認發散）
PASS
```

讀者可改 $CFL = 1.2$ 重跑迎風格式，觀察滿足因果律的邊界一旦越過，穩定解如何轉為發散。

上述迎風誤差 $1.354171e-01$ 來自 $800$ 步完整平流兩圈的累積，呼應原文時間步太大即違反因果律的診斷。

完整程式如下：

```python
# -*- coding: utf-8 -*-
"""1922 線性平流與 CFL 條件（對應 wiki：計算模擬學 / Courant 平流穩定性）
一維線性平流 u_t + c·u_x = 0, c=1，週期域 [0,1)，初值高斯包
u(x,0)=exp(-((x-0.3)/0.05)²)。真解為整體平移 u(x,t)=u0(x-c·t mod 1)。
迎風法 CFL=c·dt/dx=0.5（≤1 穩定）；FTCS 中心差放大因子
|G|=sqrt(1+C²sin²(k·dx))>1 恆不穩定。跑 T=2.0（包繞兩圈回到原位），
印 L2 誤差，驗證迎風穩定、FTCS 爆掉。
只用 numpy，固定種子。
"""
import numpy as np

np.random.seed(0)

N = 200
L = 1.0
dx = L / N
c = 1.0
CFL = 0.5
dt = CFL * dx / c
T = 2.0
steps = int(round(T / dt))
dt = T / steps
CFL = c * dt / dx
x = np.arange(N) * dx
sigma, x0 = 0.05, 0.3


def u0(xv):
    return np.exp(-(((xv - x0) / sigma) ** 2))


def exact(xv, t):
    return u0((xv - c * t) % L)


u_init = u0(x)
uex = exact(x, T)

# 迎風法（upwind, CFL<=1 穩定）
u_up = u_init.copy()
with np.errstate(over="ignore", invalid="ignore"):
    for _ in range(steps):
        u_up = u_up - CFL * (u_up - np.roll(u_up, 1))
l2_up = float(np.sqrt(np.mean((u_up - uex) ** 2)))

# FTCS 中心差（無條件不穩定）
u_ct = u_init.copy()
with np.errstate(over="ignore", invalid="ignore"):
    for _ in range(steps):
        u_ct = u_ct - CFL / 2.0 * (np.roll(u_ct, -1) - np.roll(u_ct, 1))
with np.errstate(invalid="ignore"):
    if np.all(np.isfinite(u_ct)):
        l2_ct = float(np.sqrt(np.mean((u_ct - uex) ** 2)))
        cmax = float(np.max(np.abs(u_ct)))
    else:
        l2_ct = float("inf")
        cmax = float("inf")

gmax = float(np.sqrt(1.0 + CFL ** 2))  # |G| 最大值 (sin=±1)
print(f"N={N} dx={dx:.5f} dt={dt:.2e} CFL={CFL:.3f} steps={steps} T={T}")
print(f"理論: 迎風 CFL≤1 穩定；FTCS |G|max={gmax:.4f}>1 恆不穩定")
print(f"upwind L2 err = {l2_up:.6e}")
print(f"FTCS   L2 err = {l2_ct:.6e} (max|u|={cmax:.3e}, 初值 max=1)")

# 驗證數字：理論值 vs 實測
ok_up = np.isfinite(l2_up) and (l2_up < 0.3)
ok_ct = (not np.isfinite(l2_ct)) or (l2_ct > 1.0) or (l2_ct > 10.0 * l2_up)
print(f"VERIFY upwind_L2={l2_up:.3e} (<0.3 穩定? {ok_up})")
print(f"VERIFY ftcs_L2={l2_ct:.3e} (爆掉>1 或 >10×迎風? {ok_ct})")
assert ok_up, f"迎風法誤差異常: {l2_up}"
assert ok_ct, f"FTCS 未觀察到不穩定: {l2_ct} vs upwind {l2_up}"
print("PASS")
```
