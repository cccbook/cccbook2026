# 1748 - 歐拉公式

## 案件摘要
1748 年，Leonhard Euler 在《無窮分析引論》（Introductio in analysin infinitorum）中發表數學最美的公式：

$$e^{i\theta} = \cos\theta + i\sin\theta$$

取 $\theta = \pi$：

$$e^{i\pi} + 1 = 0$$

**五個最重要的常數**（$e, i, \pi, 1, 0$）在一條等式裡相會。這個公式把**指數與三角函數**統一（複指數），把**虛數從三次方程的怪物**（1545，見 `1545-Cardano三次方程.md`）升格為**分析的舞台**——複變函數論、傅立葉分析（見 `../傅立葉轉換/README.md`）、量子力學的基礎。物理學家 Feynman 稱它為「我們的寶石」（our jewel）。

## 前因 -- 為什麼會有這個案子
1740 年代的三個線索等待統一：

1. **指數**：$e^x$ 的微積分性質優美（$d/dx\, e^x = e^x$，見 `1665-Newton微積分.md`）
2. **三角函數**：$\sin, \cos$ 的泰勒級數與圓週期性——但與指數「無關」
3. **虛數**：Cardano 的怪物（1545）——有運算規則但「不是實的」，地位尷尬

**歐拉的問題**：$e^x$ 的泰勒級數把 $x$ 換成 $ix$ 會發生什麼？

## 線索與推理 -- 數學式、程式、理論

### 歐拉公式的推導
**泰勒級數**：

$$e^x = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \dots$$

把 $x$ 換成 $i\theta$（$i^2 = -1$）：

$$e^{i\theta} = 1 + i\theta - \frac{\theta^2}{2!} - \frac{i\theta^3}{3!} + \frac{\theta^4}{4!} + \frac{i\theta^5}{5!} - \dots$$

**分組**（實部與虛部）：

$$e^{i\theta} = \underbrace{\left(1 - \frac{\theta^2}{2!} + \frac{\theta^4}{4!} - \dots\right)}_{\cos\theta \text{ 的泰勒級數}} + i\underbrace{\left(\theta - \frac{\theta^3}{3!} + \frac{\theta^5}{5!} - \dots\right)}_{\sin\theta \text{ 的泰勒級數}}$$

$$\boxed{e^{i\theta} = \cos\theta + i\sin\theta} \quad \blacksquare$$

**實部是 cos、虛部是 sin**——指數與三角函數**本來就是同一件事**（在複數域中）。

### 幾何意義：單位圓
$e^{i\theta}$ 是複平面上單位圓上的點（角度 $\theta$）：

- $\theta = 0$：$e^{i \cdot 0} = 1$
- $\theta = \pi/2$：$e^{i\pi/2} = i$
- $\theta = \pi$：$e^{i\pi} = -1$
- $\theta = 2\pi$：$e^{2i\pi} = 1$（回到起點——**週期性**）

**取 $\theta = \pi$**：

$$e^{i\pi} = -1 \implies e^{i\pi} + 1 = 0$$

**五常數相會**：$e$（分析）、$i$（代數）、$\pi$（幾何）、$1$（單位）、$0$（虛無）——數學各分支的「靈魂」在一條等式裡。

### 為什麼重要：分析的複數化
**深遠的意義**：

1. **傅立葉分析**（1807，見 `../傅立葉轉換/README.md`）：信號的分解 $f(t) = \sum c_k e^{ikt}$——**歐拉公式的直接應用**（三角級數 = 複指數級數）
2. **複變函數論**（Cauchy、Riemann，19 世紀）：複分析成為數學最優雅的分支——解析延拓、留數定理
3. **量子力學**（1926）：Schrödinger 方程 $i\hbar\frac{\partial\psi}{\partial t} = \hat{H}\psi$——**虛數是量子世界的核心**（波函數的相位）
4. **電機工程**：交流電的相量（phasor）表示——$V = V_0 e^{i\omega t}$

**偵探筆記**：歐拉公式的推理是「**換個變數試試**」——$x \to i\theta$ 的一次代換，揭開指數與三角的統一。這個「越界」的風格（把 $e^x$ 的級數用到虛數域）與巴塞爾問題（見 `1734-Euler巴塞爾問題.md`）的無窮多項式同源：**形式操作先於嚴格證明**，最終都被嚴格化（複分析的收斂理論）。

### 程式碼：歐拉公式的驗證

```python
import cmath, math

# 數值驗證：e^{iθ} = cosθ + i·sinθ
for theta in [0, math.pi/6, math.pi/4, math.pi/2, math.pi, 2*math.pi]:
    lhs = cmath.exp(1j * theta)
    rhs = complex(math.cos(theta), math.sin(theta))
    print(f"θ={theta:.4f}: e^iθ = {lhs:.4f}，cos+isin = {rhs:.4f}，相等 = {abs(lhs-rhs) < 1e-12}")

# 歐拉恆等式：e^{iπ} + 1 = 0
print(f"\ne^(iπ) + 1 = {cmath.exp(1j*math.pi) + 1:.2e} ≈ 0 ✓")

# 單位圓：e^{iθ} 的軌跡
pts = [cmath.exp(1j * t) for t in [0, math.pi/2, math.pi, 3*math.pi/2]]
print(f"單位圓四點：{[f'{p.real:.2f}{p.imag:+.2f}i' for p in pts]}")
# (1.00+0.00i), (0.00+1.00i), (-1.00+0.00i), (0.00-1.00i)——逆時針轉一圈

# 傅立葉的種子：信號 = 複指數的和
def signal(t):
    return cmath.exp(1j*t) + 0.5*cmath.exp(3j*t) + 0.2*cmath.exp(5j*t)
print(f"\n信號 f(t) = Σ c_k e^{ikt}（歐拉公式使三角級數 = 複指數級數）")
```

### 從虛數怪物到分析的舞台
**譜系**：

1. **Cardano（1545）**：$\sqrt{-121}$ 的怪物——不情願的技巧（見 `1545-Cardano三次方程.md`）
2. **Bombelli（1572）**：虛數的運算規則——「plus of minus」
3. **Euler（1748）**：$e^{i\theta} = \cos\theta + i\sin\theta$——**虛數升格為分析的舞台**
4. **Argand / Wessel**（1797/1806）：複平面——虛數的幾何圖像
5. **Gauss（1799）**：代數基本定理——複數域封閉（見 `1799-Gauss代數基本定理.md`）
6. **Cauchy / Riemann**（19 世紀）：複變函數論——數學最優雅的分支

## 結案 -- 後果與影響
- **分析的複數化**：虛數從怪物成為舞台——複變函數論、傅立葉分析的基礎。
- **數學最美的公式**：$e^{i\pi}+1=0$——五常數相會，數學統一性的象徵。
- **量子力學的虛數**：波函數的相位 $e^{i\theta}$——虛數是量子世界的核心（不是技巧）。
- **工程的名詞**：相量、阻抗（複數）、頻域分析——電機工程的語言全是歐拉公式。
- **傅立葉的橋樑**：三角級數 = 複指數級數——信號處理的基礎（見 `../傅立葉轉換/README.md`）。
- **歐拉的帝國**：無窮分析引論（1748）是分析學的聖經——「讀歐拉的書」。

## 關鍵人物與文獻
- **Leonhard Euler**（1707–1783）：Introductio in analysin infinitorum (1748)——歐拉公式的發表
- **Roger Cotes**（1682–1716）：1714 接近發現（$\ln(\cos\theta + i\sin\theta) = i\theta$）——早於歐拉 30 年
- **Abraham de Moivre**（1667–1754）：$(\cos\theta + i\sin\theta)^n$ 公式（1722）——歐拉公式的先聲
- **Jean-Robert Argand**（1768–1822）：複平面 (1806)
- **Feynman**：〈我們的寶石〉（The Feynman Lectures）
- 交叉參照：`1545-Cardano三次方程.md`、`1734-Euler巴塞爾問題.md`、`1799-Gauss代數基本定理.md`、`../傅立葉轉換/README.md`
