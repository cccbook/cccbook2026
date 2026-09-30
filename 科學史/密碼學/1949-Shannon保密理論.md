# 1949 - Shannon 保密理論

## 案件摘要
1949 年，Claude Shannon 發表《Communication Theory of Secrecy Systems》：把密碼學從「手藝與迷信」變成**數學科學**——定義完美保密（密文不洩漏任何明文資訊），用資訊熵證明**一次性密碼本是唯一完美保密系統**，並提出「混合變換」（mixing transformation）與「擴散/混淆」（diffusion/confusion）的設計原則——現代密碼（DES、AES）的設計藍圖。這是密碼學史的分水嶺：Shannon 之前是古典密碼，之後是現代密碼。

## 前因 -- 為什麼會有這個案子
Shannon 的動機有三層：

1. **戰時經驗**：Shannon 在貝爾實驗室參與美軍密碼工作（與英國 X 站合作），接觸到 Vernam 的一次性密碼本
2. **資訊論**：1948 年 Shannon 發表《A Mathematical Theory of Communication》——資訊熵 $H$、通道容量。密碼學是「敵對通道」——自然延伸
3. **Kerckhoffs 原則的數學化**：1883 年的原則（保密在金鑰）需要定理級的證明（見 `1883-Kerckhoffs原則.md`）

## 線索與推理 -- 數學式、程式、理論

### 密碼系統的數學模型
Shannon 的模型（與圖靈機同年代的公理化風格）：

$$\text{明文 } M \xrightarrow{E_k} \text{密文 } C = E_k(M) \xrightarrow{D_k} M = D_k(C)$$

其中 $E_k, D_k$ 是金鑰 $k$ 的函數，$D_k(E_k(M)) = M$（可逆）。

### 完美保密
**定義**：密碼系統是完美保密的，若密文與明文**統計獨立**：

$$P(M = m \mid C = c) = P(M = m) \quad \forall m, c$$

（觀察密文後，對明文的認識**完全沒有增加**。）

**定理（Shannon）**：完美保密 ⟺

$$H(M \mid C) = H(M) \iff H(K \mid C) \ge H(M)$$

由熵的鏈式法則：

$$H(K, M, C) = H(K) + H(M) = H(C \mid K, M) + H(K, M) = H(C \mid K, M) + H(K) + H(M)$$

且 $H(C \mid K, M) = 0$（$C$ 由 $K, M$ 決定）、$H(K \mid C, M) = 0$（給定 $C, M$ 可解 $K$），推出：

$$H(C) = H(K) + H(M) - H(K \mid C) \ge H(M) \implies H(K \mid C) \ge H(M)$$

**白話**：**金鑰的不確定性必須 ≥ 明文的不確定性**——金鑰要與訊息等長且真隨機。

### 一次性密碼本（OTP）的唯一性
**驗證**：OTP（Vernam 1917）：$C = M \oplus K$，$K$ 真隨機、等長、只用一次：

$$H(K) = n \log_2 26 = H(M) \implies \text{完美保密} \quad \blacksquare$$

**反面**：任何金鑰較短的系統（Vigenère、Enigma、DES、AES、RSA），$H(K) < H(M)$，**都不是完美保密**——理論上可被「無限計算」破譯。實用密碼只能追求**計算保密**：破譯需要超過實際可行的計算資源。

### 擴散與混淆（Diffusion & Confusion）
Shannon 的設計原則——實用密碼的兩大支柱：

- **混淆（confusion）**：密文與金鑰的關係越複雜越好——敵人無法利用金鑰-密文的簡單結構。實現：S-Box（代換盒）
- **擴散（diffusion）**：明文的一位元影響密文的許多位元——統計結構被攤平，頻率分析失效。實現：P-Box（置換盒）與多輪迭代

$$\text{理想：} \text{改變明文一位元} \implies \text{密文約一半位元改變（雪崩效應）}$$

**混合變換**：混淆與擴散的反覆迭代——**S-Box + P-Box 的多輪結構**。這個藍圖在 Feistel（1970，見 `1970-Lucifer.md`）的 Lucifer、DES（1977）、AES（2001）中完整實現。

### 程式碼：OTP 與熵

```python
import os, math
from collections import Counter

def otp_encrypt(msg):
    key = os.urandom(len(msg))       # 真隨機、等長
    return bytes(a ^ b for a, b in zip(msg.encode(), key)), key

def otp_decrypt(cipher, key):
    return bytes(a ^ b for a, b in zip(cipher, key)).decode()

msg = "ATTACK AT DAWN" * 100
c, k = otp_encrypt(msg)
print(otp_decrypt(c, k) == msg)      # True

# Shannon 的判準：H(K) = H(M)？
def entropy(data):
    freq = Counter(data)
    n = len(data)
    return -sum(f/n * math.log2(f/n) for f in freq.values())

print(f"H(M) = {entropy(msg.encode()):.1f} bits（英文文本熵低！約 4.5/字母）")
print(f"H(K) = {entropy(k):.1f} bits（真隨機 = 8/byte，且長度 = 訊息長度）")
# H(K) > H(M)：完美保密 ✓

# 反例：Caesar 密碼 H(K) = log2(25) ≈ 4.6 bits——遠小於 H(M)
print(f"H(Caesar key) = {math.log2(25):.1f} bits → 非完美保密")
```

### 訊息驗證的伏筆
Shannon 還區分了兩個目標：**保密性（secrecy）**與**認證性（authentication）**——敵人不僅能偷看，還能偽造。認證的數學化（MAC、數位簽章）在 1970 年代由 Carter–Wegman（見 `1979-CarterWegman通用雜湊.md`）與 Diffie–Hellman 完成觀點（見 `1974-Diffie公鑰構想.md`）。

## 結案 -- 後果與影響
- **密碼學成為數學**：公理化模型、定理、證明——現代密碼學的誕生。
- **一次性密碼本的地位**：唯一完美保密，用於莫斯科–華盛頓熱線（紅色電話）。
- **擴散/混淆藍圖**：DES、AES 的 S-Box + P-Box 多輪結構直接源於此。
- **計算保密的確立**：實用密碼的目標從「完美」降為「計算上不可破」——與計算複雜度理論（見 `../計算理論/README.md`）的連結。
- **資訊論的帝國**：Shannon 的熵、通道容量、率失真理論——資訊時代的一切基礎。

## 關鍵人物與文獻
- **Claude Shannon**（1916–2001）：Communication Theory of Secrecy Systems (1949, Bell System Tech. J.)；A Mathematical Theory of Communication (1948)
- **Gilbert Vernam**：一次性密碼本 (1917)
- 交叉參照：`1883-Kerckhoffs原則.md`、`1970-Lucifer.md`、`../隨機算法/README.md`
