# 1982 - Aspect 實驗

## 案件摘要
Bell 把哲學變成實驗，但早期實驗留有漏洞。1982 年 Alain Aspect 在巴黎光學研究所完成決定性實驗：以鈣原子級聯躍遷產生糾纏光子對，並用 13 奈秒的快速切換「在光子飛行途中」改變測量方向。結果違反 Bell 不等式，局域隱變數理論被判死刑。

## 前因 -- 為什麼會有這個案子
- 1964 年 Bell 不等式給出判決標準：局域實在論要求 $|S| \leq 2$，量子力學預測 $S = 2\sqrt{2}$。
- 1972 年 Freedman–Clauser 前驅實驗（UC Berkeley）：用鈣原子級聯躍遷的偏振糾纏光子對，首次測得違反（違反幅度約 6 個標準差），支持量子力學。
- 但 Freedman–Clauser 與後續實驗的測量方向是**事先固定的**——批評者（包括 Bell 本人）指出：也許光源與分析器之間有未知訊號交換，即「局域性漏洞」仍未關閉。
- Aspect 的目標：讓測量選擇在光子離開光源**之後**才決定，使任何潛在通訊來不及發生。

## 線索與推理 -- 數學式、程式、理論

### 實驗設計
1. **光源**：氪離子雷射激發鈣原子束，鈣原子發生級聯躍遷（$J=0 \to J=1 \to J=0$，$4p^2\,^1S_0 \to 4s4p\,^1P_1 \to 4s^2\,^1S_0$，波長 551.3 nm 與 422.7 nm），因初末態總角動量為零，發出的兩個光子偏振**糾纏**：

$$|\psi\rangle = \frac{1}{\sqrt{2}}\left(|x\rangle_1 |x\rangle_2 + |y\rangle_1 |y\rangle_2\right)$$

2. **測量**：兩側各置偏振分析器（可旋轉的偏振片 + 光電倍增管），量子預測的相關為

$$E(\mathbf{a}, \mathbf{b}) = -\cos 2\theta_{ab} \quad (\text{偏振版本})$$

3. **快速切換**：每側分析器由聲光開關（acousto-optical switch）在兩個通道間切換，切換週期約 **13 ns**——比光子在光源與分析器之間飛行時間（約 40 ns）還短，故切換時光子已「上路」，任何隱變數機制來不及預知未來的測量方向。

### CHSH 判決
四組角度下計算

$$|S| = |E(a,b) + E(a,b') + E(a',b) - E(a',b')| \leq 2$$

### 實驗結果
Aspect 等人 1982 年測得

$$S_{exp} \approx 2.7 \pm 0.15$$

明確超過局域實在論上限 2（違反約 5 個標準差），與量子預測 $2\sqrt{2} \approx 2.83$ 在誤差內一致。次年（1982 第二篇）加入時間相依切換的版本同樣違反。

### 模擬：切換時序的意義

```python
import numpy as np

c = 3e8; L = 12  # 光源到分析器距離 ~12 m
flight_time = L / c          # ~40 ns
switch_period = 13e-9        # 13 ns

print(f"光子飛行時間: {flight_time*1e9:.1f} ns")
print(f"分析器切換週期: {switch_period*1e9:.1f} ns")
print("切換比飛行快 -> 光子途中無法得知未來測量方向")
```

## 結案 -- 後果與影響
- **局域隱變數理論被判死刑**：自然界關聯確實「非局域」，Einstein 的局域實在論必須放棄其一。
- **諾貝爾獎 2022**：Aspect、Clauser、Zeilinger 因「糾纏光子實驗、違反 Bell 不等式、開創量子資訊科學」共享諾貝爾物理獎。
- **漏洞（loopholes）與後續**：
  - *偵測漏洞*（detection loophole）：光電倍增管效率低，也許只有「被偵測的子樣本」違反。2013 年後高效率超導偵測器實驗關閉此漏洞。
  - *局域性漏洞*：Aspect 切換仍是準週期；2015 年 Delft（Hensen et al., 金剛石色心）、NIST、Vienna 的「無漏洞 Bell 實驗」以隨機選擇 + 空間分離同時關閉偵測與局域性漏洞；2017 年「cosmic Bell test」以星光決定測量方向。
  - *自由選擇漏洞*：2018 年「BIG Bell Test」以 10 萬名網路人類的隨機輸入選擇測量設定。
- Aspect 實驗奠定量子資訊時代：量子密碼、量子遙傳、裝置無關密碼學都建立在「非局域關聯是真實且可用的」這一判決之上。

## 關鍵人物與文獻
- **Alain Aspect**（1947– ），法國，巴黎-薩克雷大學 / CREST。
- **John Clauser**（1942– ），美國，1972 前驅實驗。
- **Anton Zeilinger**（1945– ），奧地利，量子遙傳與無漏洞實驗先驅。
- Aspect, Dalibard, Roger, "Experimental Test of Bell's Inequalities Using Time-Varying Analyzers", *PRL* **49**, 1804 (1982)。
- Aspect, Grangier, Roger, "Experimental Realization of Einstein-Podolsky-Rosen-Bohm Gedankenexperiment", *PRL* **49**, 91 (1982)。
- Freedman & Clauser, *PRL* **28**, 938 (1972)。
- Hensen et al., "Loophole-free Bell inequality violation...", *Nature* **526**, 682 (2015)。
