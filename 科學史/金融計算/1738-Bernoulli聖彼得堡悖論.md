# 1738 -- Daniel Bernoulli 聖彼得堡悖論：風險厭惡的誕生

## 案件描述

1738 年，瑞士數學家 Daniel Bernoulli 在聖彼得堡科學院發表《風險測度的新理論之闡述》（Specimen theoriae novae de mensura sortis）。他解決了一個困擾數學界 25 年的悖論：

> **聖彼得堡悖論**：一個「期望收益無限大」的賭局，沒有人願意付超過幾十塊錢去玩——為什麼？

他的答案創立了一個全新的概念：**期望效用**（expected utility）與**風險厭惡**（risk aversion）。這是 300 年後 Markowitz（1952）與所有現代金融理論的心理學基礎。

## 前因：無限大的期望

- 1713 年，Daniel 的堂哥 Nicolaus Bernoulli 在寫給 Montmort 的信中提出這個悖論：
  
  > 擲銅板直到出現正面為止。若第 $n$ 次才出現正面，贏 $2^{n-1}$ 元。你願意付多少錢玩？
  
- **數學難題**：期望收益是

  $$E = \sum_{n=1}^{\infty} \frac{1}{2^n} \cdot 2^{n-1} = \sum_{n=1}^{\infty} \frac{1}{2} = \infty$$

  期望無限大——理論上應該願意付任何價錢。但任何人（包括數學家自己）只願意付 10–50 元。**理論與直覺徹底矛盾**。
- **線索**：Daniel Bernoulli 在聖彼得堡與歐拉共事，他追問的不是「怎麼算」，而是「**為什麼算出來的東西不符合人的行為**」——這是從數學到心理學的跳躍。

## 推理過程

### 線索一：價值不是金錢——是效用

Daniel Bernoulli 的洞察：

> **金錢的價值不是線性的——100 元對窮人的價值遠大於對富人的價值。**

他提出用「效用」（moral expectation，後世稱 utility）代替金錢本身：

$$U(w) = \ln(w)$$

**對數效用**：財富越多，每一塊錢的邊際效用越小（**邊際效用遞減**）。

### 線索二：期望效用解開悖論

用對數效用計算聖彼得堡賭局的「期望效用收益」：

$$E[U] = \sum_{n=1}^{\infty} \frac{1}{2^n} \ln(2^{n-1}) = \sum_{n=1}^{\infty} \frac{n-1}{2^n} \ln 2 = \ln 2 < \infty$$

**有限了！** 而且可以反解出「確定等值」（certainty equivalent）：

$$CE = e^{E[U] - \ln(w_0)}$$

對中等財富的人，CE 約為 2–4 元——**與人的實際意願吻合**。

**歷史意義**：這是第一次「**用一個變換（效用函數）修正期望值，使理論符合人的行為**」——這正是現代行為金融與風險管理的哲學起點。

### 線索三：風險厭惡的數學

對數效用的**絕對風險厭惡係數**（Arrow–Pratt 度量，1960 年代正式化）：

$$A(w) = -\frac{U''(w)}{U'(w)} = \frac{1}{w}$$

**解讀**：財富越多，風險厭惡越低——富人比窮人更敢冒險（絕對意義上）。這解釋了：
- 為什麼投資人要**分散投資**（風險厭惡 → 不願承受全部波動）
- 為什麼保險存在（願意付確定的保費，換掉不確定的損失）
- 為什麼避險有價值（見 [1973-BlackScholes選擇權定價.md](1973-BlackScholes選擇權定價.md)）

## 現代程式重現：聖彼得堡悖論與期望效用

```python
import numpy as np

def st_petersburg_payoff(n_sims=1_000_000, seed=0):
    """模擬聖彼得堡賭局：期望無限大，但中位數很小"""
    rng = np.random.default_rng(seed)
    # 幾何分配：第 n 次才出現正面的機率 = (1/2)^n
    n = rng.geometric(0.5, n_sims)          # 第一次正面出現在第 n 次
    payoff = 2.0**(n - 1)
    return payoff

payoff = st_petersburg_payoff()
print("樣本期望（有限的樣本下）:", payoff.mean())     # 隨模擬數發散
print("中位數:", np.median(payoff))                   # 1 — 大多數人只贏 1 元
print("P(payoff > 100):", (payoff > 100).mean())      # 極小 — 無限期望來自極罕見的巨大支付

# 對數效用下的確定等值
w0 = 1000
E_log = np.mean(np.log(payoff + 1e-9))
CE = w0 * np.exp(E_log)
print("確定等值（財富 1000）:", CE)   # 幾塊錢 — 符合人的實際意願
```

## 後果

- **期望效用理論**：經 von Neumann–Morgenstern（1944）公理化，成為現代經濟學的決策理論基石。
- **Markowitz 的哲學基礎**（1952，見 [1952-Markowitz投資組合理論.md](1952-Markowitz投資組合理論.md)）：「投資人關心報酬與風險」——背後正是 Bernoulli 的風險厭惡。Markowitz 自己承認效用理論是先決條件。
- **Arrow–Pratt 風險厭惡度量**（1960s）：把 Bernoulli 的直覺正式化，成為資產定價（CAPM 的風險溢價）的理論語言。
- **保險經濟學**：風險厭惡解釋了保險的需求——「願意付確定的小錢，換掉不確定的大損失」。
- **行為金融的挑戰**：Allais 悖論（1953）與 Kahneman–Tversky 的展望理論（1979）發現人的實際行為違反期望效用——「效用革命」之後的「行為革命」。
- 期望無限大的悖論的另一條解法：**現實中的賭局有上限**（莊家的財富有限）——「有限莊家」版本（Buffon 也討論過）的期望值是有限的。

## 偵探筆記

- 動機：期望無限大 vs 人的實際意願的矛盾
- 工具：對數效用、邊際效用遞減、確定等值、風險厭惡係數
- 遺產：期望效用理論、Markowitz 的哲學基礎、保險經濟學
- 盲點：實際人違反期望效用（Allais、展望理論）——行為金融的戰場

## 參考資料

- Bernoulli, D. (1738). *Specimen theoriae novae de mensura sortis*.（英譯：Sommer, L. (1954). "Exposition of a New Theory on the Measurement of Risk". *Econometrica*.）
- von Neumann, J., Morgenstern, O. (1944). *Theory of Games and Economic Behavior*.
