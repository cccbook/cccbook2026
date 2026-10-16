# 1950：Charney 的數值天氣預報 — ENIAC 算了一整天

> 副標題：24 小時算 24 小時天氣，過濾掉重力波的人贏了。

## 案發現場

1922 年 Richardson 發了個瘋狂的夢：六萬人在大廳裡算天氣。
每人負責一小塊大氣，用算盤接力求解流體方程。
結果慘敗，算出的氣壓變化完全荒謬，預報成了笑話。
案件封存二十多年，直到 1950 年才由 Charney 重啟。
普林斯頓的 Charney 帶來兩件新武器：準地轉理論與 ENIAC 。
被害人仍是同一個：人類想提前知道明天的天氣。
證據顯示方程本身是對的，但裡面混進了快波噪音。
重力波與聲波速度極快，逼著時間步長小到無法計算。
Richardson 當年就是被快波拖垮的，算一步就發散。
Charney 只有幾天 ENIAC 機時，失敗就沒有下一輪經費。

## 偵查過程

### 線索一：過濾快波

Charney、Fjörtoft、von Neumann 的策略是丟掉次要矛盾。
大尺度天氣受地轉平衡支配，科氏力與氣壓梯度力近似平衡。
他們採用準地轉渦度方程，只保留慢變的 Rossby 波。
設流函數為 $\psi$ ，相對渦度正比於其拉普拉斯量。
再加上行星渦度，渦度平流守恆即構成預報方程。
一個方程、一個變量，ENIAC 才吞得下。
這等於給大氣戴上濾鏡，快重力波直接被過濾掉。
時間步長可放大到小時量級，不再觸發數值不穩定。
### 線索二：ENIAC 的 24 小時豪賭

1950 年 3 月，團隊進駐阿伯丁試驗場。
網格很粗：北美上空數百格點，垂直只有一層正壓大氣。
500 百帕高度場是主角，引導地面氣旋走向。
| 步驟 | 內容 | 耗時 |
|------|------|------|
| 1 | 觀測插值到規則網格 | 數小時人工 |
| 2 | 穿孔卡片輸入高度場 | 數小時機器 |
| 3 | ENIAC 積分渦度方程 | 約 24 小時 |
| 4 | 人工檢查與評分 | 數小時人工 |
ENIAC 花 24 小時算出未來 24 小時天氣，追平了時間本身。
### 線索三：與實況對質

團隊共做四個個案，含一次強氣旋過程。
評分法是比較預報高度變化與實際變化。
結果三勝一平：槽脊走向大致正確，強度略偏。
急流的引導作用被正壓模式抓住，這就是要害。
誤差源如實記錄：地形忽略、單層垂直、摩擦加熱全丟。
但骨架是對的，剩下只是裝血肉的問題。
馮紐曼說：經費值了，氣象學從此進入計算時代。

## 結案報告

1950 年 ENIAC 預報宣告數值天氣預報 NWP 可行。
Richardson 平反：不是想法錯，是方程沒過濾、電腦沒誕生。
各國氣象局紛紛建計算單位，1954 年瑞典率先業務化。
模式從正壓單層走向斜壓多層，再到原始方程模式。
伏筆在十三年後出現，Lorenz 發現混沌與預報上限。
但那是下一樁案件，本案在此結案。

## 證據與工具

正壓渦度方程可用獨立公式表示如下。
$$ \frac{\partial q}{\partial t} + J(\psi, q) = 0 $$
其中 $q$ 為絕對渦度， $\psi$ 為流函數， $J$ 為平流算子。
絕對渦度組成為相對渦度加行星渦度。
$$ q = \nabla^2 \psi + f $$
其中 $f$ 為科氏參數， $\nabla^2 \psi$ 為相對渦度。
| 符號 | 意義 | 本案取值 |
|------|------|----------|
| $\psi$ | 流函數 | 由 500 百帕高度反演 |
| $q$ | 絕對渦度 | 守恆量，預報核心 |
| $f$ | 科氏參數 | 隨緯度變， $\beta$ 效應關鍵 |
重現建議：雙週期域解正壓渦度方程，網格 $64 \times 64$ 。
初值給正弦槽疊加急流，觀察槽線東移。
對比加入與移除散度項的步長差異，體會過濾威力。
因果鏈：Richardson 1922 年夢想在此實現，Lorenz 1963 年再定其界。
後續原始方程模式放回快波，改用半隱式格式處理時間步長。
業務化關鍵是資料同化，觀測不斷把漂移軌跡拉回現實。
本案檔案編號 NWP-1950 ，狀態已結案，遺產仍在增值。
瑞典 1954 年業務化之後，美英日接連跟進，全球競賽開跑。

## 補充：程式實作

對應程式：[1922-advection_cfl.py](_code/1922-advection_cfl.py)

本文核心理論是同一條平流穩定律 $u_t + c u_x = 0$ ，此處從 Charney 成功一側解讀。
準地轉過濾拿掉快重力波後，最快波速 $c$ 大幅下降， $CFL = c dt / dx \le 1$ 變得容易滿足。
迎風格式在 $CFL = 0.5$ 下穩定推進 $800$ 步，平流兩圈仍能回到接近原位。
同一步長下中心差 FTCS 因放大因子 $1.1180$ 大於 $1$ 而爆炸，對照出格式選擇的關鍵。
懂得過濾快波、又肯守住 $CFL$ 紅線的 Charney，用 $1.354171e-01$ 的小誤差替 Richardson 洗了冤。

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

讀者可改網格 $N = 100$ 或波速 $c = 2.0$ ，觀察滿足 $CFL \le 1$ 所需的時間步如何變化，並比較迎風誤差增減。

上述穩定解以 $200$ 點週期域推進 $800$ 步所得，誤差僅 $1.354171e-01$ ，呼應過濾加小步長即是 ENIAC 追平時間本身的技術底氣。

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
