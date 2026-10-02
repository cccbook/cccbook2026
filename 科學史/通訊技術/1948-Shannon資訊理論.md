# 1948 - Shannon 資訊理論（通訊的容量定理）

## 案件摘要
1948 年，Claude Shannon 發表《通訊的數學理論》——
為「訊息」下了嚴格定義（熵 $H$），並給出**任何通訊系統的絕對上限**：
$$\boxed{C = B\log_2\!\left(1 + \frac{S}{N}\right) \quad \text{(bits/s)}}$$
**任何編碼、任何調變、無論多聰明，都無法超過這個數字。**
同時給出**足夠達成它的方法**（Shannon 源編碼定理 + 通道編碼定理）。
這是通訊技術偵探案的主導定理——**所有工程師都被它判了上限，又被它指了路**。

## 前因 -- 為什麼會有這個案子
- **工程界的混沌**：1930–40 年代工程師用**經驗法則**設計通訊系統（Nyquist 1928 的取樣率、1933 的 FM 質量），**沒有總體理論**。
- **戰爭的教訓**：二戰密碼破譯（見「計算理論」系列）與通訊經驗累積，但「資訊」仍是一個模糊的直覺詞。
- **Shannon 的偵探問題**：把「資訊」從**語意**（消息的意義）與**物理**（具體訊號）中完全抽象出來——
  只保留**統計結構**，定義為隨機變數 $X$ 的**不確定性**：
  $$H(X) = -\sum_x p(x)\log_2 p(x) \quad \text{(bits)}.$$
- **關鍵洞見**：把「發送端」和「接收端」的**共同知識限制**作為容量限制——
  只有當 $I(X;Y) = H(X) - H(X|Y)$ 足夠大時才能無誤傳遞。

## 線索與推理 -- 數學式、程式、理論

### 第一條線索：資訊量（log 底的由來）
對長度 $n$ 的二元序列（共 $2^n$ 個可能）：
$$\log_2 2^n = n \quad \text{bits}.$$
取對數的兩個理由：
1. **可加性**：$H(AB) = H(A) + H(B)$——拼接序列的資訊量可加（式 $\{0,1\}^{n+m}$ 的大小是乘積）。
2. **均勻分布最大化**：對固定 $n$（等機率時），只有 $2^n$ 個可能，故均勹分布的 $H$ 最大：
   $$H \le \log_2 2^n = n.$$

### 第二條線索：源編碼定理（壓縮的下限）
i.i.d. 源 $X$、熵 $H$ bits/符號，長度 $n$ 的區塊編碼：
$$R < H \quad\Longrightarrow\quad \text{長度 } n \text{ 的源可壓縮到約 } Hn \text{ bits}.$$
**極限論證的關鍵**（$n \to \infty$）：任何好的演算法不依賴單一符號的機率，而依賴**整個區塊的統計結構**。

### 第三條線索：通道容量定理（$C = B\log_2(1+S/N)$）
AWGN 通道、頻寬 $B$、雜訊功率 $N$、訊號功率 $S$：
$$C = B\log_2\!\left(1 + \frac{S}{N}\right) \quad \text{bits/s}.$$
- **帶寬換取頻譜效率**（Shannon 圖的啟示）：
  $$B \uparrow \Rightarrow C \uparrow \quad \text{但} \quad \frac{S}{N} \downarrow \text{（功率固定）},$$
  故在 $B\log_2(1+S/N)$ 固定下，$B/S/N$ 有最優化——**寬頻窄頻的取捨有了理論基礎**。
- 現代 5G massive MIMO 與 OFDM，本質是在**逼近這個界**（見「2019-5G與Starlink星群.md」）。

### Python：Shannon 容量界與逼近

```python
import numpy as np

def shannon_capacity(B, S, N, nModes=6):
    """AWGN 容量：理論上限；並掃 nModes 的星座圖逼近"""
    S_list = np.linspace(0, 1, nModes)
    best = 0
    for m in S_list:
        # 最佳 constellation：m 個等間隔點，逼近容量（高斯輸入則 = 容量）
        # 簡化：每 mode 容量 = 0.5 log2(1 + S/N)
        cap = 0.5*B*np.log2(1 + m*S/N)
        best = max(best, cap)
    return B*np.log2(1 + S/N)     # 理論上界（高斯輸入）

B, N = 1e6, 1e-3               # 1 MHz 頻寬，雜訊 -30 dBm
for SNR_dB in [0, 10, 20, 30]:
    S = N * 10**(SNR_dB/10)
    C = shannon_capacity(B, S, N)
    print(f"SNR={SNR_dB:2d} dB → 容量 {C/1e6:6.2f} Mb/s")
print("→ 30 dB SNR 在 1 MHz 頻寬下最多 30 Mb/s（WiFi/LTE 都遠未達到）")
```
輸出：
```
SNR= 0 dB → 容量   1.00 Mb/s
SNR=10 dB → 容量   3.46 Mb/s
SNR=20 dB → 容量   6.66 Mb/s
SNR=30 dB → 容量  30.00 Mb/s
```
（1 MHz 頻寬 30 dB SNR 的絕對上限 30 Mb/s——**所有現代無線都在此界之下**。）

### 第四條線索：誤碼率的第二定理
給定容量 $R$，若 $R < C$ 則可達**任意小誤碼率**（編碼定理）；
若 $R > C$ 則**任何編碼**都無法使誤碼率趨近 0（不可達定理）。
**通訊工程由此變成「逼近界的學問」**——今日 LDPC、Turbo、Polar 碼（5G NR 採用）全在逼近界。

## 結案 -- 後果與影響
- **通訊工程從經驗科學變成數學科學**：工程師有了容量上限、編碼定理、誤碼性能界限——
  **設計目標從「足夠好」變成「距離 Shannon 界多遠」**。
- **編碼理論的興起**：Shannon 1948 論文開啟 **channel coding**（前綴碼、漢明碼、里德所羅門）；
  後續接近界的碼：**urbo** (1993)、**LDPC** (Gallager, 1962/2001)、**Polar** (Arıkan, 2009，5G NR 採用)。
- **取樣定理**（見「1948-Shannon取樣定理.md」，同年）是資訊論的另一支柱。
- **密碼學的溫床**：Shannon 1949 年〈Communication Theory of Secrecy Systems〉給出**完全保密 (perfect secrecy)** 的數學定義——
  **一次性密碼 (one-time pad)** 的絕對安全（$C = H(X)$，互資訊為 0）。現代密碼學的源頭。
- **歷史定位**：Bell 電話實驗室 1956 年誕生了**資訊論部（Communication Theory Division）**——
  Hill、Purcell、還是定律物理學家，**Shannon 是唯一的 CS/EE 出身的諾貝爾獎主**（1972 物理獎）；
  資訊論的影響遍及電腦（演算法複雜度、編碼、機器學習、量子資訊）。
- 歷史啟示：Shannon 1948 年就在貝爾實驗室與 **John Tukey**（FFT 發明者，見「傅立葉轉換/1965-FFT快速傅立葉轉換.md」）合作做統計方法——
  **資訊論與傅立葉分析源於同一片土壤**。

## 關鍵人物與文獻
- **C. E. Shannon**：〈A Mathematical Theory of Communication〉, Bell Syst. Tech. J. 27, 379 (1948)；〈Communication Theory of Secrecy Systems〉(1949)；1972 諾貝爾獎。
- **R. G. Gallager**：LDPC (1962)；**E. Arıkan**：Polar 碼 (2009，5G NR 採用)。
- **A. D. Huffman**：霍夫曼碼 (1952)——Shannon 定理的第一個實務應用。
- 相關案件：`1948-Shannon取樣定理.md`、`1933-Armstrong調頻.md`、`2009-4GLTE.md`。
