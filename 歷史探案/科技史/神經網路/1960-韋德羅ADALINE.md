# 1960 - Widrow–Hoff ADALINE（delta 規則與最小均方）

## 案件摘要
1960 年，史丹佛的 **Bernard Widrow（1929–）** 與博士生 **Ted Hoff（1937–）**
（後來的 Intel 4004 微處理器共同發明人！）發表 **ADALINE**
（Adaptive Linear Neuron，自適應線性神經元）：
$$\boxed{\text{對「連續輸出」的誤差學習——delta 規則（LMS 最小均方）}}$$
**ADALINE** 與感知機的關鍵差別：
- 感知機用**階梯函數後**的離散誤差 $(t - o)$；
- ADALINE 用**階梯函數前**的連續誤差：
$$E = \frac{1}{2}(t - y)^2, \quad y = w \cdot x$$
**delta 規則（LMS）**——對誤差 $E$ 做梯度下降：
$$\Delta w = \eta \, (t - y) \, x$$
**形式上與感知機相同，本質上更深刻**：它在最小化**二次誤差面**——
**收斂性更強、對雜訊更穩健**。
ADALINE/Madaline 是**第一批實際應用的神經網路**：
**電話迴音消除器（adaptive filter）**曾部署在全球的電話網路中——
$$\text{神經網路} \xrightarrow{\text{ADALINE（1960）}} \text{第一次走出實驗室}.$$

## 前因 -- 為什麼會有這個案子
- **Rosenblatt 感知機的缺陷（1958）**：
  感知機的學習用**階梯輸出**的誤差 $(t - o) \in \{-1, 0, 1\}$——
  **錯很多只知「錯了」**：誤差訊號粗、收斂慢、對雜訊敏感。
  $$\boxed{\text{「能不能用連續的誤差大小，而不是只有對錯？」}}$$
  Widrow 的回答：**對連續誤差做梯度下降**——delta 規則。
- **McCulloch–Pitts 與 Hebb 的遺產（1943、1949）**：
  神經元 = 閾值單元（`1943-麥卡洛克皮茨神經元.md`）；
  Hebb 規則 = 學習的第一定律（`1949-赫布學習規則.md`）——
  Widrow 把它們工程化：**他要的不是模擬大腦，是有用的機器**。
- **最小平方法的回聲（1795 → 1960）**：
  **Gauss 與 Legendre** 在 1795 年前後發明**最小平方法**（least squares）：
  $$\min_w \sum_k (t^{(k)} - w \cdot x^{(k)})^2 \quad \text{（二次誤差面）}$$
  這是**回歸分析的基礎**。Widrow–Hoff 的 LMS 是**最小平方法的線上版**——
  不一次吃全部資料，而是**一個樣本一個樣本地更新**：
  $$\text{Gauss（1795）：批次最小平方} \xrightarrow{\text{Widrow（1960）：線上 delta 規則}} \text{隨機梯度下降}.$$
- **貝爾實驗室的迴音問題（1950s–1960s）**：
  長途電話有**迴音**（訊號反射回原端）——
  迴音路徑**因線路而異、隨時間變化**——
  **固定濾波器無法消除**——需要**自適應（adaptive）**的濾波器——
  ADALINE 正好是「會自我調整的線性濾波器」——
  $$\text{工程需求} \xrightarrow{} \text{自適應濾波} \xrightarrow{} \text{神經網路的第一個殺手級應用}.$$

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：ADALINE 的形式定義
**ADALINE** 是一個**線性單元**（無階梯函數的輸出）：
$$y = \sum_i w_i x_i = w \cdot x$$
- 輸出 $y$ 是**連續的**（與感知機的二值輸出不同）；
- 二值決策（若需要）在 $y$ 之後用符號函數 $\mathrm{sgn}(y)$ 做出；
- **學習發生在連續輸出 $y$ 上**——這是核心差別。

### 第二條線索：delta 規則 = 誤差面的梯度下降
**均方誤差**（單一樣本）：
$$E = \frac{1}{2}(t - y)^2 = \frac{1}{2}(t - w \cdot x)^2$$
**對 $E$ 求梯度**（連鎖法則）：
$$\frac{\partial E}{\partial w_i} = (t - y) \cdot \frac{\partial y}{\partial w_i} = (t - y) \, x_i$$
**梯度下降**（往誤差下降最快的方向走）：
$$\boxed{\Delta w_i = -\eta \frac{\partial E}{\partial w_i} = \eta \, (t - y) \, x_i}$$
**這是 delta 規則（LMS, least mean squares）**——
- 感知機：誤差 $(t - o)$ 只有 $\{-1, 0, +1\}$（階梯後）；
- ADALINE：誤差 $(t - y)$ 是**連續實數**（階梯前）——
  **錯得越多，推得越用力**——
  $$\text{感知機（1958）：}(t - o) \in \{-1,0,1\} \xrightarrow{\text{ADALINE（1960）}} (t - y) \in \mathbb{R}.$$
- **收斂性**：當 $\eta$ 足夠小（$\eta < 2/\lambda_{\max}$，$\lambda_{\max}$ 是輸入相關矩陣的最大特徵值），
  LMS **必收斂到誤差面的最低點**——比感知機的行為更可控。

### 第三條線索：LMS = 最小平方法的線上版
**批次最小平方**（Gauss, 1795）：一次用全部 $p$ 筆資料解正規方程：
$$X^{\top} X \, w = X^{\top} t$$
**線上 LMS**（Widrow, 1960）：一筆一筆更新：
$$w \leftarrow w + \eta \, (t^{(k)} - w \cdot x^{(k)}) \, x^{(k)}$$
- **兩者收斂到同一個解**（最小均方解）；
- 但 LMS **不需要儲存全部資料**、**能追蹤緩慢變化的系統**——
  $$\boxed{\text{線上更新} + \text{自我調整} = \text{自適應濾波}}$$
- 這正是**迴音消除**需要的：迴音路徑隨時間變化，
  LMS 濾波器**即時跟蹤**——
  **這是隨機梯度下降（SGD）的第一次實戰**。

### Python：LMS 線性回歸與自適應濾波

```python
# 1) LMS（delta 規則）：Δw = η (t - y) x，對「連續輸出」的誤差
def lms_train(X, t, eta=0.1, epochs=50):
    """線性回歸：y = w·x，最小化均方誤差"""
    w = [0.0] * len(X[0])
    history = []
    for ep in range(1, epochs + 1):
        total_se = 0.0
        for x, target in zip(X, t):
            y = sum(wi * xi for wi, xi in zip(w, x))   # 連續輸出（無階梯函數）
            e = target - y
            total_se += e * e
            for i in range(len(w)):
                w[i] += eta * e * x[i]                 # Δw = η(t-y)x
        mse = total_se / len(X)
        history.append((ep, mse, list(w)))
    return w, history

# 2) 線性回歸：學習 y = 2x1 + 3x2（沒有截距的簡單案例）
X = [(1, 1), (2, 1), (3, 2), (1, 3)]
t = [5, 7, 12, 11]   # y = 2x1 + 3x2

w, hist = lms_train(X, t, eta=0.05, epochs=30)

print("LMS 線性回歸（學習 y = 2x1 + 3x2）：")
for ep, mse, ww in hist[:4]:
    print(f"  epoch {ep:2d}: MSE={mse:.4f}  w={ww}")
print("  ...")
for ep, mse, ww in hist[-2:]:
    print(f"  epoch {ep:2d}: MSE={mse:.6f}  w={ww}")

print("\n學到的權重：")
print(f"  w1={w[0]:.4f}（目標 2）、w2={w[1]:.4f}（目標 3）")

# 3) 驗證：預測新資料
print("\n新資料的預測：")
for x in [(4, 1), (2, 2)]:
    y = w[0] * x[0] + w[1] * x[1]
    print(f"  x={x} → y={y:.3f}  (真值 {2*x[0] + 3*x[1]})")

# 4) 自適應濾波：電話迴音消除
print("\n自適應濾波（電話迴音消除）：")
# 接收訊號 d = 原聲 s + 迴音；LMS 濾波器先「辨識」迴音路徑（學到係數）
s = [1.0, 0.5, -0.5, 1.0, 0.0, 0.5]
echo_a = 0.6                    # 真實迴音係數（未知，待學習）
echo = [echo_a * s[i-1] if i > 0 else 0.0 for i in range(len(s))]
d = [s[i] + echo[i] for i in range(len(s))]  # 接收到的訊號
w_f = 0.0                       # 濾波器對迴音係數的估計
step_no = 0
for rep in range(6):            # 通話持續，訊號反覆輸入
    for k in range(1, len(s)):
        step_no += 1
        x_echo = s[k-1]         # 迴音的來源訊號（延遲一拍）
        y_echo = w_f * x_echo   # 估計的迴音
        e = echo[k] - y_echo    # 誤差 = 真迴音 - 估計迴音
        w_f += 0.5 * e * x_echo # LMS 更新
        if step_no % 6 == 0:
            print(f"  step {step_no:2d}: 迴音估計={w_f:.4f}  誤差={e:.4f}")
print(f"  最終估計 w={w_f:.4f}（真實迴音係數 {echo_a}）✓")
print("  迴音消除：從接收訊號減去估計的迴音：")
for k in range(1, len(s)):
    residual = d[k] - w_f * s[k-1]
    print(f"    原聲={s[k]:+.1f}  消除後殘留={residual:+.4f}  （≈原聲，迴音已被移除）")

print("\n結論：delta 規則 = 最小平方法的線上版——Gauss（1795）的現代迴響。")
```
輸出：
```
LMS 線性回歸（學習 y = 2x1 + 3x2）：
  epoch  1: MSE=38.6127  w=[2.34875, 2.0962500000000004]
  epoch  2: MSE=1.1261  w=[2.5729332499999997, 2.4818947500000004]
  epoch  3: MSE=0.5877  w=[2.5119136657999994, 2.6065766604000005]
  epoch  4: MSE=0.4337  w=[2.4265237128070694, 2.68139029060641]
  ...
  epoch 29: MSE=0.000024  w=[2.0031487732557163, 2.9976620378129493]
  epoch 30: MSE=0.000016  w=[2.0025871300312024, 2.998079057558382]

學到的權重：
  w1=2.0026（目標 2）、w2=2.9981（目標 3）

新資料的預測：
  x=(4, 1) → y=11.008  (真值 11)
  x=(2, 2) → y=10.001  (真值 10)

自適應濾波（電話迴音消除）：
  step  6: 迴音估計=0.5426  誤差=0.1148
  step 12: 迴音估計=0.5904  誤差=0.0055
  step 18: 迴音估計=0.5984  誤差=-0.0009
  step 24: 迴音估計=0.5998  誤差=0.0003
  step 30: 迴音估計=0.6000  誤差=0.0000
  最終估計 w=0.6000（真實迴音係數 0.6）✓
  迴音消除：從接收訊號減去估計的迴音：
    原聲=+0.5  消除後殘留=+0.5000  （≈原聲，迴音已被移除）
    原聲=-0.5  消除後殘留=-0.5000  （≈原聲，迴音已被移除）
    原聲=+1.0  消除後殘留=+1.0000  （≈原聲，迴音已被移除）
    原聲=+0.0  消除後殘留=+0.0000  （≈原聲，迴音已被移除）
    原聲=+0.5  消除後殘留=+0.5000  （≈原聲，迴音已被移除）

結論：delta 規則 = 最小平方法的線上版——Gauss（1795）的現代迴響。
```

## 結案 -- 後果與影響
- **第一批實用的神經網路（1960s）**：
  $$\boxed{\text{ADALINE/Madaline 是第一個走出實驗室的神經網路}}$$
  - **Madaline I（1961）**：多層 ADALINE，做**自適應模式辨識**；
  - **迴音消除器**：部署在全球電話網路——**神經網路的第一個商業應用**。
    $$\text{delta 規則} \xrightarrow{\text{應用}} \text{電話、數據機、雷達、天線陣列}.$$
- **反向傳播的預言（1960 → 1986）**：
  delta 規則是「**對連續誤差做梯度下降**」——
  Rumelhart–Hinton–Williams 的**反向傳播（1986）**把它推廣到**多層**：
  誤差從輸出層**逐層回傳**，每層都用 delta 規則更新——
  $$\text{delta 規則（單層, 1960）} \xrightarrow{\text{反傳（多層, 1986）}} \text{深度學習}.$$
  **Widrow 的單層規則，養育了多層的世界**。
- **Hoff 的另一個傳奇（1971）**：
  Ted Hoff 離開史丹佛後加入 Intel，
  是 **Intel 4004 微處理器（1971）**的四位共同發明人之一——
  $$\text{ADALINE（1960）：學習的晶片} \xrightarrow{\text{4004（1971）：計算的晶片}} \text{兩條傳奇線在同一人身上交會}.$$
- **第一次寒冬中的倖存者（1969–1980s）**：
  Minsky–Papert 的批判（1969）凍結了感知機路線——
  但 ADALINE 因為**有實際應用**（電話、數據機）而**倖存**——
  Widrow 的史丹佛實驗室持續運作，培養了新一代的神經網路研究者——
  **務實的工程活過了理論的寒冬**。
- 歷史定位：**Widrow–Hoff 是神經網路的工程師與倖存者**——
  $$\text{計算（1943）} \xrightarrow{\text{學習（1949）}} \text{機器（1958）} \xrightarrow{\text{應用（1960）}} \text{走出實驗室}.$$
  **「讓它有用」——ADALINE 用電話網路證明了神經網路的價值**。

## 關鍵人物與文獻
- **B. Widrow 與 M. E. Hoff**：*Adaptive Switching Circuits*（1960 WESCON）——ADALINE 與 delta 規則。
- **B. Widrow 與 S. Stearns**：*Adaptive Signal Processing*（1985）——自適應濾波的教科書。
- **M. E. Hoff**：Intel 4004 微處理器（1971）四位發明人之一。
- **F. Rosenblatt**：感知機（1958）——同年的競爭與對照（見 `1958-羅森布拉特感知機.md`）。
- **C. F. Gauss 與 A. M. Legendre**：最小平方法（1795/1805）——LMS 的數學遠祖。
- **D. E. Rumelhart、G. E. Hinton、R. J. Williams**：反向傳播（1986）——delta 規則的多層推廣。
- 相關案件：`1943-麥卡洛克皮茨神經元.md`、`1949-赫布學習規則.md`、`1958-羅森布拉特感知機.md`、`資訊科學/1936-圖靈機.md`。
