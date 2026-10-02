# 1910-Steinitz 域論

## 案件摘要
1910 年，德國數學家 Ernst Steinitz 發表論文《Algebraische Theorie der Körper》（域的代數理論），首次將「域」這個對象系統化地分類。這篇被譽為「抽象代數誕生標誌之一」的著作，讓域論從零散的計算技巧，變成一座結構分明的邏輯大廈。

## 前因 -- 為什麼會有這個案子
- **Galois（1832）與 Abel（1824）** 已用「根的置換群」解開五次方程無根式解之謎，但他們的「域」只是隱含在計算中，沒有獨立地位。
- **Dedekind（1871）** 在數論中提出「體（Körper）」的概念雛形，Kronecker 也用「添加根」的方式構造擴張。
- 19 世紀末，數學家手上已有許多域的例子：$\mathbb{Q}$、$\mathbb{R}$、$\mathbb{C}$、有限域 $\mathbb{F}_p$（Galois 早已研究 $\mathbb{F}_{p^n}$）、函數域 $\mathbb{C}(t)$，但**沒有人問：這些域到底能分成哪幾類？擴張有幾種？什麼時候擴張「長得一樣」？**
- Steinitz 的偵探問題：**「給定一個域 $K$，它的所有擴張由什麼不變量完全決定？」**

## 線索與推理 -- 數學式、程式、理論

### 線索一：素域 —— 所有域的「起點指紋」
任何域 $K$ 都包含一個最小的子域，稱為**素域**。由特徵決定：

$$\mathrm{char}(K) = \min\{ n \geq 1 : n \cdot 1 = 0 \}$$

- 若 $\mathrm{char}(K) = p$（質數），素域 $\cong \mathbb{F}_p$；
- 若 $\mathrm{char}(K) = 0$，素域 $\cong \mathbb{Q}$。

這給出第一張分類樹：

```
域 K
├── char = 0（素域 ℚ）
│   ├── 代數擴張：ℚ̄、代數數域、分圓域
│   └── 超越擴張：ℝ、ℂ、ℚ(t)、函數域
└── char = p（素域 𝔽_p）
    ├── 有限域：𝔽_{p^n}（唯一，見線索四）
    └── 無限域：𝔽_p(t)
```

### 線索二：超越基 —— 域的「維度座標」
Steinitz 仿照線性代數的基底概念，定義**超越基**：一組代數獨立的元素 $S \subseteq K$，使得 $K$ 在 $\mathrm{Frac}(F(S))$ 上是代數擴張。

$$\text{tr.deg}(K/F) = |S|$$

**交換定理（Exchange Theorem）**：任意兩個超越基的基數相同 —— 就像線性代數中基底大小唯一。於是 $\mathbb{R}/\mathbb{Q}$ 有超越度 $2^{\aleph_0}$，$\mathbb{C}(t)/\mathbb{C}$ 有超越度 $1$。任何擴張可拆成兩段：

$$F \xrightarrow{\text{純超越}} F(S) \xrightarrow{\text{代數}} K$$

### 線索三：可分擴張與正規擴張 —— 擴張的「兩個品質標章」
- **可分（separable）**：極小多項式無重根，即 $f'(a) \neq 0$。特徵 0 時永遠可分；特徵 $p$ 時可能出現「不可分」的怪獸 $x^p - t$（在 $\mathbb{F}_p(t)$ 上）。
- **正規（normal）**：擴張中任何不可約多項式若有一根在 $K$ 內，則所有根都在 $K$ 內 —— 擴張對共軛「封閉」。
- **Galois 擴張 = 可分 + 正規**，此時 $|\mathrm{Gal}(K/F)| = [K:F]$，Galois 理論的核心對應才有完整基礎：

$$\{ \text{中間域} \} \longleftrightarrow \{ \text{子群} \}, \quad E \mapsto \mathrm{Gal}(K/E)$$

Steinitz 並證明：**任何代數擴張都有唯一（在同構意義下）的代數閉包 $\bar{K}$**，且可分擴張可嵌入正規閉包 $K^{gal}$。

### 線索四：有限域分類 —— 完全破案
Steinitz 給出有限域的完整分類（補全 Galois 1830 年代的結果）：

$$\text{有限域存在且唯一} \iff q = p^n,\quad \mathbb{F}_{p^n} \cong \mathbb{F}_p[x]/(f),\ f \text{ 為 } n \text{ 次不可約多項式}$$

$\mathbb{F}_{p^n}^\times$ 是 $p^n - 1$ 階循環群（存在本原元素 $\alpha$）。乘法規則由 $x^{p^n} = x$ 主宰。

### 程式碼：Python 實作 $\mathbb{F}_{256}$（AES 的算術心臟）
AES 用 $\mathbb{F}_{2^8} = \mathbb{F}_2[x]/(x^8+x^4+x^3+x+1)$，乘法就是多項式乘法對不可約多項式取模：

```python
# 𝔽_256 = 𝔽_2[x] / (x^8 + x^4 + x^3 + x + 1)，AES 的 Rijndael 域
IRRED = 0x11B  # x^8 + x^4 + x^3 + x + 1

def gf256_add(a, b):          # 特徵 2：加法 = 減法 = XOR
    return a ^ b

def gf256_mul(a, b):          # 乘法 = 進位乘 + 模約簡
    p = 0
    while b:
        if b & 1:
            p ^= a
        b >>= 1
        a <<= 1
        if a & 0x100:         # x^8 項出現，用不可約多項式約簡
            a ^= IRRED
    return p

def gf256_pow(a, n):          # 費馬小定理：a^255 = 1（對非零 a）
    r = 1
    while n:
        if n & 1:
            r = gf256_mul(r, a)
        a = gf256_mul(a, a)
        n >>= 1
    return r

def gf256_inv(a):             # 逆元 = a^254（或用擴展歐幾里得）
    return gf256_pow(a, 254)

# 驗證：0x57 * 0x83 = 0xC1（AES 規格書中的例子）
assert gf256_mul(0x57, 0x83) == 0xC1
assert gf256_mul(0x57, gf256_inv(0x57)) == 1
print("𝔽_256 算術驗證通過：Steinitz 的理論在 AES 中活著")
```

## 結案 -- 後果與影響
- **抽象代數的憲法**：Steinitz 論文被譽為「數學史上第一篇真正意義上的抽象代數論文」，影響了 Noether、Artin 建立現代抽象代數（見 1920s-Noether 交叉參照）。
- **Galois 理論現代化**：Artin（1930s）用線性代數重寫 Galois 理論，正是站在 Steinitz 的可分/正規分類之上。
- **代數幾何與數論**：超越度、正則擴張成為代數曲線、代數數域的基本語言；Weil 猜想、p-adic 理論皆賴此基礎。
- **密碼學的意外豐收**：AES（2001，Rijndael）的 S-盒與 MixColumns 完全建構在 $\mathbb{F}_{2^8}$ 上；橢圓曲線密碼學（ECC）建構在 $\mathbb{F}_p$、$\mathbb{F}_{2^m}$ 上。一百年前的純理論，成為每天數十億次加密運算的引擎。

## 關鍵人物與文獻
- **Ernst Steinitz（1871–1928）**：德國數學家，布雷斯勞大學教授。終身發表論文極少，但 1910 年這一篇就足以不朽。
- E. Steinitz, *Algebraische Theorie der Körper*, J. reine angew. Math. 137 (1910), 167–309。（英譯重刊：Chelsea, 1950）
- 相關文獻：Galois, *Écrits mathématiques*（1832）；E. Artin, *Galois Theory*（1942）；N. Jacobson, *Basic Algebra I*（1985）。
