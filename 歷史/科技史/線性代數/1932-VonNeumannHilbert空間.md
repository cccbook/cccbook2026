# 1932 — Von Neumann Hilbert 空間

## 案件摘要
1932 年，John von Neumann 出版《Mathematische Grundlagen der Quantenmechanik》（量子力學的數學基礎），把線性代數推廣到**無窮維**：在 Hilbert 空間 $\mathcal{H}$ 中，內積 $\langle x, y\rangle$ 取代點積，自伴算子的譜理論取代特徵值分解。Heisenberg 的矩陣力學與 Schrödinger 的波動力學被統一在同一個架構下——矩陣力學只是有限維的片段，波動力學只是座標表象。量子力學的嚴格基礎，就此結案。

## 前因 -- 為什麼會有這個案子
- **Fredholm 1903**：Erik Fredholm 研究積分方程
  $$\phi(x) - \lambda\int K(x, y)\phi(y)\,dy = f(x)$$
  發現其理論與線性代數方程組驚人地相似（Fredholm 二擇一）：無窮維問題「模仿」有限維。這是無窮維線性代數的第一條線索。
- **Hilbert 1906**：David Hilbert 把 Fredholm 理論抽象化，研究無窮平方和收斂的序列空間 $\ell^2$（內積 $\langle x, y\rangle = \sum x_n y_n$），並對積分算子提出**譜理論**——特徵值概念推廣到無窮維。但 Hilbert 只處理「有界算子」，且他堅持用序列而非幾何語言。
- **物理的緊急需求**：1925 年 Heisenberg 矩陣力學橫空出世——物理量用**無窮矩陣**表示，能量的可能值是矩陣的特徵值。但這些矩陣常常是**無界的**（位置算子 $x$ 的特徵值鋪滿整個實數軸），連「特徵向量」都不在 Hilbert 空間裡（要用 Dirac 的 $\delta$ 函數勉強湊合）。
- **測不準原理 1927**：Heisenberg 用 $[x, p] = i\hbar$ 論證測不準，但交換子的數學意義（兩個無界算子如何相乘？定義域呢？）完全沒有根據。
- von Neumann——Hilbert 的學生、二十歲就精通集合論的天才——接下這樁懸案。他的問題：**量子力學的數學骨架到底是什麼？**

## 線索與推理 -- 數學式、程式、理論

### 線索一：Hilbert 空間——把 $\ell^2$ 變成幾何
von Neumann 的第一個動作：把 Hilbert 的序列空間幾何化。**Hilbert 空間**是完備內積空間：向量空間 $\mathcal{H}$ 配上內積 $\langle \cdot, \cdot\rangle$，且在誘導的範數 $\|x\| = \sqrt{\langle x, x\rangle}$ 下完備。典型例子：

$$\ell^2 = \left\{ x : \sum_{n=1}^\infty |x_n|^2 < \infty \right\}, \qquad L^2(\mathbb{R}) = \left\{ \psi : \int |\psi|^2 < \infty \right\}$$

關鍵區分：**維度**。有限維時所有 Hilbert 空間同構於 $\mathbb{C}^n$，矩陣力學夠用；但 $L^2(\mathbb{R})$ 是**可分無窮維**，而量子力學中位置算子的「廣義特徵向量」根本不在 $\mathcal{H}$ 內——譜不再是點的集合。

### 線索二：自伴算子與譜定理——無窮維的特徵值分解
von Neumann 的核心武器：**自伴（self-adjoint）算子**。無界算子 $A$ 必須指定定義域 $\mathcal{D}(A)$；$A$ 自伴意味着 $A = A^*$ 且定義域完全吻合——這比「對稱」更嚴格，卻是譜定理成立的精確條件。

**譜定理（von Neumann, 1929–30）**：自伴算子 $A$ 對應一個投影值測度（projection-valued measure）$E_A$，使

$$A = \int_{\sigma(A)} \lambda \, dE_A(\lambda)$$

其中 $\sigma(A)$ 是**譜**（不只是特徵值，還包括連續譜）。幾何意義：$E_A(B)$ 是「測量結果落在集合 $B$ 中」的投影——**量子測量的數學，就是投影算子的分解**。這一舉統一了矩陣力學（純點譜 → 矩陣對角化）與波動力學（連續譜 → 積分表現）：兩者都是同一譜定理的特例。

### 線索三：正交投影——測量與期望值的幾何
量子力學的基本機制在 von Neumann 的架構下變成純幾何：

- **態** = 單位向量 $\psi \in \mathcal{H}$（差一相位等價）。
- **測量** = 對算子 $A$ 的譜投影 $E_A(B)$；結果落在 $B$ 的機率是 $\|E_A(B)\psi\|^2$。
- **期望值** = $\langle \psi, A\psi\rangle$。
- **投影算子** $P$ 滿足 $P^2 = P = P^*$——「是/否」問題的數學化身。von Neumann 甚至用投影格（lattice of projections）分析量子邏輯：**量子力學的命題結構不是分配格**，這就是量子性與經典性的代數分野。

### 程式碼範例：Hilbert 空間的有限維類比——正交投影與譜分解
```python
import numpy as np

# 有限維 Hilbert 空間 C^4 的類比：內積、投影、譜定理
rng = np.random.default_rng(0)

# Hermitian（自伴的有限維類比）算子
A = rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4))
H = (A + A.conj().T) / 2                  # A† A：Hermitian
print("Hermitian? ", np.allclose(H, H.conj().T))

# 內積 <x, y>（共軛線性於第一個參數，物理慣例）
x = rng.normal(size=4) + 1j * rng.normal(size=4)
y = rng.normal(size=4) + 1j * rng.normal(size=4)
inner = lambda u, v: np.vdot(u, v)        # <u,v> = Σ conj(u_n) v_n
print("<x,y> =", np.round(inner(x, y), 4),
      "  <y,x> =", np.round(inner(y, x), 4))  # 共軛對稱

# 譜定理（有限維）：H = Σ λ_k P_k，λ 為實數，P_k 為正交投影
vals, vecs = np.linalg.eigh(H)            # 特徵值實數、特徵向量正交
print("特徵值（實數） =", np.round(vals, 4))
print("正交性 <v_i, v_j> ≈ I? ", np.allclose(vecs.conj().T @ vecs, np.eye(4)))

# 投影算子 P_k = v_k v_k†：滿足 P² = P = P†
k = 2
P = np.outer(vecs[:, k], vecs[:, k].conj())
print("P² = P? ", np.allclose(P @ P, P), "  P† = P? ", np.allclose(P.conj().T, P))

# 重建 H = Σ λ_k P_k（譜定理）
H_rebuilt = sum(vals[m] * np.outer(vecs[:, m], vecs[:, m].conj()) for m in range(4))
print("譜定理重建 H? ", np.allclose(H_rebuilt, H))

# 期望值與 Born 規則：||P ψ||² = <ψ, P ψ>
psi = x / np.linalg.norm(x)
print("機率（第 k 個特徵值） =", round(abs(inner(vecs[:, k], psi))**2, 4),
      "  <ψ,Pψ> =", np.round(np.real(inner(psi, P @ psi)), 4))
```

輸出顯示：Hermitian 算子特徵值為實數、特徵向量正交，$H = \sum_k \lambda_k P_k$ 精確重建，且 Born 機率 $\|P_k\psi\|^2 = \langle \psi, P_k\psi\rangle$——von Neumann 譜定理與量子測量的有限維縮影。

## 結案 -- 後果與影響
- **量子力學的嚴格基礎**：Heisenberg 與 Schrödinger 的兩套表述在 Hilbert 空間中統一；測不準原理獲得嚴格證明（$[A, B] \ne 0$ 時無法同時對角化），Dirac 的 $\delta$ 函數被投影值測度取代（懸置爭議，直到 Gelfand 1940 年代的 rigged Hilbert space 才正式收編）。
- **泛函分析誕生**：von Neumann 的譜定理（1929–30 系列論文）與 Banach、Hahn 等人的工作共同奠定泛函分析；**算子代數**（1930 年代的 von Neumann 代數，$W^*$-代數）成為獨立領域。
- **von Neumann 代數與量子邏輯**：投影格的非分配性開啟了量子邏輯研究；因子分類（type I/II/III）至今仍是活躍領域。
- **現代應用**：量子計算（態向量、么正算子、測量投影正是這套語言）、量子資訊的密度矩陣理論、PDE 理論中的 Sobolev 空間，全是 Hilbert 空間框架的後代。
- 線性代數的最後一塊拼圖：從 Möbius 的點組合、Weierstrass 的初等因子、Ricci 的下標語言，到 von Neumann 的無窮維 Hilbert 空間——「向量空間」的故事跨越一個世紀，就此完結。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| John von Neumann | 案件主嫌：Hilbert 空間與譜定理（1932） |
| David Hilbert | 譜理論的開創者（1906） |
| Erik Fredholm | 積分方程的無窭維線性代數（1903） |
| Werner Heisenberg | 矩陣力學提出物理需求（1925） |
| Paul Dirac | $\delta$ 函數與形式化表述（1930） |

- J. von Neumann, *Mathematische Grundlagen der Quantenmechanik*, Springer (1932)。
- J. von Neumann, *Allgemeine Eigenwerttheorie Hermitescher Funktionaloperatoren*, Math. Ann. **102** (1929–30)：無界自伴算子譜定理。
- D. Hilbert, *Grundzüge einer allgemeinen Theorie der linearen Integralgleichungen* (1912)：1904–1910 論文的結集。
