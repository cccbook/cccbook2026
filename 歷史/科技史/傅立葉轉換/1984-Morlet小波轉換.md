# 1984 - Morlet 小波轉換（突破「全域頻率」的限制）

## 案件摘要
1984 年，法國地球物理學家 Jean Morlet 與瑞士數學物理學家 Alex Grossmann 發表小波轉換 (wavelet transform) 的完整理論：
$$W_f(a,b) = \frac{1}{\sqrt{|a|}}\int_{-\infty}^{\infty} f(t)\,\psi^*\!\left(\frac{t-b}{a}\right) dt.$$
傅立葉轉換的百年難題在此破案：**全域正弦波無法「同時」定位時間與頻率**（Gibbs 現象的根源，見「1898-Gibbs現象定名」）。
小波——可伸縮、可平移的「局部波」——補上了這一塊拼圖。

## 前因 -- 為什麼會有這個案子
- **傅立葉的百年缺陷**：$\sin(\omega t)$ 在整條時間軸上振動——頻譜只告訴你「有哪些頻率」，不告訴你「**何時**出現」。
- **不確定性原理的枷鎖**：時間—頻率同時定位受海森堡式限制
  $$\Delta t \cdot \Delta\omega \ge \frac{1}{2}.$$
  短窗看不清低頻、長窗看不清高頻——**固定窗（短時傅立葉轉換 STFT）無法兩全**：
  $$X(\tau,\omega) = \int x(t)\, w(t-\tau)\, e^{-i\omega t} dt.$$
- **地震波的實際需求**：Morlet 分析油氣勘探的地震反射波——需要**在高頻處用短窗、低頻處用長窗**（時頻解析度隨尺度自適應）。STFT 做不到。
- **Morlet 的偵探直覺**：他是地球物理學家而非數學家，提出「伸縮 + 平移」的小波想法後，找上 Grossmann 用泛函分析證明其嚴格性——**偵探 + 理論家的聯手破案**。

## 線索與推理 -- 數學式、程式、理論

### 第一步：小波 = 可伸縮的探員
取母小波 $\psi$（零均值、局部化的振盪），伸縮參數 $a$（尺度 $\leftrightarrow$ 頻率的倒數）與平移參數 $b$（時間）：
$$\psi_{a,b}(t) = \frac{1}{\sqrt{|a|}}\psi\!\left(\frac{t-b}{a}\right).$$
- $a$ 小 → 小波窄 → **高頻、短窗**（時間解析好）。
- $a$ 大 → 小波寬 → **低頻、長窗**（頻率解析好）。

**解析度自動適配**——Morlet 需要的特性，小波天生具備：
$$\Delta t_{a} \cdot \Delta\omega_{a} \ge \frac12 \text{（恆定下界），但 } \Delta t_a \propto a,\ \Delta\omega_a \propto 1/a.$$

### 第二步：嚴格性——容許條件與重構公式
Grossmann 證明：只要 $\psi$ 滿足**容許條件** (admissibility)
$$C_\psi = \int_0^\infty \frac{|\hat{\psi}(\omega)|^2}{|\omega|}\, d\omega < \infty,$$
則訊號可由小波係數完全重建：
$$f(t) = \frac{1}{C_\psi}\int_0^\infty\int_{-\infty}^{\infty} W_f(a,b)\; \psi_{a,b}(t)\; \frac{da\,db}{a^2}.$$
$\hat{\psi}(0)=0$（零均值）即容許——**零均值是探員的入職資格**。

### 第三步：與傅立葉的對偶偵查
- 傅立葉基底 $\{e^{i\omega t}\}$：全域、正交、**無局部化**——Gibbs 過衝的根源。
- 小波基底 $\{\psi_{a,b}\}$：局部、冗餘（連續版）或正交（離散版）——**可局部化**，跳躍處無過衝。
- 多解析度分析 (MRA, Mallat 1988) 使離散小波成為正交基底：尺度函數 $\phi$ 與小波 $\psi$ 的雙尺度方程
  $$\phi(t) = \sum_k h_k \phi(2t - k), \qquad \psi(t) = \sum_k g_k \phi(2t - k).$$

### Python：Morlet 小波偵測「啾啾訊號」的時頻定位

```python
import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 1, 2000)
# 啾啾訊號：頻率隨時間上升 5→40 Hz；中段有突波
sig = np.sin(2*np.pi*(5*t + 17.5*t**2))
sig[900:920] += 3.0

def morlet(s, a, b0):
    tm = np.arange(-3*a, a*3, t[1]-t[0])
    psi = np.pi**-0.25 * np.exp(1j*6*tm/a - (tm/a)**2/2) / np.sqrt(a)
    return np.trapz(s[:len(tm)]*np.conj(psi), tm)

fig, ax = plt.subplots()
for a in [0.02, 0.05, 0.1]:
    coef = [abs(morlet(np.roll(sig, -i), a, i)) for i in range(0, 1800, 20)]
    ax.plot(range(0, 1800, 20), coef, label=f'a={a} (頻率~{np.round(6/a/2/np.pi,1)}Hz)')
ax.legend(); plt.savefig('chirp_wavelet.png', dpi=100)
print("小尺度 a=0.02 對突波最敏感，大尺度 a=0.1 對低頻主體最敏感")
```
小 $a$（高頻）精準定位突波位置，大 $a$（低頻）描繪主體趨勢——**同一時間軸、不同解析度**，STFT 做不到。

## 結案 -- 後果與影響
- **時頻分析的革命**：地震勘探、語音、醫學（心電圖、腦電圖）、影像邊緣偵測全面改寫。
- **JPEG 2000 標準**採用離散小波（取代 JPEG 的 DCT，見「1992-JPEG離散餘弦變換.md」）——小波壓縮的方塊邊界無 Gibbs 振鈴。
- Mallat 的多解析度分析（1988）與 Daubechies 的緊支撐正交小波（1988）使小波成為工程標準工具。
- 數學影響：調和分析的新分支；Daubechies 小波成為 Hilbert 空間的標準基底。
- 歷史定位：傅立葉轉換仍是「平穩訊號」之王（見「1965-FFT快速傅立葉轉換.md」）；小波是「非平穩訊號」之王——**兩者互補，而非取代**。

## 關鍵人物與文獻
- **J. Morlet & A. Grossmann**：Grossmann & Morlet, SIAM J. Math. Anal. 15, 723 (1984)。
- **Mallat**：多解析度分析, IEEE Trans. PAMI 11, 674 (1989)。
- **Daubechies**：緊支撐正交小波, Comm. Pure Appl. Math. 41, 909 (1988)。
- 相關案件：`1898-Gibbs現象定名.md`、`1992-JPEG離散餘弦變換.md`。
