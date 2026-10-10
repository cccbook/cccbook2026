# 複變函數史 -- AI 偵探風格

以「推理探案」的方式，追查複變函數論從 1545 年 Cardano 被迫寫下 $\sqrt{-15}$，到今日分形、FFT 與現代計算的每一步：
前因是什麼？線索在哪裡？推理如何展開？後果又如何改變了整個數學、物理與資訊科學？

這樁「懸案」橫跨近五百年：一個被稱為「不可能」的數 $\sqrt{-1}$，從三次方程的陰影中誕生，在 Argand 的地圖上現形，被 Cauchy 的圍道積分加冕為分析學的皇后，再由 Riemann 的曲面與 Weierstrass 的冪級數開疆拓土——而今天，它藏身於每一張 Mandelbrot 圖、每一次 FFT、與每個量子波函數之中。

## 案件卷宗（歷史年表）

### 虛數誕生（1545–1799）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1545 | Cardano《Ars Magna》：三次方程公式中出現 $\sqrt{-15}$，虛數被迫誕生 | [1545-Cardano虛數.md](1545-Cardano虛數.md) |
| 1572 | Bombelli《L'Algebra》：定義虛數四則運算，為 casus irreducibilis 辨護 | [1572-Bombelli虛數運算.md](1572-Bombelli虛數運算.md) |
| 1748 | Euler 的 $e^{i\theta}=\cos\theta+i\sin\theta$ 與恆等式 $e^{i\pi}+1=0$ | [1748-Euler複數指數與恆等式.md](1748-Euler複數指數與恆等式.md) |
| 1799 | Gauss 博士論文：代數基本定理的幾何式證明，複數合法性確立 | [1799-Gauss代數基本定理.md](1799-Gauss代數基本定理.md) |

### 地圖與大憲章（1806–1844）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1806 | Argand（與 Wessel 1797）以複數平面幾何詮釋虛數：乘法即旋轉 | [1806-Argand複數平面.md](1806-Argand複數平面.md) |
| 1814 | Cauchy 積分定理 $\oint_\gamma f(z)\,dz=0$，複變函數論的大憲章 | [1814-Cauchy積分定理.md](1814-Cauchy積分定理.md) |
| 1826 | Cauchy 積分公式與留數定理，計算積分的強大機器 | [1826-Cauchy留數定理.md](1826-Cauchy留數定理.md) |
| 1843 | Laurent 級數：圓環展開與奇點分類 | [1843-Laurent級數.md](1843-Laurent級數.md) |
| 1844 | Liouville 定理：有界整函數必為常數，超越數論開端 | [1844-Liouville定理.md](1844-Liouville定理.md) |

### Riemann 與 Weierstrass 的兩座大山（1851–1885）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1851 | Riemann 博士論文：解析函數的幾何本質、Riemann 球面 | [1851-Riemann複變函數基礎.md](1851-Riemann複變函數基礎.md) |
| 1857 | Riemann 曲面：多值函數的單值化與虧格 | [1857-Riemann曲面.md](1857-Riemann曲面.md) |
| 1865 | Riemann–Roch 定理 $\ell(D)-\ell(K-D)=\deg D+1-g$ | [1865-RiemannRoch定理.md](1865-RiemannRoch定理.md) |
| 1876 | Weierstrass 的冪級數路線：解析延拓與因子分解 | [1876-Weierstrass解析延拓.md](1876-Weierstrass解析延拓.md) |
| 1879 | Picard 定理：本性奇點取遍所有複數（至多一個例外） | [1879-Picard定理.md](1879-Picard定理.md) |
| 1884 | Mittag-Leffler 定理：極點與主部構造亞純函數 | [1884-MittagLeffler定理.md](1884-MittagLeffler定理.md) |
| 1885 | Weierstrass 逼近定理：連續函數可被多項式一致逼近 | [1885-Weierstrass逼近定理.md](1885-Weierstrass逼近定理.md) |

### 分類與動力系統（1907–1984）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1907 | Poincaré–Koebe 單值化定理：黎曼面分類為球/平面/雙曲盤 | [1907-單值化定理.md](1907-單值化定理.md) |
| 1918 | Fatou 與 Julia 的復動力系統；1980 Mandelbrot 集合 | [1918-JuliaMandelbrot復動力系統.md](1918-JuliaMandelbrot復動力系統.md) |
| 1925 | Nevanlinna 值分布理論 $T(r,f)$ | [1925-Nevanlinna值分布理論.md](1925-Nevanlinna值分布理論.md) |
| 1984 | de Branges 證明 Bieberbach 猜想 $|a_n|\le n$ | [1984-DeBrangesBieberbach猜想.md](1984-DeBrangesBieberbach猜想.md) |

### 現代應用（2020s）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 2020s | 複分析與現代計算：FFT、共形映射、Riemann zeta、勢流 | [2020s-複分析與現代計算.md](2020s-複分析與現代計算.md) |

## 關鍵人物年表

| 年代 | 人物 | 貢獻 |
|------|------|------|
| 1545 | Cardano / Tartaglia | 三次方程公式、虛數誕生 |
| 1572 | Bombelli | 虛數運算規則 |
| 1748 | Leonhard Euler | $e^{i\theta}$、Euler 恆等式 |
| 1799 | Carl Friedrich Gauss | 代數基本定理 |
| 1797/1806 | Wessel / Argand | 複數平面 |
| 1814/1826 | Augustin-Louis Cauchy | 積分定理、積分公式、留數 |
| 1843/1844 | Laurent / Liouville | Laurent 級數、Liouville 定理 |
| 1851/1857 | Bernhard Riemann | 幾何函數論、Riemann 曲面 |
| 1865 | Riemann / Roch | Riemann–Roch 定理 |
| 1876–1885 | Karl Weierstrass | 解析延拓、逼近定理 |
| 1879/1884 | Picard / Mittag-Leffler | 值分布、亞純函數 |
| 1907 | Poincaré / Koebe | 單值化定理 |
| 1918/1980 | Fatou / Julia / Mandelbrot | 復動力系統、分形 |
| 1925 | Rolf Nevanlinna | 值分布理論 |
| 1984 | Louis de Branges | Bieberbach 猜想 |

## 案件主軸：三幕劇

1. **第一幕：現形**（1545–1799）——虛數從三次方程的陰影誕生，經 Euler 的指數公式獲得靈魂、Gauss 的證明獲得戶籍，從「鬼魅」變成公民。
2. **第二幕：登基**（1806–1885）——Argand 的地圖讓複數「看得見」；Cauchy 的圍道積分、Riemann 的曲面、Weierstrass 的冪級數，三條路線把複變函數論建成數學最優美的帝國。
3. **第三幕：遠征**（1879–至今）——Picard 與 Nevanlinna 追問函數「值」的去向，Poincaré–Koebe 完成分類，Julia–Mandelbrot 讓迭代開出分形之花，最終複分析滲透進物理、工程與計算機科學的每個角落。

## 核心數學一覽

- Euler 公式：$e^{i\theta} = \cos\theta + i\sin\theta$
- Cauchy–Riemann 方程：$\dfrac{\partial u}{\partial x} = \dfrac{\partial v}{\partial y},\quad \dfrac{\partial u}{\partial y} = -\dfrac{\partial v}{\partial x}$
- Cauchy 積分公式：$f(a) = \dfrac{1}{2\pi i}\displaystyle\oint_\gamma \frac{f(z)}{z-a}\,dz$
- Laurent 級數：$f(z) = \displaystyle\sum_{n=-\infty}^{\infty} a_n (z-a)^n$
- Riemann–Roch：$\ell(D) - \ell(K-D) = \deg D + 1 - g$
- 單值化：單連通黎曼面 $\cong \hat{\mathbb{C}}$、$\mathbb{C}$ 或 $\mathbb{H}$
- Mandelbrot 集：$M = \{c \in \mathbb{C} : \lim_{n\to\infty} |z_n| \neq \infty,\ z_{n+1}=z_n^2+c\}$
