# 1950-LaxMilgram定理

| 案件檔案 | |
|------|------|
| 案發年份 | 1950（美國，紐約大學；論文 1954 發表） |
| 主嫌 | 連續強制雙線性形式 $B(u,v)$ |
| 受害者 | 橢圓邊值問題：解的存在性與唯一性缺乏統一工具 |
| 關鍵證人 | Peter Lax 與 Arthur Milgram（1954 論文） |
| 結案結果 | Lax–Milgram 定理問世，橢圓邊值問題的萬能鑰匙、FEM 收斂基石 |

## 案發現場

1950 年前後，數學家在解橢圓邊值問題時遭遇一樁舊案重啟：

$$-\Delta u + c\,u = f\quad\text{在}\ \Omega\ \text{內},\qquad u\big|_{\partial\Omega}=0 .$$

已有的偵查路線有三條，各有死角：

1. **Fredholm–Riesz 路線**（1900–1916）：把方程寫成緊算子擾動，但需要 $f$ 與解都很光滑，且對高階方程無能為力。
2. **Ritz–Galerkin 變分路線**（1932）：把解極小化 $J(u)=\frac12 B(u,u)-\ell(u)$ ，但「極小元是否存在」缺乏一般證明。
3. **Sobolev 弱解路線**（1935）：弱解的語言有了，但存在唯一性的抽象定理還缺一環。

謎題的核心問題：**在 Hilbert 空間中，什麼樣的雙線性形式能保證變分問題有唯一解？** 這是 Peter Lax 與 Arthur Milgram 在紐約大學要接的案子。

## 偵查過程

Lax–Milgram 的偵查策略是：**抽象化變分法——把「能量」與「強制性」變成公理**。

### 第一步：雙線性形式的兩條公理

設 $H$ 為實 Hilbert 空間， $B:H\times H\to\mathbb{R}$ 為雙線性形式，滿足：

1. **連續性**：存在 $\gamma>0$ 使
$$|B(u,v)|\le\gamma\|u\|\,\|v\|,\qquad \forall u,v\in H ;$$
2. **強制性**（coercivity）：存在 $\alpha>0$ 使
$$B(u,u)\ge\alpha\|u\|^2,\qquad \forall u\in H .$$

### 第二步：Riesz 表示的變形

由連續性，固定 $u$ 後 $v\mapsto B(u,v)$ 是 $H$ 上的連續線性泛函。由 Riesz 表示定理，存在 $A:H\to H$ 線性有界使

$$B(u,v)=\langle Au,v\rangle,\qquad \|A\|\le\gamma .$$

強制性化為

$$\langle Au,u\rangle\ge\alpha\|u\|^2 .$$

於是原方程 $B(u,v)=\ell(v)\ (\forall v\in H)$ 等價於算子方程 $Au=g$ ，其中 $g$ 是 $\ell$ 的 Riesz 代表元。

### 第三步：不動點論證

關鍵技巧：不直接解 $Au=g$ ，而是構造壓縮映射。對參數 $\rho>0$ ，定義 $S_\rho:H\to H$ ：

$$S_\rho(u)=u-\rho(Au-g) .$$

計算範數的平方：

$$\|S_\rho(u)-S_\rho(w)\|^2=\|u-w\|^2-2\rho\langle A(u-w),u-w\rangle+\rho^2\|A(u-w)\|^2 \le \big(1-2\rho\alpha+\rho^2\gamma^2\big)\|u-w\|^2 .$$

取 $\rho=\alpha/\gamma^2$ ，壓縮常數為 $\sqrt{1-\alpha^2/\gamma^2}<1$ 。由 Banach 不動點定理， $S_\rho$ 有唯一不動點 $u$ ，即 $Au=g$ 的唯一解。結案。

### 第四步：偵查筆記本——定理的完整陳述

**Lax–Milgram 定理（1954）：** 設 $B$ 連續且強制， $\ell\in H^*$ ，則存在唯一 $u\in H$ 使

$$B(u,v)=\ell(v),\qquad \forall v\in H ,$$

且 $\|u\|\le\alpha^{-1}\|\ell\|$ 。

### 第五步：套用到橢圓邊值問題

取 $H=H_0^1(\Omega)$ ， $B(u,v)=\int_\Omega\nabla u\cdot\nabla v\,dx+c\int_\Omega u\,v\,dx$ ， $\ell(v)=\int_\Omega f\,v\,dx$ 。

- 連續性：由 Cauchy–Schwarz， $|B(u,v)|\le\|u\|_{H^1}\|v\|_{H^1}$ （適當常數）。
- 強制性：由 Poincaré 不等式 $\|u\|_{L^2}\le C_P\|\nabla u\|_{L^2}$ ，當 $c\ge 0$ 時
$$B(u,u)\ge\|\nabla u\|_{L^2}^2\ge\frac{1}{1+C_P^2}\|u\|_{H_0^1}^2 .$$

於是弱解 $u\in H_0^1(\Omega)$ 存在且唯一。

各種邊值條件的對照表：

| 問題 | 空間 $H$ | 雙線性形式 | 強制性來源 |
|------|----------|-----------|-----------|
| Dirichlet | $H_0^1$ | $\int\nabla u\cdot\nabla v+cuv$ | Poincaré |
| Neumann（ $c>0$ ） | $H^1$ | 同上 | $c>0$ 項 |
| Neumann（ $c=0$ ） | $H^1/\mathbb{R}$ 或相容性條件 | 同上 | 商空間 |
| 彈性系統 | $H^1$ 向量值 | 應變能形式 | Korn 不等式 |

### 第六步：Galerkin 逼近與 FEM 伏筆

設 $V_n\subset H_0^1$ 為有限維子空間（Lagrangian 有限元、譜方法基底），Galerkin 解 $u_n$ 由

$$B(u_n,v_n)=\ell(v_n),\qquad \forall v_n\in V_n$$

定義。由 Lax–Milgram（限制在 $V_n$ 上仍連續強制）， $u_n$ 存在唯一；再由強制性與正交性論證得誤差估計

$$\|u-u_n\|_{H^1}\le\frac{\gamma}{\alpha}\inf_{v_n\in V_n}\|u-v_n\|_{H^1} .$$

這就是 **Céa 引理**：誤差由最佳逼近控制。FEM 的收斂理論由此奠基。

## 結案報告

1954 年 Lax–Milgram 論文發表，宣布結案：連續＋強制的雙線性形式保證變分問題有唯一解，且解以線性方式連續依賴於資料。案件遺產如下：

- **橢圓邊值問題的萬能鑰匙**：Dirichlet、Neumann、混合、彈性系統，一個定理統一處理；弱解存在唯一性成為 PDE 現代理論的標準開場。
- **FEM 收斂的基石**：Céa 引理＋Sobolev 空間的插值理論，構成有限元方法的完整誤差分析；工程計算的數學保證由此而來。
- **Banach 不動點的變形用武之地**：Lax–Milgram 的證明是「壓縮映射＋Riesz 表示」的典範組合。
- **後續浪潮**：1956 年 Gårding 不等式把強制性放寬為 $B(u,u)\ge\alpha\|u\|_{H^1}^2-\beta\|u\|_{L^2}^2$ ，擴大可解範圍；Babuška–Lax–Milgram 定理（1971）把框架推廣到非對稱、非強制的 Banach 空間情形。

## 證據與工具

**關鍵公式一覽表：**

| 工具 | 公式／陳述 | 用途 |
|------|-----------|------|
| 連續性 | $|B(u,v)|\le\gamma\|u\|\,\|v\|$ | 算子 $A$ 有界 |
| 強制性 | $B(u,u)\ge\alpha\|u\|^2$ | 唯一性 |
| Riesz 表示 | $B(u,v)=\langle Au,v\rangle$ | 化為算子方程 |
| 壓縮映射 | $S_\rho(u)=u-\rho(Au-g)$ | 存在性 |
| 誤差估計 | $\|u\|\le\alpha^{-1}\|\ell\|$ | 連續依賴 |
| Céa 引理 | $\|u-u_n\|\le\frac{\gamma}{\alpha}\inf_{v_n}\|u-v_n\|$ | FEM 收斂 |

**證明骨架：**

1. 連續性 $\Rightarrow$ $A:H\to H$ 有界（Riesz 表示）。
2. 強制性 $\Rightarrow$ $\langle Au,u\rangle\ge\alpha\|u\|^2$ ，故 $A$ 單射且有下界 $\alpha$ 。
3. 構造 $S_\rho$ ，取 $\rho=\alpha/\gamma^2$ ，得壓縮常數 $\sqrt{1-\alpha^2/\gamma^2}$ 。
4. Banach 不動點定理給出唯一不動點 $u= A^{-1}g$ 。 $\blacksquare$

**典型例子：** 一維問題 $-u''=f$ ， $u(0)=u(1)=0$ 。 $B(u,v)=\int_0^1 u'v'\,dx$ ；Poincaré 常數為 $C_P=1/\pi$ ，強制常數 $\alpha=\pi^2/(1+\pi^2)$ 。取 $f=1$ ，精確解 $u(x)=\frac{x(1-x)}{2}$ ；Galerkin 用單一基函數 $\phi_1=x(1-x)$ 得 $u_1=\frac{1}{12}\phi_1=\frac{x(1-x)}{12}$ （因 $\ell(\phi_1)=1/6$ 、 $B(\phi_1,\phi_1)=1/3$ ），逼近誤差由 Céa 引理控制在最佳逼近以下——萬能鑰匙在最低維子空間就已靈驗。
