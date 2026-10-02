# 2000 -- David X. Li 的高斯 Copula：CDO 的定時炸彈

## 案件描述

2000 年，任職於加拿大 CIBC 的精算師 David X. Li 在《Journal of Fixed Income》發表《On Default Correlation: A Copula Function Approach》。他解決了一個當時 Credit Derivatives 業界最頭痛的問題：

> **如何為「多個借款人同時違約」的相關性建模？**

他的答案優雅得可怕：用一個高斯 Copula 把多個個別違約時間「黏」在一起。這個公式後來被業界奉為「定價聖杯」，用來為數兆美元的 CDO 定價——並在 2008 年成為金融海嘯的技術核心。

《Wired》雜誌 2009 年的名文《The Formula That Killed Wall Street》就是講這個公式。

## 前因：違約相關性之謎

- 1990 年代末，信用衍生品（CDS、CDO）市場起飛。CDO 的結構：把一籃子債券/貸款的現金流分層（tranche），高層先吸收違約損失……不對——**低層（equity）先吸收損失，高層（senior）最後**。
- 核心數學難題：要為分層定價，必須知道「**多少借款人會同時違約**」——即違約時間的**聯合分配**。個別違約率容易估（信用評等 + 市場價差），但**相關結構**幾乎沒有資料（違約是稀有事件，觀測不到足夠的聯合樣本）。
- **線索**：Li 是精算師出身（曾研究壽險的死亡相關性——配偶同時死亡的精算模型），他把壽險的「 mortality copula」想法搬到信用市場。

## 推理過程

### 線索一：Sklar 定理——Copula 的數學基礎

Sklar 定理（1959）：任何聯合分配都可以拆成「邊際分配 + 相依結構（copula）」：

$$F(x_1, \dots, x_n) = C(F_1(x_1), \dots, F_n(x_n))$$

其中 $C$ 是 copula——純粹描述「相關結構」的函數。Li 的洞察：**既然違約的邊際容易估、聯合觀測不到，那就假設一個 copula**。

### 線索二：高斯 Copula 的具體形式

Li 的模型：違約時間 $\tau_i$ 的邊際用風險中立下的生存函數（由 CDS 價差推出），相關結構用**單因子高斯 Copula**：

$$\tau_i = \Phi^{-1}\left(F_i(\tau_i)\right) = a_i Z + \sqrt{1-a_i^2}\, \varepsilon_i, \quad Z, \varepsilon_i \sim N(0,1)$$

其中 $Z$ 是共同因子（經濟體質）、$\varepsilon_i$ 是個別風險、$a_i$ 是相關係數。

**實務簡潔性**：整個 CDO 的分層定價只需要**一個相關係數**——業界很快把「base correlation」變成標準報價。一個數字決定數兆美元的定價。

### 線索三：公式為什麼如此致命

高斯 Copula 的隱含性質：**尾部相關太弱**。

$$P(\tau_1 > t \mid \tau_2 > t) \to \text{常數} \quad (\text{as } t \to \infty)$$

高斯分配的尾部是「指數衰減」的——它說：**極端事件（大量借款人同時違約）幾乎不可能同時發生**。這在 2008 年被證明是致命錯誤：

- 房市崩盤時，所有 MBS 的違約**同時**爆發——相關性收斂到 1。
- 用高斯 Copula 定價的 AAA 級 CDO 分層，在危機中違約率遠超模型預測。

**偵探的核心推理**：錯的不是「用 copula」這個想法，而是**用高斯這個特定的 copula**——它把「多個借款人」想像成多元常態，而真實世界的違約是**跳躍式的、傳染式的**。

## 現代程式重現：高斯 Copula 的尾部相關性

```python
import numpy as np

def gaussian_copula_tail(n_sims=1_000_000, rho=0.5, seed=0):
    """模擬高斯 Copula：檢驗尾部相關"""
    rng = np.random.default_rng(seed)
    Z = rng.standard_normal(n_sims)
    e1, e2 = rng.standard_normal(2*n_sims).reshape(2, -1)
    x = np.sqrt(rho)*Z + np.sqrt(1-rho)*e1
    y = np.sqrt(rho)*Z + np.sqrt(1-rho)*e2
    # 一般相關 vs 尾部相關
    corr_all = np.corrcoef(x, y)[0,1]
    # 條件相關：給定 y 在尾部（> 3 個標準差），x 也超過同樣門檻的機率
    tail_y = y > 3
    tail_corr = (x[tail_y] > 3).mean()
    return corr_all, tail_corr

corr, tail = gaussian_copula_tail(rho=0.5)
print(f"整體相關 = {corr:.3f}")
print(f"P(x>3 | y>3) = {tail:.3%}")
# 高斯 Copula：即使 rho=0.5，尾部共同超標機率仍極低
# 真實違約（t-Copula、跳躍傳染）的尾部共同機率遠高於此 — 這是 2008 的漏洞
```

## 後果

- **2000–2007**：高斯 Copula 成為 CDO 定價的業界標準。CDO 市場從數千億暴增到數兆美元。Li 自己後來說他從未想到公式會被這樣濫用。
- **2008 年**：高斯 Copula 崩潰，CDO 的 AAA 分層大規模違約——見 [2008-金融海嘯與CDO.md](2008-金融海嘯與CDO.md)。
- **修正路線**：
  - **t-Copula**：厚尾的 copula，尾部相關更強
  - **動態相關模型**：相關性隨危機上升（DCC-GARCH）
  - **由下而上的傳染模型**：違約像流行病一樣傳播（Giesecke、Longstaff 等）
  - **因子模型 + 蒙地卡羅**：不假設解析結構，直接模擬
- **監管教訓**：巴塞爾協定 III（2010）提高資本要求、加入壓力測試——「一個相關係數決定數兆美元」的時代結束。
- Li 本人在 2008 年後淡出業界，接受《WSJ》訪問時說：「破壞模型的最簡單方法，就是所有人都使用它。」

## 偵探筆記

- 動機：違約相關結構無資料可估
- 工具：Sklar 定理、單因子高斯 Copula、風險中立違約時間
- 遺產：CDO 定價標準（以及它的崩潰）、尾部相關性的教訓
- 盲點：高斯尾部的指數衰減嚴重低估共同違約；單一參數的簡潔性成為濫用的溫床

## 參考資料

- Li, D. X. (2000). "On Default Correlation: A Copula Function Approach". *Journal of Fixed Income*, 9(4), 43–54.
- Salmon, F. (2009). "The Formula That Killed Wall Street". *Wired*, 17(3).
- Sklar, A. (1959). "Fonctions de répartition à n dimensions et leurs marges". *Publications de l'Institut de Statistique de l'Université de Paris*.
