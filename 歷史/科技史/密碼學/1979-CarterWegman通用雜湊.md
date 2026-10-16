# 1979 - Carter–Wegman 通用雜湊

## 案件摘要
1979 年，Larry Carter 與 Mark Wegman 發表《Universal Classes of Hash Functions》：定義**通用雜湊函數族**——任何兩個不同元素，在族中隨機選的雜湊函數下碰撞機率 $\le 1/|S|$。這是「隨機化雜湊」的數學基礎，並直接催生**訊息認證碼（MAC）**：用通用雜湊製造「幾乎不可偽造」的認證標籤（Wegman–Carter MAC）。Karp–Rabin 滾動雜湊（見 `../隨機算法/1987-KarpRabin字串匹配.md`）的理論基礎、現代 TLS 的 Poly1305、Chacha20 的祖師。

## 前因 -- 為什麼會有這個案子
1970 年代雜湊表的困境：**最壞情況輸入**——敵人可以構造全部碰撞的輸入，雜湊表退化為 $O(n)$ 鏈表。同時，Shannon 區分的認證問題（見 `1949-Shannon保密理論.md`）需要數學化：**如何讓偽造訊息的機率極小？**

Carter–Wegman 的兩個問題：
1. **雜湊**：能否保證「任何輸入」下碰撞機率可控？（不依賴輸入分佈）
2. **認證**：能否用短標籤證明訊息未被篡改？

## 線索與推理 -- 數學式、程式、理論

### 通用雜湊的定義
**定義**：函數族 $\mathcal{H}: U \to S$ 是通用的（universal），若任何 $x \ne y$：

$$P_{h \sim \mathcal{H}}(h(x) = h(y)) \le \frac{1}{|S|}$$

（隨機選 $h$，兩元素碰撞機率至多為「純隨機」的水準。）

**範例**：$U = \mathbb{Z}_p$、$S = \mathbb{Z}_m$（$m \le p$），

$$h_{a,b}(x) = (ax + b) \bmod p \bmod m, \quad a, b \text{ 隨機}$$

——**多項式族**的通用性（由 $ax + b = ay + b \implies a(x - y) \equiv 0 \implies a \equiv 0$ 的唯一解）。

**對照**：固定雜湊（如 CRC）沒有此保證——敵人構造碰撞。**隨機化雜湊 = 任何輸入都安全**——這與 Kerckhoffs 原則（見 `1883-Kerckhoffs原則.md`）同源：安全不依賴輸入的分佈假設。

### Wegman–Carter MAC
**認證協議**：

1. 雙方共享金鑰：雜湊族中的一個函數 $h$（或一次性密鑰 $k$）
2. 發送方：標籤 $\sigma = h(m)$
3. 驗證方：$h(m) \stackrel{?}{=} \sigma$

**定理（Wegman–Carter）**：偽造機率 $\le 1/|S|$；若每次訊息換一個一次性密鑰（選新的 $h$），偽造機率 $\le (1/|S|)^t$ 級——**指數衰減**。

**推理**：偽造者沒見過 $h(m)$ 對應的真標籤（或見過的是另一訊息的），從 $h$ 的通用性，猜中標籤的機率至多 $1/|S|$——**通用雜湊的碰撞界就是偽造界**。

### 程式碼：通用雜湊與 MAC

```python
import random, os

class UniversalHash:
    """h_{a,b}(x) = (a*x + b) mod p mod m"""
    def __init__(self, p=2**61 - 1, m=2**32):
        self.p, self.m = p, m
        self.a = random.randrange(1, p)
        self.b = random.randrange(0, p)

    def __call__(self, x):
        return ((self.a * x + self.b) % self.p) % self.m

def carter_mac(msg_bytes, key):
    h = UniversalHash()
    h.a, h.b = key
    x = int.from_bytes(msg_bytes, 'big') % h.p
    return h(x)

random.seed(42)
msg = b"transfer $1000 to Alice"
key = (random.randrange(1, 2**61 - 1), random.randrange(2**61 - 1))
tag = carter_mac(msg, key)
print(f"MAC = {tag}")

# 攻擊者：改訊息但不知道金鑰，偽造標籤的機率 ≤ 1/2^32
forged = carter_mac(b"transfer $9999 to Eve", key)  # 攻擊者算不出！
# 驗證方拒絕：h(m') != 偽標籤（機率上）
print("通用雜湊的碰撞界 = 偽造界")
```

### 現代 MAC 的譜系
- **HMAC**（Bellare–Canetti–Krawczyk 1996）：用密碼學雜湊（SHA-256）構造 MAC——標準化（見 `1985-密碼學雜湊函數.md`）。
- **Poly1305**（Bernstein 2005）：通用雜湊（多項式求值）+ 一次性密鑰——ChaCha20-Poly1305（TLS 1.3 的 AEAD 標準）。
- **AEAD**（authenticated encryption with associated data）：加密 + 認證合一——GCM（Galois/Counter Mode，用通用雜湊的 GHASH）。
- **CMS 的親戚**：Carter–Wegman 的通用雜湊也是串流算法的基礎（見 `../隨機算法/2005-CountMinSketch.md` 的 Count Sketch）。

**偵探筆記**：Carter–Wegman 的推理是「通用性 = 對抗最壞輸入」——不假設輸入分佈，而是**隨機化雜湊函數本身**讓任何輸入都安全。這與 Yao 原理（見 `../隨機算法/1985-Yao計算隨機性.md`）的思想同源：**最壞情況 + 隨機化 = 平均情況的行為**。

## 結案 -- 後果與影響
- **現代 MAC 的基礎**：HMAC、Poly1305、GHASH——TLS 的訊息認證全是其後代。
- **AEAD 的誕生**：加密 + 認證合一（GCM、ChaCha20-Poly1305）成為 TLS 1.3 標準。
- **隨機化雜湊的理論**：Karp–Rabin（見 `../隨機算法/1987-KarpRabin字串匹配.md`）、MinHash（見 `../隨機算法/1997-BroderMinHash.md`）的理論基礎。
- **雜湊表的魯棒性**：Cuckoo hashing、randomized hashing——對抗雜湊泛洪攻擊（hash flooding，2003 年 SipHash 的動機）。
- **認證問題的數學化**：Shannon 區分的第二目標（認證）終於有了數學基礎——保密與認證是**不同的問題**（這個區分到 Diffie–Hellman 的構想才被廣泛理解，見 `1974-Diffie公鑰構想.md`）。

## 關鍵人物與文獻
- **Larry Carter**（1949–2017）：IBM；通用雜湊
- **Mark Wegman**（1953–）：IBM；Wegman–Carter MAC
- Carter & Wegman: Universal Classes of Hash Functions (1979, JCSS)
- **Bellare, Canetti, Krawczyk**：HMAC (1996)
- **Bernstein**：Poly1305 (2005)
- 交叉參照：`1949-Shannon保密理論.md`、`1985-密碼學雜湊函數.md`、`../隨機算法/1987-KarpRabin字串匹配.md`
