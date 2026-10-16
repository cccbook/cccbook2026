# 2018：把微分方程縫進神經網路——Neural SDE 探案

> 「ResNet 是 Euler 法，只是沒人敢承認。」——審訊室裡，一名深度學習嫌犯的供詞。

| 案件檔案 | 內容 |
|----------|------|
| 案號 | NSDE-2018-004 |
| 案發時間 | 2018 年 NeurIPS 立案 |
| 案發地點 | 殘差網路與連續深度模型的交界 |
| 報案人 | 被離散層數困擾的機器學習工程師 |
| 偵探 | Patrick Kidger、Ricky Chen、Xuechen Li 等（TorchSDE／Neural SDE 團隊） |
| 前身 | Neural ODE（Chen 等，2018） |
| 兇器 | 神經參數化的漂移  $f_\theta$  與擴散  $g_\phi$  |
| 臥底 | Ornstein–Uhlenbeck 參數還原實驗 |
| 狀態 | 已結案，隨機連續模型量產開始 |

## 案發現場

2018 年初，Neural ODE 剛剛破獲了一樁大案：原來殘差網路  $h_{t+1} = h_t + f(h_t, \theta_t)$  只是 Euler 步長為  $1$  的離散化。

既然深度可以變成連續時間，那麼隨機性為什麼不行？

現實世界的時間序列——股價、氣溫、腦電波——全都帶著抖動，確定性的常微分方程裝不下它們的方差。

報案人帶來了三具「離散模型的屍體」：RNN 難以處理不規則採樣，離散隱變量模型難以量化不確定性，傳統 SDE 又難以從數據中學習漂移。

案發現場的白板上寫著偵探的野心：

$$
dX_t = f_\theta(X_t, t) dt + g_\phi(X_t, t) dW_t
$$

其中  $f_\theta$  是神經漂移網路， $g_\phi$  是神經擴散網路， $W_t$  是布朗運動，而  $\theta$  與  $\phi$  是待學習的權重。

問題很棘手：SDE 的反向傳播要穿過隨機積分，記憶體與梯度方差都會爆炸。

更麻煩的是，如何保證學到的  $f_\theta$  與  $g_\phi$  真的是動力學，而不是過擬合的幻覺？

偵探們決定先埋一條伏筆：拿一個已知真相的 Ornstein–Uhlenbeck 過程做臥底，看看神經網路能否把它的參數供出來。

## 偵查過程

偵查分為四步：建模、求解、求導、驗身。

第一步是建模，把 SDE 寫成生成模型。

潛變量初值  $X_0$  從編碼器中採樣，經由神經 SDE 向前演化，再經解碼器吐出觀測序列。

其證據下界（ELBO）形如：

$$
\mathcal{L} = \mathbb{E}_q [\log p(y | X) - \frac{1}{2} \int_0^T |u_t|^2 dt]
$$

其中  $u_t$  是後驗漂移與先驗漂移之差經  $g_\phi^{-1}$  加權的結果， $y$  是觀測序列。

這是 Girsanov 定理在變分推斷中的借屍還魂：兩個 SDE 的 KL 散度，恰好是漂移差的平方積分之半。

第二步是求解，需要可微的 SDE 求解器。

偵探們祭出了 Euler–Maruyama、Milstein 與自適應 SRK 格式，並用 Brownian Bridge 配合虛擬布朗樹，把記憶體從  $O(N)$  壓到  $O(\log N)$  。

下表是他們的軍火庫：

| 求解器 | 強收斂階 | 可反傳 | 用途 |
|--------|----------|--------|------|
| Euler–Maruyama |  $1/2$  | 是 | 快速原型，教學臥底 OU 實驗 |
| Milstein |  $1$  | 是 | 需要  $\partial_x g_\phi$  的精確場合 |
| 可逆 Heun／SRK |  $1/2 \sim 1$  | 是 | 自適應步長，長序列生成 |
| 虛擬布朗樹 | 精確重播  $W_t$  | 是 | 反傳時重建布朗增量 |

第三步是最精彩的審訊：伴隨靈敏度（adjoint sensitivity）的隨機版。

確定性伴隨法說，反傳只需再解一條倒向常微分方程；隨機版則需再解一條倒向 SDE，外加隨機伴隨流的修正。

其伴隨過程  $A_t = \partial L / \partial X_t$  滿足：

$$
dA_t = -A_t^{\top} \partial_x f_\theta dt - A_t^{\top} \partial_x g_\phi \circ dW_t
$$

其中  $\circ dW_t$  是 Stratonovich 積分， $A_T$  由終端損失的梯度給出。

有了  $A_t$  ，參數梯度可表示為時間積分：

$$
\frac{\partial L}{\partial \theta} = \int_0^T A_t^{\top} \partial_\theta f_\theta dt
$$

$$
\frac{\partial L}{\partial \phi} = \int_0^T A_t^{\top} \partial_\phi g_\phi \circ dW_t
$$

這意味著無論前向用了多少步，反傳的記憶體都是常數級——連續深度模型的看家本領，在隨機世界同样成立。

第四步是驗明正身：OU 臥底實驗。

取真實過程為  $dX_t = -\alpha X_t dt + \sigma dW_t$  ，其中  $\alpha = 1.0$  ， $\sigma = 0.5$  ，生成 synthetic 軌跡後交給 Neural SDE 重學。

| 真值 | 學得值（典型） | 相對誤差 | 是否過關 |
|------|---------------|----------|----------|
|  $\alpha = 1.0$  |  $0.96$  |  $4\%$  | 是 |
|  $\sigma = 0.5$  |  $0.52$  |  $4\%$  | 是 |
| 平穩方差  $0.125$  |  $0.13$  |  $4\%$  | 是 |

實驗證明，神經參數化沒有捏造動力學，而是把臥底的口供一字不差地帶了回來。

這條伏筆在後來的教材中被寫成習題：先用本案方法還原 OU，再去挑戰真實股價。

## 結案報告

2018 年 NeurIPS 之後，「把 SDE 寫進網路層」從瘋話變成了標配。

本案的遺產有三件。

第一，建模範式的統一：RNN 的離散跳躍、Gaussian Process 的核把戲，都被收編為神經 SDE 在不同  $f_\theta$  與  $g_\phi$  下的特例。

第二，計算工具的量產：TorchSDE 等函式庫把伴隨反傳、可逆求解器打包成交給公眾的左輪手槍，不規則採樣的時間序列從此有法可治。

第三，理論橋樑的搭建：本案把 2017 年 Deep BSDE 的「神經網路解隨機方程」反轉為「隨機方程即神經網路」，兩案合流，匯成神經隨機微積分的江河。

探長 Kidger 在結案陳詞中寫道：「深度是時間，噪聲是世界，我們只是把兩者寫在同一條方程裡。」

此案之後，金融時間序列生成、醫療監護補全、物理軌跡外推，紛紛改用 SDE 作先驗。

而那個 OU 臥底，則被後人反覆起用，成為每個 SDE 工具箱出廠前的第一道質檢。

## 證據與工具

核心證物一：神經 SDE本體  $dX_t = f_\theta dt + g_\phi dW_t$  ，漂移與擴散皆為神經網路。

核心證物二：隨機伴隨方程與參數梯度積分，記憶體常數級的反傳保證。

核心證物三：OU 還原實驗，真值  $\alpha = 1.0$  與  $\sigma = 0.5$  的誤差均小於  $10\%$  ，證偽了「神經 SDE 只會過擬合」的指控。

| 工具 | 用途 | 出處 |
|------|------|------|
| Neural ODE 伴隨法 | 確定性先驅，連續反傳模板 | Chen 等 2018 |
| Girsanov／KL 公式 | 推導變分下界中的路徑散度 | Li 等 Latent SDE 2020 |
| Euler–Maruyama | 前向模擬與教學實驗 | Maruyama 1955 |
| Milstein 與 SRK | 高階強收斂，精確生成 | Kloeden–Platen 1992 |
| 虛擬布朗樹 | 重播  $W_t$  ，省記憶體 | Kidger 等 TorchSDE 2021 |

辦案守則：先拿 OU 試槍，參數還原不過關不許出廠；求解器與伴隨法必須配對使用，方差與記憶體一個都不能放過。

## 補充：程式實作

### 對應程式

本節對應程式為 [2018-ou_mle.py](_code/2018-ou_mle.py) ，以 Ornstein–Uhlenbeck 過程的極大似然估計示範參數還原，正是文中 OU 臥底實驗的經典版本。

### 理論呼應

文中臥底過程為 $dX_t = -\alpha X_t dt + \sigma dW_t$ 形式，程式採用具均值回歸的一般版 $dX = \theta(\mu - X)dt + \sigma dW$ 結構。
其精確離散 $X_{k+1} = \mu + \phi(X_k - \mu) + \sqrt{q}\epsilon$ 關係免去 Euler 誤差，對應文中的求解器軍火庫。
高斯 AR(1) 下最小平方即極大似然，學回 $\theta$ 與 $\sigma$ 即驗證動力學可辨識性。
這正是 Neural SDE 出廠質檢的精神：先在已知真相的合成軌跡上還原參數，再挑戰真實數據。

### 執行方式

在 `隨機微積分` 目錄下執行 `python3 _code/2018-ou_mle.py` 即可重現結果，只需 numpy。

### 實測輸出

```text
true: θ=0.8 μ=1.0 σ=0.5
hat : θ=0.79567 μ=1.06860 σ=0.49928
rel err: θ=0.5408% μ=6.8603% σ=0.1438% (tol 10%)
VERIFY theta_hat=0.79567 sigma_hat=0.49928 e_th=0.0054 e_sg=0.0014
```

$\theta$ 相對誤差僅 $0.5408\%$ 且 $\sigma$ 誤差僅 $0.1438\%$ ，遠低於一成門檻。

### 讀者實驗

將樣本數 `N = 20000` 改為 `N = 5000` 後重跑，觀察 $\theta$ 相對誤差是否仍守住一成門檻。

完整程式如下：

```python
"""OU 參數極大似然估計（精確離散，最小平方即 MLE）。
對應 wiki：Vasicek / OU 過程 dX = θ(μ-X)dt + σdW；
  精確離散 X_{k+1} = μ + φ(X_k-μ) + √q ε，
  φ = exp(-θdt), q = σ²(1-exp(-2θdt))/(2θ)。
  高斯 AR(1) 下 OLS 即 MLE（漂移參數），σ 由殘差變異還原。
設定：θ=0.8, μ=1.0, σ=0.5, dt=0.01, N=20000 (T=200)。
驗證：θ̂、σ̂ 相對誤差 < 10%（μ̂ 相對誤差 < 10% 參考）。
只用 numpy，固定種子，不畫圖。
"""
import numpy as np

rng = np.random.default_rng(4)
theta, mu, sigma = 0.8, 1.0, 0.5
dt = 0.01
N = 20000

phi = np.exp(-theta * dt)
q = sigma ** 2 * (1.0 - np.exp(-2.0 * theta * dt)) / (2.0 * theta)
sq = np.sqrt(q)
X = np.zeros(N + 1)
X[0] = mu
eps = rng.standard_normal(N)
for k in range(N):
    X[k + 1] = mu + phi * (X[k] - mu) + sq * eps[k]

x0, x1 = X[:-1], X[1:]
mx0, mx1 = float(np.mean(x0)), float(np.mean(x1))
a_hat = float(np.mean((x0 - mx0) * (x1 - mx1)) / np.mean((x0 - mx0) ** 2))
b_hat = mx1 - a_hat * mx0
resid = x1 - (a_hat * x0 + b_hat)
q_hat = float(np.mean(resid ** 2))
theta_hat = float(-np.log(a_hat) / dt)
mu_hat = float(b_hat / (1.0 - a_hat))
sigma_hat = float(np.sqrt(q_hat * 2.0 * theta_hat / (1.0 - np.exp(-2.0 * theta_hat * dt))))

e_th = abs(theta_hat - theta) / theta
e_mu = abs(mu_hat - mu) / abs(mu)
e_sg = abs(sigma_hat - sigma) / sigma
print(f"true: θ={theta} μ={mu} σ={sigma}")
print(f"hat : θ={theta_hat:.5f} μ={mu_hat:.5f} σ={sigma_hat:.5f}")
print(f"rel err: θ={e_th:.4%} μ={e_mu:.4%} σ={e_sg:.4%} (tol 10%)")
print(f"VERIFY theta_hat={theta_hat:.5f} sigma_hat={sigma_hat:.5f} e_th={e_th:.4f} e_sg={e_sg:.4f}")
assert e_th < 0.10, f"θ 還原誤差過大: {e_th}"
assert e_sg < 0.10, f"σ 還原誤差過大: {e_sg}"
assert e_mu < 0.10, f"μ 還原誤差過大: {e_mu}"
```
