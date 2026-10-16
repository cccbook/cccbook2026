# 1872 - Klein 的 Erlangen 綱領：以群論統一幾何

## 案件摘要
1872 年，23 歲的 Felix Klein 就任埃爾朗根大學教授，提出著名的「Erlangen 綱領」：**一種幾何，就是某個變換群作用下的不變量理論**。他用「群」一把尺量盡歐氏、仿射、射影等所有幾何，終結了 19 世紀幾何學的分裂亂局。

## 前因 -- 為什麼會有這個案子
- **非歐幾何的衝擊**：Lobachevsky（1829）與 Bolyai（1832）創立雙曲幾何，Riemann（1854）提出一般流形，幾何學一夜之間冒出好幾個互不相容的體系——「什麼才是幾何」成為懸案。
- **射影幾何的興起**：Poncelet、Chasles、von Staudt 等人把射影幾何捧為「最高幾何」，但射影、歐氏、度量幾何之間的關係混亂。
- **Jordan 的線索**：Jordan《Traité》（1870）剛系統化了變換群概念；Klein 與 Lie 同在柏林追隨 Jordan 與 Plücker，深受群觀念洗禮。

## 線索與推理 -- 數學式、程式、理論

### 1. 核心定義：幾何 = 群作用下的不變量
設 $X$ 為一空間（點集），$G$ 為 $X$ 上的變換群：

$$g: X \to X,\qquad g \in G,\quad \mathrm{id} \in G,\quad g_1, g_2 \in G \Rightarrow g_1 g_2 \in G,\quad g^{-1} \in G$$

**Erlangen 綱領**：一門幾何即研究 $(X, G)$ 中在所有 $g \in G$ 下不變的性質（不變量）：

$$P \text{ 是幾何性質} \iff P(x_1, \dots, x_n) = P(gx_1, \dots, gx_n),\ \forall g \in G$$

兩圖形等價 $\iff$ 存在 $g \in G$ 把一個映成另一個（同一 $G$-軌道）。

### 2. 各幾何對應的群
| 幾何 | 空間 | 群 | 典型不變量 |
|------|------|-----|-----------|
| 歐氏幾何 | $\mathbb{E}^2$ | $\mathrm{E}(2) = \mathrm{O}(2) \ltimes \mathbb{R}^2$ | 長度、角度、面積 |
| 相似幾何 | $\mathbb{E}^2$ | $\mathrm{Sim}(2)$ | 角度、比例 |
| 仿射幾何 | $\mathbb{R}^2$ | $\mathrm{A}(2) = \mathrm{GL}(2) \ltimes \mathbb{R}^2$ | 平行性、共線性、面積比 |
| 射影幾何 | $\mathbb{RP}^2$ | $\mathrm{PGL}(3)$ | 共線性、交比 (cross-ratio) |

- 歐氏群：$\begin{pmatrix} x' \\ y \end{pmatrix} = R_\theta \begin{pmatrix} x \\ y \end{pmatrix} + t$，其中 $R_\theta^T R_\theta = I$
- 仿射變換：$x' = Ax + t$，$A \in \mathrm{GL}(2)$ 任意可逆
- 射影變換：齊次坐標 $\tilde{x}' = H\tilde{x}$，$H \in \mathrm{GL}(3)$，$\tilde{x} = (x, y, 1)^T$

### 3. 幾何學的層級：群越大，不變量越少
$$\mathrm{O}(2) \subset \mathrm{Sim}(2) \subset \mathrm{A}(2) \subset \mathrm{PGL}(3)$$

群包含關係決定幾何層級：

$$\text{歐氏幾何} \subset \text{相似幾何} \subset \text{仿射幾何} \subset \text{射影幾何}$$

- $G$ 越小 → 保留的不變量越多 → 幾何越「精細」
- $G$ 越大 → 不變量越少 → 幾何越「粗略」
- 射影幾何是最粗略的骨架；歐氏度量是射影幾何加上「絕對形」（absolute / 無窮遠圓）後的細化。

### 4. Python 演示：旋轉/仿射/射影變換下的不變量

```python
import numpy as np

P = np.array([[0.,0.],[4.,0.],[4.,3.],[0.,3.]])  # 矩形四頂點

def apply_affine(A, t, pts):
    return pts @ A.T + t

theta = np.pi/6
R = np.array([[np.cos(theta), -np.sin(theta)],[np.sin(theta), np.cos(theta)]])

# --- 歐氏（旋轉+平移）：長度與面積皆不變 ---
rot = apply_affine(R, [1,2], P)
side = lambda Q: np.linalg.norm(Q[1]-Q[0])
area = lambda Q: 0.5*abs(np.sum(Q[:,0]*np.roll(Q[:,1],-1) - np.roll(Q[:,0],-1)*Q[:,1]))
print("邊長:", side(P), "->", side(rot))    # 4 -> 4
print("面積:", area(P), "->", area(rot))    # 12 -> 12

# --- 仿射：長度會變，平行性與面積比不變 ---
A = np.array([[2.,0.],[1.,1.]]); t = [0,0]
aff = apply_affine(A, t, P)
print("仿射後邊長:", side(aff))             # 8（變了！）
print("仿射後面積:", area(aff))             # 24 = det(A)*12（面積比 = |det A| 不變）

# --- 射影：連直線與共線性都要用齊次坐標 ---
H = np.array([[1.,0,0],[0,1.,0],[0.3,0.2,1.]])
Ph = np.hstack([P, np.ones((4,1))])
Qh = Ph @ H.T
Q = Qh[:,:2] / Qh[:,2:3]
# 交比（射影不變量）：四共線點才可算；此處驗證「對邊平行性已喪失」
print("射影後四點:\n", np.round(Q,3))
print("原為矩形(對邊平行)，射影後對邊向量:", Q[1]-Q[0], Q[3]-Q[2])
```

輸出顯示：旋轉下長度、面積皆不變；仿射下長度改變但面積比（$|\det A|$）不變；射影下連平行性都喪失，只剩共線性與交比——正是 Erlangen 層級的實證。

## 結案 -- 後果與影響
- **幾何學的統一**：分裂的各幾何體系被安置在同一張「群譜系表」上，幾何教學與研究獲得明確地圖。
- **催生 Lie 群**：Klein 的好友 Lie 把「連續變換群」發展成 Lie 群與 Lie 代數理論（1888–1893）；兩人 1870 年代在巴黎的合作是直接淵源。
- **現代物理的對稱性語言**：Noether 定理（1918，對稱群 $\leftrightarrow$ 守恆律）、狹義相對論的 Lorentz 群、廣義相對論的微分同胚群、粒子物理的規範群，全是 Erlangen 思想的延伸。
- **Felix Klein（ Klein bottle 的 Klein）**：此綱領使他成為哥廷根學派掌門人，延攬 Hilbert，塑造了 20 世紀數學中心。

## 關鍵人物與文獻
- **Felix Klein**（1849–1925）：《Vergleichende Betrachtungen über neuere geometrische Forschungen》（Erlangen 綱領，1872）。
- **Sophus Lie**（1842–1899）：連續變換群理論創立者，Klein 的合作者。
- **Camille Jordan**（1838–1922）：變換群理論的系統化者（1870）。
- **Emmy Noether**（1882–1935）：對稱性與守恆律的橋樑（1918）。
