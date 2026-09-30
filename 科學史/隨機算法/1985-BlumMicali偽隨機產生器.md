# 1985 - Blum–Micali 偽隨機產生器

## 案件摘要
1985 年，Manuel Blum 與 Silvio Micali 發表《How to Generate Cryptographically Strong Sequences of Pseudorandom Bits》：如果**單向函數**存在，就能用少量真隨機種子（$O(\log n)$ 位元）產生**任何多項式時間演算法都無法區別**的偽隨機序列。這是計算隨機性理論的奠基之作：第一次給「偽隨機」一個嚴格定義，並證明偽隨機性與密碼學（單向函數）等價。

## 前因 -- 為什麼會有這個案子
隨機算法（Miller–Rabin 等）需要真隨機位元，但電腦只有**偽隨機數產生器**（PRNG）——線性同餘法等「看起來隨機」。問題：**演算法的機率分析還成立嗎？** 若敵人（或問題實例）能利用 PRNG 的規律，錯誤率分析就崩潰。Blum–Micali 的問題：**能否證明某種 PRNG 「足夠隨機」**——隨機到任何多項式時間演算法都分不出真假？

## 線索與推理 -- 數學式、程式、理論

### 單向函數
**定義**：函數 $f$ 是單向的，若 $f$ 多項式時間可計算，但對任意多項式時間演算法 $A$：

$$P(A(f(x)) = x' \text{ 使 } f(x') = f(x)) \le \frac{1}{\text{poly}(n)}$$

**容易算，難逆推**。範例：離散對數——$f(x) = g^x \bmod p$（$p$ 質數），算 $f$ 快，逆推 $x$ 被認為難。

### Blum–Micali 產生器
從種子 $s_0 \in \mathbb{Z}_p^*$ 出發，迭代：

$$s_{i+1} = g^{s_i} \bmod p$$

每步輸出一位元：

$$b_i = \begin{cases} 1 & \text{若 } s_i < p/2 \\ 0 & \text{否則} \end{cases}$$

**定理**：若離散對數難，則序列 $b_1 b_2 \dots b_m$ 通過一切多項式時間統計檢驗——**任何多項式時間演算法無法區別它與真隨機序列**，優勢可忽略。

### 證明骨架：預測器 → 離散對數求解器
反證法：假設多項式時間預測器 $A$ 能以優勢 $\epsilon$ 預測 $b_{i+1}$。構造離散對數求解器：把 $A$ 當子程序，**反覆詢問「下一個位元」**，逐步重建 $s_i$ 的最高位元——由 $b_i$ 判定 $s_i \in [0, p/2)$ 或 $[p/2, p)$，二分搜尋 $\log p$ 步重建 $s_0$。這違反單向性。$\blacksquare$

**偵探筆記**：這個「預測器 → 反轉演算法」的歸約成為密碼學證明的標準模式：**任何能看出規律的演算法，都能被反轉成破解單向函數的演算法**。Yao (1982) 把它一般化為「下一個位元測試」（next-bit test）：通過一切統計檢驗 ⟺ 下一個位元不可預測。

### Yao 的一般化 (1982)
Yao 證明：單向函數存在 ⟺ 強偽隨機產生器（ stretch $n \to n+1$ 以上）存在。並給出：

$$\text{PRG 存在} \iff \text{單向函數存在}$$

Håstad–Impagliazzo–Levin–Lerman（HILL, 1999）完成最後一步：一般單向函數（不需置換）足以構造 PRG。**偽隨機性 = 密碼學**，兩者等價。

### 程式碼：Blum–Micali 骨架

```python
def blum_micali(seed, p, g, n_bits):
    """s_{i+1} = g^{s_i} mod p；輸出最高位元方向"""
    s, bits = seed, []
    for _ in range(n_bits):
        s = pow(g, s, p)
        bits.append(1 if s < p // 2 else 0)
    return bits

p = 2**61 - 1          # Mersenne 質數
g = 3
bits = blum_micali(12345, p, g, 10000)
ones = sum(bits) / len(bits)
print(f"1 的比例 = {ones:.3f}")   # ≈ 0.5：統計上像真隨機

# 安全性依賴：離散對數難（若有人能預測下一個位元，就能解離散對數）
```

### 為什麼重要：去隨機化的種子
Blum–Micali 的深遠意義：**隨機算法只需 $O(\log n)$ 位真隨機種子**——若 PRG 能拉伸到多項式長度，隨機算法（BPP）就能被確定性模擬（窮舉所有種子）：

$$\text{BPP} \subseteq \bigcup_c \text{DTIME}(2^{c\log n}) = \text{P} \quad \text{（若 PRG 夠強）}$$

這條線在 Impagliazzo–Wigderson (1997) 達到頂點（見 `1997-ImpagliazzoWigderson去隨機化.md`）。

## 結案 -- 後果與影響
- **現代密碼學的基礎**：串流加密（RC4 前身、ChaCha20）、金鑰產生、Nonce 生成——一切密碼學隨機性都建立在「單向函數 → PRG」上。
- **計算隨機性理論**：BPP 與 PRG 的關係、去隨機化綱領、HILL 定理。
- **Yao 的下一個位元測試**：密碼學證明的標準工具。
- **實務警示**：2012 年 Debian OpenSSL 弱隨機事件、區塊鏈私鑰重用攻擊——偽隨機性不足的災難。

## 關鍵人物與文獻
- **Manuel Blum**（1938–）：圖靈獎 1995（計算複雜度）
- **Silvio Micali**（1954–）：圖靈獎 2012（密碼學）
- Blum & Micali: How to Generate Cryptographically Strong Sequences... (1985, SIAM J. Comput.)
- **Andrew Yao**：Theory and Applications of Trapdoor Functions (1982)
- **Håstad, Impagliazzo, Levin, Luby**：HILL 定理 (1999)
- 交叉參照：`1985-Yao計算隨機性.md`、`1997-ImpagliazzoWigderson去隨機化.md`、`../計算理論/README.md`
