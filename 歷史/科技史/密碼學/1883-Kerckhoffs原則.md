# 1883 - Kerckhoffs 原則

## 案件摘要
1883 年，荷蘭語言學家 Auguste Kerckhoffs 在法國軍事密碼期刊發表《La cryptographie militaire》，提出軍事密碼的六項原則，其中第二條成為整個現代密碼學的基石：**「系統必須不要求保密，即使落入敵人手中也必須可靠」**——保密的應該是金鑰，不是演算法。這個「公開演算法、只藏金鑰」的原則，是 Shannon 理論（1949）、公開標準（DES、AES）、公鑰密碼學的哲學前題。

## 前因 -- 為什麼會有這個案子
19 世紀的軍事密碼界盛行「保密至上」：演算法本身是機密（法國的「黑室」、各國外交密碼局）。Kerckhoffs 觀察到這條路的致命弱點：

1. **演算法遲早洩漏**：間諜、叛逃、戰場繳獲——指望演算法不洩漏是幻想
2. **洩漏後無法補救**：演算法是硬體/程序，戰時換不掉
3. **無法檢驗安全性**：閉門造車的密碼，沒有社群檢驗，破綻無人發現

Kerckhoffs 的六原則：系統應實用（不可破譯、不依賴保密、金鑰可記憶、密文可電報傳輸、可一人操作、易用不複雜）。

## 線索與推理 -- 數學式、程式、理論

### 原則的數學化
Kerckhoffs 原則的形式化：**攻擊者知道一切除金鑰外**：

$$\text{攻擊者知道：} E, D, \text{密文 } c \quad \text{攻擊者不知道：} k$$

$$\text{安全性要求：} \text{給定 } (E, D, c)，\text{無法推出明文 } m \text{（除非窮舉 } k\text{）}$$

**對照**：security through obscurity（靠隱蔽求安全）：

$$\text{攻擊者不知道：} E, D, k \quad \text{——一旦 } E, D \text{ 洩漏，全盤崩潰}$$

### 為什麼公開演算法更安全
**推理**（Kerckhoffs 的邏輯 + 後世的驗證）：

1. **演算法必洩漏**：$P(\text{演算法洩漏}) \approx 1$（長期、大規模使用下）
2. **公開 = 免費的檢驗**：全世界密碼學家、駭客、情報機構都在攻擊——漏洞被發現得早
3. **金鑰可換**：金鑰是資料，每天/每 session 換一次，洩漏損害有限

**範例對照**：
- DES（1977，公開標準）：40 年公開攻擊下依然「金鑰空間內安全」（見 `1977-DES.md`）
- GSM 的 A5/1（保密演算法）：1990 年代被逆向工程後漏洞頻出

### Shannon 的理論化 (1949)
Shannon 在《Communication Theory of Secrecy Systems》中把 Kerckhoffs 原則數學化：

**完美保密**的定義：

$$P(m \mid c) = P(m) \quad \text{（密文不提供任何關於明文的資訊）}$$

**定理**：完美保密 ⟺ 金鑰不確定性 ≥ 明文不確定性：

$$H(K) \ge H(M)$$

**推論**：金鑰必須與訊息等長且真隨機（一次性密碼本）——任何金鑰較短的系統（所有實用密碼）都**不是完美保密**，只能追求**計算保密**：

$$\text{計算保密} = \text{破譯需要超過多項式（或實際可行）的計算資源}$$

**偵探筆記**：Kerckhoffs 原則的推理是「假設最壞」——不是希望演算法不洩漏，而是**設計成洩漏了也沒事**。這個「最壞情況安全」的思維與計算理論的最壞情況分析（見 `../計算理論/1965-HartmanisStearns時間階層.md`）同源：**工程的安全與效率都建立在「敵人/最壞情況存在」的假設上**。

### 程式碼：Kerckhoffs 原則的概念示範

```python
# security through obscurity：藏演算法（脆弱）
def secret_algorithm_encrypt(msg):   # 假設這是機密
    return caesar_encrypt(msg, k=7)  # 一旦被逆向，全崩

# Kerckhoffs：公開演算法，金鑰保密（魯棒）
def encrypt(msg, key):               # E 公開
    return caesar_encrypt(msg, key)  # k 每日更換
# 洩漏 k=今天的金鑰 → 只影響今天的訊息，明天換新的

# Shannon 的完美保密：一次性密碼本
import random, os
def otp_encrypt(msg):
    key = os.urandom(len(msg))       # 真隨機、等長、只用一次
    return bytes(a ^ b for a, b in zip(msg.encode(), key)), key
def otp_decrypt(cipher, key):
    return bytes(a ^ b for a, b in zip(cipher, key)).decode()

c, k = otp_encrypt("ATTACK AT DAWN")
print(otp_decrypt(c, k))             # ATTACK AT DAWN
# H(K) = H(M)：完美保密——但金鑰要安全傳給對方（雞生蛋問題！）
# 這個「金鑰分發問題」正是公鑰密碼學（1976）要解的
```

## 結案 -- 後果與影響
- **現代密碼學的第一原理**：所有標準（DES、AES、TLS）都是公開演算法——社群攻擊是安全性的來源。
- **計算保密 vs 完美保密**：Shannon 的區分確立了現代密碼學的目標（計算保密）與理想（完美保密）。
- **公開標準的流程**：NIST 的 AES 競賽（1997–2001）——公開徵求、公開攻擊、公開評選。
- **「security through obscurity」成為貶義**：閉源密碼（GSM A5、多數商業系統）的教訓。
- **金鑰分發問題**：Kerckhoffs 之謎的延伸——公開演算法後，金鑰怎麼安全送到對方手上？這個問題吊了 90 年，直到 Diffie–Hellman（1976，見 `1976-DiffieHellman金鑰交換.md`）。

## 關鍵人物與文獻
- **Auguste Kerckhoffs**（1835–1903）：La cryptographie militaire (1883, J. des Sciences Militaires)
- **Claude Shannon**（1916–2001）：Communication Theory of Secrecy Systems (1949)
- 交叉參照：`1949-Shannon保密理論.md`、`1976-DiffieHellman金鑰交換.md`、`1977-DES.md`
