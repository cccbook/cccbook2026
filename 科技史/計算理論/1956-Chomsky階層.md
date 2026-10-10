# 1956-Chomsky 階層

## 案件摘要
1956 年，Noam Chomsky 發表《Syntactic Structures》並在同年論文《Three models for the description of language》中提出文法階層：將所有形式文法按「產生規則的自由度」分成四層，每一層恰好對應一種自動機。語言的複雜度，從此有了精確的階梯。

## 前因 -- 為什麼會有這個案子
- 1950 年代，通訊工程需要描述語言（Shannon 的資訊論、有限狀態機用於編碼）。
- 結構語言學（Bloomfield 學派）對自然語言只有鬆散的描述工具，無法處理巢狀結構（如 "the man who ... left"）。
- Chomsky 的偵探手法：不問「語言是什麼」，而問「**描述語言的文法有幾種能力等級**」——用數學對文法分類，再找出每類對應的機器。這是「文法 ↔ 自動機」對應（Chomsky–Schützenberger）的開端。

## 線索與推理 -- 數學式、程式、理論

### 四類文法與對應自動機
形式文法 $G = (V, \Sigma, P, S)$：非終結符 $V$、終結符 $\Sigma$、產生規則 $P$、起始符 $S$。依規則形式限制分四層：

| 層級 | 文法名稱 | 規則形式限制 | 對應自動機 | 識別的語言 |
|---|---|---|---|---|
| **Type-3** | 正則文法 | $A \to aB$ 或 $A \to a$（右線性） | 有限狀態機 FSM | 正則語言 |
| **Type-2** | 上下文無關文法 CFG | $A \to \alpha$（左邊必為單一非終結符） | 下推自動機 PDA | CFL |
| **Type-1** | 上下文有關文法 CSG | $\alpha A \beta \to \alpha \gamma \beta$（$|\gamma| \geq |A|$，不縮短） | 線性有界自動機 LBA | CSL |
| **Type-0** | 無限制文法 | $\alpha \to \beta$（任意） | 圖靈機 TM | 遞迴可枚舉語言 |

### 產生規則形式範例
```text
Type-3:  S -> aS | bA          （正則：右邊至多一個非終結符在末端）
         A -> bA | b

Type-2:  S -> aSb | ε           （CFG：a^n b^n，需配對計數）
         S -> SS | (S) | ε      （括號配對文法）

Type-1:  S -> aSBC | aBC        （CSG：a^n b^n c^n）
         CB -> BC
         aB -> ab, bB -> bb, bC -> bc, cC -> cc

Type-0:  任意重寫規則，可模擬圖靈機的計算過程
```

### 包含關係
四層語言族形成嚴格的包含鏈：

$$\text{Type-3} \subsetneq \text{Type-2} \subsetneq \text{Type-1} \subsetneq \text{Type-0}$$

經典見證：
- $a^n b^n \in$ Type-2 但 $\notin$ Type-3（有限狀態機無法無限計數——泵引理可證）。
- $a^n b^n c^n \in$ Type-1 但 $\notin$ Type-2（PDA 只有一個堆疊，無法同時比對三段——CFL 泵引理可證）。
- 存在 Type-0 但 $\notin$ Type-1 的語言（如某些不可判定的編碼）——LBA 的接受問題可判定，但圖靈機的不行。

### 自動機對應的計算本質
每一層的計算能力由「記憶體結構」決定：
- FSM：無輔助記憶（只有有限狀態）。
- PDA：一個堆疊（LIFO），只能後進先出。
- LBA：長度受限的 tape（輸入長度的線性函數）。
- TM：無限 tape，完全自由。

### Python 實作：下推自動機檢查括號配對
括號配對語言 $\{ w : \text{括號平衡} \}$ 是典型 CFL，用 PDA（以 list 模擬堆疊）識別：

```python
def pda_paren(s: str) -> bool:
    """下推自動機：狀態 q，堆疊 Z，規則：
    q, '(' -> push；q, ')' -> pop；輸入盡且堆疊空 -> 接受"""
    stack = ['Z']          # 底部標記
    for ch in s:
        if ch == '(':
            stack.append('(')          # 轉移: (, Z -> (, (Z
        elif ch == ')':
            if stack[-1] == 'Z':
                return False           # 多餘的右括號：無法 pop
            stack.pop()                # 轉移: ), ( -> ε, Z
        else:
            return False               # 非法字元
    return stack == ['Z']              # 接受條件：堆疊回到底部

# 測試
assert pda_paren("(()())") is True
assert pda_paren("(()")   is False
assert pda_paren("())(")  is False
assert pda_paren("")      is True
print("PDA 括號配對：全部通過")

# 對照：FSM 無法識別此語言（需無限狀態記錄巢狀深度）
# 這正是 Type-3 ⊊ Type-2 的實例證明
```

## 結案 -- 後果與影響
- **結案**：文法分層成功，且每層都找到對應的自動機——「文法 ↔ 機器」的對偶成為計算理論的核心範式。
- Chomsky–Schützenberger 定理（1963）：CFL 恰為「正則語言與 Dyck 語言的交集之同態像」，將 CFL 帶入代數視角。
- 編譯器理論直接受惠：詞法分析用正則文法（Type-3）、語法分析用 CFG（Type-2，如 LALR、LL 解析器）、語義分析需要更多（屬性文法）。
- 自然語言研究革命：《Syntactic Structures》引發語言學的認知科學轉向，Chomsky 階層成為衡量自然語言「在哪一層」的標準問題（自然語言微妙地超越 Type-2 的證據至今仍有爭論）。
- 深遠影響：階層概念滲透到複雜度理論（時間/空間階層定理）、描述複雜度，成為「分層看計算能力」的普適方法論。

## 關鍵人物與文獻
- **Noam Chomsky**（1928–）：MIT 語言學家，《Syntactic Structures》, Mouton, 1957；《Three models for the description of language》, *IRE Trans. IT*, 1956。
- **Morris Halle**：與 Chomsky 合作音韻理論，鞏固生成文法學派。
- **Joseph Schützenberger**：Chomsky–Schützenberger 定理，CFL 的代數刻劃。
- **Stephen Kleene / Michael Rabin & Dana Scott**：正則語言與 FSM 的等價性（1956），Type-3 層的機器對應。
- **Donald Knuth**：1965 年 LR(k) 文法，將 CFG 理論推向編譯器實務。
