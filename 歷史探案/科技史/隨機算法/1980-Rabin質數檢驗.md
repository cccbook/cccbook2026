# 1980 - Rabin 質數檢驗

## 案件摘要
1980 年，Michael O. Rabin 發表《Probabilistic Algorithm for Testing Primality》：把 Miller (1976) 的檢驗隨機化——**隨機選基底 $a$**，錯誤機率 $\le 4^{-k}$。這是歷史上第一個「隨機算法大幅超越已知確定性算法」的實用案例，確立了 BPP/RP 類的地位，也宣告了一個新範式：**允許極小機率出錯，換取指數級的加速**。

## 前因 -- 為什麼會有這個案子
Miller 的檢驗（見 `1976-Miller質數檢驗.md`）吊在 ERH 上：沒有 ERH，已知需要 $O(\sqrt{n})$ 試除。Rabin 的問題：**能否不依賴任何未證明假設？** 他的答案充滿智慧——不消除錯誤，而是**控制錯誤**：讓錯誤機率小到比硬體故障還低。

## 線索與推理 -- 數學式、程式、理論

### 關鍵定理：證人很多
**定理**：奇合數 $n$ 中，使 Miller 檢驗通過的「說謊者」$a \in \mathbb{Z}_n^*$ **至多佔 1/4**。

證明骨架（反證法，用到群論）：設說謊者集合太大，利用 $\mathbb{Z}_n^*$ 的子群結構——說謊者構成某個真子群的子集，而真子群大小至多為群的一半；對非循環群結構進一步分半，最終上界 1/4。（Rabin 的原始證明用了 $\mathbb{Z}_n^*$ 至少有 $\varphi(n)$ 個元素與根號鏈結構的組合計數。）

### Miller–Rabin 演算法
```
輸入：奇數 n；參數 k（安全參數）
重複 k 次：
    隨機選 a ∈ {2, ..., n-2}
    若 a 是合數性證人 => 回答「合數」（確定正確！）
回答「質數」
```

**誤差分析**（單邊錯誤，RP 風格）：
- 若 $n$ 是合數：每輪抓包機率 $\ge 3/4$，$k$ 輪全部漏掉機率 $\le (1/4)^k = 4^{-k}$
- 若 $n$ 是質數：**永遠答對**（無偽證）

$k = 40$ 時錯誤機率 $\le 4^{-40} \approx 10^{-24}$——比宇宙射線翻轉位元的機率還低。**這不是「可能錯」的算法，是「錯了比硬體壞掉還罕見」的算法。**

### 程式碼：完整的 Miller–Rabin

```python
import random

def is_probable_prime(n, k=40):
    if n < 2: return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:
        if n % p == 0: return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2; s += 1
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x in (1, n - 1): continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1: break
        else:
            return False            # 證人 => 確定是合數
    return True                     # 錯誤機率 <= 4^-k

random.seed(42)
# 產生 RSA 模數的實戰流程
p = random.getrandbits(512) | 1
while not is_probable_prime(p): p = random.getrandbits(512) | 1
print("找到 512 位質數", p % 1000, "...")

# Carmichael 數無所遁形
print(is_probable_prime(561))            # False（費馬檢驗會被騙！）
print(is_probable_prime(341550071728321))  # False（更大的 Carmichael 數）
```

### 複雜度類的意義
Miller–Rabin 屬於 co-RP：合數判定在 RP 中（一邊可能錯）。合成：

- COMPOSITE ∈ RP ∩ co-RP ⟹ ZPP（Las Vegas：總是對，期望多項式）
- PRIMES ∈ coRP ⟹ PRIMES ⊆ BPP

**1976–2002 的懸案**：PRIMES ∈ P 嗎？AKS (2002) 最終證明是——但 Miller–Rabin 仍是不二之選（快得多）。

**偵探筆記**：Rabin 的推理是「反守為攻」——Miller 試圖消除錯誤（依賴 ERH），Rabin 把錯誤當成資源**用機率放大器壓縮**。這個模式（隨機取樣 + 錯誤機率指數衰減）成為整個 Monte Carlo 算法的標準配置。

## 結案 -- 後果與影響
- **密碼學標配**：RSA、Diffie–Hellman、橢圓曲線的金鑰生成全用 Miller–Rabin；OpenSSL 每天跑幾億次。
- **BPP 類的確立**：隨機算法從「玩具」變成「工業標準」，隨機複雜度理論（RP、BPP、ZPP）有了殺手級應用。
- **去隨機化懸案**：PRIMES 被證明在 P（AKS, 2002），暗示 BPP 或許可去隨機化（見 `1997-ImpagliazzoWigderson去隨機化.md`）。
- **單邊/雙邊錯誤的區分**：Miller–Rabin（co-RP）成為複雜度類教學的標準例子。

## 關鍵人物與文獻
- **Michael O. Rabin**（1931–2025）：Probabilistic Algorithm for Testing Primality (1980, J. Number Theory)；圖靈獎 1976（與 Shamir，非確定性自動機）
- **Gary Miller**：1976 基礎檢驗
- **Solovay & Strassen**：1977 獨立提出機率質數檢驗（Euler 準則版本）
- 交叉參照：`1976-Miller質數檢驗.md`、`1981-Rabin指紋比對.md`、`../計算理論/2002-AKS質數檢驗.md`
