# 1835 - Hamilton 特徵函數——光學與力學的統一

## 案件摘要
1835 年，Hamilton 發表《論力學中的一般方法，第二篇》，完成「特徵函數」(characteristic function) 理論。
他發現：光學中的費馬原理與力學中的最小作用量原理，**數學結構完全相同**——
兩者都由一個純量函數 $S$（光學中的 eikonal、力學中的作用量）主導：
$$S = \int L\,dt, \qquad \frac{\partial S}{\partial q_i} = p_i$$
光線與粒子軌跡，是同一個「波前」的特徵線。這個類比在 1835 年只是數學巧合，
但 90 年後（1926 年）Schrödinger 沿著它找到波動力學——**粒子本來就是波**（見 [1926-波動力學誕生.md](1926-波動力學誕生.md)）。

## 前因
- **Hamilton 的光學三部曲（1824–1833）**：《光線系統理論》(Theory of Systems of Rays, 1827) 中已發明特徵函數：
  對光學系統定義 $V(x, y, z)$（從起點到該點的光程），光線方向由 $\nabla V$ 決定。
- **雙軸晶體的圓錐折射**：Hamilton 從特徵函數的數學**預言**了圓錐折射（conical refraction），1833 年被 Humphrey Lloyd 實驗證實——純數學推理擊出實驗鐵證，Hamilton 一戰成名。
- **1834 年正則方程**：力學的相空間架構已就位（見 [1834-Hamilton正則方程.md](1834-Hamilton正則方程.md)）。
- **費馬 vs 莫佩圖伊的平行**：兩條變分原理（見 [1744-Maupertuis最小作用量.md](1744-Maupertuis最小作用量.md)）的對稱性等待統一。

## 線索與推理

### 特徵函數的定義與核心性質
沿真實軌跡定義作用量函數：
$$S(q, t; \alpha) = \int_{t_0}^{t} L\,dt$$
（$\alpha$ 是標記不同軌跡的積分常數。）對終點微分：
$$\boxed{\ \frac{\partial S}{\partial q_i} = p_i, \qquad \frac{\partial S}{\partial t} = -H\ }$$
**作用量的梯度 = 動量**。這是整個理論最關鍵的一條式子。

### 光學–力學類比表
| 光學（Hamilton 1827） | 力學（Hamilton 1834–35） |
|---|---|
| 光程（eikonal）$V$ | 作用量 $S$ |
| 光線方向 $\nabla V$ | 動量 $\nabla S = p$ |
| 等光程面（波前）| 等作用量面 $S = \text{const}$ |
| 費馬原理 $\delta\int n\,ds = 0$ | 最小作用量 $\delta\int L\,dt = 0$ |
| 折射率 $n$ | 動量大小 $p$（或 $\sqrt{2m(E-V)}$）|
| 光線 = 波前的法線族 | 軌跡 = 等作用量面的正交軌跡族 |

### 特徵線： $S$ 的方程
$S$ 滿足（今日稱 Hamilton–Jacobi 方程的前身）：
$$H\left(q, \frac{\partial S}{\partial q}\right) = E \quad\Longleftrightarrow\quad \frac{1}{2m}\left(\nabla S\right)^2 + V(q) = E$$
這正是**幾何光學的 eikonal 方程** $\left(\nabla V\right)^2 = n^2$ 的力學版。
波前的傳播速度（rays 的正交速度）為：
$$u = \frac{E}{|\nabla S|} = \frac{E}{\sqrt{2m(E - V)}} \propto \frac{1}{p}$$
**慢波對應大動量**——這個反比關係正是日後 de Broglie 關係 $\lambda = h/p$ 的經典影子。

### 預言的悲劇性伏筆
Hamilton 親手寫下了「粒子軌跡是波前特徵線」的數學，卻沒有追問：
**波前的波動方程是什麼？** 幾何光學是波動光學的短波長極限；
同理，牛頓力學會不會是某個「物質波動力學」的短波長極限？
這個問題要等 de Broglie（1924）與 Schrödinger（1926）來回答。

## 結案
- 特徵函數理論完成；光學與力學在同一數學框架下統一，Hamilton 稱之為「方法的一般化」。
- 1837 年 Jacobi 把 $S$ 的方程發展為完全積分法（見 [1837-HamiltonJacobi方程.md](1837-HamiltonJacobi方程.md)）。
- 史上最長的伏筆：1835 年的數學巧合，在 1926 年成為量子力學的誕生證明——**偵探 Hamilton 留下了指紋，凶手在 91 年後現形**。
