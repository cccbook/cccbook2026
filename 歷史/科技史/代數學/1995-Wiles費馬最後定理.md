# 1994/1995 - Wiles 費馬最後定理

## 案件摘要
1637 年 Fermat 在頁邊寫下「我有一個絕妙的證明，可惜這裡空白太小寫不下」，留下 $x^n + y^n = z^n$ 對 $n \geq 3$ 無正整數解的 358 年懸案。1994 年 9 月 Andrew Wiles 補上最後一塊拼圖，1995 年論文發表於 Annals of Mathematics，本案結案——但證明的附帶效應（模性定理）開啟了新紀元。

## 前因 -- 為什麼會有這個案子
- **1637 年**：Fermat 在 Diophantus《算術》頁邊寫下命題，去世後由其子整理出版。$n=4$ 由 Fermat 自己（無窮遞降法）解決，$n=3$ 由 Euler（1753），$n=5$ 由 Dirichlet 與 Legendre（1825），$n=7$ 由 Lamé（1839）——但一般情形始終無解。
- **Kummer 理論**（1847）：在分圓域 $\mathbb{Q}(\zeta_n)$ 中嘗試分解 $x^n + y^n$，遭遇非唯一因子分解；理想類數與正則質數 $p$（$p \nmid h_{\mathbb{Q}(\zeta_p)}$）處理了大量 $n$，卻無法窮盡。
- **現代轉折**：1984 年 Frey 提出：若 $a^n + b^n = c^n$ 有解，則橢圓曲線
  $$y^2 = x(x - a^n)(x + b^n)$$
  （Frey 曲線）會是「病態」的——Ribet（1986）證明它違反 **Taniyama–Shimura 猜想**（半穩定情形）。於是：證明半穩定橢圓曲線的模性 $\Rightarrow$ FLT 成立。
- **Wiles 的計畫**：1986 年起，在普林斯頓閣樓上秘密工作七年，目標是 Taniyama–Shimura 的半穩定情形，路線是 Galois 表示的形變理論。

## 線索與推理 -- 數學式、程式、理論

### 1. 命題
**費馬最後定理（FLT）**：對 $n \geq 3$，

$$x^n + y^n = z^n \quad \text{無正整數解}$$

只需考慮 $n$ 為質數 $p \geq 3$（若 $n = km$，則 $(x^k)^m + (y^k)^m = (z^k)^m$ 歸約到質數指數；$n=4$ 已由 Fermat 解決）。

### 2. 橢圓曲線 ↔ 模形式：Taniyama–Shimura 猜想
橢圓曲線 $E/\mathbb{Q}$：

$$E: y^2 = x^3 + ax + b, \qquad \Delta = -16(4a^3 + 27b^2) \neq 0$$

**Taniyama–Shimura（模性）猜想**：每條有理橢圓曲線都是模的——存在權 2、級 $N$ 的新形式（newform）

$$f(q) = \sum_{n \geq 1} a_n q^n = q + \sum_{n \geq 2} a_n q^n \in S_2(\Gamma_0(N))$$

使得對幾乎所有質數 $p$：

$$a_p = p + 1 - \#E(\mathbb{F}_p)$$

幾何對象（橢圓曲線）與分析對象（模形式）被 Galois 表示縫合：模形式給出 Galois 表示

$$\rho_{f, \ell} : G_{\mathbb{Q}} \to GL_2(\mathbb{Z}_\ell)$$

而橢圓曲線給出 $\rho_{E, \ell} : G_{\mathbb{Q}} \to GL_2(\mathbb{Z}_\ell)$（作用在 $\ell$-進 Tate 模 $T_\ell(E)$ 上）。猜想即：$\rho_{E,\ell} \sim \rho_{f,\ell}$。

### 3. Wiles 的武器：形變理論與 $R = \mathbb{T}$
**形變問題**：固定 mod $\ell$ 的表示 $\bar{\rho} : G_{\mathbb{Q}} \to GL_2(\mathbb{F}_\ell)$，問它能否提升（lift）到特徵 $\ell$ 的表示 $\rho : G_{\mathbb{Q}} \to GL_2(\mathbb{Z}_\ell)$？Mazur 的形變理論說：所有形變由萬有形變環 $R$ 參數化：

$$\text{Def}(\bar{\rho}) \cong \text{Hom}(R, \mathbb{Z}_\ell\text{-代數})$$

**Hecke 代數** $\mathbb{T}$：級 $N$、權 2 的模形式在 Hecke 算符作用下生成的代數，編碼「哪些 mod $\ell$ 表示可被模形式提升」。

Wiles 的策略：
1. 選 $\bar{\rho}_{E,3}$（mod 3 的 Galois 表示），用 Langlands–Tunnell 定理證明它是模的（因 $GL_2(\mathbb{F}_3)$ 可解）；
2. 證明：若 $\bar{\rho}$ 是模的且局部條件良好，則 $\bar{\rho}$ 的形變環 $R$ 等於 Hecke 代數 $\mathbb{T}$：

   $$\boxed{R \cong \mathbb{T}}$$

3. 由 $R = \mathbb{T}$ 推出每條半穩定橢圓曲線都模。
4. Ribet + 模性 $\Rightarrow$ Frey 曲線不存在 $\Rightarrow$ FLT。

技術核心是**岩澤理論（Iwasawa theory）與完全交（complete intersection）**：Wiles 用 CM 情形的岩澤主猜想證明 $\mathbb{T}$ 的某個映射是滿射，再用「Rolling idée」處理剩餘情形。

### 4. 1993 宣告與漏洞
- **1993 年 6 月 23 日**，劍橋 Newton 研究所，Wiles 以「Modular Forms, Elliptic Curves and Galois Representations」為題作三場演講，結尾宣稱證明 FLT。全球頭條。
- **審稿中發現漏洞**：第 3 章「歐拉系（Euler system）」的關鍵引理在半穩定非一般情形的估值不夠精確——計算中出現 gap。
- **14 個月的絕境**後，1994 年 9 月 19 日，Wiles 與學生 **Richard Taylor** 合作，放棄 Euler system 路線，改用 **3-5 切換（3-5 switch）**：在形變問題上於 $\ell = 3$ 與 $\ell = 5$ 之間切換，用 $\bar{\rho}_{E,5}$ 的形變性質補上證明。

```python
# Python 演示：橢圓曲線 y^2 = x^3 + ax + b 的點運算（有限域上）
# 這是 Wiles 證明中計算 #E(F_p) 的離散原型

def ec_add(P, Q, a, p):
    """有限域 F_p 上橢圓曲線點加法 y^2 = x^3 + ax + b"""
    if P is None: return Q
    if Q is None: return P
    x1, y1 = P; x2, y2 = Q
    if x1 == x2 and (y1 + y2) % p == 0:
        return None                      # 無窮遠點 O
    if P == Q:
        if y1 == 0: return None
        m = (3*x1*x1 + a) * pow(2*y1, -1, p) % p   # 切線斜率
    else:
        m = (y2 - y1) * pow(x2 - x1, -1, p) % p    # 割線斜率
    x3 = (m*m - x1 - x2) % p
    y3 = (m*(x1 - x3) - y1) % p
    return (x3, y3)

def ec_mul(k, P, a, p):
    """純量乘法 k*P（橢圓曲線上的 Galois 模擬）"""
    R, Q = None, P
    while k:
        if k & 1: R = ec_add(R, Q, a, p)
        Q = ec_add(Q, Q, a, p)
        k >>= 1
    return R

def count_points(a, b, p):
    """Hasse 定理範圍內計數 #E(F_p)，驗證 |#E - (p+1)| <= 2*sqrt(p)"""
    N = 1  # 含無窮遠點
    for x in range(p):
        rhs = (x**3 + a*x + b) % p
        N += 1 if pow(rhs, (p-1)//2, p) in (0, 1) else 0
        if rhs != 0:
            N += 1 if pow(rhs, (p-1)//2, p) == 1 else 0
    return N

# 示範：a=1, b=0 在 F_11 上
p = 11
N = count_points(1, 0, p)
import math
print(f"#E(F_{p}) = {N}, p+1 = {p+1}, Hasse 界 ±{2*math.isqrt(p)}")
# 驗證 Hasse：|N - (p+1)| <= 2*sqrt(p)
assert abs(N - (p+1)) <= 2*math.sqrt(p)
print("Hasse 定理驗證通過")
```

### 5. 1995 年 Annals 論文
- **1995 年 5 月**，Annals of Mathematics 141 卷刊出兩篇：
  - Wiles, *Modular elliptic curves and Fermat's Last Theorem*（108 頁，含完整證明）；
  - Taylor & Wiles, *Ring-theoretic properties of certain Hecke algebras*（填補 3-5 切換的細節）。
- 審稿人（包括 Katz、Faltings）經數月逐行驗證後確認正確。

## 結案 -- 後果與影響
- **358 年懸案結案**：$x^n + y^n = z^n$ 對 $n \geq 3$ 無正整數解，正式成為定理。
- **模性定理**：Wiles 實際證明的是半穩定橢圓曲線的模性；2001 年 Breuil–Conrad–Diamond–Taylor 補完一般情形（稱為 **Modularity Theorem** 或 Taniyama–Shimura–Weil 定理）。
- **開啟新紀元**：
  - **Fermat–Catalan 猜想**、**abc 猜想**、**BSD 猜想**的研究方法全部升級；
  - **形變理論 + $R = \mathbb{T}$** 成為處理 Galois 表示模性的標準工具，直接鋪向 **Langlands 綱領**的算術面；
  - 2016 年 Scholze 等人的 **perfectoid 空間**繼續推進 $p$-進表示的模性。
- **文化影響**：Wiles 獲 2016 Abel 獎（Fields Medal 因超齡未頒），FLT 成為「數學的聖杯」被攻克的象徵，也是抽象理論（Galois 表示、形變、岩澤理論）戰勝初等技巧的典範。

## 關鍵人物與文獻
- **Pierre de Fermat**（1607–1665）：1637 年頁邊筆記。
- **Andrew Wiles**（1953–）：1995 證明，2016 Abel 獎。
- **Richard Taylor**（1962–）：3-5 切換合作者。
- **Goro Frey、Ken Ribet**：Frey 曲線與 Ribet 定理。
- **Barry Mazur**：形變理論。
- **主要文獻**：
  - Wiles, *Modular elliptic curves and Fermat's Last Theorem*, Ann. of Math. 141 (1995), 443–551.
  - Taylor & Wiles, *Ring-theoretic properties of certain Hecke algebras*, Ann. of Math. 141 (1995), 553–572.
  - Ribet, *On modular representations of Gal(Q̄/Q) arising from modular forms*, Invent. Math. 100 (1990).
  - Darmon, Diamond & Taylor, *Fermat's Last Theorem*, 1995（綜述）。
  - Singh, *Fermat's Enigma*, 1997（科普）。
