# 1955-Serre FAC

## 案件摘要
1955 年，Jean-Pierre Serre 發表《Faisceaux algébriques cohérents》（簡稱 FAC），把 Leray 的層（sheaf）與上同調工具引入代數幾何，證明了凝聚層的對偶定理與消失定理。上同調 $H^i(X, \mathcal{F})$ 從此成為代數幾何的日常語言，並為 Grothendieck 的概形革命鋪平道路。

## 前因 -- 為什麼會有這個案子
- **Leray（1945，戰俘營中！）** 在 Oflag XVII-A 戰俘營裡創立了層論與譜序列，原本是為拓撲學服務 —— 數學在苦難中開花。
- **Cartan研討班（1948–1954）**：Henri Cartan 與 Eilenberg 把層論整理成《Homological Algebra》（1956）的公理化框架，同調代數正式誕生。
- **舊代數幾何的困境**：義大利學派（Castelnuovo、Enriques）的代數曲線/曲面理論靠直觀與分類，缺乏嚴格基礎；Zariski 用交換代數重建了幾何（Zariski 拓撲），但缺少「整體不變量」—— 怎麼把局部資訊黏成整體？
- Serre 的偵探問題：**「射影代數簇上的『解析函數層』式工具，能不能用純代數方式重建，並算出整體不變量？」**

## 線索與推理 -- 數學式、程式、理論

### 線索一：層 —— 「局部資訊的黏合手冊」
拓撲空間 $X$ 上的一個**層** $\mathcal{F}$ 是一個資料結構：對每個開集 $U$ 給一個集合 $\mathcal{F}(U)$（「$U$ 上的函數/截面」），滿足**層公理**：

$$U = \bigcup_i U_i,\ \ s_i \in \mathcal{F}(U_i),\ \ s_i|_{U_i \cap U_j} = s_j|_{U_i \cap U_j} \implies \exists!\ s \in \mathcal{F}(U),\ s|_{U_i} = s_i$$

（局部相容的截面可以唯一黏合成整體截面。）典型例子：$\mathcal{O}_X$（正則函數層）、$\mathcal{O}_X(D)$（除子相關的函數層）。

### 線索二：凝聚層 —— 有限性的「品質認證」
Serre 定義（在仿射簇上）**凝聚層**：$\mathcal{F}$ 是 $\mathcal{O}_X$-模層，且局部可由有限多個生成：

$$\exists\ \mathcal{O}_X^m|_U \twoheadrightarrow \mathcal{F}|_U \quad \text{且核也有限生成}$$

**Serre 的重大定理（FAC §1，GAGA 前身）**：

$$X \text{ 仿射} \iff H^i(X, \mathcal{F}) = 0 \ \ \forall i \geq 1,\ \forall \text{ 凝聚層 } \mathcal{F}$$

這把「仿射」這個幾何性質，翻譯成上同調消失 —— 幾何與代數的橋樑架好了。

### 線索三：上同調 —— 從層算出整體不變量
層上同調由**Cech 複形**或內射分解定義：對開覆蓋 $\mathfrak{U} = \{U_i\}$，

$$C^q(\mathfrak{U}, \mathcal{F}) = \prod_{i_0 < \cdots < i_q} \mathcal{F}(U_{i_0} \cap \cdots \cap U_{i_q}), \qquad H^q \xrightarrow{d} C^{q+1}, \quad H^i(X,\mathcal{F}) = \frac{\ker d_i}{\mathrm{im}\ d_{i-1}}$$

**經典應用**：對射影空間 $\mathbb{P}^n$ 與扭轉層 $\mathcal{O}_{\mathbb{P}^n}(d)$，

$$H^0(\mathbb{P}^n, \mathcal{O}(d)) = \{ \text{次數 } d \text{ 的齊次多項式} \}, \qquad H^i(\mathbb{P}^n, \mathcal{O}(d)) = 0 \ (0 < i < n)$$

上同調直接「算出」了幾何對象的函數空間。

### 線索四：Serre 對偶定理 —— 幾何的「鏡像恆等式」
對光滑射影簇 $X$（維度 $n$）、典範層 $\omega_X = \Omega^n_X$（或 $\wedge^n \Omega$）：

$$H^i(X, \mathcal{F}) \cong H^{n-i}(X, \mathcal{F}^\vee \otimes \omega_X)^*$$

**特例（曲線 $n=1$）**：$\dim H^1(C, \mathcal{L}) = \dim H^0(C, \mathcal{L}^\vee \otimes \omega_C)$ —— 這正是經典的 **Riemann–Roch** 中「非常數項」的來源。對 $C$、除子 $D$：

$$\ell(D) - \ell(K_C - D) = \deg D + 1 - g$$

Riemann–Roch 從「分析不等式」升級為「上同調恆等式」。

### 程式碼：Python 算 Cech 上同調（小例子）
用離散拓撲的玩具模型演示 Cech 複形：

```python
import itertools
from collections import defaultdict

def cech_cohomology(sections, intersections, n_cover):
    """sections: dict {open_set: vector space (list of basis labels)}
       intersections: dict {(i,j): restriction map (dict)}
       以 ℤ/2 係數的玩具複形計算 H^0, H^1"""
    F2 = lambda x: x % 2
    # C^0: 全域截面 = 相容的局部截面
    C0 = [tuple(s) for s in sections]
    # d^0: C^0 -> C^1, 差映射
    def d0(s):
        return tuple(F2(s[i] - s[j]) for i, j in itertools.combinations(range(n_cover), 2))
    C1 = list(itertools.product([0, 1], repeat=len(list(itertools.combinations(range(n_cover), 2)))))
    ker_d0 = [s for s in C0 if all(v == 0 for v in d0(s))]
    im_d0 = {tuple(d0(s)) for s in C0}
    H0 = len(ker_d0)
    H1 = len(C1) - len(im_d0)          # 玩具維度計數
    return H0, H1

# 例：兩個開集覆蓋 U0 ∪ U1，局部截面各 1 維、交疊上要相容
H0, H1 = cech_cohomology([(1,), (1,)], None, 2)
print(f"dim H^0 = {H0}, dim H^1 = {H1}")
# 當交疊「斷開」時（如兩個不相交開集），H^1 就會跳出來 —— 這就是「黏不住」的上同調障礙
```

## 結案 -- 後果與影響
- **上同調成為幾何工具**：$H^i(X, \mathcal{F})$ 從此是代數幾何的日常語言；代數曲線的分類（$g$、虧格）、Hodge 理論、Weil 猜想全部上同調化。
- **GAGA（1956）**：Serre 隨後證明代數幾何與解析幾何的範疇等價（FAC 的姊妹篇），凝聚層在兩個世界間自由穿梭。
- **為 Grothendieck 鋪路**：Grothendieck（1957 Tohoku 論文）將層上同調公理化，1960 年代進一步建立**概形（scheme）**理論與 Étale 上同調（見 [1960-Grothendieck概形](./1960-Grothendieck概形.md) 交叉參照）—— FAC 是這場革命的直接前身。
- **菲爾茲 + 阿貝爾**：Serre 因 FAC 時期的工作獲 1954 年菲爾茲獎（史上最年輕，28 歲），2000 年獲首屆沃爾夫獎，2003 年獲首屆阿貝爾獎 —— 三大獎全收。

## 關鍵人物與文獻
- **Jean-Pierre Serre（1926–2022，享年 95 歲）**：法國數學家，布爾巴基學派核心成員。1954 菲爾茲獎 + 2003 首屆阿貝爾獎雙料得主。他的數學人生橫跨拓撲、代數幾何、數論、群論，FAC 時代（1954–1956）是其黃金起點。
- J.-P. Serre, *Faisceaux algébriques cohérents*, Ann. of Math. 61 (1955), 197–278.
- J.-P. Serre, *Géométrie algébrique et géométrie analytique* (GAGA), Ann. Inst. Fourier 6 (1956), 1–42.
- 相關文獻：A. Grothendieck, *Sur quelques points d'algèbre homologique* (Tohoku), Math. J. Okayama 4 (1957)；R. Hartshorne, *Algebraic Geometry* (GTM 52, 1977)。
