# 1843-Hamilton 四元數

## 案件摘要
1843 年 10 月 16 日，Hamilton 在都柏林布魯姆橋（Broom Bridge）散步時頓悟：
要推廣複數到三維，必須**放棄交換律**。他當場用小刀在橋石上刻下
$$i^2 = j^2 = k^2 = ijk = -1$$
史上第一個非交換代數結構——四元數——就此誕生。

## 前因 -- 為什麼會有這個案子
- **複數的代數地位**：1830 年代複數 $\mathbb{C}$ 已被接受為平面上的點（Argand 圖示），
  $$z = a + bi, \quad i^2 = -1$$
  乘法 $z w$ 對應平面上的旋轉＋縮放：$(a+bi)(c+di) = (ac - bd) + (ad + bc)i$。
- **十五年失敗（1828–1843）**：Hamilton 试图把複數推廣到**三維空間**——
  他想做「三元數」$q = a + bi + cj$，要求乘法保持模長（賦范可除代數）：
  $$|q_1 q_2| = |q_1| \, |q_2|$$
  但三元組合始終湊不出這條性質——**三維的旋轉沒有與之相容的交換乘法**。
- 他給兒子的家書：「我每天清晨坐在書桌前，努力幾小時，卻一無所獲。」
- 案件問題：**擴張複數一定要保持交換律嗎？**

## 線索與推理 -- 數學式、程式、理論

### 線索一：布魯姆橋的頓悟
1843 年 10 月 16 日，Hamilton 沿著皇家運河散步，突然想到：**少一個維度不行，多一個維度可以**。
$$i^2 = j^2 = k^2 = ijk = -1$$
他當場用小刀刻在布魯姆橋的石頭上（原刻已風化，現有紀念牌匾）。

### 線索二：放棄交換律的革命
由基本關係式可推出完整的乘法表：
$$ij = k, \quad jk = i, \quad ki = j$$
$$ji = -k, \quad kj = -i, \quad ik = -j$$
**$ij = k$ 但 $ji = -k$** —— 交換律被犧牲了。
四元數定義：
$$q = a + bi + cj + dk, \quad a, b, c, d \in \mathbb{R}$$
- 共軛：$\bar{q} = a - bi - cj - dk$，模長：$|q| = \sqrt{a^2 + b^2 + c^2 + d^2}$
- **賦范可除性成立**：$q \bar{q} = |q|^2$，故 $q^{-1} = \bar{q}/|q|^2$。
- 這就是 Frobenius 定理（1877）的第一個案例：
  $\mathbb{R}$ 上有限維**結合可除代數**只有 $\mathbb{R}, \mathbb{C}, \mathbb{H}$ 三種。

### 線索三：旋轉表示——純四元數的共軛運算
單位四元數 $u = \cos\frac{\theta}{2} + \mathbf{v}\sin\frac{\theta}{2}$（$\mathbf{v}$ 為純虛單位向量）
作用在純四元數 $p = (0, \mathbf{x})$ 上：
$$p' = u \, p \, u^{-1} = u \, p \, \bar{u}$$
即三維空間繞軸 $\mathbf{v}$ 旋轉角 $\theta$。
對應關係：單位四元數 $S^3 \twoheadrightarrow SO(3)$（二對一，$u$ 與 $-u$ 同一旋轉），
這是**李群覆蓋理論**的最早實例之一。

### Python 實作：numpy 四元數旋轉

```python
import numpy as np

def quat(a, b, c, d):
    return np.array([a, b, c, d], dtype=float)   # (w, x, y, z)

def qmul(p, q):
    """Hamilton 乘積：i²=j²=k²=ijk=-1, ij=k 但 ji=-k"""
    w1, x1, y1, z1 = p; w2, x2, y2, z2 = q
    return np.array([
        w1*w2 - x1*x2 - y1*y2 - z1*z2,
        w1*x2 + x1*w2 + y1*z2 - z1*y2,   # ij = k, ji = -k 的符號就在這裡
        w1*y2 - x1*z2 + y1*w2 + z1*x2,
        w1*z2 + x1*y2 - y1*x2 + z1*w2,
    ])

def qconj(q):
    return np.array([q[0], -q[1], -q[2], -q[3]])

def qnorm(q):
    return np.linalg.norm(q)

def from_axis_angle(axis, theta):
    """單位四元數 u = cos(θ/2) + v sin(θ/2)"""
    axis = np.asarray(axis, float); axis /= np.linalg.norm(axis)
    return quat(np.cos(theta/2), *(axis * np.sin(theta/2)))

def rotate(point, axis, theta):
    """p' = u p ū"""
    p = quat(0, *point)
    u = from_axis_angle(axis, theta)
    return qmul(qmul(u, p), qconj(u))[1:]

# --- 驗證非交換性 ---
i, j = quat(0,1,0,0), quat(0,0,1,0)
k = quat(0,0,0,1)
assert np.allclose(qmul(i, j),  k)   # ij = k
assert np.allclose(qmul(j, i), -k)   # ji = -k  ← 革命性的一步
assert np.allclose(qmul(i, quat(0,1,0,0)), quat(-1,0,0,0))  # i² = -1

# --- 驗證旋轉：z 軸轉 90°，(1,0,0) → (0,1,0) ---
print(rotate([1,0,0], [0,0,1], np.pi/2))   # ≈ [0, 1, 0]

# --- 驗證模長保持（賦范可除）---
p, q = quat(1,2,3,4), quat(5,6,7,8)
assert np.isclose(qnorm(qmul(p, q)), qnorm(p) * qnorm(q))
print("四元數旋轉與模長律驗證通過")
```

### 理論定義
> **定義（四元數體 $\mathbb{H}$）**：$\mathbb{H} = \{a + bi + cj + dk\}$，
> 基本關係 $i^2 = j^2 = k^2 = ijk = -1$，加法逐項、乘法由分配律與上式決定。
> $\mathbb{H}$ 是結合可除代數，但**非交換**：$\mathbb{H}^\times$ 是非交換群。

## 結案 -- 後果與影響
- 結案陳詞：**放棄交換律，才能換到三維的對稱性**——這是代數學史上第一次「違反常識的革命」。
- **向量分析的誕生**：Gibbs 與 Heaviside 從四元數中抽出純虛部分
  （$\mathbf{v} = bi + cj + dk$ 的向量觀念），發展成現代向量分析
  （點積 $\mathbf{a}\cdot\mathbf{b}$、叉積 $\mathbf{a}\times\mathbf{b}$ 皆源於 $q_1 q_2$ 的實部與虛部）。
  Maxwell 方程組的原始形式就是用四元數寫的。
- Frobenius 定理（1877）：$\mathbb{R}, \mathbb{C}, \mathbb{H}$ 是僅有的結合可除代數；
  再放棄結合律還有 Cayley 八元數 $\mathbb{O}$（1845）。
- **深遠影響**：
  - 李群 $S^3 \to SO(3)$ 覆蓋、旋量（spinor）理論。
  - **現代應用**：3D 電腦圖學、遊戲引擎（Unity/Unreal）、太空飛行器姿態控制、
    慣性導航、機器人運動學——都靠單位四元數表示旋轉
    （無萬向節鎖 gimbal lock、數值穩定、插值 slerp 平滑）。
- 布魯姆橋的紀念牌匾寫著：「…as he was walking here on 16 October 1843,
  Sir William Rowan Hamilton in a flash of genius discovered the fundamental formula
  for quaternion multiplication.」

## 關鍵人物與文獻
| 人物 | 年份 | 貢獻 |
|------|------|------|
| Hamilton | 1843 | 布魯姆橋頓悟，四元數誕生 |
| Hamilton | 1853 | 《Lectures on Quaternions》 |
| Cayley | 1845 | 八元數（非結合可除代數）|
| Gibbs / Heaviside | 1880s | 向量分析（從四元數抽出）|
| Frobenius | 1877 | 結合可除代數分類定理 |
