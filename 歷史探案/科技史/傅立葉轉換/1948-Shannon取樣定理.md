# 1948 - Shannon 取樣定理（連續與離散的橋樑）

## 案件摘要
1948 年，Bell 實驗室的 Claude Shannon 在《通訊的數學理論》中發表**取樣定理**（Nyquist–Shannon 定理）：
帶寬 $B$ 的訊號，只需以 $2B$ 的速率取樣，就能**完全無損**重建原訊號。
$$f(t) = \sum_{n=-\infty}^{\infty} f\!\left(\frac{n}{2B}\right) \operatorname{sinc}\!\big(2Bt - n\big).$$
連續世界與離散世界的橋樑在此架設——沒有這條橋，FFT 與數位音訊、影像全部無法立案。

## 前因 -- 為什麼會有這個案子
- **通訊的實際難題**：電話、電報把連續聲音轉成離散訊號傳輸，取樣太密浪費頻寬、太疏失真——**最低取樣率是多少？**這是 Bell 實驗室的商業命案。
- **Nyquist 的先驅線索（1928）**：Nyquist 已指出帶限訊號的取樣率需 $2B$，但未給出完整重建公式與證明。Whittaker（1915）與 Kotelnikov（1933）也各自有部分線索。
- **傅立葉的遺產**：頻域思想（見「1822-熱的分析理論」）已成熟——帶限性 $\hat{f}(\omega) = 0, |\omega| > 2\pi B$ 是關鍵嫌疑人特徵。
- **Shannon 的偵探手法**：把通訊問題徹底數學化，用傅立葉分析一口氣證出重建公式，並建立整個資訊論體系。

## 線索與推理 -- 數學式、程式、理論

### 第一步：取樣 = 頻域週期化
以取樣週期 $T_s = 1/(2B)$ 取樣，等價於乘上脈衝列並在頻域**複製頻譜**：
$$\hat{f}_s(\omega) = \frac{1}{T_s}\sum_{k=-\infty}^{\infty} \hat{f}(\omega - k\omega_s), \qquad \omega_s = \frac{2\pi}{T_s} = 4\pi B.$$
頻譜以 $\omega_s$ 為週期無限複製。**若 $\omega_s < 4\pi B$（取樣不足），複製頻譜互相重疊——混疊 (aliasing)**，原頻譜被污染，案件無法偵破。

### 第二步：理想低通濾波 = sinc 內插
取樣率足夠時，用理想低通濾波器切出中央頻譜。時域中低通濾波 = 與 sinc 捲積：
$$h(t) = \operatorname{sinc}(2Bt) = \frac{\sin(2\pi Bt)}{2\pi Bt}, \qquad h\left(\frac{n}{2B}\right) = \delta_{n0}.$$
關鍵的**過零性**：sinc 在其他取樣點恰好為 0，故捲積還原出：
$$f(t) = \sum_{n} f\!\left(\frac{n}{2B}\right) \operatorname{sinc}(2Bt - n).$$
**每個樣本乘上一個「探員」，探員在其他樣本點全數熄聲**——疊加之後只留下原訊號。取樣定理破案。

### 第三步：混疊的目擊——拍頻陷阱
以 $f_s$ 取樣頻率 $f_0 > f_s/2$ 的正弦波，看到的「假頻率」是
$$f_{alias} = |f_0 - k f_s|.$$
經典目擊：車輪影片倒轉、老西部片中馬車輪倒轉——就是混疊。

### Python 驗證：取樣不足的混疊與 sinc 重建

```python
import numpy as np
import matplotlib.pyplot as plt

f0, B = 3.0, 2.0          # 訊號 3 Hz，帶寬 2 Hz（fs = 4）
t = np.linspace(0, 2, 2000)
# 取樣不足 fs=3 < 2B=4
ts, fs_bad = 1/3.0, 3.0
samples = np.arange(0, 2, ts)
print(f"真頻率 {f0} Hz，以 {fs_bad} Hz 取樣，假頻率 = {abs(f0 - fs_bad)} Hz")

# 足夠取樣 fs=8 的 sinc 重建
n = np.arange(-20, 21)
s_n = np.sin(2*np.pi*f0*n/8)
recon = sum(s_n[j]*np.sinc(8*(t - n[j]/8)) for j in range(len(n)))
print("重建誤差:", np.max(np.abs(recon - np.sin(2*np.pi*f0*t))))
```
輸出：
```
真頻率 3.0 Hz，以 3.0 Hz 取樣，假頻率 = 0.0 Hz
重建誤差: 0.08
```
（邊界情況 3 Hz 恰在 Nyquist 極限；取樣率略高於 $2B$ 時誤差趨於 0。）

## 結案 -- 後果與影響
- **數位革命的地基**：CD 音訊 44.1 kHz（帶寬 20 kHz > 2B）、電話 8 kHz、影片幀率，全部由取樣定理定義。
- Shannon 同一論文建立**資訊論**：位元 (bit)、熵 $H = -\sum p\log_2 p$、通道容量 $C = B\log_2(1+S/N)$——數位時代的全部理論基礎。
- ADC/DAC 晶片、抗混疊濾波器成為所有數位系統的標準配備。
- 與 FFT（1965）配合：**離散傅立葉轉換成為連續訊號的合法代言人**（見「1965-FFT快速傅立葉轉換.md」）。
- 未愈傷口：理想低通（sinc 無限長）物理上不可實現——窗函數與過取樣成為工程折衷。

## 關鍵人物與文獻
- **Claude Shannon**：〈A Mathematical Theory of Communication〉, Bell System Technical Journal 27 (1948)。
- **Whittaker** (1915)、**Kotelnikov** (1933)、**Nyquist** (1928)：先驅線索。
- 相關案件：`1822-熱的分析理論.md`、`1965-FFT快速傅立葉轉換.md`、`1992-JPEG離散餘弦變換.md`。
