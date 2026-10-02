# 1952 -- Harry Markowitz《投資組合選擇》：分散風險變成數學

## 案件描述

1952 年 3 月，一位 25 歲的芝加哥大學博士生 Harry Markowitz 在《Journal of Finance》發表了短短 14 頁的論文《投資組合選擇》（Portfolio Selection）。這篇論文做了一件改變整個金融業的事：

> **把「不要把雞蛋放在同一個籃子裡」這句古老的諺語，變成可以求解的數學最佳化問題。**

1990 年，Markowitz 因這篇論文獲得諾貝爾經濟學獎。評審委員稱之為「華爾街第一次革命」。

## 前因：投資學的黑暗時代

- 1950 年代的投資學教科書還在教「選好股票」：強調公司的品質、股息記錄、產業前景——**只看個股，不看組合**。
- 凱因斯主義盛行，但投資決策完全沒有數學基礎。
- Cowles（1933）已經證明預測無用，但「那投資人該怎麼辦？」沒有人有系統性的答案。
- **線索**：Markowitz 在準備博士論文時，讀到 John Burr Williams（1938）的《投資價值理論》，書中主張股票的價值等於未來股息的現值。Markowitz 立刻抓到矛盾：**如果每個人都最大化期望報酬，那為什麼不把所有錢都投進期望報酬最高的那一檔股票？**

## 推理過程

### 線索一：報酬不是唯一的目標——還有風險

Markowitz 的洞察：投資人關心的是「**期望報酬**」與「**風險**」的組合，而不是單獨的期望報酬。他提出用**變異數**衡量風險。

### 線索二：相關性是分散的靈魂

關鍵數學：對 $n$ 檔資產，權重 $\mathbf{w} = (w_1, \dots, w_n)^T$，期望報酬向量 $\boldsymbol{\mu}$，共變異數矩陣 $\Sigma$：

$$E[R_p] = \mathbf{w}^T \boldsymbol{\mu}, \qquad \mathrm{Var}(R_p) = \mathbf{w}^T \Sigma \, \mathbf{w}$$

**展開變異數**：

$$\mathbf{w}^T \Sigma \, \mathbf{w} = \sum_i w_i^2 \sigma_i^2 + \sum_{i \neq j} w_i w_j \, \sigma_{ij}$$

當資產間相關係數 $\rho_{ij} < 1$ 時，組合變異數**小於**個股變異數的加權平均——這就是「分散投資降低風險」的數學證明。極端情況下，若 $\rho = -1$，可以構造出零風險組合。

### 線索三：效率前緣——一個二次規劃問題

Markowitz 把投資組合選擇寫成二次規劃（QP）：

$$\min_{\mathbf{w}} \; \mathbf{w}^T \Sigma \, \mathbf{w} \quad \text{s.t.} \quad \mathbf{w}^T \boldsymbol{\mu} = \mu^*, \quad \mathbf{w}^T \mathbf{1} = 1$$

對每個目標報酬 $\mu^*$ 求解，得到的最低風險組合連成一條曲線——**效率前緣（Efficient Frontier）**。理性投資人只應該選擇前緣上的組合。

Markowitz 在 1950 年代初期用**手工計算**（參考線性規劃的 Dantzig 單純形法）求解小規模問題——這也是二次規劃演算法發展的動力之一。

## 現代程式重現：計算效率前緣

```python
import numpy as np
from scipy.optimize import minimize

mu = np.array([0.10, 0.12, 0.07, 0.09])          # 期望報酬
Sigma = np.array([[0.04, .01, .002, 0],
                  [.01, .06, .003, .005],
                  [.002, .003, .01, .001],
                  [0, .005, .001, .025]])        # 共變異數矩陣
n = len(mu)

def port_var(w): return w @ Sigma @ w

# 最小變異數組合（s.t. 權重和 = 1）
cons = [{'type': 'eq', 'fun': lambda w: w.sum() - 1}]
res = minimize(port_var, np.repeat(1/n, n), constraints=cons)
print("最小變異數組合權重:", res.x)
print("組合波動率:", np.sqrt(port_var(res.x)))

# 掃描目標報酬，畫出效率前緣
for mu_star in np.linspace(0.07, 0.12, 20):
    cons2 = cons + [{'type': 'eq', 'fun': lambda w: w @ mu - mu_star}]
    r = minimize(port_var, np.repeat(1/n, n), constraints=cons2)
    # (mu_star, sqrt(port_var(r.x))) 即前緣上的一點
```

## 後果

- **1959 年**，Markowitz 出版專書《Portfolio Selection: Efficient Diversification of Investments》，加入完整的計算方法。
- **1964 年**，他的學生 Sharpe 從這套框架中提煉出 CAPM（見 [1964-SharpeCAPM.md](1964-SharpeCAPM.md)）。
- **1990 年**諾貝爾獎。
- 現代資產管理業的根基：**所有現代資產配置、風險平價、Robo-advisor 的數學核心都是 Markowitz 的 $\mathbf{w}^T \Sigma \mathbf{w}$。**
- Markowitz 自己曾說，他的貢獻不是告訴投資人「如何選股」，而是「**如何在不選股的前提下思考風險**」。
- 著名的盲點：Markowitz 框架依賴 $\Sigma$ 的估計，而實務上 $\Sigma$ 難以準確估計（高維度下估計誤差巨大）——這催生了後來的 shrinkage 估計（Ledoit–Wolf 2004）與因子模型。

## 偵探筆記

- 動機：Williams 股息現值理論的內在矛盾
- 工具：二次規劃、共變異數矩陣、效率前緣
- 遺產：現代資產管理業的數學根基
- 盲點：估計誤差、常態分配假設、單期框架（沒有跨期動態）

## 參考資料

- Markowitz, H. (1952). "Portfolio Selection". *Journal of Finance*, 7(1), 77–91.
- Markowitz, H. (1959). *Portfolio Selection: Efficient Diversification of Investments*. Wiley.
