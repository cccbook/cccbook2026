# 1996-Grover 演算法

## 案件摘要
1996 年，AT&T 實驗室的 Lov Grover 在費米實驗室的一場研討會上宣布：量子電腦可以在 $O(\sqrt{N})$ 時間內於非結構化資料庫中找到目標項。偵探注意到，這個加速雖然不如 Shor 演算法的指數級，卻適用於「所有」搜尋問題——線索指向「振幅放大」的幾何結構。

## 前因 -- 為什麼會有這個案子
- 1994 年 Shor 提出質因數分解演算法，證明量子電腦在某些問題上有指數優勢，但僅限特定代數結構。
- 經典上，在一個毫無結構（亂序、無索引）的 $N$ 項資料庫中找一個特定項，平均需要 $N/2$ 次、最壞需要 $N$ 次查詢。資訊論上，每查一次只能得到 1 bit 的「是/否」資訊。
- Bennett 等人（1994）指出：即使把查詢函數 $f(x)$ 變成量子 oracle（一次可對疊加態的所有 $x$ 同時求值），也不能直接「平行讀出」所有答案——量測會坍縮。問題變成：如何讓答案的振幅被「放大」到可測得？
- 這就是本案的謎題：oracle 已經給出，答案藏在振幅裡，如何把它挖出來？

## 線索與推理 -- 數學式、程式、理論
### 問題定義
給定 $N = 2^n$ 個項與一個布林函數 $f$，恰有一個解 $w$ 使得 $f(w)=1$。Oracle 定義為

$$O_f|x\rangle = (-1)^{f(x)}|x\rangle$$

（相位 oracle，將解的振幅反相）。

### Grover 迭代
從均勻疊加態出發：

$$|s\rangle = \frac{1}{\sqrt{N}}\sum_{x=0}^{N-1}|x\rangle$$

Grover 迭代 $G$ 由兩個算符組成：

$$G = (2|s\rangle\langle s| - I)\, O_f$$

其中 $D = 2|s\rangle\langle s| - I = \frac{2}{N}\sum_{x}\sum_{y}|x\rangle\langle y| - I$ 稱為 **diffusion 算符**（關於平均值的反轉，inversion about the mean）：對任意振幅 $a_i$，它將其映射為 $2\bar{a} - a_i$。

### 幾何直覺
把狀態分解為「解平面」上的兩個分量：

$$|s\rangle = \sin\theta\,|w\rangle + \cos\theta\,|r\rangle,\quad \sin\theta = \frac{1}{\sqrt{N}}$$

其中 $|r\rangle$ 是所有非解態的歸一化疊加。每次迭代 $G$ 在 $\{|w\rangle, |r\rangle\}$ 平面上旋轉 $2\theta$ 角度，把振幅從 $|r\rangle$ 搬向 $|w\rangle$。經過 $k$ 次迭代：

$$\sin\big((2k+1)\theta\big) \approx \text{成功機率}$$

取 $k \approx \frac{\pi}{4}\sqrt{N}$ 時成功機率接近 1，故查詢次數為 $O(\sqrt{N})$。

例如 $N = 2^{20} \approx 10^6$：經典需約 $5\times 10^5$ 次查詢，Grover 只需約 $\frac{\pi}{4}\cdot 1024 \approx 805$ 次。

### 最優性證明
Bennett–Bernstein–Brassard–Vazirani（BBBV, 1997）用混合態論證證明：任何量子演算法搜尋非結構化資料庫至少需要 $\Omega(\sqrt{N})$ 次 oracle 查詢。因此 Grover 是**漸近最優**的——加速最多是二次方，不可能更快。後續 Zalka（1999）更證明常數因子 $\pi/4$ 也是最優的。

### 4 量子位 Grover 模擬（Python/qiskit 風格偽碼）
```python
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import numpy as np

n, target = 4, 13          # N=16, 找 |1101>

def oracle(qc):
    # 對 |1101> 反相：X 翻轉 0 位元，MCZ 反相，再翻回
    for q in range(n):
        if (target >> q) & 1 == 0:
            qc.x(q)
    qc.h(3); qc.mcx([0,1,2], 3); qc.h(3)
    for q in range(n):
        if (target >> q) & 1 == 0:
            qc.x(q)

def diffusion(qc):
    for q in range(n): qc.h(q)
    for q in range(n): qc.x(q)
    qc.h(3); qc.mcx([0,1,2], 3); qc.h(3)
    for q in range(n): qc.x(q)
    for q in range(n): qc.h(q)

qc = QuantumCircuit(n, n)
qc.h(range(n))             # 均勻疊加 |s>
k = int(np.floor(np.pi/4 * np.sqrt(2**n)))   # k=3
for _ in range(k):
    oracle(qc)
    diffusion(qc)
qc.measure(range(n), range(n))

sim = AerSimulator()
result = sim.run(transpile(qc, sim), shots=1024).result()
print(result.get_counts()) # |1101> 出現機率 > 0.95
```

## 結案 -- 後果與影響
- **振幅放大（amplitude amplification）成為通用量子技術**：Grover 迭代可推廣為 Brassard–Høyer–Mossard–Tapp 的振幅放大框架，用於量子計數、碰撞問題、NP 完全問題的平方加速。
- 複雜度 $O(\sqrt{N})$ vs 經典 $O(N)$：對 hash 碰撞、 satisfiability 等問題提供實質（但非指數）加速。
- 深遠影響：Grover 演算法迫使對稱式密碼學加倍金鑰長度（AES-128 在量子攻擊下安全度只剩約 64 bit），成為後量子密碼學討論的起點之一；今日所有量子雲端平台上的入門教材，幾乎都以 Grover 作為第二個示範電路。

## 關鍵人物與文獻
- Lov K. Grover, *A fast quantum mechanical algorithm for database search*, Proc. STOC 1996, pp. 212–219.
- Bennett, Bernstein, Brassard, Vazirani, *Strengths and weaknesses of quantum computing*, SIAM J. Comput. 26(5), 1997（最優性下界）.
- Christof Zalka, *Grover's quantum searching algorithm is optimal*, Phys. Rev. A 60, 1999.
- Brassard, Høyer, Mosca, Tapp, *Quantum Amplitude Amplification and Estimation*, 2002.
