# 2000 -- Almgren–Chriss 最佳執行演算法：大單怎麼賣

## 案件描述

2000 年，Robert Almgren（普林斯頓）與 Neil Chriss（高盛）在《Journal of Risk》發表《Optimal Execution of Portfolio Transactions》。他們解決了一個實務上每天發生數百萬次的問題：

> **基金要賣出 100 萬股，一次全賣會砸垮價格、分太多次賣又承受市場風險——怎麼賣最好？**

答案是一個優雅的最佳化問題：**在「市場衝擊成本」與「時間風險」之間求平衡**。這篇論文催生了「最佳執行」（optimal execution）這個學科，也是今日演算法交易（algo trading）的數學基礎。

## 前因：大單的兩難

- 1990 年代機構投資者的單量越來越大，一次市價單會造成巨大的**市場衝擊**（market impact）。
- 傳統做法靠交易員的直覺（VWAP 策略：平均分配在一天內賣）——但沒有理論基礎。
- **線索**：市場衝擊的成本結構已有實證研究（BARRA、Loeb 1983 的「衝擊 ∝ 交易量的平方根」等），但沒有**動態最佳化**框架。
- Almgren（數學家）與 Chriss（數學家出身的交易員）把這變成一個**變分法/最佳控制**問題。

## 推理過程

### 線索一：把執行拆成兩種成本

設總量 $X$ 股、要在時間 $T$ 內賣完。交易軌跡 $x_k$（第 $k$ 期還剩多少），每期賣出 $n_k = x_{k-1} - x_k$。總成本由兩部分構成：

1. **市場衝擊（暫時性 + 永久性）**：
   - 暫時性衝擊：$h(n_k/V) \propto \gamma\, n_k$（賣太快，價格暫時壓低）
   - 永久性衝擊：$g(n_k/V) \propto \eta\, n_k$（賣出的量永久壓低價格）
2. **時間風險**：還沒賣完的部位暴露在價格波動下：$\sigma^2 \sum_k x_k^2 \tau$

**兩難的數學表述**：
- 賣得快（$n_k$ 大）→ 衝擊成本高，但時間風險低
- 賣得慢（$n_k$ 小）→ 衝擊成本低，但時間風險高

### 線索二：效率前緣式的最佳化

Almgren–Chriss 定義「期望成本 + 風險懲罰」的效用：

$$\min_{x_k} \; E[\text{成本}] + \lambda \, \mathrm{Var}[\text{成本}]$$

用變分法求解（拉格朗日 + 離散動態規劃），得到**閉式解**：最優軌跡是指數衰減：

$$x_k = X \, \frac{\sinh(\kappa (T - t_k))}{\sinh(\kappa T)}$$

其中 $\kappa$ 由風險厭惡 $\lambda$、波動率 $\sigma$ 與衝擊係數 $\eta$ 決定：

$$\kappa \approx \sqrt{\frac{\lambda \sigma^2}{\eta}}$$

**解讀**：
- 風險厭惡高（$\lambda$ 大）→ $\kappa$ 大 → 軌跡前重後輕（先賣多、快）
- 風險厭惡低 → $\kappa \to 0$ → 軌跡趨近**線性**（= VWAP 策略！）

**VWAP 策略第一次有了理論基礎**：它正是「無風險厭惡」的特例。

### 線索三：衝擊的平方根律

後續實證（Almgren 2005 等）發現市場衝擊更接近**平方根律**：

$$\text{衝擊} \propto \sigma \sqrt{\frac{Q}{V}}$$

其中 $Q$ 是交易量、$V$ 是日均成交量。這個冪律成為現代執行演算法的實證基礎。

## 現代程式重現：AC 軌跡

```python
import numpy as np

def ac_trajectory(X, T, sigma, eta, lam, n=100):
    """Almgren-Chriss 最優執行軌跡（指數衰減）"""
    t = np.linspace(0, T, n+1)
    kappa = np.sqrt(lam * sigma**2 / eta)
    x = X * np.sinh(kappa * (T - t)) / np.sinh(kappa * T)
    return t, x

# 風險厭惡低 → 接近線性 (VWAP)；高 → 前重後輕
for lam in [0.1, 1.0, 10.0]:
    t, x = ac_trajectory(X=1e6, T=1, sigma=0.02, eta=0.01, lam=lam)
    print(f"lam={lam:>4}: 前 10% 時間賣出 {100*(x[0]-x[int(0.1*len(t))])/x[0]:.0f}%")
```

## 後果

- **演算法交易產業的誕生**：VWAP/TWAP/POV、Implementation Shortfall 演算法——今日機構訂單的絕大多數都由這類演算法執行。
- **高頻交易的理論基礎**：最佳執行是 HFT 的前身——把「怎麼交易」變成數學問題（見 [2010-閃電崩盤與高頻交易.md](2010-閃電崩盤與高頻交易.md)）。
- **學科化**：Cartea–Jaramilloz–Jaimungal（2015）的《Algorithmic and High-Frequency Trading》把最佳執行擴展成隨機控制理論的完整學科。
- **交易的統一理論**：最佳執行、做市（Avellaneda–Stoikov 2008）、流動性供給——都變成「隨機控制 + 效用最佳化」。
- 盲點：衝擊函數是估計出來的（且非線性、狀態相依）；在恐慌中（如 2010 閃電崩盤）衝擊函數本身會劇變。

## 偵探筆記

- 動機：大單的衝擊成本 vs 時間風險兩難
- 工具：變分法/最佳控制、指數衰減閉式解、平方根衝擊律
- 遺產：演算法交易產業、HFT 的理論基礎
- 盲點：衝擊函數在壓力下不穩定

## 參考資料

- Almgren, R., Chriss, N. (2000). "Optimal Execution of Portfolio Transactions". *Journal of Risk*, 3(2), 5–39.
- Cartea, Á., Jaimungal, S., Penalva, J. (2015). *Algorithmic and High-Frequency Trading*. Cambridge University Press.
