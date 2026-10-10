# 1926-Schrodinger與譜論

## 案件檔案表

| 項目 | 內容 |
|------|------|
| 案發年份 | 1926 |
| 主偵探 | John von Neumann（接案人） |
| 報案人 | Erwin Schrödinger |
| 案發地點 | Zürich → Göttingen / Berlin |
| 案件類型 | 物理理論等價性之謎 → 無界算子譜論 |
| 關鍵證物 | Fourier 變換 $U$ 把位置表象映到動量表象；Schrödinger 方程的 Hamilton 算子 $H$ |
| 涉案對象 | 矩陣力學（Heisenberg 1925）vs 波動力學（Schrödinger 1926） |
| 案件地位 | 量子力學數學基礎的起點，無界算子理論的誕生現場 |
| 後續影響 | von Neumann 譜定理（1929–1930）、《量子力學的數學基礎》（1932） |

## 案發現場

1925 年，Heisenberg 在海利根達姆提出「矩陣力學」：物理量是無窮維矩陣，能量是對角矩陣，本徵值即觀測到的譜線。同年稍晚，Born 與 Jordan、Dirac 把它整理成矩陣力學體系。

1926 年初，Schrödinger 在 Zürich 提出「波動力學」：量子態是波函數 $\psi(x)$ ，服從偏微分方程

$$
i\hbar\frac{\partial \psi}{\partial t}=-\frac{\hbar^2}{2m}\Delta\psi+V(x)\psi.
$$

兩套理論給出完全相同的能量譜與躍遷振幅——例如諧振子 $V=\frac{m\omega^2x^2}{2}$ 都給出能階 $E_n=\hbar\omega\left(n+\frac12\right)$ 。

現場留下三重謎團：

1. **兩種看似毫不相干的數學（矩陣 vs 微分方程）為何給出相同答案？** Schrödinger 自己試圖證明等價性：他宣稱波動力學蘊含矩陣力學，但他的論證只是形式上的推導，**在數學上並不嚴格——實際上是失敗的**。困難在於：他所處理的算子（動量 $p=-i\hbar\,d/dx$ ）處處無界，根本不是 Hilbert 空間上的有界算子，當時的譜論（Hilbert 的二次型理論、Hellinger 的譜分解）都只對有界算子有效。
2. **波函數 $\psi(x)$ 屬於什麼空間？** 動量表象下是 Fourier 變換 $\hat\psi(\xi)$ ，兩個表象中的「同一個態」如何嚴格對應？
3. **Hamilton 算子 $H$ 的譜論何在？** 連續譜（散射態）與離散譜（束縛態）混合出現，當時沒有任何定理能處理。

1926 年底，年方二十三的 von Neumann——Hilbert 的助手——接下這樁懸案。

## 偵查過程

von Neumann 的偵查分四步。

**第一步：勘定空間。** 量子態是 Hilbert 空間 $\mathcal{H}=L^2(\mathbb{R}^d)$ 中的向量 $\psi$ ， $\|\psi\|^2=\int|\psi|^2=1$ 。兩個表象（位置、動量）只是同一空間的兩種座標——由 Fourier 變換

$$
\hat\psi(\xi)=\frac{1}{(2\pi)^{d/2}}\int e^{-ix\cdot\xi}\psi(x)\,dx
$$

聯繫，而 Plancherel 定理（1910–1913）保證 $U:\psi\mapsto\hat\psi$ 是酉算子： $\|U\psi\|=\|\psi\|$ 。**表象的選擇不改變物理。**

**第二步：比對指紋——等價性的真相。** Heisenberg 的矩陣力學中，位置算子是對角矩陣 $(Q\psi)_n=q_n\psi_n$ （在合適的表象下），動量算子是 $(P\psi)_n=-i\hbar\,\partial\psi/\partial q_n$ 。在波動力學中 $Q\psi(x)=x\psi(x)$ 、 $P\psi(x)=-i\hbar\psi'(x)$ 。對易關係同為

$$
QP-PQ=i\hbar I.
$$

von Neumann 發現：**兩套力學之所以等價，是因為它們都是同一個抽象 Hilbert 空間上同一組無界算子的不同具體實現，而連接它們的酉算子（Fourier 變換或更一般的變換）保持所有代數關係。** Schrödinger 失敗之處在於他企圖在「函數」層面直接比較，而正確的地點是「空間＋酉等價」層面。

| 表象 | 態 | 位置算子 | 動量算子 | 能量算子 |
|------|----|----------|----------|----------|
| 矩陣力學 | 數列 $\psi_n\in l^2$ | 對角矩陣 $q_n$ | $-i\hbar\,\partial_n$ | $H=P^2/2m+V(Q)$ |
| 波動力學 | 函數 $\psi(x)\in L^2$ | $x\psi(x)$ | $-i\hbar\,d/dx$ | $-\frac{\hbar^2}{2m}\Delta+V(x)$ |
| 聯繫 | 酉算子 $U$ （Fourier 變換等） | $UQU^*$ | $UPU^*$ | $UHU^*$ |

**第三步：撞上銅牆——無界算子的難關。** 位置算子 $Q\psi=x\psi$ 只在 $\int x^2|\psi|^2<\infty$ 的 $\psi$ 上有定義；微分算子 $P\psi=-i\hbar\psi'$ 更糟： $L^2$ 中到處有定義的對稱算子必有界（Hellinger–Toeplitz，1927），而 $P$ 無界——所以 $P$ **不可能處處有定義**。結論：無界算子必須帶定義域 $\mathcal{D}(P)\subset\mathcal{H}$ 來研究，且定義域是理論的一部分，不是附屬品。

更尖銳的難關： $P$ 是對稱的（ $\langle P\psi,\varphi\rangle=\langle\psi,P\varphi\rangle$ ），但對稱 $\neq$ 自伴。對稱算子可以有很多不同的自伴延拓，譜論對它們各有不同答案。物理上要求的是自伴（self-adjoint）——這才有唯一的譜分解。

**第四步：確認動機——譜論必須升級。** 有界算子的譜論（Hilbert、Hellinger 1906–1912 的二次型譜分解）無法直接搬到無界算子： $H$ 的譜含連續部分，其「特徵向量」根本不在 $\mathcal{H}$ 中（散射態的平面波 $e^{ikx}$ 不平方可和）。von Neumann 意識到：需要全新的譜分解概念——不是分解成特徵向量之和，而是**分解成投影算子的連續族**。這正是 1929–1930 年譜定理的種子。

## 結案報告

結案：**矩陣力學與波動力學的等價性，是同一抽象 Hilbert 空間上算子組的酉等價性；證明它的正確語言是 Hilbert 空間幾何而非形式推導。** Schrödinger 的失敗暴露了真正的懸案：無界算子的譜論。

結案的遺產：

1. **無界算子必須連同定義域研究**： $\mathcal{D}(H)$ 是理論核心，自伴性（而非對稱性）才是物理可觀測量的正確數學性質。
2. **Schrödinger 方程的嚴格譜論**： $H=-\Delta+V$ 的譜分解（束縛態＝離散特徵值、散射態＝連續譜）成為 1930 年代數學物理的主戰場。
3. **直通後續三案**：von Neumann 譜定理（1929–1930，投影值測度）、《量子力學的數學基礎》（1932，公理化）、Weyl–von Neumann 奇異擾動（1931，連續譜的病理）。
4. **物理學的數學化**：Dirac 的 $\delta$ 函數等「物理直覺」的合法性問題，直通 Schwartz 分布理論（1945）。

## 證據與工具

**關鍵定義**：

- 酉算子： $U^*U=UU^*=I$ ，保持內積與範數。
- 對稱算子： $\mathcal{D}(A)$ 稠密且 $\langle A\psi,\varphi\rangle=\langle\psi,A\varphi\rangle$ （ $\varphi,\psi\in\mathcal{D}(A)$ ）。
- 自伴算子： $A^*=A$ ，即 $A$ 的伴隨與 $A$ 有相同定義域與作用。自伴 $\Rightarrow$ 對稱，反之不然。

**關鍵公式一覽**：

| 公式 | 意義 |
|------|------|
| $i\hbar\dfrac{\partial\psi}{\partial t}=-\dfrac{\hbar^2}{2m}\Delta\psi+V\psi$ | Schrödinger 方程 |
| $\hat\psi(\xi)=(2\pi)^{-d/2}\displaystyle\int e^{-ix\cdot\xi}\psi\,dx$ | 表象之間的酉橋樑 |
| $\|U\psi\|=\|\psi\|$ （Plancherel） | 表象不改變物理 |
| $QP-PQ=i\hbar I$ | 正則對易關係，兩套力學共享 |
| $E_n=\hbar\omega(n+\tfrac12)$ | 諧振子能階：兩理論的共同答案 |

**偵查骨架**：

1. 定空間： $\mathcal{H}=L^2$ ，態＝單位向量。
2. 等價性：酉算子 $U$ 使 $UQ_1U^*=Q_2$ 、 $UP_1U^*=P_2$ ，故譜與觀測量全同。
3. 難關： $Q$ 、 $P$ 無界 $\Rightarrow$ 必須帶定義域；Hellinger–Toeplitz 排除「處處無界定義」的對稱算子。
4. 動機：有界譜論不敷使用 $\Rightarrow$ 需要投影值測度式的譜分解。

**一句話結論**：Schrödinger 的失敗證明了問題不在波動力學，而在當時的數學工具；von Neumann 接案後發現，破案鑰匙是「無界自伴算子」——量子力學的數學地基自此動工。
