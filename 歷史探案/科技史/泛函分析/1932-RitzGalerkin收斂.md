# 1932-RitzGalerkin收斂

## 案件檔案表

| 項目 | 內容 |
|------|------|
| 案發年份 | 1932（收斂理論定稿年代；Ritz 1908/1909、Galerkin 1915） |
| 主偵探 | Walter Ritz 與 Boris Galerkin 的遺產，Lax–Milgram 的前身 |
| 案發地點 | Göttingen（Ritz）→ Petrograd（Galerkin） |
| 案件類型 | 變分法的投影收斂理論 |
| 關鍵證物 | 能量誤差 $J(u)-J(u_n)\le C\,\mathrm{dist}(u,V_n)^2$ ；最佳逼近性質 |
| 涉案對象 | 變分問題 $J(u)=\frac12 a(u,u)-\ell(u)$ 的近似解 |
| 案件地位 | 有限元素法（FEM）的血緣源頭 |
| 後續影響 | Lax–Milgram（1950）、FEM、Céa 引理 |

## 案發現場

1908–1909 年，Ritz 在 Göttingen 發表兩篇論文，提出求解邊值問題的變分法：把微分方程的解寫成某個能量泛函的極小點，然後在有限維子空間上求極小。以 Dirichlet 問題為例：

$$
-\Delta u=f\ \text{於}\ \Omega,\qquad u|_{\partial\Omega}=0,
$$

等價於極小化能量泛函

$$
J(u)=\frac12\int_\Omega|\nabla u|^2\,dx-\int_\Omega fu\,dx
$$

於 $u$ 的容許函數類中。Ritz 的方法：取有限維子空間 $V_n=\mathrm{span}\{\varphi_1,\dots,\varphi_n\}$ ，在 $V_n$ 中求極小：

$$
J(u_n)=\min_{v\in V_n}J(v),\qquad u_n=\sum_{k=1}^n c_k\varphi_k.
$$

1915 年，Galerkin 在 Petrograd 獨立提出投影法：直接令殘量與 $V_n$ 正交，

$$
a(u_n,v)=\ell(v)\qquad\forall v\in V_n.
$$

兩人發現（Ritz 用能量、Galerkin 用正交）這其實是同一個方法——當 $a$ 對稱時完全等價。

現場的未解之謎：** $u_n$ 何時收斂到 $u$ ？收斂速度如何？** Ritz 自己只給出形式推導，嚴格的收斂理論要到 1930 年代——配合 Sobolev 空間（1935 前身）與投影理論——才完成。

## 偵查過程

**第一步：勘定空間——能量內積。** 設 $a$ 是對稱、連續、強制（coercive）的雙線性形式：

$$
|a(u,v)|\le M\|u\|\|v\|,\qquad a(v,v)\ge\alpha\|v\|^2\qquad(\alpha>0).
$$

由 $a$ 定義能量內積 $\langle u,v\rangle_a=a(u,v)$ ，其誘導範數 $\|u\|_a=\sqrt{a(u,u)}$ 與原範數等價（由強制性）：

$$
\sqrt{\alpha}\,\|u\|\le\|u\|_a\le\sqrt{M}\,\|u\|.
$$

變分問題變成： $u$ 是 $J$ 在 $\mathcal{H}$ 上的唯一極小點，且滿足變分方程 $a(u,v)=\ell(v)\ \forall v$ 。

**第二步：確認物證一——最佳逼近性質。** Ritz–Galerkin 解 $u_n$ （ $V_n$ 上的極小點）滿足

$$
a(u-u_n,v)=0\qquad\forall v\in V_n,
$$

即 ** $u_n$ 是 $u$ 在 $V_n$ 上的能量正交投影**。由此立刻得到誤差的正交分解：

$$
\|u-u_n\|_a=\mathrm{dist}_a(u,V_n)=\min_{v\in V_n}\|u-v\|_a.
$$

**Ritz 解是能量範數下的最佳逼近**——這是整個理論的關鍵證物。

**第三步：確認物證二——能量誤差估計。** 由正交性展開：

$$
J(u)-J(u_n)=\frac12 a(u,u)-\frac12 a(u_n,u_n)=\frac12 a(u-u_n,u-u_n)=\frac12\,\mathrm{dist}_a(u,V_n)^2.
$$

更精細地，用原範數與強制性：

$$
J(u)-J(u_n)\le\frac{M}{2}\,\mathrm{dist}(u,V_n)^2,\qquad \|u-u_n\|\le\sqrt{\frac{M}{\alpha}}\,\mathrm{dist}(u,V_n).
$$

**誤差完全由「 $u$ 到 $V_n$ 的距離」控制**——只要 $V_n$ 越來越大（稠密）， $u_n$ 就越來越接近 $u$ 。

**第四步：收網——收斂定理。** 設 $V_1\subset V_2\subset\cdots$ 逐步稠密於 $\mathcal{H}$ （ $\overline{\bigcup_n V_n}=\mathcal{H}$ ）。則

$$
\|u_n-u\|_a\to 0,\qquad J(u_n)\to J(u),
$$

且收斂速度由逼近速度決定。例如 $u\in H^2_0(\Omega)$ 時取分片線性元素，逼近論給出 $\mathrm{dist}(u,V_n)\le C h\|u\|_{H^2}$ （ $h$ 是網格大小），故

$$
\|u-u_n\|_{H^1}\le C h\,\|u\|_{H^2}:\quad \textbf{一階收斂}.
$$

| 步驟 | 物證 | 公式 |
|------|------|------|
| Ritz（1908） | 能量極小 | $J(u_n)=\min_{v\in V_n}J(v)$ |
| Galerkin（1915） | 殘量正交 | $a(u_n,v)=\ell(v)\ \forall v\in V_n$ |
| 投影性質 | 最佳逼近 | $\|u-u_n\|_a=\mathrm{dist}_a(u,V_n)$ |
| 誤差估計 | 能量誤差 | $J(u)-J(u_n)=\frac12\,\mathrm{dist}_a(u,V_n)^2$ |
| 收斂 | 稠密性 | $\overline{\bigcup V_n}=\mathcal{H}\Rightarrow u_n\to u$ |

**第五步：比對指紋——Ritz 與 Galerkin 的合流。** 當 $a$ 對稱時，能量極小的一階條件正是 $a(u_n,v)=\ell(v)\ \forall v\in V_n$ ——**Ritz 法＝Galerkin 法**。當 $a$ 不對稱時，Ritz 能量法失效，但 Galerkin 正交法仍然有效——這正是 Lax–Milgram（1950）的前身：Galerkin 方程在連續＋強制（不必對稱）的 $a$ 下有唯一解，且收斂性保持。

## 結案報告

結案：**Ritz–Galerkin 解是能量範數下的最佳逼近；能量誤差 $J(u)-J(u_n)=\frac12\,\mathrm{dist}_a(u,V_n)^2$ ；只要近似空間逐步稠密，近似解必收斂，速度由逼近速度決定。**

結案的遺產：

1. **Céa 引理（1964）**： $\|u-u_n\|\le\frac{M}{\alpha}\min_{v\in V_n}\|u-v\|$ ——FEM 誤差分析的第一定律，是本案誤差估計的直接後裔。
2. **Lax–Milgram（1950）**：Galerkin 方程的存在唯一性在非對稱強制形式下成立，是本案「Ritz＝Galerkin（對稱）」偵查的推廣。
3. **有限元素法（FEM）的血緣**：Ritz 的有限維極小＋Galerkin 的正交投影＋Sobolev 空間的正則性＝現代 FEM 的三大支柱；1948 年 Lax 等價定理（一致性＋穩定性＝收斂性）承接其收斂思想。
4. **數值 PDE 的誕生**：1930 年代的收斂理論使變分法從「形式方法」升級為「嚴格數值演算法」。

## 證據與工具

**定理（Ritz–Galerkin 收斂）**：設 $a$ 對稱連續強制， $\ell$ 連續， $V_n\nearrow$ 稠密於 $\mathcal{H}$ 。則

1. 變分問題有唯一解 $u$ ，Galerkin 方程有唯一解 $u_n\in V_n$ ；
2. $u_n=P^{V_n}_a u$ （能量正交投影）；
3. $J(u)-J(u_n)=\dfrac12\,\mathrm{dist}_a(u,V_n)^2\to 0$ ；
4. $\|u-u_n\|\le\sqrt{M/\alpha}\,\mathrm{dist}(u,V_n)$ 。

**證明骨架**：

1. 變分方程 $a(u,v)=\ell(v)$ ：對 $J$ 求方向導數 $dJ(u)v=a(u,v)-\ell(v)=0$ 。
2. 正交性： $a(u_n,v)=\ell(v)=a(u,v)\ \forall v\in V_n$ ，故 $a(u-u_n,v)=0$ 。
3. 能量誤差： $J(u)-J(u_n)=\frac12 a(u-u_n,u-u_n)$ （由正交性消去交叉項 $a(u-u_n,u_n)=0$ ）。
4. 收斂： $\mathrm{dist}_a(u,V_n)\to 0$ （ $V_n$ 稠密＋範數等價）。

**關鍵公式一覽**：

| 公式 | 意義 |
|------|------|
| $J(u)=\frac12 a(u,u)-\ell(u)$ | 能量泛函 |
| $a(u_n,v)=\ell(v)\ \forall v\in V_n$ | Galerkin 方程 |
| $\|u-u_n\|_a=\mathrm{dist}_a(u,V_n)$ | 最佳逼近性質 |
| $J(u)-J(u_n)=\frac12\,\mathrm{dist}_a(u,V_n)^2$ | 能量誤差估計 |
| $\|u-u_n\|\le\sqrt{M/\alpha}\,\mathrm{dist}(u,V_n)$ | 範數誤差（Céa 前身） |

**一句話結論**：Ritz 1908/1909 與 Galerkin 1915 各自挖出同一塊化石——變分問題的近似解是能量正交投影；1930 年代的收斂理論為它驗明正身，並留下 FEM 的完整血緣。
