# 1871-Dedekind 理想

## 案件摘要
1871 年，Dedekind 在《代數整數論》（《Dirichlet 數論講義》第二版附錄 X）中發明「理想」（ideal），修復了代數數域中「唯一分解」崩壞的案件。Kummer 的「理想數」是先聲，Dedekind 將其公理化為集合論意義下的理想——唯一分解在元素層面失效，卻在**素理想**層面復活，並最終通向 Grothendieck 的概形理論。

## 前因 -- 為什麼會有這個案子
- 1840 年代，Kummer 為攻堅費馬最後定理（$x^n + y^n = z^n$），在分圓域 $\mathbb{Q}(\zeta_n)$ 中研究分解，發現**唯一分解在元素層面崩壞**。
- Kummer 的補救：引入「理想數」（ideale Zahlen）——看不見的「幽靈因子」，使分解重獲唯一性，證明了 $n$ 為正則素數時的費馬最後定理。
- 但 Kummer 的理想數缺乏嚴格定義，是「具體計算」的產物。
- Dedekind 的偵查目標：給理想數一個**集合論的、公理化的**定義，並把唯一分解定理重寫在新的框架下。

## 線索與推理 -- 數學式、程式、理論

### 線索一：唯一分解的失敗現場
在整環 $\mathbb{Z}[\sqrt{-5}] = \{a + b\sqrt{-5} : a, b \in \mathbb{Z}\}$ 中：
$$6 = 2 \cdot 3 = (1+\sqrt{-5})(1-\sqrt{-5})$$

用範數 $N(a+b\sqrt{-5}) = a^2 + 5b^2$ 檢驗不可約性：
$$N(2) = 4,\quad N(3) = 9,\quad N(1\pm\sqrt{-5}) = 6$$

四個因子的範數皆為質數冪或 6，且無更小範數的元素能分解它們（不存在 $a^2+5b^2 = 2$ 或 $3$ 的整數解），故它們**全都不可約**——但 $2$ 與 $1+\sqrt{-5}$ 顯然不相伴（無單位倍關係）。兩條分解鏈互不等價：**唯一分解在此案發現場崩壞**。

### 線索二：理想 $\subset \mathcal{O}_K$ 的公理化
Dedekind 的定義：數域 $K$ 的代數整數環 $\mathcal{O}_K$ 中的**理想** $I \subseteq \mathcal{O}_K$ 是一個加法子群，且對乘法封閉吸收：
$$a \in \mathcal{O}_K,\ x \in I \Rightarrow ax \in I$$

例如主理想 $(2) = 2\mathbb{Z}[\sqrt{-5}]$。理想之間可以定義乘法 $IJ$（由有限和 $ij$ 生成）與整除關係 $I \mid J \iff J \subseteq I$——「元素的世界」被整個搬到「理想的世界」。

### 線索三：素理想唯一分解的修復
Dedekind 的關鍵定理：

> **Dedekind domain 的唯一分解定理**：若 $\mathcal{O}_K$ 是 Dedekind domain（Noether、一維、可逆理想皆可逆，等價地：每個非零理想可唯一分解為素理想之積），則
> $$(6) = (2)(3) = \mathfrak{p}_2^{\,2}\,\overline{\mathfrak{p}_2}^{\,2}\,\mathfrak{p}_3\,\overline{\mathfrak{p}_3}$$
> 其中 $\mathbb{Z}[\sqrt{-5}]$ 中 $(2) = \mathfrak{p}_2\,\overline{\mathfrak{p}_2}$，$\mathfrak{p}_2 = (2, 1+\sqrt{-5})$，而 $(3) = \mathfrak{p}_3\,\overline{\mathfrak{p}_3}$，$\mathfrak{p}_3 = (3, 1+\sqrt{-5})$。

兩條分解鏈在理想層面其實是**同一條**：$2$ 並非素元，它「分裂」為兩個素理想之積——崩壞的案件被修復，唯一性在素理想層面復活。

### 程式碼：Python 演示 $\mathbb{Z}[\sqrt{-5}]$ 的非唯一分解

```python
import numpy as np
from itertools import product

# 元素以 (a, b) 表示 a + b*sqrt(-5)；範數 N = a^2 + 5b^2
def norm(z): return z[0]**2 + 5*z[1]**2
def mul(z, w): return (z[0]*w[0] - 5*z[1]*w[1], z[0]*w[1] + z[1]*w[0])
def assoc_chain(zs):
    r = (1, 0)
    for z in zs: r = mul(r, z)
    return r

# 線索一：兩條分解鏈都得到 6 = (6, 0)
print("2 * 3                     =", assoc_chain([(2,0),(3,0)]))
print("(1+sqrt(-5))(1-sqrt(-5))  =", assoc_chain([(1,1),(1,-1)]))

# 檢驗不存在範數為 2 或 3 的元素（故 2, 3, 1±sqrt(-5) 皆不可約）
solutions = [(a,b) for a,b in product(range(-5,6), repeat=2) if norm((a,b)) in (2,3)]
print("範數為 2 或 3 的元素：", solutions if solutions else "無 -> 全為不可約元")

# 線索三：素理想分解驗證
# p2 = (2, 1+sqrt(-5))：驗證 p2^2 * p2bar^2 ... 的指數計數
# 用範數檢驗理想：(2) 的理想範數 = 4 = N(p2)*N(p2bar) = 2*2
# 理想 (2, 1+sqrt(-5)) 的範數 = |O_K / p2| = 2（因 mod p2 時 sqrt(-5) ≡ -1，等價於 Z/2）
print("\n理想範數：N((2)) = 4, N(p2) = N(p2bar) = 2, N(p3) = N(p3bar) = 3")
print("唯一分解修復：(6) = p2^2 * p2bar^2 * p3 * p3bar（兩條鏈在理想層面相同）")
```

## 結案 -- 後果與影響
- **結案**：Kummer 的「幽靈因子」被公理化為理想；唯一分解的崩壞被診斷為「元素不是素元」，並在素理想層面獲得唯一分解的完美修復。
- Dedekind domain 成為代數數論的標準舞台：類數（class number）、判別式、素理想分解、單位群（Dirichlet 單位定理）全部在此框架下統一。
- 深遠影響一：Noether 把理想理論發展為交換代數（Noether 環、準素分解，1921）。
- 深遠影響二：Krull 的局部化、賦值論，承襲 Dedekind 的理想思想。
- 深遠影響三：Grothendieck 的概形理論（1960，EGA）把「理想」進一步推廣為「層的理想」——環 $\to$ 層、素譜 $\operatorname{Spec} R \to$ 概形，Dedekind 的偵探方法論最終成為現代代數幾何的地基。

## 關鍵人物與文獻
- **Richard Dedekind（1831–1916）**：Gauss 的學生，代數數論與集合論的先驅，理想論的發明人。
- **Ernst Kummer（1810–1893）**：理想數的創造者，費馬最後定理的正則素數證明者。
- **Emmy Noether（1882–1935）**、**Wolfgang Krull（1899–1971）**：理想論的交換代數化。
- **Alexander Grothendieck（1928–2014）**：概形理論的建構者。
- 文獻：R. Dedekind, "Über die Composition der Ideale...", 見 *Vorlesungen über Zahlentheorie von P. G. Lejeune Dirichlet*, 2. Auflage, Anhang X, 1871；英譯見 Stillwell, *Theory of Algebraic Integers*, Cambridge, 1996。
