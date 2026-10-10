# 2017：百維迷宮脫逃——Deep BSDE 探案

> 「網格法在百維空間裡，連第一個路口都走不出去。」——維度災難案的現場勘查筆錄。

| 案件檔案 | 內容 |
|----------|------|
| 案號 | DBSDE-2017-003 |
| 案發時間 | 2017 年 arXiv 立案（2018 年正式發表） |
| 案發地點 |  $100$  維拋物型偏微分方程的迷宮 |
| 報案人 | 高維金融衍生品、隨機控制與物理學家 |
| 偵探 | Weinan E、Jiequn Han、Arnulf Jentzen |
| 兇器 | 維度災難：網格複雜度按  $h^{-d}$  爆炸 |
| 破案工具 | 倒向隨機微分方程＋深度神經網路 |
| 戰績 | 百維 Black–Scholes、Hamilton–Jacobi–Bellman 一網打盡 |
| 狀態 | 已結案，科學機器學習大門洞開 |

## 案發現場

二十世紀末，Pardoux 與 Peng 留下一份遺產：倒向隨機微分方程（BSDE）。

它說，一大類半線性拋物型偏微分方程的解，可以表示為某個倒向系統的初值。

考慮終值問題：

$$
\partial_t u + \frac{1}{2} \mathrm{Tr}(\sigma \sigma^{\top} \mathrm{Hess}_x u) + \mu \cdot \nabla_x u + f(t, x, u, \sigma^{\top} \nabla_x u) = 0
$$

終端條件為  $u(T,x) = g(x)$  ，其中  $u = u(t,x)$  是未知函數， $x \in \mathbb{R}^d$  是高維變量。

Feynman–Kac 與 Pardoux–Peng 告訴我們，若  $X_t$  服從前向擴散，則  $Y_t = u(t, X_t)$  與  $Z_t = \sigma^{\top} \nabla_x u(t, X_t)$  滿足：

$$
dX_t = \mu(t, X_t) dt + \sigma(t, X_t) dW_t
$$

$$
-dY_t = f(t, X_t, Y_t, Z_t) dt - Z_t^{\top} dW_t
$$

其中  $W_t$  是  $d$  維布朗運動， $Y_T = g(X_T)$  是已知的終點。

理論很美，現實很殘酷：當  $d = 100$  時，有限差分網格需要  $N^{100}$  個點，蒙地卡羅迴歸的基函數也會爆炸。

案發現場的白板上寫著一行絕望的算式：若每維取  $10$  個點，則百維需要  $10^{100}$  個網格，超過宇宙原子總數。

傳統稀疏網格、最小二乘蒙地卡羅在  $d \le 10$  尚可掙扎，到了  $d = 100$  全軍覆沒。

報案人的訴求很簡單：給我一個能在多項式時間內算出  $u(0, x_0)$  的方法。

## 偵查過程

三位偵探的靈感來自一次角色互換：如果把 BSDE 看成控制問題呢？

他們注意到， $Z_t$  的本質是「對沖策略」或「控制」，而  $Y_0$  是待定的初始資本。

於是把求解 BSDE 改寫為：尋找初值  $y_0 \in \mathbb{R}$  與反饋策略  $Z_t = \phi(t, X_t)$  ，使得終端誤差最小：

$$
\inf_{y_0, \phi} \mathbb{E} [|Y_T^{\phi} - g(X_T)|^2]
$$

其中  $(X, Y^{\phi})$  服從前向耦合系統：

$$
X_{t_{n+1}} = X_{t_n} + \mu(t_n, X_{t_n}) \Delta t + \sigma(t_n, X_{t_n}) \Delta W_n
$$

$$
Y_{t_{n+1}}^{\phi} = Y_{t_n}^{\phi} - f(t_n, X_{t_n}, Y_{t_n}^{\phi}, \phi(t_n, X_{t_n})) \Delta t + \phi(t_n, X_{t_n})^{\top} \Delta W_n
$$

這一步是神來之筆：原本倒著解的方程，被轉成順著模擬、正著優化的隨機控制問題。

第二步更大膽：用神經網路參數化策略  $\phi$  。

他們為每個時間層  $t_n$  配備一個前饋子網路  $\phi_n(\cdot ; \theta_n)$  ，整條時間鏈構成一個深度殘差結構。

損失函數就是終端均方誤差：

$$
L(\theta) = \mathbb{E} [|Y_T(\theta) - g(X_T)|^2]
$$

以隨機梯度下降（SGD 及其變體）訓練，配合批量布朗路徑模擬，即可逼近真解。

偵探們在論文中展示了令人咋舌的戰績表：

| 測試方程 | 維度  $d$  | 相對誤差 | 運行時間 |
|----------|------------|----------|----------|
| Allen–Cahn 型 |  $100$  |  $0.3\%$  | 數分鐘（GPU） |
| Hamilton–Jacobi–Bellman |  $100$  |  $0.5\%$  | 數分鐘（GPU） |
| Black–Scholes  basket |  $100$  |  $0.4\%$  | 數分鐘（GPU） |
| 非線性 Burgers 型 |  $50$  |  $0.6\%$  | 數分鐘（GPU） |

作為對照，任何網格法在  $d = 100$  的欄位只能填上「宇宙熱寂前算不完」。

第三步是理論辯護：為什麼神經網路能逃出維度災難？

偵探們指出，解的梯度  $\nabla_x u$  在許多問題中具有低複雜度的複合結構，而深度網路對這類函數的逼近率與  $d$  呈多項式關係，而非指數關係。

後續 Jentzen 等人的分析進一步證明，對一類 Black–Scholes 與 Allen–Cahn 方程，存在參數量按  $d^p$  增長的網路達到精度  $\varepsilon$  。

下表整理了新舊辦案手法的對比：

| 手法 | 複雜度對  $d$  的依賴 | 適用維度 | 備註 |
|------|----------------------|----------|------|
| 有限差分 |  $O(h^{-d})$  |  $d \le 3$  | 指數爆炸 |
| 稀疏網格 |  $O(N (\log N)^{d-1})$  |  $d \le 10$  | 常數仍大 |
| 最小二乘蒙地卡羅 | 基函數數按  $d^k$  膨脹 |  $d \le 20$  | 高維基難選 |
| Deep BSDE（本案） |  $O(d^p)$  經驗多項式 |  $d = 100$  | 靠網路表達力與 SGD |

值得注意的是，本案把  $Z_t$  學出來，等於順手得到了對沖比率  $\nabla_x u$  ，這是金融應用夢寐以求的副產品。

## 結案報告

2017 年 arXiv 編號一經貼出，高維偏微分方程社群連夜改寫了授課大綱。

本案的定罪有三重意義。

第一，它證明 BSDE 不只是理論表示工具，更是可計算的控制問題：倒著的方程可以正著練。

第二，它首次在百維非線性方程上展示了  $1\%$  以內的精度，終結了「深度學習只能做分類」的偏見。

第三，它催生了整個科學機器學習分支：Deep Galerkin、Physics-Informed Neural Networks、Deep Ritz 隨後蜂擁而至，Feynman–Kac 街道從此車水馬龍。

當然，懸念並未完全消除：本案的收斂理論在 2017 年尚不完整，SGD 的非凸優化也缺乏保證。

但正如探長 E 在結案記者會上所說：「我們先證明了逃出迷宮是可能的，至於最短路徑，留給下一代測量員。」

此案之後，百維不再是禁區，而是一個邀請函。

## 證據與工具

核心證物一：BSDE 表示  $Y_t = u(t, X_t)$  與  $Z_t = \sigma^{\top} \nabla_x u$  ，連接偏微分方程與隨機系統的臍帶。

核心證物二：控制重構  $\inf \mathbb{E}|Y_T - g(X_T)|^2$  ，把倒向問題轉為前向優化。

核心證物三：分層子網路  $\phi_n(\cdot ; \theta_n)$  與損失  $L(\theta)$  ，百維實驗的全部彈藥。

| 工具 | 用途 | 出處 |
|------|------|------|
| BSDE 理論 | 高維線性與半線性表示 | Pardoux–Peng 1990 |
| Euler 離散  $\Delta W_n$  | 前向路徑批量模擬 | 本案第 3 節 |
| 全連接子網路  $\phi_n$  | 參數化梯度策略  $Z_t$  | E–Han–Jentzen 2017 |
| Adam／SGD | 最小化終端誤差  $L(\theta)$  | 機器學習標準配備 |
| 後驗誤差估計 | 用  $L(\theta)$  大小反推精度 | Han–Jentzen–E 後續工作 |

辦案守則：遇到高維先別佈網格，先問它有沒有隨機表示；若有，就把它變成控制問題，再交給神經網路去練。

## 補充：程式實作

### 對應程式

本節對應程式為 [1990-linear_bsde.py](_code/1990-linear_bsde.py) ，以一維線性 BSDE 的最小平方蒙地卡羅示範倒向方程如何正著解，本程式與 1990 年 BSDE 倒向方程篇共用，此處從高維 Deep BSDE 的角度解讀。

### 理論呼應

本文把半線性偏微分方程化為倒向系統 $Y_t = u(t, X_t)$ 與 $Z_t = \sigma^{\top} \nabla_x u$ 關係。
程式處理一維線性特例，終值 $\xi = \sin(W_T)$ 配合 $f = -rY$ 仍服從同一表示結構。
它用最小平方迴歸逼近條件期望，正是 Deep BSDE 以神經網路參數化 $Z_t = \phi(t, X_t)$ 策略的前身。
此一維可驗證案例相當於 Deep BSDE 降維到一維的經典對照，誤差判準則呼應損失 $L(\theta)$ 思想。

### 執行方式

在 `隨機微積分` 目錄下執行 `python3 _code/1990-linear_bsde.py` 即可重現結果，只需 numpy。

### 實測輸出

```text
Y0_true = 0.000000
Y0_lsmc = 0.002081
abs_err_Y0 = 0.002081 (tol 0.02)
RMSE@t=0.5 = 0.003550 (tol 0.05)
VERIFY Y0_abs_err=0.002081 rmse_half=0.003550
```

初值絕對誤差僅 $0.002081$ 且中段 RMSE 僅 $0.003550$ ，雙雙通過容忍門檻。

### 讀者實驗

將時間切分 `N = 20` 改為 `N = 40` 後重跑，觀察初值誤差 $0.002081$ 是否進一步下降。

完整程式如下：

```python
"""1990 線性 BSDE：最小平方蒙地卡羅 (LSMC) vs 解析解。
對應 wiki：Pardoux–Peng (1990) BSDE 解存在唯一；線性 BSDE 顯式解
  Y_t = E[ ξ * exp(-r(T-t)) | F_t ]（此處 f = -rY, b = 0）。
本檔：終值 ξ = sin(W_T), T = 1, r = 0.05, W 為標準布朗運動。
解析：E[sin(W_T)|F_t] = sin(W_t) exp(-(T-t)/2)，故
  Y_t = sin(W_t) exp(-(r+0.5)(T-t))，特別 Y_0 = 0。
數值：向後 Euler 隱式格式 Y_k = E[Y_{k+1}|F_k] / (1+r dt)，
條件期望以 W_k 的 5 次多項式基函數最小平方迴歸近似。
驗證：Y_0 真值為 0，「誤差 < 2%」採絕對誤差 |Y0_hat| < 0.02
（尺度：ξ∈[-1,1]，2% 尺度即 0.02）；另檢 t=0.5 路徑 RMSE < 0.05。
只用 numpy，固定種子，不畫圖。
"""
import numpy as np

rng = np.random.default_rng(0)
r = 0.05
T = 1.0
N = 20
dt = T / N
M = 100000
DEG = 5

dW = np.sqrt(dt) * rng.standard_normal((M, N))
W = np.zeros((M, N + 1))
W[:, 1:] = np.cumsum(dW, axis=1)

Y_next = np.sin(W[:, N])
Y_at_half = None
HALF_K = N // 2  # t = 0.5

for k in range(N - 1, 0, -1):
    Wk = W[:, k]
    X = np.vander(Wk, DEG + 1, increasing=True)  # [1, w, ..., w^5]
    beta, *_ = np.linalg.lstsq(X, Y_next, rcond=None)
    Yk = (X @ beta) / (1.0 + r * dt)
    if k == HALF_K:
        Y_at_half = Yk.copy()
    Y_next = Yk  # Y_1 的各路徑估計

Y0_hat = float(np.mean(Y_next) / (1.0 + r * dt))
Y0_true = 0.0
abs_err = abs(Y0_hat - Y0_true)

# t = 0.5 解析解對照（非退化檢驗）
t_half = HALF_K * dt
Y_true_half = np.sin(W[:, HALF_K]) * np.exp(-(r + 0.5) * (T - t_half))
rmse_half = float(np.sqrt(np.mean((Y_at_half - Y_true_half) ** 2)))

print(f"Y0_true = {Y0_true:.6f}")
print(f"Y0_lsmc = {Y0_hat:.6f}")
print(f"abs_err_Y0 = {abs_err:.6f} (tol 0.02)")
print(f"RMSE@t=0.5 = {rmse_half:.6f} (tol 0.05)")
print(f"VERIFY Y0_abs_err={abs_err:.6f} rmse_half={rmse_half:.6f}")
assert abs_err < 0.02, f"Y0 誤差過大: {abs_err}"
assert rmse_half < 0.05, f"t=0.5 RMSE 過大: {rmse_half}"
```
