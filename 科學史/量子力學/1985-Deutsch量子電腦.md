# 1985 - Deutsch 量子電腦

## 案件摘要
Feynman 說「用量子系統模擬量子系統」，但那只是模擬器。1985 年 David Deutsch 提出通用量子電腦：一台能執行任何可量子計算任務的機器，並發明第一個展現量子加速的演算法（Deutsch–Jozsa 的前身）。量子電腦從構想變成正式計算模型。

## 前因 -- 為什麼會有這個案子
- 1982 年 Feynman 提出量子模擬構想，Benioff 提出量子圖靈機，但兩者都未回答：「量子電腦能算什麼經典電腦算不了的東西？」
- Church–Turing 假設說所有可計算函數都等價於圖靈機可計算；Deutsch 的挑戰是「物理版的 Church–Turing 原理」：應以物理系統的實際可計算性來定義計算。
- **多世界詮釋對 Deutsch 的影響**：Deutsch 是 Everett 多世界詮釋的堅定信徒。在他看來，量子疊加的每個分支都真實存在；量子計算的力量正來自「計算在多個平行分支中同時進行，最後干涉合併」。他明言量子計算理論的動機之一是為多世界詮釋提供可檢驗的實證基礎。

## 線索與推理 -- 數學式、程式、理論

### 量子圖靈機
Deutsch 將圖靈機量子化：計算帶狀態、讀寫頭、內部狀態全部由么正演化 $U$ 取代經典轉移函數。並證明存在**通用量子圖靈機** $U_T$，可模擬任何量子圖靈機——量子計算有了嚴格的計算模型。

### 量子閘模型（電路模型，今日的標準形式）
計算在 $n$ 個量子位元的 Hilbert 空間（$\dim = 2^n$）中，由一系列么正閘完成：

**Hadamard 閘**（製備疊加）：

$$H = \frac{1}{\sqrt{2}}\begin{pmatrix}1&1\\1&-1\end{pmatrix}, \quad H|0\rangle = \frac{|0\rangle+|1\rangle}{\sqrt2}, \quad H|1\rangle = \frac{|0\rangle-|1\rangle}{\sqrt2}$$

**CNOT 閘**（糾纏）：

$$\text{CNOT} = \begin{pmatrix}1&0&0&0\\0&1&0&0\\0&0&0&1\\0&0&1&0\end{pmatrix}, \quad |x,y\rangle \to |x, y \oplus x\rangle$$

**相位閘**（$S, T$ 閘，控制複數相位）：

$$S = \begin{pmatrix}1&0\\0&i\end{pmatrix}, \quad T = \begin{pmatrix}1&0\\0&e^{i\pi/4}\end{pmatrix}$$

### 通用量子閘集合
{H, T, CNOT}（或 {H, S, CNOT} 加任意單位元旋轉的近似）是**萬能閘集合**：任何 $n$ 量子位元么正算符 $U$ 都可被分解為這些閘的乘積（Solovay–Kitaev 定理保證近似效率）。qiskit 風格偽碼：

```python
from qiskit import QuantumCircuit

qc = QuantumCircuit(2)
qc.h(0)        # Hadamard: 疊加
qc.cx(0, 1)    # CNOT: 糾纏 -> Bell 態
qc.t(0)        # 相位閘: 任意么正的基本元件
print(qc)
```

### Deutsch–Jozsa 演算法（1992，Deutsch 1985 單位元版之推廣）
問題：黑箱函數 $f: \{0,1\}^n \to \{0,1\}$ 保證是「常數」（全 0 或全 1）或「平衡」（恰好一半為 1）。判斷是哪一種。

- 經典：最壞要查 $2^{n-1}+1$ 次。
- 量子：**只查 1 次**。流程：
  1. $|0\rangle^{\otimes n}|1\rangle \xrightarrow{H^{\otimes n} \otimes H} \frac{1}{\sqrt{2^n}}\sum_x |x\rangle \cdot \frac{|0\rangle-|1\rangle}{\sqrt2}$
  2. 一次 oracle 呼叫：$|x\rangle \to (-1)^{f(x)}|x\rangle$（相位反轉）
  3. $H^{\otimes n}$ 干涉
  4. 測量：全 0 ⟹ 常數，否則 ⟹ 平衡

這是第一個「指數 vs 常數」分離的量子演算法，證明量子計算有本質優勢。

### Python 模擬 Deutsch–Jozsa（numpy）

```python
import numpy as np

n = 3
N = 2**n

def oracle(f, dim):
    U = np.diag([(-1)**f(x) for x in range(dim)])
    return U

H1 = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
Hn = np.eye(1, dtype=complex)
for _ in range(n):
    Hn = np.kron(Hn, H1)

f_constant = lambda x: 0
f_balanced = lambda x: x.bit_count() % 2

def dj(f):
    psi = np.zeros(N, dtype=complex); psi[0] = 1
    psi = Hn @ psi                                # 疊加
    psi = oracle(f, N) @ psi                      # 一次 oracle
    psi = Hn @ psi                                # 干涉
    return abs(psi[0])**2 > 0.99                  # 測到全 0 ?

print("constant -> 常數?", dj(f_constant))   # True
print("balanced -> 常數?", dj(f_balanced))   # False
```

## 結案 -- 後果與影響
- 量子閘模型（+ 1993 年 Yao 證明量子閘電路等價於量子圖靈機）成為整個量子計算領域的標準語言，今天的 qiskit、Cirq 都建立其上。
- Deutsch–Jozsa 開啟量子演算法序列：1993 Bernstein–Vazirani、1994 Simon 演算法（直接啟發 Shor）、1994 Shor、1996 Grover。
- 萬能閘集合 + 糾錯碼（1994 年後）構成「可容錯量子計算」的理論基石，使建造大型量子電腦在原理上可行。
- 多世界詮釋因 Deutsch 而在物理/哲學圈重新活躍；他 1997 年《The Fabric of Reality》把量子計算作為多世界的論證核心。
- Deutsch 與 Feynman 並列為量子電腦之父：Feynman 給了動機，Deutsch 給了模型。

## 關鍵人物與文獻
- **David Deutsch**（1953– ），英國牛津大學。
- Deutsch, D., "Quantum Theory, the Church–Turing Principle and the Universal Quantum Computer", *Proc. R. Soc. Lond. A* **400**, 97 (1985)。
- Deutsch, D. & Jozsa, R., "Rapid solution of problems by quantum computation", *Proc. R. Soc. Lond. A* **439**, 553 (1992)。
- Deutsch, D., *The Fabric of Reality* (1997)。
- Yao, A., "Quantum circuit complexity", FOCS (1993)。
- Nielsen & Chuang, *Quantum Computation and Quantum Information* (2000)。
