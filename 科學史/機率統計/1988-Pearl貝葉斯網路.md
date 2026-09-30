# 1988 - Pearl 貝葉斯網路（Probabilistic Reasoning in Intelligent Systems）

## 案件摘要
1988 年 Judea Pearl 出版《Probabilistic Reasoning in Intelligent Systems》，提出貝葉斯網路，用「有向無環圖 + 條件機率表」馴服了 AI 中的不確定性。這本書不只奠定了機率圖模型，更在 2011 年為 Pearl 贏得圖靈獎，並開啟了因果推論（do-calculus）的新學科。

## 前因 -- 為什麼會有這個案子
- 早期 AI（1960–70 年代）的專家系統依賴**符號邏輯**（規則、IF-THEN），面對現實世界的不確定性束手無策。
- 當時主流的處理方式：
  - **MYCIN 的確定因子（certainty factors）**：經驗性規則，缺乏機率基礎，會產生矛盾推論。
  - **模糊邏輯（fuzzy logic）**：處理「程度」而非「隨機性」，無法統一進機率架構。
- 完整的聯合機率表需要 $2^n - 1$ 個參數（$n$ 個二元變數），指數爆炸使機率方法在大型系統中不可行。
- 統計學家雖有機率理論，但缺乏「如何在圖結構上高效推論」的工具；AI 學家雖有演算法，卻缺乏機率基礎——Pearl 在兩個世界的交會處破案。

## 線索與推理 -- 數學式、程式、理論

### 貝葉斯網路：DAG + 條件機率表
貝葉斯網路是一個**有向無環圖（DAG）**$G = (V, E)$，每個節點 $X$ 有一個條件機率表：

$$
P(X \mid \text{parents}(X))
$$

聯合分布**鏈式分解**：

$$
P(X_1, \dots, X_n) = \prod_{i=1}^n P(X_i \mid \text{parents}(X_i))
$$

若每個節點的父母很少（如 $\le k$ 個），參數量從 $2^n - 1$ 降為 $O(n \cdot 2^k)$——**這就是打敗指數爆炸的關鍵**。DAG 的結構編碼了**條件獨立性**，是參數節省的來源。

### d-分離（d-separation）與條件獨立性
給定集合 $Z$，節點 $X$ 與 $Y$ 之間的資訊流被「阻斷」的判定規則：

- **鏈（chain）** $X \to M \to Y$：若 $M \in Z$，則阻斷。
- **分岔（fork）** $X \leftarrow M \to Y$：若 $M \in Z$，則阻斷。
- **對撞（collider）** $X \to M \leftarrow Y$：若 $M \notin Z$（且其後代都不在 $Z$ 中），則阻斷；**觀察對撞節點反而打開通路**（explaining away 效應）。

若所有 $X$-$Y$ 路徑都被阻斷，稱 $X \perp Y \mid Z$（d-分離）。**d-分離定理**：圖上的 d-分離蘊含機率上的條件獨立（在 faithful 分布下反之亦然）。

### 信賴傳播（belief propagation）
Pearl 提出**訊息傳遞演算法**：在樹狀結構上，每個節點與鄰居交換訊息 $\lambda$（證據向上）、$\pi$（因果向下），可在 $O(n)$ 時間內算出每個節點的後驗。在一般有環圖上，迴圈展開或 junction tree 演算法可處理。

訊息更新：

$$
\lambda_X(x) = \sum_{e} P(e \mid x) \prod_{c \in \text{children}} \lambda_c(x),
\qquad
\pi_X(x) \propto P(x \mid \text{parents}) \prod_{p \in \text{parents}} \pi_p(x)
$$

### 因果推論的誕生：do-calculus
Pearl 的更深洞察：**觀察 $X=x$ 與干預 $do(X=x)$ 是兩回事**。

- 觀察：$P(Y \mid X = x)$——被動看見。
- 干預：$P(Y \mid do(X = x))$——主動改變世界，截斷所有指向 $X$ 的因果箭頭。

**do-演算**三條公理（Pearl 1995）允許在因果圖上把干預表達式化約為可從觀察資料估計的形式：

1. **插入/刪除觀察**：$P(Y \mid do(Z), X, W) = P(Y \mid do(Z), W)$ 若 $Y \perp X \mid do(Z), W$。
2. **動作/觀察交換**：$P(Y \mid do(Z), do(X), W) = P(Y \mid do(Z), X, W)$ 若 $Z$ 阻斷所有 $X \to Y$ 的後門路徑。
3. **插入/刪除動作**：$P(Y \mid do(Z), do(X), W) = P(Y \mid do(Z), W)$ 若沒有 $X \to Y$ 的因果路徑。

對照：傳統的後門調整公式

$$
P(Y \mid do(X)) = \sum_z P(Y \mid X, z)\, P(z)
$$

（$z$ 遍歷滿足後門準則的協變數集合）。這是現代因果推論（含反事實、中介分析）的基石。

### Python 實作：雨–灑水器–草地貝葉斯網路

經典案例：`下雨(R) → 灑水器(S)`（下雨時灑水器關閉，為對撞前驅），`下雨(R) → 草地濕(W) ← 灑水器(S)`（$W$ 是對撞節點）。

```python
import numpy as np
from itertools import product

# 網路結構：R → W ← S（R 與 S 之間還有 R → S 這條邊）
# P(R=1) = 0.2
# P(S=1 | R=0) = 0.4,  P(S=1 | R=1) = 0.01   （下雨時灑水器關閉）
# P(W=1 | R, S) = 1 - (1 - R * 0.9) * (1 - S * 0.8)  （兩條來源任一有效即濕）

p_R = {0: 0.8, 1: 0.2}
p_S_given_R = {(0, 0): 0.6, (0, 1): 0.4, (1, 0): 0.99, (1, 1): 0.01}

def p_W(r, s, w):
    base = 1 - (1 - r * 0.9) * (1 - s * 0.8)
    return base if w == 1 else 1 - base

# 建立聯合分布（鏈式分解）
joint = {}
for r, s, w in product([0, 1], repeat=3):
    joint[(r, s, w)] = p_R[r] * p_S_given_R[(r, s)] * p_W(r, s, w)

assert abs(sum(joint.values()) - 1) < 1e-12   # 驗證機率總和為 1

def query(cond, target):
    """cond: dict 變數→值（證據），target: 變數名"""
    num = den = 0.0
    for (r, s, w), p in joint.items():
        state = {"R": r, "S": s, "W": w}
        if all(state[k] == v for k, v in cond.items()):
            den += p
            if state[target] == 1:
                num += p
    return num / den

print(f"P(草地濕)                    = {query({}, 'W'):.4f}")
print(f"P(下雨 | 草地濕)             = {query({'W': 1}, 'R'):.4f}")
print(f"P(下雨 | 草地濕, 灑水器關)    = {query({'W': 1, 'S': 0}, 'R'):.4f}")
print(f"P(灑水器開 | 草地濕)          = {query({'W': 1}, 'S'):.4f}")

# do-calculus：主動打開灑水器 vs 觀察灑水器開
def do_query(do_val, target):
    """干預：截斷指向 S 的邊，S 被強制設為 do_val"""
    num = den = 0.0
    for r, w in product([0, 1], repeat=2):
        s = do_val
        p = p_R[r] * p_W(r, s, w)      # P(R) * P(W | R, do(S))
        den += p
        state = {"R": r, "W": w}
        if state[target] == 1:
            num += p
    return num / den

print(f"--- 干預 vs 觀察 ---")
print(f"P(下雨 | 灑水器開)  [觀察]   = {query({'S': 1}, 'R'):.4f}")
print(f"P(下雨 | do(灑水器開))[干預] = {do_query(1, 'R'):.4f}")
```

執行結果展示了 **explaining away**：觀察到草地濕後 $P(R)$ 上升，但若同時觀察到「灑水器關閉」，$P(R)$ 又進一步上升（兩個解釋互相競爭）。而「觀察灑水器開」會降低 $P(R)$（下雨時灑水器通常關閉，兩者負相關），但「**主動打開**灑水器」（$do$）則**完全不影响** $P(R)$——因為干預截斷了 $R \to S$ 的因果箭頭。這正是 Pearl 說的「觀察與干預是兩回事」。

## 結案 -- 後果與影響
- **貝葉斯網路成為機率圖模型（PGM）的基礎**：Markov 隨機場、因子圖、動態貝葉斯網路（DBN）、隱馬可夫模型皆屬此家族。
- **因果推論的誕生**：do-calculus、結構因果模型（SCM）、反事實推論、中介分析，深刻影響流行病學、經濟學、社會科學。Pearl 因此獲 **2011 年圖靈獎**。
- 應用：診斷系統（微軟 Windows 的故障診斷）、基因網路、風險評估、推薦系統。
- 現代延續：causal discovery（從資料學習因果圖）、causal machine learning、do-calculus 的完備性證明（Shpitser & Pearl 2006）。
- Pearl 的《Causality》(2000)、《The Book of Why》(2018) 使因果思維普及到大眾。

## 關鍵人物與文獻
- **Judea Pearl**（UCLA）：貝葉斯網路之父、2011 年圖靈獎得主、因果推論奠基者。
- Pearl, J. (1988). *Probabilistic Reasoning in Intelligent Systems: Networks of Plausible Inference*. Morgan Kaufmann.
- Pearl, J. (1995). *Causal diagrams for empirical research*. Biometrika 82(4), 669–688.
- Pearl, J. (2000). *Causality: Models, Reasoning, and Inference*. Cambridge University Press.
- Pearl, J., & Mackenzie, D. (2018). *The Book of Why*. Basic Books.
- Koller, D., & Friedman, N. (2009). *Probabilistic Graphical Models*. MIT Press.
