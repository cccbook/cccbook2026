# 1982 - Feynman 量子電腦構想

## 案件摘要
1982 年 Feynman 在 MIT「Physics of Computation」會議上指出：經典電腦模擬量子系統需要指數級資源，本質上做不到。他的解藥是驚人的一句話——「用量子系統模擬量子系統」。這篇演講是量子電腦的誕生證明。

## 前因 -- 為什麼會有這個案子
- 1970 年代末，計算機科學家開始追問：物理定律對「什麼可以被計算」設了什麼限制？（Church–Turing 假設：任何可計算的都可被圖靈機計算。）
- Landauer、Bennett 等人研究計算的物理極限（可逆計算），為「物理之於計算」的思路鋪路。
- 同時，化學家與物理學家深知：即使是小型分子（如含數十個電子），Schrödinger 方程式的精確數值解也遠超當時（與現在）的經典電腦能力。
- Benioff 1980 年提出量子力學的圖靈機模型，但只是「用離散力學系統模擬經典計算」，尚未發揮量子特性。Feynman 更進一步：量子模擬需要量子硬體。

## 線索與推理 -- 數學式、程式、理論

### 指數爆炸：經典模擬的天文數字
$n$ 個自旋 1/2 粒子的態空間維度為

$$\dim = 2^n$$

$n$ 個電子的 Hilbert 空間維度更以場模數成長。描述一般量子態需要 $2^n$ 個複數振幅：$n=50$ 時 $2^{50} \approx 10^{15}$（petabyte 級），$n=300$ 時 $2^{300}$ 已超過可觀測宇宙的原子數（$\approx 10^{80}$）。跟蹤量子演化的時間複雜度同樣指數級。

Feynman 的觀察：**大自然不是經典的，硬要用經典方式模擬它，代價是指數爆炸。**

### Feynman 論證：用量子模擬量子
他的提案：建造一台本身服從量子力學的機器，讓它的 Hilbert 空間直接「扮演」目標系統的 Hilbert 空間：

$$\text{模擬器狀態 } |\psi_{sim}(t)\rangle = U_{sim}(t)|\psi_{sim}(0)\rangle \longleftrightarrow \text{目標系統 } |\psi_{target}(t)\rangle$$

資源需求從指數降為多項式：模擬 $n$ 個自旋只需 $n$ 個（或 $O(n)$ 個）量子位元。Feynman 進一步論證：通用量子系統可以有效率地模擬**任何**局域交互作用的量子系統。

### 量子位元與 Hilbert 空間
單一量子位元：

$$|\psi\rangle = \alpha|0\rangle + \beta|1\rangle, \quad |\alpha|^2 + |\beta|^2 = 1$$

$n$ 個量子位元的疊加態：

$$|\Psi\rangle = \sum_{x \in \{0,1\}^n} c_x |x\rangle, \quad \sum_x |c_x|^2 = 1$$

一般態的參數量 $\sim 2^{n+1}$，量子硬體「天然」存在於這個 $2^n$ 維 Hilbert 空間中——這正是模擬力的來源。

### 現代發展：量子模擬的落地
- **VQE（Variational Quantum Eigensolver, 2014）**：量子電腦製備試探態 $|\psi(\theta)\rangle$、測量能量 $\langle\psi(\theta)|H|\psi(\theta)\rangle$，古典最佳化器更新 $\theta$，逼近分子基態能量：

$$E_0 \leq \min_\theta \langle\psi(\theta)| H |\psi(\theta)\rangle$$

- **量子化學**：模擬 $\mathrm{H}_2$、$\mathrm{LiH}$、$\mathrm{BeH}_2$ 等分子；未來目標包括固氮酶（FeMoco）與高溫超導機制。
- **類比量子模擬器**：冷原子光晶格、離子阱直接仿真自旋/Hubbard 模型，是 Feynman 原始構想最直接的實現。
- qiskit 風格偽碼（單自旋演化 $\exp(-i Z t)$）：

```python
from qiskit import QuantumCircuit
import numpy as np

t = 0.7
qc = QuantumCircuit(1)
qc.h(0)                      # 製備 (|0>+|1>)/sqrt(2)
qc.rz(2*t, 0)                # exp(-i*Z*t) 的閘實作
print(qc)                    # n 個量子位元 => 2^n 維 Hilbert 空間
```

## 結案 -- 後果與影響
- 1985 年 Deutsch 提出通用量子電腦的嚴格模型（見另篇），把 Feynman 的直覺形式化。
- 1994 年 Shor 演算法證明量子電腦有實際殺傷力（分解質因數），資金湧入。
- 量子模擬至今仍是量子電腦最可信的近期應用：量子化學、材料科學、量子場論模擬。
- Feynman 的挑戰也反向催生了「量子複雜度理論」：BQP 類別（量子多項式時間）成為與 P、NP 並列的基本類別。
- 演講的格言流傳至今：「Nature isn't classical, dammit, and if you want to make a simulation of nature, you'd better make it quantum mechanical.」

## 關鍵人物與文獻
- **Richard P. Feynman**（1918–1988），1965 諾貝爾物理獎得主。
- Feynman, R. P., "Simulating Physics with Computers", *International Journal of Theoretical Physics* **21**, 467 (1982)（MIT 會議演講）。
- Benioff, P., "The computer as a physical system...", *J. Stat. Phys.* **22**, 563 (1980)。
- Peruzzo et al., "A variational eigenvalue solver on a photonic quantum processor", *Nat. Commun.* **5**, 4213 (2014)（VQE）。
- Nielsen & Chuang, *Quantum Computation and Quantum Information* (2000)。
