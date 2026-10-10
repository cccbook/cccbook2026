# 1998・Lyons 粗糙路徑：Hölder 指數小於二分之一的世界

> 「布朗運動已經夠粗糙了，Lyons 卻說：還能更粗。」
> 本案時間：1998 年，地點：英國牛津與倫敦，報案人：被  $p$  變差難住的分析學家。

| 案件檔案 | 內容 |
|----------|------|
| 案號 | RP-1998-Lyons |
| 年份 | 1998 年 |
| 主角 | Terry Lyons |
| 關鍵文獻 | Differential Equations Driven by Rough Signals（1998） |
| 涉案對象 |  $p$  變差、signature、Hölder 指數  $\alpha < 1/2$  |
| 核心證物 | signature 提升、Itô–Lyons 連續性定理、 Universal Limit 定理 |
| 關聯舊案 | 1923 年 Wiener 過程、1951 年 Itô 公式、2014 年 Hairer 正則結構 |
| 遺產 | 粗糙波動、機器學習 signature 特徵、隨機偏微分方程新解法 |

## 案發現場

1990 年代末，隨機分析撞上了一面看不見的牆。

Itô 積分要求被積函數適應、積分路徑是半鞅。布朗運動的 Hölder 指數恰為  $1/2$  以下，勉強還能用 Itô 機制馴服。可一旦噪聲比布朗更粗——分數布朗  $H < 1/2$ 、物理近似的光滑逼近取極限結果飄移——Itô 機制當場失效。Wong–Zakai 近似告訴大家：用光滑路徑逼近布朗，極限未必是 Itô 解，可能是 Stratonovich 解。極限依賴逼近方式，這在古典分析裡是不可饒恕的醜聞。

更深的病灶是「路徑」本身。Itô 解映射  $W \mapsto X$  在一致拓撲下不連續：兩條肉眼難分的布朗路徑，可以解出差很遠的  $X$ 。這意味著隨機微分方程的解不是路徑的連續函數，數值逼近與穩定性都站在流沙上。

Lyons 是研究 perurbation 與大偏差出身的分析學家。他盯著 Chen 在 1950 年代留下的 signature（路徑的迭代積分序列），心裡浮現一個大膽的猜想：與其抱怨路徑太粗，不如給路徑「升級」——把高階迭代積分一起打包， head 進一個更大的空間，解映射在那裡恢復連續。

1998 年，粗糙路徑理論橫空出世。

## 偵查過程

偵探的第一步，是給「粗糙」定罪量刑。對路徑  $x$ ，定義  $p$  變差度量， $p$  越大容忍越粗：

$$
\|x\|_{p} = \sup_{\mathcal{P}}\left(\sum \lvert x_{t_{i+1}} - x_{t_i}\rvert^p\right)^{1/p}
$$

布朗運動的  $p$  變差有限當且僅當  $p > 2$ 。這正是本案的立案標準： $p > 2$  的世界，Young 積分（要求  $p < 2$ ）已死，Itô 機制岌岌可危，新理論必須接管。

第二步是關鍵證物：signature 提升。對光滑路徑，定義其截斷 signature 為迭代積分全家桶：

$$
S(x) = \left(1, \int dx, \iint dx \otimes dx, \dots\right)
$$

粗糙路徑就是「帶著高階積分一起出庭的路徑」。一條  $p$  粗糙路徑，攜帶  $\lfloor p \rfloor$  層迭代積分： $2 < p < 3$  時帶一階增量與二階「面積」， $p$  更大則帶更多層。Lévy 面積不再是數值惡夢，而是路徑身分證的一部分。

下表是粗糙度與裝備的對照，供探員按圖索驥：

| 粗糙度 | 例子 | 所需層數 | 積分機制 |
|--------|------|----------|----------|
|  $p < 2$  | 有限變差、光滑 | 一層 | Young／Riemann–Stieltjes |
|  $2 < p < 3$  | 布朗運動 | 兩層（含面積） | Itô／Stratonovich 皆可嵌入 |
|  $3 \le p < 4$  | 分數布朗  $H \in (1/4, 1/3]$  | 三層 | 必須粗糙積分 |
|  $p \ge 4$  | 更粗噪聲 | 更多層 | Lyons 層級逐層加碼 |

第三步是全案高潮：Itô–Lyons 連續性（Universal Limit 定理）。設驅動信號為粗糙路徑  $\mathbf{x}$ ，考慮受控微分方程：

$$
dY = V(Y)\,d\mathbf{x}
$$

則解映射  $\mathbf{x} \mapsto Y$  在粗糙路徑拓撲下連續且可延拓。白話翻譯：只要把面積等高階資訊一起比較，解就不再亂跳；光滑逼近的極限由提升後的極限唯一決定，Wong–Zakai 的歧義一次性澄清——Itô 與 Stratonovich 只是同一粗糙路徑的不同提升。

一個具體的驗屍：布朗運動提升為 Itô 型或 Stratonovich 型粗糙路徑，兩者差一個確定的漂移修正  $\tfrac{1}{2}I$ 。Lyons 框架下，這不再是哲學爭論，而是同一個 signature 空間裡的兩個點。

本案還埋下一條 2014 年的伏筆。當  $p$  大到連 Lyons 層級都吃力、噪聲成為時空分佈（如 KPZ 的白噪聲），signature 得換成 Hairer 的正則結構模型。粗糙路徑是前傳，正則結構是續集。

## 結案報告

1998 年一案，把「對路徑連續依賴」還給了隨機分析。

從此，SDE 的穩定性、數值格式的收斂、大偏差與支撐定理，都可以在確定性的粗糙拓撲裡重證一遍，不必每次都回頭求助機率。Friz 與 Hairer、Friz 與 Wik 的教科書隨後把這套語言標準化，機器學習更把截斷 signature 拿去當時間序列特徵，在手寫辨識與金融預測上大放異彩。

在歷史年表裡，本案上承 1923 年 Wiener 的嚴格構造，下啟 2014 年 Hairer 與 Rough Volatility。Wiener 證明布朗路徑連續卻無處可微，Lyons 證明即使 Hölder 指數  $\alpha < 1/2$  ，微分方程依然可以有條不紊地被驅動。

案件狀態：已破案，粗糙之路已鋪平，歡迎攜帶面積上路。

## 證據與工具

證物一，Hölder 與  $p$  變差換算。 $\alpha$ -Hölder 路徑具有有限  $p$  變差對一切  $p > 1/\alpha$ ：

$$
\alpha < \frac{1}{2} \;\Longleftrightarrow\; p > 2
$$

布朗運動  $\alpha = 1/2^-$ ，分數布朗  $\alpha = H^-$ 。看到  $H = 0.1$  的粗糙波動，就知道它住在  $p \approx 10$  的深粗區。

證物二，粗糙積分速寫。對受控粗糙路徑  $(Y, Y')$ ，積分由補償 Riemann 和定義：

$$
\int Y\,d\mathbf{x} = \lim_{\lvert\mathcal{P}\rvert \to 0}\sum \left(Y_i\,\delta x_i + Y'_i\,\mathbb{X}_i\right)
$$

其中  $\mathbb{X}$  為二階提升。记住：少了面積項，和就不收斂。

證物三，工具與實驗對照表：

| 工具 | 用途 | 備註 |
|------|------|------|
| signature 截斷特徵 | 時間序列分類 | 階數越高表達力越強，維度指數膨脹 |
| Lyons 提升 | 判定 Itô／Stratonovich | 差一個  $1/2$  修正 |
| 分形標度檢驗 | 估 Hölder／Hurst | 對應程式  `_code/1998-fbm_hurst.py`  驗  $t^{2H}$  |

探員格言：路徑不帶面積出庭，證詞一律視為不完整。先問  $p$  ，再問層數，最後才寫方程。

## 補充：程式實作

### 對應程式

本節對應程式為 [1998-fbm_hurst.py](_code/1998-fbm_hurst.py) ，以 Cholesky 分解生成分數布朗運動路徑，並用變異數標度迴歸估計 Hurst 指數。

### 理論呼應

本文以 $p$ 變差與 Hölder 指數 $\alpha$ 刻畫粗糙度，判準為 $\alpha < 1/2$ 對應 $p > 2$ 之情形。
程式直接驗證分數布朗運動的自相似律 $Var B(t) = t^{2H}$ 關係，並以對數迴歸斜率還原 $2H$ 數值。
當 $H = 0.1$ 路徑落在深粗區，Young 積分失效，正是 Lyons 要求攜帶面積 $\mathbb{X}$ 出庭的情形。
而 $H = 0.7$ 對照組回到較光滑一側，呼應文中粗糙度與層數對照表及 $t^{2H}$ 標度檢驗。

### 執行方式

在 `隨機微積分` 目錄下執行 `python3 _code/1998-fbm_hurst.py` 即可重現結果，只需 numpy。

### 實測輸出

```text
H = 0.1: slope = 0.2264, target 2H = 0.2000, err = 0.0264
H = 0.7: slope = 1.4560, target 2H = 1.4000, err = 0.0560
VERIFY slope_H01=0.2264 slope_H07=1.4560
```

兩組斜率誤差皆小於容忍值 $0.15$ ，確認標度律成立。

### 讀者實驗

將 `Hs = (0.1, 0.7)` 改為 `(0.3, 0.5)` 並重跑，觀察斜率是否仍緊貼 $2H$ 目標值。

完整程式如下：

```python
"""1998 分數布朗運動 Hurst 估計（Cholesky 生成）。
對應 wiki：Mandelbrot–Van Ness (1968) fBM 定義；此處驗證自相似性
  Var B(t) = t^{2H}，即 log Var 對 log t 斜率 = 2H。
生成：時格 t_i = i/N (N=256，含 0 共 257 點)，
  共變異 C(s,t) = (s^{2H}+t^{2H}-|t-s|^{2H})/2，Cholesky L，路徑 = L z。
實驗：H = 0.1 與 0.7，各 500 條；逐 t 樣本變異數，
  線性迴歸 log Var ~ log t 得斜率，容忍 |slope - 2H| < 0.15。
只用 numpy，固定種子，不畫圖。
"""
import numpy as np

rng = np.random.default_rng(3)
N = 256
M = 500
Hs = (0.1, 0.7)
t = np.arange(N + 1) / N  # 含 0

slopes = {}
for H in Hs:
    p = 2.0 * H
    ti = t[:, None]
    tj = t[None, :]
    C = 0.5 * (ti ** p + tj ** p - np.abs(ti - tj) ** p)
    C += 1e-12 * np.eye(N + 1)  # 數值 jitter（H=0.1 時近奇異）
    L = np.linalg.cholesky(C)
    Z = rng.standard_normal((N + 1, M))
    paths = L @ Z  # (257, 500)
    var_t = np.var(paths[1:, :], axis=1, ddof=1)  # 去掉 t=0
    logt = np.log(t[1:])
    logv = np.log(var_t)
    slope, intercept = np.polyfit(logt, logv, 1)
    slopes[H] = float(slope)
    print(f"H = {H}: slope = {slope:.4f}, target 2H = {p:.4f}, err = {abs(slope - p):.4f}")

print(f"VERIFY slope_H01={slopes[0.1]:.4f} slope_H07={slopes[0.7]:.4f}")
assert abs(slopes[0.1] - 0.2) < 0.15, f"H=0.1 斜率偏差過大: {slopes[0.1]}"
assert abs(slopes[0.7] - 1.4) < 0.15, f"H=0.7 斜率偏差過大: {slopes[0.7]}"
```
