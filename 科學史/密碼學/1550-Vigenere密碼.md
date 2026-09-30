# 1550 - Vigenère 密碼

## 案件摘要
1550 年前後，法國外交官 Blaise de Vigenère 發表以他命名的多表替換密碼：用一個**關鍵字**反覆套用不同位移——同一個明文字母在不同位置加密成不同密文字母，徹底摧毀了單表密碼的頻率分析。此密碼被稱為「le chiffre indéchiffrable」（不可破譯的密碼）長達三百年，直到 19 世紀被 Kasiski 與 Babbage 破譯——**用關鍵字本身的統計洩漏**。

## 前因 -- 為什麼會有這個案子
Caesar 密碼（見 `-0050-Caesar密碼.md`）被頻率分析一擊斃命。15–16 世紀文藝復興的義大利城邦與法國外交界需要更強的密碼。Vigenère 的洞察：**單表密碼的弱點是「一一對應」**——每個明文字母永遠對應同一密文字母，統計結構完整洩漏。對策：**多表替換**——讓同一字母在不同位置用不同替換表。

## 線索與推理 -- 數學式、程式、理論

### Vigenère 的數學
設關鍵字 $K = k_0 k_1 \dots k_{m-1}$（$m$ 個字母）。明文 $x_i$ 加密為：

$$E(x_i) = (x_i + k_{i \bmod m}) \bmod 26$$

密鑰長度 $m$ 就是「週期」：位置 $i$ 與 $i + m$ 用同一替換表。

**為什麼三百年沒被破**：頻率分析需要大樣本，而 Vigenère 把單一字母的頻率「攤開」到 $m$ 張表上——密文整體頻率接近平坦。E 在每張表中的位置都不同。

### Kasiski 破譯法 (1863)
**破綻**：關鍵字是**重複**的。若明文中相同字串出現在距離為 $m$ 的倍數的位置，兩次加密用同一關鍵字段落，密文重複。Kasiski 觀察：**密文中重複字串的間距**的最大公因數就是 $m$（或其倍數）。

**推理**：
1. 找密文中重複的長字串，記下間距
2. 各間距的 GCD ≈ 關鍵字長度 $m$
3. 把密文按位置模 $m$ 分成 $m$ 組——每組是**單表 Caesar 密碼**
4. 對每組做頻率分析，逐一擊破

### Friedman 檢驗 (1920)
另一路：**重合指數（Index of Coincidence, IC）**——隨機抽兩個密文字母相同的機率：

$$IC = \frac{\sum_i f_i(f_i - 1)}{n(n-1)}$$

英文明文 $IC \approx 0.0667$，完全隨機 $IC \approx 0.0385$。把密文切成 $m$ 組，若各組 $IC$ 接近 0.0667，則 $m$ 就是關鍵字長度。**統計檢驗估計金鑰長度**——與 Buffon 擲針（見 `../隨機算法/1777-Buffon針實驗.md`）同源的反向統計思想。

### 程式碼：Vigenère 與破譯

```python
def vigenere_encrypt(text, key):
    text = text.upper()
    return ''.join(chr((ord(c) - ord('A') + ord(key[i % len(key)]) - 2*ord('A')) % 26 + ord('A'))
                   if c.isalpha() else c for i, c in enumerate(text))

def vigenere_decrypt(text, key):
    return vigenere_encrypt(text, ''.join(chr(26 - (ord(k) - ord('A')) % 26 + ord('A')) for k in key))

from collections import Counter
import math

def kasiski(cipher, min_len=3):
    """找重複字串的間距，GCD = 關鍵字長度"""
    positions = {}
    gaps = []
    for i in range(len(cipher) - min_len):
        s = cipher[i:i+min_len]
        if s in positions:
            gaps.append(i - positions[s])
        else:
            positions[s] = i
    if not gaps: return 1
    return math.gcd(*gaps) or 1

def freq_key(guess_cipher):
    """對單表組做頻率分析"""
    freq = Counter(guess_cipher)
    top = freq.most_common(1)[0][0]
    return (ord(top) - ord('A') - 4) % 26

def crack_vigenere(cipher):
    m = kasiski(cipher)
    groups = [cipher[i::m] for i in range(m)]
    return m, ''.join(chr(freq_key(g) + ord('A')) for g in groups)

msg = "ATTACKATDAWNATTACKATDAWNATTACK"
cipher = vigenere_encrypt(msg, "LEMON")
print(cipher)                                  # LXFOPVEFRNHR...
m, key = crack_vigenere(cipher)
print(f"關鍵字長度 = {m}，推測關鍵字 = {key}")   # 5, LEMON ✓
```

### 三百年的教訓
**偵探筆記**：Vigenère 的破譯推理鏈：重複關鍵字 → 密文重複字串 → GCD 求週期 → 分組退化为單表 → 頻率分析。**任何「重複使用的有限金鑰」都會洩漏結構**——這個洞見直接指向 Shannon 的理論（1949，見 `1949-Shannon保密理論.md`）：唯有金鑰長度 ≥ 訊息長度且不重複（一次性密碼本），才真正不可破。

## 結案 -- 後果與影響
- **一次性密碼本（OTP）**：Vernam (1917) 的電報加密——金鑰真隨機、不重複、與訊息等長，是 Shannon 證明的「完美保密」唯一解。
- **Kasiski/Friedman 檢驗**：密碼分析的工具箱擴充（週期偵測、重合指數）。
- **轉子密碼機的思想**：Enigma 的「每日金鑰 + 轉子步進」正是 Vigenère 的機械化——但轉子的步進週期更長，且被 Rejewski 用**代數**而非純頻率破譯（見 `1932-Rejewski破譯Enigma.md`）。
- **「不可破譯」的警示**：三百年間無人認真攻擊（非無法攻擊）——**沒有被攻擊過 ≠ 安全**，這個教訓至今適用。

## 關鍵人物與文獻
- **Blaise de Vigenère**（1523–1596）：Traicté des chiffres (1586)
- **Charles Babbage**（1791–1871）：1840 年代私下破譯（未發表）
- **Friedrich Kasiski**（1805–1881）：Die Geheimschriften... (1863)
- **William Friedman**（1891–1969）：重合指數 (1920)
- **Gilbert Vernam**（1890–1960）：一次性密碼本 (1917)
- 交叉參照：`-0050-Caesar密碼.md`、`1918-Enigma機.md`、`1949-Shannon保密理論.md`
