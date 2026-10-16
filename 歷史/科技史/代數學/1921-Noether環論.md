# 1921 - Emmy Noether《Idealtheorie in Ringbereichen》

## 案件摘要
1921 年，Emmy Noether 發表《Idealtheorie in Ringbereichen》（環域中的理想理論），以公理化方法重構交換環與理想理論，提出升鏈條件（ACC）與 Noether 環，證明主理想整環是唯一分解整環。偵探的結論：這樁案子把 19 世紀 Dedekind 的「數論遺產」鑄造成 20 世紀的「抽象環論」。

## 前因 -- 為什麼會有這個案子
- **代數整數分解的危機**：Fermat 大定理的研究（Kummer 1840s）發現，$\mathbb{Z}[\sqrt{-5}]$ 中唯一分解性失效：
  $$6 = 2 \times 3 = (1+\sqrt{-5})(1-\sqrt{-5})$$
  Kummer 以「理想數」挽救，Dedekind (1871) 將其發展為**理想**理論：代數整數環中「理想皆可唯一分解為素理想之積」。
- **Hilbert 的不變量環**：Hilbert 1890 年證明多項式不變量環的有限生成定理（Hilbert 基定理），但其證明使用非構造性的存在論證，Gordan 曾抗議「這不是數學，是神學」。
- **Noether 的線索**：Noether 是 Hilbert 在 Göttingen 的同事，她發現 Hilbert 與 Dedekind 的兩條線索其實指向同一個源頭——**鏈條條件**。她決定把整個理論公理化。

## 線索與推理 -- 數學式、程式、理論

### 線索一：環與理想的公理化
**（交換）環**：集合 $R$ 配備兩個二元運算 $+, \cdot$，滿足：
1. $(R, +)$ 是交換群（單位 $0$）；
2. 乘法滿足結合律與單位元素 $1$；
3. 分配律：$a(b+c) = ab + ac$；
4. 交換律：$ab = ba$（交換環）。

**理想**：子集 $I \subseteq R$ 滿足：
1. $(I, +)$ 是加法子群；
2. 吸收性：$\forall r \in R,\; \forall a \in I,\; ra \in I$。

記 $I \triangleleft R$。由元素 $a_1, \dots, a_n$ 生成的理想記
$$(a_1, \dots, a_n) = \{ r_1 a_1 + \cdots + r_n a_n : r_i \in R \}$$
若 $I = (a)$ 僅由一個元素生成，稱**主理想**。商環 $R/I = \{a + I : a \in R\}$ 自然成為交換環。

### 線索二：升鏈條件（ACC）與 Noether 環
**升鏈條件（ACC）**：$R$ 中任意理想升鏈
$$I_1 \subseteq I_2 \subseteq I_3 \subseteq \cdots$$
必然在有限步後穩定：存在 $N$，使得 $I_N = I_{N+1} = I_{N+2} = \cdots$。

**Noether 環**：滿足 ACC 的交換環（等價於：每個理想皆有限生成）。

**推理**：ACC 是「無限遞降不可能」的公理化版本（類似良序原理），也是 Hilbert 基定理背後的真正引擎。**Hilbert 基定理**：若 $R$ 是 Noether 環，則多項式環 $R[x]$ 也是 Noether 環。推論：域 $k$ 是 Noether 環，故 $k[x_1, \dots, x_n]$ 皆為 Noether 環——Hilbert 的不變量問題由此解決，並開啟了代數幾何。

### 線索三：主理想整環（PID）與唯一分解性（UFD）
- **主理想整環（PID）**：每個理想皆為主理想的整環，如 $\mathbb{Z}$、$F[x]$。
- **唯一分解整環（UFD）**：每個非零非單位元素都可唯一分解為不可約元素之積（相差順序與單位）。

**Noether 的定理（1921）**：
$$\text{PID} \implies \text{UFD}$$
證明核心：在 PID 中，任取不可約元素鏈 $(a) \subseteq (a_2) \subseteq \cdots$，由 ACC 知鏈必穩定，故不能有無限真升鏈——每個元素必在有限步內分解為不可約元素；而 PID 中不可約元素生成素理想，唯一性由素理想性質保證。**推理**：Kummer 在 $\mathbb{Z}[\sqrt{-5}]$ 中看到的分解失效，正是因為該環不是 UFD；但 Dedekind 的素理想分解永遠成立——**「元素層次」的失敗，由「理想層次」補救**，這是本案最精彩的一筆推理。

### 線索四：Noether 定理（1918）——物理學的對稱性
同一時期（1918），Noether 證出物理學最重要的定理之一：**Noether 定理**——每一個連續對稱性對應一個守恆量：
- 時間平移對稱 $\Rightarrow$ 能量守恆
- 空間平移對稱 $\Rightarrow$ 動量守恆
- 旋轉對稱 $\Rightarrow$ 角動量守恆

這與她 1918 年對廣義相對論的能量守恆爭議（Klein–Hilbert 與 Einstein 的辯論）的解決密切相關，並為後來規範場論（規範對稱 $\Rightarrow$ 電荷守恆）鋪路。抽象代數與理論物理，在 Noether 手中同時開花。

### Python 實作：多項式環 mod p 的理想運算
在 $R = (\mathbb{Z}/p\mathbb{Z})[x]$（Noether 主理想整環）中操作理想：
```python
# GF(p)[x]：係數在模 p 域上的多項式環（PID）
p = 7
def pmod(c): return [v % p for v in c]                    # 正規化係數
def padd(a, b): return pmod([x + y for x, y in
                            zip(a + [0]*(len(b)-len(a)), b + [0]*(len(a)-len(b)))])
def pmul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i + j] = (r[i + j] + x * y) % p
    return r

def deg(c):
    return max((i for i, v in enumerate(c) if v % p), default=-1)

# 歐幾里得除法：a = q*b + r  (deg r < deg b)
def pdivmod(a, b):
    a, b = pmod(a), pmod(b)
    q, r = [0], a[:]
    db = deg(b)
    while deg(r) >= db:
        shift, lead = deg(r), r[deg(r)] * pow(b[db], -1, p)
        q = [0]*shift + [0]            # 佔位
        q[shift] = lead
        sub = [0]*shift + [lead * v % p for v in b]
        r = pmod([x - y for x, y in zip(r + [0]*len(sub), sub + [0]*len(r))])
        r = r[:max(deg(r)+1, 1)]
    return q, pmod(r)

# 最大公因式（歐幾里得演算法）：PID 中 (a,b) = (gcd(a,b)) 是主理想
def pgcd(a, b):
    while deg(b) >= 0:
        _, r = pdivmod(a, b)
        a, b = b, r
    return a

f = [1, 0, 0, 1]      # x^3 + 1
g = [2, 1]            # x + 2
d = pgcd(f, g)
print(f"gcd(f,g) = {d}  →  理想 (f,g) = ({d}) 是主理想")
```
程式示範了 PID 的核心：任意理想 $(f, g)$ 都等於單一生成元的理想 $(\gcd(f,g))$——這正是 1921 年 Noether 定理在有限域多項式環上的具體呈現。

## 結案 -- 後果與影響
- **現代交換代數的誕生**：ACC、Noether 環、素理想分解成為標準語言，直接催生 Zariski 的代數幾何與 Grothendieck 的概形理論。
- **抽象代數教科書的骨幹**：van der Waerden《Moderne Algebra》（1930）第二冊的環與理想章節，幾乎全部來自 Noether 的課程與論文。
- **「Noether 學派」**：B.L. van der Waerden、E. Artin、B. Segal 等人傳播其方法，公理化方法成為 20 世紀數學主流。
- **物理學的致敬**：Noether 定理至今是理論物理的基石，2015 年後仍有新推廣。
- **結案陳詞**：Noether 從「分解失效」與「Hilbert 神學」兩條線索，追出 ACC 這個公理化引擎，把數論遺產鑄成抽象環論——並順手解決了物理學的守恆之謎。

## 關鍵人物與文獻
- **Emmy Noether (1882–1935)**：德國數學家，Göttingen 學派核心，1933 年因納粹迫害流亡美國 Bryn Mawr。
- Noether, E. (1921). *Idealtheorie in Ringbereichen*. Math. Ann. 83, 24–66.
- Noether, E. (1918). *Invariante Variationsprobleme*. Nachr. Ges. Wiss. Göttingen, 235–257.（Noether 定理）
- Dedekind, R. (1871). 代數整數的理想理論（《數論講義》第十補篇）。
- Hilbert, D. (1890). *Über die Theorie der algebraischen Formen*.（Hilbert 基定理）
- 交叉參照：`1893-抽象群公理化.md`、`1930-VanderWaerden近代代數.md`、`1945-範疇論.md`。
