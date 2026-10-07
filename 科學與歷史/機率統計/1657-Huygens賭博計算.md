# 1657 - Huygens 出版《論賭博中的推理》

## 案件摘要
1657 年，荷蘭科學家 Christiaan Huygens 出版拉丁文小冊《De Ratiociniis in Ludo Aleae》（論賭博中的推理），共 14 個命題與 5 個習題。這是史上第一本正式出版的機率論教科書，把 Pascal 與 Fermat 的書信思想整理成可傳授的公理化體系。

## 前因 -- 為什麼會有這個案子
Pascal 與 Fermat 1654 年解決賭注分配問題的書信並未公開出版。荷蘭數學家 Frans van Schooten 知道此事後，在 1656 年安排 Huygens 訪問巴黎。Huygens 雖未直接讀到書信，但透過 van Schooten 及巴黎數學界（如 Roberval）聽聞了解法的輪廓。

Huygens 決心不依賴聽來的答案，而是**從頭自己重建整個理論**。他在 1656 年完成手稿，1657 年以拉丁文出版於 van Schooten 的《Exercitationum Mathematicarum》附錄中。他在扉頁坦言：「我相信，仔細研究這個問題的人會發現，這不只是賭博的遊戲，而是奠定了一門愉悅而深刻的新理論的基礎。」

## 線索與推理 -- 數學式、程式、理論

### 期望值的公式化：公平賭局的價值

Huygens 的出發點極為聰明：他不定義「機率」，而是直接以**公平賭局**（fair game）定義期望值：

> **命題 3（基本定義）**：若一人在公平賭局中，以機率 $p$ 獲得 $a$、以機率 $q=1-p$ 獲得 $b$，則這個賭局的「價值」為：
>
> $$E = \frac{p \cdot a + q \cdot b}{p + q} = p\,a + q\,b$$

Huygens 特別處理了等可能的情形：若獲得 $a$ 與 $b$ 的機會均等，則賭局價值為 $\frac{a+b}{2}$。他的論證方式是構造性的：把一個賭局拆解成若干「等價的公平子賭局」，若 $n$ 人各自投入 $x$ 元參與等機會的賭局，總獎金 $nx$ 平分給勝者，故單一賭局價值為 $x$。由此可解出 $x$，例如：

- 獲得 $a$ 與 $b$ 機會均等：$\frac{a+b}{2}$
- 獲得 $a, b, c$ 機會均等：$\frac{a+b+c}{3}$
- 獲得 $a$ 佔 1 份、$b$ 佔 2 份：$\frac{a + 2b}{3}$

這正是現代期望值 $E[X] = \sum_i x_i P(x_i)$ 的最早系統表述，只是以「賭局價值」為名。

### 14 個命題的推演結構

Huygens 以命題鏈方式推進，核心命題包括：

- **命題 1–3**：期望值的基本定義與線性組合。
- **命題 4**：賭注分配問題（problem of points）——兩人比數 $a:b$ 時的分配公式：
  $$E(a,b) = \frac{1}{2}E(a+1,b) + \frac{1}{2}E(a,b+1)$$
- **命題 9–12**：多個骰子的擲骰問題，例如「同時擲兩顆骰子，擲出 6 點所需次數的期望值」。
- **命題 14**：著名的「Huygens 問題」——兩人輪流擲一對骰子，A 先擲出雙 6 獲勝，B 先擲出雙 5 獲勝，B 沒擲時 A 先擲，求雙方獲勝機率比（答案 $1 : \frac{31}{...}$ 級的複雜分數）。

### 5 個習題

書末附 5 個習題供讀者練習，其中習題 5 最為著名：

> **習題 5**：A、B 輪流擲一對骰子，先擲出雙 6 者勝。A 先擲，求兩人獲勝機率。

設單局出現雙 6 的機率為 $p = \frac{1}{36}$，A 先擲的獲勝機率為：

$$P_A = \frac{p}{1 - (1-p)^2 \cdot ...} \quad\text{（幾何級數求和）}$$

以現代記號，A、B 輪流時：

$$P_A = \frac{p}{p + (1-p)p\,\big/1} \cdot \frac{1}{1} = \frac{p}{1-(1-p)^2}\Big|_{\text{修正}}$$

精確地：$P_A = \dfrac{p}{1-(1-p)^2}\Big/ 1 = \dfrac{36}{71}$（因 $P_A = p + (1-p)^2 P_A \Rightarrow P_A = \frac{p}{1-(1-p)^2} = \frac{1/36}{1-(35/36)^2} = \frac{36}{71}$）。

### 與 Pascal/Fermat 的關係

Huygens 的書實質上是 Pascal–Fermat 書信內容的**首次公開出版**。他獨立重導了賭注分配的解法，並將期望值提升為整個理論的核心概念——這一點甚至超越了兩位通信者原本的框架。Pascal 得知此書後大為讚賞。

### Python 驗證習題 5

```python
from fractions import Fraction

p = Fraction(1, 36)                     # 單局擲出雙 6 的機率
q = 1 - p
P_A = p / (1 - q*q)                     # A 先擲的獲勝機率
print("A 獲勝機率 =", P_A, "=", float(P_A))   # 36/71 ≈ 0.507

# Monte Carlo 驗證
import random
random.seed(1)
wins = 0
N = 100_000
for _ in range(N):
    turn = 0
    while True:
        d1, d2 = random.randint(1,6), random.randint(1,6)
        if d1 == 6 and d2 == 6:
            wins += (turn == 0)
            break
        turn ^= 1
print("模擬值 =", wins / N)                   # ≈ 0.507
```

## 結案 -- 後果與影響
《De Ratiociniis in Ludo Aleae》在此後約 50 年間是唯一的機率教科書，被譯為法文（1678）與英文。Jacob Bernoulli 在撰寫《Ars Conjectandi》前半部時，直接以註解形式重刊並擴充 Huygens 的 14 個命題；Laplace 則在《機率的解析理論》中把 Huygens 的期望值思想發展成完整的機率公理。期望值從賭桌走向保險、年金與決策理論，Huygens 本人也因此被視為「機率論的奠基者之一」。

## 關鍵人物與文獻
- **Christiaan Huygens**（1629–1695）：荷蘭數學家、物理學家，擺鐘發明者、土星環發現者。
- **Frans van Schooten**（1615–1660）：荷蘭數學家，Huygens 的老師與出版促成者。
- 文獻：C. Huygens, *De Ratiociniis in Ludo Aleae*（1657），收於 van Schooten《Exercitationum Mathematicarum》。
- 後續：J. Bernoulli, *Ars Conjectandi*（1713）第一部分即為 Huygens 論文之重刊與註解。
