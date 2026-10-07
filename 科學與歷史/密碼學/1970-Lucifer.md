# 1970 - Lucifer

## 案件摘要
1970 年前後，IBM 的 Horst Feistel 領導團隊開發 **Lucifer**——第一個實用的區塊密碼：64 位元區塊、Feistel 結構（一半加密另一半、互換、多輪迭代）。它直接成為 DES（1977，見 `1977-DES.md`）的原型，而 **Feistel 結構**成為區塊密碼設計的經典範式——「加密函數不必可逆，結構保證可逆」的天才設計。這是 Shannon 擴散/混淆藍圖（見 `1949-Shannon保密理論.md`）的第一次工程實現。

## 前因 -- 為什麼會有這個案子
1970 年代的商業需求：銀行間電子轉帳（花旗、IBM 客戶）需要加密——但一次性密碼本金鑰分發不可行（見 `1949-Shannon保密理論.md`），古典密碼可破。Feistel 的問題：**能否造一個「金鑰較短、可機械化、抗統計攻擊」的實用密碼？**

## 線索與推理 -- 數學式、程式、理論

### Feistel 結構
把 64 位元區塊分成左右兩半 $L, R$（各 32 位元），每輪：

$$L_{i+1} = R_i, \qquad R_{i+1} = L_i \oplus F(R_i, k_i)$$

其中 $F$ 是輪函數（混淆函數），$k_i$ 是子金鑰。$n$ 輪後輸出 $(L_n, R_n)$。

**天才之筆**：$F$ **不必可逆**！解密只需：

$$R_i = L_{i+1}, \qquad L_i = R_{i+1} \oplus F(L_{i+1}, k_i)$$

**可逆性來自結構（互換 + XOR），不來自 $F$ 本身**——$F$ 可以是任意的複雜函數（S-Box、混淆），不用管可逆性。這解開了區塊密碼設計的枷鎖。

### 為什麼多輪
單輪 Feistel 的安全性等於 $F$ 的安全性（可分析）。多輪的**雪崩效應**（Shannon 的擴散，見 `1949-Shannon保密理論.md`）：

$$\text{改變 } L \text{ 或 } R \text{ 一位元} \xrightarrow{\text{每輪擴散}} \text{數輪後約一半位元改變}$$

16 輪 DES 的雪崩效應：一位元差異 → 約 32 位元密文差異（統計上）。

### Lucifer → DES
Lucifer 的參數：64 位元區塊、128 位元金鑰、輪數可變。NSA（美國國家安全局）介入標準化過程，要求**縮短金鑰至 56 位元**、修改 S-Box 設計——這個「削弱」後來成為 DES 的最大爭議（見 `1977-DES.md`），但 1990 年代的差分密碼分析（Biham–Shamir）發現：NSA 修改後的 S-Box **反而抗差分攻擊**——NSA 早在 1970 年代就知道差分攻擊（保密十餘年）。

### 程式碼：Feistel 結構

```python
def feistel_encrypt(block, round_keys, F):
    """block: (L, R) 各 32 位元；round_keys: 子金鑰列表"""
    L, R = block
    for k in round_keys:
        L, R = R, L ^ F(R, k)          # 一輪：互換 + F + XOR
    return L, R

def feistel_decrypt(block, round_keys, F):
    L, R = block
    for k in reversed(round_keys):      # 反向跑輪
        R, L = L, R ^ F(L, k)          # 等等——解密要用同一結構反推
    return L, R

# 更清楚的解密：直接逆推每輪
def feistel_decrypt2(block, round_keys, F):
    L, R = block
    for k in reversed(round_keys):
        R, L = L, R                     # 逆互換
        R = L ^ F(R, k)                 # 逆 XOR：R = L_new ^ F(R_old, k)
    return L, R

def avalanche(F, block, k, flip_bit=0):
    """雪崩效應：翻轉一位元，數密文差異"""
    L, R = block
    L2, R2 = L ^ (1 << flip_bit), R
    c1 = feistel_encrypt((L, R), [k]*16, F)
    c2 = feistel_encrypt((L2, R2), [k]*16, F)
    diff = bin(c1[0] ^ c2[0]).count('1') + bin(c1[1] ^ c2[1]).count('1')
    return diff

import random
F = lambda x, k: ((x * 2654435761 + k * 40503) ^ (x >> 7)) & 0xFFFFFFFF
random.seed(42)
L, R = random.getrandbits(32), random.getrandbits(32)
print(f"翻轉一位元後密文差異位元數 = {avalanche(F, (L, R), 12345)}")
# 理想 ≈ 32（一半）：雪崩效應 ✓
```

### S-Box：混淆的實現
Lucifer 與 DES 的輪函數核心是 **S-Box**（代換盒）：$n$ 位元 → $m$ 位元的非線性查表。S-Box 的設計準則（後來由密碼分析反推）：

- **非線性**：與仿射函數的最大距離（抗線性分析）
- **差分均勻性**：$\max_{\Delta x, \Delta y} \#\{x : S(x \oplus \Delta x) = S(x) \oplus \Delta y\}$ 最小化（抗差分分析）

**偵探筆記**：Feistel 結構的推理是「結構性可逆」——用外層結構（互換 + XOR）保證可逆，內層函數（$F$、S-Box）專心混淆。**分工**：結構管可逆，函數管安全。這個模式與 Kerckhoffs 原則（見 `1883-Kerckhoffs原則.md`）同源：把複雜性放在該放的地方。

## 結案 -- 後果與影響
- **DES 誕生**：Lucifer 縮短版成為 1977 年的國家標準（見 `1977-DES.md`）。
- **Feistel 結構的帝國**：DES、3DES、Blowfish、Camellia、Khazad——數十年區塊密碼的主流範式（AES 例外，用 SPN 結構）。
- **密碼分析的催化**：DES 公開 15 年後，Biham–Shamir 的差分分析（1991）與 Matsui 的線性分析（1993）證明 S-Box 設計的科學性——NSA 早就知道。
- **S-Box 設計準則**：非線性、差分均勻性成為 SPN/Feistel 密碼的設計科學。
- **Feistel 的正名**：Lucifer 的「魔鬼」之名（Feistel 的幽默）——密碼學史上最被低估的工程師之一。

## 關鍵人物與文獻
- **Horst Feistel**（1915–1990）：IBM；Block Cipher Cryptographic System (1974 專利)、Feistel 結構
- **Tuchman & Meyer**：Lucifer 團隊
- **Biham & Shamir**：差分密碼分析 (1991)
- **Matsui**：線性密碼分析 (1993)
- 交叉參照：`1949-Shannon保密理論.md`、`1977-DES.md`、`2001-AES.md`
