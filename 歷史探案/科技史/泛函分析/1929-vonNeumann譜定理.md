# 1929-vonNeumann譜定理

## 案件檔案表

| 項目 | 內容 |
|------|------|
| 案發年份 | 1929–1930（三篇論文系列） |
| 主偵探 | John von Neumann |
| 案發地點 | Göttingen / Berlin / Hamburg |
| 案件類型 | 無界自伴算子的譜分解 |
| 關鍵證物 | 譜定理 $A=\displaystyle\int_{\sigma(A)}\lambda\,dE_\lambda$ ，投影值測度（PVM） |
| 涉案對象 | 自伴算子 $A=A^*$ （定義域 $\mathcal{D}(A)\subset\mathcal{H}$ ） |
| 案件地位 | 量子力學可觀測量的數學地基 |
| 後續影響 | 《量子力學的數學基礎》（1932）、算子代數、譜測度理論 |

## 案發現場

1926 年矩陣力學與波動力學的等價性之謎（見 1926-Schrodinger與譜論）暴露了真正的懸案：量子力學的 Hamilton 算子 $H$ 處處無界，當時所有譜分解定理——Hilbert 的二次型理論、Hellinger 的譜分解——都只對有界算子有效。

現場有三個障礙：

1. **無界性**： $A$ 只在稠密定義域 $\mathcal{D}(A)$ 上有定義；「 $\|A\|<\infty$ 」這類有界譜論的基本假設全部失效。
2. **連續譜**：物理上散射態對應連續譜，其「特徵向量」（如平面波 $e^{ikx}$ ）根本不在 Hilbert 空間中。分解成「特徵向量之和」的舊框架失效。
3. **自伴 vs 對稱**：對稱算子可能有多個自伴延拓，各有不同譜；物理要求的是自伴——但當時連「何時對稱算子有自伴延拓」都沒有判據。

von Neumann 在 1929–1930 年間發表三篇論文《Allgemeine Eigenwerttheorie Hermitescher Funktionaloperatoren》（Hermite 泛函算子的一般特徵值理論），一舉破案。

## 偵查過程

**第一步：確定偵查對象的資格——自伴性。** von Neumann 先證明：對稱算子 $A$ 總有自伴延拓的候選——其伴隨 $A^*$ 的約化子空間 $\ker(A^*\pm iI)$ 維數相等時， $A$ 有自伴延拓（Cayley 變換把問題化為酉算子的延拓）。具體地， $A$ 的 Cayley 變換

$$
V=(A-iI)(A+iI)^{-1}
$$

是把 $A$ 的譜問題搬到單位圓上的酉算子（部分等距）。 $A$ 自伴 $\iff V$ 是酉算子。這一變換把「無界」難關繞道「酉算子」這片已開發的地形。

**第二步：發明新兇器——投影值測度。** 舊框架問「特徵向量在哪裡？」新框架問「**譜投影如何作用？**」von Neumann 證明：對自伴算子 $A$ ，存在一族正交投影 $\{E_\lambda\}_{\lambda\in\mathbb{R}}$ （遞增： $\lambda\le\mu\Rightarrow E_\lambda\le E_\mu$ ；右連續； $E_{-\infty}=0$ 、 $E_{+\infty}=I$ ），使得

$$
A=\int_{\mathbb{R}}\lambda\,dE_\lambda,\qquad \mathcal{D}(A)=\left\{\psi\in\mathcal{H}:\int\lambda^2\,d\langle E_\lambda\psi,\psi\rangle<\infty\right\}.
$$

右式的 Stieltjes 積分意為：對 $\psi\in\mathcal{D}(A)$ 與任意 $\varphi$ ，

$$
\langle A\psi,\varphi\rangle=\int \lambda\,d\langle E_\lambda\psi,\varphi\rangle.
$$

這就是投影值測度（PVM）： $E(\Delta)=E_b-E_a$ 是把態投影到「譜落在區間 $\Delta$ 中」的子空間上的正交投影。

**第三步：驗證物證——譜的完整解剖。** 由 PVM 可讀出全部譜資訊：

| 譜的成分 | PVM 判據 | 物理意義 |
|----------|----------|----------|
| 點譜 $\lambda_0$ | $E_{\lambda_0}\neq E_{\lambda_0-0}$ （跳躍） | 束縛態，特徵值 |
| 連續譜 | $E_\lambda$ 連續變化處 | 散射態，「廣義特徵向量」 |
| 剩餘譜 | 自伴算子：**恆空** | 對稱算子才有此病理 |

最後一項是重大突破：**自伴算子沒有剩餘譜**。對稱而非自伴的算子會出現剩餘譜——這解釋了為何物理必須要求自伴：對稱算子的譜可以「藏」在不對應任何測量的地方。

**第四步：統一戰線——函數演算。** PVM 立刻給出 Borel 函數演算：

$$
f(A)=\int f(\lambda)\,dE_\lambda,\qquad \|f(A)\psi\|^2=\int|f(\lambda)|^2\,d\langle E_\lambda\psi,\psi\rangle,
$$

特別地酉群 $U_t=e^{itA}$ 由 Stone 定理（1932）與 $A$ 一一對應——這正是 Schrödinger 方程解 $e^{-itH/\hbar}$ 的數學骨架：**量子動力學＝自伴算子的譜分解。**

## 結案報告

von Neumann 結案：**自伴算子（無界亦然）有唯一譜分解 $A=\int\lambda\,dE_\lambda$ ；譜由投影值測度完整記錄；自伴算子無剩餘譜；量子力學的可觀測量恰好就是自伴算子。**

結案的遺產：

1. **量子力學的數學地基**：可觀測量 $=$ 自伴算子、測量 $=$ 譜投影、期望值 $\langle\psi,A\psi\rangle=\int\lambda\,d\langle E_\lambda\psi,\psi\rangle$ ，全部寫進《量子力學的數學基礎》（1932）。
2. **無界算子理論誕生**：定義域、閉算子、自伴延拓判據成為標準；直通 1931 年閉算子理論與 Weyl–von Neumann 奇異擾動。
3. **譜測度與算子代數**：PVM 是 $C^*$ -代數、von Neumann 代數（1930 年代與 Murray 合作）的種子。
4. **Stone 定理的呼應**： $t\mapsto U_t$ 酉群 $\leftrightarrow$ 自伴生成元，動力學與譜論合流。

## 證據與工具

**定理（von Neumann 譜定理，1929–1930）**：設 $A$ 為 Hilbert 空間 $\mathcal{H}$ 上的自伴算子。則存在唯一的譜族 $\{E_\lambda\}$ （遞增右連續的正交投影族）使

$$
A=\int_{\mathbb{R}}\lambda\,dE_\lambda,
$$

且 $A$ 的定義域由 $\int\lambda^2\,d\langle E_\lambda\psi,\psi\rangle<\infty$ 刻畫。

**證明骨架**：

1. **Cayley 變換**： $V=(A-iI)(A+iI)^{-1}$ 把自伴性化為酉性。
2. **酉算子的譜分解**（先對有界正規算子證明）：存在譜族使 $V=\int z\,dF_z$ 。
3. **繞回實軸**：由 $V$ 的譜族構造 $A$ 的譜族 $E_\lambda=F_{(\lambda-i)/(\lambda+i)}$ ，驗證 $A=\int\lambda\,dE_\lambda$ 。
4. **唯一性**：譜族由 $\langle E_\lambda\psi,\psi\rangle$ （一個正測度）的 Stieltjes 反轉唯一決定，而此測度由 $A$ 的二次型決定。

**關鍵公式一覽**：

| 公式 | 意義 |
|------|------|
| $A=\displaystyle\int\lambda\,dE_\lambda$ | 譜定理核心 |
| $E(\Delta)=E_b-E_a$ | 譜投影：測量「譜在 $\Delta$ 中」 |
| $\langle\psi,A\psi\rangle=\displaystyle\int\lambda\,d\langle E_\lambda\psi,\psi\rangle$ | 期望值的譜分解 |
| $V=(A-iI)(A+iI)^{-1}$ | Cayley 變換：無界→酉 |
| $U_t=e^{itA}$ | 動力學酉群，Stone 定理 |

**範例**：位置算子 $(Q\psi)(x)=x\psi(x)$ 的譜族是 $(E_\lambda\psi)(x)=\mathbf{1}_{(-\infty,\lambda]}(x)\psi(x)$ ——譜全為連續譜 $[0,1]$ （限制在 $[0,1]$ 上時），測量「位置 $\le\lambda$ 」就是把波函數截斷。沒有任何特徵向量，但譜定理依然完整描述它。

**一句話結論**：von Neumann 1929–1930 破案——譜不必是特徵向量的點名冊，而是一族投影的連續測度；自伴算子的譜分解，就是量子世界的測量理論本身。
