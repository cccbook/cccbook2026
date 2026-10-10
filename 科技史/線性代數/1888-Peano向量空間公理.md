# 1888 — Peano 向量空間公理

## 案件摘要
1888 年，意大利都靈的年輕數學家 Giuseppe Peano 出版《Calcolo geometrico secondo l'Ausdehnungslehre di H. Grassmann》（依據 H. Grassmann 的延伸論所寫的幾何計算）。在第九章中，他首次以**公理化的方式**定義了「線性空間」——就是我們今天所稱的向量空間——以及線性映射。向量與幾何從此不再依賴坐標與直觀圖像，而成為一套純粹由公理驅動的抽象結構。這是現代線性代數的「案發第一現場」。

## 前因 -- 為什麼會有這個案子
- **1844 年 Grassmann 的《Ausdehnungslehre》（延伸論）**：Hermann Grassmann 建立了 n 維線性代數的雛形——線性組合、線性無關、基底、維度，甚至外代數。但他是一位中學教師，不屬於任何數學權威圈子，書写得極為抽象難讀，幾乎無人問津。第一版只賣出寥寥數本，克雷勒（Klein）等人後來才承認「我們忽略了這部巨著」。
- **1843 年 Hamilton 的四元數**：Hamilton 為了推廣複數發明四元數，卻犧牲了乘法交換律。數學家第一次意識到：代數律不是天經地義，而是可以選擇的。
- **公理化思潮**：19 世紀後半，非歐幾何（Lobachevsky、Bolyai、Riemann）證明幾何公理可以替換；Boole 的邏輯代數、Cayley 的矩陣代數（1858）紛紛出現。「從具體對象中抽離，只保留公理」成為新的數學方法論。
- **Peano 的動機**：Peano 讀到 Grassmann 的《Ausdehnungslehre》深受震撼，認為這套理論應該被邏輯清晰地重寫，讓被忽視的思想重見天日。他將書名直接題獻給 Grassmann。

## 線索與推理 -- 數學式、程式、理論

### 線索一：Peano 的向量空間公理（1888 年原始版本）
Peano 在《Calcolo geometrico》第九章定義：設 $V$ 為一類「量」（entities），其上定義加法與實數純量乘法，滿足以下公理（Peano 原文編號為 1–8，以現代語言整理）：

1. （加法封閉與交換）$x + y = y + x$
2. $(x + y) + z = x + (y + z)$
3. 存在零元 $0$，使 $x + 0 = x$
4. 對每個 $x$ 存在 $-x$，使 $x + (-x) = 0$
5. （純量乘法對加法的分配）$a(x + y) = ax + ay$
6. $(a + b)x = ax + bx$
7. $a(bx) = (ab)x$
8. $1 \cdot x = x$

這就是今日教科書中向量空間的**八條公理**。Peano 接著定義了線性相依、線性無關、基底、維度（他稱為「線性系統的最大獨立組」的元素個數），全部用公理化的純邏輯語言寫成——不依賴任何坐標表示。

### 線索二：線性映射的首度公理化
Peano 同一章還首次定義了**線性映射**（linear transformation，他稱為 linear transformation of one linear system into another）：設 $A: V \to W$ 滿足

$$A(x + y) = Ax + Ay, \qquad A(ax) = aAx$$

並定義了核（kernel，他稱之為被映到 $0$ 的那些 $x$）與值域，得到了「維度定理」的早期形式：

$$\dim(\ker A) + \dim(\operatorname{im} A) = \dim V$$

這條秩–零化度定理（rank–nullity theorem）在 Peano 的書中已有清晰陳述，是抽象線性代數的第一個深刻結果。

### 線索三：為什麼公理化是關鍵證據
在 Peano 之前，「向量」是箭頭、是坐標、是位移。Peano 證明：只要一個集合滿足八條公理，**所有**線性代數的定理自動成立——多項式空間、矩陣空間、微分方程的解空間都是向量空間。檢驗方法只有一個：逐條核對公理。以下用程式示範這種「偵探式驗證」。

### 程式碼範例：向量空間公理檢驗
```python
import numpy as np
from itertools import combinations_with_replacement

# 待檢驗的「向量空間」候選：2x2 實矩陣空間（用隨機樣本抽驗公理）
rng = np.random.default_rng(0)
V = [rng.normal(size=(2, 2)) for _ in range(20)]
Z = np.zeros((2, 2))
scalars = [rng.normal() for _ in range(20)] + [0.0, 1.0, -1.0]

axioms = {
    1: lambda: all(np.allclose(x + y, y + x) for x in V for y in V),
    2: lambda: all(np.allclose((x + y) + z_, x + (y + z_))
                   for x in V for y in V for z_ in V),
    3: lambda: all(np.allclose(x + Z, x) for x in V),
    4: lambda: all(np.allclose(x + (-x), Z) for x in V),
    5: lambda: all(np.allclose(a * (x + y), a * x + a * y)
                   for a in scalars for x in V for y in V),
    6: lambda: all(np.allclose((a + b) * x, a * x + b * x)
                   for a in scalars for b in scalars for x in V),
    7: lambda: all(np.allclose(a * (b * x), (a * b) * x)
                   for a in scalars for b in scalars for x in V),
    8: lambda: all(np.allclose(1.0 * x, x) for x in V),
}

print("M_2(R) 是否滿足 Peano 八條公理？")
for i, check in axioms.items():
    print(f"  公理 {i}: {'通過' if check() else '不通過'}")

# 反例偵探：正實數集合，定義 x*y := x^y（違反公理 1）
try:
    assert 2.0 ** 3.0 == 3.0 ** 2.0
except AssertionError:
    print("  反例：正實數上的『乘法 x^y』不交換，故不構成向量空間")
```

抽樣檢驗顯示 $M_2(\mathbb{R})$ 通過全部八條公理——它是一個向量空間；而違反任何一條的候選結構立即被排除。這正是公理方法的威力：**判定只需查驗公理，不需知道對象的具體面貌**。

### 線索四：Peano 為何「結案卻無人知」
諷刺的是，Peano 的公理化當時也未引起廣泛迴響。直到 20 世紀：Weyl 1918 年《空間・時間・物質》、Banach 1922 年的賦篤空間公理、Noether 學派的抽象代數，才把公理化方法推上主流。1930 年代 Van der Waerden《Moderne Algebra》與 Birkhoff–Mac Lane 的教科書，使「向量空間 = 八條公理」成為全世界數學系的共同語言。歷史的判決書，延遲了四十年才送達。

## 結案 -- 後果與影響
- **現代線性代數的公理體系**：向量空間、線性映射、秩–零化度定理自此有了不依賴坐標的定義，教科書語言定型。
- **抽象代數誕生**：公理化從幾何擴展到群、環、體，催生 Noether 學派與 1930 年代的《Moderne Algebra》。
- **函數分析的道路**：把無窮維函數集視為向量空間，是 Banach、Hilbert 空間理論的前置條件。
- **Grassmann 平反**：被埋沒的《Ausdehnungslehre》透過 Peano 的轉述重獲重視，Grassmann 被追認為線性代數的先驅。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Giuseppe Peano | 1888 年公理化定義向量空間與線性映射 |
| Hermann Grassmann | 1844《Ausdehnungslehre》，n 維線性代數先驅 |
| William Rowan Hamilton | 1843 四元數，證明代數律可替換 |
| Arthur Cayley | 1858 矩陣代數 |
| Emmy Noether | 抽象代數學派的旗手 |

- G. Peano, *Calcolo geometrico secondo l'Ausdehnungslehre di H. Grassmann*, Bocca, Torino (1888)。
- H. Grassmann, *Die lineale Ausdehnungslehre*, Wiegand, Leipzig (1844)。
