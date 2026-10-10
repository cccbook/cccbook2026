# 1909-Riesz表示定理

## 案件檔案表

| 項目 | 內容 |
|------|------|
| 發生時間 | 1909 年（Frigyes Riesz 發表定稿論文） |
| 發生地點 | 匈牙利布達佩斯（發表於 Annalen） |
| 報案人 | 1907 年初版的遺留疑點： $\alpha$ 不唯一，測度與泛函的關係不明 |
| 偵探 | Frigyes Riesz |
| 兇器 | 積分器 $\alpha$ 的多重面目：加常數、拆分方式不同，同一泛函多種表示 |
| 結論 | 表示定稿與唯一性確立， $\alpha$ 有界變差，測度從泛函中長出來 |

## 案發現場

1907 年，Riesz 證明了 $C[a,b]$ 上有界線性泛函的表示： $\Phi(f) = \int_a^b f\, d\alpha$ 。但初版留下兩個疑點：

1. ** $\alpha$ 不唯一**： $\alpha$ 加一個常數， $d\alpha$ 不變，表示式照樣成立；更糟的是， $\alpha$ 的取法有多種規範（左連續？右連續？端點值怎麼定？），同一個泛函對應多個 integrator。
2. **測度的地位不明**：Riemann–Stieltjes 積分是「分析」的工具，而 Lebesgue 測度論（1902）是「測度」的理論。兩者的關係是什麼？泛函 $\Phi$ 到底是在「對應一個函數 $\alpha$ 」，還是在「對應一個測度 $\mu$ 」？

**謎題升級：** 能否給 $\alpha$ 一個**唯一**的規範化，並證明泛函與測度是同一枚硬幣的兩面？

Riesz 在 1909 年的定稿論文中（發表於 Annalen）收網。這篇論文也正式奠定了**對偶理論**的地基。

## 偵查過程

### 線索一：泛函長出區間函數—— $\alpha$ 的本質

回顧 1907 年的偵查：泛函 $\Phi$ 對區間的「反應」是

$$
\alpha_\Phi(x) = \Phi(\mathbf{1}_{[a,x]}) \quad (\text{適當極限定義}) .
$$

更自然地，泛函對**區間本身**的賦值是

$$
\mu_\Phi\big( (s, t] \big) = \alpha_\Phi(t) - \alpha_\Phi(s) .
$$

Riesz 觀察到： $\mu_\Phi$ 是區間集合上的**有限可加集函數**——它有測度的所有雛形：

- 非負性（當 $\Phi$ 是正泛函時）；
- 可加性： $\mu((s,u]) = \mu((s,t]) + \mu((t,u])$ ；
- 全質量有限： $|\mu_\Phi|([a,b]) \le \|\Phi\|$ 。

### 線索二：唯一性的偵查——規範化

為什麼 $\alpha$ 不唯一？因為 Stieltjes 積分只看 $\alpha$ 的**增量**，不看端點。Riesz 的規範化方案：

**規範一（標準）**：要求 $\alpha$ 右連續且 $\alpha(a) = 0$ 。

在這個規範下，若兩個有界變差函數 $\alpha_1, \alpha_2$ 滿足

$$
\int_a^b f\, d\alpha_1 = \int_a^b f\, d\alpha_2 \quad \text{對所有 } f \in C[a,b] ,
$$

則對所有 $t \in (a, b]$ ，取階梯近似 $f_n \to \mathbf{1}_{(a,t]}$ ，得

$$
\alpha_1(t) - \alpha_1(a) = \alpha_2(t) - \alpha_2(a) \implies \alpha_1(t) = \alpha_2(t) .
$$

**結論**：規範化後 $\alpha$ **唯一**。疑點一收網。

### 線索三：Jordan 分解——有界變差的解剖

對一般（不必正的）泛函， $\alpha_\Phi$ 是有界變差函數。Riesz 用 **Jordan 分解**解剖它：

$$
\alpha = \alpha^+ - \alpha^- , \qquad
\alpha^+(x) = \tfrac{1}{2} \big( V_a^x(\alpha) + \alpha(x) - \alpha(a) \big), \quad
\alpha^-(x) = \tfrac{1}{2} \big( V_a^x(\alpha) - \alpha(x) + \alpha(a) \big) ,
$$

其中 $V_a^x(\alpha)$ 是 $[a,x]$ 上的總變差。 $\alpha^+$ 與 $\alpha^-$ 都是遞增函數，於是

$$
\Phi(f) = \int_a^b f\, d\alpha^+ - \int_a^b f\, d\alpha^- .
$$

**正泛函與負泛函分家**：每個有界線性泛函都是兩個正泛函之差——這正是日後符號測度理論的胚胎。

### 線索四：測度從泛函中長出來

規範化後的 $\alpha^+$ 、 $\alpha^-$ 是遞增右連續函數，它們各自誘導一個 **Lebesgue–Stieltjes 測度**：

$$
\mu^+\big( (s, t] \big) = \alpha^+(t) - \alpha^+(s), \qquad
\mu^-\big( (s, t] \big) = \alpha^-(t) - \alpha^-(s) .
$$

由 Carathéodory 擴張定理（1918 年定稿，此處是先聲），區間上的集函數可以唯一擴張成 Borel 集上的測度。於是表示式升級為

$$
\Phi(f) = \int_a^b f(x)\, d\mu^+(x) - \int_a^b f(x)\, d\mu^-(x) = \int_{[a,b]} f\, d\mu ,
$$

其中 $\mu = \mu^+ - \mu^-$ 是**符號測度**。

| 1907 年初版 | 1909 年定稿 |
|-------------|-------------|
| $\Phi(f) = \int f\, d\alpha$ （Riemann–Stieltjes） | $\Phi(f) = \int_{[a,b]} f\, d\mu$ （Lebesgue–Stieltjes） |
| $\alpha$ 有界變差但不唯一 | 規範化後唯一（右連續、 $\alpha(a)=0$ ） |
| 分析工具 | 測度誕生：泛函 = 符號測度 |
| 樣本驗證 | Jordan 分解 + 測度擴張 |

### 線索五：範數與全變差——對偶的幾何量

定稿的最後一塊拼圖：

$$
\|\Phi\| = |\mu|([a,b]) = V(\alpha) ,
$$

其中 $|\mu| = \mu^+ + \mu^-$ 是 $\mu$ 的全變差測度。泛函空間的幾何量（範數）與測度論的分析量（全變差）畫上等號——對偶空間 $(C[a,b])^*$ 從此有了精確的解剖圖。

## 結案報告

1. **表示定理定稿**： $C[a,b]$ 上每個有界線性泛函唯一地對應一個規範化的有界變差函數 $\alpha$ （右連續、 $\alpha(a) = 0$ ），表示為 $\Phi(f) = \int f\, d\alpha$ 。
2. **測度從泛函中長出來**： $\alpha$ 的 Jordan 分解誘導符號測度 $\mu = \mu^+ - \mu^-$ ，泛函與測度是同一枚硬幣的兩面。
3. **範數 = 全變差**： $\|\Phi\| = |\mu|([a,b])$ ，對偶空間的幾何量與分析量統一。
4. **遺產**：
   - 此定理是**對偶理論的基石**：日後抽象化為 Hilbert 空間的 Riesz 表示、 $L^p$ 對偶（ $(L^p)^* = L^q$ ）、以及一般 $C(X)$ 上的 Riesz–Markov 表示定理。
   - **Radon–Nikodym 伏筆**：Radon（1913）沿此路線研究 Stieltjes 積分與測度的導數，Radon–Nikodym 定理（1930 定稿）由此醞釀——「測度從泛函中長出來」的精神，日後反轉為「密度從測度中長出來」。
   - 測度論與泛函分析的合流，為机率論（Kolmogorov 公理化）與分布理論鋪路。

## 證據與工具

| 證據/工具 | 陳述 | 用途 |
|-----------|------|------|
| 區間集函數 | $\mu_\Phi((s,t]) = \alpha(t) - \alpha(s)$ | 測度的雛形 |
| 規範化 | $\alpha$ 右連續且 $\alpha(a) = 0$ | 唯一性的鑰匙 |
| Jordan 分解 | $\alpha = \alpha^+ - \alpha^-$ ，皆遞增 | 符號測度的解剖 |
| 全變差測度 | $|\mu| = \mu^+ + \mu^-$ | $\|\Phi\| = |\mu|([a,b])$ |
| Lebesgue–Stieltjes 測度 | $\mu((s,t]) = \alpha(t) - \alpha(s)$ 擴張成 Borel 測度 | 測度誕生的產房 |

**證明骨架**（唯一性 + 測度誕生）：

```
Φ 有界線性於 C[a,b]
  → α_Φ(x) = Φ(1_[a,x])，規範化（右連續、α(a)=0）
  → 唯一性：階梯近似 1_(a,t] ⇒ α₁(t) = α₂(t)
  → Jordan 分解：α = α⁺ − α⁻（皆遞增右連續）
  → Lebesgue–Stieltjes 測度 μ± 誕生
  → Φ(f) = ∫ f dμ，‖Φ‖ = |μ|([a,b])
```

**一句話結案**：Riesz 在 1909 年定稿收網——規範化還 $\alpha$ 以唯一身分，Jordan 分解讓測度從泛函中長出來，對偶理論的基石就此落定，Radon–Nikodym 的伏筆悄然埋下。
