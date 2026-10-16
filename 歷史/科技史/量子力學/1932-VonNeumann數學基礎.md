# 1932 — Von Neumann《量子力學的數學基礎》

## 案件摘要
1932 年，數學家 John von Neumann 出版《Mathematical Foundations of Quantum Mechanics》（德文原版 *Mathematische Grundlagen der Quantenmechanik*）。他偵破了一樁懸案：量子力學的數學「地基」究竟是什麼？答案是 Hilbert 空間上的算符理論，並附帶一份震驚學界的「隱變數不可行」證明——這份證明日後被 Bell 抓出漏洞。

## 前因 -- 為什麼會有這個案子
- 1925–1926 年，量子力學出現兩套「犯罪現場」截然不同卻給出同樣結論的表述：
  - Heisenberg 的**矩陣力學**：無窮維矩陣、非對易性。
  - Schrödinger 的**波動力學**：波函數 $\psi(x)$、微分方程。
- Dirac（1930《Quantum Mechanics》初版）用 $\delta$ 函數與抽象記號統一兩者，但 $\delta$ 函數在數學上「不合法」（不是真正的函數）。
- 數學家不滿意：物理學家用的「無窮維矩陣」何時可對角化？「本徵函數完備性」在什麼條件下成立？von Neumann 決定以嚴格的**算符理論**重建整座大廈。

## 線索與推理 -- 數學式、程式、理論

### 1. 舞台：Hilbert 空間 $\mathcal{H}$
量子態是複內積空間 $\mathcal{H}$ 中的向量。內積 $\langle \phi | \psi \rangle$ 滿足完備性（Cauchy 序列收斂於空間內）。

> 理論定義：$\mathcal{H}$ 為完備複內積空間；量子系統的純態是射影空間 $\mathbb{P}(\mathcal{H})$ 的一點（全域相位不可觀測）。

### 2. 狀態向量與 Dirac 記號
von Neumann 原本用元素記號 $\psi \in \mathcal{H}$；Dirac 的 bra–ket 記號則把內積「拆開」：

$$|\psi\rangle \in \mathcal{H}, \qquad \langle \psi| = (|\psi\rangle)^\dagger, \qquad \langle \phi | \psi \rangle \in \mathbb{C}$$

Dirac 記號的威力在於可以「推廣」到連續譜與廣義本徵態（rigged Hilbert space 的前身）：

$$\int |x\rangle\langle x| \, dx = I, \qquad \langle x | x' \rangle = \delta(x - x')$$

von Neumann 證明：在 $\mathcal{H}$ 內部這些式子可改寫為**譜測度**（spectral measure）的嚴格形式，$\delta$ 函數的非法性被繞過。

### 3. 觀測算符與譜定理
物理可觀測量對應到 **self-adjoint（自伴）算符** $\hat{A} = \hat{A}^\dagger$。譜定理保證：

$$\hat{A} = \int \lambda \, dE(\lambda)$$

其中 $E(\lambda)$ 是投影值測度（PVM）。對離散譜：$\hat{A} = \sum_n a_n |n\rangle\langle n|$。
非對易性是核心線索：

$$[\hat{x}, \hat{p}] = i\hbar \, I \implies \Delta x \, \Delta p \geq \frac{\hbar}{2}$$

von Neumann 嚴格證明 Heisenberg 測不準原理是此對易關係的必然推論。

### 4. 測量公理（投影公設）
- 測量前：狀態 $|\psi\rangle$。
- 測量 $\hat{A}$ 得到本徵值 $a_n$ 的機率為 $|\langle a_n | \psi \rangle|^2$（Born 法則）。
- 測量後（投影公設 / collapse）：狀態坍縮為 $|a_n\rangle$。
- 期望值：$\langle \hat{A} \rangle = \langle \psi | \hat{A} | \psi \rangle$。

### 5. 密度矩陣：von Neumann 的獨門發明
純態：$\rho = |\psi\rangle\langle\psi|$，滿足 $\rho^2 = \rho$、$\mathrm{Tr}\,\rho = 1$。
混合態：$\rho = \sum_i p_i |\psi_i\rangle\langle\psi_i|$，此時 $\rho^2 \neq \rho$。

演化方程（von Neumann equation）：

$$i\hbar \frac{d\rho}{dt} = [\hat{H}, \rho]$$

熵的定義至今仍以他命名：

$$S(\rho) = -k_B \, \mathrm{Tr}(\rho \ln \rho)$$

純態 $S=0$；混合態 $S>0$。密度矩陣日後成為量子資訊、量子統計力學的基石。

### 6. 隱變數「不可行」證明（含致命漏洞）
von Neumann 證明：不存在「隱變數理論」能重現量子力學的統計預測。推理骨架：

1. 假設存在隱變數 $\lambda$，使每個觀測量有確定值 $v_\lambda(\hat{A})$。
2. von Neumann 要求線性：$v_\lambda(\alpha \hat{A} + \beta \hat{B}) = \alpha v_\lambda(\hat{A}) + \beta v_\lambda(\hat{B})$。
3. 但若 $\hat{A}, \hat{B}$ 不對易，取 $\hat{A} = \sigma_x, \hat{B} = \sigma_y$，則 $\sigma_z^2$ 之類的組合會導出矛盾（如 $v_\lambda(\sigma_z^2) = 1$ 卻被線性要求逼成負值）。
4. 故隱變數不存在。

**漏洞**（Bell 1966 指出）：線性要求對「對易」的組合量是自然的，但對「不對易」的組合量，隱變數理論根本不必滿足——因為兩者無法同時測量。此假設過強，證明因此失效。1952 年 Bohm 構造出成功的隱變數模型，更直接戳破結論。這是偵探史上的經典教訓：**前提太強，證明再漂亮也是冤案**。

### 7. 程式碼範例：驗證密度矩陣性質
```python
import numpy as np

# 純態 |psi> = (|0> + i|1>)/sqrt(2)
psi = np.array([1, 1j]) / np.sqrt(2)
rho_pure = np.outer(psi, psi.conj())

# 混合態：50% |0> + 50% |1>
rho_mix = 0.5 * np.outer([1, 0], [1, 0].conj()) + \
          0.5 * np.outer([0, 1], [0, 1].conj())

def entropy(rho):
    vals = np.linalg.eigvalsh(rho)
    vals = vals[vals > 1e-12]
    return -np.sum(vals * np.log(vals))

print("pure rho^2 == rho:", np.allclose(rho_pure @ rho_pure, rho_pure))  # True
print("mixed rho^2 == rho:", np.allclose(rho_mix @ rho_mix, rho_mix))    # False
print("S(pure) =", entropy(rho_pure))  # ~0
print("S(mixed) =", entropy(rho_mix))  # ln 2
```

## 結案 -- 後果與影響
- **結案**：量子力學的數學基礎定為 Hilbert 空間上的 self-adjoint 算符理論；Dirac 的記號被「合法化」並推廣，兩套表述（矩陣/波動）正式統一。
- von Neumann 熵成為量子熱力學與量子資訊理論的出發點。
- 密度矩陣是今日量子計算（OpenQASM、Qiskit 的 statevector/density_matrix 模擬）的數學核心。
- 隱變數冤案刺激了 1952 Bohm 理論、1964 Bell 不等式、1970s CHSH 實驗，最終證實：量子力學確實**非局域**——但這是與 von Neumann 的論證不同的、更深刻的非局域性。
- von Neumann 算符代數後來發展為 C*-代數與算符代數（Alice/Faddeev 學派），是數學物理的標準語言。

## 關鍵人物與文獻
| 人物 | 角色 |
|---|---|
| John von Neumann | 偵探，Hilbert 空間形式化、密度矩陣、隱變數證明 |
| Paul Dirac | 提供記號與 $\delta$ 函數工具（被合法化） |
| David Bohm | 1952 構造隱變數模型，反證 |
| John Bell | 1966 指出線性假設漏洞 |

**文獻**
- J. von Neumann, *Mathematische Grundlagen der Quantenmechanik*, Springer (1932)；英譯 *Mathematical Foundations of Quantum Mechanics*, Princeton Univ. Press (1955).
- J. S. Bell, "On the Problem of Hidden Variables in Quantum Mechanics", *Rev. Mod. Phys.* **38**, 447 (1966).
- P. A. M. Dirac, *The Principles of Quantum Mechanics*, Oxford (1930).
