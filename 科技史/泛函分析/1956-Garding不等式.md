# 1956-Garding不等式

| 案件檔案 | |
|------|------|
| 案發年份 | 1953 提出、1956 定稿（美國，史丹佛） |
| 主嫌 | Gårding 不等式 $B(u,u)\ge\alpha\|u\|_{H^1}^2-\beta\|u\|_{L^2}^2$ |
| 受害者 | Lax–Milgram 的嚴格強制性：許多自然出現的問題不滿足 |
| 關鍵證人 | Lars Gårding（1953 論文、1956 定稿） |
| 結案結果 | 一致橢圓估計問世，正則性理論的基石 |

## 案發現場

1953 年，Lax–Milgram 定理（1954 年發表前夕已流傳）雖然是橢圓邊值問題的萬能鑰匙，卻有一個致命的入場限制：雙線性形式必須**嚴格強制**

$$B(u,u)\ge\alpha\|u\|^2,\qquad \forall u\in H .$$

但自然出現的問題往往不滿足：

1. **含低階項的方程**： $-\Delta u-\lambda u=f$ （Helmholtz 型）， $B(u,u)=\|\nabla u\|^2-\lambda\|u\|^2$ 在 $\lambda>0$ 時不是強制的。
2. **Neumann 問題**（ $c=0$ ）： $B(u,u)=\|\nabla u\|^2$ 在常函數上為零，強制性破產。
3. **高階方程**： $k$ 階橢圓算子的變分形式強制性需要逐項檢查。

謎題的核心：**能否放寬強制性，同時保住存在唯一性與估計？** 這是 Lars Gårding 在史丹佛要接的案子。

## 偵查過程

Gårding 的偵查策略是：**「低階項不傷大雅」——把低階項的破壞力變成可控的負項**。

### 第一步：不等式的誕生

設 $\Omega\subset\mathbb{R}^n$ 有界， $B(u,v)$ 為二階一致橢圓算子 $L$ 的變分形式：

$$B(u,v)=\int_\Omega\sum_{i,j}a_{ij}\,\partial_i u\,\overline{\partial_j v}+\sum_i b_i\,\partial_i u\,\overline v+c\,u\,\overline v\,dx ,$$

其中 $(a_{ij})$ 一致橢圓： $\sum a_{ij}\xi_i\xi_j\ge\lambda|\xi|^2$ 。Gårding 證明存在 $\alpha>0,\ \beta\ge 0$ 使

$$B(u,u)\ge\alpha\|u\|_{H^1}^2-\beta\|u\|_{L^2}^2,\qquad \forall u\in H^1(\Omega) .$$

這就是 **Gårding 不等式**：主部貢獻正項 $\alpha\|u\|_{H^1}^2$ ，低階項只能貢獻可控的負項 $-\beta\|u\|_{L^2}^2$ 。

### 第二步：偵查的兩段式

證明分兩段：

1. **主部估計**：由一致橢圓性，
$$\int_\Omega\sum_{i,j}a_{ij}\,\partial_i u\,\overline{\partial_j u}\,dx\ge\lambda\|\nabla u\|_{L^2}^2=\lambda\big(\|u\|_{H^1}^2-\|u\|_{L^2}^2\big) ;$$
2. **低階項控制**：由 Cauchy–Schwarz 與 $\varepsilon$ -不等式（ $2ab\le\varepsilon a^2+b^2/\varepsilon$ ），把 $b_i$ 與 $c$ 的項吃進去，留下一個 $\beta\|u\|_{L^2}^2$ 的尾巴。

合併兩段即得 Gårding 不等式。關鍵靈感：**低階項在 $H^1$ 中是「緊」的擾動**——它們透過 $L^2$ 作用，而 $H^1\hookrightarrow L^2$ 是緊嵌入（Rellich 定理）。

### 第三步：Rellich 緊性的接手

Rellich 定理（1930）說： $H^1(\Omega)\hookrightarrow\hookrightarrow L^2(\Omega)$ （有界 $\Omega$ ）。Gårding 把它轉化為算子語言：

$$B(u,u)\ge\alpha\|u\|_{H^1}^2-\beta\|u\|_{L^2}^2\ \Longleftrightarrow\ B+\beta\,\langle\cdot,\cdot\rangle_{L^2}\ \text{是}\ H^1\text{-強制的} .$$

於是「加一個 $\beta$ 的位移」就讓 Lax–Milgram 的萬能鑰匙重新開鎖。算子論證如下：

1. 令 $\widetilde B(u,v)=B(u,v)+\beta\int u\overline v\,dx$ ；由 Gårding 不等式 $\widetilde B(u,u)\ge\alpha\|u\|_{H^1}^2$ 。
2. Lax–Milgram： $\widetilde B$ 的方程有唯一解，等價於 $(L+\beta I)$ 可逆。
3. Fredholm 二擇一： $L=(L+\beta I)-\beta I$ 是「可逆算子－緊擾動」，故 $L$ 可逆當且僅當其零空間平凡。

### 第四步：Fredholm 二擇一的抽象版

Gårding 框架下的二擇一：

| 情形 | 條件 | 結論 |
|------|------|------|
| 零空間平凡 | $Lu=0\Rightarrow u=0$ | 對任意 $f$ 有唯一弱解 |
| 零空間非平凡 | 存在非零 $u$ 使 $Lu=0$ | 可解當且僅當 $f$ 與共軛零空間正交 |
| 特徵值 | $L u=\lambda u$ | 特徵值離散，僅可能在 $\lambda\to-\infty$ 積聚 |

特別地，Neumann 問題（ $c=0$ ）：零空間是常函數，可解條件為 $\int_\Omega f\,dx=0$ （與右端積分相容）；這與物理直覺完全吻合。

### 第五步：正則性的橋樑

Gårding 不等式還是正則性理論的第一根支柱：

1. **內部正則性**：若 $f\in L^2$ 、係數光滑，則弱解 $u\in H^2_{\mathrm{loc}}$ （差商論證＋Gårding 估計控制）。
2. **一般階推廣**： $2m$ 階一致橢圓算子滿足 $B(u,u)\ge\alpha\|u\|_{H^m}^2-\beta\|u\|_{L^2}^2$ 。
3. **偽微分算子**：Gårding 不等式推廣為符號計算版 $\mathrm{Re}\,p(x,\xi)\ge c|\xi|^m$ （適當條件下），成為微局部分析的基礎。

## 結案報告

1956 年 Gårding 定稿，宣布結案：低階項的破壞力可控，強制性放寬為「主部強制－低階負項」；加一個位移即可重新套用 Lax–Milgram。案件遺產如下：

- **橢圓估計的一致支柱**：Helmholtz 型問題、Neumann 問題、特徵值問題，全部納入 Gårding–Fredholm 框架。
- **正則性理論的基石**：內部正則性、邊界正則性（Agmon–Douglis–Nirenberg 1959 的 $L^p$ 理論）都以 Gårding 型估計為起點。
- **數值分析的伏筆**：1948 年 Lax 等價定理中「穩定性」的雙線性形式版本，正是 Gårding 估計；位移論證也是離散穩定性的標準技巧。
- **微局部分析的預告**：1960 年代 Hörmander、Nirenberg 的偽微分算子理論中，Gårding 不等式升級為符號層面的強力估計（強 Gårding 不等式）。

## 證據與工具

**關鍵公式一覽表：**

| 工具 | 公式／陳述 | 用途 |
|------|-----------|------|
| Gårding 不等式 | $B(u,u)\ge\alpha\|u\|_{H^1}^2-\beta\|u\|_{L^2}^2$ | 低階項可控 |
| 一致橢圓性 | $\sum a_{ij}\xi_i\xi_j\ge\lambda|\xi|^2$ | 主部估計 |
| $\varepsilon$ -不等式 | $2ab\le\varepsilon a^2+b^2/\varepsilon$ | 吸收低階項 |
| Rellich 緊嵌入 | $H^1\hookrightarrow\hookrightarrow L^2$ | 緊擾動 |
| 位移論證 | $\widetilde B=B+\beta\langle\cdot,\cdot\rangle_{L^2}$ 強制 | Lax–Milgram 開鎖 |
| Fredholm 二擇一 | 可逆 ⟺ 零空間平凡 | 完整可解性 |

**證明骨架：**

1. 一致橢圓性 $\Rightarrow$ 主部 $\ge\lambda\|\nabla u\|^2=\lambda(\|u\|_{H^1}^2-\|u\|_{L^2}^2)$ 。
2. Cauchy–Schwarz ＋ $\varepsilon$ -不等式把 $b_i$ 、 $c$ 的項吸收，尾巴為 $\beta\|u\|_{L^2}^2$ 。
3. 合併得 $B(u,u)\ge\alpha\|u\|_{H^1}^2-\beta\|u\|_{L^2}^2$ 。 $\blacksquare$

**典型例子：** 一維問題 $-u''-\lambda u=f$ ， $u(0)=u(1)=0$ 。 $B(u,u)=\int|u'|^2-\lambda\int|u|^2$ 。由 Poincaré $\|u\|_{L^2}\le\frac{1}{\pi}\|u'\|_{L^2}$ ，得

$$B(u,u)\ge\Big(1-\frac{\lambda}{\pi^2}\Big)\|u'\|_{L^2}^2 .$$

當 $\lambda<\pi^2$ 時嚴格強制（Lax–Milgram 直接開鎖）；當 $\lambda>\pi^2$ 時用 Gårding 位移論證＋Fredholm 二擇一：可解性由零空間（ $\sin(k\pi x)$ 型特徵函數）決定—— $\lambda=\pi^2$ 正是第一個特徵值的臨界位置。
