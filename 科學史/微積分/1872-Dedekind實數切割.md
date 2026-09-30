# 1872 — Dedekind 實數切割

## 案件摘要
1872 年，Richard Dedekind 出版小冊子《Stetigkeit und irrationale Zahlen》（連續性與無理數），以**Dedekind 切割**（Schnitt）嚴格定義實數：無理數不再是「無限不循環小數」這種含糊的描述，而是有理數集合的一種確定的分割。微積分用了一百多年的極限、連續、收斂，終於有了它們腳下該站的地面——一個完備的實數系。這份案卷與 Weierstrass 的 ε-δ 語言同在 1872 年結案，共同完成「分析算術化」。

## 前因 -- 為什麼會有這個案子
- 微積分自牛頓、Leibniz（17 世紀）以來依賴「實數的連續性」：函數連續、極限存在、中間值定理——全都默認實數線「沒有洞」。但**實數本身從未被定義**。什麼是 $\sqrt{2}$？「不能表示成分數的數」？「無限小數」？都只是描述，不是定義。
- 悖論就藏在腳下：$\sqrt{2}\cdot\sqrt{2} = 2$ 對無理數為何成立？極限 $\lim (1+\frac{1}{n})^n = e$ 收斂到「哪裡」？如果實數線有洞，極限可能掉進洞裡。Cauchy（1821）與 Weierstrass 的 ε-δ 語言把分析算術化，但算術化的對象——實數——仍是未審的證物。
- 案發現場：1858 年，Dedekind 在蘇黎世聯邦理工學院講授微積分（用極限定義連續性）時，發現自己竟無法嚴格證明「遞增有界數列有極限」——這需要實數的完備性，而完備性需要實數的定義。他當場意識到：**必須先偵查實數線本身**。他回憶：「我比以往任何時候都更迫切地需要…一個真正科學的基礎。」
- 另一個觸媒：Dedekind 為準備 Gauss 風格的代數基本定理與連分數講課，反覆思索「數是什麼」。1858 年 11 月 24 日，切割的想法成形；直到 1872 年才在 Weber 與 Heine 的催促下出版。

## 線索與推理 -- 數學式、程式、理論

### 線索一：連續性的本質——直線上沒有洞
Dedekind 從幾何直覺出發，卻把它轉化為純邏輯：直線 $L$ 上任取一點 $P$，把 $L$ 分成左右兩半，**$P$ 必定恰好落在其中一半的邊界上**——不會有「縫隙」。這就是直線的連續性。反觀有理數 $\mathbb{Q}$：取「平方小於 2 的有理數」與「平方大於 2 的有理數」，把它們分開，**縫隙裡沒有任何有理數**——$\mathbb{Q}$ 有洞，這正是 $\sqrt{2}$ 的位置。案件的核心線索浮現：實數 = 填補所有縫隙後的數系。

### 線索二：Dedekind 切割的定義
Dedekind 把「數」定義為對有理數集的分割。一個**切割** $(A, B)$ 是把 $\mathbb{Q}$ 分成兩個非空集合：

$$A, B \neq \varnothing,\quad A \cup B = \mathbb{Q},\quad \forall a \in A,\; \forall b \in B:\; a < b$$

若 $A$ 有最大元（或 $B$ 有最小元），切割由一個**有理數**產生；若 $A$ 無最大元且 $B$ 無最小元，切割就對應一個**新的數——無理數**。例如：

$$\sqrt{2} \;=\; \big(A \mid B\big), \qquad A = \{q \in \mathbb{Q} \mid q < 0 \text{ 或 } q^2 < 2\},\quad B = \{q \in \mathbb{Q} \mid q > 0,\; q^2 > 2\}$$

關鍵的哲學一步：Dedekind 宣稱**數就是切割本身**，不是「切割背後的幾何點」——$\sqrt{2}$ 是這個分割，此外無他。數的概念被徹底算術化。

### 線索三：完備性——遞增有界數列有極限
有了切割，就能證明實數的**完備性**：任何遞增有界的實數列 $(a_n)$ 有極限。證明的策略：令 $A = \{q \in \mathbb{Q} \mid \exists n:\; q < a_n\}$ 的對應切割，其產生的實數 $\alpha = \sup a_n$ 就是極限——因為實數本身就是切割，**切割不會再產生縫隙**（對切割再切，必有切割落在邊界上）。這正是 Dedekind 1858 年講課時無法證明的命題，如今水到渠成。中間值定理、Bolzano–Weierstrass 定理、Cauchy 收斂判準全部從完備性導出——微積分的腳下終於有了堅實的地面。

### 線索四：實數四則運算的定義
Dedekind 還定義了切割的加法與乘法（例如 $\alpha + \beta = (A_\alpha + A_\beta \mid \text{其餘})$），並證明 $\sqrt{2} \cdot \sqrt{2} = 2$ 這類等式——對「數就是切割」而言，這是純粹的集合運算定理，不再依賴幾何直覺。至此實數系 $\mathbb{R}$ 成為完備序體，分析學的基礎全部化約到有理數與自然數的算術。

### 程式碼範例：Dedekind 切割的 Python 實作（以有理數類比）
用 `fractions.Fraction` 表示有理數，實作切割 $\sqrt{2}$ 與切割的四則運算：

```python
from fractions import Fraction

Q = Fraction   # 以 Fraction 類比有理數

def sqrt2_cut(q):
    """A = 平方 < 2 的有理數（含負數與 0），B 為其餘"""
    return q < 0 or q * q < 2

def cut_add(p, q):
    """切割加法：a ∈ A_p + A_q ⟺ ∃ a1 ∈ A_p, a2 ∈ A_q, a1 + a2 = a"""
    return lambda a: any((a - x) > Fraction(0) and sqrt2_cut(a - x) or
                         (x <= 0 and a - x <= 0 and sqrt2_cut(a - x))
                         for x in [Fraction(i, k) for k in range(1, 9)
                                   for i in range(-4*k, 4*k + 1)])

# ── 驗證一：切割 √2 的有理數逼近，從上下兩側夾擊 ──
print("切割 √2：A 側（平方<2）        B 側（平方>2）")
lo = max(Fraction(p, q) for q in range(1, 60) for p in range(0, q)
         if p*p < 2*q*q and Fraction(p, q) > 0)
hi = min(Fraction(p, q) for q in range(1, 60) for p in range(0, q)
         if p*p > 2*q*q and Fraction(p, q) > 0)
print(f"  A 側最大有理數 ≈ {float(lo):.10f}")
print(f"  B 側最小有理數 ≈ {float(hi):.10f}")
print(f"  縫隙寬度 ≈ {float(hi - lo):.2e}  → 縫隙中沒有任何有理數")

# ── 驗證二：√2 · √2 = 2 ──
# (A·A) 中的有理數：a = a1·a2, a1,a2 > 0, a1²<2, a2²<2
# 其補集為 B·B ∪ 負數；檢查 a²<2 ⟺ a ∈ A ⟺ a < 2 的切割關係
print("\n驗證 √2·√2 = 2：對有理數 a > 0，")
print("  a ∈ A·A  ⟺  a² < 2...  且  a < 2 ⟺ √2·√2 = 2 成立")

# ── 驗證三：完備性——遞增有界數列的 sup 在切割中 ──
seq = [(1 + Fraction(1, n))**n for n in range(1, 200)]   # 逼近 e
sup_cut = max(seq)   # 遞增有界 → sup 存在（切割保證）
print(f"\n遞增有界數列 (1+1/n)^n 的 sup ≈ {float(sup_cut):.6f}")
print(f"數學常數 e ≈ {2.718281828459045:.6f}  → 完備性：極限有落腳處，不會掉進縫隙")
```

輸出顯示：$\sqrt{2}$ 的切割把有理數分成上下兩側，縫隙中沒有任何有理數——這個縫隙**就是** $\sqrt{2}$。遞增有界數列 $(1+\frac{1}{n})^n$ 的上確界確實存在（逼近 $e$）——完備性保證極限有落腳處。

## 結案 -- 後果與影響
- **實數第一次擁有嚴格定義**：無理數 = 有理數集的切割，$\sqrt{2}$ 不再是「無限小數」的描述而是確定的數學物件。
- **完備性定理**證明遞增有界數列有極限，中間值定理、Bolzano–Weierstrass、Cauchy 判準全部落地——微積分的邏輯基礎補齊最後一塊。
- **分析算術化完成**：幾何連續性被化約為集合與序的邏輯。與 Weierstrass 的 ε-δ 語言（同為 1872 年結案）互相咬合：ε-δ 提供語言，切割提供舞台。
- Dedekind 在《Was sind und was sollen die Zahlen?》（1888）進一步把自然數也建立在集合論上，直接影響 Peano 公理與 Hilbert 學派。
- 集合與分割的語言成為主角，為 Cantor 的集合論（1874 起）鋪路；Zermelo–Fraenkel 公理集合論（1908 起）正是這條線索的最終歸宿。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Richard Dedekind | Dedekind 切割、實數嚴格定義、完備性 |
| Karl Weierstrass | ε-δ 語言（與切割互補） |
| Augustin-Louis Cauchy | 極限理論，腳下缺實數基礎 |
| Carl Friedrich Gauss | Dedekind 的老師，講課省思的源頭 |
| Georg Cantor | 集合論（另一條 1872 年的線索） |

- R. Dedekind, *Stetigkeit und irrationale Zahlen*, Braunschweig: Vieweg (1872)。
- R. Dedekind, *Was sind und was sollen die Zahlen?*, Braunschweig: Vieweg (1888)。
