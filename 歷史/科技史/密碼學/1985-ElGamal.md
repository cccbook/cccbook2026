# 1985 - ElGamal

## 案件摘要
1985 年，Taher ElGamal 發表《A Public Key Cryptosystem and a Signature Scheme Based on Discrete Logarithms》：用**離散對數的單向性**實現公鑰加密與數位簽章——Diffie–Hellman（1976，見 `1976-DiffieHellman金鑰交換.md`）的直接延伸。ElGamal 加密的**隨機化**（每次加密用新隨機數）使它天然語義安全，而 ElGamal 簽章演變成 **DSA**（1991，美國國家數位簽章標準）。離散對數密碼學（DH、ElGamal、DSA、ECDH）成為與 RSA 並列的兩大體系。

## 前因 -- 為什麼會有這個案子
1976 年 Diffie–Hellman 只解決了金鑰**交換**（雙方都線上），還缺：
1. **單向加密**：任何人（不需線上）用公鑰加密
2. **數位簽章**：RSA（1977）已有，但基於分解；離散對數側缺

ElGamal 的問題：**離散對數能否承擔加密與簽章？** 答案：能，而且**隨機化**是關鍵。

## 線索與推理 -- 數學式、程式、理論

### ElGamal 加密
**金鑰生成**：

1. 公開參數：質數 $p$、生成元 $g$
2. 私鑰：隨機 $x$；公鑰：$y = g^x \bmod p$

**加密**（用公鑰 $y$，對明文 $m \in \mathbb{Z}_p^*$）：

1. 隨機選 $r$（**每次加密新選！**）
2. 密文對：

$$c_1 = g^r \bmod p, \qquad c_2 = m \cdot y^r \bmod p$$

**解密**（私鑰 $x$）：

$$m = c_2 \cdot (c_1^x)^{-1} = m \cdot (g^{rx})^{-1} \cdot g^{rx} = m \quad \blacksquare$$

（$c_1^x = g^{rx} = y^r$，除掉遮罩。）

### 為什麼隨機化是關鍵：語義安全
**問題**：確定性加密（教科書式 RSA）的弱點：同一明文永遠同密文——**字典攻擊**（明文空間小時逐項加密比對）。

**ElGamal 的隨機化**：每次加密新選 $r$：

$$\text{同一 } m \text{ 加密兩次} \implies (c_1, c_2) \ne (c_1', c_2') \quad \text{（} r \text{ 不同）}$$

**語義安全（IND-CPA）**：攻擊者選 $m_0, m_1$，看到其中之一的密文，無法分辨是誰：

$$P(\text{猜中}) \le \frac{1}{2} + \epsilon$$

ElGamal 滿足 IND-CPA（在 DDH 假設下，Goldwasser–Micali 的語義安全概念，見 `1989-零知識證明.md` 的框架）——**隨機化 = 語義安全**。這個洞見後來成為公鑰加密的標準要求（RSA 的 OAEP 填補也是為了隨機化，見 `1977-RSA.md`）。

### ElGamal 簽章 → DSA
**簽章**（私鑰 $x$，對訊息 $m$）：

1. 隨機選 $k$（**每次簽章新選！**）
2. $r = g^k \bmod p$；$s = k^{-1}(H(m) - x r) \bmod (p-1)$
3. 簽章對 $(r, s)$

**驗證**（公鑰 $y$）：

$$g^{H(m)} \equiv y^r r^s \pmod p$$

（$y^r r^s = g^{xr} g^{k \cdot k^{-1}(H - xr)} = g^{H(m)}$。）

**DSA（1991）**：美國 NIST 的數位簽章標準，ElGamal 簽章的修改版（更短簽章、更快）。**隨機數 $k$ 的致命重要性**：2010 年 Sony PS3 的 ECDSA 私鑰洩漏——$k$ 重複使用使私鑰可由兩個簽章代數解出：

$$k = \frac{H(m_1) - H(m_2)}{s_1 - s_2}$$

——**隨機數重複 = 私鑰洩漏**，這是 ElGamal/DSA/ECDSA 的頭號實戰陷阱。

### 程式碼：ElGamal 加密與簽章

```python
import random, hashlib

P, G = 2**61 - 1, 3

def mod_pow(b, e, n):
    result = 1; b %= n
    while e > 0:
        if e & 1: result = result * b % n
        b = b * b % n; e >>= 1
    return result

# 金鑰生成
x = random.getrandbits(40)            # 私鑰
y = mod_pow(G, x, P)                  # 公鑰

# 加密（每次新隨機 r！）
def elgamal_encrypt(m, y, p=P, g=G):
    r = random.getrandbits(40)        # 每次加密新選
    c1 = mod_pow(g, r, p)
    c2 = m * mod_pow(y, r, p) % p
    return c1, c2

def elgamal_decrypt(c1, c2, x, p=P):
    s = mod_pow(c1, x, p)
    return c2 * pow(s, -1, p) % p

m = 123456789
c1, c2 = elgamal_encrypt(m, y)
print(f"解密 = {elgamal_decrypt(c1, c2, x)}")          # 123456789 ✓
c1b, c2b = elgamal_encrypt(m, y)
print(f"同明文兩次密文不同：{(c1, c2) != (c1b, c2b)}")   # True（隨機化！）

# 簽章（每次新隨機 k！）
def elgamal_sign(m, x, p=P, g=G):
    H = int.from_bytes(hashlib.sha256(str(m).encode()).digest(), 'big') % (p-1)
    k = random.getrandbits(40)
    r = mod_pow(g, k, p)
    s = (pow(k, -1, p-1) * (H - x*r)) % (p-1)
    return r, s, H

r, s, H = elgamal_sign(m, x)
# 驗證：g^H == y^r * r^s mod p
lhs = mod_pow(G, H, P)
rhs = mod_pow(y, r, P) * mod_pow(r, s, P) % P
print(f"簽章驗證：{lhs == rhs}")                        # True
```

### 與 RSA 的對照

| | RSA | ElGamal |
|---|-----|---------|
| 難解問題 | 大數分解 | 離散對數 |
| 加密 | 確定性（需 OAEP 填補） | 天然隨機化（語義安全） |
| 簽章 | $m^d$（需 PSS） | $(r, s)$ 對 |
| 密文膨脹 | 1 倍 | 2 倍（$c_1, c_2$ 對） |

## 結案 -- 後果與影響
- **離散對數密碼學體系**：DH、ElGamal、DSA、ECDH、EdDSA——與 RSA 並列的兩大體系。
- **DSA 標準**：1991 年 NIST 的數位簽章標準（FIPS 186）——ElGamal 簽章的國家標準化。
- **語義安全的示範**：隨機化加密的天然語義安全——證明式安全（Goldwasser–Micali）的實例。
- **ECDSA 與區塊鏈**：比特幣/以太坊的簽章是 ECDSA（ElGamal 的橢圓曲線後代）——$k$ 重複的教訓（PS3 事件）成為區塊鏈安全的經典案例（見 `2016-區塊鏈密碼學.md`）。
- **量子威脅**：Shor 演算法（1994，見 `1994-Shor演算法.md`）破離散對數——ElGamal 家族全部需要後量子替代（見 `2017-後量子密碼學.md`）。

## 關鍵人物與文獻
- **Taher ElGamal**（1955–）：A Public Key Cryptosystem... (1985, IEEE Trans. Info. Theory)；當時是 HP 實驗室的研究員
- **NIST**：DSA 標準 (1991)
- **Goldwasser & Micali**：語義安全 (1984)——見 `1989-零知識證明.md`
- **Bernstein et al.**：EdDSA (2011)——橢圓曲線 ElGamal 簽章的現代版
- 交叉參照：`1976-DiffieHellman金鑰交換.md`、`1977-RSA.md`、`1989-零知識證明.md`、`2017-後量子密碼學.md`
