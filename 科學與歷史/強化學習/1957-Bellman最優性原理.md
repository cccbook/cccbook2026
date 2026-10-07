# 1957 - Bellman 最優性原理（$V^*, Q^*$ 的誕生與心理學的匯流）

## 案件摘要
1957 年，Bellman 出版《Dynamic Programming》專書，把 1953 年的報告正式定名為
**最優性原理 (Principle of Optimality)**，並給出完整收斂性理論。
同年，Skinner 出版《Verbal Behavior》，把行為主義的「增強 (reinforcement)」推到頂點；
心理學的試誤學習（Thorndike 的效果律，1911）與數學的最優性原理，
兩條線索在 1957 年前後開始匯流——**強化學習這個詞，即將誕生。**

## 前因 -- 為什麼會有這個案子
- **1953 年的半成品**：Bellman 的 RAND 報告已有遞迴思想，但「收斂性」仍是懸案——
  迭代 $V_{k+1} = T V_k$ 真的會收斂到 $V^*$ 嗎？收斂要多快？**收斂性是兇手。**
- **心理學的百年懸案**：Thorndike 1911 年提出**效果律 (Law of Effect)**——
  「帶來滿意的行為更容易被重複」。貓的迷籠實驗證實了它，但沒人能把效果律寫成數學。
- **Bellman 的偵探直覺**：他把最優性原理從「啟發式直覺」升格為「可證明定理」，
  並引入 $V$（狀態價值）與後續的 $Q$（動作價值）函數，為效果律的數學化鋪路。

## 線索與推理 -- 數學式、程式、理論

### 核心推理：壓縮映射證收斂
Bellman 算子定義為
$$(T V)(s) = \max_a \Big[ r(s,a) + \gamma \sum_{s'} P(s'|s,a) V(s') \Big].$$
關鍵引理：$T$ 是**壓縮映射 (contraction)**：
$$\|T V_1 - T V_2\|_\infty \le \gamma \|V_1 - V_2\|_\infty, \qquad \gamma < 1.$$
證明只需一行：$\max_a [x_a + c] - \max_a [y_a + c] = \max_a[x_a] - \max_a[y_a]$，
而 $\gamma$ 的折扣吸收了狀態差異。
由 Banach 不動點定理（見微積分史），$T$ 有唯一不動點 $V^*$，且
$$V_k = T^k V_0 \Longrightarrow \|V_k - V^*\|_\infty \le \gamma^k \|V_0 - V^*\|_\infty.$$
**收斂速度是指數級的**——誤差每輪縮小 $(1-\gamma)$ 倍。

### 效果律的數學化：從 Thorndike 到 $Q$
| 心理學（1911–1957） | 數學對應物 |
|---------------------|-----------|
| 刺激情境 | 狀態 $s \in \mathcal{S}$ |
| 行為反應 | 動作 $a \in \mathcal{A}$ |
| 滿意/厭惡 | 獎勵 $r \in \mathbb{R}$ |
| 效果律（重複帶來滿意的行為） | $\pi(a|s) \propto \exp(Q(s,a)/\tau)$ 或 $\epsilon$-greedy |
| 增強 (reinforcement) | $Q(s,a) \leftarrow Q(s,a) + \alpha\, \delta$ |

### Python：壓縮映射的指數收斂偵查

```python
import numpy as np

np.random.seed(0)
S, A = 5, 2
P = np.random.rand(S, A, S); P /= P.sum(axis=2, keepdims=True)   # 隨機 MDP
r = np.random.randn(S, A)

V_star = np.zeros(S)                        # 解析解（長期迭代）
for _ in range(500):
    V_star = (r + 0.9*np.einsum('sak,k->sa', P, V_star)).max(axis=1)

V = np.zeros(S); errs = []                  # 值迭代，追查誤差衰減
for k in range(10):
    V = (r + 0.9*np.einsum('sak,k->sa', P, V)).max(axis=1)
    errs.append(np.abs(V - V_star).max())

print("誤差 :", [f"{e:.2f}" for e in errs[:6]])
print("比值 :", [f"{errs[i+1]/errs[i]:.3f}" for i in range(5)])
```
輸出：
```
誤差 : ['5.48', '4.79', '4.29', '3.86', '3.47', '3.12']
比值 : ['0.874', '0.895', '0.899', '0.900', '0.900']
```
**誤差比值收斂到恰好 0.900**——壓縮映射的 $\gamma$ 界不是鬆界，而是**極限的精確值**
（誤差漸近衰減率 = Bellman 算子的主特徵值 $= \gamma$）。

## 結案 -- 後果與影響
- **收斂性成為標準配備**：之後每個 RL 演算法（TD 1988、Q-learning 1989）都必須回答
  「會不會收斂」——證明手法全部源自 Bellman 的壓縮映射框架。
- **$Q$ 函數的伏筆**：Bellman 定義了 $V^*(s)$；Watkins 1989 年將「狀態-動作」對的價值
  $Q^*(s,a)$ 提升為主角，成為無模型學習的基石。
- **心理學與數學的匯流**：Skinner 的行為主義在 1957 年達到頂峰卻隨即被喬姆斯基批判（1959），
  行為主義在心理學死亡，但它的數學幽靈在工程中重生為 RL。
- Thorndike 效果律 + Bellman 方程 = 增強學習的完整語義。

## 關鍵人物與文獻
- **Richard Bellman**：《Dynamic Programming》(Princeton University Press, 1957)。
- **B. F. Skinner**：《Verbal Behavior》(1957)；Thorndike 效果律（1911，先驅）。
- 相關案件：`1953-Bellman動態規劃.md`、`1972-Klopf獎懲塑造.md`、`1989-WatkinsQ-learning.md`。
