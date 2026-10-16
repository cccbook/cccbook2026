# 1928 - von Neumann 極小極大

## 案件摘要
1928 年，25 歲的 John von Neumann 發表《論社會博弈理論》（Zur Theorie der Gesellschaftsspiele）：證明**極小極大定理**——**兩人零和博弈必有最優策略**：

$$\max_a \min_b = \min_b \max_a$$

（你所能保證的最大收益 = 對手所能造成的最小損失——**混合策略**（隨機化）下成立。）**博弈論的誕生**——從「賭徒的直覺」（Pascal–Fermat 1654，見 `1654-PascalFermat機率.md`）到「理性的數學」——**經濟學、政治學、軍事、AI（AlphaGo 的極小極大搜尋）的基礎**。

## 前因 -- 為什麼會有這個案子
**兩千年的博弈智慧**：
- **孫子（前 500）**：「知己知彼」——軍事博弈的直覺
- **Zermelo（1913）**：西洋棋的定理——**完美信息博弈有必勝/必和策略**（但沒有混合策略）
- **Borel（1921）**：提出**混合策略**（隨機化）的想法——但未能證明一般定理

**von Neumann 的問題**：**兩人零和博弈**（我贏 = 你輸）中，**混合策略**下是否有「最優解」？

**von Neumann 的環境**：布達佩斯的神童（6 歲心算除八位數、8 歲懂微積分），1926 年赴 Göttingen（Hilbert 的門下）——**數學、物理、經濟、電腦的四棲天才**。

## 線索與推理 -- 數學式、程式、理論

### 零和博弈與混合策略
**兩人零和博弈**：收益矩陣 $A$（$a_{ij}$ = 我選策略 $i$、對手選 $j$ 時我的收益；對手的收益是負的）。

**純策略的困境**：固定策略會被預測——**對手針對**：

$$\max_i \min_j a_{ij} \ne \min_j \max_i a_{ij} \quad \text{（純策略下通常不等）}$$

（剪刀石頭布：沒有純策略最優——固定出剪刀必輸。）

**混合策略**：**隨機化**——以機率分佈 $p$ 選策略：

$$\text{期望收益} = p^T A q \quad \text{（} p, q \text{ 是雙方的機率分佈）}$$

### 極小極大定理
**von Neumann 定理（1928）**：

$$\max_p \min_q \; p^T A q = \min_q \max_p \; p^T A q$$

（**混合策略下相等**——存在「值」$v^*$：我能保證 $v^*$，對手能把我壓到 $v^*$。）

**推理（凸分析）**：
- $\min_q p^T A q$ 是 $p$ 的**凹函數**（線性的 min——凸組合）
- $\max_p$ 的最大化——**極小極大 = 凹函數的最大化**
- **Kakutani 不動點 / 線性規劃的對偶性**：零和博弈 ⟺ 線性規劃（LP 的對偶，見 `../隨機算法/1998-HalesKepler猜想.md`）——**博弈與最佳化的等價**

**剪刀石頭布**：混合策略 $\left(\frac{1}{3}, \frac{1}{3}, \frac{1}{3}\right)$——值 $v^* = 0$（公平）——**隨機化對抗預測**（與 Yao 原理同源，見 `../隨機算法/1985-Yao計算隨機性.md`）。

### 程式碼：極小極大

```python
import random

# 零和博弈：剪刀石頭布（收益矩陣，從我的視角）
A = [[0, -1, 1],      # 我出剪刀：vs 剪刀=0、石頭=-1、布=+1
     [1, 0, -1],      # 石頭
     [-1, 1, 0]]      # 布

def expected_payoff(p, q):
    return sum(p[i] * q[j] * A[i][j] for i in range(3) for j in range(3))

# 極小極大：均勻混合策略 (1/3, 1/3, 1/3)
p_star = [1/3, 1/3, 1/3]
print(f"均勻策略的期望收益（vs 任何純策略）：")
for j, name in enumerate(["剪刀", "石頭", "布"]):
    q = [1 if i == j else 0 for i in range(3)]
    print(f"  對手出 {name}：{expected_payoff(p_star, q):.4f}")
# 全部 = 0——值 v* = 0，公平 ✓

# 蒙地卡羅驗證：極小極大策略 vs 隨機對手
random.seed(42)
total = 0
for _ in range(100000):
    i = random.choices([0, 1, 2], p_star)[0]       # 極小極大
    j = random.randrange(3)                        # 隨機對手
    total += A[i][j]
print(f"蒙地卡羅：期望收益 = {total/100000:.4f} ≈ 0 ✓")

# 極小極大的搜尋（AlphaGo 的基礎）：電腦博弈
def minimax_search(state, depth, maximizing):
    """極小極大搜尋：兩人完美信息博弈的決策"""
    if depth == 0:
        return evaluate(state)                     # 葉節點評分
    children = successors(state)
    if maximizing:
        return max(minimax_search(c, depth-1, False) for c in children)
    else:
        return min(minimax_search(c, depth-1, True) for c in children)

def evaluate(s): return s.get("score", 0)
def successors(s): return [{**s, "score": s.get("score", 0) + d} for d in [1, -1]]

print(f"\n極小極大搜尋（depth=3）= {minimax_search({'score': 0}, 3, True)}")
print("AlphaGo 的基礎：極小極大 + 蒙地卡羅樹搜索（1946 蒙地卡羅 + 1928 極小極大）")
```

### 博弈論的誕生
**von Neumann 的帝國**：**數學、物理（量子力學的數學基礎 1932）、經濟（博弈論）、電腦（架構 1945）——四棲天才**。

**偵探筆記**：von Neumann 的推理是「**隨機化對抗預測**」——混合策略讓對手無法針對。**與 Quicksort 的隨機樞紐（1961，見 `../隨機算法/1961-Hoare快速排序.md`）、Yao 原理（1985，見 `../隨機算法/1985-Yao計算隨機性.md`）同源**：**隨機化的價值在於「不可預測性」**——博弈論是這個思想的數學化。

## 結案 -- 後果與影響
- **博弈論的誕生**：從賭徒直覺到理性的數學——經濟學的革命（與 Pascal–Fermat 1654 的賭局譜系匯流）。
- **零和博弈 = 線性規劃**：對偶性——**博弈與最佳化的等價**（Dantzig 1947 單純形法的動機之一）。
- **混合策略與 AI**：AlphaGo 的極小極大搜尋 + 蒙地卡羅樹搜索——**AI 的決策基礎**。
- **軍事的運用**：冷戰的核威懾（互相保證毀滅 MAD）——**博弈論的國際政治**。
- **電腦的誕生**：von Neumann 的四棲——**博弈論與電腦的同一人**（曼哈頓計畫、EDVAC）。
- **Zermelo 的先聲**：西洋棋定理（1913）——完美信息博弈的策略存在性。

## 關鍵人物與文獻
- **John von Neumann**（1903–1957）：Zur Theorie der Gesellschaftsspiele (1928)；量子力學的數學基礎 (1932)、EDVAC (1945)
- **Ernst Zermelo**（1871–1953）：西洋棋定理 (1913)
- **Émile Borel**（1871–1956）：混合策略的想法 (1921)
- **John Nash**：非零和的推廣（1950，見 `1950-Nash均衡.md`）
- 交叉參照：`1654-PascalFermat機率.md`、`../隨機算法/1985-Yao計算隨機性.md`、`../隨機算法/1998-HalesKepler猜想.md`、`1950-Nash均衡.md`
