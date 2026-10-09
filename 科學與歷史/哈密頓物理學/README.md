# 哈密頓物理學史 -- AI 偵探風格

以「推理探案」的方式，追查哈密頓力學從 Newton《原理》到今日幾何數值積分與波動力學誕生的每一步：
前因是什麼？線索在哪裡？推理如何展開？後果又如何改變了整個物理與數學？

哈密頓物理學的核心，是「能量」取代「力」成為主角：

- **Newton**：$\vec F = m\vec a$，向量式、力學觀點。
- **Lagrange**：以「廣義座標」與作用量 $L = T - V$ 描述系統，解析式觀點。
- **Hamilton**：以「相空間」與正則方程 $\dot q = \partial H/\partial p,\ \dot p = -\partial H/\partial q$ 描述系統，幾何觀點。

三者等價，但 Hamilton 形式最能顯露結構：辛幾何、正則變換、可積性、混沌，乃至量子力學，都從這裡生長出來。

## 案件卷宗（歷史年表）

### 前奏：從力到能量（1687–1744）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1687 | Newton《自然哲學的數學原理》發表，$\vec F = m\vec a$ 誕生 | [1687-Newton原理.md](1687-Newton原理.md) |
| 1736 | Euler 出版《力學》，以分析（微積分）方法重寫力學，並提出動量守恆的分析形式 | [1736-Euler力學.md](1736-Euler力學.md) |
| 1744 | Maupertuis 提出最小作用量原理 $\delta \int p\,dq = 0$ | [1744-Maupertuis最小作用量.md](1744-Maupertuis最小作用量.md) |

### Lagrange 的解析革命（1755–1788）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1755 | 19 歲的 Lagrange 寫信 Euler，提出「變分法的一般方法」（Euler–Lagrange 方程雛形） | [1755-Lagrange變分法.md](1755-Lagrange變分法.md) |
| 1788 | Lagrange 出版《分析力學》(Mécanique analytique)，全書無一張圖，Euler–Lagrange 方程正式定名 | [1788-分析力學.md](1788-分析力學.md) |

### Hamilton 的正則架構（1834–1843）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1834 | Hamilton 發表《論力學中的一般方法》，提出正則方程與「特徵函數」（Hamiltonian 雛形） | [1834-Hamilton正則方程.md](1834-Hamilton正則方程.md) |
| 1835 | Hamilton 完成特徵函數理論，將光學與力學統一（波動–粒子對應的預言） | [1835-Hamilton特徵函數.md](1835-Hamilton特徵函數.md) |
| 1837 | Jacobi 發展 Hamilton–Jacobi 方程：找到變換使 $H$ 變為常數，運動方程「完全積出」 | [1837-HamiltonJacobi方程.md](1837-HamiltonJacobi方程.md) |
| 1843 | Jacobi 提出正則變換理論與「最後乘子」，奠定相空間幾何的基礎 | [1843-Jacobi正則變換.md](1843-Jacobi正則變換.md) |

### 混沌與可積性的危機（1890–1963）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1890 | Poincaré 研究三體問題，發現同宿纏結與「不可積性」，混沌第一次現形 | [1890-Poincare三體問題.md](1890-Poincare三體問題.md) |
| 1918 | Noether 定理：對稱性 ⇔ 守恆量，Hamilton/Lagrange 形式的深層結構被揭開 | [1918-Noether定理.md](1918-Noether定理.md) |
| 1954 | Kolmogorov 提出 KAM 定理構想：近可積系統中多數不變環面存活 | [1954-KAM定理.md](1954-KAM定理.md) |
| 1955 | Fermi–Pasta–Ulam–Tsingou 實驗（MANIAC 電腦模擬非線性晶格），發現能量不均分、復發現象 | [1955-FPUT實驗.md](1955-FPUT實驗.md) |
| 1963 | Arnold 與 Moser 各自完成 KAM 定理證明；同年 Hénon–Heiles 發現典型混沌相圖 | [1963-HeonHeiles混沌.md](1963-HeonHeiles混沌.md) |

### 從哈密頓到量子（1925–1948）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1925 | Heisenberg 矩陣力學：正則對易關係 $[q,p] = i\hbar$ 取代正則方程 | [1925-矩陣力學.md](1925-矩陣力學.md) |
| 1926 | Schrödinger 從 Hamilton–Jacobi 方程出發，推導出波動力學 $\hat H \psi = i\hbar \partial_t \psi$ | [1926-波動力學誕生.md](1926-波動力學誕生.md) |
| 1948 | Feynman 路徑積分：作用量 $S = \int L\,dt$ 直接成為量子振幅的相位 $e^{iS/\hbar}$ | [1948-Feynman路徑積分.md](1948-Feynman路徑積分.md) |

### 幾何數值積分與遺產（1983–至今）

| 年份 | 事件 | 檔案 |
|------|------|------|
| 1983 | Ruth 提出辛積分器：保結構的數值方法，長期模擬不漂移 | [1983-辛積分器.md](1983-辛積分器.md) |
| 1988 | Forest–Ruth 蛙跳式四階辛積分器普及；太陽系長期模擬（如数字 Orrery）成為可能 | [1988-幾何數值積分.md](1988-幾何數值積分.md) |

## 關鍵人物速寫

| 人物 | 貢獻 |
|------|------|
| Newton | 力的三定律、微積分 |
| Euler | 分析力學先驅、變分法 $\delta \int f\,dx = 0$ 的 Euler 方程 |
| Maupertuis | 最小作用量原理 |
| Lagrange | Euler–Lagrange 方程、《分析力學》 |
| Hamilton | 正則方程、特徵函數、光學–力學類比 |
| Jacobi | Hamilton–Jacobi 方程、正則變換 |
| Poincaré | 三體問題、混沌、同宿纏結 |
| Noether | 對稱性與守恆律 |
| Kolmogorov / Arnold / Moser | KAM 定理 |
| Schrödinger / Heisenberg / Feynman | 量子力學三條路，皆源自哈密頓結構 |

## 主線結案陳詞

整部哈密頓物理學史，是一場「表示法」的革命史：

1. **力 → 能量**（Newton → Maupertuis → Lagrange）：描述系統不再需要向量分解，只要一個純量函數 $L$ 與變分原理。
2. **能量 → 相空間**（Hamilton → Jacobi）：狀態變成 $(q,p)$ 點，動力學變成流，守恆律變成幾何（辛結構）。
3. **相空間 → 量子**（Schrödinger / Heisenberg / Feynman）：三條通往量子力學的路，全是哈密頓結構的變奏。
4. **相空間 → 混沌與計算**（Poincaré → KAM → FPUT → 辛積分器）：當不可積性現形，電腦與保結構演算法成為新的偵探工具。
