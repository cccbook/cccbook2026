# 1979 - Merkle–Hellman 背包密碼

## 案件摘要
1978–79 年，Ralph Merkle 與 Martin Hellman 發表**背包密碼**（knapsack cryptosystem）：用 NP 完備的子集和問題當單向陷門函數——公鑰是「難」的背包，私鑰是陷門（超遞增背包）。這是第一個用 **NP 完備問題**設計的公鑰密碼，理論上漂亮；但 1982 年被 Shamir 用**格基數論**（LLL 演算法的前身）破解——**NP 難 ≠ 密碼安全**。這個「失敗」的教訓塑造了整個密碼學：平均難度與最壞難度的鴻溝。

## 前因 -- 為什麼會有這個案子
RSA（1977，見 `1977-RSA.md`）的分解問題「被認為難」但沒有理論證明。Merkle 的野心：**用 NP 完備問題設計密碼**——最壞情況指數難，安全性有理論保證。子集和問題（subset sum / knapsack）：

$$\text{給定 } a_1, \dots, a_n \text{ 與 } s \text{，是否存在子集 } \sum_{i \in I} a_i = s$$

**NP 完備**（Karp 1971 的 21 問題之一，見 `../計算理論/1971-Karp21問題.md`）——最壞情況指數難。

## 線索與推理 -- 數學式、程式、理論

### 超遞增背包的陷門
**超遞增序列**（superincreasing）：每項大於之前所有項之和：

$$a_i > \sum_{j<i} a_j$$

範例：$(1, 3, 7, 14, 30, 57)$（$3 > 1$、$7 > 4$、$14 > 11$……）。

**超遞增背包容易解**（貪心）：從最大項往回，$s \ge a_i$ 則選 $a_i$——$O(n)$ 時間唯一解：

$$s = 43: \; 43 \ge 57? \text{否} \; \to 43 \ge 30? \text{是，選} \to 13 \ge 14? \text{否} \to 13 \ge 7? \text{是，選} \to 6 \ge 3? \text{是，選} \to 3 \ge 1? \text{是，選} \to \{1, 3, 7, 30\}$$

### Merkle–Hellman 的陷門化
**金鑰生成**：

1. 私鑰：超遞增序列 $(a_i)$、模數 $M > \sum a_i$、乘數 $w$（$\gcd(w, M) = 1$）
2. 公鑰：「一般」背包 $b_i = w \cdot a_i \bmod M$

**加密**：明文位元 $x_i$，密文 $s = \sum b_i x_i$

**解密**（知道陷門 $w, M$）：

$$s' = w^{-1} \cdot s \bmod M = \sum w^{-1} b_i x_i = \sum a_i x_i \pmod M$$

——化為**超遞增背包**，貪心 $O(n)$ 解。$\blacksquare$

**推理**：公鑰 $(b_i)$ 看起來是一般背包（NP 難），實際是「偽裝的超遞增」——陷門是 $w^{-1}$。

### Shamir 的破解 (1982)
**破綻**：公鑰 $(b_i = w a_i \bmod M)$ 的**有理數近似結構**。Shamir 發現：

$$\frac{w}{M} \approx \text{某個用 } b_i \text{ 可逼近的有理數}$$

**連分數攻擊**：由 $b_i$ 逼近 $\frac{w}{M}$（利用 $a_i$ 超遞增的結構）——**多項式時間**破解。Adi Shamir 在 1982 年發表，Merkle–Hellman 背包密碼死亡。

**更深的武器：LLL 演算法**（1982，見 `../隨機算法/`）——Lenstra–Lenstra–Lovász 的格基約化：把背包問題化為**最短向量問題（SVP）**，LLL 在低維近似求解——**幾乎所有背包密碼變體都被 LLL 破解**。

### NP 難 ≠ 密碼安全
**教訓**（Merkle–Hellman 的失敗）：

- **NP 完備是「最壞情況」難度**：最壞實例指數難，但**隨機實例可能容易**（平均難度，見 Impagliazzo 的五個世界，見 `../隨機算法/1997-ImpagliazzoWigderson去隨機化.md`）
- **密碼需要「平均難度」**：攻擊者面對的是「隨機金鑰」生成的實例——不是最壞實例
- **構造的密碼實例特別「好解」**：Merkle–Hellman 的公鑰有超遞增結構的殘留——**陷門化洩漏結構**

$$\text{密碼安全的條件：} \text{「隨機金鑰生成的實例」在平均意義上難} \ne \text{NP 完備}$$

**偵探筆記**：這是密碼學史最重要的失敗之一——它證明「**理論難 ≠ 實際安全**」，並催生了兩個傳統：1) 證明式安全（provable security，從「假設 X 難」出發的規約證明）；2) 平均複雜度理論（見 `../隨機算法/1997-ImpagliazzoWigderson去隨機化.md` 的五個世界）。

### 程式碼：背包密碼與破解

```python
def knapsack_greedy(a, s):
    """超遞增背包：貪心 O(n)"""
    sel = []
    for ai in sorted(a, reverse=True):
        if s >= ai:
            sel.append(ai); s -= ai
    return sorted(sel) if s == 0 else None

def merkle_hellman_keygen():
    """私鑰：超遞增序列；公鑰：偽裝的一般背包"""
    import random
    a, total = [], 0
    for _ in range(8):
        ai = random.randint(total + 1, 2 * total + 3)   # 超遞增！
        a.append(ai); total += ai
    M = random.randint(total + 1, 2 * total)             # 模數
    w = random.randint(2, M - 1)
    import math
    while math.gcd(w, M) != 1:
        w = random.randint(2, M - 1)
    b = [w * ai % M for ai in a]                         # 公鑰
    return (b,), (a, w, M, pow(w, -1, M))

random.seed(42)
(pb,), (a, w, M, winv) = merkle_hellman_keygen()

# 加密：明文位元 x
x = [1, 0, 1, 1, 0, 0, 1, 0]
s = sum(bi * xi for bi, xi in zip(pb, x))
print(f"密文 s = {s}")

# 解密（陷門）：化為超遞增背包
s2 = s * winv % M
print(f"解密 = {knapsack_greedy(a, s2)}")   # [1, 3, 7, 30...] 對應 x ✓

# Shamir 的破解：從 b_i 逼近 w/M（連分數）——多項式時間
print("公鑰 b 有超遞增的殘留結構 → LLL/連分數破解")
```

## 結案 -- 後果與影響
- **NP 難 ≠ 安全的教訓**：密碼學界對「用 NP 完備問題」的警惕——至今後量子密碼（見 `2017-後量子密碼學.md`）用的格問題也是 NP 難，但需要**平均難度**的證據（LWE 有規約）。
- **LLL 演算法**：1982 年的格基約化——破解背包的武器，後來成為格密碼（NTRU、LWE）的基礎工具（諷刺：破解武器成為下一代密碼的工具）。
- **證明式安全**：1982 年後「從難解假設出發的規約證明」成為密碼學的標準方法論（Goldwasser–Micali 1984 的語義安全）。
- **平均複雜度理論**：Merkle 的失敗啟發 Impagliazzo 的五個世界（見 `../隨機算法/1997-ImpagliazzoWigderson去隨機化.md`）。
- **Merkle 的其他貢獻**：Merkle–Hellman 的失敗不妨礙 Merkle 的偉大——Merkle 樹（1988，區塊鏈的基礎，見 `2016-區塊鏈密碼學.md`）、Merkle 謎題（公鑰密碼的先聲）。

## 關鍵人物與文獻
- **Ralph Merkle**（1952–）：Merkle–Hellman 背包 (1978)、Merkle 樹 (1988)、圖靈獎級的貢獻（迄今未得，密碼學史的爭議）
- **Martin Hellman**（1945–）：圖靈獎 2015（DH）
- **Adi Shamir**（1952–）：連分數破解 (1982)；圖靈獎 2002
- **Lenstra, Lenstra, Lovász**：LLL 演算法 (1982)
- 交叉參照：`1977-RSA.md`、`1985-ElGamal.md`、`2017-後量子密碼學.md`、`../計算理論/1971-Karp21問題.md`
