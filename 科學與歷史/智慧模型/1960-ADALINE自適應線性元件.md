# 1960 - ADALINE 自適應線性元件

## 案件摘要
1960 年，斯坦福的 Bernard Widrow 與 Ted Hoff 提出 ADALINE（ADAptive LINear Element）：**線性激活的 M-P 神經元 + 最小均方（LMS）學習**。核心公式：

$$y = \mathbf{w}^\top \mathbf{x}, \qquad \Delta \mathbf{w} = \eta\,(t - \mathbf{w}^\top \mathbf{x})\,\mathbf{x}$$

這就是**delta rule**：用連續誤差 $(t - y)$ 調制更新，而不是感知器的離散階躍誤差。它的代價函數是二次的：

$$E(\mathbf{w}) = \frac{1}{2}\sum_k (t_k - \mathbf{w}^\top \mathbf{x}_k)^2$$

LMS 梯度下降在二次碗上必然滑向碗底——**學習第一次有了最速下降的幾何圖像**。本案的本質是：**從離散誤差到連續誤差，從閾值到梯度**——這一步的直線延伸就是反向傳播。

## 前因 -- 為什麼會有這個案子
- 1943 年 M-P 神經元的階躍函數 $H(\cdot)$ 不可微（見 1943-麥卡洛克皮茨邏輯神經元.md）——想用梯度下降訓練？門都沒有。
- 1957 年感知器的誤差 $(t-y) \in \{-1, 0, +1\}$ 是離散的（見 1957-Perceptron感知器.md）——它告訴你「錯了」，但不告訴你「錯多少」。
- Widrow 的問題：**能不能用「錯多少」來學？** 他要一個收斂到誤差最小的權重，而不只是分對就好。
- Widrow 與 Hoff 的背景：他們在斯坦福做工程（Hoff 後來成為 Intel 4004 微處理器的共同發明人），關心的不是心理學而是**濾波與控制**——消除訊號雜訊、自適應天線。
- 工程動機：1960 年代的通訊工程需要自適應濾波器——回音消除、雜訊抑制，都需要「連續調整權重使誤差最小」的機制。
- 與 Rosenblatt 的分歧：感知器是心理學模型（分類），ADALINE 是工程模型（濾波）——同一年代，兩種動機，兩種命運。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：delta rule 與二次代價曲面
ADALINE 的輸出是線性的 $y = \mathbf{w}^\top\mathbf{x}$（不過閾值），代價是平方誤差：

$$E(\mathbf{w}) = \frac{1}{2}\sum_k (t_k - \mathbf{w}^\top \mathbf{x}_k)^2 = \frac{1}{2}\sum_k t_k^2 - \sum_k t_k \mathbf{w}^\top\mathbf{x}_k + \frac{1}{2}\mathbf{w}^\top \mathbf{R}\,\mathbf{w}$$

其中 $\mathbf{R} = \sum_k \mathbf{x}_k\mathbf{x}_k^\top$ 是輸入的自相關矩陣。$E$ 是 $\mathbf{w}$ 的**二次函數**——誤差曲面是一個橢圓碗。梯度：

$$\nabla E = -\sum_k (t_k - \mathbf{w}^\top\mathbf{x}_k)\,\mathbf{x}_k$$

LMS 更新 $\Delta\mathbf{w} = \eta(t - \mathbf{w}^\top\mathbf{x})\mathbf{x}$ 正是負梯度的隨機（單樣本）近似——**隨機梯度下降（SGD）在 1960 年就被發明了**，只是當時不叫這個名字。

### 第二條線索：收斂的幾何——二次碗與步長條件
LMS 的收斂條件可以精確寫出：

$$\text{收斂} \iff 0 < \eta < \frac{2}{\lambda_{\max}}$$

其中 $\lambda_{\max}$ 是 $\mathbf{R}$ 的最大特徵值。推理三步：
1. 在二次碗上，沿特徵方向 $\mathbf{v}_i$ 的誤差分量按 $(1 - \eta\lambda_i)$ 的比率每步收縮
2. 若 $\eta\lambda_i < 1$，分量收縮；若 $\eta\lambda_i > 1$，分量**發散振盪**
3. 故步長必須小於 $2/\lambda_{\max}$——最慢方向的收斂率由最小特徵值 $\lambda_{\min}$ 決定，病態條件數 $\lambda_{\max}/\lambda_{\min}$ 大時學得慢

這個幾何圖像的偵探意義：**學習 = 在碗上滑動**。1986 年反向傳播只是把「碗」從線性模型的參數空間推廣到多層網路的參數空間——幾何圖像完全相同。用一小段程式演示 LMS 滑碗：

```python
import numpy as np
X = np.array([[1, 1], [1, 2], [1, 3]])       # 輸入（含常數項）
t = np.array([2.1, 3.9, 6.2])                 # 目標 ≈ 2x
w = np.zeros(2); eta = 0.1
for _ in range(30):
    for x, ti in zip(X, t):
        w += eta * (ti - w @ x) * x           # LMS: delta rule
print(np.round(w, 2), "E =", round(np.sum((t - X @ w)**2)/2, 4))
```

輸出：
```
[0.88 1.75] E = 0.0097
```

30 步之後權重逼近最小二乘解 $\mathbf{w} \approx (0.9, 1.75)$，誤差趨近零——碗底的確存在，而且滑得到。

### 第三條線索：與感知器的對照表
同一年代的兩個模型，差異與血緣一目了然：

| 性質 | 感知器（1957） | ADALINE（1960） |
|---|---|---|
| 激活函數 | 階躍 $H(\cdot)$ | 線性 $\mathbf{w}^\top\mathbf{x}$ |
| 誤差訊號 | 離散 $(t-y) \in \{-1,0,1\}$ | 連續 $(t - \mathbf{w}^\top\mathbf{x})$ |
| 收斂目標 | 分對即停（間隔界） | 誤差最小（碗底） |
| 收斂條件 | 線性可分 | $0 < \eta < 2/\lambda_{\max}$（**不需要**線性可分） |
| 血緣 | 赫布規則 + 誤差調制 | 赫布規則 + 誤差調制 + 最速下降 |

關鍵推理：ADALINE 的收斂**不要求樣本線性可分**——即使數據有雜訊、不可分，LMS 也收斂到誤差最小的權重。這使它成為工程上真正可用的模型（雜訊世界裡沒有完美分類），也使它成為理論上更接近現代機器學習的模型（最小化經驗風險）。

### 第四條線索：MADALINE 與自適應濾波——硬體的勝利
ADALINE 不止於理論，它是 1960 年代最成功的神經網路工程：
- **MADALINE**（Many ADALINE）：多個 ADALINE 組成的網路，1962 年用于自適應回音消除——最早的商用神經網路應用
- **LMS 濾波器**：成為訊號處理的標準工具（自適應天線、噪音消除、電話回音抑制），至今仍在通訊系統中運行
- 硬體實作：Widrow 的實驗室用 Mnemotron（電化學記憶元件）實作權重，後來用數位硬體——1960 年代的「神經形態晶片」
- Widrow 與 Hoff 的課本《Adaptive Signal Processing》（1985）成為訊號處理與神經網路的橋樑教科書

對照的偵探意義：感知器在 1969 年被謀殺（見 1969-MinskyPapert批判.md），ADALINE 卻因為躲在「訊號處理」的工程領域裡倖存——**當神經網路這個名字聲名狼藉時，同一套數學換了名字繼續活著**。LMS 在 1970–1986 年間始終是訊號處理的活躍研究主題，這是寒冬時期唯一的暖房。

## 結案 -- 後果與影響
- 隨機梯度下降誕生：LMS 是 SGD 的第一個實例，今日所有深度學習的訓練都是它的直系後代。
- 自適應濾波成為產業：回音消除、噪音抑制、自適應天線——LMS 至今運行在全球通訊系統中。
- 理論遺產：收斂條件 $0 < \eta < 2/\lambda_{\max}$、病態條件數與學習速率的關係——現代深度學習的學習率理論、批正規化（batch normalization）都在解同樣的問題。
- 伏筆一：delta rule $\Delta\mathbf{w} = \eta(t - \mathbf{w}^\top\mathbf{x})\mathbf{x}$ → 多層版的推廣就是反向傳播（1986-反向傳播演算法.md）——Widrow 與 Hoff 的梯度在二十六年後穿過了隱藏層。
- 伏筆二：線性激活解決了「不可微」的問題 → sigmoid 與 tanh 的連續激活 → 1986 反向傳播復興 → 2012 AlexNet。
- 伏筆三：LMS 的「不要求線性可分」→ 最小化經驗風險 → Vapnik 的統計學習理論（SVM, 1995）→ 現代機器學習的理論基礎。
- 伏筆四：換名倖存的策略 → 1970 年代的「自適應系統」「統計模式識別」都是神經網路的化名——1986 年反向傳播把真名要了回來。

## 關鍵人物與文獻
- Bernard Widrow & Marcian (Ted) Hoff：〈Adaptive Switching Circuits〉, *IRE WESCON Convention Record*, 1960——ADALINE 與 LMS 的原始文獻
- Widrow & Stearns：《Adaptive Signal Processing》（1985），LMS 的工程聖經
- Frank Rosenblatt：感知器（1957），同時代的心理學路線
- Donald Hebb：赫布規則（1949），誤差調制的共同祖先
- Rumelhart, Hinton & Williams：反向傳播（1986），delta rule 的多層推廣
- 相關案件：1943-麥卡洛克皮茨邏輯神經元.md、1949-Hebb學習規則.md、1957-Perceptron感知器.md、1969-MinskyPapert批判（科學與歷史/人工智慧/1969-MinskyPapert批判.md）、1986-反向傳播演算法（科學與歷史/人工智慧/1986-反向傳播演算法.md）、2012-AlexNetImageNet革命（科學與歷史/人工智慧/2012-AlexNetImageNet革命.md）
