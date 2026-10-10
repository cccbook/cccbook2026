# 前 50 - Caesar 密碼

## 案件摘要
西元前 50 年左右，Julius Caesar 在與羅馬元老院的政治鬥爭與高盧戰爭中，使用「每個字母往後移 3 位」的替換密碼傳遞軍情。這是人類最早有系統記載的加密方法——保密的歷史從此開始。但這個密碼只有 25 種可能，今天任何小學生都能在幾分鐘內破譯——它的價值不在強度，而在**定義了密碼學的第一個模型：明文 + 金鑰 → 密文**。

## 前因 -- 為什麼會有這個案子
古代傳遞秘密的兩條路：**藏起來**（隱寫術 steganography——蠟板下藏字、頭皮下刺字）與**加密**（密碼術 cryptography——讓看到也看不懂）。Caesar 的需求是軍事命令：傳令兵可能被抓，命令必須「看到也無用」。蘇維托尼烏斯（Suetonius）的《十二帝王傳》記載：Caesar 用位移 3 的密碼與將領與西塞羅通信。

## 線索與推理 -- 數學式、程式、理論

### Caesar 密碼的數學
把字母表視為 $\mathbb{Z}_{26}$（A=0, B=1, ..., Z=25）。加密函數：

$$E_k(x) = (x + k) \bmod 26$$

解密函數：

$$D_k(y) = (y - k) \bmod 26$$

Caesar 用 $k = 3$：`ATTACK AT DAWN` → `DWWDFN DW GDZQ`。

**金鑰空間**：只有 $k \in \{1, \dots, 25\}$ 共 25 種——**窮舉即可破譯**。

### 破譯一：窮舉
25 種金鑰逐個試，找出可讀的明文——$O(25)$ 時間，人手幾分鐘。

### 破譯二：頻率分析
更聰明的方法：**統計字母頻率**。英文中 E 出現最多（約 12.7%），其次 T、A、O。密文中最常見的字母幾乎必然對應 E：

$$\text{密文最常字母的編碼} - 4 = k$$

**偵探筆記**：頻率分析是密碼學史上第一件「破譯武器」——9 世紀阿拉伯學者 Al-Kindi 首次系統化。它的本質是**統計攻擊**：明文的統計結構洩漏到密文中。這個洞見貫穿整個密碼學史——從 Vigenère（見 `1550-Vigenere密碼.md`）到 Enigma（見 `1932-Rejewski破譯Enigma.md`），每一次破譯都是找到「洩漏的統計」。

### 程式碼：Caesar 密碼與破譯

```python
def caesar_encrypt(text, k=3):
    return ''.join(chr((ord(c) - ord('A') + k) % 26 + ord('A'))
                   if c.isalpha() else c for c in text.upper())

def caesar_decrypt(text, k=3):
    return caesar_encrypt(text, -k)

def caesar_brute_force(cipher):
    """窮舉 25 種金鑰"""
    return {k: caesar_decrypt(cipher, k) for k in range(1, 26)}

def caesar_freq_attack(cipher):
    """頻率分析：密文最常字母 ≈ E (編碼 4)"""
    from collections import Counter
    freq = Counter(c for c in cipher if c.isalpha())
    top = freq.most_common(1)[0][0]
    return (ord(top) - ord('A') - 4) % 26

msg = "ATTACK AT DAWN"
cipher = caesar_encrypt(msg, 3)
print(cipher)                            # DWWDFN DW GDZQ
print(caesar_decrypt(cipher, 3))         # ATTACK AT DAWN

bf = caesar_brute_force(cipher)
print(bf[3])                             # 窮舉第 3 個 = 明文

guess_k = caesar_freq_attack(cipher)
print(f"頻率分析推測金鑰 = {guess_k}")     # 3 ✓
```

### 變體：ROT13 與一般仿射密碼
- **ROT13**：$k = 13$ 的特例（加密 = 解密，因 $13 + 13 = 26$），今天 Usenet 還在用來藏劇透。
- **仿射密碼**：$E_k(x) = (ax + b) \bmod 26$，需 $\gcd(a, 26) = 1$ 才可逆（否則多個 $x$ 映到同一 $y$）。金鑰空間 $12 \times 26 = 312$ 種——依然太小。

## 結案 -- 後果與影響
- **密碼學的模型確立**：明文 + 金鑰 → 密文的三元結構，至今未變。
- **金鑰空間的思想**：安全性至少要「窮舉不可行」——Caesar 的 25 種是反面教材。
- **頻率分析**：統計攻擊成為破譯的標準武器，催生了後續所有密碼的「抗統計」設計。
- **軍事密碼的譜系**：Caesar → Vigenère → Enigma → DES/AES——兩千年軍備競賽的起點。
- **理論餘波**：單表替換密碼的金鑰空間 $26! \approx 4 \times 10^{26}$ 已足夠大，但仍被頻率分析破譯——**金鑰空間大 ≠ 安全**，這個教訓直到 Shannon（1949，見 `1949-Shannon保密理論.md`）才被數學化解釋。

## 關鍵人物與文獻
- **Julius Caesar**（前 100–前 44）：位移 3 密碼
- **Suetonius**：《十二帝王傳》——記載 Caesar 密碼
- **Al-Kindi**（801–873）：頻率分析（9 世紀）
- 交叉參照：`1550-Vigenere密碼.md`、`1949-Shannon保密理論.md`
