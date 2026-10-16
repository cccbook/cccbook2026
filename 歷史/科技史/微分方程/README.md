# 微分方程的歷史年表（科學史）

> 微分方程是「以方程式描述未知函數與其導數關係」的數學分支，從 17 世紀牛頓、萊布尼茲發明微積分後隨之誕生，成為描述自然律（力學、熱、波、電磁、量子、混沌）的核心語言。
>
> 本書以「推理探案」的方式，為每個歷史事件寫一篇 wiki，包含前因後果、數學式、理論與程式。每篇檔名以年份開頭。

## 目錄（Wiki 書篇目）

### 第一幕：誕生與常微分方程（1690s–1740s）

| 年份 | 事件 | Wiki |
|------|------|------|
| 1690 | Jacob Bernoulli 以微分方程解等時曲線，微積分首次用於力學問題 | [1690-JacobBernoulli等時曲線.md](1690-JacobBernoulli等時曲線.md) |
| 1695 | Jacob Bernoulli 提出 Bernoulli 方程 $y' + P(x)y = Q(x)y^n$，並以變換化為線性 | [1695-Bernoulli方程.md](1695-Bernoulli方程.md) |
| 1696 | Johann Bernoulli 提出「最速降線問題」挑戰全歐洲，催生變分法 | [1696-最速降線問題.md](1696-最速降線問題.md) |
| 1727 | Euler 系統化常微分方程，建立積分因子與線性方程理論 | [1727-Euler常微分方程.md](1727-Euler常微分方程.md) |
| 1739 | Clairaut 研究隱式解與奇解，發現「包絡線」現象 | [1739-Clairaut隱式解與奇解.md](1739-Clairaut隱式解與奇解.md) |

### 第二幕：偏微分方程與數學物理（1747–1810s）

| 年份 | 事件 | Wiki |
|------|------|------|
| 1747 | d'Alembert 導出波動方程 $\frac{\partial^2 u}{\partial t^2} = c^2 \frac{\partial^2 u}{\partial x^2}$，弦振動之謎 | [1747-dAlembert波動方程.md](1747-dAlembert波動方程.md) |
| 1755 | Euler 導出理想流體力學方程組 | [1755-Euler流體力學方程.md](1755-Euler流體力學方程.md) |
| 1763 | d'Alembert、Euler、Daniel Bernoulli 關於三角級數能否代表任意函數的大辯論 | [1763-三角級數大辯論.md](1763-三角級數大辯論.md) |
| 1782 | Laplace 提位勢方程 $\nabla^2 V = 0$，開啟位勢理論 | [1782-Laplace位勢方程.md](1782-Laplace位勢方程.md) |
| 1788 | Lagrange《分析力學》以廣義座標與 Lagrange 方程重寫全部力學 | [1788-Lagrange分析力學.md](1788-Lagrange分析力學.md) |

### 第三幕：嚴格化與經典理論（1812–1890s）

| 年份 | 事件 | Wiki |
|------|------|------|
| 1812 | Gauss 研究超幾何級數並處理調和函數的邊值問題 | [1812-Gauss與超幾何函數.md](1812-Gauss與超幾何函數.md) |
| 1822 | Fourier《熱的解析理論》：任意函數可展開為三角級數，熱傳導方程 | [1822-Fourier熱傳導與級數之謎.md](1822-Fourier熱傳導與級數之謎.md) |
| 1824 | Cauchy 首次證明常微分方程解的存在性與唯一性 | [1824-Cauchy存在性定理.md](1824-Cauchy存在性定理.md) |
| 1828 | Green 提出 Green 函數，將邊值問題化為積分表示 | [1828-Green函數.md](1828-Green函數.md) |
| 1834 | Hamilton 提出正則方程與最小作用量原理的變分形式 | [1834-Hamilton正則方程.md](1834-Hamilton正則方程.md) |
| 1838 | Jacobi 完成 Hamilton-Jacobi 方程理論，找到積分捷徑 | [1838-Jacobi與Hamilton-Jacobi方程.md](1838-Jacobi與Hamilton-Jacobi方程.md) |
| 1841 | Liouville 證明 Riccati 方程一般情況無初等解，開啟「可積性」研究 | [1841-Liouville可積性之謎.md](1841-Liouville可積性之謎.md) |
| 1858 | Dedekind/Weierstrass 時代的 Sturm-Liouville 理論與本徵值問題成形 | [1858-SturmLiouville理論.md](1858-SturmLiouville理論.md) |
| 1886 | Poincaré 研究三體問題，發現積分不變量不足，無法求解 | [1886-Poincare三體問題.md](1886-Poincare三體問題.md) |
| 1890 | Poincaré 發現同宿軌道與混沌，開創微分方程定性理論（動態系統） | [1890-Poincare定性理論與混沌.md](1890-Poincare定性理論與混沌.md) |

### 第四幕：二十世紀與計算時代（1900–至今）

| 年份 | 事件 | Wiki |
|------|------|------|
| 1900 | Hilbert 在巴黎數學家大會提出 23 個問題，其中多個與微分方程相關 | [1900-Hilbert與微分方程問題.md](1900-Hilbert與微分方程問題.md) |
| 1926 | Schrödinger 提出波動力學方程 $i\hbar \frac{\partial \psi}{\partial t} = \hat{H}\psi$ | [1926-Schrodinger方程.md](1926-Schrodinger方程.md) |
| 1927 | van der Pol 以電路實驗發現極限環振盪，成為非線性振動典範 | [1927-van_der_Pol振盪子.md](1927-van_der_Pol振盪子.md) |
| 1952 | Courant 提出有限元素法思想，數值求解 PDE 的工程革命 | [1952-有限元素法.md](1952-有限元素法.md) |
| 1963 | Lorenz 以三個變數的簡化對流方程發現蝴蝶效應，混沌學誕生 | [1963-Lorenz混沌與蝴蝶效應.md](1963-Lorenz混沌與蝴蝶效應.md) |
| 1975 | 數值軟體（Fortran 庫至 SciPy）普及，微分方程數值解成為大眾工具 | [1975-數值解與SciPy.md](1975-數值解與SciPy.md) |

## 因果鏈總覽

```
微積分誕生 (1665-1684)
    │
    ├─ 等時曲線 (1690) ── Bernoulli方程 (1695) ── Euler線性理論 (1727)
    │                                              │
    └─ 最速降線 (1696) ── 變分法 ── Euler-Lagrange (1744/1788) ── Hamilton (1834) ── Jacobi (1838)
    │                                                      │
    │                                                      └─ 量子力學 Schrödinger (1926)
    │
    ├─ 波動方程 (1747) ── 三角級數大辯論 (1763) ── Fourier級數 (1822) ── 函數概念嚴格化
    │                                                      │
    │                                                      └─ Sturm-Liouville (1858) ── 本徵值/譜理論
    │
    ├─ 位勢方程 (1782) ── Green函數 (1828) ── 邊值問題理論
    │
    ├─ Cauchy存在性 (1824) ── 嚴格化浪潮
    │         │
    │         └─ Liouville不可積性 (1841) ── 可積性理論 ── Poincaré三體 (1886)
    │                                                            │
    │                                                            └─ 混沌定性理論 (1890) ── Lorenz (1963)
    │
    └─ 數值方法 ── 有限元素法 (1952) ── 數值軟體/SciPy (1975)
```

## 寫作方式說明

每篇 wiki 採「推理探案」結構：

1. **案發現場（前因）**：當時的未解之謎是什麼？誰遇到的？為何重要？
2. **偵查過程（推理）**：數學家如何思考？關鍵靈感為何？逐步推導核心數學式。
3. **結案報告（後果）**：謎題如何被解？留下什麼遺產？影響了哪些後續發展？
4. **證據與工具**：數學式、理論推導，以及 Python 程式（數值解示範）。
