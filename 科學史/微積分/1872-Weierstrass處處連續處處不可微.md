# 1872 — Weierstrass 處處連續處處不可微

## 案件摘要
1872 年 1 月 18 日，Karl Weierstrass 在柏林科學院宣讀了一份報告，展示了一個讓整個數學界瞠目結舌的函數：

$$W(x) = \sum_{n=0}^{\infty} a^n \cos(b^n \pi x)$$

當 $0 < a < 1$、$b$ 為奇整數且 $ab > 1 + \frac{3\pi}{2}$ 時，這個函數**處處連續，卻處處不可微**——沒有一個點有切線。連續的曲線居然可以處處是「鋸齒中的鋸齒」，直覺與邏輯在此徹底決裂。這份報告是 ε-δ 嚴格化的加冕禮，也是「分析算術化」完成的標誌。

## 前因 -- 為什麼會有這個案子
- 18 世紀以來，數學家普遍相信：**連續函數除了少數孤立點外必可微**。Euler、Lagrange 甚至把「連續」與「可由解析式表示」混為一談；「連續曲線必有切線」被視為幾何常識。
- 1830 年代，Bolzano 已私下構造出處處連續處處不可微的函數（Bolzano 函數，以部分和的折線逼近），但手稿塵封數十年，未產生影響。
- Cauchy（1821）用極限定義連續與導數，但他的語言仍帶幾何直覺（「無限接近」「趨於」），且他一度錯誤地相信連續函數的極限函數仍連續（對不一致收斂不成立）。
- 案件的導火線：Riemann（1854）的病態可積函數已經讓數學界意識到函數可以病態，但「連續卻不可微」是更根本的挑戰——它攻擊的是微分學本身。Weierstrass 決定用最無可辯駁的方式結案：一個明確的公式、一個完整的證明。

## 線索與推理 -- 數學式、程式、理論

### 線索一：函數的構造——無窮疊加的高頻振盪
Weierstrass 取餘弦級數

$$W(x) = \sum_{n=0}^{\infty} a^n \cos(b^n \pi x), \qquad 0 < a < 1,\; b \text{ 奇整數},\; ab > 1 + \tfrac{3\pi}{2}$$

構造的邏輯像偵探佈局：第 $n$ 項 $\cos(b^n\pi x)$ 的頻率是 $b^n$——指數增長的高頻振盪，但振幅 $a^n$ 指數衰減。每一項都是光滑的（餘弦無限可微），**但無窮多個越來越細的鋸齒疊加在一起，在任何尺度上都留下新的折角**。

### 線索二：連續性的證明——一致收斂
連續性不難：因為 $|a^n \cos(b^n\pi x)| \le a^n$，而 $\sum a^n$ 收斂（幾何級數），由 Weierstrass M-判別法，級數**一致收斂**。連續函數的一致收斂極限仍連續——所以 $W$ 處處連續。這正是 Cauchy 當年缺的一致收斂概念，如今成為證明的第一塊基石。

### 線索三：不可微的證明——差商的爆炸
關鍵在於證明：對**任何**點 $x$，差商

$$\frac{W(x+h) - W(x)}{h}$$

在 $h \to 0$ 時不收斂。Weierstrass 的策略：取特定的 $h_m \to 0$（利用 $b$ 是奇整數、$b^m \pi x$ 的整數部分性質），使得每一項 $\cos(b^n \pi (x+h_m)) - \cos(b^n\pi x)$ 都與最高頻項**同號疊加**，於是

$$\left|\frac{W(x+h_m) - W(x)}{h_m}\right| \ge \sum_{n=0}^{m-1} a^n \cdot \frac{|\cos(b^n\pi(x+h_m)) - \cos(b^n\pi x)|}{|h_m|} \to \infty$$

條件 $ab > 1 + \frac{3\pi}{2}$ 保證低頻項貢獻的增長 $(ab)^m$ 壓過 $h_m$ 的縮小——差商爆炸，導數不存在。**每一項都光滑，極限卻處處無切線**：交換「無窮求和」與「求導」的直覺在此破產。

### 線索四：ε-δ 語言與分析算術化
Weierstrass 的深遠貢獻不在函數本身，而在證明所用的**語言**：他把「極限」徹底算術化——

$$\lim_{x \to x_0} f(x) = L \iff \forall \varepsilon > 0,\; \exists \delta > 0:\; 0 < |x - x_0| < \delta \implies |f(x) - L| < \varepsilon$$

「趨於」「無限接近」這些幾何手勢全部退位，只剩下量詞、不等式、實數的四則運算。連同「一致收斂」「一致連續」的 ε-δ 定義，分析學從幾何直覺的領域徹底遷移到算術的疆土——這就是「**分析算術化**」（arithmetization of analysis）。而支撐一切不等式的實數系，同年由 Dedekind（《Stetigkeit und irrationale Zahlen》）與 Cantor 的理論給出嚴格基礎——兩份 1872 年的案卷，是同一場革命的兩翼。

### 程式碼範例：Weierstrass 函數部分和的圖像
畫出 $W(x)$ 的部分和，觀察「放大後仍有鋸齒」的自相似病態：

```python
import numpy as np
import matplotlib.pyplot as plt

a, b = 0.5, 13          # ab = 6.5 > 1 + 3π/2 ≈ 5.712 ✓

def W_partial(x, N):
    """Weierstrass 函數的前 N 項部分和"""
    return sum(a**n * np.cos(b**n * np.pi * x) for n in range(N))

x = np.linspace(-1, 1, 4000)
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for ax, N in zip(axes, [5, 15, 30]):
    ax.plot(x, W_partial(x, N), lw=0.6, c="darkred")
    ax.set_title(f"W(x) 部分和, N = {N}")
plt.suptitle("Weierstrass 函數：項數越多，鋸齒越細 → 處處不可微")
plt.show()

# 數值驗證：對任意點，差商隨 h → 0 爆炸（不收斂）
for x0 in [0.0, 0.123, 0.5]:
    print(f"x0 = {x0}: ", end="")
    for N in [10, 20, 30]:
        hs = np.array([a**k * b**(-k) for k in range(2, N)])
        # 用步長 h = b^-k 級別的差商（高頻項主導）
        dq = [(W_partial(np.array([x0 + h]), N)[0] - W_partial(np.array([x0 - h]), N)[0])
              / (2*h) for h in hs]
        print(f"|dq| max ≈ {max(abs(d) for dq_val in [dq] for d in dq_val):8.1f}", end=" ")
    print()   # 差商不收斂且量級隨 N 增大 → 不可微
```

圖像顯示：部分和項數從 5 增到 30，曲線越來越「毛」——任何尺度放大都會出現新的折角。差商的量級隨 $N$ 增大而不穩定且爆炸，這正是「處處不可微」的數值證據。

## 結案 -- 後果與影響
- 「連續 ⟹ 幾乎處處可微」的百年信念被一份公式、一個證明徹底粉碎。Poincaré 嘆稱這是「對直覺的鞭打」；Hermite 承認「我懷著恐懼與驚駭遠離這個可憐的、沒有導數的函數的世界」。
- **ε-δ 語言成為分析學的標準**：極限、連續、導數、一致收斂全部算術化。今日所有微積分教科書的定義，都是 Weierstrass 的遺產。
- **分析算術化完成**：分析的基礎從幾何（曲線、面積）遷移到實數與自然數的算術。連同 Dedekind（1872）的實數理論、Cantor 的集合論，數學的嚴格化工程告一段落。
- 病態函數的時代來臨：Peano 曲線（1890，連續曲線填滿正方形）、Lebesgue 的不可積函數——怪物不再被恐懼，而是被研究。
- 對「無窮過程可隨意操作」的懷疑，孕育了 20 世紀初的直覺主義（Brouwer）與對數學基礎的重新審視。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Karl Weierstrass | 處處連續處處不可微函數、ε-δ 語言、分析算術化 |
| Bernard Bolzano | 1830 年代先行者，函數手稿塵封 |
| Augustin-Louis Cauchy | 極限理論奠基者，語言仍含糊 |
| David Hilbert / Henri Poincaré | 評論者與繼承者 |

- K. Weierstrass, 〈Über continuirliche Functionen eines reellen Arguments, die für keinen Werth des letzteren einen bestimmten Differentialquotienten besitzen〉, 柏林科學院宣讀 (1872 年 1 月 18 日)；刊於 *Mathematische Werke* **2**, 71–74。
- K. Weierstrass, *Einleitung in die Theorie der analytischen Functionen*（講義）：ε-δ 語言的系統化。
