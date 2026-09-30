# 1748 — Euler 複數指數與恆等式

## 案件摘要
1748 年，Leonhard Euler 出版《Introductio in analysin infinitorum》（無窮分析引論），在其中寫下數學史上最美的一條公式：

$$e^{i\theta} = \cos\theta + i\sin\theta$$

令 $\theta = \pi$，即得著名的 Euler 恆等式 $e^{i\pi} + 1 = 0$——分析學的五個基本常數 $e,\, i,\, \pi,\, 1,\, 0$ 在一行式中相遇。這條公式不是靈感乍現，而是 Euler 從級數與對數的長年偵查中**推理**出來的：虛數從此不再是代數方程的幽靈，而是分析學的正式公民。

## 前因 -- 為什麼會有這個案子
- **1614 年 Napier 發明對數**：把乘法化為加法，成為計算利器；但對數的底數 $e$（$e = \lim_{n\to\infty}(1+1/n)^n$）要到 Euler 手中才被命名並系統研究。
- **1665–1676 年 Newton 與 Leibniz 的微積分**：冪級數 $e^x = \sum x^n/n!$、$\sin x$、$\cos x$ 的展開式在 17 世紀已為人知。
- **1676 年 Leibniz 手稿**：已寫下 $i = \sqrt{-1}$ 與虛數的形式運算，但視其為「介於存在與不存在之間的兩棲動物」。
- **1707 年 De Moivre 公式**：$(\cos\theta + i\sin\theta)^n = \cos(n\theta) + i\sin(n\theta)$（$n$ 為整數），暗示複數的乘冪與三角函數之間有深層聯繫，但 De Moivre 未寫成指數形式。
- **1712–1740 年代對數的爭議**：負數與虛數的對數是否存在？Leibniz 與 Bernoulli 筆戰多年：Bernoulli 主張 $\ln(-x) = \ln x$（因 $(-x)^2 = x^2$），Leibniz 反對。爭議懸而未決。

案子就在對數與級數的交叉點上成形：$e^x$ 的級數裡若允許 $x = i\theta$，會出現什麼？

## 線索與推理 -- 數學式、程式、理論

### 線索一：三個級數的並排
Euler 在《Introductio》第七章把三個級數並排：

$$e^x = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \frac{x^4}{4!} + \cdots$$

$$\cos\theta = 1 - \frac{\theta^2}{2!} + \frac{\theta^4}{4!} - \cdots, \qquad \sin\theta = \theta - \frac{\theta^3}{3!} + \frac{\theta^5}{5!} - \cdots$$

把 $x = i\theta$ 代入 $e^x$ 的級數，注意 $i^2 = -1$、$i^3 = -i$、$i^4 = 1$（四項一循環）：

$$e^{i\theta} = \left(1 - \frac{\theta^2}{2!} + \frac{\theta^4}{4!} - \cdots\right) + i\left(\theta - \frac{\theta^3}{3!} + \frac{\theta^5}{5!} - \cdots\right) = \cos\theta + i\sin\theta$$

實部自動收斂成 $\cos\theta$，虛部自動收斂成 $\sin\theta$——級數的結構本身洩露了天機。

### 線索二：De Moivre 公式的指數化
De Moivre 公式 $(\cos\theta+i\sin\theta)^n = \cos n\theta + i\sin n\theta$ 在 Euler 的公式下變得顯而易見：

$$(e^{i\theta})^n = e^{in\theta} = \cos(n\theta) + i\sin(n\theta)$$

De Moivre 的「魔術」原來只是**指數律**：複數乘冪就是角度乘法。更進一步，歐拉寫下複數的極座標形式：

$$z = r(\cos\theta + i\sin\theta) = re^{i\theta}$$

複數乘法 $z_1 z_2 = r_1 r_2\, e^{i(\theta_1+\theta_2)}$——長度相乘、角度相加，幾何與代數在此合流。

### 線索三：Euler 恆等式與複對數
令 $\theta = \pi$：$e^{i\pi} = -1$，即

$$e^{i\pi} + 1 = 0$$

這條恆等式把五個常數 $e$（分析）、$i$（代數）、$\pi$（幾何）、$1$ 與 $0$（算術）連成一線。Euler 還解決了複對數懸案：由 $e^{i\theta} = \cos\theta+i\sin\theta$ 取對數得

$$\ln(\cos\theta + i\sin\theta) = i\theta \quad\Rightarrow\quad \ln(-1) = i\pi \neq \ln(1) = 0$$

Bernoulli 錯了：$\ln(-x) \neq \ln x$。而且 Euler 指出複對數是**多值的**：$e^{i(\theta+2k\pi)} = e^{i\theta}$ 對所有整數 $k$ 成立，故

$$\ln z = \ln|z| + i(\theta + 2k\pi), \quad k \in \mathbb{Z}$$

複對數不是單一函數，而是無限多層的螺旋——這是「多值函數」概念的誕生，也是日後複變函數論的核心難題（分支切割）的起點。

### 線索四：從 Euler 公式到三角恆等式
Euler 公式立刻產生兩個推論（把 $\theta$ 換成 $-\theta$ 相加減）：

$$\cos\theta = \frac{e^{i\theta}+e^{-i\theta}}{2}, \qquad \sin\theta = \frac{e^{i\theta}-e^{-i\theta}}{2i}$$

三角函數變成複指數的代數組合，一切三角恆等式（和角、倍角、積化和差）都化為指數律的機械操作——Euler 用一條公式把整本三角學「降維」成代數。

### 程式碼範例：Euler 公式的數值驗證
```python
import numpy as np
from math import factorial

# 線索一：級數部分和逼近 e^{iθ}
theta = 1.0  # 弧度
for k in [5, 10, 20]:
    n = np.arange(k)
    partial = np.sum(1j**n * theta**n / np.array([factorial(m) for m in n]))
    print(f"前 {k} 項部分和 = {complex(round(partial.real,8), round(partial.imag,8))}")
print("精確值 e^{i} =", np.exp(1j*theta), " cos+i sin =", np.cos(theta)+1j*np.sin(theta))

# 線索二：De Moivre 公式數值驗證
z = np.exp(0.5j)  # r=1, θ=0.5
for n in [2, 3, 7]:
    lhs = z**n
    rhs = np.exp(1j*0.5*n)
    print(f"n={n}: (e^(i0.5))^{n} = {lhs:.8f}  vs  e^(i{n*0.5}) = {rhs:.8f}  相等: {np.allclose(lhs, rhs)}")

# 線索三：Euler 恆等式
print("e^{iπ} =", np.exp(1j*np.pi), " → e^{iπ}+1 =", np.exp(1j*np.pi)+1)

# 複數平面視覺化：單位圓上 e^{iθ}
import matplotlib.pyplot as plt
ths = np.linspace(0, 2*np.pi, 100)
plt.figure(figsize=(6, 6))
plt.plot(np.cos(ths), np.sin(ths), 'b-', label='e^{iθ} 單位圓')
for t in np.linspace(0, 2*np.pi, 8, endpoint=False):
    plt.arrow(0, 0, np.cos(t)*0.95, np.sin(t)*0.95, head_width=0.05, fc='r', ec='r')
    plt.text(np.cos(t)*1.1, np.sin(t)*1.1, f'{t:.2f}', ha='center')
plt.axhline(0, c='gray', lw=0.5); plt.axvline(0, c='gray', lw=0.5)
plt.gca().set_aspect('equal'); plt.legend(); plt.title('e^{iθ} traces the unit circle')
plt.show()
```

數值輸出：級數部分和隨項數增加收斂至 $e^{i\theta}$；$(e^{i\theta})^n$ 與 $e^{in\theta}$ 在所有 $n$ 下完全相等（De Moivre 是指數律）；$e^{i\pi}+1 \approx 0$（浮點誤差 $10^{-16}$ 量級）；單位圓圖像顯示 $e^{i\theta}$ 就是複數平面上的逆時針旋轉。

## 結案 -- 後果與影響
- 虛數從代數的「幽靈」升格為**分析學的公民**：$e^{i\theta}$ 把複數與微積分、級數、微分方程連成一體。
- 三角學被「降維」：一切三角恆等式化為指數律；今日電機工程中的**相量（phasor）**分析直接源於 $e^{i\omega t}$。
- 複對數的**多值性**被發現，是 Riemann 面與分支切割理論的遠祖；$e^z$ 的週期性（$2\pi i$）成為複變函數論的基礎事實。
- Euler 公式是 Fourier 分析（1807）的語言基礎：Fourier 級數 $f(t)=\sum c_n e^{in\omega t}$ 正是用複指數寫的。
- 為 1799 年 Gauss 代數基本定理與 1851 年 Riemann 複變函數論鋪路——本案是「複變函數論」這門學科的直接起點。
- $e^{i\pi}+1=0$ 被譽為「最美數學公式」，它見證了：數學的分支（代數、幾何、分析）本是一體。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Leonhard Euler | 《Introductio》寫下 $e^{i\theta}=\cos\theta+i\sin\theta$ |
| Abraham de Moivre | $(\cos\theta+i\sin\theta)^n$ 公式的先驅 |
| John Napier | 對數的發明者 |
| Johann Bernoulli | 複對數爭議中主張 $\ln(-x)=\ln x$（Euler 證其誤） |

- L. Euler, *Introductio in analysin infinitorum*, Lausanne: Bousquet (1748)，第七章：$e^{i\theta}$ 公式與複對數。
- L. Euler, *De la controverse entre Mrs. Leibniz et Bernoulli sur les logarithmes des nombres négatifs et imaginaires* (1749)：複對數多值性的系統論述。
