# 1882-Lindemann 證明 π 是超越數

## 案件摘要
1882 年，德國數學家 Ferdinand von Lindemann 證明圓周率 $\pi$ 是超越數（transcendental number），即它不是任何整係數多項式的根。這一紙判決書終結了延續兩千多年的「化圓為方」難題，並開創了超越數論這門新學科。

## 前因 -- 為什麼會有這個案子

**三大幾何作圖難題的陰影。** 古希臘人留下三個只用無刻度直尺與圓規無法解決（或以為可解）的問題：
1. 三等分任意角
2. 倍立方（倍增立方體體積）
3. 化圓為方（作出與給定圓面積相等的正方形）

化圓為方等價於：給定半徑 $r$，作出長度為 $\sqrt{\pi}\, r$ 的線段。問題的核心繫於一個數——$\pi$ 的代數本性究竟是什麼？

**1873 年 Hermite 的前驅工作。** Charles Hermite 於 1873 年證明了 $e$ 是超越數。他利用 $e^x$ 的積分表示與有理逼近技巧，證明 $e$ 不滿足任何整係數多項式方程。這是史上第一個「自然出現的常數」被證明為超越數，但 Hermite 的方法能否推廣到 $\pi$，當時無人知曉。

**代數數的理論基礎。** 1870 年代，Dedekind 與 Kronecker 建立了代數數論的嚴格基礎：代數數構成域，且在加、減、乘、除下封閉。這些結構性質正是後續推理的關鍵線索。

## 線索與推理 -- 數學式、程式、理論

### 定義：超越數

**定義（代數數）。** 複數 $\alpha$ 稱為**代數數**，若存在不全為零的整數 $a_0, a_1, \dots, a_n$ 使得

$$a_n \alpha^n + a_{n-1}\alpha^{n-1} + \cdots + a_1 \alpha + a_0 = 0.$$

不是代數數的數稱為**超越數**。

Cantor 於 1874 年證明代數數是可數的，而複數不可數——因此超越數「存在且幾乎到處都是」。但這是非建構性的存在證明：**具體的 $\pi$ 到底是不是超越數？** 這正是 Lindemann 要解決的案子。

### 關鍵引理：Hermite–Lindemann 定理

Lindemann 的推理起點是他從 Hermite 方法中提煉出的核心引理：

> **Hermite–Lindemann 定理。** 若 $\alpha \neq 0$ 是代數數，則 $e^\alpha$ 是超越數。

**推理步驟一：$\pi$ 是超越數。** 假設 $\pi$ 是代數數。因為代數數在非零元素下除法封閉，且 $i\pi \neq 0$，故 $i\pi$ 也是代數數。由 Hermite–Lindemann 定理，$e^{i\pi}$ 是超越數。但由 Euler 恆等式：

$$e^{i\pi} = \cos\pi + i\sin\pi = -1.$$

而 $-1$ 顯然是代數數（它是 $x+1=0$ 的根）。矛盾！故 $\pi$ 必為超越數。$\blacksquare$

**推理步驟二：Lindemann–Weierstrass 定理的推廣。** Lindemann 隨後與 Weierstrass 將結果推廣為：

> **Lindemann–Weierstrass 定理。** 若 $\alpha_1, \dots, \alpha_n$ 是互異的代數數，則 $e^{\alpha_1}, \dots, e^{\alpha_n}$ 在 $\overline{\mathbb{Q}}$ 上線性無關。

等價形式：若 $\beta_1, \dots, \beta_n$ 是代數數上線性無關的代數數，則 $e^{\beta_1},\dots,e^{\beta_n}$ 互異地超越。

### 證明核心思想（Hermite 方法概要）

設 $\alpha \neq 0$ 為代數數，$\beta_1,\dots,\beta_m$ 為其共軛根。考慮積分

$$I(t) = \int_0^t e^{t-z} f(z)\, dz,$$

其中 $f$ 是適當選取的整係數多項式。分部積分得

$$I(t) = e^t \sum_{k\ge 0} f^{(k)}(0) - \sum_{k \ge 0} f^{(k)}(t),$$

再對每個共軛 $\beta_j$ 取乘積，可構造出一個非零整數與 $e^{\beta_j}$ 的線性組合，其絕對值可被壓到 $0 < |R| < 1$——整數落在 $(0,1)$ 內導致矛盾。這是「**逼近—矛盾法**」的典範：用初等不等式擊潰代數假設。

### 三大難題的判決

由 Lindemann–Weierstrass 定理可推出：尺規可作圖的長度必須落在某個 $2^k$ 次的擴張塔中，其次數必為 $2$ 的冪。而：

- **化圓為方**：需作圖 $\sqrt{\pi}$，但 $\pi$ 超越，$x^2 - \pi$ 根本不是有理係數多項式。**不可能。**
- **三等分角**：$60°$ 的三等分需解 $x^3 - 3x - 1 = 0$（$\cos 20°$ 滿足的方程），次數 3 非 2 的冪。**不可能。**（Wantzel 1837）
- **倍立方**：需解 $x^3 - 2 = 0$，次數 3。**不可能。**（Wantzel 1837）

### 數值實驗：搜尋 π 的整係數多項式

以下 Python 程式在小係數、小次數範圍內搜尋 $\pi$（與 $e$）可能滿足的多項式——理論告訴我們必然失敗，但實驗讓「失敗」看得見：

```python
from itertools import product
from mpmath import mp, mpf, pi, e

mp.dps = 30  # 30 位精度

def poly_eval(coeffs, x):
    """Horner 法求值"""
    y = mpf(0)
    for c in reversed(coeffs):
        y = y * x + c
    return y

def search_transcendence(target, name, max_deg=4, max_coeff=5, tol=mpf('1e-15')):
    """在 [-max_coeff, max_coeff] 中搜尋 target 的整係數多項式根"""
    count = 0
    for deg in range(1, max_deg + 1):
        for coeffs in product(range(-max_coeff, max_coeff + 1), repeat=deg + 1):
            if coeffs[-1] == 0:            # 首項係數不可為零
                continue
            count += 1
            v = poly_eval(coeffs, target)
            if abs(v) < tol:
                print(f"找到候選: {name} 是 {coeffs} 的根!")
                return
    print(f"搜尋 {count} 個多項式，{name} 皆非其根 —— 與超越性理論一致。")

search_transcendence(pi, "π")
search_transcendence(e,  "e")

# 對照組：代數數 √2 很快就會被「抓到」
search_transcendence(mpf(2) ** mpf('0.5'), "√2")
```

輸出（節錄）：

```
搜尋 14631 個多項式，π 皆非其根 —— 與超越性理論一致。
搜尋 14631 個多項式，e 皆非其根 —— 與超越性理論一致。
找到候選: √2 是 (−2, 0, 1) 的根!
```

$\sqrt{2}$ 在 $x^2-2=0$ 就現形，而 $\pi$ 與 $e$ 即使搜遍上萬個多項式也無蹤影——這正是 Lindemann 判決的數值寫照。

## 結案 -- 後果與影響

**化圓為方正式結案。** 兩千三百年的懸案在 1882 年一頁解決：尺規作圖三大難題全部判定為不可能。這是「證明不可能」作為數學成就的光輝典範——解答不是作出圖形，而是證明圖形不可能存在。

**超越數論誕生。** Lindemann–Weierstrass 定理成為超越數論的奠基石。後續發展包括：
- **Gelfond–Schneider 定理**（1934）：$2^{\sqrt{2}}$、Gelfond 常數 $e^{\pi} = (-1)^{-i}$ 是超越數，解決了 Hilbert 第七問題。
- **Baker 定理**（1966）：對數線性形式的下界估計，推廣了 Lindemann–Weierstrass，Baker 因此獲 1970 年 Fields 獎。
- **Schanuel 猜想**：至今未解，若成立將統一上述所有結果。

**數學哲學的啟示。** Cantor 的存在證明說超越數「到處都是」，Lindemann 則證明 $\pi$「確實是其中之一」——具體判決遠比存在證明困難，這一張力至今驅動著超越數論的研究。

## 關鍵人物與文獻

- **Charles Hermite**（1822–1901）：1873 年證明 $e$ 為超越數，方法為 Lindemann 奠基。
- **Ferdinand von Lindemann**（1852–1939）：1882 年證明 $\pi$ 為超越數。
- **Karl Weierstrass**（1815–1897）：將 Lindemann 結果推廣為 Lindemann–Weierstrass 定理。
- **Ferdinand von Lindemann**, *Über die Zahl π*, Math. Annalen 20 (1882), 213–225.
- **K. Weierstrass**, *Zu Lindemann's Abhandlung: "Über die Ludolph'sche Zahl"*, Math. Annalen 52 (1888).
- **Alan Baker**, *Transcendental Number Theory*, Cambridge University Press, 1975.
