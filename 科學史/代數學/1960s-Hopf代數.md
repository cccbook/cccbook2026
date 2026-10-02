# 1960s-Hopf 代數

## 案件摘要
Hopf 代數是「既是代數、又能反過來分解自己」的對象：它帶有餘積 $\Delta$ 與餘單位 $\epsilon$，把乘法公理「鏡像」成餘乘法公理。從 Heinz Hopf 1941 年的拓撲源頭，到 Sweedler 1969 年的系統化专著，再到 1986 年 Drinfeld 的量子群 —— 這是一條從拓撲流形通到量子物理的偵探長線。

## 前因 -- 為什麼會有這個案子
- **Hopf（1941）** 研究拓撲群（李群）的上同調環 $H^\ast(G)$ 時發現：這種環有一種奇怪的「自我分解」結構 —— 上同調類可以「餘乘」。他用這結構證明了對稱空間上同調的定理。
- **代數拓撲的線索**：對每個空間 $X$ 有對角映射 $\mathrm{diag}: X \to X \times X$，取上同調後反向變成 $H^\ast(X \times X) \to H^\ast(X)$，即「餘積」的幾何來源。
- **群表示論的線索**：兩個表示的張量積 $V \otimes W$ 仍是表示 —— 這個「張量積」在群代數上正好對應一個餘積 $\Delta$。數學家隱約感覺：「表示論的秘密藏在代數的鏡像結構裡。」
- Sweedler 的偵探問題：**「把『代數』的公理全部箭頭反轉，會得到什麼？兩者合起來又是什麼？」**

## 線索與推理 -- 數學式、程式、理論

### 線索一：餘積與餘單位 —— 代數的「鏡像公理」
域 $k$ 上的**餘代數** $(C, \Delta, \epsilon)$：$\Delta: C \to C \otimes C$（餘積，餘結合），$\epsilon: C \to k$（餘單位）：

$$(\Delta \otimes \mathrm{id}) \circ \Delta = (\mathrm{id} \otimes \Delta) \circ \Delta, \qquad (\epsilon \otimes \mathrm{id}) \circ \Delta = \mathrm{id} = (\mathrm{id} \otimes \epsilon) \circ \Delta$$

**雙代數（bialgebra）**：同時是代數 $(A, m, u)$ 與餘代數 $(A, \Delta, \epsilon)$，且 $\Delta, \epsilon$ 是代數同態：

$$\Delta(xy) = \Delta(x)\Delta(y), \qquad \Delta(1) = 1 \otimes 1$$

### 線索二：Hopf 代數公理 —— 加上「鏡像中的逆」
**Hopf 代數**是雙代數再加上** antipode** $S: A \to A$（餘乘法世界裡的「取逆」）：

$$m \circ (S \otimes \mathrm{id}) \circ \Delta = u \circ \epsilon = m \circ (\mathrm{id} \otimes S) \circ \Delta$$

用 Sweedler 記法（線索三），雙代數的餘結合律寫成：

$$\sum_{(x)} \Delta(x)_{(1)} \otimes \Delta(x)_{(2)} \otimes \Delta(x)_{(3)} = \sum_{(x)} x_{(1)} \otimes x_{(2)} \otimes x_{(3)}$$

而 antipode 公理是：

$$\sum_{(x)} S(x_{(1)})\, x_{(2)} = \epsilon(x) \cdot 1 = \sum_{(x)} x_{(1)}\, S(x_{(2)})$$

（就像 $g^{-1} g = e$ 的鏡像。）

### 線索三：Sweedler 記法 —— 讓「餘積」變得可讀
Sweedler（1969）發明的省略記法：

$$\Delta(x) = \sum_{(x)} x_{(1)} \otimes x_{(2)}$$

不用真的寫出 $\Delta(x)$ 的所有項，只標記「第 1 個位置」$x_{(1)}$ 與「第 2 個位置」$x_{(2)}$。這個記法讓 Hopf 代數的計算從災難變成日常工作 —— 就像 Leibniz 記法之於微積分。

### 線索四：群代數 $\mathbb{C}[G]$ 是 Hopf 代數 —— 最重要的例子
對群 $G$，群代數 $\mathbb{C}[G]$（基 $\{g : g \in G\}$，乘法 $g \cdot h = gh$）帶有自然的 Hopf 結構：

$$\Delta(g) = g \otimes g, \qquad \epsilon(g) = 1, \qquad S(g) = g^{-1}$$

**為什麼 $\Delta$ 恰好是「張量積表示」？** 若 $V, W$ 是 $G$ 的表示，$G$ 透過 $\Delta$ 作用在 $V \otimes W$ 上：

$$g \cdot (v \otimes w) = \Delta(g)(v \otimes w) = (g v) \otimes (g w)$$

**表示論的張量積 = Hopf 代數的餘積** —— 這就是偵探的答案：表示範疇的「單子結構」由 $\Delta$ 編碼。

### 程式碼：Python 實作群代數的 Hopf 結構
以 $S_3$（或小群 $C_3$）為例：

```python
from itertools import product

# 以置換群 S3 為例（用 tuple 表示置換）
def compose(p, q):          # 置換合成：先 q 後 p
    return tuple(p[q[i]] for i in range(len(q)))

def inv(p):
    r = [0] * len(p)
    for i, pi in enumerate(p):
        r[pi] = i
    return tuple(r)

S3 = [ (0,1,2), (1,0,2), (2,1,0), (0,2,1), (1,2,0), (2,0,1) ]
e = S3[0]

def coproduct(g):
    """Δ(g) = g ⊗ g —— 群代數的餘積（群像元是『群like』的）"""
    return [(g, g)]        # 只有單一項：Δ(g) = g⊗g

def antipode(g):
    """S(g) = g^{-1}"""
    return inv(g)

def counit(g):
    """ε(g) = 1"""
    return 1

# 驗證 Hopf 公理：Σ S(x_(1)) x_(2) = ε(x)·1
for g in S3:
    lhs = sum(compose(antipode(a), b) for a, b in coproduct(g))  # S(g)·g = e
    assert lhs == e and counit(g) == 1, f"Hopf 公理失敗於 {g}"
print("S3 群代數的 Hopf 公理全部通過：S(g)g = e = gS(g)")

# 順帶驗證 Δ 是代數同態：Δ(gh) = Δ(g)Δ(h) = (g⊗g)(h⊗h) = gh ⊗ gh
g, h = S3[1], S3[2]
assert coproduct(compose(g, h)) == [(compose(g, h), compose(g, h))]
assert [(compose(g, h), compose(g, h))] == [(a[0], b[1]) for a, b in zip(coproduct(g), coproduct(h))]
print("Δ(gh) = Δ(g)Δ(h) 驗證通過：張量積表示的秘密被 Δ 編碼")
```

## 結案 -- 後果與影響
- **表示論的統一語言**：有限群、李群、李代數的表示論全部可以用 Hopf 代數語言重寫 —— 「表示範疇 = Hopf 代數的餘模範疇」。
- **量子群（1986）**：Drinfeld 與 Jimbo 提出 **quantum group** $U_q(\mathfrak{g})$ —— Hopf 代數的「變形」，因 Drinfeld 獲 1990 菲爾茲獎。量子群成為可積系統、結點理論（knot invariants，如 Jones 多項式）、共形場論的核心工具。
- **拓撲的回響**：Hopf 代數反哺拓撲 —— Steenrod 代數（模 p 上同調運算）是 Hopf 代數；譜同倫、Borel 定理皆賴此。
- **物理與密碼學的延伸**：量子逆散射方法、Yangian（另一類 Hopf 代數）、任意子（anyon）與拓撲量子計算，全部站在 Hopf 代數之上。
- ** monoidal 範疇的橋樑**：Tannaka–Krein 對偶說「 monoidal 範疇 + fiber functor = Hopf 代數」—— 反過來用表示重建代數，這是 1960s 之後範疇論的偵探續集。

## 關鍵人物與文獻
- **Heinz Hopf（1894–1971）**：瑞士數學家，蘇黎世聯邦理工（ETH）教授。1941 年論文 *Über die Topologie der Gruppen-Mannigfaltigkeiten und ihre Verallgemeinerungen* 開啟了這條線。
- **Moss Sweedler（1942–2021）**：美國數學家，康乃爾大學教授。1969 年专著 *Hopf Algebras*（Benjamin, 1969）系統化整個理論，並發明 Sweedler 記法。
- **Vladimir Drinfeld（1954–）**：1990 菲爾茲獎得主，1986 年 Berkeley ICM 講演提出量子群。
- 相關文獻：S. Montgomery, *Hopf Algebras and Their Actions on Rings* (CBMS 82, 1993)；C. Kassel, *Quantum Groups* (GTM 155, 1995)。
