# 1985-Splay Tree 與自我調整資料結構

## 案件摘要

1985 年，Daniel Sleator 與 Robert Tarjan 在《Journal of the ACM》發表〈Self-Adjusting Binary Search Trees〉，宣告一種「不需要任何平衡資訊、卻自動適應存取模式」的樹誕生：splay tree。平衡樹（AVL、紅黑樹）的偵辦思路是「用額外資訊防止樹長歪」，他們卻反問：能不能不防止，只把剛被存取的節點搬到根，讓熱點自然浮上來？破案時刻在於攤還分析：單次操作可能花 $O(n)$，但用勢能法可證**攤還複雜度為 $O(\log n)$**。而這棵樹是否為所有 BST 中漸近最優——動態最優性猜想——至今仍是懸案。

## 前因 -- 為什麼會有這個案子

- AVL 樹（1962）與紅黑樹（1978）每個節點都要儲存額外平衡資訊（高度差或顏色位元），插入刪除需持續維護，程式碼與常數成本不低。
- 實務上存取有強烈**區域性（locality）**：剛存取的資料極可能很快再被存取，但平衡樹對此無感——熱點與冷門資料待遇相同；Sleator 與 Tarjan 先前在 1983 年發表 link-cut tree（LCT），其核心已用到把節點旋到根的手法，需要一套嚴格的攤還分析；他們想要「自我調整（self-adjusting）」的結構：無需平衡資訊、無需預知存取模式，結構隨使用自動演化。

## 線索與推理 -- 數學式、程式、理論

### 線索一：splay 操作——旋到根

存取節點 $x$ 後，用旋轉把 $x$ 移到根，分三種情況：**zig**（父節點是根，單旋一次）；**zig-zig**（$x$、父 $p$、祖父 $g$ 同側，先旋 $g\text{-}p$ 再旋 $p\text{-}x$，順序不可顛倒，是分析的關鍵）；**zig-zag**（$x$ 與 $p$、$g$ 異側，旋 $p\text{-}x$ 再旋 $g\text{-}x$，等同兩次單旋）。

### 線索二：勢能法證攤還 $O(\log n)$

定義勢能 $\Phi$ 為所有節點 rank 之和，$\text{rank}(x) = \log \text{size}(x)$，$\text{size}(x)$ 為子樹節點數：

$$
\Phi(T) = \sum_{x \in T} \log \text{size}(x), \qquad \widehat{c} = c + \Phi_{\text{after}} - \Phi_{\text{before}}
$$

每種情況可證 splay 一步的攤還成本不超過 $3(\text{rank}'(x) - \text{rank}(x)) + 1$，沿路伸縮和累加，整個 splay 操作為 $O(\log n)$。單次最壞雖是 $O(n)$（鏈狀樹），但那次操作同時拉平了樹、償還了勢能債——這就是攤還分析的破案時刻。

### 線索三：動態最優性猜想（至今未解）

他們猜想：對任意合法的 BST 演算法（遵守旋轉模型），splay tree 的總成本都在常數倍之內：$\text{cost(splay)} = O(\text{OPT}(A))$ 對任意存取序列 $A$。若成立，splay tree 便是 BST 的漸近最優解——此猜想提出近四十年，仍是 BST 領域最重要的懸案。

### 線索四：working set 與 static finger 定理

splay tree 自動滿足兩個區域性定理，無需任何額外機制：**working set 定理**——存取 $x$ 的成本為 $O(\log w(x))$，$w(x)$ 是自上次存取 $x$ 以來不同元素的數量，熱點越「新鮮」越快；**static finger 定理**——若固定「手指」元素 $f$，存取 $x$ 的成本為 $O(\log |x - f|)$，離手指近就快。

### 線索五：與 AVL／紅黑樹的對照

- splay tree：零額外平衡資訊、攤還 $O(\log n)$、單次最壞 $O(n)$、自動適應區域性；AVL／紅黑樹：需存高度或顏色、單次保證 $O(\log n)$ 最壞、對存取模式無感。
- 取捨在於：要「單次最壞保證」還是要「攤還 + 自適應」。

### 程式偵查：Python 實測區域性存取

```python
class Node:
    def __init__(self, key):
        self.key, self.left, self.right, self.parent = key, None, None, None
class SplayTree:
    def __init__(self):
        self.root, self.cost = None, 0
    def _rotate(self, x):
        self.cost += 1
        p, g = x.parent, x.parent.parent
        if p.left is x: p.left, x.right = x.right, p
        else:           p.right, x.left = x.left, p
        x.parent, p.parent = g, x
        if g is None: self.root = x
        elif g.left is p: g.left = x
        else: g.right = x
    def splay(self, x):
        while x.parent:
            p, g = x.parent, x.parent.parent
            if g is None: self._rotate(x)                    # zig
            elif (g.left is p) == (p.left is x):             # zig-zig
                self._rotate(p); self._rotate(x)
            else: self._rotate(x); self._rotate(x)           # zig-zag
    def insert(self, key):
        if self.root is None:
            self.root = Node(key); return
        cur = self.root
        while True:
            if key < cur.key and cur.left is None:
                cur.left = n = Node(key); n.parent = cur; break
            if key >= cur.key and cur.right is None:
                cur.right = n = Node(key); n.parent = cur; break
            cur = cur.left if key < cur.key else cur.right
        self.splay(n)
    def find(self, key):
        cur = self.root
        while cur:
            if cur.key == key:
                self.splay(cur); return True
            cur = cur.left if key < cur.key else cur.right
        return False
if __name__ == "__main__":
    t = SplayTree()
    for k in range(1, 129):
        t.insert(k)
    t.cost = 0
    for _ in range(10): t.find(1); t.find(128)   # 冷門：交替存取樹的兩端
    cold = t.cost
    t.cost = 0
    for _ in range(20): t.find(64)               # 熱點：已被 splay 到根
    print(f"存取兩端極端值 20 次：{cold} 次旋轉")
    print(f"重複存取熱點 64 20 次：{t.cost} 次旋轉")
```

實測可見：第一次存取熱點後節點被 splay 到根附近，後續重複存取幾乎免費——working set 性質當場現形。

## 結案 -- 後果與影響

- 「自我調整資料結構」正式誕生：結構不需平衡資訊，靠使用模式自動優化，影響整個資料結構設計哲學；splay tree 並成為「攤還分析 + 勢能法」的教科書案例，與 LCT（Sleator-Tarjan 1983）一起成為動態樹問題的基礎工具。
- 動態最優性猜想成為 BST 理論最大的懸案，催生 tango tree（Demaine 等人 2004，$O(\log\log n)$ 競爭比）等研究路線；splay tree 廣泛用於快取、記憶體配置器與 LCT 實作，Sleator 之後並參與 C++ STL 的記憶體 allocator 介面設計。

## 關鍵人物與文獻（條列，含真實文獻書目）

- Daniel D. Sleator, Robert E. Tarjan (1985). *Self-Adjusting Binary Search Trees*. Journal of the ACM, 32(3), 652–686.
- Daniel D. Sleator, Robert E. Tarjan (1983). *A Data Structure for Dynamic Trees*. Journal of Computer and System Sciences, 26(3), 362–391.
- G. M. Adelson-Velskii, E. M. Landis (1962). *An Algorithm for the Organization of Information*. Soviet Mathematics Doklady, 3, 1259–1263.
- Leonidas J. Guibas, Robert Sedgewick (1978). *A Dichromatic Framework for Balanced Trees*. Proceedings of FOCS 1978, 8–21.
- Erik D. Demaine, Dion Harmon, John Iacono, Mihai Pătraşcu (2004). *Dynamic Optimality—Almost*. Proceedings of FOCS 2004, 484–490.
