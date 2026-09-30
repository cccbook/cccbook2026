# 1979 - Shamir 秘密分享

## 案件摘要
1979 年，Adi Shamir 發表《How to Share a Secret》：把秘密 $S$（如核武發射碼）拆成 $n$ 片分給 $n$ 人，**任意 $k$ 片可以重組秘密，$k-1$ 片什麼都不知道**。用 Lagrange 多項式插值實現——數學優雅到一頁就能證明。這是「門檻密碼學」（threshold cryptography）的誕生：安全性不再依賴單點，而是分佈式信任——核武控制、金鑰託管、多簽錢包的基礎。

## 前因 -- 為什麼會有這個案子
現實的安全困境：**單點秘密太脆弱**——

- 核武發射碼放在總統一人手裡？（獨裁）
- 放在保險櫃？（偷竊、火災、單點故障）
- 復印多份？（洩漏風險倍增）

**需求**：秘密的「分佈式保管」——$n$ 人保管，需要 $k$ 人合作才能用。數學問題：**如何拆分秘密，使得少於 $k$ 片洩漏零資訊？**

## 線索與推理 -- 數學式、程式、理論

### Shamir 的 $(k, n)$ 門檻方案
**拆分**：秘密是 $\mathbb{Z}_p$ 中的元素 $S$（$p$ 大質數）。

1. 構造 $k-1$ 次多項式：

$$f(x) = S + a_1 x + a_2 x^2 + \dots + a_{k-1} x^{k-1} \pmod p$$

其中 $a_1, \dots, a_{k-1}$ 真隨機。

2. 發給第 $i$ 人一片：$f(i)$（$i = 1, \dots, n$）

**重組**：任意 $k$ 片 $(x_i, f(x_i))$，用 **Lagrange 插值**還原多項式，取 $f(0) = S$：

$$S = \sum_{i=1}^k f(x_i) \prod_{j \ne i} \frac{-x_j}{x_i - x_j} \pmod p$$

### 為什麼 k-1 片什麼都不知道
**定理**：$k-1$ 片 $(x_i, f(x_i))$ 對 $S$ 的資訊為**零**。

**證明**：$k-1$ 個點只能確定 $k-2$ 次多項式；對任何候選秘密 $S'$，都存在唯一 $k-1$ 次多項式經過這 $k-1$ 點與 $(0, S')$——**所有 $S'$ 等機率**：

$$P(S = s' \mid k-1 \text{ 片}) = \frac{1}{p} = P(S = s') \quad \blacksquare$$

（$a_{k-1}$ 以上的係數是真隨機的——多餘的自由度讓所有 $S'$ 皆可能。）

**偵探筆記**：這個證明的推理是「自由度」——$k-1$ 點 + 任意 $S'$ 恰好唯一確定多項式，所以每個 $S'$ 的後驗機率相同。**與 Shannon 完美保密（見 `1949-Shannon保密理論.md`）同源**：$H(S \mid k-1 \text{ 片}) = H(S)$——完美保密的門檻版。

### 程式碼：Shamir 秘密分享

```python
import random

P = 2**61 - 1     # 大質數

def share_secret(S, k, n):
    """(k, n) 門檻：S 拆成 n 片，k 片可重組"""
    coeffs = [S] + [random.getrandbits(40) for _ in range(k - 1)]
    shares = []
    for i in range(1, n + 1):
        y = sum(c * pow(i, j, P) for j, c in enumerate(coeffs)) % P
        shares.append((i, y))
    return shares

def reconstruct(shares):
    """Lagrange 插值：k 片還原 f(0) = S"""
    S = 0
    for i, yi in shares:
        num = den = 1
        for j, yj in shares:
            if j != i:
                num = num * (-j) % P
                den = den * (i - j) % P
        S = (S + yi * num * pow(den, -1, P)) % P
    return S

random.seed(42)
S = 987654321
shares = share_secret(S, k=3, n=5)
print(f"5 片：{shares}")

# 3 片可重組
print(f"3 片重組 = {reconstruct(shares[:3])}")   # 987654321 ✓
print(f"另 3 片重組 = {reconstruct(shares[2:])}")  # 987654321 ✓

# 2 片什麼都不知道（自由度：所有 S' 皆可能）
print("k-1=2 片：任何候選 S' 都有多項式經過——零資訊")
```

### 變體與擴展
- **可驗證秘密分享（VSS）**（Feldman 1987、Pedersen 1991）：片可驗證（防惡意分享）——用指數承諾。
- **Feldman VSS**：公開 $g^{a_j}$（承諾），任何人驗證 $g^{f(i)} = \prod (g^{a_j})^{i^j}$——與 DH 的離散對數結合（見 `1976-DiffieHellman金鑰交換.md`）。
- **主動攻擊**（ proactive）：定期換片（秘密不變）——長期保管的魯棒性。
- **MPC 的基礎**：多方安全計算（secure multi-party computation）用秘密分享在秘密上計算——Yao 的百萬富翁問題（1982）的實現基礎。

### 門檻密碼學的帝國
- **核武控制**：兩人規則（two-man rule）的數學化——NASA、軍方系統。
- **金鑰託管**：CA 根金鑰、DNSSEC 的多簽。
- **多簽錢包**：比特幣/以太坊的 multisig（$k$-of-$n$ 簽章）——門檻簽章的區塊鏈實現（見 `2016-區塊鏈密碼學.md`）。
- **門檻 RSA/ECDSA**：簽章金鑰拆片——機構簽章的分散式保管。

**偵探筆記**：Shamir 的推理是「把 Shannon 的完美保密從空間維度搬到人數維度」——密文換成「片」，隨機金鑰換成「隨機多項式」。**同一個數學（隨機化 + 完美保密），不同的應用場景**——這是密碼學理論的統一之美。

## 結案 -- 後果與影響
- **門檻密碼學誕生**：$(k, n)$ 門檻成為分佈式信任的標準模型。
- **MPC 的基礎**：多方安全計算（Yao 1982、GMW 1987）以秘密分享為基礎工具。
- **區塊鏈的 multisig**：$k$-of-$n$ 多簽錢包、門檻簽章（threshold signatures）。
- **VSS 與主動攻擊**：可驗證、可更新的秘密分享——長期保管的工程化。
- **Shamir 的帝國**：RSA（1977）、背包破解（1982）、秘密分享（1979）——Shamir 是密碼學史最多產的人物之一，圖靈獎 2002。

## 關鍵人物與文獻
- **Adi Shamir**（1952–）：How to Share a Secret (1979, Comm. ACM)；圖靈獎 2002
- **Blakley**：1979 同期獨立提出（幾何版本——超平面交集）
- **Feldman / Pedersen**：可驗證秘密分享 (1987/1991)
- **Goldreich–Micali–Wigderson**：GMW 協議 (1987)——MPC
- 交叉參照：`1977-RSA.md`、`1976-DiffieHellman金鑰交換.md`、`1949-Shannon保密理論.md`、`2016-區塊鏈密碼學.md`
