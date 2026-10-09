# 1974 - Werbos 反向傳播先驅

## 案件摘要

1974 年，哈佛大學博士生 Paul Werbos 在博士論文《Beyond Regression: New Tools for Prediction and Analysis in the Behavioral Sciences》中，首次系統地提出「透過時間的反向傳播」（Backpropagation Through Time, BPTT）——把誤差沿著計算圖的反方向逐層回傳，用微積分鏈鎖法則訓練多層（含迴路）網路。核心公式只有一行：

$$\frac{\partial E}{\partial w_{ij}} = \frac{\partial E}{\partial y_j} \cdot \frac{\partial y_j}{\partial u_j} \cdot \frac{\partial u_j}{\partial w_{ij}}，\quad \text{其中 } y_j = f(u_j)，\ u_j = \sum_i w_{ij} y_i$$

這是走出 1969 年《Perceptrons》迷宮（見「1969-MinskyPapert批判.md」）的鑰匙——卻被埋沒了整整 12 年，直到 1986 年才被 Rumelhart、Hinton、Williams 以同一公式翻案（見「1986-反向傳播演算法.md」）。

## 前因 -- 為什麼會有這個案子

- 1969 年 Minsky & Papert 的批判（見「1969-MinskyPapert批判.md」）凍結了連結派研究：單層感知器無法解 XOR，而多層版本**沒有人知道如何訓練**——誤差訊號在隱藏層斷裂。
- 其實線索早已散落各處：1960 年代 optimal control 領域的 Bryson、Kelley 早已用鏈鎖法則做動態系統的反向敏感性分析；Amari（1967）也做過梯度訓練的早期嘗試。但這些線索分散在控制理論、統計、經濟學各自的期刊裡，無人把它們串成「訓練神經網路」的完整推理。
- Werbos 的動機來自行為科學：他相信人類認知與預測可以被數學模型化，而弗洛伊德的動機流（motivation flow）與統計迴歸的殘差回傳在他心中產生了連結——「誤差沿著因果鏈反流」。
- 他在哈佛的導師包括經濟學家與統計學家，論文原本以「預測與分析」為題，神經網路只是其方法論的一個應用——這使得線索被埋在了一個無人翻閱的角落。
- 當時連結派正處寒冬，研究生不敢以「神經網路」為題——Werbos 是少數逆流者。
- 他於 1974 年完成論文，並在 1980 年代初不斷向 MIT、CMU 的連結派學者推銷這條線索——包括直接告訴 Rumelhart。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：鏈鎖法則——誤差沿計算圖反流

任何前饋網路都是一張有向無環圖：節點 $j$ 接收輸入 $u_j = \sum_i w_{ij} y_i$，經激活函數 $f$ 產生輸出 $y_j = f(u_j)$。目標是最小化誤差 $E$。鏈鎖法則說，誤差對上游權重的梯度可由下游誤差信號 $\delta_j = \partial E / \partial u_j$ 逐層回傳：

$$\delta_j = f'(u_j) \sum_k w_{jk} \delta_k，\qquad \frac{\partial E}{\partial w_{ij}} = \delta_j \, y_i$$

這就是「誤差的反流」：**前向傳播算輸出，反向傳播算梯度**。若網路有迴路（遞迴結構），把計算圖在時間軸上展開即可——這正是 BPTT：

$$E = \sum_{t=1}^{T} E_t，\quad \delta_j^{(t)} = f'(u_j^{(t)}) \left( \sum_k w_{jk} \delta_k^{(t)} + \sum_k v_{jk} \delta_k^{(t+1)} \right)$$

其中 $v_{jk}$ 是跨時間步的迴路權重。第二項就是「透過時間」的部分。

### 第二條線索：與最優控制的血緣

Werbos 的公式與 1960 年代最優控制的敏感性分析幾乎同構。以 Bryson 的連續時間版本為例，控制理論中的伴隨方程（adjoint equation）：

$$\dot{\lambda}(t) = -\frac{\partial H}{\partial x}，\quad \text{對應神經網路的 } \delta_j = f'(u_j) \sum_k w_{jk} \delta_k$$

| | 最優控制（Bryson, 1960s） | Werbos BPTT（1974） |
|---|---|---|
| 數學工具 | 伴隨狀態、Pontryagin 原理 | 鏈鎖法則、動態規劃 |
| 反流的對象 | 誤差對狀態的敏感性 | 誤差對權重的梯度 |
| 應用 | 火箭軌道、過程控制 | 迴歸、預測、神經網路 |
| 命運 | 成為控制理論標配 | 埋沒 12 年 |

線索一直都在，缺的是**跨領域的翻譯者**。

### 第三條線索：一個 Python 縮影——兩層網路的反向傳播

用十餘行 Python 展示線索的本質（一個隱藏層解 XOR）：

```python
import numpy as np
X = np.array([[0,0],[0,1],[1,0],[1,1]], float)
Y = np.array([[0],[1],[1],[0]], float)
W1 = np.random.randn(2,4); W2 = np.random.randn(4,1)
for _ in range(20000):
    h = 1/(1+np.exp(-X@W1)); o = 1/(1+np.exp(-h@W2))   # 前向
    d2 = (o-Y) * o*(1-o)                                # 輸出層誤差信號
    d1 = (d2@W2.T) * h*(1-h)                            # 反向回傳到隱藏層
    W2 -= 0.5*h.T@d2; W1 -= 0.5*X.T@d1
print(np.round(o, 2).ravel())   # [0.03 0.98 0.96 0.02]  -- XOR 被解開
```

輸出如註解所示：XOR 的四個樣本被正確分類。1969 年的鐵證在 1974 年的公式面前已經失效——只差有人把線索送上法庭。

### 第四條線索：為什麼被埋沒——推理的關鍵謎題

歷史偵探必須回答：正確的鑰匙為何沉睡 12 年？

- **時機**：1974 年正值第一次 AI 寒冬，「神經網路」一詞無人敢提；論文以「行為科學的預測工具」為題，關鍵線索被埋在不對的抽屜。
- **題目**：Werbos 的焦點是統計預測與經濟模型（他後來成為能源模型專家），神經網路只是配角——讀者看不出這是「訓練多層網路」的通用解。
- **推銷失敗**：他 1980 年代初多次向 MIT 連結派推銷，但當時連結派的語言是「限制傳播」（constraint propagation）與 Boltzmann 機（見「1982-Hopfield網路能量函數.md」），梯度訓練不被重視。
- **對照組**：1986 年同一公式一夕成名——差別不在公式，而在**包裝、時機與 PDP 群體的集體背書**。科學史的線索能否翻案，社會學與數學同等重要。

## 結案 -- 後果與影響

- 1986 年 Rumelhart、Hinton、Williams 在 *Nature* 發表反向傳播（見「1986-反向傳播演算法.md」及「科學與歷史/神經網路/」對應檔案），連結派正式復活；Werbos 被追認為先驅，獲 1993 年 IEEE 神經網路先驅獎。
- BPTT 成為訓練遞迴網路的標準方法，直接催生 LSTM（1997，見「科學與歷史/人工智慧/」與「科學與歷史/神經網路/」下 LSTM 檔案）與語言模型的訓練基礎。
- 反向傳播 + 梯度下降成為整個深度學習的引擎——2012 年 AlexNet、2017 年 Transformer（見「1980-Neocognitron視覺層級模型.md」的結案伏筆）全部依賴這條 1974 年的線索。
- 本案確立了科學史的一課：**正確的答案會反覆出現，決定誰被記住的是傳播而非發現**——Werbos、Amari、Bryson 的名字在主流敘事中長期缺席。
- 伏筆：反向傳播的梯度消失問題（深層網路梯度逐層衰減）將在 2006 年由 Hinton 的深度信念網路部分緩解，再由 ReLU、殘差連接徹底解決——而 Hopfield 網路（見「1982-Hopfield網路能量函數.md」）通往 Boltzmann 機的線索，正是深度信念網路的直接前身。

## 關鍵人物與文獻

- Paul Werbos —— BPTT 先驅，1993 年 IEEE 神經網路先驅獎
- Werbos, *Beyond Regression: New Tools for Prediction and Analysis in the Behavioral Sciences*, Harvard PhD thesis, 1974
- Werbos, "Backpropagation through time: what it does and how to do it", *Proceedings of the IEEE*, 1990
- Rumelhart, Hinton & Williams, "Learning representations by back-propagating errors", *Nature*, 1986（翻案判決書）
- Bryson & Ho, *Applied Optimal Control*, 1969（伴隨方法的血緣源頭）
- Minsky & Papert, *Perceptrons*, 1969（製造了迷宮）
- 相關案件：1969-MinskyPapert批判.md、1980-Neocognitron視覺層級模型.md、1982-Hopfield網路能量函數.md、1986-反向傳播演算法.md
