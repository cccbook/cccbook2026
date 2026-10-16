# 1884 — Gibbs 向量分析

## 案件摘要
1881 至 1884 年間，美國物理學家 Josiah Willard Gibbs 在耶魯大學印行私人講義《Elements of Vector Analysis》（向量分析原理），把三維幾何從四元數的桎梏中解放出來：以向量 $\vec{v}$ 為主角，定義點積 $\vec{a}\cdot\vec{b}$ 與叉積 $\vec{a}\times\vec{b}$，並用這套語言重寫 Maxwell 方程組。這場「向量 vs 四元數之爭」在 1890 年代引爆，最終向量分析完勝，成為今日物理與工程的標準語言。

## 前因 -- 為什麼會有這個案子
- 1843 年 Hamilton 發明四元數 $q = a + b\,i + c\,j + d\,k$，宣稱它是三維旋轉的天然代數；四元數學派（尤其 Edinburgh 的 Tait）視之為神聖不可侵犯。
- 1844 年 Grassmann 發表《線性擴張論》，提出更一般的 $n$ 維外代數，但幾乎無人問津——被埋沒了四十年。
- Hamilton 的四元數乘法中，純量部分 $ab - \vec{a}\cdot\vec{b}$ 與向量部分 $a\times b$（外積）糾纏在一起，物理學家（Maxwell 本人）就抱怨過四元數「在該純量的地方給你向量」。
- Gibbs 在耶魯教熱力學與電磁學，深深感到：**物理需要的只是「有方向的數」與兩種分離的乘法**，不需要四元數的純量尾巴。他把 Hamilton 的向量部分與 Grassmann 的外積拆開重組——這就是案發現場。

## 線索與推理 -- 數學式、程式、理論

### 線索一：三維向量與點積
Gibbs 以基底 $\{\hat{i}, \hat{j}, \hat{k}\}$ 表示三維向量

$$\vec{v} = v_x \hat{i} + v_y \hat{j} + v_z \hat{k}, \qquad |\vec{v}| = \sqrt{v_x^2 + v_y^2 + v_z^2}$$

並定義**點積**（純量積）：

$$\vec{a}\cdot\vec{b} = |\vec{a}||\vec{b}|\cos\theta = a_x b_x + a_y b_y + a_z b_z$$

點積是純量、可交換、度量長度與夾角——這正是物理中「功」$W = \vec{F}\cdot\vec{d}$ 所需要的全部。

### 線索二：叉積
Gibbs 定義**叉積**（向量積）：

$$\vec{a}\times\vec{b} = |\vec{a}||\vec{b}|\sin\theta\ \hat{n}, \qquad \hat{n} \perp \vec{a},\vec{b}\ \text{（右手定向）}$$

座標形式為行列式展開：

$$\vec{a}\times\vec{b} = \begin{vmatrix} \hat{i} & \hat{j} & \hat{k} \\ a_x & a_y & a_z \\ b_x & b_y & b_z \end{vmatrix} = (a_y b_z - a_z b_y)\,\hat{i} + (a_z b_x - a_x b_z)\,\hat{j} + (a_x b_y - a_y b_x)\,\hat{k}$$

叉積是向量、**反交換**（$\vec{a}\times\vec{b} = -\vec{b}\times\vec{a}$）、度量面積與法向——這正是力矩 $\vec{\tau} = \vec{r}\times\vec{F}$、角動量、磁力 $\vec{F} = q\vec{v}\times\vec{B}$ 所需要的。兩種乘法分離、各司其職——四元數的糾纏被解開。

### 線索三：以向量重寫 Maxwell 方程
Gibbs 用 $\nabla$（del 算子）與點積、叉積組合出散度 $\nabla\cdot$ 與旋度 $\nabla\times$，把 Maxwell 1873 年以四元數雜揉的方程組重寫為現代形式（高斯單位制）：

$$\nabla\cdot\vec{E} = 4\pi\rho, \qquad \nabla\cdot\vec{B} = 0$$
$$\nabla\times\vec{E} = -\frac{1}{c}\frac{\partial\vec{B}}{\partial t}, \qquad \nabla\times\vec{B} = \frac{1}{c}\frac{\partial\vec{E}}{\partial t} + \frac{4\pi}{c}\vec{J}$$

四條方程、對稱完美、一眼可見電磁波的波動結構（取旋度可得 $\nabla^2\vec{E} = \frac{1}{c^2}\partial^2\vec{E}/\partial t^2$）。Heaviside 在 1885 年後獨立做了同樣的事——兩位「兇手」殊途同歸。

### 程式碼範例：Gibbs 向量運算 vs 四元數的對照
```python
import numpy as np

a = np.array([2.0, 1.0, 0.0])
b = np.array([1.0, 3.0, 2.0])

# 線索一：點積（純量、可交換）
dot_ab = a @ b
print("a·b =", dot_ab, "，可交換：", np.allclose(a @ b, b @ a))
cos_theta = dot_ab / (np.linalg.norm(a) * np.linalg.norm(b))
print("夾角 cosθ =", round(cos_theta, 4), "→ θ =", round(np.degrees(np.arccos(cos_theta)), 2), "°")

# 線索二：叉積（向量、反交換）——手算行列式
cross_ab = np.array([a[1]*b[2]-a[2]*b[1],
                     a[2]*b[0]-a[0]*b[2],
                     a[0]*b[1]-a[1]*b[0]])
print("a×b 手算 =", cross_ab.tolist(), "，numpy 一致：", np.allclose(cross_ab, np.cross(a, b)))
print("反交換：a×b = -b×a ?", np.allclose(np.cross(a, b), -np.cross(b, a)))
print("a×b ⊥ a 且 ⊥ b ?", np.allclose(cross_ab @ a, 0), np.allclose(cross_ab @ b, 0))

# 線索三：四元數 vs Gibbs 對照——四元數乘法把兩者糾纏在一起
def quat_mul(p, q):
    w1, x1, y1, z1 = p; w2, x2, y2, z2 = q
    return np.array([w1*w2 - x1*x2 - y1*y2 - z1*z2,   # 純量部分：-a·b 藏在這
                     w1*x2 + x1*w2 + y1*z2 - z1*y2,
                     w1*y2 - x1*z2 + y1*w2 + z1*x2,
                     w1*z2 + x1*y2 - y1*x2 + z1*w2])

qa = np.r_[0.0, a]; qb = np.r_[0.0, b]        # 純向量四元數
prod = quat_mul(qa, qb)
print("\n四元數積 qa*qb =", np.round(prod, 4).tolist())
print("純量部分 = -a·b ?", np.allclose(prod[0], -dot_ab))
print("向量部分 = a×b ?", np.allclose(prod[1:], np.cross(a, b)))
```

程式證實 Gibbs 的拆解：四元數乘積的純量部分正是 $-\vec{a}\cdot\vec{b}$、向量部分正是 $\vec{a}\times\vec{b}$——Gibbs 把這兩部分「分家」，物理從此清爽。

## 結案 -- 後果與影響
- 向量分析成為**物理與工程的標準語言**：電磁學、流體力學、剛體力學全部改用 $\vec{a}\cdot\vec{b}$、$\vec{a}\times\vec{b}$、$\nabla$ 語法。
- 四元數被邊緣化近一世紀，直到 1985 年代後才在電腦圖學與太空姿態控制中「平反復活」（避免萬向節鎖）。
- 1890 年代的「向量之戰」（Gibbs-Heaviside vs Tait）以向量勝訴結案；Heaviside 的《電磁理論》(1893) 使向量微積分進入教科書。
- Gibbs 的叉積源自 Grassmann 外積——被埋沒的 Grassmann 自此逐步被發掘，直通 1888 年 Peano 的公理化。
- E. B. Wilson 1901 年依 Gibbs 講義整理出版《Vector Analysis》，成為經典教科書。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| J. Willard Gibbs | 1881–1884 講義《Elements of Vector Analysis》，向量語言之父 |
| Oliver Heaviside | 1885 年後獨立發展向量分析，電工應用 |
| William Rowan Hamilton | 1843 年四元數，糾纏的起點 |
| Hermann Grassmann | 1844 年外代數，叉積的真正源頭、被埋沒者 |
| Peter Guthrie Tait | 四元數學派旗手，向量之戰的對手 |

- J. W. Gibbs, *Elements of Vector Analysis*, New Haven: private printing (1881, 1884)。
- E. B. Wilson, *Vector Analysis*, New York: Scribner (1901)（依 Gibbs 講義整理）。
