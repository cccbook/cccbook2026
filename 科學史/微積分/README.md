# 微積分史 -- AI 偵探風格

以「推理探案」的方式，追查微積分從 Archimedes 的窮竭法到今日深度學習的自動微分，每一步的前因是什麼？線索在哪裡？推理如何展開？後果又如何重塑了整個數學、物理與資訊科學？

微積分這樁「懸案」橫跨兩千餘年：古希臘人看見了面積與體積的謎題，十七世紀 Newton 與 Leibniz 各自破案卻爭執不修，十九世紀 Cauchy、Weierstrass、Dedekind 重新驗證每一條證據，二十世紀 Lebesgue、Robinson 再度翻案——而今天，微積分化身為自動微分，藏身於每一行深度學習程式碼之中。

## 案件卷宗（歷史年表）

### 遠古與前夜（前 250–1666）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 前250 | Archimedes 以窮竭法求拋物線弓形面積與圓周率，積分思想的遠古原型 | [前250-Archimedes窮竭法.md](前250-Archimedes窮竭法.md) |
| 1635 | Cavalieri 出版《不可分量的幾何》，提出 Cavalieri 原理與 $\int x^n dx$ 雛形 | [1635-Cavalieri不可分量法.md](1635-Cavalieri不可分量法.md) |
| 1637 | Fermat 以「擬等法」求極值與切線，微分思想原型；Descartes 出版《幾何學》 | [1637-Fermat極大極小法.md](1637-Fermat極大極小法.md) |
| 1655 | Wallis 出版《無窮算術》，以數列插值求 $4/\pi$、猜想廣義二項式 | [1655-Wallis無窮分析.md](1655-Wallis無窮分析.md) |
| 1665 | Newton 提出廣義二項式定理 $(1+x)^\alpha$ 級數，由插值得出面積 | [1665-Newton廣義二項式定理.md](1665-Newton廣義二項式定理.md) |
| 1666 | Newton 在瘟疫年間創立流數術（fluxions），正反流數問題與基本定理雛形 | [1666-Newton流數術.md](1666-Newton流數術.md) |

### 微積分誕生（1673–1697）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1673 | Leibniz 在巴黎研究特徵三角形，發明 $dx$、$dy$、$\int$ 記號 | [1673-Leibniz特徵三角形.md](1673-Leibniz特徵三角形.md) |
| 1684 | Leibniz 發表〈Nova Methodus〉，史上第一篇微積分論文 | [1684-Leibniz發表微積分.md](1684-Leibniz發表微積分.md) |
| 1687 | Newton 出版《Principia》，以幾何極限論述萬有引力與軌道力學 | [1687-Newton原理與微積分.md](1687-Newton原理與微積分.md) |
| 1696 | L'Hôpital 出版第一本微積分教科書，L'Hôpital 法則（實為 Bernoulli 手筆） | [1696-LHopital法則.md](1696-LHopital法則.md) |
| 1697 | Bernoulli 提出最速降線問題，擺線為解，變分法誕生 | [1697-Bernoulli最速降線.md](1697-Bernoulli最速降線.md) |

### Euler 世紀（1715–1797）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1715 | Taylor 出版《增量法》，泰勒級數 $f(x)=\sum \frac{f^{(n)}(a)}{n!}(x-a)^n$ | [1715-Taylor級數.md](1715-Taylor級數.md) |
| 1744 | Euler 出版《求曲線的方法》，系統化變分法 | [1744-Euler變分法.md](1744-Euler變分法.md) |
| 1748 | Euler 出版《無窮分析引論》：現代函數概念、$e$、Euler 恆等式 | [1748-Euler函數概念與e.md](1748-Euler函數概念與e.md) |
| 1797 | Lagrange 出版《解析函數論》，以冪級數重建微積分 | [1797-Lagrange解析函數論.md](1797-Lagrange解析函數論.md) |

### 嚴格化革命（1821–1874）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1821 | Cauchy 出版《分析教程》，極限與連續的現代定義 | [1821-Cauchy極限與連續.md](1821-Cauchy極限與連續.md) |
| 1823 | Cauchy 嚴格定義定積分為和的極限，證明微積分基本定理 | [1823-Cauchy定積分.md](1823-Cauchy定積分.md) |
| 1829 | Dirichlet 分析 Fourier 級數收斂，提出處處不連續的 Dirichlet 函數 | [1829-Dirichlet函數概念.md](1829-Dirichlet函數概念.md) |
| 1854 | Riemann 就職論文：黎曼積分、可積的病態函數、級數重排定理 | [1854-Riemann定積分與級數.md](1854-Riemann定積分與級數.md) |
| 1872 | Weierstrass 提出處處連續處處不可微函數，$\varepsilon$-$\delta$ 嚴格化完成 | [1872-Weierstrass處處連續處處不可微.md](1872-Weierstrass處處連續處處不可微.md) |
| 1872 | Dedekind 以「切割」嚴格定義實數，分析算術化 | [1872-Dedekind實數切割.md](1872-Dedekind實數切割.md) |

### 集合論與現代分析（1874–1902）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1874 | Cantor 證明實數不可數，無窮分層 $\aleph_0 < 2^{\aleph_0}$ | [1874-Cantor不可數無窮.md](1874-Cantor不可數無窮.md) |
| 1881 | Heaviside 運算微積分：微分當代數符號、Laplace 變換前身 | [1881-Heaviside運算微積分.md](1881-Heaviside運算微積分.md) |
| 1902 | Lebesgue 測度與積分 $\int f\,d\mu$，實分析與機率公理化的基礎 | [1902-Lebesgue測度與積分.md](1902-Lebesgue測度與積分.md) |

### 無窮小重生與計算時代（1960–至今）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1960 | Robinson 以模型論建立非標準分析，Leibniz 的無窮小被平反 | [1960-Robinson非標準分析.md](1960-Robinson非標準分析.md) |
| 2020s | 符號計算（SymPy/Mathematica）與自動微分，深度學習的微積分基礎設施 | [2020s-符號計算與自動微分.md](2020s-符號計算與自動微分.md) |

## 關鍵人物年表

| 年代 | 人物 | 貢獻 |
|------|------|------|
| 前250 | Archimedes | 窮竭法、拋物線面積、圓周率 |
| 1635 | Cavalieri | 不可分量原理 |
| 1637 | Fermat / Descartes | 極值與切線、解析幾何 |
| 1655 | John Wallis | 無窮算術、插值 |
| 1665/1666 | Isaac Newton | 二項式定理、流數術、《原理》 |
| 1673/1684 | Gottfried Leibniz | 特徵三角形、微積分記號與論文 |
| 1696 | L'Hôpital / J. Bernoulli | 第一本教科書、L'Hôpital 法則 |
| 1697 | Johann Bernoulli | 最速降線、變分法前夜 |
| 1715 | Brook Taylor | 泰勒級數 |
| 1744/1748 | Leonhard Euler | 變分法、函數概念、$e$ |
| 1797 | Joseph-Louis Lagrange | 解析函數論、解析力學 |
| 1821/1823 | Augustin-Louis Cauchy | 極限、連續、定積分 |
| 1829 | Peter Dirichlet | Fourier 級數收斂、函數革命 |
| 1854 | Bernhard Riemann | 黎曼積分 |
| 1872 | Karl Weierstrass | 處處不可微函數、$\varepsilon$-$\delta$ |
| 1872 | Richard Dedekind | 實數切割 |
| 1874 | Georg Cantor | 不可數無窮、集合論 |
| 1881 | Oliver Heaviside | 運算微積分 |
| 1902 | Henri Lebesgue | 測度與積分 |
| 1960 | Abraham Robinson | 非標準分析 |
| 2020s | 機器學習社群 | 自動微分、梯度下降 |

## 案件主軸：三幕劇

1. **第一幕：發現**（前250–1687）——從 Archimedes 的窮竭到 Newton 的流數，面積、切線、極值三大謎題逐一偵破，最終匯流成「微積分基本定理」：微分與積分互為逆運算。
2. **第二幕：驗證**（1821–1872）——Cauchy 的極限、Weierstrass 的 $\varepsilon$-$\delta$、Dedekind 的切割，把直覺的幾何「無窮小」換成嚴格的算術邏輯，連續與可微的病態案例震驚全場。
3. **第三幕：翻案與重生**（1874–至今）——Cantor 的集合論、Lebesgue 的測度積分擴張了戰場；Robinson 平反了 Leibniz 的無窮小；自動微分讓微積分成為深度學習的引擎。

## 核心數學一覽

- 微積分基本定理：$\dfrac{d}{dx}\displaystyle\int_a^x f(t)\,dt = f(x)$
- 導數定義：$f'(x) = \displaystyle\lim_{h\to 0}\frac{f(x+h)-f(x)}{h}$
- Riemann 積分：$\displaystyle\int_a^b f = \lim_{\|P\|\to 0}\sum_i f(\xi_i)\Delta x_i$
- Lebesgue 積分：$\displaystyle\int f\,d\mu = \lim_n \int \phi_n\,d\mu$（單調收斂）
- 梯度下降：$\theta_{n+1} = \theta_n - \eta\nabla L(\theta_n)$
