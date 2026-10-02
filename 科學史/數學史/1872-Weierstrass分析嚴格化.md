# 1872 - Weierstrass 分析嚴格化

## 案件摘要
1870 年代，Karl Weierstrass 在柏林大學的講座把**分析學徹底嚴格化**：$\epsilon$-$\delta$ 語言、一致收斂、以及 1872 年的**處處連續處處不可微函數**：

$$f(x) = \sum_{n=0}^{\infty} a^n \cos(b^n \pi x)$$

**連續的函數可以「處處不光滑」**——直覺的崩塌！**直覺與嚴格的分離**——分析學從牛頓的「無窮小」（含糊）變成「$\epsilon$-$\delta$」（精確）。**與 Cantor 集合論（1874，見 `1874-Cantor集合論.md`）同期**——分析的嚴格化與集合論的革命共同完成 19 世紀的基礎建設。

## 前因 -- 為什麼會有這個案子
**牛頓以來的含糊**（1665，見 `1665-Newton微積分.md`）：

- **無窮小**：$\Delta t \to 0$ 的「極限」——但 0/0 是什麼？
- **貝克萊的批評**（1734）：「消逝量的幽靈」（ghosts of departed quantities）——**神學家揪出數學的漏洞**
- **歐拉與拉格朗日**：形式操作（級數、級數求和）——**嚴格性有漏洞**

**1821 年 Cauchy 的半步**：極限的定義（「變數趨近的值」）——但仍依賴直覺的「趨近」。

**Weierstrass 的問題**：**能否用純邏輯（不等式）定義極限，徹底消除直覺？**

## 線索與推理 -- 數學式、程式、理論

### ε-δ 語言
**Weierstrass 的定義**：

**極限**：$\lim_{x \to a} f(x) = L$ ⟺ 對任意 $\epsilon > 0$，存在 $\delta > 0$ 使

$$0 < |x - a| < \delta \implies |f(x) - L| < \epsilon$$

**連續**：$f$ 在 $a$ 連續 ⟺ $\lim_{x \to a} f(x) = f(a)$。

**一致收斂**：$f_n \to f$ 一致 ⟺ 對任意 $\epsilon > 0$，存在 $N$ 使

$$n > N \implies \sup_x |f_n(x) - f(x)| < \epsilon$$

**革命性**：**純不等式**——無「趨近」「無窮小」「幽靈」的直覺詞彙——**邏輯的精確**。

**為什麼一致收斂重要**：逐點收斂（pointwise）不保持連續性——**一致收斂**才保持（Weierstrass 判準）——**收斂的「層次」**。

### 處處連續處處不可微函數
**1872 年的地震**：Weierstrass 的函數

$$f(x) = \sum_{n=0}^{\infty} a^n \cos(b^n \pi x), \quad 0 < a < 1, \; b \text{ 奇數}, \; ab > 1 + \frac{3\pi}{2}$$

**處處連續、處處不可微**！

**推理**：每一項 $a^n \cos(b^n \pi x)$ 平滑（可微），**無窮項的和**卻處處「毛刺」——頻率 $b^n$ 指數增長、振幅 $a^n$ 指數衰減，$ab > 1$ 使**毛刺不消失**：

$$f'(x) = -\sum_n a^n b^n \pi \sin(b^n \pi x) \quad \text{（} a^n b^n \to \infty \text{——發散！）}$$

**直覺的崩塌**：19 世紀的數學家（包括 Poincaré 稱之為「令人憎惡的函數」）相信「連續必可微（除有限點）」——**Weierstrass 的函數摧毀這個直覺**。

**Poincaré 的名言**：「Newton 時代以來，我們相信變數的函數沒有導數的地方是**例外**——這個信念被 Weierstrass 的例子粉碎。」

**深遠的後果**：
- **實分析的嚴格化**：可微性的精確研究——**處處不可微是常態**（Baire 綱領：連續函數集的「一般」元素不可微！）
- **分形的先聲**：自相似、無限細節（Mandelbrot 1975，見 `1984-Mandelbrot分形.md`）——**Weierstrass 函數是分形曲線的祖先**（Hausdorff 維數 > 1）
- **物理的隱喻**：布朗運動的路徑**處處連續處處不可微**（見 `../隨機算法/1905-布朗運動.md`）——**Weierstrass 函數是布朗路徑的表兄弟**

### 程式碼：Weierstrass 函數

```python
import math, random

def weierstrass(x, a=0.5, b=13, terms=50):
    """Weierstrass 函數：處處連續處處不可微"""
    return sum(a**n * math.cos(b**n * math.pi * x) for n in range(terms))

# 連續性：相鄰點的函數值接近
x0 = 0.3
for h in [0.1, 0.01, 0.001]:
    print(f"|f({x0}+{h}) - f({x0})| = {abs(weierstrass(x0+h) - weierstrass(x0)):.6f}")
# 接近 0——連續 ✓

# 不可微性：差商不收斂（震盪）
print("\n差商（導數的數值近似）：")
for h in [0.1, 0.01, 0.001, 0.0001]:
    dq = (weierstrass(x0+h) - weierstrass(x0)) / h
    print(f"h={h}: 差商 = {dq:.4f}")
# 不收斂（震盪）——不可微 ✓

# 對照：x² 的差商收斂到 2x
g = lambda x: x*x
print(f"\n對照 x²：h=0.001 差商 = {(g(x0+0.001)-g(x0))/0.001:.6f}（收斂到 2x = {2*x0}）")

# 布朗運動的路徑：處處連續處處不可微的「實例」
def wiener_path(steps=1000):
    x, path = 0.0, [0.0]
    for _ in range(steps):
        x += random.gauss(0, 0.01)
        path.append(x)
    return path
random.seed(42)
p = wiener_path()
print(f"\n布朗運動路徑：也處處連續處處不可微（Weierstrass 的表兄弟）")
```

### 分析嚴格化的帝國
**譜系**：
- **Newton（1665）**：無窮小（含糊）——見 `1665-Newton微積分.md`
- **Berkeley（1734）**：幽靈的批評——嚴格化的動機
- **Cauchy（1821）**：極限的半步
- **Weierstrass（1872）**：$\epsilon$-$\delta$ 的完成
- **Dedekind（1872）**：實數的切割（Dedekind cut）——實數的嚴格定義
- **Cantor（1874）**：集合論（見 `1874-Cantor集合論.md`）——分析的地基
- **Lebesgue（1902）**：測度論——積分的完成（見 `1933-Kolmogorov公理化.md`）

**偵探筆記**：Weierstrass 的推理是「**純不等式**」——消除一切直覺詞彙（趨近、無窮小）。**「嚴格化」的教訓**：直覺可以作為嚮導（發現），但證明必須純邏輯——與歐幾里得的公理化（見 `-0300-Euclid幾何原本.md`）、Bourbaki 的零圖形（見 `1935-Bourbaki結構革命.md`）同源：**直覺與嚴格的分離**。

## 結案 -- 後果與影響
- **分析的嚴格化完成**：$\epsilon$-$\delta$ 語言——分析學從「含糊的無窮小」到「精確的不等式」。
- **直覺的崩塌**：處處連續處處不可微——**19 世紀的地震**（「例外」變「常態」，Baire 綱領）。
- **分形的先聲**：無限細節、自相似——Weierstrass 函數是 Mandelbrot 分形的祖先（見 `1984-Mandelbrot分形.md`）。
- **布朗運動的數學**：處處不可微的路徑——**隨機分析的起點**（見 `../隨機算法/1905-布朗運動.md`）。
- **Dedekind 與 Cantor**：實數的嚴格定義（1872 同年）——**分析的數學地基**。
- **Weierstrass 的學派**：柏林學派（Kovalevskaya、Runge、Hurwitz）——**嚴格化的教學傳統**。

## 關鍵人物與文獻
- **Karl Weierstrass**（1815–1897）：Über continuirliche Functionen... (1872 講座，1895 出版)；$\epsilon$-$\delta$
- **George Berkeley**（1685–1753）：The Analyst (1734)——幽靈的批評
- **Augustin-Louis Cauchy**（1789–1857）：極限的半步 (1821)
- **Richard Dedekind**（1831–1916）：Stetigkeit und irrationale Zahlen (1872)——實數的切割
- **Henri Poincaré**（1854–1912）：「令人憎惡的函數」的批評
- 交叉參照：`1665-Newton微積分.md`、`1874-Cantor集合論.md`、`1984-Mandelbrot分形.md`、`../隨機算法/1905-布朗運動.md`、`1935-Bourbaki結構革命.md`
