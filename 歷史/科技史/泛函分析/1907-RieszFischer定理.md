# 1907-RieszFischer定理

## 案件檔案表

| 項目 | 內容 |
|------|------|
| 發生時間 | 1907 年（春季，Riesz 與 Fischer 各自投稿發表） |
| 發生地點 | 匈牙利布達佩斯（Riesz）與挪威克里斯蒂安尼亞（Fischer） |
| 報案人 | 調和分析（Fourier 級數何時收斂，八十年無定論） |
| 偵探 | Frigyes Riesz 與 Ernst Fischer |
| 兇器 | du Bois-Reymond 的發散怪談：連續函數的 Fourier 級數可以處處發散 |
| 結論 | $L^2$ 完備性證明，Fourier 係數平方和收斂 $\iff$ 函數存在， $L^2$ 與 $\ell^2$ 同構 |

## 案發現場

調和分析的懸案要追溯到 1807 年：Fourier 宣稱「任意函數都能展開成三角級數」

$$
f(x) = \frac{a_0}{2} + \sum_{n=1}^\infty \left( a_n \cos nx + b_n \sin nx \right) .
$$

八十年來，這個宣稱的真相撲朔迷離：

- Dirichlet（1829）：函數分段光滑時級數收斂——但條件太強。
- **du Bois-Reymond（1876）的怪談**：存在**連續**函數，其 Fourier 級數在**一點**發散；更可怕的版本（後被證實）甚至可以處處發散。
- Lebesgue（1902）：新積分理論問世， $L^2$ 空間現形，但它的完備性無人能證。

核心謎題：**給定一組係數 $\{c_n\}$ ，什麼時候它真的是某個函數的 Fourier 係數？** 換句話說，Fourier 展開到底能不能「反著走」？

1907 年春天，兩位年輕人——匈牙利裔的 Riesz（27 歲）與挪威的 Fischer——**幾乎同時、各自獨立**地破案。兩篇論文在同年發表，內容互補，合稱 **Riesz–Fischer 定理**。

## 偵查過程

### 線索一： $L^2$ 空間——Lebesgue 積分的幾何

Lebesgue 積分問世後，平方可積函數構成的空間浮出水面：

$$
L^2[a,b] = \left\{ f : \int_a^b |f(x)|^2\,dx < \infty \right\} ,
$$

配備內積與範數：

$$
\langle f, g \rangle = \int_a^b f(x)\,\overline{g(x)}\,dx, \qquad
\|f\| = \left( \int_a^b |f(x)|^2\,dx \right)^{1/2} .
$$

由 Cauchy–Schwarz 不等式，內積對所有 $f, g \in L^2$ 良定義。三角函數系 $\{1, \cos nx, \sin nx\}$ 是正交系，Fourier 係數是投影：

$$
a_n = \frac{1}{\pi} \int_a^b f(x) \cos nx\,dx, \qquad b_n = \frac{1}{\pi} \int_a^b f(x) \sin nx\,dx .
$$

### 線索二：Bessel 不等式——必要的條件

對任意 $f \in L^2$ ，部分和是最佳逼近，由此得 **Bessel 不等式**：

$$
\sum_{n=1}^\infty |a_n|^2 + |b_n|^2 \le \frac{2}{\pi} \int_a^b |f(x)|^2\,dx = \|f\|^2 \cdot \frac{2}{\pi} .
$$

所以 Fourier 係數**必須**平方可和——這是必要條件。謎題是：它夠嗎？

### 線索三：Fischer 的偵查—— $L^2$ 的完備性

Fischer 從完備性下手。他證明： $L^2$ 中的 Cauchy 序列（在平均平方收斂意義下 $d(f_m, f_n) \to 0$ ）必收斂到某個 $L^2$ 函數。

證明的骨架（後世標準版本）：

1. Cauchy 序列取子列 $f_{n_k}$ 使 $\|f_{n_{k+1}} - f_{n_k}\| \le 2^{-k}$ 。
2. 由 $\|g\|_1 \le \|g\|_2 \cdot \sqrt{b-a}$ ，得 $\sum_k \|f_{n_{k+1}} - f_{n_k}\|_1 < \infty$ ，故
   $$
   f(x) = f_{n_1}(x) + \sum_{k=1}^\infty \big( f_{n_{k+1}}(x) - f_{n_k}(x) \big)
   $$
   幾乎處處絕對收斂，定義出一個可測函數 $f$ 。
3. 由逐項估計 $\|f - f_{n_N}\|_2 \le \sum_{k \ge N} 2^{-k} \to 0$ ，得 $f \in L^2$ 且整個 Cauchy 序列收斂於 $f$ 。

**結論**： $L^2$ 完備。這是 Hilbert 的 $\ell^2$ 完備性（1906）在函數空間的翻版。

### 線索四：Riesz 的偵查——反著走

Riesz 從另一端進攻：給定平方可和的係數序列 $\{c_n\}$ ，構造

$$
s_N(x) = \sum_{n=1}^N c_n \varphi_n(x) ,
$$

其中 $\{\varphi_n\}$ 是標準正交系（如三角系）。由畢氏定理：

$$
\|s_N - s_M\|^2 = \sum_{n=M+1}^N |c_n|^2 \to 0 \quad (M, N \to \infty) ,
$$

故 $(s_N)$ 是 $L^2$ 中的 Cauchy 序列。**Fischer 的完備性在此接手**：存在 $f \in L^2$ 使 $s_N \to f$ （平均平方收斂）。對任意固定的 $\varphi_k$ ，內積連續：

$$
\langle f, \varphi_k \rangle = \lim_{N \to \infty} \langle s_N, \varphi_k \rangle = c_k .
$$

所以 $c_k$ 恰好就是 $f$ 的第 $k$ 個 Fourier 係數——反著走成功。

### 收網：等價性與同構

兩人的工作合起來就是完整的**Riesz–Fischer 定理**：

$$
\{c_n\} \text{ 平方可和} \iff \exists\, f \in L^2 \text{ 使 } c_n = \langle f, \varphi_n \rangle ,
$$

且此時 **Parseval 等式**成立：

$$
\|f\|^2 = \int_a^b |f(x)|^2\,dx = \sum_{n=1}^\infty |c_n|^2 \qquad (\text{完備標準正交系}) .
$$

更深一層：映射 $f \mapsto (\langle f, \varphi_n \rangle)$ 是 $L^2$ 到 $\ell^2$ 的**等距同構**——函數空間與序列空間是同一個空間的兩種面目，Hilbert 的 $\ell^2$ 幾何完全覆蓋了 $L^2$ 。

### 對照表：du Bois-Reymond 怪談 vs Riesz–Fischer 收斂

| 收斂概念 | du Bois-Reymond 怪談（逐點） | Riesz–Fischer（平均平方） |
|----------|------------------------------|----------------------------|
| 收斂對象 | Fourier 級數的部分和 | 部分和序列 $\to f \in L^2$ |
| 失敗案例 | 連續函數可在一點/處處發散 | **無**： $L^2$ 完備，永遠收斂 |
| 度量 | 無統一幾何 | $\|f\|_2$ 誘導的度量 |
| 結局 | 調和分析的噩夢 | 換對收斂概念，噩夢消散 |

## 結案報告

1. ** $L^2$ 完備性**：平均平方收斂下的 Cauchy 序列必收斂於 $L^2$ 函數——Hilbert 幾何在函數空間完全成立。
2. **Fourier 係數的反向定理**： $\sum |c_n|^2 < \infty \iff$ 存在 $f \in L^2$ 以 $\{c_n\}$ 為 Fourier 係數，且 Parseval 等式成立。
3. ** $L^2 \cong \ell^2$ **：等距同構確立，函數空間與序列空間合流，Hilbert 空間理論從此通用。
4. **du Bois-Reymond 怪談的降伏**：逐點收斂的噩夢無法在 $L^2$ 幾何中重演——換用平均平方收斂，Eighty 年的迷霧散盡。這為日後「處處發散 Fourier 級數的 Baire 綱論構造（1960）」埋下伏筆：發散怪談並未消失，只是被完備性關進了另一個房間。

## 證據與工具

| 證據/工具 | 陳述 | 用途 |
|-----------|------|------|
| $L^2$ 空間 | $\int_a^b \lvert f\rvert^2\,dx < \infty$ ，內積 $\int f\bar g$ | 案發地點 |
| Bessel 不等式 | $\sum \lvert c_n\rvert^2 \le \|f\|^2$ | 必要條件 |
| Fischer 完備性 | $L^2$ 中 Cauchy 序列收斂 | 反向構造的接手者 |
| 畢氏定理 | $\|s_N - s_M\|^2 = \sum_{M<n\le N} \lvert c_n\rvert^2$ | 部分和是 Cauchy 序列 |
| Parseval 等式 | $\|f\|^2 = \sum \lvert c_n\rvert^2$ | 等距同構的憑證 |

**證明骨架**（Riesz–Fischer）：

```
係數平方可和 {c_n}
  → 部分和 s_N 是 L² 中的 Cauchy 序列（畢氏定理）
  → Fischer：L² 完備 ⇒ s_N → f ∈ L²
  → 內積連續 ⇒ ⟨f, φ_k⟩ = c_k（反向走成功）
  → Parseval：‖f‖² = Σ|c_n|²（L² ≅ ℓ²）
```

**一句話結案**：Riesz 與 Fischer 各自獨立地證明 $L^2$ 完備——平方可和的係數必屬於某個函數，du Bois-Reymond 的發散怪談被關進逐點收斂的房間，調和分析八十年迷霧就此散盡。
