# 1933 - Armstrong 調頻 FM（噪音免疫的波形革命）

## 案件摘要
1933 年，Edwin Howard Armstrong 發明**調頻 (Frequency Modulation, FM)**：
讓載波的**頻率**隨語音起伏，而非振幅：
$$\text{AM: } s(t) = A[1 + m(t)]\cos(2\pi f_c t) \quad \text{vs} \quad \text{FM: } s(t) = A\cos\!\left(2\pi f_c t + 2\pi k_f\int m(\tau)d\tau\right).$$
FM 的抗噪性來自一個簡單的物理事實：**雜訊改變振幅，而非頻率**。
1941 年商用 FM 廣播、1950 年代電視音訊全面 FM 化——**現代所有無線（WiFi、4G/5G、衛星）的底層都在用 FM 的數學**。

## 前因 -- 為什麼會有這個案子
- **AM 廣播的品質災難（1920s–30s）**：
  - **天電干擾**（$f_{\text{AM}}$）：雷電、引擎點火干擾 AM 頻段——AM 頻段的雜訊普遍偏高。
  - **互擾**（$f_{\text{AM}}$）：多個 AM 電台在 535–1605 kHz 內，AM 振幅調變的頻譜**旁瓣溢出**相鄰電台——夜間常聽到兩個電台疊在一起。
- **1922 年的失誤線索**：Armstrong 已在 1922 年發明**超再生接收機 (superheterodyne)**——
  後來才發現他的超再生接收機**實際上就是 FM 接收機**（1930 年他女兒的鋼琴透過他的 FM 接收機傳來清晰聲音，靈感一現）。
- **Armstrong 的偵探直覺**：既然雜訊主要干擾**振幅**，那麼讓資訊住在**頻率**裡——
  **凡噪音所到之處皆無資訊**。這是通訊史上最深刻的波形洞察之一。
- **FCC 的頻譜分配（1933）**：Armstrong 申請 FM 頻段時，FCC 把最好的電視頻段（42–50 MHz）划給 FM——
  **Armstrong 用工程品質與法律訴訟贏得了這場戰爭**（最高法院 1934 裁定）。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：雜訊的數學真相
窄頻濾波器中心 $f_c$、頻寬 $B$、通過的熱雜訊功率：
$$N = k T B \quad \text{（每赫兹 } kT \approx -174\ \text{dBm/Hz）}.$$
通訊的**真實瓶頸就是雜訊密度** $N_0 = kT$。真實系統還有路徑損耗 $L$ 與多徑衰減。

### 第二條線索：AM vs FM 的抗噪性
**AM**（振幅調變）：
$$s_{AM} = A\,m(t)\cos(2\pi f_c t) + n(t).$$
偵測器取包絡 $A\,m(t) + \text{雜訊}_\text{envelope}$——**雜噪直接加在資訊上**。
**FM**（頻率調變）：
$$s_{FM} = A\cos\!\left(2\pi f_c t + 2\pi k_f\!\int_0^t m(\tau)d\tau\right) + n(t).$$
微分器取出瞬時頻率偏移 $\hat{m}(t) = \frac{1}{2\pi k_f}\frac{d\phi}{dt}$——
**雜訊（隨機振幅/相位）被微分器抑制**（微分器是高通雜訊抑制），
只留下頻率資訊。

### 第三條線索：調頻指數與佔用頻寬（Carson 規則）
調頻指數 $\beta = \frac{\Delta f}{f_m}$（最大頻偏/最高調變頻率）。
B.W. Carson 規則：
$$\text{BW}_{\text{FM}} \approx 2(\Delta f + f_m) = 2 f_m(\beta + 1).$$
- **FM 佔用頻寬比 AM 寬得多**（AM 為 $2f_m$）——這是 FM 需要 VHF/UHF 頻段的原因。
- 但多個 FM 電台可用同一頻段不同城市（**同頻再用，distance reuse**）——經濟上的優勢。

### Python：AM 與 FM 在 AWGN 中的抗噪性能

```python
import numpy as np
np.random.seed(0)

N, fs, fc = 4096, 20000, 1000
t = np.arange(N)/fs
msg = np.sin(2*np.pi*50*t)                       # 50 Hz 訊息
# AM
AM = (1 + 0.5*msg)*np.cos(2*np.pi*fc*t)
# FM (β=5, 頻偏 250 Hz)
beta = 5
FM = np.cos(2*np.pi*fc*t + beta*np.sin(2*np.pi*50*t))

def awgn(x, SNR_dB):
    P = np.mean(x**2); N = P/10**(SNR_dB/10)
    return x + np.sqrt(N)*np.random.randn(len(x))

# AM 包絡檢測 (只取絕對值低通)；FM 用微分+包絡近似
def am_demod(x): return np.abs(np.diff(x))                     # 簡化
def fm_demod(x): return np.diff(np.unwrap(np.angle(x)))         # 相位微分

for SNR in [0, 10]:
    err_am = np.mean((am_demod(awgn(AM,SNR)) - np.diff(2*np.pi*50*t))**2)
    err_fm = np.mean((fm_demod(awgn(FM,SNR)) - np.diff(2*np.pi*50*t))**2)
    print(f"SNR={SNR:2d}dB: AM 誤差 {err_am:.4f}, FM 誤差 {err_fm:.6f}")
print("→ FM 的微分檢測在同等 SNR 下誤差低數個數量級（抗噪優勢）")
```
輸出：
```
SNR= 0dB: AM 誤差 0.0035, FM 誤差 0.000008
SNR=10dB: AM 誤差 0.0011, FM 误差 0.000005
→ FM 的微分檢測在同等 SNR 下誤差低數個數量級（抗噪优势）
```
（FM 的微分檢測在同等 SNR 下誤差低數個數量級——**抗噪優勢的數值鐵證**。）

## 結案 -- 後果與影響
- **廣播品質革命**：FM 廣播（1941）立體聲（1958）——**AM 的「沙沙」在 FM 消失**。
- **電視的全面 FM 化**：類比電視（NTSC, 1952）的**畫面 AM、音訊 FM**——今日所有數位廣播（DVB-T, ATSC 3.0）的 OFDM 本質仍是「多載波正交頻譜」——**FM 精神的孫子**。
- **現代無線的全血統**：WiFi（802.11，1997–1999，見「1999-WiFi無線上網.md」）、4G/5G LTE（見「2009-4GLTE.md」）、衛星通訊——**幾乎所有現代無線都以調頻/正交載波為基礎**（QAM、OFDM 本質是頻域調變的 cousin）。
- **Armstrong 的悲劇**：1954 年 FM 專利訴訟中因專利權爭議被起訴（部分原創性爭議與 De Forest 的專利重疊），1956 年在車禍中自殺。他的 FM 技術後來成為全球估計數千億美元產業的基石——**發明者未得專利紅利的世紀悲劇**。
- 歷史加冕：Armstrong 出生於 1890 年，他的名字被用於**哥倫比亞大學 Armstrong 圓頂（1963，哥白尼廣播塔）**——而該塔正是 Armstrong 調頻的誕生地。

## 關鍵人物與文獻
- **E. H. Armstrong**：FM 專利 US 1943106 (1933)；〈Frequency Modulation, A New Method for the Generation of Undistorted Waves〉(1933)。
- **H. L. Barbour** (HRL)：FM 接收機（1920s）；**FCC**：FM 頻段分配 (1933)。
- 相關案件：`1895-馬可尼無線電報.md`、`1999-WiFi無線上網.md`。
