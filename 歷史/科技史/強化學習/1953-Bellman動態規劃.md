# 1953 - Bellman 動態規劃（多期決策之謎化為遞迴）

## 案件摘要
1953 年，Richard Bellman 在 RAND 公司的研究報告中發明了**動態規劃 (Dynamic Programming)** 與
**Bellman 方程**。他證明：多期決策問題
$$\max_\pi \; \mathbb{E}\left[\sum_{t=0}^{T} \gamma^t r_t\right]$$
不必暴力枚舉所有策略（$|\mathcal{A}|^{T}$ 種！），而可以用一個遞迴方程解決——
$$V(s) = \max_a \big[ r(s,a) + \gamma V(s') \big].$$
這是強化學習的數學地基。**試誤有了思想（Turing 1950），數學骨架在這裡出現。**

## 前因 -- 為什麼會有這個案子
- **RAND 的軍事決策問題**：二戰後 RAND 需處理飛彈路徑、後勤補給、庫存調度等
  「一連串互相糾纏的決策」——今天省一點，明天會吃虧。**時間耦合是兇手。**
- **暴力枚舉的絕望**：$T$ 期、每期 $m$ 個選擇，就有 $m^T$ 種策略。$T=30, m=10$ 時是 $10^{30}$，
  宇宙的原子都不夠數。古典變分法（Euler–Lagrange，見微積分史）只能處理連續情形。
- **名稱的偵探花絮**：Bellman 為什麼叫 "dynamic programming"？他自述——當年國防部長
  Wilson 討厭 "research"，他故意選一個神祕的名字「動態的、程式化的」，
  讓官僚聽不懂也砍不掉。**命名本身就是一場偽裝行動。**

## 線索與推理 -- 數學式、程式、理論

### 核心推理：最優性原理 (Principle of Optimality)
Bellman 的洞察只有一句話：
> 「最優策略有這樣的性質：無論初始狀態與初始決策為何，剩餘的決策對前一個狀態而言，
> 仍構成一個最優策略。」

翻譯成數學：既然「未來的最優」與「過去怎麼走到這裡」無關（馬爾可夫性），
那麼每一步只需問「**眼前這一步 + 未來的價值**」：
$$\boxed{V^*(s) = \max_{a \in \mathcal{A}(s)} \Big[ r(s,a) + \gamma \sum_{s'} P(s'|s,a)\, V^*(s') \Big]}$$
這就是 **Bellman 方程**。狀態數 $|S|$，每個狀態只需 $\mathcal{O}(|S|^2 |\mathcal{A}|)$ 次運算，
把 $m^T$ 降成多項式時間。

### 計算量偵查

| 方法 | 複雜度 | $T=30, m=10, |S|=100$ |
|------|--------|----------------------|
| 暴力枚舉所有策略 | $m^T$ | $10^{30}$（不可能） |
| 動態規劃 | $|S|^2 |\mathcal{A}| \cdot K$ | $10^5 \cdot K$（毫秒級） |

### Python：最短路徑的 Bellman 方程（值迭代）

```python
import numpy as np

def value_iteration(P, r, gamma=0.9, tol=1e-10):
    # P[s,a,s'] 轉移機率, r[s,a] 獎勵
    V = np.zeros(P.shape[0])
    while True:
        Q = r + gamma * np.einsum('sak,k->sa', P, V)  # Bellman 算子
        V_new = Q.max(axis=1)
        if np.abs(V_new - V).max() < tol: break
        V = V_new
    return V, Q.argmax(axis=1)

# 走廊：0~3 四格，動作 0/1 = 往右/往左，終點 = 3
P = np.zeros((4, 2, 4)); r = np.zeros((4, 2))
for s in range(3):
    P[s,0,s+1], P[s,1,max(s-1,0)] = 1, 1
    r[s,0], r[s,1] = (1.0 if s+1 == 3 else 0.0), 0.0
P[3,0,3], P[3,1,3] = 1, 1                 # 終點吸收
V, pi = value_iteration(P, r)
print(V.round(3), pi)                     # 值隨距終點遞減；策略指向終點
```
輸出：
```
[0.81 0.9 1. 0.] [0 0 0 0]   # V(3)=0，越靠近終點價值越接近 1
```

### 從 Bellman 方程到強化學習的橋
$$V(s) \leftarrow \underbrace{\max_a \big[r + \gamma V(s')\big]}_{\text{Bellman 算子}}$$
- 動態規劃需要**知道模型** $P, r$（model-based）。
- 1959 年 Samuel、1988 年 Sutton、1989 年 Watkins 的問題變成：
  **不知道 $P, r$ 時，能不能靠試誤逼近同一個方程？**——答案是能，這就是 Q-learning。

## 結案 -- 後果與影響
- **強化學習的數學基礎**：Bellman 方程是 MDP（馬爾可夫決策過程）的核心。
  之後所有的 RL 演算法（TD、Q-learning、DQN、AlphaGo）都是在**逼近或求解這個方程**。
- **最優控制理論**：Bellman 的動態規劃與 Pontryagin 的極大值原理（1956）並立，
  成為現代控制的兩大支柱；離散版叫 DP，連續版叫 HJB 方程。
- **演算法史的地位**：動態規劃成為演算法設計五大範式之一（分治、貪心、DP、回溯、隨機）。
- 後續案件：`1959-Samuel跳棋自學程式.md` 把 DP 思想帶進下棋、
  `1988-SuttonTD學習.md` 把它變成無模型的試誤學習。

## 關鍵人物與文獻
- **Richard Bellman**：RAND Report P-259 (1953)；《Dynamic Programming》(1957, Princeton)。
- **Wilson 部長**：逼出「dynamic programming」這個神祕名字的官僚（黑色幽默的來源）。
- 相關案件：`1957-Bellman最優性原理.md`、`1988-SuttonTD學習.md`、`1989-WatkinsQ-learning.md`。
