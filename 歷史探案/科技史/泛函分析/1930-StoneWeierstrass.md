# 1930-StoneWeierstrass

## 案件檔案表

| 項目 | 內容 |
|------|------|
| 案發年份 | 1930（初版），1937（推廣定稿） |
| 主偵探 | Marshall H. Stone |
| 原始線索 | Karl Weierstrass（1885） |
| 案發地點 | Harvard / Columbia |
| 案件類型 | 逼近論的代數化 |
| 關鍵證物 | Stone–Weierstrass 定理：含常數＋分離點的子代數在 $C(X)$ 稠密 |
| 涉案對象 | 緊空間 $X$ 上的連續函數代數 $C(X)$ |
| 案件地位 | 逼近論從「多項式特例」升級為「代數判據」 |
| 後續影響 | $C^*$ -代數的 Gelfand 理論、譜逼近、Fourier 級數的稠密性 |

## 案發現場

1885 年 Weierstrass 證明了震驚數學界的定理：閉區間 $[a,b]$ 上的任何連續函數都可以被多項式一致逼近——對任意 $f\in C[a,b]$ 與 $\varepsilon>0$ ，存在多項式 $p$ 使

$$
\|f-p\|_\infty=\sup_{x\in[a,b]}|f(x)-p(x)|<\varepsilon.
$$

從此「連續」與「可逼近」劃上等號，分析學的地基得以加固。

但現場留下謎團：**多項式逼近的本質是什麼？** 多項式是「由 $x$ 經加法、乘法、數乘生成的代數」——那麼在一個一般緊空間 $X$ 上，什麼樣的函數族 $\mathcal{A}\subset C(X)$ 能扮演多項式的角色？是什麼性質保證 $\mathcal{A}$ 稠密？

例如： $[0,2\pi]$ 上的三角多項式（ $\sum a_n\cos nx+b_n\sin nx$ ）能否一致逼近任何連續函數？答案微妙地依賴共軛結構。Weierstrass 的多項式只是龐大理論的一塊化石，Stone 要辨識出完整的物種。

## 偵查過程

Stone 的偵查分三步。

**第一步：列出嫌疑人特徵——代數的兩條性質。** 設 $\mathcal{A}\subset C(X)$ （ $X$ 緊 Hausdorff）是子代數（對加法、數乘、乘法封閉）。Stone 辨識出稠密的兩個關鍵指紋：

1. **含常數**： $\mathbf{1}\in\mathcal{A}$ （或等價地 $\mathcal{A}$ 在每點非零）。
2. **分離點**：對任意 $x\neq y\in X$ ，存在 $f\in\mathcal{A}$ 使 $f(x)\neq f(y)$ 。

多項式在 $[a,b]$ 上兩者皆備：常數函數是 $0$ 次多項式， $f(x)=x$ 分離任何兩點。

**第二步：偵查手法——逼近的代數引擎。** Stone 的證明核心（後人整理的標準路線）：

1. **格運算從代數中長出來**：在 $\mathcal{A}$ 稠密的假設下，可證 $|f|\in\overline{\mathcal{A}}$ （ $f\in\mathcal{A}$ ）。技巧：在 $[-1,1]$ 上用多項式 $p_n(t)$ 一致逼近 $\sqrt{1-t^2}$ ...（實際用 $|t|=\sqrt{t^2}$ 的多項式逼近，Weierstrass 定理在此回收），然後

   $$
   \max(f,g)=\frac{f+g+|f-g|}{2},\qquad \min(f,g)=\frac{f+g-|f-g|}{2},
   $$

   故 $\overline{\mathcal{A}}$ 對 $\max,\min$ 封閉——它成為函數格。
2. **分離性收網**：對給定 $f\in C(X)$ 、 $\varepsilon>0$ 與每對點 $x,y$ ，用分離性造 $g_{x,y}\in\mathcal{A}$ 使 $g_{x,y}(x)\approx f(x)$ 且 $g_{x,y}(y)\approx f(y)$ ；對 $y$ 取 $\min$ 、對 $x$ 取 $\max$ （緊性保證有限運算足夠），得 $g\in\mathcal{A}$ 使 $\|f-g\|_\infty<\varepsilon$ 。

**第三步：比對複數版的指紋——共軛封閉的必要性。** 實數版成立後，複數版出現微妙案情：考慮單位圓 $\mathbb{T}$ 上的解析多項式代數 $\mathcal{A}=\{\sum_{n\ge 0}a_nz^n\}$ 。它含常數、分離點，但**不稠密**——它的閉包是圓盤代數 $A(\mathbb{T})$ ，其中的函數在圓內有全純延拓，而一般 $C(\mathbb{T})$ 函數（如 $\bar z$ ）不具此性質。失蹤的指紋是：

3. **共軛封閉**： $f\in\mathcal{A}\Rightarrow\bar f\in\mathcal{A}$ 。

三角多項式 $\sum_{|n|\le N}c_ne^{inx}$ 含 $\bar z=z^{-1}$ （在 $\mathbb{T}$ 上 $\bar z=\overline{z}$ ），共軛封閉，故**三角多項式在 $C(\mathbb{T})$ 稠密**——這是 Weierstrass 第二逼近定理的特例。

## 結案報告

Stone 結案：**在緊 Hausdorff 空間 $X$ 上，含常數且分離點的子代數在 $C(X,\mathbb{R})$ 中稠密；複值情形還需對共軛封閉。** Weierstrass 的多項式逼近是 $X=[a,b]$ 、 $\mathcal{A}=$ 多項式的特例。

結案的遺產：

1. **逼近論的統一**：多項式逼近（1885）、三角逼近、Legendre 多項式、正交多項式逼近，全部是同一判據的特例。
2. **Gelfand 理論的先聲**： $C(X)$ 是交換 $C^*$ -代數的原型；Stone–Weierstrass 是「代數的規模由其分離能力決定」思想的化石，直通 Gelfand–Naimark（1943）與譜理論的代數化。
3. **應用爆發**：Fourier 級數的一致收斂判據、Stone–Čech 緊化中函數的延拓、動力系統中不變函數的逼近、機器學習中神經網路萬能逼近定理的精神先祖。
4. **Stone 的雙重貢獻**：1930 年證實數版，1937 年定稿並推廣到局部緊空間（在 $C_0(X)$ 中以「在一點消失」取代常數條件）。

## 證據與工具

**定理（Stone–Weierstrass，實數版）**：設 $X$ 緊 Hausdorff， $\mathcal{A}\subset C(X,\mathbb{R})$ 是子代數，含常數函數且分離點。則 $\mathcal{A}$ 在 $C(X,\mathbb{R})$ 中一致稠密。

**定理（複數版）**：若 $\mathcal{A}\subset C(X,\mathbb{C})$ 是子代數，含常數、分離點，且 $\bar{\mathcal{A}}$ 對共軛封閉（ $f\in\mathcal{A}\Rightarrow\bar f\in\mathcal{A}$ ），則 $\mathcal{A}$ 在 $C(X,\mathbb{C})$ 中稠密。

**證明骨架**：

1. 由 Weierstrass 多項式逼近（1885）得 $|f|\in\overline{\mathcal{A}}$ ：多項式 $p$ 滿足 $\big||t|-p(t)\big|<\varepsilon$ 於 $[-M,M]$ ，代入 $t=f$ （ $M=\|f\|_\infty$ ）。
2. $\max,\min$ 公式把格結構注入 $\overline{\mathcal{A}}$ 。
3. 分離性＋緊性：有限次 $\min$ 、 $\max$ 運算拼出 $\varepsilon$ -逼近 $g\in\mathcal{A}$ 。

**關鍵公式一覽**：

| 公式 / 條件 | 意義 |
|------|------|
| $\|f-p\|_\infty<\varepsilon$ | Weierstrass 多項式逼近（特例） |
| $\mathbf{1}\in\mathcal{A}$ ，分離點 | 實數版稠密的兩指紋 |
| $f\in\mathcal{A}\Rightarrow\bar f\in\mathcal{A}$ | 複數版的第三指紋 |
| $\max(f,g)=\frac{f+g+|f-g|}{2}$ | 格結構從代數中長出 |
| $\sum_{|n|\le N}c_ne^{inx}$ 稠密 | 三角版：Weierstrass 第二定理 |

**反例（共軛封閉不可省）**： $\mathbb{T}$ 上 $\mathcal{A}=\{\text{解析多項式}\}$ 含常數、分離點，但 $\bar z\notin\overline{\mathcal{A}}$ ——不共軛封閉的代數會漏掉「反向旋轉」的資訊。

**一句話結論**：Stone 1930/1937 破案——逼近的本質不是多項式，而是「含常數＋分離點（複數版再加共軛封閉）」的代數判據；凡是能分離空間中任何兩點的代數，就能鋪滿整個 $C(X)$ 。
