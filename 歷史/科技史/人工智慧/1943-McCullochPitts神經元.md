# 1943 - McCulloch–Pitts 神經元（機器之心的第一塊積木）

## 案件摘要
1943 年，神經生理學家 Warren McCulloch 與 18 歲的邏輯天才 Walter Pitts 在《Bulletin of Mathematical Biophysics》發表
〈A Logical Calculus of the Ideas Immanent in Nervous Activity〉：
用一個極簡的數學模型描述神經元——加權輸入、超過閾值就「放電」。
$$y = H\!\left(\sum_i w_i x_i - \theta\right).$$
這是人工智慧偵探案的第一塊積木：**神經元的行為，可以用邏輯與算術完全描述**。

## 前因 -- 為什麼會有這個案子
- **大腦之謎**：神經元已被確認是大腦的基本單位（Cajal, 1900s），但神經元如何產生「思想」，完全無人能數學化。
- **邏輯的現代化**：Russell 與 Whitehead 的《數學原理》(1910–1913) 已把數學化約為邏輯；Turing 機（1936，見計算理論案件）已把「計算」形式化。
- **偵探的跨域聯手**：McCulloch 懂大腦、Pitts 懂邏輯。兩人在芝加哥相遇，決定用 Turing 機的語言描述神經元——**生理學 + 邏輯學 = 機器之心**。

## 線索與推理 -- 數學式、程式、理論

### 第一步：神經元的「口供」
McCulloch 觀察神經元的行為特徵：
1. 有多個輸入（樹突），有興奮性與抑制性。
2. 輸入加權總和超過閾值就**放電**（全有全無律，all-or-none）。
3. 輸出只有 0 或 1 兩種狀態。

### 第二步：數學模型
$$y = H\!\left(\sum_i w_i x_i - \theta\right), \qquad H(z) = \begin{cases}1 & z \ge 0 \\ 0 & z < 0\end{cases}$$
$w_i$ 權重（興奮 $>0$、抑制 $<0$）、$\theta$ 閾值、$H$ 階梯函數。

### 第三步：驚人的推論——邏輯閘的誕生
適當選 $w_i$ 與 $\theta$，單一神經元就能實作所有基本邏輯閘：
- **AND**：$w=(1,1), \theta=2$ → $y = x_1 \wedge x_2$
- **OR**：$w=(1,1), \theta=1$ → $y = x_1 \vee x_2$
- **NOT**：$w=(-1), \theta=0$ → $y = \neg x_1$
- **NAND**：$w=(-1,-1), \theta=-1$ → $y = \neg(x_1 \wedge x_2)$

而 NAND 閘是**萬能閘**——任何布林函數都能用 NAND 組合（Sheffer, 1913）。
**推論**：神經元網路 = 布林電路 = Turing 機可計算的一切。McCulloch 與 Pitts 據此宣稱：大腦在原理上是一台圖靈機。

### Python 驗證：McCulloch–Pitts 神經元實作邏輯閘

```python
import numpy as np

def mcp_neuron(x, w, theta):
    return 1 if np.dot(w, x) >= theta else 0

gates = {
    "AND":  (lambda x: mcp_neuron(x, [1, 1], 2)),
    "OR":   (lambda x: mcp_neuron(x, [1, 1], 1)),
    "NOT":  (lambda x: mcp_neuron([x[0]], [-1], 0)),
    "NAND": (lambda x: mcp_neuron(x, [-1, -1], -1)),
}
for name, g in gates.items():
    print(name, [g(x) for x in [(0,0),(0,1),(1,0),(1,1)]])
```
輸出：
```
AND [0, 0, 0, 1]
OR  [0, 1, 1, 1]
NOT [1, 1, 0, 0]
NAND [1, 1, 1, 0]
```

## 結案 -- 後果與影響
- **神經網路的開端**：1957 年 Rosenblatt 的感知器（見「1957-Perceptron感知器.md」）就是把閾值 $\theta$ 與權重 $w_i$ 變成**可學習**參數。
- **邏輯閘 → 數位電腦**：McCulloch–Pitts 模型直接影響早期數位電路設計——神經科學反向啟發了電腦硬體。
- **符號 AI 的哲學基礎**：「思想 = 邏輯運算」的宣言，催生了 1956 年的 Dartmouth 會議（見「1956-Dartmouth會議.md」）。
- 限制：模型不可學習（權重寫死）、無法處理連續輸出、階梯函數不可微——這些缺口正是日後感知器與反向傳播要補的洞。
- Pitts 的悲劇結局：這位天才晚年被維納拒絕往來，手稿未發表而終；機器之心的第一塊積木，由一位 18 歲的流浪少年砌下。

## 關鍵人物與文獻
- **W. S. McCulloch & W. Pitts**：Bulletin of Mathematical Biophysics 5, 115 (1943)。
- **Sheffer**：NAND 萬能閘 (1913)；**Turing**：計算理論 (1936)。
- 相關案件：`1957-Perceptron感知器.md`、`1956-Dartmouth會議.md`。
