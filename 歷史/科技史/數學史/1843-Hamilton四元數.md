# 1843 - Hamilton 四元數

## 案件摘要
1843 年 10 月 16 日，William Rowan Hamilton 在都柏林的 Broom 橋上刻下：$i^2 = j^2 = k^2 = ijk = -1$——**四元數（quaternions）的誕生**。他試圖把複數（$a + bi$）擴張到三維（旋轉表示），**15 年失敗**——突然領悟：**必須放棄交換律**（$ij \ne ji$）！**第一個非交換代數結構**——代數從「數的運算」解放成「任意的結構」——現代抽象代數（矩陣、群、李群）的先聲。**橋上的刻字是數學史上最戲劇性的頓悟**。

## 前因 -- 為什麼會有這個案子
**複數的成功**（歐拉公式 1748，見 `1748-Euler公式.md`）：$a + bi$ 表示平面的旋轉與縮放——**二維旋轉的完滿表示**。

**三維的困境**：物理（力學、光學、天文）需要**三維旋轉**的表示——能否把複數擴張到三維：

$$(a + bi + cj) \text{？}$$

**15 年的失敗**（1828–1843）：Hamilton 試圖保持**交換律**（$ij = ji$）與**模長性**（$|uv| = |u||v|$）——**不可能**（這個「不可能」在 1898 年由 Frobenius 定理嚴格化：實數域上的**結合可除代數**只有 $\mathbb{R}, \mathbb{C}, \mathbb{H}$ 三個）。

**Hamilton 的頓悟（1843 年 10 月 16 日）**：與妻子散步都柏林運河，走過 Broom 橋時突然領悟——**放棄交換律**：

$$ij = k, \quad ji = -k \quad \text{（} ij \ne ji \text{！）}$$

**刻在橋上**：$i^2 = j^2 = k^2 = ijk = -1$——**數學史上最著名的刻字**。

## 線索與推理 -- 數學式、程式、理論

### 四元數的結構
**定義**：四元數 $q = a + bi + cj + dk$（$a, b, c, d \in \mathbb{R}$），基本單位：

$$i^2 = j^2 = k^2 = ijk = -1$$

**乘法表**（非交換！）：

| $\times$ | $i$ | $j$ | $k$ |
|----------|-----|-----|-----|
| $i$ | $-1$ | $k$ | $-j$ |
| $j$ | $-k$ | $-1$ | $i$ |
| $k$ | $j$ | $-i$ | $-1$ |

**$ij = k$ 但 $ji = -k$**——**第一個非交換代數結構**。

**共軛與模長**：$\bar{q} = a - bi - cj - dk$，$q\bar{q} = a^2 + b^2 + c^2 + d^2 = |q|^2$——**模長性保留**（四個平方和）。

### 旋轉的表示
**四元數表示三維旋轉**：單位四元數 $q = \cos\frac{\theta}{2} + \sin\frac{\theta}{2}(u_x i + u_y j + u_z k)$（軸 $u$、角度 $\theta$），向量 $v$ 的旋轉：

$$v' = q\, v\, q^{-1}$$

**優點**：比歐拉角**無萬向鎖**（gimbal lock）、比旋轉矩陣**4 個參數**（vs 9 個）、**插值自然**（slerp）——**電腦圖學與遊戲引擎的標準**（Unity、Unreal 的旋轉都是四元數）。

**四元數的「復仇」**：向量分析（Gibbs–Heaviside 1880s）一度取代四元數——但 20 世紀末**電腦圖學復活了它**——**被遺忘的代數成為遊戲引擎的基礎**。

### 非交換的解放
**深遠的意義**：

1. **代數的解放**：運算律（交換律）**不是神聖的**——代數從「數的運算」解放成「任意的結構」——**抽象代數的先聲**（Galois 群論 1832 的交換律問題、矩陣代數 Cayley 1858）
2. **矩陣的先聲**：四元數的乘法表本質是 $4 \times 4$ 矩陣的表示——**線性代數**（見 `../線性代數/README.md`）
3. **物理的旋轉群**：$SO(3)$、$SU(2)$（四元數的單位球）——**量子力學的自旋**（泡利矩陣 $i, j, k$ 的表兄弟）、粒子物理
4. **Frobenius 定理**（1898）：結合可除代數只有 $\mathbb{R}, \mathbb{C}, \mathbb{H}$——**四元數是唯一的四維**（八元數 $\mathbb{O}$ 連結合律都放棄，Graves 1843）

**偵探筆記**：Hamilton 的推理是「**放棄交換律**」——15 年的失敗源於「交換律是神聖的」這個假設。**頓悟的瞬間**（橋上的刻字）是「假設的拆除」——與 Galois（1832，見 `1832-Galois群論.md`）的群論（方程的對稱性取代運算律）、Lobachevsky 的非歐幾何（1829，見 `1854-Riemann幾何.md`，平行公設的拆除）同源：**偉大的革命常是「拆除神聖假設」**。

### 程式碼：四元數與旋轉

```python
import math

class Quaternion:
    def __init__(self, a, b, c, d):
        self.a, self.b, self.c, self.d = a, b, c, d   # a + bi + cj + dk

    def __mul__(self, o):
        """非交換乘法！"""
        a, b, c, d = self.a, self.b, self.c, self.d
        e, f, g, h = o.a, o.b, o.c, o.d
        return Quaternion(
            a*e - b*f - c*g - d*h,
            a*f + b*e + c*h - d*g,
            a*g - b*h + c*e + d*f,
            a*h + b*g - c*f + d*e)

    def conjugate(self):
        return Quaternion(self.a, -self.b, -self.c, -self.d)

    def norm(self):
        return math.sqrt(self.a**2 + self.b**2 + self.c**2 + self.d**2)

# 非交換的驗證：ij = k 但 ji = -k
i = Quaternion(0, 1, 0, 0)
j = Quaternion(0, 0, 1, 0)
k = i * j
ki = j * i
print(f"i·j = ({k.a}, {k.b}, {k.c}, {k.d})——= k")
print(f"j·i = ({ki.a}, {ki.b}, {ki.c}, {ki.d})——= -k")
print(f"非交換：{(k.a, k.b, k.c, k.d) != (ki.a, ki.b, ki.c, ki.d)} ✓")

# 模長性：|uv| = |u||v|（四個平方和）
q1 = Quaternion(1, 2, 3, 4)
q2 = Quaternion(5, 6, 7, 8)
print(f"|q1·q2| = {q1*q2 and (q1*q2).norm():.4f}，|q1|·|q2| = {q1.norm()*q2.norm():.4f} ✓")

# 旋轉：90° 繞 z 軸（單位四元數）
theta = math.pi / 2
qz = Quaternion(math.cos(theta/2), 0, 0, math.sin(theta/2))
v = Quaternion(0, 1, 0, 0)          # x 軸的單位向量
v_rot = qz * v * qz.conjugate()
print(f"旋轉後向量 = ({v_rot.b:.4f}, {v_rot.c:.4f}, {v_rot.d:.4f})——(0,1,0)→y 軸 ✓")
```

## 結案 -- 後果與影響
- **抽象代數的先聲**：非交換的解放——矩陣（Cayley 1858）、群論（見 `1832-Galois群論.md`）、李群——代數從「數」到「結構」。
- **電腦圖學的基礎**：四元數的旋轉——Unity、Unreal、3D 遊戲的標準（無萬向鎖）。
- **物理的旋轉群**：$SU(2)$ 與量子自旋——泡利矩陣、粒子物理的對稱群。
- **Frobenius 定理**（1898）：$\mathbb{R}, \mathbb{C}, \mathbb{H}$ 的唯一性——四元數是唯一的四維結合可除代數。
- **橋上的頓悟**：假設的拆除（交換律）——與非歐幾何（平行公設）、群論（運算律的相對化）同源：**革命 = 拆除神聖假設**。
- **向量分析的插曲**：Gibbs–Heaviside 的取代 → 電腦圖學的復活——**被遺忘的代數成為遊戲引擎的基礎**。

## 關鍵人物與文獻
- **William Rowan Hamilton**（1805–1865）：都柏林；四元數 (1843)、Broom 橋刻字、哈密頓力學（見 `../微積分/README.md`）
- **John Graves**（1806–1870）：八元數（1843，Graves 的信）——連結合律都放棄
- **Ferdinand Frobenius**（1849–1917）：1898 定理——結合可除代數的分類
- **Josiah Gibbs / Oliver Heaviside**：向量分析（1880s）——四元數的取代者
- **Arthur Cayley**（1821–1895）：矩陣代數 (1858)——四元數的先聲
- 交叉參照：`1832-Galois群論.md`、`1854-Riemann幾何.md`、`1748-Euler公式.md`、`../線性代數/README.md`
