# 1932-vonNeumann量子力學

## 案件檔案表

| 項目 | 內容 |
|------|------|
| 案發年份 | 1932 |
| 主偵探 | John von Neumann |
| 案發地點 | Berlin / Princeton |
| 案件類型 | 量子力學的公理化 |
| 關鍵證物 | 《Mathematische Grundlagen der Quantenmechanik》、疊加原理、測量即投影 $E_\lambda$ 、von Neumann 熵 |
| 涉案對象 | Hilbert 空間上的量子力學全體 |
| 案件地位 | 量子力學數學基礎的定稿之作 |
| 後續影響 | von Neumann 代數、量子測量理論、量子資訊理論 |

## 案發現場

1925–1930 年間，量子力學經歷了狂飆：Heisenberg 的矩陣力學、Schrödinger 的波動力學、von Neumann 的自伴譜定理（1929–1930）。理論的每一塊積木都已存在，但整體仍然是一堆各說各話的計算規則：

1. **沒有統一的公理系統**：物理學家（Dirac 1930 的《量子力學原理》）用直覺符號（ $\delta$ 函數、bra-ket）書寫理論，數學合法性存疑。
2. **測量過程沒有數學描述**：測量時波函數「塌縮」——這一物理直覺需要嚴格的算子語言。
3. **統計力學的量子版沒有基礎**：混合態（密度矩陣）的熵如何定義？熱力學第二定律在量子世界的對應是什麼？

von Neumann 在 1932 年出版《Mathematische Grundlagen der Quantenmechanik》（量子力學的數學基礎），把整座大廈公理化，一舉結案。

## 偵查過程

**第一步：勘定地基——Hilbert 空間公理。** von Neumann 的公理系統（以現代語言整理）：

| 公理 | 內容 |
|------|------|
| 態 | 純態是 Hilbert 空間 $\mathcal{H}$ 中的單位向量 $\psi$ （ $\|\psi\|=1$ ）；一般態是密度算子 $\rho\ge 0$ 、 $\mathrm{Tr}\,\rho=1$ |
| 可觀測量 | 自伴算子 $A=A^*$ （一般無界，定義域 $\mathcal{D}(A)$ ） |
| 觀測期望值 | $\langle A\rangle_\psi=\langle\psi,A\psi\rangle=\displaystyle\int\lambda\,d\langle E_\lambda\psi,\psi\rangle$ |
| 動力學 | 酉群 $U_t=e^{-itH/\hbar}$ ，Schrödinger 方程 $i\hbar\dot\psi=H\psi$ |
| 複合系統 | 張量積 $\mathcal{H}_1\otimes\mathcal{H}_2$ |

**第二步：確認物證一——疊加原理。** 若 $\psi_1,\psi_2$ 是可能的態，則 $\alpha\psi_1+\beta\psi_2$ （ $|\alpha|^2+|\beta|^2=1$ ）也是可能的態——這是 Hilbert 空間線性結構的直接推論。**量子疊加不是附加假設，而是空間公理的必然。** von Neumann 指出：這正是 Hilbert 空間（而非相空間）作為量子態空間的理由——古典力學的相空間沒有自然的「疊加」。

**第三步：確認物證二——測量即投影。** 由譜定理 $A=\int\lambda\,dE_\lambda$ ，測量可觀測量 $A$ 得到值在集合 $\Delta$ 中的機率是

$$
\mathbb{P}(\text{測值}\in\Delta)=\|E(\Delta)\psi\|^2=\langle\psi,E(\Delta)\psi\rangle,
$$

而測量後的態「塌縮」為

$$
\psi\ \longmapsto\ \frac{E(\Delta)\psi}{\|E(\Delta)\psi\|}.
$$

**測量過程＝譜投影的應用**——這是量子測量理論的第一個嚴格數學模型（Lüders 規則的先聲）。

**第四步：確認物證三——von Neumann 熵。** 對密度算子 $\rho$ （混合態），von Neumann 定義熵

$$
S(\rho)=-\mathrm{Tr}(\rho\log\rho).
$$

由譜分解 $\rho=\sum_k p_k P_k$ （ $p_k$ 是 $\rho$ 的特徵值， $P_k$ 是對應投影），

$$
S(\rho)=-\sum_k p_k\log p_k,
$$

正是 Shannon 熵（1948）的量子前身，也是古典 Gibbs 熵 $\int f\log f$ 的算子化。von Neumann 證明其關鍵性質：

| 性質 | 內容 |
|------|------|
| 非負 | $S(\rho)\ge 0$ ，純態時 $S=0$ |
| 次可加 | $S(\rho_{12})\le S(\rho_1)+S(\rho_2)$ |
| 酉不變 | $S(U\rho U^*)=S(\rho)$ ：動力學不改變熵 |
| 極大值 | $\dim\mathcal{H}=n$ 時 $S(\rho)\le\log n$ ，等號在 $\rho=\frac{I}{n}$ |

**第五步：鋪設道路——算子代數的種子。** von Neumann 在書中與 Murray 合作（1936 年起系列論文）發展出 von Neumann 代數：Hilbert 空間上對合的算子代數 $\mathcal{M}\subset B(\mathcal{H})$ ，滿足 $\mathcal{M}''=\mathcal{M}$ 。量子力學的可觀測量代數、對稱性、統計（Bose–Fermi）由代數的分類刻畫——這是 1930 年代後數學物理的主幹道。

## 結案報告

von Neumann 結案：**量子力學是 Hilbert 空間上的自伴算子理論——態是向量或密度算子，可觀測量是自伴算子，測量是譜投影，動力學是酉群，熵是 $-\mathrm{Tr}(\rho\log\rho)$ 。** 整座理論從公理出發，無一處依賴物理直覺符號。

結案的遺產：

1. **量子測量理論**：塌縮 $=$ 投影（Lüders 1956 規則）、POVM 的推廣（1970 年代）、量子去相干理論，全部從本書的測量公理出發。
2. **von Neumann 代數**：與 Murray 的因子分類（Type I/II/III）成為算子代數的核心，直通 Connes 的非交換幾何（1980s）。
3. **量子資訊理論**：von Neumann 熵是量子通訊、量子計算的基礎量；量子糾纏熵、量子態區分，都是本書物證的續集。
4. **數學物理的定稿**：Dirac 的 $\delta$ 函數、跳躍的物理直覺，被 Hilbert 空間語言完全吸收；Schrödinger–Heisenberg 等價性之謎（1926）在此書中得到最終定稿。

## 證據與工具

**關鍵公式一覽**：

| 公式 | 意義 |
|------|------|
| $i\hbar\dfrac{\partial\psi}{\partial t}=H\psi$ ， $U_t=e^{-itH/\hbar}$ | 動力學：酉群 |
| $A=\displaystyle\int\lambda\,dE_\lambda$ | 譜定理：可觀測量的解剖 |
| $\psi\mapsto\dfrac{E(\Delta)\psi}{\|E(\Delta)\psi\|}$ | 測量即投影（塌縮） |
| $S(\rho)=-\mathrm{Tr}(\rho\log\rho)$ | von Neumann 熵 |
| $\rho=\sum_k p_k P_k$ ， $S=-\sum p_k\log p_k$ | 熵的譜分解形式 |
| $\mathcal{H}_1\otimes\mathcal{H}_2$ | 複合系統 |

**測量流程**：

1. 態 $\psi$ （單位向量）。
2. 對可觀測量 $A$ 的譜投影 $E(\Delta)$ 計算 $\|E(\Delta)\psi\|^2$ ＝測值落在 $\Delta$ 的機率。
3. 測後態塌縮為 $E(\Delta)\psi/\|E(\Delta)\psi\|$ 。
4. 重複測量 $A$ ：若再測 $\Delta$ ，機率為 $1$ （投影的冪等性 $E(\Delta)^2=E(\Delta)$ ）——**測量擾動系統的數學記錄**。

**一句話結論**：von Neumann 1932 破案——量子力學的每一條物理規則都能寫成 Hilbert 空間上的算子語言；疊加是線性、測量是投影、動力學是酉群、熵是迹的對數，公理大廈自此落成。
