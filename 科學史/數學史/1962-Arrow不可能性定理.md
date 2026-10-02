# 1962 - Arrow 不可能性定理

## 案件摘要
1951 年，Kenneth Arrow 出版《社會選擇與個人價值》：證明**不可能性定理**——**不存在**滿足合理條件的「完美投票制度」：

$$\text{任何投票制度} \implies \text{違反以下之一：無獨裁、無關選項獨立、Pareto、傳遞}$$

**民主的數學極限**——「多數決不完美」不是經驗觀察，是**定理**。孔多塞悖論（1785）的完整一般化——**社會選擇理論的誕生**。Arrow 51 歲獲**諾貝爾經濟學獎（1972）**——**史上最年輕的得主**。

## 前因 -- 為什麼會有這個案子
**孔多塞悖論（1785）**：法國數學家 Marquis de Condorcet 發現**多數決的循環**：

三人（A、B、C）對三個選項（x、y、z）的偏好：
- A：x > y > z
- B：y > z > x
- C：z > x > y

**多數決**：x vs y → x 贏（A、C）；y vs z → y 贏（A、B）；z vs x → z 财（B、C）——**x > y > z > x——循環！**（傳遞性崩塌）

**投票制度的設計**（19 世紀–20 世紀）：孔多塞方法、Borda 計分、比例代表——**每種制度都有缺陷**——**缺陷是偶然還是必然**？

**Arrow 的問題**：**是否存在滿足合理條件的完美投票制度**？

**Arrow 的背景**：紐約市立學院（大蕭條年代）、哥倫比亞博士——1948 年起斯坦福。**戰時的氣象預報**（與統計學家合作）啟發了他對「集體決策」的興趣。

## 線索與推理 -- 數學式、程式、理論

### 合理條件的公理化
**Arrow 的四條條件**：

1. **無限制域**（universal domain）：任何偏好組合都允許
2. **Pareto 原則**：所有人都偏好 x > y ⟹ 社會偏好 x > y
3. **無關選項獨立性**（IIA）：社會對 (x, y) 的偏好**只依賴**個人對 (x, y) 的偏好（與 z 無關）
4. **無獨裁**：不存在一個人，其偏好**永遠**決定社會偏好

**定理（Arrow 1951）**：

$$\text{條件 1–3} \implies \text{獨裁（違反條件 4）}$$

**白話**：滿足「無限制、Pareto、IIA」的投票制度**必然是獨裁**——**完美民主不可能**。$\blacksquare$

### 證明骨架：決定性聯盟的擴張
**推理**：考慮「決定性聯盟」（其偏好決定社會偏好的團體）：

1. **全體是決定性的**（Pareto）
2. **最小化**：取最小的決定性聯盟 $V$
3. **擴張引理**：用 IIa 分析 $V$ 對某選項的決定性——**推出 $V$ 的真子集也決定性**——**矛盾**（除非 $V$ 是單人）
4. **結論**：單人決定性 = **獨裁**。$\blacksquare$

**與 Nash 的不動點同源**：Arrow 的證明也是「**化約**」——把社會選擇化約為**聯盟結構的分析**（與 Nash 把博弈化約為不動點、Atiyah–Singer 把分析化約為拓撲同源的傳統）。

### 孔多塞悖論的重現
**數值驗證**：隨機偏好下多數決的**循環機率**：

$$P(\text{循環}) \approx \frac{1}{12}\text{？} \quad \text{（三選項三人的孔多塞機率隨人數增長）}$$

**Condorcet 的計算**：3 人 3 選項時循環機率 $\approx 5.6\%$——**隨人數增長**（無限人數時約 8.8%）——**多數決的傳遞性必然崩塌**（無限域下）。

### 程式碼：孔多塞悖論與不可能性

```python
import random
from itertools import permutations

def condorcet_winner(preferences, options):
    """多數決的孔多塞贏家（或循環）"""
    # 兩兩比較：多數決
    wins = {o: 0 for o in options}
    for x, y in permutations(options, 2):
        count = sum(1 for prefs in preferences
                    if prefs.index(x) < prefs.index(y))
        if count > len(preferences) / 2:
            wins[x] += 1
    # 循環：沒有人全贏
    winner = [o for o in options if wins[o] == len(options) - 1]
    return winner[0] if winner else "循環！"

def random_preferences(voters, options):
    """隨機偏好（無限制域）"""
    return [random.sample(options, len(options)) for _ in range(voters)]

random.seed(42)
options = ["x", "y", "z"]
# 孔多塞悖論的機率
for voters in [3, 9, 21, 99]:
    cycles = sum(1 for _ in range(2000)
                 if condorcet_winner(random_preferences(voters, options), options) == "循環！")
    print(f"{voters} 人：循環機率 = {cycles/2000:.3f}")
# 循環是「常態」——多數決的傳遞性必然崩塌（無限域）

# 不可能性定理的結構（聯盟的分析）
def arrow_demonstration():
    """Arrow 不可能性：條件 1-3 ⟹ 獨裁"""
    print("\nArrow 條件：無限制域、Pareto、IIA、無獨裁")
    print("定理：前三者 ⟹ 獨裁（違反第四）——完美民主不可能")
    print("證明：最小決定性聯盟的擴張 → 單人決定性 = 獨裁")
    print("教訓：投票制度的缺陷是必然，不是偶然")

arrow_demonstration()

# Borda 計分：另一種制度（也違反 IIA）
def borda_count(preferences, options):
    """Borda：排名分數（最後一名 0 分，遞增）"""
    scores = {o: 0 for o in options}
    for prefs in preferences:
        for i, o in enumerate(prefs):
            scores[o] += len(options) - 1 - i
    return max(scores, key=scores.get)

# IIA 的違反：加入無關選項改變結果
prefs1 = [["x", "y", "z"], ["x", "y", "z"], ["y", "z", "x"]]
prefs2 = [["x", "y", "w", "z"], ["x", "y", "w", "z"], ["y", "z", "w", "x"]]
print(f"\nBorda：無 w 時 = {borda_count(prefs1, ['x','y','z'])}，")
print(f"加入無關選項 w 後 = {borda_count(prefs2, ['x','y','w','z'])}")
print("IIA 違反：無關選項改變結果——每種制度都有此缺陷")
```

### 社會選擇理論的誕生
**譜系**：
- **Condorcet（1785）**：多數決循環——悖論的發現
- **Borda（1781）**：計分法——另一種制度
- **Arrow（1951）**：不可能性定理——**缺陷是必然**
- **Sen（1970）**：自由悖論（Pareto 與自由的衝突）——**擴展的不可能性**（諾貝爾 1998）
- **Gibbard（1973）/ Satterthwaite（1975）**：操縱的不可能性——**無「防操縱」的投票制度**

**偵探筆記**：Arrow 的推理是「**公理化 → 不可能性**」——不定義「完美的投票制度」，而是**公理化合理條件**，證明**條件互斥**。**與 Gödel 不完備（1931）、Nash 均衡（1950）同源的「公理化」傳統**：**把「理想」形式化，證明理想不可達**——社會選擇的極限是定理，不是經驗。

## 結案 -- 後果與影響
- **社會選擇理論的誕生**：投票制度的數學——**民主的極限是定理**。
- **孔多塞悖論的一般化**：循環是必然——**多數決的傳遞性崩塌**（無限域下）。
- **機制設計的反向**：與其找完美制度，不如**設計制度使均衡 = 社會最優**——Hurwicz–Maskin–Myerson（2007 諾貝爾）的機制設計。
- **Gibbard–Satterthwaite**：防操縱的不可能性——**每一種投票都可被操縱**。
- **Sen 的擴展**：自由悖論、福利經濟學——**諾貝爾 1998**。
- **Arrow 的帝國**：一般均衡（與 Debreu 合作）、資訊經濟、醫療經濟——**史上最年輕的諾貝爾得主**（51 歲）。
- **實務的影響**：排名算法（Google 的 PageRank 是「社會選擇」的變體）、拍賣設計、選舉改革。

## 關鍵人物與文獻
- **Kenneth Arrow**（1921–2017）：Social Choice and Individual Values (1951)——諾貝爾 1972（51 歲，最年輕）
- **Marquis de Condorcet**（1743–1794）：多數決循環 (1785)——法國大革命的殉難者（死於獄中）
- **Jean-Charles de Borda**（1733–1799）：Borda 計分 (1781)
- **Amartya Sen**（1933–）：自由悖論 (1970)——諾貝爾 1998
- **Gibbard & Satterthwaite**：操縱的不可能性 (1973/1975)
- 交叉參照：`1950-Nash均衡.md`、`1944-vonNeumannMorgenstern博弈論.md`、`../計算理論/1931-Godel不完備定理.md`、`../計算理論/1950-Rice定理.md`
