# 1987 - Karp–Rabin 字串匹配

## 案件摘要
1987 年，Richard Karp 與 Michael Rabin 發表《Efficient Randomized Pattern-Matching Algorithms》：在長度 $n$ 的文字中找長度 $m$ 的模式，用**滾動雜湊（rolling hash）**實現期望 $O(n + m)$ 時間——比經典 KMP 的 $O(n+m)$ 更簡單，且能自然擴展到二維匹配與多模式匹配。這是 Rabin 指紋（1981，見 `1981-Rabin指紋比對.md`）的實用化，也是「隨機化換簡潔」的典範。

## 前因 -- 為什麼會有這個案子
子字串匹配的經典難題：樸素方法是 $O(nm)$（每個位置逐字比較）。1977 年 Knuth–Morris–Pratt 與 Boyer–Moore 已給出 $O(n+m)$ 確定性算法，但**前處理複雜、實作困難**。Karp–Rabin 的問題：**能否不預處理，用更簡單的方法達到線性時間？** 答案：用雜湊——把「字串相等」歸約為「指紋相等」。

## 線索與推理 -- 數學式、程式、理論

### 滾動雜湊
把長度 $m$ 的字串視為以 $b$ 為基底的數：

$$H(s) = \sum_{i=0}^{m-1} s_i \cdot b^{m-1-i} \bmod p$$

**關鍵技巧——滾動更新**：從窗口 $s[i..i+m]$ 移到 $s[i+1..i+m+1]$，$O(1)$ 步：

$$H_{i+1} = (H_i - s_i \cdot b^{m-1}) \cdot b + s_{i+m} \pmod p$$

（減去離開的頭字元、乘基底移位、加上進入的尾字元。）

**演算法**：算好模式的雜湊 $H(\text{pattern})$，掃描文字所有窗口的滾動雜湊，雜湊相等時**逐字驗證**（防偽陽性）或直接信任（允許極小錯誤率）：

$$P(\text{偽陽性}) \le \frac{n \cdot (m-1)}{p} \quad \text{（union bound over 根）}$$

選 $p \approx n \cdot m \cdot 2^{40}$，整個匹配的錯誤機率可壓到 $2^{-40}$。

### 複雜度
- 預處理：$O(m)$（模式雜湊）
- 掃描：$O(n)$ 次滾動更新 + 偽陽性驗證
- 期望總時間：$O(n + m)$（偽陽性極少，驗證成本可忽略）

### 程式碼：Karp–Rabin

```python
import random

def karp_rabin(text, pattern, p=2**61 - 1, b=256):
    n, m = len(text), len(pattern)
    # 模式雜湊
    hp = 0
    for ch in pattern:
        hp = (hp * b + ord(ch)) % p
    # 第一個窗口
    h = 0
    for ch in text[:m]:
        h = (h * b + ord(ch)) % p
    bm = pow(b, m - 1, p)             # b^(m-1) mod p，預算好
    matches = []
    for i in range(n - m + 1):
        if h == hp and text[i:i+m] == pattern:  # 指紋相等 + 驗證
            matches.append(i)
        if i + m < n:                 # 滾動更新：O(1)
            h = ((h - ord(text[i]) * bm) * b + ord(text[i+m])) % p
    return matches

random.seed(42)
text = "abcabcabd" * 1000
print(karp_rabin(text, "abcabd")[:5])   # [3, 9, 12, 18, 21] ...
```

### 二維擴展與多模式
Karp–Rabin 的真正威力在擴展性：

- **二維匹配**（$n \times n$ 文字找 $m \times m$ 模式）：每列滾動雜湊 + 每行滾動雜湊，$O(n^2 + nm)$——確定性二維算法極複雜，隨機化輕鬆解決。
- **多模式匹配**（同時找 $k$ 個模式）：把所有模式雜湊放雜湊表，掃描一次——$O(n + \sum m_i + \text{命中數})$。
- **抄襲偵測**：文件比對（MOSS 系統）用 Karp–Rabin 找共同子字串。

### 錯誤控制 vs 驗證的選擇
兩種模式：
1. **Las Vegas**：雜湊相等時逐字驗證（總是對，最壞情況時間隨機）
2. **Monte Carlo**：信任指紋（時間固定，錯誤 $\le (nm/p)$）

**偵探筆記**：Karp–Rabin 的推理是「降維歸約」——字串匹配（大問題）歸約為整數比較（小問題），用 Rabin 指紋的根上界保證可靠性。**簡潔性的勝利**：KMP 的失敗函數 vs Karp–Rabin 的一行滾動更新——隨機化常常買到的不只是速度，還有優雅。

## 結案 -- 後果與影響
- **抄襲偵測**：Stanford MOSS 系統（Schleimer–Wilkersom–Aiken 2003 的 winnowing 建立在 Karp–Rabin 上）。
- **內容定址儲存**：rsync 的 rolling checksum、云儲存去重（content-defined chunking）。
- **雜湊表實務**：隨機化雜湊（universal hashing，Carter–Wegman 1979）成為對抗最壞情況輸入的標準。
- **字串匹配教科書**：Karp–Rabin 與 KMP、Boyer–Moore 並列三大經典；CLRS 教科書的標準章節。
- **生物資訊**：基因序列比對的初步篩選。

## 關鍵人物與文獻
- **Richard Karp**（1935–）：圖靈獎 1985（NP 完備理論）；Karp–Rabin 匹配
- **Michael O. Rabin**（1931–2025）：指紋比對、質數檢驗
- Karp & Rabin: Efficient Randomized Pattern-Matching Algorithms (1987, IBM J. Res. Dev.)
- **Carter & Wegman**：Universal hashing (1979)
- 交叉參照：`1981-Rabin指紋比對.md`、`1980-Rabin質數檢驗.md`、`1997-BroderMinHash.md`
