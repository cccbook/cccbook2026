# 1844 — Grassmann 向量空間

## 案件摘要
1844 年，一位默默無聞的什切青（Stettin）中學教師 Hermann Grassmann 自費出版《線性擴張論》（*Die lineale Ausdehnungslehre, ein neuer Zweig der Mathematik*，簡稱 Ausdehnungslehre 1844）。他在書中建立了 $n$ 維線性空間、線性相依與線性獨立、基底與維數、外積 $\wedge$ 的完整理論——換言之，今日線性代數教科書的核心概念，比公理化時代早了半個多世紀。但這部巨著問世時幾乎無人問津，是一樁被長期忽視的懸案。

## 前因 -- 為什麼會有這個案子
- 1679 年 Leibniz 在寫給 Huygens 的信中夢想一種「幾何的代數」：直接用符號運算處理位置、方向與幾何關係，而不必依賴座標。他說這種語言「對力學會有重大用處」——這是本案最早的失蹤人口報案。
- 1827 年 Möbius 出版《重心計算》（*Der barycentrische Calcul*）：用重心座標處理點、線、面的關係，並注意到有向線段與「符號幾何」的思想。Möbius 的書影響有限，但 Grassmann 讀過並受其啟發。
- 1830–1840 年代：Hamilton 在追逐三元數（1843 年成案為四元數），Cauchy、Jacobi 的行列式理論成熟——但這些工具都綁在「數字陣列」上，沒有人回答 Leibniz 的夢想：位置的代數。
- Grassmann 的切入點出人意料：研究潮汐理論（1840 年論文）時，他發現自己需要的正是「點與向量的加減法」。他隨後把這套方法推廣成一般理論。
- 案件核心疑問：什麼是「$n$ 維空間」？什麼決定一個空間的「維數」？如何不靠座標直接運算幾何？

## 線索與推理 -- 數學式、程式、理論

### 線索一：$n$ 維線性空間與線性組合
Grassmann 把基本物件定義為「擴張量」（extensive Grösse）：由 $n$ 個獨立單位 $e_1, \dots, e_n$ 生成的形式和：

$$v = a_1 e_1 + a_2 e_2 + \cdots + a_n e_n$$

加法與數乘按係數進行，滿足今日的向量空間公理（結合、交換、分配、單位元）。他明確定義**線性相依**：若存在不全為零的係數使

$$c_1 v_1 + c_2 v_2 + \cdots + c_m v_m = 0$$

則 $v_1, \dots, v_m$ 線性相依；否則線性獨立。這是「線性獨立」一詞的最早清晰定義之一。

### 線索二：基底與維數的現代概念
Grassmann 證明：若 $e_1,\dots,e_n$ 線性獨立，則任意至多 $n$ 個獨立向量構成一組基底，任何向量可用基底唯一表示；且**所有基底的個數相同**——這個數就是空間的維數。用今日語言：

$$\dim V = n, \qquad V = \operatorname{span}(e_1, \dots, e_n)$$

維數不再是「我們畫得出幾條軸」，而是「極大線性獨立組的大小」——這個內在定義讓 $n > 3$ 的空間完全合法。Grassmann 甚至毫不猶豫地討論任意 $n$ 維乃至無窮維，遠超同時代人的想像。

### 線索三：外積 $\wedge$ 與叉積
Grassmann 的招牌發明是**外積**（äußeres Produkt）$\wedge$：滿足**反交換律** $e_i \wedge e_j = -\, e_j \wedge e_i$（故 $e_i \wedge e_i = 0$）與分配律。兩個向量的外積是一個「有向面元」：

$$u \wedge v = \sum_{i<j} (a_i b_j - a_j b_i)\; e_i \wedge e_j$$

其係數正是二階子行列式。幾何上，$u \wedge v$ 的「大小」就是 $u, v$ 張成的平行四邊形面積（Gram 行列式 $|u \wedge v| = \sqrt{\det(G)}$）。這與 Hamilton 的叉積對照：三維中叉積 $\mathbf{u}\times\mathbf{v}$ 是一個**向量**（用 Hodge 對偶把面元轉成法向量），分量 $ (b_1c_2-b_2c_1,\; c_1a_2-c_2a_1,\; a_1b_2-a_2b_1) $ 恰是外積的三個二階子行列式。Grassmann 的外積更一般：它在任何維度都有意義，且可直接外推 $u \wedge v \wedge w$（有向體元）。今日的外代數（exterior algebra）、微分形式（Cartan）、行列式的多重線性理論，全部由此而生。

### 程式碼範例：Grassmann 外積與叉積對照
```python
import numpy as np
from itertools import combinations

def wedge(u, v, n):
    """外積：回傳 {平面基: 係數}，係數 = 二階子行列式"""
    w = {}
    for (i, j) in combinations(range(n), 2):
        coef = u[i]*v[j] - u[j]*v[i]
        if coef != 0:
            w[(i, j)] = coef
    return w

def cross3(u, v):
    """三維叉積"""
    return np.array([u[1]*v[2]-u[2]*v[1],
                     u[2]*v[0]-u[0]*v[2],
                     u[0]*v[1]-u[1]*v[0]])

u = np.array([1., 2., 3.]); v = np.array([4., 5., 6.])
w = wedge(u, v, 3)
print("外積係數 (01,02,12) =", [w.get(p, 0) for p in [(0,1),(0,2),(1,2)]])
print("叉積              =", cross3(u, v), "  <- 分量相同（Hodge 對偶）")

# 外積的反交換律：wedge(v,u) = -wedge(u,v)
wu = wedge(v, u, 3)
print("反交換驗證        =", all(w.get(p,0) == -wu.get(p,0) for p in [(0,1),(0,2),(1,2)]))

# 面積：|u∧v| = sqrt(det(G))，G 為 Gram 行列式
area_wedge = np.sqrt(sum(c*c for c in w.values()))
G = np.array([[u @ u, u @ v], [u @ v, v @ v]])
print("外積面積          =", area_wedge, " Gram 面積 =", np.sqrt(np.linalg.det(G)))

# 三重外積 = 平行六面體體積（有向）
def triple_wedge(u, v, w3):
    return np.linalg.det(np.array([u, v, w3]))
w3 = np.array([0., 1., 0.])
print("三重外積（有向體積） =", triple_wedge(u, v, w3),
      " det[u;v;w] =", np.linalg.det(np.vstack([u, v, w3])))

# 四維空間的外積：Grassmann 理論在任何維度皆可用
u4 = np.array([1., 0, 2, 0]); v4 = np.array([0, 3, 0, 4])
print("4 維外積          =", wedge(u4, v4, 4))
```

輸出顯示：三維中外積係數與叉積分量一致（差一個對偶方向）、反交換律成立、$|u\wedge v|$ 等於 Gram 面積、三重外積等於有向體積，且四維外積毫無障礙——Leibniz 的「幾何代數」夢想在此成真。

## 結案 -- 後果與影響
- 悲劇性忽視：1844 版 Ausdehnungslehre 因文風抽象、術語自創、作者是無名校師，幾乎無人閱讀。1862 年 Grassmann 重寫新版，仍然遇冷。他向數學界求職屢屢被拒，終生以中學教師為業。
- 關鍵平反：1860 年代末 Möbius 與 Clebsch 讚揚其工作；1878 年 Peano 翻譯並公理化 Ausdehnungslehre，向量空間的公理定義首次出現。Grassmann 晚年（1878 年前）終於獲選進入哥丁根科學院。
- 遺產全面開花：外代數 → Cartan 的微分形式與外微分（1899）→ 現代微分幾何與廣義相對論的數學語言；向量空間公理 → 20 世紀泛函分析、量子力學的希爾伯特空間。
- 與 Hamilton 的四元數（1843）、Sylvester 的矩陣（1850）相比，Grassmann 的抽象最徹底、影響最深遠，卻也最孤獨。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Hermann Grassmann | 《擴張論》作者，向量空間與外積的發明者 |
| Gottfried Wilhelm Leibniz | 「幾何代數」夢想的提出者（1679） |
| August Ferdinand Möbius | 重心座標（1827）、Grassmann 的平反者 |
| Giuseppe Peano | 1878 年公理化 Grassmann 理論 |
| Alfred Clebsch | 讚揚並推廣 Grassmann 工作 |

- H. Grassmann, *Die lineale Ausdehnungslehre, ein neuer Zweig der Mathematik*, Leipzig: Otto Wigand (1844)。
- H. Grassmann, *Die Ausdehnungslehre. Vollständig und in strenger Form bearbeitet*, Berlin: Enslin (1862)。
- G. Peano, *Calcolo geometrico secondo l'Ausdehnungslehre di H. Grassmann*, Torino (1888)。
