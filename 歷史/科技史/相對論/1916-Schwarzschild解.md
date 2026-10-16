# 1916-Schwarzschild 解

## 案件摘要
1916 年 1 月，Karl Schwarzschild 在一戰東線戰壕中，於彈藥聲裡求出 Einstein 場方程的第一個精確解。這個解藏著一個詭異的半徑——在 $r_s = 2GM/c^2$ 處時間「凍結」。半世紀的誤解之後，這個「病態」終於被確認為宇宙中最真實的天體：黑洞。

## 前因 -- 為什麼會有這個案子
- **1915 年 12 月**：Einstein 剛發表場方程，只做了近似計算（水星進動）。理論急需一個**精確解**來證明其威力。
- **最簡單的題目**：一顆靜止球對稱質量（太陽的理想化）外部的時空幾何——類似牛頓力學中「球體外部如同點質量」的殼層定理。
- **偵探背景**：Schwarzschild 是波茨坦天文台台長、傑出的理論與觀測天文學家，1914 年開戰即志願入伍，在俄國前線服務。他透過信件收到 Einstein 的論文。

## 線索與推理 -- 數學式、程式、理論

### 1. 求解的設定
要求：靜態、球對稱度規。Schwarzschild 採用球座標寫下最一般的形式，令愛因斯坦方程 $G_{\mu\nu} = 0$（真空）逐分量為零，解一組非線性 ODE。他於 1915 年 12 月 22 日寄給 Einstein，1916 年 1 月 13 日由 Einstein 代為提交普魯士科學院。

### 2. Schwarzschild 度規

$$\boxed{ds^2 = -\left(1-\frac{2GM}{c^2 r}\right)c^2dt^2 + \left(1-\frac{2GM}{c^2 r}\right)^{-1}dr^2 + r^2 d\Omega^2}$$

其中 $d\Omega^2 = d\theta^2 + \sin^2\theta\, d\phi^2$，$M$ 是中心質量。

**性質檢驗**：
- $r \to \infty$ 時退化回閔可夫斯基度規（漸近平坦）。
- 弱場極限 $g_{00} \approx -(1 + 2\Phi/c^2)$ 對應牛頓位能 $\Phi = -GM/r$。
- **Birkhoff 定理**（1923）：此解是球對稱真空的**唯一**解——即使星體脈動，外部時空也不變（故沒有球對稱重力波）。

### 3. 史瓦西半徑與事件視界

$$\boxed{r_s = \frac{2GM}{c^2}}$$

在 $r = r_s$ 處度規出現奇異：
- $g_{tt} \to 0$：外觀測者看見落體的時間**無限減慢**——「**凍結星**」（frozen star）。
- $g_{rr} \to \infty$：徑向距離被無限拉伸。

**「時間奇點」的誤解**：1916–1950 年代，多數物理學家（包括 Einstein 與 Eddington）認為 $r_s$ 是真實奇點，是數學病態，自然界不會出現。Eddington 1926 年甚至說：「應有一自然律阻止星球如此坍縮。」

**釐清**：
- 1933 年 Lemaitre、1960 年 Kruskal 與 Szekeres 分別證明：$r = r_s$ 只是**座標奇點**（如地圖的極點），可透過座標變換移除（Lemaitre 座標、Kruskal–Szekeres 座標）。
- 真實的物理奇點在 $r = 0$，且 $r=0$ 是**類空的未來**——一旦越過視界，$r$ 就像時間一樣只能減小。
- 1967 年 Wheeler 命名「**黑洞**（black hole）」。1958 年 Kruskal 圖、1965 年 Penrose 奇點定理確立了黑洞概念的數學地位。

### 4. Schwarzschild 半徑的數值計算

```python
import numpy as np

G = 6.674e-11       # m^3 kg^-1 s^-2
c = 2.998e8         # m/s

def rs(mass_kg):
    return 2 * G * mass_kg / c**2

bodies = {
    "太陽":     1.989e30,
    "地球":     5.972e24,
    "月球":     7.348e22,
    "太陽→人類質量": 70.0,
    "Sgr A* (銀河系中心黑洞)": 4.3e6 * 1.989e30,
}

for name, m in bodies.items():
    r = rs(m)
    print(f"{name}: r_s = {r:.3e} m = {r/1000:.3e} km")
```

輸出：

| 天體 | 質量 | Schwarzschild 半徑 |
|------|------|--------------------|
| 太陽 | $1.989\times10^{30}$ kg | **2.95 km** |
| 地球 | $5.972\times10^{24}$ kg | **8.87 mm** |
| 月球 | $7.348\times10^{22}$ kg | 0.109 mm |
| 70 kg 的人 | 70 kg | $1.0\times10^{-25}$ m（遠小於普朗克長度） |
| Sgr A* | $4.3\times10^6 M_\odot$ | $\sim 1.27\times10^{10}$ m（約 0.08 AU） |

太陽若壓縮到半徑 3 km 以內、地球壓縮到 9 mm 以內，都會成為黑洞——這說明 $r_s$ 遠小於天體實際半徑，正常情況下視界深藏在星體內部（對太陽而言，太陽半徑 $7\times10^5$ km，視界僅在其 24 萬分之一處）。

### 5. 視界上的詭異：誰的時間？
$g_{tt} = -(1 - r_s/r)c^2$ 意味著：

$$d\tau = \sqrt{1 - \frac{r_s}{r}}\, dt$$

靜止在 $r$ 處的時鐘相對於無窮遠觀測者走得慢。$r \to r_s$ 時 $d\tau \to 0$：從遠方看，落體在視界上**凍結**、光線**紅移至無窮**。但對落體本人，他**在有限原時內平滑穿越視界**——兩個參考系都是對的，這正是廣義相對論的精妙之處。

## 結案 -- 後果與影響
- **第一個精確解**證明了場方程的可解性與威力，直接用於 1919 年光線偏折與水星進動的精確計算。
- 黑洞概念確立後：1963 年 Kerr 解（旋轉黑洞）、1974 年 Hawking 輻射、2015 年 LIGO 偵測雙黑洞併合、2019 年 EHT 拍攝 M87 黑洞影像、2022 年 Sgr A* 影像。
- Schwarzschild 本人的悲劇：論文發表後數月，他於 1916 年 5 月死於前線染上的天皰瘡，年僅 42 歲——他從未知道自己的解會成為 20 世紀物理最重要的遺產之一。

## 關鍵人物與文獻
| 人物 | 角色 |
|------|------|
| Karl Schwarzschild | 戰壕中求出第一個精確解 |
| Albert Einstein | 代為提交論文 |
| Georges Lemaître | 指出視界是座標奇點（1933） |
| Martin Kruskal / George Szekeres | Kruskal 最大延拓圖（1960） |
| John Wheeler | 命名「黑洞」（1967） |
| Roy Kerr | 旋轉黑洞精確解（1963） |

**文獻**
1. Schwarzschild, K. (1916). *Über das Gravitationsfeld eines Massenpunktes*, Sitzungsberichte der Preußischen Akademie der Wissenschaften.
2. Kruskal, M. (1960). *Maximal Extension of Schwarzschild Metric*, Phys. Rev. 119.
3. Thorne, K. (1994). *Black Holes and Time Warps: Einstein's Outrageous Legacy.*
