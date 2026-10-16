# 1957 - Perceptron 感知器

## 案件摘要
1957 年，Cornell 航空實驗室的 Frank Rosenblatt 提出感知器（Perceptron）：**M-P 神經元 + 可學習的權重**。它不只是模型，還附帶史上第一個學習收斂定理：

> **若訓練樣本線性可分，感知器必在有限步內收斂。**

$$\Delta w_i = \eta\,(t - y)\,x_i$$

其中 $t$ 是教師訊號、$y$ 是感知器輸出。這是赫布規則加上誤差調制的結果——神經網路第一次有「保證會學會」的數學證明。本案的本質是：**學習的模型第一次可以被證明收斂，也可以被證明有極限（XOR）**——榮耀與謀殺同時埋在這一行公式裡。

## 前因 -- 為什麼會有這個案子
- 1943 年 M-P 神經元能算邏輯（見 1943-麥卡洛克皮茨邏輯神經元.md），但權重手工指定；1949 年 Hebb 規則讓權重可學（見 1949-Hebb學習規則.md），但無教師訊號、無收斂保證。
- Rosenblatt 的問題：**能不能證明一個網路「一定學得會」？** 他要的不是描述性規則，而是有收斂定理的演算法。
- Hebb 規則的缺口：$\Delta w_i = \eta x_i y$ 只在兩端同時活躍時加強，沒有「學錯了就修正」的機制——Rosenblatt 把 $y$ 換成誤差 $(t-y)$，補上這個洞。
- 1950 年圖靈測試的兒童機器綱領（見 1950-圖靈測試.md）提到「獎勵與懲罰」——誤差 $(t-y)$ 的正負正是懲罰與獎勵的數學化身。
- 1956 年 Dartmouth 會議把「神經網路自組織」列入議題（見 1956-Dartmouth會議.md）——Rosenblatt 是會議圈內人，感知器是該議題第一個工程化成果。
- 時代動機：冷戰與軍方資金——美國海軍研究辦公室（ONR）資助 Rosenblatt，看中的是「能自動辨識圖案的機器」。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：感知器的數學結構
感知器 = M-P 神經元 + 誤差驅動的學習：

$$y = H\!\left(\mathbf{w}^\top \mathbf{x} - \theta\right), \qquad \Delta \mathbf{w} = \eta\,(t - y)\,\mathbf{x}$$

更新規則的四種情況：

| $t$ | $y$ | 誤差 $t-y$ | 更新效果 |
|---|---|---|---|
| 1 | 1 | 0 | 不動（答對了） |
| 0 | 0 | 0 | 不動（答對了） |
| 1 | 0 | $+1$ | 權重沿 $\mathbf{x}$ 方向增加（補強漏報） |
| 0 | 1 | $-1$ | 權重沿 $\mathbf{x}$ 方向減少（抑制誤報） |

關鍵推理：與赫布規則 $\Delta w_i = \eta x_i y$ 對照，感知器只是把「突觸後活性 $y$」換成「誤差 $t-y$」——**用教師訊號調制共激活**。這一換，讓無教師的聯想變成有教師的分類。

### 第二條線索：收斂定理——「一定學得會」的證明
**感知器收斂定理**（Perceptron Convergence Theorem, 1960/1962）：

> 若存在超平面 $\mathbf{w}^*$ 使所有樣本正確分類（即樣本集線性可分，存在間隔 $\gamma > 0$），則感知器演算法至多 $\dfrac{R^2}{\gamma^2}$ 次更新後收斂。

其中 $R = \max_i \|\mathbf{x}_i\|$ 是樣本的最大範數。證明骨架（偵探式三步）：
1. 每次犯錯，權重向量與理想分類器 $\mathbf{w}^*$ 的內積至少增加 $\gamma$：$\mathbf{w}_{k+1}^\top \mathbf{w}^* \ge \mathbf{w}_k^\top \mathbf{w}^* + \gamma$
2. 但權重範數至多增加 $R$：$\|\mathbf{w}_{k+1}\|^2 \le \|\mathbf{w}_k\|^2 + R^2$
3. 內積增長是線性的、範數增長是平方根級的——兩者矛盾在某有限步必然出現，故必收斂

這個證明的偵探意義：它把「學習」從心理學假說（Hebb）升格為**數學定理**。1960 年代其後發展出的間隔界（margin bounds）就是這條推理的直系後代——統計學習理論（Vapnik, SVM）的種子在此埋下。

### 第三條線索：XOR——榮耀的極限
收斂定理有前提：**線性可分**。Minsky 與 Papert 1969 年在《Perceptrons》中指出，單層感知器無法表達 XOR：

| $x_1$ | $x_2$ | XOR | 單層感知器能否分類 |
|---|---|---|---|
| 0 | 0 | 0 |  |
| 0 | 1 | 1 | ✗ 四點交叉，任何一條直線 |
| 1 | 0 | 1 | ✗ 都無法把 $(0,0),(1,1)$ 與 |
| 1 | 1 | 0 | ✗ $(0,1),(1,0)$ 分開 |

幾何推理：XOR 的正類兩點與負類兩點在平面上對角相望，任何直線都無法分開——單層感知器的假設空間裡沒有解。但 Minsky 與 Papert 也知道解法：**多層**（隱藏層）可以——兩個感知器各分一半，再合起來就是 XOR。問題是 1969 年沒有人會訓練多層網路（反向傳播要到 1986 年，見 1986-反向傳播演算法.md）。這個「知道極限、也知道解法、卻不會訓練」的僵局，就是第一次 AI 寒冬的直接兇手。

### 第四條線索：Mark I 感知器——硬體的承諾
Rosenblatt 不只做理論，還造了實體機器。Mark I Perceptron（1958–1960）：
- 輸入是一個 20×20 的光電池網格（400 個「視網膜」感受器）
- 權重由可變電位器（potentiometer）實作，馬達驅動的機構在訓練時物理地轉動電位器
- 學習是**機械運動**：每犯一次錯，馬達把對應電位器轉一點——$\Delta w = \eta(t-y)x$ 的物理版

這台機器讓「學習的機器」從思想實驗變成新聞：《紐約時報》1958 年報導感知器「將能走路、說話、有意識地自我複製」——記者誇大了，但 Rosenblatt 自己的論文相當克制。新聞的誇大後來反噬：當 1969 年極限被指出時，輿論的落差使整個領域被連坐懲罰。

### 第五條線索：Rosenblatt 的遠見——多層與隨機搜尋
常被忽略的事實：Rosenblatt 自己知道單層的極限。他在《Principles of Neurodynamics》（1962）中討論了多層系統（series-coupled perceptrons）與隨機搜尋的訓練方式：

- 他提出用**隨機擾動**訓練多層網路：隨機改變隱藏層權重，若整體錯誤下降就保留——這是「爬山法」（hill climbing）的版本
- 他也考慮過「反向傳播誤差」的觀念，但沒有找到可微激活 + 鏈式法則的組合——差一步就是歷史
- 他預言感知器「將成為能感知、認記、辨識的系統原型」——1990 年代的 CNN 完全兌現了這個預言

Rosenblatt 的悲劇結局：1969 年 Minsky 的批判、1971 年 ONR 停止資助、他在生日當天駕船出海溺亡（1971）——死後兩年，領域進入寒冬。直到 1986 年反向傳播，他的收斂定理與多層遠見才被追認為深度學習的遠祖。

## 結案 -- 後果與影響
- 神經網路有了第一個收斂定理：學習從假說變成數學，統計學習理論（SVM、margin bounds）由此發源。
- 硬體神經網路的先聲：Mark I 證明學習可以物理實作——2010 年代的神經形態晶片（neuromorphic chips）是它的遠代子孫。
- 第一次 AI 寒冬：Minsky 與 Papert 1969 年的 XOR 批判 + 新聞誇大的反噬，使神經網路研究在 1970 年代被逐出主流資金圈（見 1969-MinskyPapert批判.md）。
- 伏筆一：感知器收斂定理的證明骨架（間隔 $\gamma$、範數 $R$）→ Vapnik 的統計學習理論 → SVM（1995）→ 深度學習的泛化界。
- 伏筆二：XOR 極限 → 「需要多層」→ 1986 反向傳播（見 1986-反向傳播演算法.md）→ 2012 AlexNet（見 2012-AlexNetImageNet革命.md）——感知器的謀殺案在四十三年後平反。
- 伏筆三：誤差調制的赫布規則 $(t-y)x$ → 1960 ADALINE 的 delta rule（見 1960-ADALINE自適應線性元件.md）→ 梯度下降 → 反向傳播——一條從離散誤差到連續梯度的直線。
- 伏筆四：光電池視網膜 → 1959 Hubel & Wiesel 的視覺皮層研究（見 1959-HubelWiesel視覺皮層.md）→ 1989 LeCun 的 CNN——「機器看世界」的三代傳承。

## 關鍵人物與文獻
- Frank Rosenblatt：〈The Perceptron: A Probabilistic Model for Information Storage and Organization in the Brain〉, *Psychological Review*, 1958
- Frank Rosenblatt：《Principles of Neurodynamics》（1962），收斂定理的完整證明
- Minsky & Papert：《Perceptrons》（1969），XOR 極限的系統性分析
- Donald Hebb：赫布規則（1949），感知器學習規則的前身
- Warren McCulloch & Walter Pitts：M-P 神經元（1943），感知器的計算骨架
- 相關案件：1943-麥卡洛克皮茨邏輯神經元.md、1949-Hebb學習規則.md、1956-Dartmouth會議.md、1959-HubelWiesel視覺皮層.md、1960-ADALINE自適應線性元件.md、1969-MinskyPapert批判（科學與歷史/人工智慧/1969-MinskyPapert批判.md）、1986-反向傳播演算法（科學與歷史/人工智慧/1986-反向傳播演算法.md）

## 補充 -- 程式實作（python + numpy + pytorch）

本案公式 `Δw = η(t−y)x` 的最小可執行版本，見 `_code/1957-Perceptron.py`（已實測可跑）：

```python
# 1957 - Perceptron 感知器 (Rosenblatt)
# 公式: y = H(w·x - θ), Δw = η (t - y) x
import numpy as np
import torch

X_and = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], float)
t_and = np.array([0, 0, 0, 1])
X_xor = X_and
t_xor = np.array([0, 1, 1, 0])


def train_perceptron(X, t, eta=0.5, epochs=20):
    w = np.zeros(X.shape[1])
    b = 0.0
    for ep in range(epochs):
        err = 0
        for xi, ti in zip(X, t):
            y = 1 if w @ xi - b > 0 else 0
            w += eta * (ti - y) * xi
            b -= eta * (ti - y)
            err += abs(ti - y)
        if err == 0:
            return w, b, ep + 1
    return w, b, epochs


def predict(X, w, b):
    return np.array([1 if w @ xi - b > 0 else 0 for xi in X])


def main():
    np.random.seed(0)
    torch.manual_seed(0)
    for name, X, t in [("AND(線性可分)", X_and, t_and), ("XOR(線性不可分)", X_xor, t_xor)]:
        w, b, ep = train_perceptron(X, t)
        pred = predict(X, w, b)
        print(f"{name}: 收斂於第 {ep} 輪, w={np.round(w,2)}, b={round(b,2)}, "
              f"預測={pred.tolist()}, 正確={bool(np.array_equal(pred, t))}")
    print("torch 驗證 AND 點積:", (torch.tensor([1.0, 1.0]) @ torch.tensor([1.0, 1.0])).item(),
          "> 1.5 即激發 (M-P/感知器同源)")


if __name__ == "__main__":
    main()
```

執行結果（`python3 _code/1957-Perceptron.py`，numpy 2.4.5／torch 2.12.0）：

```
AND(線性可分): 收斂於第 6 輪, w=[1.  0.5], b=1.0, 預測=[0, 0, 0, 1], 正確=True
XOR(線性不可分): 收斂於第 20 輪, w=[-0.5  0. ], b=-0.5, 預測=[1, 1, 0, 0], 正確=False
torch 驗證 AND 點積: 2.0 > 1.5 即激發 (M-P/感知器同源)
```

程式解說：AND 在第 6 輪誤差歸零——這就是收斂定理的活體演示：線性可分則有限步必收斂。XOR 跑滿 20 輪仍錯兩題，且任何超平面都註定如此（見 1943 章補充的窮舉），正是 Minsky–Papert 1969 年判處的死刑。對照本文第一條線索的表格：更新只發生在答錯時（`t−y = ±1`），答對時權重不動——「用教師訊號調制的赫布規則」在此一覽無遺。
