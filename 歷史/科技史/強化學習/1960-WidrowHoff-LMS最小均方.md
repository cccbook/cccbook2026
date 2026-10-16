# 1960 - Widrow–Hoff LMS 最小均方（神經元開始會「按獎懲調整權重」）

## 案件摘要
1960 年，Stanford 的 Bernard Widrow 與 Ted Hoff（後來 Intel 4004 的設計者）發表
**ADALINE (Adaptive Linear Neuron)** 與 **LMS (Least Mean Squares)** 演算法。
神經元不再是 Perceptron（1958，Rosenblatt）那種「對錯二元的懲罰」，
而是**連續誤差驅動的權重調整**：
$$w \leftarrow w + \eta \, (d - y)\, x.$$
這是最速下降法（見微積分史）在自適應系統的化身，也是神經網路與強化學習的共用引擎。

## 前因 -- 為什麼會有這個案子
- **Perceptron 的二元懲罰**：Rosenblatt 1958 年的感知器只會說「對/錯」，錯了就整組翻轉權重——
  收斂慢、對雜訊敏感，而且**線性不可分的資料（XOR）直接死當**。**二元性是兇手。**
- **濾波器的需求**：貝爾實驗室的電話線路需要自適應濾波器——雜訊是連續的，
  權重調整也必須是連續的、平滑的。
- **Widrow 的偵探直覺**：與其問「對不對」，不如問「**差多少**」——把懲罰從二元改為平方誤差：
  $$E = \tfrac{1}{2}(d - y)^2 = \tfrac{1}{2}(d - w^\top x)^2.$$
  這是一個光滑的凸函數，梯度直接可算。

## 線索與推理 -- 數學式、程式、理論

### 核心推理：梯度的即時取樣
對 $E$ 求梯度：
$$\nabla_w E = -(d - w^\top x)\, x.$$
最速下降要「整批資料算完再更新」（batch gradient），但 Widrow–Hoff 的洞見是：
**每來一個樣本就更新一次**——這就是**隨機梯度下降 (SGD)** 的先驅：
$$\boxed{w_{k+1} = w_k + \eta \, (d_k - y_k)\, x_k}$$
稱為 **delta rule**。當 $\eta$ 足夠小，期望值方向與 batch gradient 相同，必收斂到最小均方解。

### 幾何偵查：為什麼平方誤差必收斂？
$E(w)$ 是 $w$ 的二次凸函數（碗狀），Hessian 為 $X^\top X \succeq 0$。
梯度永遠指向碗底，步長 $\eta < 2/\lambda_{\max}$ 時必收斂：
$$\|w_k - w^*\| \le \max_i |1 - \eta \lambda_i|^k \, \|w_0 - w^*\|.$$
**Perceptron 只能保證「可分時收斂」，LMS 保證「任何情況下收斂到最優線性解」。**

### Python：LMS vs Perceptron 收斂偵查

```python
import numpy as np

X = np.array([[0,0],[0,1],[1,0],[1,1]], float)
d = np.array([0, 0, 0, 1], float)             # AND 問題（0/1 標記）

def lms(X, d, eta=0.1, iters=200):
    w = np.zeros(2); hist = []
    for _ in range(iters):
        y = X @ w
        w += eta * ((d - y) @ X) / len(X)     # delta rule
        hist.append(((d - X@w)**2).mean())
    return w, hist

w, hist = lms(X, d)
print("w =", w.round(3), " 最終 MSE =", f"{hist[-1]:.4f}")
print("誤差衰減:", [f"{e:.3f}" for e in hist[:4]], "->", f"{hist[-1]:.3f}")
```
輸出：
```
w = [0.333 0.333]  最終 MSE = 0.0833
誤差衰減: [0.226, 0.205, 0.188, 0.173] -> 0.083
```
誤差平滑指數衰減——碗狀地貌的必然結果。

### LMS 與 RL 的橋樑
LMS 的更新項 $(d - y)$ 就是**誤差訊號**。強化學習中，這個誤差變成
$$\delta = r + \gamma V(s') - V(s) \qquad \text{(TD 誤差)}$$
權重更新 $w \leftarrow w + \eta\, \delta\, \phi(s)$。
**LMS 是 TD 學習的特例**：當 $\gamma = 0$、$r = d - V(s)$ 時兩者完全相同。
Widrow–Hoff 因此被 Sutton 稱為「RL 學習規則的直系祖先」。

## 結案 -- 後果與影響
- **SGD 的先驅**：delta rule 是現代深度學習的核心引擎——反向傳播 (1986) 的每一步
  都是 delta rule 的鏈式推廣。
- **自適應濾波器**：ADALINE 直接商用於數據機的回音消除、電話線路均衡——
  LMS 是**第一個賺到錢的機器學習演算法**。
- **神經網路的火種**：1969 年 Minsky–Papert 的《Perceptrons》批判凍結了神經網路研究，
  但 LMS 因為有工程應用而存活，成為寒冬中的火種。
- **RL 的祖先**：TD 學習（1988）明言自己是「LMS 在時間序樂上的推廣」。
- Hoff 後來參與設計 Intel 4004 微處理器——**同一雙手，先教神經元學習，再造出電腦心臟**。

## 關鍵人物與文獻
- **Bernard Widrow & Ted Hoff**：IRE WESCON Convention Record (1960)。
- **Frank Rosenblatt**：Perceptron（1958，本案的「對手」）。
- 相關案件：`1972-Klopf獎懲塑造.md`、`1988-SuttonTD學習.md`、`2013-DQN打Atari.md`。
