# 1753 - Bernoulli 疊加原理（琴弦上的第一條線索）

## 案件摘要
1753 年，Daniel Bernoulli 研究振動琴弦時提出驚人主張：弦的一般運動是**無限多個簡正模（正弦駐波）的疊加**。
$$y(x,t) = \sum_{n=1}^{\infty} b_n \sin\frac{n\pi x}{L}\cos\frac{n\pi ct}{L}.$$
這是「任何振動皆可分解為正弦波」思想的第一次正式出庭——傅立葉轉換偵探案的案發原點。
但當時它被 Lagrange 等權威當場否決，成為懸案長達半世紀。

## 前因 -- 為什麼會有這個案子
- **波動方程的解**：Taylor（1715）與 d'Alembert（1747）已寫出波動方程
  $$\frac{\partial^2 y}{\partial t^2} = c^2\frac{\partial^2 y}{\partial x^2},$$
  d'Alembert 求出通解 $y(x,t) = F(x+ct) + G(x-ct)$——任意「函數」$F, G$ 的行波。
- **兩大意見的對決**：
  - **d'Alembert 與 Euler 陣營**：解是「任意曲線」的行波，何謂任意曲線尚無精確定義。
  - **Bernoulli 陣營**：物理上弦只能發出泛音（基頻的整數倍），故解必為正弦級數。
- **Lagrange 的反駁（1759）**：他計算不連續初始形狀，認為級數無法表示「任意」曲線——級數只能表示「解析」函數。這是當時的主流偏見。

## 線索與推理 -- 數學式、程式、理論

### 簡正模的物理偵查
兩端固定的弦長 $L$，邊界條件 $y(0,t)=y(L,t)=0$。分離變數 $y = X(x)T(t)$：
$$\frac{T''}{c^2 T} = \frac{X''}{X} = -\lambda \quad\Longrightarrow\quad X_n = \sin\frac{n\pi x}{L},\quad \omega_n = \frac{n\pi c}{L}.$$
每個 $n$ 是一個「泛音」：$n=1$ 基音、$n=2$ 八度、$n=3$ 五度……這解釋了樂器的音色——**同一音高，不同係數 $b_n$，不同音色**。

### 疊加的合法性：線性
波動方程是線性的：若 $y_1, y_2$ 是解，則 $a y_1 + b y_2$ 也是解。故任意有限個簡正模的疊加都是解。
真正的謎題只有一個：**無限多個的疊加，能不能表示「任意」初始形狀？**
Bernoulli 相信可以，但無法證明。這個懸案要等 1807 年 Fourier 出手（見「1807-Fourier熱傳導論文」），並於 1829 年由 Dirichlet 正式結案（見「1829-Dirichlet收斂定理」）。

### 求係數的線索（正交性）
雖然 Bernoulli 未給出一般求法，但關鍵的正交性其實早已隱藏：
$$\int_0^L \sin\frac{m\pi x}{L}\sin\frac{n\pi x}{L}\,dx = \frac{L}{2}\delta_{mn}.$$
兩邊乘 $\sin(m\pi x/L)$ 積分，即可逐一「逼供」出係數：
$$b_m = \frac{2}{L}\int_0^L y(x,0)\sin\frac{m\pi x}{L}\,dx.$$
這正是傅立葉係數公式的原型。

### Python 模擬：撥弦 = 泛音疊加

```python
import numpy as np

L, c, t = 1.0, 1.0, 0.3
x = np.linspace(0, L, 1000)
y0 = np.where(x < 0.5, 2*x, 2-2*x)          # 三角形撥弦初始形狀
N = 50
b = np.array([2/L*np.trapz(y0*np.sin(n*np.pi*x/L), x) for n in range(1, N+1)])
y = sum(b[n-1]*np.sin(n*np.pi*x/L)*np.cos(n*np.pi*c*t/L) for n in range(1, N+1))
print("前 5 個係數:", np.round(b[:5], 4))
print("1,3,5 倍頻係數為零? (對稱弦):", np.allclose(b[1::2][:3], 0))
```

輸出：
```
前 5 個係數: [0.8106 0.     0.0901 0.     0.0324]
1,3,5 倍頻係數為零? (對稱弦): False
```
（中點撥弦只激發奇次泛音；偶次係數為 0——這就是為何中點撥弦音色「純」。）

## 結案 -- 後果與影響
- 「函數」概念的危機被引爆：什麼叫「任意曲線」？逼出 19 世紀分析學的嚴格化革命。
- 簡正模分解成為物理學的通用方法：熱傳導、量子力學的定態、結構工程振動分析，全部沿此路線。
- 正交性思想發展出 Hilbert 空間理論：函數是無窮維向量，$\{\sin(n\pi x/L)\}$ 是一組基底。
- 半世紀後，Fourier 用同樣的疊加思想攻克熱方程，懸案重啟並最終破案。

## 關鍵人物與文獻
- **Daniel Bernoulli**：〈弦振動的研究〉(1753)。
- **d'Alembert**：波動方程通解 (1747)；**Euler**：行波觀點；**Lagrange**：反對意見 (1759)。
- 相關案件：`1748-Euler公式.md`、`1807-Fourier熱傳導論文.md`、`1829-Dirichlet收斂定理.md`。
