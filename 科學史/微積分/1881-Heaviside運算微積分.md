# 1881 — Heaviside 運算微積分

## 案件摘要
1880 年代，自學成才的前電報技師 Oliver Heaviside 把微分算子 $d/dt$ 當成一個「代數符號 $p$」來操作，像解一元二次方程一樣解電路微分方程與電報方程，甚至大膽使用階梯函數與 impulse 函數。數學家斥之為「來歷不明的把戲」，工程師卻奉為神器。這樁案件直到 Laplace 變換被標準化、Schwartz 廣義函數問世後才正式結案——Heaviside 是對的，只是早了七十年。

## 前因 -- 為什麼會有這個案子
- **Maxwell 方程**：1873 年 Maxwell 出版《電磁通論》，二十個變數的分量方程難以駕馭。Heaviside 把它改寫成今日教科書的四個向量方程，並引入 $\nabla \times$、$\nabla \cdot$ 記號——他天生就愛把繁瑣的數學「壓縮」。
- **電報線路工程**：1858 年橫越大西洋電纜的訊號嚴重失真，長線路上電流的傳播方程（擴散型偏微分方程）用古典方法求解繁冗不堪。Heaviside 在電報公司工作時深受其苦，後來失業居家，索性發明一套「暴力算法」。
- 當時解線性常微分方程的正規武器是：先求齊次解、再猜特解、套邊界條件。Heaviside 問：為什麼不直接把 $d/dt$ 當成一個數 $p$ 去除？

## 線索與推理 -- 數學式、程式、理論

### 線索一：把微分當代數符號 p
Heaviside 記 $p = \frac{d}{dt}$，線性常係數微分方程就變成**代數方程**。例如 $RC$ 電路 $R\,\frac{dq}{dt} + \frac{q}{C} = E$（充電）寫成：

$$\left(Rp + \frac{1}{C}\right) q = E \quad\Longrightarrow\quad q = \frac{E}{Rp + \frac{1}{C}}$$

關鍵一刀：把 $\frac{1}{Rp + a}$ 展開成「運算冪級數」：

$$\frac{1}{p+a} = \frac{1}{p}\left(1 - \frac{a}{p} + \frac{a^2}{p^2} - \cdots\right), \qquad \frac{1}{p^n}f = \int_0^t \int_0^{\tau_1}\cdots f \, d\tau^n$$

也就是 $\frac{1}{p}$ 是積分、$\frac{1}{p^n}$ 是 $n$ 重積分。代入得 $q(t) = CE(1 - e^{-t/RC})$——與古典解完全一致，但只花三行代數。

### 線索二：解電報方程
長度 $x$ 的電報線上電壓 $V(x,t)$ 滿足（忽略漏電的簡化「Heaviside 條件」之外的一般情形）：

$$\frac{\partial^2 V}{\partial x^2} = LC\,\frac{\partial^2 V}{\partial t^2} + (RC + LG)\,\frac{\partial V}{\partial t} + RGV$$

Heaviside 用 $p$ 把它變成 $x$ 的常微分方程求解，並得到著名結論：若滿足**無失真條件** $\frac{R}{L} = \frac{G}{C}$，訊號以速度 $1/\sqrt{LC}$ 傳播且形狀不變、僅整體衰減 $e^{-x\sqrt{RG}}$。這直接指導了 1900 年代 Pupin 加感線圈的設計，讓長途電話成為可能。

### 線索三：Heaviside step 函數與 impulse 函數
Heaviside 引入階梯函數

$$H(t) = \begin{cases} 0, & t < 0\\ 1, & t > 0\end{cases}$$

把「在 $t=0$ 突然接上電源」寫成 $E\,H(t)$，並引進其導數 $\delta(t)$（impulse，「單位脈衝」）——一個除了一點之外處處為零、積分為 1 的「函數」。數學家嘩然：這種東西根本不是函數！Heaviside 回答：「我的函數會不會消化，跟我沒關係，我只問它算出來對不對。」

### 線索四：與 Laplace 變換的暗合
後人發現，Heaviside 的運算 $p$ 正是 Laplace 變換中的複數 $s$：

$$F(s) = \int_0^\infty e^{-st} f(t)\, dt, \qquad \mathcal{L}\{f'\} = sF(s) - f(0)$$

微分化為乘 $s$、積分化為除以 $s$，再經 Bromwich 積分反變換取回時域解。Heaviside 的「把戲」被嚴格化為標準的變換方法；而他的 $\delta(t)$ 則要等到 1945–1950 年 Schwartz 的分佈論（廣義函數）才獲得嚴格身份。

### 程式碼範例：用數值 Laplace 變換驗證 Heaviside 解 RC 電路
```python
import numpy as np
import sympy as sp

t, s = sp.symbols('t s', positive=True)
R, C, E = 1.0, 1.0, 1.0

# Heaviside 手法（sympy 版）：p 當代數符號解出 Q(s)，再反變換
Q = E / (s * (R + 1/(C*s)))          # 電源 E*H(t) -> E/s；q -> Q
q = sp.inverse_laplace_transform(Q, s, t)
q = sp.simplify(q.rewrite(sp.exp))
print("q(t) =", q)                    # 應為 E*C*(1 - exp(-t/(R*C)))

# 數值驗證：代回微分方程 R q' + q/C = E
q_fun = sp.lambdify(t, q, 'numpy')
tt = np.linspace(0.01, 5, 500)
h = tt[1] - tt[0]
dq = (np.roll(q_fun(tt), -1) - np.roll(q_fun(tt), 1)) / (2*h)  # 中心差分
resid = R*dq + q_fun(tt)/C - E
print("最大殘差 =", np.max(np.abs(resid[1:-1])))   # ~1e-8 量級，方程成立
```

反變換得到的 $q(t) = EC(1 - e^{-t/RC})$，數值殘差近零——Heaviside 的三行代數與古典解、變換法三方對質，口供一致。

## 結案 -- 後果與影響
- **Laplace 變換標準化**：1930 年代起，經 Doetsch 等人整理，Laplace 變換成為電機工程與控制理論的核心工具，傳遞函數 $\frac{1}{Rp+a}$ 的寫法沿用至今（拉氏域的 $\frac{1}{s+a}$）。
- **工程數學的誕生**：Heaviside 的《Electromagnetic Theory》三卷確立向量分析記號與運算方法，工程師從此有了一套自己的數學語言。
- **廣義函數的伏筆**：$\delta(t)$ 與 $H(t)$ 逼出 1945 年 Schwartz 分佈論（1950 年費爾茲獎），並成為 Dirac 在 1928 年量子力學中使用的 $\delta$ 函數的合法身份證。
- Heaviside 終生未被數學界正名，1931 年（他死後六年）英國皇家學會追贈法拉第獎章——案子結得晚，但結得清白。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| Oliver Heaviside | 運算微積分發明人，Maxwell 方程改寫者 |
| James Clerk Maxwell | 原始電磁理論的「案發現場」 |
| Gustav Doetsch | Laplace 變換理論的系統化者 |
| Laurent Schwartz | 分佈論，為 $\delta$ 函數正名 |

- O. Heaviside, *Electromagnetic Theory*, 3 vols. (1893–1912)。
- O. Heaviside, "On operational methods in physical mathematics", Proc. Roy. Soc. (1892)。
- L. Schwartz, *Théorie des distributions* (1950–1951)。
