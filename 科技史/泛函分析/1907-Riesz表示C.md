# 1907-Riesz表示C

## 案件檔案表

| 項目 | 內容 |
|------|------|
| 發生時間 | 1907 年（Frigyes Riesz 發表表示定理初版） |
| 發生地點 | 匈牙利布達佩斯（發表於巴黎 Comptes Rendus） |
| 報案人 | Fréchet 的追問： $C[a,b]$ 上的連續線性泛函長什麼樣？ |
| 偵探 | Frigyes Riesz |
| 兇器 | 抽象泛函的隱形面目：只知連續線性，不知具體形式 |
| 結論 | $C[a,b]$ 上有界線性泛函皆可表示為 Riemann–Stieltjes 積分 $\Phi(f) = \int f\, d\alpha$ |

## 案發現場

1906 年，Fréchet 在巴黎發明「泛函」（fonctionnelle）一詞，並追問：**無窮維空間上的連續線性泛函，到底長什麼樣？**

具體的案發現場是 $C[a,b]$ ——閉區間上的連續函數空間，配備最大值範數

$$
\|f\| = \max_{x \in [a,b]} |f(x)| .
$$

其上的線性泛函 $\Phi$ 滿足：

$$
\Phi(\alpha f + \beta g) = \alpha\, \Phi(f) + \beta\, \Phi(g) ,
$$

且有界： $|\Phi(f)| \le C \|f\|$ 。

**謎題：** 這些泛函的具體面目是什麼？我們認得幾個樣本——

- $\Phi(f) = \int_a^b f(x)\,dx$ （積分）
- $\Phi(f) = f(c)$ （在點 $c$ 取值，即「點測」）
- $\Phi(f) = \sum_{k=1}^n w_k f(x_k)$ （加權點測）

但**一般的**泛函呢？有沒有一個統一的表示式，把所有連續線性泛函一網打盡？

Hadamard 猜測表示式應該是積分；Riesz 在 1907 年的短文（發表於巴黎科學院報告 Comptes Rendus）中給出了完整的答案——**Stieltjes 積分**登場。

## 偵查過程

### 線索一：Stieltjes 積分——比 Riemann 積分更廣的機器

Stieltjes 於 1894 年引進了一種新積分：給定遞增函數 $\alpha$ （integrator），定義

$$
\int_a^b f(x)\, d\alpha(x) = \lim_{\|P\| \to 0} \sum_{i} f(\xi_i) \big( \alpha(x_i) - \alpha(x_{i-1}) \big) ,
$$

其中 $P: a = x_0 < x_1 < \cdots < x_n = b$ 是分割， $\xi_i \in [x_{i-1}, x_i]$ 。

這台機器的威力在於：**換一個 $\alpha$ ，就換一種積分**。

| integrator $\alpha$ | 積分變成什麼 |
|---------------------|--------------|
| $\alpha(x) = x$ | Riemann 積分 $\int f\,dx$ |
| $\alpha(x) = 0$ （ $x < c$ ）， $1$ （ $x \ge c$ ） | 點測 $f(c)$ |
| 階梯函數 $\sum w_k \mathbf{1}_{x \ge x_k}$ | 加權點測 $\sum w_k f(x_k)$ |
| 一般遞增函數 | 連續與離散的混合 |

點測 $f(c)$ 與 Riemann 積分 $\int f$ 表面上完全不同，卻被同一台機器統一——這正是 Riesz 鎖定的線索。

### 線索二：Riesz 的偵查——從階梯函數下手

Riesz 的策略：先用最簡單的函數「審問」泛函 $\Phi$ 。

1. 對每個分割點 $x$ ，考慮階梯函數 $\mathbf{1}_{[a, x]}$ 的某種連續近似，令
   $$
   g_\Phi(x) = \Phi(\mathbf{1}_{[a,x]}) \quad (\text{經適當極限定義}) .
   $$
   這個函數記錄了泛函對「區間指示函數」的反應——它就是 integrator 的候選人。
2. 線性泛函對階梯函數的和的作用是
   $$
   \Phi\!\left( \sum_i c_i \mathbf{1}_{(x_{i-1}, x_i]} \right) = \sum_i c_i \big( g_\Phi(x_i) - g_\Phi(x_{i-1}) \big) .
   $$
   這正是 Stieltjes 和的形狀。
3. 連續函數 $f$ 可以被階梯函數一致逼近，故由 $\Phi$ 的連續性，
   $$
   \Phi(f) = \lim \sum_i f(\xi_i) \big( g_\Phi(x_i) - g_\Phi(x_{i-1}) \big) = \int_a^b f(x)\, d g_\Phi(x) .
   $$

### 線索三：有界變差——泛函的「總質量」

為了讓表示式乾淨，Riesz 需要控制 $g_\Phi$ 的性質。由 $\Phi$ 有界（ $|\Phi(f)| \le \|\Phi\|\,\|f\|$ ），對任意分割：

$$
\sum_i \big| g_\Phi(x_i) - g_\Phi(x_{i-1}) \big| \le \|\Phi\| \cdot \max_i \|\mathbf{1}_{(x_{i-1}, x_i]}\| \le \|\Phi\| \cdot 1 ,
$$

所以 $g_\Phi$ 是**有界變差**函數，總變差 $\le \|\Phi\|$ 。於是有

$$
\left| \int_a^b f\, d g_\Phi \right| \le \|f\| \cdot V(g_\Phi) \le \|\Phi\|\,\|f\| .
$$

**結論**： $C[a,b]$ 上每個有界線性泛函 $\Phi$ 都可以表示為

$$
\Phi(f) = \int_a^b f(x)\, d\alpha(x) ,
$$

其中 $\alpha$ 是有界變差函數（由 $g_\Phi$ 拆分為增函數之差得到）。反之，每個這樣的積分都定義一個有界線性泛函，且範數滿足

$$
\|\Phi\| = V(\alpha) \quad (\text{取最小變差的代表 } \alpha) .
$$

### 線索四：與 Lebesgue 的雙向奔赴

Riesz 的 1907 年短文與 Fischer 的完備性論文發表在同一期的 Comptes Rendus 上——兩人還在文末互相致謝。這樁巧合的深意是：

| Fischer（1907） | Riesz（1907） |
|------------------|----------------|
| $L^2$ 完備性 | $C[a,b]$ 上泛函的表示 |
| 函數空間的幾何 | 泛函的具體面目 |
| 誰在空間裡 | 誰在對偶面上 |

一個研究空間本身，一個研究空間上的泛函——對偶理論的兩半在同一個春天合流。樣本驗證也全部通過： $\int_a^b f\,dx$ 對應 $\alpha(x) = x$ ，點測 $f(c)$ 對應跳躍 $1$ 的階梯函數，加權點測 $\sum w_k f(x_k)$ 對應跳躍 $w_k$ 的階梯函數——所有樣本一網打盡。

## 結案報告

1. **表示定理初版**： $C[a,b]$ 上每個有界線性泛函皆可表示為 Riemann–Stieltjes 積分 $\Phi(f) = \int_a^b f\, d\alpha$ ， $\alpha$ 為有界變差函數。
2. **範數即總變差**： $\|\Phi\| = V(\alpha)$ （在適當規範下），泛函的幾何量與 integrator 的分析量畫上等號。
3. **積分與點測統一**：Riemann 積分、點取值、加權點測全是同一台 Stieltjes 機器的特例。
4. **遺產**：
   - Riesz 於 1909 年發表定稿，證明 $\alpha$ 的唯一性（規範化後），並從泛函中長出**測度**——測度論與泛函分析的合流。
   - 此定理日後抽象化為 Hilbert 空間上的 Riesz 表示（1907 後）與 $L^p$ 對偶理論，成為對偶理論的基石。
   - Radon–Nikodym 定理（1913 前身）沿此路線醞釀。

## 證據與工具

| 證據/工具 | 陳述 | 用途 |
|-----------|------|------|
| Stieltjes 積分 | $\int_a^b f\, d\alpha = \lim \sum f(\xi_i)\Delta\alpha_i$ | 統一的積分機器 |
| 有界變差 | $\sum \lvert\Delta\alpha_i\rvert \le \|\Phi\|$ | integrator 的質量控制 |
| 一致逼近 | 連續函數被階梯函數一致逼近 | 從階梯推廣到連續 |
| 泛函的連續性 | $\|f_n - f\| \to 0 \Rightarrow \Phi(f_n) \to \Phi(f)$ | 逼近合法化 |
| 範數等式 | $\|\Phi\| = V(\alpha)$ | 幾何量 = 分析量 |

**證明骨架**：

```
泛函 Φ 有界線性於 C[a,b]
  → 審問階梯函數：g_Φ(x) = Φ(1_[a,x])
  → Φ 有界 ⇒ g_Φ 有界變差
  → 階梯函數的 Φ 值 = Stieltjes 和
  → 一致逼近 + 連續性 ⇒ Φ(f) = ∫ f dα
```

**一句話結案**：Riesz 用 Stieltjes 積分審問 $C[a,b]$ 上的所有泛函，積分與點測被同一台機器一網打盡——抽象泛函現出具體面目，對偶理論的第一塊基石落定。
