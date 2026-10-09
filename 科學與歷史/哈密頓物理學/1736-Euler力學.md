# 1736 - Euler《力學》——用微積分重寫力學

## 案件摘要
1736 年，Euler 出版兩卷本《力學》(Mechanica sive motus scientia analytice exposita)。
副標題說明一切：「以分析法講解的運動科學」。牛頓用幾何證明，Euler 改用微分方程。
他第一個把質點運動系統化為 $m\ddot x = F(x, \dot x, t)$，並研究出今日所稱的「Euler 方程」。
這是力學從幾何學科轉型為**解析學科**的關鍵一步。

## 前因
- **Newton《原理》的幾何包袱**：證明優美但技巧個別化，每個問題要畫不同的輔助線，難以教學與推廣。
- **Leibniz 微積分（1684）**：$\frac{dy}{dx}$ 記號的傳入，使「變化率」可以當作代數對象操作。
- **Johann Bernoulli 的傳承**：Euler 師從 Bernoulli，年輕時就熟練萊布尼茲學派的解析技術。
- **實際需求**：船舶、鐘錶、彈道——18 世紀的工程問題需要可以「算」而非「證」的力學。

## 線索與推理

### 分析化力學的範式
Euler 的方法論：任何質點問題都可以寫成
$$m\ddot x = F(x, y, z, \dot x, \dot y, \dot z, t), \quad (\text{三個分量同理})$$
一組（常）微分方程 + 初值 ⇒ 一切化為積分技巧。這是「力學 = 微分方程理論」的宣言。

### 求解 $\ddot x = f(x)$ 的能量積分（第一次乘法積分）
Euler 對 $\ddot x = f(x)$ 兩邊乘 $\dot x\,dt$：
$$\dot x\, d\dot x = f(x)\,dx \;\Rightarrow\; \frac{1}{2}\dot x^2 = \int f(x)\,dx + C$$
左邊正是動能項，右邊是位能——**能量守恆的第一次解析推導**。
這一步埋下了伏筆：能量是可以當作「主角」的量，力反而是衍生品。

### 角動量與有心力
Euler 分析有心力運動時寫出（今日記法）：
$$\frac{d}{dt}(m r^2 \dot\theta) = 0 \;\Rightarrow\; m r^2 \dot\theta = \ell\ (\text{常數})$$
角動量守恆的分析形式。守恆律 = 某個「對稱性」的影子——這個思想的完全體要到 1918 年 Noether 才揭曉（見 [1918-Noether定理.md](1918-Noether定理.md)）。

### 歐拉–拉格朗日方程的前身
Euler 在變分法中（1736 年同一時期）已得到：使積分 $J = \int f(x, y, y')\,dx$ 極值的曲線滿足
$$\frac{\partial f}{\partial y} - \frac{d}{dx}\frac{\partial f}{\partial y'} = 0$$
這條方程在 1755 年被 19 歲的 Lagrange 重新發明並發揚光大（見 [1755-Lagrange變分法.md](1755-Lagrange變分法.md)）。

## 結案
- 力學教科書從此以微分方程為骨架；「解力學題 = 解 ODE」成為新常識。
- 能量積分技巧證明：$T$ 與 $V$ 可以獨立於「力」存在，為 Maupertuis 的最小作用量原理（見 [1744-Maupertuis最小作用量.md](1744-Maupertuis最小作用量.md)）鋪路。
- Euler 本人終其一生是 Lagrange 變分法的最佳宣傳者——大師為後進抬轎，成為科學史佳話。
