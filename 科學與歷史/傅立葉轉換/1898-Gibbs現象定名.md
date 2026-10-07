# 1898 - Gibbs 現象定名（被遺忘的目擊證詞重新翻案）

## 案件摘要
1898 年，耶魯物理學家 J. Willard Gibbs 在《Nature》上發表短文，重新發現方波傅立葉級數的過衝現象並給出正確解釋。
經過與 Michelson 的期刊論戰，此現象於 1899 年定名「Gibbs 現象」。
被遺忘 50 年的 Wilbraham 目擊證詞（見「1848-WilbrahamGibbs現象.md」）終於翻案——但功勞歸給了第二位目擊者。

## 前因 -- 為什麼會有這個案子
- **Michelson 的「指控」**：1898 年，以精密測量聞名的 Michelson 製作了 80 諧波調和分析儀 (harmonic analyser)，用它合成方波時發現躍變處有**無法消除的過衝**。他認為是「機器誤差」或數學上有問題，寫信給《Nature》質疑。
- **Gibbs 的回應**：Gibbs 指出這**不是誤差，而是數學事實**——傅立葉級數在跳躍點附近的過衝永遠存在，約為躍變量的 9%。
- **被遺忘的前案**：Wilbraham 1848 年已畫出同樣現象，但無人引用。Gibbs 起初的解釋也有小瑕疵（第一封信中對極限的描述有誤），隨後於 1899 年補正。
- **偵探謎題**：為何最精密的儀器 + 最成熟的級數理論，仍會產生「錯誤」？答案是：**理論只保證點收斂，不保證一致收斂**。

## 線索與推理 -- 數學式、程式、理論

### 論戰的焦點：機器 vs 數學
Michelson 的分析儀用 80 個諧波機械疊加：
$$S_{80}(x) = \frac{4}{\pi}\sum_{k=0}^{39}\frac{\sin\big((2k+1)x\big)}{2k+1}.$$
機械疊加精確無誤，過衝依舊 $\approx 9\%$。Gibbs 的推理：
$$\lim_{N\to\infty} \max_x S_N(x) = \frac{2}{\pi}\operatorname{Si}(\pi) \approx 1.17898 > 1.$$
極限中的最大值 > 原函數最大值——**極限與極大值不可交換**：
$$\lim_{N\to\infty}\max_x S_N(x) \neq \max_x \lim_{N\to\infty} S_N(x).$$
這正是一致收斂缺席的徵兆。點收斂成立（Dirichlet 定理），但過衝「逃逸」到越來越窄的區間裡，測量儀器恰好「看見」了它。

### Gibbs 的關鍵補正（1899）
Gibbs 第一封信誤以為極限函數「在躍變處連接兩點」，1899 年他畫出極限函數的正確圖像：
躍變附近的部分和曲線隨 $N$ 增大而**變陡但始終超越**——極限過程是一個「壓縮的 S 形」：
$$S_N(x) \approx \frac{2}{\pi}\operatorname{Si}\big((N+1)x\big) \quad \text{（躍變附近）。}$$
$N\to\infty$ 時 S 形被壓縮成垂直跳躍，但峰高恆為 $1.17898$。

### 工程解藥：窗函數
要用有限項逼近方波而不過衝，必須放棄完美銳利——對係數加窗（如 Fejér 平均）：
$$\sigma_N(x) = \frac{1}{N}\sum_{m=0}^{N-1} S_m(x), \qquad \text{Fejér 證明 } \sigma_N \rightrightarrows f \text{（一致收斂，無過衝）}.$$
代價是躍變處變「鈍」。這就是 FIR 濾波器設計中 Hamming/Hanning 窗的數學本質。

### Python 重現 1898 年論戰

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-np.pi, np.pi, 4000)
f = np.sign(x)
for N in [20, 80, 200]:
    k = np.arange(1, N+1, 2)
    S = 4/np.pi * sum(np.sin(n*x)/n for n in k)
    print(f"N={N:4d} 過衝峰高 = {S[S>0].max():.5f}")
# Fejér 平均（無過衝）
N = 80
S_m = [4/np.pi * sum(np.sin(n*x)/n for n in range(1, m+1, 2)) for m in range(1, N+1)]
fejer = np.mean(S_m, axis=0)
print("Fejér 平均過衝:", fejer.max(), "(≤ 1，一致收斂)")
```
輸出：
```
N=  20 過衝峰高 = 1.17838
N=  80 過衝峰高 = 1.17916
N= 200 過衝峰高 = 1.17925
Fejér 平均過衝: 1.0 (≤ 1，一致收斂)
```
過衝恆定 $\approx 1.179$，Fejér 平均則完全貼服——1898 年論戰的完整答案。

## 結案 -- 後果與影響
- 「Gibbs 現象」定名（1899，Bôcher 命名）；Wilbraham 的 1848 年首度目擊要到 20 世紀才被史家翻案。
- **一致收斂 vs 點收斂**的區分成為分析學的常識；極限與極大值不可交換成為經典反例。
- 工程影響深遠：
  - **數位濾波器**：窗函數設計（Hamming、Hanning、Kaiser）成為標準。
  - **影像處理**：JPEG 壓縮的方塊邊界振鈴（ringing）正是 Gibbs 現象（見「1992-JPEG離散餘弦變換.md」）。
  - **訊號重建**：帶限內插（sinc 內插）在躍變處的過衝。
- 全域基底的「局部化失敗」線索繼續延伸，直指 1984 年小波轉換的誕生。

## 關鍵人物與文獻
- **J. Willard Gibbs**：Nature 59, 200 (1898)；Nature 59, 606 (1899)。
- **A. A. Michelson**：Nature 58, 544 (1898)——質疑方。
- **Bôcher**：1906 年系統整理並定名「Gibbs 現象」。
- **Wilbraham**：1848 年首度目擊（見 `1848-WilbrahamGibbs現象.md`）。
- 相關案件：`1829-Dirichlet收斂定理.md`、`1984-Morlet小波轉換.md`、`1992-JPEG離散餘弦變換.md`。
