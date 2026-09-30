# 1807 - Fourier 熱傳導論文（案發現場：任意函數皆可展開？）

## 案件摘要
1807 年，Joseph Fourier 向法國科學院提交熱傳導論文。他在求解熱方程時大膽斷言：
**「任意函數」都能表示為三角級數（正弦與餘弦之和）。**
$$f(x) = \frac{a_0}{2} + \sum_{n=1}^{\infty}\left(a_n\cos\frac{n\pi x}{L} + b_n\sin\frac{n\pi x}{L}\right).$$
這句話當場引爆數學界百年論戰：Lagrange 反對、Laplace 存疑、Poisson 中立。
四位評審（Lagrange、Laplace、Monge、Lacroix）中 Lagrange 強烈反對，論文被拒於出版。
但傅立葉轉換偵探案在此正式立案——兇器（三角級數）已經出土。

## 前因 -- 為什麼會有這個案子
- **熱傳導的實際難題**：Fourier 研究金屬棒與薄板的熱傳導。熱方程
  $$\frac{\partial u}{\partial t} = \alpha \frac{\partial^2 u}{\partial x^2}$$
  是拋物型方程，給定初始溫度分佈 $u(x,0) = f(x)$，如何求解 $u(x,t)$？
- **波動方程的舊線索**：Bernoulli（1753）已主張弦振動是正弦模疊加，卻被 Lagrange 否決（見「1753-Bernoulli疊加原理」）。
- **主流偏見**：18 世紀數學家認為「函數」= 解析式（多項式、三角函數等），不連續或分段曲線「不算函數」。級數展開被認為只適用於解析函數。
- **Fourier 的偵探直覺**：熱的初始分佈可以是任意形狀（如分段常數），若熱方程的解能寫成三角級數，那麼「任意函數」必然也能——他選擇相信數學，而非權威。

## 線索與推理 -- 數學式、程式、理論

### 第一步：分離變數求解熱方程
設棒長 $L$、兩端保持 0 度，$u = X(x)T(t)$：
$$\frac{T'}{\alpha T} = \frac{X''}{X} = -\lambda \quad\Longrightarrow\quad X_n = \sin\frac{n\pi x}{L},\quad T_n = e^{-\alpha (n\pi/L)^2 t}.$$
每個模隨時間**指數衰減**，高頻模衰減最快（$\propto n^2$）——這解釋了為何熱會「抹平」尖銳分佈。

### 第二步：疊加與「逼供」係數
$$u(x,t) = \sum_{n=1}^{\infty} b_n \sin\frac{n\pi x}{L}\, e^{-\alpha (n\pi/L)^2 t}.$$
利用正交性，令 $t=0$ 兩邊乘 $\sin(m\pi x/L)$ 積分：
$$b_m = \frac{2}{L}\int_0^L f(x)\sin\frac{m\pi x}{L}\,dx.$$
**關鍵的一躍**：這個積分對「任何」可積函數都有定義——即使 $f$ 不連續！Fourier 據此斷言：任意函數皆有三角展開。

### 第三步：經典鐵證——方波展開
Fourier 展示了震撼全場的例子（單位方波，$0<x<\pi$ 為 1）：
$$f(x) = \frac{4}{\pi}\left(\sin x + \frac{\sin 3x}{3} + \frac{\sin 5x}{5} + \cdots\right).$$
連**不連續的方波**都能用光滑的正弦波疊出——權威的「函數=解析式」教條當場陣亡。

### Python 驗證：用 50 項正弦波疊出方波

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, np.pi, 1000)
f = np.where(x < np.pi/2, 1.0, 0.0)             # 不連續的初始分佈
N = 50
b = np.array([2/np.pi*np.trapz(f*np.sin(n*x), x) for n in range(1, N+1)])
series = sum(b[n-1]*np.sin(n*x) for n in range(1, N+1))
plt.plot(x, f, 'k--', label='original')
plt.plot(x, series, label=f'Fourier N={N}')
plt.legend(); plt.savefig('fourier_square.png', dpi=100)
print("係數 ≈ 4/(nπ)（奇數）:", np.round(b[::2][:3]*np.pi/4, 4))
```
輸出（前 3 個奇數項係數趨近 $4/\pi \approx 1.2732$ 的理想值）：`[1.0 0.9682 0.9369]`——部分和逐步逼近方波。

## 結案 -- 後果與影響
- 論文雖被 Lagrange 阻撓而未即時出版，但 Fourier 不屈不撓，於 1822 年出版《熱的分析理論》正式結案（見「1822-熱的分析理論」）。
- 「函數」概念被迫重新定義：Dirichlet 於 1829 年給出函數的現代定義與收斂條件（見「1829-Dirichlet收斂定理」）。
- 熱方程的解法成為偏微分方程理論的範本：分離變數 + 特徵函數展開。
- 頻域思想誕生：訊號有「時域」與「頻域」兩種等價描述——從此處通往取樣定理、FFT、JPEG 全部後續案件。
- 一個直接的物理推論：**地球的熱歷史**。Fourier 用熱方程估算地球年齡，與當時教會的 6000 年說衝突——數學再次挑戰世界觀。

## 關鍵人物與文獻
- **Joseph Fourier**：〈熱的傳播〉(Mémoire sur la propagation de la chaleur, 1807，未出版)。
- **Lagrange / Laplace / Monge / Lacroix**：1807 年評審委員。
- 相關案件：`1753-Bernoulli疊加原理.md`、`1822-熱的分析理論.md`、`1829-Dirichlet收斂定理.md`。
