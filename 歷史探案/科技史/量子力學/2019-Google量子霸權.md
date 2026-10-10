# 2019-Google 量子霸權

## 案件摘要
2019 年 10 月，Google 團隊在 Nature 發表論文，宣稱其 53 量子位元 Sycamore 處理器以 200 秒完成「隨機電路取樣」，而最強經典超級電腦需 1 萬年——首次宣稱達成 **quantum supremacy**（量子霸權）。偵探發現，這場結案立即被 IBM 反駁為「2.5 天」——本案的真正遺產是「量子霸權 vs 量子優勢」的概念釐清。

## 前因 -- 為什麼會有這個案子
- 2012 年 John Preskill 提出「quantum supremacy」一詞：找一個「量子電腦能做到、經典電腦（在合理時間內）做不到」的任務，證明量子優勢的存在性。
- 為何不直接用有用的問題（如 Shor 分解大整數）？因為那需要數百萬個物理量子位元與容錯糾錯，遠超當年硬體能力。
- 2011 年 Aaronson–Arkhipov 提出的 BosonSampling 與 2017 年隨後的 random circuit sampling，成為「計算複雜度上有理論依據的取樣任務」候選。
- Google 自 2014 年起布局超導量子位元，2017 年 Bristlecone（72 量子位元）後，目標明確指向隨機電路取樣實驗。
- 任務選擇的偵探邏輯：隨機電路沒有結構、難以被經典模擬「取巧」，但對量子硬體而言只是「跑自己的本行」。

## 線索與推理 -- 數學式、程式、理論
### 隨機電路取樣任務
給定一個由隨機選擇的單量子位元門（$\sqrt{X}, \sqrt{Y}, \sqrt{W}$）與交錯的雙量子位元門（iSWAP/CZ）構成的深度 $d$ 電路 $U$，作用於 $n$ 個量子位元。任務：從輸出分佈

$$P(x) = |\langle x|U|0^n\rangle|^2$$

中取樣 $N_s$ 個位元串 $x$。經典模擬需儲存 $2^n$ 維狀態向量（$n=53$ 時約 $2^{53} \approx 9\times10^{15}$ 個複數，數百 PB），取樣極為昂貴。

### Sycamore 電路與交叉熵基準
Sycamore：53 個（共 54 個，其中 1 個故障）可調耦合 transmon 量子位元，2D 方格拓樸，門深度 $d = 20$，總計約 $10^3$ 個雙量子位元閘。

**交叉熵基準（Cross-Entropy Benchmarking, XEB）**：定義

$$F_{\mathrm{XEB}} = N_s\sum_{i=1}^{N_s}|\langle x_i|U|0^n\rangle|^2 - 1 = \langle N\,P(x_i)\rangle - 1$$

- 若取樣來自均匀分佈：$F_{\mathrm{XEB}} \approx 0$。
- 若取樣來自理想量子分佈：$F_{\mathrm{XEB}} \to$ 電路深度相關的上限（約 0.0024，隨深度衰減）。

Google 的實驗結果：$F_{\mathrm{XEB}} = 0.0024$（考慮誤差後），宣稱與理想量子模擬一致，而經典模擬無法在合理時間達到。

### 200 秒 vs 1 萬年 vs 2.5 天
- Google 宣稱：Summit 超級電腦（200 PFLOPS）需 **1 萬年** 才能完成同任務。
- **IBM 反駁**（論文發表當天）：IBM 認為經典模擬可利用磁碟儲存與 Schrödinger–Feynman 混合演算法，在 **2.5 天** 內完成，且「量子霸權」的定義不應被如此輕易宣告。
- 偵探的判斷：即使 2.5 天 vs 200 秒，仍約有 1000 倍的差距，量子優勢的存在性大體被支持；但「1 萬年」的宣稱被證明是對經典演算法進步速度的低估。
- 後續（2021–2022）中國與美國團隊進一步用張量網路改進，把經典模擬時間壓到數小時甚至更短，顯示這場競賽是動態的。

### 量子霸權 vs 量子優勢
- **Quantum supremacy（量子霸權/量子至上）**：證明量子電腦在某個（哪怕無用的）任務上超越經典，純粹是計算複雜度存在性證明。
- **Quantum advantage（量子優勢/量子實用）**：量子電腦在「有實際用處」的問題上超越經典。2020 年代初的共識是：2019 年達成 supremacy，quantum advantage 仍待容錯時代。
- 因霸權一詞的政治敏感性（「supremacy」的英文含義），學界漸改用「quantum advantage」或「computational advantage」。

### 簡化模擬（Python 偽碼）
```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

n, depth = 8, 12   # 真實實驗 n=53，此處縮小示範
rng = np.random.default_rng(42)

qc = QuantumCircuit(n)
for d in range(depth):
    for q in range(n):                      # 隨機單量子位元門
        qc.append(rng.choice(['sx','sy','w']) and
                  __import__('qiskit.circuit.library', fromlist=['SXGate']).SXGate(), [q])
    for q in range(0, n-1, 2):              # 交錯雙量子位元門
        qc.cz(q, q+1)

sv = Statevector(qc)
probs = np.abs(sv.data)**2

# XEB：對量子分佈取樣後計算
samples = rng.choice(2**n, size=1000, p=probs/probs.sum())
F_xeb = len(samples) * np.mean(probs[samples]) - 1
print(F_xeb)    # 接近量子理論上限（遠 > 0）
```

## 結案 -- 後果與影響
- **量子霸權的存在性大體被確立**：即使經典模擬時間被大幅壓縮，Sycamore 實驗仍被廣泛視為量子計算的里程碑。
- **競賽動態化**：經典演算法（張量網路、GPU 模擬）持續追趕，顯示 supremacy 宣稱必須動態看待。
- **後續發展**：2020 年 12 月中國潘建偉團隊的「九章」（Jiuzhang）用光學 BosonSampling 宣稱霸權；2021 年「祖沖之號」用超導電路跟進；2023 年 IBM、Google、Quantinuum 各有新進展。
- 深遠影響：各國政府大幅增加量子科技預算（美國 NQI Act 2018、中國多個國家級計畫）；「quantum advantage」成為 2020 年代量子產業的關鍵 KPI。

## 關鍵人物與文獻
- Frank Arute et al. (Google AI Quantum), *Quantum supremacy using a programmable superconducting processor*, Nature 574, 505–510 (2019).
- Edwin Pednault, John Gunnels, et al. (IBM), *On "Quantum Supremacy"*, IBM Research Blog (2019/10/21).
- Scott Aaronson, Alex Arkhipov, *The computational complexity of linear optics*, Proc. STOC 2011.
- John Preskill, *Quantum Computing in the NISQ era and beyond*, Quantum 2, 79 (2018).
- 潘建偉團隊, *Quantum computational advantage using photons*, Science 370, 1460 (2020)（九章）.
