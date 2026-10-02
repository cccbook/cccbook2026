# 1844-Grassmann 外代數

## 案件摘要
1844 年，德國中學教師 Hermann Grassmann 自費出版《線性擴張論》（*Die lineale Ausdehnungslehre*），發明了**外代數**（exterior algebra）——一種帶有反交換楔積 $\wedge$ 的乘法結構。這本書太超前於時代，幾乎無人閱讀，卻在數十年後成為微分幾何與理論物理的基石。

## 前因 -- 為什麼會有這個案子
- 1844 年，向量還沒有被發明成現代形式：Hamilton 的四元數要到 1843 年剛誕生，Gibbs/Heaviside 的向量分析要到 1880 年代。
- Grassmann 原本研究的是**潮汐理論**（1829 年起），需要一種能同時處理「點、方向、面積、體積」的統一代數語言。
- Leibniz 曾夢想一種「位置的幾何」（geometria situs）——直接對幾何物件做符號運算。Grassmann 認為自己實現了這個夢想。
- 悲劇前因：Grassmann 不是大學教授，而是**中學老師**（Stettin 的中學），沒有學術地位，著作自費出版、由母親賣書，初版幾乎無人問津。

## 線索與推理

### 線索一：楔積 $\wedge$ 與反交換性

設 $V$ 是佈於域 $K$ 的向量空間。外代數 $\bigwedge V = \bigoplus_{k=0}^{\infty} \bigwedge^k V$，其中 $\bigwedge^k V$ 是 $k$-向量（$k$-form 空間）。楔積滿足：

- **結合律**：$(u \wedge v) \wedge w = u \wedge (v \wedge w)$
- **反交換性**：$u \wedge v = -\,v \wedge u$，因此 $u \wedge u = 0$
- **雙線性**：對每個變元線性

**理論定義**：$\bigwedge^k V$ 是「$k$ 個向量的反對稱張量積」：

$$\bigwedge^k V = \frac{V^{\otimes k}}{\mathrm{span}\{v_1 \otimes \cdots \otimes v_k : v_i = v_j \text{ 對某 } i \neq j\}}$$

若 $\dim V = n$，則 $\dim \bigwedge^k V = \binom{n}{k}$，特別地 $\dim \bigwedge^n V = 1$——最高階只有一維，這就是「有向體積」的代數化身。

**推理核心**：為什麼要 $u \wedge u = 0$？因為面積為零！一條線段自己與自己張不成面積。反交換性不是任意規定，而是**幾何事實的代數反映**：交換兩個向量會翻轉有向面積的符號。

### 線索二：幾何意義——面積與體積

在 $\mathbb{R}^3$ 中，設 $u = u_1 e_1 + u_2 e_2 + u_3 e_3$，$v = v_1 e_1 + v_2 e_2 + v_3 e_3$：

$$u \wedge v = (u_2 v_3 - u_3 v_2)\, e_2 \wedge e_3 + (u_3 v_1 - u_1 v_3)\, e_3 \wedge e_1 + (u_1 v_2 - u_2 v_1)\, e_1 \wedge e_2$$

其係數正是**叉積的分量**！而

$$\|u \wedge v\| = \|u\| \|v\| \sin\theta = \text{平行四邊形的有向面積}$$

$$\|u \wedge v \wedge w\| = |\det(u, v, w)| = \text{平行六面體的有向體積}$$

**偵探推理**：叉積 $\times$ 只是外積在 3 維的「影子」（透過 Hodge 對偶 $u \wedge v \mapsto \star(u \wedge v)$ 識別 2-向量與向量）。叉積只在 3 維（與 7 維）存在，但**外積在所有維度存在**——這就是 Grassmann 版本更深刻的證據。

### 線索三：微分形式 $dx \wedge dy$ 的誕生

Grassmann 的符號直接孕育了**微分形式**：

$$dx \wedge dy = -\,dy \wedge dx, \qquad dx \wedge dx = 0$$

於是二重積分的面積元自然寫成 $\iint_D f\, dx \wedge dy$，而變數變換的 Jacobian：

$$dx \wedge dy = \frac{\partial(x,y)}{\partial(u,v)}\, du \wedge dv = (\det J)\, du \wedge dv$$

**這就是 Jacobian 行列式出現在換元公式中的代數原因**——不需要死背，楔積的反交換性自動給出。Poincaré 於 1899 年將外微分 $d$ 系統化，Cartan 於 1920 年代完成現代微分形式理論，最終 Stokes 定理寫成優雅的：

$$\int_{\partial M} \omega = \int_M d\omega$$

### 程式驗證（Python + numpy）

```python
import numpy as np

def wedge2(u, v):
    """R^3 中兩向量的楔積，回傳 (e23, e31, e12) 係數的 2-向量"""
    u1, u2, u3 = u
    v1, v2, v3 = v
    return np.array([u2*v3 - u3*v2,
                     u3*v1 - u1*v3,
                     u1*v2 - u2*v1])

def norm2(w):
    """2-向量的範數 = 有向面積大小"""
    return np.linalg.norm(w)

u = np.array([3.0, 0.0, 0.0])
v = np.array([0.0, 4.0, 0.0])
w = wedge2(u, v)
print("u ∧ v =", w)                     # [ 0.  0. 12.] -> 只有 e12 分量
print("||u ∧ v|| =", norm2(w))          # 12.0 = 3*4 矩形面積

# 幾何驗證：等於 |叉積| 與 |行列式|
print("u × v =", np.cross(u, v))        # [ 0.  0. 12.] 一致！
print("det[u,v,e3] =", abs(np.linalg.det(np.column_stack([u, v, [0,0,1]]))))  # 12.0

# 體積：三向量的楔積（3 維中外積是純量 = 行列式）
def wedge3(u, v, t):
    return np.dot(wedge2(u, v), t)      # (u∧v)·t = det[u,v,t]
print("u ∧ v ∧ e3 =", wedge3(u, v, np.array([0,0,1])))   # 12.0

# 反交換性驗證
print("u ∧ v + v ∧ u =", wedge2(u, v) + wedge2(v, u))    # [0. 0. 0.] ✓
print("u ∧ u =", wedge2(u, u))                            # [0. 0. 0.] ✓

# 一般情形：任意兩向量，面積 = ||u|| ||v|| sinθ
import math
a, b = np.array([1., 2., 3.]), np.array([4., 5., 6.])
cos_t = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
print("wedge 範數 =", norm2(wedge2(a, b)))
print("a||b||sinθ =", np.linalg.norm(a) * np.linalg.norm(b) * math.sqrt(1 - cos_t**2))
# 兩者相等 ✓ —— 楔積範數就是有向面積
```

**程式偵探筆記**：`wedge2(u,v)` 的係數恰為叉積分量、範數恰為面積——這證實「叉積是外積的 3 維影子」。反交換性與 $u \wedge u = 0$ 全部自動成立。

## 結案 -- 後果與影響
- **當時的悲劇**：1844 年初版僅數百本，Möbius 拒審、Gauss 未回應。Grassmann 1862 年出版徹底改寫的第二版，仍無人理解。他在 1878 年給 Sturm 的信中痛苦地寫道：「我完全確信，即使再過五十年，這本書也不會有人跟進。」——諷刺的是，這封信寄出後不久他就去世了，而 Gibbs 當年正好讀到了 Grassmann。
- **1880 年代**：Gibbs 與 Heaviside 發展向量分析時，明確採用了 Grassmann 的體系（而非 Hamilton 的四元數），引發著名的「向量戰爭」。
- **1899 年 Poincaré、1920 年代 Élie Cartan**：外微分與微分形式理論誕生，Grassmann 代數成為微分幾何的標準語言。
- **物理**：量子力學中費米子的反對稱波函數 $\Psi(x_1, \ldots, x_n)$（Pauli 不相容原理）本質上是外代數；現代規範場論、超對稱（Grassmann 變數 $\theta\eta = -\eta\theta$）、外爾旋量，全是 Grassmann 遺產。
- **計算數學**：計算機圖學中的外積代數（PGA）、幾何代數（Clifford 代數的推廣）用於剛體運動學。

## 關鍵人物與文獻
- **Hermann Günther Grassmann**（1809–1877）：德國 Stettin 中學教師，語言學家（曾編梵文字典），數學上超前時代半世紀。
- H. Grassmann, *Die lineale Ausdehnungslehre, ein neuer Zweig der Mathematik*, Leipzig, 1844.（第二版 1862）
- F. M. J. Fierz & V. A. Fock 對 Grassmann 變數在物理中應用的發展。
- D. Hestenes, *New Foundations for Classical Mechanics*, Kluwer, 1986.（幾何代數復興）
- J. Dieudonné, *Grassmann's Ausdehnungslehre*, Archive for History of Exact Sciences, 1979.
