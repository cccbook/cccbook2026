# 1935-Sobolev空間

| 案件檔案 | |
|------|------|
| 案發年份 | 1935（蘇聯，列寧格勒） |
| 主嫌 | Sobolev 空間 $W^{k,p}$ |
| 受害者 | 經典導數概念：PDE 理論無法處理不夠光滑的函數 |
| 關鍵證人 | Sergei Sobolev（1935 論文、1938 弱導數定稿） |
| 結案結果 | 弱導數與嵌入定理問世，PDE 有了現代語言 |

## 案發現場

1930 年代，數學家在解偏微分方程時遇到一樁懸案：許多自然出現的函數（例如有角點的函數、甚至不連續的極限）根本沒有經典意義下的導數，但方程式卻宣稱它們是「解」。Poincaré 在變分法中、Richardson 在數值方法中，都隱約使用過「分部積分轉移導數」的技巧，卻沒有人給它一個嚴格的身分證。

謎題的關鍵線索有三條：

1. 變分法中，泛函 $J(u)=\int |\nabla u|^2\,dx$ 的極小化問題，其極小元可能不在 $C^1$ 中。
2. 物理中的彈性薄板振動問題，需要「廣義解」的框架。
3. Fourier 級數理論顯示：函數的光滑性與係數的衰變速度有深刻的對應。

誰能替「不存在的導數」補辦身分證？這就是 Sobolev 要接下的案子。

## 偵查過程

Sobolev 的偵查策略是：**不放棄導數，而是放寬「導數存在」的定義**。

### 第一步：弱導數的定義

設 $u,\,v\in L^1_{\mathrm{loc}}(\Omega)$ ，若對所有測試函數 $\phi\in C_c^\infty(\Omega)$ 都有

$$\int_\Omega u\,\partial^\alpha \phi\,dx = (-1)^{|\alpha|}\int_\Omega v\,\phi\,dx ,$$

則稱 $v$ 是 $u$ 的 $\alpha$ 階弱導數，記作 $\partial^\alpha u=v$ 。關鍵技巧是分部積分：把導數「轉移」到光滑且緊支撐的測試函數 $\phi$ 身上，原本不存在的 $\partial^\alpha u$ 就由積分恆等式代言。

弱導數的性質偵查表：

| 性質 | 經典導數 | 弱導數 |
|------|----------|--------|
| 定義域 | 逐點存在 | $L^1_{\mathrm{loc}}$ 中由積分恆等式定義 |
| 唯一性 | 逐點唯一 | 在 a.e. 意義下唯一 |
| 鏈法則 | 需要可微 | 光滑複合仍成立 |
| 閉包性 | 無 | $\partial^\alpha$ 是閉算子 |

### 第二步：Sobolev 空間 $W^{k,p}$

對非負整數 $k$ 與 $1\le p\le\infty$ ，定義

$$W^{k,p}(\Omega)=\{u\in L^p(\Omega):\ \partial^\alpha u\in L^p(\Omega),\ |\alpha|\le k\} ,$$

並配備範數

$$\|u\|_{W^{k,p}}=\left(\sum_{|\alpha|\le k}\|\partial^\alpha u\|_{L^p}^p\right)^{1/p} .$$

Sobolev 證明： $W^{k,p}$ 是 Banach 空間（完備性由弱導數的閉性與 $L^p$ 的完備性共同保證）；當 $p=2$ 時 $H^k=W^{k,2}$ 是 Hilbert 空間，內積為

$$\langle u,v\rangle_{H^k}=\sum_{|\alpha|\le k}\int_\Omega \partial^\alpha u\,\overline{\partial^\alpha v}\,dx .$$

### 第三步：稠密性與磨光

用 Friedrichs 磨光子 $\rho_\varepsilon$ 做卷積： $\rho_\varepsilon * u\in C^\infty$ ，且當 $\varepsilon\to 0$ 時在 $W^{k,p}$ 中收斂到 $u$ 。於是

$$C^\infty(\Omega)\cap W^{k,p}(\Omega)\ \text{在}\ W^{k,p}(\Omega)\ \text{中稠密} .$$

這條線索極為關鍵：光滑函數是稠密的「臥底」，任何在 $W^{k,p}$ 中成立的證明都可以先在光滑函數上完成，再取極限。

### 第四步：嵌入定理

1935 年的核心發現：Sobolev 嵌入定理。設 $\Omega\subset\mathbb{R}^n$ 有界且具備適當的正則性（Lipschitz 邊界），若 $k>n/p$ ，則

$$W^{k,p}(\Omega)\hookrightarrow C^{0,\alpha}(\overline{\Omega}),\qquad \alpha=k-\frac{n}{p}\in(0,1) .$$

特別地，取 $k=2,\ p=2$ ：當 $n=1$ 時 $\alpha=1$ ；當 $n=2$ 時 $\alpha=0$ （邊界情形，需 Morrey 不等式輔助）；當 $n\ge 3$ 時則需更精細的指標計算。一般情形的嵌入金字塔如下：

| 指標條件 | 嵌入結果 | 典型場景 |
|----------|----------|----------|
| $kp<n$ | $W^{k,p}\hookrightarrow L^{p^*}$ ， $p^*=\frac{np}{n-kp}$ | 臨界指數 |
| $kp=n$ | $W^{k,p}\hookrightarrow L^q$ （任意有限 $q$ ） | 邊界情形 |
| $kp>n$ | $W^{k,p}\hookrightarrow C^{0,\alpha}$ | 連續代表元 |

莫雷（Morrey）不等式給出定量版本：當 $kp>n$ 時存在 $C$ 使得

$$|u(x)-u(y)|\le C\|u\|_{W^{k,p}}\,|x-y|^{\alpha} .$$

由此，Sobolev 空間中的等價類 $[u]$ 可挑選出 Hölder 連續的代表元——「不存在的導數」的案子有了實體。

### 第五步：1938 年的定稿與緊嵌入

1938 年 Sobolev 證明緊嵌入：當 $kp'<n$ 時， $W^{1,p}\hookrightarrow\hookrightarrow L^{q}$ （ $q<p^*$ ）。緊性由 Arzelà–Ascoli（ $kp>n$ 的連續情形）與一致 $L^p$ 積分控制（ $p'$ 的衰減情形）共同取得。

## 結案報告

1935 年，Sobolev 宣布結案：導數不一定要逐點存在，它可以「分給弱拓樸」——由積分恆等式定義、在 $L^p$ 中封閉。案件遺產如下：

- **PDE 的現代語言**：邊值問題的「廣義解」正式入籍 $W^{k,p}$ ；弱解的存在性由變分法與不動點論證取得，正則性再由嵌入定理升級為經典解。
- **嵌入定理成為估算的骨架**： $W^{1,2}\hookrightarrow C^{0,\alpha}$ 等嵌入，是橢圓方程正則性理論（Gårding、Schauder 估計的推廣）的核心支柱。
- **與 Schwartz 分布理論接軌**：1945 年 Schwartz 的分布理論把弱導數推廣到任意階、任意分布，Sobolev 空間成為分布論中的天然函數空間。
- **數值分析的伏筆**：Sobolev 空間是有限元方法（FEM）收斂理論的舞台，Céa 引理在 $H^1$ 中量測誤差。

Sobolev 於 1963 年獲列寧格勒獎、1988 年獲 Wolf 數學獎； $W^{k,p}$ 至今是 PDE、變分法、幾何分析的通用語言。

## 證據與工具

**關鍵公式一覽表：**

| 工具 | 公式／陳述 | 用途 |
|------|-----------|------|
| 弱導數 | $\int u\,\partial^\alpha\phi=(-1)^{|\alpha|}\int v\,\phi$ | 定義廣義導數 |
| Sobolev 範數 | $\|u\|_{W^{k,p}}=\big(\sum_{|\alpha|\le k}\|\partial^\alpha u\|_{L^p}^p\big)^{1/p}$ | 空間的度量 |
| 嵌入定理 | $kp>n\Rightarrow W^{k,p}\hookrightarrow C^{0,\alpha}$ | 連續代表元 |
| Morrey 不等式 | $|u(x)-u(y)|\le C\|u\|_{W^{k,p}}|x-y|^\alpha$ | Hölder 估計 |
| 磨光稠密性 | $C^\infty\cap W^{k,p}$ 稠密於 $W^{k,p}$ | 歸約到光滑情形 |
| Poincaré 不等式 | $\|u\|_{L^2}\le C\|\nabla u\|_{L^2}$ （ $u$ 有緊支撐或零邊界值） | 零空間控制 |

**證明骨架（嵌入定理 $kp>n$ ）：**

1. 用磨光子把 $u$ 換成光滑函數 $u_\varepsilon$ 。
2. 逐點用複合的 $k$ 階導數與 $L^p$ 界，得到 $|u_\varepsilon(x)-u_\varepsilon(y)|$ 的 $\alpha$ 次 Hölder 估計。
3. 取 $\varepsilon\to 0$ ，由 $L^p$ 收斂抽出一個子列 a.e. 收斂，極限繼承 Hölder 估計。
4. 由 Arzelà–Ascoli 升級為一致收斂，得到連續代表元。

**典型例子：** 一維區間 $(0,1)$ 上， $W^{1,2}\hookrightarrow C^{0,1/2}$ 。函數 $u(x)=\sqrt{x}$ 在 $L^2$ 中、弱導數 $\frac{1}{2\sqrt{x}}$ 也在 $L^2$ 中，但它在 $x=0$ 處不連續且不可微——這說明嵌入是最優的， $\alpha=1/2$ 不能再大。
