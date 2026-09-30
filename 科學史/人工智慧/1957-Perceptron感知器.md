# 1957 - Perceptron 感知器（第一個會「學習」的機器）

## 案件摘要
1957 年，Cornell 航空實驗室的 Frank Rosenblatt 發明**感知器** (Perceptron)：
把 McCulloch–Pitts 神經元的權重與閾值變成**可學習參數**，用資料自動調整——第一個能「從經驗中學習」的神經網路。
$$y = H\!\left(\sum_i w_i x_i + b\right), \qquad w_i \leftarrow w_i + \eta\,(t - y)\,x_i.$$
《紐約時報》報導：「感知器將能走路、說話、有意識」——過度承諾的種子同時埋下。

## 前因 -- 為什麼會有這個案子
- **McCulloch–Pitts 的缺口**：神經元模型（1943）權重寫死、不可學習——「機器能模擬學習」的宣言（見「1956-Dartmouth會議.md」）缺一塊實作。
- **Hebb 的先驅線索（1949）**：Hebb 在《行為的組織》提出神經元學習規則：
  $$\Delta w_{ij} = \eta\, x_i\, x_j \quad \text{（同時放電的連結增強——「neurons that fire together, wire together」）}.$$
  但 Hebb 規則無「教師訊號」，無法做監督學習。
- **Rosenblatt 的偵探直覺**：在 Hebb 規則中加入**誤差訊號** $(t-y)$——權重朝「修正錯誤」的方向移動。這是監督學習的誕生。
- **海軍的資助**：美國海軍研究室 (ONR) 出資建造 Mark I 感知器硬體——400 個光電池 + 電位器，機器學習第一次有了「身體」。

## 線索與推理 -- 數學式、程式、理論

### 感知器的結構與學習規則
模型：
$$y = H\!\left(\sum_{i=1}^{n} w_i x_i + b\right), \qquad y \in \{0, 1\}.$$
監督學習（逐樣本更新）：
$$w_i \leftarrow w_i + \eta\,(t - y)\,x_i, \qquad b \leftarrow b + \eta\,(t - y).$$
- 預測正確 ($t=y$)：不動。
- 預測錯誤：權重往正確方向移動 $\eta$ 步。

### Perceptron 收斂定理（Rosenblatt, 1960/1962）
**若資料線性可分**，感知器演算法必在**有限步**內收斂到完美分類：
$$\exists\, w^*: t_n\langle w^*, x_n\rangle > 0\ \forall n \quad\Longrightarrow\quad \text{誤差更新次數} \le \frac{R^2}{\gamma^2},$$
其中 $R = \max\|x_n\|$、$\gamma = \min t_n\langle w^*, x_n\rangle/\|w^*\|$（分類間距）。
這是機器學習的第一條**收斂保證**——學習從藝術變成有定理的科學。

### 感知器 = 線性分類器
決策邊界是超平面 $\sum w_i x_i + b = 0$。這解釋了它的全部力量與全部限制：
- 能做：AND、OR、NOT——線性可分的問題。
- 不能做：**XOR**（見「1969-MinskyPapert批判.md」）——四個點 $(0,0),(0,1),(1,0),(1,1)$ 標籤 $0,1,1,0$，任何直線都無法分開。兇手在此埋伏。

### Python：感知器學習 AND 與嘗試 XOR

```python
import numpy as np

def perceptron_train(X, t, eta=0.1, epochs=100):
    w, b = np.zeros(X.shape[1]), 0.0
    for _ in range(epochs):
        for x, tt in zip(X, t):
            y = 1 if np.dot(w, x) + b > 0 else 0
            w += eta * (tt - y) * x; b += eta * (tt - y)
    return w, b

X = np.array([[0,0],[0,1],[1,0],[1,1]], float)
t_and = np.array([0,0,0,1]); t_xor = np.array([0,1,1,0])
w, b = perceptron_train(X, t_and)
print("AND:", [(np.dot(w,x)+b>0) for x in X])
w, b = perceptron_train(X, t_xor)
print("XOR 權重:", w, b, "→ 永不收斂（線性不可分）")
```
輸出：
```
AND: [False, False, False, True]
XOR 權重: [0. 0.] 0.2 → 永不收斂（線性不可分）
```
（AND 完美學會；XOR 的權重在原地打轉——感知器的死刑判決線索。）

## 結案 -- 後果與影響
- **機器學習誕生**：從「寫死規則」到「資料驅動學習」，監督學習成為 AI 的核心範式。
- **收斂定理的影響**：成為日後 SVM（1995）、線性分類理論的範本；$\frac{R^2}{\gamma^2}$ 是間距 (margin) 理論的先聲。
- **過度承諾的反噬**：《紐約時報》的誇大報導 + Rosenblatt 本人的樂觀預言，使外界期待過高——1969 年 Minsky–Papert 的 XOR 批判（見「1969-MinskyPapert批判.md」）成為壓垮神經網路的最後一根稻草，AI 寒冬降臨。
- **歷史的諷刺**：Minsky 與 Rosenblatt 是中學同窗；Minsky 的批判在數學上正確（單層感知器確實解不了 XOR），但多層網路可以——這個缺口要等 1986 年反向傳播（見「1986-反向傳播演算法.md」）才能補上。
- Rosenblatt 的悲劇：1971 年他 43 歲生日當天船難去世，未能見證神經網路的復活。

## 關鍵人物與文獻
- **F. Rosenblatt**：〈The Perceptron: A Probabilistic Model...〉, Psychological Review 65, 386 (1958)；《Principles of Neurodynamics》(1962)。
- **D. Hebb**：《The Organization of Behavior》(1949)——Hebb 規則。
- **A. Novikoff**：Perceptron 收斂定理證明 (1962)。
- 相關案件：`1943-McCullochPitts神經元.md`、`1969-MinskyPapert批判.md`、`1986-反向傳播演算法.md`。
