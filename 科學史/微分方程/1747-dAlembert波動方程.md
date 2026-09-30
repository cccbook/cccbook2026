# 1747 達朗貝爾與波動方程

## 案發現場

十八世紀中葉，巴黎與柏林的科學院裡最熱門的「懸案」之一，是**弦振動問題**：一根兩端固定的弦被撥動之後，它的形狀 $y(x,t)$ 究竟如何隨時間演化？這不是純粹的數學遊戲——小提琴、大鍵琴的音色，乃至聲學的一般理論，都繫於這個問題之上。

泰勒（Brook Taylor, 1715）與約翰·伯努利（Johann Bernoulli, 1727）曾研究過弦的**簡正模式**（即正弦形狀的駐波），但他們只處理了特殊的初始形狀。真正的謎題是：**任意**形狀的初始位移——例如用手指捏出一個尖角——釋放後弦會怎麼運動？當時「函數」的觀念仍被理解為解析式子（冪級數、正弦等），一個有尖角的形狀似乎「不是函數」，於是謎題陷入僵局。

1746/1747 年，年方三十的達朗貝爾（Jean le Rond d'Alembert）在《流體阻力論文集》與柏林科學院院刊上發表論文〈張緊弦的振動研究〉，首次把問題寫成**偏微分方程**，並求出了**通解**。這是歷史上第一個被解出的非平凡偏微分方程，堪稱數學物理的開山之作。

## 偵查過程

達朗貝爾的偵查手法，是先把物理直覺翻譯成微積分的語言。

**第一步：牛頓第二定律應用於弦的一小段。**
設弦的線密度為 $\rho$，張力為 $T$（近似常數，因振動微小）。考慮 $x$ 與 $x+dx$ 之間的一小段，其橫向加速度為 $u_{tt}$，質量為 $\rho\, dx$。兩端張力的橫向分量之差提供回復力：

$$
\rho \, dx \cdot u_{tt} = T \left[ u_x(x+dx,t) - u_x(x,t) \right] \approx T\, u_{xx}\, dx
$$

**第二步：消去 $dx$，得到波動方程。**

$$
u_{tt} = \frac{T}{\rho}\, u_{xx} \quad\Longrightarrow\quad u_{tt} = c^2 u_{xx}, \qquad c = \sqrt{T/\rho}
$$

$c$ 正是波的傳播速度。這一步看似平凡，實則革命：達朗貝爾把「無窮多質點耦合系統」的問題，壓縮成一條**單一方程**。

**第三步：變數變換與通解。**
達朗貝爾的關鍵靈感是引入**特徵變數**：

$$
\xi = x + ct, \qquad \eta = x - ct
$$

用鏈鎖法則改寫導數：

$$
\partial_t = c\,\partial_\xi - c\,\partial_\eta, \qquad \partial_x = \partial_\xi + \partial_\eta
$$

於是

$$
u_{tt} - c^2 u_{xx} = c^2(u_{\xi\xi} - 2u_{\xi\eta} + u_{\eta\eta}) - c^2(u_{\xi\xi} + 2u_{\xi\eta} + u_{\eta\eta}) = -4c^2\, u_{\xi\eta}
$$

波動方程化為 $u_{\xi\eta} = 0$。對 $\xi$ 積分得 $u_\eta = \Phi(\eta)$（與 $\xi$ 無關），再對 $\eta$ 積分得

$$
\boxed{\,u(x,t) = f(x+ct) + g(x-ct)\,}
$$

**第四步：物理詮釋。** $g(x-ct)$ 是向右傳播的波（形狀不變、以速度 $c$ 前進），$f(x+ct)$ 是向左傳播的波。兩個波疊加，各自獨立行進——這就是**行波解**，也隱含了疊加原理。

**第五步：套用邊界與初始條件。** 對長度 $L$、兩端固定的弦，初始形狀 $u(x,0)=\varphi(x)$、初速度 $u_t(x,0)=\psi(x)$。由端點條件 $u(0,t)=u(L,t)=0$ 可推出 $g = f$（相差常數）且 $f$ 必須以 $2L$ 為週期**奇延伸**。達朗貝爾因此宣稱：$\varphi$ 必須夠「正規」（解析且能奇週期延伸），解才成立。

## 結案報告

達朗貝爾解出了波動方程，卻也引爆了**第二起懸案**：

- **Euler（1748）**接受通解形式，但認為 $\varphi$ 可以是任意的「力學曲線」——包括有尖角、分段定義的曲線，只要物理上能畫出來即可。
- **Daniel Bernoulli（1753）**則主張弦的運動是無窮多個簡正模式的疊加：

$$
u(x,t) = \sum_{n=1}^{\infty} b_n \sin\frac{n\pi x}{L} \cos\frac{n\pi c t}{L}
$$

並宣稱這樣的級數能代表**任何**初始形狀。達朗貝爾與 Euler 都反駁：正弦級數是解析的、週期的，怎可能等於一個非週期、有尖角的函數？

這場爭論（詳見 [1763-三角級數大辯論.md](1763-三角級數大辯論.md)）的核心其實是「**函數是什麼**」的概念危機，要到 Fourier（1822）與 Dirichlet（1829）才徹底解決。而達朗貝爾的遺產極為深遠：

1. **偏微分方程成為獨立學科**，波動方程是第一個範本；
2. **特徵變數法**後來發展成雙曲方程的特徵線理論（Riemann 不變量、激波理論）；
3. **分離變數法之源**——Bernoulli 的簡正模式思想經 Fourier 發揚，成為解線性偏微分方程的標準武器；
4. 波動方程至今是聲學、電磁學（馬克士威方程導出光速 $c$）、廣義相對論中引力波的共同祖先。

## 證據與工具

以下程式重現達朗貝爾的行波解：一個有尖角的三角形初始形狀（Euler 陣營支持的「力學曲線」），釋放後分裂成兩個反向行進的波。

```python
import numpy as np
import matplotlib.pyplot as plt

# 弦參數：長度 L=1，波速 c=1
L, c = 1.0, 1.0
x = np.linspace(0, L, 400)

# 達朗貝爾通解所需：初始位移 phi 與初速度 psi
# 三角形初始形狀（有尖角！）：在 x=0.4 處尖峰 0.3
peak_x, peak_h = 0.4, 0.3
def phi(s):
    # 兩端固定的弦：端點為 0，尖峰為 peak_h
    left = np.where(s < peak_x, peak_h * s / peak_x, 0.0)
    right = np.where(s >= peak_x, peak_h * (L - s) / (L - peak_x), 0.0)
    return left + right

psi = np.zeros_like(x)          # 靜止釋放，初速度為零

# 奇週期延伸（2L 週期、奇函數）：f(s) 對任意實數 s 的取值
def odd_periodic(s):
    s = np.mod(s, 2 * L)        # 折回 [0, 2L)
    return np.where(s <= L, phi(np.clip(s, 0, L)), -phi(np.clip(2 * L - s, 0, L)))

# 靜止釋放時，通解 u = [F(x+ct) + F(x-ct)] / 2，F 為 phi 的奇週期延伸
def u(x, t):
    return 0.5 * (odd_periodic(x + c * t) + odd_periodic(x - c * t))

# 畫出幾個時刻的弦形狀
times = [0.0, 0.2, 0.4, 0.6]
fig, ax = plt.subplots(figsize=(8, 5))
for t in times:
    ax.plot(x, u(x, t), label=f"t = {t}")

ax.set_title("d'Alembert solution: a plucked string splits into two waves")
ax.set_xlabel("x"); ax.set_ylabel("u(x,t)")
ax.legend(); ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("dalembert_waves.png", dpi=120)
plt.show()

# 驗證：波速 c = sqrt(T/rho)，改變張力 T 應等比改變傳播速度
for T in [1.0, 4.0]:
    cc = np.sqrt(T / 1.0)       # rho = 1
    print(f"T = {T}, c = {cc}, 尖峰位置隨 t=0.2 移動至約 x = {peak_x - cc*0.2:.2f} 與 {peak_x + cc*0.2:.2f}")
```

執行後可見：初始的三角形在 $t>0$ 時分裂成左右兩個三角形，各自以速度 $c$ 行進，在端點處發生反射（反相）——這正是 $u = f(x+ct) + g(x-ct)$ 的圖像化驗屍報告。
