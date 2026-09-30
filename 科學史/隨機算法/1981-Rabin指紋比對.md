# 1981 - Rabin 指紋比對

## 案件摘要
1981 年，Michael Rabin 發表《Fingerprinting by Random Polynomials》：要比對兩個巨大的檔案（如上億字元）是否相同，不必傳輸整個檔案——**隨機選一個多項式，把檔案當多項式求值，只比對「指紋」**。出錯機率可壓到任意小。這是「隨機化歸約」的典範：把大物件的相等問題歸約為小物件的相等問題，用隨機化保證可靠性。

## 前因 -- 為什麼會有這個案子
Rabin 在訪問時遇到實際問題：電腦間要比對資料庫副本是否一致，傳輸整個檔案太貴。確定性方法（固定雜湊如 CRC）有個致命弱點：**敵人可以構造碰撞**。Rabin 的洞察：**隨機化**——敵人不知道你選哪個多項式，就無法構造碰撞。

## 線索與推理 -- 數學式、程式、理論

### 多項式指紋
把長度 $n$ 的字串 $s = s_0 s_1 \dots s_{n-1}$ 視為多項式係數：

$$S(x) = s_0 + s_1 x + s_2 x^2 + \dots + s_{n-1} x^{n-1}$$

隨機選質數 $p$（或隨機點 $x_0 \in \mathbb{Z}_p$），指紋為：

$$F_p(s) = S(x_0) \bmod p$$

**兩字串相等 ⟹ 指紋相等**（確定）。指紋相等但字串不同（假陽性）當且僅當：

$$D(x) = S(x) - T(x) \ne 0 \text{ 但 } D(x_0) \equiv 0 \pmod p$$

即 $x_0$ 是非零多項式 $D$ 的根。$D$ 至多 $n-1$ 個根（代數基本定理），$\mathbb{Z}_p$ 有 $p$ 個元素：

$$P(\text{假陽性}) \le \frac{n-1}{p}$$

**單邊錯誤 + 可放大**：用大質數 $p \approx 2^{60}$，百億字元檔案的碰撞機率 $\approx 10^{-8}$；或者比對 $k$ 個獨立指紋，錯誤 $\le (n/p)^k$ 指數衰減。

### 程式碼：Rabin 指紋

```python
import random

def rabin_fingerprint(s, p=None):
    if p is None:
        p = random.choice([2**61 - 1, 2**31 - 1, 10**18 + 9])  # 大質數
    x = random.randrange(2, p)
    h = 0
    for ch in s.encode():
        h = (h * x + ch) % p        # Horner 法：O(n) 次模乘
    return h, p

random.seed(42)
f1, p = rabin_fingerprint("hello world" * 1000000)   # 1100 萬字元
f2, _ = rabin_fingerprint("hello world" * 1000000, p)
print(f1 == f2)   # True

# 攻擊者無法構造碰撞（除非預測到隨機的 p 與 x）
```

### Karp–Rabin 滾動雜湊的伏筆
指紋的下一步是**滾動更新**：字串 $s[i..i+m]$ 的指紋移到 $s[i+1..i+m+1]$，只需 $O(1)$ 步：

$$F_{i+1} = (F_i - s_i x^{m-1}) \cdot x + s_{i+m} \pmod p$$

（以 $x$ 為底的移位。详见 `1987-KarpRabin字串匹配.md`。）

### 更廣的框架：Schwartz–Zippel 引理
Rabin 指紋是一般原理的特例——**Schwartz–Zippel 引理**（1979/1980）：

**定理**：域 $F$ 上 $d$ 次非零 $n$ 元多項式 $P$，在 $S^n$ 中隨機取點：

$$P(P(x_1, \dots, x_n) = 0) \le \frac{d}{|S|}$$

**應用**：多項式恆等式測試（PIT）——判定兩個多項式是否恆等，隨機取點求值即可。這成為互動式證明、PCP 定理（見 `../計算理論/1990-PCP定理.md`）的基礎工具。矩陣恆等式（如驗證 $AB = C$）也可以隨機化：選隨機向量 $v$，驗證 $ABv = Cv$，$O(n^2)$ 而非 $O(n^3)$（Freivalds 演算法，1979）。

**偵探筆記**：Rabin 指紋的推理鏈：大物件相等 → 多項式表示 → 隨機點求值 → 根的數量上界。**「非零多項式的根很少」** 這個代數事實成為隨機化的免費午餐——多項式世界給隨機算法的禮物。

## 結案 -- 後果與影響
- **Karp–Rabin 字串匹配**（1987）：滾動雜湊使子字串匹配 $O(n+m)$ 期望時間（見 `1987-KarpRabin字串匹配.md`）。
- **Freivalds 演算法**（1979）：矩陣乘法驗證 $O(n^2)$——隨機化驗證優於計算。
- **Schwartz–Zippel 引理**：多項式恆等式測試成為代數複雜度、PCP、互動式證明的基石。
- **資料去重與同步**：rsync、內容定址儲存（content-defined chunking）都源於 Rabin 指紋。
- **隨機化歸約的典範**：把難問題歸約為「隨機點求值」，這個模式貫穿現代隨機算法。

## 關鍵人物與文獻
- **Michael O. Rabin**（1931–2025）：Fingerprinting by Random Polynomials (1981, Harvard TR)
- **Schwartz / Zippel**：多項式零點引理 (1979/1980)
- **Freivalds**：矩陣驗證演算法 (1979)
- 交叉參照：`1980-Rabin質數檢驗.md`、`1987-KarpRabin字串匹配.md`、`../計算理論/1990-PCP定理.md`
