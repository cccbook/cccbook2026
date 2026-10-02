# 2009 - Lurie 高階範疇

## 案件摘要
1945 年 Eilenberg–Mac Lane 創立範疇論，把數學的「結構」統一成態射的語言；但同倫論的世界裡，等價不再是同構，而是「同倫」。2009 年，Jacob Lurie 以萬頁巨著《Higher Topos Theory》與《Higher Algebra》完成了從範疇到 ∞-範疇的飛躍，讓同倫論成為現代數學的通用語言。

## 前因 -- 為什麼會有這個案子
- **範疇論（1945）**：Eilenberg–Mac Lane 的《General theory of natural equivalences》定義範疇、函子與自然變換（參照 1945-範疇論）。範疇的等價是「同構」。但拓撲空間的映射等價是**同倫** $f \simeq g$——用 1-範疇硬套同倫論，會丟失高階同倫資訊。
- **同倫的層級問題**：空間之間有 $f \simeq g$、同倫之間有同倫的同倫（2-同倫）……無窮層級。1-範疇的態射集合無法表達「態射之間的態射」。
- **擬範疇（Joyal, 1990s）**：Boardman–Vogt 的弱結合結構被 Joyal 用**單純集**嚴格化——quasi-category 是一個單純集，滿足內 Horn 提升條件，其 1-單純形是「態射」、2-單純形是「同倫證據」。Joyal 證明了它們的基本理論，但層疊（∞-topos）、導出幾何等高樓尚未蓋起。
- **Grothendieck 的遺願**：Grothendieck 晚年的 *Pursuing Stacks*（1983）與 *Les dérivateurs* 試圖把層論推廣到同倫世界——偵探的方向確定：**蓋一座「∞-層論」的大廈**。

## 線索與推理 -- 數學式、程式、理論
### 線索一：從範疇到 ∞-範疇的飛躍
1-範疇 $\mathcal{C}$ 的態射有單位律與結合律**嚴格成立**。∞-範疇把這些定律「放鬆成同倫」：
$$f \circ (g \circ h) \ \simeq\ (f \circ g) \circ h \quad \text{（同倫而非相等）}.$$
形式上，**擬範疇**是單純集 $S: \Delta^{op} \to \mathbf{Set}$ 滿足：
> 對所有 $0 < i < n$ 與映射 $\Lambda_i^n \to S$，擴張 $\Delta^n \to S$ 存在（內 Horn 提升）。

- $S_0$ = 物件、$S_1$ = 態射、$S_2$ = 態射的複合同倫……
- Kan 複雜（所有 Horn 皆可提升）= 「∞-群胚」= 空間的同倫模型。
- 嚴格範疇 N(C)（神經）是擬範疇的特例——**1-範疇是 ∞-範疇的剛化版本**。

### 線索二：∞-topos 與同倫層論（Higher Topos Theory, 2009）
Lurie 在《Higher Topos Theory》中將 Grothendieck 拓撲與層論推廣：
$$\mathbf{Shv}_\infty(\mathcal{C}) := \text{函子 } \mathcal{C}^{op} \to \mathcal{S}_\infty \text{ 中滿足下降條件者}.$$
其中 $\mathcal{S}_\infty$ 是 Kan 複雜構成的 ∞-範疇（= 空間）。**∞-topos** 是 $\mathbf{Shv}_\infty(\mathcal{C})$ 中滿足（∞-版本的）Giraud 公理者。書中建立了：
- **物件的分類空間**、覆疊、局部化（left/right Bousfield localization）。
- **∞-範疇上的極限、伴隨、順向極限**——所有 1-範疇工具的同倫版本。
- Descent theory：同倫版的 Grothendieck 下降，是導出幾何的黏合基礎。

### 線索三：導出代數幾何與 Higher Algebra（2009）
《Higher Algebra》將交換代數「同倫化」：
- **E∞-環**：乘法滿足「交換律直到所有同倫」的環譜，如複 K 理論譜 $KU$。
- **譜上的模**取代鏈複形：$\mathrm{Mod}_R$ 是穩定 ∞-範疇，其同倫群 $\pi_i$ 推廣了上同調。
- **導出代數幾何（DAG）**：用 $E_\infty$-環譜作為「導出概形」的結構層，使交互（intersection）理論有自然的導出修正——Quillen 的 K 理論（參照 1981-Quillen代數K理論）在這裡成為穩定 ∞-範疇的不變量。

### 程式：單純集的 Python 實作
單純集由「面映射」與「退化映射」構成。以下用簡單的 Python 類實作抽象單純複形，展示 2-單純形（三角面）如何攜帶「同倫證據」：

```python
class SimplicialSet:
    """抽象單純集：以 (維度, 頂點標號) 表示單純形，面映射取頂點"""
    def __init__(self):
        self.simplices = {}          # dim -> set of frozenset 頂點標號
        self.vertices  = set()

    def add_vertex(self, v):
        self.vertices.add(v)

    def add_simplex(self, verts):
        """加入以 verts 為頂點的單純形（自動補齊所有面）"""
        verts = tuple(verts)
        dim = len(verts) - 1
        self.simplices.setdefault(dim, set()).add(frozenset(verts))
        if dim > 0:
            # 面映射 d_i：刪掉第 i 個頂點，遞迴補齊所有面
            for i in range(len(verts)):
                self.add_simplex(verts[:i] + verts[i+1:])

    def summary(self):
        return {d: len(s) for d, s in sorted(self.simplices.items())}

# 建一個 2-單純形（三角形 0-1-2），含 3 條邊與 3 個頂點
S = SimplicialSet()
for v in range(3): S.add_vertex(v)
S.add_simplex([0, 1, 2])
print(S.summary())   # {0: 3, 1: 3, 2: 1}

# 再貼一個共用邊 1-2 的三角形 → 呈現「黏合」：單純集由面關係決定幾何
S.add_simplex([1, 2, 3])
print(S.summary())   # {0: 4, 1: 5, 2: 2} — 1-單純形 5 條（共用邊只算一次）
```

輸出顯示：一個 2-單純形自動生成 3 個面（邊）與 3 個頂點——這正是擬範疇中「2-單純形攜帶複合同倫證據」的離散模型；黏合兩個三角形時共用邊不重複，體現單純集的下降（descent）結構。

## 結案 -- 後果與影響
- **同倫論成為通用語言**：現代代數幾何（導出幾何）、表示論（stable ∞-範疇）、數學物理（TFT、拓撲場論）普遍採用 ∞-範疇語言；代數 K 理論（Waldhausen→stable ∞-範疇）被徹底重寫。
- **同倫型態（Homotopy Type Theory, HoTT）**：Voevodsky 的單價性（univalence axiom）與 HoTT 在語義上正是 ∞-群胚的類型論——Lurie 的 ∞-topos 理論為 HoTT 的模型論提供了數學基礎（2013 年 HoTT 書；Shulman 2019 的 (∞,1)-topos 模型）。
- **Lurie 萬頁著作的寫作風格**：《Higher Topos Theory》（949 頁）與《Higher Algebra》（1552 頁）以「先建全語言、再證定理」的公理式風格寫成——所有證明在 ∞-範疇框架內自足，成為 21 世紀數學寫作的範本（及爭議：有人認為過於抽象）。
- **後續案件**：Lurie 之後的幾何 Langlands（與 1974-Deligne 的 Weil 猜想技術匯流）、動力幺半群理論的範疇化、2010s 後的 spectral algebraic geometry，都以 ∞-範疇為地基。
- **趨勢**：與電腦證明（Lean、Coq 的 HoTT 模式）交叉——∞-群胚的「等價即同倫」觀念正在改變形式化數學的樣貌。

## 關鍵人物與文獻
- **Samuel Eilenberg & Saunders Mac Lane**：*General theory of natural equivalences*（1945），範疇論源頭。
- **Alexander Grothendieck**：*Pursuing Stacks*（1983）、*Les dérivateurs*，同倫層論的先聲。
- **André Joyal**：quasi-category 理論的建立者（*The theory of quasi-categories I*）。
- **Jacob Lurie**：*Higher Topos Theory*（Princeton, 2009）、*Higher Algebra*（2009/2017）。
- 延伸：Voevodsky 的 univalence 綱領；The Univalent Foundations Program《Homotopy Type Theory》（2013）。
