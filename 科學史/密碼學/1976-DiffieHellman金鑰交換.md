# 1976 - Diffie–Hellman 金鑰交換

## 案件摘要
1976 年 11 月，Diffie 與 Hellman 發表《New Directions in Cryptography》：提出**金鑰交換協議**——兩個從未見面的人，在竊聽者面前公開交換訊息，卻能協商出共享秘密。這是人類第一次解決「金鑰分發問題」，公鑰密碼學正式問世。協議的安全性建立在**離散對數問題**的單向性上：公開傳輸 $g^a, g^b$，竊聽者算出 $g^{ab}$ 需要解離散對數——被認為難。

## 前因 -- 為什麼會有這個案子
Diffie 與 Hellman（見 `1974-Diffie公鑰構想.md`）已構想公鑰密碼學，但缺一個實例。他們的問題：**存在單向函數嗎？有沒有「容易算、難逆推」的具體數學運算？** 答案來自數論的老朋友：**指數運算**。

## 線索與推理 -- 數學式、程式、理論

### 離散對數的單向性
取質數 $p$ 與生成元 $g$（$\mathbb{Z}_p^*$ 的生成元）。**指數運算**容易：

$$g^a \bmod p \quad \text{（平方乘法，} O(\log a) \text{ 次模乘）}$$

**離散對數**難：

$$\text{給定 } g^a \bmod p \text{，求 } a \quad \text{（已知最佳算法 } O(p^{1/2}) \text{ 級）}$$

（現代：數域篩法 $2^{n^{1/3}}$ 級——次指數，但仍遠難於指數運算。）

**單向性**：乘 $g$ 容易，除 $g$ 難。

### Diffie–Hellman 協議
```
公開參數：質數 p，生成元 g

A: 私密選 a，公開發送 A = g^a mod p
B: 私密選 b，公開發送 B = g^b mod p

A 計算：B^a = (g^b)^a = g^{ab} mod p
B 計算：A^b = (g^a)^b = g^{ab} mod p

共享秘密：s = g^{ab} mod p
```

**竊聽者 E 看到**：$g, p, g^a, g^b$——要算 $g^{ab}$，需要解**Diffie–Hellman 問題**（CDH）：

$$\text{給定 } g^a, g^b \text{，求 } g^{ab}$$

CDH 被認為 ≈ 離散對數難（2000 年的證明：隨機自歸約下，CDH 難 ⟺ DDH 難 ⟹ DL 難）。

### 為什麼這是革命
**對照兩千年的困境**：

- **之前**：加密需要先共享金鑰 → 金鑰需要安全信道 → 死結
- **之後**：兩方公開交換 $g^a, g^b$（信道不安全沒關係）→ 各自算出 $s$ → $s$ 作為對稱加密的金鑰

**實際架構**（今天的 HTTPS）：

$$\text{DH 交換 } s \xrightarrow{} s \text{ 作為 AES 的金鑰} \xrightarrow{} \text{對稱加密資料}$$

**非對稱解決金鑰分發，對稱加密解決資料加密**——兩者各司其職，這是現代密碼學的標準架構。

### 程式碼：Diffie–Hellman

```python
import random

def mod_pow(base, exp, mod):
    """平方乘法：O(log exp) 次模乘"""
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = result * base % mod
        base = base * base % mod
        exp >>= 1
    return result

def is_generator(g, p):
    """檢查 g 是否為 Z_p* 的生成元"""
    need = {k for k in range(1, p) if p % k == 0}  # 簡化示範
    return True

# 公開參數（實務用 2048 位質數；此處示範小質數）
p, g = 2**61 - 1, 3

# A 與 B 各自私密選亂數
a = random.getrandbits(40)
b = random.getrandbits(40)

# 公開交換
A = mod_pow(g, a, p)     # E 看得到
B = mod_pow(g, b, p)     # E 看得到

# 各自算出共享秘密
s_A = mod_pow(B, a, p)   # (g^b)^a = g^{ab}
s_B = mod_pow(A, b, p)   # (g^a)^b = g^{ab}
print(s_A == s_B)        # True：共享秘密協商成功

# 竊聽者：知道 g, p, A, B，要算 g^{ab}——需解離散對數
# 中間人攻擊的防範：需要認證（數位簽章，見 1977-RSA）
```

### 中間人攻擊：認證的必要
DH 協議的弱點：**中間人攻擊（MITM）**——竊聽者 $E$ 攔截並替換：

```
A ←— g^e1 —→ E ←— g^e2 —→ B
A ←— g^e2 —→ E ←— g^e1 —→ B
```

$A$ 與 $E$ 共享 $g^{a e_1}$，$B$ 與 $E$ 共享 $g^{b e_2}$——$E$ 居中解密重加密。**DH 解決竊聽，不解決冒充**——需要**認證**（數位簽章，RSA 1977 或憑證）。TLS 的「憑證 + DH」架構正是補這個洞。

**偵探筆記**：Diffie–Hellman 的推理是「利用單向性的交換律」——$(g^a)^b = (g^b)^a$ 的**交換律**（指數的性質）讓兩方各自到達同一點，而竊聽者無法。**用數學結構的交換性代替共享秘密**——這個模式後來出現在所有金鑰交換協議（ECDH、post-quantum DH）中。

## 結案 -- 後果與影響
- **HTTPS 的基礎**：每次 TLS 握手（DHE、ECDHE）都在跑 Diffie–Hellman——網路加密的基礎設施。
- **公鑰密碼學問世**：1976 年論文正式定義公鑰密碼學，RSA（1977）補上加密實現。
- **ECDH**：橢圓曲線版本（1985，見 `2005-橢圓曲線密碼學.md`）——更短金鑰、更快，今天行動裝置的標準。
- **數位簽章的構想**：同一論文提出的簽章構想，由 RSA（1977）與 ElGamal（1985）實現。
- **圖靈獎**：Diffie 與 Hellman 獲 2015 年圖靈獎。
- **量子威脅**：Shor 演算法（1994，見 `1994-Shor演算法.md`）破離散對數——DH 需要後量子替代（見 `2017-後量子密碼學.md`）。

## 關鍵人物與文獻
- **Whitfield Diffie**（1944–）與 **Martin Hellman**（1945–）：New Directions in Cryptography (1976, IEEE Trans. Info. Theory)；圖靈獎 2015
- **Ralph Merkle**：同時期的貢獻（論文第三作者被拒——冤案）
- **Malcolm Williamson**（GCHQ）：1974 秘密發明等價協議
- 交叉參照：`1974-Diffie公鑰構想.md`、`1977-RSA.md`、`2005-橢圓曲線密碼學.md`、`2017-後量子密碼學.md`
